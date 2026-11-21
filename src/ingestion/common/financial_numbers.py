"""Strict locale-aware Decimal parsing for financial source tokens.

Grammar: ASCII/Persian/Arabic-Indic digits; optional leading sign or enclosing
parentheses for negatives; ASCII dot or Arabic decimal separator (U+066B) for
decimals; one grouping symbol (ASCII comma, Arabic thousands separator U+066C,
or Arabic comma U+060C) in groups of exactly three digits. Grouping must occur
before the decimal separator. ASCII comma is grouping only. Mixed grouping
symbols, repeated decimal separators, exponent notation, and ambiguous layouts
are rejected. No rounding is performed.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation


_DIGITS = str.maketrans(
    "۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789"
)
_GROUPS = {",", "٬", "،"}
_DECIMALS = {".", "٫"}


@dataclass(frozen=True, slots=True)
class FinancialNumber:
    value: Decimal | None
    source_token: str | None
    value_kind: str
    diagnostic_code: str | None = None


def parse_financial_number(raw: object, *, source_kind: str = "TEXT") -> FinancialNumber:
    """Parse one source token without float arithmetic or implicit rounding."""
    if raw is None:
        return FinancialNumber(None, None, "BLANK")
    if isinstance(raw, bool):
        return FinancialNumber(None, str(raw), "INVALID", "INVALID_NUMERIC_TOKEN")
    if isinstance(raw, float):
        return FinancialNumber(None, str(raw), "INVALID", "BINARY_FLOAT_UNSUPPORTED")
    if not isinstance(raw, (str, int, Decimal)):
        return FinancialNumber(None, str(raw), "INVALID", "INVALID_NUMERIC_TOKEN")
    token = str(raw)
    text = token.strip()
    if not text:
        return FinancialNumber(None, token, "BLANK")
    if source_kind not in {"TEXT", "NUMERIC"}:
        return FinancialNumber(None, token, "INVALID", "INVALID_SOURCE_KIND")

    normalized = text.translate(_DIGITS)
    negative = False
    if normalized.startswith("(") or normalized.endswith(")"):
        if not (normalized.startswith("(") and normalized.endswith(")")):
            return FinancialNumber(None, token, "INVALID", "INVALID_NUMERIC_TOKEN")
        negative = True
        normalized = normalized[1:-1]
        if normalized.startswith(("+", "-")):
            return FinancialNumber(None, token, "INVALID", "INVALID_NUMERIC_TOKEN")
    elif normalized[:1] in {"+", "-"}:
        negative = normalized[0] == "-"
        normalized = normalized[1:]
    if not normalized:
        return FinancialNumber(None, token, "INVALID", "INVALID_NUMERIC_TOKEN")

    decimals = [char for char in normalized if char in _DECIMALS]
    if len(decimals) > 1:
        return FinancialNumber(None, token, "AMBIGUOUS", "AMBIGUOUS_SEPARATOR")
    decimal_separator = decimals[0] if decimals else None
    if decimal_separator:
        whole, fraction = normalized.split(decimal_separator, 1)
        if not fraction or any(char in _GROUPS or char in _DECIMALS for char in fraction):
            return FinancialNumber(None, token, "INVALID", "INVALID_NUMERIC_TOKEN")
        if not fraction.isdigit():
            return FinancialNumber(None, token, "INVALID", "INVALID_NUMERIC_TOKEN")
    else:
        whole, fraction = normalized, ""

    used_groups = {char for char in whole if char in _GROUPS}
    if len(used_groups) > 1:
        return FinancialNumber(None, token, "AMBIGUOUS", "AMBIGUOUS_SEPARATOR")
    if used_groups:
        separator = next(iter(used_groups))
        groups = whole.split(separator)
        if (not groups[0].isdigit() or not 1 <= len(groups[0]) <= 3
                or any(not group.isdigit() or len(group) != 3 for group in groups[1:])):
            return FinancialNumber(None, token, "AMBIGUOUS", "AMBIGUOUS_SEPARATOR")
        whole_digits = "".join(groups)
    else:
        if not whole.isdigit():
            return FinancialNumber(None, token, "INVALID", "INVALID_NUMERIC_TOKEN")
        whole_digits = whole
    canonical = whole_digits + ("." + fraction if decimal_separator else "")
    try:
        value = Decimal(canonical)
    except InvalidOperation:
        return FinancialNumber(None, token, "INVALID", "INVALID_NUMERIC_TOKEN")
    if negative:
        value = -value
    if not value.is_finite():
        return FinancialNumber(None, token, "INVALID", "INVALID_NUMERIC_TOKEN")
    if value == 0:
        kind = "NUMERIC_ZERO" if source_kind == "NUMERIC" else "TEXT_ZERO"
    elif value < 0:
        kind = "NEGATIVE"
    else:
        kind = "NUMBER"
    return FinancialNumber(value, token, kind)
