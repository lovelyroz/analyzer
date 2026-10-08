"""Stage 6 Prompt 20 — Reliability + Calibration governance (spec Sections 19-36).

Fail-closed governance layer. P17 classified every Reliability mapping
threshold (B2: MAPE->Score, Bias->Score, Advantage->Score, Confidence
Adjustment), the unavailable-component rule (B7), the persistence definition
(B3), and the candidate->calibrated transition (B4) as UNRESOLVED
METHODOLOGY AUTHORITY — and no later decision has resolved them. P20's own
testing requirement forbids writing numeric expected values for B2/B7/B3/B4
while they remain unresolved: the required behavior is fail-closed plus an
explicit report of the missing authority.

What this module DOES implement (all AUTHORITATIVE):

* Performance Score assembly from caller-supplied versioned component
  scores, with the spec Section 21 weights 50% / 20% / 30% (P17 section E:
  weights are AUTHORITATIVE; mappings are not). The three component scores
  arrive from whoever owns the mapping authority — this layer multiplies
  but never maps.
* The Architecture invariant that Performance Score != Reliability: the two
  are distinct types. A Performance Score can never be read as a
  Reliability, so no caller can silently equate them.
* Calibration state machine restricted to NO_CALIBRATION: any transition
  toward CANDIDATE or CALIBRATED requires the unresolved B3/B4 authority
  and is refused with the missing-authority reason named.
* Old-version preservation + new-version naming guard: calibration never
  overwrites; a new version name is derived, never assigned in place.
* Training/calibration vs holdout/OOS split validation: a holdout that
  overlaps the evidence period contaminates by construction and is
  rejected; OOS evaluation consumes only post-evidence observations.
* The Section 35/36 invariant: Reliability never numerically adjusts
  Forward P/E. A structural guard documents the refusal point for Stage 7.

What this module REFUSES (fail-closed, with reasons):

* Reliability 0-100 from unresolved mappings (B2) — withheld, never zero.
* Score for unavailable components (B7) — reported missing, never 0.0.
* Confidence Adjustment coefficients (B2) — not applied, never defaulted.
* CANDIDATE/CALIBRATED transitions (B3/B4) — refused until the
  persistence definition and transition rule carry authority.
* Direct forecast scaling ``Forecast x (1 + Bias)`` (Section 31) —
  structurally absent: no function here touches a forecast value.

Parameter versioning (Section 27): every governance decision carries the
``parameters_version`` it was evaluated under. Withheld values carry the
version too — the version names the authority snapshot, and a future
authorized mapping set will arrive as a new version, never as a silent
default inside this one.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional

# Spec Section 21 weights — AUTHORITATIVE (P17 section E). The weights alone
# authorize the assembly; they do NOT authorize the component mappings.
ACCURACY_WEIGHT = 0.50
BIAS_CONTROL_WEIGHT = 0.20
BASELINE_ADVANTAGE_WEIGHT = 0.30

# Calibration states — spec Section 29 names all three, but only
# NO_CALIBRATION has an authorized transition rule today (B3/B4 unresolved).
CALIBRATION_STATES = (
    "NO_CALIBRATION",
    "CALIBRATION_CANDIDATE",
    "CALIBRATED",
)

# Missing-authority reasons — the exact P17 blockers this layer refuses to
# decide. Surfaced verbatim so reports name the decision, not a number.
MISSING_RELIABILITY_MAPPINGS = (
    "B2:MAPE_TO_ACCURACY_SCORE",
    "B2:BIAS_TO_BIAS_CONTROL_SCORE",
    "B2:ADVANTAGE_TO_BASELINE_ADVANTAGE_SCORE",
    "B2:CONFIDENCE_ADJUSTMENT",
)
MISSING_UNAVAILABLE_COMPONENT_RULE = "B7:UNAVAILABLE_COMPONENT_SCORE"
MISSING_PERSISTENCE_DEFINITION = "B3:PERSISTENT_BIAS_DEFINITION"
MISSING_CALIBRATION_TRANSITION = "B4:CANDIDATE_TO_CALIBRATED_TRANSITION"


@dataclass(frozen=True)
class VersionedComponentScores:
    """The three 0-100 component scores, supplied by the mapping authority.

    This layer never derives these from MAPE/Bias/improvement — the mappings
    are unresolved (B2), so construction requires the caller to state which
    parameters version produced each score. Bounds are structural (Section 21:
    all components in 0-100), not methodology.
    """

    accuracy_score: float
    bias_control_score: float
    baseline_advantage_score: float
    parameters_version: str

    def __post_init__(self) -> None:
        for name in (
            "accuracy_score",
            "bias_control_score",
            "baseline_advantage_score",
        ):
            value = getattr(self, name)
            if not 0.0 <= value <= 100.0:
                raise ValueError(f"{name} out of 0-100 bounds: {value!r}")
        if not self.parameters_version:
            raise ValueError("parameters_version must name the mapping authority")


@dataclass(frozen=True)
class PerformanceScore:
    """Assembled Performance Score — distinct type from Reliability.

    Spec Section 20: Performance Score feeds Confidence Adjustment feeds
    Reliability. The types are separate so ``Performance Score = Reliability``
    is a type error, not a silent equation.
    """

    value: float
    parameters_version: str


def assemble_performance_score(
    components: VersionedComponentScores,
) -> PerformanceScore:
    """Combine versioned component scores with the Section 21 weights.

    Only the weighted sum is authorized. No mapping, no clamping beyond the
    structural 0-100 bound, no confidence adjustment (B2 unresolved).
    """
    value = (
        ACCURACY_WEIGHT * components.accuracy_score
        + BIAS_CONTROL_WEIGHT * components.bias_control_score
        + BASELINE_ADVANTAGE_WEIGHT * components.baseline_advantage_score
    )
    return PerformanceScore(
        value=max(0.0, min(100.0, value)),
        parameters_version=components.parameters_version,
    )


@dataclass(frozen=True)
class WithheldReliability:
    """A Reliability that methodology authority does not permit computing.

    ``reliability`` is always None — never 0, never the Performance Score.
    ``withheld_because`` names the exact missing decisions (B2/B7 items), so
    the report carries authority gaps instead of invented numbers.
    """

    reliability: Optional[float] = None
    withheld_because: tuple = ()
    parameters_version: str = ""
    confidence_level: str = "INSUFFICIENT_DATA"


def assess_reliability(
    performance: Optional[PerformanceScore],
    confidence_level: str,
    parameters_version: str,
    unavailable_components: tuple = (),
) -> WithheldReliability:
    """Fail-closed Reliability assessment.

    The Confidence Adjustment coefficients are unresolved (B2), and the
    unavailable-component rule is unresolved (B7). Every branch withholds:
    a missing mapping and a missing component alike yield no number, whether
    or not a Performance Score was assembled upstream. The confidence level
    travels verbatim for audit — it describes the evidence count, not a
    multiplier this layer may apply.
    """
    reasons = list(MISSING_RELIABILITY_MAPPINGS)
    for component in unavailable_components:
        reasons.append(f"UNAVAILABLE:{component}")
    if unavailable_components:
        reasons.append(MISSING_UNAVAILABLE_COMPONENT_RULE)
    return WithheldReliability(
        reliability=None,
        withheld_because=tuple(reasons),
        parameters_version=parameters_version,
        confidence_level=confidence_level,
    )


@dataclass(frozen=True)
class CalibrationAssessment:
    """Calibration state verdict for one Metric + Horizon + Model Version scope.

    Only NO_CALIBRATION is reachable: persistence (B3) and the
    candidate->calibrated transition (B4) are unresolved, so any evidence —
    however suggestive — stays NO_CALIBRATION with the missing authority
    named. The scope travels for audit; the verdict never overwrites.
    """

    metric_code: str
    horizon: str
    model_version: str
    state: str = "NO_CALIBRATION"
    reason: Optional[str] = None
    missing_authority: tuple = ()
    parameters_version: str = ""

    def __post_init__(self) -> None:
        if self.state not in CALIBRATION_STATES:
            raise ValueError(f"unknown calibration state: {self.state!r}")
        if self.state != "NO_CALIBRATION":
            raise ValueError(
                "CALIBRATION_CANDIDATE/CALIBRATED require B3/B4 authority: "
                "use refuse_calibration_transition to record the refusal"
            )


def refuse_calibration_transition(
    metric_code: str,
    horizon: str,
    model_version: str,
    requested_state: str,
    parameters_version: str,
) -> CalibrationAssessment:
    """Record the refusal to enter CANDIDATE or CALIBRATED.

    The requested state is carried in ``reason`` for audit; the verdict
    stays NO_CALIBRATION with B3/B4 named. Single-observation evidence is
    refused here too (spec Section 28/34: never calibrate from one
    observation) — but even multi-observation evidence cannot advance
    without the persistence definition.
    """
    if requested_state not in ("CALIBRATION_CANDIDATE", "CALIBRATED"):
        raise ValueError(f"not a calibration advance: {requested_state!r}")
    return CalibrationAssessment(
        metric_code=metric_code,
        horizon=horizon,
        model_version=model_version,
        state="NO_CALIBRATION",
        reason=f"REFUSED_TRANSITION_TO:{requested_state}",
        missing_authority=(
            MISSING_PERSISTENCE_DEFINITION,
            MISSING_CALIBRATION_TRANSITION,
        ),
        parameters_version=parameters_version,
    )


def derive_calibrated_version_name(
    current_model_version: str,
    assessment: CalibrationAssessment,
) -> Optional[str]:
    """Name the next version — only from an authorized CALIBRATED verdict.

    Since CALIBRATED is unreachable without B3/B4 authority, this always
    returns None today: no new version is minted, and the current version is
    never overwritten (spec Sections 6, 31, 34). The function exists so the
    versioning rule has production-path coverage proving the refusal.
    """
    if assessment.state != "CALIBRATED":
        return None
    if assessment.model_version != current_model_version:
        raise ValueError("assessment scope does not match the version")
    return f"{current_model_version}.CAL1"


@dataclass
class EvidenceHoldoutSplit:
    """Training/calibration vs holdout/OOS period separation (Section 32).

    Periods are opaque ordered identifiers (financial_period_id values); the
    split is valid only when every holdout period sorts after every
    evidence period. Overlap or inversion is contamination by construction
    and is rejected — holdout outcomes must never qualify the calibration
    evaluated on that same holdout.
    """

    evidence_periods: tuple
    holdout_periods: tuple

    def __post_init__(self) -> None:
        overlap = set(self.evidence_periods) & set(self.holdout_periods)
        if overlap:
            raise ValueError(
                f"holdout contaminates evidence periods: {sorted(overlap)!r}"
            )
        if self.evidence_periods and self.holdout_periods:
            if max(self.evidence_periods) >= min(self.holdout_periods):
                raise ValueError(
                    "holdout must be strictly after the evidence period"
                )


def oos_observations(
    scored_by_period: Dict[int, float],
    split: EvidenceHoldoutSplit,
) -> Dict[int, float]:
    """Project observations onto the holdout side of the split.

    Only holdout-period entries pass through; evidence-period entries never
    leak into the OOS evaluation. Unknown periods (in neither side) are
    dropped, not assigned — silent assignment would invent scope.
    """
    holdout = set(split.holdout_periods)
    return {
        period: value
        for period, value in scored_by_period.items()
        if period in holdout
    }


def forward_pe_untouched_by_reliability(forward_pe: float) -> float:
    """Structural guard for spec Sections 35-36.

    Reliability never numerically adjusts Forward P/E: the value passes
    through untouched. Stage 7 consumes Reliability as a confidence label
    only. Any formula of the forbidden family (P/E x Reliability, P/E /
    Reliability, ...) has no function to live in — this identity is the
    production-path proof that none was applied.
    """
    return forward_pe


@dataclass
class SeriesReliabilityGovernance:
    """Governance verdict for one evaluated series (P19 SeriesEvaluation in).

    Consumes the authorized P19 aggregates read-only — MAPE, Bias,
    confidence band, baseline comparison — and attaches the P20
    fail-closed verdicts without recomputing or altering any of them.
    """

    company_id: int
    metric_code: str
    horizon: str
    model_version: str
    observation_count: int
    confidence_level: str
    performance: Optional[PerformanceScore]
    reliability: WithheldReliability
    calibration: CalibrationAssessment
    evaluation_timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


def govern_series(
    series,
    component_scores: Optional[VersionedComponentScores] = None,
    parameters_version: str = "STAGE6_V1",
) -> SeriesReliabilityGovernance:
    """Attach P20 governance to one P19 SeriesEvaluation (read-only in).

    * With caller-supplied versioned components: Performance Score is
      assembled (weights AUTHORITATIVE); Reliability is still withheld
      (mappings B2 unresolved).
    * Without components: both Performance and Reliability are withheld —
      the layer assembles nothing from MAPE/Bias directly, because that
      assembly would BE the unresolved mapping.
    * Calibration is always NO_CALIBRATION (B3/B4 unresolved).
    * The input series is never mutated.
    """
    unavailable = []
    if series.mape is None:
        unavailable.append("MAPE")
    if series.bias is None:
        unavailable.append("BIAS")
    if series.relative_improvement is None:
        unavailable.append("BASELINE_IMPROVEMENT")

    performance: Optional[PerformanceScore] = None
    if component_scores is not None:
        performance = assemble_performance_score(component_scores)
        version = component_scores.parameters_version
    else:
        version = parameters_version
        unavailable.append("VERSIONED_COMPONENT_SCORES")

    reliability = assess_reliability(
        performance,
        series.confidence_level,
        version,
        tuple(unavailable),
    )
    calibration = CalibrationAssessment(
        metric_code=series.metric_code,
        horizon=series.horizon,
        model_version=series.model_version,
        state="NO_CALIBRATION",
        reason="B3_B4_UNRESOLVED",
        missing_authority=(
            MISSING_PERSISTENCE_DEFINITION,
            MISSING_CALIBRATION_TRANSITION,
        ),
        parameters_version=version,
    )
    return SeriesReliabilityGovernance(
        company_id=series.company_id,
        metric_code=series.metric_code,
        horizon=series.horizon,
        model_version=series.model_version,
        observation_count=series.observation_count,
        confidence_level=series.confidence_level,
        performance=performance,
        reliability=reliability,
        calibration=calibration,
    )


def govern_aggregates(
    aggregates,
    parameters_version: str = "STAGE6_V1",
) -> Dict[tuple, SeriesReliabilityGovernance]:
    """Govern every series from ``aggregate_observations`` without components.

    Production-path entry: P18 observations -> P19 aggregates -> P20
    governance. No component scores exist anywhere in that path (mappings
    unresolved), so Performance is withheld for every series and the verdict
    proves the path refuses to invent values end to end.
    """
    return {
        key: govern_series(series, None, parameters_version)
        for key, series in aggregates.items()
    }
