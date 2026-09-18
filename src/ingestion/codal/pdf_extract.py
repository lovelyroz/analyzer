"""Replaceable PDF text/table extraction backends for CODAL.

Backends:
  1. pdfplumber tables (preferred for multi-column Codal forms)
  2. pypdf text lines (fallback)

The extraction layer is deliberately conservative: source text is not
heuristically reversed, date-like cells are never treated as financial
amounts, and section/header-only rows are not emitted as raw financial facts.

OCR is not bundled; scanned PDFs without a text layer yield extraction errors.
"""

from __future__ import annotations

import re
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


_PERSIAN_CHAR_RE = re.compile(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]")
_DIGIT_RE = re.compile(r"[\d۰-۹٠-٩]")
_DATE_CELL_RE = re.compile(
    r"^\s*(?:13|14|15)[۰-۹٠-٩\d]{2}[/-][۰-۹٠-٩\d]{1,2}[/-][۰-۹٠-٩\d]{1,2}\s*$"
)


def fix_persian_rtl(text: str) -> str:
    """Compatibility helper: preserve extractor text exactly.

    Older versions reversed cells based on Persian-character density. That is
    unsafe because a correctly ordered cell can be reversed and numeric tokens
    can be corrupted. Raw extraction must remain source-faithful; any future
    RTL repair must be driven by explicit extractor evidence, not a heuristic.
    """
    return text


def _persian_score(cell: str) -> int:
    return len(_PERSIAN_CHAR_RE.findall(cell or ""))


def _looks_like_date(cell: str) -> bool:
    return bool(_DATE_CELL_RE.fullmatch(cell or ""))


def _looks_pure_number(cell: str) -> bool:
    if not cell or cell in {"-", "—", "–"}:
        return True
    if _looks_like_date(cell):
        return False
    s = cell.replace(",", "").replace("٬", "").replace(" ", "")
    s = re.sub(r"[()\-−]", "", s)
    if not s:
        return True
    return bool(re.fullmatch(r"[\d۰-۹٠-٩.]+", s))


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


def _header_labels(header_row: Sequence[str]) -> List[str]:
    labels: List[str] = []
    for i, h in enumerate(header_row):
        h = (h or "").strip().replace("\n", " ")
        labels.append(h if h else f"col_{i}")
    return labels


def _pick_name_cell(cells: Sequence[str]) -> Tuple[int, str]:
    """Choose a text label cell conservatively.

    Prefer cells containing Persian/Arabic letters. If several such cells are
    present, choose the longest one. This remains a heuristic and is kept only
    at the adapter boundary; downstream persistence preserves provenance.
    """
    best_i, best_score, best_len = -1, 0, 0
    for i, c in enumerate(cells):
        if not c:
            continue
        score = _persian_score(c)
        if score > best_score or (score == best_score and len(c) > best_len):
            best_i, best_score, best_len = i, score, len(c)
    if best_i < 0 or best_score == 0:
        return -1, ""
    return best_i, cells[best_i].strip()


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
                for t_i, table in enumerate(tables):
                    if not table:
                        continue

                    header_idx = 0
                    for ri, raw in enumerate(table[:5]):
                        joined = " ".join((c or "") for c in raw)
                        if any(
                            k in joined
                            for k in ("نام محصول", "نام", "شرح", "واحد", "مبلغ فروش", "مقدار مصرف")
                        ):
                            header_idx = ri
                            break
                    headers = _header_labels([(c or "") for c in table[header_idx]])

                    section = f"page_{page_idx}_table_{t_i}"

                    for r_i, raw_row in enumerate(table):
                        if r_i == header_idx:
                            continue
                        cells = [(c or "").strip().replace("\n", " ") for c in raw_row]
                        if not any(cells):
                            continue

                        name_col, name = _pick_name_cell(cells)
                        if not name:
                            continue

                        unit = ""
                        for idx in (name_col - 1, name_col + 1):
                            if 0 <= idx < len(cells) and cells[idx]:
                                cand = cells[idx].strip()
                                if cand in {
                                    "تن",
                                    "کیلوگرم",
                                    "عدد",
                                    "مترمکعب",
                                    "متر مکعب",
                                    "مگاوات ساعت",
                                    "کیلووات ساعت",
                                }:
                                    unit = cand
                                    break

                        for c_i, cell in enumerate(cells):
                            if c_i == name_col or not cell:
                                continue
                            if unit and cell == unit:
                                continue
                            if _looks_like_date(cell):
                                continue
                            if not _looks_pure_number(cell):
                                continue

                            col_label = headers[c_i] if c_i < len(headers) else f"col_{c_i}"
                            item = name
                            if unit:
                                item = f"{item} | {unit}"
                            if col_label and not col_label.startswith("col_"):
                                item = f"{item} | {col_label}"

                            rows.append(
                                ExtractedCellRow(
                                    item_name=item,
                                    value_text=cell,
                                    source_section=section,
                                    source_row=r_i + 1,
                                    source_column=col_label,
                                    page=page_idx,
                                )
                            )
    except Exception:
        # Never return a partial table extraction after a backend failure.
        # Let the caller fall back to the pypdf text backend.
        return []

    return rows


def _lines_from_text_pages(pages: Sequence[Tuple[int, str]]) -> List[ExtractedCellRow]:
    rows: List[ExtractedCellRow] = []
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
                value = m.group("value").strip()
                if _looks_like_date(value):
                    continue
                rows.append(
                    ExtractedCellRow(
                        item_name=m.group("name").strip(),
                        value_text=value,
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
    rows = _lines_from_text_pages(pages)
    if not rows:
        raise CodalExtractionError(
            f"PDF has text but no extractable financial value rows: {path}"
        )
    return rows
