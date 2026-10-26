"""Regression tests for the Stage 8 historical market-row retrieval query.

These tests cover only the persistence-side contract of
``select_market_history_as_of``: Jalali as-of boundary, deterministic ordering,
company isolation, and no fabrication of missing values. They do not exercise
``MarketEngine`` (a Jalali-to-engine-date contract is not yet defined), so they
are not evidence of an end-to-end Stage 8 production path.
"""

from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.core.database import Base
from src.ingestion.market.queries import (
    MarketHistoryObservation,
    select_market_history_as_of,
)
from src.models.entity import Company, Industry
from src.models.market import MarketDaily


@pytest.fixture
def history_session():
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


def _row(company_id, date, close="100.00", **overrides):
    year, month, day = date
    values = dict(
        company_id=company_id,
        jalali_year=year,
        jalali_month=month,
        jalali_day=day,
        close_price=Decimal(close),
    )
    values.update(overrides)
    return MarketDaily(**values)


def test_history_is_ordered_oldest_first_across_month_and_year_boundaries(history_session):
    session, company_id, _ = history_session
    # Inserted deliberately out of chronological order.
    for date in [(1405, 1, 2), (1404, 12, 29), (1405, 1, 1), (1404, 11, 30), (1405, 2, 5)]:
        session.add(_row(company_id, date))
    session.flush()

    history = select_market_history_as_of(session, company_id, (1405, 2, 5))

    assert [obs.jalali_date for obs in history] == [
        (1404, 11, 30), (1404, 12, 29), (1405, 1, 1), (1405, 1, 2), (1405, 2, 5),
    ]
    assert all(isinstance(obs, MarketHistoryObservation) for obs in history)
    assert isinstance(history, tuple)


def test_history_as_of_boundary_is_inclusive_and_excludes_every_future_row(history_session):
    session, company_id, _ = history_session
    on_boundary = (1405, 2, 11)
    session.add_all([
        _row(company_id, (1405, 2, 10)),
        _row(company_id, on_boundary),
        _row(company_id, (1405, 2, 12)),   # later day, same month
        _row(company_id, (1405, 3, 1)),    # later month, same year
        _row(company_id, (1406, 1, 1), close="999999.00"),  # later year
    ])
    session.flush()

    history = select_market_history_as_of(session, company_id, on_boundary)

    assert [obs.jalali_date for obs in history] == [(1405, 2, 10), on_boundary]
    assert Decimal("999999.00") not in {obs.close_price for obs in history}


def test_history_earlier_month_with_larger_day_is_not_excluded(history_session):
    session, company_id, _ = history_session
    # Day 29 of an earlier month must be kept even though 29 > as-of day 3.
    session.add_all([_row(company_id, (1405, 1, 29)), _row(company_id, (1405, 2, 3))])
    session.flush()

    history = select_market_history_as_of(session, company_id, (1405, 2, 3))

    assert [obs.jalali_date for obs in history] == [(1405, 1, 29), (1405, 2, 3)]


def test_history_is_isolated_by_company(history_session):
    session, first_id, second_id = history_session
    session.add_all([
        _row(first_id, (1405, 2, 1), close="100.00"),
        _row(second_id, (1405, 2, 1), close="200.00"),
        _row(second_id, (1405, 2, 2), close="210.00"),
    ])
    session.flush()

    first = select_market_history_as_of(session, first_id, (1405, 2, 11))
    second = select_market_history_as_of(session, second_id, (1405, 2, 11))

    assert [obs.close_price for obs in first] == [Decimal("100.00")]
    assert {obs.company_id for obs in first} == {first_id}
    assert [obs.close_price for obs in second] == [Decimal("200.00"), Decimal("210.00")]


def test_history_without_rows_returns_empty_tuple(history_session):
    session, company_id, _ = history_session
    session.add(_row(company_id, (1405, 3, 1)))  # only a future row exists
    session.flush()

    assert select_market_history_as_of(session, company_id, (1405, 2, 11)) == ()


def test_history_excludes_legacy_rows_without_complete_jalali_date(history_session):
    session, company_id, _ = history_session
    session.add_all([
        _row(company_id, (1405, 2, 1)),
        MarketDaily(company_id=company_id, close_price=Decimal("50.00")),
        MarketDaily(company_id=company_id, jalali_year=1405, jalali_month=2, close_price=Decimal("51.00")),
    ])
    session.flush()

    history = select_market_history_as_of(session, company_id, (1405, 2, 11))

    assert [obs.jalali_date for obs in history] == [(1405, 2, 1)]


def test_history_preserves_missing_values_as_none_and_provenance(history_session):
    session, company_id, _ = history_session
    session.add_all([
        _row(
            company_id, (1405, 2, 1), close="100.00",
            open_price=Decimal("99.00"), high_price=Decimal("101.00"),
            low_price=Decimal("98.00"), adjusted_close=Decimal("100.50"),
            volume=1500, value=Decimal("150000.00"), trade_count=12, source="CSV_PROVIDER",
        ),
        _row(company_id, (1405, 2, 2), close="101.00"),  # all optional fields absent
    ])
    session.flush()

    full, sparse = select_market_history_as_of(session, company_id, (1405, 2, 11))

    assert full.open_price == Decimal("99.00")
    assert full.high_price == Decimal("101.00")
    assert full.low_price == Decimal("98.00")
    assert full.adjusted_close == Decimal("100.50")
    assert full.volume == 1500
    assert full.value == Decimal("150000.00")
    assert full.trade_count == 12
    assert full.source == "CSV_PROVIDER"
    assert full.market_data_id is not None

    assert sparse.close_price == Decimal("101.00")
    for field_name in ("open_price", "high_price", "low_price", "adjusted_close",
                       "volume", "value", "trade_count", "source"):
        assert getattr(sparse, field_name) is None, field_name


def test_history_duplicate_company_date_fails_explicitly(history_session):
    session, company_id, _ = history_session
    session.add_all([
        _row(company_id, (1405, 2, 1)),
        _row(company_id, (1405, 2, 2), close="101.00"),
        _row(company_id, (1405, 2, 2), close="102.00"),
    ])
    session.flush()

    with pytest.raises(ValueError, match="duplicate market observations"):
        select_market_history_as_of(session, company_id, (1405, 2, 11))


def test_history_duplicate_after_as_of_does_not_block_earlier_history(history_session):
    session, company_id, _ = history_session
    session.add_all([
        _row(company_id, (1405, 2, 1)),
        _row(company_id, (1405, 2, 20), close="101.00"),
        _row(company_id, (1405, 2, 20), close="102.00"),
    ])
    session.flush()

    history = select_market_history_as_of(session, company_id, (1405, 2, 11))

    assert [obs.jalali_date for obs in history] == [(1405, 2, 1)]


# (1405, 13, 1) and (1405, 2, 0) rely on the shared Jalali validator, whose parser
# (src/ingestion/common/parsing.py) was not part of the inspected package.
@pytest.mark.parametrize(
    "bad_date",
    [
        (1405, 13, 1),
        (1405, 2, 0),
        (1405, 2),
        [1405, 2, 11],
        "1405-02-11",
        (1405, 2, "11"),
        (1405.0, 2, 11),
        None,
    ],
)
def test_history_rejects_invalid_as_of_dates(history_session, bad_date):
    session, company_id, _ = history_session
    with pytest.raises(ValueError):
        select_market_history_as_of(session, company_id, bad_date)
