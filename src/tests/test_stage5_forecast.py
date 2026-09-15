from datetime import datetime, timezone

import pytest

from src.forecast.drivers import ForecastDriver
from src.forecast.engine import ForecastEngine


def test_forecast_driver_general_chain():
    chain = ForecastDriver.build_general_chain(
        base_revenue=1000.0,
        growth_rate=0.10,
        operating_margin=20.0,
        net_margin=15.0,
        share_count=100.0,
    )
    assert chain.revenue == 1100.0
    assert chain.operating_profit == 220.0
    assert chain.net_profit == 165.0
    assert chain.eps == 1.65


def test_stage5_uses_seasonal_baseline_and_parameterized_trend():
    engine = ForecastEngine()
    context = {
        "seasonality_valid": True,
        "seasonal_baseline_revenue": 10000.0,
        "recent_run_rate_revenue": 9000.0,
        "baseline_revenue_growth": 0.20,
        "historical_operating_margin": 0.20,
        "historical_net_margin": 0.10,
        "share_count": 1000.0,
        "model_parameters": {
            "trend_adjustments": {"Strong Improvement": 0.05},
            "scenario_revenue_growth_spread": 0.05,
        },
    }

    result = engine.generate_forecast(
        company_id=1,
        forecast_period_id=101,
        industry_code="PETROCHEMICAL",
        financial_context=context,
        trend_state="Strong Improvement",
        horizon="12M",
        data_cutoff_datetime=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )

    assert result.baseline_method == "SEASONAL_BASELINE"
    assert result.horizon == "12M"
    assert result.scenario_forecasts.base.revenue == 12500.0
    assert result.scenario_forecasts.base.eps == 1.25
    assert result.scenario_forecasts.bear.eps < result.scenario_forecasts.base.eps
    assert result.scenario_forecasts.base.eps < result.scenario_forecasts.bull.eps


def test_low_base_disables_trend_adjustment():
    engine = ForecastEngine()
    context = {
        "seasonality_valid": True,
        "seasonal_baseline_revenue": 1000.0,
        "baseline_revenue_growth": 0.10,
        "historical_operating_margin": 0.20,
        "historical_net_margin": 0.10,
        "share_count": 100.0,
        "low_base": True,
        "model_parameters": {
            "trend_adjustments": {"Strong Improvement": 0.50},
            "scenario_revenue_growth_spread": 0.05,
        },
    }
    result = engine.generate_forecast(
        1, 101, "CEMENT", context, trend_state="Strong Improvement"
    )
    assert result.scenario_forecasts.base.revenue == 1100.0


def test_component_based_net_profit_has_priority_and_roe():
    chain = ForecastDriver.build_non_financial_chain(
        revenue=1000.0,
        operating_margin=0.20,
        share_count=100.0,
        non_operating_items=20.0,
        financial_costs=10.0,
        tax=30.0,
        net_margin=0.01,
        beginning_equity=400.0,
        ending_equity=600.0,
    )
    assert chain.method == "COMPONENT_BASED"
    assert chain.net_profit == 180.0
    assert chain.eps == 1.8
    assert chain.roe == 0.36


def test_missing_core_data_falls_back_to_insufficient_data():
    result = ForecastEngine().generate_forecast(
        1,
        101,
        "FOOD",
        {"share_count": 1000.0},
    )
    assert result.baseline_method == "INSUFFICIENT_DATA"
    assert result.data_quality == "INSUFFICIENT_DATA"
    assert result.scenario_forecasts.base.method == "INSUFFICIENT_DATA"


def test_bank_specialized_core_does_not_use_general_revenue_model():
    context = {
        "base_nii": 1000.0,
        "baseline_nii_growth": 0.10,
        "bank_net_profit_nii_conversion": 0.50,
        "share_count": 100.0,
        "model_parameters": {"scenario_financial_growth_spread": 0.05},
    }
    result = ForecastEngine().generate_forecast(1, 10, "BANK", context)
    assert result.baseline_method == "BANK_SPECIALIZED"
    assert result.scenario_forecasts.base.net_profit == 550.0
    assert result.scenario_forecasts.base.eps == 5.5


def test_holding_core_excludes_p_nav():
    context = {
        "base_nav": 2000.0,
        "baseline_nav_growth": 0.10,
        "holding_net_profit_nav_conversion": 0.20,
        "share_count": 100.0,
    }
    result = ForecastEngine().generate_forecast(1, 10, "HOLDING", context)
    assert result.baseline_method == "HOLDING_SPECIALIZED"
    assert result.scenario_forecasts.base.net_profit == 440.0
    assert result.scenario_forecasts.base.eps == 4.4
    assert "p_nav" not in result.scenario_forecasts.base.assumptions


def test_unsupported_horizon_and_industry_are_rejected():
    engine = ForecastEngine()
    with pytest.raises(ValueError):
        engine.generate_forecast(1, 1, "FOOD", {}, horizon="2Y")
    with pytest.raises(ValueError):
        engine.generate_forecast(1, 1, "INSURANCE", {})
