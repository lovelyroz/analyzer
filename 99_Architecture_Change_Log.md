# 99 — ARCHITECTURE CHANGE LOG

## Project

**Tehran Stock Analysis — V1**

This document records intentional changes to the system architecture.

It is a change-history document.

It does NOT replace:

`00_Master_Architecture.md`

The current architecture is always determined by the latest approved Master Architecture and the latest approved Locked Specifications.

---

# 1. Change Control Rules

1. Locked architecture must not be changed casually.
2. Implementation problems do not automatically justify architectural changes.
3. A change must be proposed only when a genuine architectural contradiction, missing contract, or structural requirement is identified.
4. Every approved architectural change must record:

   * Change ID
   * Date
   * Affected stage(s)
   * Previous rule
   * New rule
   * Reason
   * Impact
   * Compatibility impact
   * Required migration
   * Approval status
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

All nine stages are currently locked.

---

# 3. Initial Architecture Baseline

### CHANGE-000 — V1 Architecture Baseline

**Status:** APPROVED

**Version:** V1.0

**Type:** BASELINE

**Affected:** Entire Architecture

**Description:**

The final V1 architecture was established as the current authoritative architecture after completion and review of Stages 1–9.

The architecture separates:

* Data Foundation
* Fundamental Analysis
* Historical/Trend Analysis
* Forecasting
* Forecast Evaluation
* Valuation
* Market Analysis
* Decision/Dashboard

Fundamental and Market analysis remain separate until the Decision Engine.

**Reason:**

To establish a stable, modular, auditable architecture before implementation.

**Impact:**

All subsequent implementation must remain compatible with this architecture unless an explicitly approved architectural change is recorded.

---

# 4. FX Architecture Baseline

### CHANGE-001 — Separate Free-Market and Operational FX

**Status:** APPROVED

**Version:** V1.0

**Affected:** Stage 1, Stage 5, Stage 7, Stage 8/9 FX Context

**Description:**

The architecture distinguishes between:

* FREE_MARKET FX
* OPERATIONAL / EXCHANGE FX

Free-market FX is used for market valuation and USD-relative market-value analysis.

Operational FX is used where appropriate for company sales and earnings exposure.

Operational FX must not silently default to free-market FX.

**Reason:**

The two rates can materially differ and serve different analytical purposes.

**Impact:**

FX data and FX-dependent calculations must preserve rate type and source.

---

# 5. Point-in-Time Baseline

### CHANGE-002 — Point-in-Time and ReportVersion Control

**Status:** APPROVED

**Version:** V1.0

**Affected:** Stage 1 and all downstream analytical stages

**Description:**

Financial information must be evaluated using the information actually available at the relevant historical cutoff date.

Report and ReportVersion are separate concepts.

Publication datetime belongs to ReportVersion.

Restated/corrected reports are versioned.

**Reason:**

Prevent look-ahead bias and preserve historical analytical integrity.

**Impact:**

Backtesting, forecasting evaluation, historical valuation, and decision history must respect information availability at the relevant time.

---

# 6. Current Architecture Changes

No post-baseline architectural changes have been approved.

---

# 7. Pending Proposals

No pending architectural proposals.

---

# 8. Change Record Template

Future architectural changes must use this structure:

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

Use for compatible architectural changes that do not invalidate the overall V1 architecture.

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

The following MAY require an architecture change:

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

**Architecture:** LOCKED

**Current Version:** V1.0

**Approved Changes After Baseline:** NONE

**Next Review Trigger:** Only when a genuine architectural issue is identified during implementation or explicitly requested by the project owner.
