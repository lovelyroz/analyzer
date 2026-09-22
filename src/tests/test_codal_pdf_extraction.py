from collections import Counter
from datetime import datetime
from decimal import Decimal
from pathlib import Path
import unicodedata

import pytest

from src.core.database import Base, SessionLocal
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
from src.models.report import Report, ReportVersion


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
    assert [line.item_name for line in lines] == ["درآمدهای عملیاتی"] * 3
    assert [line.value for line in lines] == [Decimal("1200"), Decimal("-300"), Decimal("0")]
    assert [line.source_column for line in lines] == ["1", "2", "3"]
    assert all(line.source_row is not None for line in lines)
    assert all(line.unit == "میلیون ریال" for line in lines)
    assert all(isinstance(line, RawLineInput) for line in lines)


def test_table_extractor_does_not_treat_dates_as_amounts():
    from src.ingestion.codal import pdf_extract
    assert pdf_extract._looks_like_date("۱۴۰۴/۰۶/۳۱")
    assert not pdf_extract._looks_pure_number("۱۴۰۴/۰۶/۳۱")
    assert pdf_extract._looks_pure_number("۱۲۳٬۴۵۶")


def test_rtl_pdf_line_extracts_trailing_label_without_reversing_text():
    from src.ingestion.codal import pdf_extract
    pages = [(1, "١٨ ١,٢١٨,۶٨٩,٢٣٩ ٢,٢٠۵,٩٨۶,٢٩٩ ﻲﻳﺎﻄﻋا تﻼﯿﮫﺴﺗ دﻣآرد")]
    rows = pdf_extract._lines_from_text_pages(pages)
    assert len(rows) == 3
    assert all(row.item_name == "ﻲﻳﺎﻄﻋا تﻼﯿﮫﺴﺗ دﻣآرد" for row in rows)
    assert [row.source_column for row in rows] == ["1", "2", "3"]


def test_representative_monthly_codal_pdf_is_deterministic_and_returns_raw_dto():
    path = PDF_ROOT / "seo-codal-report (1).pdf"
    kwargs = dict(
        title="sample",
        report_type="MONTHLY_ACTIVITY",
        publication_datetime=datetime(2026, 9, 1),
        codal_tracking_id="CODAL-SAMPLE-1",
        source_url="https://example.invalid/codal/sample-1",
    )
    result_a = extract_raw_lines_from_pdf(path, **kwargs)
    result_b = extract_raw_lines_from_pdf(path, **kwargs)
    assert result_a.raw_lines
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
    result = extract_raw_lines_from_pdf(
        PDF_ROOT / filename,
        title=filename,
        report_type="CODAL",
        publication_datetime=datetime(2026, 9, 1),
    )
    assert result.raw_lines
    assert all(line.source_row is not None for line in result.raw_lines)


def test_malformed_pdf_is_rejected_and_ingestion_is_audited(tmp_path, ingestion_session):
    session, company, period = ingestion_session
    path = tmp_path / "malformed.pdf"
    path.write_bytes(b"this is not a valid pdf")
    with pytest.raises(CodalPdfExtractionError):
        ingest_codal_pdf(
            session, path, company_id=company.company_id, period_id=period.period_id,
            title="Malformed sample", report_type="CODAL",
            publication_datetime=datetime(2026, 9, 1), codal_tracking_id="CODAL-MALFORMED-1",
        )
    run = session.query(IngestionRun).order_by(IngestionRun.ingestion_id.desc()).first()
    assert run is not None and run.source == "CODAL" and run.status == "FAILED"
    assert run.records_failed == 1 and "EXTRACTION_FAILED" in (run.error_log or "")
    assert session.query(Report).count() == 0
    assert session.query(RawFinancialFact).count() == 0


def test_all_supplied_codal_pdfs_have_explicit_extraction_outcomes():
    pdfs = sorted(PDF_ROOT.glob("*.pdf"))
    assert pdfs
    outcomes = {}
    for path in pdfs:
        try:
            result = extract_raw_lines_from_pdf(path, title=path.name, report_type="CODAL", publication_datetime=datetime(2026, 9, 1))
            outcomes[path.name] = len(result.raw_lines)
        except CodalPdfExtractionError:
            outcomes[path.name] = None
    assert all(count is not None and count > 0 for count in outcomes.values())


