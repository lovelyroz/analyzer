from datetime import datetime

import pytest

from src.forecast.canonical_adapter import CanonicalMetricBinding, CanonicalReadError
from src.forecast.canonical_queries import CanonicalFactAtCutoff
from src.kpi.canonical_adapter import (
    STAGE6_INPUT_KEYS, build_stage6_input,
    calculate_stage6_kpis_from_canonical,
)
from src.kpi.engine import KPIEngine


def _key_base(key):
    return key.removesuffix("_curr").removesuffix("_prev")


def _bindings():
    keys = sorted(STAGE6_INPUT_KEYS)
    ids = {_key_base(key): index + 1 for index, key in enumerate(sorted({_key_base(k) for k in keys}))}
    bindings = {}
    for key in keys:
        base = _key_base(key)
        is_balance = base in {"avg_assets", "avg_equity"}
        is_ratio = base in {"nim", "loan_growth", "deposit_growth", "npl"}
        is_per_share = base == "eps"
        bindings[key] = CanonicalMetricBinding(
            input_key=key, metric_id=ids[base],
            temporal_type="INSTANT" if is_balance else "DURATION",
            duration_basis=None if is_balance else "YTD",
            source_unit=("unit-percent" if is_ratio else "unit-per-share" if is_per_share else "unit-rial"),
            source_currency=("currency-none" if is_ratio or is_per_share else "currency-irr"),
            source_scale="scale-unit",
            period_end_jalali=(1404, 3, 31) if key.endswith("_prev") else (1404, 6, 30),
        )
    return bindings


def _fact(binding, value, version, *, end=None, state="REPORTED_VALUE", unit=None,
          dimensions=None, report_type="PERIODIC_FINANCIAL"):
    end = end or binding.period_end_jalali
    instant = binding.temporal_type == "INSTANT"
    return CanonicalFactAtCutoff(
        company_id=7, report_type_id=report_type, metric_id=binding.metric_id,
        period_id=100 + version, temporal_type=binding.temporal_type,
        start_jalali=end if instant else (1404, 1, 1), end_jalali=end,
        duration_basis=binding.duration_basis, value_integer=value,
        value_state=state, scenario="ACTUAL",
        source_unit=unit or binding.source_unit, source_currency=binding.source_currency,
        source_scale=binding.source_scale, report_version_id=version,
        publication_datetime=datetime(2025, 1, version), is_audited=True,
        is_restated=False, dimensions=dimensions if dimensions is not None else binding.dimensions,
        source_identity="source", revision_identity=str(version), source_coordinate="C5",
    )


def test_stage6_maps_explicit_bank_inputs_and_preserves_missing_zero_and_lineage():
    bindings = _bindings()
    selected = [
        _fact(bindings["revenue_curr"], 250, 1),
        _fact(bindings["revenue_prev"], 100, 2, end=(1404, 3, 31)),
        _fact(bindings["nii"], 0, 3, state="ZERO_FALLBACK"),
    ]

    adapted = build_stage6_input(
        selected, bindings, company_id=7, period_id=22, period_end_jalali=(1404, 6, 30), fiscal_year_start_month=1
    )

    assert adapted.financial_data["revenue_curr"] == 250
    assert type(adapted.financial_data["revenue_curr"]) is int
    assert adapted.financial_data["nii"] == 0
    assert adapted.quality_statuses["nii"] == "ESTIMATED"
    assert "net_profit_curr" not in adapted.financial_data
    assert adapted.quality_statuses["net_profit_curr"] == "MISSING"
    assert adapted.canonical_period_ids == {
        "revenue_curr": 101, "revenue_prev": 102, "nii": 103,
    }
    assert {ref.fact_key for ref in adapted.input_refs} == {"revenue_curr", "revenue_prev", "nii"}

    results = KPIEngine().calculate_all_kpis_for_company(
        7, adapted.period_id, "BANK", dict(adapted.financial_data),
    )
    growth = next(result for result in results if result.kpi_code == "REVENUE_GROWTH")
    assert growth.value == 150.0


def test_stage6_rejects_incomplete_mapping_and_wrong_unit():
    bindings = _bindings()
    with pytest.raises(CanonicalReadError, match="CANONICAL_STAGE6_MAPPING_INCOMPLETE"):
        build_stage6_input(
            [], {key: value for key, value in bindings.items() if key != "nii"}, company_id=7,
            period_id=22, period_end_jalali=(1404, 6, 30), fiscal_year_start_month=1
        )
    wrong = _fact(bindings["nii"], 5, 4, unit="unit-guessed")
    with pytest.raises(CanonicalReadError, match="CANONICAL_FACT_METADATA_MISMATCH"):
        build_stage6_input(
            [wrong], bindings, company_id=7, period_id=22, period_end_jalali=(1404, 6, 30), fiscal_year_start_month=1
        )

    duplicate = dict(bindings)
    duplicate["nii"] = CanonicalMetricBinding(
        input_key="nii", metric_id=bindings["revenue_curr"].metric_id,
        temporal_type="DURATION", duration_basis="YTD",
        source_unit="unit-nii", source_currency="currency-irr",
        source_scale="scale-unit", period_end_jalali=(1404, 6, 30),
    )
    with pytest.raises(CanonicalReadError, match="CANONICAL_STAGE6_MAPPING_AMBIGUOUS"):
        build_stage6_input(
            [], duplicate, company_id=7, period_id=22,
            period_end_jalali=(1404, 6, 30), fiscal_year_start_month=1
        )


