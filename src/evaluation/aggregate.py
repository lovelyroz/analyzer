"""Stage 6 Prompt 19 layer, Prompt 25 (Part B)-authorized — evaluation metrics
(spec Sections 6-18, AUTHORITATIVE only).

Consumes P18 ``EvaluationObservation`` carriers and computes the authorized
metrics: Error, Percentage Error, APE, MAPE, Bias, observation sufficiency,
and the Section 17 baseline *comparison* from caller-supplied baseline values.

Exact formulas (spec Sections 6-10, 14, 17):

* ``Error = Actual - Forecast`` (positive = under-forecast).
* ``Percentage Error = (Actual - Forecast) / abs(Forecast) x 100``.
* ``APE = abs(Actual - Forecast) / abs(Forecast) x 100``.
* ``MAPE = mean of valid APE observations only``.
* ``Bias = mean signed percentage error`` (positive = under-forecast).
* Sufficiency bands: <5 INSUFFICIENT_DATA; 5-7 LOW_CONFIDENCE;
  8-11 MODERATE_CONFIDENCE; >=12 ADEQUATE — applied to the scored count.
* ``Improvement = (Baseline Error - Model Error) / Baseline Error``.

Deliberately absent (P17 UNRESOLVED — implement only the authorized
portions, report the rest):

* Seasonal Naive value construction — no seasonal period, formula, required
  history, insufficient-history behavior, or fallback has methodology
  authority (blocker B1). Baseline *comparison* mechanics are implemented;
  baseline *values* arrive from the caller that owns that authority.
* MODEL_UNDERPERFORMS_BASELINE persistence flag — "persistently" has no
  threshold (blocker B8). ``relative_improvement`` is reported; no flag set.
* Per-state data-quality participation (blocker B6) — RESOLVED by Stage 6
  Prompt 25 (Part A): ``is_scoring_eligible`` in schema.py (single source of
  truth; ``PARTICIPATING_QUALITY_STATES`` =
  VALID/ESTIMATED/RESTATED, ``QUARANTINED_QUALITY_STATES`` =
  MISSING/SUSPICIOUS/UNMAPPED) decides. ESTIMATED / RESTATED score fully
  (Error, APE, MAPE, Bias, sufficiency, baseline) per the scoring-layer
  precedent, flagged downstream via ``limited_quality``; MISSING /
  SUSPICIOUS / UNMAPPED are quarantined as
  ``DATA_QUALITY_QUARANTINED:<state>``, whatever their value: spec §41
  forbids an invalid Actual entering MAPE/Bias like a valid one. States
  travel verbatim for audit (``ScoredObservation.data_quality_state``); the
  quarantine tally names them.
* Duplicate preference (blocker B9) — FAIL-CLOSED and P25-authorized: every
  observation sharing a duplicate key is quarantined wholesale
  (``DUPLICATE_QUARANTINED``); none is preferred, dropped, or merged
  silently. Scenario is part of the observation identity (Part A 7-tuple),
  so only same-scenario keys collide; series grouping stays scenario-free
  per spec §14 (SeriesKey = company, metric, horizon, version — spec §14
  defines series without scenario and §37 keeps ONE Reliability beside
  three scenario tracks).
* Zero-Actual scoring — P25-authorized: ``Actual=0 / Forecast!=0`` scores
  normally through the authorized formulas (``Error = Actual - Forecast``,
  PE/APE over ``|Forecast|``) because ``metrics.py`` already handles it
  correctly: ``classify_regime(f != 0, 0)`` is None since ``f*a = 0`` is not
  ``< 0``, so no regime fires and percentage metrics are valid. No
  ``metrics.py`` change was needed. ``F=0 / A=0`` and ``F=0 / A!=0`` stay
  ``ZERO_BASE`` (``forecast == 0``); NULL actuals still quarantine as
  ``MISSING_VALUE`` (NULL != 0, never coerced).
* B1 (Seasonal Naive construction) and B8 (persistence flag) stay
  UNRESOLVED. Reliability / Calibration — forbidden here (Prompts 20+ own them).
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Mapping, Optional, Tuple

from src.evaluation.metrics import (
    calculate_ape,
    calculate_bias,
    calculate_error,
    calculate_mape,
    calculate_percentage_error,
    calculate_relative_improvement,
    classify_regime,
    observation_confidence,
)
from src.evaluation.observation import (
    EvaluationKey,
    EvaluationObservation,
    flag_duplicates,
)
from src.evaluation.schema import is_scoring_eligible

# Series grouping per spec Section 14: Company + Metric + Horizon + Version.
SeriesKey = Tuple[int, str, str, str]


@dataclass
class ScoredObservation:
    """One P18 observation with its authorized error metrics attached.

    ``scored=False`` means quarantined: the observation carries its values
    for audit but contributes nothing to MAPE, Bias, band counts, or baseline
    aggregates. ``exclusion_reason`` names why (a status, a regime, or a
    quarantine cause) so the aggregate can tally it without inventing
    silently-dropped observations.
    """

    key: EvaluationKey
    forecast_value: Optional[float]
    actual_value: Optional[float]
    error: Optional[float]
    percentage_error: Optional[float]
    ape: Optional[float]
    regime: Optional[str]
    baseline_value: Optional[float]
    baseline_error: Optional[float]
    baseline_ape: Optional[float]
    scored: bool
    exclusion_reason: Optional[str] = None
    # Stage 6 Prompt 25 (Part B): verbatim §41 state of the attached Actual
    # (None when unbound). Scored ESTIMATED / RESTATED observations keep
    # their state here for audit; quarantined ones do too.
    data_quality_state: Optional[str] = None


def _quarantined(
    observation: EvaluationObservation,
    reason: str,
    baseline_value: Optional[float] = None,
) -> ScoredObservation:
    actual = observation.actual
    return ScoredObservation(
        key=observation.key,
        forecast_value=observation.forecast_value,
        actual_value=observation.actual_value,
        error=None,
        percentage_error=None,
        ape=None,
        regime=None,
        baseline_value=baseline_value,
        baseline_error=None,
        baseline_ape=None,
        scored=False,
        exclusion_reason=reason,
        data_quality_state=actual.data_quality_state if actual is not None else None,
    )


def score_observation(
    observation: EvaluationObservation,
    baseline_value: Optional[float] = None,
) -> ScoredObservation:
    """Attach authorized error metrics to one P18 observation.

    Percentage metrics are None (not zero) wherever the spec declares them
    invalid; absolute error is always retained for numeric pairs. A missing
    baseline value yields missing baseline metrics — never an invented
    fallback value.
    """
    if observation.evaluation_status != "READY":
        return _quarantined(observation, observation.evaluation_status, baseline_value)
    if observation.duplicate_key is not None:
        return _quarantined(observation, "DUPLICATE_QUARANTINED", baseline_value)

    # Stage 6 Prompt 25 (Part B): single source of truth — the Part A
    # ``is_scoring_eligible`` predicate (PARTICIPATING_QUALITY_STATES).
    # Order: non-READY (covers INVALID_REPORT_VERSION verbatim) → duplicate
    # → eligibility → MISSING_VALUE on None forecast/actual (NULL != 0) →
    # regime scoring. Zero-Actual (Actual=0 / Forecast!=0) scores normally:
    # P25-authorized since classify_regime(f != 0, 0) is None (f*a = 0 is
    # not < 0) and PE/APE over |Forecast| are valid there.
    if observation.actual is not None and not is_scoring_eligible(observation.actual):
        return _quarantined(
            observation,
            f"DATA_QUALITY_QUARANTINED:{observation.actual.data_quality_state}",
            baseline_value,
        )

    forecast = observation.forecast_value
    actual = observation.actual_value
    if forecast is None or actual is None:
        return _quarantined(observation, "MISSING_VALUE", baseline_value)

    regime = classify_regime(forecast, actual)
    error = calculate_error(forecast, actual)
    if regime is not None:
        percentage_error: Optional[float] = None
        ape: Optional[float] = None
    else:
        percentage_error = calculate_percentage_error(forecast, actual)
        ape = calculate_ape(forecast, actual)

    baseline_error: Optional[float] = None
    baseline_ape: Optional[float] = None
    if baseline_value is not None:
        baseline_error = calculate_error(baseline_value, actual)
        if regime is None:
            baseline_ape = calculate_ape(baseline_value, actual)

    attached = observation.actual
    state = attached.data_quality_state if attached is not None else None
    if regime is not None:
        return ScoredObservation(
            key=observation.key,
            forecast_value=forecast,
            actual_value=actual,
            error=error,
            percentage_error=None,
            ape=None,
            regime=regime,
            baseline_value=baseline_value,
            baseline_error=baseline_error,
            baseline_ape=None,
            scored=False,
            exclusion_reason=regime,
            data_quality_state=state,
        )
    return ScoredObservation(
        key=observation.key,
        forecast_value=forecast,
        actual_value=actual,
        error=error,
        percentage_error=percentage_error,
        ape=ape,
        regime=None,
        baseline_value=baseline_value,
        baseline_error=baseline_error,
        baseline_ape=baseline_ape,
        scored=True,
        data_quality_state=state,
    )


@dataclass
class SeriesEvaluation:
    """Authorized aggregates for one Company + Metric + Horizon + Version series.

    ``observation_count`` is the scored count that drives the sufficiency
    band; ``total_observations`` and ``quarantined`` preserve everything else
    for audit. No Reliability, no Calibration, no underperformance flag —
    those belong to later prompts or lack authority (B8).
    """

    company_id: int
    metric_code: str
    horizon: str
    model_version: str
    observation_count: int
    total_observations: int
    quarantined: Dict[str, int] = field(default_factory=dict)
    mape: Optional[float] = None
    bias: Optional[float] = None
    confidence_level: str = "INSUFFICIENT_DATA"
    baseline_mape: Optional[float] = None
    relative_improvement: Optional[float] = None
    observations: List[ScoredObservation] = field(default_factory=list)
    # Stage 6 Prompt 25 (Part B): True when any scored observation carries
    # ESTIMATED / RESTATED quality — they score fully per the scoring-layer
    # precedent but the series is flagged as limited quality for audit.
    limited_quality: bool = False
    evaluation_timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


def _series_key_for(key: EvaluationKey) -> SeriesKey:
    return (key.company_id, key.metric_code, key.forecast_horizon, key.model_version)


def aggregate_series(
    company_id: int,
    metric_code: str,
    horizon: str,
    model_version: str,
    scored: List[ScoredObservation],
) -> SeriesEvaluation:
    """Aggregate one isolated series from its scored observations."""
    valid = [item for item in scored if item.scored]
    mape = calculate_mape([item.ape for item in valid])
    bias = calculate_bias([item.percentage_error for item in valid])
    count = len(valid)
    baseline_apes = [
        item.baseline_ape for item in valid if item.baseline_ape is not None
    ]
    baseline_mape = calculate_mape(baseline_apes) if baseline_apes else None
    improvement = calculate_relative_improvement(baseline_mape, mape)
    quarantined = dict(
        Counter(item.exclusion_reason for item in scored if not item.scored)
    )
    limited = any(
        item.scored and item.data_quality_state in ("ESTIMATED", "RESTATED")
        for item in scored
    )
    return SeriesEvaluation(
        company_id=company_id,
        metric_code=metric_code,
        horizon=horizon,
        model_version=model_version,
        observation_count=count,
        total_observations=len(scored),
        quarantined=quarantined,
        mape=mape,
        bias=bias,
        confidence_level=observation_confidence(count),
        baseline_mape=baseline_mape,
        relative_improvement=improvement,
        observations=list(scored),
        limited_quality=limited,
    )


def aggregate_observations(
    observations: List[EvaluationObservation],
    baselines: Optional[Mapping[tuple, Optional[float]]] = None,
) -> Dict[SeriesKey, SeriesEvaluation]:
    """Score P18 observations and aggregate each isolated series.

    ``baselines`` maps ``EvaluationKey.as_tuple()`` to the caller-supplied
    baseline value for that forecast (blocker B1: this layer never constructs
    a Seasonal Naive value). Horizons and model versions are grouped, never
    mixed; duplicates are flagged by the P18 helper and quarantined wholesale.
    """
    supplied = dict(baselines or {})
    flagged = flag_duplicates(list(observations))
    scored = [
        score_observation(item, supplied.get(item.key.as_tuple()))
        for item in flagged
    ]
    groups: Dict[SeriesKey, List[ScoredObservation]] = {}
    for item in scored:
        series = _series_key_for(item.key)
        groups.setdefault(series, []).append(item)
    return {
        (company_id, metric_code, horizon, model_version): aggregate_series(
            company_id, metric_code, horizon, model_version, items
        )
        for (company_id, metric_code, horizon, model_version), items in groups.items()
    }
