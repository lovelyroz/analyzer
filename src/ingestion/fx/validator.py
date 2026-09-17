"""FX observation validation before persistence."""

from __future__ import annotations

from decimal import Decimal
from typing import List, Optional

from src.ingestion.common.validation import validate_fx_rate_type
from src.ingestion.service import FxRateInput


def validate_fx_input(item: FxRateInput) -> Optional[str]:
    """Return error message or None if valid."""
    if not validate_fx_rate_type(item.rate_type):
        return f"invalid rate_type={item.rate_type!r}"
    try:
        rate_val = Decimal(item.rate)
    except Exception:
        return "rate not numeric"
    if rate_val <= 0:
        return "rate must be positive"
    has_jalali = (
        item.jalali_year is not None
        and item.jalali_month is not None
        and item.jalali_day is not None
    )
    if not has_jalali and item.rate_date is None:
        return "need jalali components or rate_date"
    return None


def validate_fx_inputs(items: List[FxRateInput]) -> List[str]:
    return [msg for item in items if (msg := validate_fx_input(item)) is not None]
