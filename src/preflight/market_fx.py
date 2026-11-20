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

from openpyxl import load_workbook


MARKET_REQUIRED = ("J-Date", "Close", "Volume", "No", "Value")
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


def _number(value: Any, *, positive: bool = False) -> bool:
    if value is None or isinstance(value, bool):
        return False
    raw = str(value).strip().replace(",", "")
    if not raw:
        return False
    try:
        n = Decimal(raw)
        return n.is_finite() and (not positive or n > 0)
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


def validate_market(path: Path, company_key: str | None = None) -> dict:
    ident = artifact_identity(path)
    issues: list[dict[str, str]] = []
    try:
        with Path(ident["path"]).open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            headers = reader.fieldnames or []
            rows = list(reader)
    except (UnicodeError, csv.Error) as exc:
        headers, rows = [], []
        _issue(issues, "FAIL", "CSV_READ_ERROR", str(exc))
    absent = [h for h in MARKET_REQUIRED if h not in headers]
    if absent: _issue(issues, "FAIL", "MISSING_REQUIRED_FIELDS", f"Missing approved fields: {absent}")
    if not company_key: _issue(issues, "BLOCKED", "COMPANY_KEY_UNRESOLVED", "Supply a stable, owner-resolved company key; ticker alone is not canonical.")
    seen: dict[str, tuple] = {}
    checked = 0
    if not absent and company_key:
        for n, row in enumerate(rows, 2):
            date = (row.get("J-Date") or "").strip()
            if not date or not _jalali(date):
                _issue(issues, "FAIL", "INVALID_JALALI_DATE", f"Row {n}: J-Date is missing or invalid."); continue
            vals = [row.get(col) for col in NUMERIC_MARKET]
            bad = [col for col in NUMERIC_MARKET if not _number(row.get(col))]
            if bad:
                _issue(issues, "FAIL", "INVALID_NUMERIC", f"Row {n}: missing/malformed numeric fields {bad}."); continue
            checked += 1
            key = f"{company_key}|{date}"
            payload = tuple((row.get(c) or "").strip() for c in NUMERIC_MARKET)
            if key in seen:
                sev = "FAIL" if seen[key] != payload else "WARNING"
                code = "CONFLICTING_DUPLICATE" if sev == "FAIL" else "IDENTICAL_DUPLICATE"
                _issue(issues, sev, code, f"Row {n}: duplicate economic key {key}; source rows are retained, no winner selected.")
            else: seen[key] = payload
    if not rows: _issue(issues, "FAIL", "NO_DATA_ROWS", "No CSV data rows were found.")
    _issue(issues, "WARNING", "PROVENANCE_UNKNOWN", "Publication, first availability, and revision evidence are absent; artifact hash does not establish source identity.")
    return {"feed": "MarketDaily", "status": _status(issues), "artifact": ident, "headers": headers,
            "data_rows": len(rows), "validated_rows": checked, "approved_fields": list(MARKET_REQUIRED),
            "ignored_fields": [h for h in ("Final", "Open", "High", "Low") if h in headers],
            "value_policy": "Value validated and preserved independently; never computed from Volume × Close.",
            "economic_key": {"company_key": company_key or UNKNOWN, "date_field": "J-Date"},
            "provenance": _provenance("CODAL (owner-approved; artifact linkage unverified)", UNKNOWN), "issues": issues}


