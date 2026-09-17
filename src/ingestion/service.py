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
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Optional, Sequence, Tuple, Union

from sqlalchemy.orm import Session

from src.ingestion.common.identity import find_fx_existing
from src.ingestion.common.parsing import parse_jalali_components as _parse_jalali_components
from src.ingestion.common.validation import VALID_FX_RATE_TYPES
from src.models.audit import IngestionRun
from src.models.fx import FXRate
from src.models.normalized import RawFinancialFact
from src.models.report import Report, ReportVersion

# Backward-compatible alias used by older tests/imports
_VALID_FX_RATE_TYPES = VALID_FX_RATE_TYPES


@dataclass(frozen=True)
class RawLineInput:
    """One extracted source line; no standardization is performed here."""

    item_name: str
    value: Optional[Decimal] = None
    item_code: Optional[str] = None
    unit: Optional[str] = None
    currency: Optional[str] = None
    source_section: Optional[str] = None
    source_row: Optional[int] = None
    source_column: Optional[str] = None


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
    """Persist one Codal report and its extracted raw lines atomically.

    PDF extraction is outside this function (CHANGE-007 / codal.adapter).
    """
    run = IngestionRun(source="CODAL", status="STARTED", records_found=len(raw_lines))
    session.add(run)
    session.flush()

    try:
        report = None
        if codal_tracking_id is not None:
            report = session.query(Report).filter_by(codal_tracking_id=codal_tracking_id).one_or_none()

        if report is None:
            report = Report(
                company_id=company_id,
                report_type=report_type,
                codal_tracking_id=codal_tracking_id,
                title=title,
                financial_period_id=period_id,
                source_url=source_url,
            )
            session.add(report)
            session.flush()

        if codal_tracking_id is not None:
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
                run.finished_at = datetime.utcnow()
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
                raw_item_name=line.item_name,
                raw_item_code=line.item_code,
                value=line.value,
                unit=line.unit,
                currency=line.currency,
                source_section=line.source_section,
                source_row=line.source_row,
                source_column=line.source_column,
            )
            for line in raw_lines
        ]
        session.add_all(facts)
        run.status = "COMPLETED"
        run.records_inserted = len(facts)
        run.finished_at = datetime.utcnow()
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
            finished_at=datetime.utcnow(),
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
    )


def ingest_fx_rates(
    session: Session,
    rates: Sequence[FxRateInput],
    *,
    source_label: str = "FX",
) -> FxIngestionResult:
    """Persist FX rate observations into fx_rates (CHANGE-001 / CHANGE-006).

    Accepts already-built FxRateInput DTOs only — no file parsing here.
    """
    run = IngestionRun(source="FX", status="STARTED", records_found=len(rates))
    session.add(run)
    session.flush()

    inserted = 0
    updated = 0
    failed = 0
    errors: list = []

    try:
        for idx, item in enumerate(rates):
            label = f"item {idx}"
            if item.rate_type not in VALID_FX_RATE_TYPES:
                failed += 1
                errors.append(f"{label}: invalid rate_type={item.rate_type!r}")
                continue
            if item.rate is None:
                failed += 1
                errors.append(f"{label}: rate is required (NULL not allowed)")
                continue
            try:
                rate_val = Decimal(item.rate)
            except Exception:
                failed += 1
                errors.append(f"{label}: rate not numeric")
                continue
            if rate_val <= 0:
                failed += 1
                errors.append(f"{label}: rate must be positive")
                continue

            has_jalali = (
                item.jalali_year is not None
                and item.jalali_month is not None
                and item.jalali_day is not None
            )
            if not has_jalali and item.rate_date is None:
                failed += 1
                errors.append(f"{label}: need jalali components or rate_date")
                continue

            c_from = (item.currency_from or "USD").strip().upper()
            c_to = (item.currency_to or "IRR").strip().upper()
            src = item.source or source_label

            jy = item.jalali_year if has_jalali else None
            jm = item.jalali_month if has_jalali else None
            jd = item.jalali_day if has_jalali else None
            rdate = None if has_jalali else item.rate_date

            existing = find_fx_existing(
                session,
                rate_type=item.rate_type,
                c_from=c_from,
                c_to=c_to,
                rate_date=rdate,
                jy=jy,
                jm=jm,
                jd=jd,
            )

            if existing is None:
                session.add(
                    FXRate(
                        rate_date=rdate,
                        jalali_year=jy,
                        jalali_month=jm,
                        jalali_day=jd,
                        currency_from=c_from,
                        currency_to=c_to,
                        rate=rate_val,
                        rate_type=item.rate_type,
                        source=src,
                    )
                )
                inserted += 1
            else:
                existing.rate = rate_val
                existing.source = src
                if has_jalali:
                    existing.jalali_year = jy
                    existing.jalali_month = jm
                    existing.jalali_day = jd
                    existing.rate_date = None
                updated += 1

        run.records_inserted = inserted
        run.records_updated = updated
        run.records_failed = failed
        run.error_log = "\n".join(errors[:50]) if errors else None
        run.status = "COMPLETED"
        run.finished_at = datetime.utcnow()
        session.commit()

        return FxIngestionResult(
            ingestion_id=run.ingestion_id,
            records_found=len(rates),
            records_inserted=inserted,
            records_updated=updated,
            records_failed=failed,
            status=run.status,
        )
    except Exception as exc:
        session.rollback()
        failed_run = IngestionRun(
            source="FX",
            status="FAILED",
            records_found=len(rates),
            records_failed=len(rates),
            error_log=str(exc),
            finished_at=datetime.utcnow(),
        )
        session.add(failed_run)
        session.commit()
        return FxIngestionResult(
            ingestion_id=failed_run.ingestion_id,
            records_found=len(rates),
            records_inserted=0,
            records_updated=0,
            records_failed=len(rates),
            status="FAILED",
        )


def ingest_fx_xlsx(
    session: Session,
    path: Union[str, Path],
    *,
    rate_type: str,
    rates_in_toman: bool = False,
    source_label: Optional[str] = None,
) -> FxIngestionResult:
    """Facade: XLSX parsing in fx.adapter; persistence via ingest_fx_rates."""
    from src.ingestion.fx.adapter import load_fx_xlsx_inputs

    label = source_label or f"XLSX_{rate_type}"
    inputs = load_fx_xlsx_inputs(
        path,
        rate_type=rate_type,
        rates_in_toman=rates_in_toman,
        source_label=label,
    )
    return ingest_fx_rates(session, inputs, source_label=label)


def parse_jalali_components(s: str) -> Optional[Tuple[int, int, int]]:
    """Re-export for tests/callers that import from service."""
    return _parse_jalali_components(s)
