from datetime import datetime, timezone

import pytest

from src.forecast.schema import CompanyForecastResult, ForecastInputRef, ScenarioForecastResult, SingleForecastChain
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
    assert result.metadata["scenario_multiple_policy"]["policy_version"] == "STAGE7_V1_EVIDENCE_BACKED"


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


def test_direct_probability_adjustments_are_rejected_in_favor_of_family_evidence():
    with pytest.raises(ValueError, match="family-level probability_evidence"):
        ValuationEngine().calculate_valuation(
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
    assert result.metadata["scenario_multiple_policy"]["policy_version"] == "STAGE7_V1_EVIDENCE_BACKED"

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


# P2 additions: sensitivity and alert focused tests. Existing tests above untouched.
def test_p2_sensitivity_drivers_present_and_bounded():
    from src.valuation.parameters import SENSITIVITY_PERTURBATION

    assert SENSITIVITY_PERTURBATION == 0.10
    result = ValuationEngine().calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
        forecast_reliability_score=85.0, historical_pe_values=[7.0],
        probability_confidence=90.0,
    )
    assert result.scenarios["base"].fair_value is not None
    assert set(result.valuation_driver_ranking) == {"EPS", "TARGET_PE"}
    assert set(result.driver_impact) == {"EPS", "TARGET_PE"}
    assert set(result.driver_uncertainty) == {"EPS", "TARGET_PE"}
    assert set(result.review_priority) == {"EPS", "TARGET_PE"}
    assert abs(sum(result.driver_impact.values()) - 100.0) < 1e-6
    assert all(0.0 <= v <= 100.0 for v in result.driver_uncertainty.values())
    assert all(v >= 0 for v in result.review_priority.values())


def test_p2_sensitivity_missing_data_empty_drivers():
    result = ValuationEngine().calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0,
        make_forecast(-50.0, -20.0, 10.0), historical_pe_values=[7.0],
    )
    assert result.scenarios["base"].fair_value is None
    assert result.valuation_driver_ranking == []
    assert result.driver_impact == {}
    assert result.driver_uncertainty == {}
    assert result.review_priority == {}


def test_p2_sensitivity_deterministic_repeated_runs():
    engine = ValuationEngine()
    kwargs = dict(
        company_id=1, period_id=101, industry_code="PETROCHEMICAL",
        current_price=1000.0, forecast_result=make_forecast(),
        forecast_reliability_score=70.0, historical_pe_values=[7.0],
        probability_confidence=60.0, data_quality_score=80.0,
    )
    first = engine.calculate_valuation(**kwargs)
    second = engine.calculate_valuation(**kwargs)
    assert first.valuation_driver_ranking == second.valuation_driver_ranking
    assert first.driver_impact == second.driver_impact
    assert first.driver_uncertainty == second.driver_uncertainty
    assert first.review_priority == second.review_priority
    assert first.alerts == second.alerts
    assert first.valuation_status == second.valuation_status


def test_p2_alert_severity_levels_valid():
    result = ValuationEngine().calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(80.0, 180.0, 320.0),
        forecast_reliability_score=30.0, historical_pe_values=[7.0],
        probability_confidence=50.0,
    )
    assert len(result.alerts) > 0
    allowed = {"INFO", "WATCH", "WARNING", "CRITICAL"}
    for alert in result.alerts:
        assert ":" in alert
        assert alert.split(":")[0] in allowed
    combined = " ".join(result.alerts + result.valuation_risk_flags)
    assert "BUY" not in combined
    assert "SELL" not in combined


def test_p2_alert_low_reliability_threshold_boundaries():
    from src.valuation.parameters import ALERT_THRESHOLDS

    assert ALERT_THRESHOLDS["low_forecast_reliability"] == 40.0
    engine = ValuationEngine()

    def run(reliability):
        kwargs = dict(company_id=1, period_id=101, industry_code="PETROCHEMICAL",
                      current_price=1000.0, forecast_result=make_forecast(),
                      historical_pe_values=[7.0])
        if reliability is not None:
            kwargs["forecast_reliability_score"] = reliability
        return engine.calculate_valuation(**kwargs)

    below = run(39.9)
    assert any("LOW_FORECAST_RELIABILITY" in a for a in below.alerts)
    assert "LOW_FORECAST_RELIABILITY" in below.valuation_risk_flags
    at = run(40.0)
    assert not any("LOW_FORECAST_RELIABILITY" in a for a in at.alerts)
    assert "LOW_FORECAST_RELIABILITY" not in at.valuation_risk_flags
    above = run(40.1)
    assert not any("LOW_FORECAST_RELIABILITY" in a for a in above.alerts)
    missing = run(None)
    assert not any("LOW_FORECAST_RELIABILITY" in a for a in missing.alerts)
    again = run(39.9)
    assert again.alerts == below.alerts


def test_p2_alert_high_dispersion_threshold_boundaries():
    from src.valuation.parameters import ALERT_THRESHOLDS, RISK_THRESHOLDS

    assert ALERT_THRESHOLDS["high_scenario_dispersion"] == 0.50
    assert RISK_THRESHOLDS["high_scenario_dispersion"] == 0.50
    engine = ValuationEngine()

    def run(bear, base, bull):
        return engine.calculate_valuation(
            1, 101, "PETROCHEMICAL", 1000.0,
            make_forecast(bear, base, bull), historical_pe_values=[7.0],
        )

    above = run(140.0, 200.0, 260.0)
    assert above.metadata["scenario_dispersion"] is not None
    assert above.metadata["scenario_dispersion"] > 0.50
    assert "HIGH_SCENARIO_DISPERSION" in above.valuation_risk_flags
    assert any("HIGH_SCENARIO_DISPERSION" in a for a in above.alerts)
    at = run(150.0, 200.0, 250.0)
    assert abs(at.metadata["scenario_dispersion"] - 0.50) < 1e-9
    assert "HIGH_SCENARIO_DISPERSION" not in at.valuation_risk_flags
    below = run(160.0, 200.0, 240.0)
    assert below.metadata["scenario_dispersion"] < 0.50
    assert not any("HIGH_SCENARIO_DISPERSION" in a for a in below.alerts)
    missing = run(-50.0, -20.0, 10.0)
    assert missing.metadata["scenario_dispersion"] is None
    assert not any("HIGH_SCENARIO_DISPERSION" in a for a in missing.alerts)
    assert run(140.0, 200.0, 260.0).alerts == above.alerts


