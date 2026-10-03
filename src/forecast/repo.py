"""Persistent forecast repository (spec sections 24, 25, 28, 29).

The persistence boundary for Stage 5:

    ForecastEngine -> ForecastRecord -> ForecastRepository -> persistent storage

The repository is the database-backed counterpart of the in-memory
``ForecastVersionStore``. Both implement the same versioning contract — a new
forecast for the same series appends a version instead of replacing one — so
the PIT behaviour established in ``src/forecast/schema.py`` is reused, not
reimplemented. The record remains the single source of truth for identity,
PIT and provenance; this module only stores it and reads it back.
"""

import json
from dataclasses import replace
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional

from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session

from src.forecast.schema import (
    ForecastInputRef,
    ForecastRecord,
    ForecastVersionExistsError,
    normalize_datetime,
)
from src.models.forecast import ForecastInputRefModel, ForecastVersion


def _json_dumps(payload: Optional[Dict[str, Any]]) -> Optional[str]:
    if payload is None:
        return None
    return json.dumps(payload, ensure_ascii=False, default=str, sort_keys=True)


def _json_loads(payload: Optional[str], default: Any = None) -> Any:
    if not payload:
        return default
    return json.loads(payload)


class ForecastRecordRepository:
    """Append-only persistent store of versioned forecast records.

    A session is expected on every call so the caller owns the transaction
    boundary. Records are stored once and never updated; a row is only ever
    inserted, never mutated in place.
    """

    def __init__(self, session: Session) -> None:
        self.session = session

    # ------------------------------------------------------------------
    # write
    # ------------------------------------------------------------------

    def save(self, record: ForecastRecord) -> ForecastRecord:
        """Persist ``record`` as the next version of its series.

        Re-saving a record equal to the stored latest version returns the
        stored row instead of inserting again (idempotent). Supplying a
        ``forecast_version`` that already exists with different contents is an
        attempted overwrite and is rejected.
        """
        latest = self._latest_row(*record.key())

        if record.forecast_version != 0:
            existing = self._version_row(*record.key(), record.forecast_version)
            if existing is not None:
                if self._records_equal(existing, record):
                    return self._to_record(existing)
                raise ForecastVersionExistsError(
                    f"forecast version {record.forecast_version} already stored for {record.key()}"
                )

        if latest is not None and self._records_equal(latest, record):
            return self._to_record(latest)

        row = ForecastVersion(
            company_id=record.company_id,
            forecast_period_id=record.forecast_period_id,
            forecast_horizon=record.forecast_horizon,
            scenario=record.scenario,
            version_number=(latest.version_number + 1) if latest is not None else 1,
            forecast_timestamp=normalize_datetime(record.forecast_timestamp),
            data_cutoff_datetime=normalize_datetime(record.data_cutoff_datetime),
            model_version=record.model_version,
            forecast_method=record.forecast_method,
            data_quality=record.data_quality,
            baseline_method=record.baseline_method,
            industry_code=record.industry_code,
            revenue=record.revenue,
            operating_profit=record.operating_profit,
            operating_margin=record.operating_margin,
            net_profit=record.net_profit,
            eps=record.eps,
            roe=record.roe,
            assumptions=_json_dumps(record.assumptions),
            stage4_provenance=_json_dumps(record.stage4_provenance),
        )
        self.session.add(row)
        self.session.flush()

        for ref in record.input_refs:
            self.session.add(ForecastInputRefModel(
                forecast_version_id=row.forecast_version_id,
                fact_key=ref.fact_key,
                report_version_id=ref.report_version_id,
                available_at=normalize_datetime(ref.available_at),
                source=ref.source,
            ))
        self.session.flush()
        return self._to_record(row)

    # ------------------------------------------------------------------
    # read
    # ------------------------------------------------------------------

    def history(self, company_id: int, forecast_period_id: int, horizon: str,
                scenario: str) -> List[ForecastRecord]:
        """Every preserved version of one series, oldest first (spec section 24)."""
        rows = self.session.execute(
            select(ForecastVersion)
            .where(_series_filter(company_id, forecast_period_id, horizon, scenario))
            .order_by(ForecastVersion.version_number.asc())
        ).scalars().all()
        return [self._to_record(row) for row in rows]

    def latest(self, company_id: int, forecast_period_id: int, horizon: str,
               scenario: str) -> Optional[ForecastRecord]:
        rows = self.history(company_id, forecast_period_id, horizon, scenario)
        return rows[-1] if rows else None

    def revision_trend(self, company_id: int, forecast_period_id: int, horizon: str,
                       scenario: str, metric: str = "eps") -> Optional[str]:
        """Earnings revision direction across preserved versions (spec section 24)."""
        values = [getattr(record, metric) for record in
                  self.history(company_id, forecast_period_id, horizon, scenario)]
        if len(values) < 2 or any(value is None for value in values):
            return None
        if all(values[i] < values[i + 1] for i in range(len(values) - 1)):
            return "UPWARD"
        if all(values[i] > values[i + 1] for i in range(len(values) - 1)):
            return "DOWNWARD"
        return "MIXED"

    def read_at_cutoff(self, company_id: int, forecast_period_id: int, horizon: str,
                       scenario: str, cutoff_datetime: datetime) -> Optional[ForecastRecord]:
        """Newest record valid at ``cutoff_datetime`` (spec section 25).

        A record whose inputs were published after the cutoff is invisible at
        that cutoff even when its own cutoff precedes it.
        """
        cutoff = normalize_datetime(cutoff_datetime)
        for record in reversed(self.history(company_id, forecast_period_id, horizon, scenario)):
            if normalize_datetime(record.data_cutoff_datetime) > cutoff:
                continue
            if self._late_inputs(record, cutoff):
                continue
            return record
        return None

    def pit_violations(self, cutoff_datetime: datetime) -> List[ForecastRecord]:
        """Stored records that saw information published after ``cutoff_datetime``."""
        cutoff = normalize_datetime(cutoff_datetime)
        rows = self.session.execute(
            select(ForecastVersion)
            .where(ForecastVersion.data_cutoff_datetime <= cutoff)
        ).scalars().all()
        return [
            record for record in (self._to_record(row) for row in rows)
            if self._late_inputs(record, cutoff)
        ]

    def count(self) -> int:
        return self.session.execute(
            select(func.count()).select_from(ForecastVersion)
        ).scalar_one()

    # ------------------------------------------------------------------
    # mapping
    # ------------------------------------------------------------------

    def _to_record(self, row: ForecastVersion) -> ForecastRecord:
        refs = [
            ForecastInputRef(
                fact_key=ref.fact_key,
                report_version_id=ref.report_version_id,
                available_at=normalize_datetime(ref.available_at),
                source=ref.source,
            )
            for ref in self.session.execute(
                select(ForecastInputRefModel)
                .where(ForecastInputRefModel.forecast_version_id == row.forecast_version_id)
                .order_by(ForecastInputRefModel.input_ref_id.asc())
            ).scalars().all()
        ]
        return ForecastRecord(
            forecast_id=row.forecast_version_id,
            forecast_version=row.version_number,
            company_id=row.company_id,
            forecast_period_id=row.forecast_period_id,
            industry_code=row.industry_code,
            forecast_horizon=row.forecast_horizon,
            scenario=row.scenario,
            forecast_timestamp=normalize_datetime(row.forecast_timestamp),
            data_cutoff_datetime=normalize_datetime(row.data_cutoff_datetime),
            model_version=row.model_version,
            forecast_method=row.forecast_method,
            data_quality=row.data_quality,
            baseline_method=row.baseline_method,
            revenue=_number(row.revenue),
            operating_profit=_number(row.operating_profit),
            operating_margin=_number(row.operating_margin),
            net_profit=_number(row.net_profit),
            eps=_number(row.eps),
            roe=_number(row.roe),
            assumptions=_json_loads(row.assumptions, default={}),
            input_refs=tuple(refs),
            stage4_provenance=_json_loads(row.stage4_provenance, default=None),
        )

    # ------------------------------------------------------------------
    # rows and equality
    # ------------------------------------------------------------------

    def _latest_row(self, company_id: int, forecast_period_id: int, horizon: str,
                    scenario: str) -> Optional[ForecastVersion]:
        return self.session.execute(
            select(ForecastVersion)
            .where(_series_filter(company_id, forecast_period_id, horizon, scenario))
            .order_by(ForecastVersion.version_number.desc())
        ).scalars().first()

    def _version_row(self, company_id: int, forecast_period_id: int, horizon: str,
                     scenario: str, version: int) -> Optional[ForecastVersion]:
        return self.session.execute(
            select(ForecastVersion)
            .where(and_(
                _series_filter(company_id, forecast_period_id, horizon, scenario),
                ForecastVersion.version_number == version,
            ))
        ).scalars().first()

    def _records_equal(self, row: ForecastVersion, record: ForecastRecord) -> bool:
        """Same series state, ignoring the surrogate id and version assignment.

        The candidate is rebuilt from the row's own primary key
        (``forecast_version_id``), never from the caller's surrogate
        ``forecast_id``: the row's identity is not forecast content, and the
        caller's id must not be able to make two identical records look
        different — or make one record match itself spuriously.

        The stored metrics carry only the column's own precision, so a fresh
        record is compared after rounding it back to what the column keeps.
        Without that, a record whose 6-digit metric lands in a 4-digit column
        could never be recognized as the same series state and the identical
        re-save would append a version instead of being a no-op.
        """
        candidate = replace(
            self._to_record(row),
            forecast_id=row.forecast_version_id,
            forecast_version=record.forecast_version,
        )
        if candidate != record:
            return _metrics_equal_at_column_precision(candidate, record)
        return True

    @staticmethod
    def _late_inputs(record: ForecastRecord, cutoff: datetime) -> List[ForecastInputRef]:
        return [
            ref for ref in record.input_refs
            if ref.available_at is not None
            and normalize_datetime(ref.available_at) > cutoff
        ]


