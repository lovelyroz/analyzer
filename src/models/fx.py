from sqlalchemy import Column, Integer, String, Date, Numeric, UniqueConstraint, CheckConstraint, ForeignKey
from src.core.database import Base


class FXRate(Base):
    __tablename__ = "fx_rates"

    fx_rate_id = Column(Integer, primary_key=True, autoincrement=True)
    rate_date = Column(Date, nullable=False)
    currency_from = Column(String(10), nullable=False, default="USD")
    currency_to = Column(String(10), nullable=False, default="IRR")
    rate = Column(Numeric(precision=18, scale=4), nullable=False)
    rate_type = Column(String(30), nullable=False)
    source = Column(String(100), nullable=True)

    __table_args__ = (
        UniqueConstraint("rate_date", "currency_from", "currency_to", "rate_type", name="uq_fx_rate"),
        CheckConstraint(
            "rate_type IN ('FREE_MARKET','OPERATIONAL','OFFICIAL','ESTIMATED','MANUAL_OPERATOR')",
            name="chk_fx_rate_type",
        ),
    )


class FXConversionRule(Base):
    __tablename__ = "fx_conversion_rules"

    rule_id = Column(Integer, primary_key=True, autoincrement=True)
    metric_type = Column(String(30), nullable=False)
    conversion_method = Column(String(50), nullable=False)
    rate_type = Column(String(30), nullable=False)
    description = Column(String(300), nullable=True)

    __table_args__ = (
        CheckConstraint(
            "metric_type IN ('FLOW','STOCK','MARKET_VALUE')",
            name="chk_fx_metric_type",
        ),
        CheckConstraint(
            "rate_type IN ('FREE_MARKET','OPERATIONAL','OFFICIAL','ESTIMATED','MANUAL_OPERATOR')",
            name="chk_fx_rule_rate_type",
        ),
    )
