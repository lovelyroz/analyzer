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
