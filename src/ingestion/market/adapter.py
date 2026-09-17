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

        header_map = {
            "jdate": "jdate",
            "date": "jdate",
            "open": "open",
            "high": "high",
            "low": "low",
            "close": "close",
            "final": "final",
            "adjclose": "final",
            "adjustedclose": "final",
            "volume": "volume",
            "value": "value",
            "no": "trade_count",
            "tradecount": "trade_count",
            "ticker": "ticker",
            "symbol": "ticker",
        }
        colmap = {}
        for h in reader.fieldnames:
            key = normalize_header(h)
            if key in header_map:
                colmap[header_map[key]] = h

        if "jdate" not in colmap or "ticker" not in colmap:
            raise ValueError("CSV missing required columns: jdate/date and ticker/symbol")

        raw_rows = list(reader)
        result.records_found = len(raw_rows)

        for line_no, row in enumerate(raw_rows, start=2):
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
            open_p = to_decimal(row.get(colmap.get("open", "")))
            high_p = to_decimal(row.get(colmap.get("high", "")))
            low_p = to_decimal(row.get(colmap.get("low", "")))
            close_p = to_decimal(row.get(colmap.get("close", "")))
            final_p = to_decimal(row.get(colmap.get("final", "")))
            adjusted = final_p if final_p is not None else close_p

            result.rows.append(
                OhlcRow(
                    ticker=ticker,
                    jalali_year=jy,
                    jalali_month=jm,
                    jalali_day=jd,
                    open_price=open_p,
                    high_price=high_p,
                    low_price=low_p,
                    close_price=close_p,
                    adjusted_close=adjusted,
                    volume=to_int(row.get(colmap.get("volume", ""))),
                    value=to_decimal(row.get(colmap.get("value", ""))),
                    trade_count=to_int(row.get(colmap.get("trade_count", ""))),
                    line_no=line_no,
                )
            )

    return result
