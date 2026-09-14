# STAGE 0 — MASTER SYSTEM ARCHITECTURE

## LOCKED SPECIFICATION

You are helping design a compact, auditable, point-in-time financial analysis and investment decision-support system for listed companies.

This document defines the MASTER ARCHITECTURE of the system before individual Stage specifications are designed.

It is the highest-level architectural contract.

All later Stages must remain compatible with this specification unless a genuine architectural contradiction is discovered.

Do NOT redesign the architecture casually.

---

# 1. PRIMARY OBJECTIVE

Build a financial analysis system that converts:

* Codal financial reports
* Daily stock-market data
* FX / USD data

into a compact company-level decision-support system.

The system must make it possible to:

1. store financial history correctly;
2. normalize heterogeneous financial statements;
3. compare companies primarily within their industries;
4. evaluate Growth, Profitability and Risk/Quality;
5. measure historical and seasonal behavior;
6. identify fundamental trends;
7. forecast future financial performance;
8. evaluate forecast reliability;
9. estimate valuation;
10. analyze market behavior;
11. combine the outputs into a final investment decision framework;
12. display only the information required for fast decision-making.

The system is intended to support investment analysis, not merely financial-statement storage.

---

# 2. CORE DESIGN PHILOSOPHY

The system follows this principle:

> Comprehensive Data Layer → Compact Analytical Layer → Minimal Decision Layer

The Raw/Data Foundation may be comprehensive.

The final Decision Layer must remain intentionally compact.

Do not expose hundreds of financial fields simply because they are available.

Every analytical metric must justify its existence by improving one of:

* company comparison;
* trend detection;
* forecasting;
* valuation;
* risk detection;
* investment decision quality.

Avoid unnecessary analytical complexity.

---

# 3. FROZEN 9-STAGE ARCHITECTURE

The system consists of exactly these nine major Stages:

1. Data Foundation & Data Model
2. KPI Specification
3. Fundamental Scoring
4. Historical, Seasonal & Trend Engine
5. Forecast Engine
6. Forecast Evaluation & Calibration
7. Valuation Engine
8. Market Engine
9. Decision Engine & Dashboard Contract

Architecture:

```
                     DATA SOURCES
         ┌──────────────┼──────────────┐
         │              │              │
       CODAL           OHLC            FX
         │              │              │
         └──────────────┼──────────────┘
                        ▼
             DATA FOUNDATION /
             NORMALIZATION
                        │
        ┌───────────────┴───────────────┐
        ▼                               ▼
 FUNDAMENTAL ENGINE               MARKET ENGINE
        │                               │
┌───────┼────────┐                      │
▼       ▼        ▼                      │
```

Growth Profitability Risk                 │
│       │        │                      │
└───────┼────────┘                      │
▼                               │
FUNDAMENTAL SCORE                      │
│                               │
▼                               │
HISTORICAL & SEASONAL COMPARISON           │
│                               │
▼                               │
TREND ENGINE                         │
│                               │
▼                               │
FORECAST ENGINE                       │
│                               │
▼                               │
FORECAST EVALUATION & CALIBRATION           │
│                               │
▼                               │
VALUATION ENGINE                     │
│                               │
└──────────────┬────────────────┘
▼
DECISION ENGINE
│
▼
COMPANY DASHBOARD

This sequence is frozen.

Do not create additional major engines unless a later contradiction proves they are architecturally necessary.

---

# 4. SEPARATION OF FUNDAMENTAL AND MARKET ANALYSIS

Fundamental analysis and market analysis must remain separate until the Decision Engine.

Fundamental-side information includes:

* financial statements;
* financial KPIs;
* profitability;
* growth;
* financial risk;
* earnings quality;
* historical financial behavior;
* fundamental trends;
* forecasts;
* valuation.

Market-side information includes:

* OHLC;
* adjusted prices;
* volume;
* value;
* trade count;
* price behavior;
* market trend;
* market-derived indicators selected later in Stage 8.

Market information must NOT influence the Fundamental Score.

Fundamental information must NOT be mixed into the Market Engine.

The two branches meet only at Stage 9.

---

# 5. DATA SOURCES

The architecture supports three primary sources.

## A. CODAL

Used for:

* financial statements;
* monthly reports;
* quarterly reports;
* annual reports;
* corrected reports;
* corporate disclosures;
* financial-period information;
* operating data where officially available.

Codal data must retain report identity and publication timing.

