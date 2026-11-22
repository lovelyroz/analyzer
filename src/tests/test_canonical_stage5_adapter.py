from dataclasses import replace
from datetime import datetime

import pytest

from src.forecast.canonical_adapter import (
    CanonicalMetricBinding, CanonicalReadError, build_stage5_input,
)
from src.forecast.canonical_queries import CanonicalFactAtCutoff
from src.forecast.schema import ForecastInputRef


def _bindings():
    result = {}
    for metric_id, key in enumerate(("REVENUE", "OPERATING_PROFIT", "NET_PROFIT", "TOTAL_EQUITY"), 1):
        temporal = "INSTANT" if key == "TOTAL_EQUITY" else "DURATION"
        result[key] = CanonicalMetricBinding(
            input_key=key, metric_id=metric_id, temporal_type=temporal,
            duration_basis=None if temporal == "INSTANT" else "YTD",
            duration_aggregation=None if temporal == "INSTANT" else "ADDITIVE_YTD",
            source_unit="unit-rial", source_currency="currency-irr",
            source_scale="scale-unit",
        )
    return result


def _fact(metric_id, key, end_month, value, version, *, temporal=None, start_month=1,
          report_type="PERIODIC_FINANCIAL", unit=None, dimensions=()):
    temporal = temporal or ("INSTANT" if key == "TOTAL_EQUITY" else "DURATION")
    return CanonicalFactAtCutoff(
        company_id=1, report_type_id=report_type, metric_id=metric_id,
        period_id=metric_id * 100 + end_month, temporal_type=temporal,
        start_jalali=(1404, end_month, 31 if end_month <= 6 else 30) if temporal == "INSTANT" else (1404, start_month, 1),
        end_jalali=(1404, end_month, 31 if end_month <= 6 else 30),
        duration_basis=None if temporal == "INSTANT" else "YTD",
        value_integer=value, value_state="REPORTED_VALUE", scenario="ACTUAL",
        source_unit=unit or "unit-rial", source_currency="currency-irr",
        source_scale="scale-unit", report_version_id=version,
        publication_datetime=datetime(2025, 1, version), is_audited=True,
        is_restated=False, dimensions=dimensions, source_identity="source",
        revision_identity=str(version), source_coordinate="B2",
    )


def test_stage5_ytd_is_adapted_to_exact_runtime_quarters_with_lineage():
    bindings = _bindings()
    facts = []
    for key in ("REVENUE", "OPERATING_PROFIT", "NET_PROFIT"):
        metric_id = bindings[key].metric_id
        facts.extend([
            _fact(metric_id, key, 3, 100, metric_id * 10 + 1),
            _fact(metric_id, key, 6, 250, metric_id * 10 + 2),
        ])
    facts.append(_fact(bindings["TOTAL_EQUITY"].metric_id, "TOTAL_EQUITY", 6, 900, 44, temporal="INSTANT"))

    adapted = build_stage5_input(facts, bindings, company_id=1, fiscal_year_start_month=1)

    assert adapted.facts["REVENUE"] == 150
    assert type(adapted.facts["REVENUE"]) is int
    assert adapted.facts["TOTAL_EQUITY"] == 900
    assert [period[1] for period in adapted.periods] == [(1404, 3, 31), (1404, 6, 30)]
    assert {ref.report_version_id for ref in adapted.input_refs if ref.fact_key == "REVENUE"} == {11, 12}
    assert all(ref.source == "canonical_financial_facts" for ref in adapted.input_refs)


def test_stage5_rejects_incomplete_or_ambiguous_metric_mapping():
    bindings = _bindings()
    with pytest.raises(CanonicalReadError, match="CANONICAL_STAGE5_MAPPING_INCOMPLETE"):
        build_stage5_input([], {key: value for key, value in bindings.items() if key != "NET_PROFIT"}, company_id=1, fiscal_year_start_month=1)
    bindings["TOTAL_EQUITY"] = CanonicalMetricBinding(
        "TOTAL_EQUITY", 1, "INSTANT", "unit-rial", "currency-irr", "scale-unit",
    )
    with pytest.raises(CanonicalReadError, match="CANONICAL_STAGE5_MAPPING_AMBIGUOUS"):
        build_stage5_input([], bindings, company_id=1, fiscal_year_start_month=1)


