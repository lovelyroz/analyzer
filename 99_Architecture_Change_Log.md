# 99 — ARCHITECTURE CHANGE LOG

## Project

**Tehran Stock Analysis — V1**

This document records intentional changes to the system architecture and locked contracts.

It does NOT replace `00_a_Master_Architecture.md`.

The current architecture is determined by the latest approved Master Architecture, Locked Specifications, and explicitly approved compatible amendments recorded here.

---

# 1. Change Control Rules

1. Locked architecture must not be changed casually.
2. Implementation problems do not automatically justify architectural changes.
3. A change must be proposed only when a genuine architectural contradiction, missing contract, or structural requirement is identified.
4. Every approved change must record its scope, reason, impact, compatibility, migration, testing, and approval status.
5. Never silently modify a locked specification.
6. Historical decisions must remain traceable.
7. If a change affects downstream stages, all affected contracts must be explicitly identified.
8. Minor implementation fixes that do not change architecture do not belong here.

---

# 2. Baseline

## Baseline Version

**V1.0**

## Baseline Status

**ARCHITECTURE LOCKED**

## Baseline Scope

The V1 architecture consists of exactly nine stages:

1. Data Foundation & Data Model
2. KPI Specification
3. Fundamental Scoring
4. Historical, Seasonal & Trend Engine
5. Forecast Engine
6. Forecast Evaluation & Calibration
7. Valuation Engine
8. Market Engine
9. Decision Engine & Dashboard Contract

All nine stages remain the major analytical stages of V1.

---

# 3. Initial Architecture Baseline

### CHANGE-000 — V1 Architecture Baseline

**Status:** APPROVED

**Version:** V1.0

**Type:** BASELINE

**Affected:** Entire Architecture

**Description:**

The final V1 architecture was established as the authoritative architecture after completion and review of Stages 1–9.

The architecture separates Data Foundation, Fundamental Analysis, Historical/Trend Analysis, Forecasting, Forecast Evaluation, Valuation, Market Analysis, and Decision/Dashboard responsibilities.

Fundamental and Market analysis remain separate until Stage 9.

---

# 4. FX Architecture Baseline

### CHANGE-001 — Separate Free-Market and Operational FX

**Status:** APPROVED

**Version:** V1.0

**Affected:** Stage 1, Stage 5, Stage 7, Stage 8/9 FX Context

**Description:**

The architecture distinguishes between FREE_MARKET FX and OPERATIONAL / EXCHANGE FX.

Free-market FX is used for market valuation and USD-relative market-value analysis.

Operational FX is used where appropriate for company sales and earnings exposure.

Operational FX must not silently default to free-market FX.

---

# 5. Point-in-Time Baseline

### CHANGE-002 — Point-in-Time and ReportVersion Control

**Status:** APPROVED

**Version:** V1.0

**Affected:** Stage 1 and all downstream analytical stages

**Description:**

Financial information must be evaluated using the information actually available at the relevant historical cutoff date.

Report and ReportVersion are separate concepts. Publication datetime belongs to ReportVersion. Restated/corrected reports are versioned.

---

# 6. Post-Baseline Approved Changes

### CHANGE-003 — Stage 1 Database Multi-Source Normalized Provenance

**Status:** APPROVED

**Version:** DATABASE_CONTRACT_V1.1

**Date:** 2026-09-17

**Affected Stage(s):** Stage 1; downstream consumers of normalized financial facts

**Previous Rule:**

`NormalizedFinancialFact` contained nullable direct provenance fields for a raw fact and mapping decision. The architecture also allowed many raw lines to map to one standard concept, but a single normalized row could not explicitly retain all raw contributors.

**New Rule:**

Add `NormalizedFinancialFactInput` as a provenance bridge. One normalized concept-level fact may now retain one or many raw inputs, each linked to its mapping decision and an explicit input role.

`NormalizedFinancialFact` remains the concept-level normalized value. `DerivedFinancialFact` remains the layer for formula-derived/aggregated values.

**Reason:**

Close a genuine auditability gap between the many-to-one mapping requirement and the physical provenance model. Without the bridge, multi-line normalization could lose source lineage or force an incorrect one-source representation.

**Evidence / Trigger:**

Post-implementation database architecture audit of `11_Database_Architecture_Stage1.md`, `12_Database_Architecture_V1.md`, and the Stage 1 SQLAlchemy models.

**Architecture Impact:**

Compatible refinement of Stage 1 data provenance. The nine-stage Analyzer architecture is unchanged.

**Contract Impact:**

