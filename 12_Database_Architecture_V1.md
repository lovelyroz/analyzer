# Analyzer V1 - Database Architecture

## Status

**LOCKED - Database Architecture V1**

**Audit status:** PASS

**Schema migration version:** 2

**Database engine:** SQLite

**ORM:** SQLAlchemy

This document is the database architecture reference for the Analyzer V1 project. It implements the locked Stage 1 contract and supports Stages 2 through 9 without moving their analytical ownership into the database layer.

---

## 1. Purpose

The database stores financial reports, market data, FX data, normalized financial facts, and their provenance in a form that is:

- point-in-time correct;
- auditable;
- reproducible;
- tolerant of different report titles and detail levels;
- compatible with industry-specific analysis;
- safe against silent data loss, silent substitution, and look-ahead bias.

The database is a data foundation. It is not a replacement for the KPI, scoring, trend, forecast, valuation, market, or decision engines.

## 2. Core Principles

### 2.1 Raw data is immutable evidence

Source titles, values, units, currencies, locations, and report versions are preserved. Normalization never overwrites raw data.

### 2.2 A missing value is not zero

Unavailable, unreported, or unextractable values remain `NULL` and carry an appropriate quality or review status.

### 2.3 Point-in-Time correctness is mandatory

Every financial observation is tied to both a financial period and a report version with a publication/availability datetime. Historical analysis may use only information available at its cutoff.

### 2.4 Report versions are historical evidence

A correction or restatement creates a new `ReportVersion`. Earlier versions and facts remain queryable and are never overwritten.

### 2.5 Standard concepts are separate from source labels

A report-specific title is not a database concept. It is mapped to a standard financial concept through an explicit, reviewable mapping decision.

### 2.6 Reported, normalized, and derived values are distinct

A value printed in a report, a value after approved normalization, and a value calculated by a formula must not be stored as interchangeable facts.

### 2.7 No fixed number of source lines

A statement may contain any number of lines and any level of decomposition. The schema imposes no fixed line count or fixed report layout.

---

## 3. Logical Architecture

```text
External Sources
    |
    +-- Codal financial reports
    +-- Daily market data
    +-- FX data
    |
    v
Ingestion and Audit
    |
    v
Raw Source Layer
    |
    v
Mapping Decision Layer
    |
    v
Standard Concept Catalog
    |
    v
Normalized Fact Layer
    |
    v
Derived Fact and Reconciliation Layer
    |
    v
Stages 2-9 analytical engines
```

The database also stores market and FX foundations as separate branches:

```text
MarketDaily --------------> Stage 8 Market Engine
FXRate / FX rules --------> Stage 5, Stage 7, Stage 8/9 context
Financial facts ----------> Stages 2-7 and Stage 9
```

The fundamental and market branches are not combined in the database into a single score or signal.

---

## 4. Schema Domains

### 4.1 Entity domain

| Table | Purpose |
|---|---|
| `industries` | Industry hierarchy and stable industry codes |
| `companies` | Stable company identity, ticker, symbol, and industry link |
| `financial_periods` | Financial period boundaries and period type |

Company identity is not based only on ticker. Tickers can change while the company identity remains stable.

### 4.2 Report and Point-in-Time domain

| Table | Purpose |
|---|---|
| `reports` | Logical report identity and source metadata |
| `report_versions` | Published versions, restatements, publication time, and supersession chain |
| `schema_migrations` | Applied database schema versions |

`Report` describes the logical report. `ReportVersion` describes the published historical state of that report.

### 4.3 Raw and normalized financial domain

| Table | Purpose |
|---|---|
| `raw_financial_facts` | Original extracted report lines and values |
| `financial_metrics` | Standard financial concept catalog |
| `mapping_rules` | Versioned rules used to identify or transform concepts |
| `mapping_decisions` | Decision connecting a raw line to a standard concept |
| `normalized_financial_facts` | Approved and normalized analytical facts |
| `derived_financial_facts` | Formula-generated facts |
| `derived_financial_fact_inputs` | Provenance links from derived facts to their inputs |

### 4.4 Market, FX, and corporate-action domain