def test_codal_raw_text_fields_are_ascii_normalized_before_persistence(ingestion_session):
    session, company, period = ingestion_session
    result = ingest_codal_report(
        session, company_id=company.company_id, period_id=period.period_id,
        report_type="گزارش ۱۴۰۴", title="فروش ۱۴۰۴/۰۶/۳۱",
        publication_datetime=datetime(2026, 9, 17, 12, 0, 0), codal_tracking_id="۱۲۳۴۵",
        source_url="https://example.test/report/۱۲۳۴۵",
        raw_lines=[RawLineInput(
            item_name="محصول ۱۲۳", item_code="کد ۴۵۶", unit="واحد ۷", currency="ریال ۸",
            source_section="بخش ۹", source_column="ستون ۱۰", value=Decimal("123.45"),
        )],
    )
    assert result.raw_fact_count == 1
    report = session.query(Report).filter_by(report_id=result.report_id).one()
    assert report.report_type == "گزارش 1404"
    assert report.title == "فروش 1404/06/31"
    assert report.codal_tracking_id == "12345"
    assert report.source_url == "https://example.test/report/12345"
    fact = session.query(RawFinancialFact).filter_by(report_version_id=result.report_version_id).one()
    assert fact.raw_item_name == "محصول 123"
    assert fact.raw_item_code == "کد 456"
    assert fact.unit == "واحد 7"
    assert fact.currency == "ریال 8"
    assert fact.source_section == "بخش 9"
    assert fact.source_column == "ستون 10"


def _independent_pdf_text_lines(path):
    from pypdf import PdfReader
    translation = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")
    lines = []
    for page in PdfReader(path).pages:
        for line in (page.extract_text() or "").splitlines():
            normalized = line.translate(translation).replace("٬", ",").replace("،", ",")
            normalized = " ".join(normalized.split())
            if normalized:
                lines.append(normalized)
    return lines


def _canonical_source_text(value):
    """Independent Unicode/RTL canonicalization; does not call production helpers."""
    if not value:
        return ""
    translation = str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789")
    text = unicodedata.normalize("NFKC", value).translate(translation)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Cf")
    text = text.replace("٬", ",").replace("،", ",")
    text = text.replace("ھ", "ه").replace("ي", "ی").replace("ى", "ی").replace("ك", "ک")
    return " ".join(text.split())


def _source_name_signature(value):
    """Create an order-independent alphabetic signature for RTL PDF text."""
    canonical = _canonical_source_text(value)
    return Counter(ch for ch in canonical if ch.isalpha())


def _name_traceable_to_source(name, line):
    """Require all name characters to occur in the same source line."""
    name_sig = _source_name_signature(name)
    line_sig = _source_name_signature(line)
    return bool(name_sig) and not name_sig - line_sig


def _value_tokens(value):
    if value is None:
        return []
    token = format(value, "f").rstrip("0").rstrip(".")
    return [token, f"({token.lstrip('-')})"] if token.startswith("-") else [token]