def test_stage6_rejects_cross_company_fact_rows():
    binding = _bindings()
    foreign = _fact(binding["nii"], 99, 5)
    foreign = CanonicalFactAtCutoff(**{
        name: (8 if name == "company_id" else getattr(foreign, name))
        for name in foreign.__dataclass_fields__
    })
    with pytest.raises(CanonicalReadError, match="CANONICAL_COMPANY_MISMATCH"):
        build_stage6_input(
            [foreign], binding, company_id=7,
            period_id=22, period_end_jalali=(1404, 6, 30), fiscal_year_start_month=1
        )


def test_stage6_rejects_inconsistent_expected_units_and_periods():
    bindings = _bindings()
    bindings["op_profit_curr"] = CanonicalMetricBinding(
        input_key="op_profit_curr", metric_id=bindings["op_profit_curr"].metric_id,
        temporal_type="DURATION", duration_basis="YTD",
        source_unit="unit-thousand-rial", source_currency="currency-irr",
        source_scale="scale-unit", period_end_jalali=(1404, 6, 30),
    )
    with pytest.raises(CanonicalReadError, match="CANONICAL_STAGE6_UNIT_CONTRACT_INCONSISTENT"):
        build_stage6_input(
            [], bindings, company_id=7, period_id=22,
            period_end_jalali=(1404, 6, 30), fiscal_year_start_month=1
        )


def test_stage6_requires_ordered_growth_periods_and_current_output_period():
    bindings = _bindings()
    bindings["revenue_prev"] = CanonicalMetricBinding(
        input_key="revenue_prev", metric_id=bindings["revenue_prev"].metric_id,
        temporal_type="DURATION", duration_basis="YTD",
        source_unit="unit-rial", source_currency="currency-irr",
        source_scale="scale-unit", period_end_jalali=(1404, 9, 30),
    )
    with pytest.raises(CanonicalReadError, match="CANONICAL_STAGE6_PERIOD_ORDER_INVALID"):
        build_stage6_input(
            [], bindings, company_id=7, period_id=22,
            period_end_jalali=(1404, 6, 30), fiscal_year_start_month=1
        )

    bindings = _bindings()
    with pytest.raises(CanonicalReadError, match="CANONICAL_STAGE6_OUTPUT_PERIOD_MISMATCH"):
        build_stage6_input(
            [], bindings, company_id=7, period_id=22,
            period_end_jalali=(1404, 3, 31), fiscal_year_start_month=1
        )

    bindings = _bindings()
    bindings["gross_profit"] = CanonicalMetricBinding(
        input_key="gross_profit", metric_id=bindings["gross_profit"].metric_id,
        temporal_type="DURATION", duration_basis="YTD",
        source_unit="unit-rial", source_currency="currency-irr",
        source_scale="scale-unit", period_end_jalali=(1404, 3, 31),
    )
    with pytest.raises(CanonicalReadError, match="CANONICAL_STAGE6_PERIOD_MAPPING_INCONSISTENT"):
        build_stage6_input(
            [], bindings, company_id=7, period_id=22,
            period_end_jalali=(1404, 6, 30), fiscal_year_start_month=1
        )


def test_stage6_does_not_accept_monthly_facts_or_guess_dimensions():
    bindings = _bindings()
    monthly = _fact(bindings["nii"], 12, 5, report_type="MONTHLY_ACTIVITY")
    selected_dimension = CanonicalMetricBinding(
        input_key="nii", metric_id=bindings["nii"].metric_id,
        temporal_type="DURATION", duration_basis="YTD",
        source_unit=bindings["nii"].source_unit,
        source_currency=bindings["nii"].source_currency,
        source_scale=bindings["nii"].source_scale,
        dimensions=(("consolidation", "consolidated"),),
        period_end_jalali=(1404, 6, 30),
    )
    bindings["nii"] = selected_dimension
    adapted = build_stage6_input(
        [monthly, _fact(bindings["nii"], 20, 6, dimensions=())],
        bindings, company_id=7, period_id=22, period_end_jalali=(1404, 6, 30), fiscal_year_start_month=1
    )
    assert "nii" not in adapted.financial_data
    assert adapted.quality_statuses["nii"] == "MISSING"


def test_stage6_validates_ytd_start_against_approved_fiscal_month():
    bindings = _bindings()
    fact = _fact(bindings["nii"], 25, 7)
    with pytest.raises(CanonicalReadError, match="CANONICAL_STAGE5_YTD_PERIOD_INVALID"):
        build_stage6_input(
            [fact], bindings, company_id=7, period_id=22,
            period_end_jalali=(1404, 6, 30), fiscal_year_start_month=7,
        )


def test_stage6_opt_in_loader_is_bank_only_and_queries_periodic_pit_facts(monkeypatch):
    from src.kpi import canonical_adapter

    bindings = _bindings()
    facts = [
        _fact(bindings["revenue_curr"], 250, 1),
        _fact(bindings["revenue_prev"], 100, 2, end=(1404, 3, 31)),
    ]
    seen = {}
    monkeypatch.setattr(canonical_adapter, "load_industry_code", lambda *_: "BANK")
    monkeypatch.setattr(canonical_adapter, "validate_active_bank_metric_bindings", lambda *_: None)
    monkeypatch.setattr(canonical_adapter, "load_approved_bank_fiscal_start_month", lambda *_: 1)

    def read(_session, company_id, **kwargs):
        seen["company_id"] = company_id
        seen.update(kwargs)
        return facts

    monkeypatch.setattr(canonical_adapter, "load_canonical_financial_facts", read)
    results, adapted = calculate_stage6_kpis_from_canonical(
        object(), 7, period_id=22, period_end_jalali=(1404, 6, 30),
        cutoff=datetime(2025, 8, 1), bindings=bindings,
    )
    assert seen["company_id"] == 7
    assert seen["report_type_id"] == "PERIODIC_FINANCIAL"
    assert seen["cutoff"] == datetime(2025, 8, 1)
    assert len(results) > 0 and adapted.input_refs
