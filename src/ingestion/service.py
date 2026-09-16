from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional, Sequence

from sqlalchemy.orm import Session

from src.models.audit import IngestionRun
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