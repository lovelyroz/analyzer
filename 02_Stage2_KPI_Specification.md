# Stage 2 — KPI Specification

## Locked Specification

### 1. Objective

Design the complete KPI Specification Layer for the financial analysis system.

Stage 2 defines:

* What financial KPIs are measured
* Which KPIs are Universal
* Which KPIs are Industry-Specific
* Which KPIs are Conditional
* Which metrics are merely Base Metrics
* How periods such as MoM, QoQ, YoY, TTM and multi-year comparisons are treated
* What is Core and what is intentionally excluded from the V1 analytical model

Stage 2 must define **what is measured**, not how the final company score is calculated.

Scoring, weighting and aggregation belong to Stage 3.

---

# 2. Core Design Principle

## Financial Statements First

The V1 KPI system must primarily use information available from official financial statements and official company financial reporting.

Do NOT make external market, commodity, macroeconomic or operational datasets mandatory for the Core KPI system.

Examples of data that must NOT become mandatory Core KPIs in V1:

* Global commodity prices
* Export prices
* Feedstock prices
* Global benchmark prices
* External industry prices
* External macroeconomic variables
* Other external datasets that may not consistently exist for all companies

External or operational information may be considered later as:

* Diagnostic information
* Forecast Drivers
* Supplementary research data

But it must not be a mandatory requirement for V1 fundamental analysis.

---

# 3. KPI Categories

Stage 2 uses four conceptual categories:

### A. Universal Core KPIs

KPIs applicable across most companies and industries.

### B. Industry Core KPIs

Minimal industry-specific KPIs that provide information not adequately captured by Universal Core KPIs.

### C. Conditional KPI

A KPI that is economically useful only for companies where it is meaningful and sufficiently available.

### D. Base Metrics

Important financial values used as foundations for calculations and later stages, but not themselves treated as independent analytical KPIs.

---

# 4. Universal Core KPIs

The Universal Core consists of three analytical groups.

---

## 4.1 Growth

Exactly four Universal Growth KPIs:

1. Revenue Growth
2. Operating Profit Growth
3. Net Profit Growth
4. EPS Growth

These form a **Profitability Cascade**:

```text
Revenue
   ↓
Operating Profit
   ↓
Net Profit
   ↓
EPS
```

These four KPIs are analytically related.

Stage 2 defines them as separate measurable KPIs, but Stage 3 must prevent them from being treated as four completely independent economic votes.

---

## 4.2 Profitability

Exactly five Universal Profitability KPIs:

5. Gross Margin
6. Operating Margin
7. Net Profit Margin
8. ROA
9. ROE

These measure different aspects of profitability and capital efficiency.

They must remain separate in Stage 2.

Stage 3 determines their weighting and controls potential overlap.

---

## 4.3 Risk & Quality

Exactly two Universal Risk & Quality KPIs:

10. Cash Earnings Conversion
11. Earnings Quality

### Cash Earnings Conversion

Conceptually:

```text
OCF / Net Profit
```

where OCF is Operating Cash Flow.

### Earnings Quality

Earnings Quality is a **composite analytical framework**, not a simple single ratio.

It should consider factors such as:

* Cash conversion
* Recurring vs non-recurring earnings
* Operating vs non-operating profit
* One-off items
* Abnormal changes in earnings components

Do not reduce Earnings Quality to a single simplistic ratio.

---

# 5. Conditional KPI

## Financial Cost Pressure

Financial Cost Pressure is a conditional KPI.

Conceptually:

```text
Financial Costs / Operating Profit
```

Use it only where:

* Financial costs are economically meaningful
* Operating Profit is an appropriate denominator
* Data is sufficiently available and reliable

It is NOT a mandatory Universal KPI for every company.

It is also not a mandatory independent component of the base Fundamental Score.

Its eventual use as a Diagnostic or Adjustment belongs to Stage 3 or later and must not be assumed here.

---

# 6. Base Metrics

The following are foundational financial metrics:

* Revenue
* Operating Profit
* Net Profit
* EPS
* TTM Revenue
* TTM Net Profit

These are **not additional analytical KPIs**.

They are base financial measures used to calculate, compare and support the analytical KPIs and later stages.

Do not count them as additional KPI votes.

---

# 7. Period Dimensions

The following are comparison dimensions, not separate KPIs:

* MoM
* QoQ
* YoY
* Multi-Year
* Same-Period Multi-Year
* Rolling / TTM
* Seasonal Comparison

Do not create separate KPI definitions such as:

