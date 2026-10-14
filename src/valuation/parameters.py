from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional, Tuple

from src.forecast.schema import normalize_datetime

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
    "expensive_base_upside": 0.0,
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

# ---------------------------------------------------------------------------
# P33 — Effective-dated parameter versioning (mechanism only; no policy)
# ---------------------------------------------------------------------------
"""Auditable parameter-version records for Stage 7 V1.

Provided today (verified facts only, no owner decision needed):

* A genesis snapshot built PROGRAMMATICALLY from the live module constants
  above, so recorded values cannot drift from executed values.
* Exact-key resolution (``resolve_parameter_set``): deterministic, with
  explicit errors for missing keys — never a silent fallback to current.
* Date-based selection (``resolve_parameter_set_as_of``) with honest
  semantics: only explicitly dated versions participate; the undated genesis
  record NEVER stands in for history; future-effective versions are never
  selected; overlaps raise instead of picking silently.

Deliberately NOT provided (needs R8/R7 owner decisions):

* ``effective_from`` dates for the existing constants (unknowable from any
  evidence — inventing them is forbidden, so genesis records carry ``None``
  with that meaning recorded explicitly);
* a database-backed registry (no architectural evidence supports one);
* any change to financial values, formulas, or thresholds (every record
  mirrors a live constant; descriptions describe, they do not decide).
"""

GENESIS_VERSION_KEY = "STAGE7_V1/GENESIS"

_UNVERSIONED_GENESIS_NOTE = (
    "Genesis record: temporal validity unknown; never valid "
    "for historical date selection (R8 pending)."
)


@dataclass(frozen=True)
class ParameterRecord:
    parameter_name: str
    parameter_value: object
    effective_from: Optional[datetime]
    description: str


@dataclass(frozen=True)
class ParameterSetVersion:
    model_version: str
    version_key: str
    effective_from: Optional[datetime]
    records: Tuple[ParameterRecord, ...]


def _rec(name: str, value: object, description: str) -> ParameterRecord:
    return ParameterRecord(
        parameter_name=name,
        parameter_value=value,
        effective_from=None,
        description=description + " " + _UNVERSIONED_GENESIS_NOTE,
    )


