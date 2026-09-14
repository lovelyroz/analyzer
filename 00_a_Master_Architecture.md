# 00_Master_Architecture

## Locked Master Architecture — V1

**Purpose:** Master reference for the complete 9-stage financial analysis and investment decision-support system for listed companies.

**Status:** LOCKED  
**Version:** V1  
**Last architectural review:** Final Stage 9 audit — PASS

---

# 1. System Objective

Build a compact, auditable, point-in-time financial analysis and investment decision-support system that converts:

- Codal financial reports
- Daily stock-market OHLC data
- Free-market and operational/exchange FX data

into a compact company-level decision-support framework.

The system must support:

1. Correct financial-history storage
2. Normalization of heterogeneous financial statements
3. Industry-relative comparison
4. Growth, Profitability and Risk/Quality analysis
5. Historical and seasonal analysis
6. Fundamental trend detection
7. Forward financial forecasting
8. Forecast evaluation, reliability and calibration
9. Valuation, with Forward P/E as a priority
10. Market-state analysis
11. FX/USD context and USD-relative valuation
12. Final investment-state decision
13. Compact dashboard presentation

Core philosophy:

> Comprehensive Data Layer → Compact Analytical Layer → Minimal Decision Layer

The database may be comprehensive; the decision layer must remain compact.

---

# 2. Frozen 9-Stage Architecture

The system consists of exactly nine major stages:

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

```text
DATA SOURCES
 ┌──────────────┬──────────────┬──────────────┐
 │              │              │
CODAL          OHLC            FX
 │              │              │
 └──────────────┼──────────────┘
                ▼
       DATA FOUNDATION /
       NORMALIZATION
                │
        ┌───────┴────────┐
        ▼                ▼
 FUNDAMENTAL          MARKET
   BRANCH             BRANCH
        │                │
        ▼                │
 FUNDAMENTAL SCORE       │
        │                │
        ▼                │
 HISTORICAL / SEASONAL   │
        │                │
        ▼                │
      TREND              │
        │                │
        ▼                │
    FORECAST             │
        │                │
        ▼                │
 FORECAST EVALUATION     │
        │                │
        ▼                │
    VALUATION            │
        │                │
        └───────┬────────┘
                │
          FX CONTEXT
                │
                ▼
        DECISION ENGINE
                │
                ▼
          DASHBOARD
```

Fundamental and Market analysis remain separate until Stage 9.

Do not create additional major analytical engines in V1 unless a genuine architectural contradiction proves one necessary.

---

# 3. Stage Responsibilities

## Stage 1 — Data Foundation & Data Model

Owns:

- Company and Industry entities
- Financial periods
- Reports and ReportVersions
- Raw and normalized financial facts
- FX data and conversion rules
- Market daily data
- Share-count history
- Corporate actions
- Data quality
- Ingestion tracking
- Point-in-Time provenance

Raw data is never destroyed by normalization.

---

## Stage 2 — KPI Specification

Defines WHAT is measured.

Universal Core:

### Growth
- Revenue Growth
- Operating Profit Growth
- Net Profit Growth
- EPS Growth

### Profitability
- Gross Margin
- Operating Margin
- Net Profit Margin
- ROA
- ROE

### Risk & Quality
- Cash Earnings Conversion
- Earnings Quality

Conditional:

- Financial Cost Pressure

V1 industry groups:

1. Bank
2. Investment / Holding
3. Petrochemical / Chemical
4. Metals / Mining
5. Cement
6. Food
7. Pharmaceutical

Industry KPIs must add meaningful information and map back to Growth, Profitability or Risk & Quality.

---

## Stage 3 — Fundamental Scoring

Produces Fundamental Score 0–100.

Default top-level weighting:

- Growth: 30%
- Profitability: 45%
- Risk & Quality: 25%

Fundamental Score represents current fundamental condition.

It must NOT contain:

- Price
- P/E
- Valuation
- Technical/market analysis
- Forecasted market movement

Industry-relative comparison is primary where sufficient peers exist.

No double counting of correlated financial information.

---

## Stage 4 — Historical, Seasonal & Trend Engine

Answers:

> How does current fundamental performance compare with history, and in what direction is it moving?

