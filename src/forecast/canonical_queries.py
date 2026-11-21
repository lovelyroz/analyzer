"""Jalali-native point-in-time reads for canonical BANK financial facts."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Iterable

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from src.core.jalali import is_valid_jalali_components
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


@dataclass(frozen=True, slots=True)
class CanonicalStandaloneQuarter:
    company_id: int
    report_type_id: str
    metric_id: int
    scenario: str
    quarter_number: int
    period_start_jalali: tuple[int, int, int]
    period_end_jalali: tuple[int, int, int]
    value_integer: int
    source_report_version_ids: tuple[int, ...]


def derive_standalone_quarters(
    facts: Iterable[CanonicalFactAtCutoff],
) -> list[CanonicalStandaloneQuarter]:
    """Derive quarter-only values in memory from compatible BANK YTD facts.

    This is a read-side calculation only. It returns no ORM objects and writes
    no calculated values. Inputs must already have been PIT-filtered by
    ``load_canonical_financial_facts``.
    """
    ytd: dict[tuple[object, ...], dict[int, CanonicalFactAtCutoff]] = {}
    for fact in facts:
        if (fact.report_type_id != "PERIODIC_FINANCIAL" or fact.temporal_type != "DURATION"
                or fact.duration_basis != "YTD" or fact.value_integer is None
                or fact.value_state not in {"REPORTED_VALUE", "ZERO_FALLBACK"}):
            continue
        start, end = fact.start_jalali, fact.end_jalali
        if start[2] != 1 or not _is_jalali_month_end(end):
            continue
        months = (end[0] - start[0]) * 12 + end[1] - start[1] + 1
        if months not in {3, 6, 9, 12}:
            continue
        key = (fact.company_id, fact.report_type_id, fact.metric_id, fact.scenario,
               start, fact.dimensions, fact.source_unit, fact.source_currency, fact.source_scale)
        periods = ytd.setdefault(key, {})
        if months in periods:
            # Duplicate period identities make caller-supplied snapshots ambiguous.
            periods[months] = None  # type: ignore[assignment]
        else:
            periods[months] = fact

    result: list[CanonicalStandaloneQuarter] = []
    for key, periods in ytd.items():
        company_id, report_type_id, metric_id, scenario, fiscal_start, *_ = key
        for months in (3, 6, 9, 12):
            current = periods.get(months)
            if current is None:
                continue
            previous = None if months == 3 else periods.get(months - 3)
            if months != 3 and previous is None:
                continue
            value = current.value_integer if previous is None else current.value_integer - previous.value_integer
            quarter_start = fiscal_start if previous is None else _next_jalali_month(previous.end_jalali)
            result.append(CanonicalStandaloneQuarter(
                company_id=company_id, report_type_id=report_type_id, metric_id=metric_id,
                scenario=scenario, quarter_number=months // 3,
                period_start_jalali=quarter_start, period_end_jalali=current.end_jalali,
                value_integer=value,
                source_report_version_ids=((current.report_version_id,) if previous is None else
                                           (previous.report_version_id, current.report_version_id)),
            ))
    return sorted(result, key=lambda item: (item.period_end_jalali, item.metric_id, item.scenario))


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


def _is_jalali_month_end(value: tuple[int, int, int]) -> bool:
    year, month, day = value
    if not is_valid_jalali_components(year, month, day):
        return False
    max_day = 31 if month <= 6 else 30 if month <= 11 else 30 if is_valid_jalali_components(year, 12, 30) else 29
    return day == max_day


def _next_jalali_month(value: tuple[int, int, int]) -> tuple[int, int, int]:
    year, month, _day = value
    return (year + 1, 1, 1) if month == 12 else (year, month + 1, 1)

