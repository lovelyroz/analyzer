# Stage 3 — Fundamental Scoring

## Locked Specification

### 1. Objective

Design and implement a **Fundamental Scoring Engine** that converts the standardized KPIs defined in Stage 2 into a single **Fundamental Score from 0 to 100**.

The Fundamental Score must measure the company's **current fundamental condition only**.

It must NOT include:

* Market price
* P/E
* P/B
* P/NAV
* Valuation
* Technical analysis
* Trading volume
* Market momentum
* Forecast results
* Forecast reliability
* Future expectations

Those belong to later stages.

---

# 2. Inputs

Stage 3 may use only:

1. Standardized KPIs from Stage 2
2. Their KPI Scores (0–100)
3. Industry classification
4. Peer-group information
5. Historical company data only for fallback benchmarking and data-context validation

Do not introduce new analytical KPIs.

---

# 3. Fundamental Score Architecture

The Fundamental Score has exactly three axes:

| Axis           |   Weight |
| -------------- | -------: |
| Growth         |      30% |
| Profitability  |      45% |
| Risk & Quality |      25% |
| **Total**      | **100%** |

The three axis weights are fixed for Stage 3 implementation.

Industry-specific weighting may change the distribution of KPI weights **inside an axis**, but must never create an additional scoring axis or increase the total weight above 100%.

---

# 4. KPI Scoring

Every KPI must first be converted into a standardized score from 0 to 100.

Conceptually:

Raw KPI
→ Comparable KPI
→ Benchmark
→ KPI Score (0–100)

Each KPI must have a direction:

* HIGHER_IS_BETTER
* LOWER_IS_BETTER
* TARGET_RANGE

TARGET_RANGE should be used sparingly and only when economically justified.

---

# 5. Primary Benchmark

The primary benchmark is **Industry Relative**.

The preferred method is **Percentile Ranking within the relevant peer group**.

Conceptually:

* Approximately 90th percentile → approximately Score 90
* Approximately 50th percentile → approximately Score 50
* Approximately 10th percentile → approximately Score 10

For LOWER_IS_BETTER KPIs, the ranking direction must be inverted so that better economic performance receives the higher score.

Examples:

* Revenue Growth → HIGHER_IS_BETTER
* ROE → HIGHER_IS_BETTER
* NPL → LOWER_IS_BETTER

---

# 6. Minimum Peer Count

Industry percentile scoring must not be trusted when the peer group is too small.

Minimum Peer Count:

**8 companies**

Rules:

```text
Peer Count >= 8
→ Industry Percentile Benchmark

Peer Count < 8
→ Historical Company Benchmark
```

If neither sufficient peer data nor sufficient historical data exists:

```text
KPI Score = INSUFFICIENT_DATA
```

Do not manufacture a score.

---

# 7. Historical Benchmark

Historical company performance is a **fallback benchmark**, not an additional scoring vote.

Historical comparison must NOT be added to the industry-relative score.

Do not calculate:

```text
Industry Score + Historical Score
```

Instead:

```text
Industry Benchmark
        ↓
if insufficient
        ↓
Historical Company Benchmark
```

Historical information may also provide context for unusual values, but must not create duplicate scoring.

---

# 8. Growth Axis

The Growth axis has a total weight of 30% in the Fundamental Score.

Default universal Growth weighting:

| KPI                     | Weight inside Growth |
| ----------------------- | -------------------: |
| Revenue Growth          |                  15% |
| Operating Profit Growth |                  25% |
| Net Profit Growth       |                  30% |
| EPS Growth              |                  30% |
| **Total**               |             **100%** |

Formula:

```text
Growth Score =
0.15 × Revenue Growth Score
+ 0.25 × Operating Profit Growth Score
+ 0.30 × Net Profit Growth Score
+ 0.30 × EPS Growth Score
```

Then:

```text
Growth Contribution =
Growth Score × 0.30
```

The weighting reflects the analytical cascade:

Revenue
→ Operating Profit
→ Net Profit
→ EPS

The four growth KPIs must not be interpreted as four completely independent economic events.

---

# 9. Profitability Axis

The Profitability axis has a total weight of 45%.

Default weighting:

| KPI               | Weight inside Profitability |
| ----------------- | --------------------------: |
| Gross Margin      |                         10% |
| Operating Margin  |                         25% |
| Net Profit Margin |                         20% |
| ROA               |                         20% |
| ROE               |                         25% |
| **Total**         |                    **100%** |

Formula:

```text
Profitability Score =
0.10 × Gross Margin Score
+ 0.25 × Operating Margin Score
+ 0.20 × Net Profit Margin Score
+ 0.20 × ROA Score
+ 0.25 × ROE Score
```

