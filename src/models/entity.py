from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from datetime import datetime, timezone
from src.core.database import Base


def _utc_now_naive() -> datetime:
    """Return naive UTC for the existing DateTime storage convention."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Industry(Base):
    __tablename__ = "industries"

    industry_id = Column(Integer, primary_key=True, autoincrement=True)
    industry_code = Column(String(50), nullable=False, unique=True)
    industry_name = Column(String(150), nullable=False)
    parent_industry_id = Column(Integer, ForeignKey("industries.industry_id", ondelete="SET NULL"), nullable=True)


class Company(Base):
    __tablename__ = "companies"

    company_id = Column(Integer, primary_key=True, autoincrement=True)
    national_id = Column(String(20), unique=True, nullable=True)
    ticker = Column(String(50), nullable=False)
    company_name = Column(String(200), nullable=False)
    industry_id = Column(Integer, ForeignKey("industries.industry_id"), nullable=False)
    codal_symbol = Column(String(50), nullable=True)
    fiscal_year_end = Column(String(10), nullable=True)
    status = Column(String(30), nullable=False, default="ACTIVE")
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=_utc_now_naive)
