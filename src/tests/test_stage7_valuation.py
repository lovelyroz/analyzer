import pytest
from datetime import datetime
from src.forecast.schema import CompanyForecastResult, ScenarioForecastResult, SingleForecastChain
from src.valuation.models import calculate_forward_pe_fair_value, calculate_margin_of_safety
from src.valuation.engine import ValuationEngine

def test_valuation_models():
    # EPS = 100, Target P/E = 7.0 -> Fair Value = 700
    assert calculate_forward_pe_fair_value(100.0, 7.0) == 700.0
    # Fair Value = 1200, Price = 1000 -> MOS = 20%
    assert calculate_margin_of_safety(1200.0, 1000.0) == 20.0

def test_valuation_engine_full():
    engine = ValuationEngine()
    
    forecast = CompanyForecastResult(
        company_id=1,
        forecast_period_id=101,
        data_cutoff_datetime=datetime.utcnow(),
        industry_code="PETROCHEMICAL",
        scenario_forecasts=ScenarioForecastResult(
            bear=SingleForecastChain(1000.0, 200.0, 150.0, 150.0),
            base=SingleForecastChain(1200.0, 240.0, 180.0, 180.0),
            bull=SingleForecastChain(1400.0, 280.0, 210.0, 210.0)
        ),
        forecast_method="DRIVER_BASED",
        model_version="V1.0",
        calculation_timestamp=datetime.utcnow()
    )

    # Price = 1000, Target P/E for PETROCHEMICAL = 6.5
    # Expected EPS = (150*0.2) + (180*0.6) + (210*0.2) = 180
    # Expected Fair Value = 180 * 6.5 = 1170.0
    # MOS = ((1170 - 1000) / 1000) * 100 = 17.0% -> FAIRLY_VALUED
    result = engine.calculate_valuation(
        company_id=1,
        period_id=101,
        industry_code="PETROCHEMICAL",
        current_price=1000.0,
        forecast_result=forecast,
        forecast_reliability_score=85.0
    )

    assert result.company_id == 1
    assert result.expected_fair_value == 1170.0
    assert result.margin_of_safety_pct == 17.0
    assert result.valuation_status == "FAIRLY_VALUED"
    assert result.valuation_confidence == 76.5