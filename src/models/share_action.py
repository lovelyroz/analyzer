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
    announcement_date = Column(Date, nullable=True)
    effective_date = Column(Date, nullable=False)
    action_type = Column(String(50), nullable=False)
    old_share_count = Column(Integer, nullable=True)
    new_share_count = Column(Integer, nullable=True)
    ratio = Column(Numeric(precision=18, scale=8), nullable=True)
    source = Column(String(100), nullable=True)

    __table_args__ = (
        UniqueConstraint("company_id", "effective_date", "action_type", name="uq_company_action_date_type"),
    )
