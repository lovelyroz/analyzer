"""Stage 6 evaluation-data identity: one forecast bound to one Actual (spec §4).

An ``EvaluationObservation`` is a *carrier*, not a decision. It freezes the
Stage 6 §4 mapping key on the forecast side and carries the corresponding
Stage 1 ``ActualObservation`` on the actual side, plus the evaluation status
and timestamp (§39).

What this module does NOT do (deliberately):

* Selection is the Stage 6 Prompt 25 (Part A) first-known-outcome rule
  (``select_actual``): earliest valid publication wins, ties break by
  version number then version id. B5 (P17 §B) is thereby RESOLVED — no
  latest-in-DB hindsight, no caller authority needed.
* Per-state participation is the Stage 6 Prompt 25 (Part A) B6 predicate
  (``is_scoring_eligible`` in schema.py); the observation still records the
  state verbatim and leaves scoring to the evaluation step.
* It never computes error, scores, reliability, calibration, or valuation.
  P18 explicitly forbids MAPE / Bias / Reliability / Calibration / Valuation.

Point-in-Time contract (Stage 6 spec §5 / Rules 9–10):

* An Actual published *after* the forecast cutoff is a legitimate outcome to
  evaluate against. ``bind_actual`` accepts it; Rule 9 governs *inputs*, never
  the outcome Actual.
* PIT leakage — an input available only after the cutoff — is detected here
  and freezes the observation as ``PIT_INVALID_INPUT``.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

from src.evaluation.schema import (
    ActualObservation,
    _normalize_datetime,
    is_valid_report_version,
)
from src.forecast.schema import ForecastRecord

# Evaluation lifecycle states carried by the foundation. ``PENDING_ACTUAL``
# means bound to a forecast whose Actual is not yet attached; ``READY`` means a
# chosen Actual is attached; ``PIT_INVALID_INPUT`` means construction-time PIT
# leakage was detected; ``UNRESOLVED_*`` states mark the two P17 blockers this
# foundation isolates instead of deciding.
EVALUATION_STATUSES = (
    "PENDING_ACTUAL",
    "READY",
    "PIT_INVALID_INPUT",
    "UNRESOLVED_ACTUAL_SELECTION",
    "UNRESOLVED_PARTICIPATION",
    # Stage 6 Prompt 25 (Part A): the attached Actual fails
    # ``is_valid_report_version`` — carried for audit, never scores
    # (aggregation quarantines every non-READY observation).
    "INVALID_REPORT_VERSION",
)


@dataclass(frozen=True)
class EvaluationKey:
    """The Stage 6 §4 mapping key: forecast identity for evaluation.

    Company + Metric + Financial Period + Forecast Horizon + Model Version +
    Forecast Cutoff + Scenario (Stage 6 Prompt 25, Part A). Scenario is
    APPENDED LAST: positions 0–5 are unchanged so existing consumers keep
    their positional reading. Spec §37 keeps ONE Reliability alongside three
    parallel scenario tracks — scenario therefore belongs in the observation
    identity, while series aggregation (Part B) stays scenario-free.
    Two observations share an evaluation series only when every component
    agrees — horizon, model version, and scenario isolate series from each
    other by construction (the P18 horizon-isolation / model-version
    isolation tests pin the first two).
    """

    company_id: int
    metric_code: str
    financial_period_id: int
    forecast_horizon: str
    model_version: str
    forecast_cutoff_datetime: datetime
    scenario: str

    def __post_init__(self) -> None:
        if not self.scenario:
            raise ValueError("scenario is required: missing scenario must not default to BASE")

    def as_tuple(self) -> Tuple[Any, ...]:
        return (
            self.company_id,
            self.metric_code,
            self.financial_period_id,
            self.forecast_horizon,
            self.model_version,
            self.forecast_cutoff_datetime,
            self.scenario,
        )


def evaluation_key_for(
    record: ForecastRecord, metric_code: str
) -> EvaluationKey:
    """Build the Stage 6 §4 key for one Stage 5 record and one metric.

    ``metric_code`` is the Stage 1 vocabulary code (``service.DEFAULT_FACT_*
    ``), not a forecast attribute name: the metric being evaluated is the
    caller's statement, because only Stage 1 owns the metric vocabulary.
    """
    return EvaluationKey(
        company_id=record.company_id,
        metric_code=metric_code,
        financial_period_id=record.forecast_period_id,
        forecast_horizon=record.forecast_horizon,
        model_version=record.model_version,
        forecast_cutoff_datetime=record.data_cutoff_datetime,
        scenario=record.scenario,
    )


def select_actual(
    candidates: List[ActualObservation],
) -> Optional[ActualObservation]:
    """Stage 6 Prompt 25 (Part A): first-known-outcome Actual selection.

    Filters candidates with ``is_valid_report_version`` (spec §4: an Actual
    without a valid ReportVersion is never eligible; the naive latest-in-DB
    is forbidden), then returns the minimum by
    ``(publication_datetime, report_version_number or 0,
    report_version_id)`` — the earliest-published outcome wins, resisting
    restatement hindsight. Same-id ties are the same ReportVersion, so the
    result is deterministic regardless of input order. Returns ``None``
    when no candidate is valid.
    """
    valid = [c for c in candidates if is_valid_report_version(c)]
    if not valid:
        return None
    return min(
        valid,
        key=lambda c: (
            c.publication_datetime,
            c.report_version_number if c.report_version_number is not None else 0,
            c.report_version_id,
        ),
    )


@dataclass
class EvaluationObservation:
    """One forecast frozen together with its corresponding Actual.

    The forecast side is immutable (a Stage 5 ``ForecastRecord`` is itself
    immutable and append-only). The actual side is attached once — either at
    construction or via ``bind_actual`` — with the Actual chosen by the
    Stage 6 Prompt 25 (Part A) first-known-outcome rule (``select_actual``).
    ``bind_actual`` returns a *new* observation rather
    than mutating, so a bound observation is itself append-only.

    Temporal split (Rule 10) is structural: the cutoff/timestamp live on the
    forecast record, the period/publication on the Actual. This object never
    compares a period against a cutoff.
    """

    forecast: ForecastRecord
    metric_code: str
    actual: Optional[ActualObservation] = None
    evaluation_status: str = "PENDING_ACTUAL"
    evaluation_timestamp: Optional[datetime] = None
    input_refs: Tuple[Any, ...] = ()
    duplicate_key: Optional[str] = None

    def __post_init__(self) -> None:
        if self.evaluation_status not in EVALUATION_STATUSES:
            raise ValueError(
                f"unknown evaluation status: {self.evaluation_status!r}"
            )
        self.evaluation_timestamp = _normalize_datetime(self.evaluation_timestamp)
        if self.actual is not None and self.evaluation_status == "PENDING_ACTUAL":
            self.evaluation_status = "READY"

    @property
    def key(self) -> EvaluationKey:
        return evaluation_key_for(self.forecast, self.metric_code)

    @property
    def forecast_value(self) -> Optional[float]:
        """The forecasted value for the evaluated metric, or None if missing.

        Attribute lookup is by Stage 1 code lowered (``REVENUE`` -> ``revenue``,
        ``OPERATING_PROFIT`` -> ``operating_profit`` ...); an unknown code is a
        missing forecast, not zero (NULL != 0).
        """
        return getattr(self.forecast, self.metric_code.lower(), None)

    @property
    def actual_value(self) -> Optional[float]:
        """The Actual value, or None when unbound or genuinely unknown."""
        if self.actual is None:
            return None
        return self.actual.value

    def bind_actual(
        self, actual: ActualObservation, at: Optional[datetime] = None
    ) -> "EvaluationObservation":
        """Attach the caller-selected Actual, returning a new observation.

        No eligibility check on ``publication_datetime`` happens here: an
        Actual published after the cutoff is the outcome being evaluated (PIT
        CONTRACT). Choosing *which* candidate is authoritative is the
        Stage 6 Prompt 25 (Part A) first-known-outcome rule — callers select
        with ``select_actual`` before binding.
        """
        timestamp = _normalize_datetime(at) or datetime.now(timezone.utc)
        return EvaluationObservation(
            forecast=self.forecast,
            metric_code=self.metric_code,
            actual=actual,
            evaluation_status=(
                "READY" if self.evaluation_status == "PENDING_ACTUAL"
                else self.evaluation_status
            ),
            evaluation_timestamp=timestamp,
            input_refs=self.input_refs,
            duplicate_key=self.duplicate_key,
        )


def detect_pit_leakage(
    cutoff: datetime, refs: Tuple[Any, ...]
) -> List[Any]:
    """Inputs knowable only after ``cutoff`` (Stage 6 spec §5 / Rule 9).

    Only *inputs* are inspected — the outcome Actual is never passed here, so
    a later-published Actual can never be misreported as leakage. A ``None``
    ``available_at`` is unknowable provenance, not leakage: it is returned
    separately by ``missing_provenance`` rather than silently passed or
    failed.
    """
    normalized_cutoff = _normalize_datetime(cutoff)
    assert normalized_cutoff is not None
    leaked = []
    for ref in refs:
        available_at = _normalize_datetime(getattr(ref, "available_at", None))
        if available_at is not None and available_at > normalized_cutoff:
            leaked.append(ref)
    return leaked


def missing_provenance(refs: Tuple[Any, ...]) -> List[Any]:
    """Input refs whose ``available_at`` is unknown.

    Kept distinct from ``detect_pit_leakage``: unknown provenance is a data
    gap the caller must resolve, not evidence of leakage and not evidence of
    cleanliness.
    """
    return [ref for ref in refs if getattr(ref, "available_at", None) is None]


def build_observation(
    record: ForecastRecord,
    metric_code: str,
    actual: Optional[ActualObservation] = None,
    evaluation_timestamp: Optional[datetime] = None,
) -> EvaluationObservation:
    """Freeze one record/metric pair into an evaluation observation.

    Runs the construction-time PIT check over the record's own
    ``input_refs``: any input published after the record's cutoff freezes the
    observation as ``PIT_INVALID_INPUT``. The attached Actual — when given —
    is *not* part of that check; instead it is validated with
    ``is_valid_report_version`` (Stage 6 Prompt 25, Part A) — an Actual
    failing it freezes the observation as ``INVALID_REPORT_VERSION``. The
    failed Actual is still carried for audit but never scores, because
    aggregation quarantines every non-READY observation.
    """
    leaked = detect_pit_leakage(record.data_cutoff_datetime, record.input_refs)
    if leaked:
        return EvaluationObservation(
            forecast=record,
            metric_code=metric_code,
            actual=actual,
            evaluation_status="PIT_INVALID_INPUT",
            evaluation_timestamp=evaluation_timestamp,
            input_refs=tuple(record.input_refs),
        )
    if actual is not None and not is_valid_report_version(actual):
        return EvaluationObservation(
            forecast=record,
            metric_code=metric_code,
            actual=actual,
            evaluation_status="INVALID_REPORT_VERSION",
            evaluation_timestamp=evaluation_timestamp,
            input_refs=tuple(record.input_refs),
        )
    observation = EvaluationObservation(
        forecast=record,
        metric_code=metric_code,
        evaluation_status="PENDING_ACTUAL",
        evaluation_timestamp=evaluation_timestamp,
        input_refs=tuple(record.input_refs),
    )
    if actual is not None:
        observation = observation.bind_actual(
            actual, at=evaluation_timestamp
        )
    return observation


def flag_duplicates(
    observations: List[EvaluationObservation],
) -> List[EvaluationObservation]:
    """Mark observations sharing a Stage 6 §4 key with a shared duplicate key.

    P17 blocker B9 leaves the *canonical* duplicate-key definition unresolved,
    so this helper does not drop, merge, or prefer any observation — it only
    *flags* collisions with a shared ``duplicate_key`` so a later,
    methodology-authorized step can decide. Order of first appearance is
    preserved.
    """
    seen: Dict[Tuple[Any, ...], int] = {}
    flagged: List[EvaluationObservation] = []
    for observation in observations:
        key = observation.key.as_tuple()
        if key in seen:
            first_index = seen[key]
            duplicate_key = (
                flagged[first_index].duplicate_key
                or f"DUPLICATE:{len(seen)}:{key!r}"
            )
            if flagged[first_index].duplicate_key is None:
                flagged[first_index] = EvaluationObservation(
                    forecast=flagged[first_index].forecast,
                    metric_code=flagged[first_index].metric_code,
                    actual=flagged[first_index].actual,
                    evaluation_status=flagged[first_index].evaluation_status,
                    evaluation_timestamp=flagged[first_index].evaluation_timestamp,
                    input_refs=flagged[first_index].input_refs,
                    duplicate_key=duplicate_key,
                )
            flagged.append(EvaluationObservation(
                forecast=observation.forecast,
                metric_code=observation.metric_code,
                actual=observation.actual,
                evaluation_status=observation.evaluation_status,
                evaluation_timestamp=observation.evaluation_timestamp,
                input_refs=observation.input_refs,
                duplicate_key=duplicate_key,
            ))
        else:
            seen[key] = len(flagged)
            flagged.append(observation)
    return flagged


def evaluation_metadata(
    observations: List[EvaluationObservation],
) -> Dict[str, Any]:
    """Aggregate series metadata for one evaluated batch (no scores).

    Counts observations by status and surfaces the distinct horizons / model
    versions present, so a caller can verify isolation without computing
    anything P18 forbids (no MAPE, Bias, Reliability, Calibration, Valuation).
    """
    by_status: Dict[str, int] = {}
    horizons = set()
    versions = set()
    for observation in observations:
        by_status[observation.evaluation_status] = (
            by_status.get(observation.evaluation_status, 0) + 1
        )
        horizons.add(observation.forecast.forecast_horizon)
        versions.add(observation.forecast.model_version)
    return {
        "observation_count": len(observations),
        "by_status": by_status,
        "horizons": sorted(horizons),
        "model_versions": sorted(versions),
    }
