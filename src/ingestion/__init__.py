"""Stage 1 ingestion services (CHANGE-007 package layout).

Physical structure:

    src/ingestion/
      common/     shared parse, validation, identity, run tracker
      codal/      PDF extraction boundary + CODAL persistence entry
      market/     OHLC adapters + persistence entry
      fx/         FX adapters (incl. Toman→Rial) + persistence entry
      service.py  core DTOs + core persistence (stable public surface)

Production data-acquisition layer that feeds the locked Stage 1 Data Foundation.
Does not implement any analytical Stage 2–9 logic.
"""

from src.ingestion.service import (
    RawLineInput,
    ReportIngestionResult,
    OhlcIngestionResult,
    FxRateInput,
    FxIngestionResult,
    ingest_codal_report,
    ingest_ohlc_csv,
    ingest_fx_rates,
    ingest_fx_xlsx,
)

__all__ = [
    "RawLineInput",
    "ReportIngestionResult",
    "OhlcIngestionResult",
    "FxRateInput",
    "FxIngestionResult",
    "ingest_codal_report",
    "ingest_ohlc_csv",
    "ingest_fx_rates",
    "ingest_fx_xlsx",
]
