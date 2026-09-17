"""Tests for FX ingestion (CHANGE-001: FREE_MARKET vs OPERATIONAL distinct)."""

from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.database import Base
from src.ingestion.service import FxRateInput, ingest_fx_rates
from src.models.audit import IngestionRun
from src.models.fx import FXRate


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    s = Session()
    yield s
    s.close()


def test_free_market_and_operational_are_stored_separately(session):
    """CHANGE-001: same date/pair with different rate_type must both persist."""
    d = date(2024, 4, 1)
    result = ingest_fx_rates(
        session,
        [
            FxRateInput(rate_date=d, rate=Decimal("600000"), rate_type="FREE_MARKET", source="TGJU"),
            FxRateInput(rate_date=d, rate=Decimal("420000"), rate_type="OPERATIONAL", source="CBI"),
        ],
    )
    assert result.status == "COMPLETED"
    assert result.records_inserted == 2
    assert result.records_failed == 0

    rows = session.query(FXRate).order_by(FXRate.rate_type).all()
    assert len(rows) == 2
    by_type = {r.rate_type: r.rate for r in rows}
    assert by_type["FREE_MARKET"] == Decimal("600000")
    assert by_type["OPERATIONAL"] == Decimal("420000")


def test_fx_idempotent_upsert(session):
    d = date(2024, 5, 10)
    r1 = ingest_fx_rates(
        session,
        [FxRateInput(rate_date=d, rate=Decimal("610000"), rate_type="FREE_MARKET", source="A")],
    )
    assert r1.records_inserted == 1
    assert session.query(FXRate).count() == 1

    r2 = ingest_fx_rates(
        session,
        [FxRateInput(rate_date=d, rate=Decimal("615000"), rate_type="FREE_MARKET", source="B")],
    )
    assert r2.status == "COMPLETED"
    assert r2.records_updated == 1
    assert r2.records_inserted == 0
    assert session.query(FXRate).count() == 1

    saved = session.query(FXRate).one()
    assert saved.rate == Decimal("615000")
    assert saved.source == "B"


def test_invalid_rate_type_and_non_positive_rate_fail_explicitly(session):
    d = date(2024, 6, 1)
    result = ingest_fx_rates(
        session,
        [
            FxRateInput(rate_date=d, rate=Decimal("100"), rate_type="BLACK_MARKET"),
            FxRateInput(rate_date=d, rate=Decimal("0"), rate_type="FREE_MARKET"),
            FxRateInput(rate_date=d, rate=Decimal("-1"), rate_type="OPERATIONAL"),
            FxRateInput(rate_date=d, rate=Decimal("500000"), rate_type="FREE_MARKET", source="OK"),
        ],
    )
    assert result.status == "COMPLETED"
    assert result.records_failed == 3
    assert result.records_inserted == 1
    assert session.query(FXRate).count() == 1
    assert session.query(FXRate).one().rate_type == "FREE_MARKET"


def test_operational_never_defaults_to_free_market(session):
    """Operational row must not appear under FREE_MARKET key."""
    d = date(2024, 7, 15)
    ingest_fx_rates(
        session,
        [FxRateInput(rate_date=d, rate=Decimal("430000"), rate_type="OPERATIONAL", source="OPS")],
    )
    free = (
        session.query(FXRate)
        .filter_by(rate_date=d, rate_type="FREE_MARKET")
        .one_or_none()
    )
    ops = (
        session.query(FXRate)
        .filter_by(rate_date=d, rate_type="OPERATIONAL")
        .one_or_none()
    )
    assert free is None
    assert ops is not None
    assert ops.rate == Decimal("430000")


def test_fx_ingestion_run_audit(session):
    d = date(2024, 8, 1)
    result = ingest_fx_rates(
        session,
        [
            FxRateInput(rate_date=d, rate=Decimal("620000"), rate_type="FREE_MARKET"),
            FxRateInput(rate_date=d, rate=Decimal("440000"), rate_type="OPERATIONAL"),
        ],
    )
    run = session.get(IngestionRun, result.ingestion_id)
    assert run is not None
    assert run.source == "FX"
    assert run.status == "COMPLETED"
    assert run.records_found == 2
    assert run.records_inserted == 2
    assert run.finished_at is not None