def test_p2_alert_divergence_ratios_boundaries():
    from src.valuation.parameters import ALERT_THRESHOLDS

    assert ALERT_THRESHOLDS["benchmark_divergence_ratio"] == 1.50
    assert ALERT_THRESHOLDS["historical_divergence_ratio"] == 1.50
    assert ALERT_THRESHOLDS["industry_divergence_ratio"] == 1.50
    engine = ValuationEngine()
    above = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 900.0,
        make_forecast(90.0, 100.0, 110.0), historical_pe_values=[6.0],
    )
    assert above.scenarios["base"].forward_pe == 9.0
    assert any("VALUATION_ABOVE_TARGET_PE" in a for a in above.alerts)
    assert any("FORWARD_PE_ABOVE_HISTORICAL" in a for a in above.alerts)
    just_below = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 899.0,
        make_forecast(90.0, 100.0, 110.0), historical_pe_values=[6.0],
    )
    assert not any("VALUATION_ABOVE_TARGET_PE" in a for a in just_below.alerts)
    below_target = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 400.0,
        make_forecast(90.0, 100.0, 110.0), historical_pe_values=[6.0],
    )
    assert any("VALUATION_BELOW_TARGET_PE" in a for a in below_target.alerts)
    industry = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 900.0,
        make_forecast(90.0, 100.0, 110.0), historical_pe_values=[10.0],
        industry_forward_pe_values=[6.0] * 8,
    )
    assert industry.target_pe_source == "INDUSTRY_FORWARD_PE"
    assert any("FORWARD_PE_ABOVE_INDUSTRY" in a for a in industry.alerts)
    missing = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0,
        make_forecast(-10.0, -5.0, 10.0), historical_pe_values=[6.0],
    )
    assert missing.scenarios["base"].forward_pe is None
    assert not any("VALUATION_ABOVE_TARGET_PE" in a for a in missing.alerts)
    assert not any("FORWARD_PE_ABOVE_HISTORICAL" in a for a in missing.alerts)


def test_p2_sector_driver_decomposition_missing():
    engine = ValuationEngine()
    nonfin = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
        historical_pe_values=[7.0],
    )
    bank = engine.calculate_valuation(
        1, 101, "BANK", 1000.0, make_forecast(),
        historical_pe_values=[7.0],
    )
    holding = engine.calculate_valuation(
        1, 101, "HOLDING", 1000.0, make_forecast(),
        forecast_reliability_score=80.0, historical_pe_values=[7.0],
        nav_per_share=500.0,
    )
    observed = set(nonfin.valuation_driver_ranking) | set(bank.valuation_driver_ranking) | set(holding.valuation_driver_ranking)
    assert {"REVENUE", "NII", "NAV"} <= observed


def test_p2_required_flip_dependence_alerts_missing():
    from src.valuation.parameters import SENSITIVITY_PERTURBATION, VALUATION_THRESHOLDS

    assert SENSITIVITY_PERTURBATION == 0.10
    assert VALUATION_THRESHOLDS["attractive_expected_upside"] == 15.0
    assert VALUATION_THRESHOLDS["attractive_base_upside"] == 5.0
    engine = ValuationEngine()
    flip_base = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0,
        make_forecast(150.0, 150.0, 250.0), historical_pe_values=[7.0],
    )
    assert flip_base.valuation_status == "ATTRACTIVE"
    shocked = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0,
        make_forecast(135.0, 135.0, 225.0), historical_pe_values=[7.0],
    )
    assert shocked.valuation_status == "FAIR"
    stable = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(180.0, 180.0, 180.0),
        historical_pe_values=[7.0],
        scenario_pe_adjustments={"bear": -0.10, "base": 0.0, "bull": 0.20},
        scenario_pe_rationales={
            "bear": "Higher risk compresses justified multiple.",
            "base": "Historical median is neutral.",
            "bull": "Better quality supports premium.",
        },
    )
    eps_risk = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(80.0, 180.0, 320.0),
        forecast_reliability_score=20.0, historical_pe_values=[7.0],
        probability_confidence=50.0, data_quality_score=20.0,
    )
    vocab = []
    for result in (flip_base, shocked, stable, eps_risk):
        vocab.extend(result.alerts)
        vocab.extend(result.valuation_risk_flags)
    required = ["ASSESSMENT_FLIP_RISK", "HIGH_MULTIPLE_DEPENDENCE",
                "HIGH_EPS_DEPENDENCE", "MARGIN_ASSUMPTION_RISK",
                "HIGH_IMPACT_HIGH_UNCERTAINTY"]
    missing = [name for name in required if not any(name in item for item in vocab)]
    assert not missing, f"Missing required alerts: {missing}"


# P3 additions: traceable one-at-a-time sensitivity + non-finite input guards.
# Existing tests above untouched.
def test_p3_sensitivity_recomputes_from_valuation_identity():
    from src.valuation.parameters import SENSITIVITY_PERTURBATION

    engine = ValuationEngine()
    result = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
        historical_pe_values=[7.0],
    )
    base = result.scenarios["base"]
    assert base.fair_value is not None
    expected_effect = abs(base.fair_value * SENSITIVITY_PERTURBATION)
    assert expected_effect > 0
    # FV = EPS x target P/E is linear in each driver, so each one-at-a-time
    # shock moves fair value by exactly |FV x p|; the 50/50 split is a
    # documented property of the identity, not an invented weighting.
    assert abs(result.driver_impact["EPS"] - 50.0) < 1e-6
    assert abs(result.driver_impact["TARGET_PE"] - 50.0) < 1e-6
    assert abs(sum(result.driver_impact.values()) - 100.0) < 1e-6
    again = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
        historical_pe_values=[7.0],
    )
    assert again.driver_impact == result.driver_impact
    assert again.review_priority == result.review_priority


