"""Owner-run integration coverage for migration 9 and canonical Excel writes.

These tests use temporary SQLite databases and are intentionally not run by
the implementer for DB-IMPL-001.
"""
from dataclasses import replace
from datetime import datetime, timezone
from decimal import Decimal
from hashlib import sha256
from io import BytesIO

import pytest
from sqlalchemy import create_engine, event, inspect, select, text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from openpyxl import Workbook

from src.forecast.canonical_queries import load_canonical_financial_facts
from src.ingestion.canonical_admission import RevisionContext
from src.ingestion.canonical_admission import (
    CanonicalPersistencePlan, PlannedFact, ValueOrigin,
)
from src.ingestion.canonical_writer import (
    CanonicalWriteError, ReportWriteMetadata, ingest_excel_source, write_canonical_plan,
)
from src.ingestion.excel.canonical_input import (
    ApprovedSelection, CanonicalInputSpec, DurationBasis, JalaliPeriod, TemporalType,
)
from src.ingestion.excel.deterministic_matcher import TableRule, TemplateVersion
from src.migrations.runner import MigrationRunner
from src.migrations import runner as migration_runner
from src.models.audit import IngestionRun
from src.models.canonical import (
    CanonicalApproval, CanonicalCompanyFiscalCalendar, CanonicalDimensionSet,
    CanonicalFinancialFact, CanonicalIngestionAudit,
    CanonicalFactProvenance, CanonicalFinancialPeriod, CanonicalIdentityBinding,
    CanonicalReportVersion,
)
from src.models.entity import Company, Industry
from src.models.normalized import FinancialMetric


@pytest.fixture
def db(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'canonical.sqlite'}")

    @event.listens_for(engine, "connect")
    def enable_foreign_keys(connection, _record):
        connection.execute("PRAGMA foreign_keys=ON")

    assert MigrationRunner(engine).upgrade() == 9
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    with factory.begin() as session:
        industry = Industry(industry_code="BANK", industry_name="Bank")
        session.add(industry)
        session.flush()
        company = Company(ticker="TST", company_name="Test Bank", industry_id=industry.industry_id,
                          codal_symbol="TST-CODAL")
        session.add(company)
        session.flush()
        fiscal_approval = CanonicalApproval(
            approval_kind="fiscal_year_start_month", external_identity="company-1:1",
            approval_ref="approval-fiscal-start-1", is_active=True,
        )
        session.add(fiscal_approval)
        session.flush()
        session.add(CanonicalCompanyFiscalCalendar(company_id=company.company_id,
                                                    fiscal_year_start_month=1,
                                                    source_identity="approved-company-calendar",
                                                    approval_ref="approval-fiscal-start-1"))
        session.add(CanonicalApproval(approval_kind="scenario", external_identity="ACTUAL",
                                      approval_ref="approval-scenario-actual", is_active=True))
        metric = FinancialMetric(metric_code="BANK_REV", metric_name="Revenue", category="BANK",
                                 flow_or_stock="FLOW")
        session.add(metric)
        session.flush()
        seeded_approvals = set()
        for kind, identity, ref in (_approval_rows("version-1") + _approval_rows("version-2")
                                    + _approval_rows("version-3")):
            if (kind, identity, ref) in seeded_approvals:
                continue
            seeded_approvals.add((kind, identity, ref))
            session.add(CanonicalApproval(approval_kind=kind, external_identity=identity,
                                          approval_ref=ref, is_active=True))
        session.add_all([
            CanonicalIdentityBinding(identity_kind="company", external_identity="company-1",
                                     internal_id=company.company_id, approval_ref="approval-company", is_active=True),
            CanonicalIdentityBinding(identity_kind="metric", external_identity="metric-sales",
                                     internal_id=metric.metric_id, approval_ref="approval-metric", is_active=True),
        ])
    yield engine, factory
    engine.dispose()


