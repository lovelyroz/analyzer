# Analyzer V1 — Database Architecture V1.1

## Status

**LOCKED — DATABASE CONTRACT V1.1**

**Audit status:** Architecture re-audit PASS pending final CI verification after the V1.1 changes.

**Database engine:** SQLite

**ORM:** SQLAlchemy

**Schema migration version:** 4

This document supersedes `12_Database_Architecture_V1.md` as the current database architecture reference. It implements the locked Stage 1 contract and supports Stages 2–9 without moving analytical ownership into the database.

---

## 1. Purpose

The database is the auditable Data Foundation. It stores source reports, financial periods, raw financial facts, standardized concepts, mapping decisions, normalized/derived facts, FX, market data, share history, corporate actions, data quality, and ingestion audit information.

The database must be:

- Point-in-Time correct;
- reproducible;
- source-traceable;
- tolerant of heterogeneous report titles and detail levels;
- safe against silent data loss, silent substitution, look-ahead bias, and aggregate/component double counting.

It is not a replacement for KPI, scoring, trend, forecast, evaluation, valuation, market, or decision engines.

---

## 2. Logical Architecture

```text
External Sources
  ├─ Codal financial reports
  ├─ Daily market data
  └─ FX data
          ↓
Ingestion + Audit
          ↓
Raw Source Layer
          ↓
Mapping Decision Layer
          ↓
Standard Concept Catalog
          ↓
Normalized Fact Layer
          ↓
Derived Fact + Reconciliation Layer
          ↓
Stages 2–9
```

Market and FX foundations remain separate branches and are consumed by their appropriate downstream stages.

---

## 3. Core Domains

### Entity

- `industries`
- `companies`
- `financial_periods`

Company identity is stable and is not based only on ticker. The implementation also preserves an optional national identifier.

### Report / PIT

- `reports`
- `report_versions`

`Report` identifies the logical report. `ReportVersion` identifies a published historical state. Publication datetime belongs to `ReportVersion`.

### Financial normalization

- `raw_financial_facts`
- `financial_metrics`
- `mapping_rules`
- `mapping_decisions`
- `normalized_financial_facts`
- `normalized_financial_fact_inputs`
- `derived_financial_facts`
- `derived_financial_fact_inputs`

### Market / FX / ownership

- `market_daily`
- `fx_rates`
- `fx_conversion_rules`
- `share_count_history`
- `corporate_actions`

### Audit

- `ingestion_runs`
- `schema_migrations`

---

## 4. Raw Financial Facts

Raw facts are source evidence. They preserve the original item title, code, value, unit, currency, statement location, period, and report version.

Raw data is never overwritten by normalization.

`NULL` remains distinct from zero.

An unmapped raw line remains queryable and is not silently converted to a usable analytical value.

---

## 5. Standard Concept Catalog

`financial_metrics` is the controlled catalog of standard financial concepts.

It supports:

- unique `metric_code`;
- statement type;
- parent concept hierarchy;
- value type;
- `FLOW` / `STOCK` classification;
- sign convention;
- derived-vs-reported metadata;
- optional industry scope.

Source-specific report labels are mapped to these concepts rather than becoming uncontrolled schema columns.

---

## 6. Mapping Decisions

`mapping_decisions` records the explicit relationship between a raw line and a standard concept.

It records mapping method, confidence, review status, mapping rule/version, composition role, transformation specification, reviewer metadata, and explanatory notes.

Allowed methods:

- `TITLE_EXACT`
- `ALIAS`
- `PATTERN`
- `POSITION`
- `MANUAL`
- `DERIVED`

Allowed review states:

- `AUTO_MAPPED`
- `REVIEW_REQUIRED`
- `APPROVED`
- `REJECTED`
- `UNMAPPED`

Allowed composition roles:

- `COMPONENT`
- `SUBTOTAL`
- `TOTAL`
- `DISCLOSURE`

A candidate mapping is not analytically usable until its review state permits it.

---

## 7. Normalized Facts and Multi-Source Provenance

`NormalizedFinancialFact` stores the standardized concept-level value for a company, period, metric, and report version.

The same standard concept may be supported by one raw line or multiple non-overlapping raw lines.

`NormalizedFinancialFactInput` is the authoritative provenance bridge for new multi-source normalized values:

```text
Raw A ─┐
Raw B ─┼──> Normalized COGS
Raw N ─┘
```

Each bridge row records:

- normalized fact;
- raw fact;
- mapping decision;
- input role.

The existing nullable direct provenance fields on `NormalizedFinancialFact` remain for compatibility and direct-source convenience.

