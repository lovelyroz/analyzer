from sqlalchemy import Column, Integer, String, Boolean, Date, CheckConstraint, UniqueConstraint
from src.core.database import Base

class FinancialPeriod(Base):
    __tablename__ = "financial_periods"

    period_id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, nullable=False)
    period_type = Column(String(20), nullable=False)  # مثلا ANNUAL یا INTERIM_Q1
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    fiscal_year = Column(Integer, nullable=False)
    fiscal_quarter = Column(Integer, nullable=True)
    months_length = Column(Integer, nullable=False)
    is_ytd = Column(Boolean, nullable=False, default=False)

    __table_args__ = (
        CheckConstraint("end_date >= start_date", name="chk_period_dates"),
        UniqueConstraint("company_id", "fiscal_year", "period_type", "end_date", name="uq_company_period"),
    )