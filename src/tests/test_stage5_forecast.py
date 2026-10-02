from dataclasses import dataclass, replace
from datetime import date, datetime, timedelta, timezone
from typing import Optional

import pytest

from src.forecast.drivers import ForecastDriver
from src.forecast.engine import ForecastEngine
from src.forecast.schema import (
    CompanyForecastResult,
    ForecastInputRef,
    ForecastRecord,
    ForecastVersionExistsError,
    ForecastVersionStore,
    ScenarioForecastResult,
    SingleForecastChain,
    filter_pit_inputs,
    normalize_datetime,
)


def _context(**overrides):
    base = {
        "seasonality_valid": True,
        "seasonal_baseline_revenue": 10000.0,
        "recent_run_rate_revenue": 9000.0,
        "baseline_revenue_growth": 0.10,
        "historical_operating_margin": 0.20,
        "historical_net_margin": 0.10,
        "share_count": 1000.0,
    }
    base.update(overrides)
    return base


CONTEXT_KEYS = {
    "input_refs", "calculation_timestamp", "share_count",
    "beginning_equity", "forecast_ending_equity", "baseline_revenue_growth",
    "seasonality_valid", "seasonal_baseline_revenue", "recent_run_rate_revenue",
    "historical_operating_margin", "historical_net_margin",
    "low_base", "sign_change",
}


def _forecast(**overrides):
    """Build a forecast, routing context keys into ``financial_context``."""
    context = _context()
    engine_kwargs = {}
    for key, value in overrides.items():
        if key in CONTEXT_KEYS:
            context[key] = value
        else:
            engine_kwargs[key] = value
    engine_kwargs.setdefault("company_id", 1)
    engine_kwargs.setdefault("forecast_period_id", 101)
    engine_kwargs.setdefault("industry_code", "PETROCHEMICAL")
    engine_kwargs.setdefault(
        "data_cutoff_datetime", datetime(2026, 1, 1, tzinfo=timezone.utc)
    )
    engine_kwargs["financial_context"] = context
    return ForecastEngine().generate_forecast(**engine_kwargs)


def test_forecast_driver_general_chain():
    chain = ForecastDriver.build_general_chain(
        base_revenue=1000.0,
        growth_rate=0.10,
        operating_margin=20.0,
        net_margin=15.0,
        share_count=100.0,
    )
    assert chain.revenue == 1100.0
    assert chain.operating_profit == 220.0
    assert chain.net_profit == 165.0
    assert chain.eps == 1.65


def test_stage5_uses_seasonal_baseline_and_parameterized_trend():
    engine = ForecastEngine()
    context = {
        "seasonality_valid": True,
        "seasonal_baseline_revenue": 10000.0,
        "recent_run_rate_revenue": 9000.0,
        "baseline_revenue_growth": 0.20,
        "historical_operating_margin": 0.20,
        "historical_net_margin": 0.10,
        "share_count": 1000.0,
        "model_parameters": {
            "trend_adjustments": {"Strong Improvement": 0.05},
            "scenario_revenue_growth_spread": 0.05,
        },
    }

    result = engine.generate_forecast(
        company_id=1,
        forecast_period_id=101,
        industry_code="PETROCHEMICAL",
        financial_context=context,
        trend_state="Strong Improvement",
        horizon="12M",
        data_cutoff_datetime=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )

    assert result.baseline_method == "SEASONAL_BASELINE"
    assert result.horizon == "12M"
    assert result.scenario_forecasts.base.revenue == 12500.0
    assert result.scenario_forecasts.base.eps == 1.25
    assert result.scenario_forecasts.bear.eps < result.scenario_forecasts.base.eps
    assert result.scenario_forecasts.base.eps < result.scenario_forecasts.bull.eps


def test_low_base_disables_trend_adjustment():
    engine = ForecastEngine()
    context = {
        "seasonality_valid": True,
        "seasonal_baseline_revenue": 1000.0,
        "baseline_revenue_growth": 0.10,
        "historical_operating_margin": 0.20,
        "historical_net_margin": 0.10,
        "share_count": 100.0,
        "low_base": True,
        "model_parameters": {
            "trend_adjustments": {"Strong Improvement": 0.50},
            "scenario_revenue_growth_spread": 0.05,
        },
    }
    result = engine.generate_forecast(
        1, 101, "CEMENT", context, trend_state="Strong Improvement"
    )
    assert result.scenario_forecasts.base.revenue == 1100.0


def test_component_based_net_profit_has_priority_and_roe():
    chain = ForecastDriver.build_non_financial_chain(
        revenue=1000.0,
        operating_margin=0.20,
        share_count=100.0,
        non_operating_items=20.0,
        financial_costs=10.0,
        tax=30.0,
        net_margin=0.01,
        beginning_equity=400.0,
        ending_equity=600.0,
    )
    assert chain.method == "COMPONENT_BASED"
    assert chain.net_profit == 180.0
    assert chain.eps == 1.8
    assert chain.roe == 0.36


def test_missing_core_data_falls_back_to_insufficient_data():
    result = ForecastEngine().generate_forecast(
        1,
        101,
        "FOOD",
        {"share_count": 1000.0},
    )
    assert result.baseline_method == "INSUFFICIENT_DATA"
    assert result.data_quality == "INSUFFICIENT_DATA"
    assert result.scenario_forecasts.base.method == "INSUFFICIENT_DATA"


def test_bank_specialized_core_does_not_use_general_revenue_model():
    context = {
        "base_nii": 1000.0,
        "baseline_nii_growth": 0.10,
        "bank_net_profit_nii_conversion": 0.50,
        "share_count": 100.0,
        "model_parameters": {"scenario_financial_growth_spread": 0.05},
    }
    result = ForecastEngine().generate_forecast(1, 10, "BANK", context)
    assert result.baseline_method == "BANK_SPECIALIZED"
    assert result.scenario_forecasts.base.net_profit == 550.0
    assert result.scenario_forecasts.base.eps == 5.5


def test_holding_core_excludes_p_nav():
    context = {
        "base_nav": 2000.0,
        "baseline_nav_growth": 0.10,
        "holding_net_profit_nav_conversion": 0.20,
        "share_count": 100.0,
    }
    result = ForecastEngine().generate_forecast(1, 10, "HOLDING", context)
    assert result.baseline_method == "HOLDING_SPECIALIZED"
    assert result.scenario_forecasts.base.net_profit == 440.0
    assert result.scenario_forecasts.base.eps == 4.4
    assert "p_nav" not in result.scenario_forecasts.base.assumptions


def test_unsupported_horizon_and_industry_are_rejected():
    engine = ForecastEngine()
    with pytest.raises(ValueError):
        engine.generate_forecast(1, 1, "FOOD", {}, horizon="2Y")
    with pytest.raises(ValueError):
        engine.generate_forecast(1, 1, "INSURANCE", {})


# --------------------------------------------------------------------------
# Forecast record schema
# --------------------------------------------------------------------------

def test_record_schema_carries_all_contract_fields():
    result = _forecast()
    record = result.to_record("base", forecast_id=7)
    assert isinstance(record, ForecastRecord)
    assert record.forecast_id == 7
    assert record.forecast_version == 0  # assigned on store, never at build
    assert record.company_id == 1
    assert record.forecast_period_id == 101
    assert record.forecast_horizon == "12M"
    assert record.scenario == "BASE"
    assert record.model_version == "V1.0"
    assert record.forecast_method == result.scenario_forecasts.base.method
    assert record.data_quality == result.scenario_forecasts.base.quality
    assert record.baseline_method == "SEASONAL_BASELINE"
    assert record.data_cutoff_datetime == datetime(2026, 1, 1, tzinfo=timezone.utc)
    assert record.data_cutoff_datetime.tzinfo is not None
    assert record.input_refs == ()


def test_records_freeze_all_three_scenarios():
    records = _forecast().records(forecast_id_start=100)
    assert [r.scenario for r in records] == ["BEAR", "BASE", "BULL"]
    assert [r.forecast_id for r in records] == [100, 101, 102]
    assert all(r.forecast_horizon == "12M" for r in records)
    assert records[0].eps < records[1].eps < records[2].eps
    # Every chain knows its own scenario identity.
    chains = _forecast().scenario_forecasts
    assert chains.base.scenario == "BASE"
    assert chains.bear.scenario == "BEAR"
    assert chains.bull.scenario == "BULL"
    assert chains.base.forecast_horizon == "12M"


def test_horizon_and_timestamp_are_recorded_per_forecast():
    result = _forecast(horizon="6M",
                       data_cutoff_datetime=datetime(2026, 6, 30, tzinfo=timezone.utc))
    record = result.to_record("base", forecast_id=1)
    assert record.forecast_horizon == "6M"
    assert record.forecast_timestamp == result.calculation_timestamp
    assert record.data_cutoff_datetime == datetime(2026, 6, 30, tzinfo=timezone.utc)
    assert record.forecast_timestamp >= record.data_cutoff_datetime


def test_missing_metric_is_none_not_zero():
    # No share count and no equity: EPS/ROE are genuinely unknown.
    result = ForecastEngine().generate_forecast(
        1, 101, "FOOD",
        _context(**{"share_count": None, "beginning_equity": None,
                    "forecast_ending_equity": None}),
        horizon="3M",
    )
    record = result.to_record("base", forecast_id=1)
    assert record.revenue is not None
    assert record.forecast_horizon == "3M"
    assert record.is_missing("roe") is True
    assert record.is_missing("eps") is True
    # Missing is never silently coerced to a zero in the stored record.
    assert record.eps is None
    assert record.roe is None
    assert not record.is_missing("revenue")


def test_naive_cutoff_datetime_is_assumed_utc():
    result = _forecast(data_cutoff_datetime=datetime(2026, 1, 1))
    record = result.to_record("base", forecast_id=1)
    assert record.data_cutoff_datetime.tzinfo is not None
    assert record.data_cutoff_datetime == datetime(2026, 1, 1, tzinfo=timezone.utc)


def test_calculation_timestamp_before_cutoff_is_rejected():
    with pytest.raises(ValueError):
        ForecastEngine().generate_forecast(
            1, 101, "PETROCHEMICAL",
            _context(calculation_timestamp=datetime(2025, 1, 1, tzinfo=timezone.utc)),
            data_cutoff_datetime=datetime(2026, 1, 1, tzinfo=timezone.utc),
        )


# --------------------------------------------------------------------------
# Input auditability
# --------------------------------------------------------------------------

def test_input_refs_are_recorded_for_auditability():
    refs = [
        ForecastInputRef("revenue_seasonal", report_version_id=42,
                         available_at=datetime(2025, 12, 1, tzinfo=timezone.utc), source="ReportVersion"),
        ForecastInputRef("operating_margin", report_version_id=42,
                         available_at=datetime(2025, 12, 5, tzinfo=timezone.utc)),
    ]
    result = _forecast(input_refs=refs)
    assert result.assumptions["pit_valid"] is True
    assert "pit_violation" not in result.assumptions
    record = result.to_record("base", forecast_id=1, input_refs=refs)
    assert [r.fact_key for r in record.input_refs] == ["revenue_seasonal", "operating_margin"]
    assert record.input_refs[0].report_version_id == 42
    assert record.input_refs[0].available_at.year == 2025


