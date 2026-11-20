"""Read-only workbook adapter for approved USD/IRR sell observations."""
from __future__ import annotations

from decimal import Decimal
from pathlib import Path
from typing import List, Optional, Union

from src.ingestion.common.parsing import parse_jalali_components, to_decimal
from src.ingestion.service import FxRateInput


def _header_kind(value) -> Optional[str]:
    if not isinstance(value, str):
        return None
    text = " ".join(value.strip().lower().replace("ـ", "").split())
    if "\u062a\u0627\u0631\u06cc\u062e" in text or "\u062a\u0627\u0631\u064a\u062e" in text:
        return "date"
    if "\u0641\u0631\u0648\u0634" in text:
        return "sell"
    return None


def parse_fx_xlsx(path: Union[str, Path], *, rate_type: str, source_label: Optional[str] = None) -> dict:
    """Parse workbook headers and sell-only cells; return DTOs and diagnostics."""
    try:
        import openpyxl
        from openpyxl.utils import get_column_letter
    except ImportError as exc:
        raise ImportError("openpyxl is required for FX XLSX adapter") from exc
    if rate_type not in {"FREE_MARKET", "EXCHANGE_CENTER"}:
        raise ValueError("rate_type must be FREE_MARKET or EXCHANGE_CENTER")
    wb = openpyxl.load_workbook(Path(path), read_only=True, data_only=True)
    inputs: List[FxRateInput] = []
    errors: List[str] = []
    mappings = []
    seen = {}
    factor = Decimal(10) if rate_type == "FREE_MARKET" else Decimal(1)
    label = source_label or f"XLSX_{rate_type}"
    try:
        for ws in wb.worksheets:
            mapping = None
            for header_row, row in enumerate(ws.iter_rows(values_only=True), 1):
                kinds = [_header_kind(v) for v in row]
                if "date" in kinds and "sell" in kinds:
                    mapping = (next(i for i, x in enumerate(kinds) if x == "date"),
                               next(i for i, x in enumerate(kinds) if x == "sell"), header_row)
                    break
            if mapping is None:
                continue
            date_col, sell_col, header_row = mapping
            mappings.append({"sheet": ws.title, "header_row": header_row,
                             "date_column": date_col + 1, "sell_column": sell_col + 1})
            for row_idx, row in enumerate(ws.iter_rows(min_row=header_row + 1, values_only=True), header_row + 1):
                date = row[date_col] if date_col < len(row) else None
                rate = row[sell_col] if sell_col < len(row) else None
                if date is None and rate is None:
                    continue
                comp = parse_jalali_components(str(date).strip()) if date is not None else None
                parsed = to_decimal(str(rate)) if rate is not None else None
                if comp is None:
                    errors.append(f"{ws.title}!row {row_idx}: invalid Jalali date {date!r}")
                    continue
                if parsed is None or not parsed.is_finite() or parsed <= 0:
                    errors.append(f"{ws.title}!row {row_idx}: invalid sell rate {rate!r}")
                    continue
                canonical = parsed * factor
                key = comp
                if key in seen:
                    previous_rate, previous_ref = seen[key]
                    kind = "identical duplicate" if previous_rate == canonical else "conflicting duplicate"
                    current_ref = f"{ws.title}!{get_column_letter(date_col + 1)}{row_idx}/{get_column_letter(sell_col + 1)}{row_idx}"
                    errors.append(f"{current_ref}: {kind} for {date!r}; prior source {previous_ref}")
                    continue
                from openpyxl.utils import get_column_letter
                seen[key] = (canonical, f"{ws.title}!{get_column_letter(date_col + 1)}{row_idx}/{get_column_letter(sell_col + 1)}{row_idx}")
                inputs.append(FxRateInput(rate=canonical, rate_type=rate_type,
                    jalali_year=comp[0], jalali_month=comp[1], jalali_day=comp[2], source=label))
    finally:
        wb.close()
    if not mappings:
        errors.append("Workbook has no row containing both a recognized date header and sell header")
    return {"inputs": inputs, "errors": errors, "mappings": mappings, "conversion_factor": str(factor)}


def load_fx_xlsx_inputs(path: Union[str, Path], *, rate_type: str,
                        rates_in_toman: bool = False, source_label: Optional[str] = None) -> List[FxRateInput]:
    """Compatibility facade; FREE_MARKET is always Toman × 10 by contract."""
    if rates_in_toman and rate_type != "FREE_MARKET":
        raise ValueError("Toman conversion is only valid for FREE_MARKET")
    result = parse_fx_xlsx(path, rate_type=rate_type, source_label=source_label)
    if result["errors"]:
        raise ValueError("FX workbook validation failed: " + "; ".join(result["errors"]))
    if not result["inputs"]:
        raise ValueError("FX workbook contains no valid sell observations")
    return result["inputs"]
