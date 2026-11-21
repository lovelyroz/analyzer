> **HISTORICAL / SUPERSEDED — 2026-11-21:** PDF-path observations and plans in this document describe the retired implementation and do not define current support or acceptance. File inputs are Excel/CSV only. See database/reports/DB_CODAL_RETIRE_001_EXCEL_CSV_ONLY_RETIREMENT.md.

# DB-DES-012 — Temporal Contract Reconciliation Audit

**Status:** RECONCILIATION AUDIT COMPLETE — fact-level duration_basis decision accepted and coordinated document amendments applied; source-evidence and implementation gates remain open  
**Date:** 2026-11-18  
**Scope:** Reconcile normative Architecture V1.3, DB-DES-003, DB-DES-009, DB-DES-010 and DB-DES-011 before ORM/migration  
**No implementation:** no ORM, migration, runtime code, database rows, or tests changed.

## 1. Executive result

The four supporting design documents are broadly aligned on the business rules, but they are **not yet fully reconciled with the normative Architecture V1.3**. The central conflict is temporal ownership:

- At audit time, Architecture V1.3 and DB-DES-003 described `is_ytd` as a FinancialPeriod attribute; this conflict has since been corrected by the coordinated amendment recorded below.
- DB-DES-009 already identifies this as unresolved and says YTD may need to move to fact-level interpretation.
- DB-DES-010 requires every duration observation to expose a `duration_basis`.
- DB-DES-011 recommends `duration_basis` on FinancialFact, because a shared FinancialPeriod identifies actual dates/shape and must not carry a value-specific accumulation meaning.

**Decision applied:** YTD/standalone belongs to each applicable FinancialFact as `duration_basis`; FinancialPeriod stores only actual Jalali interval, temporal kind and period classification. Architecture V1.3, DB-DES-003, DB-DES-009, DB-DES-010 and DB-DES-011 were amended in a coordinated documentation sequence. The amendments resolve ownership, but do not make the physical schema implementation-ready: source-evidence and fiscal-calendar gates remain open.

## 2. Normative hierarchy and change control

Architecture V1.3 explicitly states that it is the normative architecture entry point and supporting documents do not override its approved decisions. Therefore:
- DB-DES-011 did not silently supersede Architecture; the coordinated amendment explicitly changed the normative Architecture and all supporting contracts.
- This audit records a proposed architectural amendment; it does not itself amend the normative contract.
- DB-DES-003 remains PARTIAL and is a supporting logical contract.
- DB-DES-009 and DB-DES-010 remain physical/query proposals, not implementation authorization.

The sequence completed for this decision is: technical ownership rule selected → Architecture and supporting contracts amended together. Remaining source-evidence, fiscal-calendar and Migration 9 gates must close before physical ORM/migration design can proceed.

## 3. Reconciliation matrix

| Topic | Architecture V1.3 | DB-DES-003 | DB-DES-009 | DB-DES-010 | DB-DES-011 | Reconciled recommendation |
|---|---|---|---|---|---|---|
| Calendar authority | Jalali | Jalali | Jalali redesign | Jalali ordering | Jalali | Consistent; Jalali components are authoritative |
| Actual period identity | Company + shape + exact dates | Same | Jalali period FK | Period series by Jalali dates | Company + kind + exact dates | Consistent |
| INSTANT/DURATION | Both required | Both required | Both required | Metric-specific expected kind | Both required | Consistent |
| YTD ownership | FinancialPeriod `is_ytd` | FinancialPeriod `is_ytd` | Explicitly unresolved | Fact-level duration_basis needed | FinancialFact duration_basis | **RESOLVED: fact-level duration_basis** |
| Standalone source | Explicitly reported standalone may be stored | Same | Needs fact-level temporal interpretation | Comparable standalone inputs | STANDALONE basis | Consistent after ownership change |
| Standalone derived from YTD | Runtime only | Runtime only | Runtime-only calculations | Runtime-only | Runtime-only | Consistent |
| TTM | Runtime only, not source period | Same | Not source period | Query/analytical window | Runtime only | Consistent |
| Fiscal year | Company-specific, not presumed Farvardin | Same | Field retained | Comparability requires fiscal identity | Company fiscal calendar | Logical rule consistent; physical fiscal-calendar source unresolved |
| Fiscal quarter | 1–4 if valid | 1–4 if valid | Field retained | Fiscal interval class | Assign only with approved calendar | Consistent |
| months_length | Number of months represented | Actual duration | DURATION > 0 proposed | Required for duration comparisons | exact whole-month count; NULL for irregular | **Unresolved for irregular spans** |
| Rate/ratio temporal kind | Source-defined | Source-defined | Needs preservation | Not fully detailed in initial metric bindings | Source-defined instant or duration | Logical alignment; metric-specific catalog needed |
| Comparative role | Fact period is actual period | PRIMARY/COMPARATIVE/UNKNOWN context | Not a core identity field | ReportVersion provenance preserved | Not central to temporal shape | Preserve publication-version linkage; explicit role may need mapping metadata |
| Report primary period | Metadata only; facts have own periods | Explicit | Report-level period not allowed to constrain facts | Period series | Not disputed | Consistent |
| PIT/version ranking | Four-level ranking and latest equal-ranked publication | Same | ReportVersion reuse | Same | Not changed | Consistent; do not rewrite ranking |
| Date derivation | Source/approved calendar only | Same | Requires exact Jalali dates | Jalali order | Same | Consistent |
| Unknown/ambiguous period | Reject, no guessing | Reject | Fail closed | Inputs unavailable/reject | Reject ingestion unit | Consistent |