Then:

```text
Profitability Contribution =
Profitability Score × 0.45
```

Margin, ROA and ROE are not identical measures and may all be used, but the implementation must prevent excessive double counting of economically overlapping information.

---

# 10. Risk & Quality Axis

The Risk & Quality axis has a total weight of 25%.

Default weighting:

| KPI                      | Weight inside Risk & Quality |
| ------------------------ | ---------------------------: |
| Cash Earnings Conversion |                          40% |
| Earnings Quality         |                          60% |
| **Total**                |                     **100%** |

Formula:

```text
Risk & Quality Score =
0.40 × Cash Earnings Conversion Score
+ 0.60 × Earnings Quality Score
```

Then:

```text
Risk & Quality Contribution =
Risk & Quality Score × 0.25
```

---

# 11. Financial Cost Pressure

Financial Cost Pressure is a conditional Stage 2 KPI.

In the base Fundamental Score it does **not** receive an independent weight.

It must not be added as an extra percentage to the score.

For Stage 3 it is treated as:

```text
Financial Cost Pressure
→ Diagnostic / Adjustment candidate
```

Do not create an additional scoring axis for it.

Any future adjustment mechanism must be explicitly designed and validated separately.

---

# 12. Industry-Specific KPIs

Industry-specific KPIs must be incorporated **inside the existing three axes**.

They must never create:

```text
Growth
Profitability
Risk & Quality
Industry Bonus
```

There is no Industry Bonus.

Industry KPIs are not additive bonuses.

When an Industry KPI materially overlaps with a Universal KPI, its weight must be reduced or redistributed rather than simply added.

General rule:

> Industry-specific KPIs may replace or redistribute weight within an existing axis when they provide economically relevant information, but they must not expand the total score beyond 100.

---

# 13. Industry Weighting Profiles

Industry-specific weighting profiles are permitted inside the existing three axes.

The axis totals must remain unchanged:

```text
Growth = 30%
Profitability = 45%
Risk & Quality = 25%
```

For example:

### Bank

Industry KPIs:

* Loan Growth
* Deposit Growth
* NII
* NIM
* NPL

They are mapped as follows:

```text
Loan Growth / Deposit Growth
→ Growth

NII / NIM
→ Profitability

NPL
→ Risk & Quality
```

They must be integrated by redistributing weights within those axes.

They must not be added on top of the Universal KPI weights.

### Investment / Holding

Industry KPIs:

* NAV
* NAV Growth
* P/NAV

These must similarly be mapped into existing axes without creating a fourth axis or additive bonus.

The same principle applies to other Stage 2 industry groups.

---

# 14. Double Counting Control

Double counting is a core Stage 3 control.

The system must detect economically overlapping KPIs.

Examples:

```text
Revenue Growth
        ↓
Operating Profit Growth
        ↓
Net Profit Growth
        ↓
EPS Growth
```

and:

```text
Loan Growth
        ↓
NII Growth
        ↓
Operating Profit Growth
        ↓
Net Profit Growth
```

The second chain is particularly relevant for banks.

Do not give every related KPI an unrestricted independent vote.

Rule:

> If an Industry KPI materially overlaps with a Universal KPI, redistribute the relevant axis weights instead of adding the Industry KPI as a new bonus.

The same principle applies to overlapping profitability measures.

---

# 15. Missing Data

Critical rule:

**Missing ≠ 0**

If a KPI is unavailable, do not assign it Score 0.

Instead, redistribute its weight proportionally among the available KPIs within the same axis.

Example:

Original Growth weights:

```text
Revenue Growth       15%
Operating Growth     25%
Net Profit Growth    30%
EPS Growth           30%
```

If EPS Growth is missing:

```text
Available weight = 15 + 25 + 30 = 70
```

Normalize the remaining weights:

```text
Revenue Growth       15 / 70
Operating Growth     25 / 70
Net Profit Growth   30 / 70
```

This prevents missing information from being interpreted as poor performance.

---

# 16. Minimum Axis Coverage

Each axis must have sufficient data coverage before producing a reliable axis score.

Minimum Axis Coverage:

**60%**

Example:

```text
Growth:
Revenue Growth       available
Operating Growth     available
Net Profit Growth    available
EPS Growth           missing

Available original weight = 70%
```

Therefore:

```text
Coverage = 70%
```

The Growth Score may be calculated.

If available original weight is below 60%:

```text
Axis Score = INSUFFICIENT_DATA
```

Do not assign zero.

Do not manufacture missing KPI scores.

---

# 17. Final Score with Missing Axes