def validate_fx(path: Path) -> dict:
    ident = artifact_identity(path)
    issues: list[dict[str, str]] = []
    wb = load_workbook(ident["path"], read_only=True, data_only=False)
    ident["worksheet_names"] = wb.sheetnames
    observations: list[dict] = []
    mapped = False
    for ws in wb.worksheets:
        header_row = None
        date_col = sell_col = None
        for row in ws.iter_rows(values_only=False):
            values = [c.value.strip() if isinstance(c.value, str) else c.value for c in row]
            ds = [i for i, v in enumerate(values) if v in FX_DATE_HEADERS]
            ss = [i for i, v in enumerate(values) if v in FX_SELL_HEADERS]
            if ds and ss:
                header_row, date_col, sell_col = row[0].row, ds[0], ss[0]
                break
        if header_row is None: continue
        mapped = True
        seen: dict[str, tuple] = {}
        for cells in ws.iter_rows(min_row=header_row + 1, values_only=False):
            date_cell, sell_cell = cells[date_col], cells[sell_col]
            date, rate = date_cell.value, sell_cell.value
            if date is None and rate is None: continue
            date_text = date.strip() if isinstance(date, str) else date
            rownum = date_cell.row
            if not _jalali(date_text):
                _issue(issues, "FAIL", "INVALID_FX_DATE", f"{ws.title}!{date_cell.coordinate}: invalid Jalali date."); continue
            if not _number(rate, positive=True):
                _issue(issues, "FAIL", "INVALID_FX_RATE", f"{ws.title}!{sell_cell.coordinate}: missing, malformed, or non-positive sell rate."); continue
            payload = str(rate).strip()
            if date_text in seen:
                sev = "FAIL" if seen[date_text] != payload else "WARNING"
                code = "CONFLICTING_DUPLICATE" if sev == "FAIL" else "IDENTICAL_DUPLICATE"
                _issue(issues, sev, code, f"{ws.title} row {rownum}: duplicate FX economic key {date_text}|USD/IRR|EXCHANGE_CENTER.")
            else: seen[date_text] = payload
            observations.append({"sheet": ws.title, "date_cell": date_cell.coordinate, "source_date": date,
                                 "sell_cell": sell_cell.coordinate, "source_sell_rate": rate,
                                 "economic_key": f"{date_text}|USD/IRR|EXCHANGE_CENTER"})
    wb.close()
    if not mapped: _issue(issues, "FAIL", "FX_MAPPING_NOT_FOUND", "Approved date and sell-rate headers were not found; no alternative mapping was inferred.")
    if not observations and mapped: _issue(issues, "FAIL", "NO_VALID_FX_ROWS", "No valid sell-rate observations were found.")
    _issue(issues, "WARNING", "PROVENANCE_UNKNOWN", "Workbook-to-profile linkage, publication/availability times, and revision identity remain unverified.")
    return {"feed": "EXCHANGE_CENTER", "status": _status(issues), "artifact": ident,
            "mapping": {"date_headers": list(FX_DATE_HEADERS), "sell_headers": list(FX_SELL_HEADERS),
                        "rate_type": "EXCHANGE_CENTER", "pair": "USD/IRR", "conversion": "none"},
            "observations": observations, "validated_rows": len(observations),
            "provenance": _provenance("EXCHANGE_CENTER (owner-approved; workbook linkage unverified)", UNKNOWN), "issues": issues}


def find_free_market_sample(root: Path) -> dict:
    matches = [p for p in root.rglob("*") if p.is_file() and "free_market" in p.name.lower()
               and p.suffix.lower() in {".csv", ".xlsx", ".xls"}]
    return {"feed": "FREE_MARKET", "status": "PASS" if matches else "BLOCKED",
            "code": None if matches else "BLOCKED_NO_SAMPLE", "samples": [str(p) for p in matches],
            "message": "Sample available for independent review." if matches else "No FREE_MARKET sample found; schema and mapping not inferred."}


def validate_all(market_path: Path, fx_path: Path, *, company_key: str | None = None, root: Path | None = None) -> dict:
    results = [validate_market(market_path, company_key), validate_fx(fx_path),
               find_free_market_sample(root or Path.cwd())]
    statuses = {r["status"] for r in results}
    overall = "BLOCKED" if "BLOCKED" in statuses else "FAIL" if "FAIL" in statuses else "WARNING" if "WARNING" in statuses else "PASS"
    return {"generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "read_only": True, "database_connection": False, "ingestion_performed": False,
            "results": results, "overall_status": overall}


def report_json(report: dict) -> str:
    return json.dumps(report, ensure_ascii=False, indent=2, default=str) + "\n"
