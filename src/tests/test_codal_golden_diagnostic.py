from pathlib import Path
import re

import pdfplumber


PDF_ROOT = Path(__file__).parents[2] / "pdf"
TARGET = "درآمد تسهیلات اعطایی"


def _normalize_digits(text):
    return text.translate(str.maketrans("۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩", "01234567890123456789"))


def test_diagnostic_codal_source_representation():
    """Diagnostic only: expose the independent PDF representation for the failing row."""
    path = PDF_ROOT / "seo-codal-report (1).pdf"
    found = []
    with pdfplumber.open(str(path)) as pdf:
        for page_no, page in enumerate(pdf.pages, start=1):
            for line in (page.extract_text() or "").splitlines():
                normalized = _normalize_digits(line)
                if any(part in normalized for part in ("درآمد", "تسهیلات", "اعطایی")):
                    numbers = re.findall(r"[-(]?\d[\d,٬،.\s]*\d|[-(]?\d+", normalized)
                    found.append((page_no, normalized, numbers))
    print("GOLDEN_DIAGNOSTIC", found)
    assert found
