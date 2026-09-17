"""Persian/Arabic digit and amount normalization for CODAL extraction.

NULL stays NULL. Missing is never converted to zero.
"""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Optional

_PERSIAN_DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")


def normalize_digits(text: str) -> str:
    """Map Persian/Arabic-Indic digits to ASCII digits."""
    return text.translate(_PERSIAN_DIGITS)


def parse_amount(raw: Optional[str]) -> Optional[Decimal]:
    """Parse a financial amount from source text.

    Rules:
    - blank / dash / explicit empty → None (NULL ≠ 0)
    - parentheses → negative
    - thousand separators (comma, slash variants) stripped
    - never invent a value when unparsable → None
    """
    if raw is None:
        return None
    s = normalize_digits(str(raw)).strip()
    if not s or s in {"-", "—", "–", ".", "..", "n/a", "N/A", "NA"}:
        return None

    negative = False
    if s.startswith("(") and s.endswith(")"):
        negative = True
        s = s[1:-1].strip()
    if s.endswith("-"):
        negative = True
        s = s[:-1].strip()
    if s.startswith("-"):
        negative = True
        s = s[1:].strip()

    s = s.replace(",", "").replace("٬", "").replace(" ", "").replace("\u200c", "")
    if not s:
        return None
    try:
        value = Decimal(s)
    except (InvalidOperation, ValueError):
        return None
    if negative and value != 0:
        value = -value
    return value
