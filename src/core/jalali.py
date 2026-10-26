"""Shared Jalali (Persian) calendar date contract.

A ``JalaliDate`` is a plain ``(year, month, day)`` tuple of integers. Values are
compared numerically, component by component; no Gregorian ``datetime`` is ever
constructed from, or inferred for, Jalali components. This module depends only
on ``jdatetime`` so that the market engine, the ingestion layer and the query
layer can all share one definition without importing each other.
"""

from typing import Tuple

import jdatetime

JalaliDate = Tuple[int, int, int]


def is_valid_jalali_components(year: int, month: int, day: int) -> bool:
    """Return whether integer components form a real Jalali calendar date.

    ``jdatetime.date`` is used only as a month-length / leap-year validator; the
    result is never converted to or stored in another calendar.
    """
    if year < 1 or not (1 <= month <= 12 and 1 <= day <= 31):
        return False
    try:
        jdatetime.date(year, month, day)
    except (TypeError, ValueError, OverflowError):
        return False
    return True


def validate_jalali_date(value: object, *, label: str) -> JalaliDate:
    """Return ``value`` unchanged if it is a valid ``JalaliDate``.

    Anything else (wrong container, non-``int`` parts including ``bool``,
    strings, or an impossible date) raises ``ValueError``.
    """
    if (
        not isinstance(value, tuple)
        or len(value) != 3
        or any(type(part) is not int for part in value)
    ):
        raise ValueError(f"{label} must be a (year, month, day) integer tuple")
    year, month, day = value
    if not is_valid_jalali_components(year, month, day):
        raise ValueError(f"{label} is not a valid Jalali date: {value!r}")
    return year, month, day