def _approval_rows(version="version-1"):
    rows = [
        ("company", "company-1", "approval-company"),
        ("report_type", "report-periodic", "approval-report-type"),
        ("report_version", version, f"approval-{version}"),
        ("metric", "metric-sales", "approval-metric"),
        ("source_unit", "unit-rial", "approval-unit"),
        ("source_currency", "currency-irr", "approval-currency"),
        ("source_scale", "scale-unit", "approval-scale"),
        ("period_mapping", "period-map-q1", "approval-period"),
        ("source_label", "label-sales", "approval-label-sales"),
        ("source_header", "header-current", "approval-header-current"),
        ("extraction_standard", "standard-v1", "approval-standard-v1"),
        ("template", "template-fixture:1:" + "b" * 64, "approval-template"),
    ]
    return rows


def _plan(*, version="version-1", source_revision="revision-1", amount=12, supersedes=None):
    fact = PlannedFact(
        company_id="company-1", report_type_id="report-periodic", report_id="report-1",
        report_version_id=version,
        period_identity=("DURATION", (1404, 1, 1), (1404, 3, 31)),
        metric_id="metric-sales", dimensions=(), source_value_decimal=Decimal(amount),
        value_integer=amount, value_origin=ValueOrigin.SOURCE_REPORTED,
        source_unit="unit-rial", source_currency="currency-irr", source_scale="scale-unit",
        duration_basis="YTD", extraction_standard_id="standard-v1",
        extraction_standard_approval_ref="approval-standard-v1", source_identity="source-1",
        revision_identity=source_revision, source_artifact_sha256="a" * 64,
        template_id="template-fixture", template_version="1", template_sha256="b" * 64,
        extraction_owner="test-table", approval_references=tuple([
            (kind, identity, ref) for kind, identity, ref in _approval_rows(version)
            if kind not in {"extraction_standard", "template"}
        ]),
        worksheet_ordinal=1, worksheet_name="Annual", source_coordinate="B2",
        source_value_kind="PRESENT_TEXT",
    )
    return CanonicalPersistencePlan(
        report_id="report-1", report_version_id=version,
        source_identity="source-1", revision_identity=source_revision,
        source_artifact_sha256="a" * 64, extraction_standard_id="standard-v1",
        extraction_standard_approval_ref="approval-standard-v1", supersedes_version_id=supersedes,
        facts=(fact,), duplicate_count=0, unchanged_existing_count=0,
        preserved_report_version_ids=(), execution_allowed=True,
        physical_persistence_compatible=True, persistence_block_code=None,
    )


def _metadata(version=1, publication=datetime(2025, 4, 1, tzinfo=timezone.utc),
              *, is_audited=False, is_restated=False):
    return ReportWriteMetadata(title="Periodic report", version_number=version,
                              publication_datetime=publication,
                              is_audited=is_audited, is_restated=is_restated,
                              scenario_approval_ref="approval-scenario-actual",
                              scenario="ACTUAL")


