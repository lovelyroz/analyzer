from sqlalchemy import Column, Integer, String, Date, Numeric, UniqueConstraint
from src.core.database import Base

class FXRate(Base):
    __tablename__ = "fx_rates"

    fx_rate_id = Column(Integer, primary_key=True, autoincrement=True)
    rate_date = Column(Date, nullable=False)
    currency_pair = Column(String(10), nullable=False, default="USD/IRR")
    fx_type = Column(String(30), nullable=False)  # 'FREE_MARKET' یا 'OPERATIONAL_EXCHANGE'
    rate_value = Column(Numeric(precision=18, scale=4), nullable=False)
    source = Column(String(100), nullable=True)

    __table_args__ = (
        UniqueConstraint("rate_date", "currency_pair", "fx_type", name="uq_fx_rate"),
    )