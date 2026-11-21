> **2026-11-21 reconciliation:** PDF corpus coverage described in historical notes below is retired. The retained CODAL persistence and PIT contracts now use synthetic parsed-row DTOs in src/tests/test_codal_extraction.py. The active owner command below excludes PDF suites. See DB_CODAL_RETIRE_001_EXCEL_CSV_ONLY_RETIREMENT.md.
# DB-TEST-002 — Ingestion and Point-in-Time Test Increment

## Status

Task 018 is **PARTIAL**. One new synthetic end-to-end regression now verifies a multi-period workbook through the Excel adapter and canonical admission boundary. This increment reuses focused existing tests for the other required behaviors instead of duplicating their assertions. No tests were run by the agent.

## New coverage

Added `test_multi_period_report_preserves_explicit_ytd_and_standalone_semantics` in `src/tests/test_excel_adapter.py`. It creates a synthetic workbook with two values for one metric, applies explicit selections at two exact coordinates, and submits different Jalali date ranges and duration bases. It asserts the admitted logical plan retains two separate fact identities, the correct YTD and STANDALONE labels, each source coordinate, and both values.

## Existing focused coverage reused

- `test_excel_canonical_input.py` and `test_excel_adapter.py`: explicit INSTANT/DURATION and YTD/STANDALONE semantics, incomplete or ambiguous temporal selections, approved matching, and provenance.
- `test_canonical_ingestion_admission.py`: all-or-nothing batch rejection, identical replay, changed-payload conflict, correction as a new version with prior-version preservation, provenance conflicts, explicit mapping approvals, BLANK/zero/ZERO_FALLBACK distinctions, and raw/calculated record rejection.
- `test_codal_extraction.py`: synthetic parsed-row coverage for ReportVersion chain, replay/idempotency, and publication-time PIT behavior against the existing CODAL persistence path.
- `test_market_fx_atomic_ingestion.py`: atomic multi-row batches, replay/conflict, rollback on commit failure, and audit failure behavior for existing Market/FX writers.
- `test_stage6_p25_selection.py`, `test_stage6_p25_adversarial.py`, and `test_stage6_evaluation_foundation.py`: deterministic publication-order selection, tie handling, future-version exclusion and PIT leakage status.

## Gaps and limits

The canonical Excel admission boundary produces a non-executable plan (`execution_allowed=False`) and has no ORM writer. Therefore this Task cannot test physical canonical Excel commit/rollback or writer audit-state behavior. No approved real Excel template or production semantic mappings are available. The synthetic regression does not establish production mapping correctness. SQLite and test fixtures do not establish production-database concurrency or cross-database behavior.

Task 017 remains **PARTIAL**. Owner-reported acceptance was **23 passed in 76.32s (0:01:16)** for:

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_task017_20261120 src/tests/test_task017_model_constraints.py src/tests/test_stage1_database_integrity.py
```

Task 017 remains PARTIAL because the FinancialPeriod model has no Jalali constraint, supported-schema coverage is limited, SQLite composite uniqueness has a NULL-related gap, and production/concurrency behavior is not proven.

## Owner command for Task 018

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_task018_20261121 src/tests/test_excel_adapter.py src/tests/test_excel_canonical_input.py src/tests/test_canonical_ingestion_admission.py src/tests/test_codal_extraction.py src/tests/test_codal_digit_normalization.py src/tests/test_market_fx_atomic_ingestion.py src/tests/test_stage6_p25_selection.py src/tests/test_stage6_p25_adversarial.py src/tests/test_stage6_evaluation_foundation.py
```

## Exact changed files

- `src/tests/test_excel_adapter.py`
- `database/reports/DB_TEST_002_INGESTION_PIT_TESTS.md`
- `database/DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md`
- `reply.md`
