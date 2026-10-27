"""Tests for the Stage 8 database adapter (history query -> Jalali engine rows -> engine).

Data is synthetic and lives only in an in-memory SQLite database created per
test. These tests cover the adapter contract; they are not evidence of a full
Stage 7-8-9 pipeline.
"""

from dataclasses import replace
from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.core.database import Base
from src.ingestion.market.queries import MarketHistoryObservation, select_market_history_as_of
from src.market import service as market_service
from src.market.indicators import cumulative_return
from src.market.service import analyze_market_as_of_jalali, market_history_to_engine_rows
from src.models.entity import Company, Industry
from src.models.market import MarketDaily


def jd(index, start_year=1404):
    """Synthetic always-valid, strictly increasing Jalali labels (29-day months)."""
    year = start_year + index // 348
    rem = index % 348
    return (year, rem // 29 + 1, rem % 29 + 1)


AS_OF = jd(258)  # (1404, 9, 27)


@pytest.fixture
def db():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        industry = Industry(industry_code="PETROCHEMICAL", industry_name="Petrochemical")
        session.add(industry)
        session.flush()
        first = Company(ticker="AAA", company_name="First", industry_id=industry.industry_id)
        second = Company(ticker="BBB", company_name="Second", industry_id=industry.industry_id)
        session.add_all([first, second])
        session.flush()
        yield session, first.company_id, second.company_id
    engine.dispose()


def _row(company_id, date, close, **overrides):
    year, month, day = date
    values = dict(
        company_id=company_id,
        jalali_year=year,
        jalali_month=month,
        jalali_day=day,
        close_price=None if close is None else Decimal(str(close)),
    )
    values.update(overrides)
    return MarketDaily(**values)


def _add_series(session, company_id, prices, start_index=0, **overrides):
    session.add_all([
        _row(company_id, jd(start_index + i), p, volume=1000, value=Decimal("100000.00"), **overrides)
        for i, p in enumerate(prices)
    ])
    session.flush()


def _observation(company_id, date, **overrides):
    values = dict(
        market_data_id=1, company_id=company_id, jalali_date=date,
        open_price=None, high_price=None, low_price=None,
        close_price=Decimal("10.00"), adjusted_close=None,
        volume=None, value=None, trade_count=None, source=None,
    )
    values.update(overrides)
    return MarketHistoryObservation(**values)


def test_adapter_runs_real_query_into_engine_with_jalali_as_of(db):
    session, company_id, _ = db
    _add_series(session, company_id, range(1, 260))

    result = analyze_market_as_of_jalali(session, company_id, AS_OF)

    assert result.company_id == company_id
    assert result.as_of_date == AS_OF
    assert result.market_data_quality == "VALID"
    assert result.indicators.returns["20D"] == cumulative_return([float(p) for p in range(1, 260)], 20)
    assert result.metadata["calendar"] == "JALALI"
    assert result.metadata["as_of_jalali_date"] == AS_OF
    assert result.metadata["latest_observation_jalali_date"] == AS_OF
    assert result.metadata["price_basis"] == "CLOSE_FALLBACK"  # no adjusted_close stored


def test_adapter_delegates_selection_to_existing_query(db, monkeypatch):
    session, company_id, _ = db
    _add_series(session, company_id, range(1, 30))
    calls = []

    def spy(sess, cid, as_of):
        calls.append((sess, cid, as_of))
        return select_market_history_as_of(sess, cid, as_of)

    monkeypatch.setattr(market_service, "select_market_history_as_of", spy)
    analyze_market_as_of_jalali(session, company_id, jd(28))
    assert calls == [(session, company_id, jd(28))]


def test_adapter_as_of_boundary_is_inclusive_and_future_rows_are_excluded(db):
    session, company_id, _ = db
    _add_series(session, company_id, range(1, 260))
    for later, price in [((1404, 9, 28), 1), ((1404, 10, 1), 1), ((1405, 1, 1), 1), ((1406, 1, 1), 1)]:
        session.add(_row(company_id, later, price))
    session.flush()

    on_boundary = analyze_market_as_of_jalali(session, company_id, AS_OF)
    assert on_boundary.metadata["latest_observation_jalali_date"] == AS_OF
    assert on_boundary.indicators.returns["1D"] == 259 / 258 - 1

    day_before = analyze_market_as_of_jalali(session, company_id, jd(257))
    assert day_before.metadata["latest_observation_jalali_date"] == jd(257)
    assert day_before.indicators.returns["1D"] == 258 / 257 - 1


def test_adapter_as_of_before_all_rows_and_no_rows_are_insufficient_data(db):
    session, company_id, other_id = db
    _add_series(session, company_id, range(1, 260))

    early = analyze_market_as_of_jalali(session, company_id, (1403, 1, 1))
    assert early.market_data_quality == "INSUFFICIENT_DATA"
    assert early.as_of_date == (1403, 1, 1)

    nothing = analyze_market_as_of_jalali(session, other_id, AS_OF)
    assert nothing.market_data_quality == "INSUFFICIENT_DATA"
    assert nothing.company_id == other_id


def test_adapter_isolates_company_identity(db):
    session, first_id, second_id = db
    _add_series(session, first_id, range(1, 260))
    _add_series(session, second_id, [1000000] * 259)

    first = analyze_market_as_of_jalali(session, first_id, AS_OF)
    second = analyze_market_as_of_jalali(session, second_id, AS_OF)

    assert first.company_id == first_id
    assert second.company_id == second_id
    assert first.indicators.returns["20D"] == 259 / 239 - 1
    assert second.indicators.returns["20D"] == 0.0


def test_engine_rows_preserve_identity_source_dates_and_none_values(db):
    session, company_id, _ = db
    session.add_all([
        _row(
            company_id, (1405, 2, 1), "100.00",
            open_price=Decimal("99.00"), high_price=Decimal("101.00"), low_price=Decimal("98.00"),
            adjusted_close=Decimal("100.50"), volume=1500, value=Decimal("150000.00"),
            trade_count=12, source="CSV_PROVIDER",
        ),
        _row(company_id, (1405, 2, 2), "101.00"),
    ])
    session.flush()
    history = select_market_history_as_of(session, company_id, (1405, 2, 11))

    full, sparse = market_history_to_engine_rows(history)

    assert [full["jalali_date"], sparse["jalali_date"]] == [(1405, 2, 1), (1405, 2, 2)]
    assert [obs.jalali_date for obs in history] == [full["jalali_date"], sparse["jalali_date"]]
    assert full["company_id"] == sparse["company_id"] == company_id
    assert full["market_data_id"] == history[0].market_data_id
    assert full["open"] == Decimal("99.00") and full["high"] == Decimal("101.00")
    assert full["low"] == Decimal("98.00") and full["close"] == Decimal("100.00")
    assert full["adjusted_close"] == Decimal("100.50")
    assert full["volume"] == 1500 and full["value"] == Decimal("150000.00")
    assert full["trade_count"] == 12 and full["source"] == "CSV_PROVIDER"
    for key in ("open", "high", "low", "adjusted_close", "volume", "value", "trade_count", "source"):
        assert sparse[key] is None, key  # missing source values are never zero-filled
    assert sparse["close"] == Decimal("101.00")
    assert all("date" not in row for row in (full, sparse))  # no Gregorian date key
    assert all(isinstance(row["jalali_date"], tuple) for row in (full, sparse))


def test_adapter_does_not_zero_fill_or_invent_missing_prices(db):
    session, company_id, _ = db
    _add_series(session, company_id, range(1, 259))
    session.add(_row(company_id, jd(258), None))  # row exists, but has no price at all
    session.flush()

    result = analyze_market_as_of_jalali(session, company_id, AS_OF)

    assert result.market_data_quality == "INSUFFICIENT_DATA"
    assert result.indicators.returns == {}


def test_adapter_duplicate_company_date_fails_explicitly(db):
    session, company_id, _ = db
    _add_series(session, company_id, range(1, 30))
    session.add(_row(company_id, jd(5), 77))
    session.flush()
    with pytest.raises(ValueError, match="duplicate"):
        analyze_market_as_of_jalali(session, company_id, jd(28))


@pytest.mark.parametrize("bad_date", [(1405, 13, 1), (1405, 2, 0), (1405, 2), [1405, 2, 11], "1405-02-11", None])
def test_adapter_rejects_invalid_as_of_dates(db, bad_date):
    session, company_id, _ = db
    with pytest.raises(ValueError):
        analyze_market_as_of_jalali(session, company_id, bad_date)


def test_adapter_rejects_history_of_another_company(db, monkeypatch):
    session, company_id, _ = db
    foreign = (_observation(company_id + 1, (1405, 2, 1)),)
    monkeypatch.setattr(market_service, "select_market_history_as_of", lambda *a, **k: foreign)
    with pytest.raises(ValueError, match="other companies"):
        analyze_market_as_of_jalali(session, company_id, (1405, 2, 11))


def test_adapter_fails_explicitly_on_invalid_observation_date_from_query(db, monkeypatch):
    session, company_id, _ = db
    broken = (_observation(company_id, (1405, 13, 1)),)
    monkeypatch.setattr(market_service, "select_market_history_as_of", lambda *a, **k: broken)
    with pytest.raises(ValueError):
        analyze_market_as_of_jalali(session, company_id, (1405, 2, 11))


def test_adapter_benchmarks_use_the_same_jalali_cutoff(db):
    session, company_id, _ = db
    _add_series(session, company_id, range(1, 260))
    benchmark = [
        {"jalali_date": jd(i), "close": float(i + 1), "adjusted_close": float(i + 1)} for i in range(259)
    ]
    baseline = analyze_market_as_of_jalali(
        session, company_id, AS_OF, industry_benchmark=benchmark, market_benchmark=benchmark
    )
    assert baseline.market_regime == "MARKET_UP"

    poisoned = benchmark + [{"jalali_date": (1405, 1, 1), "close": 1.0, "adjusted_close": 1.0}]
    result = analyze_market_as_of_jalali(
        session, company_id, AS_OF, industry_benchmark=poisoned, market_benchmark=poisoned
    )
    assert replace(result, calculation_timestamp=None) == replace(baseline, calculation_timestamp=None)

    missing = analyze_market_as_of_jalali(session, company_id, AS_OF)
    assert missing.relative_strength_industry == "INSUFFICIENT_DATA"
    assert missing.relative_strength_market == "INSUFFICIENT_DATA"
    assert missing.market_regime == "INSUFFICIENT_DATA"


def test_adapter_repeated_execution_is_deterministic(db):
    session, company_id, _ = db
    # Insert out of chronological order; the query orders, the engine re-validates.
    prices = [100 + (i * 7) % 23 for i in range(259)]
    for i in reversed(range(259)):
        session.add(_row(company_id, jd(i), prices[i], volume=1000, value=Decimal("100000.00")))
    session.flush()

    first = analyze_market_as_of_jalali(session, company_id, AS_OF)
    second = analyze_market_as_of_jalali(session, company_id, AS_OF)
    assert replace(first, calculation_timestamp=None) == replace(second, calculation_timestamp=None)
    assert first.indicators.returns["1D"] == prices[-1] / prices[-2] - 1


def test_adapter_has_no_gregorian_conversion():
    import inspect

    source = inspect.getsource(market_service)
    for forbidden in ("jdatetime", "fromisoformat", "isoformat", "strptime", "timedelta", "datetime("):
        assert forbidden not in source, forbidden


# --- P74: numeric validation across the adapter boundary -------------------
#
# ``market_history_to_engine_rows`` copies attribute values verbatim, so a
# non-finite observation value reaches ``MarketEngine`` unchanged. These tests
# use the existing pattern of substituting the query result with
# ``MarketHistoryObservation`` objects (as the date/foreign-company tests do);
# they prove the adapter -> engine boundary, NOT that the database can store or
# return such values (the model/query sources are outside this test module).

NON_FINITE_OBSERVATION_VALUES = [
    Decimal("NaN"), Decimal("Infinity"), Decimal("-Infinity"), float("nan"), float("inf"), float("-inf"),
]


def _history(company_id, size=3, **last_overrides):
    """Observations on jd(0..size-1); ``last_overrides`` apply to the final one."""
    history = [
        _observation(company_id, jd(i), market_data_id=i + 1, volume=1000, value=Decimal("100000.00"))
        for i in range(size - 1)
    ]
    values = dict(volume=1000, value=Decimal("100000.00"))
    values.update(last_overrides)
    history.append(_observation(company_id, jd(size - 1), market_data_id=size, **values))
    return tuple(history)


def _use_history(monkeypatch, history):
    monkeypatch.setattr(market_service, "select_market_history_as_of", lambda *a, **k: history)


@pytest.mark.parametrize("bad", NON_FINITE_OBSERVATION_VALUES, ids=repr)
def test_adapter_maps_non_finite_values_verbatim_without_filtering_or_zero_fill(bad):
    (row,) = market_history_to_engine_rows([
        _observation(1, jd(0), close_price=bad, adjusted_close=bad, volume=bad, value=bad)
    ])
    for key in ("close", "adjusted_close", "volume", "value"):
        assert row[key] is bad, key  # not transformed, dropped or replaced by 0


@pytest.mark.parametrize("bad", NON_FINITE_OBSERVATION_VALUES, ids=repr)
@pytest.mark.parametrize("field_name", ["close_price", "adjusted_close", "volume", "value"])
def test_adapter_non_finite_observation_value_is_rejected_by_the_engine(db, monkeypatch, field_name, bad):
    session, company_id, _ = db
    _use_history(monkeypatch, _history(company_id, **{field_name: bad}))
    with pytest.raises(ValueError, match="Non-finite numeric value"):
        analyze_market_as_of_jalali(session, company_id, jd(2))


@pytest.mark.parametrize("which", ["industry_benchmark", "market_benchmark"])
@pytest.mark.parametrize("bad", [float("nan"), float("inf"), float("-inf")], ids=repr)
def test_adapter_non_finite_benchmark_price_is_rejected_with_real_history(db, which, bad):
    session, company_id, _ = db
    _add_series(session, company_id, range(1, 260))
    benchmark = [
        {"jalali_date": jd(i), "close": float(i + 1), "adjusted_close": float(i + 1)} for i in range(259)
    ]
    benchmark[-1] = dict(benchmark[-1], adjusted_close=bad)
    with pytest.raises(ValueError, match="Non-finite numeric value"):
        analyze_market_as_of_jalali(session, company_id, AS_OF, **{which: benchmark})


@pytest.mark.parametrize("which", ["industry_benchmark", "market_benchmark"])
def test_adapter_non_finite_benchmark_is_rejected_even_without_company_history(db, which):
    session, _, other_id = db  # no market rows stored: the engine's early-return path
    benchmark = [{"jalali_date": jd(i), "close": float(i + 1), "adjusted_close": float("inf")} for i in range(5)]
    with pytest.raises(ValueError, match="Non-finite numeric value"):
        analyze_market_as_of_jalali(session, other_id, AS_OF, **{which: benchmark})


def test_adapter_zero_and_missing_volume_and_value_remain_valid_observations(db, monkeypatch):
    session, company_id, _ = db
    _use_history(monkeypatch, _history(company_id, volume=0, value=Decimal("0")))
    zero = analyze_market_as_of_jalali(session, company_id, jd(2))
    assert zero.market_data_quality == "VALID"

    _use_history(monkeypatch, _history(company_id, volume=None, value=None))
    missing = analyze_market_as_of_jalali(session, company_id, jd(2))
    assert missing.market_data_quality == "VALID"
