from datetime import date, datetime

import pytest
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from src.core.database import Base
from src.migrations.runner import MigrationRunner
from src.models.audit import IngestionRun  # noqa: F401
from src.models.entity import Company, Industry
from src.models.fx import FXConversionRule, FXRate  # noqa: F401
from src.models.market import MarketDaily  # noqa: F401
from src.models.normalized import (
    DerivedFinancialFact,
    DerivedFinancialFactInput,
    FinancialMetric,
    MappingDecision,
    MappingRule,
    NormalizedFinancialFact,
    RawFinancialFact,
)
from src.models.normalized_provenance import NormalizedFinancialFactInput
from src.models.period import FinancialPeriod
from src.models.report import Report, ReportVersion
from src.models.share_action import CorporateAction, ShareCountHistory  # noqa: F401


def test_migration_reaches_version_five_and_is_idempotent():
    engine = create_engine("sqlite:///:memory:")
    runner = MigrationRunner(engine)

    assert runner.upgrade() == 5
    assert runner.upgrade() == 5
    tables = set(inspect(engine).get_table_names())
    assert "normalized_financial_fact_inputs" in tables
    cols = {c["name"] for c in inspect(engine).get_columns("market_daily")}
    assert {"jalali_year", "jalali_month", "jalali_day"}.issubset(cols)

    with engine.connect() as connection:
        versions = connection.execute(text("SELECT version FROM schema_migrations ORDER BY version")).scalars().all()
    assert versions == [1, 2, 3, 4, 5]


def test_current_report_version_unique_index_is_present_on_bootstrap():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    indexes = inspect(engine).get_indexes("report_versions")
    assert any(index["name"] == "uq_report_current_version" and index["unique"] for index in indexes)


def test_current_report_version_constraint_rejects_two_current_versions():
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

    session.add_all(
        [
            ReportVersion(
                report_id=report.report_id,
                version_number=1,
                publication_datetime=datetime(2024, 4, 15),
                is_current_version=True,
            ),
            ReportVersion(
                report_id=report.report_id,
                version_number=2,
                publication_datetime=datetime(2024, 5, 15),
                is_current_version=True,
            ),
        ]
    )

    with pytest.raises(IntegrityError):
        session.commit()

    session.rollback()
    session.close()
