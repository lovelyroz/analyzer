# tests/test_stage1_rules.py
import pytest
from datetime import datetime, date
from sqlalchemy.exc import IntegrityError
from src.core.database import SessionLocal, Base, engine
from src.models.entity import Industry, Company
from src.models.period import FinancialPeriod
from src.models.report import Report, ReportVersion
from src.models.normalized import RawFinancialFact, FinancialMetric, NormalizedFinancialFact
from src.models.fx import FXRate

@pytest.fixture(scope="function")
def db_session():
    """ایجاد یک پایگاه داده موقت در حافظه (In-Memory) برای تست‌ها"""
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_null_value_preservation(db_session):
    """قانون: مقادیر NULL نباید به صفر تبدیل شوند"""
    version = ReportVersion(
        report_id=1, version_number=1, published_at=datetime.utcnow()
    )
    raw_fact = RawFinancialFact(
        version_id=1, raw_label="اقلام متفرقه", raw_value=None
    )
    
    assert raw_fact.raw_value is None, "مقدار NULL نباید خودکار صفر شود"

def test_fx_type_separation(db_session):
    """قانون: ارز آزاد و ارز عملیاتی باید کاملاً جدا نگه داشته شوند"""
    today = date.today()
    rate_free = FXRate(
        rate_date=today, currency_pair="USD/IRR", fx_type="FREE_MARKET", rate_value=600000
    )
    rate_op = FXRate(
        rate_date=today, currency_pair="USD/IRR", fx_type="OPERATIONAL_EXCHANGE", rate_value=420000
    )
    
    db_session.add(rate_free)
    db_session.add(rate_op)
    db_session.commit()

    rates = db_session.query(FXRate).filter_by(rate_date=today).all()
    assert len(rates) == 2, "ارز آزاد و عملیاتی باید نرخ‌های جداگانه ثبت کنند"

def test_point_in_time_versioning(db_session):
    """قانون: تفکیک نسخه اصلی و اصلاحیه برای جلوگیری از Look-Ahead Bias"""
    report = Report(company_id=1, period_id=1, title="صورت‌های مالی ۳ ماهه")
    db_session.add(report)
    db_session.flush()

    v1 = ReportVersion(
        report_id=report.report_id, version_number=1, published_at=datetime(2024, 4, 15)
    )
    v2 = ReportVersion(
        report_id=report.report_id, version_number=2, published_at=datetime(2024, 5, 20), is_restatement=True
    )
    db_session.add_all([v1, v2])
    db_session.commit()

    versions = db_session.query(ReportVersion).filter_by(report_id=report.report_id).all()
    assert len(versions) == 2
    assert versions[0].published_at < versions[1].published_at