"""Stage 1 ingestion services.

Production data-acquisition layer that feeds the locked Stage 1 Data Foundation.
Does not implement any analytical Stage 2–9 logic.
"""

from src.ingestion.service import (
    RawLineInput,
    ReportIngestionResult,
    OhlcIngestionResult,
    ingest_codal_report,
    ingest_ohlc_csv,
)

__all__ = [
    "RawLineInput",
    "ReportIngestionResult",
    "OhlcIngestionResult",
    "ingest_codal_report",
    "ingest_ohlc_csv",
]
