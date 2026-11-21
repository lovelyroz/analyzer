"""Jalali-native point-in-time reads for canonical BANK financial facts."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from src.models.canonical import (
    CanonicalDimensionMember, CanonicalFactProvenance,
    CanonicalFinancialFact, CanonicalFinancialPeriod, CanonicalReport,
    CanonicalReportVersion,
)


@dataclass(frozen=True, slots=True)
class CanonicalFactAtCutoff:
    company_id: int
    report_type_id: str
    metric_id: int
    period_id: int
    temporal_type: str
    start_jalali: tuple[int, int, int]
    end_jalali: tuple[int, int, int]
    duration_basis: str | None
    value_integer: int | None
    value_state: str
    scenario: str
    source_unit: str
    source_currency: str
    source_scale: str
    report_version_id: int
    publication_datetime: datetime
    is_audited: bool
    is_restated: bool
    dimensions: tuple[tuple[str, str], ...]
    source_identity: str
    revision_identity: str
    source_coordinate: str


def load_canonical_financial_facts(
    session: Session,
    company_id: int,
    *,
    cutoff: datetime,
    metric_ids: tuple[int, ...] | None = None,
) -> list[CanonicalFactAtCutoff]:
    """Return the highest-quality visible version per report type/fact identity.

    Period ordering and identity remain Jalali components. Publication time is
    the PIT cutoff; within that set, audited/restated rank precedes publication
    time and version tie-breaks. A period end never substitutes for publication.
    """
    statement = (
        select(CanonicalFinancialFact, CanonicalFinancialPeriod,
               CanonicalReportVersion, CanonicalReport, CanonicalFactProvenance)
        .join(CanonicalReportVersion,
              CanonicalFinancialFact.report_version_id == CanonicalReportVersion.canonical_report_version_id)
        .join(CanonicalReport,
              CanonicalReportVersion.canonical_report_id == CanonicalReport.canonical_report_id)
        .join(CanonicalFinancialPeriod,
              CanonicalFinancialFact.period_id == CanonicalFinancialPeriod.period_id)
        .join(CanonicalFactProvenance,
              CanonicalFactProvenance.fact_id == CanonicalFinancialFact.fact_id)
        .where(and_(CanonicalReport.company_id == company_id,
                    CanonicalReportVersion.publication_datetime <= _utc_naive(cutoff)))
    )
    if metric_ids is not None:
        if not metric_ids:
            return []
        statement = statement.where(CanonicalFinancialFact.metric_id.in_(metric_ids))
    rows = session.execute(statement).all()
    chosen: dict[tuple[object, ...], tuple[CanonicalFactAtCutoff, tuple[int, datetime, int, int]]] = {}
    for fact, period, version, report, provenance in rows:
        dimensions = tuple(sorted(session.execute(
            select(CanonicalDimensionMember.dimension_id,
                   CanonicalDimensionMember.dimension_value_id)
            .where(CanonicalDimensionMember.dimension_set_id == fact.dimension_set_id)
        ).all()))
        dto = CanonicalFactAtCutoff(
            company_id=report.company_id, report_type_id=report.report_type_id,
            metric_id=fact.metric_id,
            period_id=period.period_id, temporal_type=period.temporal_type,
            start_jalali=(period.start_year, period.start_month, period.start_day),
            end_jalali=(period.end_year, period.end_month, period.end_day),
            duration_basis=fact.duration_basis, value_integer=fact.value_integer,
            value_state=fact.value_state, source_unit=fact.source_unit,
            scenario=fact.scenario,
            source_currency=fact.source_currency, source_scale=fact.source_scale,
            report_version_id=version.canonical_report_version_id,
            publication_datetime=version.publication_datetime,
            is_audited=version.is_audited, is_restated=version.is_restated,
            dimensions=dimensions, source_identity=provenance.source_identity,
            revision_identity=provenance.revision_identity,
            source_coordinate=provenance.source_coordinate,
        )
        key = (dto.report_type_id, dto.scenario, fact.metric_id,
               dto.start_jalali, dto.end_jalali, dimensions)
        quality = (4 if version.is_audited and version.is_restated else
                   3 if version.is_audited else
                   2 if version.is_restated else 1)
        rank = (quality, version.publication_datetime, version.version_number,
                version.canonical_report_version_id)
        current = chosen.get(key)
        if current is None or rank > current[1]:
            chosen[key] = (dto, rank)
    return sorted((item[0] for item in chosen.values()),
                  key=lambda item: (item.end_jalali, item.start_jalali, item.report_type_id,
                                    item.scenario, item.metric_id, item.dimensions))


def _utc_naive(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value
    return value.astimezone(timezone.utc).replace(tzinfo=None)

