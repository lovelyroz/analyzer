"""Opt-in, fail-closed BANK bridge from canonical facts to Stage 5 inputs."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, Mapping

from sqlalchemy.orm import Session
from sqlalchemy import select

from src.core.jalali import is_valid_jalali_components
from src.forecast.canonical_queries import (
    CanonicalFactAtCutoff, _is_jalali_month_end, derive_standalone_quarters,
    load_canonical_financial_facts,
)
from src.forecast.queries import load_industry_code
from src.forecast.schema import ForecastInputRef
from src.ingestion.approval_catalog import ApprovalResolutionError, resolve_approval
from src.models.canonical import CanonicalCompanyFiscalCalendar, CanonicalIdentityBinding
from src.models.normalized import FinancialMetric

STAGE5_METRIC_KEYS = frozenset({
    "REVENUE", "OPERATING_PROFIT", "NET_PROFIT", "TOTAL_EQUITY",
})


class CanonicalReadError(ValueError):
    """Stable fail-closed error from the opt-in canonical read boundary."""

    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


@dataclass(frozen=True, slots=True)
class CanonicalMetricBinding:
    """Caller-approved Stage consumer key and exact canonical fact contract."""

    input_key: str
    metric_id: int
    temporal_type: str
    source_unit: str
    source_currency: str
    source_scale: str
    dimensions: tuple[tuple[str, str], ...] = ()
    duration_basis: str | None = None
    duration_aggregation: str | None = None
    period_end_jalali: tuple[int, int, int] | None = None


@dataclass(frozen=True, slots=True)
class CanonicalStage5Input:
    """In-memory Stage 5 facts, ordered by Jalali period end.

    The first value in each period tuple is an adapter-local ordinal required
    by existing Stage 5 helpers; it is not a canonical or Gregorian period ID.
    """

    facts: Mapping[str, int]
    input_refs: tuple[ForecastInputRef, ...]
    periods: tuple[tuple[int, tuple[int, int, int], Mapping[str, int], tuple[ForecastInputRef, ...]], ...]


def validate_stage5_bindings(
    bindings: Mapping[str, CanonicalMetricBinding],
) -> None:
    if not isinstance(bindings, Mapping):
        raise CanonicalReadError("CANONICAL_MAPPING_INVALID")
    if set(bindings) != STAGE5_METRIC_KEYS:
        raise CanonicalReadError("CANONICAL_STAGE5_MAPPING_INCOMPLETE")
    metric_ids: set[int] = set()
    for key, binding in bindings.items():
        validate_metric_binding(key, binding, require_period=False)
        expected_temporal = "INSTANT" if key == "TOTAL_EQUITY" else "DURATION"
        if binding.temporal_type != expected_temporal:
            raise CanonicalReadError("CANONICAL_STAGE5_TEMPORAL_CONTRACT_INCONSISTENT")
        if binding.metric_id in metric_ids:
            raise CanonicalReadError("CANONICAL_STAGE5_MAPPING_AMBIGUOUS")
        metric_ids.add(binding.metric_id)
    if len({(item.temporal_type, item.duration_basis)
            for item in bindings.values()
            if item.temporal_type == "DURATION"}) > 1:
        raise CanonicalReadError("CANONICAL_STAGE5_TEMPORAL_CONTRACT_INCONSISTENT")
    contracts = {
        (binding.source_unit, binding.source_currency, binding.source_scale)
        for binding in bindings.values()
    }
    if len(contracts) != 1:
        raise CanonicalReadError("CANONICAL_STAGE5_UNIT_CONTRACT_INCONSISTENT")


def validate_metric_binding(key: str, binding: CanonicalMetricBinding,
                            *, require_period: bool) -> None:
    if not isinstance(binding, CanonicalMetricBinding) or binding.input_key != key:
        raise CanonicalReadError("CANONICAL_MAPPING_INVALID")
    if type(binding.metric_id) is not int or binding.metric_id <= 0:
        raise CanonicalReadError("CANONICAL_MAPPING_INVALID")
    if any(not isinstance(value, str) or not value for value in
           (binding.source_unit, binding.source_currency, binding.source_scale)):
        raise CanonicalReadError("CANONICAL_MAPPING_INVALID")
    if (not isinstance(binding.dimensions, tuple)
            or any(not isinstance(pair, tuple) or len(pair) != 2
            or not all(isinstance(value, str) and value for value in pair)
            for pair in binding.dimensions)
            or tuple(sorted(binding.dimensions)) != binding.dimensions):
        raise CanonicalReadError("CANONICAL_DIMENSION_SELECTION_INVALID")
    if len({name for name, _ in binding.dimensions}) != len(binding.dimensions):
        raise CanonicalReadError("CANONICAL_DIMENSION_SELECTION_AMBIGUOUS")
    if binding.temporal_type == "INSTANT":
        if binding.duration_basis is not None or binding.duration_aggregation is not None:
            raise CanonicalReadError("CANONICAL_TEMPORAL_MAPPING_INVALID")
    elif binding.temporal_type == "DURATION":
        if binding.duration_basis != "YTD":
            raise CanonicalReadError("CANONICAL_TEMPORAL_MAPPING_INVALID")
        if key in STAGE5_METRIC_KEYS and binding.duration_aggregation != "ADDITIVE_YTD":
            raise CanonicalReadError("CANONICAL_YTD_AGGREGATION_UNAPPROVED")
        if key not in STAGE5_METRIC_KEYS and binding.duration_aggregation is not None:
            raise CanonicalReadError("CANONICAL_TEMPORAL_MAPPING_INVALID")
    else:
        raise CanonicalReadError("CANONICAL_TEMPORAL_MAPPING_INVALID")
    if require_period and binding.period_end_jalali is None:
        raise CanonicalReadError("CANONICAL_PERIOD_SELECTION_MISSING")
    if binding.period_end_jalali is not None and (
        not isinstance(binding.period_end_jalali, tuple)
        or len(binding.period_end_jalali) != 3
        or any(type(part) is not int for part in binding.period_end_jalali)
        or not is_valid_jalali_components(*binding.period_end_jalali)
    ):
        raise CanonicalReadError("CANONICAL_PERIOD_SELECTION_INVALID")


def matching_canonical_facts(
    facts: Iterable[CanonicalFactAtCutoff],
    binding: CanonicalMetricBinding,
    *,
    period_end: tuple[int, int, int] | None = None,
) -> list[CanonicalFactAtCutoff]:
    matched = []
    for fact in facts:
        if fact.metric_id != binding.metric_id or fact.dimensions != binding.dimensions:
            continue
        if period_end is not None and fact.end_jalali != period_end:
            continue
        if (fact.temporal_type != binding.temporal_type
                or fact.duration_basis != binding.duration_basis
                or fact.source_unit != binding.source_unit
                or fact.source_currency != binding.source_currency
                or fact.source_scale != binding.source_scale):
            raise CanonicalReadError("CANONICAL_FACT_METADATA_MISMATCH")
        if fact.scenario != "ACTUAL":
            raise CanonicalReadError("CANONICAL_SCENARIO_UNSUPPORTED")
        matched.append(fact)
    return matched


def validate_active_bank_metric_bindings(
    session: Session,
    metric_ids: Iterable[int],
) -> None:
    """Require each caller-selected metric ID to be active, approved, and BANK-scoped."""
    requested = set(metric_ids)
    if not requested or any(type(metric_id) is not int or metric_id <= 0 for metric_id in requested):
        raise CanonicalReadError("CANONICAL_METRIC_BINDING_INVALID")
    metrics = session.scalars(select(FinancialMetric).where(
        FinancialMetric.metric_id.in_(tuple(sorted(requested)))
    )).all()
    by_id = {metric.metric_id: metric for metric in metrics}
    if set(by_id) != requested:
        raise CanonicalReadError("CANONICAL_METRIC_BINDING_MISSING")
    if any(metric.category != "BANK" for metric in metrics):
        raise CanonicalReadError("CANONICAL_METRIC_INDUSTRY_MISMATCH")

    for metric_id in sorted(requested):
        bindings = session.scalars(select(CanonicalIdentityBinding).where(
            CanonicalIdentityBinding.identity_kind == "metric",
            CanonicalIdentityBinding.internal_id == metric_id,
            CanonicalIdentityBinding.is_active.is_(True),
        ).order_by(CanonicalIdentityBinding.binding_id)).all()
        if not bindings:
            raise CanonicalReadError("CANONICAL_METRIC_BINDING_MISSING")
        if len(bindings) != 1:
            raise CanonicalReadError("CANONICAL_METRIC_BINDING_AMBIGUOUS")
        binding = bindings[0]
        try:
            resolve_approval(
                session, approval_kind="metric",
                external_identity=binding.external_identity,
                expected_scope={"industry_code": "BANK"},
                approval_ref=binding.approval_ref,
            )
        except ApprovalResolutionError as exc:
            raise CanonicalReadError(exc.code) from exc


def load_approved_bank_fiscal_start_month(session: Session, company_id: int) -> int:
    calendar = session.get(CanonicalCompanyFiscalCalendar, company_id)
    if calendar is None:
        raise CanonicalReadError("CANONICAL_FISCAL_CALENDAR_MISSING")
    if not calendar.source_identity.strip():
        raise CanonicalReadError("CANONICAL_FISCAL_SOURCE_MISSING")
    if type(calendar.fiscal_year_start_month) is not int or not 1 <= calendar.fiscal_year_start_month <= 12:
        raise CanonicalReadError("CANONICAL_FISCAL_CALENDAR_INVALID")
    company_binding = session.scalar(select(CanonicalIdentityBinding).where(
        CanonicalIdentityBinding.identity_kind == "company",
        CanonicalIdentityBinding.internal_id == company_id,
        CanonicalIdentityBinding.is_active.is_(True),
    ))
    if company_binding is None:
        raise CanonicalReadError("CANONICAL_COMPANY_BINDING_MISSING")
    try:
        resolve_approval(
            session, approval_kind="company",
            external_identity=company_binding.external_identity,
            expected_scope={"industry_code": "BANK"},
            approval_ref=company_binding.approval_ref,
        )
        resolve_approval(
            session, approval_kind="fiscal_year_start_month",
            external_identity=f"{company_binding.external_identity}:{calendar.fiscal_year_start_month}",
            expected_scope={"company_id": company_binding.external_identity,
                            "industry_code": "BANK"},
            approval_ref=calendar.approval_ref,
        )
    except ApprovalResolutionError as exc:
        raise CanonicalReadError(exc.code) from exc
    return calendar.fiscal_year_start_month


def validate_periodic_ytd_identity(
    fact: CanonicalFactAtCutoff,
    fiscal_year_start_month: int,
) -> None:
    start, end = fact.start_jalali, fact.end_jalali
    months = (end[0] - start[0]) * 12 + end[1] - start[1] + 1
    if (start[2] != 1 or start[1] != fiscal_year_start_month
            or not is_valid_jalali_components(*start)
            or not _is_jalali_month_end(end)
            or months not in {3, 6, 9, 12}):
        raise CanonicalReadError("CANONICAL_STAGE5_YTD_PERIOD_INVALID")


def build_stage5_input(
    facts: Iterable[CanonicalFactAtCutoff],
    bindings: Mapping[str, CanonicalMetricBinding],
    *,
    company_id: int,
    fiscal_year_start_month: int,
) -> CanonicalStage5Input:
    """Validate and adapt PIT-filtered facts without float/unit conversion."""
    validate_stage5_bindings(bindings)
    if type(company_id) is not int or company_id <= 0:
        raise CanonicalReadError("CANONICAL_COMPANY_ID_INVALID")
    if type(fiscal_year_start_month) is not int or not 1 <= fiscal_year_start_month <= 12:
        raise CanonicalReadError("CANONICAL_FISCAL_CALENDAR_INVALID")
    if facts is None:
        raise CanonicalReadError("CANONICAL_FACTS_INVALID")
    rows = list(facts)
    if any(fact.company_id != company_id for fact in rows):
        raise CanonicalReadError("CANONICAL_COMPANY_MISMATCH")
    source = [fact for fact in rows if fact.report_type_id == "PERIODIC_FINANCIAL"]
    ytd_facts: list[CanonicalFactAtCutoff] = []
    instant_by_key: dict[tuple[str, tuple[int, int, int]], CanonicalFactAtCutoff] = {}

    for key, binding in bindings.items():
        selected = matching_canonical_facts(source, binding)
        if binding.temporal_type == "DURATION":
            for fact in selected:
                validate_periodic_ytd_identity(fact, fiscal_year_start_month)
            ytd_facts.extend(selected)
        else:
            for fact in selected:
                identity = (key, fact.end_jalali)
                if identity in instant_by_key:
                    raise CanonicalReadError("CANONICAL_FACT_AMBIGUOUS")
                instant_by_key[identity] = fact

    ytd_period_starts: dict[tuple[int, int, int], tuple[int, int, int]] = {}
    for fact in ytd_facts:
        existing_start = ytd_period_starts.get(fact.end_jalali)
        if existing_start is not None and existing_start != fact.start_jalali:
            raise CanonicalReadError("CANONICAL_STAGE5_PERIOD_MISMATCH")
        ytd_period_starts[fact.end_jalali] = fact.start_jalali

    # Runtime-only quarterly values retain both cumulative-version references.
    quarters = derive_standalone_quarters(ytd_facts)
    by_version = {fact.report_version_id: fact for fact in ytd_facts}
    by_metric_id = {binding.metric_id: key for key, binding in bindings.items()}
    values_by_end: dict[tuple[int, int, int], dict[str, int]] = {}
    refs_by_end: dict[tuple[int, int, int], list[ForecastInputRef]] = {}
    for fact in ytd_facts:
        values_by_end.setdefault(fact.end_jalali, {})
        if fact.value_integer is None:
            refs_by_end.setdefault(fact.end_jalali, []).append(ForecastInputRef(
                by_metric_id[fact.metric_id], fact.report_version_id,
                fact.publication_datetime, "canonical_financial_facts",
            ))

    for quarter in quarters:
        key = by_metric_id.get(quarter.metric_id)
        if key is None:
            continue
        current_candidates = [fact for fact in ytd_facts
                              if fact.metric_id == quarter.metric_id
                              and fact.end_jalali == quarter.period_end_jalali
                              and fact.start_jalali[2] == 1
                              and ((fact.end_jalali[0] - fact.start_jalali[0]) * 12
                                   + fact.end_jalali[1] - fact.start_jalali[1] + 1)
                              == quarter.quarter_number * 3]
        if len(current_candidates) > 1:
            raise CanonicalReadError("CANONICAL_FACT_AMBIGUOUS")
        if not current_candidates:
            continue
        end_values = values_by_end.setdefault(quarter.period_end_jalali, {})
        if key in end_values:
            raise CanonicalReadError("CANONICAL_FACT_AMBIGUOUS")
        end_values[key] = quarter.value_integer
        for version_id in quarter.source_report_version_ids:
            source_fact = by_version.get(version_id)
            if source_fact is None:
                raise CanonicalReadError("CANONICAL_PROVENANCE_MISSING")
            refs_by_end.setdefault(quarter.period_end_jalali, []).append(
                ForecastInputRef(key, version_id, source_fact.publication_datetime,
                                 "canonical_financial_facts")
            )

    for (key, end), fact in instant_by_key.items():
        values_by_end.setdefault(end, {})
        refs_by_end.setdefault(end, []).append(ForecastInputRef(
            key, fact.report_version_id, fact.publication_datetime,
            "canonical_financial_facts",
        ))
        if fact.value_integer is None:
            continue
        values_by_end.setdefault(end, {})[key] = fact.value_integer

    if not values_by_end:
        raise CanonicalReadError("CANONICAL_FACTS_MISSING")
    ordered_ends = sorted(values_by_end)
    periods = tuple(
        (index, end, values_by_end[end], tuple(refs_by_end.get(end, ())))
        for index, end in enumerate(ordered_ends, 1)
    )
    return CanonicalStage5Input(
        facts=periods[-1][2],
        input_refs=tuple(ref for period in periods for ref in period[3]),
        periods=periods,
    )


def load_stage5_input(
    session: Session,
    company_id: int,
    *,
    cutoff: datetime,
    bindings: Mapping[str, CanonicalMetricBinding],
) -> CanonicalStage5Input:
    validate_stage5_bindings(bindings)
    if load_industry_code(session, company_id) != "BANK":
        raise CanonicalReadError("CANONICAL_BANK_COMPANY_REQUIRED")
    validate_active_bank_metric_bindings(
        session, {binding.metric_id for binding in bindings.values()},
    )
    fiscal_year_start_month = load_approved_bank_fiscal_start_month(session, company_id)
    facts = load_canonical_financial_facts(
        session, company_id, cutoff=cutoff,
        metric_ids=tuple(sorted({item.metric_id for item in bindings.values()})),
        report_type_id="PERIODIC_FINANCIAL",
    )
    return build_stage5_input(
        facts, bindings, company_id=company_id,
        fiscal_year_start_month=fiscal_year_start_month,
    )
