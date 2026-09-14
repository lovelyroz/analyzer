# Stage 1 — Data Foundation & Data Model tests
from datetime import date, datetime

import pytest
from sqlalchemy.exc import IntegrityError

from src.core.database import Base, SessionLocal, engine
from src.core.point_in_time import select_report_version
from src.models.audit import IngestionRun
from src.models.entity import Company, Industry
from src.models.fx import FXConversionRule, FXRate
from src.models.market import MarketDaily
from src.models.normalized import (
    FinancialMetric,
    NormalizedFinancialFact,
    RawFinancialFact,
)
from src.models.period import FinancialPeriod
from src.models.report import Report, ReportVersion
from src.models.share_action import CorporateAction, ShareCountHistory


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


def seed_company(session):
    industry = Industry(industry_code="BANK", industry_name="Bank")
    session.add(industry)
    session.flush()
    company = Company(
        ticker="TEST",
        company_name="Test Company",
        industry_id=industry.industry_id,
        codal_symbol="TEST",
    )
    session.add(company)
    session.flush()
    return company, industry


def seed_period(session, company_id, period_type="QUARTER"):
    period = FinancialPeriod(
        company_id=company_id,
        period_type=period_type,
        start_date=date(2024, 1, 1),
        end_date=date(2024, 3, 31),
        fiscal_year=1403,
        fiscal_quarter=1,
        months_length=3,
        is_ytd=False,
    )
    session.add(period)
    session.flush()
    return period


def test_all_stage1_tables_create(db_session):
    expected = {
        "companies",
        "industries",
        "financial_periods",
        "reports",
        "report_versions",
        "raw_financial_facts",
        "financial_metrics",
        "normalized_financial_facts",
        "fx_rates",
        "fx_conversion_rules",
        "market_daily",
        "share_count_history",
        "corporate_actions",
        "ingestion_runs",
    }
    assert expected.issubset(set(Base.metadata.tables))


def test_null_value_preservation_and_raw_provenance(db_session):
    company, _ = seed_company(db_session)
    period = seed_period(db_session, company.company_id)
    report = Report(
        company_id=company.company_id,
        report_type="QUARTERLY",
        title="Test report",
        financial_period_id=period.period_id,
    )
    db_session.add(report)
    db_session.flush()
    version = ReportVersion(
        report_id=report.report_id,
        version_number=1,
        publication_datetime=datetime(2024, 4, 15, 10, 0),
    )
    db_session.add(version)
    db_session.flush()
    raw = RawFinancialFact(
        company_id=company.company_id,
        report_version_id=version.report_version_id,
        period_id=period.period_id,
        raw_item_name="اقلام متفرقه",
        raw_item_code="X01",
        value=None,
        unit="IRR",
        currency="IRR",
        source_section="Income Statement",
        source_row=12,
        source_column="D",
    )
    db_session.add(raw)
    db_session.commit()

    saved = db_session.get(RawFinancialFact, raw.raw_fact_id)
    assert saved.value is None
    assert saved.raw_item_code == "X01"
    assert saved.source_section == "Income Statement"
    assert saved.source_row == 12
    assert saved.source_column == "D"


def test_financial_period_fk_and_type_constraints(db_session):
    company, _ = seed_company(db_session)
    period = seed_period(db_session, company.company_id, "TTM")
    assert period.period_type == "TTM"

    invalid_type = FinancialPeriod(
        company_id=company.company_id,
        period_type="INVALID",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 3, 31),
        fiscal_year=1403,
        months_length=3,
    )
    db_session.add(invalid_type)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()

    invalid_company = FinancialPeriod(
        company_id=999999,
        period_type="MONTH",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 1, 31),
        fiscal_year=1403,
        months_length=1,
    )
    db_session.add(invalid_company)
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_report_version_uniqueness_and_restatement_chain(db_session):
    company, _ = seed_company(db_session)
    period = seed_period(db_session, company.company_id)
    report = Report(
        company_id=company.company_id,
        report_type="QUARTERLY",
        title="Test report",
        financial_period_id=period.period_id,
    )
    db_session.add(report)
    db_session.flush()

    v1 = ReportVersion(
        report_id=report.report_id,
        version_number=1,
        publication_datetime=datetime(2024, 4, 15),
        is_current_version=False,
    )
    db_session.add(v1)
    db_session.flush()
    v2 = ReportVersion(
        report_id=report.report_id,
        version_number=2,
        publication_datetime=datetime(2024, 5, 20),
        is_current_version=True,
        is_restated=True,
        supersedes_version_id=v1.report_version_id,
    )
    db_session.add(v2)
    db_session.commit()

    assert v2.supersedes_version_id == v1.report_version_id
    duplicate = ReportVersion(
        report_id=report.report_id,
        version_number=2,
        publication_datetime=datetime(2024, 6, 1),
    )
    db_session.add(duplicate)
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_point_in_time_selector_never_uses_future_version(db_session):
    company, _ = seed_company(db_session)
    period = seed_period(db_session, company.company_id)
    report = Report(
        company_id=company.company_id,
        report_type="QUARTERLY",
        title="PIT report",
        financial_period_id=period.period_id,
    )
    db_session.add(report)
    db_session.flush()
    v1 = ReportVersion(
        report_id=report.report_id,
        version_number=1,
        publication_datetime=datetime(2024, 4, 15),
        is_current_version=False,
    )
    v2 = ReportVersion(
        report_id=report.report_id,
        version_number=2,
        publication_datetime=datetime(2024, 5, 20),
        is_current_version=True,
        is_restated=True,
        supersedes_version_id=1,
    )
    db_session.add_all([v1, v2])
    db_session.commit()

    before_v2 = select_report_version(db_session, report.report_id, datetime(2024, 5, 1))
    after_v2 = select_report_version(db_session, report.report_id, datetime(2024, 6, 1))
    before_first = select_report_version(db_session, report.report_id, datetime(2024, 4, 1))

    assert before_v2.version_number == 1
    assert after_v2.version_number == 2
    assert before_first is None


