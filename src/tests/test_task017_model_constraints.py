"""Focused SQLite checks for constraints actually declared by Stage 1 models."""
from datetime import date, datetime

import pytest
from sqlalchemy import create_engine, event, inspect, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.core.database import Base
from src.migrations import runner as migration_runner
from src.migrations.runner import Migration, MigrationRunner
from src.models.entity import Company, Industry
from src.models.normalized import (
    DerivedFinancialFact,
    DerivedFinancialFactInput,
    FinancialMetric,
    MappingDecision,
    MappingRule,
    NormalizedFinancialFact,
    RawFinancialFact,
)
from src.models.period import FinancialPeriod
from src.models.report import Report, ReportVersion


@pytest.fixture
def db(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'constraints.sqlite'}")

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(connection, _record):
        connection.execute("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(engine)
    with engine.connect() as connection:
        assert connection.exec_driver_sql("PRAGMA foreign_keys").scalar_one() == 1
    yield engine
    engine.dispose()


def _base_rows(session):
    industry = Industry(industry_code="BANK", industry_name="Bank")
    session.add(industry)
    session.flush()
    company = Company(ticker="TST", company_name="Test", industry_id=industry.industry_id)
    session.add(company)
    session.flush()
    period = FinancialPeriod(company_id=company.company_id, period_type="QUARTER",
        start_date=date(2024, 1, 1), end_date=date(2024, 3, 31), fiscal_year=1403,
        fiscal_quarter=1, months_length=3, is_ytd=False)
    session.add(period)
    session.flush()
    report = Report(company_id=company.company_id, report_type="QUARTERLY", title="Test",
        financial_period_id=period.period_id)
    session.add(report)
    session.flush()
    version = ReportVersion(report_id=report.report_id, version_number=1,
        publication_datetime=datetime(2024, 4, 1))
    metric = FinancialMetric(metric_code="REV", metric_name="Revenue", category="BASE",
        flow_or_stock="FLOW")
    session.add_all([version, metric])
    session.flush()
    raw = RawFinancialFact(company_id=company.company_id, report_version_id=version.report_version_id,
        period_id=period.period_id, raw_item_name="Revenue", value=10)
    session.add(raw)
    session.flush()
    derived = DerivedFinancialFact(company_id=company.company_id, period_id=period.period_id,
        metric_id=metric.metric_id, formula_code="F", formula_version="1",
        source_report_version_id=version.report_version_id, data_cutoff_datetime=datetime(2024, 4, 1))
    session.add(derived)
    session.flush()
    return industry, company, period, report, version, metric, raw, derived


def _rejected(session, row):
    session.add(row)
    with pytest.raises(IntegrityError):
        session.flush()
    session.rollback()


def test_company_required_fields_industry_fk_and_supported_uniqueness(db):
    # Ticker/CODAL uniqueness is introduced by migration 9, not by the legacy baseline metadata.
    migration_runner._apply_canonical_jalali_excel_schema(db)
    with Session(db) as s:
        industry, company, *_ = _base_rows(s)
        s.commit()
        s.add(Company(ticker="BAD", company_name="Bad FK", industry_id=999))
        with pytest.raises(IntegrityError):
            s.flush()
        s.rollback()
        _rejected(s, Company(company_name="Missing ticker", industry_id=industry.industry_id))
        _rejected(s, Company(ticker="NO-NAME", industry_id=industry.industry_id))
        _rejected(s, Industry(industry_code="NO-NAME"))
        _rejected(s, Industry(industry_code="BANK", industry_name="Duplicate"))
        s.add_all([Company(ticker="A", company_name="A", industry_id=industry.industry_id),
                   Company(ticker="B", company_name="B", industry_id=industry.industry_id)])
        s.flush()  # Multiple NULL national IDs are allowed by SQLite UNIQUE semantics.
        _rejected(s, Company(ticker="A", company_name="Duplicate ticker", industry_id=industry.industry_id))
        s.add_all([Company(ticker="C1", company_name="C1", industry_id=industry.industry_id, codal_symbol="CODAL"),
                   Company(ticker="C2", company_name="C2", industry_id=industry.industry_id, codal_symbol=None),
                   Company(ticker="C3", company_name="C3", industry_id=industry.industry_id, codal_symbol=None)])
        s.flush()
        _rejected(s, Company(ticker="C4", company_name="C4", industry_id=industry.industry_id, codal_symbol="CODAL"))
        s.add(Company(ticker="C", company_name="C", industry_id=industry.industry_id, national_id="N1"))
        s.flush()
        _rejected(s, Company(ticker="D", company_name="D", industry_id=industry.industry_id, national_id="N1"))


@pytest.mark.parametrize("changes", [
    {"start_date": date(2024, 4, 1), "end_date": date(2024, 3, 31)},
    {"period_type": "WEEK"},
])
def test_period_checks_reject_invalid_dates_or_type(db, changes):
    with Session(db) as s:
        rows = _base_rows(s)
        company = rows[1]
        s.commit()
        fields = dict(company_id=company.company_id, period_type="MONTH", start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31), fiscal_year=1403, months_length=1)
        fields.update(changes)
        _rejected(s, FinancialPeriod(**fields))


