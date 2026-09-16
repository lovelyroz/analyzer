# Stage 1 — Data Foundation & Data Model tests
from datetime import date, datetime
from decimal import Decimal

import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy import create_engine, inspect, text

from src.core.database import Base, SessionLocal, engine
from src.core.point_in_time import select_report_version
from src.ingestion.service import RawLineInput, ingest_codal_report
from src.models.audit import IngestionRun
from src.models.entity import Company, Industry
from src.models.fx import FXConversionRule, FXRate
from src.models.market import MarketDaily
from src.models.normalized import (
    FinancialMetric,
    DerivedFinancialFact,
    DerivedFinancialFactInput,
    MappingDecision,
    MappingRule,
    NormalizedFinancialFact,
    RawFinancialFact,
)
from src.models.period import FinancialPeriod
from src.models.report import Report, ReportVersion
from src.models.share_action import CorporateAction, ShareCountHistory
from src.migrations.runner import MigrationRunner


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
        "companies", "industries", "financial_periods", "reports", "report_versions",
        "raw_financial_facts", "financial_metrics", "mapping_rules", "mapping_decisions",
        "normalized_financial_facts", "derived_financial_facts", "derived_financial_fact_inputs",
        "fx_rates", "fx_conversion_rules", "market_daily", "share_count_history",
        "corporate_actions", "ingestion_runs",
    }
    assert expected.issubset(set(Base.metadata.tables))


