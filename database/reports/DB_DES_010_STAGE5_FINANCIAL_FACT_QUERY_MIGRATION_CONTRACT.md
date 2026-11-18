# DB-DES-010 — Stage 5 FinancialFact Query Migration Contract

**Status:** DESIGN PROPOSAL; NO CODE OR SCHEMA CHANGE AUTHORIZED  
**Date:** 2026-11-18  
**Depends on:** DB-DES-009, DB-AUD-014, DB-AUD-015  
**Scope:** Replace Stage 5 reads from legacy `normalized_financial_facts` with dimension-aware, Jalali-period-aware reads from the proposed canonical `financial_facts` table.

## 1. Objective and non-goals

Stage 5 is the only direct production reader of `NormalizedFinancialFact` found in DB-AUD-014. Its database query is in `src/forecast/queries.py`; `src/forecast/service.py` uses those observations to build an in-memory forecast context and returns runtime results.

This contract defines the query behavior required when the canonical Excel pipeline begins writing `financial_facts`.

It does **not** authorize:
- ORM or migration changes;
- a new canonical writer;
- a production switch or dual-read;
- deletion of legacy Normalized/Derived tables;
- persisted forecast or derived outputs;
- automatic migration/backfill of legacy rows.

The local database snapshot from DB-AUD-015 has zero rows in all four Normalized/Derived tables. This removes a local row-backfill requirement for that one database file, but does not prove other environments are empty.

## 2. Current Stage 5 behavior inspected

Current `src/forecast/queries.py`:
1. Reads `NormalizedFinancialFact.value_irr`, metric code, period ID/end date, source ReportVersion ID and publication datetime.
2. Filters by company, requested metric codes and `publication_datetime <= cutoff`.
3. Groups observations by `period_id`.
4. Within each period and metric code, chooses the row with latest publication datetime.
5. Builds a period series; NULL values are omitted from the numeric fact dictionary.
6. Converts selected values to Python `float`.
7. Sorts periods by numeric `period_id`, then treats the final one as latest.
8. Creates `ForecastInputRef(fact_key, report_version_id, available_at, source)`.
9. Stage 5 derives margins, prior revenue and beginning equity in memory. No database writes occur.

### 2.1 Behaviors to preserve

- Strict publication-time PIT cutoff, inclusive at the exact cutoff.
- Report-version provenance for every reported input.
- Latest eligible report version for each logical fact, under the approved version ranking.
- One selected value per Stage 5 metric/dimension/period.
- NULL is not treated as zero.
- A genuine reported zero remains a valid zero.
- Historical observations remain available for opening balance and prior-period context.
- Derived values remain in memory and do not create database rows.
- Stage 5 forecast generation remains read-only.

### 2.2 Current implementation details that must not be copied as new canonical rules

- Sorting by numeric `period_id` is not a valid chronological contract. The canonical query must sort by authoritative Jalali period boundaries.
- Latest publication timestamp alone is not sufficient when the report-version audit/restatement ranking has a higher-priority rule. Apply the approved ReportVersion ranking first, then choose newest publication among equal-ranked candidates.
- Metric code alone is no longer a sufficient selector when facts may have different approved dimension sets.
- The legacy `value_irr`/float conversion cannot define canonical unit, basis or numeric precision.
- The current query does not prove comparability of duration values (standalone vs YTD, or period length) before constructing historical growth inputs.

## 3. Query identity and scope

The canonical query starts from:
- `company_id`;
- a requested Stage 5 metric binding (stable `metric_code`);
- a requested forecast cutoff datetime;
- an approved Stage 5 dimension-selection policy for that metric;
- the required temporal kind and basis policy.

Company identity is resolved through:
`financial_facts.report_version_id -> reports.company_id`.

The query must verify the ReportVersion belongs to the requested company. Do not rely on a duplicated company ID on FinancialFact unless the physical schema later introduces and enforces it.

A selected canonical fact is identified by:
`(report_version_id, period_id, metric_id, dimension_set_id)`.

No query may silently aggregate across different dimension sets.

## 4. ReportVersion eligibility and PIT selection

### 4.1 Cutoff

A version is eligible only if:
- `publication_datetime` is known and valid;
- normalized publication instant is less than or equal to the requested cutoff;
- the version belongs to the requested company's Report;
- required template and interpretation-standard bindings are valid for new canonical facts.

A publication exactly equal to cutoff is eligible. A later publication is excluded even if it is marked current or restated today.

