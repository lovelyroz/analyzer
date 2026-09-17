"""Market OHLC persistence entry — re-exports service.ingest_ohlc_csv."""

from src.ingestion.service import OhlcIngestionResult, ingest_ohlc_csv

__all__ = ["OhlcIngestionResult", "ingest_ohlc_csv"]
