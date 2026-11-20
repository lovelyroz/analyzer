"""OHLC format adapters (CSV today; XLSX can be added without touching core)."""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from decimal import Decimal
from pathlib import Path
from typing import List, Optional, Union

from src.ingestion.common.parsing import (
    normalize_header,
    parse_jalali_components,
    to_decimal,
    to_int,
)


@dataclass(frozen=True)
class OhlcRow:
    ticker: str
    jalali_year: int
    jalali_month: int
    jalali_day: int
    open_price: Optional[Decimal]
    high_price: Optional[Decimal]
    low_price: Optional[Decimal]
    close_price: Optional[Decimal]
    adjusted_close: Optional[Decimal]
    volume: Optional[int]
    value: Optional[Decimal]
    trade_count: Optional[int]
    line_no: int


@dataclass
class OhlcCsvParseResult:
    """Adapter output: DTOs + parse diagnostics (no DB)."""

    rows: List[OhlcRow] = field(default_factory=list)
    records_found: int = 0
    errors: List[str] = field(default_factory=list)


def load_ohlc_csv_rows(path: Union[str, Path]) -> OhlcCsvParseResult:
    """Parse Iranian-market OHLC CSV into OhlcRow DTOs (no DB access)."""
    path = Path(path)
    result = OhlcCsvParseResult()

    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            return result

        # Keep the MarketDaily allowlist deliberately narrow.  OHLC/Final
        # columns may exist in source exports but are never inspected or mapped.
        header_map = {"jdate": "jdate", "ticker": "ticker", "close": "close",
                      "volume": "volume", "no": "trade_count", "value": "value"}
        colmap = {}
        for h in reader.fieldnames:
            key = normalize_header(h)
            if key in header_map:
                colmap[header_map[key]] = h

        required = ("jdate", "ticker", "close", "volume", "trade_count", "value")
        missing = [name for name in required if name not in colmap]
        if missing:
            raise ValueError(f"CSV missing approved required columns: {missing}")

        raw_rows = list(reader)
        result.records_found = len(raw_rows)
        seen = {}

        for line_no, row in enumerate(raw_rows, start=2):
            if None in row:
                result.errors.append(f"line {line_no}: row has more fields than the header")
                continue
            if any(row.get(h) is None for h in reader.fieldnames):
                result.errors.append(f"line {line_no}: row has fewer fields than the header")
                continue
            jdate_raw = (row.get(colmap["jdate"]) or "").strip()
            ticker = (row.get(colmap["ticker"]) or "").strip()
            if not jdate_raw or not ticker:
                result.errors.append(f"line {line_no}: missing date or ticker")
                continue

            components = parse_jalali_components(jdate_raw)
            if components is None:
                result.errors.append(f"line {line_no}: invalid Jalali date {jdate_raw!r}")
                continue

            jy, jm, jd = components
            close_p = to_decimal(row.get(colmap.get("close", "")))
            volume = to_int(row.get(colmap["volume"]))
            value = to_decimal(row.get(colmap["value"]))
            trade_count = to_int(row.get(colmap["trade_count"]))
            if close_p is None or volume is None or value is None or trade_count is None:
                result.errors.append(f"line {line_no}: invalid Close, Volume, No, or Value")
                continue
            key = (ticker, jy, jm, jd)
            payload = (close_p, volume, trade_count, value)
            if key in seen:
                kind = "identical" if seen[key][0] == payload else "conflicting"
                result.errors.append(f"line {line_no}: {kind} duplicate for {ticker} {jdate_raw}; prior line {seen[key][1]}")
                continue
            seen[key] = (payload, line_no)

            result.rows.append(
                OhlcRow(
                    ticker=ticker,
                    jalali_year=jy,
                    jalali_month=jm,
                    jalali_day=jd,
                    open_price=None,
                    high_price=None,
                    low_price=None,
                    close_price=close_p,
                    adjusted_close=None,
                    volume=volume,
                    value=value,
                    trade_count=trade_count,
                    line_no=line_no,
                )
            )

    return result