### 4.2 Version ranking

For each logical fact identity apart from ReportVersion (company, actual period, metric, dimension set and applicable scenario/basis), apply the approved report-version precedence:
1. audit/restatement eligibility and ranking rules;
2. among versions tied at the same priority, newest publication datetime wins;
3. if publication datetime also ties, use a deterministic stable final tie-break only if the source contract establishes one; otherwise treat the candidates as ambiguous and fail closed.

Preserve all versions and their provenance. Selection is a read-time PIT decision; never overwrite an older version.

A future restatement must not replace the version that was knowable at an earlier cutoff. A report marked current now is not automatically the version visible at a historical cutoff.

### 4.3 Publication time and missing metadata

A new canonical ReportVersion without a valid publication datetime cannot supply a Stage 5 PIT fact. Do not substitute ingestion time, file timestamp, current time, or report period end.

## 5. Period ordering and temporal comparability

### 5.1 Authoritative order

Use Jalali components from the redesigned FinancialPeriod as the authoritative period order:
- duration: compare end date, then start date and deterministic period identity;
- instant: compare the exact Jalali instant date;
- do not sort by database ID, insertion order, Gregorian conversion, or fiscal-quarter label alone.

The query returns chronological periods oldest to newest. The latest period is the greatest eligible Jalali end boundary under the relevant metric policy.

### 5.2 Temporal kind

The Stage 5 metric binding declares expected temporal kind:
- flow metrics (e.g. revenue, operating profit, net profit): DURATION;
- stock metrics (e.g. total equity): INSTANT;
- ratios/per-share metrics require explicit metric-specific semantics and are not inferred from the current `flow_or_stock` field alone.

Reject facts whose temporal kind conflicts with the approved metric definition.

### 5.3 Duration basis and period length

For each duration fact, the query must know:
- exact Jalali start/end;
- months_length;
- whether the value is standalone or cumulative/YTD;
- fiscal-year identity where needed.

Do not compare or combine duration values with incompatible bases or lengths.

For Stage 5 V1:
- margins may be calculated only from numerator and denominator observations with the same actual period and compatible temporal basis;
- historical revenue comparisons must use comparable standalone intervals (same duration length and matching fiscal interval class), or an explicitly approved transformation that produces comparable standalone values before query consumption;
- do not treat a YTD cumulative amount as a standalone quarter;
- if only cumulative/YTD values exist and no approved deterministic conversion is available, the affected historical growth input is unavailable; do not fabricate a flat rate or silently compare mismatched intervals.

### 5.4 Stock observations

For TOTAL_EQUITY and other stock metrics:
- use INSTANT period facts;
- the current ending balance is the latest PIT-eligible instant at or before the selected forecast reference date;
- beginning equity is the nearest earlier PIT-eligible instant observation with the same metric and dimension selector;
- do not use a duration/flow value as a stock observation.

### 5.5 Latest reporting period across metrics

Do not force every metric to share one global latest period if the latest report legitimately omits a metric. Select the latest eligible observation per metric under its own temporal/dimension policy, then construct the Stage 5 context only from compatible facts. If a Stage 5 calculation requires same-period inputs (e.g. operating profit/revenue margin), both facts must resolve to the same period identity and compatible basis; otherwise that derived input is unavailable.

## 6. Dimension selection contract

The new model is dimension-aware. Every Stage 5 metric binding must declare one of these policies:

1. **EXACT_DIMENSION_SET** — select one explicitly approved canonical dimension-set key.
2. **EMPTY_DIMENSION_SET_ONLY** — select only the canonical empty set for company-level facts.
3. **APPROVED_SELECTOR** — select one dimension-set matching a versioned, metric-specific selector (for example a consolidated/company-total value) with deterministic exact matching.

Rules:
- No automatic SUM, MAX, MIN, first-row, latest-row, or arbitrary choice across dimension sets.
- If more than one fact matches the declared selector for the same ReportVersion/period/metric, reject the query result as ambiguous; do not pick one.
- If no fact matches, the metric is unavailable for that period.
- If a metric needs aggregation across segments/products, that aggregation must be separately specified as a versioned semantic calculation with explicit non-overlap and completeness rules. It is not part of the generic Stage 5 query.
- Dimension selector version must be included in the Stage 5 model/configuration provenance.

