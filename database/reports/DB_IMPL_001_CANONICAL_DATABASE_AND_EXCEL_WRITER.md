# DB-IMPL-001 — Canonical database and Excel writer implementation

**Date:** 2026-11-21  
**Status:** PARTIAL — implementation and owner-run tests are ready; production approval, test execution, and historical database reconciliation remain open.

## Implemented architecture

The existing `financial_periods`, `normalized_financial_facts`, `reports`, and `report_versions` tables remain intact for their legacy consumers. Migration 9 adds an independent Jalali-native canonical write model in `src/models/canonical.py`: approvals and external-to-internal identity bindings; report and append-only report versions; an explicit company fiscal calendar; Jalali period components; non-null dimension-set identities and members; integer financial facts; and per-fact source provenance. This keeps the Gregorian contract out of canonical period identity and avoids rewriting or silently converting legacy rows.

The canonical fact stores the rounded signed integer required by admission, explicit INSTANT/DURATION and duration basis, unit/currency/scale, scenario, and value state/origin. The source Decimal is retained as canonical text in the provenance record to audit the approved rounding boundary, together with whether the original cell was text, numeric, or blank. Each fact has one non-null `dimension_set_id`, including the empty dimension set, so SQLite NULL behavior cannot disable economic uniqueness. Approval references are checked against active catalog rows; company and Metric IDs must resolve through explicit bindings. Template approval uses the exact ID/version/SHA-256 tuple and its approval reference is stored on the report version. No mapping, fiscal start, currency conversion, or approval is inferred.

## Migration 9 and existing data

`canonical_jalali_excel_writer` is additive and idempotent for the repository's supported v8 schema. It creates canonical tables, adds a fiscal calendar table, and installs unique company ticker and non-null `codal_symbol` indexes after a duplicate preflight. Duplicate legacy symbols stop the migration without changing existing values. It does not translate Gregorian periods, alter legacy fact rows, or remove the historical `source_sheet` / `source_column_header` metadata.

The repository has owner-reported evidence of an earlier migration 9 named `codal_excel_source_metadata`, with populated columns, but its implementation source remains unrecovered. The runner therefore refuses any existing version-9 ledger entry whose name is not `canonical_jalali_excel_writer`. This avoids recording or assuming that the two different migrations are equivalent. The conflict is intentionally not auto-repaired. No real database was opened or changed and Migration 9 was not executed against any user database.

## Writer, transactions, and replay behavior

`src/ingestion/canonical_writer.py::ingest_excel_source()` creates and commits an `IngestionRun` in STARTED state before calling the current Excel adapter with admission enabled. It then validates the admitted plan again and resolves its BANK company, Metric, extraction standard, template, and all supplied approvals against active catalog rows. The caller must supply report title, positive version number, publication datetime, audit/restatement flags, and scenario explicitly. A DURATION YTD fact is accepted only when its start is the configured company's first fiscal month and day; BANK periods must span 3, 6, 9, or 12 complete Jalali months. INSTANT requires equal endpoints and no duration basis. Metric FLOW/STOCK must match DURATION/INSTANT. Derived Metrics and malformed source coordinates are rejected.

The writer owns a SQLAlchemy session. A report version, every period/dimension/fact/provenance row, accepted/duplicate/rejected audit counts, and the transition to COMPLETED are committed together. A failed validation or write rolls that transaction back, then marks the same run FAILED in a separate transaction using a stable code without source values or raw exception details. No commit occurs inside the fact loop. An exact replay of report metadata, source revision, fact payload, source locator, and approval provenance returns duplicate counts without inserting rows. Any difference under the same external version is a conflict. Reuse of a source revision or version number is rejected. A correction must identify a prior version and is appended while the prior version remains stored.

`src/forecast/canonical_queries.py` adds a Jalali-native read API. It filters by ReportVersion publication time at the requested PIT cutoff, keeps report types separate, and applies the approved audit/restatement quality ordering before publication/version tie-breaks for each metric/period/dimension identity. It returns exact integer values and source coordinates. Existing `src/forecast/queries.py` and Stage 5/6 are intentionally still on the legacy schema; they have not been silently switched to canonical tables.

## Tests added or updated (not run)

