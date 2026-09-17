from pathlib import Path

import pytest

from src.ingestion.codal.acquisition import CodalAcquisitionError, acquire_codal_pdf


def test_local_pdf_acquisition_preserves_source_and_bytes(tmp_path):
    source = Path(__file__).parents[2] / "pdf" / "seo-codal-report (1).pdf"
    destination = tmp_path / "acquired.pdf"

    result = acquire_codal_pdf(str(source), destination)

    assert result.path == destination
    assert result.source_url == str(source)
    assert result.source_identity == str(source.resolve())
    assert destination.read_bytes() == source.read_bytes()


def test_missing_source_is_distinguished_as_acquisition_failure(tmp_path):
    with pytest.raises(CodalAcquisitionError):
        acquire_codal_pdf(str(tmp_path / "missing.pdf"), tmp_path / "acquired.pdf", retries=0)


def test_non_pdf_local_source_is_rejected(tmp_path):
    source = tmp_path / "not-a-pdf.txt"
    source.write_text("not a pdf", encoding="utf-8")
    with pytest.raises(CodalAcquisitionError):
        acquire_codal_pdf(str(source), tmp_path / "acquired.pdf", retries=0)