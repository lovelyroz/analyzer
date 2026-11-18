# CODAL/PDF dependency inventory

- Repository root: D:\winprojects\analyzer
- Text/source files scanned: 5611
- Files with matches: 26
- Database opened: NO
- Source files changed: NO
- Tests executed: NO

## Match counts by category (matching lines)
- PRODUCTION_SOURCE: 131
- TEST: 121
- SCRIPT: 24
- ROOT_OR_CONFIG: 0

## Match counts by symbol
- CodalAcquisitionError: 20
- CodalExtractionError: 20
- CodalExtractionResult: 6
- RawFinancialFact: 45
- RawLineInput: 35
- ReportIngestionResult: 13
- acquire_codal_pdf: 5
- acquire_local_pdf: 7
- acquire_pdf_from_url: 6
- extract_raw_lines_from_pdf: 21
- ingest_codal_pdf: 11
- ingest_codal_report: 26
- load_codal_pdf: 9
- load_codal_pdf_from_url: 1
- normalize_digits: 16
- parse_amount: 17
- raw_financial_facts: 27
- src.ingestion.codal: 29
- validate_raw_lines: 3

## File and line matches

### src/ingestion/__init__.py [PRODUCTION_SOURCE]
- L17 | symbols=RawLineInput |     RawLineInput,
- L18 | symbols=ReportIngestionResult |     ReportIngestionResult,
- L22 | symbols=ingest_codal_report |     ingest_codal_report,
- L29 | symbols=RawLineInput |     "RawLineInput",
- L30 | symbols=ReportIngestionResult |     "ReportIngestionResult",
- L34 | symbols=ingest_codal_report |     "ingest_codal_report",
### src/ingestion/codal/__init__.py [PRODUCTION_SOURCE]
- L3 | symbols=src.ingestion.codal | from src.ingestion.codal.acquisition import (
- L5 | symbols=CodalAcquisitionError |     CodalAcquisitionError,
- L6 | symbols=acquire_local_pdf |     acquire_local_pdf,
- L7 | symbols=acquire_pdf_from_url |     acquire_pdf_from_url,
- L9 | symbols=src.ingestion.codal, CodalExtractionResult, extract_raw_lines_from_pdf | from src.ingestion.codal.adapter import CodalExtractionResult, extract_raw_lines_from_pdf
- L10 | symbols=src.ingestion.codal, ingest_codal_report | from src.ingestion.codal.ingestion import ingest_codal_report
- L11 | symbols=src.ingestion.codal, CodalExtractionError | from src.ingestion.codal.pdf_extract import CodalExtractionError
- L15 | symbols=CodalAcquisitionError |     "CodalAcquisitionError",
- L16 | symbols=CodalExtractionError |     "CodalExtractionError",
- L17 | symbols=CodalExtractionResult |     "CodalExtractionResult",
- L18 | symbols=acquire_local_pdf |     "acquire_local_pdf",
- L19 | symbols=acquire_pdf_from_url |     "acquire_pdf_from_url",
- L20 | symbols=extract_raw_lines_from_pdf |     "extract_raw_lines_from_pdf",
- L21 | symbols=ingest_codal_report |     "ingest_codal_report",
### src/ingestion/codal/acquisition.py [PRODUCTION_SOURCE]
- L17 | symbols=CodalAcquisitionError | class CodalAcquisitionError(Exception):
- L45 | symbols=acquire_local_pdf | def acquire_local_pdf(
- L54 | symbols=CodalAcquisitionError |         raise CodalAcquisitionError(f"local PDF not found: {p}")
- L56 | symbols=CodalAcquisitionError |         raise CodalAcquisitionError(f"expected .pdf file, got: {p.suffix!r}")
- L66 | symbols=acquire_codal_pdf | def acquire_codal_pdf(
- L75 | symbols=acquire_pdf_from_url |     acquisition remains available through acquire_pdf_from_url().
- L79 | symbols=acquire_local_pdf |     acquired = acquire_local_pdf(source_path)
- L85 | symbols=CodalAcquisitionError |         raise CodalAcquisitionError(
- L97 | symbols=acquire_pdf_from_url | def acquire_pdf_from_url(
- L125 | symbols=CodalAcquisitionError |         raise CodalAcquisitionError(f"HTTP {exc.code} acquiring {url}") from exc
- L127 | symbols=CodalAcquisitionError |         raise CodalAcquisitionError(f"URL error acquiring {url}: {exc.reason}") from exc
- L129 | symbols=CodalAcquisitionError |         raise CodalAcquisitionError(f"acquisition failed for {url}: {exc}") from exc
- L132 | symbols=CodalAcquisitionError |         raise CodalAcquisitionError(f"empty response from {url}")
- L134 | symbols=CodalAcquisitionError |         raise CodalAcquisitionError(f"response is not a PDF from {url}")
### src/ingestion/codal/adapter.py [PRODUCTION_SOURCE]
- L7 | symbols=RawLineInput, CodalExtractionResult |         → Sequence[RawLineInput] + CodalExtractionResult
- L19 | symbols=src.ingestion.codal, normalize_digits, parse_amount | from src.ingestion.codal.numbers import normalize_digits, parse_amount
- L20 | symbols=src.ingestion.codal, CodalExtractionError | from src.ingestion.codal.pdf_extract import CodalExtractionError, extract_cell_rows
- L23 | symbols=RawLineInput |     from src.ingestion.service import RawLineInput
- L30 | symbols=normalize_digits |     return normalize_digits(value)
- L34 | symbols=CodalExtractionResult | class CodalExtractionResult:
- L37 | symbols=RawLineInput |     raw_lines: Sequence[RawLineInput]
- L48 | symbols=extract_raw_lines_from_pdf | def extract_raw_lines_from_pdf(
- L59 | symbols=CodalExtractionResult | ) -> CodalExtractionResult:
- L60 | symbols=RawLineInput |     """Extract RawLineInput rows from a CODAL PDF (local path).
- L66 | symbols=CodalExtractionError |     Raises CodalExtractionError on unreadable/unsupported PDFs.
- L70 | symbols=RawLineInput |     # preserving the existing RawLineInput public DTO contract.
- L71 | symbols=RawLineInput |     from src.ingestion.service import RawLineInput
- L76 | symbols=RawLineInput |     raw_lines: List[RawLineInput] = []
- L85 | symbols=parse_amount |         value = parse_amount(cell.value_text)
- L87 | symbols=RawLineInput |             RawLineInput(
- L100 | symbols=CodalExtractionError, RawLineInput |         raise CodalExtractionError(f"PDF produced zero RawLineInput rows: {path}")
- L106 | symbols=CodalExtractionResult |     return CodalExtractionResult(
### src/ingestion/codal/ingestion.py [PRODUCTION_SOURCE]
- L9 | symbols=src.ingestion.codal, extract_raw_lines_from_pdf | from src.ingestion.codal.adapter import extract_raw_lines_from_pdf
- L10 | symbols=src.ingestion.codal, CodalExtractionError | from src.ingestion.codal.pdf_extract import CodalExtractionError
- L14 | symbols=RawLineInput, ReportIngestionResult |     from src.ingestion.service import RawLineInput, ReportIngestionResult
- L17 | symbols=ingest_codal_report | def ingest_codal_report(
- L25 | symbols=RawLineInput |     raw_lines: Sequence["RawLineInput"],
- L29 | symbols=ReportIngestionResult | ) -> "ReportIngestionResult":
- L31 | symbols=ingest_codal_report |     from src.ingestion.service import ingest_codal_report as _persist
- L47 | symbols=ingest_codal_pdf | def ingest_codal_pdf(
- L59 | symbols=ReportIngestionResult | ) -> "ReportIngestionResult":
- L63 | symbols=RawFinancialFact |     original exception is re-raised. No Report/RawFinancialFact persistence is
- L67 | symbols=extract_raw_lines_from_pdf |         extraction = extract_raw_lines_from_pdf(
- L76 | symbols=CodalExtractionError |     except CodalExtractionError as exc:
- L90 | symbols=ingest_codal_report |     return ingest_codal_report(
- L104 | symbols=ingest_codal_report, ingest_codal_pdf | __all__ = ["ingest_codal_report", "ingest_codal_pdf"]
### src/ingestion/codal/numbers.py [PRODUCTION_SOURCE]
- L15 | symbols=normalize_digits | def normalize_digits(text: str) -> str:
- L20 | symbols=parse_amount | def parse_amount(raw: Optional[str]) -> Optional[Decimal]:
- L32 | symbols=normalize_digits |     s = normalize_digits(raw).strip()
### src/ingestion/codal/parser.py [PRODUCTION_SOURCE]
- L12 | symbols=src.ingestion.codal, CodalExtractionError | from src.ingestion.codal.pdf_extract import CodalExtractionError as CodalPdfExtractionError
- L13 | symbols=RawLineInput | from src.ingestion.service import RawLineInput
- L70 | symbols=RawLineInput | def extract_raw_lines_from_text(text: str, *, unit: Optional[str] = None) -> List[RawLineInput]:
- L78 | symbols=RawLineInput |     raw_lines: List[RawLineInput] = []
- L94 | symbols=RawLineInput |             raw_lines.append(RawLineInput(
### src/ingestion/codal/pdf_extract.py [PRODUCTION_SOURCE]
- L22 | symbols=CodalExtractionError | class CodalExtractionError(Exception):
- L28 | symbols=RawLineInput |     """One logical source row before conversion to RawLineInput."""
- L44 | symbols=normalize_digits | def _normalize_digits_for_detection(text: str) -> str:
- L70 | symbols=normalize_digits |     normalized = _normalize_digits_for_detection(text)
- L80 | symbols=normalize_digits |     normalized = _normalize_digits_for_detection(cell).replace("٫", "/")
- L89 | symbols=normalize_digits |     s = _normalize_digits_for_detection(cell)
- L101 | symbols=CodalExtractionError |         raise CodalExtractionError(
- L108 | symbols=CodalExtractionError |         raise CodalExtractionError(f"failed to open PDF: {path}: {exc}") from exc
- L296 | symbols=CodalExtractionError |         raise CodalExtractionError(f"PDF not found: {path}")
- L304 | symbols=CodalExtractionError |         raise CodalExtractionError(
- L309 | symbols=CodalExtractionError |         raise CodalExtractionError(
### src/ingestion/codal/pipeline.py [PRODUCTION_SOURCE]
- L11 | symbols=src.ingestion.codal | from src.ingestion.codal.acquisition import (
- L12 | symbols=CodalAcquisitionError |     CodalAcquisitionError,
- L13 | symbols=acquire_local_pdf |     acquire_local_pdf,
- L14 | symbols=acquire_pdf_from_url |     acquire_pdf_from_url,
- L16 | symbols=src.ingestion.codal, extract_raw_lines_from_pdf | from src.ingestion.codal.adapter import extract_raw_lines_from_pdf
- L17 | symbols=src.ingestion.codal, CodalExtractionError | from src.ingestion.codal.pdf_extract import CodalExtractionError
- L18 | symbols=src.ingestion.codal, validate_raw_lines | from src.ingestion.codal.validator import validate_raw_lines
- L19 | symbols=ReportIngestionResult, ingest_codal_report | from src.ingestion.service import ReportIngestionResult, ingest_codal_report
- L24 | symbols=RawFinancialFact |     """Persist a failure audit without writing Report/RawFinancialFact rows."""
- L51 | symbols=ReportIngestionResult | ) -> ReportIngestionResult:
- L53 | symbols=extract_raw_lines_from_pdf |         extracted = extract_raw_lines_from_pdf(
- L62 | symbols=CodalExtractionError |     except CodalExtractionError as exc:
- L66 | symbols=validate_raw_lines |     errors = validate_raw_lines(extracted.raw_lines)
- L72 | symbols=ingest_codal_report |     return ingest_codal_report(
- L86 | symbols=load_codal_pdf | def load_codal_pdf(
- L98 | symbols=ReportIngestionResult | ) -> ReportIngestionResult:
- L102 | symbols=CodalAcquisitionError |         CodalAcquisitionError — source missing / unreadable as file
- L103 | symbols=CodalExtractionError, RawLineInput |         CodalExtractionError — PDF cannot be turned into RawLineInput
- L107 | symbols=acquire_local_pdf |         acquired = acquire_local_pdf(
- L112 | symbols=CodalAcquisitionError |     except CodalAcquisitionError as exc:
- L131 | symbols=load_codal_pdf_from_url | def load_codal_pdf_from_url(
- L143 | symbols=ReportIngestionResult | ) -> ReportIngestionResult:
- L146 | symbols=acquire_pdf_from_url |         acquired = acquire_pdf_from_url(
- L151 | symbols=CodalAcquisitionError |     except CodalAcquisitionError as exc:
### src/ingestion/codal/validator.py [PRODUCTION_SOURCE]
- L7 | symbols=RawLineInput | from src.ingestion.service import RawLineInput
- L10 | symbols=validate_raw_lines, RawLineInput | def validate_raw_lines(raw_lines: Sequence[RawLineInput]) -> List[str]:
### src/ingestion/service.py [PRODUCTION_SOURCE]
- L12 | symbols=RawLineInput |   - DTOs (RawLineInput, FxRateInput, result types)
- L13 | symbols=ingest_codal_report |   - CODAL raw persistence (ingest_codal_report)
- L26 | symbols=src.ingestion.codal, normalize_digits | from src.ingestion.codal.numbers import normalize_digits
- L32 | symbols=RawFinancialFact | from src.models.normalized import RawFinancialFact
- L41 | symbols=RawLineInput | class RawLineInput:
- L58 | symbols=normalize_digits |     return normalize_digits(value)
- L62 | symbols=ReportIngestionResult | class ReportIngestionResult:
- L112 | symbols=ingest_codal_report | def ingest_codal_report(
- L120 | symbols=RawLineInput |     raw_lines: Sequence[RawLineInput],
- L124 | symbols=ReportIngestionResult | ) -> ReportIngestionResult:
- L187 | symbols=RawFinancialFact |                 existing_count = session.query(RawFinancialFact).filter_by(
- L195 | symbols=ReportIngestionResult |                 return ReportIngestionResult(
- L229 | symbols=RawFinancialFact |             RawFinancialFact(
- L250 | symbols=ReportIngestionResult |         return ReportIngestionResult(
### src/migrations/runner.py [PRODUCTION_SOURCE]
- L22 | symbols=RawFinancialFact |     RawFinancialFact,
### src/models/normalized.py [PRODUCTION_SOURCE]
- L23 | symbols=RawFinancialFact | class RawFinancialFact(Base):
- L24 | symbols=raw_financial_facts |     __tablename__ = "raw_financial_facts"
- L86 | symbols=raw_financial_facts |     raw_fact_id = Column(Integer, ForeignKey("raw_financial_facts.raw_fact_id"), nullable=False)
- L125 | symbols=raw_financial_facts |     raw_fact_id = Column(Integer, ForeignKey("raw_financial_facts.raw_fact_id"), nullable=True)
### src/models/normalized_provenance.py [PRODUCTION_SOURCE]
- L19 | symbols=raw_financial_facts |         ForeignKey("raw_financial_facts.raw_fact_id"),
### src/scripts/audit_legacy_raw_fact_links.py [SCRIPT]
- L1 | symbols=raw_financial_facts | """Read-only row-linkage audit for legacy raw_financial_facts.
- L45 | symbols=RawFinancialFact |         "# Legacy RawFinancialFact Row-Linkage Audit",
- L53 | symbols=raw_financial_facts |         if not table_exists(connection, "raw_financial_facts"):
- L54 | symbols=raw_financial_facts |             raise SystemExit("Table raw_financial_facts does not exist.")
- L57 | symbols=raw_financial_facts |             "SELECT COUNT(*) FROM raw_financial_facts"
- L111 | symbols=raw_financial_facts |                 f"FROM raw_financial_facts r "
- L124 | symbols=raw_financial_facts |                 f"LEFT JOIN raw_financial_facts r ON r.raw_fact_id=t.{qcolumn} "
- L143 | symbols=raw_financial_facts |                 "FROM raw_financial_facts r "
### src/scripts/audit_legacy_raw_fact_provenance.py [SCRIPT]
- L1 | symbols=RawFinancialFact | """Read-only audit of legacy RawFinancialFact provenance in the local SQLite DB.
- L39 | symbols=RawFinancialFact |         "# Legacy RawFinancialFact Provenance Audit",
- L53 | symbols=raw_financial_facts |         if "raw_financial_facts" not in tables:
- L54 | symbols=raw_financial_facts |             raise SystemExit("Table raw_financial_facts does not exist.")
- L59 | symbols=raw_financial_facts |                 "PRAGMA table_info(raw_financial_facts)"
- L63 | symbols=raw_financial_facts |             "SELECT COUNT(*) FROM raw_financial_facts"
- L68 | symbols=raw_financial_facts |             f"- Total raw_financial_facts rows: **{total}**",
- L82 | symbols=raw_financial_facts |                 f"SELECT COUNT(*) FROM raw_financial_facts WHERE {qfield} IS NOT NULL"
- L85 | symbols=raw_financial_facts |                 f"SELECT COUNT(DISTINCT {qfield}) FROM raw_financial_facts "
- L96 | symbols=raw_financial_facts |                 f"SELECT DISTINCT {qfield} AS value FROM raw_financial_facts "
- L108 | symbols=raw_financial_facts |         lines.extend(["## 4. Foreign-key references to raw_financial_facts", ""])
- L118 | symbols=raw_financial_facts |                 if fk["table"] == "raw_financial_facts":
### src/scripts/audit_migration_9_column_usage.py [SCRIPT]
- L24 | symbols=raw_financial_facts |             "PRAGMA table_info(raw_financial_facts)"
- L44 | symbols=raw_financial_facts |             FROM raw_financial_facts
- L58 | symbols=raw_financial_facts |             FROM raw_financial_facts
### src/scripts/init_db.py [SCRIPT]
- L15 | symbols=RawFinancialFact |     RawFinancialFact,
### src/tests/test_codal_acquisition.py [TEST]
- L5 | symbols=src.ingestion.codal, CodalAcquisitionError, acquire_codal_pdf | from src.ingestion.codal.acquisition import CodalAcquisitionError, acquire_codal_pdf
- L12 | symbols=acquire_codal_pdf |     result = acquire_codal_pdf(str(source), destination)
- L21 | symbols=CodalAcquisitionError |     with pytest.raises(CodalAcquisitionError):
- L22 | symbols=acquire_codal_pdf |         acquire_codal_pdf(str(tmp_path / "missing.pdf"), tmp_path / "acquired.pdf", retries=0)
- L28 | symbols=CodalAcquisitionError |     with pytest.raises(CodalAcquisitionError):
- L29 | symbols=acquire_codal_pdf |         acquire_codal_pdf(str(source), tmp_path / "acquired.pdf", retries=0)
### src/tests/test_codal_digit_normalization.py [TEST]
- L3 | symbols=src.ingestion.codal, normalize_digits, parse_amount | from src.ingestion.codal.numbers import normalize_digits, parse_amount
- L6 | symbols=normalize_digits | def test_normalize_digits_maps_persian_and_arabic_indic_to_ascii():
- L7 | symbols=normalize_digits |     assert normalize_digits("۱۲۳۴۵۶۷۸۹۰ ١٢٣٤٥٦٧٨٩٠") == "1234567890 1234567890"
- L10 | symbols=parse_amount | def test_parse_amount_accepts_persian_digits_and_arabic_separators():
- L11 | symbols=parse_amount |     assert parse_amount("(۱۲۳٬۴۵۶٫۷۸۹)") == Decimal("-123456.789")
### src/tests/test_codal_extraction.py [TEST]
- L15 | symbols=src.ingestion.codal, CodalAcquisitionError, acquire_local_pdf | from src.ingestion.codal.acquisition import CodalAcquisitionError, acquire_local_pdf
- L16 | symbols=src.ingestion.codal, extract_raw_lines_from_pdf | from src.ingestion.codal.adapter import extract_raw_lines_from_pdf
- L17 | symbols=src.ingestion.codal, normalize_digits, parse_amount | from src.ingestion.codal.numbers import normalize_digits, parse_amount
- L18 | symbols=src.ingestion.codal, CodalExtractionError | from src.ingestion.codal.pdf_extract import CodalExtractionError, fix_persian_rtl
- L19 | symbols=src.ingestion.codal, load_codal_pdf | from src.ingestion.codal.pipeline import load_codal_pdf
- L20 | symbols=RawLineInput, ingest_codal_report | from src.ingestion.service import RawLineInput, ingest_codal_report
- L23 | symbols=RawFinancialFact | from src.models.normalized import RawFinancialFact
- L109 | symbols=normalize_digits |     assert normalize_digits("۱۲۳۴۵۶") == "123456"
- L110 | symbols=normalize_digits |     assert normalize_digits("٠١٢") == "012"
- L113 | symbols=parse_amount | def test_parse_amount_null_not_zero():
- L114 | symbols=parse_amount |     assert parse_amount(None) is None
- L115 | symbols=parse_amount |     assert parse_amount("") is None
- L116 | symbols=parse_amount |     assert parse_amount("-") is None
- L117 | symbols=parse_amount |     assert parse_amount("—") is None
- L118 | symbols=parse_amount |     assert parse_amount("0") == Decimal("0")
- L119 | symbols=parse_amount |     assert parse_amount("1,234") == Decimal("1234")
- L120 | symbols=parse_amount |     assert parse_amount("(1,500)") == Decimal("-1500")
- L121 | symbols=parse_amount |     assert parse_amount("۱۲۳") == Decimal("123")
- L122 | symbols=parse_amount |     assert parse_amount("not-a-number") is None
- L141 | symbols=extract_raw_lines_from_pdf |     result = extract_raw_lines_from_pdf(
- L158 | symbols=extract_raw_lines_from_pdf |     result = extract_raw_lines_from_pdf(
- L171 | symbols=CodalExtractionError |     with pytest.raises((CodalExtractionError, Exception)):
- L172 | symbols=extract_raw_lines_from_pdf |         extract_raw_lines_from_pdf(
- L185 | symbols=load_codal_pdf |     result = load_codal_pdf(
- L202 | symbols=RawFinancialFact |     facts = session.query(RawFinancialFact).filter_by(report_version_id=version.report_version_id).all()
- L211 | symbols=src.ingestion.codal, load_codal_pdf |     from src.ingestion.codal.pipeline import load_codal_pdf
- L213 | symbols=CodalAcquisitionError |     with pytest.raises(CodalAcquisitionError):
- L214 | symbols=load_codal_pdf |         load_codal_pdf(
- L229 | symbols=RawFinancialFact |     assert session.query(RawFinancialFact).count() == 0
- L233 | symbols=src.ingestion.codal, load_codal_pdf |     from src.ingestion.codal.pipeline import load_codal_pdf
- L238 | symbols=CodalExtractionError |     with pytest.raises(CodalExtractionError):
- L239 | symbols=load_codal_pdf |         load_codal_pdf(
- L254 | symbols=RawFinancialFact |     assert session.query(RawFinancialFact).count() == 0
- L259 | symbols=load_codal_pdf |     r1 = load_codal_pdf(
- L269 | symbols=load_codal_pdf |     r2 = load_codal_pdf(
- L318 | symbols=ingest_codal_report |         ingest_codal_report(
- L325 | symbols=RawLineInput |             raw_lines=[RawLineInput(item_name="unmapped source row")],
- L329 | symbols=RawFinancialFact |     assert session.query(RawFinancialFact).count() == 0
- L333 | symbols=ingest_codal_report |     first = ingest_codal_report(
- L341 | symbols=RawLineInput |         raw_lines=[RawLineInput(item_name="unmapped source row")],
- L367 | symbols=ingest_codal_report |         ingest_codal_report(
- L375 | symbols=RawLineInput |             raw_lines=[RawLineInput(item_name="unmapped source row")],
- L380 | symbols=RawFinancialFact |     assert session.query(RawFinancialFact).count() == 1
- L402 | symbols=extract_raw_lines_from_pdf |     result = extract_raw_lines_from_pdf(
### src/tests/test_codal_pdf_extraction.py [TEST]
- L9 | symbols=src.ingestion.codal, extract_raw_lines_from_pdf | from src.ingestion.codal.adapter import extract_raw_lines_from_pdf
- L10 | symbols=src.ingestion.codal, ingest_codal_pdf | from src.ingestion.codal.ingestion import ingest_codal_pdf
- L11 | symbols=src.ingestion.codal | from src.ingestion.codal.parser import (
- L17 | symbols=RawLineInput, ingest_codal_report | from src.ingestion.service import RawLineInput, ingest_codal_report
- L20 | symbols=RawFinancialFact | from src.models.normalized import RawFinancialFact
- L132 | symbols=RawLineInput |     assert all(isinstance(line, RawLineInput) for line in lines)
- L136 | symbols=src.ingestion.codal |     from src.ingestion.codal import pdf_extract
- L143 | symbols=src.ingestion.codal |     from src.ingestion.codal import pdf_extract
- L171 | symbols=extract_raw_lines_from_pdf |     result = extract_raw_lines_from_pdf(
- L180 | symbols=RawLineInput |     assert all(isinstance(line, RawLineInput) for line in result.raw_lines)
- L200 | symbols=extract_raw_lines_from_pdf |     result_a = extract_raw_lines_from_pdf(path, **kwargs)
- L201 | symbols=extract_raw_lines_from_pdf |     result_b = extract_raw_lines_from_pdf(path, **kwargs)
- L202 | symbols=extract_raw_lines_from_pdf |     result_c = extract_raw_lines_from_pdf(path, **kwargs)
- L218 | symbols=extract_raw_lines_from_pdf |     result = extract_raw_lines_from_pdf(
- L253 | symbols=src.ingestion.codal |     from src.ingestion.codal.parser import parse_numeric_token
- L271 | symbols=ingest_codal_pdf |         ingest_codal_pdf(
- L280 | symbols=RawFinancialFact |     assert session.query(RawFinancialFact).count() == 0
- L289 | symbols=extract_raw_lines_from_pdf |             result = extract_raw_lines_from_pdf(path, title=path.name, report_type="CODAL", publication_datetime=datetime(2026, 9, 1))
- L306 | symbols=ingest_codal_report |     result = ingest_codal_report(
- L315 | symbols=RawLineInput |             RawLineInput(item_name="absent amount", value=None, source_column="1"),
- L316 | symbols=RawLineInput |             RawLineInput(item_name="explicit zero", value=Decimal("0"), source_column="2"),
- L320 | symbols=RawFinancialFact |         session.query(RawFinancialFact)
- L339 | symbols=ingest_codal_report |     result = ingest_codal_report(
- L344 | symbols=RawLineInput |         raw_lines=[RawLineInput(
- L355 | symbols=RawFinancialFact |     fact = session.query(RawFinancialFact).filter_by(report_version_id=result.report_version_id).one()
- L369 | symbols=ingest_codal_pdf |         results.append(ingest_codal_pdf(
- L377 | symbols=RawFinancialFact |     assert session.query(RawFinancialFact).count() == sum(r.raw_fact_count for r in results)
- L393 | symbols=ingest_codal_pdf |     result = ingest_codal_pdf(
- L414 | symbols=RawFinancialFact, RawFinancialFact |     facts = session.query(RawFinancialFact).filter_by(report_version_id=version.report_version_id).order_by(RawFinancialFact.raw_fact_id).all()
- L451 | symbols=extract_raw_lines_from_pdf |     extraction = extract_raw_lines_from_pdf(
- L456 | symbols=ingest_codal_report |     first = ingest_codal_report(
- L462 | symbols=ingest_codal_report |     second = ingest_codal_report(
- L470 | symbols=RawFinancialFact |     assert session.query(RawFinancialFact).count() == first.raw_fact_count
- L477 | symbols=RawFinancialFact |     """Full logical-state snapshot of RawFinancialFact for drift detection.
- L483 | symbols=RawFinancialFact, RawFinancialFact |     facts = session.query(RawFinancialFact).order_by(RawFinancialFact.raw_fact_id).all()
- L506 | symbols=ingest_codal_report |     The idempotency key in ingest_codal_report() is (codal_tracking_id,
- L508 | symbols=RawFinancialFact |     must reuse the same ReportVersion and must not duplicate RawFinancialFact
- L516 | symbols=extract_raw_lines_from_pdf |     extraction = extract_raw_lines_from_pdf(
- L539 | symbols=ingest_codal_report |     first = ingest_codal_report(**ingest_kwargs)
- L548 | symbols=ingest_codal_report |     second = ingest_codal_report(**ingest_kwargs)
- L549 | symbols=ingest_codal_report |     third = ingest_codal_report(**ingest_kwargs)
- L564 | symbols=RawFinancialFact |     # No duplicate RawFinancialFact rows and no value/provenance drift.
- L583 | symbols=RawFinancialFact |     assert session.query(RawFinancialFact).count() == expected_fact_count
- L638 | symbols=ingest_codal_pdf |     result = ingest_codal_pdf(
- L680 | symbols=RawFinancialFact |         session.query(RawFinancialFact)
- L682 | symbols=RawFinancialFact |         .order_by(RawFinancialFact.raw_fact_id)
- L710 | symbols=ingest_codal_pdf |     result = ingest_codal_pdf(
- L797 | symbols=ingest_codal_pdf |     first = ingest_codal_pdf(
- L807 | symbols=ingest_codal_pdf |     second = ingest_codal_pdf(
- L853 | symbols=RawFinancialFact |         session.query(RawFinancialFact)
- L858 | symbols=RawFinancialFact |         session.query(RawFinancialFact)
- L886 | symbols=ingest_codal_pdf |     result = ingest_codal_pdf(
- L897 | symbols=RawFinancialFact |     assert session.query(RawFinancialFact).count() == result.raw_fact_count
### src/tests/test_stage1_database_architecture.py [TEST]
- L8 | symbols=RawFinancialFact | from src.models.normalized import FinancialMetric, MappingDecision, MappingRule, NormalizedFinancialFact, RawFinancialFact
- L69 | symbols=RawFinancialFact |     raw_a = RawFinancialFact(
- L76 | symbols=RawFinancialFact |     raw_b = RawFinancialFact(
### src/tests/test_stage1_database_integrity.py [TEST]
- L21 | symbols=RawFinancialFact |     RawFinancialFact,
- L65 | symbols=raw_financial_facts |         connection.execute(text("INSERT INTO raw_financial_facts (company_id, report_version_id, period_id, raw_item_name) VALUES (1, 1, 1, 'preserve-me')"))
- L81 | symbols=raw_financial_facts |         assert connection.execute(text("SELECT raw_item_name FROM raw_financial_facts")).scalar_one() == "preserve-me"
### src/tests/test_stage1_rules.py [TEST]
- L11 | symbols=RawLineInput, ingest_codal_report | from src.ingestion.service import RawLineInput, ingest_codal_report
- L23 | symbols=RawFinancialFact |     RawFinancialFact,
- L76 | symbols=raw_financial_facts |         "raw_financial_facts", "financial_metrics", "mapping_rules", "mapping_decisions",
- L94 | symbols=RawFinancialFact |     raw = RawFinancialFact(
- L101 | symbols=RawFinancialFact |     saved = db_session.get(RawFinancialFact, raw.raw_fact_id)
### src/tests/test_stage5_forecast.py [TEST]
- L812 | symbols=RawFinancialFact |     RawFinancialFact,
- L1209 | symbols=RawFinancialFact |                 for row in production_db.query(RawFinancialFact).all()