def test_input_refs_accept_mapping_form():
    result = _forecast(input_refs=[
        {"fact_key": "share_count", "report_version_id": 7,
         "available_at": "2025-11-01T00:00:00+00:00"},
    ])
    assert result.assumptions["input_refs"][0]["fact_key"] == "share_count"
    assert result.assumptions["input_refs"][0]["report_version_id"] == 7


def test_input_ref_without_publication_date_is_never_rejected():
    ref = ForecastInputRef("undated_input")
    assert ref.available_at is None
    result = _forecast(input_refs=[ref])
    assert result.assumptions["pit_valid"] is True
    assert "pit_violation" not in result.assumptions


def test_malformed_input_ref_is_rejected():
    with pytest.raises(ValueError):
        _forecast(input_refs=[{"report_version_id": 7}])
    with pytest.raises(ValueError):
        _forecast(input_refs=["revenue"])


# --------------------------------------------------------------------------
# Version preservation and no-overwrite semantics
# --------------------------------------------------------------------------

def test_version_store_appends_and_never_overwrites():
    store = ForecastVersionStore()
    base = _forecast()
    # August, September, October forecasts for the same series (spec §24).
    for i, eps in enumerate((1100.0, 1180.0, 1270.0)):
        result = _forecast()
        result.calculation_timestamp = datetime(2026, 8 + i, 1, tzinfo=timezone.utc)
        result.scenario_forecasts.base.eps = eps
        record = store.save(result.to_record("base", forecast_id=i + 1))
        assert record.forecast_version == i + 1

    history = store.history(1, 101, "12M", "BASE")
    assert len(history) == 3
    assert [r.forecast_version for r in history] == [1, 2, 3]
    # Every version survives; none was replaced.
    assert [r.eps for r in history] == [1100.0, 1180.0, 1270.0]
    assert store.latest(1, 101, "12M", "BASE").eps == 1270.0
    assert history[0].eps == 1100.0


def test_revised_forecast_keeps_the_older_version():
    store = ForecastVersionStore()
    store.save(_forecast().to_record("base", forecast_id=1))

    revised = _forecast()
    revised.scenario_forecasts.base.eps = 999.0
    store.save(revised.to_record("base", forecast_id=2))

    history = store.history(1, 101, "12M", "BASE")
    assert len(history) == 2
    assert history[0].eps != 999.0  # the original survived
    assert history[1].eps == 999.0


def test_identical_resave_is_idempotent():
    store = ForecastVersionStore()
    record = _forecast(**{
        "calculation_timestamp": datetime(2026, 1, 1, tzinfo=timezone.utc)
    }).to_record("base", forecast_id=1)
    store.save(record)
    same = store.save(record)
    assert same.forecast_version == 1
    assert store.count() == 1
    assert store.latest(1, 101, "12M", "BASE").forecast_version == 1


def test_explicit_version_collision_is_rejected():
    store = ForecastVersionStore()
    store.save(_forecast().to_record("base", forecast_id=1))
    different = _forecast()
    different.scenario_forecasts.base.eps = 5.0
    with pytest.raises(ForecastVersionExistsError):
        store.save(different.to_record("base", forecast_id=1).__class__(
            forecast_id=1, forecast_version=1,
            company_id=1, forecast_period_id=101, industry_code="PETROCHEMICAL",
            forecast_horizon="12M", scenario="BASE",
            forecast_timestamp=datetime(2026, 1, 1, tzinfo=timezone.utc),
            data_cutoff_datetime=datetime(2026, 1, 1, tzinfo=timezone.utc),
            model_version="V1.0", forecast_method="RUN_RATE", data_quality="MEDIUM",
            baseline_method="SEASONAL_BASELINE",
            revenue=None, operating_profit=None, operating_margin=None,
            net_profit=5.0, eps=5.0, roe=None,
        ))


def test_revision_trend_reports_direction():
    store = ForecastVersionStore()
    for i, eps in enumerate((1100.0, 1180.0, 1270.0)):
        result = _forecast()
        result.scenario_forecasts.base.eps = eps
        store.save(result.to_record("base", forecast_id=i + 1))
    assert store.revision_trend(1, 101, "12M", "BASE") == "UPWARD"

    store2 = ForecastVersionStore()
    for i, eps in enumerate((1270.0, 1180.0, 1100.0)):
        result = _forecast()
        result.scenario_forecasts.base.eps = eps
        store2.save(result.to_record("base", forecast_id=i + 1))
    assert store2.revision_trend(1, 101, "12M", "BASE") == "DOWNWARD"

    store3 = ForecastVersionStore()
    store3.save(_forecast().to_record("base", forecast_id=1))
    assert store3.revision_trend(1, 101, "12M", "BASE") is None


def test_scenarios_are_separate_series():
    store = ForecastVersionStore()
    for scenario in ("bear", "base", "bull"):
        store.save(_forecast().to_record(scenario, forecast_id=1))
    assert store.count() == 3
    assert len(store.history(1, 101, "12M", "BEAR")) == 1
    assert len(store.history(1, 101, "12M", "BASE")) == 1
    assert len(store.history(1, 101, "12M", "BULL")) == 1


# --------------------------------------------------------------------------
# Point-in-Time protection
# --------------------------------------------------------------------------

def test_filter_pit_inputs_drops_future_information():
    refs = [
        ForecastInputRef("old", available_at=datetime(2025, 1, 1, tzinfo=timezone.utc)),
        ForecastInputRef("future", available_at=datetime(2026, 6, 1, tzinfo=timezone.utc)),
    ]
    cutoff = datetime(2026, 1, 1, tzinfo=timezone.utc)
    available, dropped = filter_pit_inputs(refs, cutoff)
    assert [r.fact_key for r in available] == ["old"]
    assert [r.fact_key for r in dropped] == ["future"]


def test_future_input_is_flagged_not_silently_used():
    result = _forecast(input_refs=[
        ForecastInputRef("q4_report", report_version_id=99,
                         available_at=datetime(2026, 6, 1, tzinfo=timezone.utc)),
    ])
    assert result.assumptions["pit_valid"] is False
    violation = result.assumptions["pit_violation"]
    assert violation["fact_key"] == "q4_report"
    assert violation["available_at"].startswith("2026-06-01")
    assert violation["action"] == "input_dropped"
    assert all(r["fact_key"] != "q4_report"
               for r in result.assumptions["input_refs"])


def test_read_at_cutoff_hides_forecasts_built_on_later_data():
    store = ForecastVersionStore()
    store.save(_forecast(
        input_refs=[ForecastInputRef("base_report",
                                     available_at=datetime(2025, 6, 1, tzinfo=timezone.utc))],
    ).to_record("base", forecast_id=1))

    # A September rebuild that secretly saw the October report.
    late = _forecast(
        data_cutoff_datetime=datetime(2026, 9, 1, tzinfo=timezone.utc),
        input_refs=[ForecastInputRef("october_report",
                                     available_at=datetime(2026, 10, 5, tzinfo=timezone.utc))],
    )
    store.save(late.to_record("base", forecast_id=2))

    assert store.read_at_cutoff(
        1, 101, "12M", "BASE", datetime(2026, 8, 1, tzinfo=timezone.utc)
    ).forecast_version == 1
    # Reading at the September cutoff falls back to the clean January record,
    # never to the one built from the October report.
    visible = store.read_at_cutoff(
        1, 101, "12M", "BASE", datetime(2026, 9, 15, tzinfo=timezone.utc)
    )
    assert visible is not None
    assert visible.forecast_version == 1
    assert [r.fact_key for r in visible.input_refs] == ["base_report"]
    assert store.latest(1, 101, "12M", "BASE").forecast_version == 2
    # The late record is flagged as contaminated at its own cutoff.
    contaminated = store.pit_violations(datetime(2026, 9, 1, tzinfo=timezone.utc))
    assert [r.forecast_version for r in contaminated] == [2]
    assert contaminated[0].input_refs[0].fact_key == "october_report"
    # Reading strictly before the September cutoff sees no contamination.
    assert store.pit_violations(datetime(2026, 8, 1, tzinfo=timezone.utc)) == []


def test_read_at_cutoff_returns_none_when_nothing_available():
    store = ForecastVersionStore()
    assert store.read_at_cutoff(1, 101, "12M", "BASE",
                                datetime(2026, 1, 1, tzinfo=timezone.utc)) is None


def test_pit_violations_are_detectable_across_the_store():
    store = ForecastVersionStore()
    store.save(_forecast(
        input_refs=[ForecastInputRef("late", available_at=datetime(2027, 1, 1, tzinfo=timezone.utc))],
    ).to_record("base", forecast_id=1))
    violations = store.pit_violations(datetime(2026, 1, 1, tzinfo=timezone.utc))
    assert len(violations) == 1
    assert violations[0].forecast_version == 1
    assert store.pit_violations(datetime(2027, 6, 1, tzinfo=timezone.utc)) == []


def test_cutoff_timezone_normalization_is_consistent():
    store = ForecastVersionStore()
    store.save(_forecast(
        data_cutoff_datetime=datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc),
    ).to_record("base", forecast_id=1))
    # A +03:30 cutoff equal to the UTC cutoff resolves the same record.
    same_instant = datetime(2026, 1, 1, 15, 30,
                            tzinfo=timezone(timedelta(hours=3, minutes=30)))
    record = store.read_at_cutoff(1, 101, "12M", "BASE", same_instant)
    assert record is not None
    assert record.forecast_version == 1


def test_normalize_datetime_contracts():
    assert normalize_datetime(None) is None
    naive = normalize_datetime(datetime(2026, 1, 1))
    assert naive == datetime(2026, 1, 1, tzinfo=timezone.utc)
    assert naive.tzinfo is not None


# ==========================================================================
# Stage 4 adapter and weighted average shares (Prompt 3)
# ==========================================================================

from src.forecast.adapter import (  # noqa: E402
    Stage4Context,
    adapt_stage4,
    build_financial_context,
)
from src.forecast.builder import (  # noqa: E402
    WeightedAverageShares,
    build_weighted_average_shares,
)
from src.trend.schema import (  # noqa: E402
    ContextFlags,
    HistoricalResult,
    MomentumResult,
    PeriodComparison,
    SeasonalResult,
    TrendResult,
)


@dataclass
class _ShareRecord:
    effective_date: "date"
    shares_outstanding: int


@dataclass
class _CorporateAction:
    action_type: str
    effective_date: "date"
    announcement_date: Optional["date"] = None
    old_share_count: Optional[int] = None
    new_share_count: Optional[int] = None
    ratio: Optional[float] = None


