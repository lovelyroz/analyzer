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
from src.models.forecast import LegacyForecastBase


def test_migration_reaches_version_eight_without_forecast_tables_and_is_idempotent():
    engine = create_engine("sqlite:///:memory:")
    runner = MigrationRunner(engine)

    assert runner.upgrade() == 8
    assert runner.upgrade() == 8
    tables = set(inspect(engine).get_table_names())
    assert "normalized_financial_fact_inputs" in tables
    assert not ({"forecast_versions", "forecast_input_refs"} & tables)
    market_cols = {c["name"] for c in inspect(engine).get_columns("market_daily")}
    assert {"jalali_year", "jalali_month", "jalali_day"}.issubset(market_cols)
    fx_cols = {c["name"] for c in inspect(engine).get_columns("fx_rates")}
    assert {"jalali_year", "jalali_month", "jalali_day"}.issubset(fx_cols)

    with engine.connect() as connection:
        versions = connection.execute(text("SELECT version FROM schema_migrations ORDER BY version")).scalars().all()
    assert versions == [1, 2, 3, 4, 5, 6, 7, 8]


def test_active_metadata_does_not_recreate_forecast_output_tables():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    tables = set(inspect(engine).get_table_names())
    assert "forecast_versions" not in tables
    assert "forecast_input_refs" not in tables


def test_version_seven_upgrade_removes_only_legacy_forecast_tables_and_rows():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    LegacyForecastBase.metadata.create_all(bind=engine)
    with engine.begin() as connection:
        connection.execute(text("CREATE TABLE schema_migrations (version INTEGER PRIMARY KEY, name VARCHAR(200) NOT NULL, applied_at DATETIME NOT NULL)"))
        for version in range(1, 8):
            connection.execute(text("INSERT INTO schema_migrations (version, name, applied_at) VALUES (:v, :n, '2024-01-01')"), {"v": version, "n": f"migration_{version}"})
        connection.execute(text("INSERT INTO raw_financial_facts (company_id, report_version_id, period_id, raw_item_name) VALUES (1, 1, 1, 'preserve-me')"))
        connection.execute(text("INSERT INTO normalized_financial_facts (company_id, period_id, metric_id, raw_fact_id, value_irr, source_report_version_id, quality_status) VALUES (1, 1, 1, 1, 123, 1, 'VALID')"))
        connection.execute(text("INSERT INTO reports (company_id, report_type, title, financial_period_id, is_correction) VALUES (1, 'QUARTERLY', 'preserve-report', 1, 0)"))
        connection.execute(text("INSERT INTO report_versions (report_id, version_number, publication_datetime, is_current_version, is_restated) VALUES (1, 1, '2024-01-01', 1, 0)"))
        connection.execute(text("INSERT INTO share_count_history (company_id, effective_date, shares_outstanding, capital, source) VALUES (1, '2024-01-01', 1000, 1000, 'preserve-share')"))
        connection.execute(text("INSERT INTO corporate_actions (company_id, effective_date, action_type, source) VALUES (1, '2024-02-01', 'SPLIT', 'preserve-action')"))
        connection.execute(text("INSERT INTO forecast_versions (company_id, forecast_period_id, forecast_horizon, scenario, version_number, forecast_timestamp, data_cutoff_datetime, model_version, forecast_method, data_quality, baseline_method, industry_code) VALUES (1, 1, '12M', 'BASE', 1, '2024-01-01', '2023-12-31', 'V1', 'test', 'OK', 'test', 'T')"))
        forecast_id = connection.execute(text("SELECT forecast_version_id FROM forecast_versions")).scalar_one()
        connection.execute(text("INSERT INTO forecast_input_refs (forecast_version_id, fact_key) VALUES (:id, 'REV')"), {"id": forecast_id})

    runner = MigrationRunner(engine)
    assert runner.upgrade() == 8
    assert runner.upgrade() == 8
    tables = set(inspect(engine).get_table_names())
    assert not ({"forecast_versions", "forecast_input_refs"} & tables)
    with engine.connect() as connection:
        assert connection.execute(text("SELECT raw_item_name FROM raw_financial_facts")).scalar_one() == "preserve-me"
        assert connection.execute(text("SELECT value_irr FROM normalized_financial_facts")).scalar_one() == 123
        assert connection.execute(text("SELECT title FROM reports")).scalar_one() == "preserve-report"
        assert connection.execute(text("SELECT version_number FROM report_versions")).scalar_one() == 1
        assert connection.execute(text("SELECT shares_outstanding FROM share_count_history")).scalar_one() == 1000
        assert connection.execute(text("SELECT source FROM corporate_actions")).scalar_one() == "preserve-action"
        versions = connection.execute(text("SELECT version FROM schema_migrations ORDER BY version")).scalars().all()
    assert versions == list(range(1, 9))


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
