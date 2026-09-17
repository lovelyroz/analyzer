"""CODAL ingestion package — acquisition, PDF extraction boundary, persistence."""

from src.ingestion.codal.acquisition import (
    AcquiredSource,
    CodalAcquisitionError,
    acquire_local_pdf,
    acquire_pdf_from_url,
)
from src.ingestion.codal.adapter import CodalExtractionResult, extract_raw_lines_from_pdf
from src.ingestion.codal.ingestion import ingest_codal_report
from src.ingestion.codal.pdf_extract import CodalExtractionError

__all__ = [
    "AcquiredSource",
    "CodalAcquisitionError",
    "CodalExtractionError",
    "CodalExtractionResult",
    "acquire_local_pdf",
    "acquire_pdf_from_url",
    "extract_raw_lines_from_pdf",
    "ingest_codal_report",
]
