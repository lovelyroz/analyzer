from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Optional

# P17 §5: the ReportVersion tie-break / restatement rule is UNRESOLVED
# METHODOLOGY AUTHORITY (blocker B5), so no selection preference is expressed
# here. These are the states a candidate ReportVersion can be carried in,
# populated by the caller that does have that authority.
ACTUAL_DATA_QUALITY_STATES = (
    "MISSING",
    "ESTIMATED",
    "SUSPICIOUS",
    "UNMAPPED",
    "RESTATED",
    "VALID",
)

# Stage 6 spec §12: percentage metrics are not computed in these regimes.
# Authority for the names themselves is AUTHORITATIVE (P17 §B); the values are
# carried, not interpreted, by the data foundation.
REGIME_STATUSES = (
    "ZERO_BASE",
    "LOSS_TO_PROFIT",
    "PROFIT_TO_LOSS",
    "SIGN_CHANGE",
)


def _normalize_datetime(value: Optional[Any]) -> Optional[datetime]:
    """Fold a naive/ISO datetime onto UTC so cutoffs stay comparable.

    Mirrors ``src.forecast.schema.normalize_datetime`` without importing Stage 5
    internals across the stage boundary (P17 §6.7).
    """
    if value is None:
        return None
    if isinstance(value, str):
        value = datetime.fromisoformat(value)
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


@dataclass
class ActualObservation:
    """A realized Stage 1 value for one metric/period, tied to a ReportVersion.

    The four temporal concepts of Stage 6 spec §4 / Rule 10 are kept distinct:

    * ``financial_period_id`` — the period the value *describes*. It is not a
      timestamp and is never compared against a cutoff.
    * ``publication_datetime`` — when the value became knowable, i.e. the
      ReportVersion publication. PIT applies to this instant only.
    * Neither is the forecast's own ``forecast_cutoff_datetime`` or
      ``forecast_timestamp``, which live on the observation's forecast side.

    ``value`` is ``None`` for a genuinely unknown Actual. Stage 6 spec §41 and
    the project-wide ``NULL != 0`` invariant: missing is never coerced to zero.
    """

    company_id: int
    financial_period_id: int
    metric_code: str
    value: Optional[float]
    report_version_id: Optional[int]
    publication_datetime: datetime
    data_quality_state: str = "VALID"
    restated: bool = False

    def __post_init__(self) -> None:
        self.publication_datetime = _normalize_datetime(self.publication_datetime)
        if self.data_quality_state not in ACTUAL_DATA_QUALITY_STATES:
            raise ValueError(
                f"unknown data quality state: {self.data_quality_state!r}"
            )


@dataclass(frozen=True)
class EvaluationInputRef:
    """Pointer from an evaluation to a fact that fed its construction.

    ``available_at`` is the instant the input became knowable. An evaluation
    whose forecast cutoff precedes ``available_at`` is Point-in-Time leakage
    (Stage 6 spec §5 / Rule 9) in an *input*, which is what Rule 9 governs —
    never the later-published Actual that is the outcome being evaluated.
    """

    fact_key: str
    available_at: Optional[datetime] = None
    source: Optional[str] = None

    def available_at_or(self, fallback: datetime) -> datetime:
        if self.available_at is None:
            normalized = _normalize_datetime(fallback)
            assert normalized is not None
            return normalized
        return self.available_at if self.available_at.tzinfo else self.available_at.replace(tzinfo=timezone.utc)


# NOTE (P23 — legacy de-authorization): the legacy carriers
# ``ForecastEvaluationResult`` and ``ReliabilityAssessment`` were removed.
# They existed only to serve the deleted ``ForecastEvaluationEngine``
# path, which produced numeric Reliability / CALIBRATION_CANDIDATE from
# unauthorized methodology. The authorized P18–P21 path carries
# observations via ``EvaluationObservation`` (observation.py), aggregates
# via ``ScoredObservation``/``SeriesEvaluation`` (aggregate.py), and
# governance via ``SeriesReliabilityGovernance`` (reliability.py).
