"""FX persistence entry points."""

from __future__ import annotations

from pathlib import Path
from typing import Optional, Sequence, Union

from sqlalchemy.orm import Session

from src.ingestion.fx.adapter import load_fx_xlsx_inputs
from src.ingestion.service import FxIngestionResult, FxRateInput, ingest_fx_rates


def ingest_fx_xlsx(
    session: Session,
    path: Union[str, Path],
    *,
    rate_type: str,
    rates_in_toman: bool = False,
    source_label: Optional[str] = None,
) -> FxIngestionResult:
    """Adapter + core: XLSX → FxRateInput[] → fx_rates."""
    label = source_label or f"XLSX_{rate_type}"
    inputs = load_fx_xlsx_inputs(
        path,
        rate_type=rate_type,
        rates_in_toman=rates_in_toman,
        source_label=label,
    )
    return ingest_fx_rates(session, inputs, source_label=label)


__all__ = ["FxRateInput", "FxIngestionResult", "ingest_fx_rates", "ingest_fx_xlsx"]