def test_stage5_rejects_unit_mismatch_and_does_not_guess_dimension():
    bindings = _bindings()
    bad_unit = [_fact(1, "REVENUE", 3, 100, 1, unit="unit-unknown")]
    with pytest.raises(CanonicalReadError, match="CANONICAL_FACT_METADATA_MISMATCH"):
        build_stage5_input(bad_unit, bindings, company_id=1, fiscal_year_start_month=1)

    scoped = dict(bindings)
    scoped["REVENUE"] = CanonicalMetricBinding(
        "REVENUE", 1, "DURATION", "unit-rial", "currency-irr", "scale-unit",
        dimensions=(("consolidation", "consolidated"),), duration_basis="YTD",
        duration_aggregation="ADDITIVE_YTD",
    )
    result = build_stage5_input([
        _fact(1, "REVENUE", 3, 100, 1),
        _fact(scoped["TOTAL_EQUITY"].metric_id, "TOTAL_EQUITY", 6, 900, 2,
              temporal="INSTANT"),
    ], scoped, company_id=1, fiscal_year_start_month=1)
    assert "REVENUE" not in result.facts


def test_stage5_ignores_other_report_types_and_rejects_non_actual_scenarios():
    bindings = _bindings()
    monthly = _fact(1, "REVENUE", 3, 100, 1, report_type="MONTHLY_ACTIVITY")
    result = build_stage5_input([monthly, _fact(1, "REVENUE", 3, 100, 3)], bindings,
                                company_id=1, fiscal_year_start_month=1)
    assert result.facts["REVENUE"] == 100

    forecast = _fact(1, "REVENUE", 3, 100, 2)
    forecast = CanonicalFactAtCutoff(**{
        name: getattr(forecast, name) for name in forecast.__dataclass_fields__
        if name != "scenario"
    }, scenario="FORECAST")
    with pytest.raises(CanonicalReadError, match="CANONICAL_SCENARIO_UNSUPPORTED"):
        build_stage5_input([forecast], bindings, company_id=1, fiscal_year_start_month=1)


def test_stage5_requires_explicit_additive_ytd_declaration():
    bindings = _bindings()
    bindings["NET_PROFIT"] = CanonicalMetricBinding(
        "NET_PROFIT", 3, "DURATION", "unit-rial", "currency-irr", "scale-unit",
        duration_basis="YTD",
    )
    with pytest.raises(CanonicalReadError, match="CANONICAL_YTD_AGGREGATION_UNAPPROVED"):
        build_stage5_input([], bindings, company_id=1, fiscal_year_start_month=1)


def test_stage5_keeps_latest_reported_null_period_missing_instead_of_using_older_quarter():
    bindings = _bindings()
    missing_q2 = replace(
        _fact(1, "REVENUE", 6, None, 2), value_state="REPORTED_NULL",
    )
    adapted = build_stage5_input(
        [_fact(1, "REVENUE", 3, 100, 1), missing_q2],
        bindings, company_id=1, fiscal_year_start_month=1,
    )
    assert adapted.periods[-1][1] == (1404, 6, 30)
    assert adapted.facts == {}
    assert any(ref.report_version_id == 2 for ref in adapted.input_refs)


def test_stage5_rejects_cross_company_fact_rows():
    with pytest.raises(CanonicalReadError, match="CANONICAL_COMPANY_MISMATCH"):
        build_stage5_input(
            [_fact(1, "REVENUE", 3, 100, 1)], _bindings(), company_id=2,
            fiscal_year_start_month=1,
        )


