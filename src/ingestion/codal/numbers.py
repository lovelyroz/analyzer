"""Persian/Arabic digit and amount normalization for CODAL extraction.

Storage policy: every numeric character that crosses the CODAL ingestion
boundary is normalized to ASCII/English digits. NULL stays NULL.
"""

from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Optional

_PERSIAN_DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")


def normalize_digits(text: str) -> str:
    """Map Persian and Arabic-Indic digits to ASCII/English digits."""
    return str(text).translate(_PERSIAN_DIGITS)


def parse_amount(raw: Optional[str]) -> Optional[Decimal]:
    """Parse a financial amount from source text.

    Rules:
    - blank / dash / explicit empty -> None (NULL != 0)
    - parentheses -> negative
    - thousand separators are stripped
    - Arabic decimal separator is normalized to '.'.
    - never invent a value when unparsable -> None
    """
    if raw is None:
        return None
    s = normalize_digits(raw).strip()
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

    s = (
        s.replace(",", "")
        .replace("٬", "")
        .replace("٫", ".")
        .replace(" ", "")
        .replace("\u200c", "")
    )
    if not s:
        return None
    try:
        value = Decimal(s)
    except (InvalidOperation, ValueError):
        return None
    if negative and value != 0:
        value = -value
    return value
