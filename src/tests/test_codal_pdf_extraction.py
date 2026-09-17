from datetime import datetime
from decimal import Decimal
from pathlib import Path

import pytest

from src.ingestion.codal.adapter import extract_raw_lines_from_pdf
from src.ingestion.codal.ingestion import ingest_codal_pdf
from src.ingestion.codal.parser import (
    CodalPdfExtractionError,
    extract_raw_lines_from_text,
    normalize_pdf_text,
    parse_numeric_token,
)
from src.ingestion.service import RawLineInput, ingest_codal_report
from src.models.audit import IngestionRun
from src.models.entity import Company, Industry
from src.models.normalized import RawFinancialFact
from src.models.period import FinancialPeriod
from src.models.report import ReportVersion
from src.core.database import Base
from src.core.database import SessionLocal
from src.models.report import Report


PDF_ROOT = Path(__file__).parents[2] / "pdf"


@pytest.fixture
def ingestion_session():
    Base.metadata.create_all(bind=SessionLocal.kw["bind"])
    session = SessionLocal()
    industry = Industry(industry_code="CODAL_TEST", industry_name="Codal test")
    session.add(industry)
    session.flush()
    company = Company(ticker="CODAL", company_name="Codal test", industry_id=industry.industry_id)
    session.add(company)
    session.flush()
    period = FinancialPeriod(
        company_id=company.company_id,
        period_type="QUARTER",
        start_date=datetime(2024, 1, 1).date(),
        end_date=datetime(2024, 3, 31).date(),
        fiscal_year=1403,
        fiscal_quarter=1,
        months_length=3,
        is_ytd=False,
    )
    session.add(period)
    session.flush()
    try:
        yield session, company, period
    finally:
        session.close()
        Base.metadata.drop_all(bind=SessionLocal.kw["bind"])


def test_persian_numeric_normalization_preserves_missing_and_negative_values():
    assert normalize_pdf_text("١٢٣٬٤٥٦") == "123,456"
    assert parse_numeric_token("(۱۲۳٬۴۵۶)") == Decimal("-123456")
    assert parse_numeric_token("0") == Decimal("0")
    assert parse_numeric_token("") is None
    assert parse_numeric_token("-") is None


def test_text_parser_preserves_row_and_column_for_multi_value_statement_rows():
    lines = extract_raw_lines_from_text(
        """
        صورت سود و زیان
        درآمدهای عملیاتی ۱,۲۰۰ (۳۰۰) 0
        توضیح بدون عدد
        """,
        unit="میلیون ریال",
    )

    assert [line.item_name for line in lines] == [
        "درآمدهای عملیاتی",
        "درآمدهای عملیاتی",
        "درآمدهای عملیاتی",
    ]
    assert [line.value for line in lines] == [Decimal("1200"), Decimal("-300"), Decimal("0")]
    assert [line.source_column for line in lines] == ["1", "2", "3"]
    assert all(line.source_row is not None for line in lines)
    assert all(line.unit == "میلیون ریال" for line in lines)
    assert all(isinstance(line, RawLineInput) for line in lines)


def test_representative_monthly_codal_pdf_is_deterministic_and_returns_raw_dto():
    path = PDF_ROOT / "seo-codal-report (1).pdf"
    result_a = extract_raw_lines_from_pdf(
        path,
        title="sample",
        report_type="MONTHLY_ACTIVITY",
        publication_datetime=datetime(2026, 9, 1),
        codal_tracking_id="CODAL-SAMPLE-1",
        source_url="https://example.invalid/codal/sample-1",
    )
    result_b = extract_raw_lines_from_pdf(
        path,
        title="sample",
        report_type="MONTHLY_ACTIVITY",
        publication_datetime=datetime(2026, 9, 1),
        codal_tracking_id="CODAL-SAMPLE-1",
        source_url="https://example.invalid/codal/sample-1",
    )

    assert len(result_a.raw_lines) > 0
    assert result_a.raw_lines == result_b.raw_lines
    assert all(isinstance(line, RawLineInput) for line in result_a.raw_lines)
    assert result_a.codal_tracking_id == "CODAL-SAMPLE-1"
    assert result_a.source_url.endswith("sample-1")
    assert result_a.publication_datetime == datetime(2026, 9, 1)
    assert all(line.item_name for line in result_a.raw_lines)


