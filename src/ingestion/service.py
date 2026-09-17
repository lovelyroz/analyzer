from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Optional, Sequence, Union

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


def ingest_ohlc_csv(
    session: Session,
    path: Union[str, Path],
    *,
    source_label: str = "CSV_OHLC",
) -> OhlcIngestionResult:
    """Ingest an OHLC CSV (Iranian market format) into MarketDaily.

    Style mirrors ingest_codal_report: single function, inline IngestionRun,
    no parallel service layer.

    Date policy (important):
    - Source CSV uses Jalali dates (e.g. 1402-01-08).
    - MarketDaily.trade_date is SQLAlchemy Date (existing contract).
    - No calendar conversion is performed here.
    - Jalali string is kept as-is in the source field / error log when needed.
    - Insertion of trade_date currently requires a date object compatible with
      the existing Date column used by Stage 1 tests. This tension is left
      explicit for an architectural decision rather than silent conversion.

    Until that decision, rows with only Jalali dates are recorded as failed
    with a clear message so that no false valid data is created.
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

                # Explicit policy: no Jalali→Gregorian conversion.
                # Existing MarketDaily.trade_date is Date type used with Gregorian
                # date objects in Stage 1 tests. Until an architectural decision
                # is made on how to store Jalali dates, we do not invent a date
                # object and do not write a false valid row.
                errors.append(
                    f"line {line_no}: Jalali date {jdate_raw!r} kept as source; "
                    f"trade_date Date column requires architectural decision "
                    f"(no silent calendar conversion)"
                )
                failed += 1
                continue

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
