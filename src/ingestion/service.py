"""Stage 1 core persistence functions (CHANGE-007).

Format-specific adapters live under:
  src/ingestion/codal/
  src/ingestion/market/
  src/ingestion/fx/
Shared helpers live under:
  src/ingestion/common/

This module keeps the public core API stable for existing tests and callers.
Core responsibilities here:
  - DTOs (RawLineInput, FxRateInput, result types)
  - CODAL raw persistence (ingest_codal_report)
  - FX rate persistence from DTOs (ingest_fx_rates)
  - Thin facades that delegate format parsing to domain adapters
"""

from dataclasses import dataclass
from datetime import date, datetime, timezone
from decimal import Decimal
from pathlib import Path
from typing import Optional, Sequence, Tuple, Union

from sqlalchemy.orm import Session

from src.ingestion.codal.numbers import normalize_digits
from src.ingestion.common.atomic import (
    IngestionAuditError,
    create_started_run,
    finish_completed_run,
    finish_failed_run,
)
from src.ingestion.common.identity import find_fx_existing
from src.ingestion.common.parsing import parse_jalali_components as _parse_jalali_components
from src.ingestion.common.validation import VALID_FX_RATE_TYPES
from src.core.jalali import is_valid_jalali_components
from src.models.audit import IngestionRun
from src.models.fx import FXRate
from src.models.normalized import RawFinancialFact
from src.models.period import FinancialPeriod
from src.models.report import Report, ReportVersion

# Backward-compatible alias used by older tests/imports
_VALID_FX_RATE_TYPES = VALID_FX_RATE_TYPES


@dataclass(frozen=True)
class RawLineInput:
    """One extracted source line; numeric text is ASCII-normalized at CODAL persistence."""

    item_name: str
    value: Optional[Decimal] = None
    item_code: Optional[str] = None
    unit: Optional[str] = None
    currency: Optional[str] = None
    source_section: Optional[str] = None
    source_row: Optional[int] = None
    source_column: Optional[str] = None


def _ascii_text(value: Optional[str]) -> Optional[str]:
    """Normalize numeric characters in CODAL text fields before DB persistence."""
    if value is None:
        return None
    return normalize_digits(value)


@dataclass(frozen=True)
class ReportIngestionResult:
    ingestion_id: int
    report_id: int
    report_version_id: int
    raw_fact_count: int


@dataclass(frozen=True)
class OhlcIngestionResult:
    ingestion_id: int
    records_found: int
    records_inserted: int
    records_updated: int
    records_failed: int
    status: str
    records_duplicated: int = 0
    records_invalid: int = 0


@dataclass(frozen=True)
class FxRateInput:
    """One FX observation. rate_type must distinguish FREE_MARKET vs OPERATIONAL.

    CHANGE-001: free-market and operational FX are never silently substituted.
    Date policy (same as market_daily / CHANGE-005 / CHANGE-006):
    - Prefer jalali_year/month/day from source Jalali string (no calendar conversion).
    - rate_date (Gregorian) is optional and left NULL for Jalali-sourced rows.
    - Identity for Jalali rows: (jalali_year, jalali_month, jalali_day, currency_from, currency_to, rate_type).
    - Identity for Gregorian-only rows: (rate_date, currency_from, currency_to, rate_type).
    """

    rate: Decimal
    rate_type: str
    rate_date: Optional[date] = None
    jalali_year: Optional[int] = None
    jalali_month: Optional[int] = None
    jalali_day: Optional[int] = None
    currency_from: str = "USD"
    currency_to: str = "IRR"
    source: Optional[str] = None


@dataclass(frozen=True)
class FxIngestionResult:
    ingestion_id: int
    records_found: int
    records_inserted: int
    records_updated: int
    records_failed: int
    status: str
    records_duplicated: int = 0
    records_invalid: int = 0