def test_period_unique_identity_and_report_version_constraints(db):
    with Session(db) as s:
        _, company, period, report, version, *_ = _base_rows(s)
        s.commit()
        _rejected(s, FinancialPeriod(company_id=company.company_id, period_type="QUARTER",
            start_date=date(2024, 1, 1), end_date=date(2024, 3, 31), fiscal_year=1403, months_length=3))
        _rejected(s, ReportVersion(report_id=report.report_id, version_number=1,
            publication_datetime=datetime(2024, 5, 1), is_current_version=False))
        s.add(ReportVersion(report_id=report.report_id, version_number=2,
            publication_datetime=datetime(2024, 5, 1), is_current_version=False))
        s.flush()
        _rejected(s, ReportVersion(report_id=report.report_id, version_number=3,
            publication_datetime=datetime(2024, 6, 1), is_current_version=True))


@pytest.mark.parametrize("field,value", [
    ("flow_or_stock", "BOTH"), ("statement_type", "UNKNOWN"), ("sign_convention", "REVERSE"),
])
def test_financial_metric_checks_reject_unsupported_values(db, field, value):
    with Session(db) as s:
        fields = dict(metric_code="M", metric_name="Metric", category="BASE", flow_or_stock="FLOW")
        fields[field] = value
        _rejected(s, FinancialMetric(**fields))


@pytest.mark.parametrize("field,value", [
    ("mapping_method", "FUZZY"), ("review_status", "PENDING"),
    ("composition_role", "OTHER"), ("confidence", 101),
])
def test_mapping_decision_checks_reject_unsupported_values(db, field, value):
    with Session(db) as s:
        *_, raw, _derived = _base_rows(s)
        s.flush()
        s.add(MappingDecision(raw_fact_id=raw.raw_fact_id, mapping_method="MANUAL",
            confidence=50, review_status="APPROVED", composition_role="TOTAL"))
        s.commit()
        raw_id = raw.raw_fact_id
        fields = dict(raw_fact_id=raw.raw_fact_id, mapping_method="MANUAL", confidence=50,
            review_status="APPROVED", composition_role="TOTAL")
        fields[field] = value
        fields["raw_fact_id"] = raw_id
        _rejected(s, MappingDecision(**fields))


def test_normalized_identity_and_quality_status_constraints(db):
    with Session(db) as s:
        _, company, period, _report, version, metric, *_ = _base_rows(s)
        row = NormalizedFinancialFact(company_id=company.company_id, period_id=period.period_id,
            metric_id=metric.metric_id, source_report_version_id=version.report_version_id,
            value_irr=10, quality_status="VALID")
        s.add(row)
        s.flush()
        s.commit()
        _rejected(s, NormalizedFinancialFact(company_id=company.company_id, period_id=period.period_id,
            metric_id=metric.metric_id, source_report_version_id=version.report_version_id, value_irr=11))
        other_metric = FinancialMetric(metric_code="OTHER", metric_name="Other", category="BASE", flow_or_stock="STOCK")
        s.add(other_metric)
        s.flush()
        _rejected(s, NormalizedFinancialFact(company_id=company.company_id, period_id=period.period_id,
            metric_id=other_metric.metric_id, source_report_version_id=version.report_version_id,
            quality_status="UNKNOWN"))


def test_derived_input_xor_is_enforced_but_sqlite_null_unique_gap_is_visible(db):
    with Session(db) as s:
        *_, raw, derived = _base_rows(s)
        normalized = NormalizedFinancialFact(company_id=raw.company_id, period_id=raw.period_id,
            metric_id=derived.metric_id, source_report_version_id=raw.report_version_id, quality_status="VALID")
        s.add(normalized)
        s.flush()
        s.add(DerivedFinancialFactInput(derived_fact_id=derived.derived_fact_id,
            normalized_fact_id=normalized.fact_id, input_role="SOURCE"))
        s.flush()
        s.commit()
        derived_id, normalized_id = derived.derived_fact_id, normalized.fact_id
        _rejected(s, DerivedFinancialFactInput(derived_fact_id=derived_id,
            input_role="SOURCE"))
        # SQLite UNIQUE treats NULLs as distinct, so the declared composite unique
        # constraint does not reject an otherwise identical normalized-input row.
        s.add(DerivedFinancialFactInput(derived_fact_id=derived_id,
            normalized_fact_id=normalized_id, input_role="SOURCE"))
        s.flush()
        assert s.query(DerivedFinancialFactInput).count() == 2