def test_synthetic_xlsx_runs_reader_match_admission_writer_and_readback(db):
    _engine, factory = db
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Annual"
    sheet["A1"] = "Revenue"
    sheet["B1"] = "Amount"
    sheet["B2"] = "125.50"
    stream = BytesIO()
    workbook.save(stream)
    source = stream.getvalue()
    source_hash = sha256(source).hexdigest()
    template = TemplateVersion(
        template_id="template-fixture", version="1", approved=True,
        source_workbook_sha256="a" * 64, worksheet_name="Annual", worksheet_ordinal=1,
        tables=(TableRule(code="income", title_cell="A1", title_text="Revenue",
                          bounds="A1:B2", header_cells=(("B1", "Amount"),),
                          owned_ranges=("B2:B2",)),),
    )
    with factory.begin() as session:
        session.add(CanonicalApproval(
            approval_kind="template",
            external_identity=f"{template.template_id}:{template.version}:{template.template_sha256}",
            approval_ref="approval-template-e2e", is_active=True,
        ))

    def approved(identity, reference):
        return ApprovedSelection(identity=identity, approved=True, candidate_count=1,
                                 approval_ref=reference)

    spec = CanonicalInputSpec(
        company=approved("company-1", "approval-company"),
        report_type=approved("report-periodic", "approval-report-type"),
        report_version=approved("version-1", "approval-version-1"),
        metric=approved("metric-sales", "approval-metric"),
        source_unit=approved("unit-rial", "approval-unit"),
        source_currency=approved("currency-irr", "approval-currency"),
        source_scale=approved("scale-unit", "approval-scale"),
        period=JalaliPeriod(TemporalType.DURATION, (1404, 1, 1), (1404, 3, 31), DurationBasis.YTD),
        period_mapping=approved("period-map-q1", "approval-period"),
        source_label=approved("label-sales", "approval-label-sales"),
        source_header=approved("header-current", "approval-header-current"),
    )
    revision = RevisionContext(
        report_id="report-1", report_version_id="version-1", company_id="company-1",
        source_identity="source-e2e", revision_identity="revision-e2e",
        source_artifact_sha256=source_hash, extraction_standard_id="standard-v1",
        extraction_standard_approval_ref="approval-standard-v1",
    )
    adapted, result = ingest_excel_source(
        source, template=template, selections_by_coordinate={"B2": spec},
        revision=revision, metadata=_metadata(), session_factory=factory,
        expected_source_sha256=source_hash,
    )
    assert adapted.accepted and result.inserted_count == 1
    with factory() as session:
        facts = load_canonical_financial_facts(session, 1, cutoff=datetime(2025, 5, 1))
        assert len(facts) == 1
        assert facts[0].value_integer == 126
        assert facts[0].start_jalali == (1404, 1, 1)
        assert facts[0].end_jalali == (1404, 3, 31)
        assert facts[0].duration_basis == "YTD"
        assert facts[0].source_coordinate == "B2"
        provenance = session.scalar(select(CanonicalFactProvenance))
        assert provenance.source_decimal_text == "125.50"
        assert provenance.source_value_kind == "PRESENT_TEXT"
        run = session.get(IngestionRun, result.ingestion_id)
        audit = session.get(CanonicalIngestionAudit, result.ingestion_id)
        assert run.status == "COMPLETED"
        assert (audit.records_accepted, audit.records_duplicate, audit.records_rejected) == (1, 0, 0)


def test_migration_nine_is_repeatable_and_preserves_supported_legacy_rows(db):
    engine, _factory = db
    with engine.begin() as connection:
        connection.execute(text("CREATE TABLE preserved_legacy (id INTEGER PRIMARY KEY, value TEXT NOT NULL)"))
        connection.execute(text("INSERT INTO preserved_legacy VALUES (1, 'keep')"))
    assert MigrationRunner(engine).upgrade() == 9
    with engine.connect() as connection:
        assert connection.execute(text("SELECT value FROM preserved_legacy WHERE id=1")).scalar_one() == "keep"
        assert connection.execute(text("SELECT COUNT(*) FROM schema_migrations WHERE version=9")).scalar_one() == 1


def test_supported_v8_database_receives_additive_migration_nine(monkeypatch, tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'supported-v8.sqlite'}")
    migrations = tuple(migration_runner._migration_list())
    monkeypatch.setattr(migration_runner, "_migration_list", lambda: migrations[:8])
    assert MigrationRunner(engine).upgrade() == 8
    with engine.begin() as connection:
        connection.execute(text("CREATE TABLE legacy_sentinel (id INTEGER PRIMARY KEY, payload TEXT NOT NULL)"))
        connection.execute(text("INSERT INTO legacy_sentinel VALUES (1, 'preserve')"))
    monkeypatch.setattr(migration_runner, "_migration_list", lambda: migrations)
    assert MigrationRunner(engine).upgrade() == 9
    with engine.connect() as connection:
        assert connection.execute(text("SELECT payload FROM legacy_sentinel WHERE id=1")).scalar_one() == "preserve"
        assert connection.execute(text("SELECT COUNT(*) FROM schema_migrations WHERE version=9")).scalar_one() == 1
        assert {item["name"] for item in inspect(engine).get_indexes("companies")} >= {
            "uq_company_ticker", "uq_company_codal_symbol",
        }
    engine.dispose()


