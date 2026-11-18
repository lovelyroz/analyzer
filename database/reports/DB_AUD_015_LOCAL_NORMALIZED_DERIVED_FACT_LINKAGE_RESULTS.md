# DB-AUD-015 — Local Normalized / Derived FinancialFact Linkage Results

**Status:** LOCAL DATABASE SNAPSHOT COMPLETE; RETIREMENT NOT AUTHORIZED  
**Date:** 2026-11-18  
**Database inspected:** `D:\\Winprojects\\analyzer\\tehran_stock.db`  
**Method:** Owner-executed `src/scripts/audit_normalized_derived_fact_links.py`; SQLite `mode=ro`; report received through `reply.md`.  
**Scope:** Table population, relevant FK/reference counts, per-target linkage distributions, duplicate input links and `PRAGMA foreign_key_check`.

## 1. Executive result

All four normalized/derived tables exist but are empty in the inspected local database:

| Table | Rows | Columns |
|---|---:|---:|
| `normalized_financial_facts` | 0 | 10 |
| `normalized_financial_fact_inputs` | 0 | 5 |
| `derived_financial_facts` | 0 | 11 |
| `derived_financial_fact_inputs` | 0 | 5 |

Additional facts:
- `raw_financial_facts` contains 505 rows.
- No row in `normalized_financial_facts` references any of those 505 raw facts.
- No row in `normalized_financial_fact_inputs` references any of those 505 raw facts.
- `mapping_decisions` has no linked rows from the two normalized tables in this snapshot.
- `derived_financial_facts` has 0 rows; the per-parent distribution reports 0 derived rows for each of the 2 `report_versions`.
- `derived_financial_fact_inputs` has 0 rows, so there are no observed normalized-fact or derived-fact input links.
- Both input tables have 0 duplicate composite-link groups.
- `PRAGMA foreign_key_check` returned 0 violations.

## 2. Interpretation

### 2.1 New canonical model compatibility

The local DB evidence is consistent with the source-code audit:
- The Stage 5 production query exists, but this database has no normalized facts for it to read.
- There is no local normalized/derived data that would need to be backfilled into the proposed `financial_facts` table.
- There is no local derived-fact input graph to migrate or preserve as populated data.
- The 505 legacy RawFinancialFact rows are currently unreferenced by the normalized fact/provenance tables inspected here.

This does **not** establish that the normalized/derived tables are empty in every deployment, backup, test fixture, or external database. It also does not prove that the 505 RawFinancialFact rows are disposable; their preservation decision remains governed by DB-AUD-011 and DB-PLAN-013.

### 2.2 FK integrity

No dangling references or SQLite FK violations were observed in this snapshot. This is a point-in-time integrity result only; it is not permission to drop tables, columns, models or migrations.

### 2.3 Derived output persistence policy

No populated persisted derived facts were found locally. The new architecture should continue to keep derived/calculated analysis outputs runtime-only. Do not introduce writers to `derived_financial_facts` or `derived_financial_fact_inputs`.

## 3. Consequences for retirement planning

1. No normalized/derived data backfill is required **for this exact local database snapshot**.
2. The old normalized/derived models and tables must nevertheless remain in the repository/schema until all environments, migration history, backups and external consumers are reconciled.
3. Do not remove the Stage 5 query just because the local table is empty. It is a production code path; migrate it only when the new canonical `financial_facts` schema and query contract are implemented.
4. Preserve all 505 `raw_financial_facts` rows and their five provenance columns as already decided in DB-AUD-011.
5. Do not change FKs or drop normalized/derived tables in this task.
6. Migration 9 discrepancy remains open and blocks destructive schema retirement.

## 4. Combined audit state

| Area | Result |
|---|---|
| Source production readers | One direct reader: Stage 5 `src/forecast/queries.py` |
| Production writers | No writer found for Normalized or Derived facts |
| Local normalized facts | 0 |
| Local normalized fact inputs | 0 |
| Local derived facts | 0 |
| Local derived fact inputs | 0 |
| Raw facts | 505; zero normalized/provenance links in this snapshot |
| Duplicate input-link groups | 0 in both input tables |
| SQLite FK check | 0 violations |
| Other environments/backups | Not audited |
| Migration 9 lineage | Still unresolved |
| Destructive retirement | Not authorized |

## 5. Next required design task

Proceed to **DB-DES-010 — Stage 5 canonical FinancialFact query migration contract**. It must map the current `forecast/queries.py` behavior to the proposed `financial_facts` model, explicitly defining:
- ReportVersion publication cutoff and point-in-time selection;
- FinancialPeriod identity, including Jalali period semantics;
- metric selection;
- dimension-set filtering and behavior when multiple dimension sets exist;
- NULL vs reported zero vs ZERO_FALLBACK;
- exact provenance carried into `ForecastInputRef`;
- integer/Decimal handling and where (if anywhere) conversion to floating-point is allowed;
- deterministic duplicate/version tie handling;
- no persisted derived outputs.

Do not change ORM, migration or runtime code until this contract and physical canonical schema are approved.

## 6. Scope and execution evidence

- The audit script was run by the owner against the local database.
- The database was opened in SQLite read-only mode.
- No schema or data rows were changed.
- No tests were run.
- This report is limited to the exact local database file identified above.
