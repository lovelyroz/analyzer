"""Source-level validation helpers. No analytical logic."""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import List, Optional


@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    def add_error(self, msg: str) -> None:
        self.errors.append(msg)
        self.is_valid = False

    def add_warning(self, msg: str) -> None:
        self.warnings.append(msg)


def validate_positive_or_null(
    value: Optional[Decimal | int | float],
    field_name: str,
    allow_zero: bool = True,
) -> Optional[str]:
    """Return error message if value is negative (or zero when not allowed)."""
    if value is None:
        return None
    try:
        v = Decimal(str(value))
    except Exception:
        return f"{field_name} is not a valid number"
    if v < 0:
        return f"{field_name} must not be negative (got {v})"
    if not allow_zero and v == 0:
        return f"{field_name} must not be zero"
    return None


def validate_ohlc_consistency(
    open_price: Optional[Decimal],
    high_price: Optional[Decimal],
    low_price: Optional[Decimal],
    close_price: Optional[Decimal],
) -> ValidationResult:
    """Basic OHLC logical consistency checks.

    Rules (only when all four values are present):
    - high >= max(open, close, low)
    - low  <= min(open, close, high)
    - high >= low
    """
    result = ValidationResult(is_valid=True)

    prices = {
        "open": open_price,
        "high": high_price,
        "low": low_price,
        "close": close_price,
    }

    for name, val in prices.items():
        err = validate_positive_or_null(val, name, allow_zero=False)
        if err:
            result.add_error(err)

    if not result.is_valid:
        return result

    if all(v is not None for v in prices.values()):
        o, h, l, c = open_price, high_price, low_price, close_price  # type: ignore
        if h < l:
            result.add_error(f"high ({h}) < low ({l})")
        if h < o or h < c:
            result.add_error(f"high ({h}) is less than open/close")
        if l > o or l > c:
            result.add_error(f"low ({l}) is greater than open/close")

    return result