| Table | Purpose |
|---|---|
| `market_daily` | Daily OHLC, adjusted prices, volume, value, and trade count |
| `fx_rates` | FX observations with source and rate type |
| `fx_conversion_rules` | FLOW, STOCK, and MARKET_VALUE conversion policies |
| `share_count_history` | Historical shares outstanding and capital |
| `corporate_actions` | Capital increases and other share-related events |

Free-market FX and operational/exchange FX remain separate data types and sources.

### 4.5 Operational audit domain

| Table | Purpose |
|---|---|
| `ingestion_runs` | Ingestion status, counters, timestamps, and error summary |

---

## 5. Core Data Flow

```text
1. Receive source report
2. Create or identify Report
3. Create a new ReportVersion
4. Extract source rows without changing their titles or values
5. Store RawFinancialFact rows
6. Generate MappingDecision candidates
7. Review or approve mappings
8. Produce NormalizedFinancialFact rows
9. Produce DerivedFinancialFact rows with formula and input provenance
10. Reconcile totals and quality statuses
11. Expose only valid, point-in-time eligible facts to analytical stages
```

The raw ingestion service currently implements steps 1 through 5. Mapping, normalization, derived calculations, and reconciliation remain separate responsibilities and must not be hidden inside raw ingestion.

---

## 6. Standard Concept Catalog

`financial_metrics` is the standard concept catalog. A concept is identified by a unique `metric_code`, not by a report title.

A concept may define:

- `statement_type`: `INCOME`, `BALANCE_SHEET`, `CASH_FLOW`, `EQUITY`, or `GENERAL`;
- `parent_metric_id` for conceptual hierarchy;
- `value_type`, such as currency or per-share value;
- `flow_or_stock`: `FLOW` or `STOCK`;
- `sign_convention`;
- `is_derived`;
- optional industry scope.

Initial concept families include:

- revenue;
- cost of goods sold;
- gross profit;
- operating expenses;
- operating profit;
- financial cost;
- tax expense;
- net profit;
- assets, liabilities, and equity;
- operating cash flow;
- capital expenditure;
- earnings per share.

The catalog is extensible by adding concepts; source-specific labels are added through mapping rules, not by creating uncontrolled columns.

---

## 7. Mapping Architecture

`MappingDecision` connects one raw fact to a candidate or approved standard concept.

It records:

- raw fact;
- standard metric, when known;
- mapping rule and version;
- mapping method;
- confidence from 0 to 100;
- review status;
- composition role;
- transformation specification;
- reviewer and review time;
- explanatory note.

### 7.1 Mapping methods

- `TITLE_EXACT`
- `ALIAS`
- `PATTERN`
- `POSITION`
- `MANUAL`
- `DERIVED`

### 7.2 Review statuses

- `AUTO_MAPPED`
- `REVIEW_REQUIRED`
- `APPROVED`
- `REJECTED`
- `UNMAPPED`

Only approved and valid mappings may create analytical normalized facts. Unmapped and ambiguous rows remain visible for review and do not silently enter downstream analysis.

### 7.3 Composition roles

- `COMPONENT`
- `SUBTOTAL`
- `TOTAL`
- `DISCLOSURE`

These roles prevent double counting when an aggregate line and its components coexist in the same report.

### 7.4 Flexible detail

Any number of source lines may map to one concept. For example, several cost components may contribute to `COGS`, while another report may provide one aggregate cost line. The original decomposition is always preserved.

---

## 8. Normalized Facts

`normalized_financial_facts` stores values after approved mapping and permitted transformations.

Each new normalized fact should carry:

- company;
- period;
- standard metric;
- raw fact provenance;
- mapping decision provenance;
- source report version;
- normalization rule;
- value in the declared base currency;
- quality status.

Supported quality states include:

- `VALID`
- `MISSING`
- `ESTIMATED`
- `RESTATED`
- `SUSPICIOUS`
- `UNMAPPED`

Existing provenance columns are nullable for backward compatibility. New pipeline writes must populate them.

---

## 9. Derived Facts and Reconciliation

`derived_financial_facts` stores calculated values separately from reported and normalized values.

Each derived fact includes:

- target metric;
- calculated value;
- formula code;
- formula version;
- source report version;
- data cutoff datetime;
- calculation timestamp;
- quality status.

