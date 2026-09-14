# scripts/seed_data.py
from src.core.database import SessionLocal
from src.models.entity import Industry
from src.models.normalized import FinancialMetric

# صنایع ۷‌گانه قفل‌شده V1
LOCKED_V1_INDUSTRIES = [
    {"industry_code": "BANK", "industry_name": "بانک‌ها و موسسات اعتباری"},
    {"industry_code": "INVESTMENT", "industry_name": "سرمایه‌گذاری و هلدینگ"},
    {"industry_code": "PETROCHEMICAL", "industry_name": "محصولات شیمیایی و پتروشیمی"},
    {"industry_code": "METALS", "industry_name": "فلزات اساسی و استخراج کانی‌های فلزی"},
    {"industry_code": "CEMENT", "industry_name": "سیمان، آهک و گچ"},
    {"industry_code": "FOOD", "industry_name": "محصولات غذایی و آشامیدنی"},
    {"industry_code": "PHARMA", "industry_name": "مواد و محصولات دارویی"},
]

# متریک‌های پایه مالی (پایه ریالی IRR)
BASE_FINANCIAL_METRICS = [
    # صورت سود و زیان (FLOW)
    {"metric_code": "REVENUE", "metric_name": "درآمد عملیاتی / فروش", "category": "INCOME_STATEMENT", "flow_or_stock": "FLOW"},
    {"metric_code": "OPERATING_PROFIT", "metric_name": "سود (زیان) عملیاتی", "category": "INCOME_STATEMENT", "flow_or_stock": "FLOW"},
    {"metric_code": "NET_PROFIT", "metric_name": "سود (زیان) خالص", "category": "INCOME_STATEMENT", "flow_or_stock": "FLOW"},
    {"metric_code": "EPS", "metric_name": "سود (زیان) هر سهم", "category": "INCOME_STATEMENT", "flow_or_stock": "FLOW"},
    
    # ترازنامه (STOCK)
    {"metric_code": "TOTAL_ASSETS", "metric_name": "جمع دارایی‌ها", "category": "BALANCE_SHEET", "flow_or_stock": "STOCK"},
    {"metric_code": "TOTAL_LIABILITIES", "metric_name": "جمع بدهی‌ها", "category": "BALANCE_SHEET", "flow_or_stock": "STOCK"},
    {"metric_code": "TOTAL_EQUITY", "metric_name": "جمع حقوق مالکانه", "category": "BALANCE_SHEET", "flow_or_stock": "STOCK"},
    
    # صورت جریان وجوه نقد (FLOW)
    {"metric_code": "OPERATING_CASH_FLOW", "metric_name": "جریان نقد حاصل از عملیات", "category": "CASH_FLOW", "flow_or_stock": "FLOW"},
]

def seed_initial_data():
    db = SessionLocal()
    try:
        print("در حال ثبت صنایع اولیه...")
        for ind in LOCKED_V1_INDUSTRIES:
            exists = db.query(Industry).filter_by(industry_code=ind["industry_code"]).first()
            if not exists:
                db.add(Industry(**ind))
        
        print("در حال ثبت متریک‌های پایه مالی...")
        for met in BASE_FINANCIAL_METRICS:
            exists = db.query(FinancialMetric).filter_by(metric_code=met["metric_code"]).first()
            if not exists:
                db.add(FinancialMetric(**met))
                
        db.commit()
        print("داده‌های اولیه با موفقیت در پایگاه داده ثبت شدند.")
    except Exception as e:
        db.rollback()
        print(f"خطا در ثبت داده‌های اولیه: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_initial_data()