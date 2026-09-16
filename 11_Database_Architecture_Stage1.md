# Stage 1 Database Architecture

## Status

**LOCKED - Stage 1 Database Architecture V1**

This document extends the locked Stage 1 contract. It does not replace the master architecture or introduce a new analytical stage.

## 1. Design Objective

The database must accept financial statements whose line-item titles and level of detail differ between companies and reporting periods, while preserving the original report and making comparable concepts available to downstream stages.

The design must support:

- Different titles for the same financial concept
- Different decomposition levels, such as three cost lines in one report and five in another
- Many raw lines mapping to one standard concept
- A raw line remaining unmapped until reviewed
- Reported, normalized, and derived values remaining distinguishable
- Complete Point-in-Time and provenance traceability

## 2. Existing Project Components

The current code already provides the first version of these layers:

| Current component | Responsibility |
|---|---|
| `RawFinancialFact` | Stores the original reported title and value |
| `FinancialMetric` | Current standard metric catalog |
| `NormalizedFinancialFact` | Stores a value linked to a standard metric |
| `ReportVersion` | Identifies the report version and publication time |
| `FinancialPeriod` | Identifies the financial period |

The explicit mapping decision between a raw line and a standard concept is part of this contract.

## 3. Logical Layers

```text
Source Report
    -> Raw Statement Line / Raw Financial Fact
    -> Mapping Decision
    -> Standard Financial Concept
    -> Normalized Financial Fact
    -> Derived Financial Fact
```

### 3.1 Raw layer

The raw layer preserves the source representation without changing the title or value. It must retain at least:

- `report_version_id`
- `period_id`
- original title
- original item code, when available
- original value
- unit and currency
- statement section
- source row and column
- extraction metadata

### 3.2 Standard concept layer

The standard catalog defines analytical concepts, not report-specific labels. Initial concepts should include:

- `REVENUE`
- `COGS`
- `GROSS_PROFIT`
- `OPERATING_EXPENSE`
- `OPERATING_PROFIT`
- `FINANCIAL_COST`
- `TAX_EXPENSE`
- `NET_PROFIT`
- `TOTAL_ASSETS`
- `TOTAL_EQUITY`
- `CASH_FROM_OPERATIONS`
- `CAPEX`

The catalog must also define:

- statement type
- parent concept, if applicable
- value type
- `FLOW` or `STOCK`
- currency and sign convention
- whether the value is reported or derived
- whether the concept is valid for a specific industry

### 3.3 Mapping decision layer

A mapping decision is a separate record connecting one raw line to one standard concept. It must include:

- raw fact identifier
- standard concept identifier
- mapping method
- confidence
- review status
- mapping rule/version
- reviewer and review timestamp, when manually reviewed
- transformation instructions, such as sign or unit conversion
- explanatory note

Required statuses:

- `AUTO_MAPPED`
- `REVIEW_REQUIRED`
- `APPROVED`
- `REJECTED`
- `UNMAPPED`

A raw line must not be treated as analytically usable merely because a candidate mapping exists.

### 3.4 Normalized layer

The normalized fact stores the value after the approved mapping and permitted transformations. It must point back to:

- the source report version
- the raw fact
- the standard concept
- the mapping decision
- the normalization rule
- quality status

The current implementation includes nullable `raw_fact_id` and `mapping_decision_id` foreign keys for backward compatibility with existing Stage 1 data and tests. New ingestion code must populate both links.

### 3.5 Derived layer

Derived facts are calculated from normalized facts and must never overwrite reported facts. Each derived result must store:

- target concept
- formula/version
- input facts
- calculation timestamp
- data cutoff
- quality result

Example:

```text
GROSS_PROFIT = REVENUE - COGS
OPERATING_PROFIT = GROSS_PROFIT - OPERATING_EXPENSE
NET_PROFIT = OPERATING_PROFIT - FINANCIAL_COST - TAX_EXPENSE
```

A reported `NET_PROFIT` and a calculated `NET_PROFIT` must be distinguishable and comparable for validation.

The current implementation represents this layer with `DerivedFinancialFact` and `DerivedFinancialFactInput`. Each derived fact stores its formula code, formula version, source report version, calculation cutoff, and quality status. Each input points to exactly one normalized or derived source fact.

## 4. Handling Different Line-Item Detail

The model supports many-to-one mappings:

```text
Direct Materials  ----\
Direct Labor       ----+--> COGS
Factory Overhead  ----/
```

If a report already provides `TOTAL_COST_OF_SALES`, that line can map directly to `COGS`. The system must prevent adding both the total and its already-included components to COGS unless the hierarchy explicitly identifies them as non-overlapping.

The mapping layer therefore needs a `composition_role` or equivalent rule to distinguish:

- component
- subtotal
- total
- disclosure-only line

This is a data-integrity rule, not a KPI rule.

## 5. Ingestion and Mapping Workflow

```text
1. Ingest report and create ReportVersion
2. Extract raw lines without changing titles or values
3. Identify candidate standard concepts
4. Apply unit, sign, and period checks
5. Store mapping decision and confidence
6. Route low-confidence or ambiguous lines to review
7. Approve only valid mappings
8. Create normalized facts from approved mappings
9. Calculate derived facts separately
10. Run reconciliation and quality checks
```

