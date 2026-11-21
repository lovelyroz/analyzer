# DB-CODAL-RETIRE-001 — Excel/CSV-only input and CODAL PDF retirement

**Date:** 2026-11-21  
**Status:** PARTIAL — implementation and static verification complete; owner-run tests and acceptance pending.

## Decision and architecture before/after

The owner decision is that supported file inputs are Excel workbooks and CSV. PDF is not a supported input for CODAL, market, FX, or future file ingestion absent a separate explicit decision.

Before this change, CODAL had local/URL PDF acquisition, PDF text/table extraction, a PDF-to-`RawLineInput` adapter, raw-line validation and a loader pipeline. The package exported PDF acquisition/extraction functions and `ingest_codal_pdf`; `pypdf` and an in-repository PDF sample corpus supported the path.

After this change, active file readers are Excel and CSV adapters. Excel reading, observation DTOs, template matching and canonical admission remain in `src/ingestion/excel/`; canonical admission still yields a non-executable plan. CSV market/FX adapters retain their current persistence. `src/ingestion/service.py` and the CODAL facade retain format-neutral persistence for already parsed `RawLineInput` rows. This preserves legacy Report/ReportVersion/RawFinancialFact identity, replay, version history, audit and provenance behavior without making it a PDF input path. No Excel ORM writer was added; Excel-to-canonical persistence remains a separate open implementation task.

## Exact deleted files and corpus

Deleted PDF-only production files:

- `src/ingestion/codal/acquisition.py`
- `src/ingestion/codal/adapter.py`
- `src/ingestion/codal/pdf_extract.py`
- `src/ingestion/codal/parser.py`
- `src/ingestion/codal/pipeline.py`
- `src/ingestion/codal/validator.py` (only called by the retired PDF pipeline)
- `src/scripts/audit_codal_pdf_dependencies.py`

Deleted PDF-only tests/plans:

- `src/tests/test_codal_acquisition.py`
- `src/tests/test_codal_pdf_extraction.py`
- `src/tests/codal_19_pdf_validation_plan.md`
- `src/tests/codal_19_pdf_validation_matrix.md`

Deleted corpus directories `pdf/` and `pdf_test/`. The tracked CODAL sample set contained `Fzar.pdf` and these 19 SEO files: `seo-codal-report (1).pdf`, `(2).pdf`, `(3).pdf`, `(4).pdf`, `(6).pdf`, `(7).pdf`, `(8).pdf`, `(9).pdf`, `(10).pdf`, `(11).pdf`, `(12).pdf`, `(13).pdf`, `(14).pdf`, `(15).pdf`, `(16).pdf`, `(19).pdf`, `(20).pdf`, `(25).pdf`, and `(26).pdf`. The former directory also contained `extraction_test/Fzar_pdfium_comparison.txt`, `Fzar_pdfium_normalized.txt`, and `Fzar_pdfium_raw.txt`. `pdf_test/` contained a duplicate `Fzar.pdf`, `Fzar_page1_full_structured.json`, and `Fzar_table_sample.json`. These were all local extraction artifacts, not supported Excel/CSV fixtures.

## Exact modified files

Production code and dependency:

- `src/ingestion/codal/ingestion.py` — retained only `ingest_codal_report`; removed PDF loader and imports.
- `src/ingestion/codal/__init__.py` — retained only the shared persistence facade as a public export.
- `src/ingestion/codal/numbers.py` — retained digit normalization; removed PDF-only amount parsing. The digit map now uses actual Persian and Arabic-Indic Unicode digits.
- `src/ingestion/service.py` — kept persistence unchanged and removed PDF-specific contract language.
- `src/ingestion/__init__.py` — corrected the package description to describe parsed-row persistence.
- `requirements.txt` — removed `pypdf`. Repository manifest scan found no other PDF extraction dependency declaration.

Tests:

- `src/tests/test_codal_extraction.py` — replaced mixed PDF extraction/pipeline cases with six synthetic parsed-row persistence tests.
- `src/tests/test_codal_digit_normalization.py` — retained format-independent Persian/Arabic-Indic digit normalization coverage.

