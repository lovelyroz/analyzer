"""Deterministic text-first parsing helpers for CODAL PDF extraction."""

from __future__ import annotations

import re
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import List, Optional, Tuple

from pypdf import PdfReader

from src.ingestion.codal.pdf_extract import CodalExtractionError as CodalPdfExtractionError
from src.ingestion.service import RawLineInput


PERSIAN_DIGITS = str.maketrans("۰۱۲۳۴۵۶۷۸۹", "0123456789")
ARABIC_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩", "0123456789")
NUMERIC_TOKEN = re.compile(r"[\(\[]?[۰-۹٠-٩0-9][۰-۹٠-٩0-9,٬،.]*[\)\]]?")
DATE_TOKEN = re.compile(r"^(?:13|14|15)\d{2}[/-]\d{1,2}[/-]\d{1,2}$")
DATE_IN_LINE = re.compile(r"(?:13|14|15)[۰-۹٠-٩0-9]{2}[/-][۰-۹٠-٩0-9]{1,2}[/-][۰-۹٠-٩0-9]{1,2}")
IGNORED_MARKERS = (
    "گزارش فعالیت ماهانه",
    "اطلاعات و صورت های مالی",
    "صورت سود و زیان",
    "شرکت:",
    "نماد",
    "کد صنعت",
    "سرمایه ثبت",
    "سال مالی منتهی",
    "وضعیت ناشر",
    "کلیه مبالغ",
)


def normalize_pdf_text(value: str) -> str:
    """Normalize digit variants and PDF separators without translating labels."""
    return (
        value.translate(PERSIAN_DIGITS)
        .translate(ARABIC_DIGITS)
        .replace("٬", ",")
        .replace("،", ",")
        .replace("﷼", "ریال")
        .strip()
    )


def parse_numeric_token(token: str) -> Optional[Decimal]:
    normalized = normalize_pdf_text(token).strip()
    negative = normalized.startswith(("(", "[")) and normalized.endswith((")", "]"))
    normalized = normalized.strip("()[]").replace(",", "")
    if not normalized or DATE_TOKEN.match(normalized):
        return None
    try:
        value = Decimal(normalized)
    except InvalidOperation:
        return None
    return -value if negative else value


def _looks_like_metadata(line: str) -> bool:
    compact = re.sub(r"\s+", "", line)
    return any(marker.replace(" ", "") in compact for marker in IGNORED_MARKERS)


def _line_value_tokens(line: str) -> List[Tuple[str, int]]:
    masked_line = DATE_IN_LINE.sub(lambda match: " " * len(match.group()), line)
    return [(match.group(), match.start()) for match in NUMERIC_TOKEN.finditer(masked_line)]


def extract_raw_lines_from_text(text: str, *, unit: Optional[str] = None) -> List[RawLineInput]:
    """Convert extracted PDF text into raw lines without concept mapping.

    Multiple numeric cells on one source row become separate raw lines with a
    source column marker. Dates, report metadata, and rows without a numeric
    value are not treated as financial facts. Missing cells remain absent or
    NULL; they are never converted to zero.
    """
    raw_lines: List[RawLineInput] = []
    for row_number, original_line in enumerate(text.splitlines(), start=1):
        line = normalize_pdf_text(original_line)
        if not line or _looks_like_metadata(line):
            continue
        tokens = _line_value_tokens(line)
        if not tokens:
            continue
        first_value_position = tokens[0][1]
        item_name = line[:first_value_position].strip(" :-|\t")
        if not item_name or DATE_TOKEN.match(item_name):
            continue
        for column_number, (token, _) in enumerate(tokens, start=1):
            value = parse_numeric_token(token)
            if value is None:
                continue
            raw_lines.append(RawLineInput(
                item_name=item_name,
                value=value,
                unit=unit,
                source_row=row_number,
                source_column=str(column_number),
            ))
    return raw_lines


def extract_text_from_pdf(path: str | Path) -> str:
    """Extract deterministic text using pypdf; reject image-only PDFs."""
    pdf_path = Path(path)
    if not pdf_path.is_file():
        raise CodalPdfExtractionError(f"CODAL PDF does not exist: {pdf_path}")
    try:
        reader = PdfReader(str(pdf_path))
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    except Exception as exc:
        raise CodalPdfExtractionError(f"Unable to read CODAL PDF: {pdf_path}") from exc
    if not text.strip():
        raise CodalPdfExtractionError(f"CODAL PDF contains no extractable text: {pdf_path}")
    return text
