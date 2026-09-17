"""CODAL ingestion package — PDF extraction boundary + raw persistence."""

from src.ingestion.codal.adapter import CodalExtractionResult, extract_raw_lines_from_pdf
from src.ingestion.codal.ingestion import ingest_codal_report

__all__ = [
    "CodalExtractionResult",
    "extract_raw_lines_from_pdf",
    "ingest_codal_report",
]