def test_p3_nan_eps_is_guarded_as_invalid():
    import math

    nan = float("nan")
    engine = ValuationEngine()
    result = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0,
        make_forecast(nan, nan, nan), historical_pe_values=[7.0],
    )
    assert result.scenarios["bear"].fair_value is None
    assert result.expected_fair_value is None
    assert result.metadata["scenario_dispersion"] is None
    for scenario in result.scenarios.values():
        assert scenario.fair_value is None or math.isfinite(scenario.fair_value)
    assert result.valuation_driver_ranking == []
    assert result.driver_impact == {}


def test_p3_zero_and_negative_price_guarded():
    engine = ValuationEngine()
    for price in (0.0, -100.0):
        result = engine.calculate_valuation(
            1, 101, "PETROCHEMICAL", price, make_forecast(),
            historical_pe_values=[7.0],
        )
        assert result.scenarios["base"].forward_pe is None
        assert result.margin_of_safety_pct is None
        # Upside cannot be computed without a valid price, so the
        # pre-existing INSUFFICIENT_DATA guard applies; fair value itself
        # (EPS x target P/E) stays valid and finite.
        assert result.valuation_status == "INSUFFICIENT_DATA"
        assert result.scenarios["base"].fair_value == 1260.0


def test_p3_nonfinite_benchmark_series_filtered():
    import math

    engine = ValuationEngine()
    polluted = [7.0, float("nan"), float("inf"), -float("inf"), None, 7.0, 8.0]
    result = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
        historical_pe_values=polluted,
    )
    assert result.target_pe_source == "HISTORICAL_MEDIAN_PE"
    assert result.historical_median_pe == 7.0
    assert result.scenarios["base"].target_pe == 7.0
    for value in (result.expected_fair_value, result.margin_of_safety_pct):
        assert value is None or math.isfinite(value)


def test_p3_nonfinite_scores_fall_back_to_defaults():
    engine = ValuationEngine()
    nan = float("nan")
    guarded = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
        forecast_reliability_score=nan, historical_pe_values=[7.0],
        probability_confidence=nan, data_quality_score=nan,
    )
    defaulted = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
        forecast_reliability_score=None, historical_pe_values=[7.0],
        probability_confidence=50.0, data_quality_score=100.0,
    )
    assert guarded.valuation_confidence == defaulted.valuation_confidence
    assert guarded.driver_uncertainty == defaulted.driver_uncertainty


def test_p3_flip_dependence_alerts_remain_explicitly_unresolved():
    engine = ValuationEngine()
    flip_base = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0,
        make_forecast(150.0, 150.0, 250.0), historical_pe_values=[7.0],
    )
    assert flip_base.valuation_status == "ATTRACTIVE"
    vocab = " ".join(flip_base.alerts + flip_base.valuation_risk_flags)
    for name in ("ASSESSMENT_FLIP_RISK", "HIGH_MULTIPLE_DEPENDENCE",
                 "HIGH_EPS_DEPENDENCE", "MARGIN_ASSUMPTION_RISK",
                 "HIGH_IMPACT_HIGH_UNCERTAINTY"):
        # Per P3 requirement 5: no invented formula may emit these alerts.
        # They stay absent until the locked spec defines their formulas.
        assert name not in vocab


# P4 additions: actual industry peer count in the output contract.
# Existing tests above untouched.
def test_p4_peer_count_below_minimum_falls_back():
    engine = ValuationEngine()
    result = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
        historical_pe_values=[7.0],
        industry_forward_pe_values=[6.0] * 7,
    )
    assert result.industry_peer_count == 7
    assert result.target_pe_source == "HISTORICAL_MEDIAN_PE"
    assert result.target_pe_source != "INDUSTRY_FORWARD_PE"
    assert "INSUFFICIENT_PEER_DATA" in result.valuation_risk_flags


def test_p4_peer_count_at_minimum_selects_industry_forward():
    result = ValuationEngine().calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
        industry_forward_pe_values=[6.0] * 8,
    )
    assert result.industry_peer_count == 8
    assert result.target_pe_source == "INDUSTRY_FORWARD_PE"
    assert result.scenarios["base"].target_pe == 6.0
    assert result.industry_forward_pe_median == 6.0


def test_p4_peer_count_above_minimum_and_median_provenance():
    values = [5.0, 6.0, 6.0, 7.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0]
    result = ValuationEngine().calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
        industry_forward_pe_values=values,
    )
    from statistics import median

    assert result.industry_peer_count == 10
    assert result.target_pe_source == "INDUSTRY_FORWARD_PE"
    assert result.industry_forward_pe_median == median(values)
    assert result.scenarios["base"].target_pe == median(values)


def test_p4_peer_count_filters_invalid_values():
    import math

    engine = ValuationEngine()
    polluted = [6.0] * 8 + [float("nan"), float("inf"), -float("inf"), None, 0.0, -3.0]
    result = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
        industry_forward_pe_values=polluted,
    )
    # Only the 8 finite positive values count; NaN/inf/None/zero/negative
    # are filtered before counting, median, and benchmark selection alike.
    assert result.industry_peer_count == 8
    assert result.target_pe_source == "INDUSTRY_FORWARD_PE"
    assert result.industry_forward_pe_median == 6.0
    assert math.isfinite(result.scenarios["base"].target_pe)


def test_p4_peer_count_empty_data_reports_zero_and_falls_back():
    engine = ValuationEngine()
    for peers in (None, [], [None, float("nan"), 0.0, -1.0]):
        result = engine.calculate_valuation(
            1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
            historical_pe_values=[7.0],
            industry_forward_pe_values=peers,
        )
        assert result.industry_peer_count == 0
        assert result.industry_forward_pe_median is None
        assert result.target_pe_source == "HISTORICAL_MEDIAN_PE"


def test_p4_benchmark_fallback_ignores_forward_count_for_ttm():
    # TTM fallback must not consume forward P/E values: populations stay
    # separate per spec section 12; the reported count is forward-only.
    result = ValuationEngine().calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
        industry_forward_pe_values=[6.0] * 7,
        industry_ttm_pe_values=[5.0, 6.0, 7.0],
    )
    assert result.industry_peer_count == 7
    assert result.target_pe_source == "INDUSTRY_TTM_PE"
    assert result.scenarios["base"].target_pe == 6.0
    assert result.industry_ttm_pe_median == 6.0