## 4. Required architectural amendment — YTD ownership

### Current wording that conflicts

Architecture Section 3 and its FinancialPeriod contract currently define:
- `is_ytd` as a FinancialPeriod attribute;
- cumulative quarterly filing examples with `is_ytd=true`;
- monthly source periods with `is_ytd=false`;
- a duration FinancialPeriod with applicable YTD semantics.

DB-DES-003 repeats this placement.

### Proposed replacement

**FinancialPeriod**
- company identity;
- temporal kind: INSTANT or DURATION;
- exact Jalali start and end;
- fiscal year and fiscal quarter where established;
- source interval class / period_type;
- months_length under the resolved rule.

**FinancialFact**
- `duration_basis`: `YTD` or `STANDALONE` for applicable DURATION facts;
- NULL / NOT_APPLICABLE for INSTANT facts;
- value-state, metric, dimensions, unit/basis, source ReportVersion and applicable interpretation standard as already defined by DB-DES-009.

Why: FinancialPeriod is a reusable identity for actual time boundaries. YTD/standalone describes how a particular reported value accumulates over those boundaries. A single period row must not force all facts attached to it to share the same value basis. This is particularly important for multi-table/multi-header workbooks and for period identity reuse.

The temporal basis must be explicit for source-reported DURATION facts where the metric's meaning requires it. It must not be inferred from quarter number, report title, publication date, or date-end alone.

## 5. months_length decision remains open

The documents agree that `months_length` must describe the actual interval and must never be guessed as day-count divided by 30. They differ in how to represent an irregular duration:

- DB-DES-009 proposes DURATION `months_length > 0`.
- DB-DES-011 recommends NULL if exact whole-calendar-month length cannot be established.
- Architecture says months_length is the number of months represented but does not explicitly settle irregular/non-whole-month cases.

**Recommendation:** retain exact Jalali start/end as authoritative; use integer months_length only for exact calendar-month spans. Permit NULL for irregular spans only if the V1 source audit confirms such spans can occur and query logic can compare exact intervals. If the real accepted V1 sources always use whole-month spans, a positive integer constraint for DURATION is simpler and safer. Do not choose either schema constraint without inspecting the source examples and the existing DB-AUD-002 evidence.

INSTANT remains unambiguous: start=end, months_length=0.

## 6. Fiscal-calendar source and lifecycle — still unresolved

All documents require company-specific fiscal boundaries but none yet fully specifies the operational physical source and lifecycle of that information.

Before schema implementation, define:
- whether fiscal-year start is maintained as company configuration, a versioned fiscal-calendar record, or derived from an approved report-family standard;
- effective-from/effective-to dates if a company changes its fiscal year;
- how a report's explicit dates are validated against the approved calendar;
- how fiscal_year labels are assigned when a fiscal year crosses Jalali year boundaries;
- whether historical calendar definitions are immutable/versioned.

