# DB-DES-011 — FinancialPeriod and Duration-Basis Temporal Contract

**Status:** ACCEPTED DESIGN DECISION — fact-level duration_basis is the canonical temporal ownership rule; implementation gates remain open; no ORM, migration, runtime code, data, or tests changed  
**Date:** 2026-11-18  
**Scope:** Jalali period identity, INSTANT/DURATION, fiscal-year boundaries, YTD versus standalone value basis, source interval classification, and Stage 5 comparability  
**Depends on:** Database Contract V1.3, DB-DES-003, DB-DES-006, DB-DES-009, DB-DES-010, DB-AUD-002, DB-AUD-013

## 1. Executive decisions proposed

This document makes the following design recommendations explicit:

1. **FinancialPeriod describes an actual time interval, not the way a value is accumulated.** Its identity is company + temporal kind + exact Jalali start and end dates.
2. **YTD versus standalone is a value-level temporal basis, not a global property of the period row.** It belongs to each duration FinancialFact (or an immutable temporal-interpretation record one-to-one with that fact). This resolves the open ambiguity in DB-DES-009.
3. **Fiscal-year boundaries are company-specific source facts.** Never assume Farvardin 1, Gregorian January 1, or a fixed 12-month calendar year.
4. **A report's publication date and report label do not define the financial period or value basis.** The source's explicit period dates and temporal meaning, or an approved company fiscal calendar, must establish them.
5. **Standalone values are source facts only when explicitly reported.** A standalone quarter computed by subtracting YTD values is runtime-derived and is not persisted as a source FinancialFact.
6. **TTM is never a FinancialPeriod source row.** It is a runtime analytical window over compatible source observations.
7. **Unknown or conflicting temporal interpretation rejects the whole ingestion unit.** No inferred period, default fiscal-year start, or guessed YTD status.

These are proposed design resolutions, not owner-approved implementation authorization.

## 2. Separate the three temporal concepts

The pipeline must not conflate:

### 2.1 Actual period interval — FinancialPeriod

The interval to which the reported value applies:
- an instant date for a stock/balance;
- a start date and end date for a flow/duration.

### 2.2 Fiscal classification — FinancialPeriod attributes

Labels that describe the company's fiscal calendar:
- fiscal year;
- fiscal quarter, when determinable;
- source interval class such as MONTH, QUARTER, SEMI_ANNUAL, NINE_MONTH, ANNUAL.

These labels do not replace the actual dates and do not establish whether the value is cumulative.

### 2.3 Value temporal basis — FinancialFact

How a DURATION value relates to the fiscal year:
- STANDALONE: value applies only to its stated actual interval;
- YTD: value is cumulative from the actual start of the company's fiscal year through the stated period end.

For INSTANT facts, duration basis is NOT_APPLICABLE. Do not store a fake FALSE/standalone value for an instant.

A possible physical representation is `duration_basis` on `financial_facts`, constrained to `STANDALONE`, `YTD`, or NULL (NULL only for INSTANT). If the same temporal semantics are bundled into a versioned interpretation object, the fact must still resolve to one unambiguous basis. Do not make it a single shared FinancialPeriod attribute.

## 3. FinancialPeriod logical identity and fields

### 3.1 Required logical fields

- `period_id`
- `company_id`
- `temporal_kind`: INSTANT or DURATION
- `start_year_jalali`, `start_month_jalali`, `start_day_jalali`
- `end_year_jalali`, `end_month_jalali`, `end_day_jalali`
- `period_type`: controlled source interval class, when known
- `fiscal_year`: company fiscal-year label, when established
- `fiscal_quarter`: 1–4 when established, otherwise NULL
- `months_length`: calendar-month span for a DURATION interval when it can be determined exactly; zero for INSTANT

### 3.2 Identity

Unique logical identity:

`(company_id, temporal_kind, start_jalali_date, end_jalali_date)`

Consequences:
- Two reports that refer to the same company and exact interval reuse the same logical period, even if their report labels differ.
- Fiscal labels and period_type are validated descriptive attributes, not identity substitutes.
- If the same exact interval is assigned conflicting fiscal classifications, do not silently create a second period; resolve the fiscal-calendar/source conflict or reject ingestion.
- An INSTANT has start = end.
- A DURATION has start <= end and, for a genuine duration, start < end.

### 3.3 Jalali date validation

Store Jalali components as integers. Validate month/day ranges and leap-year correctness in deterministic domain code. Do not convert to Gregorian merely to make SQL Date the authoritative representation. Gregorian helper values, if ever needed by an external library, are derived/transient and must not become the source of truth.

Sort by the tuple of Jalali components (year, month, day), not by period_id, insertion order, Gregorian conversion, or fiscal-quarter label.