Current architecture and task records:

- `10_Production_Codal_Extraction_and_Data_Load.md`
- `11_Production_Data_Load_and_Foundation_Validation.md` (marked superseded/historical)
- `roadMap.md` (marked superseded/historical)
- `PROJECT_HANDOFF_INSTRUCTIONS.md`
- `CODAL_EXCEL_PREPROCESSING_MASTER_WORKING_PACKET.md`
- `database/DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md`
- `database/README.md`
- `database/reports/DB_AUD_003_004_ENTITY_REPORT_PIT_AUDIT_2026-11-19.md`
- `database/reports/DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md`
- `database/reports/DB_AUD_008_EXCEL_LIBRARY_CAPABILITY_ASSESSMENT.md`
- `database/reports/DB_AUD_011_LEGACY_RAW_FACT_PROVENANCE_DECISION.md`
- `database/reports/DB_AUD_011_MARKET_FX_SOURCE_PROVENANCE_DOSSIER.md`
- `database/reports/DB_AUD_012_CODAL_PDF_PATH_DEPENDENCY_AUDIT.md`
- `database/reports/DB_AUD_013_EXCEL_CANONICAL_PERSISTENCE_READINESS.md`
- `database/reports/DB_AUD_014_NORMALIZED_DERIVED_FACT_CONSUMER_AUDIT.md`
- `database/reports/DB_AUD_016_TEMPORAL_CONTRACT_RECONCILIATION.md`
- `database/reports/DB_DES_005_INGESTION_ATOMICITY_CONTRACT.md`
- `database/reports/DB_DES_006_CODAL_CANONICAL_INGESTION_PIPELINE.md`
- `database/reports/DB_DES_007_EXCEL_SOURCE_OBSERVATION_DTO_CONTRACT.md`
- `database/reports/DB_DES_007_PYTHON_DTO_DESIGN.md`
- `database/reports/DB_DES_009_CANONICAL_FINANCIAL_FACT_PHYSICAL_MODEL.md`
- `database/reports/DB_DES_011_FINANCIAL_PERIOD_TEMPORAL_BASIS_CONTRACT.md`
- `database/reports/DB_DES_012_COMPANY_FISCAL_YEAR_LOGICAL_MODEL.md`
- `database/reports/DB_ING_006_VISUAL_TABLE_REGION_DETECTION.md`
- `database/reports/DB_PLAN_013_PDF_PATH_RETIREMENT_SEQUENCE.md` (marked superseded)
- `database/reports/DB_STD_004_INPUT_SELECTION_AND_FRONTEND_ADMISSION_CONTRACT.md`
- `database/reports/DB_STD_005_AND_DB_AUD_001_MARKET_FX_EVIDENCE_REVIEW.md`
- `database/reports/DB_TEST_002_INGESTION_PIT_TESTS.md`
- `database/reports/market_fx_source_evidence.json` (historical source inventory wording clarified)
- `database/reports/BANK_MASTER_STANDARD_WORKING_CHECKLIST.md`
- `database/reports/BANK_SAMAN_MONTHLY_STANDARD_WORKING_CHECKLIST.md`
- `prompts/10_Implementation_Status.md` (marked historical)
- `src/tests/codal_report_identity_review.md`
- `src/tests/final_validation_audit.md`
- `src/tests/golden_audit_blocked_spec.md`
- `src/tests/golden_audit_source_plan.md`
- `src/tests/golden_dataset_schema.md`
- `src/tests/golden_source_verification_report.md`
- `STAGE7_COMPLETED_CHECKLIST.md`
- `STAGE7_HANDOFF_INSTRUCTION.md`
- `STAGE7_MASTER_WORKING_PACKET.md`
- `temp_report2.md`
- `zErrors.md`
- `reply.md`
- `database/reports/DB_CODAL_RETIRE_001_EXCEL_CSV_ONLY_RETIREMENT.md` (this report)

