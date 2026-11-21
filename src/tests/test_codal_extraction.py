"""CODAL shared persistence contracts using already parsed source rows."""

from datetime import date, datetime, timedelta
from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.database import Base
from src.core.point_in_time import select_report_version
from src.ingestion.service import RawLineInput, ingest_codal_report
from src.migrations.runner import MigrationRunner
from src.models.audit import IngestionRun
from src.models.entity import Company, Industry
from src.models.normalized import RawFinancialFact
from src.models.period import FinancialPeriod
from src.models.report import Report, ReportVersion


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    MigrationRunner(engine).upgrade()
    session = sessionmaker(bind=engine)()
    industry = Industry(industry_code="BANK", industry_name="Bank")
    session.add(industry)
    session.flush()
    company = Company(ticker="TEST", company_name="Test Co", industry_id=industry.industry_id, codal_symbol="TEST")
    session.add(company)
    session.flush()
    period = FinancialPeriod(
        company_id=company.company_id,
        period_type="QUARTER",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 3, 31),
        fiscal_year=1403,
        fiscal_quarter=1,
        months_length=3,
        is_ytd=False,
    )
    session.add(period)
    session.commit()
    session.test_company_id = company.company_id
    session.test_period_id = period.period_id
    yield session
    session.close()
    engine.dispose()


def _ingest(session, *, published, lines, tracking="CODAL-CONTRACT-1", company_id=None, period_id=None):
    return ingest_codal_report(
        session,
        company_id=company_id or session.test_company_id,
        period_id=period_id or session.test_period_id,
        report_type="QUARTERLY",
        title="Quarterly report",
        publication_datetime=published,
        codal_tracking_id=tracking,
        source_url="https://example.test/report/123",
        raw_lines=lines,
    )


def test_raw_persistence_preserves_null_zero_digits_and_provenance(session):
    result = _ingest(
        session,
        published=datetime(2024, 4, 15, 10),
        lines=[
            RawLineInput(item_name="مبلغ ۱۲۳", value=None, item_code="کد ۴۵", unit="واحد ۶", currency="ریال ۷", source_section="بخش ۸", source_row=9, source_column="ستون ۱۰"),
            RawLineInput(item_name="صفر", value=Decimal("0"), source_column="۲"),
        ],
    )
    report = session.get(Report, result.report_id)
    version = session.get(ReportVersion, result.report_version_id)
    facts = session.query(RawFinancialFact).filter_by(report_version_id=version.report_version_id).order_by(RawFinancialFact.raw_fact_id).all()
    run = session.get(IngestionRun, result.ingestion_id)

    assert report.source_url == "https://example.test/report/123"
    assert version.version_number == 1 and version.is_current_version is True
    assert facts[0].raw_item_name == "مبلغ 123"
    assert facts[0].raw_item_code == "کد 45"
    assert facts[0].unit == "واحد 6" and facts[0].currency == "ریال 7"
    assert facts[0].source_section == "بخش 8" and facts[0].source_row == 9
    assert facts[0].source_column == "ستون 10" and facts[0].value is None
    assert facts[1].value == Decimal("0")
    assert run.source == "CODAL" and run.status == "COMPLETED"
    assert run.records_inserted == 2 and result.raw_fact_count == 2


def test_same_tracking_id_and_publication_replays_existing_version(session):
    published = datetime(2024, 4, 15, 10)
    lines = [RawLineInput(item_name="revenue", value=Decimal("125.50"))]
    first = _ingest(session, published=published, lines=lines)
    replay = _ingest(session, published=published, lines=lines)

    assert first.report_id == replay.report_id
    assert first.report_version_id == replay.report_version_id
    assert session.query(Report).count() == 1
    assert session.query(ReportVersion).count() == 1
    assert session.query(RawFinancialFact).count() == 1
    runs = session.query(IngestionRun).order_by(IngestionRun.ingestion_id).all()
    assert [run.status for run in runs] == ["COMPLETED", "COMPLETED"]
    assert runs[1].records_updated == 1 and runs[1].records_inserted == 0


