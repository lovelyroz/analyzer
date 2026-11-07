# Analyzer V1 — Database Architecture V1.3

## Status

**UNDER REVIEW — DATABASE CONTRACT V1.3 (REOPENED FOR ARCHITECTURAL REVIEW)**

**Database engine:** SQLite

**ORM:** SQLAlchemy

**Schema migration version:** 8

This document is reopened for review. The decisions explicitly recorded as reviewed/approved below are the current working contract; sections not yet audited remain provisional. Earlier V1 / V1.1 / V1.2 references are historical context and do not override the decisions recorded here. The database stores identified source inputs and their provenance; backend services own runtime calculations and analytical outputs. This contract supports Stages 2–9 without persisting calculated analytical results.

---

## 1. Purpose

The database is the auditable Data Foundation. It stores identified source inputs and their provenance, report/version and period metadata, the controlled concept/mapping metadata needed to interpret source inputs, market/FX/share foundations, and ingestion audit information. It must not become a store for values that the backend can validly derive from persisted inputs.

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
  ├─ CODAL financial reports (current PDF path; Excel adapter planned)
  ├─ Daily market data (CSV / XLSX / …)
  └─ FX data — FREE_MARKET & OPERATIONAL (CSV / XLSX / …)
          ↓
Format-specific acquisition / extraction adapters
  ├─ CODAL PDF adapter (existing; retain during Excel transition)
  ├─ CODAL Excel adapter (planned; emits the same common DTO contract)
  ├─ OHLC parser → MarketDaily fields
  └─ FX parser → FxRateInput[]
          ↓
Common DTO boundary
          ↓
Core Ingestion (service.py)
  + IngestionRun audit
          ↓
Persisted source-input / foundation layer
          ↓
Backend runtime mapping, validation and calculations
          ↓
