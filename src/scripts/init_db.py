# scripts/init_db.py
from src.core.database import engine, Base

# Import all models so SQLAlchemy registers every table before create_all().
from src.models.entity import Industry, Company
from src.models.period import FinancialPeriod
from src.models.report import Report, ReportVersion
from src.models.normalized import (
    DerivedFinancialFact,
    DerivedFinancialFactInput,
    FinancialMetric,
    MappingDecision,
    MappingRule,
    NormalizedFinancialFact,
    RawFinancialFact,
)
from src.models.normalized_provenance import NormalizedFinancialFactInput
from src.models.fx import FXRate, FXConversionRule
from src.models.market import MarketDaily
from src.models.share_action import ShareCountHistory, CorporateAction
from src.models.audit import IngestionRun


def init_db():
    print("در حال ساخت جداول پایگاه داده SQLite...")
    Base.metadata.create_all(bind=engine)
    print("جداول با موفقیت ساخته شدند.")


if __name__ == "__main__":
    init_db()
