# EXECUTION PROMPT — DB-CONSOLIDATION-002
## Multi-task implementation: Excel ingestion, canonical DB, approval infrastructure, and downstream readiness

**Repository:** `analyzer`  
**Branch:** `master`  
**Priority:** EXECUTION — implement and close as many tasks as technically possible in this run.  
**Code changes:** REQUIRED.  
**Tests:** Add/update tests, but DO NOT execute pytest or other test suites. The owner runs tests locally.

---

## 1. Mission

Continue from the current repository state. Do not restart previous work, repeat completed audits, or produce another report-only assessment.

The owner has now accepted the DB-IMPL-001 focused test suite:

- 93 tests passed in the full run.
- The remaining failed test was corrected.
- Its isolated rerun passed: `1 passed in 1.11s`.
- Therefore, the focused DB-IMPL-001 test set has 94 successful tests and zero known failures.

Your job is to convert the remaining PARTIAL tasks into DONE wherever the implementation and evidence genuinely permit it.

Work across the following related tasks in one coherent implementation:

1. DB-IMPL-001 — canonical database, migration, and Excel writer.
2. DB-ING-002 / DB-ING-003 — canonical admission, deterministic Excel mapping, and adapter readiness.
3. DB-TEST-002 / DB-TEST-003 — integration and downstream contract coverage.
4. DB-EXIT-001 — database configuration exit readiness.
5. DB-ING-007 / DB-ING-008 — Market/FX schema and atomic ingestion limitations, where they can be resolved safely as part of the schema work.

Do not spend this run merely reviewing these tasks. Implement concrete changes.

## 2. Mandatory owner decisions and constraints

These decisions are final. Do not reopen them or implement alternatives:

- Current financial-report standardization scope is **BANK only**. Do not invent templates, metrics, or report rules for other industries.
- Supported financial source files are Excel and CSV only. Do not reintroduce PDF extraction or PDF dependencies.
- BANK periodic financial reports use cumulative YTD values for 3, 6, 9, and 12 months from the company's actual fiscal-year start.
- Standalone-quarter values required by the frontend are runtime calculations from compatible cumulative values. Do not presume they are separately reported source facts and do not persist calculated quarter values.
- MONTHLY_ACTIVITY is a separate report type. Do not impose periodic-report temporal rules on it.
- Jalali dates are authoritative for financial-period identity, storage, validation, and comparison. Gregorian conversion must not become the primary identity or comparison mechanism.
- Only `fiscal_year_start_month` is collected. The fiscal year starts on day 1 of that explicitly configured Jalali month. Do not add a fiscal-start-day field.
- Each company belongs to exactly one industry. Do not add sub-industries or subsidiary handling.
- Listed-company tickers are unique. `codal_symbol` is the approved unique ticker identity.
- FREE_MARKET and EXCHANGE_CENTER FX workbooks share one file structure and parser:
  - EXCHANGE_CENTER values are Rial/USD.
  - FREE_MARKET values are Toman/USD and must be multiplied by 10 to produce canonical Rial/USD.
  - Use the sell column only.
- MarketDaily CSV mapping:
  - `J-Date` = Jalali date.
  - `Ticker` = unique listed ticker; use as `codal_symbol` when present and consistent.
  - `Close` = Rial/share.
  - `Volume` = shares.
  - `No` = transaction count.
  - `Value` = source-provided traded value in Rial; preserve independently. Never derive it from `Volume × Close`.
  - Exclude `Final`, `Open`, `High`, and `Low`.
- Persist input facts only. Do not persist derived/calculated financial values or analysis/decision outputs.
- Frontend-entered data does not require external source provenance, URL, API, or download manifest.
- Preserve all report versions and their provenance. Apply the approved version/PIT selection policy; do not delete prior versions.
- Do not edit `WORKFLOW_RULES.md`.
- Never run migrations against an actual user database, never modify or delete real user data, and never reset a database.
- The owner runs tests. You must not run tests.

## 3. First: establish the exact starting point

Read these files before implementation:

- `database/DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md`
- `database/reports/DB_IMPL_001_CANONICAL_DATABASE_AND_EXCEL_WRITER.md`
- `database/reports/DB_EXIT_001_FINAL_ASSESSMENT.md`
- `12_Database_Architecture_V1.1.md`
- `src/models/canonical.py`
- `src/ingestion/canonical_writer.py`
- `src/ingestion/canonical_admission.py`
- `src/migrations/runner.py`
- `src/forecast/canonical_queries.py`

