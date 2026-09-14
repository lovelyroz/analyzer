import pytest
from datetime import datetime
from src.kpi.schema import KPIResult
from src.scoring.functions import min_max_scale
from src.scoring.engine import FundamentalScoringEngine

def test_min_max_scale():
    # نگاشت معمولی (کاهش ریسک یا افزایش سود)
    assert min_max_scale(30.0, min_val=-20.0, max_val=80.0) == 50.0
    # Clamping (مقادیر فراتر از مرزها)
    assert min_max_scale(100.0, min_val=-20.0, max_val=80.0) == 100.0
    assert min_max_scale(-50.0, min_val=-20.0, max_val=80.0) == 0.0
    # Reverse Scaling (برای KPIهایی که مقدار کمتر بهتر است مثل NPL)
    assert min_max_scale(2.0, min_val=0.0, max_val=10.0, reverse=True) == 80.0

def test_fundamental_scoring_engine():
    engine = FundamentalScoringEngine()
    
    # داده‌های نمونه خروجی مرحله ۲ (KPI Results)
    kpis = [
        KPIResult(
            company_id=1, period_id=10, kpi_code="REVENUE_GROWTH", 
            value=30.0, unit="PERCENTAGE", quality_status="VALID", calculation_timestamp=datetime.utcnow()
        ),
        KPIResult(
            company_id=1, period_id=10, kpi_code="OP_MARGIN", 
            value=30.0, unit="PERCENTAGE", quality_status="VALID", calculation_timestamp=datetime.utcnow()
        ),
        KPIResult(
            company_id=1, period_id=10, kpi_code="ROE", 
            value=None, unit="PERCENTAGE", quality_status="MISSING", calculation_timestamp=datetime.utcnow()
        )
    ]
    
    result = engine.calculate_score(
        company_id=1, 
        period_id=10, 
        industry_code="GENERAL", 
        kpi_results=kpis
    )
    
    assert result.company_id == 1
    assert result.overall_score is not None
    # ۵۰.۰ (برای ۳۰.۰ در بازه -۲۰ تا ۸۰)
    assert result.overall_score == 50.0 
    assert len(result.kpi_scores) == 3