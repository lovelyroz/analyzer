"""Read-only preflight checks for approved MarketDaily and FX artifacts."""
from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from src.ingestion.fx.adapter import parse_fx_xlsx


MARKET_REQUIRED = ("J-Date", "Ticker", "Close", "Volume", "No", "Value")
FX_DATE_HEADERS = ("تاریخ", "تاريخ")
FX_SELL_HEADERS = ("فروش (ریال)", "فروش(ریال)", "فروش")
NUMERIC_MARKET = ("Close", "Volume", "No", "Value")
UNKNOWN = "UNKNOWN"


def artifact_identity(path: Path) -> dict[str, Any]:
    resolved = path.expanduser().resolve(strict=True)
    if not resolved.is_file():
        raise ValueError(f"not a regular file: {resolved}")
    h = hashlib.sha256()
    with resolved.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(chunk)
    return {"path": str(resolved), "sha256": h.hexdigest(), "size_bytes": resolved.stat().st_size,
            "file_type": resolved.suffix.lower().lstrip("."), "worksheet_names": []}


def _jalali(value: Any) -> bool:
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value.strip()):
        return False
    y, m, d = map(int, value.strip().split("-"))
    if y < 1 or not 1 <= m <= 12 or d < 1:
        return False
    limit = 31 if m <= 6 else 30 if m <= 11 else (30 if _jalali_leap(y) else 29)
    return d <= limit