## 4. INSTANT versus DURATION

### INSTANT
Use for balances and other values measured at one point in time:
- start date equals end date;
- months_length = 0;
- duration_basis = NULL / NOT_APPLICABLE;
- no YTD concept;
- period_type may be INSTANT (or an explicitly controlled point-in-time class), but must not pretend the value is a month/quarter flow.

Examples: closing cash balance, total equity at a reporting date, deposits outstanding at period end.

### DURATION
Use for flows accumulated or measured over an interval:
- start date is earlier than or equal to end date; for non-zero reporting spans it is strictly earlier;
- months_length is positive when the interval is an exact whole-calendar-month span;
- duration_basis must be explicitly STANDALONE or YTD for metrics whose semantics require this distinction;
- YTD interval must start on the actual fiscal-year start date and end on the reported end date;
- STANDALONE interval must use its actual source start and end dates and must not be assumed to begin at the fiscal-year start.

Examples: revenue over a month, net profit over a quarter, cumulative operating income from fiscal-year start to the reporting date.

If a source interval is not an exact whole-month span, preserve its exact Jalali dates. Do not fabricate months_length by dividing day count by 30. In that case, months_length may be NULL (recommended) unless the existing approved contract requires a stricter interval class; comparability must then use exact dates or an explicit interval-class rule. This point must be reconciled with DB-DES-003 before schema implementation.

## 5. Fiscal year and quarter rules

- `fiscal_year` is the label of the company's fiscal year, not necessarily the Jalali year of the period end.
- A fiscal-year start date must come from an authoritative company/report source or an approved company fiscal-calendar record.
- The first fiscal month may be any Jalali month; never default to month 1.
- A fiscal quarter is assigned only when the actual interval and approved company fiscal calendar establish it.
- A YTD value is cumulative from the exact fiscal-year start date, not from a guessed calendar-year start.
- A standalone Q2 interval is the actual interval covered by Q2 only; it is not the six-month YTD interval.
- The annual fiscal interval may be represented as YTD when the source reports the cumulative full fiscal year. Its duration basis remains explicit even though it spans the full fiscal year.
- Fiscal year/quarter labels alone cannot establish exact start/end dates. If dates are absent, derive them only from a previously approved fiscal calendar with deterministic coverage; otherwise reject.

## 6. Period type and months_length

`period_type` describes the source interval class, not report publication cadence. Controlled examples:
- MONTH
- QUARTER
- SEMI_ANNUAL
- NINE_MONTH
- ANNUAL
- INSTANT

Do not use TTM as a source period type. TTM is a runtime analytical window.

`months_length`:
- INSTANT = 0;
- DURATION = exact number of calendar months only when supported by the actual Jalali interval and company fiscal calendar;
- never infer it from day count / 30;
- if the interval is not an exact whole-month span, use NULL and compare by exact interval or an approved interval class rather than inventing a month count.

The existing DB-DES-009 proposal currently says DURATION months_length > 0. This should be refined to permit NULL for non-whole-month intervals, or the domain may explicitly reject such intervals if V1 source evidence proves they cannot occur. Do not choose the restrictive option without examining real reports.

## 7. YTD / standalone interpretation rules

### 7.1 Explicit source semantics take precedence

Determine basis from:
1. explicit header/column temporal axis or report label that has been semantically approved;
2. explicit source description and exact date interval;
3. an approved company/report-family temporal rule with unambiguous coverage.

Publication date, report title alone, fiscal_quarter alone, or period_type alone is insufficient.

### 7.2 No implicit arithmetic conversion at ingestion

- A source-reported YTD value is stored as YTD.
- A source-reported standalone value is stored as STANDALONE.
- A standalone quarter calculated as current YTD minus prior YTD is a runtime-derived value, not a source FinancialFact.
- Such subtraction is allowed only when fiscal year, metric, dimension set, unit/basis, report-version compatibility and temporal boundaries are all compatible.
- If the current and prior cumulative versions do not form a valid chain, the derived standalone interval is unavailable.
- No calculated standalone amount is written to FinancialFact or another persistent derived table.

### 7.3 Monthly activity reports

Monthly reports commonly represent a month-specific amount, but the pipeline must not assume this universally. Each report family/column mapping must explicitly declare STANDALONE or YTD. A monthly report that explicitly provides cumulative values is stored as YTD with its true fiscal-year-to-date interval.

### 7.4 Instant facts

YTD is inapplicable to INSTANT. A balance at a date is a point-in-time observation, not a cumulative duration.

## 8. Stage 5 temporal comparability

Stage 5 must query and compare temporal shapes explicitly.

### 8.1 Flow metrics

