"""OHLC ingestion into MarketDaily with idempotency and audit."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

from sqlalchemy.orm import Session

from src.ingestion.common.run_tracker import IngestionRunTracker
from src.ingestion.common.validation import validate_ohlc_consistency
from src.ingestion.market.parser import OhlcRow, parse_ohlc_csv
from src.models.entity import Company
from src.models.market import MarketDaily


@dataclass(frozen=True)
class OhlcIngestionResult:
    ingestion_id: int
    records_found: int
    records_inserted: int
    records_updated: int
    records_failed: int
    status: str


def _resolve_company(session: Session, ticker: str) -> Optional[Company]:
    """Resolve company by ticker (exact match). Returns None if not found."""
    return session.query(Company).filter_by(ticker=ticker).one_or_none()


def _upsert_market_daily(
    session: Session,
    company_id: int,
    row: OhlcRow,
    source: str = "CSV_OHLC",
) -> str:
    """Insert or update a MarketDaily row.

    Returns 'inserted' or 'updated'.
    Deterministic identity: (company_id, trade_date).
    """
    existing = (
        session.query(MarketDaily)
        .filter_by(company_id=company_id, trade_date=row.trade_date)
        .one_or_none()
    )

    if existing is None:
        md = MarketDaily(
            company_id=company_id,
            trade_date=row.trade_date,
            open_price=row.open_price,
            high_price=row.high_price,
            low_price=row.low_price,
            close_price=row.close_price,
            adjusted_close=row.adjusted_close,
            volume=row.volume,
            value=row.value,
            trade_count=row.trade_count,
            source=source,
        )
        session.add(md)
        return "inserted"

    existing.open_price = row.open_price
    existing.high_price = row.high_price
    existing.low_price = row.low_price
    existing.close_price = row.close_price
    existing.adjusted_close = row.adjusted_close
    existing.volume = row.volume
    existing.value = row.value
    existing.trade_count = row.trade_count
    existing.source = source
    return "updated"


def ingest_ohlc_csv(
    session: Session,
    path: Union[str, Path],
    *,
    source_label: str = "CSV_OHLC",
    require_company: bool = True,
) -> OhlcIngestionResult:
    """Ingest an OHLC CSV file into MarketDaily.

    Behaviour:
    - Creates an IngestionRun (source=OHLC).
    - Parses rows; validates OHLC consistency.
    - Resolves company by ticker.
    - Upserts by (company_id, trade_date) — idempotent.
    - Never converts missing values to zero.
    - Records failures explicitly.
    - Does not invent missing trading days.
    """
    tracker = IngestionRunTracker(session, source="OHLC")
    path = Path(path)

    try:
        rows = list(parse_ohlc_csv(path))
        tracker.start(records_found=len(rows))

        inserted = 0
        updated = 0
        failed = 0

        for row in rows:
            vr = validate_ohlc_consistency(
                row.open_price, row.high_price, row.low_price, row.close_price
            )
            if not vr.is_valid:
                failed += 1
                tracker.record_failure(
                    failed=1,
                    error=f"line {row.source_line}: {'; '.join(vr.errors)}",
                )
                continue

            company = _resolve_company(session, row.ticker)
            if company is None:
                failed += 1
                tracker.record_failure(
                    failed=1,
                    error=f"line {row.source_line}: company ticker={row.ticker!r} not found",
                )
                continue

            try:
                action = _upsert_market_daily(
                    session, company.company_id, row, source=source_label
                )
                if action == "inserted":
                    inserted += 1
                    tracker.record_success(inserted=1)
                else:
                    updated += 1
                    tracker.record_success(updated=1)
            except Exception as exc:
                failed += 1
                tracker.record_failure(failed=1, error=f"line {row.source_line}: {exc}")

        run = tracker.complete()
        session.commit()

        return OhlcIngestionResult(
            ingestion_id=run.ingestion_id,
            records_found=run.records_found or 0,
            records_inserted=run.records_inserted or 0,
            records_updated=run.records_updated or 0,
            records_failed=run.records_failed or 0,
            status=run.status,
        )

    except Exception as exc:
        session.rollback()
        run = tracker.fail(str(exc))
        session.commit()
        return OhlcIngestionResult(
            ingestion_id=run.ingestion_id,
            records_found=run.records_found or 0,
            records_inserted=0,
            records_updated=0,
            records_failed=run.records_failed or 0,
            status="FAILED",
        )