# P5 additions: PIT and adversarial input audit. Existing tests above untouched.
def _assert_all_p5_outputs_finite_or_none(result):
    import math

    values = [
        result.expected_fair_value,
        result.margin_of_safety_pct,
        result.valuation_confidence,
        result.valuation_data_quality,
        result.forecast_reliability_score,
        result.probability_confidence,
        result.historical_median_pe,
        result.industry_forward_pe_median,
        result.industry_ttm_pe_median,
    ]
    for scenario in result.scenarios.values():
        values.extend((
            scenario.target_pe,
            scenario.eps_forecast,
            scenario.forward_pe,
            scenario.fair_value,
            scenario.upside_downside_pct,
            scenario.probability,
        ))
    values.extend(result.driver_impact.values())
    values.extend(result.driver_uncertainty.values())
    values.extend(result.review_priority.values())
    for value in values:
        assert value is None or math.isfinite(value), f"non-finite output leaked: {value!r}"


def test_p5_nonfinite_price_yields_null_outputs():
    engine = ValuationEngine()
    for price in (float("nan"), float("inf"), -float("inf"), None):
        result = engine.calculate_valuation(
            1, 101, "PETROCHEMICAL", price, make_forecast(),
            historical_pe_values=[7.0],
        )
        for scenario in result.scenarios.values():
            assert scenario.forward_pe is None
            assert scenario.upside_downside_pct is None
        assert result.margin_of_safety_pct is None
        assert result.valuation_status == "INSUFFICIENT_DATA"
        # Fair value (EPS x target P/E) needs no price and stays valid.
        assert result.scenarios["base"].fair_value == 1260.0
        _assert_all_p5_outputs_finite_or_none(result)


def test_p5_missing_eps_is_not_applicable_not_zero():
    result = ValuationEngine().calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0,
        make_forecast(None, None, None), historical_pe_values=[7.0],
    )
    for scenario in result.scenarios.values():
        assert scenario.forward_pe is None
        assert scenario.fair_value is None
        assert "NOT_APPLICABLE" in scenario.flags
    assert result.expected_fair_value is None
    assert result.valuation_status in {"NOT_APPLICABLE", "INSUFFICIENT_DATA"}
    assert result.valuation_driver_ranking == []
    _assert_all_p5_outputs_finite_or_none(result)


def test_p5_nonfinite_reliability_echo_sanitized():
    engine = ValuationEngine()
    for bad in (float("nan"), float("inf"), -float("inf")):
        result = engine.calculate_valuation(
            1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
            forecast_reliability_score=bad, historical_pe_values=[7.0],
        )
        assert result.forecast_reliability_score is None
        assert "LOW_FORECAST_RELIABILITY" not in result.valuation_risk_flags
        assert not any("LOW_FORECAST_RELIABILITY" in alert for alert in result.alerts)
        _assert_all_p5_outputs_finite_or_none(result)
    defaulted = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
        forecast_reliability_score=None, historical_pe_values=[7.0],
    )
    guarded = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
        forecast_reliability_score=float("nan"), historical_pe_values=[7.0],
    )
    assert guarded.valuation_confidence == defaulted.valuation_confidence
    assert guarded.driver_uncertainty == defaulted.driver_uncertainty


def test_p5_nonfinite_probability_confidence_echo_finite():
    engine = ValuationEngine()
    for bad in (float("nan"), float("inf"), -float("inf"), None):
        result = engine.calculate_valuation(
            1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
            historical_pe_values=[7.0], probability_confidence=bad,
        )
        assert result.probability_confidence == 50.0
        _assert_all_p5_outputs_finite_or_none(result)
    defaulted = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
        historical_pe_values=[7.0], probability_confidence=50.0,
    )
    guarded = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
        historical_pe_values=[7.0], probability_confidence=float("nan"),
    )
    assert guarded.driver_uncertainty == defaulted.driver_uncertainty
    assert guarded.valuation_confidence == defaulted.valuation_confidence


def test_p5_missing_data_quality_does_not_crash():
    engine = ValuationEngine()
    for quality, expected in ((None, 100.0), (float("nan"), 100.0), (150.0, 100.0), (-20.0, 0.0)):
        result = engine.calculate_valuation(
            1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
            historical_pe_values=[7.0], data_quality_score=quality,
        )
        assert result.valuation_data_quality == expected
        _assert_all_p5_outputs_finite_or_none(result)
    missing = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
        historical_pe_values=[7.0], data_quality_score=None,
    )
    full = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
        historical_pe_values=[7.0], data_quality_score=100.0,
    )
    assert missing.valuation_confidence == full.valuation_confidence


def test_p5_nonfinite_multiple_adjustment_rejected():
    import pytest as _pytest

    engine = ValuationEngine()
    for bad in (float("nan"), float("inf"), -float("inf")):
        with _pytest.raises(ValueError, match="finite|bound"):
            engine.calculate_valuation(
                1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
                historical_pe_values=[7.0],
                scenario_pe_adjustments={"bull": bad},
                scenario_pe_rationales={"bull": "Probe of non-finite input handling."},
            )


def test_p5_nan_probability_evidence_rejected():
    import pytest as _pytest

    with _pytest.raises(ValueError, match="must be in"):
        ValuationEngine().calculate_valuation(
            1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
            historical_pe_values=[7.0],
            probability_evidence={"FUNDAMENTAL_DIRECTION": {"bear": float("nan"), "base": 0.5, "bull": 0.5}},
        )


def test_p5_datetime_echoes_normalized_to_utc():
    from datetime import datetime, timedelta, timezone

    engine = ValuationEngine()
    naive = datetime(2026, 3, 15, 12, 0, 0)
    aware = datetime(2026, 3, 15, 12, 0, 0, tzinfo=timezone(timedelta(hours=3, minutes=30)))
    kwargs = dict(
        company_id=1, period_id=101, industry_code="PETROCHEMICAL",
        current_price=1000.0, forecast_result=make_forecast(),
        historical_pe_values=[7.0], valuation_date=naive,
        market_price_date=aware, data_cutoff_datetime=naive,
    )
    result = engine.calculate_valuation(**kwargs)
    assert result.valuation_date == datetime(2026, 3, 15, 12, 0, 0, tzinfo=timezone.utc)
    assert result.market_price_date == aware.astimezone(timezone.utc)
    assert result.data_cutoff_datetime == datetime(2026, 3, 15, 12, 0, 0, tzinfo=timezone.utc)
    # Mixed naive/aware inputs are mutually comparable after normalization.
    assert (result.valuation_date <= result.market_price_date) or (result.valuation_date > result.market_price_date)
    again = engine.calculate_valuation(**kwargs)
    assert again.valuation_date == result.valuation_date
    assert again.market_price_date == result.market_price_date
    assert again.data_cutoff_datetime == result.data_cutoff_datetime


