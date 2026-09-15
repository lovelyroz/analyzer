from typing import Dict

# Backward-compatible export retained for existing package consumers.
# Stage 7 V1 no longer uses hard-coded industry target P/E values; target multiples
# come from the benchmark hierarchy and versioned scenario parameters.
INDUSTRY_TARGET_PE: Dict[str, float] = {}

SCENARIO_WEIGHTS: Dict[str, float] = {
    "bear": 0.20,
    "base": 0.60,
    "bull": 0.20,
}

# Versioned scenario multiple parameters. They do not use Fundamental Score or
# Forecast Reliability and are intended to be backtested/calibrated later.
SCENARIO_PE_MULTIPLIER: Dict[str, float] = {
    "bear": 0.90,
    "base": 1.00,
    "bull": 1.10,
}

VALUATION_THRESHOLDS: Dict[str, float] = {
    "very_attractive_expected_upside": 30.0,
    "very_attractive_base_upside": 15.0,
    "attractive_expected_upside": 15.0,
    "attractive_base_upside": 5.0,
    "expensive_expected_upside": -10.0,
    "very_expensive_expected_upside": -25.0,
    "very_expensive_base_upside": -10.0,
}

CONFIDENCE_THRESHOLDS: Dict[str, float] = {
    "very_high": 90.0,
    "high": 75.0,
    "moderate": 60.0,
    "low": 40.0,
}

RISK_THRESHOLDS: Dict[str, float] = {
    "extreme_confidence": 40.0,
    "high_scenario_dispersion": 0.50,
    "high_bear_downside": -30.0,
    "medium_confidence": 60.0,
    "medium_bear_downside": -15.0,
}

ALERT_THRESHOLDS: Dict[str, float] = {
    "high_scenario_dispersion": 0.50,
    "low_forecast_reliability": 40.0,
    "benchmark_divergence_ratio": 1.50,
    "historical_divergence_ratio": 1.50,
    "industry_divergence_ratio": 1.50,
    "high_dependence_share": 0.60,
}

# One-at-a-time sensitivity shock for V1 driver impact calculations.
SENSITIVITY_PERTURBATION = 0.10

MIN_INDUSTRY_PEERS = 8
MODEL_VERSION = "STAGE7_V1"
CONTRACT_VERSION = "VALUATION_CONTRACT_V1"