@pytest.mark.parametrize("filename", [
    "seo-codal-report (1).pdf",
    "seo-codal-report (3).pdf",
    "seo-codal-report (10).pdf",
    "seo-codal-report (13).pdf",
])
def test_representative_codal_layouts_extract_rows(filename):
    path = PDF_ROOT / filename
    result = extract_raw_lines_from_pdf(
        path,
        title=filename,
        report_type="CODAL",
        publication_datetime=datetime(2026, 9, 1),
    )
    assert result.raw_lines
    assert all(line.source_row is not None for line in result.raw_lines)


def test_image_only_or_empty_text_pdf_is_rejected():
    path = PDF_ROOT / "seo-codal-report (5).pdf"
    with pytest.raises(CodalPdfExtractionError):
        extract_raw_lines_from_pdf(
            path,
            title="empty",
            report_type="CODAL",
            publication_datetime=datetime(2026, 9, 1),
        )


def test_all_supplied_codal_pdfs_have_explicit_extraction_outcomes():
    pdfs = sorted(PDF_ROOT.glob("*.pdf"))
    assert len(pdfs) == 20
    outcomes = {}
    for path in pdfs:
        try:
            result = extract_raw_lines_from_pdf(
                path,
                title=path.name,
                report_type="CODAL",
                publication_datetime=datetime(2026, 9, 1),
            )
            outcomes[path.name] = len(result.raw_lines)
        except CodalPdfExtractionError:
            outcomes[path.name] = None

    assert outcomes["seo-codal-report (5).pdf"] is None
    assert all(count is not None and count > 0 for name, count in outcomes.items() if name != "seo-codal-report (5).pdf")


def test_pdf_output_loads_into_core_persistence_and_duplicate_is_idempotent(ingestion_session):
    session, company, period = ingestion_session
    extraction = extract_raw_lines_from_pdf(
        PDF_ROOT / "seo-codal-report (1).pdf",
        title="Monthly sample",
        report_type="MONTHLY_ACTIVITY",
        publication_datetime=datetime(2026, 9, 1),
        codal_tracking_id="CODAL-IDEMPOTENT-1",
    )
    first = ingest_codal_report(
        session,
        company_id=company.company_id,
        period_id=period.period_id,
        report_type=extraction.report_type,
        title=extraction.title,
        publication_datetime=extraction.publication_datetime,
        raw_lines=extraction.raw_lines,
        codal_tracking_id=extraction.codal_tracking_id,
    )
    second = ingest_codal_report(
        session,
        company_id=company.company_id,
        period_id=period.period_id,
        report_type=extraction.report_type,
        title=extraction.title,
        publication_datetime=extraction.publication_datetime,
        raw_lines=extraction.raw_lines,
        codal_tracking_id=extraction.codal_tracking_id,
    )

    assert first.report_version_id == second.report_version_id
    assert session.query(ReportVersion).count() == 1
    assert session.query(RawFinancialFact).count() == first.raw_fact_count
    runs = session.query(IngestionRun).order_by(IngestionRun.ingestion_id).all()
    assert len(runs) == 2
    assert runs[1].records_updated == first.raw_fact_count


def test_codal_pdf_facade_connects_extraction_to_raw_persistence(ingestion_session):
    session, company, period = ingestion_session
    result = ingest_codal_pdf(
        session,
        PDF_ROOT / "seo-codal-report (10).pdf",
        company_id=company.company_id,
        period_id=period.period_id,
        title="Interim sample",
        report_type="INTERIM",
        publication_datetime=datetime(2026, 9, 2),
        codal_tracking_id="CODAL-FACADE-1",
        source_url="local://seo-codal-report-10.pdf",
    )

    assert result.raw_fact_count > 0
    report = session.get(Report, result.report_id)
    assert report.source_url == "local://seo-codal-report-10.pdf"
    assert session.query(RawFinancialFact).count() == result.raw_fact_count