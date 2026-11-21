from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.database import Base
from src.ingestion.service import FxRateInput, ingest_fx_rates, ingest_ohlc_csv
from src.models.audit import IngestionRun
from src.models.entity import Company, Industry
from src.models.fx import FXRate
from src.models.market import MarketDaily


@pytest.fixture
def db(tmp_path):
    engine = create_engine(f"sqlite:///{tmp_path / 'atomic-test.db'}")
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    with factory() as session:
        industry = Industry(industry_code="BANK", industry_name="Banking")
        session.add(industry)
        session.flush()
        session.add(Company(ticker="SAMAN", company_name="Saman", industry_id=industry.industry_id,
                            codal_symbol="SAMAN", status="ACTIVE", is_active=True))
        session.commit()
    yield engine, factory
    engine.dispose()


def market_csv(tmp_path, rows):
    path = tmp_path / "market.csv"
    path.write_text("J-Date,Ticker,Close,Volume,No,Value,Open,High,Low,Final\n" +
                    "".join(",".join(map(str, row)) + ",bad,bad,bad,bad\n" for row in rows),
                    encoding="utf-8")
    return path


def market_row(day, close="100", volume="10", count="2", value="1000"):
    return [f"1404-01-{day:02d}", "SAMAN", close, volume, count, value]


def fx(rate, day=1, *, rate_type="FREE_MARKET"):
    return FxRateInput(rate=Decimal(str(rate)), rate_type=rate_type,
                       jalali_year=1404, jalali_month=1, jalali_day=day,
                       source="TEST")


def test_market_valid_multirow_batch_and_independent_value(db, tmp_path):
    _, factory = db
    with factory() as session:
        result = ingest_ohlc_csv(session, market_csv(tmp_path, [market_row(1), market_row(2, value="1234")]))
        assert (result.status, result.records_inserted, result.records_duplicated) == ("COMPLETED", 2, 0)
        rows = session.query(MarketDaily).order_by(MarketDaily.jalali_day).all()
        assert [r.value for r in rows] == [Decimal("1000.00"), Decimal("1234.00")]
        assert all(r.open_price is r.high_price is r.low_price is r.adjusted_close is None for r in rows)


def test_market_invalid_row_rejects_whole_batch(db, tmp_path):
    _, factory = db
    with factory() as session:
        result = ingest_ohlc_csv(session, market_csv(tmp_path, [market_row(1), market_row(2, volume="bad")]))
        assert result.status == "FAILED" and result.records_inserted == 0
        assert result.records_failed == 2 and result.records_invalid == 1
        assert session.query(MarketDaily).count() == 0
        run = session.get(IngestionRun, result.ingestion_id)
        assert run.status == "FAILED" and run.records_inserted == 0 and run.records_failed == 2
        assert "invalid_count=1" in run.error_log


def test_market_ticker_codal_symbol_conflict_rejects_batch(db, tmp_path):
    _, factory = db
    with factory() as session:
        original = session.query(Company).filter_by(ticker="SAMAN").one()
        session.add(Company(ticker="OTHER", company_name="Other", industry_id=original.industry_id,
                            codal_symbol="SAMAN-ALT", status="ACTIVE", is_active=True))
        session.commit()
        result = ingest_ohlc_csv(session, market_csv(tmp_path, [market_row(1)]))
        assert result.status == "FAILED"
        audit = session.get(IngestionRun, result.ingestion_id)
        assert "ROW_1_TICKER_IDENTITY_CONFLICT" in audit.error_log


def test_market_inbatch_identical_duplicate_and_existing_replay_are_unchanged(db, tmp_path):
    _, factory = db
    path = market_csv(tmp_path, [market_row(1), market_row(1)])
    with factory() as session:
        first = ingest_ohlc_csv(session, path)
        assert first.status == "COMPLETED" and first.records_inserted == 1
        assert first.records_duplicated == 1
    with factory() as session:
        replay = ingest_ohlc_csv(session, market_csv(tmp_path, [market_row(1)]))
        assert replay.status == "COMPLETED" and replay.records_inserted == 0
        assert replay.records_duplicated == 1
        assert session.query(MarketDaily).count() == 1


def test_market_inbatch_conflict_rejects_batch(db, tmp_path):
    _, factory = db
    with factory() as session:
        result = ingest_ohlc_csv(session, market_csv(tmp_path, [market_row(1), market_row(1, close="101")]))
        assert result.status == "FAILED" and result.records_inserted == 0
        assert session.query(MarketDaily).count() == 0


def test_market_existing_payload_conflict_rejects_batch(db, tmp_path):
    _, factory = db
    with factory() as session:
        assert ingest_ohlc_csv(session, market_csv(tmp_path, [market_row(1)])).status == "COMPLETED"
    with factory() as session:
        result = ingest_ohlc_csv(session, market_csv(tmp_path, [market_row(1, close="999"), market_row(2)]))
        assert result.status == "FAILED" and result.records_inserted == 0
        assert session.query(MarketDaily).count() == 1
        assert session.query(MarketDaily).filter_by(jalali_day=1).one().close_price == Decimal("100.00")