def test_later_publication_preserves_version_history_and_point_in_time_selection(session):
    first_time = datetime(2024, 4, 15, 10)
    second_time = datetime(2024, 5, 15, 10)
    first = _ingest(session, published=first_time, lines=[RawLineInput(item_name="revenue", value=Decimal("10"))])
    second = _ingest(session, published=second_time, lines=[RawLineInput(item_name="revenue", value=Decimal("12"))])
    versions = session.query(ReportVersion).filter_by(report_id=first.report_id).order_by(ReportVersion.version_number).all()

    assert len(versions) == 2
    assert versions[0].is_current_version is False
    assert versions[1].is_current_version is True and versions[1].version_number == 2
    assert versions[1].supersedes_version_id == versions[0].report_version_id
    assert session.query(RawFinancialFact).filter_by(report_version_id=versions[0].report_version_id).one().value == Decimal("10")
    assert session.query(RawFinancialFact).filter_by(report_version_id=versions[1].report_version_id).one().value == Decimal("12")
    assert select_report_version(session, first.report_id, first_time - timedelta(seconds=1)) is None
    assert select_report_version(session, first.report_id, first_time).report_version_id == first.report_version_id
    assert select_report_version(session, second.report_id, second_time).report_version_id == second.report_version_id


def test_wrong_company_period_fails_without_partial_business_rows(session):
    industry = session.query(Industry).one()
    other = Company(ticker="OTHER", company_name="Other Co", industry_id=industry.industry_id, codal_symbol="OTHER")
    session.add(other)
    session.flush()
    other_period = FinancialPeriod(
        company_id=other.company_id, period_type="QUARTER", start_date=date(2024, 1, 1),
        end_date=date(2024, 3, 31), fiscal_year=1403, fiscal_quarter=1, months_length=3, is_ytd=False,
    )
    session.add(other_period)
    session.commit()

    with pytest.raises(ValueError, match="period company_id does not match"):
        _ingest(session, published=datetime(2024, 4, 15), lines=[RawLineInput(item_name="row")], period_id=other_period.period_id)

    assert session.query(Report).count() == 0
    assert session.query(ReportVersion).count() == 0
    assert session.query(RawFinancialFact).count() == 0
    assert session.query(IngestionRun).filter_by(status="FAILED").count() == 1


def test_tracking_id_cannot_be_reused_for_another_company_or_period(session):
    _ingest(session, published=datetime(2024, 4, 15), lines=[RawLineInput(item_name="row")], tracking="CODAL-IDENTITY")
    industry = session.query(Industry).one()
    other = Company(ticker="OTHER", company_name="Other Co", industry_id=industry.industry_id, codal_symbol="OTHER")
    session.add(other)
    session.flush()
    period = FinancialPeriod(
        company_id=other.company_id, period_type="QUARTER", start_date=date(2024, 1, 1),
        end_date=date(2024, 3, 31), fiscal_year=1403, fiscal_quarter=1, months_length=3, is_ytd=False,
    )
    session.add(period)
    session.commit()

    with pytest.raises(ValueError, match="tracking ID is already assigned"):
        _ingest(session, published=datetime(2024, 5, 15), lines=[RawLineInput(item_name="row")], tracking="CODAL-IDENTITY", company_id=other.company_id, period_id=period.period_id)

    assert session.query(Report).count() == 1
    assert session.query(ReportVersion).count() == 1
    assert session.query(RawFinancialFact).count() == 1
    assert session.query(IngestionRun).filter_by(status="FAILED").count() == 1


def test_commit_failure_rolls_back_business_rows_and_records_failed_run(session, monkeypatch):
    original_commit = session.commit
    calls = 0

    def fail_first_commit():
        nonlocal calls
        calls += 1
        if calls == 1:
            raise RuntimeError("simulated commit failure")
        return original_commit()

    monkeypatch.setattr(session, "commit", fail_first_commit)
    with pytest.raises(RuntimeError, match="simulated commit failure"):
        _ingest(
            session,
            published=datetime(2024, 4, 15),
            lines=[RawLineInput(item_name="row", value=Decimal("1"))],
            tracking="CODAL-ROLLBACK",
        )

    assert session.query(Report).count() == 0
    assert session.query(ReportVersion).count() == 0
    assert session.query(RawFinancialFact).count() == 0
    failed = session.query(IngestionRun).filter_by(status="FAILED").one()
    assert failed.error_log == "simulated commit failure"
