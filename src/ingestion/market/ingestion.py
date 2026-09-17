"""Market OHLC persistence — adapter DTOs → MarketDaily (CHANGE-007)."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Union

from sqlalchemy.orm import Session

from src.ingestion.common.identity import find_market_daily_existing
from src.ingestion.common.validation import validate_ohlc_consistency
from src.ingestion.market.adapter import load_ohlc_csv_rows
from src.models.audit import IngestionRun
from src.models.entity import Company
from src.models.market import MarketDaily


# Result type kept compatible with service.OhlcIngestionResult fields
class OhlcIngestionResult:
    def __init__(
        self,
        ingestion_id: int,
        records_found: int,
        records_inserted: int,
        records_updated: int,
        records_failed: int,
        status: str,
    ):
        self.ingestion_id = ingestion_id
        self.records_found = records_found
        self.records_inserted = records_inserted
        self.records_updated = records_updated
        self.records_failed = records_failed
        self.status = status


def ingest_ohlc_csv(
    session: Session,
    path: Union[str, Path],
    *,
    source_label: str = "CSV_OHLC",
) -> OhlcIngestionResult:
    """Parse via market.adapter, then persist to MarketDaily."""
    run = IngestionRun(source="OHLC", status="STARTED", records_found=0)
    session.add(run)
    session.flush()

    try:
        parsed = load_ohlc_csv_rows(path)
        run.records_found = parsed.records_found

        if parsed.records_found == 0 and not parsed.rows:
            # Distinguish empty/invalid file (no fieldnames) from empty data rows
            run.status = "FAILED"
            run.error_log = "empty or invalid CSV"
            run.finished_at = datetime.utcnow()
            session.commit()
            return OhlcIngestionResult(
                ingestion_id=run.ingestion_id,
                records_found=0,
                records_inserted=0,
                records_updated=0,
                records_failed=0,
                status="FAILED",
            )

        inserted = 0
        updated = 0
        failed = len(parsed.errors)
        errors = list(parsed.errors)

        for row in parsed.rows:
            if not validate_ohlc_consistency(
                row.open_price, row.high_price, row.low_price, row.close_price
            ):
                failed += 1
                errors.append(f"line {row.line_no}: OHLC consistency failed")
                continue

            company = session.query(Company).filter_by(ticker=row.ticker).one_or_none()
            if company is None:
                failed += 1
                errors.append(f"line {row.line_no}: company ticker={row.ticker!r} not found")
                continue

            existing = find_market_daily_existing(
                session,
                company_id=company.company_id,
                jy=row.jalali_year,
                jm=row.jalali_month,
                jd=row.jalali_day,
            )

            if existing is None:
                session.add(
                    MarketDaily(
                        company_id=company.company_id,
                        trade_date=None,
                        jalali_year=row.jalali_year,
                        jalali_month=row.jalali_month,
                        jalali_day=row.jalali_day,
                        open_price=row.open_price,
                        high_price=row.high_price,
                        low_price=row.low_price,
                        close_price=row.close_price,
                        adjusted_close=row.adjusted_close,
                        volume=row.volume,
                        value=row.value,
                        trade_count=row.trade_count,
                        source=source_label,
                    )
                )
                inserted += 1
            else:
                existing.open_price = row.open_price
                existing.high_price = row.high_price
                existing.low_price = row.low_price
                existing.close_price = row.close_price
                existing.adjusted_close = row.adjusted_close
                existing.volume = row.volume
                existing.value = row.value
                existing.trade_count = row.trade_count
                existing.source = source_label
                updated += 1

        run.records_inserted = inserted
        run.records_updated = updated
        run.records_failed = failed
        run.error_log = "\n".join(errors[:50]) if errors else None
        run.status = "COMPLETED"
        run.finished_at = datetime.utcnow()
        session.commit()

        return OhlcIngestionResult(
            ingestion_id=run.ingestion_id,
            records_found=run.records_found or 0,
            records_inserted=inserted,
            records_updated=updated,
            records_failed=failed,
            status=run.status,
        )

    except Exception as exc:
        session.rollback()
        failed_run = IngestionRun(
            source="OHLC",
            status="FAILED",
            records_found=0,
            records_failed=0,
            error_log=str(exc),
            finished_at=datetime.utcnow(),
        )
        session.add(failed_run)
        session.commit()
        return OhlcIngestionResult(
            ingestion_id=failed_run.ingestion_id,
            records_found=0,
            records_inserted=0,
            records_updated=0,
            records_failed=0,
            status="FAILED",
        )