def test_stage5_rejects_inconsistent_units_and_ytd_period_starts():
    bindings = _bindings()
    bindings["NET_PROFIT"] = CanonicalMetricBinding(
        "NET_PROFIT", 3, "DURATION", "unit-thousand-rial", "currency-irr",
        "scale-unit", duration_basis="YTD", duration_aggregation="ADDITIVE_YTD",
    )
    with pytest.raises(CanonicalReadError, match="CANONICAL_STAGE5_UNIT_CONTRACT_INCONSISTENT"):
        build_stage5_input([], bindings, company_id=1, fiscal_year_start_month=1)

    bindings = _bindings()
    facts = [
        _fact(1, "REVENUE", 3, 100, 1),
        _fact(2, "OPERATING_PROFIT", 3, 20, 2, start_month=2),
    ]
    with pytest.raises(CanonicalReadError, match="CANONICAL_STAGE5_PERIOD_MISMATCH"):
        build_stage5_input(facts, bindings, company_id=1, fiscal_year_start_month=1)


def test_stage5_uses_configured_company_fiscal_start_month():
    bindings = _bindings()
    fact = _fact(1, "REVENUE", 9, 100, 1, start_month=7)
    adapted = build_stage5_input(
        [fact], bindings, company_id=1, fiscal_year_start_month=7,
    )
    assert adapted.facts["REVENUE"] == 100

    with pytest.raises(CanonicalReadError, match="CANONICAL_STAGE5_YTD_PERIOD_INVALID"):
        build_stage5_input(
            [_fact(1, "REVENUE", 9, 100, 1, start_month=1)],
            bindings, company_id=1, fiscal_year_start_month=7,
        )


def test_generate_forecast_canonical_opt_in_never_reads_legacy_financial_facts(monkeypatch):
    from src.forecast import service
    from src.forecast.canonical_adapter import CanonicalStage5Input

    bindings = _bindings()
    adapted = CanonicalStage5Input(
        facts={"REVENUE": 100, "OPERATING_PROFIT": 20, "NET_PROFIT": 10},
        input_refs=(ForecastInputRef("REVENUE", 1, datetime(2025, 1, 1), "canonical_financial_facts"),),
        periods=((1, (1404, 3, 31),
                  {"REVENUE": 100, "OPERATING_PROFIT": 20, "NET_PROFIT": 10},
                  (ForecastInputRef("REVENUE", 1, datetime(2025, 1, 1), "canonical_financial_facts"),)),),
    )
    monkeypatch.setattr(service, "load_industry_code", lambda *_: "BANK")
    monkeypatch.setattr(service, "load_share_history", lambda *_args, **_kwargs: pytest.fail("legacy read"))
    monkeypatch.setattr(service, "load_financial_facts", lambda *_args, **_kwargs: pytest.fail("legacy read"))
    monkeypatch.setattr(service, "load_financial_fact_periods", lambda *_args, **_kwargs: pytest.fail("legacy read"))
    monkeypatch.setattr("src.forecast.canonical_adapter.load_stage5_input", lambda *_args, **_kwargs: adapted)
    monkeypatch.setattr(
        service.ForecastEngine, "generate_forecast",
        lambda _self, *args, **_kwargs: args[3],
    )

    result = service.generate_forecast(
        object(), 7, 88, trend_result=None,
        data_cutoff_datetime=datetime(2025, 2, 1),
        canonical_metric_bindings=bindings,
    )

    assert result["recent_run_rate_revenue"] == 100
    assert result["forecast_weighted_average_shares"] is None
    assert result["input_refs"][0].source == "canonical_financial_facts"


def test_generate_forecast_canonical_failure_does_not_fall_back_to_legacy(monkeypatch):
    from src.forecast import service

    monkeypatch.setattr(service, "load_industry_code", lambda *_: "BANK")
    monkeypatch.setattr(service, "load_financial_facts", lambda *_args, **_kwargs: pytest.fail("legacy fallback"))
    monkeypatch.setattr(service, "load_financial_fact_periods", lambda *_args, **_kwargs: pytest.fail("legacy fallback"))

    def fail_canonical(*_args, **_kwargs):
        raise CanonicalReadError("CANONICAL_FACTS_MISSING")

    monkeypatch.setattr("src.forecast.canonical_adapter.load_stage5_input", fail_canonical)
    with pytest.raises(CanonicalReadError, match="CANONICAL_FACTS_MISSING"):
        service.generate_forecast(
            object(), 7, 88, trend_result=None,
            data_cutoff_datetime=datetime(2025, 2, 1),
            canonical_metric_bindings=_bindings(),
        )
