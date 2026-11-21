# DB-CONSOLIDATION-002 implementation report

Date: 2026-11-21. This report records implementation and evidence; it does not claim owner acceptance of newly added tests or production readiness.

## Delivered

- Added Migration 10, `market_fx_approval_scope_schema`, leaving Migration 9 untouched. It preflights duplicate and partial Jalali identities, adds partial unique indexes and completeness triggers for MarketDaily and FXRate, adds scoped approval/source-token columns, and rebuilds the SQLite FX rate-type CHECK to admit the already-approved `EXCHANGE_CENTER` contract while preserving rows. It refuses conflicting reserved temporary-table names and foreign-key-dependent rebuilds. Migration 10 tests cover success/idempotency, duplicate preflight rollback, and reserved-name refusal. No database was opened or migrated.
- Added exact-scope active approval resolution. The canonical writer and Excel adapter share preflight rules; the writer repeats resolution in its write transaction. Caller references are checked against active kind, identity, and canonical JSON scope. Production approval records remain absent/unverified.
- Added strict Decimal lexical parsing for Excel and CSV: ASCII, Persian and Arabic-Indic digits; `.` and U+066B decimal marks; comma/U+066C/U+060C grouping in groups of three; grouping precedes decimal; optional leading sign or enclosing parentheses; no mixed grouping, exponent notation, malformed grouping, implicit rounding, or float input. Blank, text zero, numeric zero, negative, invalid, and ambiguous tokens remain distinguishable. Original tokens flow into canonical provenance.
- Added runtime-only exact integer YTD quarter differences for compatible BANK PERIODIC_FINANCIAL facts, preserving both source report-version IDs and requiring a contiguous period chain. MONTHLY_ACTIVITY and other bases are excluded. Legacy Stage 5/6 consumers still expect legacy/Gregorian interfaces; no silent switch or duplication was made.
- Market CSV now resolves a ticker against `codal_symbol` when present, allows the legacy ticker fallback only if the CODAL identity is absent or consistent, and rejects conflicting identities as `TICKER_IDENTITY_CONFLICT`. Market source Value remains independently preserved. Physical unique indexes back concurrency semantics.

## Evidence and limits

The owner reports acceptance of the focused DB-IMPL-001 suite: 93 passed in the full run and the corrected isolated case passed (1 passed in 1.11s), for 94 successes and zero known failures. These are owner-run results and predate this consolidation. Tests added or changed in this run were not executed.

`excel/parsian_periodic.xlsx` is absent from this checkout, so no current workbook geometry, fingerprint, bounds, or mapping could be verified. Existing reports are historical evidence only and were not promoted into a production template. `git log --all -S'codal_excel_source_metadata' -- src/migrations/runner.py` did not recover the historical implementation; no real database was inspected. The v9 conflict guard remains.

Tasks DB-IMPL-001, DB-ING-002/003, DB-TEST-002/003, DB-EXIT-001 and DB-ING-008 remain PARTIAL: newly added tests await owner execution, production approvals/template evidence are missing, Stage 5/6 integration remains incompatible, and historical migration lineage is unresolved. DB-ING-007 remains at its existing owner-accepted status. No task is marked DONE based solely on code or tests being added.

## Tests added or changed (not run)

- `src/tests/test_approval_catalog.py`: valid, missing, inactive/revoked, wrong scope, ambiguous active approval.
- `src/tests/test_financial_numbers.py`: digit/separator grammar, signs, precision, blank/zero distinction, malformed/ambiguous values, float rejection, CSV facade.
- `src/tests/test_canonical_queries.py`: exact quarter differences, gap handling, report-type filtering.
- `src/tests/test_canonical_writer.py`: scoped approval fixtures, migration 10 and monthly/periodic regression coverage.
- `src/tests/test_excel_canonical_input.py`, `src/tests/test_ingestion_fx.py`, `src/tests/test_market_fx_atomic_ingestion.py`, `src/tests/test_stage1_database_integrity.py`, and `src/tests/test_task017_model_constraints.py`: integration and migration expectation updates.

## Owner commands

Focused consolidation suites:

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_db_consolidation_002_20261121 src/tests/test_approval_catalog.py src/tests/test_financial_numbers.py src/tests/test_excel_canonical_input.py src/tests/test_canonical_ingestion_admission.py src/tests/test_excel_adapter.py src/tests/test_canonical_writer.py src/tests/test_canonical_queries.py src/tests/test_market_fx_atomic_ingestion.py src/tests/test_market_fx_adapters.py src/tests/test_ingestion_fx.py src/tests/test_stage1_database_integrity.py src/tests/test_task017_model_constraints.py
```

Broader affected regression suites:

```powershell
.\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_db_consolidation_002_regression_20261121 src/tests/test_market_fx_preflight.py src/tests/test_ingestion_ohlc.py src/tests/test_ingestion_fx.py src/tests/test_stage5_queries.py src/tests/test_stage6_p25_selection.py src/tests/test_stage6_p25_adversarial.py src/tests/test_excel_template_matching.py src/tests/test_excel_adapter.py src/tests/test_canonical_ingestion_admission.py src/tests/test_canonical_writer.py
```


## Owner-run test failure corrections — 2026-11-21

The first owner run of the DB-CONSOLIDATION-002 focused command returned **14 failed, 140 passed**. The failures were reviewed against the actual source and corrected directly:

- `src/ingestion/canonical_writer.py`: added the global empty-scope `industry` approval kind and included `report_version_id` in the report-version approval scope. This aligns runtime validation with the exact scoped catalog rows and removes the shared root cause behind the cascading writer failures.
- `src/tests/test_excel_canonical_input.py`: changed the malformed-number fixture from `1,000` to `1,00`. Under the documented parser grammar, `1,000` is a valid three-digit grouping token and must not be rejected.
- `src/tests/test_canonical_writer.py`: supplied the required legacy `status` and `is_active` fields in the Migration 10 duplicate-preflight fixture.
- `src/tests/test_market_fx_atomic_ingestion.py`: corrected the identity-conflict fixture so the CSV ticker resolves to a company whose configured `codal_symbol` actually differs. The previous fixture added an unrelated second company and did not create a conflict.

No production database was opened or migrated. These corrections have not been test-executed by the assistant; owner rerun is required. Existing production template/approval, Stage 5/6 bridge, and historical Migration 9 lineage gates remain unchanged.


## Second owner-run test result and follow-up — 2026-11-21

After the first correction set, the owner reran the focused suite: **1 failed, 153 passed**. The only remaining failure was the synthetic XLSX end-to-end test, caused by its shared source-label/source-header approval fixtures retaining a placeholder template fingerprint (`b` repeated 64 times), while the test's actual generated template has a different fingerprint. The test now updates those two approval scopes to the exact generated template fingerprint before exercising reader → matcher → admission → writer → readback. This is a test-fixture correction; production exact-scope validation remains unchanged.

Owner should rerun the isolated test first, then the focused suite if it passes. No production database was opened or migrated.