The initial Stage 5 bindings should default to EMPTY_DIMENSION_SET_ONLY unless an approved metric definition explicitly requires a non-empty dimension. This prevents accidental use of a segment/product amount as a company-wide metric.

## 7. Value state, units and numeric handling

### 7.1 Value states

| FinancialFact state | Stage 5 query behavior |
|---|---|
| `REPORTED_VALUE` with non-NULL integer (including 0) | Eligible subject to metric policy |
| `REPORTED_NULL` with NULL | Omit as unavailable; never coerce to zero |
| `ZERO_FALLBACK` with integer 0 | Include only if the Stage 5 metric binding explicitly permits this fallback state; otherwise treat as unavailable and expose a quality/provenance reason |

A missing fact row is not a NULL fact and must not be synthesized by the query.

### 7.2 Unit/currency/basis

Stage 5 must consume only values whose canonical unit, currency and basis match the metric binding. No implicit Rial conversion, scale adjustment, per-share conversion, or quantity conversion is allowed in the query.

If a metric is monetary, the query may require canonical Rial. If it is quantity, ratio, price-per-unit or per-share, the binding must specify its exact canonical unit and basis.

### 7.3 Integer and Decimal

- Read persisted INTEGER values as integers/Decimal-compatible exact values.
- Do not convert to binary float at the SQL/persistence boundary.
- Any conversion to float for the existing forecast engine must occur at one explicit adapter boundary, after range/precision checks and only if the engine contract accepts the approximation.
- Document the numeric tolerance for each affected Stage 5 calculation. If precision cannot be represented safely, fail closed or migrate the engine arithmetic to Decimal; do not silently round.
- No second ROUND_HALF_UP operation occurs in Stage 5. The canonical persistence boundary already performed the one approved rounding.

## 8. Provenance contract for Stage 5

Current `ForecastInputRef` contains:
`fact_key`, `report_version_id`, `available_at`, `source`.

For the canonical path, each direct input reference must additionally preserve:
- `financial_fact_id`;
- `period_id`;
- `dimension_set_id`;
- `metric_code`;
- `template_version_id`;
- `interpretation_standard_version_id`;
- `value_state`;
- canonical unit/currency/basis identity as needed.

`available_at` is the exact ReportVersion publication datetime, never the ingestion timestamp.

For a runtime-derived value (margin, prior/current comparison, opening-equity selection, dispersion pair):
- do not create a FinancialFact row;
- retain references to **all** direct facts used to derive it, not only the maximum publication timestamp;
- derived reference availability is the latest publication datetime among its source facts;
- preserve each source fact's own ReportVersion, period and dimension-set identity;
- if inputs came from different ReportVersions, do not collapse them into one fabricated ReportVersion ID.

This likely requires a structured multi-input provenance object or a `source_fact_refs` collection in the runtime forecast schema. Keep this runtime-only; do not persist derived input graphs.

## 9. Metric-specific Stage 5 query bindings

Initial binding proposal:

| Metric code | Expected temporal kind | Initial dimension policy | Stage 5 use |
|---|---|---|---|
| `REVENUE` | DURATION | EMPTY_DIMENSION_SET_ONLY | Latest comparable revenue; historical comparable standalone series |
| `OPERATING_PROFIT` | DURATION | EMPTY_DIMENSION_SET_ONLY | Same-period numerator for operating margin |
| `NET_PROFIT` | DURATION | EMPTY_DIMENSION_SET_ONLY | Same-period numerator for net margin; EPS only if attributable basis is separately proven |
| `TOTAL_EQUITY` | INSTANT | EMPTY_DIMENSION_SET_ONLY | Latest closing balance and nearest prior closing balance |
| `EPS` | Metric-specific; explicit per-share basis required | EMPTY_DIMENSION_SET_ONLY | Not used as a substitute for profit; retain only if a separate Stage 5 rule consumes it |

These are defaults for the current Stage 5 seeded metric vocabulary, not authorization to create missing metric mappings. If the semantic standard establishes another valid dimension or temporal shape, revise the binding explicitly and version it.

The current Stage 5 EPS rule remains unchanged: `NET_PROFIT` is not presumed to be profit attributable to common shareholders. The query migration must not weaken the existing fail-closed behavior.

## 10. Query output shape and deterministic selection

Recommended logical output per selected fact:

```text
SelectedFinancialObservation:
  financial_fact_id
  company_id (resolved and validated)
  period_id
  jalali_period_start/end
  temporal_kind
  duration_basis
  months_length
  metric_id / metric_code
  dimension_set_id / canonical_key
  value_integer
  value_state
  canonical_unit/currency/basis
  report_version_id
  publication_datetime
  template_version_id
  interpretation_standard_version_id
```

