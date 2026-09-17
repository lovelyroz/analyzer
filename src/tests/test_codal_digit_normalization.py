from decimal import Decimal

from src.ingestion.codal.numbers import normalize_digits, parse_amount


def test_normalize_digits_maps_persian_and_arabic_indic_to_ascii():
    assert normalize_digits("۱۲۳۴۵۶۷۸۹۰ ١٢٣٤٥٦٧٨٩٠") == "1234567890 1234567890"


def test_parse_amount_accepts_persian_digits_and_arabic_separators():
    assert parse_amount("(۱۲۳٬۴۵۶٫۷۸۹)") == Decimal("-123456.789")
