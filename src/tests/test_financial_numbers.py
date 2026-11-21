from decimal import Decimal

import pytest

from src.ingestion.common.financial_numbers import parse_financial_number
from src.ingestion.common.parsing import to_decimal


@pytest.mark.parametrize(("token", "expected"), [
    ("123,456.78", "123456.78"),
    ("۱۲۳٬۴۵۶٫۷۸", "123456.78"),
    ("١٢٣٬٤٥٦٫٧٨", "123456.78"),
    ("۱۲۳۴۵۶٫۷۸۹۰۱۲۳۴۵۶۷۸۹", "123456.7890123456789"),
    ("1.234", "1.234"),
    ("1٬234", "1234"),
])
def test_supported_digit_and_separator_grammar_is_exact(token, expected):
    parsed = parse_financial_number(token)
    assert parsed.value == Decimal(expected)
    assert parsed.source_token == token
    assert parsed.diagnostic_code is None


@pytest.mark.parametrize(("token", "expected"), [
    ("-۱۲٫۵", "-12.5"),
    ("(١٢٫٥)", "-12.5"),
    ("+0.00000000000000000001", "0.00000000000000000001"),
])
def test_sign_and_precision_forms(token, expected):
    assert parse_financial_number(token).value == Decimal(expected)


def test_blank_and_textual_or_numeric_zero_remain_distinct():
    assert parse_financial_number("   ").value_kind == "BLANK"
    assert parse_financial_number("۰", source_kind="TEXT").value_kind == "TEXT_ZERO"
    assert parse_financial_number("0", source_kind="NUMERIC").value_kind == "NUMERIC_ZERO"
    assert parse_financial_number(None).value_kind == "BLANK"


@pytest.mark.parametrize("token", ["1,23", "1,,000", "1٬23", "1,234٬567", "1.2.3", "1٫2٫3", "1,234.56٫7"])
def test_ambiguous_separator_layouts_are_rejected(token):
    parsed = parse_financial_number(token)
    assert parsed.value is None
    assert parsed.diagnostic_code == "AMBIGUOUS_SEPARATOR"


@pytest.mark.parametrize("token", ["12x", "--1", "(1)-", "1 2", "NaN", "∞", "1e3"])
def test_malformed_tokens_are_rejected_without_guessing(token):
    parsed = parse_financial_number(token)
    assert parsed.value is None
    assert parsed.diagnostic_code == "INVALID_NUMERIC_TOKEN"


def test_binary_float_is_never_accepted_by_numeric_parser():
    parsed = parse_financial_number(0.1, source_kind="NUMERIC")
    assert parsed.value is None
    assert parsed.diagnostic_code == "BINARY_FLOAT_UNSUPPORTED"


def test_csv_decimal_facade_uses_same_strict_parser():
    assert to_decimal("۱۲۳٬۴۵۶٫۷۸") == Decimal("123456.78")
    assert to_decimal("1,23") is None
