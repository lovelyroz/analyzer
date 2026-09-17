"""Parse OHLC CSV files in the common Iranian market format.

Expected columns (case-insensitive, flexible order):
  J-Date / Date, Open, High, Low, Close, Final (optional adjusted),
  Volume, Value, No / TradeCount, Ticker, Name, Market
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Iterator, Optional, Dict, Union
from datetime import date

from src.ingestion.common.jalali import parse_jalali_date


@dataclass(frozen=True)
class OhlcRow:
    """One validated raw OHLC observation before persistence."""

    trade_date: date
    open_price: Optional[Decimal]
    high_price: Optional[Decimal]
    low_price: Optional[Decimal]
    close_price: Optional[Decimal]
    adjusted_close: Optional[Decimal]
    volume: Optional[int]
    value: Optional[Decimal]
    trade_count: Optional[int]
    ticker: str
    company_name: Optional[str] = None
    market: Optional[str] = None
    source_line: Optional[int] = None


def _to_decimal(raw: Optional[str]) -> Optional[Decimal]:
    if raw is None or str(raw).strip() == "":
        return None
    try:
        return Decimal(str(raw).strip().replace(",", ""))
    except (InvalidOperation, ValueError):
        return None


def _to_int(raw: Optional[str]) -> Optional[int]:
    if raw is None or str(raw).strip() == "":
        return None
    try:
        return int(Decimal(str(raw).strip().replace(",", "")))
    except (InvalidOperation, ValueError):
        return None


def _normalize_header(h: str) -> str:
    return h.strip().lower().replace("-", "").replace("_", "").replace(" ", "")


_HEADER_MAP = {
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
    "name": "name",
    "market": "market",
}


def parse_ohlc_csv(
    path: Union[str, Path],
    *,
    encoding: str = "utf-8-sig",
) -> Iterator[OhlcRow]:
    """Yield OhlcRow objects from a CSV file.

    Skips rows that cannot be parsed; caller is responsible for counting failures.
    """
    path = Path(path)
    with path.open(encoding=encoding, newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            return

        colmap: Dict[str, str] = {}
        for h in reader.fieldnames:
            key = _normalize_header(h)
            if key in _HEADER_MAP:
                colmap[_HEADER_MAP[key]] = h

        required = {"jdate", "ticker"}
        missing = required - set(colmap.keys())
        if missing:
            raise ValueError(f"CSV missing required columns: {missing}")

        for line_no, row in enumerate(reader, start=2):
            try:
                jdate_raw = row.get(colmap["jdate"], "").strip()
                if not jdate_raw:
                    continue
                trade_date = parse_jalali_date(jdate_raw)

                ticker = row.get(colmap.get("ticker", ""), "").strip()
                if not ticker:
                    continue

                open_p = _to_decimal(row.get(colmap.get("open", "")))
                high_p = _to_decimal(row.get(colmap.get("high", "")))
                low_p = _to_decimal(row.get(colmap.get("low", "")))
                close_p = _to_decimal(row.get(colmap.get("close", "")))
                final_p = _to_decimal(row.get(colmap.get("final", "")))

                adjusted = final_p if final_p is not None else close_p

                yield OhlcRow(
                    trade_date=trade_date,
                    open_price=open_p,
                    high_price=high_p,
                    low_price=low_p,
                    close_price=close_p,
                    adjusted_close=adjusted,
                    volume=_to_int(row.get(colmap.get("volume", ""))),
                    value=_to_decimal(row.get(colmap.get("value", ""))),
                    trade_count=_to_int(row.get(colmap.get("trade_count", ""))),
                    ticker=ticker,
                    company_name=row.get(colmap.get("name", ""), None) or None,
                    market=row.get(colmap.get("market", ""), None) or None,
                    source_line=line_no,
                )
            except Exception:
                continue
