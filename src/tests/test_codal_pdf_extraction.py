from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path

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

# Locked validation corpus from codal_19_pdf_validation_plan.md / matrix.md.
# Inventory must fail with SCOPE_ERROR if this set drifts.
LOCKED_CODAL_VALIDATION_CORPUS = frozenset(
    {
        "seo-codal-report (1).pdf",
        "seo-codal-report (2).pdf",
        "seo-codal-report (3).pdf",
        "seo-codal-report (4).pdf",
        "seo-codal-report (6).pdf",
        "seo-codal-report (7).pdf",
        "seo-codal-report (8).pdf",
        "seo-codal-report (9).pdf",
        "seo-codal-report (10).pdf",
        "seo-codal-report (11).pdf",
        "seo-codal-report (12).pdf",
        "seo-codal-report (13).pdf",
        "seo-codal-report (14).pdf",
        "seo-codal-report (15).pdf",
        "seo-codal-report (16).pdf",
        "seo-codal-report (19).pdf",
        "seo-codal-report (20).pdf",
        "seo-codal-report (25).pdf",
        "seo-codal-report (26).pdf",
    }
)


def test_codal_validation_corpus_inventory_is_exactly_locked_19_pdfs():
    """SCOPE gate: validation corpus must be exactly the locked 19-PDF set."""
    assert PDF_ROOT.is_dir(), f"SCOPE_ERROR: PDF root missing: {PDF_ROOT}"
    present = {path.name for path in PDF_ROOT.glob("*.pdf")}
    missing = LOCKED_CODAL_VALIDATION_CORPUS - present
    unexpected = present - LOCKED_CODAL_VALIDATION_CORPUS
    assert not missing and not unexpected and len(present) == 19, (
        "SCOPE_ERROR: CODAL validation corpus drifted from the locked 19-PDF set. "
        f"expected_count=19 actual_count={len(present)} "
        f"missing={sorted(missing)} unexpected={sorted(unexpected)}"
    )


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


def _normalized_raw_line_snapshot(raw_lines):
    """Comparable, field-stable view of extraction output for determinism checks."""
    return tuple(
        (
            line.item_name,
            line.value,
            line.item_code,
            line.unit,
            line.currency,
            line.source_section,
            line.source_row,
            line.source_column,
        )
        for line in raw_lines
    )


def test_representative_monthly_codal_pdf_returns_raw_dto_contract():
    """DTO/metadata contract for one monthly sample; corpus determinism is separate."""
    path = PDF_ROOT / "seo-codal-report (1).pdf"
    result = extract_raw_lines_from_pdf(
        path,
        title="sample",
        report_type="MONTHLY_ACTIVITY",
        publication_datetime=datetime(2026, 9, 1),
        codal_tracking_id="CODAL-SAMPLE-1",
        source_url="https://example.invalid/codal/sample-1",
    )
    assert result.raw_lines
    assert all(isinstance(line, RawLineInput) for line in result.raw_lines)
    assert result.codal_tracking_id == "CODAL-SAMPLE-1"
    assert result.source_url.endswith("sample-1")
    assert result.publication_datetime == datetime(2026, 9, 1)
    assert all(line.item_name for line in result.raw_lines)


@pytest.mark.parametrize("filename", sorted(LOCKED_CODAL_VALIDATION_CORPUS))
def test_locked_codal_corpus_extraction_is_deterministic_across_three_independent_runs(
    filename,
):
    """Layer F: three independent extractions per locked PDF must yield A == B == C."""
    path = PDF_ROOT / filename
    kwargs = dict(
        title=filename,
        report_type="CODAL",
        publication_datetime=datetime(2026, 9, 1),
        codal_tracking_id=f"CODAL-DET-{filename}",
        source_url=f"local://determinism/{filename}",
    )
    result_a = extract_raw_lines_from_pdf(path, **kwargs)
    result_b = extract_raw_lines_from_pdf(path, **kwargs)
    result_c = extract_raw_lines_from_pdf(path, **kwargs)
    snap_a = _normalized_raw_line_snapshot(result_a.raw_lines)
    snap_b = _normalized_raw_line_snapshot(result_b.raw_lines)
    snap_c = _normalized_raw_line_snapshot(result_c.raw_lines)
    assert snap_a, f"empty extraction for {filename}"
    assert snap_a == snap_b == snap_c, (
        f"NONDETERMINISTIC_EXTRACTION: independent runs A/B/C diverge for {filename}. "
        f"len_a={len(snap_a)} len_b={len(snap_b)} len_c={len(snap_c)}"
    )


@pytest.mark.parametrize(
    "filename",
    [path.name for path in sorted(PDF_ROOT.glob("*.pdf"))],
)
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