Database contract advances to V1.1. New normalized multi-source records must use the bridge for complete provenance.

**Downstream Impact:**

Stages 2–9 continue to consume standardized concept values and must not read raw labels directly. No analytical ownership moves into Stage 1.

**Migration Required:**

Schema migration version 3: `normalized_fact_multi_source_provenance`.

**Testing Required:**

Verify one-to-many raw-to-concept provenance, uniqueness, foreign keys, raw immutability, and migration behavior.

**Approval:** APPROVED

---

### CHANGE-004 — Stage 8 Drawdown State Contract Correction

**Status:** APPROVED

**Version:** MARKET_CONTRACT_V1.1

**Date:** 2026-09-17

**Affected Stage(s):** Stage 8 and Stage 9 market-context consumption

**Previous Rule:**

The drawdown state set contained `NEAR_PEAK`, `RECOVERING`, `DEEP_DRAWDOWN`, and `NEW_LOW`, leaving moderate stable drawdowns without a dedicated state.

**New Rule:**

Add `STABLE_DRAWDOWN`. `RECOVERING` requires material rebound evidence; the V1 implementation uses a 5% recovery threshold. Moderate drawdown without recovery/deep/new-low evidence is `STABLE_DRAWDOWN`.

**Reason:**

Prevent the engine from labeling a moderate, non-recovering drawdown as recovery merely because no other state matched.

**Evidence / Trigger:**

Stage 8 implementation audit identified the classification gap.

**Architecture Impact:**

Compatible correction to the Stage 8 external state contract. No new engine and no market score are introduced.

**Contract Impact:**

`market_contract_version` becomes `MARKET_CONTRACT_V1.1`; `model_version` remains `STAGE8_V1`.

**Downstream Impact:**

Stage 9 treats `STABLE_DRAWDOWN` as contextual market evidence only; it is not an automatic Buy/Sell/Hold instruction.

**Migration Required:**

No database migration. Existing market observations remain valid; the output contract is versioned.

**Testing Required:**

Verify moderate drawdown classification, recovery threshold, and downstream contextual handling.

**Approval:** APPROVED

---

### CHANGE-005 — Jalali Date Components on MarketDaily

**Status:** APPROVED

**Version:** DATABASE_CONTRACT_V1.2

**Date:** 2026-09-17

**Affected Stage(s):** Stage 1 (Market foundation); Stage 8 consumers of daily market data

**Previous Rule:**

`market_daily.trade_date` was a single SQLAlchemy `Date` column. Stage 1 tests populated it with Gregorian `date` objects. Source OHLC files from the Iranian market supply Jalali dates (e.g. `1402-01-08`). There was no first-class representation of Jalali year/month/day, so same-month comparisons across years (all month-2 / Ordibehesht, all month-12 / Esfand) could not be expressed correctly without relying on Gregorian month identity, which does not match the Jalali calendar.

**New Rule:**

`market_daily` gains three additive nullable integer columns:

- `jalali_year`
- `jalali_month` (1–12)
- `jalali_day`

These store the source Jalali components directly. Same-month analysis across years uses `jalali_month` and is independent of year and day. No silent Jalali→Gregorian calendar conversion is performed by the ingestion layer.

`trade_date` (Date) is retained for backward compatibility with existing Stage 1 tests and any Gregorian-oriented range queries. New Jalali-sourced rows fill the three component fields from the source string (parse of `YYYY-MM-DD` Jalali text only — not a calendar conversion).

**Reason:**

Enable correct seasonal/month-aligned market analysis for Iranian data (compare all Ordibehesht across years, all Esfand across years) without making month identity dependent on the Gregorian calendar.

**Evidence / Trigger:**

Production OHLC ingestion of real Iranian CSV (Jalali dates) plus explicit analytical requirement for cross-year same-month comparison.

**Architecture Impact:**

Compatible additive refinement of Stage 1 market foundation. Nine-stage architecture unchanged. No analytical engine added.

**Contract Impact:**

Database contract advances to `DATABASE_CONTRACT_V1.2`.

**Downstream Impact:**

Stage 8 (and any later consumer) should prefer `jalali_month` / `jalali_year` for month-aligned and year-over-year seasonal analysis of Iranian market data. `trade_date` remains available for ordering when present.

**Migration Required:**

Schema migration version 5: `market_daily_jalali_components`.

**Testing Required:**

- Migration idempotency on fresh and legacy DBs
- Columns exist and are nullable
- Ingestion fills jalali_* from source string without Gregorian conversion
- Existing Stage 1–9 regression suite continues to pass

**Approval:** APPROVED

