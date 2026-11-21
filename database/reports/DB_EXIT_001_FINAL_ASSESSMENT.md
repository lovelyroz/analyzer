# DB-EXIT-001 — Final Database Configuration Exit Assessment

**Assessment date:** 2026-11-21  
**Status:** PARTIAL — assessment completed; the database-configuration exit criteria are not yet satisfied.  
**Scope:** The ten global exit criteria in Section 6 of `database/DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md`. This is an evidence-based status assessment, not authorization to alter the ORM, schema, migrations, or an existing database.

## Executive result

The Excel-only extraction boundary and a pure, fail-closed canonical admission plan exist. The Market/FX adapters and application-level atomic ingestion have also advanced, and the owner has accepted the focused Task 017–019 test results recorded in the Master Packet.

The database configuration is **not production-ready**. The principal blocker is not a missing adapter or another test prompt: the physical ORM/schema still cannot represent the approved canonical financial-input contract. In particular, the current period model is Gregorian-date/period-level-YTD based, the normalized fact model uses `Numeric(30,4)` and lacks required canonical identity/provenance/value-state fields, and the canonical plan explicitly sets `execution_allowed=False` and `physical_persistence_compatible=False`. Migration history currently ends at version 8; Migration 9 remains unreconciled. A production Excel template and authenticated semantic/temporal mapping catalog are also not approved.

No production code, ORM model, schema, migration, database, or data was changed for this assessment. No tests were run.

## Ten exit criteria

| # | Exit criterion | Status | Evidence and reason |
|---|---|---|---|
| 1 | Architecture matches owner decisions and all in-scope sections are audited | **PARTIAL** | The logical contracts and owner decisions are extensively recorded in the Architecture and Master Packet. However, several logical contracts are not implemented physically; DB-AUD inventory and reconciliation work remains open. |
| 2 | ORM models and actual migrated schema match the target contract | **BLOCKED** | `src/models/period.py` stores SQL/Gregorian dates; `src/models/normalized.py` defines `NormalizedFinancialFact.value_irr` as `Numeric(30,4)` and does not represent the full canonical identity/value-origin/provenance contract. `Company.ticker` uniqueness and nullable composite-unique behavior also have documented gaps. The migration runner defines versions 1–8 only. |
| 3 | Jalali periods, YTD/standalone, runtime-only TTM, and multi-column period assignment work without inference | **BLOCKED** | The Excel DTO/adapter and admission plan preserve Jalali dates and per-fact temporal basis in memory, but the physical `FinancialPeriod` model uses Gregorian endpoints and period-wide `is_ytd`. There is no production writer that maps the plan into the current model without losing or changing meaning. |
| 4 | ReportVersion correction/PIT behavior is correct and does not leak future data | **PARTIAL** | Existing ReportVersion/PIT selection tests and Stage 6 adversarial tests provide meaningful isolated evidence, including owner acceptance of the corrected Stage 6 suites (**167 passed in 55.40s**). The current CODAL persistence route is still the legacy raw-row route; complete canonical writer, late-arrival/revision reconciliation, and full consumer coverage are not established. |
| 5 | Only selected canonical inputs and minimum provenance are stored; no raw-row archive or calculated financial persistence remains in production | **BLOCKED** | `src/ingestion/service.py::ingest_codal_report` remains a raw-row ingestion path. The canonical Excel plan is non-executable, and the current normalized model is not a compatible replacement. The retained legacy raw/derived schema requires a reviewed, non-destructive transition plan; no new canonical production persistence path is active. |
| 6 | Entity/Industry admission, metric mapping, OTHER_*, NULL and ZERO_FALLBACK follow the contract | **PARTIAL** | The pure admission boundary checks explicit identities, approval references, batch consistency, NULL/zero/fallback distinctions, and OTHER_* approval requirements. However, the supplied approval references are not authenticated against an authoritative production catalog/resolver; production industry/company and metric mappings are not fully approved. |
| 7 | Market/FX/share foundations use valid dates/units and approved policies | **PARTIAL** | Task 034 adapter owner acceptance and Task 035 atomic-ingestion owner acceptance are recorded. Task 035 remains limited: `EXCHANGE_CENTER` is rejected by the current FX schema constraint, Jalali-key uniqueness is not guaranteed under concurrent sessions, and ShareCountHistory/CorporateAction publication/PIT foundations remain incomplete. |
| 8 | Migrations are safe, repeatable, and non-destructive for supported existing schemas | **BLOCKED** | Migration Runner tests cover the current v8 baseline and selected failure/idempotency cases, but Migration 9 is explicitly unreconciled. There is no approved physical-schema target or complete owner-run inventory of every existing database/environment. No further migration should be generated or applied before this is resolved. |
| 9 | Ingestion is atomic/auditable and Excel financial reports use the canonical boundary | **BLOCKED** | Market/FX has an application-level atomic path with documented schema limitations. CODAL Excel reaches `CanonicalPersistencePlan` only; no production ORM writer connects it to downstream models. The plan explicitly disables execution and declares physical persistence incompatible. PDF extraction is retired; supported financial-report inputs are Excel/CSV. |
| 10 | Focused and integrated tests are owner-run and PASS; limitations are explicit | **PARTIAL** | Owner-run evidence includes Task 017 (**23 passed in 76.32s**), Task 018 correction suites (**167 passed in 55.40s**), and Task 019 Excel integration (**115 passed in 2.75s**). These are focused suites, not proof of a complete production schema/writer/migration path or real approved template/mapping. |

