# DB-EXIT-001 — Final Database Configuration Exit Assessment

**Assessment date:** 2026-11-21  
**Status:** PARTIAL — implementation advanced; owner validation, production approvals, and historical database reconciliation remain.
**Scope:** The ten global exit criteria in Section 6 of `database/DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md`, updated after DB-IMPL-001 code changes.

## Executive result

An additive Jalali-native canonical schema, migration 9, transactional Excel writer, and canonical PIT read API are now implemented in source. The Market/FX adapters and application-level atomic ingestion have also advanced, and the owner has accepted the focused Task 017–019 test results recorded in the Master Packet.

The database configuration is **not production-ready**. The canonical contract is represented by new additive tables; legacy `FinancialPeriod`, `NormalizedFinancialFact`, and existing Stage 5/6 consumers remain unchanged. Repository migration history now defines version 9, with a guard against treating the historical `codal_excel_source_metadata` version 9 as equivalent. That historical lineage and each installed database remain unreconciled. Production Excel templates and an authoritative approval catalog are also unavailable, and all new owner-run integration tests remain unexecuted.

No migration was run against a real database and no user data was read, changed, or deleted. New tests were written but not run, as directed by `PROMPT.md`.

## Owner clarifications recorded after this assessment — 2026-11-21

The owner has confirmed that the current financial-report standardization and ingestion scope is **BANK only**. Other industries must not be pre-modeled with hypothetical report patterns, metrics, or extraction schemas; the shared core remains extensible and each new industry's standard is added after reviewing its real reports.

The BANK periodic financial reports reviewed to date follow the cumulative pattern: 3-, 6-, 9-, and 12-month values are YTD from the company's actual fiscal-year start. Standalone-quarter values needed by the frontend are runtime calculations from compatible cumulative periods, not presumed independent source inputs and not persisted. This clarification supersedes any generic wording in this assessment that suggests standalone source values should be anticipated for current BANK reports.

The approved Jalali calendar contract remains authoritative: FinancialPeriod identity and endpoints are Jalali. The current Gregorian SQL Date implementation is a code/schema gap to fix, not a reason to weaken or reinterpret the contract. The technical implementation decisions are delegated to ChatGPT; the assessment's previous request for further owner authorization of technical design is superseded. Any migration must still be non-destructive and must not be applied to a real database without a separately controlled deployment step.

## Ten exit criteria

