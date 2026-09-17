"""FX format adapters (XLSX today). Unit conversion belongs here (CHANGE-006)."""

from __future__ import annotations

from decimal import Decimal
from pathlib import Path
from typing import List, Optional, Union

from src.ingestion.common.parsing import parse_jalali_components, to_decimal
from src.ingestion.common.validation import VALID_FX_RATE_TYPES
from src.ingestion.service import FxRateInput


def load_fx_xlsx_inputs(
    path: Union[str, Path],
    *,
    rate_type: str,
    rates_in_toman: bool = False,
    source_label: Optional[str] = None,
) -> List[FxRateInput]:
    """Parse a two-column Jalali FX workbook into FxRateInput DTOs.

    col0 = Jalali date string; col1 = rate.
    rates_in_toman=True multiplies by 10 (free-market Toman → IRR).
    """
    try:
        import openpyxl
    except ImportError as exc:
        raise ImportError("openpyxl is required for FX XLSX adapter") from exc

    if rate_type not in VALID_FX_RATE_TYPES:
        raise ValueError(f"invalid rate_type={rate_type!r}")

    path = Path(path)
    label = source_label or f"XLSX_{rate_type}"
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.active

    inputs: List[FxRateInput] = []
    for row_idx, row in enumerate(ws.iter_rows(values_only=True), start=1):
        if not row or row[0] is None:
            continue
        date_raw = str(row[0]).strip()
        if row_idx == 1 and any(ch.isalpha() for ch in date_raw.replace("-", "").replace("/", "")):
            continue
        if len(row) < 2 or row[1] is None:
            continue
        components = parse_jalali_components(date_raw)
        if components is None:
            continue
        jy, jm, jd = components
        rate_val = to_decimal(str(row[1]))
        if rate_val is None:
            continue
        if rates_in_toman:
            rate_val = rate_val * Decimal(10)
        inputs.append(
            FxRateInput(
                rate=rate_val,
                rate_type=rate_type,
                jalali_year=jy,
                jalali_month=jm,
                jalali_day=jd,
                source=label,
            )
        )
    wb.close()
    return inputs