The existing workspace edit to `prompt.md` was present before this task and was preserved. `WORKFLOW_RULES.md` was not modified.

## Retained legacy components and reason

`src/ingestion/service.py`, `RawLineInput`, `RawFinancialFact`, `Report`, `ReportVersion`, `IngestionRun`, models, migrations, and legacy database tables remain unchanged. They support shared persistence and compatibility contracts beyond file extraction. The CODAL persistence facade remains useful to direct callers that provide parsed rows; it does not accept a file path. `normalize_digits()` remains because persistence normalizes numeric characters in CODAL metadata and raw text fields. `parse_amount()` was removed because its only consumer was the retired PDF adapter.

## Dependency and test disposition

`pypdf` was removed from `requirements.txt`. Static searches found no active production import of `pypdf`, `pdfplumber`, `fitz`, or PDF helpers. Excel and CSV adapters have no dependency on the deleted CODAL package modules.

PDF extraction, acquisition, malformed-file, corpus determinism, and PDF-specific parser tests were removed. Independent persistence assertions were retained or rebuilt in `test_codal_extraction.py` using synthetic `RawLineInput` data: Report identity and version chain, replay, PIT cutoff selection, source provenance, digit normalization, NULL versus explicit zero, cross-company/period rejection, transaction rollback, and FAILED audit recording. No test was run by this agent, as required by `PROMPT.md`.

## Repository-wide search and remaining reference classification

Scanned the repository for every requested term: `pdf`, `.pdf`, `pypdf`, `pdfplumber`, `fitz`, `extract_raw_lines_from_pdf`, `load_codal_pdf`, `ingest_codal_pdf`, `acquire_pdf_from_url`, and `acquire_local_pdf`. Binary files were not text-searched. Ripgrep reported access denied for the pre-existing generated `.pytest_task017_20261120/` and `.pytest_task018_20261121/` directories; active source and tracked documentation were scanned, while those protected test-output folders were not inspected. The `pdf/` and `pdf_test/` inventories were inspected before removal. The following applies to the final source state:

- **A — active production code: zero matches.** No production acquisition/extraction module, import, call site, or public API remains. Shared `service.py` contains no PDF-specific reference. The Excel/CSV adapter trees do not import the retired CODAL modules.
- **B — active tests, fixtures, and commands for PDF extraction: zero.** The PDF suites, corpus, plans and script were removed. Active owner commands in this report, `DB_TEST_002`, `reply.md`, and Master §9.40 include only retained Excel/CSV, parsed-row persistence, market/FX and PIT tests. Exact old test command text survives only inside clearly marked historical audit/error records listed below.
- **C — historical/superseded records:** `11_Production_Data_Load_and_Foundation_Validation.md`, `roadMap.md`, `prompts/10_Implementation_Status.md`, `99_Architecture_Change_Log.md`, `12_Database_Architecture_V1.1.md`, `PROJECT_HANDOFF_INSTRUCTIONS.md`, `database/DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md`, `database/README.md`, `reply.md`, `zErrors.md`, `temp_report2.md`, `STAGE7_COMPLETED_CHECKLIST.md`, `STAGE7_HANDOFF_INSTRUCTION.md`, `STAGE7_MASTER_WORKING_PACKET.md`; `database/reports/DB_AUD_003_004_ENTITY_REPORT_PIT_AUDIT_2026-11-19.md`, `DB_AUD_006_CODAL_PIPELINE_IMPLEMENTATION_READINESS_AUDIT.md`, `DB_AUD_011_LEGACY_RAW_FACT_PROVENANCE_DECISION.md`, `DB_AUD_012_CODAL_PDF_PATH_DEPENDENCY_AUDIT.md`, `DB_AUD_014_NORMALIZED_DERIVED_FACT_CONSUMER_AUDIT.md`, `DB_AUD_016_TEMPORAL_CONTRACT_RECONCILIATION.md`, `DB_DES_005_INGESTION_ATOMICITY_CONTRACT.md`, `DB_DES_009_CANONICAL_FINANCIAL_FACT_PHYSICAL_MODEL.md`, `DB_PLAN_013_PDF_PATH_RETIREMENT_SEQUENCE.md`, `DB_STD_005_AND_DB_AUD_001_MARKET_FX_EVIDENCE_REVIEW.md`, and `DB_TEST_002_INGESTION_PIT_TESTS.md`; `src/tests/codal_report_identity_manifest.md`, `codal_report_identity_review.md`, `final_validation_audit.md`, `golden_audit_blocked_spec.md`, `golden_audit_source_plan.md`, `golden_dataset_schema.md`, and `golden_source_verification_report.md`. Their pre-retirement findings and commands are historical; superseded/retirement notices were added where the old status could be mistaken for current policy. `DB_PLAN_013` no longer gates retirement.
- **D — unrelated legitimate references:** `database/reports/postbank_periodic_report_1.md` recommends a human reviewer compare an Excel worksheet against an original filing/PDF; it is manual source verification and no application PDF reader is involved. Excel-library, DTO, architecture and bank-standard documents that say PDF is excluded describe the current format boundary, not an ingestion capability. `database/reports/market_fx_source_evidence.json` is labeled historical source evidence. `PROMPT.md` is the preserved task specification; its retired symbol names define cleanup scope, not an active API, test, or command.

