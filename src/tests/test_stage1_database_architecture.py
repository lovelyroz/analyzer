from datetime import date, datetime

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from src.core.database import Base
from src.models.entity import Company, Industry
from src.models.normalized import FinancialMetric, MappingDecision, MappingRule, NormalizedFinancialFact, RawFinancialFact
from src.models.normalized_provenance import NormalizedFinancialFactInput
from src.models.period import FinancialPeriod
from src.models.report import Report, ReportVersion

# Import all Stage 1 models so the test metadata represents the production schema.
from src.models.audit import IngestionRun  # noqa: F401
from src.models.fx import FXConversionRule, FXRate  # noqa: F401
from src.models.market import MarketDaily  # noqa: F401
from src.models.share_action import CorporateAction, ShareCountHistory  # noqa: F401
from src.models.normalized import DerivedFinancialFact, DerivedFinancialFactInput  # noqa: F401


def test_normalized_fact_supports_multiple_raw_inputs_without_duplicate_metric_rows():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    industry = Industry(industry_code="TEST", industry_name="Test")
    session.add(industry)
    session.flush()
    company = Company(ticker="T", company_name="Test", industry_id=industry.industry_id)
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
    session.flush()
    report = Report(
        company_id=company.company_id,
        report_type="QUARTERLY",
        title="Test",
        financial_period_id=period.period_id,
    )
    session.add(report)
    session.flush()
    version = ReportVersion(
        report_id=report.report_id,
        version_number=1,
        publication_datetime=datetime(2024, 4, 15),
    )
    metric = FinancialMetric(
        metric_code="COGS",
        metric_name="Cost of goods sold",
        category="BASE",
        statement_type="INCOME",
        flow_or_stock="FLOW",
    )
    rule = MappingRule(rule_code="TEST_ALIAS", rule_version="1.0")
    session.add_all([version, metric, rule])
    session.flush()

    raw_a = RawFinancialFact(
        company_id=company.company_id,
        report_version_id=version.report_version_id,
        period_id=period.period_id,
        raw_item_name="Direct materials",
        value=100,
    )
    raw_b = RawFinancialFact(
        company_id=company.company_id,
        report_version_id=version.report_version_id,
        period_id=period.period_id,
        raw_item_name="Factory overhead",
        value=40,
    )
    session.add_all([raw_a, raw_b])
    session.flush()

    decision_a = MappingDecision(
        raw_fact_id=raw_a.raw_fact_id,
        metric_id=metric.metric_id,
        mapping_rule_id=rule.mapping_rule_id,
        mapping_method="ALIAS",
        confidence=95,
        review_status="APPROVED",
        composition_role="COMPONENT",
    )
    decision_b = MappingDecision(
        raw_fact_id=raw_b.raw_fact_id,
        metric_id=metric.metric_id,
        mapping_rule_id=rule.mapping_rule_id,
        mapping_method="ALIAS",
        confidence=95,
        review_status="APPROVED",
        composition_role="COMPONENT",
    )
    session.add_all([decision_a, decision_b])
    session.flush()

    normalized = NormalizedFinancialFact(
        company_id=company.company_id,
        period_id=period.period_id,
        metric_id=metric.metric_id,
        value_irr=140,
        source_report_version_id=version.report_version_id,
        quality_status="VALID",
    )
    session.add(normalized)
    session.flush()

    session.add_all([
        NormalizedFinancialFactInput(
            normalized_fact_id=normalized.fact_id,
            raw_fact_id=raw_a.raw_fact_id,
            mapping_decision_id=decision_a.mapping_decision_id,
            input_role="COMPONENT",
        ),
        NormalizedFinancialFactInput(
            normalized_fact_id=normalized.fact_id,
            raw_fact_id=raw_b.raw_fact_id,
            mapping_decision_id=decision_b.mapping_decision_id,
            input_role="COMPONENT",
        ),
    ])
    session.commit()

    assert session.query(NormalizedFinancialFact).count() == 1
    assert session.query(NormalizedFinancialFactInput).count() == 2
    assert {row.raw_fact_id for row in session.query(NormalizedFinancialFactInput).all()} == {
        raw_a.raw_fact_id,
        raw_b.raw_fact_id,
    }
    assert "normalized_financial_fact_inputs" in inspect(engine).get_table_names()
    session.close()
