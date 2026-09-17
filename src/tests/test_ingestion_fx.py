"""Tests for FX ingestion (CHANGE-001 + CHANGE-006 Jalali date policy)."""

from __future__ import annotations

from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker

from src.core.database import Base
from src.ingestion.service import FxRateInput, ingest_fx_rates, ingest_fx_xlsx
from src.migrations.runner import MigrationRunner
from src.models.audit import IngestionRun
from src.models.fx import FXRate


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    runner = MigrationRunner(engine)
    runner.upgrade()
    Session = sessionmaker(bind=engine)
    s = Session()
    yield s
    s.close()


def test_free_market_and_operational_are_stored_separately(session):
    """CHANGE-001: same date/pair with different rate_type must both persist."""
    result = ingest_fx_rates(
        session,
        [
            FxRateInput(
                rate=Decimal("600000"),
                rate_type="FREE_MARKET",
                jalali_year=1403,
                jalali_month=1,
                jalali_day=15,
                source="TGJU",
            ),
            FxRateInput(
                rate=Decimal("420000"),
                rate_type="OPERATIONAL",
                jalali_year=1403,
                jalali_month=1,
                jalali_day=15,
                source="CBI",
            ),
        ],
    )
    assert result.status == "COMPLETED"
    assert result.records_inserted == 2
    assert result.records_failed == 0

    rows = session.query(FXRate).order_by(FXRate.rate_type).all()
    assert len(rows) == 2
    by_type = {r.rate_type: r for r in rows}
    assert by_type["FREE_MARKET"].rate == Decimal("600000")
    assert by_type["OPERATIONAL"].rate == Decimal("420000")
    for r in rows:
        assert r.jalali_year == 1403
        assert r.jalali_month == 1
        assert r.jalali_day == 15
        assert r.rate_date is None


def test_fx_idempotent_upsert_jalali(session):
    r1 = ingest_fx_rates(
        session,
        [
            FxRateInput(
                rate=Decimal("610000"),
                rate_type="FREE_MARKET",
                jalali_year=1404,
                jalali_month=2,
                jalali_day=10,
                source="A",
            )
        ],
    )
    assert r1.records_inserted == 1
    assert session.query(FXRate).count() == 1

    r2 = ingest_fx_rates(
        session,
        [
            FxRateInput(
                rate=Decimal("615000"),
                rate_type="FREE_MARKET",
                jalali_year=1404,
                jalali_month=2,
                jalali_day=10,
                source="B",
            )
        ],
    )
    assert r2.status == "COMPLETED"
    assert r2.records_updated == 1
    assert r2.records_inserted == 0
    assert session.query(FXRate).count() == 1
    saved = session.query(FXRate).one()
    assert saved.rate == Decimal("615000")
    assert saved.source == "B"


def test_invalid_rate_type_and_non_positive_rate_fail_explicitly(session):
    result = ingest_fx_rates(
        session,
        [
            FxRateInput(rate=Decimal("100"), rate_type="BLACK_MARKET", rate_date=date(2024, 6, 1)),
            FxRateInput(rate=Decimal("0"), rate_type="FREE_MARKET", rate_date=date(2024, 6, 1)),
            FxRateInput(rate=Decimal("-1"), rate_type="OPERATIONAL", rate_date=date(2024, 6, 1)),
            FxRateInput(rate=Decimal("500000"), rate_type="FREE_MARKET", rate_date=date(2024, 6, 1), source="OK"),
        ],
    )
    assert result.status == "COMPLETED"
    assert result.records_failed == 3
    assert result.records_inserted == 1
    assert session.query(FXRate).count() == 1


