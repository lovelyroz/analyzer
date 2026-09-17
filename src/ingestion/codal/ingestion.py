"""CODAL core persistence entry — re-exports service.ingest_codal_report."""

from src.ingestion.service import ReportIngestionResult, RawLineInput, ingest_codal_report

__all__ = ["RawLineInput", "ReportIngestionResult", "ingest_codal_report"]
