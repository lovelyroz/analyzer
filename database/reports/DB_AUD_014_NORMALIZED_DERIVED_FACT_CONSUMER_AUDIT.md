# DB-AUD-014 — Normalized and Derived Financial Fact Consumer Audit

**Status:** SOURCE-CODE INVENTORY COMPLETE; LOCAL DATABASE LINKAGE REVIEW PARTIAL  
**Date:** 2026-11-18  
**Repository/ref reviewed:** `lovelyroz/analyzer` / `master`  
**Scope:** Read/write consumers of `NormalizedFinancialFact`, `NormalizedFinancialFactInput`, `DerivedFinancialFact`, and `DerivedFinancialFactInput`; compatibility implications for DB-DES-009  
**Method:** Read-only GitHub source-tree inventory and targeted inspection of all Python source, scripts, and tests in the current repository tree. No local SQLite database was opened.

## 1. Executive findings

1. **One production runtime reader of `NormalizedFinancialFact` was identified:** Stage 5 forecast query code in `src/forecast/queries.py`.
2. **No production writer of `NormalizedFinancialFact` was identified.** The current CODAL persistence function writes `RawFinancialFact`; the Excel Reader has no canonical persistence path.
3. **No production runtime reader or writer of `NormalizedFinancialFactInput` was identified.** It is a legacy provenance/schema model used by metadata registration, migrations and tests.
4. **No production runtime reader or writer of `DerivedFinancialFact` / `DerivedFinancialFactInput` was identified.** Their current repository role is persisted legacy schema/metadata and test coverage, not an active calculation path.
5. **Stage 5 is the critical consumer to migrate** from `normalized_financial_facts` to the proposed `financial_facts`.
6. The local DB-AUD-011 linkage audit found zero rows in `mapping_decisions`, `normalized_financial_fact_inputs`, and `normalized_financial_facts`; however, it did **not** establish row counts or linkage in `derived_financial_facts` and `derived_financial_fact_inputs`. The latter contains an FK to `normalized_financial_facts`. This remains a database-level migration gate.

## 2. Production source inventory

### 2.1 NormalizedFinancialFact — direct production consumer

**File:** `src/forecast/queries.py`

The Stage 5 read path:
- imports `FinancialMetric` and `NormalizedFinancialFact`;
- selects `NormalizedFinancialFact.value_irr` and `source_report_version_id`;
- joins to `FinancialMetric`, `ReportVersion`, and `FinancialPeriod`;
- filters by company, requested metric codes, and publication datetime <= forecast cutoff;
- groups/selects PIT-eligible facts and carries report-version/publication provenance into `ForecastInputRef`;
- skips NULL values and converts persisted numeric values to Python float for the existing forecast engine;
- declares `FACT_SOURCE = "normalized_financial_facts"`.

**Service caller:** `src/forecast/service.py::generate_forecast` invokes `load_financial_facts` and `load_financial_fact_periods`. It derives margins, opening equity, prior revenue, and dispersion context in memory, then returns a runtime `CompanyForecastResult`. It does not write derived financial facts.

**Migration impact:** this is the only identified production query that must be adapted to the new canonical table. It must preserve:
- PIT cutoff on ReportVersion publication datetime;
- correct selection across periods and report versions;
- exact ReportVersion provenance;
- metric-code filtering;
- NULL != zero semantics;
- all approved dimension filters/selection when the new fact identity is dimension-aware.

The current query does not select dimensions because the old table has no dimension-set identity. Stage 5's required dimension selection policy must be designed explicitly before replacing this query; it must not silently collapse multiple dimensioned facts into one metric value.

### 2.2 NormalizedFinancialFact — production writes

No production writer to `NormalizedFinancialFact` was found in the inspected `src/` production modules.

The current CODAL path in `src/ingestion/service.py::ingest_codal_report`:
- creates `Report` and `ReportVersion`;
- creates one `RawFinancialFact` for each `RawLineInput`;
- does not create `NormalizedFinancialFact`.

The Excel Reader currently provides DTO/observation reading only; no Excel-to-canonical writer was found. This is consistent with DB-AUD-013.

Therefore the current Stage 5 consumer depends on normalized rows that the inspected current production ingestion path does not create. The source audit does not identify the out-of-repository/manual process, if any, that may populate those rows.