def test_golden_source_audit_reconciles_persisted_facts_with_independent_pdf_text(ingestion_session):
    """Persisted facts must be independently traceable to the PDF source text."""
    session, company, period = ingestion_session
    filenames = [
        "seo-codal-report (1).pdf", "seo-codal-report (3).pdf",
        "seo-codal-report (10).pdf", "seo-codal-report (13).pdf",
    ]
    for idx, filename in enumerate(filenames, start=1):
        result = ingest_codal_pdf(
            session, PDF_ROOT / filename, company_id=company.company_id, period_id=period.period_id,
            title=filename, report_type="CODAL_GOLDEN_AUDIT",
            publication_datetime=datetime(2026, 9, idx), codal_tracking_id=f"CODAL-GOLDEN-{idx}",
        )
        independent_lines = _independent_pdf_text_lines(PDF_ROOT / filename)
        assert independent_lines
        facts = session.query(RawFinancialFact).filter_by(report_version_id=result.report_version_id).all()
        assert facts
        for fact in facts:
            matching_lines = [line for line in independent_lines if _name_traceable_to_source(fact.raw_item_name, line)]
            assert matching_lines, f"{filename}: source row not found for {fact.raw_item_name!r}"
            if fact.value is not None:
                tokens = _value_tokens(fact.value)
                canonical_lines = [_canonical_source_text(line) for line in matching_lines]
                assert any(any(token in line for token in tokens) for line in canonical_lines), (
                    f"{filename}: persisted value {fact.value} is not traceable to source row {fact.raw_item_name!r}"
                )
            else:
                assert fact.value is None
            assert fact.currency == "IRR"
            assert fact.report_version_id == result.report_version_id
            assert fact.period_id == period.period_id


def test_representative_codal_samples_load_into_core_persistence(ingestion_session):
    session, company, period = ingestion_session
    filenames = [
        "seo-codal-report (1).pdf", "seo-codal-report (3).pdf",
        "seo-codal-report (10).pdf", "seo-codal-report (13).pdf",
    ]
    results = []
    for idx, filename in enumerate(filenames, start=1):
        results.append(ingest_codal_pdf(
            session, PDF_ROOT / filename, company_id=company.company_id, period_id=period.period_id,
            title=filename, report_type="CODAL_SAMPLE", publication_datetime=datetime(2026, 9, idx),
            codal_tracking_id=f"CODAL-PRODUCTION-SAMPLE-{idx}", source_url=f"local://{filename}",
        ))
    assert all(result.raw_fact_count > 0 for result in results)
    assert session.query(Report).count() == len(filenames)
    assert session.query(ReportVersion).count() == len(filenames)
    assert session.query(RawFinancialFact).count() == sum(r.raw_fact_count for r in results)
    runs = session.query(IngestionRun).filter_by(source="CODAL").all()
    assert len(runs) == len(filenames)
    assert all(run.status == "COMPLETED" for run in runs)


def test_independent_final_foundation_audit_checks_pit_provenance_and_version_invariants(ingestion_session):
    session, company, period = ingestion_session
    publication = datetime(2026, 9, 6, 12, 0)
    result = ingest_codal_pdf(
        session, PDF_ROOT / "seo-codal-report (3).pdf", company_id=company.company_id, period_id=period.period_id,
        title="Final audit sample", report_type="CODAL_FINAL_AUDIT", publication_datetime=publication,
        codal_tracking_id="CODAL-FINAL-AUDIT-1", source_url="local://seo-codal-report-3.pdf",
    )
    report = session.get(Report, result.report_id)
    assert report is not None
    assert report.company_id == company.company_id and report.financial_period_id == period.period_id
    assert report.codal_tracking_id == "CODAL-FINAL-AUDIT-1"
    assert report.source_url == "local://seo-codal-report-3.pdf"
    versions = session.query(ReportVersion).filter_by(report_id=report.report_id).order_by(ReportVersion.version_number).all()
    assert len(versions) == 1
    version = versions[0]
    assert version.publication_datetime == publication
    assert version.is_current_version is True and version.version_number == 1
    facts = session.query(RawFinancialFact).filter_by(report_version_id=version.report_version_id).order_by(RawFinancialFact.raw_fact_id).all()
    assert facts and len(facts) == result.raw_fact_count
    for fact in facts:
        assert fact.company_id == company.company_id and fact.period_id == period.period_id
        assert fact.report_version_id == version.report_version_id and fact.raw_item_name
        for value in (fact.raw_item_name, fact.raw_item_code, fact.unit, fact.currency, fact.source_section, fact.source_column):
            assert value is None or not any(ch in "۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩" for ch in value)
        assert fact.value is None or isinstance(fact.value, Decimal)
    assert version.publication_datetime <= publication
    later_cutoff = datetime(2026, 9, 5, 11, 59, 59)
    assert not (version.publication_datetime <= later_cutoff)
    current_count = session.query(ReportVersion).filter_by(report_id=report.report_id, is_current_version=True).count()
    assert current_count == 1
    run = session.get(IngestionRun, result.ingestion_id)
    assert run is not None and run.source == "CODAL" and run.status == "COMPLETED"
    assert run.records_inserted == len(facts) and run.records_failed == 0


