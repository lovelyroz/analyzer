from pathlib import Path
import re
import unicodedata

import pypdfium2 as pdfium


# --------------------------------------------------
# Configuration
# --------------------------------------------------

PDF_FILE = Path("pdf/Fzar.pdf")

RAW_FILE = Path("pdf/extraction_test/Fzar_pdfium_raw.txt")
NORMALIZED_FILE = Path("pdf/extraction_test/Fzar_pdfium_normalized.txt")
COMPARISON_FILE = Path("pdf/extraction_test/Fzar_pdfium_comparison.txt")


# Three numbers to verify in the extracted text.
# Commas are intentionally omitted because normalization removes separators.
TARGETS = [
    "17754190",
    "19603040",
    "26854565",
]

# Persian and Arabic digits -> ASCII digits
DIGIT_MAP = str.maketrans(
    "۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩",
    "01234567890123456789",
)


# --------------------------------------------------
# Text normalization
# --------------------------------------------------

def normalize_persian_text(text: str) -> str:
    """
    Normalize extracted Persian text for searching and comparison.

    - Apply Unicode NFKC normalization.
    - Convert Persian/Arabic digits to ASCII.
    - Normalize Arabic Yeh and Kaf.
    - Remove thousands separators.
    """

    text = unicodedata.normalize("NFKC", text)

    text = text.translate(DIGIT_MAP)

    text = text.replace("ي", "ی")
    text = text.replace("ك", "ک")

    # Remove numeric separators.
    text = text.replace(",", "")
    text = text.replace("٬", "")
    text = text.replace("،", "")

    return text


# --------------------------------------------------
# PDF extraction
# --------------------------------------------------

def extract_pdf_text(pdf_path: Path) -> str:
    if not pdf_path.exists():
        raise FileNotFoundError(
            f"PDF file not found: {pdf_path.resolve()}"
        )

    pdf = pdfium.PdfDocument(str(pdf_path))

    pages = []

    try:
        for page_number in range(len(pdf)):
            page = pdf[page_number]
            text_page = page.get_textpage()

            try:
                page_text = text_page.get_text_range()
                pages.append(
                    f"\n========== PAGE {page_number + 1} ==========\n"
                    f"{page_text}"
                )
            finally:
                text_page.close()
                page.close()

    finally:
        pdf.close()

    return "\n".join(pages)


# --------------------------------------------------
# Comparison report
# --------------------------------------------------

def create_comparison_report(
    raw_text: str,
    normalized_text: str,
) -> str:

    report = []

    # Persian word checks
    words = [
        "تراورتن",
        "کانسنگ",
        "طلا",
        "فروش",
        "تن",
    ]

    report.append("PERSIAN WORD CHECK")
    report.append("==================")

    for word in words:
        count = normalized_text.count(word)
        report.append(f"{word}: {count}")

    # Target number checks
    report.append("")
    report.append("--- Target numbers ---")

    for target in TARGETS:
        report.append("")
        report.append(f"Searching for: {target}")

        matches = [
            line.strip()
            for line in normalized_text.splitlines()
            if target in line
        ]

        if matches:
            for line in matches:
                report.append(line)
        else:
            report.append("NOT FOUND")

    # Raw text separator
    report.append("")
    report.append("--- Raw extraction check ---")

    for target in TARGETS:
        report.append("")
        report.append(f"Searching raw text for: {target}")

        matches = [
            line.strip()
            for line in raw_text.splitlines()
            if target in normalize_persian_text(line)
        ]

        if matches:
            for line in matches:
                report.append(line)
        else:
            report.append("NOT FOUND")

    return "\n".join(report)


# --------------------------------------------------
# Main
# --------------------------------------------------

def main():

    print("Extracting PDF...")

    raw_text = extract_pdf_text(PDF_FILE)

    print("Normalizing Persian text...")

    normalized_text = normalize_persian_text(raw_text)

    print("Saving raw extraction...")

    RAW_FILE.write_text(
        raw_text,
        encoding="utf-8",
    )

    print("Saving normalized extraction...")

    NORMALIZED_FILE.write_text(
        normalized_text,
        encoding="utf-8",
    )

    print("Creating comparison report...")

    report = create_comparison_report(
        raw_text,
        normalized_text,
    )

    COMPARISON_FILE.write_text(
        report,
        encoding="utf-8",
    )

    print("\nCompleted successfully.")

    print(f"Raw file:        {RAW_FILE.resolve()}")
    print(f"Normalized:     {NORMALIZED_FILE.resolve()}")
    print(f"Comparison:     {COMPARISON_FILE.resolve()}")


if __name__ == "__main__":
    main()