* Revenue Growth MoM
* Revenue Growth QoQ
* Revenue Growth YoY

as separate KPIs.

Instead:

```text
KPI
+
Period Dimension
```

For example:

```text
Revenue Growth
    ├── MoM
    ├── QoQ
    ├── YoY
    └── Multi-Year
```

Stage 4 will later use these dimensions for Historical, Seasonal and Trend analysis.

---

# 8. TTM

TTM is a derived analytical period.

It is not a raw financial reporting period.

TTM may be calculated for relevant metrics such as:

* Revenue
* Net Profit
* Other appropriate flow metrics

Do not treat TTM as an additional KPI.

TTM is a **period construction method**.

---

# 9. EPS Growth

EPS Growth must be calculated with awareness of:

* Share count changes
* Capital increases
* Corporate actions
* Other events affecting per-share comparability

EPS Growth must not blindly compare EPS values when share-count changes make the comparison economically misleading.

The underlying share history and corporate actions are supplied by Stage 1.

---

# 10. Industry Scope — V1

Stage 2 V1 supports exactly these seven industry groups:

1. Bank
2. Investment / Holding
3. Petrochemical / Chemical
4. Metals / Mining
5. Cement
6. Food
7. Pharmaceutical

Do not add new industry packs in V1.

Deferred industries include:

* Insurance
* General Manufacturing
* Automotive / Parts
* Construction
* Transportation
* Power / Energy
* Agriculture
* Specialized Services
* Other sectors

They may be added in a later version after validation.

---

# 11. Industry Core KPI Philosophy

Industry KPIs must be minimal.

An industry KPI is included only when:

1. It provides information not already adequately captured by Universal Core KPIs.
2. It is economically meaningful for that industry.
3. It can be obtained reliably enough for V1.
4. It does not require mandatory external data.

Do NOT add a KPI merely because it is interesting or commonly discussed by analysts.

The objective is:

**Minimum sufficient KPI set**

not:

**Maximum available data set**

---

# 12. Industry Core KPIs — Final V1

The total Industry Core consists of **11 KPIs**.

---

## 12.1 Bank — 5 KPIs

1. NII — Net Interest Income
2. NIM — Net Interest Margin
3. Loan Growth
4. Deposit Growth
5. NPL / Credit Quality

Mapping conceptually:

```text
Growth:
- Loan Growth
- Deposit Growth

Profitability:
- NII
- NIM

Risk & Quality:
- NPL / Credit Quality
```

These are additional analytical dimensions specific to banking economics.

Stage 3 must control overlap with Universal KPIs.

---

## 12.2 Investment / Holding — 3 KPIs

1. NAV
2. NAV Growth
3. P/NAV

These capture valuation and asset-base characteristics particularly relevant to holding companies.

Important:

Stage 2 defines P/NAV as an Industry Core KPI because it is analytically relevant to this industry.

The actual valuation architecture and integration of P/NAV into the broader investment decision system belong to Stage 7.

Stage 3 must not allow P/NAV to contaminate the general Fundamental Score without explicit Stage 3 rules.

---

## 12.3 Petrochemical / Chemical — 0 Core KPIs

No mandatory industry-specific Core KPI in V1.

Potential information such as:

* Production
* Sales volume
* Selling price
* Feedstock cost
* Export share
* Global commodity prices

is not Core in V1.

If available, such information may later be used as:

* Diagnostic
* Forecast Driver

---

## 12.4 Metals / Mining — 0 Core KPIs

No mandatory industry-specific Core KPI in V1.

Production, commodity prices, export information and similar data are not mandatory Core KPIs.

They may be used later as Diagnostic or Forecast Driver information.

---

## 12.5 Cement — 1 KPI

1. Sales Volume

Sales Volume is Core only when official company data is available.

If it is missing:

**The company remains analyzable.**

Missing Sales Volume must not be interpreted as zero.

---

## 12.6 Food — 1 KPI

1. Sales Volume

Same rule:

* Use when official company data exists.
* If unavailable, do not assign zero.
* The company remains analyzable.

---

## 12.7 Pharmaceutical — 1 KPI

1. Sales Volume

Same rule:

* Optional when official company data exists.
* Missing does not mean zero.
* Company remains analyzable.

---

# 13. Industry Core Summary

| Industry                 | Core KPIs |
| ------------------------ | --------: |
| Bank                     |         5 |
| Investment / Holding     |         3 |
| Petrochemical / Chemical |         0 |
| Metals / Mining          |         0 |
| Cement                   |         1 |
| Food                     |         1 |
| Pharmaceutical           |         1 |
| **Total**                |    **11** |

