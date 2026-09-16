from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
)
from src.core.database import Base


class RawFinancialFact(Base):
    __tablename__ = "raw_financial_facts"

    raw_fact_id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.company_id"), nullable=False)
    report_version_id = Column(Integer, ForeignKey("report_versions.report_version_id"), nullable=False)
    period_id = Column(Integer, ForeignKey("financial_periods.period_id"), nullable=False)
    raw_item_name = Column(String(300), nullable=False)
    raw_item_code = Column(String(100), nullable=True)
    value = Column(Numeric(precision=30, scale=4), nullable=True)
    unit = Column(String(50), nullable=True)
    currency = Column(String(20), nullable=True)
    source_section = Column(String(150), nullable=True)
    source_row = Column(Integer, nullable=True)
    source_column = Column(String(100), nullable=True)


class FinancialMetric(Base):
    __tablename__ = "financial_metrics"

    metric_id = Column(Integer, primary_key=True, autoincrement=True)
    metric_code = Column(String(100), nullable=False, unique=True)
    metric_name = Column(String(200), nullable=False)
    category = Column(String(50), nullable=False)
    industry_id = Column(Integer, ForeignKey("industries.industry_id", ondelete="SET NULL"), nullable=True)
    statement_type = Column(String(30), nullable=True)
    parent_metric_id = Column(Integer, ForeignKey("financial_metrics.metric_id", ondelete="SET NULL"), nullable=True)
    value_type = Column(String(30), nullable=False, default="CURRENCY_IRR")
    flow_or_stock = Column(String(10), nullable=False)
    sign_convention = Column(String(20), nullable=False, default="NATURAL")
    is_derived = Column(Boolean, nullable=False, default=False)

    __table_args__ = (
        CheckConstraint("flow_or_stock IN ('FLOW','STOCK')", name="chk_metric_flow_stock"),
        CheckConstraint(
            "statement_type IS NULL OR statement_type IN ('INCOME','BALANCE_SHEET','CASH_FLOW','EQUITY','GENERAL')",
            name="chk_metric_statement_type",
        ),
        CheckConstraint(
            "sign_convention IN ('NATURAL','EXPENSE_POSITIVE','EXPENSE_NEGATIVE')",
            name="chk_metric_sign_convention",
        ),
    )


class MappingRule(Base):
    __tablename__ = "mapping_rules"

    mapping_rule_id = Column(Integer, primary_key=True, autoincrement=True)
    rule_code = Column(String(100), nullable=False)
    rule_version = Column(String(30), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)

    __table_args__ = (
        UniqueConstraint("rule_code", "rule_version", name="uq_mapping_rule_version"),
    )


class MappingDecision(Base):
    __tablename__ = "mapping_decisions"

    mapping_decision_id = Column(Integer, primary_key=True, autoincrement=True)
    raw_fact_id = Column(Integer, ForeignKey("raw_financial_facts.raw_fact_id"), nullable=False)
    metric_id = Column(Integer, ForeignKey("financial_metrics.metric_id"), nullable=True)
    mapping_rule_id = Column(Integer, ForeignKey("mapping_rules.mapping_rule_id"), nullable=True)
    mapping_method = Column(String(30), nullable=False)
    confidence = Column(Numeric(precision=5, scale=2), nullable=True)
    review_status = Column(String(20), nullable=False, default="REVIEW_REQUIRED")
    composition_role = Column(String(20), nullable=True)
    transformation_spec = Column(Text, nullable=True)
    reviewer = Column(String(150), nullable=True)
    reviewed_at = Column(DateTime, nullable=True)
    note = Column(Text, nullable=True)

    __table_args__ = (
        CheckConstraint(
            "mapping_method IN ('TITLE_EXACT','ALIAS','PATTERN','POSITION','MANUAL','DERIVED')",
            name="chk_mapping_method",
        ),
        CheckConstraint(
            "review_status IN ('AUTO_MAPPED','REVIEW_REQUIRED','APPROVED','REJECTED','UNMAPPED')",
            name="chk_mapping_review_status",
        ),
        CheckConstraint(
            "composition_role IS NULL OR composition_role IN ('COMPONENT','SUBTOTAL','TOTAL','DISCLOSURE')",
            name="chk_mapping_composition_role",
        ),
        CheckConstraint(
            "confidence IS NULL OR (confidence >= 0 AND confidence <= 100)",
            name="chk_mapping_confidence",
        ),
    )