Stages 2–9 consume runtime results; calculated outputs are not persisted
```

Market and FX foundations remain separate branches and are consumed by their appropriate downstream stages.

**Persistence principle:** persist identified source inputs, not redundant totals or system-generated calculations. A value is not considered a base input merely because a source workbook contains a populated cell; its semantic role must be established. See the financial fact policy in Section 3.

## 3. Core Domains

### Entity

- `industries`
- `companies`
- `financial_periods`

#### Company and industry contract — reviewed

- Each company belongs to **exactly one industry** in this version.
- Subsidiary-company relationships, multiple industry assignments, and sub-industry classifications are out of scope.
- The seven V1 industry groups remain the initial catalog. The catalog is data-driven and may be extended with additional industry groups without redesigning the schema.
- A company's industry must be explicitly selected and validated before any report or financial data for that company is admitted.
- An absent, unknown, ambiguous, or guessed industry is a hard admission failure. The system must not assign a default or infer an industry.
- Company identity uses the stable internal `company_id`; it must never depend solely on the ticker.
- For V1, the ticker remains a fixed company attribute. A separate ticker-history table is not introduced: the current CODAL ingestion boundary receives an already-resolved `company_id`, so ticker history would add identity/mapping complexity without helping the extraction path. Any future need to support ticker changes must be separately designed around stable `company_id` and must not change historical report ownership.
- The optional national identifier may supplement identity matching but must not replace `company_id`.

The current implementation contains `parent_industry_id`, but parent/child industry classification is not part of the approved V1 contract. Its removal or migration treatment must be handled during schema implementation review, not by silently assigning sub-industries.

### FinancialPeriod — reviewed and approved contract

A financial period describes the actual source reporting span, using Jalali calendar components. Do not use SQL/Gregorian `Date` fields as the authoritative financial-period dates.

Required date components:

- `start_jalali_year`, `start_jalali_month`, `start_jalali_day`
- `end_jalali_year`, `end_jalali_month`, `end_jalali_day`

Retain and define these period attributes:

- `fiscal_year`: the company's fiscal-year label, resolved from its actual fiscal calendar and source; do not assume it is always Farvardin-starting.
- `fiscal_quarter`: nullable where not applicable; otherwise an integer from 1 through 4.
- `period_type`: describes the duration/span of the source data, not how often the report is published.
- `months_length`: number of months represented by the source period.
- `is_ytd`: whether the source amount is cumulative from the start of that company's fiscal year.

The actual start of a fiscal year/period must be resolved from the source or a validated company fiscal calendar. Never infer Farvardin 1 or another start date from a market-wide convention.

For the usual cumulative quarterly filing pattern:

| Fiscal quarter | Source period type | months_length | is_ytd |
|---|---|---:|---|
| Q1 | `QUARTER` | 3 | true |
| Q2 | `SEMI_ANNUAL` | 6 | true |
| Q3 | `NINE_MONTH` | 9 | true |
| Q4 | `ANNUAL` | 12 | true |

Monthly source periods use `MONTH`, `months_length=1`, and `is_ytd=false`.

Standalone-quarter amounts derived by differencing cumulative YTD reports are runtime calculations, not separate persisted source facts. A valid differencing operation must use compatible report versions from the same fiscal-year reporting chain; it must not subtract a restated later cumulative report from an incompatible earlier version.

`TTM` is not a source `FinancialPeriod` type. TTM is a derived analytical window and is computed at runtime.

The logical period identity is the company plus the exact Jalali start date and end date. Enforce valid Jalali components, start date not after end date, quarter range 1–4, and consistency between dates, duration, period type, and YTD semantics. Reject unresolved or contradictory period metadata rather than guessing.

**Migration caution:** existing SQL `Date` values must be inspected before migration. Do not assume they represent Gregorian dates or Jalali dates and do not blindly convert them. Ambiguous/unresolvable records require an explicit migration report and safe resolution path.

### Report / PIT

- `reports`
- `report_versions`

`Report` identifies the logical report. `ReportVersion` identifies a published historical state. Publication datetime belongs to `ReportVersion`. Each version is a distinct source snapshot; PIT consumers must select the version available at the relevant cutoff.

### Financial fact and calculation contract — reviewed and approved

The database stores **base/source input facts** required for analysis. It does not store redundant totals or values calculated by the application.

- Persist independently reported input components such as production quantity, sales quantity, unit price/rate, unit cost, and other genuine source inputs when their meaning, unit, period, and provenance are resolved.
- Do not persist a total/subtotal or other value when it is a reproducible calculation from sufficient, identified base inputs and a valid, explicitly defined calculation rule. The backend computes it when needed.
- **Preserve a reported aggregate when it is the only available source observation.** If a report provides only a total/aggregate and does not provide the underlying components needed to reconstruct it, retain that reported amount as a source observation (for example, a sale of an asset reported only as one amount, or an item under «سایر درآمدها» / «سایر هزینه‌ها»). Do not discard genuine reported information merely because it is an aggregate.
- A populated cell is not automatically a base input. Its semantic role must be classified. A reported aggregate is redundant only when sufficient validated components and an explicit valid rule make it reproducible; otherwise it remains a source observation, not an application-generated calculation.
- Where both components and an aggregate are present, do not persist both as independent additive inputs when the aggregate is reproducible from those components. Preserve source provenance and any relevant source-row classification so the backend can avoid double counting.
- Never invent a formula from labels or visual proximity. A derived value may be calculated only when its formula/relationship is known and all required inputs are available and valid.
- Do not substitute one measure for another. For example, production quantity is not sales quantity.
- A blank source cell is not zero. A blank base-input cell remains unknown/NULL. A blank calculated cell may be calculated at runtime only if its calculation rule is known and every required input is present; otherwise its result remains unknown.
- An explicit source zero remains zero. Do not turn NULL into zero or zero into NULL.
- Do not infer missing inputs, totals, quantities, rates, units, periods, or labels.
- Calculated values are runtime-only. They must not be inserted into raw, normalized, derived, cache, or history tables.
- Runtime calculation results must retain enough in-memory lineage to explain their inputs and formula where auditability requires it, but this does not authorize persistence of the calculated result.

The current schema/document references `derived_financial_facts` and `derived_financial_fact_inputs`. These tables conflict with the approved no-persisted-calculations policy if they store application-calculated financial values. Their future treatment must be resolved in the schema implementation/migration plan: remove or deprecate them safely, inspect existing contents before any destructive migration, and do not write new calculated results to them. The same no-duplication review applies to normalized fact tables: mapping/classification metadata may be persisted where necessary, but a second persisted copy of a source value or a calculated/analytical value is not permitted without a separately approved data contract.

### Financial normalization and mapping

- `raw_financial_facts` is the source-input fact layer, limited by the policy above.
- `financial_metrics` is the controlled catalog of concepts/metrics, not a repository of calculated results.
- `mapping_rules` and `mapping_decisions` may retain the metadata needed to map source labels to concepts and to audit/resolve mappings.
- Mapping/normalization performed by the backend must not silently create or persist calculated financial amounts. Any persisted normalized representation must be justified as necessary metadata or a canonical representation of an input, not a redundant analytical result.

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

## 4–11. (Unchanged principles from V1.1)

Raw facts, metrics, mapping, normalized/derived provenance, periods, ReportVersion PIT rules, and base FX architecture remain as in DATABASE_CONTRACT_V1.1 (CHANGE-003) and the locked Stage 1 principles (NULL ≠ 0, raw immutability, IRR base currency).

---

## 12. Market and Share Foundations

`market_daily` preserves raw close and adjusted close separately.

### Jalali components (CHANGE-005 / V1.2)

Source OHLC from the Iranian market uses Jalali dates. To support correct **same-month comparisons across years** (e.g. all Ordibehesht / month 2, all Esfand / month 12) without depending on Gregorian month identity:

| Column | Type | Role |
|--------|------|------|
| `jalali_year` | INTEGER nullable | Source Jalali year |
| `jalali_month` | INTEGER nullable (1–12) | Source Jalali month — **independent of year** |
| `jalali_day` | INTEGER nullable | Source Jalali day |
| `trade_date` | Date nullable | Retained for backward compatibility; may be NULL for Jalali-sourced rows |

- Ingestion parses the source Jalali string into components only (no Jalali→Gregorian calendar conversion).
- Cross-year same-month analysis must use `jalali_month` (and optionally `jalali_year`).
- Upsert identity for Jalali-sourced rows: `(company_id, jalali_year, jalali_month, jalali_day)`.
- Stage 8 owns market analysis; Stage 1 only stores the foundation.

Historical share counts and corporate actions are preserved so EPS comparability and historical valuation can account for changes in shares outstanding.

---

## 13. FX Foundation (CHANGE-001 + CHANGE-006)

### Rate types (locked)

- `FREE_MARKET` — free-market dollar (e.g. دلار آزاد)
- `OPERATIONAL` — exchange / NIMA / مبادله‌ای
- `OFFICIAL`, `ESTIMATED`, `MANUAL_OPERATOR` — supporting types

FREE_MARKET and OPERATIONAL must never be silently substituted for each other.

### Jalali components and identity (CHANGE-006)

| Column | Type | Role |
|--------|------|------|
| `jalali_year` | INTEGER nullable | Source Jalali year |
| `jalali_month` | INTEGER nullable (1–12) | Source Jalali month |
| `jalali_day` | INTEGER nullable | Source Jalali day |
| `rate_date` | Date nullable | Gregorian; NULL for Jalali-sourced rows |

**Identity:**

- Jalali-sourced: `(jalali_year, jalali_month, jalali_day, currency_from, currency_to, rate_type)`
- Gregorian-only: `(rate_date, currency_from, currency_to, rate_type)`

Same calendar day may hold both FREE_MARKET and OPERATIONAL rows.

### Unit storage policy (CHANGE-006)

- Persisted `rate` is always **IRR (Rial) per 1 unit of `currency_from`**.
- Free-market sources quoted in **Toman** are converted ×10 at the **adapter** boundary (explicit flag, e.g. `rates_in_toman=True`).
- Operational / NIMA rates already in Rial are stored as-is.
- Downstream stages consume IRR rates only; they do not re-apply unit conversion.

### Conversion rules

`fx_conversion_rules` remains the home of FLOW / STOCK / MARKET_VALUE methods and preferred `rate_type`. Defaults:

- FLOW → period-average FX
- STOCK → period-end FX
- MARKET_VALUE → same-date FREE_MARKET FX

---

## 14. Ingestion Boundary (CHANGE-007)

### Layering

```text
Source file / PDF / Excel / API
        ↓
