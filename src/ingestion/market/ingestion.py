"""Atomic MarketDaily persistence for the approved Jalali CSV contract."""
from __future__ import annotations

from decimal import Decimal
from pathlib import Path
from typing import Union

from sqlalchemy.orm import Session

from src.core.jalali import is_valid_jalali_components
from src.ingestion.common.atomic import (
    IngestionAuditError, create_started_run, finish_completed_run,
    finish_failed_run,
)
from src.ingestion.common.identity import find_market_daily_existing
from src.ingestion.market.adapter import load_ohlc_csv_rows
from src.models.audit import IngestionRun
from src.models.entity import Company
from src.models.market import MarketDaily


class OhlcIngestionResult:
    def __init__(self, ingestion_id: int, records_found: int, records_inserted: int,
                 records_updated: int, records_failed: int, status: str,
                 records_duplicated: int = 0, records_invalid: int = 0):
        self.ingestion_id = ingestion_id
        self.records_found = records_found
        self.records_inserted = records_inserted
        self.records_updated = records_updated
        self.records_failed = records_failed
        self.status = status
        self.records_duplicated = records_duplicated
        self.records_invalid = records_invalid


def _payload(row) -> tuple:
    return (row.close_price, row.volume, row.trade_count, row.value)


def _existing_payload(row) -> tuple:
    return (row.close_price, row.volume, row.trade_count, row.value)


def _resolve_company(session: Session, ticker: str) -> tuple[Company | None, str | None]:
    """Resolve the CSV ticker against the approved unique CODAL identity."""
    by_codal = session.query(Company).filter_by(codal_symbol=ticker).one_or_none()
    by_ticker = session.query(Company).filter_by(ticker=ticker).one_or_none()
    if by_codal is not None and by_ticker is not None and by_codal.company_id != by_ticker.company_id:
        return None, "TICKER_IDENTITY_CONFLICT"
    company = by_codal or by_ticker
    if company is not None and company.codal_symbol not in (None, ticker):
        return None, "TICKER_IDENTITY_CONFLICT"
    return company, None


def _fits_numeric(value: Decimal, *, max_integer_digits: int, scale: int) -> bool:
    if not value.is_finite():
        return False
    normalized = value.normalize()
    exponent = normalized.as_tuple().exponent
    fractional_digits = max(0, -exponent)
    integer_digits = max(0, len(normalized.as_tuple().digits) + exponent)
    return fractional_digits <= scale and integer_digits <= max_integer_digits


def _safe_parse_codes(errors: list[str]) -> tuple[int, list[str], int]:
    invalid = 0
    codes = []
    duplicates = 0
    for idx, message in enumerate(errors, 1):
        if "identical duplicate" in message:
            duplicates += 1
            continue
        invalid += 1
        if "conflicting duplicate" in message:
            code = "IN_BATCH_CONFLICT"
        elif "invalid Jalali date" in message:
            code = "INVALID_JALALI_DATE"
        elif "invalid Close" in message:
            code = "INVALID_MARKET_VALUE"
        elif "missing date or ticker" in message:
            code = "MISSING_REQUIRED_VALUE"
        elif "fewer fields" in message or "more fields" in message:
            code = "CSV_ROW_WIDTH"
        else:
            code = "PARSER_ROW_INVALID"
        codes.append(f"ROW_{idx}_{code}")
    return invalid, codes, duplicates