## B. MARKET DATA

Daily market data should support at least:

* Open
* High
* Low
* Close
* Adjusted Close
* Volume
* Value
* Trade Count

Market data is stored from Stage 1 but analyzed only in Stage 8.

## C. FX

FX/USD data is part of the Data Foundation.

FX must NOT be created as a separate analytical engine.

Its primary uses include:

* inflation/currency-context analysis;
* conversion of IRR financial facts into USD;
* nominal vs FX-adjusted growth;
* valuation and historical comparisons where relevant.

---

# 6. POINT-IN-TIME ARCHITECTURE

Point-in-Time correctness is mandatory throughout the system.

Every financial observation must distinguish between:

* Financial Period
* Publication / Availability Date
* Report Version

These concepts must NEVER be treated as equivalent.

Example:

A financial statement may describe the period ending:

2026-06-30

but may only have become publicly available on:

2026-08-15

A backtest performed on 2026-07-15 must NOT use that report.

This rule applies to:

* KPI calculation;
* Fundamental Scores;
* historical comparisons;
* forecasts;
* forecast evaluations;
* valuation;
* backtests;
* dashboard history.

Look-ahead bias prevention is a non-negotiable requirement.

---

# 7. REPORT CORRECTIONS AND RESTATEMENTS

Corrected financial reports must never overwrite history.

The system must distinguish:

Report

from:

Report Version

A report may have multiple versions.

The system must retain:

* original publication;
* corrected publication;
* version number;
* publication datetime;
* superseded version relationships.

Current analysis may use:

Latest Valid Version.

Historical backtests must use:

The version that was available at that historical date.

---

# 8. RAW VS NORMALIZED FINANCIAL DATA

Raw financial facts and normalized financial facts must remain separate.

Raw data represents what was actually extracted from the source.

Normalized data represents standardized financial concepts.

Normalization must never destroy the original data.

Required logical relationship:

Codal Report
→ Report Version
→ Raw Financial Fact
→ Normalization Mapping
→ Normalized Financial Fact
→ KPI

If normalization rules change later, historical raw data must be re-normalizable.

---

# 9. FINANCIAL STATEMENTS FIRST

The KPI architecture follows:

> Financial Statements First

Do not design the system around arbitrary market ratios or dozens of secondary indicators.

Core fundamental analysis should originate primarily from standardized financial statement information.

Analytical priorities are:

1. Growth
2. Profitability
3. Risk & Quality

Industry-specific metrics may supplement these dimensions.

---

# 10. FUNDAMENTAL ANALYSIS STRUCTURE

The fundamental system is organized around three major analytical dimensions:

## Growth

Measures expansion or contraction of core financial performance.

## Profitability

Measures economic efficiency and profit generation.

## Risk & Quality

Measures the sustainability, cash quality and financial reliability of reported earnings.

These dimensions ultimately feed:

Fundamental Score

The score represents CURRENT FUNDAMENTAL CONDITION.

It must not include:

* price;
* P/E;
* valuation;
* technical analysis;
* forecasted market movement.

---

# 11. INDUSTRY-RELATIVE COMPARISON

Companies should primarily be compared within their own industries.

A bank should generally not be benchmarked directly against a cement company.

Industry-relative analysis may affect:

* KPI interpretation;
* benchmarking;
* scoring;
* valuation;
* industry-specific KPIs.

Industry-specific KPIs are permitted only when they add economically meaningful information beyond the universal KPIs.

They must map back to the main analytical dimensions:

* Growth
* Profitability
* Risk & Quality

Do not create an uncontrolled fourth scoring axis for industry KPIs.

---

# 12. V1 INDUSTRY SCOPE

The initial system targets exactly seven industry groups:

1. Bank
2. Investment / Holding
3. Petrochemical / Chemical
4. Metals / Mining
5. Cement
6. Food
7. Pharmaceutical

Do not automatically expand V1 to additional industries.

Additional industry packs may be designed later.

---

# 13. HISTORICAL AND SEASONAL ANALYSIS

The system must distinguish:

Current Fundamental Condition

from:

Historical Direction.

Historical comparisons should eventually support:

* MoM
* QoQ
* YoY
* Same-Period Multi-Year
* Multi-Year
* Rolling / TTM
* Seasonal Comparison

TTM is derived.

It must not be stored as a raw financial statement observation.

Historical analysis should also detect misleading growth caused by effects such as:

* Low Base
* abnormal prior period;
* one-off gains/losses;
* restatements.