def test_representative_codal_samples_load_into_core_persistence(ingestion_session):
    session, company, period = ingestion_session
    filenames = [path.name for path in sorted(PDF_ROOT.glob("*.pdf"))]
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
    """
    Final audit: PDF -> production ingestion -> persisted foundation invariants.

    Source of truth is the database contract/invariants, not a second PDF
    parser. A true Golden Data Audit will be added only after an independently
    verified expected dataset exists in the repository.
    """
    session, company, period = ingestion_session
    publication = datetime(2026, 9, 6, 12, 0)
    result = ingest_codal_pdf(
        session, PDF_ROOT / "seo-codal-report (3).pdf",
        company_id=company.company_id, period_id=period.period_id,
        title="Final audit sample", report_type="CODAL_FINAL_AUDIT",
        publication_datetime=publication, codal_tracking_id="CODAL-FINAL-AUDIT-1",
        source_url="local://seo-codal-report-3.pdf",
    )
    report = session.get(Report, result.report_id)
    assert report is not None
    assert report.company_id == company.company_id
    assert report.financial_period_id == period.period_id
    assert report.codal_tracking_id == "CODAL-FINAL-AUDIT-1"
    assert report.source_url == "local://seo-codal-report-3.pdf"

    versions = session.query(ReportVersion).filter_by(report_id=report.report_id).order_by(ReportVersion.version_number).all()
    assert len(versions) == 1
    version = versions[0]
    assert version.publication_datetime == publication
    assert version.is_current_version is True
    assert version.version_number == 1

    facts = session.query(RawFinancialFact).filter_by(report_version_id=version.report_version_id).order_by(RawFinancialFact.raw_fact_id).all()
    assert facts
    assert len(facts) == result.raw_fact_count

    def contains_non_ascii_digit(value):
        return any("۰" <= char <= "۹" or "٠" <= char <= "٩" for char in (value or ""))

    for fact in facts:
        assert fact.company_id == company.company_id
        assert fact.period_id == period.period_id
        assert fact.report_version_id == version.report_version_id
        assert fact.raw_item_name
        assert not contains_non_ascii_digit(fact.raw_item_name)
        assert not contains_non_ascii_digit(fact.raw_item_code)
        assert not contains_non_ascii_digit(fact.unit)
        assert not contains_non_ascii_digit(fact.currency)
        assert not contains_non_ascii_digit(fact.source_section)
        assert not contains_non_ascii_digit(fact.source_column)
        assert fact.value is None or isinstance(fact.value, Decimal)

    assert version.publication_datetime <= publication
    earlier_cutoff = publication - timedelta(seconds=1)
    assert version.publication_datetime > earlier_cutoff

    current_count = session.query(ReportVersion).filter_by(report_id=report.report_id, is_current_version=True).count()
    assert current_count == 1

    run = session.get(IngestionRun, result.ingestion_id)
    assert run is not None
    assert run.source == "CODAL"
    assert run.status == "COMPLETED"
    assert run.records_inserted == len(facts)
    assert run.records_failed == 0


def test_pdf_output_loads_into_core_persistence_and_duplicate_is_idempotent(ingestion_session):
    session, company, period = ingestion_session
    extraction = extract_raw_lines_from_pdf(
        PDF_ROOT / "seo-codal-report (1).pdf",
        title="Monthly sample", report_type="MONTHLY_ACTIVITY",
        publication_datetime=datetime(2026, 9, 1), codal_tracking_id="CODAL-IDEMPOTENT-1",
    )
    first = ingest_codal_report(
        session, company_id=company.company_id, period_id=period.period_id,
        report_type=extraction.report_type, title=extraction.title,
        publication_datetime=extraction.publication_datetime,
        raw_lines=extraction.raw_lines, codal_tracking_id=extraction.codal_tracking_id,
    )
    second = ingest_codal_report(
        session, company_id=company.company_id, period_id=period.period_id,
        report_type=extraction.report_type, title=extraction.title,
        publication_datetime=extraction.publication_datetime,
        raw_lines=extraction.raw_lines, codal_tracking_id=extraction.codal_tracking_id,
    )
    assert first.report_version_id == second.report_version_id
    assert session.query(ReportVersion).count() == 1
    assert session.query(RawFinancialFact).count() == first.raw_fact_count
    runs = session.query(IngestionRun).order_by(IngestionRun.ingestion_id).all()
    assert len(runs) == 2
    assert runs[1].records_updated == first.raw_fact_count


