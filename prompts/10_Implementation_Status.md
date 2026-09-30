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

### Stage 2 KPI Specification — final audit record

The Stage 2 final audit is complete. Established facts:

| Finding | Classification |
|---|---|
| Universal KPI inventory (11), Conditional KPI (1), Industry KPI inventory (11) | COMPLIANT |
| Missing ≠ zero preserved across all KPI paths | COMPLIANT |
| EPS comparability and data-quality propagation | COMPLIANT |
| `PHARMA` corrected to the canonical industry name `PHARMACEUTICAL` (implementation commit `da050ed`) | COMPLIANT — closed |
| Earnings Quality is intentionally DEFERRED as a composite framework | COMPLIANT (intentional, not a gap) |
| Period Dimensions beyond the implemented TTM/YoY behavior | FUTURE STAGE — Stage 4, not a Stage 2 gap |
| Stage 1 → Stage 2 production wiring | OUT OF SCOPE — integration gap that must not be implemented as part of the Stage 2 freeze |
| Database contract, Stage 1, KPI architecture, or Stage 2 source-code changes required | NONE |

The `PHARMA` correction was an implementation correction and requires no architecture change-log entry.

**Stage 2 final status: READY TO FREEZE — FROZEN / COMPLETE.**

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

## CODAL PDF Extraction Phase

**Status: COMPLETE / LOCKED**

The CODAL PDF extraction phase is now formally complete. Real PDF acquisition/extraction has been implemented and validated as an operational implementation behind the existing Stage 1 ingestion boundary.

### Locked architectural boundary

```text
PDF
 ↓
RawLineInput
 ↓
Persistence
```

The implementation may perform acquisition and extraction before producing `RawLineInput`, but it does not introduce a new analytical stage or move analytical responsibilities into ingestion.

### Locked extraction rules

- Numeric characters are normalized to English/ASCII digits before persistence.
- PDF extraction failures are recorded explicitly and audibly through the ingestion audit path.
- Incomplete or unextractable data is not inserted into the database.
- Source metadata, provenance, Report/ReportVersion, PIT, and raw-data immutability rules remain intact.
- Extraction remains replaceable behind the locked boundary.
- No KPI mapping, scoring, forecasting, valuation, or decision logic is performed by the extraction layer.

### Final validated CI evidence

- Workflow: `Tests`
- Run ID: `35375069943`
- Verified commit: `aab35e9bc72782ba9de178c17d1f35273ea5946b`
- Result: **SUCCESS**
- Test result: **158 passed, 1 skipped, 0 failed**

**Architecture status:** the nine-stage architecture remains unchanged.

**Database contract status:** `DATABASE_CONTRACT_V1.3` remains unchanged and LOCKED.

**Lock interpretation:** this is an implementation-phase lock of CODAL PDF extraction, not a new architectural stage or contract version.

### Known non-blocking note

DB unique constraint on `fx_rates` remains keyed on `rate_date` for legacy Gregorian rows. Jalali identity is enforced at application upsert level (documented in CHANGE-006). Acceptable for V1.3; a future partial unique index may be added without contract break.

---

## Final CI verification

The final CI reference must always correspond to the audited commit below. The previous V1.3 record for run `35200297255` is historical and is retained only as prior evidence.

### Final verified CODAL PDF extraction CI

- Workflow: `Tests`
- Run ID: `35375069943`
- Verified commit: `aab35e9bc72782ba9de178c17d1f35273ea5946b`
- Result: **SUCCESS**
- Test result: **158 passed, 1 skipped, 0 failed**

This CI result is the final implementation evidence for the CODAL PDF extraction phase.

---

## Final audit result

- Architecture boundaries preserved (9 stages).
- DATABASE_CONTRACT_V1.3 requirements for CHANGE-006 and CHANGE-007: **PASS**.
- Point-in-Time / ReportVersion rules preserved.
- FREE_MARKET vs OPERATIONAL separation preserved.
- Raw → normalized → derived separation preserved.
- Stage 2–9 contracts remain compatible.
- Market and FX ingestion framework is implemented and regression-tested.
- CODAL PDF extraction is implemented and validated behind the existing adapter boundary and is now COMPLETE / LOCKED.
- No production bulk load is required for this lock.

## Lock statement

**INGESTION FRAMEWORK PHASE: COMPLETE / LOCKED**

Scope locked:

- common ingestion boundary
- CODAL `RawLineInput` boundary and core persistence
- market/OHLC adapter and persistence path
- FX adapter and persistence path
- PIT / ReportVersion / raw immutability rules
- idempotency and IngestionRun audit
- explicit FREE_MARKET / OPERATIONAL separation
- explicit Toman→Rial conversion boundary
- no production bulk load requirement

Explicitly deferred:

- production bulk loading

Deferred work must integrate with the locked boundary and must not reopen `DATABASE_CONTRACT_V1.3` unless a genuine architectural contradiction is demonstrated.

---

## CODAL PDF Extraction Phase Status

**COMPLETE / LOCKED**

The operational CODAL PDF extraction implementation is formally locked behind the existing ingestion boundary. See the detailed phase lock and final CI evidence above.

---

## Repository status

## CODAL PDF extraction operational phase

The previously deferred CODAL PDF extraction work has now been implemented and validated behind the locked CHANGE-007 boundary.