Such conditions should generally be represented as context or quality flags rather than additional independent scoring votes.

---

# 14. TREND ENGINE

The Trend Engine describes the direction of fundamental change.

It does NOT replace the Fundamental Score.

Conceptually:

# Fundamental Score

Where the company stands now.

# Trend Engine

Where the fundamentals are moving.

The Trend Engine should ultimately support:

* 3M momentum;
* 6M momentum;
* 12M trend.

High-level Trend States:

* Strong Improvement
* Improving
* Stable
* Deteriorating
* Strong Deterioration

Exact mathematical definitions belong to Stage 4.

---

# 15. FORECAST ARCHITECTURE

Forecasting is a dedicated Stage.

Potential forecast targets include:

* Revenue
* Operating Profit
* Net Profit
* EPS
* Margin
* ROE

Forecasts may use scenarios:

* Bear
* Base
* Bull

Forecasts must be versioned.

Old forecasts must NEVER be overwritten.

Example:

August EPS Forecast = 1,100
September Forecast = 1,180
October Forecast = 1,270

All three forecasts must remain stored.

This enables analysis of:

Earnings Revision Trend.

---

# 16. FORECAST EVALUATION

Forecast creation and forecast evaluation are different responsibilities.

The architecture therefore has a dedicated:

Forecast Evaluation & Calibration Stage.

Process:

Forecast
→ Actual
→ Forecast Error
→ Accuracy
→ Bias
→ Reliability
→ Model Calibration

Forecast performance should eventually be evaluated across horizons such as:

* 1M
* 3M
* 6M
* 12M

Potential forecast targets include:

* Revenue
* Operating Profit
* Net Profit
* EPS
* FX

Forecast models must be compared against a simple Naive/Baseline model.

If a complex model consistently performs worse than the baseline, it must be revised or rejected.

The system may calculate:

Forecast Reliability Score: 0–100.

Forecast reliability should influence how much trust is placed in forward valuation metrics.

---

# 17. VALUATION ARCHITECTURE

Valuation is separate from Fundamental Scoring.

A strong company may still be overvalued.

A weak company may still temporarily appear statistically cheap.

Therefore:

Fundamental Quality ≠ Valuation.

Forward P/E is a priority valuation output.

Conceptual flow:

Forecast Net Profit
→ Forecast EPS
→ Current Market Price
→ Forward P/E

Forward P/E should eventually be evaluated under:

* Bear
* Base
* Bull scenarios.

When sufficient data exists, valuation context may also include:

* Historical P/E
* Industry Median P/E

Historical valuation calculations must obey Point-in-Time rules.

Do not use today's financial information to calculate a supposedly historical valuation ratio.

---

# 18. FX CONVERSION ARCHITECTURE

IRR is the base accounting currency for normalized financial facts.

USD is derived.

Default conversion principles:

## Flow variables

Examples:

* Revenue
* Operating Profit
* Net Profit

Use:

Period Average FX

## Stock variables

Examples:

* Assets
* Equity
* Debt

Use:

Period-End FX

## Market Value

Use:

Same-Date FX

The conversion method must remain traceable.

The system should be able to calculate both:

Nominal Growth

and:

USD-Adjusted Growth.

---

# 19. SHARE COUNT AND CORPORATE ACTIONS

EPS and valuation require historical share-count correctness.

The system must account for events such as:

* capital increases;
* splits;
* share-count changes;
* relevant corporate actions.

A single present-day share count must not be blindly applied to all historical periods.

---

# 20. DATA QUALITY

The system must explicitly represent data quality.

Examples of useful states:

* VALID
* MISSING
* ESTIMATED
* RESTATED
* SUSPICIOUS
* UNMAPPED

Critical principle:

NULL ≠ 0

Missing data must never automatically become zero.

Suspicious or unresolved data must not silently flow into:

* Fundamental Score;
* Forecast;
* Valuation;
* Decision Engine.

---

# 21. AUDITABILITY AND PROVENANCE

Every important derived analytical result should be traceable backward.

Conceptual chain:

Decision
→ Valuation / Market / Fundamental Inputs
→ KPI
→ Normalized Fact
→ Raw Fact
→ Report Version
→ Source Report

The system should make it possible to answer:

* Which report generated this value?
* Which report version?
* Which period?
* Which normalization rule?
* Which FX rule?
* Which scoring method?
* Which forecast model/version?

