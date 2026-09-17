"""Replaceable PDF text/table extraction backends for CODAL.

Backends:
  1. pdfplumber tables (preferred for multi-column Codal forms)
  2. pypdf text lines (fallback)

Persian cells extracted from Codal PDFs are often visual-RTL reversed;
`fix_persian_rtl` restores readable order for storage as raw item names.

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


def fix_persian_rtl(text: str) -> str:
    """Restore readable order for cells that pdfplumber emits reversed."""
    if not text:
        return text
    persian = len(_PERSIAN_CHAR_RE.findall(text))
    if persian == 0:
        return text
    if persian >= max(1, len(text.replace(" ", "")) // 3):
        return text[::-1]
    return text


def _persian_score(cell: str) -> int:
    return len(_PERSIAN_CHAR_RE.findall(cell or ""))


def _looks_pure_number(cell: str) -> bool:
    if not cell or cell in {"-", "—", "–"}:
        return True
    s = cell.replace(",", "").replace("٬", "").replace(" ", "").replace("/", "")
    s = re.sub(r"[()\-−]", "", s)
    if not s:
        return True
    # pure numeric / decimal — not a label that happens to contain a grade digit
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
        h = fix_persian_rtl((h or "").strip().replace("\n", " "))
        labels.append(h if h else f"col_{i}")
    return labels


def _pick_name_cell(cells: Sequence[str]) -> Tuple[int, str]:
    """Choose product/label cell by highest Persian-letter density."""
    best_i, best_score, best_len = -1, 0, 0
    for i, c in enumerate(cells):
        if not c:
            continue
        score = _persian_score(c)
        if score > best_score or (score == best_score and len(c) > best_len):
            best_i, best_score, best_len = i, score, len(c)
    if best_i < 0 or best_score == 0:
        return -1, ""
    return best_i, fix_persian_rtl(cells[best_i])


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
                        joined = fix_persian_rtl(" ".join((c or "") for c in raw))
                        if any(k in joined for k in ("نام محصول", "نام", "شرح", "واحد", "مبلغ فروش", "مقدار مصرف")):
                            header_idx = ri
                            break
                    headers = _header_labels([(c or "") for c in table[header_idx]])

                    section = f"page_{page_idx}_table_{t_i}"
                    current_section_label = section

                    for r_i, raw_row in enumerate(table):
                        if r_i == header_idx:
                            continue
                        cells = [(c or "").strip().replace("\n", " ") for c in raw_row]
                        if not any(cells):
                            continue

                        non_empty = [c for c in cells if c]
                        if len(non_empty) == 1:
                            label = fix_persian_rtl(non_empty[0])
                            if label.startswith(":") or label.endswith(":") or any(
                                k in label for k in ("فروش", "درآمد", "برگشت", "تخفیف", "تخفيف", "جمع")
                            ):
                                current_section_label = f"{section}:{label.strip(':')}"
                                rows.append(
                                    ExtractedCellRow(
                                        item_name=label.strip(":"),
                                        value_text=None,
                                        source_section=current_section_label,
                                        source_row=r_i + 1,
                                        source_column="section",
                                        page=page_idx,
                                    )
                                )
                                continue

                        name_col, name = _pick_name_cell(cells)
                        if not name:
                            continue

                        unit = ""
                        for idx in (name_col - 1, name_col + 1):
                            if 0 <= idx < len(cells) and cells[idx]:
                                cand = fix_persian_rtl(cells[idx])
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

                        emitted = 0
                        for c_i, cell in enumerate(cells):
                            if c_i == name_col:
                                continue
                            if unit and fix_persian_rtl(cell) == unit:
                                continue
                            if not cell:
                                continue
                            if not _looks_pure_number(cell) and _persian_score(cell) > 0:
                                continue
                            if not _looks_pure_number(cell) and not _DIGIT_RE.search(cell):
                                continue
                            # value cells: pure numbers or dash
                            if not (_looks_pure_number(cell) or _DIGIT_RE.search(cell)):
                                continue
                            col_label = headers[c_i] if c_i < len(headers) else f"col_{c_i}"
                            item = name
                            if unit:
                                item = f"{name} | {unit}"
                            if col_label and not col_label.startswith("col_"):
                                item = f"{item} | {col_label}"
                            rows.append(
                                ExtractedCellRow(
                                    item_name=item,
                                    value_text=cell,
                                    source_section=current_section_label,
                                    source_row=r_i + 1,
                                    source_column=col_label,
                                    page=page_idx,
                                )
                            )
                            emitted += 1

                        if emitted == 0:
                            rows.append(
                                ExtractedCellRow(
                                    item_name=f"{name} | {unit}".strip(" |") if unit else name,
                                    value_text=None,
                                    source_section=current_section_label,
                                    source_row=r_i + 1,
                                    source_column="label",
                                    page=page_idx,
                                )
                            )
    except Exception:
        return rows
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
                rows.append(
                    ExtractedCellRow(
                        item_name=fix_persian_rtl(m.group("name").strip()),
                        value_text=m.group("value").strip(),
                        source_section=section,
                        source_row=line_no,
                        source_column="text",
                        page=page_no,
                    )
                )
            else:
                rows.append(
                    ExtractedCellRow(
                        item_name=fix_persian_rtl(line),
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