---

# 14. Explicitly Excluded from Industry Core V1

The following are NOT mandatory Core KPIs in V1:

* Production Volume
* Selling Price
* Feedstock Cost
* Export Share
* Global Commodity Price
* Global Benchmark Price
* Export Rate
* Other external market variables

Reason:

Their availability and comparability across companies are not sufficiently reliable for the mandatory V1 KPI layer.

If reliable data becomes available later, it may be incorporated into:

* Diagnostic Analysis
* Forecast Drivers
* Supplementary Research

without automatically becoming a Fundamental Core KPI.

---

# 15. Industry KPI and Universal KPI Relationship

Industry KPIs must not automatically become additional scoring votes.

Examples of potential overlap:

```text
Loan Growth
    ↓
NII
    ↓
Operating Profit
    ↓
Net Profit
    ↓
EPS
```

Therefore Stage 3 must control double counting.

Stage 2 only defines the KPI inventory.

It does not determine final weights.

Rule:

> Industry KPIs must add information rather than simply duplicate Universal KPI information.

---

# 16. Companies Are Primarily Compared Within Their Industry

The system should primarily compare companies against peers within the same industry.

For example:

* Bank vs Bank
* Cement vs Cement
* Pharmaceutical vs Pharmaceutical

Cross-industry comparison may exist for broader analysis later, but Stage 2 does not attempt to force all companies into identical economic KPI structures.

---

# 17. Industry KPI Mapping to Universal Analytical Axes

Industry KPIs must eventually map into the same three broad analytical concepts:

```text
Growth
Profitability
Risk & Quality
```

Examples:

### Bank

```text
Loan Growth / Deposit Growth
→ Growth

NII / NIM
→ Profitability

NPL
→ Risk & Quality
```

### Holding

```text
NAV Growth
→ Growth / asset-base development

NAV / P-NAV
→ Holding-specific profitability/value context
```

The exact scoring weights are a Stage 3 responsibility.

Stage 2 must not define the Fundamental Score.

---

# 18. Diagnostic vs Core vs Forecast Driver

The system must distinguish:

### Core KPI

Directly part of the V1 KPI specification.

### Diagnostic

Useful for explaining why a KPI changed but not automatically part of the Fundamental Score.

### Forecast Driver

Potential input into the Forecast Engine.

A data point must not become a Core KPI simply because it is useful for diagnosis or forecasting.

This separation is mandatory to prevent KPI explosion.

---

# 19. Missing Data Principle

The following rule is mandatory across Stage 2:

**Missing ≠ Zero**

Examples:

```text
Sales Volume unavailable
≠
Sales Volume = 0
```

and:

```text
Industry KPI unavailable
≠
Poor company performance
```

The handling of missing KPI values belongs to Stage 3, but Stage 2 must preserve this distinction.

---

# 20. Data Quality Dependency

Stage 2 uses the data-quality architecture established in Stage 1.

KPIs must respect statuses such as:

* VALID
* MISSING
* ESTIMATED
* RESTATED
* SUSPICIOUS
* UNMAPPED

A KPI based on suspicious or unmapped data must not silently be treated as valid.

The exact treatment in scoring belongs to Stage 3.

---

# 21. Point-in-Time Requirement

All Stage 2 KPI definitions must remain compatible with the Stage 1 Point-in-Time architecture.

Relevant concepts include:

* Financial Period
* Publication / Availability Date
* Report Version

Historical analysis and backtesting must use only information that was actually available at the relevant historical date.

Restated information must not leak into historical calculations when it was not available at that time.

---

# 22. Currency and FX

Stage 2 does not create a separate FX KPI category.

The Stage 1 rule remains:

* Financial statements are fundamentally stored in IRR.
* USD figures are derived.
* Flow metrics use appropriate period-average FX.
* Stock metrics use period-end FX.
* Market value uses same-date FX.

Both nominal and USD-adjusted growth may be derived when relevant.

FX is a data transformation/input mechanism, not a new KPI group in Stage 2.

---

# 23. What Stage 2 Must NOT Do

Stage 2 must NOT:

* Create a Fundamental Score
* Assign KPI weights for the final score
* Perform valuation
* Calculate P/E as a Stage 2 scoring KPI
* Perform technical analysis
* Forecast earnings
* Evaluate forecast accuracy
* Build a trading signal
* Add mandatory external commodity datasets
* Create large industry-specific KPI catalogs
* Add KPIs merely because data is available
* Treat every period comparison as a new KPI