## Consolidated blockers and next executable work

The remaining work should be treated as two coherent implementation tracks, not as repeated audit-only tasks:

1. **Canonical physical persistence track — critical path.** Reconcile Migration 9 and approve a target physical contract for Jalali `FinancialPeriod`, canonical integer fact values, per-fact temporal basis, dimensions, value origin/state, minimum provenance, and economic uniqueness. Then implement the ORM/migration and one transactional writer from `CanonicalPersistencePlan` into that contract, including ReportVersion replay/correction and IngestionRun atomicity. This requires an explicit owner authorization for ORM/schema/migration changes and a non-destructive inventory/plan for existing databases. Do not work around the mismatch by writing into the current `NormalizedFinancialFact` shape.

2. **Production Excel approval track.** Complete owner review of the Parsian template bounds/partitions and independent-period drift evidence; establish the authoritative approval catalog/resolver and the locale-specific Persian/Arabic digit and separator parsing contract; then run one representative real-workbook end-to-end acceptance through the canonical writer. Synthetic templates and caller-supplied approval references are not production approvals.

Market/FX follow-up (EXCHANGE_CENTER schema support and Jalali concurrent uniqueness) must be included in the same physical-schema authorization/reconciliation rather than patched around in application code.

## Task status and dashboard reconciliation

- Task 019 / DB-TEST-003 is **PARTIAL**, not OPEN: the owner accepted its focused integration suite (**115 passed in 2.75s**), while production approvals and the physical writer remain open.
- Task 020 / DB-EXIT-001 is **PARTIAL**: this assessment is complete, but the exit criteria themselves are not satisfied.
- The cross-cutting PDF-retirement work is recorded in Sections 8.46 and 9.41 for traceability but is one activity, not two separate tasks in the 35-task dashboard denominator.
- Reconciled 35-task dashboard: **8 DONE / 24 PARTIAL / 3 OPEN = 57%** (DONE=100, PARTIAL=50, OPEN=0).
- DB-TEST / DB-EXIT group: **0 DONE / 4 PARTIAL / 0 OPEN = 50%**.

## Guardrails retained

- No ORM, schema, migration, database, or data changes were made.
- No migration 9/10 was created or applied.
- No production ingestion or PDF path was reintroduced.
- `WORKFLOW_RULES.md` was not modified.
- No tests were run as part of this assessment.

**Conclusion:** Database Configuration is not complete. The critical next step is one authorized canonical physical-schema + migration + writer implementation, coordinated with production Excel approval. Additional report-only audits do not resolve these blockers.
