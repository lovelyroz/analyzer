# Stage 1 — Data Foundation & Data Model

## Locked Specification

### 1. Objective

Design and implement the **Data Foundation Layer** for the financial analysis and investment decision-support system.

Stage 1 is responsible for:

* Ingesting raw data
* Preserving source data
* Structuring financial periods
* Versioning financial reports
* Normalizing financial facts
* Managing FX data and conversion rules
* Storing daily market data
* Managing historical share counts
* Managing corporate actions
* Tracking data quality
* Preserving provenance
* Preventing Point-in-Time and Look-Ahead Bias
* Supporting historical backtesting

Stage 1 must provide a reliable foundation for all later stages.

It must **not prematurely implement**:

* KPI scoring
* Fundamental scoring
* Forecasting
* Forecast evaluation
* Valuation
* Technical analysis
* Decision rules
* Dashboard logic

Those belong to later stages.

---

# 2. Core Architecture

The data architecture is:

```text id="h8q3zn"
                         DATA SOURCES
             ┌──────────────┼──────────────┐
             │              │              │
           CODAL           OHLC            FX
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                  DATA FOUNDATION
                  / NORMALIZATION
                            │
                            ▼
                     LATER STAGES
```

The three primary external data sources are:

1. Codal / Financial Reports
2. Daily Market OHLC
3. FX / Currency Data

FX is part of the Data Foundation.

It is NOT a separate analytical engine.

OHLC is stored here and analyzed later by Stage 8.

---

# 3. Design Principles

The following principles are mandatory.

### 3.1 Raw Data Is Immutable

Raw source data must never be overwritten by normalization.

The system must preserve the original source representation.

```text id="u4j2m1"
RAW
 ↓
NORMALIZATION
 ↓
ANALYSIS
```

Never:

```text id="wz0a7f"
RAW
 ↓
overwrite
NORMALIZED
```

---

### 3.2 Provenance Must Be Traceable

Every normalized financial fact must be traceable back to:

* Company
* Report
* Report Version
* Financial Period
* Original item
* Source section
* Source row/column
* Normalization rule

The system must be able to answer:

> Where did this number come from?

---

### 3.3 Missing ≠ Zero

A missing value must remain missing.

```text id="j4c3o2"
NULL ≠ 0
```

Do not convert unavailable information into zero.

---

### 3.4 Point-in-Time Is Mandatory

Every report must be associated with the information availability timeline.

The system must distinguish:

* Financial Period
* Report
* Report Version
* Publication / Availability Date

Historical backtests must use only information that was actually available at the historical decision date.

Future information must never leak into historical analysis.

---

### 3.5 Restatements Must Be Preserved

Corrected or restated reports must never overwrite the original historical version.

Both versions must remain available.

Current analysis may use the latest valid version.

Historical backtesting must use the version that was actually available at that historical point in time.

---

### 3.6 IRR Is the Base Financial Currency

Financial statement values are fundamentally stored in IRR.

USD values are derived.

Do not replace the original IRR financial fact with a USD value.

---

# 4. Company Entity

Table / Entity:

`Company`

Required fields:

```text id="g5v9h4"
company_id
ticker
company_name
industry_id
codal_symbol
fiscal_year_end
status
```

### Important Rule

`company_id` must NOT be based only on ticker.

Ticker symbols may change.

The company identity must remain stable across ticker changes.

---

# 5. Industry Entity

Table:

`Industry`

Fields:

```text id="7kgw8j"
industry_id
industry_code
industry_name
parent_industry_id
```

This allows:

* Industry classification
* Peer comparison
* Parent/child industry hierarchy

Industry KPI definitions belong to Stage 2, not Stage 1.

---

# 6. Financial Period

Table:

`FinancialPeriod`

Fields:

```text id="c9u0y1"
period_id
company_id
period_type
start_date
end_date
fiscal_year
fiscal_quarter
months_length
is_ytd
```

Supported period types:

* MONTH
* QUARTER
* SEMI_ANNUAL
* NINE_MONTH
* ANNUAL
* TTM

### TTM Rule

TTM is a **derived period**.

It is not treated as an original/raw reporting period.

---

# 7. Report

Table:

`Report`

Fields:

```text id="s2q8kk"
report_id
company_id
report_type
codal_tracking_id
title
financial_period_id
source_url
original_report_id
is_correction
created_at
```

`Report` identifies the report itself.

It must be kept separate from `ReportVersion`.

---

# 8. Report Version

Table:

`ReportVersion`

Fields:

```text id="5i3t9m"
report_version_id
report_id
version_number
publication_datetime
is_current_version
is_restated
supersedes_version_id
```

### Critical Rule

Publication date belongs to **ReportVersion**, not Report.

This is required because a report may have:

* Original publication
* Correction
* Restatement
* Additional version

Each version can have a different publication time.

---

# 9. Report vs ReportVersion

The architecture must distinguish:

```text id="a7p3ds"
Report
  │
  ├── Version 1
  │     └── Publication Date A
  │
  ├── Version 2
  │     └── Publication Date B
  │
  └── Version 3
        └── Publication Date C
```

Current analysis:

```text
Latest Valid Version
```

Historical backtest:

```text
Version available at historical decision date
```

Never use a later restatement in a historical backtest if it was not yet available at that time.

---

# 10. Raw Financial Fact

Table:

`RawFinancialFact`

Fields:

```text id="m1l4zf"
raw_fact_id
company_id
report_version_id
period_id
raw_item_name
raw_item_code
value
unit
currency
source_section
source_row
source_column
```

The raw layer uses a **fact-based long-format structure**.

Do NOT create a giant wide financial table with hundreds of columns.

The raw layer should preserve the source structure while allowing flexible mappings.

---

# 11. Financial Metric

Table:

`FinancialMetric`

Fields:

```text id="u7r4np"
metric_id
metric_code
metric_name
category
industry_id
value_type
flow_or_stock
```

Purpose:

Map different Codal labels and source representations into standardized financial concepts.

Examples conceptually:

```text
Different Codal labels
        ↓
Standard Financial Metric
```

Stage 1 defines the mapping infrastructure.

Stage 2 defines the analytical KPI inventory.

Do not prematurely embed Stage 2 scoring logic into this table.

---

# 12. Normalized Financial Fact

Table:

`NormalizedFinancialFact`

Fields:

```text id="r8e5qa"
fact_id
company_id
period_id
metric_id
value_irr
source_report_version_id
normalization_rule_id
quality_status
```

The normalized layer provides standardized values suitable for later analysis.

Raw and normalized facts must remain separate.

---

# 13. Raw vs Normalized Architecture

The required structure is:

```text id="6w0v5c"
Codal
  ↓
RawFinancialFact
  ↓
Normalization Rules
  ↓
NormalizedFinancialFact
  ↓
Stage 2+
```

If a normalization rule changes later, the raw source data must still be available so the normalized layer can be recalculated.

Never make the normalized layer the only source of truth.

---

# 14. Flow vs Stock Classification

Financial metrics must distinguish:

### Flow

Examples:

* Revenue
* Profit
* Cash Flow

### Stock

Examples:

* Assets
* Liabilities
* Equity
* Loan Balance
* Deposit Balance

This distinction is required for correct FX conversion and period analysis.

---

# 15. FX Rate

Table:

`FXRate`

Fields:

```text id="z1o9wp"
fx_rate_id
date
currency_from
currency_to
rate
rate_type
source
```

FX data is stored independently from financial facts.

Do not permanently replace IRR financial facts with converted USD values.

---

# 16. FX Conversion Rule

Table:

`FXConversionRule`

Fields:

```text id="b6j7ux"
rule_id
metric_type
conversion_method
```

Default rules:

### Flow

Use:

**Period Average FX**

### Stock

Use:

**Period-End FX**

### Market Value

