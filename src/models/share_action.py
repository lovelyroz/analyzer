from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey, UniqueConstraint
from src.core.database import Base

class ShareCountHistory(Base):
    __tablename__ = "share_count_history"

    share_history_id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.company_id"), nullable=False)
    effective_date = Column(Date, nullable=False)
    shares_outstanding = Column(Integer, nullable=False)
    capital = Column(Numeric(precision=24, scale=2), nullable=False)
    source = Column(String(100), nullable=True)

    __table_args__ = (
        UniqueConstraint("company_id", "effective_date", name="uq_company_share_date"),
    )

class CorporateAction(Base):
    __tablename__ = "corporate_actions"

    action_id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.company_id"), nullable=False)
    ex_date = Column(Date, nullable=False)
    action_type = Column(String(50), nullable=False)
    capital_before = Column(Numeric(precision=24, scale=2), nullable=False)
    capital_after = Column(Numeric(precision=24, scale=2), nullable=False)
    split_factor = Column(Numeric(precision=12, scale=6), default=1.0)