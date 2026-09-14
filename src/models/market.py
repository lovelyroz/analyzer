from sqlalchemy import Column, Integer, Date, Numeric, ForeignKey, UniqueConstraint, String
from src.core.database import Base


class MarketDaily(Base):
    __tablename__ = "market_daily"

    market_data_id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.company_id"), nullable=False)
    trade_date = Column(Date, nullable=False)
    open_price = Column(Numeric(precision=18, scale=2), nullable=True)
    high_price = Column(Numeric(precision=18, scale=2), nullable=True)
    low_price = Column(Numeric(precision=18, scale=2), nullable=True)
    close_price = Column(Numeric(precision=18, scale=2), nullable=True)
    adjusted_close = Column(Numeric(precision=18, scale=2), nullable=True)
    volume = Column(Integer, nullable=True)
    value = Column(Numeric(precision=24, scale=2), nullable=True)
    trade_count = Column(Integer, nullable=True)
    source = Column(String(100), nullable=True)

    __table_args__ = (
        UniqueConstraint("company_id", "trade_date", name="uq_company_trade_date"),
    )