def ingest_codal_report(
    session: Session,
    *,
    company_id: int,
    period_id: int,
    report_type: str,
    title: str,
    publication_datetime: datetime,
    raw_lines: Sequence[RawLineInput],
    codal_tracking_id: Optional[str] = None,
    source_url: Optional[str] = None,
    is_restated: bool = False,
) -> ReportIngestionResult:
    """Persist one CODAL report and extracted raw lines atomically.

    All textual CODAL fields persisted here are normalized so Persian/Arabic
    digits cannot enter the database. Numeric values remain Decimal. The
    Original source-file parsing is outside this persistence function.
    """
    run = IngestionRun(source="CODAL", status="STARTED", records_found=len(raw_lines))
    session.add(run)
    session.flush()

    try:
        normalized_report_type = _ascii_text(report_type) or ""
        normalized_title = _ascii_text(title) or ""
        normalized_tracking_id = _ascii_text(codal_tracking_id)
        normalized_source_url = _ascii_text(source_url)

        period = session.get(FinancialPeriod, period_id)
        if period is None:
            raise ValueError(f"financial period not found: period_id={period_id}")
        if period.company_id != company_id:
            raise ValueError(
                "financial period company_id does not match CODAL company_id"
            )

        report = None
        if normalized_tracking_id is not None:
            report = session.query(Report).filter_by(codal_tracking_id=normalized_tracking_id).one_or_none()

        if report is not None and (
            report.company_id != company_id
            or report.financial_period_id != period_id
        ):
            raise ValueError(
                "CODAL tracking ID is already assigned to a different company "
                "or financial period"
            )

        if report is None:
            report = Report(
                company_id=company_id,
                report_type=normalized_report_type,
                codal_tracking_id=normalized_tracking_id,
                title=normalized_title,
                financial_period_id=period_id,
                source_url=normalized_source_url,
            )
            session.add(report)
            session.flush()

        if normalized_tracking_id is not None:
            existing_version = (
                session.query(ReportVersion)
                .filter_by(
                    report_id=report.report_id,
                    publication_datetime=publication_datetime,
                )
                .order_by(ReportVersion.version_number.desc())
                .first()
            )
            if existing_version is not None:
                existing_count = session.query(RawFinancialFact).filter_by(
                    report_version_id=existing_version.report_version_id,
                ).count()
                run.status = "COMPLETED"
                run.records_inserted = 0
                run.records_updated = existing_count
                run.finished_at = datetime.now(timezone.utc).replace(tzinfo=None)
                session.commit()
                return ReportIngestionResult(
                    ingestion_id=run.ingestion_id,
                    report_id=report.report_id,
                    report_version_id=existing_version.report_version_id,
                    raw_fact_count=existing_count,
                )

        current_version = (
            session.query(ReportVersion)
            .filter_by(report_id=report.report_id, is_current_version=True)
            .one_or_none()
        )
        if current_version is not None:
            current_version.is_current_version = False

        last_version = (
            session.query(ReportVersion)
            .filter_by(report_id=report.report_id)
            .order_by(ReportVersion.version_number.desc())
            .first()
        )
        version_number = 1 if last_version is None else last_version.version_number + 1
        version = ReportVersion(
            report_id=report.report_id,
            version_number=version_number,
            publication_datetime=publication_datetime,
            is_current_version=True,
            is_restated=is_restated,
            supersedes_version_id=None if last_version is None else last_version.report_version_id,
        )
        session.add(version)
        session.flush()

        facts = [
            RawFinancialFact(
                company_id=company_id,
                report_version_id=version.report_version_id,
                period_id=period_id,
                raw_item_name=_ascii_text(line.item_name) or "",
                raw_item_code=_ascii_text(line.item_code),
                value=line.value,
                unit=_ascii_text(line.unit),
                currency=_ascii_text(line.currency),
                source_section=_ascii_text(line.source_section),
                source_row=line.source_row,
                source_column=_ascii_text(line.source_column),
            )
            for line in raw_lines
        ]
        session.add_all(facts)
        run.status = "COMPLETED"
        run.records_inserted = len(facts)
        run.finished_at = datetime.now(timezone.utc).replace(tzinfo=None)
        session.commit()

        return ReportIngestionResult(
            ingestion_id=run.ingestion_id,
            report_id=report.report_id,
            report_version_id=version.report_version_id,
            raw_fact_count=len(facts),
        )
    except Exception as exc:
        session.rollback()
        failed_run = IngestionRun(
            source="CODAL",
            status="FAILED",
            records_found=len(raw_lines),
            records_failed=len(raw_lines),
            error_log=str(exc),
            finished_at=datetime.now(timezone.utc).replace(tzinfo=None),
        )
        session.add(failed_run)
        session.commit()
        raise


