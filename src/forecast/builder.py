"""Weighted average share-count builder (Stage 5 EPS input, spec §9).

Turns the Stage 1 ``ShareCountHistory`` / ``CorporateAction`` records into the
``forecast_weighted_average_shares`` figure the forecast engine divides net
profit by. Both inputs are ordinary Stage 1 models, so the builder works with
mapped SQLAlchemy instances and with plain duck-typed stand-ins of the same
shape (which is what the unit tests use).
"""

from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Sequence, Tuple

from src.forecast.schema import normalize_datetime

# Corporate-action vocabulary supported by the Stage 1 model. Stage 5 does not
# invent actions; it only applies the ones Stage 1 recorded.
SHARE_CHANGING_ACTIONS = frozenset({
    "CAPITAL_INCREASE",
    "CAPITAL_DECREASE",
    "STOCK_SPLIT",
    "SPLIT",
    "REVERSE_SPLIT",
    "SHARE_CONSOLIDATION",
})


@dataclass(frozen=True)
class WeightedAverageShares:
    """Result of a weighted-average-share build.

    ``shares`` is ``None`` whenever the share base cannot be established: no
    history at all, or no observation on or before the forecast cutoff. A
    corporate action that cannot be resolved to a share count is skipped and
    reported in ``notes`` rather than guessed (spec §27).
    """
    shares: Optional[float]
    basis: str
    effective_date: Optional[date] = None
    applied_actions: List[str] = field(default_factory=list)
    notes: List[str] = field(default_factory=list)

    def get(self) -> Optional[float]:
        return self.shares


def _as_date(value: Any) -> Optional[date]:
    """Accept a ``date``, a ``datetime``, or an ISO string."""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    normalized = normalize_datetime(value)
    return normalized.date() if normalized is not None else None


def _shares_of(record: Any) -> Optional[int]:
    value = getattr(record, "shares_outstanding", None)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return int(value)


def _effective_date(record: Any) -> Optional[date]:
    value = getattr(record, "effective_date", None)
    return value if isinstance(value, date) else None


def _action_type(action: Any) -> str:
    value = getattr(action, "action_type", None)
    return str(value).strip().upper() if isinstance(value, str) else ""


def _share_count_of(action: Any, attribute: str) -> Optional[int]:
    value = getattr(action, attribute, None)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return int(value)


def _action_factor(action: Any) -> Optional[float]:
    """New shares per old share.

    The recorded ``old_share_count`` / ``new_share_count`` pair is
    authoritative; ``ratio`` is the fallback Stage 1 stores for the same
    relationship.
    """
    old_count = _share_count_of(action, "old_share_count")
    new_count = _share_count_of(action, "new_share_count")
    if old_count and new_count and old_count > 0:
        return new_count / old_count
    ratio = getattr(action, "ratio", None)
    if isinstance(ratio, (int, float)) and not isinstance(ratio, bool) and ratio > 0:
        return float(ratio)
    return None


def _resolved_count(action: Any, current: float) -> Optional[float]:
    """Share count in force from the action's effective date onward."""
    new_count = _share_count_of(action, "new_share_count")
    if new_count is not None:
        return float(new_count)
    factor = _action_factor(action)
    if factor is not None:
        return current * factor
    return None


def _segment_weights(walk: Sequence[Tuple[date, float]], start: date,
                     end: date) -> Dict[int, float]:
    """Days each segment was in force within ``[start, end]``."""
    weights: Dict[int, float] = {}
    for index, (segment_start, _) in enumerate(walk):
        segment_end = end if index == len(walk) - 1 else walk[index + 1][0]
        span = (min(segment_end, end) - max(segment_start, start)).days
        if span > 0:
            weights[index] = float(span)
    return weights


def build_weighted_average_shares(
    history: Optional[Sequence[Any]],
    actions: Optional[Sequence[Any]] = None,
    *,
    cutoff: Any = None,
    window_start: Any = None,
) -> WeightedAverageShares:
    """Derive ``forecast_weighted_average_shares`` (spec §9).

    ``ShareCountHistory`` supplies the authoritative share counts; corporate
    actions extend the series beyond the last observation up to the forecast
    cutoff. The cutoff is honoured three ways: history after it is invisible,
    an action effective after it is ignored, and an action effective before it
    but only announced after it is ignored too — a forecast dated before the
    announcement could not have known the new count (spec §25).

    Returns ``WeightedAverageShares(shares=None, ...)`` when the share base
    cannot be established. Nothing is fabricated.
    """
    if not history:
        return WeightedAverageShares(
            shares=None, basis="NO_SHARE_HISTORY",
            notes=["no ShareCountHistory records supplied"],
        )

    cutoff_date = _as_date(cutoff)
    start_date = _as_date(window_start)

    observations = [
        record for record in sorted(
            (_record for _record in history
             if _shares_of(_record) is not None
             and _effective_date(_record) is not None),
            key=_effective_date,
        )
        if cutoff_date is None or _effective_date(record) <= cutoff_date
    ]
    if not observations:
        return WeightedAverageShares(
            shares=None, basis="NO_OBSERVATION_AT_OR_BEFORE_CUTOFF",
            effective_date=cutoff_date,
            notes=[f"no share count on or before cutoff {cutoff_date}"],
        )

    walk: List[Tuple[date, float]] = [
        (_effective_date(record), float(_shares_of(record)))
        for record in observations
    ]
    last_observed_date, current_count = walk[-1]
    applied: List[str] = []
    notes: List[str] = []

    for action in sorted(
        (_action for _action in actions or ()
         if _action_type(_action) in SHARE_CHANGING_ACTIONS
         and _effective_date(_action) is not None),
        key=_effective_date,
    ):
        effective = _effective_date(action)
        if cutoff_date is not None and effective > cutoff_date:
            continue
        # Stage 1's own point-in-time rule: an unannounced action is unknowable.
        announced = getattr(action, "announcement_date", None)
        if (isinstance(announced, date) and cutoff_date is not None
                and announced > cutoff_date):
            notes.append(
                f"ignored {_action_type(action)} effective {effective}: "
                f"announced {announced}, after the cutoff"
            )
            continue
        if effective <= last_observed_date:
            # Already reflected in the recorded share-count history.
            continue

        resolved = _resolved_count(action, current_count)
        if resolved is None:
            notes.append(
                f"unusable {_action_type(action)} at {effective}: no "
                "new_share_count and no resolvable ratio"
            )
            continue
        walk.append((effective, resolved))
        current_count = resolved
        applied.append(f"{_action_type(action)}@{effective}")

    window_start_date = start_date
    if window_start_date is None or window_start_date < walk[0][0]:
        window_start_date = walk[0][0]
    window_end = cutoff_date if cutoff_date is not None else walk[-1][0]
    if window_end < window_start_date:
        return WeightedAverageShares(
            shares=None, basis="EMPTY_WEIGHT_WINDOW",
            effective_date=window_end, applied_actions=applied, notes=notes,
        )

    weights = _segment_weights(walk, window_start_date, window_end)
    if not weights:
        return WeightedAverageShares(
            shares=None, basis="EMPTY_WEIGHT_WINDOW",
            effective_date=window_end, applied_actions=applied, notes=notes,
        )

    total_weight = sum(weights.values())
    weighted_average = sum(
        count * weights[index] for index, (_date, count) in enumerate(walk)
    ) / total_weight

    basis = "UNADJUSTED" if not applied else "WEIGHTED_AVERAGE"
    return WeightedAverageShares(
        shares=weighted_average,
        basis=basis,
        effective_date=window_end,
        applied_actions=applied,
        notes=notes,
    )