Use:

**Same-Date FX**

Conceptually:

```text id="k1j0aa"
FLOW
→ Period Average FX

STOCK
→ Period-End FX

MARKET VALUE
→ Same-Date FX
```

Overrides are permitted when economically justified.

The conversion method must be traceable.

---

# 17. IRR and USD

The system must preserve both concepts:

### Primary

IRR financial fact

### Derived

USD equivalent

This allows the system to calculate both:

* Nominal growth
* USD-adjusted growth

without destroying the original financial information.

---

# 18. Market Daily Data

Table:

`MarketDaily`

Fields:

```text id="t2f8xz"
company_id
date
open
high
low
close
adjusted_close
volume
value
trade_count
source
```

Both:

* Close
* Adjusted Close

must remain distinct.

Do not overwrite one with the other.

Market data is stored in Stage 1.

Market analysis belongs to Stage 8.

---

# 19. Share Count History

Table:

`ShareCountHistory`

Fields:

```text id="e6j2kc"
company_id
effective_date
shares_outstanding
capital
source
```

Historical share count is mandatory for reliable per-share calculations.

It must support changes over time.

---

# 20. Corporate Actions

Table:

`CorporateAction`

Fields:

```text id="p9r3aw"
action_id
company_id
action_type
announcement_date
effective_date
old_share_count
new_share_count
ratio
source
```

Corporate actions must be stored historically.

They are important for:

* EPS comparability
* Share-count history
* Market-price adjustment
* Historical valuation
* Backtesting

Do not treat corporate actions as disposable metadata.

---

# 21. EPS Integrity

EPS-related analysis must be able to account for:

* Share-count changes
* Capital increases
* Corporate actions

Therefore Stage 1 must preserve enough historical information to reconstruct the correct share denominator for each relevant period.

EPS itself may be supplied by Codal, but the system must retain the underlying share history required for validation and comparison.

---

# 22. Data Quality Status

The system uses these standard statuses:

```text id="d3f4nn"
VALID
MISSING
ESTIMATED
RESTATED
SUSPICIOUS
UNMAPPED
```

Meaning must remain explicit.

Examples:

### VALID

Data has passed required validation.

### MISSING

Expected data is unavailable.

### ESTIMATED

Data is estimated rather than directly reported.

### RESTATED

Data comes from a restated/corrected version.

### SUSPICIOUS

Data exists but fails validation or appears abnormal.

### UNMAPPED

Raw data exists but has not yet been mapped reliably to a standardized metric.

---

# 23. Data Quality Propagation

Suspicious or unmapped data must not silently flow into later analytical engines as valid information.

Later stages must be able to distinguish:

```text
Valid
vs
Estimated
vs
Suspicious
vs
Missing
vs
Unmapped
```

The exact scoring treatment belongs to later stages.

Stage 1 only establishes the quality state.

---

# 24. Ingestion Run

Table:

`IngestionRun`

Fields:

```text id="s0g5cf"
ingestion_id
source
started_at
finished_at
status
records_found
records_inserted
records_updated
records_failed
```

Purpose:

Track each data-ingestion process.

This allows the system to identify:

* What source was processed
* When it was processed
* Whether ingestion succeeded
* How many records were affected
* Whether failures occurred

---

# 25. Data Lineage

Every important normalized financial fact must be traceable through:

```text id="k5r2dj"
Company
   ↓
Financial Period
   ↓
Report
   ↓
Report Version
   ↓
Raw Financial Fact
   ↓
Normalization Rule
   ↓
Normalized Financial Fact
```

This is mandatory for auditability.

---

# 26. Point-in-Time / Look-Ahead Bias

The system must support historical reconstruction.

Suppose:

```text id="2t5m0h"
Financial Period:
September

Publication:
October 15
```

A backtest occurring on October 10 must NOT have access to that September report.

A backtest occurring after October 15 may use it.

If a corrected report is published later, the historical backtest must continue using the version that was actually available at that historical date.