def _jalali_leap(year: int) -> bool:
    """Jalaali break-year cycle; returns whether Esfand has 30 days."""
    breaks = (-61, 9, 38, 199, 426, 686, 756, 818, 1111, 1181, 1210,
              1635, 2060, 2097, 2192, 2262, 2324, 2394, 2456, 3178)
    if year < breaks[0] or year >= breaks[-1]:
        return False
    jp, leap_j, jump = breaks[0], -14, 0
    for jm in breaks[1:]:
        jump = jm - jp
        if year < jm:
            break
        leap_j += (jump // 33) * 8 + ((jump % 33) // 4)
        jp = jm
    n = year - jp
    leap_j += (n // 33) * 8 + (((n % 33) + 3) // 4)
    if jump % 33 == 4 and jump - n == 4:
        leap_j += 1
    leap_g = ((year + 621) // 4) - ((((year + 621) // 100 + 1) * 3) // 4) - 150
    _march = 20 + leap_j - leap_g
    if jump - n < 6:
        n = n - jump + ((jump + 4) // 33) * 33
    leap = ((n + 1) % 33 - 1) % 4
    if leap == -1:
        leap = 4
    return leap == 0


def _number(value: Any, *, positive: bool = False, integer: bool = False) -> bool:
    if value is None or isinstance(value, bool):
        return False
    raw = str(value).strip().replace(",", "")
    if not raw:
        return False
    try:
        n = Decimal(raw)
        return n.is_finite() and (not positive or n > 0) and (not integer or n == n.to_integral_value())
    except (InvalidOperation, ValueError):
        return False


def _status(issues: list[dict[str, str]]) -> str:
    if any(i["severity"] == "BLOCKED" for i in issues): return "BLOCKED"
    if any(i["severity"] == "FAIL" for i in issues): return "FAIL"
    if issues: return "WARNING"
    return "PASS"


def _issue(issues: list, severity: str, code: str, message: str) -> None:
    issues.append({"severity": severity, "code": code, "message": message})


def _provenance(source_identity: str, publication_identity: str) -> dict:
    return {"source_identity": source_identity,
            "source_publication_identity": publication_identity,
            "artifact_identity": "SHA-256 identifies byte equality only",
            "revision_identity": UNKNOWN,
            "source_published_at": UNKNOWN, "source_available_at": UNKNOWN,
            "ingested_at": "NOT_INGESTED"}


def validate_market(path: Path) -> dict:
    ident = artifact_identity(path)
    issues: list[dict[str, str]] = []
    try:
        with Path(ident["path"]).open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.reader(f)
            all_rows = list(reader)
        headers = all_rows[0] if all_rows else []
        records = [(line, row) for line, row in enumerate(all_rows[1:], 2) if row != []]
    except (UnicodeError, csv.Error) as exc:
        headers, records = [], []
        _issue(issues, "FAIL", "CSV_READ_ERROR", str(exc))
    absent = [h for h in MARKET_REQUIRED if h not in headers]
    if absent: _issue(issues, "FAIL", "MISSING_REQUIRED_FIELDS", f"Missing approved fields: {absent}")
    duplicated = sorted({h for h in headers if h in MARKET_REQUIRED and headers.count(h) > 1})
    if duplicated:
        _issue(issues, "FAIL", "DUPLICATE_HEADER", f"Approved fields occur more than once: {duplicated}")
    positions = {name: i for i, name in enumerate(headers)}
    ticker_idx = positions.get("Ticker")
    tickers = [row[ticker_idx] if ticker_idx is not None and ticker_idx < len(row) else "" for _, row in records]
    codal_symbol = tickers[0] if tickers and tickers[0] else None
    if ticker_idx is None or not tickers or any(not ticker for ticker in tickers):
        _issue(issues, "BLOCKED", "CODAL_SYMBOL_MISSING", "Ticker is missing or empty; economic-key checks cannot run.")
        codal_symbol = None
    elif any(ticker != codal_symbol for ticker in tickers):
        _issue(issues, "BLOCKED", "CODAL_SYMBOL_INCONSISTENT", "Ticker values differ within the artifact; economic-key checks cannot run.")
        codal_symbol = None
    seen: dict[str, tuple[tuple[str, ...], int]] = {}
    checked = 0
    for line, row in records:
        if len(row) != len(headers):
            _issue(issues, "FAIL", "CSV_ROW_WIDTH", f"Record at CSV line {line} has {len(row)} fields; header has {len(headers)}.")
        def field(name: str) -> str | None:
            idx = positions.get(name)
            return row[idx] if idx is not None and idx < len(row) else None
        date = field("J-Date")
        date_valid = bool(date and _jalali(date))
        if not date_valid:
            _issue(issues, "FAIL", "INVALID_JALALI_DATE", f"CSV line {line}: J-Date is missing or invalid (source={date!r}).")
        bad = []
        for col in NUMERIC_MARKET:
            if col in absent:
                continue
            value = field(col)
            if not _number(value, integer=col in {"Volume", "No"}):
                bad.append(col)
                rule = "integer" if col in {"Volume", "No"} else "finite numeric"
                _issue(issues, "FAIL", "INVALID_NUMERIC", f"CSV line {line}: {col} must be a {rule} value (source={value!r}).")
        checked += 1
        if codal_symbol is not None and date_valid:
            key = f"{codal_symbol}|{date}"
            payload = tuple(field(c) if field(c) is not None else "<MISSING>" for c in NUMERIC_MARKET)
            if key in seen:
                prior_payload, prior_line = seen[key]
                sev = "FAIL" if prior_payload != payload else "WARNING"
                code = "CONFLICTING_DUPLICATE" if sev == "FAIL" else "IDENTICAL_DUPLICATE"
                _issue(issues, sev, code, f"CSV lines {prior_line} and {line}: duplicate economic key {key}; no winner selected.")
            else:
                seen[key] = (payload, line)
    if not records: _issue(issues, "FAIL", "NO_DATA_ROWS", "No CSV data rows were found.")
    _issue(issues, "WARNING", "PROVENANCE_UNKNOWN", "Publication, first availability, and revision evidence are absent; artifact hash does not establish source identity.")
    return {"feed": "MarketDaily", "status": _status(issues), "artifact": ident, "headers": headers,
            "data_rows": len(records), "validated_rows": checked, "approved_fields": list(MARKET_REQUIRED),
            "ignored_fields": [h for h in ("Final", "Open", "High", "Low") if h in headers],
            "value_policy": "Value validated and preserved independently; never computed from Volume × Close.",
            "economic_key": {"codal_symbol": codal_symbol or UNKNOWN, "date_field": "J-Date"},
            "provenance": _provenance("CODAL (owner-approved; artifact linkage unverified)", UNKNOWN), "issues": issues}


def validate_fx(path: Path, *, rate_type: str = "EXCHANGE_CENTER") -> dict:
    ident = artifact_identity(path)
    issues: list[dict[str, str]] = []
    parsed = parse_fx_xlsx(path, rate_type=rate_type)
    mappings = parsed["mappings"]
    ident["worksheet_names"] = list(dict.fromkeys(m["sheet"] for m in mappings))
    observations = []
    for item in parsed["observations"]:
        observations.append({"sheet": item["sheet"], "row": item["row"],
            "date_cell": item["date_cell"], "source_date": item["date"],
            "sell_cell": item["sell_cell"], "source_sell_rate": item["source_sell_rate"],
            "canonical_rate": item["canonical_rate"],
            "economic_key": f"{item['date']}|USD/IRR|{rate_type}"})
    for message in parsed["errors"]:
        if "conflicting duplicate" in message:
            code, severity = "CONFLICTING_DUPLICATE", "FAIL"
        elif "identical duplicate" in message:
            code, severity = "IDENTICAL_DUPLICATE", "WARNING"
        elif "invalid Jalali date" in message:
            code, severity = "INVALID_FX_DATE", "FAIL"
        elif "invalid sell rate" in message:
            code, severity = "INVALID_FX_RATE", "FAIL"
        else:
            code, severity = "FX_MAPPING_NOT_FOUND", "FAIL"
        _issue(issues, severity, code, message)
    if not mappings: _issue(issues, "FAIL", "FX_MAPPING_NOT_FOUND", "Approved date and sell-rate headers were not found.")
    if not observations and mappings: _issue(issues, "FAIL", "NO_VALID_FX_ROWS", "No valid sell-rate observations were found.")
    _issue(issues, "WARNING", "PROVENANCE_UNKNOWN", "Workbook-to-profile linkage, publication/availability times, and revision identity remain unverified.")
    return {"feed": rate_type, "status": _status(issues), "artifact": ident,
            "mapping": {"worksheets": mappings, "rate_type": rate_type, "pair": "USD/IRR",
                        "conversion": "Toman to Rial × 10" if rate_type == "FREE_MARKET" else "none"},
            "observations": observations, "validated_rows": len(observations),
            "provenance": _provenance(f"{rate_type} (owner-approved; workbook linkage unverified)", UNKNOWN), "issues": issues}


def find_free_market_sample(root: Path) -> dict:
    matches = [p for p in root.rglob("*") if p.is_file() and "free_market" in p.name.lower()
               and p.suffix.lower() in {".csv", ".xlsx", ".xls"}]
    return {"feed": "FREE_MARKET", "status": "PASS" if matches else "BLOCKED",
            "code": None if matches else "BLOCKED_NO_SAMPLE", "samples": [str(p) for p in matches],
            "message": "Sample available for independent review." if matches else "No FREE_MARKET sample found; schema and mapping not inferred."}


def validate_all(market_path: Path, fx_path: Path, *, root: Path | None = None,
                 fx_rate_type: str = "EXCHANGE_CENTER") -> dict:
    results = [validate_market(market_path), validate_fx(fx_path, rate_type=fx_rate_type)]
    statuses = {r["status"] for r in results}
    overall = "BLOCKED" if "BLOCKED" in statuses else "FAIL" if "FAIL" in statuses else "WARNING" if "WARNING" in statuses else "PASS"
    return {"generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "read_only": True, "database_connection": False, "ingestion_performed": False,
            "results": results, "overall_status": overall}


def report_json(report: dict) -> str:
    return json.dumps(report, ensure_ascii=False, indent=2, default=str) + "\n"
