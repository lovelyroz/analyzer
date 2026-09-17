from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Optional, Sequence, Tuple, Union

from sqlalchemy.orm import Session

from src.models.audit import IngestionRun
from src.models.entity import Company
from src.models.market import MarketDaily
from src.models.normalized import RawFinancialFact
from src.models.report import Report, ReportVersion


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

    This function deliberately stops at the raw layer. Mapping decisions and
    normalized facts belong to later steps in the ingestion pipeline.
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


def _to_decimal(raw: Optional[str]) -> Optional[Decimal]:
    if raw is None or str(raw).strip() == "":
        return None
    try:
        return Decimal(str(raw).strip().replace(",", ""))
    except Exception:
        return None


def _to_int(raw: Optional[str]) -> Optional[int]:
    if raw is None or str(raw).strip() == "":
        return None
    try:
        return int(Decimal(str(raw).strip().replace(",", "")))
    except Exception:
        return None


def _normalize_header(h: str) -> str:
    return h.strip().lower().replace("-", "").replace("_", "").replace(" ", "")


def _parse_jalali_components(s: str) -> Optional[Tuple[int, int, int]]:
    """Parse 'YYYY-MM-DD' or 'YYYY/MM/DD' Jalali text into (year, month, day).

    This is string splitting of the source calendar label only.
    It is NOT a Jalali→Gregorian calendar conversion.
    """
    s = s.strip().replace("/", "-")
    parts = s.split("-")
    if len(parts) != 3:
        return None
    try:
        y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
    except ValueError:
        return None
    if not (1 <= m <= 12 and 1 <= d <= 31):
        return None
    return y, m, d


def ingest_ohlc_csv(
    session: Session,
    path: Union[str, Path],
    *,
    source_label: str = "CSV_OHLC",
) -> OhlcIngestionResult:
    """Ingest an OHLC CSV (Iranian market format) into MarketDaily.

    Style mirrors ingest_codal_report: single function, inline IngestionRun.

    Date policy (CHANGE-005):
    - Source CSV uses Jalali dates (e.g. 1402-01-08).
    - jalali_year / jalali_month / jalali_day are filled from the source string.
    - No Jalali→Gregorian calendar conversion is performed.
    - Same-month comparisons across years use jalali_month (independent of year/day).
    - trade_date is left NULL for Jalali-sourced rows (backward-compatible Date column).
    - Identity / idempotency key for Jalali rows: (company_id, jalali_year, jalali_month, jalali_day).
    - Missing numeric values stay NULL (NULL != 0).
    """
    import csv
    from pathlib import Path as P

    path = P(path)
    run = IngestionRun(source="OHLC", status="STARTED", records_found=0)
    session.add(run)
    session.flush()

    try:
        with path.open(encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
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

            colmap = {}
            header_map = {
                "jdate": "jdate", "date": "jdate",
                "open": "open", "high": "high", "low": "low", "close": "close",
                "final": "final", "adjclose": "final", "adjustedclose": "final",
                "volume": "volume", "value": "value",
                "no": "trade_count", "tradecount": "trade_count",
                "ticker": "ticker", "symbol": "ticker",
            }
            for h in reader.fieldnames:
                key = _normalize_header(h)
                if key in header_map:
                    colmap[header_map[key]] = h

            if "jdate" not in colmap or "ticker" not in colmap:
                raise ValueError("CSV missing required columns: jdate/date and ticker/symbol")

            rows = list(reader)
            run.records_found = len(rows)

            inserted = 0
            updated = 0
            failed = 0
            errors = []

            for line_no, row in enumerate(rows, start=2):
                jdate_raw = (row.get(colmap["jdate"]) or "").strip()
                ticker = (row.get(colmap["ticker"]) or "").strip()
                if not jdate_raw or not ticker:
                    failed += 1
                    errors.append(f"line {line_no}: missing date or ticker")
                    continue

                components = _parse_jalali_components(jdate_raw)
                if components is None:
                    failed += 1
                    errors.append(f"line {line_no}: invalid Jalali date {jdate_raw!r}")
                    continue

                jy, jm, jd = components

                company = session.query(Company).filter_by(ticker=ticker).one_or_none()
                if company is None:
                    failed += 1
                    errors.append(f"line {line_no}: company ticker={ticker!r} not found")
                    continue

                open_p = _to_decimal(row.get(colmap.get("open", "")))
                high_p = _to_decimal(row.get(colmap.get("high", "")))
                low_p = _to_decimal(row.get(colmap.get("low", "")))
                close_p = _to_decimal(row.get(colmap.get("close", "")))
                final_p = _to_decimal(row.get(colmap.get("final", "")))
                adjusted = final_p if final_p is not None else close_p
                volume = _to_int(row.get(colmap.get("volume", "")))
                value = _to_decimal(row.get(colmap.get("value", "")))
                trade_count = _to_int(row.get(colmap.get("trade_count", "")))

                # Basic OHLC consistency when all four present
                if all(v is not None for v in (open_p, high_p, low_p, close_p)):
                    if high_p < low_p or high_p < open_p or high_p < close_p or low_p > open_p or low_p > close_p:
                        failed += 1
                        errors.append(f"line {line_no}: OHLC consistency failed")
                        continue

                existing = (
                    session.query(MarketDaily)
                    .filter_by(
                        company_id=company.company_id,
                        jalali_year=jy,
                        jalali_month=jm,
                        jalali_day=jd,
                    )
                    .one_or_none()
                )

                if existing is None:
                    session.add(MarketDaily(
                        company_id=company.company_id,
                        trade_date=None,
                        jalali_year=jy,
                        jalali_month=jm,
                        jalali_day=jd,
                        open_price=open_p,
                        high_price=high_p,
                        low_price=low_p,
                        close_price=close_p,
                        adjusted_close=adjusted,
                        volume=volume,
                        value=value,
                        trade_count=trade_count,
                        source=source_label,
                    ))
                    inserted += 1
                else:
                    existing.open_price = open_p
                    existing.high_price = high_p
                    existing.low_price = low_p
                    existing.close_price = close_p
                    existing.adjusted_close = adjusted
                    existing.volume = volume
                    existing.value = value
                    existing.trade_count = trade_count
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
