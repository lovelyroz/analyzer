"""Tests for OHLC / MarketDaily production ingestion."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.database import Base
from src.ingestion.common.jalali import jalali_to_gregorian, parse_jalali_date
from src.ingestion.common.validation import validate_ohlc_consistency
from src.ingestion.market.parser import parse_ohlc_csv
from src.ingestion.market.ingestion import ingest_ohlc_csv
from src.models.entity import Company, Industry
from src.models.market import MarketDaily
from src.models.audit import IngestionRun


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    s = Session()
    ind = Industry(industry_code="BANK", industry_name="\u0628\u0627\u0646\u06a9\u200c\u0647\u0627")
    s.add(ind)
    s.flush()
    co = Company(
        ticker="\u0633\u0627\u0645\u0627\u0646",
        company_name="\u0628\u0627\u0646\u06a9 \u0633\u0627\u0645\u0627\u0646",
        industry_id=ind.industry_id,
        codal_symbol="\u0633\u0627\u0645\u0627\u0646",
        status="ACTIVE",
    )
    s.add(co)
    s.commit()
    yield s
    s.close()


def test_jalali_conversion_basic():
    d = jalali_to_gregorian(1402, 1, 8)
    assert isinstance(d, date)
    assert d.year == 2023
    assert d.month == 3


def test_parse_jalali_date_string():
    d = parse_jalali_date("1402-01-08")
    assert d == jalali_to_gregorian(1402, 1, 8)


def test_ohlc_consistency_valid():
    vr = validate_ohlc_consistency(
        Decimal("100"), Decimal("110"), Decimal("95"), Decimal("105")
    )
    assert vr.is_valid


def test_ohlc_consistency_invalid_high_low():
    vr = validate_ohlc_consistency(
        Decimal("100"), Decimal("90"), Decimal("95"), Decimal("105")
    )
    assert not vr.is_valid
    assert any("high" in e.lower() for e in vr.errors)


def test_null_not_zero(session, tmp_path):
    """Missing volume must stay NULL, never become 0."""
    csv_content = (
        "J-Date,Open,High,Low,Close,Final,Volume,Value,No,Ticker,Name,Market\n"
        "1402-01-08,100,110,95,105,105,,1000000,10,\u0633\u0627\u0645\u0627\u0646,\u0628\u0627\u0646\u06a9 \u0633\u0627\u0645\u0627\u0646,\u0641\u0631\u0627\u0628\u0648\u0631\u0633\n"
    )
    p = tmp_path / "test.csv"
    p.write_text(csv_content, encoding="utf-8")

    result = ingest_ohlc_csv(session, p)
    assert result.status == "COMPLETED"
    md = session.query(MarketDaily).one()
    assert md.volume is None  # critical: NULL != 0
    assert md.close_price == Decimal("105")


def test_ingest_ohlc_idempotent(session, tmp_path):
    csv_content = (
        "J-Date,Open,High,Low,Close,Final,Volume,Value,No,Ticker,Name,Market\n"
        "1402-01-08,3022,3022,3022,3022,3022,14738930,44541046460,263,\u0633\u0627\u0645\u0627\u0646,\u0628\u0627\u0646\u06a9 \u0633\u0627\u0645\u0627\u0646,\u067e\u0627\u06cc\u0647 \u0632\u0631\u062f\n"
        "1402-01-09,3112,3112,3112,3112,3112,10918715,33979041080,208,\u0633\u0627\u0645\u0627\u0646,\u0628\u0627\u0646\u06a9 \u0633\u0627\u0645\u0627\u0646,\u067e\u0627\u06cc\u0647 \u0632\u0631\u062f\n"
    )
    p = tmp_path / "saman.csv"
    p.write_text(csv_content, encoding="utf-8")

    r1 = ingest_ohlc_csv(session, p)
    assert r1.status == "COMPLETED"
    assert r1.records_inserted == 2
    count1 = session.query(MarketDaily).count()
    assert count1 == 2

    r2 = ingest_ohlc_csv(session, p)
    assert r2.status == "COMPLETED"
    count2 = session.query(MarketDaily).count()
    assert count2 == 2  # no uncontrolled duplicates
    assert r2.records_updated == 2

    runs = session.query(IngestionRun).filter_by(source="OHLC").all()
    assert len(runs) >= 2
    assert all(run.status == "COMPLETED" for run in runs)