def ingest_ohlc_csv(
    session: Session,
    path: Union[str, Path],
    *,
    source_label: str = "CSV_OHLC",
) -> OhlcIngestionResult:
    """Facade: CSV parsing in market.adapter; persistence in market.ingestion."""
    from src.ingestion.market.ingestion import ingest_ohlc_csv as _market_ingest

    result = _market_ingest(session, path, source_label=source_label)
    return OhlcIngestionResult(
        ingestion_id=result.ingestion_id,
        records_found=result.records_found,
        records_inserted=result.records_inserted,
        records_updated=result.records_updated,
        records_failed=result.records_failed,
        status=result.status,
        records_duplicated=result.records_duplicated,
        records_invalid=result.records_invalid,
    )


def ingest_fx_rates(
    session: Session,
    rates: Sequence[FxRateInput],
    *,
    source_label: str = "FX",
    _prevalidation_errors: Sequence[str] = (),
    _records_found: Optional[int] = None,
    _parser_duplicate_count: int = 0,
) -> FxIngestionResult:
    """Validate and persist a whole FX batch atomically; never overwrite."""
    items = list(rates)
    found = len(items) if _records_found is None else _records_found
    run_id, can_continue = create_started_run(session, "FX", found)
    if not can_continue:
        return FxIngestionResult(run_id, found, 0, 0, found, "FAILED", 0, 0)

    invalid: list[str] = []
    duplicate_count = _parser_duplicate_count
    prepared: list[FXRate] = []
    seen: dict[tuple, Decimal] = {}
    try:
        run = session.get(IngestionRun, run_id)
        if run is None:
            raise IngestionAuditError("started FX audit row is missing")
        if _prevalidation_errors or not items:
            if not items and not _prevalidation_errors:
                invalid.append("EMPTY_BATCH")
            for idx, message in enumerate(_prevalidation_errors, 1):
                if "conflicting duplicate" in message:
                    code = "IN_BATCH_CONFLICT"
                elif "invalid Jalali date" in message:
                    code = "INVALID_JALALI_DATE"
                elif "invalid sell rate" in message:
                    code = "INVALID_RATE"
                elif "no row containing" in message:
                    code = "FX_HEADER_NOT_FOUND"
                else:
                    code = "FX_SOURCE_ROW_INVALID"
                invalid.append(f"ROW_{idx}_{code}")
            session.rollback()
            finish_failed_run(session, run_id, records_found=found,
                              duplicate_count=duplicate_count, invalid_count=len(invalid), codes=invalid)
            return FxIngestionResult(run_id, found, 0, 0, found, "FAILED", duplicate_count, len(invalid))
        for idx, item in enumerate(items, 1):
            code = None
            if item.rate_type == "EXCHANGE_CENTER":
                code = "SCHEMA_RATE_TYPE_UNSUPPORTED"
            elif not isinstance(item.rate_type, str) or item.rate_type not in VALID_FX_RATE_TYPES:
                code = "INVALID_RATE_TYPE"
            try:
                rate = Decimal(item.rate) if item.rate is not None else None
            except Exception:
                rate = None
            if code is None and (rate is None or not rate.is_finite() or rate <= 0):
                code = "INVALID_RATE"
            if code is None and rate is not None:
                scale = max(0, -rate.as_tuple().exponent)
                integer_digits = max(0, len(rate.as_tuple().digits) - scale)
                if scale > 4 or integer_digits > 14:
                    code = "RATE_PRECISION_OUT_OF_RANGE"
            has_any_jalali = any(v is not None for v in (item.jalali_year, item.jalali_month, item.jalali_day))
            has_full_jalali = all(v is not None for v in (item.jalali_year, item.jalali_month, item.jalali_day))
            if code is None:
                if has_any_jalali and not has_full_jalali:
                    code = "INCOMPLETE_JALALI_IDENTITY"
                elif has_full_jalali:
                    parts = (item.jalali_year, item.jalali_month, item.jalali_day)
                    if any(type(v) is not int for v in parts) or not is_valid_jalali_components(*parts):
                        code = "INVALID_JALALI_DATE"
                    elif item.rate_date is not None:
                        code = "AMBIGUOUS_DATE_IDENTITY"
                elif type(item.rate_date) is not date:
                    code = "MISSING_OR_INVALID_DATE_IDENTITY"
            c_from = item.currency_from.strip().upper() if isinstance(item.currency_from, str) else ""
            c_to = item.currency_to.strip().upper() if isinstance(item.currency_to, str) else ""
            src = item.source if item.source is not None else source_label
            if code is None and (not c_from or not c_to or len(c_from) > 10 or len(c_to) > 10):
                code = "INVALID_CURRENCY_PAIR"
            if code is None and src is not None and (not isinstance(src, str) or len(src) > 100):
                code = "SOURCE_LABEL_TOO_LONG"
            if code is not None:
                invalid.append(f"ROW_{idx}_{code}")
                continue

            jy, jm, jd = (item.jalali_year, item.jalali_month, item.jalali_day) if has_full_jalali else (None, None, None)
            rdate = None if has_full_jalali else item.rate_date
            key = (jy, jm, jd, rdate, c_from, c_to, item.rate_type)
            if key in seen:
                if seen[key] == rate:
                    duplicate_count += 1
                else:
                    invalid.append(f"ROW_{idx}_IN_BATCH_CONFLICT")
                continue
            seen[key] = rate

            existing = find_fx_existing(session, rate_type=item.rate_type, c_from=c_from,
                c_to=c_to, rate_date=rdate, jy=jy, jm=jm, jd=jd)
            if existing is not None:
                if Decimal(existing.rate) == rate:
                    duplicate_count += 1
                else:
                    invalid.append(f"ROW_{idx}_EXISTING_KEY_CONFLICT")
                continue
            prepared.append(FXRate(rate_date=rdate, jalali_year=jy, jalali_month=jm,
                jalali_day=jd, currency_from=c_from, currency_to=c_to, rate=rate,
                rate_type=item.rate_type, source=src))

        if invalid:
            session.rollback()
            finish_failed_run(session, run_id, records_found=found,
                              duplicate_count=duplicate_count, invalid_count=len(invalid), codes=invalid)
            return FxIngestionResult(run_id, found, 0, 0, found, "FAILED", duplicate_count, len(invalid))

        session.add_all(prepared)
        finish_completed_run(run, records_found=found, records_inserted=len(prepared),
                             duplicate_count=duplicate_count)
        session.flush()
        session.commit()
        return FxIngestionResult(run_id, found, len(prepared), 0, 0, "COMPLETED", duplicate_count, 0)
    except IngestionAuditError:
        session.rollback()
        raise
    except Exception:
        session.rollback()
        finish_failed_run(session, run_id, records_found=found,
                          duplicate_count=duplicate_count, invalid_count=len(invalid),
                          codes=invalid + ["CANONICAL_TRANSACTION_FAILED"])
        return FxIngestionResult(run_id, found, 0, 0, found, "FAILED", duplicate_count, len(invalid))