The period-series query returns one observation per:
`(period identity, metric binding, selected dimension set)`.

The latest-facts query derives its values from that period series; it must not implement a second independent selection algorithm.

Deterministic order:
1. period chronological order by Jalali boundaries;
2. metric code;
3. ReportVersion ranking;
4. publication datetime;
5. stable ID only as a final tie-break when source semantics guarantee equivalent candidates.

If the last tie-break would conceal a semantic conflict, fail closed instead.

## 11. Acceptance and regression requirements

Before switching Stage 5 to the new table, add tests proving:

1. Publication exactly at cutoff is included; one instant after cutoff is excluded.
2. A future restatement/current flag cannot leak into an earlier cutoff.
3. Audit/restatement priority precedes newest-publication tie-break; equal-ranked candidates choose newest publication.
4. A publication-time tie without a valid source tie-break fails closed.
5. Period order follows Jalali dates even when period IDs are deliberately out of chronological order.
6. Non-calendar fiscal years and Jalali year boundaries order correctly without Gregorian conversion.
7. Flow and stock facts cannot be interchanged.
8. YTD and standalone values are never silently mixed.
9. Historical revenue comparisons require comparable standalone intervals.
10. Margins require same-period, compatible-basis numerator and denominator.
11. Beginning equity selects the nearest earlier valid INSTANT fact.
12. Empty dimension set is selected by default; segment/product facts are never substituted.
13. Multiple matching dimension sets fail closed; no implicit aggregation.
14. REPORTED_NULL is omitted; genuine REPORTED_VALUE zero remains zero.
15. ZERO_FALLBACK follows explicit metric policy and is traceable.
16. Unit/currency/basis mismatch is rejected or reported unavailable, never silently converted.
17. All direct and multi-input derived provenance is preserved in runtime output.
18. Integer precision is maintained until the explicit engine adapter boundary.
19. Forecast generation performs no INSERT/UPDATE/DELETE and persists no derived output.
20. Query behavior remains deterministic across repeated runs and database insertion orders.

Owner executes tests locally. Do not claim tests pass until owner supplies the result.

## 12. Migration sequence and gates

1. Approve DB-DES-009 physical model and resolve its open period/dimension/provenance decisions.
2. Approve Stage 5 metric binding and temporal comparability rules in this document.
3. Reconcile Migration 9 source/database lineage before any schema migration.
4. Implement additive ORM/migration for the canonical fact structures.
5. Implement Excel canonical writer and end-to-end atomicity/idempotency tests.
6. Implement canonical Stage 5 query behind an explicit switch/contract; keep legacy query intact until verified.
7. Run parity/adversarial tests using real approved report versions and independent-period workbooks.
8. Switch Stage 5 read path only after evidence; then separately authorize legacy table retirement if all environments and consumers are reconciled.

No dual-write and no unverified union of legacy/new fact rows.

## 13. Decisions and open gates

| Topic | Contract recommendation | Status |
|---|---|---|
| PIT cutoff | publication <= cutoff; apply approved version ranking | PROPOSED |
| Equal-ranked version tie | newest publication wins | OWNER-DECIDED |
| Period order | Jalali boundaries, never period ID | PROPOSED |
| Dimension selection | explicit metric binding; empty set default; fail on ambiguity | PROPOSED |
| Duration comparability | no YTD/standalone or length mixing | PROPOSED |
| Stock selection | latest/nearest prior INSTANT | PROPOSED |
| NULL / zero / fallback | three distinct states and metric policy | OWNER-DECIDED / PROPOSED query behavior |
| Provenance | preserve direct fact IDs and all inputs of runtime derivations | PROPOSED |
| Derived output persistence | none; runtime-only | OWNER-DECIDED |
| Numeric conversion | INTEGER/Decimal until explicit engine adapter | PROPOSED |
| Migration 9 | resolve before migration | OPEN BLOCKER |

## 14. Outcome

DB-DES-010 defines the proposed query contract and identifies several correctness improvements required beyond a mechanical table rename: Jalali chronological ordering, approved report-version ranking, dimension selectors, temporal comparability and complete multi-input runtime provenance.

No ORM, migration, production code, database data or tests were changed. No tests were run. Owner review is required before implementation.
