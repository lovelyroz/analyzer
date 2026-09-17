"""OHLC row validation."""

from __future__ import annotations

from src.ingestion.common.validation import validate_ohlc_consistency
from src.ingestion.market.adapter import OhlcRow


def is_valid_ohlc_row(row: OhlcRow) -> bool:
    return validate_ohlc_consistency(
        row.open_price, row.high_price, row.low_price, row.close_price
    )