Black-box calculations should be avoided where practical.

---

# 22. VERSIONING OF ANALYTICAL LOGIC

Important analytical systems should be versionable.

Examples:

* normalization rules;
* KPI definitions;
* scoring rules;
* forecasting models;
* calibration methods;
* valuation methods;
* decision rules.

Historical analysis should remain reproducible even after analytical logic evolves.

---

# 23. NO DOUBLE COUNTING

The architecture must actively prevent the same economic information from receiving multiple artificial votes.

Examples:

Revenue Growth
→ Operating Profit Growth
→ Net Profit Growth
→ EPS Growth

These belong to the same economic cascade.

Similarly:

Gross Margin
Operating Margin
Net Margin

are related profitability measures.

Industry KPIs may also overlap with universal KPIs.

Later scoring systems must control these overlaps through:

* weighting;
* substitution;
* weight redistribution;
* diagnostics.

Do not simply add every available metric into the score.

---

# 24. EXTERNAL DATA POLICY

The V1 fundamental architecture should not depend on unnecessary external datasets.

A company should remain analyzable even when data such as the following is unavailable:

* global commodity price;
* feedstock price;
* export share;
* detailed production volume;
* selling price;
* macro indicators;
* external industry datasets.

Such information may later be used as:

* Diagnostic variables;
* Forecast Drivers;
* Context variables.

They are not mandatory Core KPIs unless explicitly specified later.

---

# 25. RAW LAYER VS DECISION LAYER

The system must avoid confusing data availability with decision usefulness.

The database may contain thousands of raw observations.

The dashboard should not.

The final decision layer should surface only the signals that materially affect a decision.

Conceptually:

DATA
↓
NORMALIZATION
↓
KPIs
↓
SCORING / TREND / FORECAST / VALUATION / MARKET
↓
DECISION SIGNALS
↓
COMPACT DASHBOARD

---

# 26. STAGE RESPONSIBILITIES

## Stage 1 — Data Foundation & Data Model

Defines how data is stored, normalized, versioned and traced.

It should NOT prematurely define final scoring or forecasting logic.

---

## Stage 2 — KPI Specification

Defines WHAT should be measured.

It should NOT define the final scoring algorithm.

---

## Stage 3 — Fundamental Scoring

Defines HOW fundamental KPIs are converted into:

* Growth Score
* Profitability Score
* Risk & Quality Score
* Fundamental Score

It must not contain valuation or market signals.

---

## Stage 4 — Historical, Seasonal & Trend Engine

Defines historical comparison, seasonality and direction of fundamentals.

It must not create a duplicate Fundamental Score.

---

## Stage 5 — Forecast Engine

Creates forward-looking financial estimates and scenarios.

Forecast versions must be preserved.

---

## Stage 6 — Forecast Evaluation & Calibration

Measures forecast quality and model reliability.

It should improve future forecasting and inform confidence in forward-looking metrics.

---

## Stage 7 — Valuation Engine

Evaluates price relative to financial value.

It consumes fundamental and forecast outputs but remains logically separate from Fundamental Score.

---

## Stage 8 — Market Engine

Analyzes OHLC and market behavior.

It must remain separate from fundamental analysis until Stage 9.

---

## Stage 9 — Decision Engine & Dashboard Contract

Combines the final outputs into a compact company-level investment decision framework.

It also defines exactly what the dashboard should display.

---

# 27. STAGE DEVELOPMENT METHOD

Each Stage must be developed independently.

Required workflow:

DESIGN
→ AUDIT
→ CORRECT
→ TEST where applicable
→ LOCK

Only after a Stage is locked should the next Stage be developed.

Do not casually reopen locked Stages.

If a later Stage reveals a genuine conflict with a locked Stage:

1. identify the exact contradiction;
2. determine whether it is:

   * an architectural contradiction;
   * an implementation detail;
3. explain the impact;
4. change the earlier Stage only if truly required.

Locked specifications act as contracts between Stages.

---

# 28. STAGE OUTPUT DISCIPLINE

Each Stage specification should clearly define:

* Objective
* Inputs
* Outputs
* Rules
* Calculations
* Missing-data handling
* Point-in-Time behavior
* Industry behavior where relevant
* Versioning requirements
* Auditability requirements
* Edge cases
* Validation checklist
* Explicit exclusions

A Stage is not considered LOCKED until it has been reviewed against the Master Architecture.

---

# 29. DESIGN CONSTRAINTS