| # | Exit criterion | Status | Evidence and reason |
|---|---|---|---|
| 1 | Architecture matches owner decisions and all in-scope sections are audited | **PARTIAL** | The logical contracts and owner decisions are extensively recorded in the Architecture and Master Packet. However, several logical contracts are not implemented physically; DB-AUD inventory and reconciliation work remains open. |
| 2 | ORM models and actual migrated schema match the target contract | **PARTIAL** | New canonical ORM tables and migration 9 define Jalali periods, integer facts, dimensions, approvals, and provenance; legacy tables remain unchanged. Migration 9 has not been run against an installed DB, and historical v9 lineage remains unresolved. |
| 3 | Jalali periods, YTD/standalone, runtime-only TTM, and multi-column period assignment work without inference | **PARTIAL** | Writer validates actual Jalali components and BANK YTD alignment against an explicit company start month. Runtime quarter derivation remains outside persistence. Legacy consumers still use the Gregorian period model; production report coverage and owner test evidence are pending. |
| 4 | ReportVersion correction/PIT behavior is correct and does not leak future data | **PARTIAL** | A canonical PIT reader selects by publication time and preserves appended report versions. Its new tests are unrun, and Stage 5/6 still read legacy normalized facts. |
| 5 | Only selected canonical inputs and minimum provenance are stored; no raw-row archive or calculated financial persistence remains in production | **PARTIAL** | The new writer stores only accepted canonical facts and minimal provenance. Existing legacy raw/derived tables and the old ingestion service are retained for compatibility; their transition is not part of this migration. |
| 6 | Entity/Industry admission, metric mapping, OTHER_*, NULL and ZERO_FALLBACK follow the contract | **PARTIAL** | The pure admission boundary checks explicit identities, approval references, batch consistency, NULL/zero/fallback distinctions, and OTHER_* approval requirements. However, the supplied approval references are not authenticated against an authoritative production catalog/resolver; production industry/company and metric mappings are not fully approved. |
| 7 | Market/FX/share foundations use valid dates/units and approved policies | **PARTIAL** | Task 034 adapter owner acceptance and Task 035 atomic-ingestion owner acceptance are recorded. Task 035 remains limited: `EXCHANGE_CENTER` is rejected by the current FX schema constraint, Jalali-key uniqueness is not guaranteed under concurrent sessions, and ShareCountHistory/CorporateAction publication/PIT foundations remain incomplete. |
| 8 | Migrations are safe, repeatable, and non-destructive for supported existing schemas | **PARTIAL** | Migration 9 is additive, preserves legacy fact/period data, is idempotent on the supported v8 layout, and refuses a conflicting historical v9 ledger name. Temporary-database tests are written but unrun; every real database still needs read-only lineage/schema inventory before deployment. |
| 9 | Ingestion is atomic/auditable and Excel financial reports use the canonical boundary | **PARTIAL** | `ingest_excel_source()` writes only an executable admitted plan; STARTED is durable before workbook reading, accepted data and COMPLETED audit commit together, and failures roll back. Production approval catalogs/templates are absent and owner integration tests have not run. |
| 10 | Focused and integrated tests are owner-run and PASS; limitations are explicit | **PARTIAL** | Previous owner-run suites remain accepted (Task 017: 23 passed; Task 018: 167 passed; Task 019: 115 passed). DB-IMPL-001 adds migration/writer/PIT tests but intentionally leaves execution to the owner. |

## Consolidated blockers and next executable work

The remaining work should be treated as two coherent implementation tracks, not as repeated audit-only tasks:

1. **Owner validation and database reconciliation.** Run the exact temporary-database test command in the new implementation report. Separately recover and reconcile the historical `codal_excel_source_metadata` migration-9 source and inventory each installed database read-only. Do not apply this migration to any existing database until its ledger/schema lineage is confirmed.

2. **Production Excel approval track.** Complete owner review of the Parsian template bounds/partitions and independent-period drift evidence; establish the authoritative approval catalog/resolver and the locale-specific Persian/Arabic digit and separator parsing contract; then run one representative real-workbook end-to-end acceptance through the canonical writer. Synthetic templates and caller-supplied approval references are not production approvals.

Market/FX follow-up (EXCHANGE_CENTER schema support and Jalali concurrent uniqueness) must be included in the same physical-schema authorization/reconciliation rather than patched around in application code.

## Task status and dashboard reconciliation

- Task 019 / DB-TEST-003 is **PARTIAL**, not OPEN: the owner accepted its focused integration suite (**115 passed in 2.75s**), while production approvals and the physical writer remain open.
- Task 020 / DB-EXIT-001 is **PARTIAL**: this assessment is complete, but the exit criteria themselves are not satisfied.
- DB-IMPL-001 is **PARTIAL**: source implementation and temporary-database tests are added; owner execution, production approvals, and historical v9 reconciliation remain.
- The cross-cutting PDF-retirement work is recorded in Sections 8.46 and 9.41 for traceability but is one activity, not two separate tasks in the dashboard denominator.
- Reconciled 36-task dashboard: **8 DONE / 25 PARTIAL / 3 OPEN = 57%** (DONE=100, PARTIAL=50, OPEN=0).
- DB-TEST / DB-EXIT group: **0 DONE / 4 PARTIAL / 0 OPEN = 50%**.

## Guardrails retained

- ORM/schema code and a source migration 9 were added; no migration was applied to a real database and no existing data was changed.
- No production ingestion or PDF path was reintroduced.
- `WORKFLOW_RULES.md` was not modified.
- No tests were run as part of this assessment.

**Conclusion:** Database Configuration is not complete. The critical next step is one authorized canonical physical-schema + migration + writer implementation, coordinated with production Excel approval. Additional report-only audits do not resolve these blockers.