def ingest_ohlc_csv(session: Session, path: Union[str, Path], *,
                    source_label: str = "CSV_OHLC") -> OhlcIngestionResult:
    """Validate the complete CSV and persist all new observations in one transaction."""
    parsed = None
    parse_failed = False
    try:
        parsed = load_ohlc_csv_rows(path)
        records_found = parsed.records_found
    except Exception:
        records_found = 0
        parse_failed = True

    run_id, can_continue = create_started_run(session, "OHLC", records_found)
    if not can_continue:
        return OhlcIngestionResult(run_id, records_found, 0, 0, records_found, "FAILED", 0, 0)

    invalid_count, issue_codes, duplicate_count = _safe_parse_codes(parsed.errors if parsed else [])
    if parse_failed:
        invalid_count = 1
        issue_codes.append("CSV_PARSE_FAILED")
    if parsed is None or records_found == 0:
        invalid_count = max(1, invalid_count)
        issue_codes.append("EMPTY_OR_INVALID_BATCH")

    prepared: list[MarketDaily] = []
    seen: dict[tuple, tuple] = {}
    try:
        run = session.get(IngestionRun, run_id)
        if run is None:
            raise IngestionAuditError("started Market audit row is missing")

        # Structural and parser errors fail the complete input before any entity lookup or staging.
        if invalid_count == 0 and parsed is not None:
            for index, row in enumerate(parsed.rows, 1):
                key = (row.ticker, row.jalali_year, row.jalali_month, row.jalali_day)
                payload = _payload(row)
                if (not row.ticker or len(row.ticker) > 100
                        or not is_valid_jalali_components(row.jalali_year, row.jalali_month, row.jalali_day)
                        or row.close_price is None or not _fits_numeric(row.close_price, max_integer_digits=16, scale=2)
                        or row.value is None or not _fits_numeric(row.value, max_integer_digits=22, scale=2)
                        or type(row.volume) is not int or not 0 <= row.volume <= 2_147_483_647
                        or type(row.trade_count) is not int or not 0 <= row.trade_count <= 2_147_483_647):
                    invalid_count += 1
                    issue_codes.append(f"ROW_{index}_INVALID_MARKET_VALUE")
                    continue
                if source_label is not None and (not isinstance(source_label, str) or len(source_label) > 100):
                    invalid_count += 1
                    issue_codes.append(f"ROW_{index}_INVALID_SOURCE_LABEL")
                    continue
                if key in seen:
                    if seen[key] == payload:
                        duplicate_count += 1
                    else:
                        invalid_count += 1
                        issue_codes.append(f"ROW_{index}_IN_BATCH_CONFLICT")
                    continue
                seen[key] = payload
                company, identity_error = _resolve_company(session, row.ticker)
                if identity_error:
                    invalid_count += 1
                    issue_codes.append(f"ROW_{index}_{identity_error}")
                    continue
                if company is None:
                    invalid_count += 1
                    issue_codes.append(f"ROW_{index}_COMPANY_NOT_FOUND")
                    continue
                existing = find_market_daily_existing(session, company_id=company.company_id,
                    jy=row.jalali_year, jm=row.jalali_month, jd=row.jalali_day)
                if existing is not None:
                    if _existing_payload(existing) == payload:
                        duplicate_count += 1
                    else:
                        invalid_count += 1
                        issue_codes.append(f"ROW_{index}_EXISTING_KEY_CONFLICT")
                    continue
                prepared.append(MarketDaily(company_id=company.company_id, trade_date=None,
                    jalali_year=row.jalali_year, jalali_month=row.jalali_month,
                    jalali_day=row.jalali_day, close_price=row.close_price,
                    volume=row.volume, value=row.value, trade_count=row.trade_count,
                    source=source_label))

        if invalid_count:
            session.rollback()
            finish_failed_run(session, run_id, records_found=records_found,
                duplicate_count=duplicate_count, invalid_count=invalid_count, codes=issue_codes)
            return OhlcIngestionResult(run_id, records_found, 0, 0, records_found,
                                       "FAILED", duplicate_count, invalid_count)

        session.add_all(prepared)
        finish_completed_run(run, records_found=records_found,
            records_inserted=len(prepared), duplicate_count=duplicate_count)
        session.flush()
        session.commit()
        return OhlcIngestionResult(run_id, records_found, len(prepared), 0, 0,
                                   "COMPLETED", duplicate_count, 0)
    except IngestionAuditError:
        session.rollback()
        raise
    except Exception:
        session.rollback()
        finish_failed_run(session, run_id, records_found=records_found,
            duplicate_count=0, invalid_count=invalid_count,
            codes=issue_codes + ["CANONICAL_TRANSACTION_FAILED"])
        return OhlcIngestionResult(run_id, records_found, 0, 0, records_found,
                                   "FAILED", 0, invalid_count)