class NormalizedFinancialFact(Base):
    __tablename__ = "normalized_financial_facts"

    fact_id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.company_id"), nullable=False)
    period_id = Column(Integer, ForeignKey("financial_periods.period_id"), nullable=False)
    metric_id = Column(Integer, ForeignKey("financial_metrics.metric_id"), nullable=False)
    raw_fact_id = Column(Integer, ForeignKey("raw_financial_facts.raw_fact_id"), nullable=True)
    mapping_decision_id = Column(Integer, ForeignKey("mapping_decisions.mapping_decision_id"), nullable=True)
    value_irr = Column(Numeric(precision=30, scale=4), nullable=True)
    source_report_version_id = Column(Integer, ForeignKey("report_versions.report_version_id"), nullable=False)
    normalization_rule_id = Column(Integer, nullable=True)
    quality_status = Column(String(20), nullable=False, default="VALID")

    __table_args__ = (
        UniqueConstraint(
            "company_id", "period_id", "metric_id", "source_report_version_id",
            name="uq_normalized_fact",
        ),
        CheckConstraint(
            "quality_status IN ('VALID','MISSING','ESTIMATED','RESTATED','SUSPICIOUS','UNMAPPED')",
            name="chk_normalized_quality_status",
        ),
    )


class DerivedFinancialFact(Base):
    __tablename__ = "derived_financial_facts"

    derived_fact_id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.company_id"), nullable=False)
    period_id = Column(Integer, ForeignKey("financial_periods.period_id"), nullable=False)
    metric_id = Column(Integer, ForeignKey("financial_metrics.metric_id"), nullable=False)
    value_irr = Column(Numeric(precision=30, scale=4), nullable=True)
    formula_code = Column(String(100), nullable=False)
    formula_version = Column(String(30), nullable=False)
    source_report_version_id = Column(Integer, ForeignKey("report_versions.report_version_id"), nullable=False)
    quality_status = Column(String(20), nullable=False, default="VALID")
    data_cutoff_datetime = Column(DateTime, nullable=False)
    calculated_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint(
            "company_id", "period_id", "metric_id", "formula_code", "formula_version",
            "source_report_version_id", name="uq_derived_financial_fact",
        ),
        CheckConstraint(
            "quality_status IN ('VALID','MISSING','ESTIMATED','SUSPICIOUS')",
            name="chk_derived_quality_status",
        ),
    )


class DerivedFinancialFactInput(Base):
    __tablename__ = "derived_financial_fact_inputs"

    input_id = Column(Integer, primary_key=True, autoincrement=True)
    derived_fact_id = Column(Integer, ForeignKey("derived_financial_facts.derived_fact_id"), nullable=False)
    normalized_fact_id = Column(Integer, ForeignKey("normalized_financial_facts.fact_id"), nullable=True)
    derived_input_fact_id = Column(Integer, ForeignKey("derived_financial_facts.derived_fact_id"), nullable=True)
    input_role = Column(String(100), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "(normalized_fact_id IS NOT NULL AND derived_input_fact_id IS NULL) OR "
            "(normalized_fact_id IS NULL AND derived_input_fact_id IS NOT NULL)",
            name="chk_derived_input_source",
        ),
        UniqueConstraint(
            "derived_fact_id", "normalized_fact_id", "derived_input_fact_id", "input_role",
            name="uq_derived_fact_input",
        ),
    )
