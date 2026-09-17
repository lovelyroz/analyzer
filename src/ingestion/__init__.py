"""Stage 1 ingestion services — production data acquisition layer.

This package feeds the locked Stage 1 Data Foundation.
It does NOT implement any analytical Stage 2–9 logic.
"""

from src.ingestion.service import RawLineInput, ReportIngestionResult, ingest_codal_report
from src.ingestion.market import ingest_ohlc_csv, OhlcIngestionResult

__all__ = [
    "RawLineInput",
    "ReportIngestionResult",
    "ingest_codal_report",
    "ingest_ohlc_csv",
    "OhlcIngestionResult",
]
