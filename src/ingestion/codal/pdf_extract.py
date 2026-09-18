"""Replaceable PDF text/table extraction backends for CODAL.

Backends:
  1. pdfplumber tables (preferred for multi-column Codal forms)
  2. pypdf text lines (fallback)

The extraction layer is conservative: source text is preserved, date-like
cells are excluded from financial values, and header/section-only rows are not
emitted as raw financial facts.

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
_DATE_CELL_RE = re.compile(
    r"^\s*(?:13|14|15)\d{2}[/-]\d{1,2}[/-]\d{1,2}\s*$"
)


def _normalize_digits_for_detection(text: str) -> str:
    return (
        (text or "")
        .translate(str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789"))
        .translate(str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789"))
    )


def fix_persian_rtl(text: str) -> str:
    """Compatibility helper: preserve extractor text exactly.

    PDF text extraction can encode visual RTL order. Reversing an entire cell
    is unsafe, so this function intentionally performs no lexical reversal.
    """
    return text


def _persian_score(cell: str) -> int:
    return len(_PERSIAN_CHAR_RE.findall(cell or ""))


def _looks_like_date(cell: str) -> bool:
    normalized = _normalize_digits_for_detection(cell).replace("٫", "/")
    return bool(_DATE_CELL_RE.fullmatch(normalized))


def _looks_pure_number(cell: str) -> bool:
    if not cell or cell in {"-", "—", "–"}:
        return True
    if _looks_like_date(cell):
        return False
    s = _normalize_digits_for_detection(cell)
    s = s.replace(",", "").replace("٬", "").replace("،", "").replace(" ", "")
    s = re.sub(r"[()\-−]", "", s)
    if not s:
        return True
    return bool(re.fullmatch(r"[0-9.]+", s))


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
    """Choose the strongest text-label cell without reversing its content."""
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

                        for c_i, cell in enumerate(cells):
                            if c_i == name_col or not cell:
                                continue
                            if _looks_like_date(cell):
                                continue
                            if not _looks_pure_number(cell):
                                continue

                            col_label = headers[c_i] if c_i < len(headers) else f"col_{c_i}"
                            rows.append(
                                ExtractedCellRow(
                                    item_name=name,
                                    value_text=cell,
                                    source_section=section,
                                    source_row=r_i + 1,
                                    source_column=col_label,
                                    page=page_idx,
                                )
                            )
    except Exception:
        return []

    return rows


_NUMBER_TOKEN_RE = re.compile(
    r"(?<!\w)[(\[]?[−-]?[0-9۰-۹٠-٩][0-9۰-۹٠-٩,٬،.]*[)\]]?(?!\w)"
)


def _extract_numeric_tokens(line: str) -> List[Tuple[str, int, int]]:
    """Return numeric tokens while excluding date tokens."""
    result: List[Tuple[str, int, int]] = []
    for match in _NUMBER_TOKEN_RE.finditer(line or ""):
        token = match.group()
        if _looks_like_date(token):
            continue
        result.append((token, match.start(), match.end()))
    return result


def _name_from_line_and_tokens(line: str, tokens: Sequence[Tuple[str, int, int]]) -> str:
    """Extract label from either LTR (name then values) or RTL (values then name).

    CODAL PDFs commonly expose RTL text in visual order. We do not reverse the
    string; instead, when numeric tokens precede the Persian label, the label is
    taken from the trailing text. This preserves the actual extracted glyph
    sequence and avoids corrupting numbers.
    """
    if not tokens:
        return ""

    first_start = tokens[0][1]
    last_end = tokens[-1][2]

    prefix = line[:first_start].strip(" :-|\t")
    suffix = line[last_end:].strip(" :-|\t")

    if _persian_score(suffix) >= _persian_score(prefix):
        return suffix
    return prefix


def _lines_from_text_pages(pages: Sequence[Tuple[int, str]]) -> List[ExtractedCellRow]:
    rows: List[ExtractedCellRow] = []

    for page_no, text in pages:
        section = f"page_{page_no}"
        line_no = 0
        for raw_line in (text or "").splitlines():
            line = raw_line.strip()
            if not line:
                continue
            line_no += 1

            tokens = _extract_numeric_tokens(line)
            if not tokens:
                continue

            name = _name_from_line_and_tokens(line, tokens)
            if not name:
                continue

            for column_number, (token, _, _) in enumerate(tokens, start=1):
                rows.append(
                    ExtractedCellRow(
                        item_name=name,
                        value_text=token,
                        source_section=section,
                        source_row=line_no,
                        source_column=str(column_number),
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
