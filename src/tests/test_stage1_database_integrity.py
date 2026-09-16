from sqlalchemy import create_engine, text

from src.core.database import Base
from src.migrations.runner import MigrationRunner
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


def test_migration_reaches_version_four_and_is_idempotent():
    engine = create_engine("sqlite:///:memory:")
    runner = MigrationRunner(engine)

    assert runner.upgrade() == 4
    assert runner.upgrade() == 4
    tables = set(__import__("sqlalchemy").inspect(engine).get_table_names())
    assert "normalized_financial_fact_inputs" in tables

    with engine.connect() as connection:
        versions = connection.execute(text("SELECT version FROM schema_migrations ORDER BY version")).scalars().all()
    assert versions == [1, 2, 3, 4]


def test_current_report_version_unique_index_is_present_on_bootstrap():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    indexes = __import__("sqlalchemy").inspect(engine).get_indexes("report_versions")
    assert any(index["name"] == "uq_report_current_version" and index["unique"] for index in indexes)