Also inspect the exact current implementations and tests for the related Market/FX adapters, template matching, canonical input, and Stage 5/6 consumers.

Use the existing reports and Master Packet as the task baseline. Do not repeat their completed work.

The latest owner test results are accepted evidence. Do not revert or rewrite the recent test fixes.

## 4. Workstream A — Approval catalog and deterministic semantic resolution

**Goal: remove the current gap between caller-supplied approval references and authenticated, authoritative approval records.**

Implement a complete, deterministic approval-resolution boundary.

Requirements:

1. Inspect the current approval/catalog models and the code paths that accept:
   - Company identity
   - Industry identity
   - Report type
   - Report/template identity and version
   - Metric identity
   - Unit, currency, and scale
   - Temporal type and duration basis
   - Row/column semantic mapping
2. Implement a single authoritative resolver/service that verifies every approval reference against the active catalog and its exact scope.
3. Reject:
   - Missing approvals.
   - Inactive or revoked approvals.
   - Approval references belonging to another company, industry, report type, template version, or semantic identity.
   - Ambiguous matches.
   - Duplicate active approvals where uniqueness is required.
4. Do not trust a caller merely because it supplies a string that looks like an approval ID.
5. Ensure the canonical writer and adapter use the same authoritative resolution rules. Avoid duplicated, inconsistent approval logic.
6. Keep the resolver deterministic and fail-closed. No inferred mappings or fallback to the first matching metric.
7. Add focused tests for valid approval, missing approval, inactive approval, scope mismatch, ambiguous approval, and revoked approval.
8. Do not create production approvals or mark synthetic test approvals as production-approved.

**Expected result:** the approval infrastructure and resolver are implemented and tested. Production approval data remains a separate owner-data gate unless genuine approved source evidence already exists.

## 5. Workstream B — Persian/Arabic numeric normalization

**Goal: complete the locale-aware numeric input layer without losing financial precision.**

Implement a strict parser/normalizer for Excel and CSV financial values.

Requirements:

1. Support Persian and Arabic-Indic digits and ASCII digits.
2. Support explicitly defined Persian/Arabic/ASCII decimal and thousands separators.
3. Normalize supported negative-number representations only when their meaning is unambiguous.
4. Preserve exact Decimal semantics. Never pass financial values through binary float.
5. Distinguish:
   - Blank cell.
   - Explicit numeric zero.
   - Textual zero.
   - Invalid numeric token.
   - Ambiguous separator pattern.
   - Negative value.
6. Reject ambiguous or malformed strings. Do not silently guess whether a separator is decimal or thousands.
7. Do not convert blank values to zero.
8. Do not change the approved rounding boundary or silently round source values during parsing.
9. Preserve source-token evidence needed by the existing canonical provenance contract.
10. Integrate the parser into the actual Excel/CSV canonical ingestion path, not merely expose an unused helper.
11. Add comprehensive parameterized tests, including mixed digit systems, separator combinations, negative values, blanks, explicit zeros, malformed tokens, and precision edge cases.

Document the accepted lexical grammar precisely. If a pattern cannot be safely interpreted, reject it with a stable diagnostic code.

**Expected result:** close the implementation portion of the locale-normalization blocker. Do not claim production acceptance of every possible workbook format.

## 6. Workstream C — Real BANK workbook template and mapping progress

**Goal: advance the actual BANK template work using available source evidence, without inventing financial meaning.**

Use the existing real workbook if it is present in the repository, particularly:

- `excel/parsian_periodic.xlsx`

Also inspect the existing Parsian template audit, DB-DES-009 mapping/geometry decisions, and the related reports before changing anything.

Requirements:

1. Reproduce the workbook's structural characteristics from the actual workbook:
   - Worksheet names and dimensions.
   - Merged cells.
   - Header paths and repeated headers.
   - Row-axis hierarchy.
   - Relevant data regions.
   - Candidate extraction bounds and partitions.
2. Reassess existing proposed bounds/partitions against the actual workbook. Do not accept historical candidate counts as proof.
3. Implement only structural rules that are unambiguously supported by the workbook.
4. Keep structural identification separate from financial semantic approval.
5. Do not assign a Metric, aggregation rule, unit, currency, scale, temporal basis, or accounting meaning based solely on a plausible Persian label.
6. Preserve the existing approved decisions, including the already-decided repeated header at row 95 and documented exclusions. Do not reopen settled decisions without concrete contradictory evidence.
7. Where a semantic decision cannot be established from the available source, create a precise unresolved item with:
   - Exact worksheet/cell/row/header evidence.
   - The competing interpretations, if any.
   - Why the available evidence is insufficient.
   - The minimum additional evidence required.