def test_operational_never_defaults_to_free_market(session):
    ingest_fx_rates(
        session,
        [
            FxRateInput(
                rate=Decimal("430000"),
                rate_type="OPERATIONAL",
                jalali_year=1404,
                jalali_month=7,
                jalali_day=15,
                source="OPS",
            )
        ],
    )
    free = (
        session.query(FXRate)
        .filter_by(jalali_year=1404, jalali_month=7, jalali_day=15, rate_type="FREE_MARKET")
        .one_or_none()
    )
    ops = (
        session.query(FXRate)
        .filter_by(jalali_year=1404, jalali_month=7, jalali_day=15, rate_type="OPERATIONAL")
        .one_or_none()
    )
    assert free is None
    assert ops is not None
    assert ops.rate == Decimal("430000")


def test_fx_ingestion_run_audit(session):
    result = ingest_fx_rates(
        session,
        [
            FxRateInput(rate=Decimal("620000"), rate_type="FREE_MARKET", jalali_year=1404, jalali_month=8, jalali_day=1),
            FxRateInput(rate=Decimal("440000"), rate_type="OPERATIONAL", jalali_year=1404, jalali_month=8, jalali_day=1),
        ],
    )
    run = session.get(IngestionRun, result.ingestion_id)
    assert run is not None
    assert run.source == "FX"
    assert run.status == "COMPLETED"
    assert run.records_found == 2
    assert run.records_inserted == 2
    assert run.finished_at is not None


def test_same_month_across_years_fx(session):
    """jalali_month independent of year — same policy as market_daily."""
    ingest_fx_rates(
        session,
        [
            FxRateInput(rate=Decimal("100"), rate_type="FREE_MARKET", jalali_year=1402, jalali_month=2, jalali_day=1),
            FxRateInput(rate=Decimal("200"), rate_type="FREE_MARKET", jalali_year=1403, jalali_month=2, jalali_day=5),
            FxRateInput(rate=Decimal("300"), rate_type="FREE_MARKET", jalali_year=1404, jalali_month=2, jalali_day=10),
            FxRateInput(rate=Decimal("400"), rate_type="FREE_MARKET", jalali_year=1404, jalali_month=12, jalali_day=1),
        ],
    )
    month2 = (
        session.query(FXRate)
        .filter_by(jalali_month=2, rate_type="FREE_MARKET")
        .order_by(FXRate.jalali_year)
        .all()
    )
    assert len(month2) == 3
    assert [r.jalali_year for r in month2] == [1402, 1403, 1404]


def test_ingest_fx_xlsx_toman_and_rial(session, tmp_path):
    openpyxl = pytest.importorskip("openpyxl")

    free_path = tmp_path / "free.xlsx"
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.append(["1404-01-05", 101785])
    ws.append(["1404-01-06", 102000])
    wb.save(free_path)

    ops_path = tmp_path / "ops.xlsx"
    wb2 = openpyxl.Workbook()
    ws2 = wb2.active
    ws2.append(["تاریخ", "دلار مبادله ای (ریال)"])
    ws2.append(["1404-01-05", 687390])
    wb2.save(ops_path)

    r_free = ingest_fx_xlsx(session, free_path, rate_type="FREE_MARKET", rates_in_toman=True, source_label="FREE_XLSX")
    assert r_free.status == "COMPLETED"
    assert r_free.records_inserted == 2
    free_row = session.query(FXRate).filter_by(rate_type="FREE_MARKET", jalali_day=5).one()
    assert free_row.rate == Decimal("1017850")
    assert free_row.rate_date is None
    assert free_row.jalali_year == 1404

    r_ops = ingest_fx_xlsx(session, ops_path, rate_type="OPERATIONAL", rates_in_toman=False, source_label="OPS_XLSX")
    assert r_ops.records_inserted == 1
    ops_row = session.query(FXRate).filter_by(rate_type="OPERATIONAL").one()
    assert ops_row.rate == Decimal("687390")
    assert ops_row.jalali_month == 1


def test_migration_6_adds_fx_jalali_columns():
    engine = create_engine("sqlite:///:memory:")
    runner = MigrationRunner(engine)
    version = runner.upgrade()
    assert version >= 6
    cols = {c["name"] for c in inspect(engine).get_columns("fx_rates")}
    assert {"jalali_year", "jalali_month", "jalali_day"}.issubset(cols)
    assert runner.upgrade() == version