Avoid:

* giant KPI libraries;
* dozens of technical indicators;
* redundant ratios;
* overlapping scoring votes;
* unnecessary external-data dependencies;
* overly complex statistical models in V1;
* hidden look-ahead bias;
* overwriting historical reports;
* overwriting forecast versions;
* mixing valuation into Fundamental Score;
* mixing market signals into Fundamental Score;
* turning missing data into zero;
* premature optimization.

Prefer:

* economically interpretable metrics;
* small KPI sets;
* explicit formulas;
* transparent rules;
* versioned logic;
* industry-relative comparisons;
* traceable calculations;
* minimal dashboard outputs.

---

# 30. SYSTEM SUCCESS CRITERIA

The architecture should eventually allow the system to answer questions such as:

* Is the company growing?
* Is profitability improving?
* Are earnings high quality?
* Is financial risk increasing?
* Is the current period stronger than historical norms?
* Is the change seasonal or structurally meaningful?
* Are fundamentals improving or deteriorating?
* What is the expected future Revenue / Profit / EPS?
* How reliable is that forecast?
* Is valuation expensive or cheap relative to expectations?
* What is the market currently doing?
* Are fundamental and market signals aligned?
* What are the main reasons for the final investment signal?

without forcing the analyst to manually inspect hundreds of financial-statement rows.

---

# 31. NON-NEGOTIABLE ARCHITECTURAL RULES

The following rules are LOCKED:

1. Exactly nine major Stages.
2. Fundamental and Market branches remain separate until Stage 9.
3. FX belongs to Data Foundation, not a separate analytical engine.
4. OHLC is stored in Stage 1 and analyzed in Stage 8.
5. Fundamental Score contains no valuation or market information.
6. Valuation is a separate Stage.
7. Forecast Evaluation is separate from Forecast creation.
8. Forecast versions are never overwritten.
9. Report corrections are versioned.
10. Point-in-Time correctness is mandatory.
11. Raw data is never destroyed by normalization.
12. IRR is base financial currency; USD is derived.
13. Flow vs Stock FX conversion rules differ.
14. Historical share-count changes must be preserved.
15. NULL is not zero.
16. Companies are primarily benchmarked within their industry.
17. Industry KPIs map back to Growth / Profitability / Risk & Quality.
18. Avoid Double Counting.
19. Raw/Data Layer may be comprehensive.
20. Decision Layer must remain minimal.
21. Stage specifications must be designed, audited and locked sequentially.
22. Locked Stages must not be reopened without a genuine contradiction.
23. Every major analytical output should remain auditable back to its source.
24. Analytical logic should be versionable where materially relevant.

---

# 32. CURRENT ARCHITECTURAL STATUS

Master Architecture:

LOCKED

Stage 1:
Data Foundation & Data Model
LOCKED

Stage 2:
KPI Specification
LOCKED

Stage 3:
Fundamental Scoring
LOCKED

Stage 4:
Historical, Seasonal & Trend Engine
DESIGN IN PROGRESS / NOT YET LOCKED

Stage 5:
Forecast Engine
NOT YET DESIGNED

Stage 6:
Forecast Evaluation & Calibration
NOT YET DESIGNED

Stage 7:
Valuation Engine
NOT YET DESIGNED

Stage 8:
Market Engine
NOT YET DESIGNED

Stage 9:
Decision Engine & Dashboard Contract
NOT YET DESIGNED

---

# 33. INSTRUCTION FOR FUTURE CHATS

If this specification is pasted into a completely new conversation:

Treat it as the authoritative Master Architecture.

Do not redesign Stages 1–3 unless a genuine contradiction is identified.

If the individual Locked Specification of a Stage is also provided, that Stage-specific specification takes precedence on implementation details while remaining subordinate to this Master Architecture on system-level structure.

When continuing development:

1. identify the first Stage that is not LOCKED;
2. work only on that Stage;
3. preserve all locked architectural boundaries;
4. audit the Stage before locking it;
5. do not jump ahead and redesign later Stages in detail;
6. mention later-stage implications only when necessary to prevent an architectural mistake.

The objective is architectural continuity, reproducibility and prevention of design drift.

---

# FINAL STATUS

STAGE 0 — MASTER SYSTEM ARCHITECTURE

DESIGNED
RECONSTRUCTED FROM FINAL SYSTEM DECISIONS
CROSS-CHECKED AGAINST LOCKED STAGES
LOCKED
