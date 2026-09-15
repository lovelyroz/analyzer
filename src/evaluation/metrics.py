from __future__ import annotations

from statistics import mean
from typing import Iterable, List, Optional


INVALID_REGIMES = {
    "ZERO_BASE",
    "LOSS_TO_PROFIT",
    "PROFIT_TO_LOSS",
    "SIGN_CHANGE",
}


def _valid_number(value: Optional[float]) -> bool:
    return value is not None and value == value


def calculate_error(forecast: float, actual: float) -> float:
    """Stage 6 canonical error: Actual - Forecast."""
    return actual - forecast


def calculate_percentage_error(forecast: float, actual: float) -> Optional[float]:
    """Signed percentage error using |Forecast| as denominator."""
    if not _valid_number(forecast) or not _valid_number(actual) or forecast == 0:
        return None
    return (actual - forecast) / abs(forecast) * 100.0


def calculate_ape(forecast: float, actual: float) -> Optional[float]:
    """Absolute percentage error using |Forecast| as denominator."""
    percentage_error = calculate_percentage_error(forecast, actual)
    return abs(percentage_error) if percentage_error is not None else None


def classify_regime(forecast: float, actual: float) -> Optional[str]:
    """Return the Stage 6 regime that invalidates ordinary percentage metrics."""
    if forecast == 0:
        return "ZERO_BASE"
    if forecast < 0 < actual:
        return "LOSS_TO_PROFIT"
    if forecast > 0 > actual:
        return "PROFIT_TO_LOSS"
    if forecast * actual < 0:
        return "SIGN_CHANGE"
    return None


def calculate_mape(ape_values: Iterable[Optional[float]]) -> Optional[float]:
    """Mean APE over valid, non-regime observations."""
    values = [value for value in ape_values if value is not None]
    if not values:
        return None
    return mean(values)


def calculate_bias(percentage_errors: Iterable[Optional[float]]) -> Optional[float]:
    """Signed mean percentage error; positive means under-forecast."""
    values = [value for value in percentage_errors if value is not None]
    if not values:
        return None
    return mean(values)


def observation_confidence(count: int) -> str:
    if count < 5:
        return "INSUFFICIENT_DATA"
    if count <= 7:
        return "LOW_CONFIDENCE"
    if count <= 11:
        return "MODERATE_CONFIDENCE"
    return "ADEQUATE"


def accuracy_score_from_mape(mape: Optional[float], perfect_mape: float = 0.0, poor_mape: float = 50.0) -> float:
    """Versioned-friendly linear MAPE mapping; parameters belong to the model version."""
    if mape is None:
        return 0.0
    if poor_mape <= perfect_mape:
        raise ValueError("poor_mape must be greater than perfect_mape")
    score = 100.0 * (poor_mape - mape) / (poor_mape - perfect_mape)
    return max(0.0, min(100.0, score))


def bias_score(bias: Optional[float], zero_bias: float = 0.0, unacceptable_bias: float = 25.0) -> float:
    """Versioned-friendly score for bias magnitude; direction is retained separately."""
    if bias is None:
        return 0.0
    if unacceptable_bias <= zero_bias:
        raise ValueError("unacceptable_bias must be greater than zero_bias")
    magnitude = abs(bias)
    score = 100.0 * (unacceptable_bias - magnitude) / (unacceptable_bias - zero_bias)
    return max(0.0, min(100.0, score))


def baseline_advantage_score(improvement: Optional[float], neutral: float = 0.0, full_advantage: float = 50.0) -> float:
    """Map relative model-vs-baseline improvement to 0-100."""
    if improvement is None:
        return 0.0
    if full_advantage <= neutral:
        raise ValueError("full_advantage must be greater than neutral")
    score = 50.0 + 50.0 * (improvement - neutral) / full_advantage
    return max(0.0, min(100.0, score))


def confidence_multiplier(status: str) -> float:
    return {
        "INSUFFICIENT_DATA": 0.0,
        "LOW_CONFIDENCE": 0.60,
        "MODERATE_CONFIDENCE": 0.80,
        "ADEQUATE": 1.00,
    }.get(status, 0.0)


def detect_persistent_bias(
    percentage_errors: Iterable[Optional[float]],
    minimum_observations: int = 5,
    bias_threshold: float = 5.0,
) -> str:
    """Detect repeatable bias only after the Stage 6 minimum evidence threshold."""
    values = [value for value in percentage_errors if value is not None]
    if len(values) < minimum_observations:
        return "NEUTRAL"
    average = mean(values)
    if average > bias_threshold:
        return "UNDER_FORECAST_BIAS"
    if average < -bias_threshold:
        return "OVER_FORECAST_BIAS"
    return "NEUTRAL"


def calculate_relative_improvement(baseline_error: Optional[float], model_error: Optional[float]) -> Optional[float]:
    if baseline_error is None or model_error is None or baseline_error == 0:
        return None
    return (baseline_error - model_error) / baseline_error


def is_underperforming_baseline(
    model_mape: Optional[float],
    baseline_mape: Optional[float],
    persistent: bool = True,
) -> bool:
    if not persistent or model_mape is None or baseline_mape is None:
        return False
    return model_mape > baseline_mape


# Backward-compatible alias retained for callers using the old name.
def calculate_pe(forecast: float, actual: float) -> Optional[float]:
    return calculate_percentage_error(forecast, actual)