Format-specific acquisition and extraction adapter
        ↓
Common DTOs (RawLineInput, FxRateInput, OHLC field map)
        ↓
ingest_codal_report / ingest_ohlc_* / ingest_fx_rates
        ↓
DB foundation tables + IngestionRun
```

### CODAL source formats and Excel transition

The intended direction is to replace CODAL PDF acquisition/extraction with Excel acquisition/extraction, while preserving the common ingestion and persistence contract.

- The Excel adapter must emit the same common financial input DTO contract consumed by `ingest_codal_report`; the existing downstream persistence boundary must remain format-independent.
- Preserve the established `RawLineInput` semantics and compatibility. Any required Excel provenance extension (such as workbook/sheet/cell coordinates) must be additive and must not break existing PDF callers.
- Excel workbooks are heterogeneous. Do not assume fixed worksheet names, row numbers, column numbers, or identical layouts across companies or report types.
- Preserve original source labels, raw numeric values, units/currencies, period metadata, and precise source provenance. For Excel, provenance should identify at least workbook/source identity, worksheet, row, and cell/column where available.
- Do not guess mappings, units, period boundaries, company identity, report type, or source attribution. Unresolved required metadata is an admission failure or must remain outside the analytical database until resolved.
- Read cached formula results from the workbook; do not evaluate spreadsheet formulas in the extraction adapter. If a formula cell has no usable cached result, emit an explicit warning/rejection/unknown state; never fabricate a value.
- Preserve the distinction between base input cells, reproducible aggregate cells, and sole-available reported aggregate observations. Persist identified base inputs; do not separately persist an aggregate that is reproducible from sufficient validated inputs; but retain an aggregate as a source observation when its underlying components are absent and it is the only reported value. Application-generated calculations remain runtime-only.
- A blank base-input cell remains NULL/unknown, not zero. A blank calculated cell may be computed only when the formula semantics are known and all required base inputs are present. Otherwise it remains unknown.
- Quarterly CODAL filings commonly report cumulative year-to-date values. Q1/Q2/Q3/Q4 source periods must follow the FinancialPeriod contract in Section 3. Standalone-quarter values are derived at runtime, using compatible report versions; they are not source facts to persist.
- Do not remove or disable the existing PDF acquisition/extraction path until the Excel adapter has been implemented and passed end-to-end validation against representative reports. During transition, both adapters may coexist and feed the same common DTO/persistence path.
- The current implementation uses PDF acquisition/extraction and `pypdf`; image-only/no-text PDFs are explicitly rejected and OCR is not silently substituted. This describes the current path, not the target format policy.

### OHLC / FX formats

- CSV, Excel, or future formats are interchangeable at the adapter layer only.
- Core persistence does not depend on file extension.
- Architecture completion does **not** require loading production data into the database.

### Failure, admission gates, and audit

- Company identity and the company's single industry must be resolved and validated before report/raw persistence.
- Unknown or ambiguous company identity, industry, report type, financial period, or source attribution is a hard admission failure. The system must not guess, silently default, or persist a partially identified record.
- Failed raw ingestion must not leave partial report/raw writes.
- The failed `IngestionRun` remains auditable, but failed source data must not be inserted into the report or financial-fact tables.
- NULL ≠ 0 remains mandatory. A genuinely absent base numeric input in an otherwise identified and valid source row may remain NULL; this is not permission to persist an unidentified or ambiguous record.
- Validation must distinguish a known-but-blank source value from an unknown label, unknown unit, unresolved period, or unresolved company/industry. The latter cases must be rejected or quarantined outside the analytical database until resolved.

## 15. Migration Policy

`Base.metadata.create_all()` is permitted only for an empty development/bootstrap database.

Production/schema evolution uses the versioned migration runner:

`python -m src.scripts.migrate_db`

The repository migration runner currently reaches schema version **8**. The architecture document must stay synchronized with the executable migration history:

| Version | Name |
|---|---|
| 1 | `baseline_schema` |
| 2 | `mapping_and_derived_schema` |
| 3 | `normalized_fact_multi_source_provenance` |
| 4 | `one_current_report_version` |
| 5 | `market_daily_jalali_components` |
| 6 | `fx_rates_jalali_components` |
| 7 | `forecast_version_repository` |
| 8 | `remove_forecast_output_persistence` |

Migrations are ordered and idempotent. Existing source values must not be silently rewritten. Any future migration implementing the Jalali FinancialPeriod contract or removing/deprecating calculated-fact persistence must first inspect existing rows, report ambiguous data, and avoid destructive or guessed conversions. Migration 8's removal of forecast-output persistence is consistent with the runtime-only analytical-output policy.

---

## 16. Ownership Boundaries

Database owns identified source-input preservation, provenance, controlled catalogs/mapping metadata, market/FX/share foundations, and ingestion audit. Backend services own mapping execution where appropriate, runtime calculations, reconciliation, KPI/scoring, trends, forecasts, valuation, and decisions. Calculated financial values and analytical/decision outputs are runtime-only and must not be persisted.

---

## 17. Version

`database_contract_version = DATABASE_CONTRACT_V1.3`

Overall Analyzer architecture remains **V1** with exactly nine analytical stages.

Approved/reviewed decisions recorded in this revision: company/industry admission contract; FinancialPeriod Jalali/YTD contract; source-input-only financial persistence and runtime calculation policy; Excel adapter direction with common DTO/persistence boundary and safe PDF transition; migration history corrected through version 8. CHANGE-003, CHANGE-005, CHANGE-006, CHANGE-007 remain historical amendment references pending a complete section-by-section audit.
