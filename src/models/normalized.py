from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, UniqueConstraint
from src.core.database import Base

class RawFinancialFact(Base):
    __tablename__ = "raw_financial_facts"

    raw_fact_id = Column(Integer, primary_key=True, autoincrement=True)
    version_id = Column(Integer, ForeignKey("report_versions.version_id"), nullable=False)
    raw_label = Column(String(300), nullable=False)  # عنوان خام در کدال
    raw_value = Column(Numeric(precision=30, scale=4), nullable=True)  # حفظ NULL در صورت عدم وجود
    table_name = Column(String(100), nullable=True)
    row_number = Column(Integer, nullable=True)
    column_name = Column(String(100), nullable=True)

class FinancialMetric(Base):
    __tablename__ = "financial_metrics"

    metric_id = Column(Integer, primary_key=True, autoincrement=True)
    metric_code = Column(String(100), nullable=False, unique=True)
    metric_name = Column(String(200), nullable=False)
    category = Column(String(50), nullable=False)
    industry_id = Column(Integer, ForeignKey("industries.industry_id", ondelete="SET NULL"), nullable=True)
    value_type = Column(String(30), nullable=False, default="CURRENCY_IRR")
    flow_or_stock = Column(String(10), nullable=False)  # 'FLOW' یا 'STOCK'

class NormalizedFinancialFact(Base):
    __tablename__ = "normalized_financial_facts"

    fact_id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.company_id"), nullable=False)
    period_id = Column(Integer, ForeignKey("financial_periods.period_id"), nullable=False)
    metric_id = Column(Integer, ForeignKey("financial_metrics.metric_id"), nullable=False)
    value_irr = Column(Numeric(precision=30, scale=4), nullable=True)  # پایه ریالی (IRR)
    source_report_version_id = Column(Integer, ForeignKey("report_versions.version_id"), nullable=False)
    normalization_rule_id = Column(Integer, nullable=True)
    quality_status = Column(String(20), nullable=False, default="VALID")  # VALID, RESTATED, ESTIMATED

    __table_args__ = (
        UniqueConstraint("company_id", "period_id", "metric_id", "source_report_version_id", name="uq_normalized_fact"),
    )