### 2.3 NormalizedFinancialFactInput

**Model:** `src/models/normalized_provenance.py`

- Table `normalized_financial_fact_inputs`.
- Each row links one normalized fact to a raw fact and a mapping decision.
- Both `raw_fact_id` and `mapping_decision_id` are NOT NULL.
- The model has no identified production service reader or writer.
- The model is imported for SQLAlchemy metadata registration and created by Migration 3.
- `src/tests/test_stage1_database_architecture.py` explicitly tests one normalized fact composed from two raw inputs and verifies two provenance rows.
- `src/tests/test_stage1_database_integrity.py` checks that the table exists after migrations.

**Migration impact:** this model is not a suitable provenance bridge for the new Excel pipeline because it requires persistent RawFinancialFact and MappingDecision rows. Do not reuse it for the new writer. Keep it intact for legacy compatibility until a separately authorized retirement.

### 2.4 DerivedFinancialFact and DerivedFinancialFactInput

**Models:** `src/models/normalized.py`

- `derived_financial_facts` stores a persisted value, formula code/version, ReportVersion, quality status, cutoff and calculation timestamp.
- `derived_financial_fact_inputs` links a derived fact to either a normalized fact or another derived fact.
- `DerivedFinancialFactInput.normalized_fact_id` is an FK to `normalized_financial_facts.fact_id`; `derived_input_fact_id` is an FK to `derived_financial_facts.derived_fact_id`.
- No production calculation service, query, repository, or writer using these models was found in the inspected source.
- Both models are imported by `src/migrations/runner.py` and `src/scripts/init_db.py` for metadata registration; Migration 2 creates the tables.
- Stage 1 schema tests import these classes and assert table/migration presence, but the inspected tests do not establish an active production calculation path.

**Architecture conflict:** the owner-approved storage policy keeps analysis/calculation outputs runtime-only. These legacy derived tables represent persisted calculated outputs and should not be used by the new Excel canonical ingestion or new analytics pipeline. Their removal is not authorized by this audit; current rows and the FK from DerivedFinancialFactInput to NormalizedFinancialFact have not yet been audited in the local database.

## 3. Test and schema consumers

| File | Observed dependency | Required treatment |
|---|---|---|
| `src/tests/test_stage1_database_architecture.py` | Creates one NormalizedFinancialFact from two RawFinancialFact inputs; asserts two NormalizedFinancialFactInput rows | Preserve as legacy contract test until legacy schema retirement is authorized; add separate new-canonical provenance tests later |
| `src/tests/test_stage1_rules.py` | Tests NormalizedFinancialFact quality status and ReportVersion link; checks legacy table presence and migration compatibility | Preserve/retarget only in a dedicated legacy retirement task |
| `src/tests/test_stage1_database_integrity.py` | Asserts table presence and Migration 7/8 preservation of a normalized row with a raw fact | Preserve; this is data-preservation coverage, not a PDF extraction test |
| `src/tests/test_stage5_forecast.py` | Seeds normalized facts, exercises real Stage 5 database query/PIT path, records source rows before/after generation | Critical consumer integration suite; migrate fixtures and assertions to `financial_facts` only when the new writer/query contract is implemented; retain legacy preservation coverage separately |
| `src/migrations/runner.py` | Imports Normalized and Derived models for metadata; adds legacy columns and creates provenance/derived tables | Do not remove imports or table creation in this task; a future migration must explicitly preserve existing schema/data and separate new tables |
| `src/scripts/init_db.py` | Imports models before `Base.metadata.create_all` | Removing model imports changes fresh-database bootstrap; defer until an explicit retirement migration |
| `src/scripts/audit_legacy_raw_fact_links.py` | Inspects raw_fact_id linkage in normalized tables | Audit-only; not an application consumer |

No direct references to these four model classes/tables were found in the inspected KPI, scoring, trend, valuation, decision, market, Stage 6 evaluation, Excel Reader, FX, or market-ingestion production modules.

## 4. Current data-flow picture