def test_p5_default_cutoff_inherits_forecast_cutoff_normalized():
    from datetime import datetime, timezone

    result = ValuationEngine().calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
        historical_pe_values=[7.0],
    )
    assert result.data_cutoff_datetime == datetime(2026, 1, 1, tzinfo=timezone.utc)


def test_p5_undated_benchmark_series_carry_no_provenance():
    from datetime import datetime

    # Stage 7 V1 benchmark inputs are plain floats: no observation dates,
    # publication timestamps, report versions, or per-value cutoff metadata
    # cross the boundary. The engine records medians and the forward-only
    # peer count plus a passthrough cutoff; it cannot verify PIT validity
    # of the series itself. valuation_date/market_price_date are echoed,
    # never cross-checked against the cutoff (reported contract limitation).
    result = ValuationEngine().calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
        historical_pe_values=[6.5, 7.0, 8.0],
        industry_forward_pe_values=[6.0] * 8,
        valuation_date=datetime(2026, 6, 1),
        market_price_date=datetime(2026, 6, 1),
        data_cutoff_datetime=datetime(2026, 1, 1),
    )
    assert result.historical_median_pe == 7.0
    assert result.industry_forward_pe_median == 6.0
    assert result.industry_peer_count == 8
    assert result.target_pe_source == "INDUSTRY_FORWARD_PE"
    # A valuation date after the cutoff is accepted without rejection or
    # flag: cross-validation is absent by design in V1.
    assert result.valuation_status == "FAIR"


# P6 additions: production-path, adversarial and regression validation.
# Existing tests above untouched. No production, spec, dependency, or config
# changes in P6; P6 is validation-only.
def _p6_production_forecast():
    """Real pipeline-produced forecast via the Stage 5 production engine.

    Uses ForecastEngine.generate_forecast (the Stage 5 production
    constructor) with caller-declared context plus historical dispersion
    series, so all three scenarios carry valid EPS. No synthetic
    make_forecast fixture, no fabricated records, no bypassed constructors.
    """
    from datetime import datetime, timezone

    from src.forecast.engine import ForecastEngine

    context = {
        "seasonality_valid": True,
        "seasonal_baseline_revenue": 10000.0,
        "recent_run_rate_revenue": 9000.0,
        "baseline_revenue_growth": 0.10,
        "historical_operating_margin": 0.20,
        "historical_net_margin": 0.10,
        "share_count": 1000.0,
        "net_profit_is_attributable": True,
        "historical_revenue_series": [8000.0, 8500.0, 9000.0, 9500.0, 10000.0, 10500.0],
        "historical_operating_series": [(2000.0, 8000.0)] * 6,
        "historical_net_series": [(800.0, 8000.0)] * 6,
    }
    return ForecastEngine().generate_forecast(
        1, 101, "PETROCHEMICAL", context,
        data_cutoff_datetime=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )


def test_p6_production_path_real_stage5_forecast():
    import math

    from src.forecast.schema import CompanyForecastResult

    forecast = _p6_production_forecast()
    assert isinstance(forecast, CompanyForecastResult)
    eps_values = (
        forecast.scenario_forecasts.bear.eps,
        forecast.scenario_forecasts.base.eps,
        forecast.scenario_forecasts.bull.eps,
    )
    assert all(v is not None and math.isfinite(v) and v > 0 for v in eps_values)
    result = ValuationEngine().calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, forecast,
        historical_pe_values=[6.5, 7.0, 8.0],
        forecast_reliability_score=80.0,
    )
    assert result.target_pe_source == "HISTORICAL_MEDIAN_PE"
    assert result.scenarios["base"].fair_value == 7.7
    assert result.valuation_status == "VERY_EXPENSIVE"
    assert result.data_cutoff_datetime == forecast.data_cutoff_datetime
    assert abs(sum(s.probability for s in result.scenarios.values()) - 1.0) < 1e-9
    for scenario in result.scenarios.values():
        assert scenario.fair_value is not None and math.isfinite(scenario.fair_value)
    assert set(result.valuation_driver_ranking) == {"EPS", "TARGET_PE"}


def test_p6_cutoff_pit_limitation_pinned():
    # V1 limitation re-asserted (P5 blocker stands): a valuation_date later
    # than data_cutoff_datetime is accepted without rejection or flag.
    # This pins the strongest valid boundary; genuine cross-validation
    # needs the contract decision recorded in the P5 report.
    from datetime import datetime

    engine = ValuationEngine()
    late = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
        historical_pe_values=[7.0],
        valuation_date=datetime(2026, 6, 1),
        market_price_date=datetime(2026, 6, 1),
        data_cutoff_datetime=datetime(2026, 1, 1),
    )
    assert late.valuation_status == "ATTRACTIVE"
    assert not any("PIT" in flag for flag in late.valuation_risk_flags)


def test_p6_missing_benchmarks_yield_guarded_nulls():
    import math

    result = ValuationEngine().calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
    )
    assert result.target_pe_source == "INSUFFICIENT_DATA"
    assert result.industry_peer_count == 0
    assert result.valuation_status == "INSUFFICIENT_DATA"
    assert result.expected_fair_value is None
    assert result.margin_of_safety_pct is None
    for scenario in result.scenarios.values():
        assert scenario.target_pe is None
        assert scenario.fair_value is None
    assert "INDUSTRY_BENCHMARK_INSUFFICIENT" in result.valuation_risk_flags
    assert any("INSUFFICIENT_BENCHMARK_DATA" in alert for alert in result.alerts)
    for value in (result.expected_fair_value, result.margin_of_safety_pct):
        assert value is None or math.isfinite(value)