These belong to later stages.

---

# 24. Final KPI Inventory

## Universal Core — 11 KPIs

### Growth — 4

1. Revenue Growth
2. Operating Profit Growth
3. Net Profit Growth
4. EPS Growth

### Profitability — 5

5. Gross Margin
6. Operating Margin
7. Net Profit Margin
8. ROA
9. ROE

### Risk & Quality — 2

10. Cash Earnings Conversion
11. Earnings Quality

---

## Conditional — 1 KPI

12. Financial Cost Pressure

---

## Industry Core — 11 KPIs

### Bank — 5

13. NII
14. NIM
15. Loan Growth
16. Deposit Growth
17. NPL / Credit Quality

### Investment / Holding — 3

18. NAV
19. NAV Growth
20. P/NAV

### Cement — 1

21. Sales Volume

### Food — 1

22. Sales Volume

### Pharmaceutical — 1

23. Sales Volume

Petrochemical / Chemical: 0

Metals / Mining: 0

---

# 25. Base Metrics — Not Additional KPIs

The following remain available as foundational data:

* Revenue
* Operating Profit
* Net Profit
* EPS
* TTM Revenue
* TTM Net Profit

They must not be counted again as analytical KPIs.

---

# 26. Period Dimensions — Not Additional KPIs

The following remain dimensions of analysis:

* MoM
* QoQ
* YoY
* Multi-Year
* Same-Period Multi-Year
* Rolling / TTM
* Seasonal Comparison

They must not expand the KPI count.

---

# 27. Final Stage 2 Design Principle

The Stage 2 KPI system must follow:

```text
                    FINANCIAL STATEMENTS
                            │
                            ▼
                    UNIVERSAL CORE
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
         Growth       Profitability    Risk & Quality
           4                5                2
            │               │               │
            └───────────────┼───────────────┘
                            │
                    CONDITIONAL KPI
                  Financial Cost Pressure
                            │
                            ▼
                   INDUSTRY CORE
                       11 KPIs
                            │
                            ▼
               Minimal Analytical Dataset
```

The objective is not to capture every available financial data point.

The objective is to capture the **minimum sufficient set of KPIs required for reliable fundamental analysis**.

---

# 28. Stage 2 Validation Checklist

Before considering Stage 2 valid, verify all of the following:

* [ ] Universal Core contains exactly 11 KPIs.
* [ ] Growth contains exactly 4 KPIs.
* [ ] Profitability contains exactly 5 KPIs.
* [ ] Risk & Quality contains exactly 2 KPIs.
* [ ] Financial Cost Pressure is Conditional.
* [ ] Financial Cost Pressure is not a mandatory Universal KPI.
* [ ] Industry V1 contains exactly 7 industry groups.
* [ ] Bank has exactly 5 Core KPIs.
* [ ] Investment / Holding has exactly 3 Core KPIs.
* [ ] Petrochemical / Chemical has 0 Core KPIs.
* [ ] Metals / Mining has 0 Core KPIs.
* [ ] Cement has 1 Core KPI.
* [ ] Food has 1 Core KPI.
* [ ] Pharmaceutical has 1 Core KPI.
* [ ] Total Industry Core = 11 KPIs.
* [ ] External commodity/macro data is not mandatory.
* [ ] Sales Volume is optional where official data is unavailable.
* [ ] Missing ≠ Zero.
* [ ] Base Metrics are not counted as analytical KPIs.
* [ ] MoM/QoQ/YoY/TTM are not separate KPIs.
* [ ] TTM is a derived period.
* [ ] EPS Growth respects share-count and corporate-action changes.
* [ ] Companies are primarily compared within their own industry.
* [ ] Industry KPIs do not automatically create additional scoring votes.
* [ ] Double Counting is explicitly delegated to Stage 3.
* [ ] Stage 2 does not define final KPI weights.
* [ ] Stage 2 does not define Fundamental Score.
* [ ] Stage 2 does not include valuation, technical analysis or forecasting.
* [ ] Stage 1 Point-in-Time and Data Quality rules remain applicable.
* [ ] FX remains a transformation/input mechanism, not a separate KPI category.

---

# 29. Stage 2 Status

**DESIGNED → AUDITED → CORRECTED → LOCKED**

Stage 2 is considered complete.

Do not redesign Stage 2 during later stages unless a genuine architectural contradiction is discovered.

Minor implementation details may be refined later without changing the locked KPI architecture.