def _genesis_records() -> Tuple[ParameterRecord, ...]:
    return (
        _rec("SCENARIO_WEIGHTS.bear", SCENARIO_WEIGHTS["bear"], "Bear prior probability weight."),
        _rec("SCENARIO_WEIGHTS.base", SCENARIO_WEIGHTS["base"], "Base prior probability weight."),
        _rec("SCENARIO_WEIGHTS.bull", SCENARIO_WEIGHTS["bull"], "Bull prior probability weight."),
        _rec("SCENARIO_PE_MULTIPLIER.bear", SCENARIO_PE_MULTIPLIER["bear"], "Neutral bear multiple (intentionally 1.00)."),
        _rec("SCENARIO_PE_MULTIPLIER.base", SCENARIO_PE_MULTIPLIER["base"], "Neutral base multiple (intentionally 1.00)."),
        _rec("SCENARIO_PE_MULTIPLIER.bull", SCENARIO_PE_MULTIPLIER["bull"], "Neutral bull multiple (intentionally 1.00)."),
        _rec("PROBABILITY_EVIDENCE_FAMILIES", PROBABILITY_EVIDENCE_FAMILIES, "Family-level evidence channels aggregated before this contract."),
        _rec("PROBABILITY_EVIDENCE_BLEND", PROBABILITY_EVIDENCE_BLEND, "Family-mean blend weight."),
        _rec("SCENARIO_MULTIPLE_MAX_ABS_ADJUSTMENT", SCENARIO_MULTIPLE_MAX_ABS_ADJUSTMENT, "Bound on explicit scenario multiple adjustments."),
        _rec("SCENARIO_MULTIPLE_POLICY_VERSION", SCENARIO_MULTIPLE_POLICY_VERSION, "Scenario-multiple policy identifier."),
        _rec("VALUATION_THRESHOLDS.very_attractive_expected_upside", VALUATION_THRESHOLDS["very_attractive_expected_upside"], "Status band gate; engine constant, spec-unratified (D9)."),
        _rec("VALUATION_THRESHOLDS.very_attractive_base_upside", VALUATION_THRESHOLDS["very_attractive_base_upside"], "Status band gate; engine constant, spec-unratified (D9)."),
        _rec("VALUATION_THRESHOLDS.attractive_expected_upside", VALUATION_THRESHOLDS["attractive_expected_upside"], "Status band gate; engine constant, spec-unratified (D9)."),
        _rec("VALUATION_THRESHOLDS.attractive_base_upside", VALUATION_THRESHOLDS["attractive_base_upside"], "Status band gate; engine constant, spec-unratified (D9)."),
        _rec("VALUATION_THRESHOLDS.expensive_expected_upside", VALUATION_THRESHOLDS["expensive_expected_upside"], "Status band gate; engine constant, spec-unratified (D9)."),
        _rec("VALUATION_THRESHOLDS.expensive_base_upside", VALUATION_THRESHOLDS["expensive_base_upside"], "Status band gate; engine constant, spec-unratified (D9)."),
        _rec("VALUATION_THRESHOLDS.very_expensive_expected_upside", VALUATION_THRESHOLDS["very_expensive_expected_upside"], "Status band gate; engine constant, spec-unratified (D9)."),
        _rec("VALUATION_THRESHOLDS.very_expensive_base_upside", VALUATION_THRESHOLDS["very_expensive_base_upside"], "Status band gate; engine constant, spec-unratified (D9)."),
        _rec("CONFIDENCE_THRESHOLDS.very_high", CONFIDENCE_THRESHOLDS["very_high"], "Confidence label gate; engine constant, spec-unratified (D9)."),
        _rec("CONFIDENCE_THRESHOLDS.high", CONFIDENCE_THRESHOLDS["high"], "Confidence label gate; engine constant, spec-unratified (D9)."),
        _rec("CONFIDENCE_THRESHOLDS.moderate", CONFIDENCE_THRESHOLDS["moderate"], "Confidence label gate; engine constant, spec-unratified (D9)."),
        _rec("CONFIDENCE_THRESHOLDS.low", CONFIDENCE_THRESHOLDS["low"], "Confidence label gate; engine constant, spec-unratified (D9)."),
        _rec("RISK_THRESHOLDS.extreme_confidence", RISK_THRESHOLDS["extreme_confidence"], "Risk grade gate; engine constant, spec-unratified (D9)."),
        _rec("RISK_THRESHOLDS.high_scenario_dispersion", RISK_THRESHOLDS["high_scenario_dispersion"], "Risk grade gate; engine constant, spec-unratified (D9)."),
        _rec("RISK_THRESHOLDS.high_bear_downside", RISK_THRESHOLDS["high_bear_downside"], "Risk grade gate; engine constant, spec-unratified (D9)."),
        _rec("RISK_THRESHOLDS.medium_confidence", RISK_THRESHOLDS["medium_confidence"], "Risk grade gate; engine constant, spec-unratified (D9)."),
        _rec("RISK_THRESHOLDS.medium_bear_downside", RISK_THRESHOLDS["medium_bear_downside"], "Risk grade gate; engine constant, spec-unratified (D9)."),
        _rec("ALERT_THRESHOLDS.high_scenario_dispersion", ALERT_THRESHOLDS["high_scenario_dispersion"], "Alert trigger; engine constant, spec-unratified (D9)."),
        _rec("ALERT_THRESHOLDS.low_forecast_reliability", ALERT_THRESHOLDS["low_forecast_reliability"], "Alert trigger; engine constant, spec-unratified (D9)."),
        _rec("ALERT_THRESHOLDS.benchmark_divergence_ratio", ALERT_THRESHOLDS["benchmark_divergence_ratio"], "Alert trigger; engine constant, spec-unratified (D9)."),
        _rec("ALERT_THRESHOLDS.historical_divergence_ratio", ALERT_THRESHOLDS["historical_divergence_ratio"], "Alert trigger; engine constant, spec-unratified (D9)."),
        _rec("ALERT_THRESHOLDS.industry_divergence_ratio", ALERT_THRESHOLDS["industry_divergence_ratio"], "Alert trigger; engine constant, spec-unratified (D9)."),
        _rec("ALERT_THRESHOLDS.high_dependence_share", ALERT_THRESHOLDS["high_dependence_share"], "Declared but unwired dead definition; must not be activated without D2 (P27)."),
        _rec("SENSITIVITY_PERTURBATION", SENSITIVITY_PERTURBATION, "Driver-impact shock size; not approved for flip detection (P27)."),
        _rec("MIN_INDUSTRY_PEERS", MIN_INDUSTRY_PEERS, "Minimum valid forward peers for industry benchmark selection."),
        _rec("MODEL_VERSION", MODEL_VERSION, "Build identifier stamped on every result; not a registry."),
        _rec("CONTRACT_VERSION", CONTRACT_VERSION, "Contract identifier stamped on every result; not a registry."),
        _rec("INDUSTRY_TARGET_PE", INDUSTRY_TARGET_PE, "Retained empty for backward compatibility; unused in V1."),
    )


