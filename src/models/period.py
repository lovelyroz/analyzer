from sqlalchemy import Column, Integer, String, Boolean, Date, CheckConstraint, UniqueConstraint, ForeignKey
from src.core.database import Base


PERIOD_TYPES = {
    "MONTH",
    "QUARTER",
    "SEMI_ANNUAL",
    "NINE_MONTH",
    "ANNUAL",
    "TTM",
}


class FinancialPeriod(Base):
    __tablename__ = "financial_periods"

    period_id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.company_id"), nullable=False)
    period_type = Column(String(20), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    fiscal_year = Column(Integer, nullable=False)
    fiscal_quarter = Column(Integer, nullable=True)
    months_length = Column(Integer, nullable=False)
    is_ytd = Column(Boolean, nullable=False, default=False)

    __table_args__ = (
        CheckConstraint("end_date >= start_date", name="chk_period_dates"),
        CheckConstraint(
            "period_type IN ('MONTH','QUARTER','SEMI_ANNUAL','NINE_MONTH','ANNUAL','TTM')",
            name="chk_period_type",
        ),
        UniqueConstraint("company_id", "fiscal_year", "period_type", "end_date", name="uq_company_period"),
    )