def test_failed_migration_nine_keeps_duplicate_legacy_rows_and_is_not_recorded(monkeypatch, tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'duplicate-symbols.sqlite'}")
    all_migrations = tuple(migration_runner._migration_list())
    monkeypatch.setattr(migration_runner, "_migration_list", lambda: all_migrations[:8])
    assert MigrationRunner(engine).upgrade() == 8
    with engine.begin() as connection:
        connection.execute(text("INSERT INTO industries (industry_code, industry_name) VALUES ('BANK','Bank')"))
        connection.execute(text("INSERT INTO companies (ticker, company_name, industry_id, codal_symbol) VALUES ('DUP','One',1,'A'),('DUP','Two',1,'B')"))
    monkeypatch.setattr(migration_runner, "_migration_list", lambda: all_migrations)
    with pytest.raises(RuntimeError, match="duplicate legacy values"):
        MigrationRunner(engine).upgrade()
    with engine.connect() as connection:
        assert connection.execute(text("SELECT COUNT(*) FROM companies WHERE ticker='DUP'")).scalar_one() == 2
        assert connection.execute(text("SELECT COUNT(*) FROM schema_migrations WHERE version=9")).scalar_one() == 0
        assert "canonical_approvals" not in inspect(engine).get_table_names()
    engine.dispose()


def test_migration_nine_refuses_a_historical_conflicting_version_name(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'historic-v9.sqlite'}")
    with engine.begin() as connection:
        connection.execute(text("CREATE TABLE schema_migrations (version INTEGER PRIMARY KEY, name VARCHAR(200) NOT NULL, applied_at DATETIME NOT NULL)"))
        connection.execute(text("INSERT INTO schema_migrations VALUES (9, 'codal_excel_source_metadata', '2026-01-01')"))
    with pytest.raises(RuntimeError, match="reconcile its source"):
        MigrationRunner(engine).upgrade()
    with engine.connect() as connection:
        assert connection.execute(text("SELECT name FROM schema_migrations WHERE version=9")).scalar_one() == "codal_excel_source_metadata"
    engine.dispose()


def test_migration_nine_enforces_unique_company_symbols_but_allows_missing_codal_symbol(db):
    _engine, factory = db
    with factory() as session:
        session.add(Company(ticker="TST", company_name="Duplicate ticker", industry_id=1))
        with pytest.raises(IntegrityError):
            session.flush()
        session.rollback()
        session.add(Company(ticker="OTHER", company_name="Duplicate CODAL symbol",
                            industry_id=1, codal_symbol="TST-CODAL"))
        with pytest.raises(IntegrityError):
            session.flush()
        session.rollback()
        session.add_all([
            Company(ticker="NULL1", company_name="No CODAL 1", industry_id=1),
            Company(ticker="NULL2", company_name="No CODAL 2", industry_id=1),
        ])
        session.commit()


def test_writer_persists_jalali_ytd_integer_fact_and_exact_provenance(db):
    _engine, factory = db
    result = write_canonical_plan(_plan(), _metadata(), factory)
    assert result.inserted_count == 1
    with factory() as session:
        fact = session.scalar(select(CanonicalFinancialFact))
        period = session.get(CanonicalFinancialPeriod, fact.period_id)
        assert fact.value_integer == 12
        assert fact.temporal_type == "DURATION" and fact.duration_basis == "YTD"
        assert (period.start_year, period.start_month, period.start_day) == (1404, 1, 1)
        assert period.months_length == 3


def test_writer_rejects_impossible_jalali_date_without_partial_rows(db):
    _engine, factory = db
    plan = _plan()
    invalid = replace(plan.facts[0], period_identity=("DURATION", (1404, 1, 1), (1402, 12, 30)))
    with pytest.raises(CanonicalWriteError, match="JALALI_DATE_INVALID"):
        write_canonical_plan(replace(plan, facts=(invalid,)), _metadata(), factory)
    with factory() as session:
        assert session.query(CanonicalFinancialFact).count() == 0