GENESIS_VERSION = ParameterSetVersion(
    model_version=MODEL_VERSION,
    version_key=GENESIS_VERSION_KEY,
    effective_from=None,
    records=_genesis_records(),
)


@dataclass(frozen=True)
class ParameterRegistry:
    versions: Tuple[ParameterSetVersion, ...] = (GENESIS_VERSION,)


DEFAULT_REGISTRY = ParameterRegistry()


def resolve_parameter_set(
    version_key: str,
    registry: ParameterRegistry = DEFAULT_REGISTRY,
) -> ParameterSetVersion:
    """Return the exact versioned parameter set for ``version_key``.

    Missing keys raise ``KeyError`` — silently falling back to the current
    version is forbidden, so absence is always explicit and loud.
    """
    for version in registry.versions:
        if version.version_key == version_key:
            return version
    raise KeyError(f"Unknown Stage 7 parameter version: {version_key!r}.")


def resolve_parameter_set_as_of(
    as_of: Optional[datetime],
    registry: ParameterRegistry = DEFAULT_REGISTRY,
) -> ParameterSetVersion:
    """Select the parameter version effective at ``as_of`` — deterministically.

    Only explicitly dated versions participate: a version covers ``as_of``
    when its ``effective_from`` is set and ``<= as_of``; the newest covering
    version wins; future-effective versions never leak in. Undated records
    (including the whole genesis set) never stand in for history, so with
    only genesis registered this ALWAYS raises ``LookupError`` naming the
    missing R8-dated records — a loud, non-silent failure, never a quiet
    fallback to current values. Overlapping effective dates raise ambiguity
    instead of picking silently. ``as_of=None`` raises: selection without an
    as-of instant is undefined and none is invented.
    """
    if as_of is None:
        raise LookupError(
            "Stage 7 parameter as-of selection requires an as-of instant; "
            "refusing to guess one."
        )
    moment = normalize_datetime(as_of)
    candidates = [
        version
        for version in registry.versions
        if version.effective_from is not None
        and normalize_datetime(version.effective_from) <= moment
    ]
    if not candidates:
        raise LookupError(
            f"No dated Stage 7 parameter version covers as_of={moment.isoformat()}; "
            "historical selection requires R8-dated records (genesis is undated "
            "and never stands in for history)."
        )
    best = max(candidates, key=lambda version: normalize_datetime(version.effective_from))
    tied = [v for v in candidates if normalize_datetime(v.effective_from) == normalize_datetime(best.effective_from)]
    if len(tied) > 1:
        raise LookupError(
            "Ambiguous Stage 7 parameter versions for as_of="
            f"{moment.isoformat()}: {[v.version_key for v in tied]}."
        )
    return best