The complete path inventory from the text scan, including policy and historical files, also includes `10_Production_Codal_Extraction_and_Data_Load.md`, `CODAL_EXCEL_PREPROCESSING_MASTER_WORKING_PACKET.md`, `database/reports/DB_AUD_008_EXCEL_LIBRARY_CAPABILITY_ASSESSMENT.md`, `DB_AUD_011_MARKET_FX_SOURCE_PROVENANCE_DOSSIER.md`, `DB_AUD_013_EXCEL_CANONICAL_PERSISTENCE_READINESS.md`, `DB_DES_006_CODAL_CANONICAL_INGESTION_PIPELINE.md`, `DB_DES_007_EXCEL_SOURCE_OBSERVATION_DTO_CONTRACT.md`, `DB_DES_007_PYTHON_DTO_DESIGN.md`, `DB_DES_011_FINANCIAL_PERIOD_TEMPORAL_BASIS_CONTRACT.md`, `DB_DES_012_COMPANY_FISCAL_YEAR_LOGICAL_MODEL.md`, `DB_ING_006_VISUAL_TABLE_REGION_DETECTION.md`, `DB_STD_004_INPUT_SELECTION_AND_FRONTEND_ADMISSION_CONTRACT.md`, `BANK_MASTER_STANDARD_WORKING_CHECKLIST.md`, `BANK_SAMAN_MONTHLY_STANDARD_WORKING_CHECKLIST.md`, and `src/ingestion/__init__.py`. These state the current exclusion policy, preserve prior architectural evidence, or document unrelated manual source verification; they contain no active PDF code or test command.

## Risks and open issues

The owner must run the command below and provide the result before this task can be marked DONE. No tests were run here. Excel-to-canonical ORM persistence and approved production mappings remain open separately; their absence is not a reason to restore PDF. Historical audit records preserve prior evidence and are labeled as such. No ORM model, schema, migration, real database, or financial record was changed.

## Exact owner-run test command

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_codal_retire_001_20261121 src/tests/test_codal_extraction.py src/tests/test_codal_digit_normalization.py src/tests/test_excel_adapter.py src/tests/test_excel_canonical_input.py src/tests/test_excel_template_matching.py src/tests/test_excel_source_reader.py src/tests/test_excel_observation_dto.py src/tests/test_canonical_ingestion_admission.py src/tests/test_market_fx_atomic_ingestion.py src/tests/test_stage6_p25_selection.py src/tests/test_stage6_p25_adversarial.py src/tests/test_stage6_evaluation_foundation.py
```

**Acceptance state:** static retirement criteria A–D were reviewed. Owner-run test results have not been supplied; therefore final status remains **PARTIAL**, not DONE.
