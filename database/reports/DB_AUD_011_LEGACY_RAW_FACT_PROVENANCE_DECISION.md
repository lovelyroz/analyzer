# DB-AUD-011 — Legacy RawFinancialFact Provenance Assessment

**Date:** 2026-11-18  
**Status:** AUDIT COMPLETE; MIGRATION / DELETION NOT AUTHORIZED  
**Scope:** Read-only review of the local SQLite provenance audit output and current GitHub ORM/application references.

## 1. Evidence reviewed

The owner ran `src/scripts/audit_legacy_raw_fact_provenance.py` against the local database `tehran_stock.db`. The report was returned in `reply.md`.

- `raw_financial_facts` contains 505 rows.
- All five audited provenance columns exist and contain non-NULL values in at least some rows.
- Three tables have foreign keys referencing `raw_financial_facts.raw_fact_id`.
- Current application source references were searched under `src`, excluding `src/scripts`.

This report records findings and architectural disposition only. It does not claim that the local database and current GitHub source are from the same revision; Migration 9 reconciliation remains unresolved.

## 2. Field-level findings

| Field | Non-NULL rows | Distinct non-NULL values | Current source-code references outside scripts | Finding |
|---|---:|---:|---|---|
| `source_sheet` | 505 | 1 | None found | Legacy worksheet provenance; current value is always `Recovered_Sheet1`. |
| `source_column_header` | 505 | 23 | None found | Legacy captured header/context text. Values combine temporal, measure, unit, and audit qualifiers in one string. |
| `source_section` | 245 | 9 | Yes | Still referenced by ingestion service, CODAL adapter, PDF extraction path, and tests. |
| `source_row` | 505 | 336 | Yes | Still referenced by service, adapter/parser, PDF extraction path, and tests. |
| `source_column` | 505 | 15 | Yes | Still referenced by service, adapter/parser, PDF extraction path, and tests. |

The ORM model in the current GitHub source defines `source_section`, `source_row`, and `source_column`, but does not define `source_sheet` or `source_column_header`. The latter two therefore remain a schema/model discrepancy requiring Migration 9 lineage reconciliation.

## 3. Referential dependencies

The local database reports these foreign-key references to `raw_financial_facts.raw_fact_id`:

- `mapping_decisions.raw_fact_id`
- `normalized_financial_fact_inputs.raw_fact_id`
- `normalized_financial_facts.raw_fact_id`

All are configured with `NO ACTION` on delete. These references make raw-fact deletion a data-integrity operation, not a harmless cleanup. This audit did not count linked/unlinked rows or inspect the semantic validity of the downstream records; no deletion or rewrite is authorized.

## 4. Architectural disposition for the new Excel ingestion design

The future Excel pipeline should not treat the legacy provenance columns as its canonical layout model.

| Legacy field | Target-design treatment | Reason |
|---|---|---|
| `source_sheet` | Represent worksheet identity through the versioned Template's worksheet record and matching rule. Retain the legacy column/data for historical compatibility until a separately approved migration. | A single sheet name is not a stable canonical identity; worksheet matching belongs to the Template version. |
| `source_column_header` | Do not use as a canonical fact key or as a replacement for structured Header definitions. Represent header ranges/levels, column slots, temporal axes, units/basis, and semantic mappings explicitly. Retain historical values unchanged. | The observed strings conflate multiple independent dimensions and are not normalized identifiers. |
| `source_section` | Treat as legacy source context for the existing ingestion/PDF path. Do not extend it as the Excel table/sub-table identity. New Excel ingestion should use stable Template table/sub-table IDs. | The field is actively referenced in current code, but its free-text section names are not stable structural IDs. |
| `source_row`, `source_column` | Keep for legacy records and compatibility. For new Excel ingestion, use exact worksheet + cell/range coordinates associated with the approved Template extraction definition and provenance contract; do not assume legacy row/column semantics are interchangeable with Excel A1 coordinates. | Existing values are heterogeneous source locators and the current code normalizes them in legacy adapters. |

### Important boundary

The Template's worksheet, layout node, header/range, column-slot, and extraction-span records describe the approved source layout. They do not automatically provide complete per-fact lineage for every persisted financial input. Before implementation, the design must specify how a selected canonical fact points back to its exact source cell(s), including cases where one fact is composed from multiple cells. Do not solve this by storing an opaque concatenated header string or by overloading `source_section`.

The existing `raw_financial_facts` table is a legacy persistence structure and has downstream references. The new architecture's policy against retaining raw financial-row archives must be implemented as a deliberate pipeline/schema transition, not by deleting this table or its columns during Template creation.

## 5. Decisions and prohibitions

1. Preserve all 505 existing raw facts and all five provenance columns unchanged for now.
2. Do not drop `source_sheet`, `source_column_header`, `source_section`, `source_row`, or `source_column` in the next migration.
3. Do not add the two missing ORM attributes merely to mirror the local database until Migration 9's exact DDL, code revision, and source lineage are reconciled.
4. Do not use free-text `source_column_header` as a metric, period, unit, or canonical column identifier.
5. Do not use `source_section` as the future Template table/sub-table ID.
6. Keep the legacy ingestion/PDF references isolated from the new Excel-only path; any removal of PDF-specific code must be a separate scoped change with its own dependency/test review.
7. Before any legacy-table retirement, inspect row-level linkage and determine whether mapping/normalized records can be retained with sufficient provenance after transition.

