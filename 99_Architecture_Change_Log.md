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

**Approved Post-Baseline Compatible Amendments:** CHANGE-003, CHANGE-004

**Current Database Contract:** DATABASE_CONTRACT_V1.1

**Current Stage 8 Market Contract:** MARKET_CONTRACT_V1.1

**Pending Proposals:** NONE

**Next Review Trigger:** Only when a genuine architectural/contract issue is identified during implementation or explicitly requested by the project owner.