```text
Legacy CODAL/PDF
    -> ingest_codal_report
    -> RawFinancialFact
    -> (no production NormalizedFinancialFact writer found)

NormalizedFinancialFact
    -> forecast/queries.py
    -> forecast/service.py
    -> runtime CompanyForecastResult
    -> Stage 7 / Stage 9 callers

NormalizedFinancialFactInput
    -> legacy schema/provenance only in inspected production source

DerivedFinancialFact / DerivedFinancialFactInput
    -> legacy schema only in inspected production source
    -> no active persisted derived-calculation caller found

New Excel Reader
    -> observations/DTO
    -> (canonical writer not yet established)
```

## 5. Implications for DB-DES-009

1. The proposed new `financial_facts` table is the appropriate target for the new Excel path; no production writer must be preserved for `normalized_financial_facts`.
2. Stage 5 `forecast/queries.py` is the primary production migration point. Its PIT behavior and source references must be preserved, and dimension-aware query semantics must be added.
3. Do not route new facts through `NormalizedFinancialFactInput`; its mandatory raw/mapping FKs conflict with the new minimal provenance model.
4. Do not build or persist new `DerivedFinancialFact` rows. Runtime calculations in Stage 5 already demonstrate the desired pattern for margins and historical context.
5. The legacy model imports in migration/bootstrap code must remain until the legacy tables can be retired safely.
6. Do not delete or weaken Stage 1/Stage 5 tests simply because the PDF path is being retired. Separate PDF extraction tests from database schema/preservation and Stage 5 query integration tests.
7. Stage 5 currently returns float values. New INTEGER storage can be read as integer, but any conversion to float must be assessed against the new canonical numeric contract and downstream forecast arithmetic; avoid unnecessary float conversion at the persistence/query boundary.
8. Existing Stage 5 source references use the literal `normalized_financial_facts`. When the new reader is introduced, update the runtime provenance label to the new source table/contract in the same change so audit output does not misidentify the source.

## 6. Local database evidence still required

DB-AUD-011 checked raw-fact references from:
- `mapping_decisions.raw_fact_id`
- `normalized_financial_fact_inputs.raw_fact_id`
- `normalized_financial_facts.raw_fact_id`

It did **not** check:
- total rows in `derived_financial_facts`;
- total rows in `derived_financial_fact_inputs`;
- count of `derived_financial_fact_inputs.normalized_fact_id` references;
- count of `derived_financial_fact_inputs.derived_input_fact_id` references;
- orphan/duplicate derived-input relationships;
- whether any normalized fact is referenced by a derived input;
- whether any derived fact is itself used as another derived fact's input.

These counts must be obtained from the exact local/target database before any table or FK retirement. Do not infer zero rows from the existing RawFinancialFact linkage audit.

## 7. Recommended next action

Create and run a separate read-only SQLite audit covering the two Derived tables and all their foreign-key/linkage distributions, plus the complete normalized/derived table counts on the target DB. This closes the remaining data-level gap without changing schema or rows.

After that, the next design task is a Stage 5 query migration contract: map old query behavior to dimension-aware `financial_facts`, define selection when more than one approved dimension set exists, and preserve PIT/report-version provenance. No production code should be changed before this query contract is explicit.

## 8. Scope and outcome

- Production source consumer inventory: COMPLETE for the inspected current repository tree.
- Stage 5 NormalizedFinancialFact reader: PRESENT.
- Production NormalizedFinancialFact writer: NOT FOUND.
- Production NormalizedFinancialFactInput reader/writer: NOT FOUND.
- Production DerivedFinancialFact / DerivedFinancialFactInput reader/writer: NOT FOUND.
- Legacy schema/bootstrap dependencies: PRESENT.
- Local Derived table/linkage evidence: PENDING.
- ORM, migration, runtime code, database rows, and tests: UNCHANGED.
- Tests run: NONE.


## 9. Read-only local database audit prepared

The follow-up script has now been added:

`src/scripts/audit_normalized_derived_fact_links.py`

Owner command from the repository root:

`python src/scripts/audit_normalized_derived_fact_links.py`

It opens `tehran_stock.db` in SQLite read-only mode and writes the results to `reply.md`. It reports counts for the four normalized/derived tables, all relevant references (including `derived_financial_fact_inputs.normalized_fact_id`), per-target linkage distributions, duplicate input-link groups and `PRAGMA foreign_key_check` output. Missing tables or columns are reported explicitly. It does not change schema or rows.

**Execution status:** script created and committed; owner execution and local database evidence are PENDING. No tests were run.
