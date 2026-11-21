# Task DB-CODAL-RETIRE-001 — Retire PDF Extraction Completely; Establish Excel/CSV-Only Input

## Objective

The owner has explicitly decided that all extractable input files for this application are Excel workbooks or CSV files.

PDF extraction was never intended to be part of the target application workflow. It must not remain as an active, supported, planned, or acceptance-required ingestion path.

Retire the CODAL PDF acquisition/extraction implementation and reconcile all active project documentation with the Excel/CSV-only architecture.

This is an implementation task, not another audit-only task.

## 1. Binding architectural decision

The supported file-input formats are:

- Excel workbooks
- CSV files

PDF is NOT a supported ingestion format.

This applies to:
- CODAL financial reports
- Market data
- FX data
- Future file-based ingestion unless a separate explicit owner decision changes this contract.

Do not build PDF fallback, OCR, PDF-to-Excel conversion, or PDF compatibility paths.

Excel and CSV adapters must remain independent of PDF-specific code and dependencies.

## 2. Production source retirement

Inspect all callers and imports before editing.

Retire PDF-only modules and entry points, including:

- `src/ingestion/codal/acquisition.py`
- `src/ingestion/codal/adapter.py`
- `src/ingestion/codal/pdf_extract.py`
- PDF-specific functionality in `src/ingestion/codal/parser.py`
- PDF acquisition/extraction functions in `src/ingestion/codal/pipeline.py`
- `ingest_codal_pdf` in `src/ingestion/codal/ingestion.py`
- PDF exports in `src/ingestion/codal/__init__.py`

Delete PDF-only modules when no supported caller remains.

Remove PDF-only imports and public exports. No production module may import `pypdf`, `pdfplumber`, PDF acquisition helpers, or PDF extraction adapters.

Do not retain dead compatibility wrappers that still expose PDF ingestion.

### Important shared-code boundary

Do NOT blindly delete:
- `src/ingestion/service.py`
- `src/models/normalized.py`
- `RawFinancialFact`
- `Report` / `ReportVersion`
- database migrations
- legacy database tables or records.

These may contain contracts or persistence behavior beyond PDF extraction.

Preserve shared functionality only where there is an identified current consumer or explicit database compatibility requirement. Clearly report remaining legacy-only code and why it remains.

Do not implement a new Excel ORM writer in this task unless it already exists and only requires connection/refactoring. Do not invent a persistence contract.

## 3. Tests and fixtures

Remove PDF-only test coverage and PDF-specific test fixtures.

Review:
- `src/tests/test_codal_pdf_extraction.py`
- `src/tests/test_codal_extraction.py`
- `src/tests/test_codal_acquisition.py`
- `src/tests/codal_19_pdf_validation_plan.md`
- `src/tests/codal_19_pdf_validation_matrix.md`

Do not simply delete all CODAL tests.

Preserve and relocate any assertions that test independent, still-required contracts, including:
- Report and ReportVersion identity
- version chain and replay behavior
- atomicity and rollback
- persistence constraints that remain supported
- source provenance contracts that remain valid
- numeric normalization that is format-independent
- NULL versus explicit zero
- failure handling unrelated to PDF

Use Excel/CSV fixtures for file-format-specific tests.

Remove PDF corpus tests and references from active test commands.

Do not weaken or remove unrelated assertions merely to make the suite pass.

## 4. Dependency and repository cleanup

- Remove `pypdf` from `requirements.txt` if no other supported feature uses it.
- Check all dependency manifests and optional dependency declarations for PDF libraries.
- Remove the PDF sample corpus directory if it has no remaining legitimate use.
- Remove obsolete PDF-only validation scripts and plans when their purpose is fully retired.
- Do not remove historical audit reports that explain prior decisions; mark them as historical/superseded instead.

## 5. Documentation reconciliation

Update the active documents:

1. `10_Production_Codal_Extraction_and_Data_Load.md`
   - Replace the obsolete PDF-oriented design with the supported Excel/CSV ingestion architecture.
2. `database/reports/DB_PLAN_013_PDF_PATH_RETIREMENT_SEQUENCE.md`
   - Mark the staged retirement plan superseded.
   - Its condition that PDF must remain until Excel production persistence is ready is no longer valid.
3. `database/reports/DB_AUD_012_CODAL_PDF_PATH_DEPENDENCY_AUDIT.md`
   - Preserve historical findings.
   - Add a clear final status and references to the completed retirement.
4. `database/reports/DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md`
   - Reconcile stale descriptions of PDF as the active path.
5. `database/reports/DB_DES_006_CODAL_CANONICAL_INGESTION_PIPELINE.md`
   - Explicitly state Excel/CSV-only input and PDF exclusion.
6. `CODAL_EXCEL_PREPROCESSING_MASTER_WORKING_PACKET.md`
   - Align with the final input-format contract.
7. `database/DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md`
   - Record this task, changed files, acceptance evidence, and final status.
   - Remove contradictions between the owner decision and active implementation plans.

Preserve historical audit evidence. Do not rewrite historical findings as if PDF extraction never existed.

`WORKFLOW_RULES.md` is owner-controlled and MUST NOT be modified.

## 6. Required repository-wide verification

Perform a repository-wide scan for:
- `pdf`
- `.pdf`
- `pypdf`
- `pdfplumber`
- `fitz`
- `extract_raw_lines_from_pdf`
- `load_codal_pdf`
- `ingest_codal_pdf`
- `acquire_pdf_from_url`
- `acquire_local_pdf`

Classify every remaining match as:
A. Active production code — must be zero.
B. Active tests/fixtures/commands — must be zero for PDF extraction.
C. Historical documentation — permitted only when clearly marked historical/superseded.
D. Unrelated legitimate PDF support — must be explicitly explained.

Do not claim completion based only on a text search. Inspect imports, public exports, call sites, test discovery, and dependency manifests.

## 7. Safety constraints

- Do not modify ORM models or database schema.
- Do not create or alter migrations.
- Do not open, mutate, or migrate the real database.
- Do not delete legacy financial records or tables.
- Do not change `WORKFLOW_RULES.md`.
- Do not run tests; the owner runs tests locally.
- Do not commit or push unless separately instructed.

## 8. Deliverables

Create:
`database/reports/DB_CODAL_RETIRE_001_EXCEL_CSV_ONLY_RETIREMENT.md`

The report must contain:
- Before/after architecture
- Exact deleted files
- Exact modified files
- Retained legacy components and justification
- Dependency cleanup
- Test relocation/removal details
- Remaining PDF references classified by category
- Full list of repository-wide search terms and findings
- Risks or unresolved issues
- Exact owner-run test command

Update `reply.md` and the Database Master Working Packet.

## 9. Acceptance criteria

The task is not DONE unless all of the following hold:

1. No active production PDF acquisition/extraction path remains.
2. No active CODAL PDF ingestion API or public export remains.
3. No PDF-only test is included in active acceptance suites.
4. Required non-PDF legacy contract tests remain covered.
5. No unnecessary PDF extraction dependency remains.
6. Excel/CSV ingestion code does not depend on PDF modules.
7. Active documentation consistently describes Excel/CSV-only input.
8. Historical PDF audits are clearly marked historical/superseded.
9. No ORM/schema/migration/database changes occurred.
10. Owner-run tests pass.

If Excel/CSV end-to-end persistence is not yet implemented, report that separately as an open implementation task. It is NOT a reason to retain PDF extraction.

Do not mark DONE before owner test results are supplied and verified.