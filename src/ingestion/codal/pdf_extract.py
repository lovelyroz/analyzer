"""Replaceable PDF text/table extraction backends for CODAL.

Primary: pypdf text extraction (always available when installed).
Optional: pdfplumber table extraction when installed.

OCR is not bundled; scanned PDFs without text layer will yield few/no lines.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence, Tuple, Union


class CodalExtractionError(Exception):
    """PDF was acquired but could not be parsed into source lines."""


@dataclass(frozen=True)
class ExtractedCellRow:
    """One logical source row before conversion to RawLineInput."""

    item_name: str
    value_text: Optional[str]
    source_section: Optional[str]
    source_row: Optional[int]
    source_column: Optional[str]
    page: int


def _extract_text_pypdf(path: Path) -> List[Tuple[int, str]]:
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise CodalExtractionError(
            "pypdf is required for CODAL PDF extraction. Install with: pip install pypdf"
        ) from exc

    try:
        reader = PdfReader(str(path))
    except Exception as exc:
        raise CodalExtractionError(f"failed to open PDF: {path}: {exc}") from exc

    pages: List[Tuple[int, str]] = []
    for i, page in enumerate(reader.pages, start=1):
        try:
            text = page.extract_text() or ""
        except Exception:
            text = ""
        pages.append((i, text))
    return pages


def _extract_tables_pdfplumber(path: Path) -> List[ExtractedCellRow]:
    try:
        import pdfplumber
    except ImportError:
        return []

    rows: List[ExtractedCellRow] = []
    try:
        with pdfplumber.open(str(path)) as pdf:
            for page_idx, page in enumerate(pdf.pages, start=1):
                tables = page.extract_tables() or []
                for table in tables:
                    for r_i, row in enumerate(table, start=1):
                        if not row:
                            continue
                        cells = [(c or "").strip() for c in row]
                        if not any(cells):
                            continue
                        # Heuristic: first non-empty cell = name, last numeric-looking = value
                        name = cells[0] if cells else ""
                        value_text = cells[-1] if len(cells) > 1 else None
                        if len(cells) > 2 and not cells[-1]:
                            value_text = cells[-2] if cells[-2] else value_text
                        if not name:
                            continue
                        rows.append(
                            ExtractedCellRow(
                                item_name=name,
                                value_text=value_text,
                                source_section=f"page_{page_idx}_table",
                                source_row=r_i,
                                source_column="last",
                                page=page_idx,
                            )
                        )
    except Exception:
        return rows
    return rows


def _lines_from_text_pages(pages: Sequence[Tuple[int, str]]) -> List[ExtractedCellRow]:
    """Split page text into candidate item lines.

    Supports simple patterns:
      NAME  1,234
      NAME: 1234
      NAME\t1234
    """
    import re

    rows: List[ExtractedCellRow] = []
    # value at end: optional sign/parens, digits with separators
    value_re = re.compile(
        r"^(?P<name>.+?)[\s:\t]+(?P<value>\(?[-−]?[\d۰-۹٠-٩٬,./\s]+\)?|-)$"
    )

    for page_no, text in pages:
        section = f"page_{page_no}"
        line_no = 0
        for raw_line in (text or "").splitlines():
            line = raw_line.strip()
            if not line:
                continue
            line_no += 1
            m = value_re.match(line)
            if m:
                rows.append(
                    ExtractedCellRow(
                        item_name=m.group("name").strip(),
                        value_text=m.group("value").strip(),
                        source_section=section,
                        source_row=line_no,
                        source_column="text",
                        page=page_no,
                    )
                )
            else:
                # Label-only line — preserve as missing value (NULL, not zero)
                rows.append(
                    ExtractedCellRow(
                        item_name=line,
                        value_text=None,
                        source_section=section,
                        source_row=line_no,
                        source_column="text",
                        page=page_no,
                    )
                )
    return rows


def extract_cell_rows(path: Union[str, Path]) -> List[ExtractedCellRow]:
    """Run replaceable backends; prefer table rows when available, else text."""
    path = Path(path)
    if not path.is_file():
        raise CodalExtractionError(f"PDF not found: {path}")

    table_rows = _extract_tables_pdfplumber(path)
    if table_rows:
        return table_rows

    pages = _extract_text_pypdf(path)
    if not any(t.strip() for _, t in pages):
        raise CodalExtractionError(
            f"no extractable text layer in PDF (scanned/image-only?): {path}"
        )
    return _lines_from_text_pages(pages)
