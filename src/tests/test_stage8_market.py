import inspect
from dataclasses import replace
from datetime import datetime, timezone
from typing import get_type_hints

import pytest

from src.core.jalali import JalaliDate
from src.market import engine as engine_module
from src.market import schema as schema_module
from src.market.engine import MarketEngine
from src.market.indicators import calculate_rsi, calculate_sma, cumulative_return, maximum_drawdown, price_position, realized_volatility
from src.market.parameters import (
    DRAWDOWN_WINDOWS,
    MARKET_REGIME_RETURN_THRESHOLD,
    MA_WINDOWS,
    PRICE_POSITION_WINDOWS,
    RETURN_HORIZONS,
    VOLATILITY_WINDOWS,
)
from src.market.schema import MarketSignalResult


def jd(index, start_year=1404):
    """Synthetic, strictly increasing, always-valid Jalali date labels.

    Twelve months of 29 days (valid in every Jalali month and year). These are
    ordering labels for isolated unit tests only, not a real trading calendar.
    """
    year = start_year + index // 348
    rem = index % 348
    return (year, rem // 29 + 1, rem % 29 + 1)


# Jalali as-of date of the 259th observation produced by ``rows`` (index 258).
AS_OF = jd(258)  # (1404, 9, 27)
FUTURE = (1405, 1, 1)


def rows(prices, volume=1000.0, value=100000.0, start_index=0):
    return [
        {"jalali_date": jd(start_index + i), "close": price, "adjusted_close": price, "volume": volume, "value": value}
        for i, price in enumerate(prices)
    ]


def without_timestamp(result):
    return replace(result, calculation_timestamp=None)


def test_legacy_indicator_helpers_remain_available():
    prices = [float(i) for i in range(1, 60)]
    assert calculate_sma(prices, 50) is not None
    assert calculate_rsi(prices, 14) == 100.0


def test_core_market_indicators():
    prices = list(range(1, 30))
    assert round(cumulative_return(prices, 5), 6) == round(29 / 24 - 1, 6)
    assert price_position(prices, 20) == 1.0
    assert maximum_drawdown(prices, 20) == 0.0
    assert realized_volatility(prices, 20) is not None


def test_market_engine_returns_state_not_score():
    prices = list(range(1, 260))
    result = MarketEngine().analyze_market(1, AS_OF, rows(prices))
    assert result.model_version == "STAGE8_V1"
    assert result.market_contract_version == "MARKET_CONTRACT_V1.1"
    assert result.trend_state in {"UPTREND", "STRONG_UPTREND"}
    assert result.momentum_state in {"POSITIVE", "STRONG_POSITIVE"}
    assert result.metadata["market_score"] is None
    assert result.metadata["decision_signal"] is None
    assert result.indicators.returns["20D"] is not None
    assert result.indicators.price_vs_ma["MA20"] is not None
    assert result.indicators.max_drawdown["252D"] == 0.0


def test_market_output_contract_includes_52w_volume_and_value_context():
    prices = list(range(1, 260))
    result = MarketEngine().analyze_market(1, AS_OF, rows(prices, volume=2000.0, value=100000.0))
    assert result.indicators.distance_from_52w_high == 0.0
    assert result.indicators.average_volume_20d == 2000.0
    assert result.indicators.average_trading_value_20d == 100000.0
    assert result.indicators.trading_value_stability_20d == 0.0
    assert result.metadata["price_basis"] == "ADJUSTED_CLOSE"


def test_trading_value_stability_is_coefficient_of_variation():
    data = rows(list(range(1, 260)), value=100000.0)
    for i, row in enumerate(data[-20:]):
        row["value"] = 100000.0 * (1.0 + i / 20.0)
    result = MarketEngine().analyze_market(1, AS_OF, data)
    assert result.indicators.trading_value_stability_20d is not None
    assert result.indicators.trading_value_stability_20d > 0.0
    assert result.metadata["trading_value_stability_definition"] == "20D coefficient_of_variation"


def test_close_fallback_is_explicitly_flagged():
    data = rows(list(range(1, 260)))
    for row in data:
        row.pop("adjusted_close")
    result = MarketEngine().analyze_market(1, AS_OF, data)
    assert result.metadata["price_basis"] == "CLOSE_FALLBACK"


def test_point_in_time_excludes_future_rows():
    prices = list(range(1, 260))
    data = rows(prices)
    data.append({"jalali_date": FUTURE, "close": 100000.0, "adjusted_close": 100000.0, "volume": 1.0, "value": 1.0})
    result = MarketEngine().analyze_market(1, AS_OF, data, point_in_time=True)
    assert result.indicators.returns["20D"] == (259 / 239 - 1)


def test_adjusted_close_drives_historical_returns():
    data = rows(list(range(1, 260)))
    for row in data:
        row["close"] = row["adjusted_close"] * 2
    result = MarketEngine().analyze_market(1, AS_OF, data)
    assert result.indicators.returns["20D"] == (259 / 239 - 1)


def test_missing_benchmark_does_not_create_synthetic_relative_strength():
    result = MarketEngine().analyze_market(1, AS_OF, rows(list(range(1, 260))))
    assert result.relative_strength_industry == "INSUFFICIENT_DATA"
    assert result.relative_strength_market == "INSUFFICIENT_DATA"
    assert result.market_regime == "INSUFFICIENT_DATA"


def test_relative_strength_uses_same_horizon():
    stock = rows(list(range(1, 260)))
    industry = rows([x * 1.5 for x in range(1, 260)])
    result = MarketEngine().analyze_market(1, AS_OF, stock, industry_benchmark=industry)
    assert result.relative_strength_industry == "NEUTRAL"


def test_negative_market_state_generates_context_alerts_not_decision():
    prices = list(range(260, 0, -1))
    result = MarketEngine().analyze_market(1, AS_OF, rows(prices))
    assert result.trend_state in {"DOWNTREND", "STRONG_DOWNTREND"}
    assert result.momentum_state in {"NEGATIVE", "STRONG_NEGATIVE"}
    assert any("DOWNTREND" in alert or "DRAWDOWN" in alert for alert in result.alerts)
    assert all(not alert.startswith("BUY") and not alert.startswith("SELL") for alert in result.alerts)


def test_drawdown_moderate_non_recovering_is_not_labeled_recovering():
    prices = [100.0] * 30
    prices[-1] = 90.0
    assert MarketEngine._drawdown_state(-0.10, prices) == "STABLE_DRAWDOWN"


def test_drawdown_recovery_requires_rebound_from_recent_low():
    prices = [100.0] * 18 + [80.0, 85.0]
    assert MarketEngine._drawdown_state(-0.15, prices) == "RECOVERING"


def test_drawdown_deep_and_new_low_states_remain_distinct():
    deep = [100.0] * 19 + [80.0]
    extreme_low = [100.0] * 19 + [50.0]
    assert MarketEngine._drawdown_state(-0.20, deep) == "DEEP_DRAWDOWN"
    assert MarketEngine._drawdown_state(-0.50, extreme_low) == "NEW_LOW"


def test_legacy_api_is_compatibility_only():
    dated_closes = [(jd(i), float(price)) for i, price in enumerate(range(1, 260))]
    result = MarketEngine().analyze_market_signals(1, AS_OF, dated_closes, 100, 50)
    assert result.metadata["market_score"] is None
    assert result.money_flow_status == "INFLOW"
    assert result.trend_state != ""
    assert result.as_of_date == AS_OF


def test_legacy_api_rejects_undated_prices_instead_of_inventing_dates():
    with pytest.raises(ValueError):
        MarketEngine().analyze_market_signals(1, AS_OF, [float(p) for p in range(1, 30)])


def test_legacy_api_rejects_duplicate_dates():
    closes = [(jd(0), 10.0), (jd(0), 11.0)]
    with pytest.raises(ValueError, match="duplicate"):
        MarketEngine().analyze_market_signals(1, AS_OF, closes)


# --- Jalali date contract -------------------------------------------------


def test_as_of_boundary_is_inclusive():
    prices = list(range(1, 260))
    on_boundary = MarketEngine().analyze_market(1, AS_OF, rows(prices))
    assert on_boundary.metadata["latest_observation_jalali_date"] == AS_OF
    assert on_boundary.indicators.returns["1D"] == 259 / 258 - 1

    day_before = MarketEngine().analyze_market(1, jd(257), rows(prices))
    assert day_before.metadata["latest_observation_jalali_date"] == jd(257)
    assert day_before.indicators.returns["1D"] == 258 / 257 - 1


def test_observations_after_as_of_are_excluded_across_day_month_and_year():
    data = rows(list(range(1, 260)))
    for later in [(1404, 9, 28), (1404, 10, 1), (1405, 1, 1), (1406, 1, 1)]:
        data.append({"jalali_date": later, "close": 1e9, "adjusted_close": 1e9, "volume": 1.0, "value": 1.0})
    result = MarketEngine().analyze_market(1, AS_OF, data)
    assert result.metadata["latest_observation_jalali_date"] == AS_OF
    assert result.indicators.returns["20D"] == (259 / 239 - 1)


def test_cutoff_compares_year_then_month_then_day_numerically():
    dates = [(1405, 1, 2), (1404, 12, 29), (1405, 1, 1), (1404, 11, 30)]
    data = [{"jalali_date": d, "close": 1.0} for d in dates]
    kept = MarketEngine._prepare_rows(data, (1405, 1, 1), True)
    # (1404, 12, 29) has a larger day than the as-of day but is an earlier month.
    assert [r["jalali_date"] for r in kept] == [(1404, 11, 30), (1404, 12, 29), (1405, 1, 1)]


def test_as_of_before_all_observations_is_insufficient_data():
    result = MarketEngine().analyze_market(1, (1403, 1, 1), rows(list(range(1, 260))))
    assert result.market_data_quality == "INSUFFICIENT_DATA"
    assert result.trend_state == "INSUFFICIENT_DATA"
    assert result.indicators.returns == {}
    assert result.as_of_date == (1403, 1, 1)
    assert result.metadata["calendar"] == "JALALI"


def test_empty_market_data_is_insufficient_data():
    result = MarketEngine().analyze_market(1, AS_OF, [])
    assert result.market_data_quality == "INSUFFICIENT_DATA"
    assert result.as_of_date == AS_OF


INVALID_JALALI_DATES = [
    (1405, 13, 1),
    (1405, 0, 1),
    (1405, 2, 0),
    (1405, 7, 31),  # Mehr has 30 days in every year
    (0, 1, 1),
    (-1405, 2, 11),
    (1405, 2),
    (1405, 2, 11, 0),
    [1405, 2, 11],
    "1405-02-11",
    (1405, 2, "11"),
    (1405.0, 2, 11),
    (True, 2, 11),
    datetime(2026, 5, 1),
    None,
]


@pytest.mark.parametrize("bad_date", INVALID_JALALI_DATES, ids=repr)
def test_invalid_as_of_date_raises_value_error(bad_date):
    with pytest.raises(ValueError):
        MarketEngine().analyze_market(1, bad_date, rows(list(range(1, 30))))
    with pytest.raises(ValueError):
        MarketEngine().analyze_market(1, bad_date, [])


@pytest.mark.parametrize("bad_date", INVALID_JALALI_DATES, ids=repr)
def test_invalid_observation_date_raises_value_error_even_if_row_is_later(bad_date):
    data = rows(list(range(1, 30)))
    data[10] = dict(data[10], jalali_date=bad_date)
    with pytest.raises(ValueError):
        MarketEngine().analyze_market(1, AS_OF, data)


def test_missing_or_gregorian_row_date_is_rejected_not_skipped():
    base = rows(list(range(1, 30)))
    missing = [dict(r) for r in base]
    del missing[3]["jalali_date"]
    with pytest.raises(ValueError, match="jalali_date"):
        MarketEngine().analyze_market(1, AS_OF, missing)

    gregorian = [dict(r) for r in base]
    gregorian[3] = {"date": datetime(2026, 1, 4), "close": 4.0, "adjusted_close": 4.0}
    with pytest.raises(ValueError, match="Gregorian"):
        MarketEngine().analyze_market(1, AS_OF, gregorian)

    ambiguous = [dict(r) for r in base]
    ambiguous[3] = dict(ambiguous[3], date=datetime(2026, 1, 4))
    with pytest.raises(ValueError, match="Gregorian"):
        MarketEngine().analyze_market(1, AS_OF, ambiguous)


def test_duplicate_jalali_dates_raise_value_error():
    data = rows(list(range(1, 30)))
    data.append(dict(data[5], close=999.0, adjusted_close=999.0))
    with pytest.raises(ValueError, match="duplicate"):
        MarketEngine().analyze_market(1, AS_OF, data)


def test_duplicate_dates_after_as_of_do_not_block_earlier_history():
    data = rows(list(range(1, 260)))
    data.append({"jalali_date": FUTURE, "close": 1.0, "adjusted_close": 1.0})
    data.append({"jalali_date": FUTURE, "close": 2.0, "adjusted_close": 2.0})
    result = MarketEngine().analyze_market(1, AS_OF, data)
    assert result.market_data_quality == "VALID"
    assert result.indicators.returns["20D"] == (259 / 239 - 1)


def test_ordering_and_repeated_execution_are_deterministic():
    prices = [100.0 + (i * 7) % 23 for i in range(259)]
    ordered = rows(prices)
    reverse = list(reversed(ordered))
    shuffled = ordered[1::2] + ordered[0::2]
    baseline = without_timestamp(MarketEngine().analyze_market(1, AS_OF, ordered))
    assert without_timestamp(MarketEngine().analyze_market(1, AS_OF, reverse)) == baseline
    assert without_timestamp(MarketEngine().analyze_market(1, AS_OF, shuffled)) == baseline
    assert without_timestamp(MarketEngine().analyze_market(1, AS_OF, ordered)) == baseline
    prepared = MarketEngine._prepare_rows(shuffled, AS_OF, True)
    assert [r["jalali_date"] for r in prepared] == [jd(i) for i in range(259)]


def test_prepare_rows_does_not_mutate_input():
    data = rows(list(range(1, 30)))
    snapshot = [dict(r) for r in data]
    MarketEngine._prepare_rows(list(reversed(data)), AS_OF, True)
    assert data == snapshot


def test_benchmark_uses_the_same_jalali_cutoff():
    stock = rows(list(range(1, 260)))
    benchmark = rows(list(range(1, 260)))
    baseline = MarketEngine().analyze_market(
        1, AS_OF, stock, industry_benchmark=benchmark, market_benchmark=benchmark
    )
    assert baseline.market_regime == "MARKET_UP"

    poisoned = benchmark + [
        {"jalali_date": FUTURE, "close": 1.0, "adjusted_close": 1.0, "volume": 1.0, "value": 1.0}
    ]
    result = MarketEngine().analyze_market(
        1, AS_OF, stock, industry_benchmark=poisoned, market_benchmark=poisoned
    )
    assert result.market_regime == "MARKET_UP"
    assert without_timestamp(result) == without_timestamp(baseline)


def test_benchmark_order_does_not_matter_and_boundary_is_inclusive():
    benchmark = rows(list(range(1, 260)))
    forward = MarketEngine._market_regime(benchmark, AS_OF)
    backward = MarketEngine._market_regime(list(reversed(benchmark)), AS_OF)
    assert forward == backward == "MARKET_UP"
    # Excluding the boundary observation changes the 20D return window.
    assert MarketEngine._prepare_rows(benchmark, AS_OF, True)[-1]["jalali_date"] == AS_OF


@pytest.mark.parametrize("which", ["industry_benchmark", "market_benchmark"])
def test_invalid_or_duplicate_benchmark_dates_fail_closed(which):
    stock = rows(list(range(1, 260)))
    bad_date = rows(list(range(1, 30)))
    bad_date[2] = dict(bad_date[2], jalali_date=(1405, 13, 1))
    with pytest.raises(ValueError):
        MarketEngine().analyze_market(1, AS_OF, stock, **{which: bad_date})

    duplicate = rows(list(range(1, 30)))
    duplicate.append(dict(duplicate[4]))
    with pytest.raises(ValueError, match="duplicate"):
        MarketEngine().analyze_market(1, AS_OF, stock, **{which: duplicate})

    gregorian = [{"date": datetime(2026, 1, 1), "close": 1.0}]
    with pytest.raises(ValueError, match="Gregorian"):
        MarketEngine().analyze_market(1, AS_OF, stock, **{which: gregorian})

    # Fails closed even when company data alone would be insufficient.
    with pytest.raises(ValueError):
        MarketEngine().analyze_market(1, AS_OF, [], **{which: bad_date})


def test_missing_benchmark_data_keeps_insufficient_data_states():
    stock = rows(list(range(1, 260)))
    for empty in (None, []):
        result = MarketEngine().analyze_market(
            1, AS_OF, stock, industry_benchmark=empty, market_benchmark=empty
        )
        assert result.relative_strength_industry == "INSUFFICIENT_DATA"
        assert result.relative_strength_market == "INSUFFICIENT_DATA"
        assert result.market_regime == "INSUFFICIENT_DATA"
    # A benchmark that lies entirely after the as-of date is empty after the cutoff.
    late = rows(list(range(1, 260)), start_index=400)
    result = MarketEngine().analyze_market(1, AS_OF, stock, industry_benchmark=late, market_benchmark=late)
    assert result.relative_strength_industry == "INSUFFICIENT_DATA"
    assert result.relative_strength_market == "INSUFFICIENT_DATA"
    assert result.market_regime == "INSUFFICIENT_DATA"


def test_missing_close_is_not_converted_to_zero_price():
    data = rows(list(range(1, 260)))
    data[-1] = dict(data[-1], close=None, adjusted_close=None)
    result = MarketEngine().analyze_market(1, AS_OF, data)
    assert result.market_data_quality == "INSUFFICIENT_DATA"
    assert result.indicators.returns == {}
    assert result.trend_state == "INSUFFICIENT_DATA"


def test_missing_adjusted_close_falls_back_to_close_without_zero_fill():
    data = rows(list(range(1, 260)))
    data[-1] = dict(data[-1], adjusted_close=None)
    result = MarketEngine().analyze_market(1, AS_OF, data)
    assert result.metadata["price_basis"] == "CLOSE_FALLBACK"
    assert result.indicators.returns["20D"] == (259 / 239 - 1)


def test_missing_volume_and_value_do_not_change_price_indicators():
    full = MarketEngine().analyze_market(1, AS_OF, rows(list(range(1, 260))))
    sparse_data = rows(list(range(1, 260)))
    for row in sparse_data:
        row["volume"] = None
        row["value"] = None
    sparse = MarketEngine().analyze_market(1, AS_OF, sparse_data)
    assert sparse.market_data_quality == "VALID"
    assert sparse.indicators.returns == full.indicators.returns
    assert sparse.indicators.volatility == full.indicators.volatility
    assert sparse.indicators.max_drawdown == full.indicators.max_drawdown
    assert sparse.indicators.price_position == full.indicators.price_position


def test_benchmark_with_missing_price_is_not_zero_filled():
    stock = rows(list(range(1, 260)))
    bench = rows(list(range(1, 260)))
    bench[-1] = dict(bench[-1], close=None, adjusted_close=None)
    result = MarketEngine().analyze_market(1, AS_OF, stock, industry_benchmark=bench)
    assert result.relative_strength_industry == "INSUFFICIENT_DATA"


def test_result_as_of_date_is_the_requested_jalali_date():
    result = MarketEngine().analyze_market(7, AS_OF, rows(list(range(1, 260))))
    assert result.company_id == 7
    assert result.as_of_date == AS_OF
    assert isinstance(result.as_of_date, tuple)
    assert result.metadata["calendar"] == "JALALI"
    assert result.metadata["as_of_jalali_date"] == AS_OF
    assert result.metadata["latest_observation_jalali_date"] == AS_OF
    assert "as_of_date" not in result.metadata

    earlier = MarketEngine().analyze_market(7, jd(200), rows(list(range(1, 260))))
    assert earlier.as_of_date == jd(200)
    assert earlier.metadata["latest_observation_jalali_date"] == jd(200)


def test_calculation_timestamp_is_separate_from_as_of_date():
    before = datetime.now(timezone.utc).replace(tzinfo=None)
    result = MarketEngine().analyze_market(1, AS_OF, rows(list(range(1, 260))))
    insufficient = MarketEngine().analyze_market(1, AS_OF, [])
    after = datetime.now(timezone.utc).replace(tzinfo=None)
    for item in (result, insufficient):
        assert isinstance(item.calculation_timestamp, datetime)
        assert before <= item.calculation_timestamp <= after
        assert item.calculation_timestamp != item.as_of_date
        assert item.as_of_date == AS_OF


def test_market_signal_result_as_of_date_is_typed_as_jalali_date():
    assert get_type_hints(MarketSignalResult)["as_of_date"] == JalaliDate
    assert get_type_hints(MarketSignalResult)["calculation_timestamp"] != JalaliDate


def test_indicator_results_match_direct_indicator_functions_on_ordered_prices():
    prices = [100.0 + ((i * 37) % 41) - (i % 5) * 0.5 for i in range(259)]
    result = MarketEngine().analyze_market(1, AS_OF, rows(prices))
    ind = result.indicators
    for name, n in RETURN_HORIZONS.items():
        assert ind.returns[name] == cumulative_return(prices, n)
    for name, n in PRICE_POSITION_WINDOWS.items():
        assert ind.price_position[name] == price_position(prices, n)
    for name, n in VOLATILITY_WINDOWS.items():
        assert ind.volatility[name] == realized_volatility(prices, n, annualized=True)
    for name, n in DRAWDOWN_WINDOWS.items():
        assert ind.max_drawdown[name] == maximum_drawdown(prices, n)
    for name, n in MA_WINDOWS.items():
        assert ind.price_vs_ma[name] == prices[-1] / calculate_sma(prices, n) - 1.0
    assert ind.sma_50 == calculate_sma(prices, 50)
    assert ind.sma_200 == calculate_sma(prices, 200)


def test_windows_count_observations_not_calendar_days():
    prices = [100.0 + (i % 9) for i in range(259)]
    contiguous = MarketEngine().analyze_market(1, AS_OF, rows(prices))
    # Same ordered sequence, but with large calendar gaps between observations.
    gapped = [
        {"jalali_date": jd(i * 3), "close": p, "adjusted_close": p, "volume": 1000.0, "value": 100000.0}
        for i, p in enumerate(prices)
    ]
    gapped_result = MarketEngine().analyze_market(1, jd(258 * 3), gapped)
    assert gapped_result.indicators == contiguous.indicators
    assert gapped_result.indicators.returns["20D"] == cumulative_return(prices, 20)


def test_equivalent_ordered_sequences_with_different_date_labels_are_identical():
    prices = [100.0 + ((i * 13) % 17) for i in range(259)]
    a = MarketEngine().analyze_market(1, jd(258), rows(prices))
    b = MarketEngine().analyze_market(1, jd(258 + 700), rows(prices, start_index=700))
    assert a.indicators == b.indicators
    for field_name in ("trend_state", "momentum_state", "volatility_state", "drawdown_state",
                       "liquidity_state", "price_volume_state", "alerts"):
        assert getattr(a, field_name) == getattr(b, field_name)


def test_stage8_core_has_no_gregorian_date_contract():
    for module in (engine_module, schema_module):
        source = inspect.getsource(module)
        assert "isoformat" not in source
        assert 'get("date")' not in source
        assert "timedelta" not in source
    engine_source = inspect.getsource(engine_module)
    assert "jdatetime" not in engine_source  # engine uses only the shared tuple validator
    assert "datetime(" not in engine_source


# --- P73: missing volume/value are missing, never zero ---------------------


def with_missing(data, field_name, positions):
    """Return rows where ``field_name`` is None at the given (negative) positions."""
    data = [dict(r) for r in data]
    for pos in positions:
        data[pos] = dict(data[pos], **{field_name: None})
    return data


def full_rows():
    # Constant volume 1000.0 and value 100000.0 over 259 ordered observations.
    return rows(list(range(1, 260)))


def test_complete_volume_and_value_baseline():
    result = MarketEngine().analyze_market(1, AS_OF, full_rows())
    ind = result.indicators
    assert ind.volume_ratio == 1.0
    assert ind.average_volume_20d == 1000.0
    assert ind.average_trading_value_20d == 100000.0
    assert ind.trading_value_stability_20d == 0.0
    assert result.liquidity_state == "NORMAL"
    assert result.price_volume_state == "WEAK_PRICE_VOLUME_CONFIRMATION"


@pytest.mark.parametrize("position", [-1, -2, -20])
def test_missing_volume_in_average_window_fails_closed_not_zero(position):
    data = with_missing(full_rows(), "volume", [position])
    result = MarketEngine().analyze_market(1, AS_OF, data)
    ind = result.indicators
    # A zero-filled window would give 950.0 for the average; missing must stay missing.
    assert ind.average_volume_20d is None
    assert ind.volume_ratio is None
    assert result.price_volume_state == "INSUFFICIENT_DATA"
    assert "INFO:ABNORMAL_VOLUME" not in result.alerts
    # Value-based metrics do not depend on volume and are unchanged.
    assert ind.average_trading_value_20d == 100000.0
    assert ind.trading_value_stability_20d == 0.0
    assert result.liquidity_state == "NORMAL"
    # Price indicators are unchanged.
    assert ind.returns == MarketEngine().analyze_market(1, AS_OF, full_rows()).indicators.returns
    assert result.market_data_quality == "VALID"


def test_missing_volume_respects_existing_window_boundaries():
    # volume_ratio reads 21 observations (latest + prior 20); the average reads 20.
    at_21 = MarketEngine().analyze_market(1, AS_OF, with_missing(full_rows(), "volume", [-21]))
    assert at_21.indicators.volume_ratio is None
    assert at_21.indicators.average_volume_20d == 1000.0

    at_22 = MarketEngine().analyze_market(1, AS_OF, with_missing(full_rows(), "volume", [-22]))
    assert at_22.indicators.volume_ratio == 1.0
    assert at_22.indicators.average_volume_20d == 1000.0


def test_missing_volume_cannot_create_abnormal_volume_or_confirmation():
    data = full_rows()
    data[-1] = dict(data[-1], volume=3000.0)
    complete = MarketEngine().analyze_market(1, AS_OF, data)
    assert complete.indicators.volume_ratio == 3.0
    assert "INFO:ABNORMAL_VOLUME" in complete.alerts
    assert complete.price_volume_state == "PRICE_VOLUME_CONFIRMATION"

    # One missing prior volume: zero-filling would lower the baseline and raise the ratio.
    missing = MarketEngine().analyze_market(1, AS_OF, with_missing(data, "volume", [-5]))
    assert missing.indicators.volume_ratio is None
    assert "INFO:ABNORMAL_VOLUME" not in missing.alerts
    assert missing.price_volume_state == "INSUFFICIENT_DATA"


def test_real_zero_volume_is_distinct_from_missing_volume():
    zero = MarketEngine().analyze_market(1, AS_OF, rows(list(range(1, 260)), volume=0.0))
    assert zero.indicators.average_volume_20d == 0.0  # a genuine observation of no volume
    assert zero.indicators.volume_ratio is None  # existing zero-average rule, unchanged

    missing = MarketEngine().analyze_market(1, AS_OF, rows(list(range(1, 260)), volume=None))
    assert missing.indicators.average_volume_20d is None
    assert missing.indicators.volume_ratio is None


@pytest.mark.parametrize("position", [-1, -10, -20])
def test_missing_value_in_last_20_fails_closed_not_zero(position):
    data = with_missing(full_rows(), "value", [position])
    result = MarketEngine().analyze_market(1, AS_OF, data)
    ind = result.indicators
    assert ind.average_trading_value_20d is None  # zero-filled would be 95000.0
    assert ind.trading_value_stability_20d is None
    assert result.liquidity_state == "INSUFFICIENT_DATA"
    assert "WARNING:LOW_LIQUIDITY" not in result.alerts
    # Volume metrics do not depend on value and are unchanged.
    assert ind.average_volume_20d == 1000.0
    assert ind.volume_ratio == 1.0
    assert result.market_data_quality == "VALID"


def test_missing_value_in_liquidity_baseline_window_fails_closed_for_liquidity_only():
    # Outside the 20-observation windows but inside the 60-observation baseline.
    for position in (-21, -60):
        result = MarketEngine().analyze_market(1, AS_OF, with_missing(full_rows(), "value", [position]))
        assert result.indicators.average_trading_value_20d == 100000.0
        assert result.indicators.trading_value_stability_20d == 0.0
        assert result.liquidity_state == "INSUFFICIENT_DATA"
        assert "WARNING:LOW_LIQUIDITY" not in result.alerts

    # Outside every window the state reads: nothing changes.
    outside = MarketEngine().analyze_market(1, AS_OF, with_missing(full_rows(), "value", [-61]))
    assert outside.indicators.average_trading_value_20d == 100000.0
    assert outside.liquidity_state == "NORMAL"


def test_missing_values_are_not_classified_as_low_liquidity_but_real_zeros_are():
    positions = list(range(-11, 0))  # 11 of the last 20 observations

    missing = MarketEngine().analyze_market(1, AS_OF, with_missing(full_rows(), "value", positions))
    assert missing.liquidity_state == "INSUFFICIENT_DATA"
    assert "WARNING:LOW_LIQUIDITY" not in missing.alerts

    zeros = full_rows()
    for pos in positions:
        zeros[pos] = dict(zeros[pos], value=0.0)
    genuine = MarketEngine().analyze_market(1, AS_OF, zeros)
    assert genuine.indicators.average_trading_value_20d == 45000.0
    assert genuine.liquidity_state == "VERY_LOW"
    assert "WARNING:LOW_LIQUIDITY" in genuine.alerts


def test_all_volume_and_value_missing_fails_closed_for_every_dependent_output():
    data = rows(list(range(1, 260)), volume=None, value=None)
    result = MarketEngine().analyze_market(1, AS_OF, data)
    ind = result.indicators
    assert ind.volume_ratio is None
    assert ind.average_volume_20d is None
    assert ind.average_trading_value_20d is None
    assert ind.trading_value_stability_20d is None
    assert result.liquidity_state == "INSUFFICIENT_DATA"
    assert result.price_volume_state == "INSUFFICIENT_DATA"
    assert "WARNING:LOW_LIQUIDITY" not in result.alerts
    assert "INFO:ABNORMAL_VOLUME" not in result.alerts
    # Price-derived outputs are still produced.
    assert result.market_data_quality == "VALID"
    assert result.trend_state in {"UPTREND", "STRONG_UPTREND"}


def test_window_helpers_do_not_fill_or_drop_missing_observations():
    engine = MarketEngine
    series = [1.0] * 19 + [None]
    assert engine._average(series, 20) is None
    assert engine._coefficient_of_variation(series, 20) is None
    assert series[-1] is None  # input not repaired

    # A missing observation outside the window is irrelevant.
    assert engine._average([None] + [1.0] * 20, 20) == 1.0
    assert engine._volume_ratio([1.0] * 20 + [None], 20) is None
    assert engine._volume_ratio([None] + [1.0] * 21, 20) == 1.0

    assert engine._liquidity_state(100.0, [100.0] * 59 + [None]) == "INSUFFICIENT_DATA"
    assert engine._liquidity_state(100.0, [None] + [100.0] * 60) == "NORMAL"


# --- P73: market-regime price fallback matches _price ----------------------


def benchmark_rows(closes, adjusted=None):
    return [
        {
            "jalali_date": jd(i),
            "close": close,
            "adjusted_close": None if adjusted is None else adjusted[i],
        }
        for i, close in enumerate(closes)
    ]


def expected_regime(closes):
    ret = cumulative_return(closes, RETURN_HORIZONS["20D"])
    if ret >= MARKET_REGIME_RETURN_THRESHOLD:
        return "MARKET_UP"
    if ret <= -MARKET_REGIME_RETURN_THRESHOLD:
        return "MARKET_DOWN"
    return "MARKET_NEUTRAL"


@pytest.mark.parametrize(
    "closes, expected",
    [
        ([100.0] * 20 + [110.0], "MARKET_UP"),
        ([100.0] * 20 + [90.0], "MARKET_DOWN"),
        ([100.0] * 20 + [102.0], "MARKET_NEUTRAL"),
    ],
)
def test_market_regime_falls_back_to_close_when_adjusted_close_is_none(closes, expected):
    bench = benchmark_rows(closes, adjusted=None)  # adjusted_close key present, value None
    assert all("adjusted_close" in r and r["adjusted_close"] is None for r in bench)
    regime = MarketEngine._market_regime(bench, jd(20))
    assert regime == expected == expected_regime(closes)
    # Identical to the same series supplied as adjusted_close.
    assert regime == MarketEngine._market_regime(benchmark_rows(closes, adjusted=closes), jd(20))


def test_market_regime_close_fallback_flows_through_analyze_market():
    closes = [100.0] * 20 + [110.0]
    result = MarketEngine().analyze_market(
        1, AS_OF, rows(list(range(1, 260))), market_benchmark=benchmark_rows(closes)
    )
    assert result.market_regime == "MARKET_UP"


def test_market_regime_does_not_fall_back_when_adjusted_close_is_numeric():
    closes = [100.0] * 20 + [110.0]
    flat_adjusted = [100.0] * 21  # numeric adjusted_close wins over a rising close
    assert MarketEngine._market_regime(benchmark_rows(closes, adjusted=flat_adjusted), jd(20)) == "MARKET_NEUTRAL"

    # Per-row choice: early rows fall back to close, the last row has a numeric adjusted_close.
    up = benchmark_rows([100.0] * 20 + [1.0], adjusted=[None] * 20 + [110.0])
    assert MarketEngine._market_regime(up, jd(20)) == "MARKET_UP"
    down = benchmark_rows([100.0] * 20 + [1000.0], adjusted=[None] * 20 + [90.0])
    assert MarketEngine._market_regime(down, jd(20)) == "MARKET_DOWN"


def test_market_regime_preserves_behavior_when_both_prices_are_missing():
    all_missing = benchmark_rows([None] * 21, adjusted=None)
    assert MarketEngine._market_regime(all_missing, jd(20)) == "INSUFFICIENT_DATA"

    # A row with neither price is skipped, not zero-filled.
    valid = benchmark_rows([100.0] * 20 + [110.0])
    valid.append({"jalali_date": jd(21), "close": None, "adjusted_close": None})
    assert MarketEngine._market_regime(valid, jd(21)) == "MARKET_UP"

    # Too few usable prices stays INSUFFICIENT_DATA.
    short = benchmark_rows([100.0] * 20)
    assert MarketEngine._market_regime(short, jd(19)) == "INSUFFICIENT_DATA"