Supports:

- MoM
- QoQ
- YoY
- Same-period multi-year
- Multi-year trend
- Rolling/TTM
- Seasonal baseline and surprise
- 3M momentum
- 6M momentum
- 12M trend

Trend states:

- Strong Improvement
- Improving
- Stable
- Deteriorating
- Strong Deterioration

Trend does not modify Fundamental Score directly and does not create a second score.

---

## Stage 5 — Forecast Engine

Produces future financial estimates.

V1 architecture uses two forecast families:

### Non-Financial
For:

- Petrochemical/Chemical
- Metals/Mining
- Cement
- Food
- Pharmaceutical

Core chain:

Revenue → Operating Margin → Operating Profit → Net Profit → EPS → ROE

### Financial
For:

- Bank
- Investment/Holding

Bank:

Loans/Deposits → NII/NIM → Net Profit → EPS → ROE

Holding:

NAV → NAV Growth → Net Profit → EPS → ROE

Forecast scenarios:

- Bear
- Base
- Bull

Forecasts are versioned and never overwritten.

Forecast reliability is evaluated later by Stage 6.

---

## Stage 6 — Forecast Evaluation & Calibration

Separates forecast creation from forecast evaluation.

Process:

Forecast → Actual → Error → Accuracy/Bias → Baseline Comparison → Reliability → Calibration

Supports:

- 1M
- 3M
- 6M
- 12M

Forecast Reliability is 0–100.

Forecast models are compared against a simple Point-in-Time baseline.

Persistent systematic bias may produce a new calibrated Model Version.

Old model versions remain preserved.

---

## Stage 7 — Valuation Engine

Core purpose:

> Given future earnings, how reasonable or attractive is the current share price?

Primary valuation axis:

```text
Forward P/E = Current Market Price / Forecast EPS
```

Scenarios:

- Bear Forward P/E
- Base Forward P/E
- Bull Forward P/E

Valuation also considers:

- Historical Point-in-Time TTM P/E
- Historical Median P/E
- Industry Forward P/E
- Industry TTM P/E
- Fair Values
- Scenario probabilities
- Expected Fair Value
- Expected Upside
- Scenario dispersion
- Forecast Reliability
- Valuation Confidence
- Valuation Risk
- Sensitivity and driver ranking
- Valuation alerts

If EPS is negative, zero or in an invalid sign-change state, P/E valuation is NOT_APPLICABLE. No artificial P/E or fair price is created.

Fundamental Score does not mathematically multiply Target P/E.

---

## Stage 8 — Market Engine

Stage 8 is a Market State Engine, not a Market Score Engine.

V1 does NOT include a Market Score.

Core areas:

- Price structure
- Returns
- Price vs moving averages
- Trend
- Momentum
- Volatility
- Drawdown
- Relative strength
- Liquidity
- Volume behavior
- Price-volume confirmation
- Market regime
- Market alerts

Market analysis must remain separate from fundamental analysis until Stage 9.

Adjusted Close is preferred for performance/return calculations.

Market conditions do not directly modify Fundamental Score, Forecast EPS or Target P/E.

---

## Stage 9 — Decision Engine & Dashboard Contract

Purpose:

> Given fundamentals, future earnings, valuation and market behavior, what is the investment state of the share?

Stage 9 is a Rule-Based Evidence Integration Engine.

It consumes:

- Fundamental Quality
- Fundamental Direction
- Forecast
- Forecast Reliability
- Valuation
- Market State
- FX Context

It does not recreate upstream analysis.

Decision states:

- STRONG_BUY
- BUY
- HOLD
- WATCH
- REDUCE
- SELL
- STRONG_SELL

Decision is NOT a simple weighted sum.

HOLD is a valid primary state.

---

# 4. Decision Evidence Families

Stage 9 integrates four families:

### A. Fundamental Quality
From Stage 3.

### B. Fundamental Direction & Future
From Stages 4, 5 and 6.

### C. Valuation
From Stage 7.

### D. Market State
From Stage 8.

The same economic information must not receive multiple artificial votes.

---

# 5. Decision Safety Rules

The following are locked:

