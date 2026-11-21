# TASK 017 — DB-TEST-001: Model Constraints and Migration Tests
**Type: TEST IMPLEMENTATION + DOCUMENTATION**

Repository: `analyzer`  
Branch: `master`

## Objective

Implement focused automated tests for the existing database models and Migration Runner.

This is an execution task. Add meaningful tests, not another broad audit.

## 1. Record latest owner acceptance

Task 016 owner-run command:

`.\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_task016_20261120 src/tests/test_excel_adapter.py src/tests/test_excel_canonical_input.py src/tests/test_excel_template_matching.py src/tests/test_canonical_ingestion_admission.py`

Result: **51 passed in 1.59s**.

Record this exact result in `reply.md` and Master Packet under Task 016. Task 016 remains PARTIAL because production template and real semantic/temporal mappings and representative real-workbook validation are still missing.

## 2. Inspect existing test coverage

Read the current implementations before adding tests:
- `src/models/entity.py`
- `src/models/period.py`
- `src/models/report.py`
- `src/models/normalized.py`
- `src/models/audit.py`
- `src/models/market.py`
- `src/models/fx.py`
- `src/models/share_action.py`
- `src/migrations/runner.py`
- `src/core/database.py`

Inspect existing tests for model constraints, foreign keys and migrations. Reuse existing fixtures and avoid duplicate test coverage.

## 3. Implement model constraint tests

Add focused tests for currently implemented constraints:

- Company → Industry foreign key and required fields.
- Unique Industry code and unique non-null national ID where supported by the database.
- FinancialPeriod:
  - `end_date >= start_date`
  - allowed `period_type`
  - uniqueness of `(company_id, fiscal_year, period_type, end_date)`.
- ReportVersion:
  - unique `(report_id, version_number)`
  - at most one current version per report.
- FinancialMetric:
  - allowed `flow_or_stock`
  - allowed `statement_type`
  - allowed `sign_convention`.
- MappingDecision:
  - allowed mapping method and review status
  - allowed composition role
  - confidence range.
- NormalizedFinancialFact:
  - unique economic identity as currently defined
  - allowed quality status.
- DerivedFinancialFactInput:
  - exactly one input source populated
  - uniqueness of the declared input identity.

For each constraint, test both an accepted case and a rejected case where practical.

Use isolated temporary SQLite databases. Ensure foreign-key enforcement is actually enabled in the test engine.

Do not assume that a model constraint exists merely because the architecture document requires it. Test the actual declared behavior.

## 4. Implement Migration Runner tests

Test the currently supported migration sequence only:

- Empty database upgrade.
- Expected current migration version (currently version 8).
- Repeated upgrade is idempotent.
- Migration history contains each applied version once.
- Existing supported legacy baseline is recognized without recreating or deleting existing business rows.
- Additive migrations preserve unrelated existing data.
- Migration 4 rejects multiple current ReportVersions and does not silently repair the data.
- Migration 8 behavior is tested explicitly, including its intended removal of forecast output tables and preservation of unrelated/input-side tables.
- Failure during a migration must not incorrectly record that migration as successfully applied.

Use temporary test databases only. Never use the user's real database.

## 5. Jalali and schema gaps — report honestly

The current FinancialPeriod model uses SQL Date columns and Gregorian date comparisons. Do not invent a Jalali constraint or silently convert Jalali dates.

Inspect whether a currently implemented Jalali validation utility exists. If it does, test its actual behavior. If no enforceable Jalali model contract exists, record it as an uncovered requirement / blocker.

Similarly, do not claim that SQLite tests prove production-database concurrency or cross-database constraint behavior.

## 6. Strict exclusions

- No ORM/model changes.
- No schema changes.
- No migration creation, modification, deletion or reordering.
- Do not resolve Migration 9.
- No database upgrade against a real or owner database.
- No data modification outside isolated temporary test databases.
- No production ingestion.
- No changes to `WORKFLOW_RULES.md`.
- Do not weaken constraints to make tests pass.
- Do not run tests; the owner runs them.

If a desired invariant is not currently implemented, document the gap rather than changing production code in this Task.

## 7. Deliverables

1. Focused model constraint tests.
2. Focused Migration Runner tests.
3. Report: `database/reports/DB_TEST_001_MODEL_MIGRATION_TESTS.md`
4. Update `reply.md`.
5. Update Task 017 in Master Packet with exact evidence.
6. Recalculate dashboard if Task 017 changes from OPEN to PARTIAL.
7. Exact changed-file list and exact owner test command.

Task 017 may become PARTIAL after meaningful test implementation, but must not become DONE while Jalali constraints, supported-schema coverage or other required migration guarantees remain unproven.

Report:
- What tests were added.
- What existing behavior they verify.
- What requirements remain unsupported.
- Which tests were not run.
- Exact command for owner acceptance.

Do not mark any task DONE without corresponding evidence.