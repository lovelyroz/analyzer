"""Opt-in canonical BANK input bridge for the existing Stage 6 KPI engine."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping

from sqlalchemy.orm import Session

from src.core.jalali import is_valid_jalali_components
from src.forecast.canonical_adapter import (
    CanonicalMetricBinding, CanonicalReadError, matching_canonical_facts,
    load_approved_bank_fiscal_start_month, validate_periodic_ytd_identity,
    validate_active_bank_metric_bindings,
    validate_metric_binding,
)
from src.forecast.canonical_queries import (
    CanonicalFactAtCutoff, load_canonical_financial_facts,
)
from src.forecast.queries import load_industry_code
from src.forecast.schema import ForecastInputRef
from src.kpi.engine import KPIEngine

_BANK_KPI_CODES = {
    "REVENUE_GROWTH", "OP_PROFIT_GROWTH", "NET_PROFIT_GROWTH", "EPS_GROWTH",
    "GROSS_MARGIN", "OPERATING_MARGIN", "NET_MARGIN", "ROA", "ROE",
    "CASH_CONVERSION", "EARNINGS_QUALITY", "FINANCIAL_COST_PRESSURE",
    "BANK_NII", "BANK_NIM", "BANK_LOAN_GROWTH", "BANK_DEPOSIT_GROWTH", "BANK_NPL",
}
_SAME_PERIOD_KPI_CODES = {
    "GROSS_MARGIN", "OPERATING_MARGIN", "NET_MARGIN", "CASH_CONVERSION",
    "EARNINGS_QUALITY", "FINANCIAL_COST_PRESSURE",
}
_SAME_END_KPI_CODES = _SAME_PERIOD_KPI_CODES | {"ROA", "ROE"}
_GROWTH_KPI_CODES = {
    "REVENUE_GROWTH", "OP_PROFIT_GROWTH", "NET_PROFIT_GROWTH", "EPS_GROWTH",
}
STAGE6_INPUT_KEYS = frozenset(
    key for code in _BANK_KPI_CODES for key in KPIEngine._KPI_INPUTS[code]
)


@dataclass(frozen=True, slots=True)
class CanonicalKPIInput:
    period_id: int
    period_end_jalali: tuple[int, int, int]
    financial_data: Mapping[str, Any]
    quality_statuses: Mapping[str, str]
    canonical_period_ids: Mapping[str, int]
    input_refs: tuple[ForecastInputRef, ...]


def validate_stage6_bindings(bindings: Mapping[str, CanonicalMetricBinding]) -> None:
    if not isinstance(bindings, Mapping):
        raise CanonicalReadError("CANONICAL_MAPPING_INVALID")
    if set(bindings) != STAGE6_INPUT_KEYS:
        raise CanonicalReadError("CANONICAL_STAGE6_MAPPING_INCOMPLETE")
    identities: set[tuple[int, tuple[int, int, int], tuple[tuple[str, str], ...]]] = set()
    for key, binding in bindings.items():
        validate_metric_binding(key, binding, require_period=True)
        identity = (binding.metric_id, binding.period_end_jalali, binding.dimensions)
        if identity in identities:
            raise CanonicalReadError("CANONICAL_STAGE6_MAPPING_AMBIGUOUS")
        identities.add(identity)
    comparable_pairs = {
        tuple(KPIEngine._KPI_INPUTS[code])
        for code in _BANK_KPI_CODES
        if len(KPIEngine._KPI_INPUTS[code]) == 2
    }
    for left_key, right_key in comparable_pairs:
        left, right = bindings[left_key], bindings[right_key]
        if ((left.source_unit, left.source_currency, left.source_scale)
                != (right.source_unit, right.source_currency, right.source_scale)):
            raise CanonicalReadError("CANONICAL_STAGE6_UNIT_CONTRACT_INCONSISTENT")
    for code in _SAME_END_KPI_CODES:
        left_key, right_key = KPIEngine._KPI_INPUTS[code]
        left, right = bindings[left_key], bindings[right_key]
        if left.period_end_jalali != right.period_end_jalali:
            raise CanonicalReadError("CANONICAL_STAGE6_PERIOD_MAPPING_INCONSISTENT")
    for code in _GROWTH_KPI_CODES:
        current_key, previous_key = KPIEngine._KPI_INPUTS[code]
        if bindings[current_key].period_end_jalali <= bindings[previous_key].period_end_jalali:
            raise CanonicalReadError("CANONICAL_STAGE6_PERIOD_ORDER_INVALID")
    for code in _SAME_PERIOD_KPI_CODES:
        left_key, right_key = KPIEngine._KPI_INPUTS[code]
        left, right = bindings[left_key], bindings[right_key]
        if (left.temporal_type, left.duration_basis) != (right.temporal_type, right.duration_basis):
            raise CanonicalReadError("CANONICAL_STAGE6_TEMPORAL_MAPPING_INCONSISTENT")


def build_stage6_input(
    facts: list[CanonicalFactAtCutoff],
    bindings: Mapping[str, CanonicalMetricBinding],
    *,
    company_id: int,
    period_id: int,
    period_end_jalali: tuple[int, int, int],
    fiscal_year_start_month: int,
) -> CanonicalKPIInput:
    """Build explicit KPI inputs; missing and null values stay missing."""
    validate_stage6_bindings(bindings)
    if type(company_id) is not int or company_id <= 0:
        raise CanonicalReadError("CANONICAL_COMPANY_ID_INVALID")
    if type(period_id) is not int or period_id <= 0:
        raise CanonicalReadError("CANONICAL_PERIOD_ID_INVALID")
    if type(fiscal_year_start_month) is not int or not 1 <= fiscal_year_start_month <= 12:
        raise CanonicalReadError("CANONICAL_FISCAL_CALENDAR_INVALID")
    if (not isinstance(period_end_jalali, tuple) or len(period_end_jalali) != 3
            or any(type(part) is not int for part in period_end_jalali)
            or not is_valid_jalali_components(*period_end_jalali)):
        raise CanonicalReadError("CANONICAL_PERIOD_SELECTION_INVALID")
    if any(key.endswith("_curr") and binding.period_end_jalali != period_end_jalali
           for key, binding in bindings.items()):
        raise CanonicalReadError("CANONICAL_STAGE6_OUTPUT_PERIOD_MISMATCH")
    if facts is None:
        raise CanonicalReadError("CANONICAL_FACTS_INVALID")
    selected: dict[str, CanonicalFactAtCutoff] = {}
    if any(fact.company_id != company_id for fact in facts):
        raise CanonicalReadError("CANONICAL_COMPANY_MISMATCH")
    periodic_facts = [fact for fact in facts
                      if fact.report_type_id == "PERIODIC_FINANCIAL"]
    for key, binding in bindings.items():
        matches = matching_canonical_facts(
            periodic_facts, binding, period_end=binding.period_end_jalali,
        )
        if len(matches) > 1:
            raise CanonicalReadError("CANONICAL_FACT_AMBIGUOUS")
        if matches:
            selected[key] = matches[0]

    for fact in selected.values():
        if fact.temporal_type == "DURATION":
            validate_periodic_ytd_identity(fact, fiscal_year_start_month)

    for code in _SAME_PERIOD_KPI_CODES:
        left_key, right_key = KPIEngine._KPI_INPUTS[code]
        left, right = selected.get(left_key), selected.get(right_key)
        if (left is not None and right is not None
                and (left.start_jalali, left.end_jalali)
                != (right.start_jalali, right.end_jalali)):
            raise CanonicalReadError("CANONICAL_STAGE6_PERIOD_MISMATCH")

    # This explicit mapping is the only source of engine keys. No aliases,
    # ratios, unit conversions, or inferred metric identities are introduced.
    data: dict[str, int] = {}
    quality: dict[str, str] = {key: "MISSING" for key in bindings}
    canonical_period_ids: dict[str, int] = {}
    refs: list[ForecastInputRef] = []
    for key, fact in selected.items():
        canonical_period_ids[key] = fact.period_id
        refs.append(ForecastInputRef(
            key, fact.report_version_id, fact.publication_datetime,
            "canonical_financial_facts",
        ))
        if fact.value_integer is None:
            quality[key] = "MISSING"
            continue
        data[key] = fact.value_integer
        quality[key] = (
            "RESTATED" if fact.is_restated else
            "ESTIMATED" if fact.value_state == "ZERO_FALLBACK" else "VALID"
        )

    return CanonicalKPIInput(
        period_id=period_id,
        period_end_jalali=period_end_jalali,
        financial_data={**data, "quality_statuses": quality},
        quality_statuses=quality,
        canonical_period_ids=canonical_period_ids,
        input_refs=tuple(refs),
    )


def calculate_stage6_kpis_from_canonical(
    session: Session,
    company_id: int,
    *,
    period_id: int,
    period_end_jalali: tuple[int, int, int],
    cutoff: datetime,
    bindings: Mapping[str, CanonicalMetricBinding],
):
    """Read canonical BANK facts and invoke the existing KPI formulas."""
    validate_stage6_bindings(bindings)
    if load_industry_code(session, company_id) != "BANK":
        raise CanonicalReadError("CANONICAL_BANK_COMPANY_REQUIRED")
    validate_active_bank_metric_bindings(
        session, {binding.metric_id for binding in bindings.values()},
    )
    fiscal_year_start_month = load_approved_bank_fiscal_start_month(session, company_id)
    facts = load_canonical_financial_facts(
        session, company_id, cutoff=cutoff,
        metric_ids=tuple(sorted({binding.metric_id for binding in bindings.values()})),
        report_type_id="PERIODIC_FINANCIAL",
    )
    adapted = build_stage6_input(
        facts, bindings, company_id=company_id, period_id=period_id,
        period_end_jalali=period_end_jalali,
        fiscal_year_start_month=fiscal_year_start_month,
    )
    results = KPIEngine().calculate_all_kpis_for_company(
        company_id, adapted.period_id, "BANK", dict(adapted.financial_data),
    )
    return results, adapted