`derived_financial_fact_inputs` records each input as either a normalized fact or another derived fact, never both in one input row.

Typical formulas include:

```text
GROSS_PROFIT = REVENUE - COGS
OPERATING_PROFIT = GROSS_PROFIT - OPERATING_EXPENSE
NET_PROFIT = OPERATING_PROFIT - FINANCIAL_COST - TAX_EXPENSE
```

Reported and calculated versions of the same concept can therefore be compared without overwriting either one.

Reconciliation must identify:

- missing inputs;
- sign conflicts;
- unit conflicts;
- duplicate totals and components;
- mismatch between reported and calculated subtotals;
- insufficient point-in-time evidence.

A reconciliation warning must be recorded as quality information, not silently repaired.

---

## 10. Ingestion and Transaction Rules

Every ingestion run creates an `IngestionRun` record.

```text
STARTED
  -> report metadata
  -> report version
  -> raw facts
  -> mapping/normalization steps
  -> derived facts and reconciliation
COMPLETED or FAILED
```

The implemented raw Codal service:

- creates or reuses logical report identity;
- creates a new report version;
- marks the previous current version as non-current;
- preserves previous raw facts;
- stores extracted lines unchanged;
- preserves `NULL` values;
- records success or failure counters;
- rolls back partial report/raw writes on failure;
- records a failed ingestion run.

A failed normalization or mapping step must not delete the raw source record.

---

## 11. Point-in-Time and Versioning Rules

For a cutoff datetime `T`:

- a `ReportVersion` is eligible only when its publication datetime is on or before `T`;
- future report versions must not be selected;
- restated versions remain distinct;
- derived facts must retain their calculation cutoff;
- analytical outputs must retain the relevant data and model metadata.

The database supports historical backtesting by preserving both the financial period and the information availability timeline.

---

## 12. Migration and Bootstrap

`Base.metadata.create_all()` is for empty development/bootstrap databases only.

The versioned migration runner is:

```text
src/migrations/runner.py
```

The command is:

```text
python -m src.scripts.migrate_db
```

Current schema versions:

| Version | Name | Responsibility |
|---|---|---|
| 1 | `baseline_schema` | Initial database schema |
| 2 | `mapping_and_derived_schema` | Concept metadata, mapping, provenance, and derived-fact tables |

The runner:

- records applied versions in `schema_migrations`;
- supports a legacy schema baseline;
- applies migrations in order;
- does not rewrite existing raw values;
- is idempotent;
- is tested against empty and legacy SQLite databases.

A contract-breaking schema change requires a new migration and an entry in `99_Architecture_Change_Log.md`.

---

## 13. Ownership Boundaries

The database owns:

- source preservation;
- report identity and versioning;
- period identity;
- standard concept metadata;
- mapping decisions;
- normalization provenance;
- derived-fact provenance;
- data quality and ingestion audit;
- market, FX, share, and corporate-action foundations.

The database does not own:

- KPI scoring logic;
- Fundamental Score calculation;
- trend state calculation;
- forecast model logic;
- forecast reliability calculation;
- valuation decisions;
- market score or trading signal;
- final Buy/Sell/Hold rules.

Those responsibilities remain in their respective Stage engines.

---

## 14. Security and Integrity Rules

The implementation must preserve these invariants:

- raw source data is not overwritten;
- `NULL` is not converted to zero;
- future report versions are not used historically;
- operational FX is not silently replaced by free-market FX;
- unmapped facts are not silently normalized;
- old model and report versions remain reproducible;
- duplicate aggregate/component values are not blindly summed;
- every material normalized or derived value is traceable to its inputs;
- schema changes are versioned;
- analytical stages do not recreate upstream database transformations without explicit justification.

---

## 15. Final Audit

**Result: PASS**

Verified evidence:

- Stage 1 tests pass;
- full project suite passes with 123 tests;
- migration runner passes fresh-database and legacy-database tests;
- current project database is migrated to schema version 2;
- Pylance reports no errors in the changed implementation files;
- `git diff --check` passes;
- no fixed report line count is assumed;
- raw, normalized, and derived layers remain distinct.

This database architecture is locked at V1. Future contract changes must be explicitly versioned and recorded through the project change log.