### Final implementation evidence

- CODAL local/HTTP acquisition adapter: IMPLEMENTED
- CODAL text/table extraction adapter: IMPLEMENTED
- CODAL extraction-to-`RawLineInput[]` boundary: IMPLEMENTED
- CODAL extraction-to-raw persistence facade: IMPLEMENTED
- Persian/Arabic-Indic digit normalization to ASCII textual values: IMPLEMENTED
- Numeric parsing, negative values, dates, and explicit missing values: IMPLEMENTED
- RTL handling avoids destructive whole-line reversal: IMPLEMENTED
- Representative CODAL layouts and generic text-line cases: TESTED
- Malformed/no-text PDF failure is explicit and auditable through `IngestionRun`
- CODAL idempotent re-ingestion: TESTED
- Supplied representative PDFs: 19 extractable; 1 explicitly rejected as no-text
- `pypdf` dependency: recorded in `requirements.txt` and CI workflow

### Final CI evidence for extraction implementation

- Workflow: `Tests`
- Run ID: `35375069943`
- Job ID: `105697726337`
- Verified commit: `aab35e9bc72782ba9de178c17d1f35273ea5946b`
- Result: **SUCCESS**
- Test command: `pytest src/tests -v`
- Result: **158 passed, 1 skipped, 0 failed**
- Duration: 65.72s
- CI checkout verified the exact commit above.

### Extraction-phase lock

The CODAL PDF extraction implementation is now **COMPLETE / LOCKED** as an operational implementation of the existing ingestion boundary.

Locked boundary:

```text
CODAL PDF / external source
        ↓
Acquisition
        ↓
PDF extraction
        ↓
Sequence[RawLineInput]
        ↓
ingest_codal_report()
        ↓
immutable raw/foundation persistence
```

Locked rules include:

- extraction does not perform KPI mapping, scoring, forecasting, valuation, or decision logic;
- textual numeric characters persisted through CODAL ingestion are normalized to ASCII digits;
- `NULL != 0`;
- uncertain/unextractable values are not invented;
- extraction failures are explicit and auditable;
- source metadata and provenance are preserved;
- raw data remains immutable;
- Report/ReportVersion and PIT rules remain intact;
- the extraction implementation remains replaceable behind the locked boundary.

This is an implementation lock, not a new architectural stage or contract version.

### Remaining operational work

The next task is **production data loading**, not another analytical stage:

- select/validate the actual production CODAL report universe;
- acquire the required reports;
- load them through the locked extraction/persistence path;
- validate completeness, duplicates, ReportVersions, PIT metadata, units, and data quality;
- then load production OHLC and FX datasets through their existing adapters;
- run end-to-end foundation-level validation before enabling downstream analytical calculations.

Production bulk loading is intentionally **NOT YET LOCKED COMPLETE**.

**IMPLEMENTATION: COMPLETE**  
**TESTING: PASS**  
**AUDIT: PASS**  
**CI: PASS**  
**CODAL PDF EXTRACTION: COMPLETE / LOCKED**  
**INGESTION FRAMEWORK: COMPLETE / LOCKED**  
**ARCHITECTURE: V1 — LOCKED**  
**DATABASE CONTRACT: V1.3 — LOCKED**

```text
Design: LOCKED
Implementation: COMPLETE
Testing: PASS
Audit: PASS
CI: PASS
Architecture: LOCKED
Database Contract: V1.3 — LOCKED
Ingestion Framework: COMPLETE / LOCKED
CODAL PDF Extraction: COMPLETE / LOCKED
Production Bulk Load: NOT YET COMPLETE
```


---

## Stage 4 — Final Freeze Record

Stage 4 Historical, Seasonal & Trend Engine has completed implementation, targeted verification, final audit, and repository-wide regression verification.

### Final Stage 4 verification

- Stage 4 targeted test suite: **102 passed, 0 failed, 0 skipped, 0 errors**
- Full repository regression: **371 passed, 0 failed, 2 skipped, 0 errors**
- Stage 4 tests within full regression: **0 failures, 0 skips**
- B1 — STOCK 12M period-end semantics: **RESOLVED**
- B2 — FLOW/STOCK momentum semantics: **RESOLVED**
- B3 — Relative-strength self-counting / PIT issue: **RESOLVED**
- Historical layer: **PASS**
- Seasonal layer: **PASS**
- Momentum/trend layer: **PASS**
- Output contract: **PASS**
- PIT / no-lookahead: **PASS**
- Determinism: **PASS**
- Stage 3 boundary: **PASS**
- Stage 5 boundary: **PASS**

### Final verified GitHub CI

- Workflow: Tests
- Run ID: **36632664614**
- Verified commit: **b288a0631cfb2bf9efc6d1112aa9b11b10e4f81e**
- Result: **SUCCESS**
- Trigger: push to `master`

### Freeze decision

**STAGE 4 — HISTORICAL, SEASONAL & TREND ENGINE: FROZEN / COMPLETE**

The Stage 4 implementation is now frozen.

No Stage 4 implementation, schema, analytical rule, threshold, or output-contract change should be made without an explicitly approved architectural or specification change.

Future work belongs to later stages or integration work and must not reopen the frozen Stage 4 implementation without documented justification.