def _persisted_fact_snapshot(session):
    """Full logical-state snapshot of RawFinancialFact for drift detection.

    Captures the actual persisted values (not just row counts) so that value
    drift, provenance drift and duplicate facts are all detectable across
    repeated ingestion cycles. Ordering by raw_fact_id makes the tuple stable.
    """
    facts = session.query(RawFinancialFact).order_by(RawFinancialFact.raw_fact_id).all()
    return tuple(
        (
            fact.report_version_id,
            fact.raw_item_name,
            fact.raw_item_code,
            fact.value,
            fact.unit,
            fact.currency,
            fact.source_section,
            fact.source_row,
            fact.source_column,
        )
        for fact in facts
    )


@pytest.mark.parametrize("filename", sorted(LOCKED_CODAL_VALIDATION_CORPUS))
def test_locked_codal_corpus_ingestion_is_idempotent_across_three_cycles(
    filename, ingestion_session
):
    """Layer E: three ingestion cycles per locked PDF must leave logical state unchanged.

    The idempotency key in ingest_codal_report() is (codal_tracking_id,
    publication_datetime). After the first successful ingestion, cycles 2 and 3
    must reuse the same ReportVersion and must not duplicate RawFinancialFact
    rows or drift values/provenance. This is corpus-wide (all 19 locked PDFs),
    unlike the single-sample idempotency test above.
    """
    session, company, period = ingestion_session
    path = PDF_ROOT / filename
    tracking_id = f"CODAL-IDEM-{filename}"

    extraction = extract_raw_lines_from_pdf(
        path,
        title=filename,
        report_type="CODAL",
        publication_datetime=datetime(2026, 9, 1),
        codal_tracking_id=tracking_id,
        source_url=f"local://idempotency/{filename}",
    )
    assert extraction.raw_lines, f"empty extraction for {filename}"

    ingest_kwargs = dict(
        session=session,
        company_id=company.company_id,
        period_id=period.period_id,
        report_type=extraction.report_type,
        title=extraction.title,
        publication_datetime=extraction.publication_datetime,
        raw_lines=extraction.raw_lines,
        codal_tracking_id=extraction.codal_tracking_id,
        source_url=extraction.source_url,
    )

    # Cycle 1: creates the Report, one current ReportVersion and the raw facts.
    first = ingest_codal_report(**ingest_kwargs)
    expected_version_id = first.report_version_id
    expected_fact_count = first.raw_fact_count
    assert expected_fact_count > 0, f"no facts persisted for {filename}"

    snapshot_after_cycle_1 = _persisted_fact_snapshot(session)
    assert len(snapshot_after_cycle_1) == expected_fact_count

    # Cycles 2 and 3 must reuse the same version (no new ReportVersion).
    second = ingest_codal_report(**ingest_kwargs)
    third = ingest_codal_report(**ingest_kwargs)
    assert second.report_version_id == expected_version_id
    assert third.report_version_id == expected_version_id

    # No unintended ReportVersions and still exactly one current version.
    assert session.query(ReportVersion).count() == 1, (
        f"DUPLICATE_REPORT_VERSION: repeated ingestion created extra versions for {filename}"
    )
    assert (
        session.query(ReportVersion)
        .filter_by(report_id=first.report_id, is_current_version=True)
        .count()
        == 1
    )

    # No duplicate RawFinancialFact rows and no value/provenance drift.
    # The snapshot is keyed by raw_fact_id (physical insertion order), so an
    # exact snapshot equality proves both that no rows were appended and that
    # no persisted field (value, unit, currency, provenance) drifted. A
    # natural key of (row, column, name) is deliberately NOT used: real CODAL
    # statements legitimately repeat the same label in the same column across
    # sections, so it is not a uniqueness key for this corpus.
    snapshot_after_cycle_3 = _persisted_fact_snapshot(session)
    assert len(snapshot_after_cycle_3) == expected_fact_count, (
        f"DUPLICATE_FACT: fact count changed after repeated ingestion of {filename}: "
        f"cycle1={expected_fact_count} cycle3={len(snapshot_after_cycle_3)}"
    )
    assert snapshot_after_cycle_3 == snapshot_after_cycle_1, (
        f"IDEMPOTENCY_FAILURE: persisted fact state drifted after repeated "
        f"ingestion of {filename}"
    )

    # Exactly one Report for the tracking id; the version and facts are reused.
    assert session.query(Report).count() == 1
    assert session.query(RawFinancialFact).count() == expected_fact_count