The same principle applies at the overall level.

The system must distinguish:

* Good performance
* Poor performance
* Missing information
* Insufficient data

A missing axis must never automatically become zero.

If an axis is unavailable because of insufficient data, the implementation must preserve a clear data-quality state rather than falsely presenting the company as fundamentally weak.

The exact policy for minimum overall coverage must remain consistent with the 60% axis-coverage rule and must not silently convert missing data into negative performance.

---

# 18. Fundamental Score Formula

For a fully available company:

```text
Fundamental Score =
0.30 × Growth Score
+ 0.45 × Profitability Score
+ 0.25 × Risk & Quality Score
```

The final score is always conceptually between:

**0 and 100**

Example:

```text
Growth = 78
Profitability = 84
Risk & Quality = 65
```

Then:

```text
Fundamental Score
= 0.30 × 78
+ 0.45 × 84
+ 0.25 × 65

= 77.45
```

Dashboard display:

```text
Fundamental Score = 77
```

Do not expose excessive decimal precision in the main dashboard.

---

# 19. Fundamental Score Categories

For presentation only:

|  Score | Category    |
| -----: | ----------- |
|   0–19 | Very Weak   |
|  20–39 | Weak        |
|  40–59 | Neutral     |
|  60–79 | Strong      |
| 80–100 | Very Strong |

The numeric score remains the primary value.

The categories are presentation labels and must not affect calculations.

---

# 20. Separation from Other Stages

Stage 3 must remain strictly independent from:

### Stage 4

Historical / Seasonal / Trend Engine

### Stage 5

Forecast Engine

### Stage 6

Forecast Evaluation & Calibration

### Stage 7

Valuation Engine

### Stage 8

Market Engine

Therefore:

```text
Fundamental Score
≠
Trend Score
≠
Forecast Score
≠
Valuation Score
≠
Market Score
```

Stage 4 may later provide context about whether fundamentals are improving or deteriorating, but that information must not retroactively change the Stage 3 Fundamental Score.

---

# 21. Output Contract

Stage 3 must provide at minimum:

```text
company_id

fundamental_score

growth_score
profitability_score
risk_quality_score

growth_coverage
profitability_coverage
risk_quality_coverage

score_data_quality

score_timestamp

scoring_method_version
```

For diagnostic purposes, preserve the component KPI scores and weights used in the calculation.

The system must be able to explain:

```text
Why did this company receive this score?
```

Therefore every score must be traceable to:

* KPI
* Raw/normalized value
* Benchmark
* KPI direction
* KPI Score
* Weight
* Axis
* Data quality
* Industry profile, if applicable

---

# 22. Non-Negotiable Rules

1. Fundamental Score = 0–100.
2. Growth = 30%.
3. Profitability = 45%.
4. Risk & Quality = 25%.
5. No fourth scoring axis.
6. No valuation input.
7. No market input.
8. No forecast input.
9. Missing ≠ 0.
10. Minimum Axis Coverage = 60%.
11. Minimum Peer Count = 8.
12. Industry-relative percentile is the primary benchmark.
13. Historical company benchmark is the fallback.
14. Historical comparison is not an additional score vote.
15. Industry KPI is not an additive bonus.
16. Industry KPI must remain inside the existing three axes.
17. Material KPI overlap must trigger weight redistribution/reduction.
18. Financial Cost Pressure has no independent base weight.
19. No excessive decimal precision in dashboard output.
20. All calculations must remain auditable and reproducible.
21. Fundamental Score must remain independent from Stage 4 onward.
22. Point-in-Time rules from Stage 1 must be respected.
23. Report versions and availability dates must be respected.
24. Restated/future information must not leak into historical scoring or backtests.

---

# 23. Final Stage 3 Architecture

```text
                STAGE 2 KPI DATA
                       │
                       ▼
                KPI Normalization
                       │
                       ▼
               KPI Benchmarking
                       │
            ┌──────────┴──────────┐
            │                     │
       Industry Relative     Historical Fallback
            │                     │
            └──────────┬──────────┘
                       ▼
                 KPI Score 0–100
                       │
                       ▼
              Double Count Control
                       │
                       ▼
               Coverage Validation
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
       Growth     Profitability   Risk & Quality
        30%           45%             25%
          │            │               │
          └────────────┼───────────────┘
                       ▼
              FUNDAMENTAL SCORE
                    0–100
```

## Stage 3 Status

**DESIGNED → AUDITED → TESTED → PASS → LOCKED**

Do not redesign Stage 3 unless a later stage exposes a genuine architectural contradiction. Minor implementation details may be refined without changing the locked architecture.