## 6. Next required audit

The next step is a focused **row-linkage and lineage-impact audit** of the 505 legacy raw facts:

- count how many raw facts are referenced by each of the three downstream tables;
- count raw facts with zero, one, or multiple downstream references;
- identify duplicate or orphaned reference patterns without changing data;
- determine whether normalized records can survive independently of raw facts and what provenance they would lose;
- inspect the current Excel ingestion/persistence call path to establish whether it still writes `RawFinancialFact` or has a separate canonical persistence path.

This is required before deciding whether the legacy raw-fact table is retained indefinitely, frozen as historical compatibility data, or retired through a controlled migration.

## 7. Completion status

- Provenance population and code-reference audit: **COMPLETE**.
- Field-level target-design disposition: **RECORDED, subject to implementation design**.
- Migration 9 source/revision reconciliation: **OPEN**.
- Downstream row-linkage audit: **NEXT**.
- ORM changes, migrations, data updates, and tests: **NONE**.

## 8. Confirmed current persistence path

The current GitHub source was inspected after the local audit:

- `src/ingestion/service.py` imports `RawFinancialFact`.
- `ingest_codal_report(...)` creates one `RawFinancialFact` object for each `RawLineInput` and calls `session.add_all(facts)`.
- The created records include `source_section`, `source_row`, and `source_column`.
- `src/ingestion/codal/adapter.py` is explicitly a PDF extraction boundary and produces `RawLineInput` values from PDF extraction.
- The current migration runner imports `RawFinancialFact` and has migrations only through version 8.

Therefore, the currently inspected CODAL persistence route writes to `raw_financial_facts`; it is the legacy PDF-oriented route, not evidence that the new Excel pipeline has been implemented. A separate production Excel-to-canonical persistence path was not established by this inspection.

## 9. Row-linkage audit script

A second read-only script was added:

`src/scripts/audit_legacy_raw_fact_links.py`

It counts downstream rows and distinct raw facts referenced by `mapping_decisions`, `normalized_financial_fact_inputs`, and `normalized_financial_facts`; computes per-raw-fact and combined linkage distributions; and checks dangling non-NULL references. It does not change the database and writes its report to `reply.md`.

Run from repository root:

`python src/scripts/audit_legacy_raw_fact_links.py`

The resulting counts are required before any legacy-table retirement decision. Zero references do not by themselves authorize deletion.


## 10. Row-linkage audit result and disposition

The owner ran `src/scripts/audit_legacy_raw_fact_links.py` against the local database and supplied the resulting `reply.md`.

| Referencing table | Total rows | Non-NULL raw_fact_id | Distinct raw facts referenced |
|---|---:|---:|---:|
| `mapping_decisions` | 0 | 0 | 0 |
| `normalized_financial_fact_inputs` | 0 | 0 | 0 |
| `normalized_financial_facts` | 0 | 0 | 0 |

All 505 raw facts have zero references in each table and zero combined references. No dangling non-NULL references were found. No rows were changed.

### Interpretation

- The three FK-bearing downstream tables exist in the inspected local database, but are empty.
- There are no current normalized facts or mapping decisions in these tables whose lineage would be lost by removing the 505 raw facts.
- This is a statement about the current database snapshot only. It does not prove that other databases, environments, exports, backups, or uninspected consumers have no dependency.
- The result does not authorize deletion: the current source still contains a PDF-oriented CODAL path that writes new `RawFinancialFact` rows.
- The Excel package currently exposes source observation DTOs and a reader; the inspected package does not establish a production Excel-to-canonical persistence route.

### Updated disposition

1. Keep all 505 legacy rows and all five provenance columns unchanged for now.
2. Do not add, alter, or drop ORM fields or migrations as part of this audit.
3. Treat the current three downstream tables as empty legacy schema in this local database; do not build new Excel ingestion on top of their raw-fact FK design without an explicit architecture decision.
4. Before retiring `raw_financial_facts`, separately decide and implement the already-planned retirement of the PDF extraction/ingestion path, including public facades, pipeline entry points, callers, tests, and migration-runner imports. A write-capable legacy path must not remain after its target table is retired.
5. Before any destructive migration, re-run the linkage audit against the exact database being migrated and verify all relevant environments/backups and any external consumers.
6. Preserve report/version metadata only if its role in the new Excel model is explicitly defined; zero downstream raw-fact links do not establish that Report/ReportVersion are unused.

### Completion status

- Current local row-linkage counts: **COMPLETE**.
- Current PDF-oriented write path confirmed in source: **PRESENT**.
- Production Excel-to-canonical persistence path: **NOT ESTABLISHED**.
- Legacy raw-fact retirement: **NOT AUTHORIZED**.
- Migration 9 source/revision reconciliation: **OPEN**.
- ORM changes, migrations, data updates, and tests: **NONE**.
