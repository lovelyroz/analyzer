from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    UniqueConstraint,
)

from src.core.database import Base


class Report(Base):
    __tablename__ = "reports"

    report_id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.company_id"), nullable=False)
    report_type = Column(String(100), nullable=False)
    codal_tracking_id = Column(String(100), unique=True, nullable=True)
    title = Column(String(300), nullable=False)
    financial_period_id = Column(Integer, ForeignKey("financial_periods.period_id"), nullable=False)
    source_url = Column(String(500), nullable=True)
    original_report_id = Column(Integer, ForeignKey("reports.report_id"), nullable=True)
    is_correction = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class ReportVersion(Base):
    __tablename__ = "report_versions"

    report_version_id = Column(Integer, primary_key=True, autoincrement=True)
    report_id = Column(Integer, ForeignKey("reports.report_id"), nullable=False)
    version_number = Column(Integer, nullable=False, default=1)
    publication_datetime = Column(DateTime, nullable=False)
    is_current_version = Column(Boolean, nullable=False, default=True)
    is_restated = Column(Boolean, nullable=False, default=False)
    supersedes_version_id = Column(Integer, ForeignKey("report_versions.report_version_id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("report_id", "version_number", name="uq_report_version"),
        Index(
            "uq_report_current_version",
            "report_id",
            unique=True,
            sqlite_where=(is_current_version.is_(True)),
        ),
    )
