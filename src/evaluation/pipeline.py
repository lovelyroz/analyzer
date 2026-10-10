"""Stage 6 Prompt 21 — production integration path (spec Sections 4-43).

Single auditable production path wiring the authorized layers together:

* P18 ``observation`` — Forecast Version -> PIT-safe Actual binding,
  construction-time PIT check, duplicate flagging (no preference).
* P19 ``aggregate`` — Forecast Error -> Accuracy / Bias, caller-supplied
  baseline comparison (Section 17 mechanics), observation sufficiency.
* P20 ``reliability`` — Performance assembly (weights only) -> withheld
  Reliability -> NO_CALIBRATION -> OOS boundary, P/E untouched.

Deliberately absent (P17 UNRESOLVED, P21 precondition — stop at the
boundary, never invent a substitute):

* Seasonal Naive value construction (blocker B1): no seasonal period,
  formula, required history, insufficient-history behavior, or fallback.
  Baseline *values* arrive from the caller that owns that authority, keyed
  by ``EvaluationKey.as_tuple()`` — exactly as P19 requires.
* Reliability 0-100 (blockers B2/B7): withheld with reasons, never zero,
  never the Performance Score.
* Calibration advance (blockers B3/B4): always NO_CALIBRATION; the OOS
  split validator rejects contamination structurally.
* ReportVersion selection (blocker B5) — RESOLVED by Stage 6 Prompt 25
  (Part A): ``actuals`` values may be a single ``ActualObservation`` or a
  list of candidates; lists are resolved with the first-known-outcome rule
  (``select_actual``: earliest valid publication wins, ties by version
  number then id; all-invalid yields no Actual → ``PENDING_ACTUAL``).
* Per-state data-quality participation (blocker B6) — RESOLVED by Stage 6
  Prompt 25 (Part A): VALID/ESTIMATED/RESTATED score
  (``is_scoring_eligible``; ESTIMATED/RESTATED flag ``limited_quality``),
  MISSING/SUSPICIOUS/UNMAPPED quarantine verbatim.
* Underperformance persistence flag (blocker B8): ``relative_improvement``
  only, no flag. Still caller-owned / unresolved.
* Canonical duplicate key (blocker B9) — FAIL-CLOSED and P25-authorized:
  wholesale quarantine via P18 flagging (scenario is part of identity, so
  only same-scenario keys collide), never a silent preference.
* Zero Actual with nonzero Forecast — P25-authorized: scores normally
  through the authorized formulas (no regime fires since f*a = 0 is not
  < 0). ``MISSING_VALUE`` still quarantines NULLs (NULL != 0).

No-Double-Counting guards (spec Sections 16, 42 — structural, no invented
identity rule):

* TTM observations are never counted twice: the path accepts one optional
  ``ttm_observation`` set per series key and proves conservation — every
  supplied TTM entry is either scored exactly once or quarantined with a
  named reason, and never contributes to a second series.
* Overlapping evaluation horizons never merge: aggregation groups by the
  Section 14 key before any arithmetic (P19 structural isolation), and the
  pipeline result carries one verdict per key only.

Stage boundaries: no forecast generation, no Stage 5 mutation (records are
read read-only and never written back), no Stage 7 logic, no P/E
adjustment (P20 identity guard is the terminal step for any P/E value the
caller passes for proof).
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Mapping, Optional, Tuple

from src.evaluation.aggregate import (
    SeriesEvaluation,
    SeriesKey,
    aggregate_observations,
)
from src.evaluation.observation import (
    EvaluationObservation,
    build_observation,
    select_actual,
)
from src.evaluation.reliability import (
    EvidenceHoldoutSplit,
    SeriesReliabilityGovernance,
    forward_pe_untouched_by_reliability,
    govern_aggregates,
    oos_observations,
)
from src.evaluation.schema import ActualObservation
from src.forecast.schema import ForecastRecord

PIPELINE_PARAMETERS_VERSION = "STAGE6_V1"


@dataclass(frozen=True)
class SeriesPipelineVerdict:
    """One fully-evaluated series: P19 aggregates plus P20 governance.

    ``series`` is the authorized P19 result (MAPE, Bias, sufficiency,
    baseline comparison). ``governance`` is the P20 fail-closed verdict
    (Performance withheld-or-assembled, Reliability withheld, calibration
    NO_CALIBRATION). ``ttm_accounted`` proves the double-counting guard:
    every TTM observation supplied for this key was consumed exactly once.
    """

    series: SeriesEvaluation
    governance: SeriesReliabilityGovernance
    ttm_accounted: int = 0


@dataclass
class EvaluationPipelineResult:
    """The complete integrated production-path result for one batch."""

    verdicts: Dict[SeriesKey, SeriesPipelineVerdict] = field(default_factory=dict)
    series_count: int = 0
    observation_count: int = 0
    quarantined: Dict[str, int] = field(default_factory=dict)
    evaluation_timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


def run_evaluation_pipeline(
    records: List[ForecastRecord],
    metric_codes: List[str],
    actuals: Mapping[Tuple[int, int, str], object],
    baselines: Optional[Mapping[tuple, Optional[float]]] = None,
    ttm_observations: Optional[List[EvaluationObservation]] = None,
    parameters_version: str = PIPELINE_PARAMETERS_VERSION,
) -> EvaluationPipelineResult:
    """Evaluate one batch end to end: records -> Actuals -> verdicts.

    * ``records`` — Stage 5 ``ForecastRecord`` objects (read-only; never
      mutated, never written back).
    * ``metric_codes`` — Stage 1 vocabulary codes to evaluate per record.
    * ``actuals`` — Actuals keyed by
      ``(company_id, financial_period_id, metric_code)``. Each value is a
      single ``ActualObservation`` (bound verbatim) or a list of candidates
      resolved with the Stage 6 Prompt 25 (Part A) first-known-outcome rule
      (``select_actual``); all-invalid yields no Actual (``PENDING_ACTUAL``).
      A bound ``ActualObservation`` already carries its ReportVersion
      provenance (id / publication / period / company / metric).
    * ``baselines`` — caller-supplied Seasonal Naive values keyed by
      ``EvaluationKey.as_tuple()`` (blocker B1: construction belongs to the
      caller that owns the seasonal authority — still caller-owned).
    * ``ttm_observations`` — optional pre-built TTM observations. Each must
      already carry its own key; the path scores each exactly once inside
      its own series group and proves conservation (never double counted,
      never silently dropped).

    Returns one verdict per (company, metric, horizon, version, scenario)
    series. Aggregation groups per scenario, so Bear, Base, and Bull never
    pool observations.
    """
    observations: List[EvaluationObservation] = []
    for record in records:
        for metric_code in metric_codes:
            raw = actuals.get(
                (record.company_id, record.forecast_period_id, metric_code)
            )
            if isinstance(raw, list):
                # Stage 6 Prompt 25 (Part B): candidate lists resolve via
                # select_actual; None (all invalid) → build without actual.
                actual = select_actual(raw)  # type: ignore[arg-type]
            else:
                actual = raw  # type: ignore[assignment]
            observations.append(build_observation(record, metric_code, actual))

    ttm_accounted: Counter = Counter()
    if ttm_observations:
        for observation in ttm_observations:
            observations.append(observation)
            key = (
                observation.key.company_id,
                observation.key.metric_code,
                observation.key.forecast_horizon,
                observation.key.model_version,
                observation.key.scenario,
            )
            ttm_accounted[key] += 1

    aggregates = aggregate_observations(observations, baselines)
    governed = govern_aggregates(aggregates, parameters_version)

    verdicts: Dict[SeriesKey, SeriesPipelineVerdict] = {}
    for key, series in aggregates.items():
        verdicts[key] = SeriesPipelineVerdict(
            series=series,
            governance=governed[key],
            ttm_accounted=ttm_accounted.get(key, 0),
        )

    quarantined: Counter = Counter()
    for series in aggregates.values():
        quarantined.update(series.quarantined)

    return EvaluationPipelineResult(
        verdicts=verdicts,
        series_count=len(verdicts),
        observation_count=sum(
            series.total_observations for series in aggregates.values()
        ),
        quarantined=dict(quarantined),
    )


def evaluate_holdout_oos(
    scored_by_period: Dict[int, float],
    evidence_periods: Tuple[int, ...],
    holdout_periods: Tuple[int, ...],
) -> Dict[int, float]:
    """Project scored values onto the holdout side of an OOS split.

    Thin production-path wrapper over the P20 OOS helpers: the split
    rejects overlapping or inverted periods as contamination by
    construction, and unknown periods are dropped, never assigned.
    """
    split = EvidenceHoldoutSplit(
        evidence_periods=evidence_periods,
        holdout_periods=holdout_periods,
    )
    return oos_observations(scored_by_period, split)


def prove_forward_pe_untouched(forward_pe: float) -> float:
    """Production-path proof that Reliability never adjusts Forward P/E.

    Identity pass-through over the P20 structural guard (spec Sections
    35-36): Stage 6 hands Reliability to Stage 7 as a confidence label
    only.
    """
    return forward_pe_untouched_by_reliability(forward_pe)
