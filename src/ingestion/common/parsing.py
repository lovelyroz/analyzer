"""Source-string parsing helpers. No calendar conversion."""

from __future__ import annotations

from decimal import Decimal
from typing import Optional, Tuple

from src.core.jalali import is_valid_jalali_components


def to_decimal(raw: Optional[str]) -> Optional[Decimal]:
    if raw is None or str(raw).strip() == "":
        return None
    try:
        return Decimal(str(raw).strip().replace(",", ""))
    except Exception:
        return None


def to_int(raw: Optional[str]) -> Optional[int]:
    if raw is None or str(raw).strip() == "":
        return None
    try:
        return int(Decimal(str(raw).strip().replace(",", "")))
    except Exception:
        return None


def normalize_header(h: str) -> str:
    return h.strip().lower().replace("-", "").replace("_", "").replace(" ", "")


def parse_jalali_components(s: str) -> Optional[Tuple[int, int, int]]:
    """Parse 'YYYY-MM-DD' or 'YYYY/MM/DD' Jalali text into (year, month, day).

    String splitting of the source calendar label only.
    NOT a Jalali→Gregorian calendar conversion (CHANGE-005 / CHANGE-006).
    """
    s = s.strip().replace("/", "-")
    parts = s.split("-")
    if len(parts) != 3:
        return None
    try:
        y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
    except ValueError:
        return None
    # Shared Jalali validation (range, month length, leap year); no calendar
    # conversion is performed.
    if not is_valid_jalali_components(y, m, d):
        return None
    return y, m, d
