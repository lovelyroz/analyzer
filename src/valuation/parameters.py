from typing import Dict, Tuple

# Backward-compatible export retained for existing package consumers.
# Stage 7 V1 no longer uses hard-coded industry target P/E values; target multiples
# come from the benchmark hierarchy and explicit, evidence-backed scenario inputs.
INDUSTRY_TARGET_PE: Dict[str, float] = {}

SCENARIO_WEIGHTS: Dict[str, float] = {
    "bear": 0.20,
    "base": 0.60,
    "bull": 0.20,
}

# Backward-compatible neutral export. V1 intentionally does not use arbitrary
# 0.9/1.0/1.1 scenario gaps; absent explicit economic evidence, all scenarios
# use the benchmark multiple unchanged.
SCENARIO_PE_MULTIPLIER: Dict[str, float] = {
    "bear": 1.00,
    "base": 1.00,
    "bull": 1.00,
}

# Scenario probabilities are built from four family-level evidence distributions.
# Each family receives one vote; correlated metrics must be aggregated before this
# contract. The blend is versioned and backtestable rather than an architecture constant.
PROBABILITY_EVIDENCE_FAMILIES: Tuple[str, ...] = (
    "FUNDAMENTAL_DIRECTION",
    "FORECAST_DIRECTION",
    "PROFITABILITY_ASSUMPTION_RISK",
    "DATA_STRUCTURAL_RISK",
)
PROBABILITY_EVIDENCE_BLEND = 0.25

# V1 does not impose an arbitrary Bear/Base/Bull P/E gap. With no explicit
# economic evidence, all scenarios use the same benchmark multiple. Scenario-
# specific multiple changes must be supplied with an economic rationale and are
# bounded so the mechanism remains explainable, versioned and backtestable.
SCENARIO_MULTIPLE_MAX_ABS_ADJUSTMENT = 0.20
SCENARIO_MULTIPLE_POLICY_VERSION = "STAGE7_V1_EVIDENCE_BACKED"

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