---

# 27. Restatement Handling

Example:

```text id="v3g6be"
Report
 ├── Version 1
 │     published January 10
 │
 └── Version 2
       published February 20
```

Analysis on January 20:

→ Version 1

Analysis on March 1:

→ Latest Valid Version

Historical backtest on January 20:

→ Version 1

Never rewrite the January historical state using Version 2.

---

# 28. Data Storage Philosophy

The architecture uses two different philosophies for different layers.

### Raw Layer

Comprehensive and source-faithful.

### Analytical / Decision Layer

Compact and standardized.

Therefore:

```text id="2lckh5"
Raw Data
= Comprehensive

Decision Data
= Minimal
```

Do not sacrifice raw information merely to keep the analytical dataset small.

Instead, keep raw data comprehensive and keep downstream analytical representations compact.

---

# 29. Industry Flexibility

Stage 1 must support industry-specific metrics without requiring a new database architecture for every industry.

The `FinancialMetric` structure must allow industry association.

However:

* Stage 1 does not define industry KPI lists.
* Stage 2 defines the KPI inventory.
* Stage 3 defines scoring.

This prevents later stages from being prematurely embedded in the data foundation.

---

# 30. No Premature Analytics

Stage 1 must NOT contain:

* Fundamental Score
* Growth Score
* Profitability Score
* Risk Score
* Forecast Score
* Valuation Score
* Market Score
* Decision Score
* Trading Signal

Stage 1 provides data infrastructure only.

---

# 31. TTM Rule

TTM is derived from underlying financial periods.

Do not treat TTM as a separate raw Codal reporting period.

The system must retain the underlying periods needed to reconstruct TTM.

TTM calculations must also respect Point-in-Time availability.

---

# 32. Data Integrity Rules

The implementation must enforce:

1. `NULL != 0`
2. Raw data is never silently overwritten.
3. Report versions are preserved.
4. Publication datetime belongs to ReportVersion.
5. Historical share counts are preserved.
6. Corporate actions are preserved.
7. FX conversion method is traceable.
8. Normalized facts remain traceable to source.
9. Suspicious data is not silently considered valid.
10. TTM is derived.
11. Close and Adjusted Close remain separate.
12. Company identity is not based only on ticker.

---

# 33. Minimum Data Foundation

At minimum, the system must be able to answer:

### Company

Who is the company?

### Industry

Which peer group does it belong to?

### Period

What financial period does the number represent?

### Report

Which report supplied the information?

### Version

Which version of that report was available?

### Source

Where exactly did the number come from?

### Metric

What standardized financial concept does it represent?

### Currency

Is the original financial value in IRR?

### FX

Which FX rule was used for any derived USD value?

### Shares

How many shares were outstanding at the relevant date?

### Corporate Action

Did a capital/share event affect comparability?

### Quality

Can this data be trusted?

---

# 34. Final Stage 1 Entity Map

```text id="g4j1mb"
Company
   │
   ├── Industry
   │
   ├── FinancialPeriod
   │
   ├── Report
   │      │
   │      └── ReportVersion
   │               │
   │               └── RawFinancialFact
   │
   ├── NormalizedFinancialFact
   │
   ├── ShareCountHistory
   │
   ├── CorporateAction
   │
   └── MarketDaily

FXRate
   │
   └── FXConversionRule

FinancialMetric

IngestionRun
```

---

# 35. Stage 1 → Stage 2 Interface

Stage 1 provides Stage 2 with:

```text id="gq0x9s"
Reliable Financial Facts
        +
Periods
        +
Industry
        +
Data Quality
        +
Point-in-Time State
        +
Provenance
```

Stage 2 then determines:

```text
Which facts become KPIs?
```

Stage 1 must not answer that question prematurely.

---

# 36. Stage 1 → Later Stages

The architecture is:

```text id="t6m0ad"
Stage 1
Data Foundation
      │
      ├──────────────→ Stage 2 KPI Specification
      │
      ├──────────────→ Stage 8 Market Engine
      │
      └──────────────→ FX / Share / Corporate Action
                              │
                              ▼
                         Later Stages
```

The same data foundation must support:

* Fundamental analysis
* Historical analysis
* Forecasting
* Valuation
* Market analysis
* Decision engine
* Historical backtesting

without duplicating the underlying source data.

---

# 37. Stage 1 Validation Checklist

Before considering Stage 1 valid, verify:

* [ ] Company identity is stable and not ticker-only.
* [ ] Industry entity exists.
* [ ] Financial periods are explicit.
* [ ] TTM is derived rather than raw.
* [ ] Report and ReportVersion are separate.
* [ ] Publication datetime belongs to ReportVersion.
* [ ] Restatements are preserved.
* [ ] Raw financial facts are preserved.
* [ ] Normalized facts are separate from raw facts.
* [ ] Normalized facts retain provenance.
* [ ] Financial metrics support standardized mapping.
* [ ] Flow vs Stock is represented.
* [ ] IRR is the base financial representation.
* [ ] USD is derived rather than replacing IRR.
* [ ] FX rates are stored separately.
* [ ] FX conversion rules are explicit.
* [ ] Flow uses period-average FX by default.
* [ ] Stock uses period-end FX by default.
* [ ] Market value uses same-date FX.
* [ ] OHLC data is stored.
* [ ] Close and Adjusted Close are separate.
* [ ] Share count history is stored.
* [ ] Corporate actions are stored.
* [ ] Missing values are not converted to zero.
* [ ] Data quality states exist.
* [ ] Suspicious/unmapped data can be identified.
* [ ] Ingestion runs are tracked.
* [ ] Point-in-Time availability is preserved.
* [ ] Historical backtests can reconstruct available information.
* [ ] Look-Ahead Bias is prevented.
* [ ] No later-stage scoring logic has leaked into Stage 1.
* [ ] Raw layer remains comprehensive.
* [ ] Downstream analytical layer can remain compact.

---

# 38. Final Stage 1 Architecture

```text id="z3p8a4"
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
     FINANCIAL DATA                    MARKET DATA
            │                               │
     ┌──────┼──────┐                        │
     ▼      ▼      ▼                        ▼
   Raw   Reports  FX                     OHLC
   Facts Versions Rules
     │
     ▼
 Normalized
   Facts
     │
     └──────────────────────┐
                            ▼
                     LATER STAGES
```

---

# 39. Non-Negotiable Rules

1. Raw data must never be overwritten by normalization.
2. Report and ReportVersion must remain separate.
3. Publication datetime belongs to ReportVersion.
4. Restated reports must be versioned.
5. Historical backtests must use point-in-time available information.
6. Look-Ahead Bias is prohibited.
7. IRR remains the primary financial representation.
8. USD is derived.
9. FX methodology must be explicit and traceable.
10. Flow → period-average FX by default.
11. Stock → period-end FX by default.
12. Market Value → same-date FX.
13. Market data is stored in Stage 1 but analyzed in Stage 8.
14. Share count history must be preserved.
15. Corporate actions must be preserved.
16. EPS-related analysis must be capable of accounting for share changes.
17. `NULL != 0`.
18. Raw facts must retain source provenance.
19. Suspicious/unmapped information must not silently become valid.
20. TTM is derived.
21. Raw layer may be comprehensive.
22. Decision/analytical layers must remain compact.
23. Stage 1 must remain independent from KPI scoring.
24. Stage 1 must remain independent from Forecast, Valuation, Market scoring and Decision logic.
25. Industry-specific data must be supportable without redesigning the database architecture.

---

# 40. Stage 1 Status

**DESIGNED → REVIEWED → CORRECTED → AUDITED → LOCKED**

Stage 1 is considered complete.

Do not redesign Stage 1 during later stages unless a genuine architectural contradiction is discovered.

Minor implementation details may be refined later without changing the locked architecture.