8. If a structural template can be safely approved from the actual workbook, implement its exact fingerprint/version and deterministic matching rules. Do not create a generic template that matches unrelated workbooks.
9. Add tests using the actual workbook where licensing/repository test policy permits, otherwise use synthetic fixtures that reproduce verified geometry.
10. Keep all production ingestion fail-closed until the required semantic and temporal approvals exist.

**Expected result:** close any structural-template/matcher work that can genuinely be established from the real workbook. Do not label the entire production mapping complete while semantic decisions remain unapproved.

## 7. Workstream D — Canonical schema, Market/FX constraints, and migration safety

**Goal: resolve schema-level limitations coherently rather than adding application workarounds.**

Inspect the current ORM models, migration runner, all migration history available in the repository, and the exact Market/FX schema constraints.

### D1. Historical Migration 9 lineage

The repository reports an older migration 9 named `codal_excel_source_metadata`, while the current source migration 9 is `canonical_jalali_excel_writer`.

1. Search repository Git history, branches, tags, and available historical source files for the original migration implementation.
2. Determine whether its exact source and schema effects can be recovered.
3. Do not infer equivalence from migration names or column names.
4. If recovered, document the exact old schema effects and provide a safe, read-only reconciliation procedure.
5. If not recovered, state precisely what evidence is missing and keep the conflict guard.
6. Do not rename, delete, overwrite, or silently mark historical migration records as applied.
7. Do not connect to or inspect an actual user database. Provide a read-only inventory/preflight utility only if it can operate safely on an explicitly supplied database connection by the owner later.

### D2. Market/FX physical schema limitations

Resolve the known limitations where safely possible:

- EXCHANGE_CENTER currently conflicts with an old FX schema constraint.
- Jalali-key uniqueness is not guaranteed under concurrent ingestion by the current physical uniqueness model.
- Any required uniqueness must be enforced at the database level, not only by an application pre-check.

Design the additive schema/migration changes needed to support the already-approved FX source contract and Jalali uniqueness.

If a new migration version is necessary, implement it as a new migration. Do not rewrite migration 9 or alter its historical meaning.

Ensure the design:
- Preserves all existing data.
- Has a duplicate preflight that stops safely before creating a unique constraint/index.
- Does not fabricate Jalali-to-Gregorian conversions.
- Uses the correct natural identity for each source.
- Is safe and idempotent on the explicitly supported schema baseline.
- Has isolated temporary-database tests for success, duplicate preflight failure, rerun/idempotency, and rollback.

Do not run migrations against real databases.

### D3. Canonical schema consistency

Check that canonical ORM declarations, migration definitions, constraints, indexes, and writer assumptions agree exactly.

Fix any discrepancies found, including:
- Uniqueness and nullable identity behavior.
- Foreign keys and delete/update behavior.
- Report/version identity.
- Fact-level Jalali period identity.
- Dimension-set identity.
- Provenance identity.
- Audit state transitions.
- Company ticker/codal_symbol uniqueness.

Do not change the approved month-only fiscal calendar rule.

**Expected result:** close code-level schema gaps that can be resolved without knowing the historical contents of a user's database. Historical lineage remains PARTIAL if source evidence cannot be recovered.

## 8. Workstream E — Downstream consumer compatibility

**Goal: remove the current dead end between canonical Excel persistence and the application's financial-data consumers.**

Inspect:

- `src/forecast/queries.py`
- `src/forecast/canonical_queries.py`
- Existing Stage 5/6 query and service interfaces.
- Legacy normalized-fact and period models.
- Canonical models and writer.

Implement a safe compatibility/read boundary.

Requirements:

1. Do not silently switch legacy Stage 5/6 consumers to the new schema.
2. Do not convert Jalali periods into Gregorian identity keys.
3. Do not duplicate canonical facts into legacy tables just to satisfy old consumers.
4. Define an explicit canonical read contract that can supply the required downstream facts and metadata.
5. Where Stage 5/6 logic can consume that contract without changing financial semantics, implement the adapter and focused tests.
6. Where the existing consumer assumes an incompatible schema or semantics, isolate the incompatibility and document the smallest required future change.
7. Preserve PIT behavior: no future publication versions, corrections, or restatements may leak into an earlier cutoff.
8. Preserve exact integer/Decimal values; do not introduce float conversion.
9. Preserve BANK periodic YTD semantics and runtime-only standalone-quarter derivation.
10. Do not persist TTM or other calculated outputs.