For REVENUE, OPERATING_PROFIT, NET_PROFIT and other DURATION metrics:
- select only approved temporal basis for the metric/binding;
- margin numerator and denominator must share the same exact period interval, duration_basis, fiscal-year identity where relevant, unit/basis compatibility and dimension selector;
- historical growth compares standalone intervals of comparable length and fiscal position, unless a separately versioned transformation is approved;
- YTD observations must never be compared directly to standalone quarters;
- if only YTD source values exist, a compatible runtime standalone derivation may be used only under §7.2; otherwise historical growth input is unavailable.

### 8.2 Stock metrics

For TOTAL_EQUITY and other stock metrics:
- require INSTANT;
- closing value is latest PIT-eligible instant at or before the selected reference date;
- opening value is the nearest earlier PIT-eligible instant under the same metric and dimension selector;
- no duration fact may substitute for a stock fact.

### 8.3 Non-calendar fiscal years

Comparability is based on fiscal-year identity and actual Jalali boundaries, not calendar-year labels. Q1 of a fiscal year beginning in Mehr is not comparable to Q1 of a company whose fiscal year begins in Farvardin merely because both are called Q1. For a single company, compare equivalent fiscal intervals within that company's approved calendar.

### 8.4 TTM

TTM is a runtime window, not a persisted period or source fact. It may be computed only from a complete, non-overlapping chain of compatible standalone durations (or through an explicitly approved deterministic conversion from cumulative values). Missing intervals, overlap, inconsistent fiscal boundaries or incompatible dimensions make TTM unavailable.

## 9. Ingestion acceptance and fail-closed cases

Reject the whole report ingestion unit if any in-scope fact has:
- missing or ambiguous actual Jalali start/end dates;
- unknown INSTANT/DURATION kind;
- a stock metric mapped to DURATION or a flow metric mapped to INSTANT;
- unknown YTD/standalone basis where the metric requires it;
- YTD dates that do not start at the approved fiscal-year boundary;
- conflicting fiscal-year/quarter assignments;
- period_type or months_length inferred from report publication date or guessed day arithmetic;
- conflicting duplicate facts whose only distinction is an unapproved temporal qualifier.

Do not create a placeholder FinancialPeriod or a NULL fact to hide a temporal interpretation failure. Explicit source-reported NULL is distinct and follows DB-DES-009 value-state rules.

## 10. Required refinements to DB-DES-009 and DB-DES-010

Before ORM/migration:
1. Keep `is_ytd` out of FinancialPeriod; represent `duration_basis` on FinancialFact.
2. Add `INSTANT` as a controlled period kind/class or otherwise represent it explicitly; do not classify instant rows as MONTH/QUARTER.
3. Make `months_length` zero for INSTANT, exact positive whole-month count for aligned DURATION, and NULL for irregular intervals unless owner-approved source evidence justifies rejection.
4. Remove TTM from source-period catalog; runtime-only.
5. Add explicit temporal basis to Stage 5 metric bindings and query identity/selection.
6. Keep exact Jalali dates authoritative and company fiscal-calendar boundaries explicit.
7. DB-DES-003, DB-DES-009 and DB-DES-010 have been amended to the same fact-level ownership rule; Architecture V1.3 has also been amended in the coordinated documentation update.

## 11. Remaining technical gates

The following are implementation questions, not requests for owner decision:
- whether irregular non-whole-month DURATION intervals occur in V1 reports; if none, schema may require months_length > 0 for all DURATION;
- which exact source fields/approved fiscal-calendar records establish company fiscal-year start and fiscal quarter;
- verify that `duration_basis` is a NOT NULL constrained field for applicable DURATION facts and NULL only for INSTANT facts (with metric-specific applicability checks).

**Resolved:** use a `duration_basis` field on FinancialFact. This is value semantics, is queried frequently, and must not be global to a period shared by different metric interpretations.

## 12. Implementation gates

No ORM or migration work should begin until:
- source evidence and fiscal-calendar gates below are closed;
- Migration 9 lineage is resolved;
- company fiscal-year boundary source is identified for each report family;
- the current real workbook samples are checked for explicit YTD/standalone headers and exact period dates;
- a later-period workbook is used to validate that temporal headers/bindings remain stable;
- adversarial tests are specified for non-calendar fiscal years, YTD vs standalone, Q4/full-year, missing periods, and PIT restatements.

Owner runs tests locally; no test result is claimed by this design document.

## 13. Status

DB-DES-011 records the accepted fact-level temporal ownership rule and its remaining implementation gates. It does not authorize code, ORM, migration, data mutation, PDF retirement, or legacy table deletion. All existing schemas and rows remain unchanged.