def _stage4(
    *,
    trend_state: str = "Stable",
    coverage: str = "FULL",
    seasonal_baseline: Optional[float] = 12000.0,
    seasonal_sufficiency: str = "FULL",
    seasonal_observations: int = 5,
    momentum_pct: Optional[float] = 0.08,
    momentum_direction: Optional[str] = "Positive",
    low_base: Optional[bool] = False,
    sign_change: Optional[str] = None,
    data_sufficiency: str = "FULL",
    trend_confidence: Optional[str] = "HIGH",
    same_period_flags: tuple = (),
) -> TrendResult:
    return TrendResult(
        company_id=1,
        period_id=101,
        metric_code="REVENUE",
        trend_state=trend_state,
        coverage=coverage,
        low_base_flag=low_base,
        sign_change_flag=bool(sign_change),
        comparisons={},
        calculation_timestamp=datetime(2025, 12, 1, tzinfo=timezone.utc),
        historical=HistoricalResult(
            same_period_detail=[
                PeriodComparison(label=f"Y{i}", pct_change=None, flag=flag)
                for i, flag in enumerate(same_period_flags)
            ],
            sufficiency=data_sufficiency,
        ),
        seasonal=SeasonalResult(
            baseline=seasonal_baseline,
            data_sufficiency=seasonal_sufficiency,
            observation_count=seasonal_observations,
        ),
        momentum={
            "12M": MomentumResult(
                pct_change=momentum_pct,
                direction=momentum_direction,
                relative_strength="Normal",
                status="VALID",
            ),
        },
        context=ContextFlags(
            low_base=low_base,
            sign_change=sign_change,
            data_sufficiency=data_sufficiency,
        ),
        trend_coverage=coverage,
        trend_confidence=trend_confidence,
    )


# --- 1. Stage 4 output -> Stage 5 context mapping --------------------------

def test_stage4_adapter_maps_core_fields_without_recalculating():
    result = _stage4()
    context = adapt_stage4(
        result,
        seasonal_baseline_revenue=12000.0,
        seasonal_naive_revenue=11800.0,
        recent_run_rate_revenue=11500.0,
    )
    assert context.trend_state == "Stable"
    assert context.coverage == "FULL"
    assert context.seasonality_valid is True
    assert context.seasonal_baseline_revenue == 12000.0
    assert context.seasonal_naive_revenue == 11800.0
    assert context.recent_run_rate_revenue == 11500.0
    # Provenance carries the Stage 4 coordinates so the forecast stays auditable.
    assert context.provenance["stage"] == "STAGE_4"
    assert context.provenance["metric_code"] == "REVENUE"
    assert context.provenance["seasonal_observations"] == 5


def test_stage4_adapter_output_drives_the_engine():
    result = _stage4(trend_state="Improving")
    context = build_financial_context(
        result,
        {
            "historical_operating_margin": 0.20,
            "historical_net_margin": 0.10,
            "share_count": 1000.0,
            "baseline_revenue_growth": 0.10,
            "model_parameters": {
                "trend_adjustments": {"Improving": 0.02},
                "scenario_revenue_growth_spread": 0.05,
            },
        },
        seasonal_baseline_revenue=12000.0,
        seasonal_naive_revenue=11800.0,
        recent_run_rate_revenue=11500.0,
    )
    forecast = ForecastEngine().generate_forecast(
        1, 101, "PETROCHEMICAL", context,
        data_cutoff_datetime=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )
    # Seasonality is valid, so the seasonal baseline wins over the run rate.
    assert forecast.baseline_method == "SEASONAL_BASELINE"
    assert forecast.scenario_forecasts.base.revenue == pytest.approx(13440.0)
    assert forecast.scenario_forecasts.base.method == "MARGIN"


# --- 2. seasonal baseline mapping -----------------------------------------

def test_seasonal_baseline_requires_stage4_sufficiency():
    # Stage 4 says there are not enough same-period observations, so the
    # seasonal baseline must not outrank the run rate.
    result = _stage4(seasonal_sufficiency="INSUFFICIENT_DATA", seasonal_observations=1)
    context = adapt_stage4(result)
    assert context.seasonality_valid is False
    assert context.seasonal_data_sufficiency == "INSUFFICIENT_DATA"


def test_seasonal_baseline_surprise_is_not_converted_to_growth():
    result = _stage4(momentum_pct=0.25)
    context = adapt_stage4(result)
    # Momentum is carried as evidence only; nothing in the context is a growth rate.
    assert context.momentum_12m_pct == 0.25
    assert "growth" not in str(context.to_dict()).lower().replace("growth_spread", "")


# --- 3. recent run-rate mapping -------------------------------------------

def test_run_rate_is_carried_verbatim():
    result = _stage4(seasonal_sufficiency="INSUFFICIENT_DATA", seasonal_observations=1)
    context = adapt_stage4(result, recent_run_rate_revenue=9000.0)
    assert context.recent_run_rate_revenue == 9000.0
    built = build_financial_context(result, {"share_count": 1000.0},
                                    recent_run_rate_revenue=9000.0)
    built["historical_operating_margin"] = 0.20
    built["historical_net_margin"] = 0.10
    forecast = ForecastEngine().generate_forecast(1, 101, "FOOD", built)
    assert forecast.baseline_method == "RUN_RATE"
    assert forecast.scenario_forecasts.base.revenue == pytest.approx(9000.0)


# --- 4. Low Base propagation ----------------------------------------------

def test_low_base_propagates_and_disables_trend_adjustment():
    result = _stage4(trend_state="Strong Improvement", low_base=True)
    context = adapt_stage4(result)
    assert context.low_base is True
    built = build_financial_context(result, {
        "historical_operating_margin": 0.20,
        "historical_net_margin": 0.10,
        "share_count": 100.0,
        "seasonal_baseline_revenue": 1000.0,
        "baseline_revenue_growth": 0.10,
        "model_parameters": {
            "trend_adjustments": {"Strong Improvement": 0.50},
            "scenario_revenue_growth_spread": 0.05,
        },
    })
    forecast = ForecastEngine().generate_forecast(1, 101, "CEMENT", built)
    # The huge trend adjustment is suppressed; only the declared growth applies.
    assert forecast.scenario_forecasts.base.revenue == pytest.approx(1100.0)
    assert forecast.assumptions["low_base"] is True


# --- 5. Sign Change propagation -------------------------------------------

def test_sign_change_propagates_from_stage4_context():
    result = _stage4(sign_change="LOSS_TO_PROFIT", momentum_pct=4.0)
    context = adapt_stage4(result)
    assert context.sign_change == "LOSS_TO_PROFIT"
    built = build_financial_context(result, {"share_count": 100.0})
    forecast = ForecastEngine().generate_forecast(1, 101, "FOOD", built)
    assert forecast.assumptions["sign_change"] == "LOSS_TO_PROFIT"


def test_sign_change_propagates_from_layer_flags_without_context():
    # No Layer-4 context block: the adapter falls back to Layer 1/2 flags.
    result = _stage4(sign_change=None, same_period_flags=("SIGN_CHANGE",))
    result.context = None
    context = adapt_stage4(result)
    assert context.sign_change == "SIGN_CHANGE"


# --- 6. no Stage 4 recalculation ------------------------------------------

def test_adapter_does_not_recompute_stage4_quantities():
    result = _stage4(momentum_pct=0.08)
    context = adapt_stage4(result)
    # The adapter must preserve Stage 4's own numbers, never recompute them.
    assert context.momentum_12m_pct == 0.08
    assert context.trend_direction == "Positive"
    assert context.trend_state == result.trend_state
    # Stage 4's momentum percentage is never turned into a forecast growth rate.
    built = build_financial_context(
        result, {"historical_operating_margin": 0.20, "historical_net_margin": 0.10,
                 "share_count": 1000.0, "seasonal_baseline_revenue": 10000.0},
    )
    forecast = ForecastEngine().generate_forecast(1, 101, "PETROCHEMICAL", built)
    assert forecast.scenario_forecasts.base.revenue == pytest.approx(10000.0)


# --- 7. unchanged share count ---------------------------------------------

def test_weighted_shares_unchanged_single_observation():
    history = [_ShareRecord(date(2025, 1, 1), 1_000_000)]
    result = build_weighted_average_shares(history, cutoff=date(2026, 1, 1))
    assert result.shares == pytest.approx(1_000_000)
    assert result.basis == "UNADJUSTED"
    assert result.applied_actions == []


def test_weighted_shares_unchanged_across_observation_history():
    history = [
        _ShareRecord(date(2025, 1, 1), 1_000_000),
        _ShareRecord(date(2025, 7, 1), 1_000_000),
    ]
    result = build_weighted_average_shares(history, cutoff=date(2026, 1, 1))
    assert result.shares == pytest.approx(1_000_000)


# --- 8. capital increase ---------------------------------------------------

def test_weighted_shares_capital_increase_extends_series():
    history = [_ShareRecord(date(2025, 1, 1), 1_000_000)]
    actions = [
        _CorporateAction("CAPITAL_INCREASE", date(2025, 7, 1),
                         old_share_count=1_000_000, new_share_count=1_500_000,
                         ratio=0.5),
    ]
    result = build_weighted_average_shares(history, actions, cutoff=date(2026, 1, 1))
    assert result.shares is not None
    # 1M for 181 days, 1.5M for 184 days -> about 1.252M
    assert 1_240_000 < result.shares < 1_262_000
    assert result.basis == "WEIGHTED_AVERAGE"
    assert result.applied_actions == ["CAPITAL_INCREASE@2025-07-01"]


# --- 9. corporate action / split ------------------------------------------

def test_weighted_shares_stock_split_uses_ratio_when_counts_absent():
    history = [_ShareRecord(date(2025, 1, 1), 1_000_000)]
    actions = [_CorporateAction("STOCK_SPLIT", date(2025, 7, 1), ratio=2.0)]
    result = build_weighted_average_shares(history, actions, cutoff=date(2026, 1, 1))
    assert result.shares is not None
    assert 1_490_000 < result.shares < 1_510_000
    assert result.applied_actions == ["STOCK_SPLIT@2025-07-01"]


def test_weighted_shares_capital_decrease_uses_new_count():
    history = [_ShareRecord(date(2025, 1, 1), 1_000_000)]
    actions = [
        _CorporateAction("CAPITAL_DECREASE", date(2025, 7, 1),
                         new_share_count=800_000),
    ]
    result = build_weighted_average_shares(history, actions, cutoff=date(2026, 1, 1))
    assert result.shares is not None
    assert 890_000 < result.shares < 910_000


# --- 10. cutoff-aware share calculation ------------------------------------

def test_action_after_cutoff_does_not_affect_the_forecast():
    history = [_ShareRecord(date(2025, 1, 1), 1_000_000)]
    actions = [
        _CorporateAction("CAPITAL_INCREASE", date(2026, 6, 1),
                         new_share_count=2_000_000),
    ]
    result = build_weighted_average_shares(history, actions, cutoff=date(2026, 1, 1))
    assert result.shares == pytest.approx(1_000_000)
    assert result.applied_actions == []


def test_action_effective_before_cutoff_but_announced_after_is_ignored():
    history = [_ShareRecord(date(2025, 1, 1), 1_000_000)]
    actions = [
        _CorporateAction("CAPITAL_INCREASE", date(2025, 7, 1),
                         announcement_date=date(2026, 3, 1),
                         new_share_count=1_500_000),
    ]
    result = build_weighted_average_shares(history, actions, cutoff=date(2026, 1, 1))
    assert result.shares == pytest.approx(1_000_000)
    assert result.applied_actions == []
    assert "after the cutoff" in result.notes[0]


