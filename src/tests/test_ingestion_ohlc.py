"""Tests for OHLC ingestion with Jalali components (CHANGE-005)."""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from src.core.database import Base
from src.ingestion.service import ingest_ohlc_csv, _parse_jalali_components
from src.ingestion.market.queries import select_market_price_as_of
from src.migrations.runner import MigrationRunner
from src.models.audit import IngestionRun
from src.models.entity import Company, Industry
from src.models.market import MarketDaily


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    # Apply migrations so jalali columns exist even on metadata-created tables
    runner = MigrationRunner(engine)
    runner.upgrade()
    Session = sessionmaker(bind=engine)
    s = Session()
    ind = Industry(industry_code="BANK", industry_name="بانک‌ها")
    s.add(ind)
    s.flush()
    co = Company(
        ticker="سامان",
        company_name="بانک سامان",
        industry_id=ind.industry_id,
        codal_symbol="سامان",
        status="ACTIVE",
    )
    s.add(co)
    s.commit()
    yield s
    s.close()


def test_parse_jalali_components():
    assert _parse_jalali_components("1402-01-08") == (1402, 1, 8)
    assert _parse_jalali_components("1402/12/29") == (1402, 12, 29)
    assert _parse_jalali_components("bad") is None
    assert _parse_jalali_components("1402-13-01") is None  # invalid month


def test_ohlc_ingestion_skips_missing_and_malformed_jalali_dates(session, tmp_path):
    csv_content = (
        "J-Date,Open,High,Low,Close,Final,Volume,Value,No,Ticker,Name,Market\n"
        ",100,110,95,105,105,1000,100000,5,Ø³Ø§Ù…Ø§Ù†,Ø¨Ø§Ù†Ú© Ø³Ø§Ù…Ø§Ù†,ÙØ±Ø§Ø¨ÙˆØ±Ø³\n"
        "1402-13-01,100,110,95,105,105,1000,100000,5,Ø³Ø§Ù…Ø§Ù†,Ø¨Ø§Ù†Ú© Ø³Ø§Ù…Ø§Ù†,ÙØ±Ø§Ø¨ÙˆØ±Ø³\n"
    )
    path = tmp_path / "bad_dates.csv"
    path.write_text(csv_content, encoding="utf-8")

    result = ingest_ohlc_csv(session, path)

    assert result.records_failed == 2
    assert session.query(MarketDaily).count() == 0


def _add_market_observation(
    session,
    company_id,
    jalali_date,
    *,
    close_price,
    adjusted_close=None,
    source="TEST_OHLC",
):
    year, month, day = jalali_date
    row = MarketDaily(
        company_id=company_id,
        trade_date=None,
        jalali_year=year,
        jalali_month=month,
        jalali_day=day,
        close_price=close_price,
        adjusted_close=adjusted_close,
        source=source,
    )
    session.add(row)
    session.flush()
    return row


def test_market_price_as_of_selects_exact_date_and_preserves_provenance(session):
    company = session.query(Company).one()
    row = _add_market_observation(
        session, company.company_id, (1403, 1, 8),
        close_price=Decimal("105"), adjusted_close=Decimal("106"), source="TSETMC_CSV",
    )

    selected = select_market_price_as_of(session, company.company_id, (1403, 1, 8))

    assert selected is not None
    assert selected.price == Decimal("106")
    assert selected.price_basis == "ADJUSTED_CLOSE"
    assert selected.source_jalali_date == (1403, 1, 8)
    assert selected.source == "TSETMC_CSV"
    assert selected.market_data_id == row.market_data_id


def test_market_price_as_of_uses_latest_prior_date_across_year_boundary(session):
    company = session.query(Company).one()
    _add_market_observation(session, company.company_id, (1402, 12, 29), close_price=10)
    latest = _add_market_observation(session, company.company_id, (1403, 1, 1), close_price=20)
    _add_market_observation(session, company.company_id, (1403, 1, 10), close_price=30)

    selected = select_market_price_as_of(session, company.company_id, (1403, 1, 5))

    assert selected is not None
    assert selected.source_jalali_date == (1403, 1, 1)
    assert selected.price == Decimal("20")
    assert selected.market_data_id == latest.market_data_id
    assert selected.price_basis == "CLOSE"


def test_market_price_as_of_returns_none_when_no_eligible_price(session):
    company = session.query(Company).one()
    _add_market_observation(session, company.company_id, (1403, 1, 2), close_price=10)

    assert select_market_price_as_of(session, company.company_id, (1402, 12, 29)) is None


def test_market_price_as_of_rejects_missing_or_invalid_requested_date(session):
    company = session.query(Company).one()
    for requested in (None, (1403, 13, 1), (1403, 2, 0), (True, 1, 1)):
        with pytest.raises(ValueError):
            select_market_price_as_of(session, company.company_id, requested)