def test_market_commit_failure_rolls_back_pending_writes_and_audits_failed(db, tmp_path, monkeypatch):
    _, factory = db
    with factory() as session:
        real_commit = session.commit
        calls = 0
        def fail_second_commit():
            nonlocal calls
            calls += 1
            if calls == 2:
                raise RuntimeError("sensitive injected failure payload")
            return real_commit()
        monkeypatch.setattr(session, "commit", fail_second_commit)
        result = ingest_ohlc_csv(session, market_csv(tmp_path, [market_row(1), market_row(2)]))
        monkeypatch.setattr(session, "commit", real_commit)
        assert result.status == "FAILED" and result.records_inserted == 0
        assert session.query(MarketDaily).count() == 0
        run = session.get(IngestionRun, result.ingestion_id)
        assert run.status == "FAILED" and run.records_failed == 2
        assert "sensitive" not in (run.error_log or "")


def test_fx_valid_batch_duplicate_replay_and_no_second_conversion(db):
    _, factory = db
    with factory() as session:
        result = ingest_fx_rates(session, [fx("123456.78"), fx("123456.78")])
        assert result.status == "COMPLETED" and result.records_inserted == 1
        assert result.records_duplicated == 1
        assert session.query(FXRate).one().rate == Decimal("123456.7800")
        run = session.get(IngestionRun, result.ingestion_id)
        assert run.records_found == 2 and run.records_inserted == 1 and run.records_updated == 0
        assert "duplicate_count=1" in run.error_log and "invalid_count=0" in run.error_log
    with factory() as session:
        replay = ingest_fx_rates(session, [fx("123456.78")])
        assert replay.status == "COMPLETED" and replay.records_duplicated == 1
        assert replay.records_inserted == 0


def test_fx_invalid_batch_rejects_all_rows(db):
    _, factory = db
    with factory() as session:
        result = ingest_fx_rates(session, [fx("123"), fx("0", day=2)])
        assert result.status == "FAILED" and result.records_inserted == 0
        assert result.records_failed == 2 and result.records_invalid == 1
        assert session.query(FXRate).count() == 0


def test_fx_inbatch_and_existing_conflicts_fail_without_overwrite(db):
    _, factory = db
    with factory() as session:
        result = ingest_fx_rates(session, [fx("100"), fx("101")])
        assert result.status == "FAILED" and session.query(FXRate).count() == 0
        assert ingest_fx_rates(session, [fx("100")]).records_inserted == 1
    with factory() as session:
        result = ingest_fx_rates(session, [fx("101"), fx("200", day=2)])
        assert result.status == "FAILED" and result.records_inserted == 0
        assert session.query(FXRate).count() == 1
        assert session.query(FXRate).one().rate == Decimal("100.0000")


def test_exchange_center_is_accepted_after_schema_migration(db):
    _, factory = db
    with factory() as session:
        result = ingest_fx_rates(session, [fx("100", rate_type="EXCHANGE_CENTER")])
        assert result.status == "COMPLETED" and result.records_inserted == 1
        assert session.query(FXRate).filter_by(rate_type="EXCHANGE_CENTER").count() == 1
        run = session.get(IngestionRun, result.ingestion_id)
        assert run.status == "COMPLETED"


def test_fx_commit_failure_rolls_back_and_records_failed(db, monkeypatch):
    _, factory = db
    with factory() as session:
        real_commit = session.commit
        calls = 0
        def fail_second_commit():
            nonlocal calls
            calls += 1
            if calls == 2:
                raise RuntimeError("injected")
            return real_commit()
        monkeypatch.setattr(session, "commit", fail_second_commit)
        result = ingest_fx_rates(session, [fx("123"), fx("456", day=2)])
        monkeypatch.setattr(session, "commit", real_commit)
        assert result.status == "FAILED" and session.query(FXRate).count() == 0
        assert session.get(IngestionRun, result.ingestion_id).status == "FAILED"


def test_started_audit_failure_does_not_write_canonical_data(db, monkeypatch):
    _, factory = db
    with factory() as session:
        real_commit = session.commit
        monkeypatch.setattr(session, "commit", lambda: (_ for _ in ()).throw(RuntimeError("audit unavailable")))
        with pytest.raises(RuntimeError, match="unable to persist STARTED or FAILED"):
            ingest_fx_rates(session, [fx("123")])
        monkeypatch.setattr(session, "commit", real_commit)
        assert session.query(FXRate).count() == 0
        assert session.query(IngestionRun).count() == 0


def test_two_independent_sessions_observe_replay_and_conflict(db, tmp_path):
    _, factory = db
    with factory() as first_session:
        first = ingest_fx_rates(first_session, [fx("123")])
        assert first.records_inserted == 1
    with factory() as second_session:
        replay = ingest_fx_rates(second_session, [fx("123")])
        assert replay.records_duplicated == 1 and replay.records_inserted == 0
    with factory() as third_session:
        conflict = ingest_fx_rates(third_session, [fx("124")])
        assert conflict.status == "FAILED" and third_session.query(FXRate).count() == 1
    market_path = market_csv(tmp_path, [market_row(3)])
    with factory() as market_session_one:
        assert ingest_ohlc_csv(market_session_one, market_path).records_inserted == 1
    with factory() as market_session_two:
        replay = ingest_ohlc_csv(market_session_two, market_path)
        assert replay.records_duplicated == 1 and replay.records_inserted == 0

