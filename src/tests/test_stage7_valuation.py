from datetime import datetime

from src.forecast.schema import CompanyForecastResult, ScenarioForecastResult, SingleForecastChain
from src.valuation.engine import ValuationEngine
from src.valuation.models import calculate_forward_pe, calculate_forward_pe_fair_value, calculate_margin_of_safety


def make_forecast(eps_bear=150.0, eps_base=180.0, eps_bull=210.0):
    return CompanyForecastResult(
        company_id=1,
        forecast_period_id=101,
        data_cutoff_datetime=datetime(2026, 1, 1),
        industry_code="PETROCHEMICAL",
        scenario_forecasts=ScenarioForecastResult(
            bear=SingleForecastChain(1000.0, 200.0, eps_bear, eps_bear),
            base=SingleForecastChain(1200.0, 240.0, eps_base, eps_base),
            bull=SingleForecastChain(1400.0, 280.0, eps_bull, eps_bull),
        ),
        forecast_method="DRIVER_BASED",
        model_version="V1.0",
        calculation_timestamp=datetime(2026, 1, 1),
    )


def test_valuation_models():
    assert calculate_forward_pe(100.0, 700.0) == 7.0
    assert calculate_forward_pe_fair_value(100.0, 7.0) == 700.0
    assert calculate_margin_of_safety(1200.0, 1000.0) == 20.0
    assert calculate_forward_pe_fair_value(-100.0, 7.0) is None
    assert calculate_forward_pe(0.0, 1000.0) is None


def test_valuation_engine_forward_pe_and_expected_fair_value():
    engine = ValuationEngine()
    result = engine.calculate_valuation(
        company_id=1,
        period_id=101,
        industry_code="PETROCHEMICAL",
        current_price=1000.0,
        forecast_result=make_forecast(),
        forecast_reliability_score=85.0,
        historical_pe_values=[6.5, 7.0, 8.0],
        probability_confidence=90.0,
    )

    assert result.target_pe_source == "HISTORICAL_MEDIAN_PE"
    assert result.scenarios["base"].target_pe == 7.0
    assert result.scenarios["base"].forward_pe == round(1000.0 / 180.0, 4)
    assert result.scenarios["bear"].fair_value == 945.0
    assert result.scenarios["base"].fair_value == 1260.0
    assert result.scenarios["bull"].fair_value == 1617.0
    assert result.expected_fair_value == 1268.4
    assert result.margin_of_safety_pct == 26.84
    assert result.valuation_status == "ATTRACTIVE"
    assert abs(sum(s.probability for s in result.scenarios.values()) - 1.0) < 1e-9


def test_industry_forward_pe_requires_eight_valid_peers():
    engine = ValuationEngine()
    forecast = make_forecast()
    seven = [6.0] * 7
    result = engine.calculate_valuation(1, 101, "PETROCHEMICAL", 1000.0, forecast, historical_pe_values=[7.0], industry_forward_pe_values=seven)
    assert result.target_pe_source == "HISTORICAL_MEDIAN_PE"
    assert result.target_pe_source != "INDUSTRY_FORWARD_PE"

    eight = [6.0] * 8
    result = engine.calculate_valuation(1, 101, "PETROCHEMICAL", 1000.0, forecast, industry_forward_pe_values=eight)
    assert result.target_pe_source == "INDUSTRY_FORWARD_PE"
    assert result.scenarios["base"].target_pe == 6.0


def test_negative_eps_does_not_create_fake_pe_or_fair_value():
    engine = ValuationEngine()
    forecast = make_forecast(-50.0, -20.0, 10.0)
    result = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, forecast, historical_pe_values=[7.0]
    )
    assert result.scenarios["bear"].forward_pe is None
    assert result.scenarios["bear"].fair_value is None
    assert "NEGATIVE_EPS" in result.scenarios["bear"].flags
    assert result.expected_fair_value is None
    assert result.valuation_status in {"NOT_APPLICABLE", "INSUFFICIENT_DATA"}


def test_reliability_does_not_change_forward_pe_or_fair_value():
    engine = ValuationEngine()
    low = engine.calculate_valuation(1, 101, "PETROCHEMICAL", 1000.0, make_forecast(), 20.0, historical_pe_values=[7.0])
    high = engine.calculate_valuation(1, 101, "PETROCHEMICAL", 1000.0, make_forecast(), 90.0, historical_pe_values=[7.0])
    assert low.scenarios["base"].forward_pe == high.scenarios["base"].forward_pe
    assert low.scenarios["base"].fair_value == high.scenarios["base"].fair_value
    assert low.expected_fair_value == high.expected_fair_value
    assert low.valuation_confidence < high.valuation_confidence
