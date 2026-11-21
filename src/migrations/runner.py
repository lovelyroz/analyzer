from dataclasses import dataclass
from datetime import datetime, timezone
import re
from typing import Callable, Iterable

from sqlalchemy import DateTime, bindparam, inspect, text
from sqlalchemy.engine import Engine

from src.core.database import Base

# Import all models before metadata-based bootstrap or table creation.
from src.models.audit import IngestionRun  # noqa: F401
from src.models.entity import Company, Industry  # noqa: F401
from src.models.fx import FXConversionRule, FXRate  # noqa: F401
from src.models.market import MarketDaily  # noqa: F401
from src.models.normalized import (  # noqa: F401
    DerivedFinancialFact,
    DerivedFinancialFactInput,
    FinancialMetric,
    MappingDecision,
    MappingRule,
    NormalizedFinancialFact,
    RawFinancialFact,
)
from src.models.normalized_provenance import NormalizedFinancialFactInput  # noqa: F401
from src.models.forecast import (
    ForecastInputRefModel,
    ForecastVersion,
    LegacyForecastBase,
)  # noqa: F401
from src.models.period import FinancialPeriod  # noqa: F401
from src.models.report import Report, ReportVersion  # noqa: F401
from src.models.share_action import CorporateAction, ShareCountHistory  # noqa: F401
from src.models import canonical as _canonical  # noqa: F401


@dataclass(frozen=True)
class Migration:
    version: int
    name: str
    apply: Callable[[Engine], None]


MIGRATION_TABLE = "schema_migrations"


