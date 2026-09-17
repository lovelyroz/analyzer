"""Tests for OHLC ingestion with Jalali components (CHANGE-005)."""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path

import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from src.core.database import Base
from src.ingestion.service import ingest_ohlc_csv, _parse_jalali_components
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

    r2 = ingest_ohlc_csv(session, p)
    assert r2.status == "COMPLETED"
    assert session.query(MarketDaily).count() == 2  # no uncontrolled duplicates
    assert r2.records_updated == 2

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
