# DB-ING-003 — Excel adapter readiness increment

**Task:** 016  
**Status:** PARTIAL  
**Date:** 2026-11-20

## Scope and architecture

Added `src/ingestion/excel/adapter.py` as a narrow orchestration boundary over the existing Reader, `TemplateVersion`/`match_template`, candidate builder, and canonical admission functions. It introduces no competing observation or candidate DTO and performs no persistence, transaction, commit, archive, or logging operation.

The caller supplies an XLSX bytes/path source, an explicit versioned template, a complete coordinate-to-`CanonicalInputSpec` mapping for observed cells in template-owned extraction ranges, optional coordinate-bound ZERO_FALLBACK rules, optional expected artifact hash, and optionally an explicit revision context. The adapter:

1. Reads using `read_excel_source()` and returns reader contract/read failures as stable code-only diagnostics.
2. Runs the real deterministic matcher and stops unless it returns exact `MATCHED`; unapproved templates, source/worksheet mismatches, and structural failures cannot proceed.
3. Checks the optional expected source SHA-256 and retains the exact observed fingerprint, worksheet, coordinate, literal-value kind/text and the full `WorkbookObservation` plus match table/header coordinate context in the result.
4. Builds only the caller-selected coordinates. Each observed cell inside an owned extraction range without a selection rejects the complete unit. Selections outside owned ranges, duplicate/invalid coordinates, ambiguous owners, missing approvals, and invalid semantic/temporal specifications also reject the complete unit. There is no semantic inference, fuzzy match, positional metric selection, or silent omission.
5. Uses `build_candidate_submission()` for source values and explicit fallback rules. BLANK, actual reported zero, and approved ZERO_FALLBACK remain distinct; formula/error cells retain the Reader's rejection behavior.
6. Returns candidate submissions without admission by default. It calls `prepare_canonical_batch()` only when `admit=True` and a caller-supplied `RevisionContext` is present. Any builder or admission diagnostic yields an empty submission result, so no partial batch escapes.

Diagnostics are immutable records sorted/deduplicated by code, worksheet, coordinate, and identity. They contain no cell values or financial payloads. The returned `observation` intentionally retains source literals for the caller; the adapter itself does not log them.

## API and stable diagnostic families

Public entry point: `adapt_excel_source(...) -> ExcelAdapterResult`. Results retain the observation, match result, complete submissions (only on full success), optional non-executable admission plan, deterministic diagnostics, and an `accepted` flag.

Adapter-level codes include source/template/selection input failures; expected or matcher source-hash mismatch; coordinate and ownership ambiguity; `IN_SCOPE_SELECTION_MISSING`; `SELECTION_OUTSIDE_OWNED_RANGE`; missing fallback/OTHER approval association; `CANDIDATES_EMPTY`; `REVISION_CONTEXT_REQUIRED`; and `CANDIDATE_BUILD_INPUT_INVALID`. Reader and matcher codes are passed through as codes and coordinates. Existing `CandidateValidationError` and `AdmissionRejected` codes are preserved. Diagnostics never include source text or numeric values.

## Synthetic coverage and owner commands

Added `src/tests/test_excel_adapter.py` for valid read → approved match → explicit candidate build; optional admission; unapproved template; worksheet and expected-source-hash mismatch; missing/ambiguous semantics and temporal selection; exact source/template/worksheet/coordinate/header provenance; formula rejection; blank without fallback; approved ZERO_FALLBACK; actual zero; unknown in-scope data; whole-unit rejection; and deterministic diagnostic ordering.

Tests were **not run**, as PROMPT.md assigns them to the owner. Adapter/regression command for owner execution:

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_task016_20261120 src/tests/test_excel_adapter.py src/tests/test_excel_canonical_input.py src/tests/test_excel_template_matching.py src/tests/test_canonical_ingestion_admission.py
```

Separate prior owner acceptance recorded for the Task 014/015 focused suite (it does not cover this new adapter):

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_task015_20261120 src/tests/test_canonical_ingestion_admission.py src/tests/test_excel_canonical_input.py
```

Owner-reported result: **36 passed in 1.61s**. This is owner-run evidence for the existing Task 014/015 boundaries, not a test run by the agent and not adapter acceptance.

## Limitations and remaining work

No approved production company template, authenticated real semantic mapping catalog, authoritative temporal mapping set, or representative real-workbook end-to-end validation is available. The tests use synthetic in-memory XLSX fixtures and do not establish Parsian or other company-template correctness. Task 015 still lacks an approved compatible physical schema and a production writer implementing DB-DES-005 atomicity. No production ingestion is authorized or connected by this adapter.

Task 014 remains **PARTIAL** (locale parser and authoritative production approval/template resolution remain open). Task 015 remains **PARTIAL** (physical schema/model alignment and atomic writer remain open). Task 016 is **PARTIAL**: the reusable orchestration boundary and synthetic tests are added, while approved production templates/mappings and real workbook validation remain outstanding.

## Exact files changed for this Task 016 increment

- `src/ingestion/excel/adapter.py`
- `src/tests/test_excel_adapter.py`
- `database/reports/DB_ING_003_EXCEL_ADAPTER_READINESS.md`
- `database/DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md`
- `reply.md`

No Reader, Matcher, Candidate, Admission, ORM, schema, migration, database, workbook, or `WORKFLOW_RULES.md` changes were made for Task 016.
