# DB-TEST-001 ? Model Constraints and Migration Tests

## Status

Task 017 is **PARTIAL**. Focused SQLite coverage for declared model constraints and Migration Runner behavior has been added. The owner has not run the new tests. The full Jalali-period contract, supported legacy schema matrix, and production-database behavior remain unproven.

## Coverage added

`src/tests/test_task017_model_constraints.py` uses isolated temporary SQLite databases and verifies `PRAGMA foreign_keys=1`. Model checks cover Company required fields and Industry FK, Industry code uniqueness, nullable/unique national IDs, FinancialPeriod Gregorian date order/type/identity, ReportVersion version/current uniqueness, FinancialMetric values, MappingDecision values and confidence, NormalizedFinancialFact identity/quality, and DerivedFinancialFactInput source XOR and uniqueness behavior.

Migration checks cover empty upgrade through v8, idempotence/history uniqueness, non-empty legacy baseline recognition without business-row loss, Migration 4 rejection of multiple current ReportVersions without repair or recording v4, and failed migration not being recorded. Existing `src/tests/test_stage1_database_integrity.py` already covers v8 forecast-table removal and preservation of unrelated/input-side rows; it is included in the owner command.

## Limits and gaps

`src/core/jalali.py` implements `validate_jalali_date()` and the new test checks valid and invalid tuples. `FinancialPeriod` uses SQL `Date` columns and only checks Gregorian `end_date >= start_date`; it has no Jalali validation. No Jalali conversion or extra model contract was introduced.

SQLite treats NULL values as distinct for composite UNIQUE constraints. Duplicate `DerivedFinancialFactInput` rows with the same populated source and NULL in the other source column currently pass; the test records that behavior. SQLite cannot establish production concurrency or cross-database constraint equivalence. The legacy test exercises generic non-empty-database recognition, not every historical schema shape.

No model, schema, or migration implementation was changed. No real or owner database was opened. Tests were not run by the agent.

## Owner command

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_task017_20261120 src/tests/test_task017_model_constraints.py src/tests/test_stage1_database_integrity.py
```

## Owner-reported Task 016 acceptance

Recorded separately as requested; it does not cover Task 017:

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_task016_20261120 src/tests/test_excel_adapter.py src/tests/test_excel_canonical_input.py src/tests/test_excel_template_matching.py src/tests/test_canonical_ingestion_admission.py
```

Owner reported **51 passed in 1.59s**. Task 016 remains PARTIAL because approved production templates, real semantic/temporal mappings, and representative real-workbook validation are missing.

## Exact changed files

- `src/tests/test_task017_model_constraints.py` (added)
- `src/tests/test_stage1_database_integrity.py` (Migration 8 input-side table assertion)
- `database/reports/DB_TEST_001_MODEL_MIGRATION_TESTS.md` (added)
- `database/DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md`
- `reply.md`