def test_runner_empty_upgrade_repeated_upgrade_and_single_history_entries(tmp_path):
    empty_engine = create_engine(f"sqlite:///{tmp_path / 'empty.sqlite'}")
    runner = MigrationRunner(empty_engine)
    assert runner.upgrade() == runner.upgrade() == 9
    with empty_engine.connect() as c:
        versions = c.execute(text("SELECT version FROM schema_migrations ORDER BY version")).scalars().all()
    assert versions == list(range(1, 10))
    empty_engine.dispose()


def test_runner_recognizes_legacy_baseline_without_losing_business_row(db):
    with db.begin() as c:
        c.execute(text("CREATE TABLE legacy_business (id INTEGER PRIMARY KEY, payload TEXT NOT NULL)"))
        c.execute(text("INSERT INTO legacy_business VALUES (1, 'keep')"))
    assert MigrationRunner(db).upgrade() == 9
    with db.connect() as c:
        assert c.execute(text("SELECT payload FROM legacy_business WHERE id=1")).scalar_one() == "keep"
        assert c.execute(text("SELECT name FROM schema_migrations WHERE version=1")).scalar_one() == "legacy_baseline"


def test_migration_four_rejects_multiple_current_versions_without_repair(db):
    Base.metadata.create_all(db)
    with db.begin() as c:
        c.execute(text("INSERT INTO industries (industry_code, industry_name) VALUES ('I','Industry')"))
        c.execute(text("INSERT INTO companies (ticker, company_name, industry_id, status, is_active) VALUES ('T','Test',1,'ACTIVE',1)"))
        c.execute(text("INSERT INTO financial_periods (company_id,period_type,start_date,end_date,fiscal_year,months_length,is_ytd) VALUES (1,'QUARTER','2024-01-01','2024-03-31',1403,3,0)"))
        c.execute(text("INSERT INTO reports (company_id,report_type,title,financial_period_id,is_correction) VALUES (1,'Q','Q',1,0)"))
        c.execute(text("DROP INDEX uq_report_current_version"))
        c.execute(text("INSERT INTO report_versions (report_id,version_number,publication_datetime,is_current_version,is_restated) VALUES (1,1,'2024-04-01',1,0),(1,2,'2024-05-01',1,0)"))
        c.execute(text("CREATE TABLE schema_migrations (version INTEGER PRIMARY KEY, name VARCHAR(200) NOT NULL, applied_at DATETIME NOT NULL)"))
        for n in range(1, 4):
            c.execute(text("INSERT INTO schema_migrations VALUES (:n,:name,'2024-01-01')"), {"n": n, "name": f"v{n}"})
    with pytest.raises(RuntimeError, match="multiple current"):
        MigrationRunner(db).upgrade()
    with db.connect() as c:
        assert c.execute(text("SELECT COUNT(*) FROM report_versions WHERE is_current_version=1")).scalar_one() == 2
        assert c.execute(text("SELECT COUNT(*) FROM schema_migrations WHERE version=4")).scalar_one() == 0


def test_failed_migration_is_not_recorded(monkeypatch, tmp_path):
    def fail(_engine):
        raise RuntimeError("injected failure")
    engine = create_engine(f"sqlite:///{tmp_path / 'failure.sqlite'}")
    monkeypatch.setattr(migration_runner, "_migration_list", lambda: (Migration(1, "fails", fail),))
    with pytest.raises(RuntimeError, match="injected failure"):
        MigrationRunner(engine).upgrade()
    with engine.connect() as c:
        assert c.execute(text("SELECT COUNT(*) FROM schema_migrations WHERE version=1")).scalar_one() == 0
    engine.dispose()


def test_jalali_date_api_remains_the_shared_validation_contract():
    from src.core.jalali import validate_jalali_date
    assert validate_jalali_date((1403, 12, 29), label="date") == (1403, 12, 29)
    with pytest.raises(ValueError):
        validate_jalali_date((1402, 12, 30), label="date")
    assert "end_date >= start_date" in {constraint.sqltext.text for constraint in FinancialPeriod.__table__.constraints if hasattr(constraint, "sqltext")}