def test_share_history_after_cutoff_is_invisible():
    history = [
        _ShareRecord(date(2025, 1, 1), 1_000_000),
        _ShareRecord(date(2026, 6, 1), 5_000_000),
    ]
    result = build_weighted_average_shares(history, cutoff=date(2026, 1, 1))
    assert result.shares == pytest.approx(1_000_000)


# --- 11. missing share data ------------------------------------------------

def test_weighted_shares_missing_history_is_none_not_invented():
    result = build_weighted_average_shares([], cutoff=date(2026, 1, 1))
    assert result.shares is None
    assert result.basis == "NO_SHARE_HISTORY"


def test_weighted_shares_no_observation_at_cutoff_is_none():
    history = [_ShareRecord(date(2026, 6, 1), 1_000_000)]
    result = build_weighted_average_shares(history, cutoff=date(2026, 1, 1))
    assert result.shares is None
    assert result.basis == "NO_OBSERVATION_AT_OR_BEFORE_CUTOFF"


def test_weighted_shares_unresolvable_action_is_reported_not_guessed():
    history = [_ShareRecord(date(2025, 1, 1), 1_000_000)]
    actions = [_CorporateAction("CAPITAL_INCREASE", date(2025, 7, 1))]
    result = build_weighted_average_shares(history, actions, cutoff=date(2026, 1, 1))
    assert result.shares == pytest.approx(1_000_000)
    assert result.notes == ["unusable CAPITAL_INCREASE at 2025-07-01: no "
                            "new_share_count and no resolvable ratio"]


def test_engine_accepts_builder_output_for_eps():
    history = [_ShareRecord(date(2025, 1, 1), 1_000_000)]
    actions = [
        _CorporateAction("CAPITAL_INCREASE", date(2025, 7, 1),
                         old_share_count=1_000_000, new_share_count=1_500_000,
                         ratio=0.5),
    ]
    shares = build_weighted_average_shares(history, actions, cutoff=date(2026, 1, 1))
    context = _context()
    context.pop("share_count")
    context["forecast_weighted_average_shares"] = shares
    forecast = ForecastEngine().generate_forecast(
        1, 101, "PETROCHEMICAL", context,
        data_cutoff_datetime=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )
    base = forecast.scenario_forecasts.base
    assert base.eps is not None
    # Net profit 10000 * 1.10 * 0.10 = 1100 over ~1.252M shares.
    assert base.eps < 1100.0 / 1_240_000
    assert base.eps > 1100.0 / 1_262_000


# --- 12. determinism -------------------------------------------------------

def test_weighted_shares_are_deterministic_across_calls():
    history = [
        _ShareRecord(date(2025, 1, 1), 1_000_000),
        _ShareRecord(date(2025, 10, 1), 1_200_000),
    ]
    actions = [_CorporateAction("STOCK_SPLIT", date(2025, 7, 1), ratio=2.0)]
    first = build_weighted_average_shares(history, actions, cutoff=date(2026, 1, 1))
    second = build_weighted_average_shares(list(reversed(history)), actions,
                                           cutoff=date(2026, 1, 1))
    assert first.shares == second.shares
    assert first.applied_actions == second.applied_actions


def test_stage4_adapter_is_deterministic():
    result = _stage4()
    first = adapt_stage4(result)
    second = adapt_stage4(result)
    assert first == second
    assert first.to_dict() == second.to_dict()


# ==========================================================================
# 13. Persistent repository (ForecastEngine -> ForecastRecord -> repository
#     -> persistent storage; spec sections 24, 25, 28, 29)
# ==========================================================================

from sqlalchemy import create_engine  # noqa: E402
from sqlalchemy.orm import sessionmaker  # noqa: E402

from src.forecast.repo import ForecastRecordRepository  # noqa: E402
from src.migrations.runner import MigrationRunner  # noqa: E402


@pytest.fixture
def repo():
    """Fresh in-memory schema, isolated from the on-disk production database."""
    engine = create_engine("sqlite:///:memory:")
    MigrationRunner(engine).upgrade()
    session = sessionmaker(bind=engine)()
    yield ForecastRecordRepository(session)
    session.close()


def _series_records(eps_values, repo, scenario="base", **overrides):
    """Save one record per eps value and return the persisted history."""
    for index, eps in enumerate(eps_values):
        result = _forecast(**{key: value for key, value in overrides.items()
                              if key in CONTEXT_KEYS})
        engine_kwargs = {
            key: value for key, value in overrides.items()
            if key not in CONTEXT_KEYS
        }
        engine_kwargs.setdefault("company_id", 1)
        engine_kwargs.setdefault("forecast_period_id", 101)
        engine_kwargs.setdefault("industry_code", "PETROCHEMICAL")
        engine_kwargs.setdefault(
            "data_cutoff_datetime", datetime(2026, 1 + index, 1, tzinfo=timezone.utc))
        engine_kwargs["financial_context"] = _context()
        record = ForecastEngine().generate_forecast(**engine_kwargs).to_record(
            scenario, forecast_id=index + 1)
        record = replace(record, eps=eps)
        repo.save(record)
    return repo.history(1, 101, "12M", scenario.upper())


def test_repo_first_forecast_persists(repo):
    record = _forecast().to_record("base", forecast_id=1)
    saved = repo.save(record)

    assert saved.forecast_version == 1
    assert repo.count() == 1
    reloaded = repo.latest(1, 101, "12M", "BASE")
    assert reloaded is not None
    # A missing metric round-trips as None, never as 0 (spec section 27).
    assert reloaded.eps is not None
    assert reloaded.company_id == 1
    assert reloaded.forecast_period_id == 101
    assert reloaded.scenario == "BASE"
    assert reloaded.forecast_horizon == "12M"


def test_repo_second_save_creates_a_new_version(repo):
    repo.save(_forecast().to_record("base", forecast_id=1))
    second = repo.save(_forecast().to_record("base", forecast_id=2))

    assert second.forecast_version == 2
    assert repo.count() == 2
    assert len(repo.history(1, 101, "12M", "BASE")) == 2


def test_repo_old_version_remains_readable(repo):
    first = repo.save(_forecast().to_record("base", forecast_id=1))
    repo.save(_forecast().to_record("base", forecast_id=2))

    history = repo.history(1, 101, "12M", "BASE")
    assert [r.forecast_version for r in history] == [1, 2]
    # The August forecast is still there after September overwrote nothing.
    assert repo.latest(1, 101, "12M", "BASE").forecast_version == 2
    assert history[0].eps == first.eps
    assert history[0].forecast_timestamp == first.forecast_timestamp


def test_repo_does_not_overwrite_the_previous_forecast(repo):
    original = repo.save(_forecast().to_record("base", forecast_id=1))
    different = replace(_forecast().to_record("base", forecast_id=2), eps=999.0)
    repo.save(different)

    history = repo.history(1, 101, "12M", "BASE")
    assert len(history) == 2
    assert history[0].eps == original.eps
    assert history[0].eps != 999.0
    assert history[1].eps == 999.0


def test_repo_identical_resave_is_idempotent(repo):
    record = _forecast().to_record("base", forecast_id=1)
    repo.save(record)
    again = repo.save(record)

    assert again.forecast_version == 1
    assert repo.count() == 1
    assert repo.latest(1, 101, "12M", "BASE").forecast_version == 1


def test_repo_conflicting_version_is_rejected(repo):
    repo.save(_forecast().to_record("base", forecast_id=1))
    # The caller asserts this is version 1, but version 1 already exists with
    # different contents: a silent overwrite must not happen.
    conflicting = replace(_forecast().to_record("base", forecast_id=2),
                          eps=5.0, forecast_version=1)

    with pytest.raises(ForecastVersionExistsError):
        repo.save(conflicting)
    # The rejected write left nothing behind.
    assert repo.count() == 1
    assert repo.latest(1, 101, "12M", "BASE").eps != 5.0


def test_repo_scenarios_are_separate_series(repo):
    for scenario in ("bear", "base", "bull"):
        repo.save(_forecast().to_record(scenario, forecast_id=1))

    assert repo.count() == 3
    assert len(repo.history(1, 101, "12M", "BEAR")) == 1
    assert len(repo.history(1, 101, "12M", "BASE")) == 1
    assert len(repo.history(1, 101, "12M", "BULL")) == 1


def test_repo_horizons_are_separate_series(repo):
    for horizon in ("6M", "12M"):
        repo.save(_forecast(horizon=horizon).to_record("base", forecast_id=1))

    assert repo.count() == 2
    assert len(repo.history(1, 101, "6M", "BASE")) == 1
    assert len(repo.history(1, 101, "12M", "BASE")) == 1


def test_repo_preserves_pit_fields(repo):
    record = _forecast(
        data_cutoff_datetime=datetime(2026, 3, 1, tzinfo=timezone.utc),
        calculation_timestamp=datetime(2026, 4, 1, tzinfo=timezone.utc),
    ).to_record("base", forecast_id=1)
    record = replace(record, model_version="V2.3")
    saved = repo.save(record)

    assert saved.model_version == "V2.3"
    reloaded = repo.latest(1, 101, "12M", "BASE")
    assert reloaded.data_cutoff_datetime == datetime(2026, 3, 1, tzinfo=timezone.utc)
    assert reloaded.forecast_timestamp == datetime(2026, 4, 1, tzinfo=timezone.utc)
    assert reloaded.model_version == "V2.3"
    assert reloaded.scenario == "BASE"
    assert reloaded.forecast_method == record.forecast_method
    assert reloaded.data_quality == record.data_quality
    assert reloaded.assumptions == record.assumptions


def test_repo_preserves_input_provenance(repo):
    record = _forecast(input_refs=[
        ForecastInputRef("q4_revenue", report_version_id=99,
                         available_at=datetime(2025, 6, 1, tzinfo=timezone.utc),
                         source="codal"),
    ]).to_record("base", forecast_id=1)
    repo.save(record)

    reloaded = repo.latest(1, 101, "12M", "BASE")
    assert len(reloaded.input_refs) == 1
    ref = reloaded.input_refs[0]
    assert ref.fact_key == "q4_revenue"
    assert ref.report_version_id == 99
    assert ref.available_at == datetime(2025, 6, 1, tzinfo=timezone.utc)
    assert ref.source == "codal"


def test_repo_revision_trend_built_from_stored_versions(repo):
    history = _series_records((1100.0, 1180.0, 1270.0), repo)
    assert [r.eps for r in history] == [1100.0, 1180.0, 1270.0]
    assert repo.revision_trend(1, 101, "12M", "BASE") == "UPWARD"


def test_repo_revision_trend_mixed_is_reported(repo):
    _series_records((1100.0, 900.0, 1270.0), repo)
    assert repo.revision_trend(1, 101, "12M", "BASE") == "MIXED"