- Cheap + Weak must not automatically produce BUY.
- Strong + Expensive must not automatically produce BUY.
- Low Forecast Reliability reduces confidence; it does not automatically produce SELL.
- Negative EPS/sign change prevents artificial P/E-driven decisions.
- Scenario dispersion must not be hidden by Expected Upside.
- Insufficient data prevents high-confidence decisions.
- Very low liquidity is execution risk, not automatic SELL.
- Market-only rallies do not override weak fundamentals.
- Strong fundamentals do not automatically imply BUY when valuation is excessive.
- Decision ≠ Trading Signal.

---

# 6. Holding Status

Holding is evaluated separately from Decision.

V1 Holding Status:

- STRONG_HOLD
- HOLD
- HOLD_WITH_CAUTION
- REVIEW_HOLD
- EXIT_CANDIDATE

Position sizing is outside V1.

---

# 7. Decision Confidence

Decision Confidence is separate from Decision.

It reflects factors such as:

- Data Quality
- Evidence agreement
- Forecast Reliability
- Valuation Confidence
- Scenario dispersion
- Decision conflicts
- Market confirmation
- Data sufficiency

Confidence is not simply another name for Fundamental Score.

---

# 8. Hysteresis and Decision Stability

Decision changes must not occur because of insignificant threshold fluctuations.

Entry and exit thresholds may differ.

Hysteresis parameters are Model Version Parameters.

Decision History is mandatory.

At minimum:

- Previous Decision
- Current Decision
- Decision Change
- Change Date
- Change Reasons

---

# 9. Risk-Aware Ranking

V1 does not create a new Ranking Score.

Primary ranking is within industry.

Ranking priority:

1. Decision State / Tier
2. Decision Confidence
3. Expected Upside
4. Valuation Risk
5. Forecast Reliability
6. Fundamental Quality

Ranking eligibility must respect data quality and valuation reliability.

---

# 10. FX Architecture

FX is part of Stage 1 Data Foundation and is consumed as context by later stages.

There are two distinct USD rates:

## Free-Market FX

Used primarily for:

- Market Cap USD
- Share Price USD
- USD-adjusted return
- Historical company value in USD
- USD-relative market valuation

## Operational / Exchange FX

Used where economically appropriate for:

- Company sales
- Export revenue
- FX-linked operating earnings
- Earnings forecasting

The two rates must NEVER be silently merged.

---

# 11. FX Conversion Rules

IRR is the base accounting currency.

USD is derived.

### Flow variables

Examples:

- Revenue
- Operating Profit
- Net Profit

Default:

> Period-average FX

### Stock variables

Examples:

- Assets
- Equity
- Debt

Default:

> Period-end FX

### Market value

Default:

> Same-date Free-Market FX

All conversion methods must be traceable.

---

# 12. FX Decision Context

Stage 9 may consume:

- fx_regime
- fx_company_impact
- usd_relative_valuation_context
- free_market_fx
- operational_fx
- fx_gap

where data is available.

```text
FX Gap = Free Market FX / Operational FX - 1
```

FX Gap is contextual only.

It is NOT a standalone Buy/Sell signal.

---

# 13. FX Double-Counting Rule

Correct path:

```text
Operational FX
      ↓
Company FX Exposure
      ↓
Revenue / Cost / Margin
      ↓
Forecast EPS
      ↓
Forward P/E
      ↓
Decision
```

Stage 9 must not add a second independent FX Buy/Sell vote.

---

# 14. FX Missing-Data Rule

Operational FX missing:

```text
Operational FX = MISSING
```

It must NOT silently default to Free-Market FX.

If a proxy is used, it must be explicit, for example:

```text
FX_ASSUMPTION = ESTIMATED
SOURCE = FREE_MARKET_PROXY
CONFIDENCE = LOW
```

Unknown company FX exposure means no assumed positive or negative effect.

---

# 15. USD-Relative Valuation Context

Example:

```text
Stock Return < Free-Market USD Return
```

means the stock has lagged USD in nominal terms.

This is an opportunity/context indicator only.

It does not automatically mean BUY.

It must be evaluated together with:

- Fundamental Quality
- Trend
- Forecast EPS
- Forecast Reliability
- Forward P/E
- Valuation Risk
- Market State