def test_writer_accepts_explicit_non_calendar_fiscal_start_and_ytd_period(db):
    _engine, factory = db
    with factory.begin() as session:
        session.add(CanonicalApproval(
            approval_kind="fiscal_year_start_month", external_identity="company-1:7",
            approval_ref="approval-fiscal-start-7", is_active=True,
        ))
        session.flush()
        calendar = session.get(CanonicalCompanyFiscalCalendar, 1)
        calendar.fiscal_year_start_month = 7
        calendar.approval_ref = "approval-fiscal-start-7"
    plan = _plan()
    non_calendar = replace(plan.facts[0],
                           period_identity=("DURATION", (1404, 7, 1), (1404, 9, 30)))
    result = write_canonical_plan(replace(plan, facts=(non_calendar,)), _metadata(), factory)
    with factory() as session:
        period = session.scalar(select(CanonicalFinancialPeriod))
        assert result.inserted_count == 1
        assert (period.start_year, period.start_month, period.end_month) == (1404, 7, 9)


def test_writer_persists_only_approved_blank_zero_fallback_as_fallback(db):
    _engine, factory = db
    with factory.begin() as session:
        session.add(CanonicalApproval(approval_kind="zero_fallback_rule",
                                      external_identity="rule-zero", approval_ref="approval-zero",
                                      is_active=True))
    plan = _plan()
    fact = replace(
        plan.facts[0], source_value_decimal=Decimal(0), value_integer=0,
        value_origin=ValueOrigin.ZERO_FALLBACK, source_value_kind="BLANK",
        approval_references=plan.facts[0].approval_references
        + (("zero_fallback_rule", "rule-zero", "approval-zero"),),
    )
    result = write_canonical_plan(replace(plan, facts=(fact,)), _metadata(), factory)
    with factory() as session:
        stored = session.scalar(select(CanonicalFinancialFact))
        provenance = session.scalar(select(CanonicalFactProvenance))
        assert result.inserted_count == 1
        assert stored.value_state == "ZERO_FALLBACK" and stored.value_integer == 0
        assert provenance.source_value_kind == "BLANK"


def test_identical_version_replay_is_duplicate_and_changed_payload_conflicts(db):
    _engine, factory = db
    first = write_canonical_plan(_plan(), _metadata(), factory)
    replay = write_canonical_plan(_plan(), _metadata(), factory)
    assert replay.inserted_count == 0 and replay.duplicate_count == 1
    with pytest.raises(CanonicalWriteError, match="REPORT_VERSION_CONFLICT"):
        write_canonical_plan(_plan(amount=13), _metadata(), factory)
    with factory() as session:
        assert session.query(CanonicalFinancialFact).count() == 1
        first_audit = session.get(CanonicalIngestionAudit, first.ingestion_id)
        replay_audit = session.get(CanonicalIngestionAudit, replay.ingestion_id)
        assert (first_audit.records_accepted, first_audit.records_duplicate, first_audit.records_rejected) == (1, 0, 0)
        assert (replay_audit.records_accepted, replay_audit.records_duplicate, replay_audit.records_rejected) == (0, 1, 0)


def test_correction_appends_a_report_version_and_pit_uses_publication_time(db):
    _engine, factory = db
    write_canonical_plan(_plan(), _metadata(), factory)
    correction = _plan(version="version-2", source_revision="revision-2", amount=15,
                       supersedes="version-1")
    write_canonical_plan(correction, _metadata(
        2, datetime(2025, 6, 1, tzinfo=timezone.utc), is_restated=True,
    ), factory)
    with factory() as session:
        before = load_canonical_financial_facts(session, 1, cutoff=datetime(2025, 5, 1))
        after = load_canonical_financial_facts(session, 1, cutoff=datetime(2025, 7, 1))
        assert before[0].value_integer == 12
        assert after[0].value_integer == 15
        assert session.query(CanonicalReportVersion).count() == 2


