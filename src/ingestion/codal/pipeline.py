"""End-to-end CODAL load: acquire → extract → validate → persist."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional, Union

from sqlalchemy.orm import Session

from src.ingestion.codal.acquisition import (
    CodalAcquisitionError,
    acquire_local_pdf,
)
from src.ingestion.codal.adapter import extract_raw_lines_from_pdf
from src.ingestion.codal.pdf_extract import CodalExtractionError
from src.ingestion.codal.validator import validate_raw_lines
from src.ingestion.service import ReportIngestionResult, ingest_codal_report


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
    acquired = acquire_local_pdf(
        path,
        codal_tracking_id=codal_tracking_id,
        source_url=source_url,
    )
    extracted = extract_raw_lines_from_pdf(
        acquired.local_path,
        title=title,
        report_type=report_type,
        publication_datetime=publication_datetime,
        codal_tracking_id=codal_tracking_id or acquired.codal_tracking_id,
        source_url=source_url or acquired.source_url,
        is_restated=is_restated,
    )
    errors = validate_raw_lines(extracted.raw_lines)
    if errors:
        raise ValueError("CODAL raw-line validation failed: " + "; ".join(errors[:20]))

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