def ingest_fx_xlsx(
    session: Session,
    path: Union[str, Path],
    *,
    rate_type: str,
    rates_in_toman: bool = False,
    source_label: Optional[str] = None,
) -> FxIngestionResult:
    """Facade: XLSX parsing in fx.adapter; persistence via ingest_fx_rates."""
    from src.ingestion.fx.adapter import parse_fx_xlsx

    label = source_label or f"XLSX_{rate_type}"
    if rates_in_toman and rate_type != "FREE_MARKET":
        raise ValueError("Toman conversion is only valid for FREE_MARKET")
    if rate_type not in {"FREE_MARKET", "EXCHANGE_CENTER"}:
        raise ValueError("rate_type must be FREE_MARKET or EXCHANGE_CENTER")
    try:
        parsed = parse_fx_xlsx(path, rate_type=rate_type, source_label=label)
    except Exception:
        return ingest_fx_rates(session, [], source_label=label,
                               _prevalidation_errors=("FX_WORKBOOK_READ_FAILED",), _records_found=0)
    identical_duplicates = sum("identical duplicate" in e for e in parsed["errors"])
    hard_errors = tuple(e for e in parsed["errors"] if "identical duplicate" not in e)
    return ingest_fx_rates(session, parsed["inputs"], source_label=label,
                           _prevalidation_errors=hard_errors,
                           _records_found=parsed["records_found"],
                           _parser_duplicate_count=identical_duplicates)


def parse_jalali_components(s: str) -> Optional[Tuple[int, int, int]]:
    """Re-export for tests/callers that import from service."""
    return _parse_jalali_components(s)
