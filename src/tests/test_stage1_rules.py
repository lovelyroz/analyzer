# Stage 1 — Data Foundation & Data Model tests
from datetime import date, datetime
from decimal import Decimal

import pytest
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.exc import IntegrityError

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


def test_migration_runner_upgrades_empty_database_and_is_idempotent():
    migration_engine = create_engine("sqlite:///:memory:")
    runner = MigrationRunner(migration_engine)
    assert runner.current_version() == 0
    assert runner.upgrade() == 6
    assert runner.current_version() == 6
    tables = set(inspect(migration_engine).get_table_names())
    assert {"schema_migrations", "mapping_rules", "derived_financial_facts", "normalized_financial_fact_inputs"}.issubset(tables)
    assert runner.upgrade() == 6
    with migration_engine.connect() as connection:
        migration_rows = connection.execute(text("SELECT COUNT(*) FROM schema_migrations")).scalar_one()
        versions = connection.execute(text("SELECT version FROM schema_migrations ORDER BY version")).scalars().all()
    assert migration_rows == 6
    assert versions == [1, 2, 3, 4, 5, 6]


def test_migration_runner_upgrades_legacy_stage1_schema():
    migration_engine = create_engine("sqlite:///:memory:")
    with migration_engine.begin() as connection:
        connection.execute(text("CREATE TABLE financial_metrics (metric_id INTEGER PRIMARY KEY, metric_code VARCHAR(100) NOT NULL, metric_name VARCHAR(200) NOT NULL, category VARCHAR(50) NOT NULL, value_type VARCHAR(30) NOT NULL, flow_or_stock VARCHAR(10) NOT NULL)"))
        connection.execute(text("CREATE TABLE normalized_financial_facts (fact_id INTEGER PRIMARY KEY, company_id INTEGER NOT NULL, period_id INTEGER NOT NULL, metric_id INTEGER NOT NULL, value_irr NUMERIC, source_report_version_id INTEGER NOT NULL, normalization_rule_id INTEGER, quality_status VARCHAR(20) NOT NULL)"))
        connection.execute(text("CREATE TABLE report_versions (report_version_id INTEGER PRIMARY KEY, report_id INTEGER NOT NULL, version_number INTEGER NOT NULL, publication_datetime DATETIME NOT NULL, is_current_version BOOLEAN NOT NULL DEFAULT 1, is_restated BOOLEAN NOT NULL DEFAULT 0, supersedes_version_id INTEGER, created_at DATETIME)"))
    runner = MigrationRunner(migration_engine)
    assert runner.upgrade() == 6
    columns = {column["name"] for column in inspect(migration_engine).get_columns("financial_metrics")}
    normalized_columns = {column["name"] for column in inspect(migration_engine).get_columns("normalized_financial_facts")}
    assert {"statement_type", "parent_metric_id", "sign_convention", "is_derived"}.issubset(columns)
    assert {"raw_fact_id", "mapping_decision_id"}.issubset(normalized_columns)
    assert "normalized_financial_fact_inputs" in inspect(migration_engine).get_table_names()
    assert any(index["name"] == "uq_report_current_version" and index["unique"] for index in inspect(migration_engine).get_indexes("report_versions"))
