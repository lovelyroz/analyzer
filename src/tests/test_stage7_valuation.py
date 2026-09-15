from datetime import datetime

import pytest

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
    result = ValuationEngine().calculate_valuation(
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
    assert result.scenarios["bear"].target_pe == 7.0
    assert result.scenarios["bull"].target_pe == 7.0
    assert result.scenarios["base"].forward_pe == round(1000.0 / 180.0, 4)
    assert result.scenarios["bear"].fair_value == 1050.0
    assert result.scenarios["base"].fair_value == 1260.0
    assert result.scenarios["bull"].fair_value == 1470.0
    assert result.expected_fair_value == 1260.0
    assert result.margin_of_safety_pct == 26.0
    assert result.valuation_status == "ATTRACTIVE"
    assert abs(sum(s.probability for s in result.scenarios.values()) - 1.0) < 1e-9
    assert result.contract_version == "VALUATION_CONTRACT_V1"
    assert result.valuation_driver_ranking[:2] == ["EPS", "TARGET_PE"]
    assert set(result.driver_impact) == {"EPS", "TARGET_PE"}
    assert all(value >= 0 for value in result.review_priority.values())
    assert result.metadata["scenario_multiple_policy"]["mode"] == "NEUTRAL_BENCHMARK_MULTIPLE"


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


def test_industry_ttm_is_fallback_after_historical_median():
    result = ValuationEngine().calculate_valuation(
        1,
        101,
        "PETROCHEMICAL",
        1000.0,
        make_forecast(),
        industry_forward_pe_values=[6.0] * 7,
        industry_ttm_pe_values=[5.0, 6.0, 7.0],
    )
    assert result.target_pe_source == "INDUSTRY_TTM_PE"
    assert result.scenarios["base"].target_pe == 6.0


def test_negative_eps_does_not_create_fake_pe_or_fair_value():
    result = ValuationEngine().calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(-50.0, -20.0, 10.0), historical_pe_values=[7.0]
    )
    assert result.scenarios["bear"].forward_pe is None
    assert result.scenarios["bear"].fair_value is None
    assert "NEGATIVE_EPS" in result.scenarios["bear"].flags
    assert result.expected_fair_value is None
    assert result.valuation_status in {"NOT_APPLICABLE", "INSUFFICIENT_DATA"}
    assert "SIGN_CHANGE" in result.scenarios["bull"].flags


def test_reliability_does_not_change_forward_pe_or_fair_value():
    engine = ValuationEngine()
    low = engine.calculate_valuation(1, 101, "PETROCHEMICAL", 1000.0, make_forecast(), 20.0, historical_pe_values=[7.0])
    high = engine.calculate_valuation(1, 101, "PETROCHEMICAL", 1000.0, make_forecast(), 90.0, historical_pe_values=[7.0])
    assert low.scenarios["base"].forward_pe == high.scenarios["base"].forward_pe
    assert low.scenarios["base"].fair_value == high.scenarios["base"].fair_value
    assert low.expected_fair_value == high.expected_fair_value
    assert low.valuation_confidence < high.valuation_confidence


def test_probability_adjustments_are_normalized_and_separate_from_reliability():
    result = ValuationEngine().calculate_valuation(
        1,
        101,
        "PETROCHEMICAL",
        1000.0,
        make_forecast(),
        forecast_reliability_score=25.0,
        historical_pe_values=[7.0],
        probability_adjustments={"bear": 0.10, "bull": -0.05},
        probability_confidence=80.0,
    )
    assert abs(sum(s.probability for s in result.scenarios.values()) - 1.0) < 1e-9
    assert result.scenarios["bear"].probability > 0.20
    assert result.scenarios["bull"].probability < 0.20
    assert result.forecast_reliability_score == 25.0
    assert result.metadata["scenario_dependency"]["separate_from_probability"] is True


