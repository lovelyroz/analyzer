from datetime import datetime
from decimal import Decimal

from src.ingestion.codal.numbers import normalize_digits, parse_amount
from src.ingestion.service import RawLineInput, ingest_codal_report


def test_normalize_digits_maps_persian_and_arabic_indic_to_ascii():
    assert normalize_digits("۱۲۳۴۵۶۷۸۹۰ ١٢٣٤٥٦٧٨٩٠") == "1234567890 1234567890"


def test_parse_amount_accepts_persian_digits_and_arabic_separators():
    assert parse_amount("(۱۲۳٬۴۵۶٫۷۸۹)") == Decimal("-123456.789")


def test_codal_raw_text_fields_are_ascii_normalized_before_persistence(db_session):
    result = ingest_codal_report(
        db_session,
        company_id=1,
        period_id=1,
        report_type="گزارش ۱۴۰۴",
        title="فروش ۱۴۰۴/۰۶/۳۱",
        publication_datetime=datetime(2026, 9, 17, 12, 0, 0),
        codal_tracking_id="۱۲۳۴۵",
        source_url="https://example.test/report/۱۲۳۴۵",
        raw_lines=[
            RawLineInput(
                item_name="محصول ۱۲۳",
                item_code="کد ۴۵۶",
                unit="واحد ۷",
                currency="ریال ۸",
                source_section="بخش ۹",
                source_column="ستون ۱۰",
                value=Decimal("123.45"),
            )
        ],
    )

    assert result.raw_fact_count == 1

    from src.models.normalized import RawFinancialFact
    from src.models.report import Report

    report = db_session.query(Report).filter_by(report_id=result.report_id).one()
    assert report.report_type == "گزارش 1404"
    assert report.title == "فروش 1404/06/31"
    assert report.codal_tracking_id == "12345"
    assert report.source_url == "https://example.test/report/12345"

    fact = (
        db_session.query(RawFinancialFact)
        .filter_by(report_version_id=result.report_version_id)
        .one()
    )
    assert fact.raw_item_name == "محصول 123"
    assert fact.raw_item_code == "کد 456"
    assert fact.unit == "واحد 7"
    assert fact.currency == "ریال 8"
    assert fact.source_section == "بخش 9"
    assert fact.source_column == "ستون 10"