def _series_filter(company_id: int, forecast_period_id: int, horizon: str,
                   scenario: str):
    return and_(
        ForecastVersion.company_id == company_id,
        ForecastVersion.forecast_period_id == forecast_period_id,
        ForecastVersion.forecast_horizon == horizon,
        ForecastVersion.scenario == scenario.upper(),
    )


def _number(value: Any) -> Optional[float]:
    """Read back a stored metric; NULL stays NULL (spec section 27)."""
    if value is None:
        return None
    if isinstance(value, Decimal):
        return float(value)
    return float(value)


# Metrics and the scale their columns keep. A stored value is only ever as
# precise as this, so equality against a fresh record is measured here.
_METRIC_SCALES = {
    "revenue": 4,
    "operating_profit": 4,
    "operating_margin": 10,
    "net_profit": 4,
    "eps": 4,
    "roe": 10,
}


def _metrics_equal_at_column_precision(
    stored: ForecastRecord, other: ForecastRecord
) -> bool:
    """Compare only the stored metrics, after rounding the fresh ones.

    Non-metric fields are not rounded: they are compared exactly so a genuinely
    different series state is still detected.
    """
    for field in ("company_id", "forecast_period_id", "industry_code",
                  "forecast_horizon", "scenario", "forecast_timestamp",
                  "data_cutoff_datetime", "model_version", "forecast_method",
                  "data_quality", "baseline_method", "assumptions",
                  "input_refs", "stage4_provenance"):
        if getattr(stored, field) != getattr(other, field):
            return False
    for field, scale in _METRIC_SCALES.items():
        stored_value = getattr(stored, field)
        other_value = getattr(other, field)
        if stored_value is None or other_value is None:
            if stored_value is not other_value:
                return False
            continue
        if float(f"{stored_value:.{scale}f}") != float(f"{other_value:.{scale}f}"):
            return False
    return True