def test_probability_evidence_is_family_level_and_equal_weighted():
    evidence = {
        "FUNDAMENTAL_DIRECTION": {"bear": 0.1, "base": 0.3, "bull": 0.6},
        "FORECAST_DIRECTION": {"bear": 0.2, "base": 0.5, "bull": 0.3},
        "PROFITABILITY_ASSUMPTION_RISK": {"bear": 0.4, "base": 0.4, "bull": 0.2},
        "DATA_STRUCTURAL_RISK": {"bear": 0.5, "base": 0.3, "bull": 0.2},
    }
    result = ValuationEngine().calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(), historical_pe_values=[7.0], probability_evidence=evidence
    )
    assert abs(sum(s.probability for s in result.scenarios.values()) - 1.0) < 1e-9
    meta = result.metadata["probability_evidence"]
    assert meta["mode"] == "FAMILY_LEVEL_EQUAL_WEIGHT"
    assert meta["family_count"] == 4
    assert meta["correlated_metric_protection"] == "ONE_DISTRIBUTION_PER_FAMILY"
    assert set(meta["families_used"]) == {
        "FUNDAMENTAL_DIRECTION",
        "FORECAST_DIRECTION",
        "PROFITABILITY_ASSUMPTION_RISK",
        "DATA_STRUCTURAL_RISK",
    }


def test_probability_evidence_rejects_unknown_or_incomplete_family_data():
    with pytest.raises(ValueError, match="Unknown probability evidence families"):
        ValuationEngine().calculate_valuation(
            1,
            101,
            "PETROCHEMICAL",
            1000.0,
            make_forecast(),
            historical_pe_values=[7.0],
            probability_evidence={"OTHER": {"bear": 0.2, "base": 0.6, "bull": 0.2}},
        )

    with pytest.raises(ValueError, match="must provide bear/base/bull scores"):
        ValuationEngine().calculate_valuation(
            1,
            101,
            "PETROCHEMICAL",
            1000.0,
            make_forecast(),
            historical_pe_values=[7.0],
            probability_evidence={"FUNDAMENTAL_DIRECTION": {"bear": 0.2, "base": 0.8}},
        )


def test_scenario_multiple_adjustments_require_economic_rationale_and_are_bounded():
    result = ValuationEngine().calculate_valuation(
        1,
        101,
        "PETROCHEMICAL",
        1000.0,
        make_forecast(),
        historical_pe_values=[7.0],
        scenario_pe_adjustments={"bear": -0.10, "base": 0.0, "bull": 0.10},
        scenario_pe_rationales={
            "bear": "Higher earnings and discount-rate risk reduces justified multiple.",
            "base": "Historical median is the neutral benchmark.",
            "bull": "Improved sustainable earnings quality supports a modest multiple premium.",
        },
    )
    assert result.scenarios["bear"].target_pe == 6.3
    assert result.scenarios["base"].target_pe == 7.0
    assert result.scenarios["bull"].target_pe == 7.7
    assert result.scenarios["bear"].fair_value == 945.0
    assert result.scenarios["bull"].fair_value == 1617.0
    assert result.metadata["scenario_multiple_policy"]["mode"] == "EXPLICIT_ECONOMIC_SCENARIO_ADJUSTMENT"

    with pytest.raises(ValueError, match="Economic rationale required"):
        ValuationEngine().calculate_valuation(
            1,
            101,
            "PETROCHEMICAL",
            1000.0,
            make_forecast(),
            historical_pe_values=[7.0],
            scenario_pe_adjustments={"bear": -0.10},
        )

    with pytest.raises(ValueError, match="exceeds V1 bound"):
        ValuationEngine().calculate_valuation(
            1,
            101,
            "PETROCHEMICAL",
            1000.0,
            make_forecast(),
            historical_pe_values=[7.0],
            scenario_pe_adjustments={"bull": 0.25},
            scenario_pe_rationales={"bull": "Unsupported large adjustment."},
        )


def test_alerts_include_severity_and_driver_focus():
    result = ValuationEngine().calculate_valuation(
        1,
        101,
        "PETROCHEMICAL",
        1000.0,
        make_forecast(80.0, 180.0, 320.0),
        forecast_reliability_score=30.0,
        historical_pe_values=[7.0],
        probability_confidence=50.0,
    )
    assert any(alert.startswith("WARNING:LOW_FORECAST_RELIABILITY") for alert in result.alerts)
    assert any(alert.startswith("INFO:TOP_DRIVER:") for alert in result.alerts)
    assert "HIGH_SCENARIO_DISPERSION" in result.valuation_risk_flags