**Recommendation:** use a versioned company fiscal-calendar record if fiscal-year boundaries can change or if historical periods must be reproducible. Do not add a static assumed month/day to Company without proving that the fiscal calendar is immutable. A source report may establish the dates for a period, but a one-off report label must not silently redefine the company's fiscal calendar.

## 7. Comparative role and source temporal axes

DB-DES-003 explicitly identifies each value's relation to the Report's primary period as PRIMARY, COMPARATIVE or UNKNOWN. DB-DES-009's fact identity centers on actual period and ReportVersion and does not yet clearly specify where this role is represented.

Recommendation:
- do not include PRIMARY/COMPARATIVE as part of FinancialPeriod identity;
- if this role is needed for audit, retain it as versioned interpretation/provenance metadata on the fact or extraction decision;
- never use it instead of actual FinancialPeriod;
- comparative facts remain published by the ReportVersion that contains them and become PIT-available only at that version's publication time;
- primary and comparative observations for the same economic period must not be silently summed or overwritten.

The exact physical field/table is a DB-DES-009 refinement, not yet approved.

## 8. Rate/ratio and metric temporal catalog

DB-DES-003 correctly permits a rate or ratio to be INSTANT or DURATION according to its source definition. DB-DES-010's initial binding table lists the principal Stage 5 metrics but does not fully define all rate/ratio semantics.

Before implementation:
- each metric definition must specify allowed temporal kind(s);
- each duration metric binding must specify whether STANDALONE, YTD, or both are accepted;
- each ratio must define numerator/denominator period and basis compatibility;
- a rate observed at a date must not be coerced into a duration;
- a period-average rate must not be treated as an instant.

No generic default should be introduced for all rates or ratios.

## 9. Already aligned decisions — do not reopen

The following are consistent across the reviewed documents and existing owner decisions:
- Jalali is authoritative; Gregorian conversion is not the financial-period source of truth.
- Each FinancialFact has its actual period; one ReportVersion may contain multiple periods.
- Report primary period is metadata and does not override fact-level period.
- INSTANT facts have start=end and no YTD.
- Stock/flow distinction controls temporal kind.
- YTD means from actual company fiscal-year start through the period end.
- Source-reported standalone may be stored; calculated standalone remains runtime-only.
- TTM remains runtime-only.
- Comparative facts are attached to the version that actually publishes them.
- PIT cutoff is applied before version ranking.
- Four-level audit/restatement ranking remains unchanged; equal-ranked candidates use newest valid CODAL publication datetime.
- Unknown/ambiguous dates or temporal meaning must fail closed.
- No calculated outputs are persisted.

## 10. Coordinated document amendments — completed

Completed in the coordinated documentation update:
1. Architecture V1.3: global FinancialPeriod `is_ytd` removed; fact-level `duration_basis` established.
2. DB-DES-003: period and YTD/standalone semantics updated; comparative and PIT semantics retained.
3. DB-DES-009: FinancialPeriod excludes `is_ytd`; FinancialFact includes `duration_basis`.
4. DB-DES-010: duration_basis is required in query projection and validation.
5. DB-DES-011: status changed to ACCEPTED DESIGN DECISION; remaining implementation gates retained.

Do not perform partial edits that leave Architecture and supporting documents contradictory.

## 11. Remaining gates before implementation

1. Source-evidence check for irregular/non-whole-month DURATION intervals and months_length constraint.
2. Identify authoritative fiscal-calendar source and lifecycle.
3. Decide physical representation of PRIMARY/COMPARATIVE/UNKNOWN role, if retained.
4. Resolve Migration 9 lineage discrepancy (local DB has migration 9; repository runner previously showed only 1–8).
5. Validate temporal headers and dates against a later-period workbook from a company already represented by an approved template.
6. Specify adversarial tests: non-calendar fiscal year, same period with different value bases, Q4/full-year, comparative period published in a later ReportVersion, PIT restatement, instant/flow mismatch, irregular interval and incomplete YTD differencing chain.

Until these gates are met, no ORM, migration, data migration, destructive legacy cleanup, or production PDF retirement is authorized.

## 12. Status

The reconciliation audit is complete. The fact-level duration_basis decision has been applied consistently to Architecture and supporting contracts. DB-DES-003 remains PARTIAL because fiscal-calendar, irregular interval, comparative-role and source-evidence gates remain open. No code, ORM, migration, database rows, or tests changed.
