# 10 — IMPLEMENTATION STATUS

## Project

**Tehran Stock Analysis — V1**

This document tracks implementation status. It does not redefine the architecture.

## Current architecture

**Analyzer Architecture:** V1 — exactly 9 stages — LOCKED

**Master Architecture:** `00_a_Master_Architecture.md`

**Stage Specifications:** `01_Stage1_Data_Foundation.md` through `09_Stage9_Decision_Dashboard.md`

**Architecture Change Log:** `99_Architecture_Change_Log.md`

**Database Contract:** `DATABASE_CONTRACT_V1.3` — LOCKED

## Stage status

| Stage | Design | Implementation | Testing | Audit | Overall |
|---|---|---|---|---|---|
| 1 — Data Foundation & Data Model | LOCKED | COMPLETE | PASS | PASS | COMPLETE / LOCKED |
| 2 — KPI Specification | LOCKED | COMPLETE | PASS | PASS | COMPLETE / LOCKED |
| 3 — Fundamental Scoring | LOCKED | COMPLETE | PASS | PASS | COMPLETE / LOCKED |
| 4 — Historical, Seasonal & Trend | LOCKED | COMPLETE | PASS | PASS | COMPLETE / LOCKED |
| 5 — Forecast Engine | LOCKED | COMPLETE | PASS | PASS | COMPLETE / LOCKED |
| 6 — Forecast Evaluation & Calibration | LOCKED | COMPLETE | PASS | PASS | COMPLETE / LOCKED |
| 7 — Valuation Engine | LOCKED | COMPLETE | PASS | PASS | COMPLETE / LOCKED |
| 8 — Market Engine | LOCKED | COMPLETE | PASS | PASS | COMPLETE / LOCKED |
| 9 — Decision Engine & Dashboard | LOCKED | COMPLETE | PASS | PASS | COMPLETE / LOCKED |

---

## Stage 1 database contract V1.3 verification

Contract documents:

- `12_Database_Architecture_V1.1.md` (title retained; body = V1.3)
- `99_Architecture_Change_Log.md` — CHANGE-003 … CHANGE-007 APPROVED

### CHANGE-006 audit (FX Jalali + unit + identity)

| Requirement | Result | Evidence |
|---|---|---|
| `fx_rates.jalali_year/month/day` additive nullable | PASS | `src/models/fx.py`; migration 6 |
| No Jalali→Gregorian conversion | PASS | `_parse_jalali_components` string split only |
| `rate_date` NULL for Jalali-sourced rows | PASS | `ingest_fx_rates` / `ingest_fx_xlsx` |
| Identity Jalali: (jy,jm,jd,from,to,rate_type) | PASS | `_find_fx_existing` + upsert tests |
| FREE_MARKET ≠ OPERATIONAL (no silent merge) | PASS | CHANGE-001 tests + coexistence test |
| Persist rate in IRR (Rial) | PASS | Contract + adapter |
| Free-market Toman → ×10 at adapter | PASS | `ingest_fx_xlsx(..., rates_in_toman=True)` + test |
| Migration 6 idempotent | PASS | `test_migration_6_adds_fx_jalali_columns`, integrity tests |

### CHANGE-007 audit (ingestion adapters + CODAL PDF boundary)

| Requirement | Result | Evidence |
|---|---|---|
| Format-agnostic core persistence | PASS | `ingest_fx_rates` / `ingest_codal_report` take DTOs |
| XLSX adapter → common DTO | PASS | `ingest_fx_xlsx` → `FxRateInput[]` → `ingest_fx_rates` |
| CODAL extraction outside core write | PASS | `ingest_codal_report` accepts `RawLineInput[]` only |
| No analytical logic in adapters | PASS | Parse + optional unit convert only |
| IngestionRun audit on all paths | PASS | FX / OHLC / CODAL runs |
| No production bulk load required for lock | PASS | Architecture policy |

### Known non-blocking note

DB unique constraint on `fx_rates` remains keyed on `rate_date` for legacy Gregorian rows. Jalali identity is enforced at application upsert level (documented in CHANGE-006). Acceptable for V1.3; a future partial unique index may be added without contract break.

---

## Final CI verification (V1.3)

- Workflow: `Tests`
- Run: `#183`
- Run ID: `35200297255`
- Job ID: `105133169117`
- Verified commit: `35b308926e60399e6a98f6f520b6b012e04c636a`
- Result: **SUCCESS**
- Test suite: **131 passed**
- Failures: **0**
- Warnings: **449** (non-blocking deprecations)

FX-specific tests exercised and passed:

- `test_free_market_and_operational_are_stored_separately`
- `test_fx_idempotent_upsert_jalali`
- `test_operational_never_defaults_to_free_market`
- `test_same_month_across_years_fx`
- `test_ingest_fx_xlsx_toman_and_rial`
- `test_migration_6_adds_fx_jalali_columns`
- migration version assertions → 6

---

## Final audit result

- Architecture boundaries preserved (9 stages).
- DATABASE_CONTRACT_V1.3 requirements for CHANGE-006 and CHANGE-007: **PASS**.
- Point-in-Time / ReportVersion rules preserved.
- FREE_MARKET vs OPERATIONAL separation preserved.
- Raw → normalized → derived separation preserved.
- Stage 2–9 contracts remain compatible.
- Full regression suite passes.
- No pending architecture proposals.

---

## Repository status

**IMPLEMENTATION: COMPLETE**  
**TESTING: PASS**  
**AUDIT: PASS**  
**CI: PASS**  
**ARCHITECTURE: LOCKED**  
**DATABASE CONTRACT: V1.3 — LOCKED**

```text
Design: LOCKED
Implementation: COMPLETE
Testing: PASS
Audit: PASS
Overall: COMPLETE / LOCKED
```

Final audited commit (docs + prior implementation): `35b308926e60399e6a98f6f520b6b012e04c636a`  
Final CI run: `#183` / `35200297255` / job `105133169117`  
Test count: **131 passed**
