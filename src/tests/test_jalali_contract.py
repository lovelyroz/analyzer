"""Tests for the shared Jalali date contract (src/core/jalali.py)."""

import pytest

from src.core.jalali import JalaliDate, is_valid_jalali_components, validate_jalali_date
from src.ingestion.common.parsing import parse_jalali_components
from src.ingestion.market import queries


@pytest.mark.parametrize("value", [(1405, 2, 11), (1404, 6, 31), (1404, 12, 29), (1403, 12, 30)])
def test_valid_jalali_dates_are_returned_unchanged(value):
    assert validate_jalali_date(value, label="d") == value


@pytest.mark.parametrize(
    "value",
    [(1405, 13, 1), (1405, 0, 1), (1405, 2, 0), (1405, 7, 31), (1404, 12, 30), (0, 1, 1), (-5, 1, 1),
     (1405, 2), [1405, 2, 11], "1405-02-11", (1405, 2, "11"), (1405.0, 2, 11), (True, 2, 11), None],
)
def test_invalid_jalali_dates_raise_value_error(value):
    with pytest.raises(ValueError):
        validate_jalali_date(value, label="d")


def test_error_message_carries_label():
    with pytest.raises(ValueError, match="my_label"):
        validate_jalali_date((1405, 13, 1), label="my_label")


def test_query_layer_and_string_parser_share_the_same_rules():
    assert queries.JalaliDate is JalaliDate
    for y, m, d in [(1405, 2, 11), (1404, 12, 30), (1405, 7, 31), (1405, 13, 1), (1405, 2, 0)]:
        parsed = parse_jalali_components(f"{y:04d}-{m:02d}-{d:02d}")
        assert (parsed is not None) == is_valid_jalali_components(y, m, d)
        assert (parsed is not None) == _query_accepts((y, m, d))


def _query_accepts(value):
    try:
        queries._validate_jalali_date(value, label="d")
    except ValueError:
        return False
    return True