def test_repo_read_at_cutoff_hides_forecasts_built_on_later_data(repo):
    repo.save(_forecast(
        input_refs=[ForecastInputRef("base_report",
                                     available_at=datetime(2025, 6, 1, tzinfo=timezone.utc))],
    ).to_record("base", forecast_id=1))

    late = _forecast(
        data_cutoff_datetime=datetime(2026, 9, 1, tzinfo=timezone.utc),
        input_refs=[ForecastInputRef("october_report",
                                     available_at=datetime(2026, 10, 5, tzinfo=timezone.utc))],
    )
    repo.save(late.to_record("base", forecast_id=2))

    visible = repo.read_at_cutoff(
        1, 101, "12M", "BASE", datetime(2026, 9, 15, tzinfo=timezone.utc))
    assert visible is not None
    # Never the version built from the October report.
    assert visible.forecast_version == 1
    assert [r.fact_key for r in visible.input_refs] == ["base_report"]
    assert repo.pit_violations(datetime(2026, 9, 1, tzinfo=timezone.utc)) != []


# ==========================================================================
# 14. Production path: Stage 1 facts + Stage 4 evidence -> engine ->
#     ForecastRecord -> ForecastRecordRepository (spec sections 9, 15-16,
#     24, 25, 29)
# ==========================================================================

from src.forecast.service import generate_and_persist_forecast  # noqa: E402
from src.migrations.runner import MigrationRunner  # noqa: E402

from src.models.entity import Company, Industry  # noqa: E402
from src.models.normalized import (  # noqa: E402
    FinancialMetric,
    NormalizedFinancialFact,
)
from src.models.period import FinancialPeriod  # noqa: E402
from src.models.report import Report, ReportVersion  # noqa: E402
from src.models.share_action import CorporateAction, ShareCountHistory  # noqa: E402


COMPANY_ID = 1
PERIOD_ID = 101
CUTOFF = datetime(2026, 1, 1, tzinfo=timezone.utc)
CALCULATED_AT = datetime(2026, 1, 2, tzinfo=timezone.utc)
PUBLISHED = datetime(2025, 12, 15, tzinfo=timezone.utc)
LATE_PUBLISHED = datetime(2026, 6, 1, tzinfo=timezone.utc)

# Seeded facts, in IRR millions. The production path must reach these.
SEEDED_REVENUE = 12_000_000.0
SEEDED_NET_PROFIT = 1_100_000.0
SEEDED_EQUITY = 25_000_000.0

# The engine's own BASE net profit for the seeded facts: revenue x net margin,
# which is the chain the production path exercises (Stage 1 supplies the
# revenue and the caller supplies the margins).
FORECAST_NET_PROFIT = 1_200_000.0

# The forecast horizon share base, built by the weighted-average builder. The
# later observation is dated on the cutoff, so it is in force for only one day
# of the window and the weighted average stays close to the earlier count.
SEEDED_SHARES = 1_000_000
INCREASED_SHARES = 1_500_000

_STAGE4_METRIC = "REVENUE"

# The builder's own answer for the seeded history: 1M shares for 181 days then
# 1.5M for 185, over the 2025-01-01..2026-01-01 window.
_WEIGHTED_SHARES = 1_252_054.7945205478


def _production_stage4(**overrides):
    """Stage 4 output as the production path receives it: already evaluated."""
    result = _stage4(**overrides)
    return replace(result, metric_code=_STAGE4_METRIC)


@pytest.fixture
def production_db():
    """Fresh in-memory schema holding real Stage 1 rows for one company."""
    engine = create_engine("sqlite:///:memory:")
    MigrationRunner(engine).upgrade()
    session = sessionmaker(bind=engine)()
    _seed_stage1(session)
    yield session
    session.close()


@pytest.fixture
def empty_share_db(production_db):
    """The same company, but with no share-count history at all."""
    session = production_db
    session.query(ShareCountHistory).delete()
    session.query(CorporateAction).delete()
    session.flush()
    return session


def _seed_stage1(session):
    industry = Industry(industry_code="PETROCHEMICAL", industry_name="Petrochemical")
    session.add(industry)
    session.flush()

    session.add(Company(
        company_id=COMPANY_ID,
        ticker="PETRO",
        company_name="Petro",
        industry_id=industry.industry_id,
    ))
    session.flush()

    session.add(FinancialPeriod(
        period_id=PERIOD_ID,
        company_id=COMPANY_ID,
        period_type="QUARTER",
        start_date=date(2025, 10, 1),
        end_date=date(2025, 12, 31),
        fiscal_year=2025,
        fiscal_quarter=3,
        months_length=3,
    ))
    session.flush()

    metrics = {
        code: FinancialMetric(
            metric_code=code,
            metric_name=code.title(),
            category="INCOME_STATEMENT",
            flow_or_stock="FLOW",
            value_type="CURRENCY_IRR",
        )
        for code in ("REVENUE", "NET_PROFIT", "TOTAL_EQUITY", "EPS")
    }
    session.add_all(metrics.values())
    session.flush()

    report = Report(
        company_id=COMPANY_ID,
        report_type="QUARTERLY",
        title="Q3 1404",
        financial_period_id=PERIOD_ID,
    )
    session.add(report)
    session.flush()

    version = ReportVersion(
        report_id=report.report_id,
        version_number=1,
        publication_datetime=PUBLISHED,
        is_current_version=True,
    )
    session.add(version)
    session.flush()

    # A second version of the same report, published after the cutoff. It must
    # be invisible to a forecast dated at the cutoff.
    restated = ReportVersion(
        report_id=report.report_id,
        version_number=2,
        publication_datetime=LATE_PUBLISHED,
        is_current_version=False,
        is_restated=True,
        supersedes_version_id=version.report_version_id,
    )
    session.add(restated)
    session.flush()

    for code, value in (
        ("REVENUE", SEEDED_REVENUE),
        ("NET_PROFIT", SEEDED_NET_PROFIT),
        ("TOTAL_EQUITY", SEEDED_EQUITY),
    ):
        session.add(NormalizedFinancialFact(
            company_id=COMPANY_ID,
            period_id=PERIOD_ID,
            metric_id=metrics[code].metric_id,
            value_irr=value,
            source_report_version_id=version.report_version_id,
        ))
    session.add(NormalizedFinancialFact(
        company_id=COMPANY_ID,
        period_id=PERIOD_ID,
        metric_id=metrics["EPS"].metric_id,
        value_irr=None,
        source_report_version_id=version.report_version_id,
        quality_status="MISSING",
    ))
    # The restatement is a look-ahead trap: published after the cutoff.
    session.add(NormalizedFinancialFact(
        company_id=COMPANY_ID,
        period_id=PERIOD_ID,
        metric_id=metrics["REVENUE"].metric_id,
        value_irr=99_999_999.0,
        source_report_version_id=restated.report_version_id,
        quality_status="RESTATED",
    ))

    session.add(ShareCountHistory(
        company_id=COMPANY_ID,
        effective_date=date(2025, 1, 1),
        shares_outstanding=SEEDED_SHARES,
        capital=10_000_000,
    ))
    session.add(ShareCountHistory(
        company_id=COMPANY_ID,
        effective_date=date(2025, 7, 1),
        shares_outstanding=INCREASED_SHARES,
        capital=15_000_000,
    ))
    session.add(CorporateAction(
        company_id=COMPANY_ID,
        announcement_date=date(2025, 6, 1),
        effective_date=date(2025, 7, 1),
        action_type="CAPITAL_INCREASE",
        old_share_count=SEEDED_SHARES,
        new_share_count=INCREASED_SHARES,
    ))
    session.flush()


def _production_kwargs(**overrides):
    kwargs = {
        "trend_result": _production_stage4(),
        "data_cutoff_datetime": CUTOFF,
        "calculation_timestamp": CALCULATED_AT,
        "model_parameters": {"trend_adjustments": {"Stable": 0.0}},
        "extra_facts": {
            "historical_operating_margin": 0.20,
            "historical_net_margin": 0.10,
        },
    }
    kwargs.update(overrides)
    return kwargs


# --- 1. Stage 1 facts reach build_financial_context -------------------------

def test_production_path_builds_forecast_from_stage1_facts(production_db):
    forecast = generate_and_persist_forecast(
        production_db, COMPANY_ID, PERIOD_ID, **_production_kwargs())

    base = forecast.scenario_forecasts.base
    # The seeded revenue is what drives the forecast, not a test fixture.
    assert base.revenue is not None
    assert base.revenue > 0.0
    # No seasonal baseline was declared, so the run rate from Stage 1 wins.
    assert forecast.baseline_method == "RUN_RATE"
    assert base.revenue == pytest.approx(SEEDED_REVENUE, rel=1e-6)


# --- 2. Stage 4 output reaches the engine without recalculation -------------

def test_production_path_uses_stage4_without_recalculation(production_db):
    trend = _production_stage4(trend_state="Improving")
    forecast = generate_and_persist_forecast(
        production_db, COMPANY_ID, PERIOD_ID,
        **_production_kwargs(trend_result=trend))

    # Stage 4 is carried through as evidence; the engine never recomputes it.
    assert forecast.assumptions["trend_evidence"] == "Improving"
    assert forecast.assumptions["low_base"] is False
    assert forecast.assumptions["sign_change"] is None

    persisted = ForecastRecordRepository(production_db).latest(
        COMPANY_ID, PERIOD_ID, "12M", "BASE")
    assert persisted is not None
    # Stage 4's own coordinates survive the whole path on the record, not in
    # the scenario assumptions.
    assert persisted.stage4_provenance["metric_code"] == _STAGE4_METRIC
    assert persisted.stage4_provenance["stage"] == "STAGE_4"
    # Stage 4 evidence is frozen on the record, and the engine did not
    # recompute it: the stored record carries the same direction the caller
    # supplied.
    assert persisted.assumptions["baseline_method"] == "RUN_RATE"


# --- 3. Real ShareCountHistory reaches the weighted-share calculation -------

def test_production_path_weights_real_share_history(production_db):
    forecast = generate_and_persist_forecast(
        production_db, COMPANY_ID, PERIOD_ID, **_production_kwargs())
    base = forecast.scenario_forecasts.base

    assert base.eps is not None
    # The weighted average over the real history sits strictly between the two
    # recorded share counts, so the builder's weighting actually ran.
    assert FORECAST_NET_PROFIT / INCREASED_SHARES < base.eps < FORECAST_NET_PROFIT / SEEDED_SHARES
    assert base.eps == pytest.approx(FORECAST_NET_PROFIT / _WEIGHTED_SHARES, rel=1e-6)


# --- 4. ForecastEngine output becomes ForecastRecord ------------------------

def test_production_path_produces_forecast_records(production_db):
    forecast = generate_and_persist_forecast(
        production_db, COMPANY_ID, PERIOD_ID, **_production_kwargs())
    records = forecast.records()

    assert [r.scenario for r in records] == ["BEAR", "BASE", "BULL"]
    assert all(isinstance(r, ForecastRecord) for r in records)
    assert all(r.company_id == COMPANY_ID for r in records)
    assert all(r.data_cutoff_datetime == CUTOFF for r in records)


# --- 5. ForecastRecord reaches the persistent repository --------------------

def test_production_path_persists_all_scenarios(production_db):
    generate_and_persist_forecast(
        production_db, COMPANY_ID, PERIOD_ID, **_production_kwargs())

    repository = ForecastRecordRepository(production_db)
    assert repository.count() == 3
    for scenario in ("BEAR", "BASE", "BULL"):
        latest = repository.latest(COMPANY_ID, PERIOD_ID, "12M", scenario)
        assert latest is not None
        assert latest.scenario == scenario
        assert latest.forecast_version == 1