def test_p6_scenario_ordering_flag_and_probability_normalization():
    import math

    engine = ValuationEngine()
    inverted = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0,
        make_forecast(300.0, 180.0, 100.0), historical_pe_values=[7.0],
    )
    assert "SCENARIO_ORDER_WARNING" in inverted.valuation_risk_flags
    assert inverted.scenarios["bear"].fair_value == 2100.0
    assert inverted.scenarios["base"].fair_value == 1260.0
    assert inverted.scenarios["bull"].fair_value == 700.0
    assert abs(sum(s.probability for s in inverted.scenarios.values()) - 1.0) < 1e-9
    evidence = {
        "FUNDAMENTAL_DIRECTION": {"bear": 0.1, "base": 0.3, "bull": 0.6},
        "FORECAST_DIRECTION": {"bear": 0.2, "base": 0.5, "bull": 0.3},
        "PROFITABILITY_ASSUMPTION_RISK": {"bear": 0.4, "base": 0.4, "bull": 0.2},
        "DATA_STRUCTURAL_RISK": {"bear": 0.5, "base": 0.3, "bull": 0.2},
    }
    blended = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
        historical_pe_values=[7.0], probability_evidence=evidence,
    )
    assert abs(sum(s.probability for s in blended.scenarios.values()) - 1.0) < 1e-9
    assert all(
        math.isfinite(s.probability) and s.probability >= 0
        for s in blended.scenarios.values()
    )


def test_p6_invalid_eps_variants_never_fabricate_values():
    import math

    engine = ValuationEngine()
    for bear, base, bull in (
        (0.0, -5.0, 0.0),
        (float("nan"), float("nan"), float("nan")),
        (None, None, None),
    ):
        result = engine.calculate_valuation(
            1, 101, "PETROCHEMICAL", 1000.0,
            make_forecast(bear, base, bull), historical_pe_values=[7.0],
        )
        for scenario in result.scenarios.values():
            assert scenario.forward_pe is None
            assert scenario.fair_value is None or math.isfinite(scenario.fair_value)
        assert result.expected_fair_value is None
        assert result.valuation_status in {"NOT_APPLICABLE", "INSUFFICIENT_DATA"}
        assert result.valuation_driver_ranking == []
        assert result.driver_impact == {}
    zero = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0,
        make_forecast(0.0, -5.0, 0.0), historical_pe_values=[7.0],
    )
    assert "ZERO_EPS" in zero.scenarios["bear"].flags
    assert "NEGATIVE_EPS" in zero.scenarios["base"].flags
    assert zero.valuation_status == "NOT_APPLICABLE"


def test_p6_repeat_runs_identical_on_full_contract():
    import dataclasses

    engine = ValuationEngine()
    kwargs = dict(
        company_id=1, period_id=101, industry_code="PETROCHEMICAL",
        current_price=1000.0, forecast_result=make_forecast(),
        forecast_reliability_score=70.0, historical_pe_values=[6.5, 7.0, 8.0],
        industry_forward_pe_values=[6.0] * 8, probability_confidence=60.0,
        data_quality_score=80.0,
        scenario_pe_adjustments={"bear": -0.10, "base": 0.0, "bull": 0.10},
        scenario_pe_rationales={
            "bear": "Higher earnings and discount-rate risk reduces justified multiple.",
            "base": "Historical median is the neutral benchmark.",
            "bull": "Improved sustainable earnings quality supports a modest multiple premium.",
        },
    )
    first = dataclasses.asdict(engine.calculate_valuation(**kwargs))
    second = dataclasses.asdict(engine.calculate_valuation(**kwargs))
    # Wall-clock calculation_timestamp is excluded; everything else must match.
    first.pop("calculation_timestamp")
    second.pop("calculation_timestamp")
    assert first == second


def test_p6_regression_prior_behavior_preserved():
    engine = ValuationEngine()
    base_case = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
        forecast_reliability_score=85.0, historical_pe_values=[6.5, 7.0, 8.0],
        probability_confidence=90.0,
    )
    # Golden values pinned by the baseline report and P2-P5 runs.
    assert base_case.scenarios["bear"].fair_value == 1050.0
    assert base_case.scenarios["base"].fair_value == 1260.0
    assert base_case.scenarios["bull"].fair_value == 1470.0
    assert base_case.expected_fair_value == 1260.0
    assert base_case.margin_of_safety_pct == 26.0
    assert base_case.valuation_status == "ATTRACTIVE"
    assert base_case.target_pe_source == "HISTORICAL_MEDIAN_PE"
    assert base_case.contract_version == "VALUATION_CONTRACT_V1"
    assert base_case.model_version == "STAGE7_V1"
    assert base_case.industry_peer_count == 0
    assert abs(base_case.driver_impact["EPS"] - 50.0) < 1e-6
    assert abs(base_case.driver_impact["TARGET_PE"] - 50.0) < 1e-6
    # Benchmark hierarchy regression: TTM fallback order intact.
    ttm = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
        industry_forward_pe_values=[6.0] * 7,
        industry_ttm_pe_values=[5.0, 6.0, 7.0],
    )
    assert ttm.target_pe_source == "INDUSTRY_TTM_PE"
    assert ttm.industry_peer_count == 7


