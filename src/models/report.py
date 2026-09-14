from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from datetime import datetime
from src.core.database import Base

class Report(Base):
    __tablename__ = "reports"

    report_id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.company_id"), nullable=False)
    period_id = Column(Integer, ForeignKey("financial_periods.period_id"), nullable=False)
    codal_tracing_id = Column(String(100), unique=True, nullable=True)
    title = Column(String(300), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class ReportVersion(Base):
    __tablename__ = "report_versions"

    version_id = Column(Integer, primary_key=True, autoincrement=True)
    report_id = Column(Integer, ForeignKey("reports.report_id"), nullable=False)
    version_number = Column(Integer, nullable=False, default=1)
    published_at = Column(DateTime, nullable=False)  # تاریخ انتشار اصلی برای عدم بروز Look-Ahead Bias
    is_restatement = Column(Boolean, nullable=False, default=False)  # آیا اصلاحیه است؟
    is_latest = Column(Boolean, nullable=False, default=True)
    raw_source_url = Column(String(500), nullable=True)
    ingestion_run_id = Column(Integer, ForeignKey("ingestion_runs.ingestion_id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("report_id", "version_number", name="uq_report_version"),
    )