# --- 6. The persisted forecast can be read back -----------------------------

def test_production_path_reads_forecast_back(production_db):
    forecast = generate_and_persist_forecast(
        production_db, COMPANY_ID, PERIOD_ID, **_production_kwargs())

    reloaded = ForecastRecordRepository(production_db).latest(
        COMPANY_ID, PERIOD_ID, "12M", "BASE")
    assert reloaded is not None
    base = forecast.scenario_forecasts.base
    assert reloaded.revenue == base.revenue
    assert reloaded.net_profit == base.net_profit
    # The store keeps 4 decimal places, so a 6-digit EPS is stored coarsely and
    # read back within the column's own precision, not bit-for-bit.
    assert reloaded.eps == pytest.approx(base.eps, abs=1e-4)
    assert reloaded.forecast_method == base.method
    # Stage 1 provenance survived the round trip.
    assert {r.fact_key for r in reloaded.input_refs} >= {
        "REVENUE", "NET_PROFIT", "TOTAL_EQUITY"}


# --- 7. PIT metadata survives the complete path -----------------------------

def test_production_path_preserves_pit_metadata(production_db):
    forecast = generate_and_persist_forecast(
        production_db, COMPANY_ID, PERIOD_ID, **_production_kwargs())

    reloaded = ForecastRecordRepository(production_db).latest(
        COMPANY_ID, PERIOD_ID, "12M", "BASE")
    assert reloaded is not None
    assert reloaded.data_cutoff_datetime == CUTOFF
    assert reloaded.forecast_timestamp == forecast.calculation_timestamp

    revenue_ref = next(r for r in reloaded.input_refs if r.fact_key == "REVENUE")
    assert revenue_ref.available_at == PUBLISHED
    assert revenue_ref.report_version_id is not None
    assert revenue_ref.source == "normalized_financial_facts"

    # Every input the forecast saw was published at or before the cutoff, so a
    # reader at the cutoff can still trust the record.
    assert reloaded.data_cutoff_datetime >= max(
        ref.available_at for ref in reloaded.input_refs
        if ref.available_at is not None)
    # The restated version published after the cutoff never entered.
    assert reloaded.revenue != 99_999_999.0


# --- 8. Duplicate persistence stays idempotent ------------------------------

def test_production_path_duplicate_save_is_idempotent(production_db):
    repository = ForecastRecordRepository(production_db)
    generate_and_persist_forecast(
        production_db, COMPANY_ID, PERIOD_ID, **_production_kwargs())
    first = repository.latest(COMPANY_ID, PERIOD_ID, "12M", "BASE")

    # Re-running the path with the same inputs is a no-op, not a new version.
    generate_and_persist_forecast(
        production_db, COMPANY_ID, PERIOD_ID, **_production_kwargs())

    assert repository.count() == 3
    again = repository.latest(COMPANY_ID, PERIOD_ID, "12M", "BASE")
    assert again.forecast_version == first.forecast_version == 1
    assert again.eps == first.eps
    # Nothing else changed: the re-run produced the same series state, so the
    # repository found its own latest record and returned it as-is.
    assert replace(again, forecast_id=first.forecast_id) == replace(
        first, forecast_id=again.forecast_id)


# --- 9. Missing share history stays None ------------------------------------

def test_production_path_missing_share_history_keeps_eps_none(empty_share_db):
    forecast = generate_and_persist_forecast(
        empty_share_db, COMPANY_ID, PERIOD_ID, **_production_kwargs())
    base = forecast.scenario_forecasts.base

    # No share base could be established, so no EPS is invented.
    assert base.eps is None
    assert base.net_profit is not None

    reloaded = ForecastRecordRepository(empty_share_db).latest(
        COMPANY_ID, PERIOD_ID, "12M", "BASE")
    assert reloaded is not None
    assert reloaded.eps is None
    assert reloaded.is_missing("eps")


# --- 10. Deterministic repeated execution -----------------------------------

def test_production_path_is_deterministic():
    def _run():
        engine = create_engine("sqlite:///:memory:")
        MigrationRunner(engine).upgrade()
        session = sessionmaker(bind=engine)()
        try:
            _seed_stage1(session)
            return generate_and_persist_forecast(
                session, COMPANY_ID, PERIOD_ID, **_production_kwargs())
        finally:
            session.close()

    first = _run()
    second = _run()

    first_records = first.records()
    second_records = second.records()
    assert [r.eps for r in first_records] == [r.eps for r in second_records]
    assert [r.revenue for r in first_records] == [r.revenue for r in second_records]
    assert first_records[1].eps == second_records[1].eps


# ==========================================================================
# 15. Non-financial forecast core (Prompt 6): one common chain for
#     PETROCHEMICAL / CHEMICAL / METALS / MINING / CEMENT / FOOD /
#     PHARMACEUTICAL.  Revenue -> Operating Margin -> Operating Profit ->
#     Net Profit -> EPS -> ROE.
# ==========================================================================

from src.forecast.schema import NON_FINANCIAL_INDUSTRIES  # noqa: E402


def _core_context(**overrides):
    """One non-financial context: seasonal baseline, margins, shares, equity."""
    context = {
        "seasonality_valid": True,
        "seasonal_baseline_revenue": 10000.0,
        "recent_run_rate_revenue": 9000.0,
        "baseline_revenue_growth": 0.10,
        "historical_operating_margin": 0.20,
        "historical_net_margin": 0.10,
        "share_count": 1000.0,
        "beginning_equity": 9000.0,
        "forecast_ending_equity": 11000.0,
    }
    context.update(overrides)
    return context


def _core_forecast(context, industry="PETROCHEMICAL"):
    return ForecastEngine().generate_forecast(
        1, 101, industry, context,
        data_cutoff_datetime=datetime(2026, 1, 1, tzinfo=timezone.utc),
    )


# --- 1. Revenue baseline hierarchy -----------------------------------------

def test_seasonal_baseline_outranks_the_run_rate():
    # Tier 1: a seasonal/historical baseline Stage 4 validated as sufficient.
    result = _core_forecast(_core_context())
    assert result.baseline_method == "SEASONAL_BASELINE"
    # The seasonal figure is used, not the 9000 run rate.
    assert result.scenario_forecasts.base.revenue == 11000.0


def test_recent_run_rate_is_the_fallback_baseline():
    # Tier 2: seasonality is not valid, so the run rate carries the forecast.
    result = _core_forecast(_core_context(
        seasonality_valid=False, seasonal_baseline_revenue=None))
    assert result.baseline_method == "RUN_RATE"
    assert result.scenario_forecasts.base.revenue == 9900.0


def test_driver_based_baseline_is_the_third_tier():
    # Tier 3: neither history nor run rate exists, so an explicit driver
    # decomposition declared by the caller supplies the level.
    result = _core_forecast(_core_context(
        seasonality_valid=False, seasonal_baseline_revenue=None,
        recent_run_rate_revenue=None, driver_volume=2000.0, driver_price=5.0))
    assert result.baseline_method == "DRIVER_BASED"
    assert result.scenario_forecasts.base.revenue == 11000.0


def test_explicit_driver_based_level_beats_the_volume_price_split():
    result = _core_forecast(_core_context(
        seasonality_valid=False, seasonal_baseline_revenue=None,
        recent_run_rate_revenue=None,
        driver_based_revenue=8000.0, driver_volume=2000.0, driver_price=5.0))
    assert result.baseline_method == "DRIVER_BASED"
    assert result.scenario_forecasts.base.revenue == 8800.0


def test_non_positive_driver_level_is_refused_not_treated_as_zero():
    result = _core_forecast(_core_context(
        seasonality_valid=False, seasonal_baseline_revenue=None,
        recent_run_rate_revenue=None, driver_based_revenue=0.0))
    assert result.baseline_method == "INSUFFICIENT_DATA"
    assert result.scenario_forecasts.base.revenue is None


def test_insufficient_baseline_reports_missing_rather_than_zero():
    result = _core_forecast(_core_context(
        seasonality_valid=False, seasonal_baseline_revenue=None,
        recent_run_rate_revenue=None))
    assert result.baseline_method == "INSUFFICIENT_DATA"
    assert result.data_quality == "INSUFFICIENT_DATA"
    for scenario in ("bear", "base", "bull"):
        chain = getattr(result.scenario_forecasts, scenario)
        assert chain.method == "INSUFFICIENT_DATA"
        assert chain.revenue is None
        assert chain.operating_profit is None
    # The missing baseline is carried through to the record, never as 0.
    record = result.to_record("base", forecast_id=1)
    assert record.is_missing("revenue")
    assert record.is_missing("operating_profit")


# --- 2. Revenue growth ------------------------------------------------------

def test_revenue_growth_applies_to_the_baseline():
    result = _core_forecast(_core_context(baseline_revenue_growth=0.25))
    chains = result.scenario_forecasts
    assert chains.base.revenue == 12500.0
    # Bear/base/bull are the growth spread around the declared rate.
    assert chains.bear.revenue == pytest.approx(10000.0 * (0.25 - 0.05) + 10000.0)
    assert chains.bull.revenue == pytest.approx(10000.0 * (0.25 + 0.05) + 10000.0)


def test_missing_revenue_growth_defaults_to_flat_not_invented():
    context = _core_context()
    del context["baseline_revenue_growth"]
    result = _core_forecast(context)
    assert result.scenario_forecasts.base.revenue == 10000.0


# --- 3. Operating margin is independent of revenue --------------------------

def test_operating_margin_method_is_recorded_separately():
    result = _core_forecast(_core_context())
    base = result.scenario_forecasts.base
    assert base.operating_margin == 0.20
    assert base.assumptions["operating_margin_method"] == "HISTORICAL_OPERATING_MARGIN"
    assert base.assumptions["baseline_method"] == "SEASONAL_BASELINE"


def test_revenue_can_rise_while_margin_falls():
    context = _core_context(baseline_revenue_growth=0.20)
    context["model_parameters"] = {"operating_margin_adjustment": -0.05}
    result = _core_forecast(context)
    base = result.scenario_forecasts.base
    assert base.revenue == 12000.0
    assert base.operating_margin == 0.15
    # Operating profit falls even though revenue rose 20%.
    assert base.operating_profit == 1800.0
    flat = _core_forecast(_core_context())  # growth 0.10, margin 0.20
    assert flat.scenario_forecasts.base.operating_profit == 2200.0
    assert base.operating_profit < flat.scenario_forecasts.base.operating_profit


def test_revenue_can_fall_while_margin_rises():
    context = _core_context(baseline_revenue_growth=-0.10)
    context["model_parameters"] = {"operating_margin_adjustment": 0.05}
    result = _core_forecast(context)
    base = result.scenario_forecasts.base
    assert base.revenue == 9000.0
    assert base.operating_margin == 0.25
    assert base.operating_profit == 2250.0
    flat = _core_forecast(_core_context())
    assert base.operating_profit > flat.scenario_forecasts.base.operating_profit