A normalized value must never lose the identity of its contributing raw facts.

### Aggregate/component rule

When a report contains both an aggregate and its components, the normalization/resolution process must choose the valid aggregate or the valid non-overlapping components according to explicit composition roles. It must never sum an aggregate together with components already included in that aggregate.

---

## 8. Derived Facts

`DerivedFinancialFact` is separate from reported/normalized values.

Every derived result retains:

- target metric;
- formula code and version;
- source report version;
- calculation cutoff;
- calculation timestamp;
- quality status.

`DerivedFinancialFactInput` preserves the normalized/derived inputs used by the formula.

Derived facts never overwrite reported or normalized evidence.

---

## 9. Financial Periods and TTM

`FinancialPeriod` supports MONTH, QUARTER, SEMI_ANNUAL, NINE_MONTH, ANNUAL, and TTM.

TTM is derived from underlying periods and is not treated as a raw Codal reporting period.

Historical TTM reconstruction must respect the Point-in-Time information set.

---

## 10. Report Versions and Point-in-Time

For cutoff `T`, only `ReportVersion.publication_datetime <= T` is eligible.

Corrections/restatements create distinct versions. Earlier versions remain immutable historical evidence.

Current analysis may use the latest valid version; historical backtesting must use the version that was actually available at the historical cutoff.

A report cannot have more than one current version. This is enforced by a unique partial index on `report_versions(report_id)` where `is_current_version = 1`.

Migration 4 refuses to apply if existing data contains multiple current versions for one report, rather than silently repairing the historical state.

---

## 11. FX Architecture

IRR is the accounting base currency. USD is derived.

The database preserves distinct FX rate types, including:

- `FREE_MARKET`
- `OPERATIONAL`
- `OFFICIAL`
- `ESTIMATED`
- `MANUAL_OPERATOR`

Default conversion policy:

- FLOW → period-average FX;
- STOCK → period-end FX;
- MARKET_VALUE → same-date FX.

Operational FX must not silently fall back to free-market FX. Any proxy must be explicit and quality-marked.

---

## 12. Market and Share Foundations

`market_daily` preserves raw close and adjusted close separately and is unique per company/trading date.

Stage 8 owns market analysis; Stage 1 only stores the foundation.

Historical share counts and corporate actions are preserved so EPS comparability and historical valuation can account for changes in shares outstanding.

---

## 13. Ingestion Boundary

Raw Codal ingestion is an orchestration/data-preservation operation:

```text
IngestionRun
  → Report
  → ReportVersion
  → RawFinancialFact
```

Mapping, normalization, derived calculations, and reconciliation remain separate operations.

A failed raw ingestion must not leave partial report/raw writes. The failed run itself remains auditable.

---

## 14. Migration Policy

`Base.metadata.create_all()` is permitted only for an empty development/bootstrap database.

Production/schema evolution uses the versioned migration runner:

`python -m src.scripts.migrate_db`

Current schema versions:

| Version | Name |
|---|---|
| 1 | `baseline_schema` |
| 2 | `mapping_and_derived_schema` |
| 3 | `normalized_fact_multi_source_provenance` |
| 4 | `one_current_report_version` |

Migrations are ordered and idempotent. Existing raw values are not silently rewritten.

No automatic backfill of the new provenance bridge is performed when the historical mapping cannot be established safely.

---

## 15. Ownership Boundaries

The database owns:

- source preservation;
- report identity/versioning;
- periods;
- standard concept metadata;
- mapping decisions;
- normalization provenance;
- derived-fact provenance;
- data quality and ingestion audit;
- market/FX/share/corporate-action foundations.

The database does not own:

- KPI scoring;
- Fundamental Score;
- trend state calculation;
- forecast model logic;
- forecast reliability;
- valuation decisions;
- Market Score or trading signals;
- final Buy/Sell/Hold rules.

---

## 16. V1.1 Audit Result

The post-implementation architecture review identified and corrected two integrity gaps:

1. multi-source normalized provenance was not physically representable through one direct raw-fact foreign key;
2. the schema did not enforce at most one current `ReportVersion` per logical report.

Both are now addressed without changing the nine-stage analytical architecture.

Required verification after these changes:

- Stage 1 and full test suite;
- migration tests for fresh and legacy databases;
- multi-source provenance test;
- one-current-version constraint test;
- `git diff --check`;
- actual CI workflow evidence.

Until the new CI run is observed, this document must not be reported as CI-verified PASS.

---

## 17. Version

`database_contract_version = DATABASE_CONTRACT_V1.1`

Overall Analyzer architecture remains **V1** with exactly nine analytical stages.
