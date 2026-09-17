"""OHLC / MarketDaily ingestion adapters."""

from src.ingestion.market.ingestion import ingest_ohlc_csv, OhlcIngestionResult

__all__ = ["ingest_ohlc_csv", "OhlcIngestionResult"]