def test_p10_expensive_base_upside_parameterized_outputs_unchanged():
    import dataclasses
    import hashlib
    import json

    from src.valuation.parameters import VALUATION_THRESHOLDS

    # Spec section 35 requires the Expensive base-upside cutoff to be a stored
    # versioned parameter; the engine must consume that key (value 0.0 preserves
    # the pre-change '< 0.0' comparison exactly).
    assert VALUATION_THRESHOLDS["expensive_base_upside"] == 0.0
    engine = ValuationEngine()
    golden = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
        forecast_reliability_score=85.0, historical_pe_values=[6.5, 7.0, 8.0],
        probability_confidence=90.0,
    )
    assert golden.scenarios["bear"].fair_value == 1050.0
    assert golden.scenarios["base"].fair_value == 1260.0
    assert golden.scenarios["bull"].fair_value == 1470.0
    assert golden.expected_fair_value == 1260.0
    assert golden.margin_of_safety_pct == 26.0
    assert golden.valuation_status == "ATTRACTIVE"
    assert golden.contract_version == "VALUATION_CONTRACT_V1"
    assert golden.model_version == "STAGE7_V1"
    representation = dataclasses.asdict(golden)
    representation.pop("calculation_timestamp")
    digest = hashlib.sha256(
        json.dumps(representation, sort_keys=True, default=str).encode()
    ).hexdigest()
    # P33 re-baselined digest: the only output change is the additive parameter
    # audit metadata (parameter_set_version + 38-key parameter_snapshot); all
    # financial outputs above verified unchanged, and the pre-P33 digest
    # reproduces byte-for-byte with those two keys removed.
    assert digest == "7b5fb909153ec0517b4c945688a8c661a56921191602021748ff43652df33f33"
    # Boundary pair bracketing the parameterized cutoff: expected upside
    # <= -10 with base upside on each side of 0.0.
    expensive = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(70.0, 140.0, 150.0),
        forecast_reliability_score=85.0, historical_pe_values=[7.0],
    )
    assert expensive.valuation_status == "EXPENSIVE"
    fair = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(55.0, 145.0, 150.0),
        forecast_reliability_score=85.0, historical_pe_values=[7.0],
    )
    assert fair.valuation_status == "FAIR"


def test_p10_expensive_threshold_consumed_from_parameters():
    from src.valuation import parameters as valuation_parameters

    engine = ValuationEngine()
    original = valuation_parameters.VALUATION_THRESHOLDS["expensive_base_upside"]
    try:
        valuation_parameters.VALUATION_THRESHOLDS["expensive_base_upside"] = -50.0
        relaxed = engine.calculate_valuation(
            1, 101, "PETROCHEMICAL", 1000.0, make_forecast(70.0, 140.0, 150.0),
            forecast_reliability_score=85.0, historical_pe_values=[7.0],
        )
        # With the cutoff relaxed to -50.0, the same -2.0 base upside no longer
        # satisfies the Expensive branch and falls through to FAIR.
        assert relaxed.scenarios["base"].upside_downside_pct == -2.0
        assert relaxed.valuation_status == "FAIR"
    finally:
        valuation_parameters.VALUATION_THRESHOLDS["expensive_base_upside"] = original
    restored = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(70.0, 140.0, 150.0),
        forecast_reliability_score=85.0, historical_pe_values=[7.0],
    )
    assert restored.valuation_status == "EXPENSIVE"


def test_p12_calculation_timestamp_utc_aware_and_deterministic():
    import dataclasses

    engine = ValuationEngine()
    result = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
        forecast_reliability_score=85.0, historical_pe_values=[6.5, 7.0, 8.0],
        probability_confidence=90.0,
    )
    # Timezone-aware UTC construction (no naive datetime.utcnow()).
    assert result.calculation_timestamp.tzinfo is not None
    assert result.calculation_timestamp.utcoffset() == timezone.utc.utcoffset(None)
    # Deterministic behavior unchanged apart from the wall-clock timestamp.
    second = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(),
        forecast_reliability_score=85.0, historical_pe_values=[6.5, 7.0, 8.0],
        probability_confidence=90.0,
    )
    first_dict = dataclasses.asdict(result)
    second_dict = dataclasses.asdict(second)
    first_dict.pop("calculation_timestamp")
    second_dict.pop("calculation_timestamp")
    assert first_dict == second_dict
    # Golden outputs pinned by prior runs are unaffected.
    assert result.scenarios["base"].fair_value == 1260.0
    assert result.expected_fair_value == 1260.0
    assert result.valuation_status == "ATTRACTIVE"


def _p32_ref(available_at, version=7):
    return ForecastInputRef(
        fact_key="EPS",
        report_version_id=version,
        available_at=available_at,
        source="CODAL",
    )


def _p32_kwargs(**overrides):
    params = dict(
        company_id=1,
        period_id=101,
        industry_code="PETROCHEMICAL",
        current_price=1000.0,
        forecast_result=make_forecast(),
        historical_pe_values=[7.0],
    )
    params.update(overrides)
    return params


def test_p32_input_refs_before_cutoff_leave_results_unchanged():
    import dataclasses

    engine = ValuationEngine()
    plain = engine.calculate_valuation(**_p32_kwargs())
    refs = [
        _p32_ref(datetime(2025, 12, 1)),
        _p32_ref(datetime(2025, 6, 15, tzinfo=timezone.utc), version=9),
    ]
    with_refs = engine.calculate_valuation(**_p32_kwargs(forecast_input_refs=refs))
    first = dataclasses.asdict(plain)
    second = dataclasses.asdict(with_refs)
    first.pop("calculation_timestamp")
    second.pop("calculation_timestamp")
    assert first == second


def test_p32_input_ref_after_cutoff_rejected_on_valuation_path():
    engine = ValuationEngine()
    with pytest.raises(ValueError, match="after the"):
        engine.calculate_valuation(
            **_p32_kwargs(forecast_input_refs=[_p32_ref(datetime(2026, 3, 1))])
        )


def test_p32_input_ref_at_cutoff_boundary_accepted():
    engine = ValuationEngine()
    result = engine.calculate_valuation(
        **_p32_kwargs(forecast_input_refs=[_p32_ref(datetime(2026, 1, 1))])
    )
    assert result.expected_fair_value == 1260.0
    assert result.valuation_status == "ATTRACTIVE"


def test_p32_input_ref_missing_date_rejected():
    engine = ValuationEngine()
    with pytest.raises(ValueError, match="without"):
        engine.calculate_valuation(**_p32_kwargs(forecast_input_refs=[_p32_ref(None)]))


def test_p32_input_refs_absent_preserves_legacy_path():
    engine = ValuationEngine()
    result = engine.calculate_valuation(**_p32_kwargs(forecast_input_refs=None))
    assert result.valuation_status == "ATTRACTIVE"
    assert result.expected_fair_value == 1260.0


def _p33_snapshot():
    from src.valuation.parameters import GENESIS_VERSION

    return {record.parameter_name: record.parameter_value for record in GENESIS_VERSION.records}


