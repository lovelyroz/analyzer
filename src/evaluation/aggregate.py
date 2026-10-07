"""Stage 6 Prompt 19 — evaluation metrics layer (spec Sections 6-18, AUTHORITATIVE only).

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

Deliberately absent (P17 UNRESOLVED, P19 precondition — implement only the
authorized portions, report the rest):

* Seasonal Naive value construction — no seasonal period, formula, required
  history, insufficient-history behavior, or fallback has methodology
  authority (blocker B1). Baseline *comparison* mechanics are implemented;
  baseline *values* arrive from the caller that owns that authority.
* MODEL_UNDERPERFORMS_BASELINE persistence flag — "persistently" has no
  threshold (blocker B8). ``relative_improvement`` is reported; no flag set.
* Data-quality participation rules (blocker B6) — only ``VALID`` Actuals
  score. Every other §41 state is quarantined as
  ``DATA_QUALITY_QUARANTINED:<state>``, whatever its value: spec §41
  forbids an invalid Actual entering MAPE/Bias like a valid one, and no
  per-state participation rule has authority, so the conservative refusal
  to score is the only non-inventive option. States travel verbatim for
  audit; the quarantine tally names them.
* Duplicate preference (blocker B9) — every observation sharing a duplicate
  key is quarantined; none is preferred, dropped, or merged silently.
* Reliability / Calibration — forbidden by P19 (Prompts 20+ own them).
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


def _quarantined(
    observation: EvaluationObservation,
    reason: str,
    baseline_value: Optional[float] = None,
) -> ScoredObservation:
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

    if observation.actual is not None and observation.actual.data_quality_state != "VALID":
        return _quarantined(
            observation,
            f"DATA_QUALITY_QUARANTINED:{observation.actual.data_quality_state}",
            baseline_value,
        )

    forecast = observation.forecast_value
    actual = observation.actual_value
    if forecast is None or actual is None:
        return _quarantined(observation, "MISSING_VALUE", baseline_value)
    if forecast != 0 and actual == 0:
        # P17 §B leaves Actual=0 / Forecast!=0 UNRESOLVED: the spec names
        # only Forecast=0 regimes, so scoring APE=100% here would invent
        # methodology. Quarantine and report instead.
        return _quarantined(observation, "ZERO_ACTUAL_UNRESOLVED", baseline_value)

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