def test_revenue_can_rise_while_operating_profit_decreases():
    context = _core_context(baseline_revenue_growth=0.05)
    context["model_parameters"] = {"operating_margin_adjustment": -0.10}
    result = _core_forecast(context)
    base = result.scenario_forecasts.base
    assert base.revenue == 10500.0
    assert base.operating_margin == 0.10
    assert base.operating_profit == 1050.0
    flat = _core_forecast(_core_context())
    assert base.operating_profit < flat.scenario_forecasts.base.operating_profit


def test_changing_revenue_growth_does_not_move_the_margin():
    # The margin hierarchy is resolved on its own evidence: widening the growth
    # spread leaves the BASE margin untouched.
    narrow = _core_forecast(_core_context(baseline_revenue_growth=0.02))
    wide = _core_forecast(_core_context(baseline_revenue_growth=0.40))
    assert narrow.scenario_forecasts.base.operating_margin == \
        wide.scenario_forecasts.base.operating_margin == 0.20


def test_forecast_margin_outranks_the_historical_margin():
    result = _core_forecast(_core_context(
        forecast_operating_margin=0.30, recent_operating_margin=0.25))
    assert result.scenario_forecasts.base.operating_margin == 0.30
    assert result.scenario_forecasts.base.assumptions["operating_margin_method"] == \
        "FORECAST_OPERATING_MARGIN"


def test_missing_operating_margin_halts_the_chain():
    context = _core_context()
    del context["historical_operating_margin"]
    result = _core_forecast(context)
    # The margin is unknown, so no operating profit is derived from revenue.
    assert result.scenario_forecasts.base.method == "INSUFFICIENT_DATA"
    assert result.scenario_forecasts.base.assumptions["reason"] == "missing_operating_margin"


# --- 4. Operating profit ----------------------------------------------------

def test_operating_profit_is_revenue_times_margin():
    result = _core_forecast(_core_context())
    base = result.scenario_forecasts.base
    assert base.revenue == 11000.0
    assert base.operating_margin == 0.20
    assert base.operating_profit == pytest.approx(base.revenue * base.operating_margin)
    assert base.operating_profit == 2200.0


def test_full_chain_is_resolved_in_order():
    # Revenue -> Operating Margin -> Operating Profit -> Net Profit -> EPS -> ROE.
    result = _core_forecast(_core_context())
    base = result.scenario_forecasts.base
    assert base.revenue == 11000.0
    assert base.operating_margin == 0.20
    assert base.operating_profit == 2200.0
    assert base.net_profit == 1100.0
    assert base.eps == 1.1
    assert base.roe == pytest.approx(1100.0 / 10000.0)
    assert base.method == "MARGIN"


# --- 5. Net profit hierarchy ------------------------------------------------

def test_component_based_net_profit_wins_through_the_engine():
    result = _core_forecast(_core_context(
        forecast_non_operating_items=100.0,
        forecast_financial_costs=50.0,
        forecast_tax=40.0))
    base = result.scenario_forecasts.base
    assert base.method == "COMPONENT_BASED"
    # 2200 operating profit + 100 other income - 50 financial costs - 40 tax.
    assert base.net_profit == 2210.0
    assert base.eps == 2.21
    assert base.assumptions["net_profit_method_hierarchy"] == [
        "COMPONENT_BASED", "HISTORICAL_CONVERSION", "NET_MARGIN", "INSUFFICIENT_DATA"]


def test_partial_components_do_not_get_fabricated():
    # Only the tax is supplied: the component path needs all three, so the
    # historical conversion is used and no financial cost is invented.
    context = _core_context(forecast_tax=40.0, historical_net_operating_conversion=0.9)
    del context["historical_net_margin"]
    result = _core_forecast(context)
    base = result.scenario_forecasts.base
    assert base.method == "HISTORICAL_CONVERSION"
    assert base.net_profit == pytest.approx(2200.0 * 0.9)


def test_historical_conversion_falls_back_from_components():
    context = _core_context(historical_net_operating_conversion=0.9)
    del context["historical_net_margin"]
    result = _core_forecast(context)
    base = result.scenario_forecasts.base
    assert base.method == "HISTORICAL_CONVERSION"
    assert base.net_profit == pytest.approx(2200.0 * 0.9)
    assert base.eps == pytest.approx(2200.0 * 0.9 / 1000.0)


def test_net_margin_is_the_third_tier():
    result = _core_forecast(_core_context())
    base = result.scenario_forecasts.base
    assert base.method == "MARGIN"
    assert base.net_profit == pytest.approx(11000.0 * 0.10)


def test_missing_net_profit_evidence_leaves_net_profit_unknown():
    context = _core_context()
    del context["historical_net_margin"]
    result = _core_forecast(context)
    base = result.scenario_forecasts.base
    # Revenue, margin and operating profit are known; net profit is not.
    assert base.revenue == 11000.0
    assert base.operating_profit == 2200.0
    assert base.net_profit is None
    assert base.eps is None
    assert base.method == "INSUFFICIENT_DATA"
    record = result.to_record("base", forecast_id=1)
    assert record.is_missing("net_profit")
    assert record.is_missing("eps")
    assert not record.is_missing("operating_profit")


def test_missing_share_count_leaves_eps_none_not_zero():
    context = _core_context()
    del context["share_count"]
    result = _core_forecast(context)
    base = result.scenario_forecasts.base
    assert base.net_profit == 1100.0
    assert base.eps is None
    assert result.to_record("base", forecast_id=1).is_missing("eps")


# --- 6. One common core for every non-financial industry --------------------

@pytest.mark.parametrize("industry", sorted(NON_FINANCIAL_INDUSTRIES))
def test_all_non_financial_industries_share_one_core(industry):
    result = _core_forecast(_core_context(), industry=industry)
    base = result.scenario_forecasts.base
    assert result.baseline_method == "SEASONAL_BASELINE"
    # Identical inputs yield the identical chain in all seven industries: there
    # is no per-industry engine.
    assert base.revenue == 11000.0
    assert base.operating_margin == 0.20
    assert base.operating_profit == 2200.0
    assert base.net_profit == 1100.0
    assert base.eps == 1.1
    assert base.roe == pytest.approx(0.11)
    assert base.method == "MARGIN"


@pytest.mark.parametrize("industry", sorted(NON_FINANCIAL_INDUSTRIES))
def test_every_industry_reports_insufficient_data_identically(industry):
    result = _core_forecast(
        {"share_count": 1000.0, "historical_operating_margin": 0.20}, industry)
    assert result.baseline_method == "INSUFFICIENT_DATA"
    assert result.scenario_forecasts.base.method == "INSUFFICIENT_DATA"


# --- 7. Determinism ---------------------------------------------------------

def test_repeated_execution_is_deterministic():
    context = _core_context(
        forecast_non_operating_items=100.0,
        forecast_financial_costs=50.0,
        forecast_tax=40.0)
    first = _core_forecast(context).records(forecast_id_start=1)
    second = _core_forecast(context).records(forecast_id_start=1)
    assert len(first) == len(second) == 3
    for left, right in zip(first, second):
        assert left == right
    assert [r.eps for r in first] == [r.eps for r in second]
    assert [r.roe for r in first] == [r.roe for r in second]


# ==========================================================================
# 16. EPS / ROE / share-count integration (Prompt 7):
#     Net Profit -> Weighted Average Shares -> EPS, and
#     Net Profit + Beginning Equity + Forecast Ending Equity -> ROE.
#     EPS and ROE are only ever derived from the forecast chain; the share base
#     comes from build_weighted_average_shares and is never reimplemented here.
# ==========================================================================

_BASE_NET_PROFIT = 1100.0  # 11000 revenue x 0.10 net margin, BASE scenario

# The drivers round every chain metric to 6 decimals, so an expected EPS is
# compared after the same rounding.
_EPS_SCALE = 6


def _expected_eps(net_profit: float, shares: float) -> float:
    return round(net_profit / shares, _EPS_SCALE)


def _shares_context(history, actions=None, **overrides):
    """Engine context whose share base is the builder's own output.

    ``share_count`` is removed so the weighted average is the only denominator;
    the engine's ``_share_count`` prefers it anyway, but keeping the plain
    number out makes the chain unambiguous.
    """
    cutoff = overrides.pop("cutoff", date(2026, 1, 1))
    context = _core_context()
    context.pop("share_count")
    context["forecast_weighted_average_shares"] = build_weighted_average_shares(
        history, actions, cutoff=cutoff)
    context.update(overrides)
    return context


def _shares_forecast(history, actions=None, **overrides):
    return _core_forecast(_shares_context(history, actions, **overrides))


# --- 1. unchanged shares ----------------------------------------------------

def test_eps_with_unchanged_shares_is_net_profit_over_the_base():
    history = [_ShareRecord(date(2025, 1, 1), 1_000_000)]
    base = _shares_forecast(history).scenario_forecasts.base
    # No corporate action, so the whole window sits at 1,000,000 shares.
    assert base.net_profit == _BASE_NET_PROFIT
    assert base.eps == pytest.approx(_expected_eps(_BASE_NET_PROFIT, 1_000_000))


def test_unchanged_shares_across_a_multi_observation_history():
    history = [
        _ShareRecord(date(2025, 1, 1), 1_000_000),
        _ShareRecord(date(2025, 7, 1), 1_000_000),
    ]
    base = _shares_forecast(history).scenario_forecasts.base
    assert base.eps == pytest.approx(_BASE_NET_PROFIT / 1_000_000)


# --- 2. capital increase ------------------------------------------------------

def test_eps_with_capital_increase_uses_the_weighted_average():
    history = [_ShareRecord(date(2025, 1, 1), 1_000_000)]
    actions = [
        _CorporateAction("CAPITAL_INCREASE", date(2025, 7, 1),
                         old_share_count=1_000_000, new_share_count=1_500_000),
    ]
    base = _shares_forecast(history, actions).scenario_forecasts.base
    shares = build_weighted_average_shares(
        history, actions, cutoff=date(2026, 1, 1)).shares
    # EPS falls strictly between the diluted and undiluted extremes, which is
    # only true when the weighting actually ran.
    assert _BASE_NET_PROFIT / 1_500_000 < base.eps < _BASE_NET_PROFIT / 1_000_000
    assert base.eps == pytest.approx(_expected_eps(_BASE_NET_PROFIT, shares))


# --- 3. capital decrease ------------------------------------------------------

def test_eps_with_capital_increase_from_a_lower_base_is_still_weighted():
    # The decrease takes effect after the increase, so the window spans three
    # share levels and EPS reflects all of them.
    history = [_ShareRecord(date(2025, 1, 1), 1_000_000)]
    actions = [
        _CorporateAction("CAPITAL_INCREASE", date(2025, 4, 1),
                         old_share_count=1_000_000, new_share_count=1_600_000),
        _CorporateAction("CAPITAL_DECREASE", date(2025, 10, 1),
                         new_share_count=1_200_000),
    ]
    base = _shares_forecast(history, actions).scenario_forecasts.base
    assert _BASE_NET_PROFIT / 1_600_000 < base.eps < _BASE_NET_PROFIT / 1_000_000
    assert base.eps < _BASE_NET_PROFIT / 1_200_000


# --- 4. split / consolidation -------------------------------------------------

