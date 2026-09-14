import pytest
from datetime import datetime
from src.evaluation.metrics import calculate_pe, calculate_mape, detect_persistent_bias
from src.evaluation.schema import ForecastEvaluationResult
from src.evaluation.engine import ForecastEvaluationEngine

def test_metrics_calculations():
    assert calculate_pe(110.0, 100.0) == 10.0
    assert calculate_pe(90.0, 100.0) == -10.0
    assert calculate_mape([10.0, -10.0, 20.0]) == 13.333333333333334

def test_persistent_bias_detection():
    # 4 overestimate errors
    errors = [15.0, 12.0, 18.0, 14.0]
    assert detect_persistent_bias(errors) == "OVERESTIMATING"

def test_forecast_evaluation_engine():
    engine = ForecastEvaluationEngine()
    
    evals = [
        ForecastEvaluationResult(1, 101, "EPS", 120.0, 100.0, 20.0, 20.0, 20.0),
        ForecastEvaluationResult(1, 102, "EPS", 115.0, 100.0, 15.0, 15.0, 15.0),
        ForecastEvaluationResult(1, 103, "EPS", 125.0, 100.0, 25.0, 25.0, 25.0),
        ForecastEvaluationResult(1, 104, "EPS", 118.0, 100.0, 18.0, 18.0, 18.0),
    ]

    result = engine.evaluate_forecasts(company_id=1, metric_code="EPS", evaluations=evals, baseline_mape=15.0)

    assert result.company_id == 1
    assert result.mape == 19.5
    assert result.reliability_score == 80.5
    assert result.persistent_bias == "OVERESTIMATING"
    assert result.calibration_state == "CALIBRATION_CANDIDATE"
    assert result.underperforms_baseline is True