The process must fail visibly for `UNMAPPED` and ambiguous lines. It must not silently discard them or convert them to zero.

## 6. Example

One report may provide a single aggregate line:

```text
Aggregate cost line -> COGS
```

Another report may provide any number of component lines:

```text
Component A -> COGS (component)
Component B -> COGS (component)
Component N -> COGS (component)
```

Both structures can produce comparable standard concepts, while their original titles and decomposition remain available for audit. The model imposes no fixed number of source lines.

## 7. First Implementation Boundary

The schema change boundary for this architecture is the mapping foundation:

1. Formally treat `FinancialMetric` as the standard concept catalog.
2. Add a mapping-rule/version entity.
3. Add a mapping-decision entity.
4. Add explicit provenance links from normalized facts to raw facts and mapping decisions.
5. Add constraints for invalid statuses, mapping methods, composition roles, and confidence values.
6. Add tests for many-to-one mapping, unmapped data, raw-data immutability, and reported-versus-derived distinction.

These items are implemented in `src/models/normalized.py`, covered by Stage 1 tests, and included in the final audit described below.

No KPI, scoring, forecast, valuation, or decision logic should change in this step.

## 8. Acceptance Criteria

This step is accepted only when the design can answer all of the following:

- What was the original title in the report?
- Which standard concept was selected?
- Why was that mapping selected?
- Was it automatic or manually approved?
- What transformation was applied?
- Which report version and publication time supplied the value?
- Is the value reported, normalized, or derived?
- Can several source lines map to one concept without double counting?
- Can an unmapped line remain visible without entering analysis?

## 9. Ingestion Contract

Ingestion is an orchestration process, not a new analytical engine. Every run must create an `IngestionRun` record and follow this transaction boundary:

```text
STARTED
    -> report metadata and ReportVersion
    -> raw facts
    -> mapping decisions
    -> approved normalized facts
    -> derived facts and reconciliation
COMPLETED / FAILED
```

The raw layer is written before normalization. A normalization or mapping failure must not mutate or delete the raw record. Failed or ambiguous rows remain queryable with their failure or review status.

The ingestion service must maintain these counters on `IngestionRun`:

- records found
- records inserted
- records updated
- records failed
- error summary

Updates to an existing report must create a new `ReportVersion` when the published content changes. Existing versions and their downstream facts are immutable historical evidence.

## 10. Migration Policy

`Base.metadata.create_all()` is permitted only for an empty development/bootstrap database. It is not the production migration mechanism and must not be used to alter or delete existing tables.

Every schema change must use a numbered migration with:

- migration identifier and version
- forward upgrade operation
- downgrade policy or explicit irreversible marker
- data backfill rule, when required
- compatibility check for existing Stage 1 and downstream contracts
- migration test against a representative existing database

The first migration after the original schema must add, in order:

1. standard concept metadata columns;
2. `mapping_rules`;
3. `mapping_decisions`;
4. normalized-fact provenance links;
5. `derived_financial_facts`;
6. `derived_financial_fact_inputs`.

No migration may reinterpret an existing raw value or silently convert a missing value to zero. Existing rows receive nullable provenance fields until an explicit, auditable backfill can establish their source mapping.

## 11. Current Implementation Boundary

The current repository supports bootstrap creation through `src/scripts/init_db.py`, including the mapping and derived-fact tables. The raw Codal ingestion boundary is implemented in `src/ingestion/service.py`: it records `IngestionRun`, creates or reuses report identity, creates a new immutable `ReportVersion`, and persists extracted lines without mapping them. Mapping and normalization remain separate downstream operations.

A versioned migration runner is now implemented in `src/migrations/runner.py`, with the command `src/scripts/migrate_db.py`. It records schema versions in `schema_migrations`, supports a legacy baseline, applies the mapping/derived schema upgrade without rewriting existing values, and is idempotent. Migration behavior is covered by Stage 1 tests.

The migration runner is intentionally limited to the current SQLite/SQLAlchemy deployment. A broader multi-database migration policy would require a separate architectural decision.

## 12. Final Architecture Audit

Audit status: **PASS**

The final review confirmed:

- raw titles and values are preserved;
- standard concepts are separate from report-specific labels;
- mapping decisions retain method, confidence, review status, and rule version;
- normalized facts retain raw and mapping provenance when produced by the new pipeline;
- derived facts retain formula version, cutoff, and input provenance;
- report versions remain point-in-time selectable and historical versions are not overwritten;
- ingestion failures roll back partial report/raw writes and retain a failed run record;
- migrations are versioned, idempotent, and tested for empty and legacy databases;
- no KPI, scoring, forecast, valuation, or decision logic was moved into the database foundation;
- no fixed number of source lines is assumed;
- `NULL` remains distinct from zero.

The Stage 1 database architecture is locked at V1. Any contract-breaking change must be recorded in `99_Architecture_Change_Log.md` and assigned a new architecture or contract version.