def test_null_value_preservation_and_raw_provenance(db_session):
    company, _ = seed_company(db_session)
    period = seed_period(db_session, company.company_id)
    report = Report(company_id=company.company_id, report_type="QUARTERLY", title="Test report", financial_period_id=period.period_id)
    db_session.add(report)
    db_session.flush()
    version = ReportVersion(report_id=report.report_id, version_number=1, publication_datetime=datetime(2024, 4, 15, 10, 0))
    db_session.add(version)
    db_session.flush()
    raw = RawFinancialFact(
        company_id=company.company_id, report_version_id=version.report_version_id, period_id=period.period_id,
        raw_item_name="اقلام متفرقه", raw_item_code="X01", value=None, unit="IRR", currency="IRR",
        source_section="Income Statement", source_row=12, source_column="D",
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
    invalid_type = FinancialPeriod(company_id=company.company_id, period_type="INVALID", start_date=date(2024, 1, 1), end_date=date(2024, 3, 31), fiscal_year=1403, months_length=3)
    db_session.add(invalid_type)
    with pytest.raises(IntegrityError):
        db_session.commit()
    db_session.rollback()
    invalid_company = FinancialPeriod(company_id=999999, period_type="MONTH", start_date=date(2024, 1, 1), end_date=date(2024, 1, 31), fiscal_year=1403, months_length=1)
    db_session.add(invalid_company)
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_report_version_uniqueness_and_restatement_chain(db_session):
    company, _ = seed_company(db_session)
    period = seed_period(db_session, company.company_id)
    report = Report(company_id=company.company_id, report_type="QUARTERLY", title="Test report", financial_period_id=period.period_id)
    db_session.add(report)
    db_session.flush()
    v1 = ReportVersion(report_id=report.report_id, version_number=1, publication_datetime=datetime(2024, 4, 15), is_current_version=False)
    db_session.add(v1)
    db_session.flush()
    v2 = ReportVersion(report_id=report.report_id, version_number=2, publication_datetime=datetime(2024, 5, 20), is_current_version=True, is_restated=True, supersedes_version_id=v1.report_version_id)
    db_session.add(v2)
    db_session.commit()
    assert v2.supersedes_version_id == v1.report_version_id
    duplicate = ReportVersion(report_id=report.report_id, version_number=2, publication_datetime=datetime(2024, 6, 1))
    db_session.add(duplicate)
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_point_in_time_selector_never_uses_future_version(db_session):
    company, _ = seed_company(db_session)
    period = seed_period(db_session, company.company_id)
    report = Report(company_id=company.company_id, report_type="QUARTERLY", title="PIT report", financial_period_id=period.period_id)
    db_session.add(report)
    db_session.flush()
    v1 = ReportVersion(report_id=report.report_id, version_number=1, publication_datetime=datetime(2024, 4, 15), is_current_version=False)
    v2 = ReportVersion(report_id=report.report_id, version_number=2, publication_datetime=datetime(2024, 5, 20), is_current_version=True, is_restated=True, supersedes_version_id=1)
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
    db_session.add_all([
        FXRate(rate_date=today, currency_from="USD", currency_to="IRR", rate=600000, rate_type="FREE_MARKET", source="TEST"),
        FXRate(rate_date=today, currency_from="USD", currency_to="IRR", rate=420000, rate_type="OPERATIONAL", source="TEST"),
    ])
    db_session.commit()
    assert db_session.query(FXRate).count() == 2


def test_fx_conversion_rule_contracts(db_session):
    rules = [
        FXConversionRule(metric_type="FLOW", conversion_method="PERIOD_AVG", rate_type="OPERATIONAL", description="Flow uses period average operational FX"),
        FXConversionRule(metric_type="STOCK", conversion_method="PERIOD_END", rate_type="OPERATIONAL", description="Stock uses period-end operational FX"),
        FXConversionRule(metric_type="MARKET_VALUE", conversion_method="SAME_DATE", rate_type="FREE_MARKET", description="Market value uses same-date free-market FX"),
    ]
    db_session.add_all(rules)
    db_session.commit()
    saved = db_session.query(FXConversionRule).order_by(FXConversionRule.rule_id).all()
    assert [(r.metric_type, r.conversion_method, r.rate_type) for r in saved] == [
        ("FLOW", "PERIOD_AVG", "OPERATIONAL"),
        ("STOCK", "PERIOD_END", "OPERATIONAL"),
        ("MARKET_VALUE", "SAME_DATE", "FREE_MARKET"),
    ]


def test_quality_status_and_eps_metadata(db_session):
    company, _ = seed_company(db_session)
    period = seed_period(db_session, company.company_id)
    metric = FinancialMetric(metric_code="EPS", metric_name="Earnings per Share", category="PROFITABILITY", value_type="PER_SHARE_IRR", flow_or_stock="FLOW")
    db_session.add(metric)
    db_session.flush()
    report = Report(company_id=company.company_id, report_type="QUARTERLY", title="EPS source", financial_period_id=period.period_id)
    db_session.add(report)
    db_session.flush()
    version = ReportVersion(report_id=report.report_id, version_number=1, publication_datetime=datetime(2024, 4, 15))
    db_session.add(version)
    db_session.flush()
    fact = NormalizedFinancialFact(company_id=company.company_id, period_id=period.period_id, metric_id=metric.metric_id, value_irr=1000, source_report_version_id=version.report_version_id, quality_status="VALID")
    db_session.add(fact)
    db_session.commit()
    saved = db_session.get(NormalizedFinancialFact, fact.fact_id)
    assert saved.source_report_version_id == version.report_version_id
    assert saved.quality_status == "VALID"
    assert metric.value_type == "PER_SHARE_IRR"

    bad = NormalizedFinancialFact(company_id=company.company_id, period_id=period.period_id, metric_id=metric.metric_id, source_report_version_id=version.report_version_id, quality_status="BAD_STATUS")
    db_session.add(bad)
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_market_daily_allows_missing_adjusted_close_and_keeps_source(db_session):
    company, _ = seed_company(db_session)
    row = MarketDaily(company_id=company.company_id, trade_date=date(2024, 4, 1), close_price=1000, adjusted_close=None, source="TEST_OHLC")
    db_session.add(row)
    db_session.commit()
    saved = db_session.query(MarketDaily).one()
    assert saved.adjusted_close is None
    assert saved.source == "TEST_OHLC"


def test_share_history_and_corporate_action_fields(db_session):
    company, _ = seed_company(db_session)
    shares = ShareCountHistory(company_id=company.company_id, effective_date=date(2024, 4, 1), shares_outstanding=1_000_000, capital=10_000_000_000, source="TEST")
    action = CorporateAction(company_id=company.company_id, announcement_date=date(2024, 3, 20), effective_date=date(2024, 4, 1), action_type="CAPITAL_INCREASE", old_share_count=1_000_000, new_share_count=1_500_000, ratio=0.5, source="TEST")
    db_session.add_all([shares, action])
    db_session.commit()
    assert action.new_share_count == 1_500_000
    assert action.ratio == 0.5


def test_ingestion_run_contract(db_session):
    run = IngestionRun(source="CODAL", status="COMPLETED", records_found=10, records_inserted=9, records_updated=1, records_failed=0, finished_at=datetime.utcnow())
    db_session.add(run)
    db_session.commit()
    saved = db_session.get(IngestionRun, run.ingestion_id)
    assert saved.source == "CODAL"
    assert saved.records_found == 10
    assert saved.records_inserted == 9


def test_normalization_does_not_mutate_raw_fact(db_session):
    company, _ = seed_company(db_session)
    period = seed_period(db_session, company.company_id)
    report = Report(company_id=company.company_id, report_type="QUARTERLY", title="Raw preservation", financial_period_id=period.period_id)
    db_session.add(report)
    db_session.flush()
    version = ReportVersion(report_id=report.report_id, version_number=1, publication_datetime=datetime(2024, 4, 15))
    db_session.add(version)
    db_session.flush()
    raw = RawFinancialFact(company_id=company.company_id, report_version_id=version.report_version_id, period_id=period.period_id, raw_item_name="Revenue", raw_item_code="REV", value=123456, unit="IRR", currency="IRR")
    db_session.add(raw)
    db_session.commit()
    raw_value_before = raw.value
    metric = FinancialMetric(metric_code="REVENUE", metric_name="Revenue", category="GROWTH", value_type="CURRENCY_IRR", flow_or_stock="FLOW")
    db_session.add(metric)
    db_session.flush()
    normalized = NormalizedFinancialFact(company_id=company.company_id, period_id=period.period_id, metric_id=metric.metric_id, value_irr=123456, source_report_version_id=version.report_version_id, quality_status="VALID")
    db_session.add(normalized)
    db_session.commit()
    db_session.refresh(raw)
    assert raw.value == raw_value_before
    assert raw.raw_item_name == "Revenue"


def test_mapping_supports_many_raw_lines_to_one_standard_metric(db_session):
    company, _ = seed_company(db_session)
    period = seed_period(db_session, company.company_id)
    report = Report(
        company_id=company.company_id,
        report_type="QUARTERLY",
        title="Mapping test",
        financial_period_id=period.period_id,
    )
    db_session.add(report)
    db_session.flush()
    version = ReportVersion(
        report_id=report.report_id,
        version_number=1,
        publication_datetime=datetime(2024, 4, 15),
    )
    metric = FinancialMetric(
        metric_code="COGS",
        metric_name="Cost of goods sold",
        category="PROFITABILITY",
        statement_type="INCOME",
        flow_or_stock="FLOW",
        sign_convention="EXPENSE_POSITIVE",
    )
    rule = MappingRule(rule_code="income_statement_alias", rule_version="1.0")
    db_session.add_all([version, metric, rule])
    db_session.flush()
    raw_lines = [
        RawFinancialFact(
            company_id=company.company_id,
            report_version_id=version.report_version_id,
            period_id=period.period_id,
            raw_item_name="Direct materials",
            value=100,
        ),
        RawFinancialFact(
            company_id=company.company_id,
            report_version_id=version.report_version_id,
            period_id=period.period_id,
            raw_item_name="Factory overhead",
            value=40,
        ),
    ]
    db_session.add_all(raw_lines)
    db_session.flush()
    decisions = [
        MappingDecision(
            raw_fact_id=raw.raw_fact_id,
            metric_id=metric.metric_id,
            mapping_rule_id=rule.mapping_rule_id,
            mapping_method="ALIAS",
            confidence=95,
            review_status="APPROVED",
            composition_role="COMPONENT",
        )
        for raw in raw_lines
    ]
    db_session.add_all(decisions)
    db_session.commit()

    saved = db_session.query(MappingDecision).order_by(MappingDecision.mapping_decision_id).all()
    assert len(saved) == 2
    assert {decision.metric_id for decision in saved} == {metric.metric_id}
    assert all(decision.review_status == "APPROVED" for decision in saved)
    assert all(decision.composition_role == "COMPONENT" for decision in saved)


def test_unmapped_decision_is_preserved_but_not_normalized(db_session):
    company, _ = seed_company(db_session)
    period = seed_period(db_session, company.company_id)
    report = Report(
        company_id=company.company_id,
        report_type="QUARTERLY",
        title="Unmapped test",
        financial_period_id=period.period_id,
    )
    db_session.add(report)
    db_session.flush()
    version = ReportVersion(
        report_id=report.report_id,
        version_number=1,
        publication_datetime=datetime(2024, 4, 15),
    )
    raw = RawFinancialFact(
        company_id=company.company_id,
        report_version_id=version.report_version_id,
        period_id=period.period_id,
        raw_item_name="Unclassified disclosure",
        value=25,
    )
    db_session.add(version)
    db_session.flush()
    raw.report_version_id = version.report_version_id
    db_session.add(raw)
    db_session.flush()
    decision = MappingDecision(
        raw_fact_id=raw.raw_fact_id,
        mapping_method="MANUAL",
        confidence=20,
        review_status="UNMAPPED",
        note="Requires analyst review",
    )
    db_session.add(decision)
    db_session.commit()

    saved = db_session.query(MappingDecision).one()
    assert saved.metric_id is None
    assert saved.review_status == "UNMAPPED"
    assert db_session.query(NormalizedFinancialFact).count() == 0


def test_mapping_constraints_reject_invalid_confidence_and_status(db_session):
    company, _ = seed_company(db_session)
    period = seed_period(db_session, company.company_id)
    report = Report(
        company_id=company.company_id,
        report_type="QUARTERLY",
        title="Mapping constraint test",
        financial_period_id=period.period_id,
    )
    db_session.add(report)
    db_session.flush()
    version = ReportVersion(
        report_id=report.report_id,
        version_number=1,
        publication_datetime=datetime(2024, 4, 15),
    )
    raw = RawFinancialFact(
        company_id=company.company_id,
        report_version_id=version.report_version_id,
        period_id=period.period_id,
        raw_item_name="Invalid mapping",
        value=25,
    )
    db_session.add(version)
    db_session.flush()
    raw.report_version_id = version.report_version_id
    db_session.add(raw)
    db_session.flush()
    invalid = MappingDecision(
        raw_fact_id=raw.raw_fact_id,
        mapping_method="MANUAL",
        confidence=101,
        review_status="REVIEW_REQUIRED",
    )
    db_session.add(invalid)
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_derived_fact_keeps_formula_and_input_provenance(db_session):
    company, _ = seed_company(db_session)
    period = seed_period(db_session, company.company_id)
    report = Report(
        company_id=company.company_id,
        report_type="QUARTERLY",
        title="Derived fact test",
        financial_period_id=period.period_id,
    )
    db_session.add(report)
    db_session.flush()
    version = ReportVersion(
        report_id=report.report_id,
        version_number=1,
        publication_datetime=datetime(2024, 4, 15),
    )
    revenue = FinancialMetric(
        metric_code="REVENUE_DERIVED_TEST",
        metric_name="Revenue",
        category="GROWTH",
        statement_type="INCOME",
        flow_or_stock="FLOW",
    )
    gross_profit = FinancialMetric(
        metric_code="GROSS_PROFIT_DERIVED_TEST",
        metric_name="Gross profit",
        category="PROFITABILITY",
        statement_type="INCOME",
        flow_or_stock="FLOW",
        is_derived=True,
    )
    db_session.add_all([version, revenue, gross_profit])
    db_session.flush()
    raw = RawFinancialFact(
        company_id=company.company_id,
        report_version_id=version.report_version_id,
        period_id=period.period_id,
        raw_item_name="Revenue",
        value=150,
    )
    db_session.add(raw)
    db_session.flush()
    normalized = NormalizedFinancialFact(
        company_id=company.company_id,
        period_id=period.period_id,
        metric_id=revenue.metric_id,
        raw_fact_id=raw.raw_fact_id,
        value_irr=150,
        source_report_version_id=version.report_version_id,
        quality_status="VALID",
    )
    db_session.add(normalized)
    db_session.flush()
    derived = DerivedFinancialFact(
        company_id=company.company_id,
        period_id=period.period_id,
        metric_id=gross_profit.metric_id,
        value_irr=90,
        formula_code="GROSS_PROFIT_FROM_REVENUE_AND_COGS",
        formula_version="1.0",
        source_report_version_id=version.report_version_id,
        data_cutoff_datetime=datetime(2024, 4, 15),
    )
    db_session.add(derived)
    db_session.flush()
    db_session.add(DerivedFinancialFactInput(
        derived_fact_id=derived.derived_fact_id,
        normalized_fact_id=normalized.fact_id,
        input_role="REVENUE",
    ))
    db_session.commit()

    saved = db_session.query(DerivedFinancialFact).one()
    saved_input = db_session.query(DerivedFinancialFactInput).one()
    assert saved.value_irr == 90
    assert saved.formula_version == "1.0"
    assert saved_input.normalized_fact_id == normalized.fact_id


def test_derived_fact_input_requires_exactly_one_source(db_session):
    company, _ = seed_company(db_session)
    period = seed_period(db_session, company.company_id)
    report = Report(
        company_id=company.company_id,
        report_type="QUARTERLY",
        title="Derived input constraint test",
        financial_period_id=period.period_id,
    )
    db_session.add(report)
    db_session.flush()
    version = ReportVersion(
        report_id=report.report_id,
        version_number=1,
        publication_datetime=datetime(2024, 4, 15),
    )
    metric = FinancialMetric(
        metric_code="DERIVED_CONSTRAINT_TEST",
        metric_name="Derived test",
        category="PROFITABILITY",
        statement_type="INCOME",
        flow_or_stock="FLOW",
        is_derived=True,
    )
    db_session.add_all([version, metric])
    db_session.flush()
    derived = DerivedFinancialFact(
        company_id=company.company_id,
        period_id=period.period_id,
        metric_id=metric.metric_id,
        value_irr=1,
        formula_code="TEST",
        formula_version="1.0",
        source_report_version_id=version.report_version_id,
        data_cutoff_datetime=datetime(2024, 4, 15),
    )
    db_session.add(derived)
    db_session.flush()
    db_session.add(DerivedFinancialFactInput(
        derived_fact_id=derived.derived_fact_id,
        input_role="INVALID",
    ))
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_codal_ingestion_persists_report_version_and_raw_lines(db_session):
    company, _ = seed_company(db_session)
    period = seed_period(db_session, company.company_id)
    result = ingest_codal_report(
        db_session,
        company_id=company.company_id,
        period_id=period.period_id,
        report_type="QUARTERLY",
        title="Raw ingestion test",
        codal_tracking_id="CODAL-001",
        publication_datetime=datetime(2024, 4, 15),
        raw_lines=[
            RawLineInput(item_name="عنوان اصلی", value=Decimal("125.50"), unit="IRR"),
            RawLineInput(item_name="عنوان ناشناخته", value=None, source_row=9),
        ],
    )

    assert result.raw_fact_count == 2
    assert db_session.get(ReportVersion, result.report_version_id).is_current_version is True
    raw_facts = db_session.query(RawFinancialFact).order_by(RawFinancialFact.raw_fact_id).all()
    assert [fact.raw_item_name for fact in raw_facts] == ["عنوان اصلی", "عنوان ناشناخته"]
    assert raw_facts[0].value == Decimal("125.5000")
    assert raw_facts[1].value is None
    run = db_session.get(IngestionRun, result.ingestion_id)
    assert run.status == "COMPLETED"
    assert run.records_inserted == 2


def test_codal_ingestion_creates_new_report_version_without_overwriting_old_raw_data(db_session):
    company, _ = seed_company(db_session)
    period = seed_period(db_session, company.company_id)
    first = ingest_codal_report(
        db_session,
        company_id=company.company_id,
        period_id=period.period_id,
        report_type="ANNUAL",
        title="Versioned report",
        codal_tracking_id="CODAL-002",
        publication_datetime=datetime(2024, 4, 15),
        raw_lines=[RawLineInput(item_name="Revenue", value=Decimal("100"))],
    )
    second = ingest_codal_report(
        db_session,
        company_id=company.company_id,
        period_id=period.period_id,
        report_type="ANNUAL",
        title="Versioned report corrected",
        codal_tracking_id="CODAL-002",
        publication_datetime=datetime(2024, 5, 20),
        is_restated=True,
        raw_lines=[RawLineInput(item_name="Revenue", value=Decimal("120"))],
    )

    versions = db_session.query(ReportVersion).order_by(ReportVersion.version_number).all()
    assert [version.version_number for version in versions] == [1, 2]
    assert versions[0].is_current_version is False
    assert versions[1].is_current_version is True
    assert versions[1].supersedes_version_id == versions[0].report_version_id
    values = [fact.value for fact in db_session.query(RawFinancialFact).order_by(RawFinancialFact.raw_fact_id)]
    assert values == [Decimal("100.0000"), Decimal("120.0000")]
    assert first.report_id == second.report_id


def test_codal_ingestion_records_failed_run_and_rolls_back_partial_report(db_session):
    with pytest.raises(IntegrityError):
        ingest_codal_report(
            db_session,
            company_id=999999,
            period_id=999999,
            report_type="QUARTERLY",
            title="Invalid report",
            publication_datetime=datetime(2024, 4, 15),
            raw_lines=[RawLineInput(item_name="Will fail", value=Decimal("1"))],
        )

    failed_runs = db_session.query(IngestionRun).filter_by(status="FAILED").all()
    assert len(failed_runs) == 1
    assert failed_runs[0].records_failed == 1
    assert db_session.query(Report).count() == 0
    assert db_session.query(RawFinancialFact).count() == 0


def test_migration_runner_upgrades_empty_database_and_is_idempotent():
    migration_engine = create_engine("sqlite:///:memory:")
    runner = MigrationRunner(migration_engine)

    assert runner.current_version() == 0
    assert runner.upgrade() == 2
    assert runner.current_version() == 2
    tables = set(inspect(migration_engine).get_table_names())
    assert {"schema_migrations", "mapping_rules", "derived_financial_facts"}.issubset(tables)

    assert runner.upgrade() == 2
    with migration_engine.connect() as connection:
        migration_rows = connection.execute(text("SELECT COUNT(*) FROM schema_migrations")).scalar_one()
    assert migration_rows == 2


def test_migration_runner_upgrades_legacy_stage1_schema():
    migration_engine = create_engine("sqlite:///:memory:")
    with migration_engine.begin() as connection:
        connection.execute(text(
            "CREATE TABLE financial_metrics ("
            "metric_id INTEGER PRIMARY KEY, metric_code VARCHAR(100) NOT NULL, "
            "metric_name VARCHAR(200) NOT NULL, category VARCHAR(50) NOT NULL, "
            "value_type VARCHAR(30) NOT NULL, flow_or_stock VARCHAR(10) NOT NULL)"
        ))
        connection.execute(text(
            "CREATE TABLE normalized_financial_facts ("
            "fact_id INTEGER PRIMARY KEY, company_id INTEGER NOT NULL, period_id INTEGER NOT NULL, "
            "metric_id INTEGER NOT NULL, value_irr NUMERIC, source_report_version_id INTEGER NOT NULL, "
            "normalization_rule_id INTEGER, quality_status VARCHAR(20) NOT NULL)"
        ))

    runner = MigrationRunner(migration_engine)
    assert runner.upgrade() == 2
    columns = {column["name"] for column in inspect(migration_engine).get_columns("financial_metrics")}
    normalized_columns = {
        column["name"] for column in inspect(migration_engine).get_columns("normalized_financial_facts")
    }
    assert {"statement_type", "parent_metric_id", "sign_convention", "is_derived"}.issubset(columns)
    assert {"raw_fact_id", "mapping_decision_id"}.issubset(normalized_columns)
