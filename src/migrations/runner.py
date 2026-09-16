from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Iterable

from sqlalchemy import inspect, text
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
from src.models.period import FinancialPeriod  # noqa: F401
from src.models.report import Report, ReportVersion  # noqa: F401
from src.models.share_action import CorporateAction, ShareCountHistory  # noqa: F401


@dataclass(frozen=True)
class Migration:
    version: int
    name: str
    apply: Callable[[Engine], None]


MIGRATION_TABLE = "schema_migrations"


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
    # Version 1 is the initial schema bootstrap for a new database.
    Base.metadata.create_all(bind=engine)


def _add_column_if_missing(engine: Engine, table_name: str, column_name: str, definition: str) -> None:
    columns = {column["name"] for column in inspect(engine).get_columns(table_name)}
    if column_name not in columns:
        with engine.begin() as connection:
            connection.execute(text(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {definition}"))


def _apply_mapping_and_derived_schema(engine: Engine) -> None:
    # Existing tables are upgraded without rewriting existing values.
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
    # Adds the multi-source provenance bridge without rewriting existing facts.
    Base.metadata.create_all(bind=engine, tables=[
        Base.metadata.tables["normalized_financial_fact_inputs"],
    ])


def _migration_list() -> Iterable[Migration]:
    return (
        Migration(1, "baseline_schema", _apply_baseline),
        Migration(2, "mapping_and_derived_schema", _apply_mapping_and_derived_schema),
        Migration(3, "normalized_fact_multi_source_provenance", _apply_normalized_provenance_schema),
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

        if current == 0 and _baseline_exists(self.engine):
            with self.engine.begin() as connection:
                connection.execute(
                    text("INSERT INTO schema_migrations(version, name, applied_at) VALUES (:version, :name, :applied_at)"),
                    {"version": 1, "name": "legacy_baseline", "applied_at": datetime.utcnow()},
                )
            current = 1

        for migration in _migration_list():
            if migration.version <= current:
                continue
            migration.apply(self.engine)
            with self.engine.begin() as connection:
                connection.execute(
                    text("INSERT INTO schema_migrations(version, name, applied_at) VALUES (:version, :name, :applied_at)"),
                    {"version": migration.version, "name": migration.name, "applied_at": datetime.utcnow()},
                )
            current = migration.version
        return current
