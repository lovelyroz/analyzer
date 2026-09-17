"""CODAL extraction-to-persistence facade."""

from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Optional, Sequence

from sqlalchemy.orm import Session

from src.ingestion.codal.adapter import extract_raw_lines_from_pdf

if TYPE_CHECKING:
    from decimal import Decimal
    from src.ingestion.service import RawLineInput, ReportIngestionResult


def ingest_codal_report(
    session: Session,
    *,
    company_id: int,
    period_id: int,
    report_type: str,
    title: str,
    publication_datetime: datetime,
    raw_lines: Sequence["RawLineInput"],
    codal_tracking_id: Optional[str] = None,
    source_url: Optional[str] = None,
    is_restated: bool = False,
) -> "ReportIngestionResult":
    """Compatibility facade for the Stage 1 core CODAL persistence API."""
    from src.ingestion.service import ingest_codal_report as _persist

    return _persist(
        session,
        company_id=company_id,
        period_id=period_id,
        report_type=report_type,
        title=title,
        publication_datetime=publication_datetime,
        raw_lines=raw_lines,
        codal_tracking_id=codal_tracking_id,
        source_url=source_url,
        is_restated=is_restated,
    )


def ingest_codal_pdf(
    session: Session,
    path: str | Path,
    *,
    company_id: int,
    period_id: int,
    title: str,
    report_type: str,
    publication_datetime: datetime,
    codal_tracking_id: Optional[str] = None,
    source_url: Optional[str] = None,
    is_restated: bool = False,
) -> "ReportIngestionResult":
    """Extract a CODAL PDF and persist only its raw facts."""
    extraction = extract_raw_lines_from_pdf(
        path,
        title=title,
        report_type=report_type,
        publication_datetime=publication_datetime,
        codal_tracking_id=codal_tracking_id,
        source_url=source_url,
        is_restated=is_restated,
    )
    return ingest_codal_report(
        session,
        company_id=company_id,
        period_id=period_id,
        report_type=extraction.report_type,
        title=extraction.title,
        publication_datetime=extraction.publication_datetime,
        raw_lines=extraction.raw_lines,
        codal_tracking_id=extraction.codal_tracking_id,
        source_url=extraction.source_url,
        is_restated=extraction.is_restated,
    )


__all__ = ["ingest_codal_report", "ingest_codal_pdf"]