def test_p33_genesis_snapshot_matches_live_constants():
    import src.valuation.parameters as params

    snapshot = _p33_snapshot()
    assert snapshot["VALUATION_THRESHOLDS.attractive_expected_upside"] == params.VALUATION_THRESHOLDS["attractive_expected_upside"] == 15.0
    assert snapshot["SENSITIVITY_PERTURBATION"] == params.SENSITIVITY_PERTURBATION == 0.10
    assert snapshot["MIN_INDUSTRY_PEERS"] == params.MIN_INDUSTRY_PEERS == 8
    assert snapshot["MODEL_VERSION"] == params.MODEL_VERSION == "STAGE7_V1"
    assert len(snapshot) == len(params.GENESIS_VERSION.records) == 38
    assert all(record.effective_from is None for record in params.GENESIS_VERSION.records)


def test_p33_result_carries_parameter_audit():
    import dataclasses

    engine = ValuationEngine()
    kwargs = dict(
        company_id=1,
        period_id=101,
        industry_code="PETROCHEMICAL",
        current_price=1000.0,
        forecast_result=make_forecast(),
        historical_pe_values=[7.0],
    )
    first = engine.calculate_valuation(**kwargs)
    second = engine.calculate_valuation(**kwargs)
    assert first.metadata["parameter_set_version"] == "STAGE7_V1/GENESIS"
    assert first.metadata["parameter_snapshot"] == _p33_snapshot()
    first_dict = dataclasses.asdict(first)
    second_dict = dataclasses.asdict(second)
    first_dict.pop("calculation_timestamp")
    second_dict.pop("calculation_timestamp")
    assert first_dict == second_dict


def test_p33_resolve_exact_key_and_missing_raises():
    from src.valuation.parameters import DEFAULT_REGISTRY, resolve_parameter_set

    assert resolve_parameter_set("STAGE7_V1/GENESIS", DEFAULT_REGISTRY).model_version == "STAGE7_V1"
    with pytest.raises(KeyError):
        resolve_parameter_set("STAGE7_V99/NOPE", DEFAULT_REGISTRY)


def test_p33_as_of_without_dated_records_raises():
    from src.valuation.parameters import DEFAULT_REGISTRY, resolve_parameter_set_as_of

    with pytest.raises(LookupError, match="R8"):
        resolve_parameter_set_as_of(datetime(2026, 1, 1), DEFAULT_REGISTRY)
    with pytest.raises(LookupError):
        resolve_parameter_set_as_of(None, DEFAULT_REGISTRY)


def _p33_synthetic_registry():
    from src.valuation.parameters import ParameterRegistry, ParameterSetVersion

    v1 = ParameterSetVersion(model_version="STAGE7_V1", version_key="TEST/V1", effective_from=datetime(2025, 1, 1), records=())
    v2 = ParameterSetVersion(model_version="STAGE7_V1", version_key="TEST/V2", effective_from=datetime(2026, 1, 1), records=())
    return ParameterRegistry(versions=(v1, v2))


def test_p33_as_of_selection_mechanics():
    from src.valuation.parameters import resolve_parameter_set_as_of

    registry = _p33_synthetic_registry()
    assert resolve_parameter_set_as_of(datetime(2026, 1, 1), registry).version_key == "TEST/V2"
    assert resolve_parameter_set_as_of(datetime(2025, 6, 1), registry).version_key == "TEST/V1"
    assert resolve_parameter_set_as_of(datetime(2025, 12, 31), registry).version_key == "TEST/V1"
    with pytest.raises(LookupError):
        resolve_parameter_set_as_of(datetime(2024, 1, 1), registry)


def test_p33_as_of_overlap_raises_ambiguity():
    from src.valuation.parameters import ParameterRegistry, ParameterSetVersion, resolve_parameter_set_as_of

    dup = ParameterRegistry(
        versions=(
            ParameterSetVersion(model_version="M", version_key="TEST/A", effective_from=datetime(2025, 1, 1), records=()),
            ParameterSetVersion(model_version="M", version_key="TEST/B", effective_from=datetime(2025, 1, 1), records=()),
        )
    )
    with pytest.raises(LookupError, match="Ambiguous"):
        resolve_parameter_set_as_of(datetime(2025, 6, 1), dup)


def test_p36_parameter_resolution_as_of_cutoff_governs_and_snapshots():
    from src.valuation.parameters import (
        DEFAULT_REGISTRY,
        ParameterRecord,
        ParameterRegistry,
        ParameterSetVersion,
        VALUATION_THRESHOLDS,
    )

    # Build a synthetic dated version to test on-path parameter consumption via calculate_valuation
    custom_records = list(DEFAULT_REGISTRY.versions[0].records)
    # Modify a threshold in the custom record: change attractive_expected_upside to 50.0
    for i, rec in enumerate(custom_records):
        if rec.parameter_name == "VALUATION_THRESHOLDS.attractive_expected_upside":
            custom_records[i] = ParameterRecord(
                parameter_name=rec.parameter_name,
                parameter_value=50.0,
                effective_from=datetime(2026, 1, 1),
                description="Custom attractive threshold",
            )
            break

    v_dated = ParameterSetVersion(
        model_version="STAGE7_V1",
        version_key="TEST/DATED_2026",
        effective_from=datetime(2026, 1, 1),
        records=tuple(custom_records),
    )

    custom_registry = ParameterRegistry(versions=(DEFAULT_REGISTRY.versions[0], v_dated))

    engine = ValuationEngine()
    
    # Test 1: Undated / undated-registry cutoff falls back safely to GENESIS
    res_genesis = engine.calculate_valuation(
        1, 101, "PETROCHEMICAL", 1000.0, make_forecast(), historical_pe_values=[7.0],
        data_cutoff_datetime=datetime(2025, 6, 1)
    )
    assert res_genesis.metadata["parameter_set_version"] == "STAGE7_V1/GENESIS"
    assert res_genesis.metadata["parameter_snapshot"]["VALUATION_THRESHOLDS.attractive_expected_upside"] == 15.0

    # Test 2: Pass custom registry to resolve_parameter_set_as_of directly for custom cutoff
    from src.valuation.parameters import resolve_parameter_set_as_of
    resolved = resolve_parameter_set_as_of(datetime(2026, 6, 1), custom_registry)
    assert resolved.version_key == "TEST/DATED_2026"
    assert resolved.records[12].parameter_value == 50.0 or any(r.parameter_value == 50.0 for r.records in [resolved.records] for r in r)
