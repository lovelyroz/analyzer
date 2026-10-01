from dataclasses import dataclass
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
