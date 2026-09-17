# Analyzer V1 — Database Architecture V1.3

## Status

**LOCKED — DATABASE CONTRACT V1.3**

**Database engine:** SQLite

**ORM:** SQLAlchemy

**Schema migration version:** 6

This document supersedes earlier V1 / V1.1 / V1.2 database architecture references. It implements the locked Stage 1 contract (including CHANGE-003, CHANGE-005, CHANGE-006, CHANGE-007) and supports Stages 2–9 without moving analytical ownership into the database.

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
  ├─ Codal financial reports (PDF)
  ├─ Daily market data (CSV / XLSX / …)
  └─ FX data — FREE_MARKET & OPERATIONAL (CSV / XLSX / …)
          ↓
Format / Extraction Adapters  (CHANGE-007)
        ├─ CODAL PDF Acquisition → PDF bytes
        ├─ CODAL PDF Extraction (pypdf text-first) → RawLineInput[]
  ├─ OHLC parser → MarketDaily fields
  └─ FX parser (+ explicit Toman→Rial if needed) → FxRateInput[]
          ↓
Core Ingestion (service.py)
  + IngestionRun audit
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
Source file / PDF / API
        ↓
Adapter or CODAL PDF Extraction Layer
        ↓
Common DTOs (RawLineInput, FxRateInput, OHLC field map)
        ↓
ingest_codal_report / ingest_ohlc_* / ingest_fx_rates
        ↓
DB foundation tables + IngestionRun
```

### CODAL

- Inputs are PDFs.
- Acquisition is independent from PDF parsing and database persistence.
- The current implementation provides deterministic local-file acquisition and retryable HTTP acquisition.
- Text extraction uses `pypdf`; image-only or no-text PDFs are rejected explicitly. OCR is not silently substituted.
- Extraction (layout/table/OCR) is **outside** `ingest_codal_report`.
- Core function receives `RawLineInput` sequence + report metadata (tracking id, URL, publication datetime, restatement flag).
- Raw facts remain immutable; mapping/normalization are separate later steps.

### OHLC / FX formats

- CSV, Excel, or future formats are interchangeable at the adapter layer only.
- Core persistence does not depend on file extension.
- Architecture completion does **not** require loading production data into the database.

### Failure and audit

- Failed raw ingestion must not leave partial report/raw writes.
- The failed `IngestionRun` remains auditable.
- NULL ≠ 0 is enforced; missing values stay missing.

---

## 15. Migration Policy

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
| 5 | `market_daily_jalali_components` |
| 6 | `fx_rates_jalali_components` |

Migrations are ordered and idempotent. Existing raw values are not silently rewritten.

---

## 16. Ownership Boundaries

Unchanged from V1.1: database owns source preservation and foundations; analytical stages own scoring, forecast, valuation, decision.

---

## 17. Version

`database_contract_version = DATABASE_CONTRACT_V1.3`

Overall Analyzer architecture remains **V1** with exactly nine analytical stages.

Approved amendments: CHANGE-003, CHANGE-005, CHANGE-006, CHANGE-007.