A stock can be cheap in USD terms and still be a value trap.

---

# 16. Data Quality

The architecture explicitly supports:

- VALID
- MISSING
- ESTIMATED
- RESTATED
- SUSPICIOUS
- UNMAPPED

Critical rule:

> NULL ≠ 0

Suspicious or unresolved data must not silently flow into Score, Forecast, Valuation or Decision.

---

# 17. Point-in-Time Architecture

Every financial observation must distinguish:

- Financial Period
- Publication/Availability Date
- Report Version

Historical analysis and backtesting may use only information available at the relevant historical date.

This applies to:

- Codal
- Reports
- FX
- Forecasts
- Forecast Evaluation
- Valuation
- Market data
- Decisions

Look-ahead bias is prohibited.

---

# 18. Restatements

Report and ReportVersion are separate.

Corrected reports must never overwrite historical availability.

Current analysis may use the Latest Valid Version.

Historical backtests must use the version that was actually available at the historical date.

---

# 19. Share Count and Corporate Actions

Historical share count must be preserved.

EPS and historical valuation must account for relevant:

- Capital increases
- Splits
- Share-count changes
- Corporate actions

A present-day share count must not be blindly applied to historical periods.

---

# 20. Auditability

Important outputs must remain traceable:

```text
Decision
 ↓
Valuation / Market / Fundamental Inputs
 ↓
KPI
 ↓
Normalized Financial Fact
 ↓
Raw Financial Fact
 ↓
Report Version
 ↓
Source Report
```

The system should be able to answer:

- Which source generated the value?
- Which report version?
- Which period?
- Which normalization rule?
- Which FX rule?
- Which scoring version?
- Which forecast model/version?
- Which decision model/version?

---

# 21. Versioning

Versioning applies to materially important analytical logic, including:

- Normalization
- KPI definitions
- Scoring
- Forecast models
- Forecast calibration
- Valuation
- Decision rules
- Hysteresis
- Ranking parameters

Historical results should remain reproducible.

Example:

```text
V1.0
V1.1
V1.2
V2.0
```

A minor internal change that preserves the Stage Contract may remain within V1.x.

A Contract or architectural change requires explicit versioning and downstream migration.

---

# 22. No Double Counting

The system must actively prevent correlated information from receiving multiple artificial votes.

Examples:

```text
Revenue Growth
→ Operating Profit Growth
→ Net Profit Growth
→ EPS Growth
```

and:

```text
Gross Margin
→ Operating Margin
→ Net Margin
```

These are related economic cascades.

Scoring and Decision layers must account for these relationships.

---

# 23. External Data Policy

V1 should remain primarily based on:

- Codal financial statements
- Market OHLC
- FX data

External datasets such as:

- Global commodity prices
- Feedstock prices
- Detailed export share
- External production data
- Macro datasets

are not mandatory Core V1 inputs.

They may later become Diagnostic Variables, Forecast Drivers or Context Variables if formally incorporated and validated.

---

# 24. Dashboard Contract

The dashboard must remain compact.

### Primary

```text
Company
Current Price
Decision
Decision Confidence
```

### Core Context

```text
Fundamental
Trend
Forecast
Forecast Reliability
Valuation
Expected Upside
Valuation Risk
Market
Relative Strength
Liquidity
FX Context
```

### Explanation

```text
Why?
Risks
Bear / Base / Bull
Scenario probabilities
Decision history
```

The dashboard displays upstream outputs; it does not recompute them.

---

# 25. Development Method

Each Stage follows:

```text
DESIGN
→ REVIEW
→ STRESS TEST
→ AUDIT
→ LOCK
```

Do not casually reopen a locked Stage.

If a later Stage reveals a genuine conflict:

1. Identify the exact contradiction.
2. Determine whether it is architectural or implementation-level.
3. Explain downstream impact.
4. Change the earlier Stage only if truly necessary.
5. Version the change explicitly.

---

# 26. Locked Architectural Boundaries

The following are non-negotiable for V1:

1. Exactly nine major Stages.
2. Fundamental and Market branches remain separate until Stage 9.
3. FX is part of Data Foundation, not a separate major engine.
4. Free-Market and Operational FX remain distinct.
5. OHLC is stored in Stage 1 and analyzed in Stage 8.
6. Fundamental Score contains no valuation or market information.
7. Forecast Evaluation is separate from Forecast creation.
8. Forecast versions are never overwritten.
9. Report corrections are versioned.
10. Point-in-Time correctness is mandatory.
11. Raw data is never destroyed by normalization.
12. IRR is the base financial currency; USD is derived.
13. Flow and Stock FX conversion rules differ.
14. Historical share-count changes are preserved.
15. NULL is not zero.
16. Companies are primarily compared within their own industry.
17. Industry KPIs map to Growth / Profitability / Risk & Quality.
18. Double Counting is actively controlled.
19. Raw/Data Layer may be comprehensive.
20. Decision Layer must remain minimal.
21. Decision is Rule-Based Evidence Integration.
22. Market Score does not exist in V1.
23. Decision is not a Trading Signal.
24. HOLD is a legitimate Decision.
25. Holding Status is separate from Decision.
26. Hysteresis is mandatory.
27. Decision History is mandatory.
28. Ranking is risk-aware and primarily within industry.
29. Ranking does not create a new V1 score.
30. FX is not a standalone Buy/Sell signal.
31. Operational FX must not silently default to Free-Market FX.
32. USD-relative cheapness does not equal value.
33. Negative EPS must not create artificial P/E.
34. Insufficient data must constrain Decision confidence.
35. All major outputs must be auditable.
36. Analytical logic must be versionable where materially relevant.

---

# 27. Current Locked Status

| Stage | Status |
|---|---|
| Stage 0 — Master Architecture | LOCKED |
| Stage 1 — Data Foundation & Data Model | LOCKED |
| Stage 2 — KPI Specification | LOCKED |
| Stage 3 — Fundamental Scoring | LOCKED |
| Stage 4 — Historical, Seasonal & Trend Engine | LOCKED |
| Stage 5 — Forecast Engine | LOCKED |
| Stage 6 — Forecast Evaluation & Calibration | LOCKED |
| Stage 7 — Valuation Engine | LOCKED |
| Stage 8 — Market Engine | LOCKED |
| Stage 9 — Decision Engine & Dashboard Contract | LOCKED |

Final Stage 9 audit:

```text
Architecture Integration      PASS
Double Counting               PASS
FX/USD Architecture           PASS
Free vs Operational FX        PASS
FX → Forecast/EPS             PASS
USD Valuation                 PASS
Decision / Holding            PASS
Ranking                       PASS
Hysteresis                    PASS
Point-in-Time                 PASS
Data Quality                  PASS
Explainability                PASS
Dashboard                     PASS
```

**MASTER ARCHITECTURE V1 = LOCKED**

---

# 28. Future Architecture Review Protocol

If the architecture must be reconsidered in the future, review all Stage Specifications together with this Master Architecture.

Do not assume the current architecture is permanently correct.

A future Architecture Review must:

1. Review Stage 0 and all Stage 1–9 Locked Specifications.
2. Identify contradictions or missing dependencies.
3. Check Double Counting.
4. Check Point-in-Time integrity.
5. Check Forecast → Reliability → Valuation → Decision flow.
6. Check Free-Market vs Operational FX separation.
7. Check USD-relative valuation logic.
8. Check Fundamental vs Market separation.
9. Check Decision/Holding/Ranking logic.
10. Determine whether each proposed change is:
   - internal implementation change,
   - Stage Contract change,
   - or genuine architecture change.
11. Assess downstream impact.
12. Preserve the existing V1 architecture unless evidence justifies a revision.
13. Version any accepted architectural revision explicitly.

The objective is to prevent architectural drift while keeping the system revisable when real evidence demonstrates that revision is necessary.

---

# FINAL

**00_Master_Architecture.md**

This file is the highest-level human-readable map of the complete V1 system.

The individual Stage Locked Specifications contain the detailed contracts and rules for each Stage.

When both are available:

- Master Architecture governs system-level structure.
- Stage Locked Specification governs the detailed implementation contract of that Stage.
- A genuine conflict must be explicitly identified and resolved through versioned architecture review.

**V1 ARCHITECTURE: LOCKED**
