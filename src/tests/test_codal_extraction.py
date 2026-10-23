"""CODAL production extraction / acquisition tests (Workstream A–C)."""

from __future__ import annotations

import os
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.core.database import Base
from src.ingestion.codal.acquisition import CodalAcquisitionError, acquire_local_pdf
from src.ingestion.codal.adapter import extract_raw_lines_from_pdf
from src.ingestion.codal.numbers import normalize_digits, parse_amount
from src.ingestion.codal.pdf_extract import CodalExtractionError, fix_persian_rtl
from src.ingestion.codal.pipeline import load_codal_pdf
from src.ingestion.service import RawLineInput, ingest_codal_report
from src.migrations.runner import MigrationRunner
from src.models.entity import Company, Industry
from src.models.normalized import RawFinancialFact
from src.models.period import FinancialPeriod
from src.models.report import Report, ReportVersion
from src.models.audit import IngestionRun


def _make_text_pdf(path: Path, lines: list[str]) -> Path:
    """Minimal PDF with a text layer via pypdf writing raw content stream."""
    y = 750
    content_ops = ["BT", "/F1 12 Tf"]
    for line in lines:
        safe = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
        content_ops.append(f"50 {y} Td ({safe}) Tj")
        content_ops.append("0 -16 Td")
        y -= 16
    content_ops.append("ET")
    stream = "\n".join(content_ops).encode("latin-1", errors="replace")

    objects = []

    def obj(n: int, body: bytes) -> bytes:
        return f"{n} 0 obj\n".encode() + body + b"\nendobj\n"

    objects.append(obj(1, b"<< /Type /Catalog /Pages 2 0 R >>"))
    objects.append(obj(2, b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>"))
    objects.append(
        obj(
            3,
            b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
            b"/Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>",
        )
    )
    objects.append(
        obj(4, f"<< /Length {len(stream)} >>\nstream\n".encode() + stream + b"\nendstream")
    )
    objects.append(obj(5, b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"))

    out = bytearray(b"%PDF-1.4\n")
    offsets = [0]
    for o in objects:
        offsets.append(len(out))
        out.extend(o)
    xref_pos = len(out)
    out.extend(f"xref\n0 {len(objects)+1}\n".encode())
    out.extend(b"0000000000 65535 f \n")
    for off in offsets[1:]:
        out.extend(f"{off:010d} 00000 n \n".encode())
    out.extend(
        f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n".encode()
    )
    path.write_bytes(bytes(out))
    return path


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    MigrationRunner(engine).upgrade()
    Session = sessionmaker(bind=engine)
    s = Session()
    ind = Industry(industry_code="BANK", industry_name="Bank")
    s.add(ind)
    s.flush()
    co = Company(ticker="TEST", company_name="Test Co", industry_id=ind.industry_id, codal_symbol="TEST")
    s.add(co)
    s.flush()
    period = FinancialPeriod(
        company_id=co.company_id,
        period_type="QUARTER",
        start_date=__import__("datetime").date(2024, 1, 1),
        end_date=__import__("datetime").date(2024, 3, 31),
        fiscal_year=1403,
        fiscal_quarter=1,
        months_length=3,
        is_ytd=False,
    )
    s.add(period)
    s.commit()
    s._test_company_id = co.company_id
    s._test_period_id = period.period_id
    yield s
    s.close()


def test_normalize_persian_digits():
    assert normalize_digits("۱۲۳۴۵۶") == "123456"
    assert normalize_digits("٠١٢") == "012"


def test_parse_amount_null_not_zero():
    assert parse_amount(None) is None
    assert parse_amount("") is None
    assert parse_amount("-") is None
    assert parse_amount("—") is None
    assert parse_amount("0") == Decimal("0")
    assert parse_amount("1,234") == Decimal("1234")
    assert parse_amount("(1,500)") == Decimal("-1500")
    assert parse_amount("۱۲۳") == Decimal("123")
    assert parse_amount("not-a-number") is None


def test_fix_persian_rtl_preserves_extracted_text():
    source = "٣ هجرد يتﻼکش نتروارت گنس جارختسا"
    assert fix_persian_rtl(source) == source
    assert fix_persian_rtl("نام محصول") == "نام محصول"


def test_extract_text_pdf_lines(tmp_path):
    p = _make_text_pdf(
        tmp_path / "fs.pdf",
        [
            "Revenue 1,000",
            "Cost of sales (400)",
            "Other income -",
            "Net profit 600",
        ],
    )
    result = extract_raw_lines_from_pdf(
        p,
        title="Test FS",
        report_type="QUARTERLY",
        publication_datetime=datetime(2024, 4, 15, 10, 0),
        codal_tracking_id="T-100",
        source_url="file://test",
    )
    assert len(result.raw_lines) >= 3
    values = [r.value for r in result.raw_lines if r.value is not None]
    assert Decimal("1000") in values or Decimal("600") in values
    assert result.codal_tracking_id == "T-100"
    assert all(r.source_section for r in result.raw_lines)


def test_extract_missing_stays_none(tmp_path):
    p = _make_text_pdf(tmp_path / "miss.pdf", ["Empty line item -"])
    result = extract_raw_lines_from_pdf(
        p,
        title="M",
        report_type="ANNUAL",
        publication_datetime=datetime(2024, 1, 1),
    )
    assert result.raw_lines
    assert any(r.value is None for r in result.raw_lines)


def test_extract_non_pdf_fails(tmp_path):
    bad = tmp_path / "x.txt"
    bad.write_text("not a pdf", encoding="utf-8")
    with pytest.raises((CodalExtractionError, Exception)):
        extract_raw_lines_from_pdf(
            bad,
            title="x",
            report_type="Q",
            publication_datetime=datetime(2024, 1, 1),
        )


def test_pipeline_persists_report_version_and_raw(session, tmp_path):
    p = _make_text_pdf(
        tmp_path / "load.pdf",
        ["Operating revenue 2500", "Operating expense (900)"],
    )
    result = load_codal_pdf(
        session,
        p,
        company_id=session._test_company_id,
        period_id=session._test_period_id,
        title="Q1 Report",
        report_type="QUARTERLY",
        publication_datetime=datetime(2024, 4, 20, 12, 0),
        codal_tracking_id="CODAL-PIPE-1",
        source_url="https://codal.ir/example",
    )
    assert result.raw_fact_count >= 1
    report = session.query(Report).filter_by(codal_tracking_id="CODAL-PIPE-1").one()
    assert report.source_url == "https://codal.ir/example"
    version = session.get(ReportVersion, result.report_version_id)
    assert version.publication_datetime == datetime(2024, 4, 20, 12, 0)
    assert version.is_current_version is True
    facts = session.query(RawFinancialFact).filter_by(report_version_id=version.report_version_id).all()
    assert len(facts) == result.raw_fact_count
    run = session.get(IngestionRun, result.ingestion_id)
    assert run.status == "COMPLETED"




def test_pipeline_acquisition_failure_is_audited_without_partial_writes(session, tmp_path):
    from src.ingestion.codal.pipeline import load_codal_pdf

    with pytest.raises(CodalAcquisitionError):
        load_codal_pdf(
            session,
            tmp_path / "missing.pdf",
            company_id=session._test_company_id,
            period_id=session._test_period_id,
            title="Missing",
            report_type="CODAL",
            publication_datetime=datetime(2024, 5, 1),
            codal_tracking_id="CODAL-ACQ-FAIL",
        )

    run = session.query(IngestionRun).order_by(IngestionRun.ingestion_id.desc()).first()
    assert run.status == "FAILED"
    assert "ACQUISITION_FAILED" in (run.error_log or "")
    assert session.query(Report).count() == 0
    assert session.query(RawFinancialFact).count() == 0


def test_pipeline_extraction_failure_is_audited_without_partial_writes(session, tmp_path):
    from src.ingestion.codal.pipeline import load_codal_pdf

    bad = tmp_path / "bad.pdf"
    bad.write_bytes(b"not a valid pdf")

    with pytest.raises(CodalExtractionError):
        load_codal_pdf(
            session,
            bad,
            company_id=session._test_company_id,
            period_id=session._test_period_id,
            title="Bad",
            report_type="CODAL",
            publication_datetime=datetime(2024, 5, 1),
            codal_tracking_id="CODAL-EXT-FAIL",
        )

    run = session.query(IngestionRun).order_by(IngestionRun.ingestion_id.desc()).first()
    assert run.status == "FAILED"
    assert "EXTRACTION_FAILED" in (run.error_log or "")
    assert session.query(Report).count() == 0
    assert session.query(RawFinancialFact).count() == 0


def test_pipeline_idempotent_version_chain(session, tmp_path):
    p = _make_text_pdf(tmp_path / "v.pdf", ["Item A 10"])
    r1 = load_codal_pdf(
        session,
        p,
        company_id=session._test_company_id,
        period_id=session._test_period_id,
        title="R",
        report_type="QUARTERLY",
        publication_datetime=datetime(2024, 5, 1),
        codal_tracking_id="CODAL-IDEM",
    )
    r2 = load_codal_pdf(
        session,
        p,
        company_id=session._test_company_id,
        period_id=session._test_period_id,
        title="R",
        report_type="QUARTERLY",
        publication_datetime=datetime(2024, 5, 15),
        codal_tracking_id="CODAL-IDEM",
        is_restated=True,
    )
    versions = (
        session.query(ReportVersion)
        .join(Report)
        .filter(Report.codal_tracking_id == "CODAL-IDEM")
        .order_by(ReportVersion.version_number)
        .all()
    )
    assert len(versions) == 2
    assert versions[0].is_current_version is False
    assert versions[1].is_current_version is True
    assert versions[1].version_number == versions[0].version_number + 1
    assert r1.report_id == r2.report_id


def test_codal_ingestion_rejects_period_owned_by_another_company(session):
    industry_id = session.query(Industry).one().industry_id
    other_company = Company(
        ticker="OTHER",
        company_name="Other Co",
        industry_id=industry_id,
        codal_symbol="OTHER",
    )
    session.add(other_company)
    session.flush()
    other_period = FinancialPeriod(
        company_id=other_company.company_id,
        period_type="QUARTER",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 3, 31),
        fiscal_year=1403,
        fiscal_quarter=1,
        months_length=3,
        is_ytd=False,
    )
    session.add(other_period)
    session.commit()

    with pytest.raises(ValueError, match="period company_id does not match"):
        ingest_codal_report(
            session,
            company_id=session._test_company_id,
            period_id=other_period.period_id,
            report_type="QUARTERLY",
            title="Identity check",
            publication_datetime=datetime(2024, 4, 15),
            raw_lines=[RawLineInput(item_name="unmapped source row")],
        )

    assert session.query(Report).count() == 0
    assert session.query(RawFinancialFact).count() == 0


def test_codal_tracking_id_cannot_be_reused_for_another_company_or_period(session):
    first = ingest_codal_report(
        session,
        company_id=session._test_company_id,
        period_id=session._test_period_id,
        report_type="QUARTERLY",
        title="Original report identity",
        publication_datetime=datetime(2024, 4, 15),
        codal_tracking_id="CODAL-IDENTITY",
        raw_lines=[RawLineInput(item_name="unmapped source row")],
    )

    industry_id = session.query(Industry).one().industry_id
    other_company = Company(
        ticker="OTHER",
        company_name="Other Co",
        industry_id=industry_id,
        codal_symbol="OTHER",
    )
    session.add(other_company)
    session.flush()
    other_period = FinancialPeriod(
        company_id=other_company.company_id,
        period_type="QUARTER",
        start_date=date(2024, 1, 1),
        end_date=date(2024, 3, 31),
        fiscal_year=1403,
        fiscal_quarter=1,
        months_length=3,
        is_ytd=False,
    )
    session.add(other_period)
    session.commit()

    with pytest.raises(ValueError, match="tracking ID is already assigned"):
        ingest_codal_report(
            session,
            company_id=other_company.company_id,
            period_id=other_period.period_id,
            report_type="QUARTERLY",
            title="Conflicting report identity",
            publication_datetime=datetime(2024, 5, 15),
            codal_tracking_id="CODAL-IDENTITY",
            raw_lines=[RawLineInput(item_name="unmapped source row")],
        )

    assert session.query(Report).count() == 1
    assert session.query(ReportVersion).count() == 1
    assert session.query(RawFinancialFact).count() == 1
    assert first.report_id == session.query(Report).one().report_id


def _candidate_real_codal_paths() -> list[Path]:
    env = os.environ.get("CODAL_SAMPLE_PDF")
    candidates = []
    if env:
        candidates.append(Path(env))
    candidates.extend(
        [
            Path("/home/workdir/attachments/fzar_403_aban.pdf"),
            Path(__file__).resolve().parents[2] / "fixtures" / "codal" / "fzar_403_aban.pdf",
        ]
    )
    return [p for p in candidates if p.is_file()]


@pytest.mark.skipif(not _candidate_real_codal_paths(), reason="real Codal sample PDF not available in CI")
def test_real_codal_monthly_activity_pdf():
    """Regression against representative monthly production/sales Codal form."""
    path = _candidate_real_codal_paths()[0]
    result = extract_raw_lines_from_pdf(
        path,
        title="گزارش فعالیت ماهانه تولید و فروش",
        report_type="MONTHLY_ACTIVITY",
        publication_datetime=datetime(2024, 11, 20),
        codal_tracking_id="FZAR-403-ABAN",
    )
    assert result.extraction_backend in {"pdfplumber_tables", "pypdf_text"}
    assert len(result.raw_lines) >= 5
    names = " ".join(r.item_name for r in result.raw_lines)
    assert any(k in names for k in ("تراورتن", "کانسنگ", "طلا", "فروش", "تن"))
    assert any(r.value is None for r in result.raw_lines) or any(r.value == 0 for r in result.raw_lines)
    assert all(r.source_section for r in result.raw_lines)
