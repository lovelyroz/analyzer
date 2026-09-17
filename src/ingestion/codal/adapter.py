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

from src.ingestion.codal.numbers import normalize_digits, parse_amount
from src.ingestion.codal.pdf_extract import CodalExtractionError, extract_cell_rows
from src.ingestion.service import RawLineInput


def _ascii_text(value: Optional[str]) -> Optional[str]:
    """Normalize numeric characters in persisted CODAL text fields to ASCII."""
    if value is None:
        return None
    return normalize_digits(value)


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
    """Extract RawLineInput rows from a CODAL PDF (local path).

    All textual fields crossing this boundary use ASCII/English digits.
    Numeric values are stored as Decimal. Blank/unparseable values remain
    None and are never forced to zero.

    Raises CodalExtractionError on unreadable/unsupported PDFs.
    Acquisition errors must be raised by acquisition.py, not this function.
    """
    path = Path(path)
    cell_rows = extract_cell_rows(path)

    raw_lines: List[RawLineInput] = []
    warnings: List[str] = []

    for cell in cell_rows:
        name = _ascii_text((cell.item_name or "").strip())
        if not name:
            warnings.append(f"page {cell.page} row {cell.source_row}: empty item name skipped")
            continue

        value = parse_amount(cell.value_text)
        raw_lines.append(
            RawLineInput(
                item_name=name,
                value=value,
                item_code=None,
                unit=_ascii_text(unit),
                currency=_ascii_text(currency),
                source_section=_ascii_text(cell.source_section),
                source_row=cell.source_row,
                source_column=_ascii_text(cell.source_column),
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
        title=_ascii_text(title) or "",
        report_type=_ascii_text(report_type) or "",
        publication_datetime=publication_datetime,
        codal_tracking_id=_ascii_text(codal_tracking_id),
        source_url=_ascii_text(source_url),
        is_restated=is_restated,
        extraction_backend=backend,
        warnings=tuple(warnings),
    )
