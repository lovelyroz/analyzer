# TASK 016 — DB-ING-003: Excel Adapter Readiness
**Type: CODE IMPLEMENTATION + DOCUMENTATION**

Repository: `analyzer`  
Branch: `master`

## Objective

Implement the next executable increment of the Excel-to-canonical ingestion adapter.

The existing components are:
- `src/ingestion/excel/reader.py`
- `src/ingestion/excel/dto.py`
- `src/ingestion/excel/deterministic_matcher.py`
- `src/ingestion/excel/canonical_input.py`
- `src/ingestion/canonical_admission.py`

Read their actual current implementations before changing anything. Reuse these contracts; do not create competing DTOs or duplicate validation logic.

## A. Implement the adapter boundary

Create a focused Excel adapter that connects the existing components:

1. Read an XLSX source through `read_excel_source()`.
2. Accept an explicitly supplied, versioned `TemplateVersion`.
3. Run `match_template()` and reject any result other than an exact approved `MATCHED` result.
4. Preserve source workbook fingerprint, worksheet identity, exact cell coordinates, literal values and relevant table/header context.
5. Accept explicit, caller-supplied semantic and temporal selections for candidate construction. Never infer Metric, dimensions, unit, currency, scale, Jalali period or YTD/standalone from position or text similarity alone.
6. Build candidates through the existing `build_candidate()` / `build_candidate_submission()` APIs.
7. Pass the resulting submissions to the existing canonical admission boundary only when the caller explicitly requests admission.
8. Return structured, deterministic diagnostics for failures. Do not log complete financial payloads.

Keep the adapter pure with respect to persistence: no database session, ORM writes, transactions, commits or file archiving.

## B. Fail-closed requirements

- Unapproved, missing, ambiguous or structurally mismatched templates must stop processing.
- Unknown or ambiguous in-scope observations must not be silently skipped.
- Do not invent mappings or use fuzzy matching.
- Do not treat every populated cell as a financial fact.
- Do not derive a financial period from workbook name, publication date or column order.
- Preserve BLANK, actual zero and approved ZERO_FALLBACK as distinct states.
- Formula cells remain prohibited under the approved Reader contract.
- Do not introduce a new numeric parser or locale policy in this Task. Use only currently supported candidate construction behavior.
- Do not use the unapproved Parsian candidate register as a production template.

## C. Tests

Add focused synthetic end-to-end tests for:
- valid read → approved template match → explicit candidate construction;
- rejected/unapproved template;
- source hash or worksheet mismatch;
- missing/ambiguous semantic or temporal selection;
- preservation of exact source coordinates and template provenance;
- blank versus actual zero versus approved ZERO_FALLBACK;
- deterministic diagnostics and whole-unit rejection.

Use synthetic fixtures only where no approved real template exists. Do not claim production workbook coverage or semantic correctness based on synthetic tests.

Do not run tests. The owner runs them.

## D. Explicit exclusions

- No ORM, schema, migration or database changes.
- No real database access or real ingestion.
- No activation of any unapproved company template.
- No PDF extraction or PDF retirement work.
- No changes to `WORKFLOW_RULES.md`.
- No unrelated refactoring or reopening completed tasks.
- Do not weaken existing Reader, Matcher, Candidate or Admission validation to make integration pass.

## E. Record the latest owner test acceptance

The owner has now run:

`.\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_task015_20261120 src/tests/test_canonical_ingestion_admission.py src/tests/test_excel_canonical_input.py`

Result: **36 passed in 1.61s**.

Record this exact owner-run evidence in `reply.md`, the relevant Task 014/015 evidence sections, and the Master Packet. Do not mark either Task DONE solely because of this test result.

## F. Required deliverables

1. New adapter implementation and focused tests.
2. A report describing architecture, API, fail-closed behavior, diagnostics and limitations.
3. Exact changed-file list.
4. Exact owner test command.
5. Update `reply.md` and Master Packet.
6. Recalculate the dashboard if Task 016 status changes.

Task 016 must remain PARTIAL if approved production templates, real semantic mappings, temporal mappings or representative real-workbook end-to-end validation are still missing.

Report each affected Task ID with DONE / PARTIAL / NOT DONE and evidence. Do not claim tests were run by the agent.