def test_pit_quality_order_prefers_audited_initial_over_later_unaudited_restatement(db):
    _engine, factory = db
    write_canonical_plan(_plan(), _metadata(), factory)
    correction = _plan(version="version-2", source_revision="revision-2", amount=15,
                       supersedes="version-1")
    write_canonical_plan(correction, _metadata(
        2, datetime(2025, 6, 1, tzinfo=timezone.utc), is_restated=True,
    ), factory)
    audited = _plan(version="version-3", source_revision="revision-3", amount=18,
                    supersedes="version-2")
    write_canonical_plan(audited, _metadata(
        3, datetime(2025, 7, 1, tzinfo=timezone.utc), is_audited=True,
    ), factory)
    with factory() as session:
        rows = load_canonical_financial_facts(session, 1, cutoff=datetime(2025, 8, 1))
        assert rows[0].value_integer == 18
        assert rows[0].is_audited is True and rows[0].is_restated is False


def test_invalid_fact_rolls_back_entire_report_version_batch(db):
    _engine, factory = db
    plan = _plan()
    invalid = replace(plan.facts[0], metric_id="unbound-metric")
    with pytest.raises(CanonicalWriteError, match="IDENTITY_BINDING_NOT_RESOLVED") as error:
        write_canonical_plan(replace(plan, facts=(plan.facts[0], invalid)), _metadata(), factory)
    with factory() as session:
        assert session.query(CanonicalFinancialFact).count() == 0
        assert session.query(CanonicalReportVersion).count() == 0
        assert session.query(CanonicalDimensionSet).count() == 0
        failed_run = session.scalar(select(IngestionRun).where(IngestionRun.status == "FAILED"))
        audit = session.get(CanonicalIngestionAudit, failed_run.ingestion_id)
        assert audit.records_accepted == 0 and audit.records_rejected == 2
        assert audit.error_code == error.value.code


def test_database_fact_identity_and_value_state_constraints_reject_null_dimension_bypass(db):
    engine, _factory = db
    assert "uq_canonical_fact_identity" in {constraint.get("name") for constraint in inspect(engine).get_unique_constraints("canonical_financial_facts")}
    with engine.connect() as connection:
        columns = {item["name"] for item in inspect(connection).get_columns("canonical_financial_facts")}
        assert "dimension_set_id" in columns and "value_state" in columns
    _result = write_canonical_plan(_plan(), _metadata(), _factory)
    with _factory() as session:
        stored = session.scalar(select(CanonicalFinancialFact))
        duplicate = CanonicalFinancialFact(
            report_version_id=stored.report_version_id, period_id=stored.period_id,
            metric_id=stored.metric_id, dimension_set_id=stored.dimension_set_id,
            temporal_type=stored.temporal_type, duration_basis=stored.duration_basis,
            value_integer=stored.value_integer, value_state=stored.value_state,
            value_origin=stored.value_origin, source_unit=stored.source_unit,
            source_currency=stored.source_currency, source_scale=stored.source_scale,
            scenario=stored.scenario,
        )
        session.add(duplicate)
        with pytest.raises(IntegrityError):
            session.flush()
        session.rollback()
        other_set = CanonicalDimensionSet(canonical_key="c" * 64)
        session.add(other_set)
        session.flush()
        invalid_state = CanonicalFinancialFact(
            report_version_id=stored.report_version_id, period_id=stored.period_id,
            metric_id=stored.metric_id, dimension_set_id=other_set.dimension_set_id,
            temporal_type="DURATION", duration_basis="YTD",
            value_integer=None, value_state="REPORTED_VALUE", value_origin="SOURCE_REPORTED",
            source_unit="unit-rial", source_currency="currency-irr", source_scale="scale-unit",
            scenario="ACTUAL",
        )
        session.add(invalid_state)
        with pytest.raises(IntegrityError):
            session.flush()
        session.rollback()
        null_dimensions = CanonicalFinancialFact(
            report_version_id=stored.report_version_id, period_id=stored.period_id,
            metric_id=stored.metric_id, dimension_set_id=None,
            temporal_type="DURATION", duration_basis="YTD",
            value_integer=1, value_state="REPORTED_VALUE", value_origin="SOURCE_REPORTED",
            source_unit="unit-rial", source_currency="currency-irr", source_scale="scale-unit",
            scenario="ACTUAL",
        )
        session.add(null_dimensions)
        with pytest.raises(IntegrityError):
            session.flush()

