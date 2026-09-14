# scripts/init_db.py
from src.core.database import engine, Base
# لود کردن مدل‌ها تا SQLAlchemy آن‌ها را بشناسد
from src.models.entity import Industry, Company
from src.models.period import FinancialPeriod
from src.models.report import Report, ReportVersion
from src.models.normalized import RawFinancialFact, FinancialMetric, NormalizedFinancialFact
from src.models.fx import FXRate
from src.models.market import MarketDaily
from src.models.share_action import ShareCountHistory, CorporateAction
from src.models.audit import IngestionRun

def init_db():
    print("در حال ساخت جداول پایگاه داده SQLite...")
    Base.metadata.create_all(bind=engine)
    print("جداول با موفقیت ساخته شدند.")

if __name__ == "__main__":
    init_db()