**Expected result:** close all consumer integration work that can be implemented without weakening the Jalali/PIT/financial contracts. Clearly identify any downstream stage that still requires a separate reviewed change.

## 9. Workstream F — Atomic Market/FX ingestion completion

Review the current implementation and tests for DB-ING-007 and DB-ING-008.

Resolve remaining code-level gaps that are not already addressed by Workstream D:

- Full-batch validation before persistence.
- No partial writes.
- Deterministic duplicate/replay/conflict semantics.
- Correct transaction rollback.
- Durable and accurate audit status/counts.
- Safe failure diagnostics.
- Correct Rial/Toman conversion.
- Correct source-specific identity and Jalali date handling.
- Concurrency safety backed by physical constraints.

Do not change the approved MarketDaily field mapping. In particular, preserve source `Value` independently.

If a gap depends on a schema migration implemented in Workstream D, coordinate the implementation rather than creating a second workaround.

## 10. Documentation and task closure

Update these durable documents:

- `database/DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md`
- `database/reports/DB_IMPL_001_CANONICAL_DATABASE_AND_EXCEL_WRITER.md`
- `database/reports/DB_EXIT_001_FINAL_ASSESSMENT.md`

Create focused reports for substantial new workstreams if useful. Do not create a separate report for every tiny code change.

Update the Master Packet task statuses and dashboard accurately.

Rules:

- `[x] DONE` only when implementation, required tests, and acceptance evidence are complete.
- `[~] PARTIAL` when code is implemented but real source approval, owner validation, historical DB evidence, or another genuine gate remains.
- Do not mark a task DONE just because tests were added.
- Do not leave tasks PARTIAL merely because a report has not been updated if all substantive criteria are actually met.
- Reconcile task counts and percentages. Do not double-count cross-cutting work.
- Explicitly record the 94 accepted DB-IMPL-001 tests.
- Distinguish owner-run tests from agent-created tests.
- Update the database exit assessment based on actual implementation, not optimistic wording.

`reply.md` is a temporary execution handoff only:
1. Use it if needed to record the current execution.
2. Transfer every durable decision/result to the proper report and Master Packet.
3. Verify the durable transfer.
4. Clear `reply.md` to zero bytes at the end.

Do not edit `WORKFLOW_RULES.md`.

## 11. Engineering and execution rules

- Implement coherent changes across the workstreams. Do not stop after one workstream merely because it is large.
- Do not ask the owner technical-design questions. Technical decisions are delegated to ChatGPT.
- Do not invent source semantics, financial mappings, historical migration effects, or production approvals.
- Do not add hypothetical industry-specific structures outside BANK.
- Do not reintroduce PDF extraction.
- Do not run tests. Add or update tests and provide exact commands for the owner.
- Do not run migrations against a real database.
- Do not change or delete user data.
- Do not claim a test passed unless the owner has run it and supplied the result.
- Do not claim a production workbook was accepted unless actual evidence supports that claim.
- Do not perform another broad repository audit. Read only the related files necessary to implement and verify these workstreams.
- Use stable diagnostic codes and deterministic behavior.
- Run static checks only if they do not execute tests or touch a database.
- Keep changes focused and avoid unrelated refactoring.

## 12. Required final response

At completion, provide one consolidated execution report containing:

1. **Tasks closed:** exact task IDs, why each now meets DONE criteria, and changed files.
2. **Tasks advanced but still PARTIAL:** exact remaining gate and why it cannot honestly be closed.
3. **Implementation summary:** concrete code/schema behavior delivered in each workstream.
4. **Migration safety:** exact migration versions added/changed and confirmation that no real database was opened or modified.
5. **Tests added/changed:** exact test names and test files. State clearly that you did not execute them.
6. **Owner test plan:** grouped exact PowerShell commands, not one command per tiny change. Separate fast focused tests from the broader regression command.
7. **Documentation:** exact Master Packet sections and report files updated.
8. **Task dashboard:** reconciled DONE/PARTIAL/OPEN totals and percentages.
9. **Remaining owner decisions/evidence:** only genuinely unavoidable items, such as missing source semantics or unrecovered historical migration evidence.

**Success criterion:** this run must deliver substantial implementation and close multiple tasks where justified. A report that only restates blockers, proposes future work, or creates more audit tasks is not an acceptable completion.