def test_fx_free_and_operational_are_distinct(db_session):
    today = date(2024, 4, 1)
    db_session.add_all(
        [
            FXRate(
                rate_date=today,
                currency_from="USD",
                currency_to="IRR",
                rate=600000,
                rate_type="FREE_MARKET",
                source="TEST",
            ),
            FXRate(
                rate_date=today,
                currency_from="USD",
                currency_to="IRR",
                rate=420000,
                rate_type="OPERATIONAL",
                source="TEST",
            ),
        ]
    )
    db_session.commit()
    assert db_session.query(FXRate).count() == 2

    db_session.add(
        FXConversionRule(
            metric_type="FLOW",
            conversion_method="PERIOD_AVG",
            rate_type="OPERATIONAL",
            description="Operational FX for flow metrics",
        )
    )
    db_session.commit()
    rule = db_session.query(FXConversionRule).one()
    assert rule.rate_type == "OPERATIONAL"
    assert rule.conversion_method == "PERIOD_AVG"


def test_quality_status_and_eps_metadata(db_session):
    company, _ = seed_company(db_session)
    period = seed_period(db_session, company.company_id)
    metric = FinancialMetric(
        metric_code="EPS",
        metric_name="Earnings per Share",
        category="PROFITABILITY",
        value_type="PER_SHARE_IRR",
        flow_or_stock="FLOW",
    )
    db_session.add(metric)
    db_session.flush()
    fact = NormalizedFinancialFact(
        company_id=company.company_id,
        period_id=period.period_id,
        metric_id=metric.metric_id,
        value_irr=1000,
        source_report_version_id=1,
        quality_status="VALID",
    )
    # The provenance FK is intentionally not committed here; metadata is tested separately.
    assert metric.value_type == "PER_SHARE_IRR"
    assert fact.quality_status == "VALID"

    bad = NormalizedFinancialFact(
        company_id=company.company_id,
        period_id=period.period_id,
        metric_id=metric.metric_id,
        source_report_version_id=1,
        quality_status="BAD_STATUS",
    )
    db_session.add(bad)
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_market_daily_allows_missing_adjusted_close_and_keeps_source(db_session):
    company, _ = seed_company(db_session)
    row = MarketDaily(
        company_id=company.company_id,
        trade_date=date(2024, 4, 1),
        close_price=1000,
        adjusted_close=None,
        source="TEST_OHLC",
    )
    db_session.add(row)
    db_session.commit()
    saved = db_session.query(MarketDaily).one()
    assert saved.adjusted_close is None
    assert saved.source == "TEST_OHLC"


def test_share_history_and_corporate_action_fields(db_session):
    company, _ = seed_company(db_session)
    shares = ShareCountHistory(
        company_id=company.company_id,
        effective_date=date(2024, 4, 1),
        shares_outstanding=1_000_000,
        capital=10_000_000_000,
        source="TEST",
    )
    action = CorporateAction(
        company_id=company.company_id,
        announcement_date=date(2024, 3, 20),
        effective_date=date(2024, 4, 1),
        action_type="CAPITAL_INCREASE",
        old_share_count=1_000_000,
        new_share_count=1_500_000,
        ratio=0.5,
        source="TEST",
    )
    db_session.add_all([shares, action])
    db_session.commit()
    assert shares.new_share_count if False else action.new_share_count == 1_500_000
    assert action.ratio == 0.5


def test_ingestion_run_contract(db_session):
    run = IngestionRun(
        source="CODAL",
        status="COMPLETED",
        records_found=10,
        records_inserted=9,
        records_updated=1,
        records_failed=0,
        finished_at=datetime.utcnow(),
    )
    db_session.add(run)
    db_session.commit()
    saved = db_session.get(IngestionRun, run.ingestion_id)
    assert saved.source == "CODAL"
    assert saved.records_found == 10
    assert saved.records_inserted == 9


def test_normalization_does_not_mutate_raw_fact(db_session):
    company, _ = seed_company(db_session)
    period = seed_period(db_session, company.company_id)
    report = Report(
        company_id=company.company_id,
        report_type="QUARTERLY",
        title="Raw preservation",
        financial_period_id=period.period_id,
    )
    db_session.add(report)
    db_session.flush()
    version = ReportVersion(
        report_id=report.report_id,
        version_number=1,
        publication_datetime=datetime(2024, 4, 15),
    )
    db_session.add(version)
    db_session.flush()
    raw = RawFinancialFact(
        company_id=company.company_id,
        report_version_id=version.report_version_id,
        period_id=period.period_id,
        raw_item_name="Revenue",
        raw_item_code="REV",
        value=123456,
        unit="IRR",
        currency="IRR",
    )
    db_session.add(raw)
    db_session.commit()
    raw_value_before = raw.value

    metric = FinancialMetric(
        metric_code="REVENUE",
        metric_name="Revenue",
        category="GROWTH",
        value_type="CURRENCY_IRR",
        flow_or_stock="FLOW",
    )
    db_session.add(metric)
    db_session.flush()
    normalized = NormalizedFinancialFact(
        company_id=company.company_id,
        period_id=period.period_id,
        metric_id=metric.metric_id,
        value_irr=123456,
        source_report_version_id=version.report_version_id,
        quality_status="VALID",
    )
    db_session.add(normalized)
    db_session.commit()
    db_session.refresh(raw)
    assert raw.value == raw_value_before
    assert raw.raw_item_name == "Revenue"
