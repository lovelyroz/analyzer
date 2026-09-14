import pytest
from datetime import datetime
from src.forecast.drivers import ForecastDriver
from src.forecast.engine import ForecastEngine

def test_forecast_driver_general_chain():
    # Base Rev: 1000, Growth: 10%, OP Margin: 20%, Net Margin: 15%, Shares: 100
    chain = ForecastDriver.build_general_chain(
        base_revenue=1000.0,
        growth_rate=0.10,
        operating_margin=20.0,
        net_margin=15.0,
        share_count=100.0
    )
    assert chain.revenue == 1100.0
    assert chain.operating_profit == 220.0
    assert chain.net_profit == 165.0
    assert chain.eps == 1.65

def test_forecast_engine_scenarios():
    engine = ForecastEngine()
    context = {
        "base_revenue": 10000.0,
        "op_margin": 20.0,
        "net_margin": 10.0,
        "share_count": 1000.0,
        "base_growth_rate": 0.20
    }
    
    result = engine.generate_forecast(
        company_id=1,
        forecast_period_id=101,
        industry_code="PETROCHEMICAL",
        financial_context=context,
        trend_state="Strong Improvement"  # باعث رشد +5% اضافه می‌شود -> Base Growth = 25%
    )

    assert result.company_id == 1
    # Base EPS = (10000 * 1.25 * 0.10) / 1000 = 1.25
    assert result.scenario_forecasts.base.eps == 1.25
    # Bear EPS < Base EPS < Bull EPS
    assert result.scenario_forecasts.bear.eps < result.scenario_forecasts.base.eps
    assert result.scenario_forecasts.base.eps < result.scenario_forecasts.bull.eps