`src/tests/test_canonical_writer.py` adds temporary-SQLite coverage for a supported v8 upgrade and legacy-row preservation, migration failure without a successful ledger entry, conflicting historical migration history, symbol uniqueness, Jalali validity/non-calendar fiscal start and YTD persistence, synthetic XLSX through reader/matcher/admission/writer/read-back, exact Decimal and source coordinates, approved zero fallback, exact replay, changed-payload conflict, append-only correction, publication-time PIT and audit/restatement quality ordering, batch rollback, and non-null dimension identity. `src/tests/test_task017_model_constraints.py` and `src/tests/test_stage1_database_integrity.py` update migration-version expectations; `src/tests/test_canonical_ingestion_admission.py` and `src/tests/test_excel_adapter.py` now assert that structurally compatible plans are executable and persistence-compatible.

Per `PROMPT.md`, these tests were not executed. After reviewing the patch, the owner can run the focused suites from the repository root:

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_db_impl_001_20261121 src/tests/test_canonical_writer.py src/tests/test_task017_model_constraints.py src/tests/test_stage1_database_integrity.py src/tests/test_canonical_ingestion_admission.py src/tests/test_excel_adapter.py src/tests/test_excel_canonical_input.py src/tests/test_excel_template_matching.py
```

No migration command is included: deployment requires a separate read-only inventory and explicit reconciliation of each target database's migration ledger and schema first.

## Remaining gates and risk

- Status remains **PARTIAL** until the owner executes the focused test command and resolves any failures.
- Production template and semantic/temporal approvals are not available. The writer fails closed until explicit active catalog approvals and company/Metric identity bindings are installed.
- Locale-specific Persian/Arabic digit and separator parsing remains unapproved; existing accepted numeric syntax is retained.
- The historical `codal_excel_source_metadata` migration 9 source and target database lineage remain unresolved. Any such target will stop at the migration-name guard pending reconciliation; do not rename or delete its history or columns based on this code change.
- Legacy Stage 5/6 consumers continue to query the old Gregorian/Numeric models and will not see canonical facts until a separately reviewed compatibility/read-path change is made.
- The writer path is implemented, but production readiness and real-workbook end-to-end acceptance are not established. No real source workbook or user database was used.

## Exact changed files

- `12_Database_Architecture_V1.1.md`
- `database/DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md`
- `database/reports/DB_EXIT_001_FINAL_ASSESSMENT.md`
- `database/reports/DB_IMPL_001_CANONICAL_DATABASE_AND_EXCEL_WRITER.md`
- `reply.md`
- `src/forecast/canonical_queries.py`
- `src/ingestion/canonical_admission.py`
- `src/ingestion/canonical_writer.py`
- `src/migrations/runner.py`
- `src/models/canonical.py`
- `src/tests/test_canonical_writer.py`
- `src/tests/test_canonical_ingestion_admission.py`
- `src/tests/test_excel_adapter.py`
- `src/tests/test_stage1_database_integrity.py`
- `src/tests/test_task017_model_constraints.py`

`src/models/entity.py` and legacy physical models remain unchanged. `WORKFLOW_RULES.md`, PDF extraction code, real databases, and stored user data were not touched.


## Post-implementation code review — 2026-11-21 (before owner test run)

Static review found a temporal-scope defect that must be corrected before the owner runs the new test suite or treats the writer as accepted:

1. `_validate_report_calendar()` currently applies the BANK periodic YTD alignment rule (3/6/9/12 complete Jalali months and month-end) to every BANK `DURATION/YTD` fact. It does not check `report_type_id`. This incorrectly couples `MONTHLY_ACTIVITY` to the separately reviewed `PERIODIC_FINANCIAL` standard. Apply the 3/6/9/12 rule only to BANK `PERIODIC_FINANCIAL`; monthly activity must use its own approved temporal standard and must not inherit periodic-report rules.
2. `CanonicalCompanyFiscalCalendar` stores only `fiscal_year_start_month`, and the writer hardcodes start day 1. The approved contract requires the actual company fiscal-year start, not an assumed first day. Store and approve the exact Jalali start month and day, validate YTD starts against both, and do not infer either from a generic calendar convention.
3. Add focused regression tests for both report types and for a non-first-day fiscal-year start, including migration/model coverage. Keep all date identity Jalali-native.

This is a concrete implementation defect, not an owner-data or production-approval blocker. DB-IMPL-001 remains PARTIAL pending this correction, the focused owner test run, historical migration-9 lineage reconciliation, and production approvals. No tests were run during this static review; no real database or migration was used.