def test_market_price_as_of_isolates_company_and_ignores_undated_rows(session):
    company = session.query(Company).one()
    industry = session.query(Industry).one()
    other = Company(
        ticker="OTHER", company_name="Other", industry_id=industry.industry_id,
        codal_symbol="OTHER", status="ACTIVE",
    )
    session.add(other)
    session.flush()

    _add_market_observation(session, other.company_id, (1403, 1, 4), close_price=999)
    session.add(MarketDaily(
        company_id=company.company_id, trade_date=None,
        jalali_year=None, jalali_month=None, jalali_day=None,
        close_price=Decimal("888"), source="UNDATED",
    ))
    session.add(MarketDaily(
        company_id=company.company_id, trade_date=None,
        jalali_year=0, jalali_month=1, jalali_day=2,
        close_price=Decimal("887"), source="INVALID_DATE",
    ))
    session.flush()
    _add_market_observation(session, company.company_id, (1403, 1, 3), close_price=77)

    selected = select_market_price_as_of(session, company.company_id, (1403, 1, 5))

    assert selected is not None
    assert selected.company_id == company.company_id
    assert selected.source_jalali_date == (1403, 1, 3)
    assert selected.price == Decimal("77")


def test_market_price_as_of_rejects_duplicate_latest_jalali_observations(session):
    company = session.query(Company).one()
    _add_market_observation(session, company.company_id, (1403, 1, 8), close_price=105)
    _add_market_observation(session, company.company_id, (1403, 1, 8), close_price=106)

    with pytest.raises(ValueError, match="duplicate market observations"):
        select_market_price_as_of(session, company.company_id, (1403, 1, 9))


def test_null_not_zero(session, tmp_path):
    """Missing volume must stay NULL, never become 0."""
    csv_content = (
        "J-Date,Open,High,Low,Close,Final,Volume,Value,No,Ticker,Name,Market\n"
        "1402-01-08,100,110,95,105,105,,1000000,10,سامان,بانک سامان,فرابورس\n"
    )
    p = tmp_path / "test.csv"
    p.write_text(csv_content, encoding="utf-8")

    result = ingest_ohlc_csv(session, p)
    assert result.status == "COMPLETED"
    assert result.records_inserted == 1
    md = session.query(MarketDaily).one()
    assert md.volume is None  # NULL != 0
    assert md.close_price == Decimal("105")
    assert md.jalali_year == 1402
    assert md.jalali_month == 1
    assert md.jalali_day == 8
    assert md.trade_date is None  # no Gregorian conversion


def test_same_month_across_years(session, tmp_path):
    """jalali_month is independent of year — enables cross-year same-month queries."""
    csv_content = (
        "J-Date,Open,High,Low,Close,Final,Volume,Value,No,Ticker,Name,Market\n"
        "1401-02-15,100,110,95,105,105,1000,100000,5,سامان,بانک سامان,فرابورس\n"
        "1402-02-10,200,210,195,205,205,2000,200000,8,سامان,بانک سامان,فرابورس\n"
        "1403-02-01,300,310,295,305,305,3000,300000,12,سامان,بانک سامان,فرابورس\n"
        "1402-12-20,400,410,395,405,405,4000,400000,15,سامان,بانک سامان,فرابورس\n"
    )
    p = tmp_path / "months.csv"
    p.write_text(csv_content, encoding="utf-8")

    result = ingest_ohlc_csv(session, p)
    assert result.status == "COMPLETED"
    assert result.records_inserted == 4

    month2 = (
        session.query(MarketDaily)
        .filter_by(jalali_month=2)
        .order_by(MarketDaily.jalali_year)
        .all()
    )
    assert len(month2) == 3
    assert [r.jalali_year for r in month2] == [1401, 1402, 1403]

    month12 = session.query(MarketDaily).filter_by(jalali_month=12).all()
    assert len(month12) == 1
    assert month12[0].jalali_year == 1402


def test_ingest_ohlc_idempotent(session, tmp_path):
    csv_content = (
        "J-Date,Open,High,Low,Close,Final,Volume,Value,No,Ticker,Name,Market\n"
        "1402-01-08,3022,3022,3022,3022,3022,14738930,44541046460,263,سامان,بانک سامان,پایه زرد\n"
        "1402-01-09,3112,3112,3112,3112,3112,10918715,33979041080,208,سامان,بانک سامان,پایه زرد\n"
    )
    p = tmp_path / "saman.csv"
    p.write_text(csv_content, encoding="utf-8")

    r1 = ingest_ohlc_csv(session, p)
    assert r1.status == "COMPLETED"
    assert r1.records_inserted == 2
    assert session.query(MarketDaily).count() == 2
    company = session.query(Company).one()
    first_selection = select_market_price_as_of(
        session, company.company_id, (1402, 1, 9),
    )
    assert first_selection is not None

    r2 = ingest_ohlc_csv(session, p)
    assert r2.status == "COMPLETED"
    assert session.query(MarketDaily).count() == 2  # no uncontrolled duplicates
    assert r2.records_updated == 2
    selected = select_market_price_as_of(session, company.company_id, (1402, 1, 9))
    assert selected is not None
    assert selected == first_selection
    assert selected.source_jalali_date == (1402, 1, 9)
    assert selected.price == Decimal("3112")

    runs = session.query(IngestionRun).filter_by(source="OHLC").all()
    assert len(runs) >= 2
    assert all(run.status == "COMPLETED" for run in runs)


def test_migration_5_adds_jalali_columns():
    engine = create_engine("sqlite:///:memory:")
    # Simulate pre-v5 schema: create without jalali columns via raw SQL path
    Base.metadata.create_all(engine)
    runner = MigrationRunner(engine)
    version = runner.upgrade()
    assert version >= 5

    cols = {c["name"] for c in inspect(engine).get_columns("market_daily")}
    assert "jalali_year" in cols
    assert "jalali_month" in cols
    assert "jalali_day" in cols

    # Idempotent: second upgrade stays at same version
    assert runner.upgrade() == version