def test_pdf_output_loads_into_core_persistence_and_duplicate_is_idempotent(ingestion_session):
    session, company, period = ingestion_session
    extraction = extract_raw_lines_from_pdf(
        PDF_ROOT / "seo-codal-report (1).pdf", title="Monthly sample", report_type="MONTHLY_ACTIVITY",
        publication_datetime=datetime(2026, 9, 1), codal_tracking_id="CODAL-IDEMPOTENT-1",
    )
    kwargs = dict(company_id=company.company_id, period_id=period.period_id, report_type=extraction.report_type,
                  title=extraction.title, publication_datetime=extraction.publication_datetime,
                  raw_lines=extraction.raw_lines, codal_tracking_id=extraction.codal_tracking_id)
    first = ingest_codal_report(session, **kwargs)
    second = ingest_codal_report(session, **kwargs)
    assert first.report_version_id == second.report_version_id
    assert session.query(ReportVersion).count() == 1
    assert session.query(RawFinancialFact).count() == first.raw_fact_count
    runs = session.query(IngestionRun).order_by(IngestionRun.ingestion_id).all()
    assert len(runs) == 2 and runs[1].records_updated == first.raw_fact_count


def test_golden_sample_rerun_is_byte_stable_and_does_not_create_new_version(ingestion_session):
    session, company, period = ingestion_session
    path = PDF_ROOT / "seo-codal-report (1).pdf"
    kwargs = dict(
        company_id=company.company_id, period_id=period.period_id, title="Golden monthly sample",
        report_type="MONTHLY_ACTIVITY", publication_datetime=datetime(2026, 9, 5, 12, 0),
        codal_tracking_id="CODAL-GOLDEN-IDEMPOTENT-1", source_url="local://seo-codal-report-1.pdf",
    )
    first = ingest_codal_pdf(session, path, **kwargs)
    def snapshot(version_id):
        return [(
            fact.raw_item_name, fact.raw_item_code, fact.value, fact.unit, fact.currency,
            fact.source_section, fact.source_row, fact.source_column, fact.period_id, fact.report_version_id,
        ) for fact in session.query(RawFinancialFact).filter_by(report_version_id=version_id).order_by(RawFinancialFact.raw_fact_id).all()]
    first_facts = snapshot(first.report_version_id)
    second = ingest_codal_pdf(session, path, **kwargs)
    assert second.report_id == first.report_id and second.report_version_id == first.report_version_id
    assert session.query(ReportVersion).count() == 1
    assert session.query(RawFinancialFact).count() == first.raw_fact_count
    assert first_facts == snapshot(second.report_version_id)
    runs = session.query(IngestionRun).order_by(IngestionRun.ingestion_id).all()
    assert len(runs) == 2 and all(run.status == "COMPLETED" for run in runs)
    assert runs[1].records_inserted == 0 and runs[1].records_updated == first.raw_fact_count


def test_codal_pdf_facade_connects_extraction_to_raw_persistence(ingestion_session):
    session, company, period = ingestion_session
    result = ingest_codal_pdf(
        session, PDF_ROOT / "seo-codal-report (10).pdf", company_id=company.company_id, period_id=period.period_id,
        title="Interim sample", report_type="INTERIM", publication_datetime=datetime(2026, 9, 2),
        codal_tracking_id="CODAL-FACADE-1", source_url="local://seo-codal-report-10.pdf",
    )
    assert result.raw_fact_count > 0
    report = session.get(Report, result.report_id)
    assert report.source_url == "local://seo-codal-report-10.pdf"
    assert session.query(RawFinancialFact).count() == result.raw_fact_count