def _assert_facts_satisfy_hard_invariants(facts, company, period, version):
    """The hard financial-data invariants, applied to a single PDF's facts.

    Returns the set of distinct (item_name, unit, currency) tuples so callers
    can assert corpus-level uniqueness properties when they hold.
    """
    seen_identity_tuples = set()
    for fact in facts:
        # FK / provenance integrity: every fact belongs to the right chain.
        assert fact.company_id == company.company_id
        assert fact.period_id == period.period_id
        assert fact.report_version_id == version.report_version_id

        # ASCII normalization: Persian/Arabic digits must not persist.
        assert fact.raw_item_name, "empty raw_item_name"
        for field in (
            fact.raw_item_name,
            fact.raw_item_code,
            fact.unit,
            fact.currency,
            fact.source_section,
            fact.source_column,
        ):
            assert not any(
                "۰" <= char <= "۹" or "٠" <= char <= "٩" for char in (field or "")
            ), f"non-ASCII digit persisted in {field!r}"

        # NULL != 0: value is either an explicit Decimal or absent, never
        # a silent coercion. (None is allowed; a Decimal("0") is explicit.)
        assert fact.value is None or isinstance(fact.value, Decimal)

        # Provenance position is preserved where the extractor recorded it.
        assert fact.source_row is None or isinstance(fact.source_row, int)

        seen_identity_tuples.add((fact.raw_item_name, fact.unit, fact.currency))
    return seen_identity_tuples


@pytest.mark.parametrize("filename", sorted(LOCKED_CODAL_VALIDATION_CORPUS))
def test_locked_codal_corpus_persistence_satisfies_hard_invariants(
    filename, ingestion_session
):
    """Layer B/C: deep per-PDF persistence invariants over the full corpus.

    The existing final-audit test checks these invariants for exactly one PDF
    (seo-codal-report (3).pdf), while the aggregate load test only counts rows
    for all 19. A single PDF with broken provenance, a non-ASCII field or a
    NULL->zero coercion would pass the aggregate count check silently. This
    parametrized test applies the hard invariants to each PDF independently.
    """
    session, company, period = ingestion_session
    publication = datetime(2026, 9, 1, 12, 0)
    result = ingest_codal_pdf(
        session,
        PDF_ROOT / filename,
        company_id=company.company_id,
        period_id=period.period_id,
        title=filename,
        report_type="CODAL_PERSIST",
        publication_datetime=publication,
        codal_tracking_id=f"CODAL-PERSIST-{filename}",
        source_url=f"local://persistence/{filename}",
    )
    assert result.raw_fact_count > 0, f"no facts persisted for {filename}"

    # Report identity and provenance are preserved per PDF.
    report = session.get(Report, result.report_id)
    assert report is not None
    assert report.company_id == company.company_id
    assert report.financial_period_id == period.period_id
    assert report.codal_tracking_id == f"CODAL-PERSIST-{filename}"
    assert report.source_url == f"local://persistence/{filename}"

    # Exactly one current ReportVersion; PIT bookkeeping is intact.
    versions = (
        session.query(ReportVersion)
        .filter_by(report_id=report.report_id)
        .order_by(ReportVersion.version_number)
        .all()
    )
    assert len(versions) == 1, f"unexpected version count for {filename}"
    version = versions[0]
    assert version.publication_datetime == publication
    assert version.is_current_version is True
    assert version.version_number == 1
    current_count = (
        session.query(ReportVersion)
        .filter_by(report_id=report.report_id, is_current_version=True)
        .count()
    )
    assert current_count == 1

    # Facts satisfy the hard invariants for this PDF.
    facts = (
        session.query(RawFinancialFact)
        .filter_by(report_version_id=version.report_version_id)
        .order_by(RawFinancialFact.raw_fact_id)
        .all()
    )
    assert len(facts) == result.raw_fact_count
    _assert_facts_satisfy_hard_invariants(facts, company, period, version)

    # The ingestion run is complete and fully accounts for the facts.
    run = session.get(IngestionRun, result.ingestion_id)
    assert run is not None
    assert run.source == "CODAL"
    assert run.status == "COMPLETED"
    assert run.records_inserted == len(facts)
    assert run.records_failed == 0


def test_codal_pdf_facade_connects_extraction_to_raw_persistence(ingestion_session):
    session, company, period = ingestion_session
    result = ingest_codal_pdf(
        session, PDF_ROOT / "seo-codal-report (10).pdf",
        company_id=company.company_id, period_id=period.period_id,
        title="Interim sample", report_type="INTERIM",
        publication_datetime=datetime(2026, 9, 2),
        codal_tracking_id="CODAL-FACADE-1",
        source_url="local://seo-codal-report-10.pdf",
    )
    assert result.raw_fact_count > 0
    report = session.get(Report, result.report_id)
    assert report.source_url == "local://seo-codal-report-10.pdf"
    assert session.query(RawFinancialFact).count() == result.raw_fact_count
