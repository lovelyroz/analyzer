"""FX ingestion package — FREE_MARKET / OPERATIONAL adapters + persistence."""

from src.ingestion.fx.adapter import load_fx_xlsx_inputs
from src.ingestion.fx.ingestion import ingest_fx_rates, ingest_fx_xlsx

__all__ = ["load_fx_xlsx_inputs", "ingest_fx_rates", "ingest_fx_xlsx"]
