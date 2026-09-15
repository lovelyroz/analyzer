from datetime import datetime, timedelta

from src.evaluation.engine import ForecastEvaluationEngine
from src.evaluation.metrics import (
    accuracy_score_from_mape,
    calculate_ape,
    calculate_bias,
    calculate_error,
    calculate_mape,
    calculate_percentage_error,
    detect_persistent_bias,
    observation_confidence,
)


def test_stage6_metric_definitions():
    assert calculate_error(110.0, 100.0) == -10.0
    assert calculate_percentage_error(100.0, 110.0) == 10.0
    assert calculate_ape(100.0, 110.0) == 10.0
    assert calculate_mape([10.0, -10.0, 20.0]) == 13.333333333333334
    assert calculate_bias([10.0, 10.0, 10.0]) == 10.0


def test_zero_and_sign_change_exceptions():
    engine = ForecastEvaluationEngine()
    cutoff = datetime(2026, 1, 1)

    zero = engine.build_evaluation(
        company_id=1,
        period_id=101,
        metric_code="EPS",
        forecast_value=0.0,
        actual_value=100.0,
        horizon="3M",
        model_version="V1",
        forecast_cutoff_datetime=cutoff,
    )
    assert zero.regime_status == "ZERO_BASE"
    assert zero.percentage_error is None
    assert zero.absolute_percentage_error is None
    assert zero.error_amount == 100.0

    transition = engine.build_evaluation(
        company_id=1,
        period_id=102,
        metric_code="EPS",
        forecast_value=-10.0,
        actual_value=5.0,
        horizon="3M",
        model_version="V1",
        forecast_cutoff_datetime=cutoff,
    )
    assert transition.regime_status == "LOSS_TO_PROFIT"
    assert transition.absolute_percentage_error is None


def test_point_in_time_actual_selection():
    engine = ForecastEvaluationEngine()
    cutoff = datetime(2026, 3, 1)
    candidates = [
        (datetime(2026, 3, 2), 1, 100.0),
        (datetime(2026, 4, 2), 2, 110.0),
    ]
    selected = engine.select_point_in_time_actual(candidates, cutoff)
    assert selected == candidates[1]
    assert engine.select_point_in_time_actual([(datetime(2026, 2, 28), 3, 90.0)], cutoff) is None


def test_seasonal_naive_baseline():
    engine = ForecastEvaluationEngine()
    assert engine.seasonal_naive_forecast([100.0, 110.0, 120.0, 130.0], 2) == 120.0
    assert engine.seasonal_naive_forecast([100.0], 2) is None


def test_observation_confidence_bands():
    assert observation_confidence(4) == "INSUFFICIENT_DATA"
    assert observation_confidence(5) == "LOW_CONFIDENCE"
    assert observation_confidence(7) == "LOW_CONFIDENCE"
    assert observation_confidence(8) == "MODERATE_CONFIDENCE"
    assert observation_confidence(11) == "MODERATE_CONFIDENCE"
    assert observation_confidence(12) == "ADEQUATE"


def test_reliability_uses_accuracy_bias_and_baseline_with_confidence():
    engine = ForecastEvaluationEngine()
    cutoff = datetime(2026, 1, 1)
    evaluations = []
    for period_id in range(1, 9):
        evaluations.append(
            engine.build_evaluation(
                company_id=1,
                period_id=period_id,
                metric_code="EPS",
                forecast_value=100.0,
                actual_value=110.0,
                horizon="3M",
                model_version="V1",
                forecast_cutoff_datetime=cutoff + timedelta(days=period_id),
                baseline_value=120.0,
            )
        )

    result = engine.evaluate_forecasts(1, "EPS", evaluations, horizon="3M", model_version="V1")

    assert result.observation_count == 8
    assert result.confidence_level == "MODERATE_CONFIDENCE"
    assert result.mape == 10.0
    assert result.bias == 10.0
    assert result.persistent_bias == "UNDER_FORECAST_BIAS"
    assert result.baseline_mape > result.mape
    assert result.relative_improvement > 0
    assert result.model_underperforms_baseline is False
    assert 0 <= result.performance_score <= 100
    assert result.reliability_score < result.performance_score
    assert result.calibration_state == "CALIBRATION_CANDIDATE"


def test_horizons_and_model_versions_are_independent_and_duplicates_removed():
    engine = ForecastEvaluationEngine()
    cutoff = datetime(2026, 1, 1)
    base = engine.build_evaluation(
        company_id=1,
        period_id=1,
        metric_code="EPS",
        forecast_value=100.0,
        actual_value=105.0,
        horizon="1M",
        model_version="V1",
        forecast_cutoff_datetime=cutoff,
    )
    duplicate = engine.build_evaluation(
        company_id=1,
        period_id=1,
        metric_code="EPS",
        forecast_value=100.0,
        actual_value=105.0,
        horizon="1M",
        model_version="V1",
        forecast_cutoff_datetime=cutoff,
    )
    other_horizon = engine.build_evaluation(
        company_id=1,
        period_id=1,
        metric_code="EPS",
        forecast_value=100.0,
        actual_value=105.0,
        horizon="12M",
        model_version="V1",
        forecast_cutoff_datetime=cutoff,
    )

    result = engine.evaluate_forecasts(1, "EPS", [base, duplicate, other_horizon], horizon="1M", model_version="V1")
    assert result.observation_count == 1


def test_persistent_underperformance_requires_evidence():
    engine = ForecastEvaluationEngine()
    cutoff = datetime(2026, 1, 1)
    evaluations = [
        engine.build_evaluation(
            company_id=1,
            period_id=i,
            metric_code="EPS",
            forecast_value=100.0,
            actual_value=120.0,
            horizon="6M",
            model_version="V1",
            forecast_cutoff_datetime=cutoff + timedelta(days=i),
            baseline_value=105.0,
        )
        for i in range(1, 6)
    ]
    result = engine.evaluate_forecasts(1, "EPS", evaluations, horizon="6M", model_version="V1")
    assert result.model_underperforms_baseline is True
    assert "MODEL_UNDERPERFORMS_BASELINE" in (result.calibration_reason or "")


def test_calibration_creates_new_version_only_after_holdout():
    engine = ForecastEvaluationEngine()
    assert engine.calibration_model_version("V1", "CALIBRATION_CANDIDATE", False) is None
    assert engine.calibration_model_version("V1", "NO_CALIBRATION", True) is None
    assert engine.calibration_model_version("V1", "CALIBRATION_CANDIDATE", True) == "V1.CAL1"


def test_accuracy_mapping_is_version_parameterized():
    assert accuracy_score_from_mape(0.0, poor_mape=50.0) == 100.0
    assert accuracy_score_from_mape(25.0, poor_mape=50.0) == 50.0
    assert accuracy_score_from_mape(60.0, poor_mape=50.0) == 0.0


def test_persistent_bias_requires_five_valid_observations():
    assert detect_persistent_bias([20.0, 20.0, 20.0, 20.0]) == "NEUTRAL"
    assert detect_persistent_bias([20.0, 20.0, 20.0, 20.0, 20.0]) == "UNDER_FORECAST_BIAS"
