# Stage 1 — Database Architecture Principles

## Status

**LOCKED — DESIGN PRINCIPLES**

This document defines the Stage 1 database design intent and boundaries. The physical schema is defined by `12_Database_Architecture_V1.1.md`. Approved contract changes are recorded in `99_Architecture_Change_Log.md`.

## 1. Objective

The database must accept heterogeneous Codal financial statements while preserving source evidence and producing auditable standardized concepts for downstream stages.

It must support:

- different titles for the same economic concept;
- different decomposition levels between companies and periods;
- many raw lines contributing to one standard concept;
- unmapped and ambiguous source lines remaining visible;
- separation of reported, normalized, and derived values;
- Point-in-Time reconstruction;
- complete provenance and data-quality traceability.

## 2. Logical Flow

```text
Source Report
  ↓
ReportVersion
  ↓
RawFinancialFact
  ↓
MappingDecision
  ↓
FinancialMetric / Standard Concept
  ↓
NormalizedFinancialFact
  ↓
DerivedFinancialFact
  ↓
Stages 2–9
```

## 3. Raw Layer

`RawFinancialFact` preserves the original source representation, including report version, period, original title/code, value, unit, currency, statement location, and extraction location.

Raw data is immutable evidence. Normalization must never overwrite or delete it.

`NULL` and zero are different states.

## 4. Standard Concept Layer

`FinancialMetric` is the controlled standard concept catalog. It defines analytical concepts rather than source-specific labels.

The catalog supports statement type, parent concept, value type, flow/stock semantics, sign convention, industry applicability, and reported/derived metadata.

## 5. Mapping Layer

`MappingRule` defines versioned mapping logic.

`MappingDecision` records the actual mapping of a raw line, including method, confidence, review status, composition role, transformation specification, reviewer metadata, and notes.

A candidate mapping is not automatically an approved analytical fact.

## 6. Normalization Layer

`NormalizedFinancialFact` stores the concept-level standardized value for a company, period, metric, and report version.

`NormalizedFinancialFactInput` provides complete provenance when one normalized value is supported by one or many raw source lines.

This permits both:

```text
Raw A → Concept X
```

and:

```text
Raw A ─┐
Raw B ─┼→ Concept X
Raw C ─┘
```

When aggregate and component lines coexist, composition roles and resolution rules must prevent double counting.

## 7. Derived Layer

`DerivedFinancialFact` contains values calculated from normalized/derived inputs. It retains formula code/version, source report version, cutoff, calculation timestamp, and quality status.

`DerivedFinancialFactInput` preserves calculation lineage.

Derived values never overwrite reported or normalized evidence.

## 8. Point-in-Time

Historical analysis may use only information published by the relevant cutoff date.

`ReportVersion` is immutable historical evidence. Restatements create new versions. Historical backtests must select the version actually available at the historical cutoff.

A logical report has at most one current version.

## 9. FX

IRR is the accounting base currency and USD is derived.

Free-market and operational/exchange FX are separate economic inputs. Operational FX must not silently fall back to free-market FX.

Default conversion rules are flow → period average, stock → period end, and market value → same date, subject to explicit versioned rules.

## 10. Market / Share Foundations

Stage 1 stores OHLC/adjusted-close data, share-count history, and corporate actions. It does not calculate Market Score, technical trading signals, or decisions.

## 11. Ingestion Boundary

Ingestion creates auditable report/version/raw-source records and an `IngestionRun`. Mapping, normalization, derived calculations, and reconciliation are separate operations.

Failed or ambiguous source rows remain visible with explicit status; they are never silently converted to zero or discarded.

## 12. Ownership Boundary

Stage 1 owns data preservation, identity, periods, report versions, mapping, normalization provenance, derived-fact provenance, FX/market/share foundations, data quality, and ingestion audit.

Stage 1 does not own KPI definitions, Fundamental Scoring, Historical/Trend analysis, Forecasting, Forecast Evaluation, Valuation, Market analysis, or Decision logic.

## 13. Physical Schema Authority

For exact table definitions, constraints, migration versions, and database acceptance criteria, use:

`12_Database_Architecture_V1.1.md`

Do not maintain a second competing schema description in this file.
