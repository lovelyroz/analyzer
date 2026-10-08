from __future__ import annotations

from statistics import mean
from typing import Iterable, Optional


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
    """Mean absolute percentage error over valid APE observations.

    The public helper accepts APE values, so each supplied observation is
    normalized to its absolute magnitude before averaging. This prevents a
    signed percentage-error value from accidentally cancelling a true APE.
    Regime-invalid observations are represented by None upstream.
    """
    values = [abs(value) for value in ape_values if value is not None and _valid_number(value)]
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


def calculate_relative_improvement(baseline_error: Optional[float], model_error: Optional[float]) -> Optional[float]:
    if baseline_error is None or model_error is None or baseline_error == 0:
        return None
    return (baseline_error - model_error) / baseline_error


# Backward-compatible alias retained for callers using the old name.
def calculate_pe(forecast: float, actual: float) -> Optional[float]:
    return calculate_percentage_error(forecast, actual)
