from datetime import datetime
from pathlib import Path

from src.ingestion.codal.adapter import extract_raw_lines_from_pdf
from src.ingestion.codal.parser import CodalPdfExtractionError


PDF_ROOT = Path(__file__).parents[2] / "pdf"


def test_report_all_codal_pdf_extraction_outcomes():
    outcomes = {}
    for path in sorted(PDF_ROOT.glob("*.pdf")):
        try:
            result = extract_raw_lines_from_pdf(
                path,
                title=path.name,
                report_type="CODAL",
                publication_datetime=datetime(2026, 9, 1),
            )
            outcomes[path.name] = len(result.raw_lines)
        except CodalPdfExtractionError as exc:
            outcomes[path.name] = f"ERROR: {exc}"

    assert all(isinstance(v, int) and v > 0 for v in outcomes.values()), outcomes
