"""CODAL extraction-to-persistence facade."""

from datetime import datetime
from pathlib import Path
from typing import TYPE_CHECKING, Optional

from sqlalchemy.orm import Session

from src.ingestion.codal.adapter import extract_raw_lines_from_pdf

if TYPE_CHECKING:
    from src.ingestion.service import ReportIngestionResult


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
    # Local import prevents service ↔ codal package initialization cycles.
    from src.ingestion.service import ingest_codal_report

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


__all__ = ["ingest_codal_pdf"]