@pytest.mark.parametrize("action_type", ["STOCK_SPLIT", "SPLIT"])
def test_eps_with_a_stock_split_doubles_the_share_base(action_type):
    history = [_ShareRecord(date(2025, 1, 1), 1_000_000)]
    actions = [_CorporateAction(action_type, date(2025, 7, 1), ratio=2.0)]
    base = _shares_forecast(history, actions).scenario_forecasts.base
    # 181 days at 1M then 184 at 2M, so the average sits just above 1.5M.
    assert base.eps == pytest.approx(_expected_eps(_BASE_NET_PROFIT, 1_504_109.589), abs=1e-9)


@pytest.mark.parametrize("action_type", ["REVERSE_SPLIT", "SHARE_CONSOLIDATION"])
def test_eps_with_a_reverse_split_halves_the_share_base(action_type):
    history = [_ShareRecord(date(2025, 1, 1), 1_000_000)]
    actions = [_CorporateAction(action_type, date(2025, 7, 1), ratio=0.5)]
    base = _shares_forecast(history, actions).scenario_forecasts.base
    # 181 days at 1M then 184 at 500k, so the average sits just below 750k.
    assert base.eps == pytest.approx(_expected_eps(_BASE_NET_PROFIT, 747_945.205), abs=1e-9)


def test_eps_with_a_consolidation_declared_as_counts():
    history = [_ShareRecord(date(2025, 1, 1), 1_000_000)]
    actions = [
        _CorporateAction("SHARE_CONSOLIDATION", date(2025, 7, 1),
                         old_share_count=1_000_000, new_share_count=500_000),
    ]
    base = _shares_forecast(history, actions).scenario_forecasts.base
    assert base.eps == pytest.approx(_expected_eps(_BASE_NET_PROFIT, 747_945.205), abs=1e-9)


# --- 5. corporate actions stay point-in-time -----------------------------------

def test_an_action_after_the_cutoff_leaves_eps_at_the_observed_base():
    history = [_ShareRecord(date(2025, 1, 1), 1_000_000)]
    actions = [
        _CorporateAction("CAPITAL_INCREASE", date(2026, 6, 1),
                         new_share_count=2_000_000),
    ]
    base = _shares_forecast(history, actions).scenario_forecasts.base
    assert base.eps == pytest.approx(_expected_eps(_BASE_NET_PROFIT, 1_000_000))


def test_an_action_announced_after_the_cutoff_leaves_eps_undiluted():
    history = [_ShareRecord(date(2025, 1, 1), 1_000_000)]
    actions = [
        _CorporateAction("CAPITAL_INCREASE", date(2025, 7, 1),
                         announcement_date=date(2026, 3, 1),
                         new_share_count=1_500_000),
    ]
    base = _shares_forecast(history, actions).scenario_forecasts.base
    # Effective before the cutoff but only knowable after it: unusable at the
    # cutoff, so the observed count stands.
    assert base.eps == pytest.approx(_BASE_NET_PROFIT / 1_000_000)


def test_a_late_announced_action_is_reported_not_silently_dropped():
    history = [_ShareRecord(date(2025, 1, 1), 1_000_000)]
    actions = [
        _CorporateAction("STOCK_SPLIT", date(2025, 7, 1),
                         announcement_date=date(2026, 3, 1), ratio=2.0),
    ]
    shares = build_weighted_average_shares(
        history, actions, cutoff=date(2026, 1, 1))
    assert shares.shares == pytest.approx(1_000_000)
    assert any("after the cutoff" in note for note in shares.notes)


# --- 6. missing shares ---------------------------------------------------------

def test_missing_share_history_leaves_eps_none_not_zero():
    context = _core_context()
    context.pop("share_count")
    context["forecast_weighted_average_shares"] = build_weighted_average_shares(
        [], cutoff=date(2026, 1, 1))
    base = _core_forecast(context).scenario_forecasts.base
    assert base.net_profit == _BASE_NET_PROFIT
    assert base.eps is None
    # Net profit is real; only the denominator is missing.
    record = _core_forecast(context).to_record("base", forecast_id=1)
    assert record.is_missing("eps")
    assert not record.is_missing("net_profit")


def test_no_observation_at_the_cutoff_leaves_eps_none():
    history = [_ShareRecord(date(2026, 6, 1), 1_000_000)]
    base = _shares_forecast(history).scenario_forecasts.base
    assert base.net_profit == _BASE_NET_PROFIT
    assert base.eps is None


def test_eps_is_never_zero_as_a_substitute_for_a_missing_share_base():
    history = [_ShareRecord(date(2025, 1, 1), 0)]
    base = _shares_forecast(history).scenario_forecasts.base
    # A zero share count is not a denominator: EPS stays unknown.
    assert base.eps is None


# --- 7. EPS is derived, never independently forecast ---------------------------

def test_eps_tracks_net_profit_across_scenarios():
    history = [_ShareRecord(date(2025, 1, 1), 1_000_000)]
    chains = _shares_forecast(history).scenario_forecasts
    # EPS is a pure function of the forecast chain: it orders with net profit
    # and divides it by the same share base in every scenario.
    assert chains.bear.net_profit < chains.base.net_profit < chains.bull.net_profit
    assert chains.bear.eps < chains.base.eps < chains.bull.eps
    for chain in (chains.bear, chains.base, chains.bull):
        assert chain.eps == pytest.approx(_expected_eps(chain.net_profit, 1_000_000))


def test_eps_moves_with_the_share_base_and_not_with_net_profit():
    # Same forecast chain, a doubled share base: EPS halves exactly.
    history = [_ShareRecord(date(2025, 1, 1), 2_000_000)]
    base = _shares_forecast(history).scenario_forecasts.base
    undiluted = _shares_forecast([_ShareRecord(date(2025, 1, 1), 1_000_000)]
                                 ).scenario_forecasts.base
    assert base.net_profit == undiluted.net_profit == _BASE_NET_PROFIT
    assert base.eps == pytest.approx(round(undiluted.eps / 2.0, _EPS_SCALE))


# --- 8. beginning / ending equity and ROE --------------------------------------

def test_roe_is_net_profit_over_average_equity():
    context = _core_context(beginning_equity=9000.0, forecast_ending_equity=11000.0)
    base = _core_forecast(context).scenario_forecasts.base
    assert base.net_profit == _BASE_NET_PROFIT
    assert base.roe == pytest.approx(_BASE_NET_PROFIT / ((9000.0 + 11000.0) / 2.0))


def test_roe_uses_both_ends_not_the_closing_balance_alone():
    # Average equity (10000) differs from closing equity (15000), so the choice
    # of denominator is visible in the result.
    context = _core_context(beginning_equity=5000.0, forecast_ending_equity=15000.0)
    base = _core_forecast(context).scenario_forecasts.base
    assert base.roe == pytest.approx(_BASE_NET_PROFIT / 10000.0)
    assert base.roe != pytest.approx(_BASE_NET_PROFIT / 15000.0)


def test_average_equity_of_zero_is_not_a_divisor():
    # Both ends are present but they cancel: ROE is undefined, not zero.
    context = _core_context(beginning_equity=10000.0, forecast_ending_equity=-10000.0)
    base = _core_forecast(context).scenario_forecasts.base
    assert base.roe is None


# --- 9. missing ROE ------------------------------------------------------------

def test_missing_both_equity_balances_leaves_roe_none():
    context = _core_context()
    context.pop("beginning_equity")
    context.pop("forecast_ending_equity")
    base = _core_forecast(context).scenario_forecasts.base
    assert base.net_profit == _BASE_NET_PROFIT
    assert base.eps is not None
    assert base.roe is None
    record = _core_forecast(context).to_record("base", forecast_id=1)
    assert record.is_missing("roe")
    assert not record.is_missing("eps")


@pytest.mark.parametrize("present", ["beginning_equity", "forecast_ending_equity"])
def test_one_missing_equity_end_leaves_roe_none(present):
    # Average equity needs both ends. A single declared balance is not
    # substituted for the average and is never fabricated into one.
    context = _core_context()
    context.pop("beginning_equity" if present == "forecast_ending_equity"
                else "forecast_ending_equity")
    base = _core_forecast(context).scenario_forecasts.base
    assert base.net_profit == _BASE_NET_PROFIT
    assert base.roe is None
    assert _core_forecast(context).to_record("base", forecast_id=1).is_missing("roe")


def test_no_equity_and_no_shares_leaves_eps_and_roe_none():
    context = _core_context()
    context.pop("share_count")
    context.pop("beginning_equity")
    context.pop("forecast_ending_equity")
    base = _core_forecast(context).scenario_forecasts.base
    assert base.net_profit == _BASE_NET_PROFIT
    assert base.eps is None
    assert base.roe is None


# --- 10. ROE is derived, never independently forecast --------------------------

def test_roe_tracks_net_profit_across_scenarios():
    context = _core_context(beginning_equity=9000.0, forecast_ending_equity=11000.0)
    chains = _core_forecast(context).scenario_forecasts
    assert chains.bear.roe < chains.base.roe < chains.bull.roe
    for chain in (chains.bear, chains.base, chains.bull):
        assert chain.roe == pytest.approx(
            chain.net_profit / ((9000.0 + 11000.0) / 2.0))


def test_roe_is_unaffected_by_the_share_base():
    # EPS halves when shares double; ROE does not move, because equity is a
    # separate input to a separate derivation.
    context = _core_context(beginning_equity=9000.0, forecast_ending_equity=11000.0)
    diluted = dict(context, share_count=2000.0)
    assert _core_forecast(diluted).scenario_forecasts.base.roe == pytest.approx(
        _core_forecast(context).scenario_forecasts.base.roe)
    assert _core_forecast(diluted).scenario_forecasts.base.eps == pytest.approx(
        _core_forecast(context).scenario_forecasts.base.eps / 2.0)


# --- 11. determinism -----------------------------------------------------------

def test_eps_and_roe_are_deterministic_across_calls():
    history = [
        _ShareRecord(date(2025, 1, 1), 1_000_000),
        _ShareRecord(date(2025, 10, 1), 1_200_000),
    ]
    actions = [
        _CorporateAction("CAPITAL_INCREASE", date(2025, 4, 1),
                         old_share_count=1_000_000, new_share_count=1_600_000),
        _CorporateAction("STOCK_SPLIT", date(2025, 7, 1), ratio=2.0),
    ]
    context = _shares_context(
        history, actions, beginning_equity=9000.0, forecast_ending_equity=11000.0)
    first = _core_forecast(context).records(forecast_id_start=1)
    second = _core_forecast(context).records(forecast_id_start=1)
    assert len(first) == len(second) == 3
    for left, right in zip(first, second):
        assert left == right
    assert [r.eps for r in first] == [r.eps for r in second]
    assert [r.roe for r in first] == [r.roe for r in second]


def test_deterministic_across_reordered_share_history():
    history = [
        _ShareRecord(date(2025, 1, 1), 1_000_000),
        _ShareRecord(date(2025, 10, 1), 1_200_000),
    ]
    actions = [_CorporateAction("STOCK_SPLIT", date(2025, 7, 1), ratio=2.0)]
    first = _shares_forecast(history, actions).scenario_forecasts.base
    second = _shares_forecast(list(reversed(history)), actions
                              ).scenario_forecasts.base
    assert first.eps == second.eps
    assert first.roe == second.roe
