"""Shared validation rules for ingestion adapters and core persistence."""

from __future__ import annotations

from decimal import Decimal
from typing import Optional

VALID_FX_RATE_TYPES = frozenset(
    {"FREE_MARKET", "OPERATIONAL", "OFFICIAL", "ESTIMATED", "MANUAL_OPERATOR"}
)


def validate_fx_rate_type(rate_type: str) -> bool:
    return rate_type in VALID_FX_RATE_TYPES


def validate_ohlc_consistency(
    open_p: Optional[Decimal],
    high_p: Optional[Decimal],
    low_p: Optional[Decimal],
    close_p: Optional[Decimal],
) -> bool:
    """Return True if OHLC values are consistent or any required leg is missing."""
    if not all(v is not None for v in (open_p, high_p, low_p, close_p)):
        return True
    return not (
        high_p < low_p
        or high_p < open_p
        or high_p < close_p
        or low_p > open_p
        or low_p > close_p
    )
