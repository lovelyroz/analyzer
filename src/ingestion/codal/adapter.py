"""CODAL PDF extraction boundary (CHANGE-007).

Codal financial statements arrive as PDFs. Extraction (table/text/OCR) is a
pre-ingestion responsibility. This adapter defines the contract:

    PDF (+ metadata)  →  Sequence[RawLineInput] + report metadata

Core persistence (`ingest_codal_report`) must not parse PDFs.

V1 does not lock a specific PDF library; implementers plug extraction here.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional, Sequence, Union

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


def extract_raw_lines_from_pdf(
    path: Union[str, Path],
    *,
    title: str,
    report_type: str,
    publication_datetime: datetime,
    codal_tracking_id: Optional[str] = None,
    source_url: Optional[str] = None,
    is_restated: bool = False,
) -> CodalExtractionResult:
    """Extract RawLineInput rows from a Codal PDF.

    Not implemented in V1 core: PDF tool choice is outside DATABASE_CONTRACT.
    Callers may supply pre-extracted lines directly to ingest_codal_report.
    """
    raise NotImplementedError(
        "CODAL PDF extraction is a pre-ingestion adapter boundary (CHANGE-007). "
        "Provide RawLineInput lines to ingest_codal_report, or implement this "
        "function with the chosen PDF extraction stack."
    )
