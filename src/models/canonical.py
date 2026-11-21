"""Additive canonical BANK financial storage for approved Excel inputs.

Legacy Gregorian tables remain available to their existing consumers. These
tables are the Jalali-native write/read boundary for newly admitted facts.
"""
from datetime import datetime, timezone

from sqlalchemy import (
    BigInteger, Boolean, CheckConstraint, Column, DateTime, ForeignKey,
    Integer, String, Text, UniqueConstraint,
)

from src.core.database import Base


def _utc_now_naive() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class CanonicalApproval(Base):
    __tablename__ = "canonical_approvals"
    approval_id = Column(Integer, primary_key=True, autoincrement=True)
    approval_ref = Column(String(200), nullable=False, unique=True)
    approval_kind = Column(String(40), nullable=False)
    external_identity = Column(String(200), nullable=False)
    scope_json = Column(Text, nullable=False, default="{}")
    is_active = Column(Boolean, nullable=False, default=True)
    __table_args__ = (UniqueConstraint("approval_kind", "external_identity", "approval_ref", name="uq_canonical_approval_identity"),)


class CanonicalIdentityBinding(Base):
    __tablename__ = "canonical_identity_bindings"
    binding_id = Column(Integer, primary_key=True, autoincrement=True)
    identity_kind = Column(String(40), nullable=False)
    external_identity = Column(String(200), nullable=False)
    internal_id = Column(Integer, nullable=False)
    approval_ref = Column(String(200), ForeignKey("canonical_approvals.approval_ref"), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    __table_args__ = (UniqueConstraint("identity_kind", "external_identity", name="uq_canonical_binding_external"),)


class CanonicalCompanyFiscalCalendar(Base):
    """Explicit company fiscal-year start; absence means unknown/fail-closed."""
    __tablename__ = "canonical_company_fiscal_calendars"
    company_id = Column(Integer, ForeignKey("companies.company_id", ondelete="CASCADE"), primary_key=True)
    fiscal_year_start_month = Column(Integer, nullable=False)
    source_identity = Column(String(200), nullable=False)
    approval_ref = Column(String(200), ForeignKey("canonical_approvals.approval_ref"), nullable=False)
    __table_args__ = (CheckConstraint("fiscal_year_start_month BETWEEN 1 AND 12", name="chk_canonical_fiscal_start_month"),)


class CanonicalIngestionAudit(Base):
    __tablename__ = "canonical_ingestion_audits"
    ingestion_id = Column(Integer, ForeignKey("ingestion_runs.ingestion_id", ondelete="CASCADE"), primary_key=True)
    records_accepted = Column(Integer, nullable=False, default=0)
    records_duplicate = Column(Integer, nullable=False, default=0)
    records_rejected = Column(Integer, nullable=False, default=0)
    error_code = Column(String(80), nullable=True)
    __table_args__ = (
        CheckConstraint("records_accepted >= 0 AND records_duplicate >= 0 AND records_rejected >= 0", name="chk_canonical_audit_counts"),
    )


class CanonicalReport(Base):
    __tablename__ = "canonical_reports"
    canonical_report_id = Column(Integer, primary_key=True, autoincrement=True)
    external_report_id = Column(String(200), nullable=False, unique=True)
    company_id = Column(Integer, ForeignKey("companies.company_id"), nullable=False)
    report_type_id = Column(String(200), nullable=False)
    title = Column(String(300), nullable=False)
    created_at = Column(DateTime, nullable=False, default=_utc_now_naive)


class CanonicalReportVersion(Base):
    __tablename__ = "canonical_report_versions"
    canonical_report_version_id = Column(Integer, primary_key=True, autoincrement=True)
    canonical_report_id = Column(Integer, ForeignKey("canonical_reports.canonical_report_id"), nullable=False)
    external_version_id = Column(String(200), nullable=False, unique=True)
    version_number = Column(Integer, nullable=False)
    publication_datetime = Column(DateTime, nullable=False)
    is_audited = Column(Boolean, nullable=False)
    is_restated = Column(Boolean, nullable=False)
    scenario_approval_ref = Column(String(200), ForeignKey("canonical_approvals.approval_ref"), nullable=False)
    source_identity = Column(String(200), nullable=False)
    revision_identity = Column(String(200), nullable=False)
    source_artifact_sha256 = Column(String(64), nullable=False)
    extraction_standard_id = Column(String(200), nullable=False)
    extraction_standard_approval_ref = Column(String(200), ForeignKey("canonical_approvals.approval_ref"), nullable=False)
    template_id = Column(String(200), nullable=False)
    template_version = Column(String(100), nullable=False)
    template_sha256 = Column(String(64), nullable=False)
    template_approval_ref = Column(String(200), ForeignKey("canonical_approvals.approval_ref"), nullable=False)
    extraction_owner = Column(String(200), nullable=False)
    supersedes_version_id = Column(Integer, ForeignKey("canonical_report_versions.canonical_report_version_id"), nullable=True)
    created_at = Column(DateTime, nullable=False, default=_utc_now_naive)
    __table_args__ = (
        UniqueConstraint("canonical_report_id", "version_number", name="uq_canonical_report_version_number"),
        UniqueConstraint("canonical_report_id", "source_identity", "revision_identity", name="uq_canonical_source_revision"),
        CheckConstraint("version_number > 0", name="chk_canonical_version_positive"),
    )


class CanonicalFinancialPeriod(Base):
    __tablename__ = "canonical_financial_periods"
    period_id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.company_id"), nullable=False)
    temporal_type = Column(String(10), nullable=False)
    start_year = Column(Integer, nullable=False)
    start_month = Column(Integer, nullable=False)
    start_day = Column(Integer, nullable=False)
    end_year = Column(Integer, nullable=False)
    end_month = Column(Integer, nullable=False)
    end_day = Column(Integer, nullable=False)
    months_length = Column(Integer, nullable=True)
    __table_args__ = (
        UniqueConstraint("company_id", "temporal_type", "start_year", "start_month", "start_day", "end_year", "end_month", "end_day", name="uq_canonical_period_identity"),
        CheckConstraint("temporal_type IN ('INSTANT','DURATION')", name="chk_canonical_period_temporal"),
        CheckConstraint("start_year > 0 AND end_year > 0 AND start_month BETWEEN 1 AND 12 AND end_month BETWEEN 1 AND 12 AND start_day BETWEEN 1 AND 31 AND end_day BETWEEN 1 AND 31", name="chk_canonical_period_components"),
        CheckConstraint("start_year < end_year OR (start_year = end_year AND (start_month < end_month OR (start_month = end_month AND start_day <= end_day)))", name="chk_canonical_period_order"),
        CheckConstraint("(temporal_type = 'INSTANT' AND start_year = end_year AND start_month = end_month AND start_day = end_day) OR (temporal_type = 'DURATION' AND (start_year < end_year OR start_month < end_month OR start_day < end_day))", name="chk_canonical_period_range"),
        CheckConstraint("months_length IS NULL OR months_length >= 0", name="chk_canonical_period_months"),
        CheckConstraint("(temporal_type = 'INSTANT' AND months_length = 0) OR (temporal_type = 'DURATION' AND (months_length IS NULL OR months_length > 0))", name="chk_canonical_period_month_length_semantics"),
    )


class CanonicalDimensionSet(Base):
    __tablename__ = "canonical_dimension_sets"
    dimension_set_id = Column(Integer, primary_key=True, autoincrement=True)
    canonical_key = Column(String(2000), nullable=False, unique=True)


class CanonicalDimensionMember(Base):
    __tablename__ = "canonical_dimension_members"
    member_id = Column(Integer, primary_key=True, autoincrement=True)
    dimension_set_id = Column(Integer, ForeignKey("canonical_dimension_sets.dimension_set_id", ondelete="CASCADE"), nullable=False)
    dimension_id = Column(String(200), nullable=False)
    dimension_value_id = Column(String(200), nullable=False)
    dimension_approval_ref = Column(String(200), ForeignKey("canonical_approvals.approval_ref"), nullable=False)
    value_approval_ref = Column(String(200), ForeignKey("canonical_approvals.approval_ref"), nullable=False)
    __table_args__ = (UniqueConstraint("dimension_set_id", "dimension_id", name="uq_canonical_dimension_member"),)


class CanonicalFinancialFact(Base):
    __tablename__ = "canonical_financial_facts"
    fact_id = Column(Integer, primary_key=True, autoincrement=True)
    report_version_id = Column(Integer, ForeignKey("canonical_report_versions.canonical_report_version_id"), nullable=False)
    period_id = Column(Integer, ForeignKey("canonical_financial_periods.period_id"), nullable=False)
    metric_id = Column(Integer, ForeignKey("financial_metrics.metric_id"), nullable=False)
    dimension_set_id = Column(Integer, ForeignKey("canonical_dimension_sets.dimension_set_id"), nullable=False)
    temporal_type = Column(String(10), nullable=False)
    duration_basis = Column(String(12), nullable=True)
    value_integer = Column(BigInteger, nullable=True)
    value_state = Column(String(24), nullable=False)
    value_origin = Column(String(24), nullable=False)
    source_unit = Column(String(100), nullable=False)
    source_currency = Column(String(30), nullable=False)
    source_scale = Column(String(50), nullable=False)
    scenario = Column(String(12), nullable=False, default="ACTUAL")
    __table_args__ = (
        UniqueConstraint("report_version_id", "period_id", "metric_id", "dimension_set_id", name="uq_canonical_fact_identity"),
        CheckConstraint("(value_state = 'REPORTED_VALUE' AND value_integer IS NOT NULL) OR (value_state = 'ZERO_FALLBACK' AND value_integer = 0) OR (value_state = 'REPORTED_NULL' AND value_integer IS NULL)", name="chk_canonical_fact_value_state"),
        CheckConstraint("(value_state = 'ZERO_FALLBACK' AND value_origin = 'ZERO_FALLBACK') OR (value_state IN ('REPORTED_VALUE','REPORTED_NULL') AND value_origin = 'SOURCE_REPORTED')", name="chk_canonical_fact_origin_state"),
        CheckConstraint("temporal_type IN ('INSTANT','DURATION')", name="chk_canonical_fact_temporal"),
        CheckConstraint("(temporal_type = 'INSTANT' AND duration_basis IS NULL) OR (temporal_type = 'DURATION' AND duration_basis IN ('YTD','STANDALONE'))", name="chk_canonical_fact_basis"),
        CheckConstraint("value_origin IN ('SOURCE_REPORTED','ZERO_FALLBACK')", name="chk_canonical_fact_origin"),
        CheckConstraint("scenario IN ('ACTUAL','FORECAST','PLAN')", name="chk_canonical_fact_scenario"),
    )


class CanonicalFactProvenance(Base):
    __tablename__ = "canonical_fact_provenance"
    provenance_id = Column(Integer, primary_key=True, autoincrement=True)
    fact_id = Column(Integer, ForeignKey("canonical_financial_facts.fact_id", ondelete="CASCADE"), nullable=False, unique=True)
    source_identity = Column(String(200), nullable=False)
    revision_identity = Column(String(200), nullable=False)
    source_artifact_sha256 = Column(String(64), nullable=False)
    worksheet_ordinal = Column(Integer, nullable=False)
    worksheet_name = Column(String(200), nullable=False)
    source_coordinate = Column(String(30), nullable=False)
    source_value_kind = Column(String(20), nullable=False)
    extraction_owner = Column(String(200), nullable=False)
    source_decimal_text = Column(Text, nullable=False)
    source_token = Column(Text, nullable=True)
    approval_references_json = Column(Text, nullable=False)

