"""End-to-end CODAL load: acquire → extract → validate → persist."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional, Union

from sqlalchemy.orm import Session

from src.ingestion.codal.acquisition import (
    CodalAcquisitionError,
    acquire_local_pdf,
    acquire_pdf_from_url,
)
from src.ingestion.codal.adapter import extract_raw_lines_from_pdf
from src.ingestion.codal.pdf_extract import CodalExtractionError
from src.ingestion.codal.validator import validate_raw_lines
from src.ingestion.service import ReportIngestionResult, ingest_codal_report
from src.models.audit import IngestionRun


def _audit_failed_run(session: Session, *, records_found: int, error_code: str, error: Exception) -> None:
    """Persist a failure audit without writing Report/RawFinancialFact rows."""
    session.rollback()
    session.add(
        IngestionRun(
            source="CODAL",
            status="FAILED",
            records_found=records_found,
            records_failed=1,
            error_log=f"{error_code}: {error}",
            finished_at=datetime.utcnow(),
        )
    )
    session.commit()


def _persist_acquired_pdf(
    session: Session,
    acquired_path: Path,
    *,
    company_id: int,
    period_id: int,
    title: str,
    report_type: str,
    publication_datetime: datetime,
    codal_tracking_id: Optional[str],
    source_url: Optional[str],
    is_restated: bool,
) -> ReportIngestionResult:
    try:
        extracted = extract_raw_lines_from_pdf(
            acquired_path,
            title=title,
            report_type=report_type,
            publication_datetime=publication_datetime,
            codal_tracking_id=codal_tracking_id,
            source_url=source_url,
            is_restated=is_restated,
        )
    except CodalExtractionError as exc:
        _audit_failed_run(session, records_found=0, error_code="EXTRACTION_FAILED", error=exc)
        raise

    errors = validate_raw_lines(extracted.raw_lines)
    if errors:
        error = ValueError("CODAL raw-line validation failed: " + "; ".join(errors[:20]))
        _audit_failed_run(session, records_found=len(extracted.raw_lines), error_code="VALIDATION_FAILED", error=error)
        raise error

    return ingest_codal_report(
        session,
        company_id=company_id,
        period_id=period_id,
        report_type=extracted.report_type,
        title=extracted.title,
        publication_datetime=extracted.publication_datetime,
        raw_lines=extracted.raw_lines,
        codal_tracking_id=extracted.codal_tracking_id,
        source_url=extracted.source_url,
        is_restated=extracted.is_restated,
    )


def load_codal_pdf(
    session: Session,
    path: Union[str, Path],
    *,
    company_id: int,
    period_id: int,
    title: str,
    report_type: str,
    publication_datetime: datetime,
    codal_tracking_id: Optional[str] = None,
    source_url: Optional[str] = None,
    is_restated: bool = False,
) -> ReportIngestionResult:
    """Production CODAL path using locked core persistence.

    Raises:
        CodalAcquisitionError — source missing / unreadable as file
        CodalExtractionError — PDF cannot be turned into RawLineInput
        ValueError — validation failed before persist
    """
    try:
        acquired = acquire_local_pdf(
            path,
            codal_tracking_id=codal_tracking_id,
            source_url=source_url,
        )
    except CodalAcquisitionError as exc:
        _audit_failed_run(session, records_found=0, error_code="ACQUISITION_FAILED", error=exc)
        raise

    return _persist_acquired_pdf(
        session,
        acquired.local_path,
        company_id=company_id,
        period_id=period_id,
        title=title,
        report_type=report_type,
        publication_datetime=publication_datetime,
        codal_tracking_id=codal_tracking_id or acquired.codal_tracking_id,
        source_url=source_url or acquired.source_url,
        is_restated=is_restated,
    )



def load_codal_pdf_from_url(
    session: Session,
    url: str,
    dest_dir: Union[str, Path],
    *,
    company_id: int,
    period_id: int,
    title: str,
    report_type: str,
    publication_datetime: datetime,
    codal_tracking_id: Optional[str] = None,
    is_restated: bool = False,
) -> ReportIngestionResult:
    """Production URL path: acquire bytes, then use the same locked local adapter."""
    try:
        acquired = acquire_pdf_from_url(
            url,
            dest_dir,
            codal_tracking_id=codal_tracking_id,
        )
    except CodalAcquisitionError as exc:
        _audit_failed_run(session, records_found=0, error_code="ACQUISITION_FAILED", error=exc)
        raise

    return _persist_acquired_pdf(
        session,
        acquired.local_path,
        company_id=company_id,
        period_id=period_id,
        title=title,
        report_type=report_type,
        publication_datetime=publication_datetime,
        codal_tracking_id=codal_tracking_id or acquired.codal_tracking_id,
        source_url=acquired.source_url or url,
        is_restated=is_restated,
    )