---

### CHANGE-006 — Jalali Components, Unit Policy, and Identity for FX Rates

**Status:** APPROVED

**Version:** DATABASE_CONTRACT_V1.3

**Date:** 2026-09-17

**Affected Stage(s):** Stage 1 (FX foundation); Stages 5, 7, 8, 9 FX context consumers

**Previous Rule:**

`fx_rates` used a Gregorian `rate_date` as the primary temporal key. Iranian free-market and operational (NIMA / مبادله‌ای) FX sources supply Jalali dates. Free-market dollar quotes are commonly published in Toman while the system stores financial facts in IRR (Rial). There was no first-class Jalali representation on FX and no explicit unit-conversion rule at the ingestion boundary.

**New Rule:**

1. **Jalali components (same policy as CHANGE-005 / market_daily)**  
   `fx_rates` gains additive nullable integer columns:
   - `jalali_year`
   - `jalali_month` (1–12)
   - `jalali_day`  
   Source Jalali strings are parsed into components only. No Jalali→Gregorian calendar conversion. For Jalali-sourced rows, `rate_date` is left NULL.

2. **Identity**  
   - Jalali-sourced rows: `(jalali_year, jalali_month, jalali_day, currency_from, currency_to, rate_type)`  
   - Gregorian-only rows: `(rate_date, currency_from, currency_to, rate_type)`  
   FREE_MARKET and OPERATIONAL for the same calendar day remain distinct rows (CHANGE-001).

3. **Unit storage policy**  
   All persisted `fx_rates.rate` values are stored in **IRR (Rial) per 1 unit of `currency_from`**.  
   When a free-market source quotes in Toman, conversion ×10 occurs at the ingestion adapter boundary and must be explicit (e.g. `rates_in_toman=True`). Operational / NIMA rates that are already in Rial are stored as-is. The conversion is not applied downstream; later stages consume IRR rates only.

4. **rate_type values remain locked**  
   `FREE_MARKET`, `OPERATIONAL`, `OFFICIAL`, `ESTIMATED`, `MANUAL_OPERATOR`. Silent substitution of OPERATIONAL by FREE_MARKET is forbidden.

**Reason:**

- Align FX temporal model with Iranian source calendars and with the market_daily Jalali policy so same-month / cross-year FX analysis is possible.
- Prevent unit ambiguity (Toman vs Rial) from corrupting valuation and USD-relative analysis.
- Keep FREE_MARKET vs OPERATIONAL separation enforceable at the unique identity level.

**Evidence / Trigger:**

Sample free-market (دلار آزاد, Toman) and operational/NIMA (دلار مبادله‌ای) Excel sources; explicit user requirement that date handling match the OHLC Jalali setup exactly.

**Architecture Impact:**

Compatible additive refinement of Stage 1 FX foundation. Nine-stage architecture unchanged. No new analytical engine.

**Contract Impact:**

Database contract advances to `DATABASE_CONTRACT_V1.3`.

**Downstream Impact:**

Stages that consume FX continue to select by `rate_type` and may use Jalali components for seasonal alignment. They must not assume Toman units or merge rate types.

**Migration Required:**

Schema migration version 6: `fx_rates_jalali_components` (additive columns; existing unique constraint on `rate_date` retained for legacy Gregorian rows; application-level upsert uses Jalali identity for new rows).

**Testing Required:**

- Migration idempotency
- Jalali parse without Gregorian conversion
- FREE_MARKET vs OPERATIONAL coexistence for the same Jalali day
- Explicit Toman→Rial (×10) conversion at adapter boundary
- Idempotent upsert by Jalali identity
- Regression suite green

**Approval:** APPROVED

---

### CHANGE-007 — Ingestion Adapter Boundary and CODAL PDF Extraction Layer

**Status:** APPROVED

**Version:** DATABASE_CONTRACT_V1.3 (ingestion boundary clarification; no new schema version)

**Date:** 2026-09-17

**Affected Stage(s):** Stage 1 ingestion only

**Previous Rule:**

Ingestion functions accepted structured inputs (`RawLineInput`, CSV paths, etc.) but the architecture did not formally separate (a) source-format parsers, (b) PDF extraction for Codal, and (c) the immutable persistence functions. File format choice (CSV vs Excel) and PDF-ness of Codal were not explicitly placed outside the core persistence contract.

**New Rule:**

Stage 1 ingestion is layered as follows:

```text
External file / API / PDF
        ↓
Format-specific Adapter (CSV / XLSX / future)
  or
CODAL PDF Extraction Layer  →  Sequence[RawLineInput]
        ↓
Common intermediate DTOs
  (RawLineInput | FxRateInput | OHLC row mapping)
        ↓
Core persistence functions (service.py style)
  ingest_codal_report / ingest_ohlc_* / ingest_fx_rates
        ↓
DB tables (immutable raw / foundation)
```

Rules:

1. **Format independence**  
   Core persistence functions do not depend on file extension. CSV, Excel, or future formats only differ in the adapter that produces the common DTOs.

2. **CODAL source form**  
   Codal financial statements arrive as PDFs. Extraction (table/text/OCR as needed) is a **pre-ingestion** responsibility. `ingest_codal_report` receives already-extracted `RawLineInput` lines plus report metadata (tracking id, URL, publication datetime, version). The PDF itself may be referenced via `source_url` / tracking fields; the binary is not required inside the DB contract for V1.

3. **No analytical logic in adapters**  
   Adapters parse and, where documented (e.g. Toman→Rial), apply explicit unit conversion. They do not map to standard metrics, score, or forecast.

4. **Production load policy**  
   Architecture completion does not require loading production data into the database. Real bulk loads occur only after contracts and regression tests are locked.

5. **Idempotency and audit**  
   All core ingest paths continue to use `IngestionRun`, preserve raw immutability, enforce NULL ≠ 0, and support PIT via ReportVersion publication datetime.

**Reason:**

- User confirmed Codal inputs are PDFs and that OHLC/FX input formats may be a mix of CSV and Excel.
- Prevents the persistence contract from being coupled to a single file type.
- Places heavy/variable PDF extraction outside the locked raw-fact write path so extraction tools can evolve without redesigning Stage 1 tables.

**Evidence / Trigger:**

Explicit project-owner statements on Codal PDF sources and undecided CSV/Excel mix for market/FX; decision to complete architecture before production DB loads.

**Architecture Impact:**

Clarification of Stage 1 ingestion boundary only. No change to the nine stages, PIT model, or analytical ownership.

**Contract Impact:**

Documented as part of `DATABASE_CONTRACT_V1.3` ingestion boundary. No new migration solely for this change.

**Downstream Impact:**

None for Stages 2–9. They continue to consume foundation tables, not source files.

**Migration Required:**

None beyond CHANGE-006.

**Testing Required:**

- Adapters produce valid DTOs
- Core ingest functions remain format-agnostic
- Failed extraction does not leave partial Report/RawFact writes
- Existing Stage 1 regression suite continues to pass

**Approval:** APPROVED

---

# 7. Pending Proposals

No pending architectural proposals.

---

# 8. Change Record Template

Future changes must use this structure:

## CHANGE-XXX — [Short Title]

**Status:** PROPOSED / APPROVED / REJECTED

**Version:** V1.x / V2.0

**Date:** YYYY-MM-DD

**Affected Stage(s):**

**Previous Rule:**

**New Rule:**

**Reason:**

**Evidence / Trigger:**

**Architecture Impact:**

**Contract Impact:**

**Downstream Impact:**

**Migration Required:**

**Testing Required:**

**Approval:**

**Notes:**

---

# 9. Versioning Rule

### V1.x

Use for compatible architectural or contract changes that do not invalidate the overall V1 architecture.

### V2.0

Use when a major structural change invalidates or substantially replaces V1 architecture.

No version increment should be created merely for normal implementation progress.

---

# 10. Important Distinction

The following are NOT automatically architecture changes:

* bug fixes
* refactoring
* performance improvements
* database index changes
* implementation details
* code organization changes
* parameter tuning inside an existing model version
* test improvements

The following MAY require an architecture or contract change:

* adding/removing a Stage
* changing a Stage's responsibility
* changing an inter-stage contract
* changing a fundamental data model assumption
* changing a locked KPI definition
* changing the fundamental scoring architecture
* changing the valuation architecture
* changing the decision architecture
* introducing a new required data source
* changing a core FX interpretation
* breaking compatibility between stages

---

# 11. Current Status

**Analyzer Architecture:** LOCKED — V1

**Major Stages:** 1–9

**Approved Post-Baseline Compatible Amendments:** CHANGE-003, CHANGE-004, CHANGE-005, CHANGE-006, CHANGE-007

**Current Database Contract:** DATABASE_CONTRACT_V1.3

**Current Stage 8 Market Contract:** MARKET_CONTRACT_V1.1

**Pending Proposals:** NONE

**Next Review Trigger:** Only when a genuine architectural/contract issue is identified during implementation or explicitly requested by the project owner.