def _utc_now_naive() -> datetime:
    """Return naive UTC for the existing migration timestamp column."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


_INSERT_MIGRATION = text(
    "INSERT INTO schema_migrations(version, name, applied_at) "
    "VALUES (:version, :name, :applied_at)"
).bindparams(bindparam("applied_at", type_=DateTime()))


def _ensure_migration_table(engine: Engine) -> None:
    with engine.begin() as connection:
        connection.execute(text(
            "CREATE TABLE IF NOT EXISTS schema_migrations ("
            "version INTEGER PRIMARY KEY, "
            "name VARCHAR(200) NOT NULL, "
            "applied_at DATETIME NOT NULL)"
        ))


def _baseline_exists(engine: Engine) -> bool:
    tables = set(inspect(engine).get_table_names())
    return bool(tables - {MIGRATION_TABLE})


def _apply_baseline(engine: Engine) -> None:
    # Keep the v1 bootstrap frozen: canonical tables belong to migration 9.
    canonical_tables = {
        "canonical_approvals", "canonical_identity_bindings", "canonical_reports",
        "canonical_company_fiscal_calendars",
        "canonical_ingestion_audits",
        "canonical_report_versions", "canonical_financial_periods",
        "canonical_dimension_sets", "canonical_dimension_members",
        "canonical_financial_facts", "canonical_fact_provenance",
    }
    Base.metadata.create_all(
        bind=engine,
        tables=[table for table in Base.metadata.sorted_tables if table.name not in canonical_tables],
    )


def _add_column_if_missing(engine: Engine, table_name: str, column_name: str, definition: str) -> None:
    tables = set(inspect(engine).get_table_names())
    if table_name not in tables:
        return
    columns = {column["name"] for column in inspect(engine).get_columns(table_name)}
    if column_name not in columns:
        with engine.begin() as connection:
            connection.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {definition}"))


def _apply_mapping_and_derived_schema(engine: Engine) -> None:
    _add_column_if_missing(engine, "financial_metrics", "statement_type", "VARCHAR(30)")
    _add_column_if_missing(engine, "financial_metrics", "parent_metric_id", "INTEGER")
    _add_column_if_missing(engine, "financial_metrics", "sign_convention", "VARCHAR(20) NOT NULL DEFAULT 'NATURAL'")
    _add_column_if_missing(engine, "financial_metrics", "is_derived", "BOOLEAN NOT NULL DEFAULT 0")
    _add_column_if_missing(engine, "normalized_financial_facts", "raw_fact_id", "INTEGER")
    _add_column_if_missing(engine, "normalized_financial_facts", "mapping_decision_id", "INTEGER")

    Base.metadata.create_all(bind=engine, tables=[
        Base.metadata.tables["mapping_rules"],
        Base.metadata.tables["mapping_decisions"],
        Base.metadata.tables["derived_financial_facts"],
        Base.metadata.tables["derived_financial_fact_inputs"],
    ])


def _apply_normalized_provenance_schema(engine: Engine) -> None:
    Base.metadata.create_all(bind=engine, tables=[
        Base.metadata.tables["normalized_financial_fact_inputs"],
    ])


def _apply_report_current_version_index(engine: Engine) -> None:
    with engine.connect() as connection:
        duplicate_count = connection.execute(text(
            "SELECT COUNT(*) FROM ("
            "SELECT report_id FROM report_versions "
            "WHERE is_current_version = 1 "
            "GROUP BY report_id HAVING COUNT(*) > 1"
            ")"
        )).scalar_one()
    if duplicate_count:
        raise RuntimeError(
            "Cannot enforce one current ReportVersion per report: "
            "existing data contains multiple current versions. Resolve the data explicitly before migration 4."
        )

    with engine.begin() as connection:
        connection.execute(text(
            "CREATE UNIQUE INDEX IF NOT EXISTS uq_report_current_version "
            "ON report_versions(report_id) WHERE is_current_version = 1"
        ))


def _apply_market_daily_jalali_components(engine: Engine) -> None:
    """CHANGE-005: additive Jalali components for cross-year same-month analysis.

    Safe on legacy DBs that do not yet have market_daily (no-op).
    """
    _add_column_if_missing(engine, "market_daily", "jalali_year", "INTEGER")
    _add_column_if_missing(engine, "market_daily", "jalali_month", "INTEGER")
    _add_column_if_missing(engine, "market_daily", "jalali_day", "INTEGER")


def _apply_fx_rates_jalali_components(engine: Engine) -> None:
    """CHANGE-006: same Jalali date policy as market_daily for fx_rates.

    Additive jalali_year/month/day. rate_date remains for Gregorian-oriented rows;
    Jalali-sourced FX leaves rate_date NULL (no calendar conversion).
    """
    _add_column_if_missing(engine, "fx_rates", "jalali_year", "INTEGER")
    _add_column_if_missing(engine, "fx_rates", "jalali_month", "INTEGER")
    _add_column_if_missing(engine, "fx_rates", "jalali_day", "INTEGER")


def _apply_forecast_version_repository(engine: Engine) -> None:
    """CHANGE-007: Stage 5 append-only forecast version store (spec sections 24/28/29)."""
    LegacyForecastBase.metadata.create_all(bind=engine, tables=[
        LegacyForecastBase.metadata.tables["forecast_versions"],
        LegacyForecastBase.metadata.tables["forecast_input_refs"],
    ])


def _apply_remove_forecast_output_persistence(engine: Engine) -> None:
    """CHANGE-008: remove output storage while preserving input-side schema."""
    with engine.begin() as connection:
        connection.execute(text("DROP TABLE IF EXISTS forecast_input_refs"))
        connection.execute(text("DROP TABLE IF EXISTS forecast_versions"))


def _apply_canonical_jalali_excel_schema(engine: Engine) -> None:
    """CHANGE-009: additive canonical write store; never reinterpret legacy dates.

    Historical installations used version 9 for a different, unrecovered
    migration. The runner checks that history before invoking this migration.
    """
    if "companies" in set(inspect(engine).get_table_names()):
        with engine.connect() as connection:
            duplicate_tickers = connection.execute(text(
                "SELECT COUNT(*) FROM (SELECT ticker FROM companies GROUP BY ticker HAVING COUNT(*) > 1)"
            )).scalar_one()
            duplicate_symbols = connection.execute(text(
                "SELECT COUNT(*) FROM (SELECT codal_symbol FROM companies WHERE codal_symbol IS NOT NULL GROUP BY codal_symbol HAVING COUNT(*) > 1)"
            )).scalar_one()
        if duplicate_tickers or duplicate_symbols:
            raise RuntimeError(
                "Cannot enforce unique company symbols: duplicate legacy values require explicit resolution."
            )
        with engine.begin() as connection:
            connection.execute(text(
                "CREATE UNIQUE INDEX IF NOT EXISTS uq_company_ticker ON companies(ticker)"
            ))
            connection.execute(text(
                "CREATE UNIQUE INDEX IF NOT EXISTS uq_company_codal_symbol "
                "ON companies(codal_symbol) WHERE codal_symbol IS NOT NULL"
            ))
    with engine.begin() as connection:
        connection.execute(text(
            "CREATE TABLE IF NOT EXISTS canonical_approvals ("
            "approval_id INTEGER PRIMARY KEY, approval_ref VARCHAR(200) NOT NULL UNIQUE, "
            "approval_kind VARCHAR(40) NOT NULL, external_identity VARCHAR(200) NOT NULL, "
            "is_active BOOLEAN NOT NULL DEFAULT 1, "
            "CONSTRAINT uq_canonical_approval_identity UNIQUE(approval_kind, external_identity, approval_ref))"
        ))
    tables = [
        "canonical_identity_bindings", "canonical_reports", "canonical_report_versions",
        "canonical_company_fiscal_calendars",
        "canonical_ingestion_audits",
        "canonical_financial_periods", "canonical_dimension_sets",
        "canonical_dimension_members", "canonical_financial_facts",
        "canonical_fact_provenance",
    ]
    Base.metadata.create_all(bind=engine, tables=[Base.metadata.tables[name] for name in tables])


def _sqlite_rebuild_rate_type_check(connection, table_name: str) -> None:
    """Rebuild one FX table without discarding rows or caller-created objects."""
    row = connection.execute(text(
        "SELECT sql FROM sqlite_master WHERE type='table' AND name=:name"
    ), {"name": table_name}).first()
    if row is None or not row[0] or "EXCHANGE_CENTER" in row[0]:
        return
    if table_name not in {"fx_rates", "fx_conversion_rules"}:
        raise RuntimeError("Migration 10 encountered an unsupported FX table.")
    references = connection.execute(text(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' AND name != :name"
    ), {"name": table_name}).scalars().all()
    for ref_table in references:
        escaped = ref_table.replace('"', '""')
        if any(str(item[2]).lower() == table_name.lower()
               for item in connection.exec_driver_sql(f'PRAGMA foreign_key_list("{escaped}")').all()):
            raise RuntimeError(f"Migration 10 cannot rebuild {table_name}: another table references it.")

    temp_name = f"{table_name}__migration10"
    occupied = connection.execute(text(
        "SELECT 1 FROM sqlite_master WHERE name=:name LIMIT 1"
    ), {"name": temp_name}).first()
    if occupied:
        raise RuntimeError(f"Migration 10 stopped because reserved temporary name {temp_name} already exists.")
    schema_objects = connection.execute(text(
        "SELECT sql FROM sqlite_master WHERE tbl_name=:name "
        "AND type IN ('index','trigger') AND sql IS NOT NULL ORDER BY type, name"
    ), {"name": table_name}).scalars().all()
    ddl = re.sub(
        rf"^CREATE TABLE\s+{re.escape(table_name)}\b",
        f'CREATE TABLE "{temp_name}"', row[0], count=1, flags=re.IGNORECASE,
    )
    if ddl == row[0]:
        raise RuntimeError(f"Migration 10 cannot identify the CREATE TABLE statement for {table_name}.")
    ddl = re.sub(
        r"(rate_type\s+IN\s*\()([^)]*)(\))",
        lambda match: match.group(1) + match.group(2) + ",'EXCHANGE_CENTER'" + match.group(3),
        ddl, count=1, flags=re.IGNORECASE,
    )
    if "EXCHANGE_CENTER" not in ddl:
        raise RuntimeError(f"Migration 10 could not locate the rate_type constraint on {table_name}.")
    connection.exec_driver_sql(ddl)
    columns = [item[1] for item in connection.exec_driver_sql(f'PRAGMA table_info("{table_name}")').all()]
    names = ", ".join(f'"{name}"' for name in columns)
    connection.exec_driver_sql(f'INSERT INTO "{temp_name}" ({names}) SELECT {names} FROM "{table_name}"')
    connection.exec_driver_sql(f'DROP TABLE "{table_name}"')
    connection.exec_driver_sql(f'ALTER TABLE "{temp_name}" RENAME TO "{table_name}"')
    for sql in schema_objects:
        connection.exec_driver_sql(sql)


def _apply_market_fx_approval_scope_schema(engine: Engine) -> None:
    """CHANGE-010: EXCHANGE_CENTER, Jalali natural keys, and approval scopes."""
    if engine.dialect.name != "sqlite":
        raise RuntimeError("Migration 10 currently supports the repository's SQLite schema only.")
    tables = set(inspect(engine).get_table_names())
    required = {"market_daily", "fx_rates", "fx_conversion_rules", "canonical_approvals", "canonical_fact_provenance"}
    if not required.issubset(tables):
        raise RuntimeError("Migration 10 requires the completed v9 canonical/Market/FX schema.")

    with engine.begin() as connection:
        duplicate_market = connection.execute(text(
            "SELECT COUNT(*) FROM (SELECT company_id, jalali_year, jalali_month, jalali_day "
            "FROM market_daily WHERE jalali_year IS NOT NULL AND jalali_month IS NOT NULL AND jalali_day IS NOT NULL "
            "GROUP BY company_id, jalali_year, jalali_month, jalali_day HAVING COUNT(*) > 1)"
        )).scalar_one()
        duplicate_fx = connection.execute(text(
            "SELECT COUNT(*) FROM (SELECT jalali_year, jalali_month, jalali_day, currency_from, currency_to, rate_type "
            "FROM fx_rates WHERE jalali_year IS NOT NULL AND jalali_month IS NOT NULL AND jalali_day IS NOT NULL "
            "GROUP BY jalali_year, jalali_month, jalali_day, currency_from, currency_to, rate_type HAVING COUNT(*) > 1)"
        )).scalar_one()
        if duplicate_market or duplicate_fx:
            raise RuntimeError("Cannot enforce Jalali uniqueness: duplicate MarketDaily or FX natural keys exist.")
        for table_name in ("market_daily", "fx_rates"):
            partial = connection.execute(text(
                f'SELECT COUNT(*) FROM "{table_name}" WHERE '
                "(jalali_year IS NOT NULL OR jalali_month IS NOT NULL OR jalali_day IS NOT NULL) AND "
                "(jalali_year IS NULL OR jalali_month IS NULL OR jalali_day IS NULL)"
            )).scalar_one()
            if partial:
                raise RuntimeError(f"Cannot enforce Jalali identity completeness: partial date exists in {table_name}.")

        _sqlite_rebuild_rate_type_check(connection, "fx_rates")
        _sqlite_rebuild_rate_type_check(connection, "fx_conversion_rules")
        approval_columns = {item["name"] for item in inspect(connection).get_columns("canonical_approvals")}
        if "scope_json" not in approval_columns:
            connection.exec_driver_sql("ALTER TABLE canonical_approvals ADD COLUMN scope_json TEXT NOT NULL DEFAULT '{}'")
        provenance_columns = {item["name"] for item in inspect(connection).get_columns("canonical_fact_provenance")}
        if "source_token" not in provenance_columns:
            connection.exec_driver_sql("ALTER TABLE canonical_fact_provenance ADD COLUMN source_token TEXT NULL")

        connection.exec_driver_sql(
            "CREATE UNIQUE INDEX IF NOT EXISTS uq_market_daily_jalali_identity "
            "ON market_daily(company_id, jalali_year, jalali_month, jalali_day) "
            "WHERE jalali_year IS NOT NULL AND jalali_month IS NOT NULL AND jalali_day IS NOT NULL"
        )
        connection.exec_driver_sql(
            "CREATE UNIQUE INDEX IF NOT EXISTS uq_fx_jalali_identity "
            "ON fx_rates(jalali_year, jalali_month, jalali_day, currency_from, currency_to, rate_type) "
            "WHERE jalali_year IS NOT NULL AND jalali_month IS NOT NULL AND jalali_day IS NOT NULL"
        )
        for table_name, prefix in (("market_daily", "market"), ("fx_rates", "fx")):
            for operation in ("INSERT", "UPDATE"):
                trigger = f"trg_{prefix}_jalali_identity_{operation.lower()}_complete"
                connection.exec_driver_sql(
                    f'CREATE TRIGGER IF NOT EXISTS "{trigger}" BEFORE {operation} ON "{table_name}" '
                    "WHEN (NEW.jalali_year IS NULL AND (NEW.jalali_month IS NOT NULL OR NEW.jalali_day IS NOT NULL)) "
                    "OR (NEW.jalali_month IS NULL AND (NEW.jalali_year IS NOT NULL OR NEW.jalali_day IS NOT NULL)) "
                    "OR (NEW.jalali_day IS NULL AND (NEW.jalali_year IS NOT NULL OR NEW.jalali_month IS NOT NULL)) "
                    "BEGIN SELECT RAISE(ABORT, 'JALALI_IDENTITY_INCOMPLETE'); END"
                )


def _migration_list() -> Iterable[Migration]:
    return (
        Migration(1, "baseline_schema", _apply_baseline),
        Migration(2, "mapping_and_derived_schema", _apply_mapping_and_derived_schema),
        Migration(3, "normalized_fact_multi_source_provenance", _apply_normalized_provenance_schema),
        Migration(4, "one_current_report_version", _apply_report_current_version_index),
        Migration(5, "market_daily_jalali_components", _apply_market_daily_jalali_components),
        Migration(6, "fx_rates_jalali_components", _apply_fx_rates_jalali_components),
        Migration(7, "forecast_version_repository", _apply_forecast_version_repository),
        Migration(8, "remove_forecast_output_persistence", _apply_remove_forecast_output_persistence),
        Migration(9, "canonical_jalali_excel_writer", _apply_canonical_jalali_excel_schema),
        Migration(10, "market_fx_approval_scope_schema", _apply_market_fx_approval_scope_schema),
    )


class MigrationRunner:
    """Apply ordered, idempotent Stage 1 schema migrations."""

    def __init__(self, engine: Engine):
        self.engine = engine

    def current_version(self) -> int:
        _ensure_migration_table(self.engine)
        with self.engine.connect() as connection:
            value = connection.execute(text("SELECT MAX(version) FROM schema_migrations")).scalar()
        return int(value or 0)

    def upgrade(self) -> int:
        _ensure_migration_table(self.engine)
        current = self.current_version()

        # Never reinterpret a historical v9 ledger entry as this migration.
        if current >= 9:
            with self.engine.connect() as connection:
                name = connection.execute(text(
                    "SELECT name FROM schema_migrations WHERE version = 9"
                )).scalar_one_or_none()
            if name != "canonical_jalali_excel_writer":
                raise RuntimeError(
                    "Migration 9 history belongs to another migration; reconcile its source before upgrade."
                )

        if current >= 10:
            with self.engine.connect() as connection:
                name = connection.execute(text(
                    "SELECT name FROM schema_migrations WHERE version = 10"
                )).scalar_one_or_none()
            if name != "market_fx_approval_scope_schema":
                raise RuntimeError("Migration 10 history belongs to another migration; reconcile its source before upgrade.")

        if current == 0 and _baseline_exists(self.engine):
            with self.engine.begin() as connection:
                connection.execute(
                    _INSERT_MIGRATION,
                    {"version": 1, "name": "legacy_baseline", "applied_at": _utc_now_naive()},
                )
            current = 1

        for migration in _migration_list():
            if migration.version <= current:
                continue
            migration.apply(self.engine)
            with self.engine.begin() as connection:
                connection.execute(
                    _INSERT_MIGRATION,
                    {"version": migration.version, "name": migration.name, "applied_at": _utc_now_naive()},
                )
            current = migration.version
        return current
