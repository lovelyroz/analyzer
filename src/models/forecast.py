"""Stage 5 forecast persistence (spec sections 24, 28, 29).

Stage 5 forecasts are append-only: a new forecast for the same logical identity
never replaces the previous one, which stays readable as an earlier version
(spec section 24). The audit trail back to the report version a forecast was
built from is a separate table, so one forecast can point at several inputs
without a second PIT implementation (spec section 29).
"""

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)

from src.core.database import Base


class ForecastVersion(Base):
    """One immutable version of one scenario forecast (spec section 28).

    The business key (company, period, horizon, scenario) identifies the
    forecast *series*; ``version_number`` identifies which revision of it this
    row is. The pair is unique, so a save can only ever append a new version.
    """

    __tablename__ = "forecast_versions"

    forecast_version_id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.company_id"), nullable=False)
    forecast_period_id = Column(Integer, ForeignKey("financial_periods.period_id"), nullable=False)
    forecast_horizon = Column(String(10), nullable=False)
    scenario = Column(String(20), nullable=False)
    version_number = Column(Integer, nullable=False)

    forecast_timestamp = Column(DateTime, nullable=False)
    data_cutoff_datetime = Column(DateTime, nullable=False)
    model_version = Column(String(50), nullable=False)
    forecast_method = Column(String(50), nullable=False)
    data_quality = Column(String(30), nullable=False)
    baseline_method = Column(String(50), nullable=False, default="UNKNOWN")
    industry_code = Column(String(50), nullable=False)

    revenue = Column(Numeric(precision=30, scale=4), nullable=True)
    operating_profit = Column(Numeric(precision=30, scale=4), nullable=True)
    operating_margin = Column(Numeric(precision=18, scale=10), nullable=True)
    net_profit = Column(Numeric(precision=30, scale=4), nullable=True)
    eps = Column(Numeric(precision=30, scale=4), nullable=True)
    roe = Column(Numeric(precision=18, scale=10), nullable=True)

    assumptions = Column(Text, nullable=True)
    stage4_provenance = Column(Text, nullable=True)

    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "forecast_period_id",
            "forecast_horizon",
            "scenario",
            "version_number",
            name="uq_forecast_version",
        ),
        CheckConstraint("version_number >= 1", name="chk_forecast_version_number"),
        CheckConstraint(
            "forecast_horizon IN ('1M','3M','6M','12M')",
            name="chk_forecast_horizon",
        ),
        CheckConstraint(
            "scenario IN ('BEAR','BASE','BULL')",
            name="chk_forecast_scenario",
        ),
        Index("ix_forecast_series", "company_id", "forecast_period_id",
              "forecast_horizon", "scenario", "version_number"),
    )


class ForecastInputRefModel(Base):
    """Provenance bridge from a stored forecast to the facts that fed it.

    One row per input reference, mirroring the in-memory ``ForecastInputRef``.
    ``available_at`` is what makes a forecast re-checkable for look-ahead
    (spec section 25): it is the instant the input became knowable.
    """

    __tablename__ = "forecast_input_refs"

    input_ref_id = Column(Integer, primary_key=True, autoincrement=True)
    forecast_version_id = Column(
        Integer,
        ForeignKey("forecast_versions.forecast_version_id", ondelete="CASCADE"),
        nullable=False,
    )
    fact_key = Column(String(200), nullable=False)
    report_version_id = Column(
        Integer,
        ForeignKey("report_versions.report_version_id", ondelete="SET NULL"),
        nullable=True,
    )
    available_at = Column(DateTime, nullable=True)
    source = Column(String(200), nullable=True)

    __table_args__ = (
        UniqueConstraint(
            "forecast_version_id", "fact_key", name="uq_forecast_input_ref"
        ),
        Index("ix_forecast_input_ref_forecast", "forecast_version_id"),
    )
