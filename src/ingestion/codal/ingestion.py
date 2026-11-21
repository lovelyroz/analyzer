"""Format-neutral CODAL persistence facade for pre-parsed source rows."""

from datetime import datetime
from typing import TYPE_CHECKING, Optional, Sequence

from sqlalchemy.orm import Session

if TYPE_CHECKING:
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


__all__ = ["ingest_codal_report"]
