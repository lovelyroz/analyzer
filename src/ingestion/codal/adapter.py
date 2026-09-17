"""CODAL PDF extraction boundary (CHANGE-007) — production implementation.

Pipeline:
    PDF path (+ metadata)
        → pdf_extract backends (pypdf / optional pdfplumber)
        → number normalization
        → Sequence[RawLineInput] + CodalExtractionResult

Does not map to standardized metrics, score, forecast, or decide.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Sequence, Union

from src.ingestion.codal.numbers import parse_amount
from src.ingestion.codal.pdf_extract import CodalExtractionError, extract_cell_rows
from src.ingestion.service import RawLineInput


@dataclass(frozen=True)
class CodalExtractionResult:
    """Output of the CODAL PDF extraction layer before persistence."""

    raw_lines: Sequence[RawLineInput]
    title: str
    report_type: str
    publication_datetime: datetime
    codal_tracking_id: Optional[str] = None
    source_url: Optional[str] = None
    is_restated: bool = False
    extraction_backend: Optional[str] = None
    warnings: Sequence[str] = ()


def extract_raw_lines_from_pdf(
    path: Union[str, Path],
    *,
    title: str,
    report_type: str,
    publication_datetime: datetime,
    codal_tracking_id: Optional[str] = None,
    source_url: Optional[str] = None,
    is_restated: bool = False,
    currency: str = "IRR",
    unit: Optional[str] = None,
) -> CodalExtractionResult:
    """Extract RawLineInput rows from a Codal PDF (local path).

    Raises CodalExtractionError on unreadable/unsupported PDFs.
    Acquisition errors must be raised by acquisition.py, not this function.
    """
    path = Path(path)
    cell_rows = extract_cell_rows(path)

    raw_lines: List[RawLineInput] = []
    warnings: List[str] = []

    for cell in cell_rows:
        name = (cell.item_name or "").strip()
        if not name:
            warnings.append(f"page {cell.page} row {cell.source_row}: empty item name skipped")
            continue

        value = parse_amount(cell.value_text)
        # Explicit blank value_text → None; unparsable also → None (never invent / never force 0)
        raw_lines.append(
            RawLineInput(
                item_name=name,
                value=value,
                item_code=None,
                unit=unit,
                currency=currency,
                source_section=cell.source_section,
                source_row=cell.source_row,
                source_column=cell.source_column,
            )
        )

    if not raw_lines:
        raise CodalExtractionError(
            f"PDF produced zero RawLineInput rows: {path}"
        )

    backend = "pdfplumber_tables" if any(
        (r.source_section or "").endswith("_table") for r in cell_rows
    ) else "pypdf_text"

    return CodalExtractionResult(
        raw_lines=tuple(raw_lines),
        title=title,
        report_type=report_type,
        publication_datetime=publication_datetime,
        codal_tracking_id=codal_tracking_id,
        source_url=source_url,
        is_restated=is_restated,
        extraction_backend=backend,
        warnings=tuple(warnings),
    )
