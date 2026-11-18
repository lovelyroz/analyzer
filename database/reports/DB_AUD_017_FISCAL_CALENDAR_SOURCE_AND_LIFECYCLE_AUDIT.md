# DB-AUD-017 — Company Fiscal Calendar Source and Lifecycle Audit

**Status:** EVIDENCE AUDIT COMPLETE — no fiscal-calendar ORM/schema/migration design authorized yet  
**Date:** 2026-11-18  
**Mode:** Report only. No code, ORM, migration, database, workbook, or test changes.  
**Repository:** `lovelyroz/analyzer` / `master`  
**Depends on:** Architecture V1.3, DB-DES-003, DB-DES-011, DB-AUD-002, DB-AUD-016

## 1. Executive result

The project has a sound logical requirement but does not yet have a sufficiently reliable, general source contract for company fiscal-year boundaries.

The real-workbook audit DB-AUD-002 explicitly concluded that exact fiscal-year start dates remain unresolved for its samples. Some workbooks say “from the beginning of the financial year” without printing the actual start date. Other workbooks show dates that are fiscal-year labels, prior-year end dates, investee-company dates, or point-in-time balances; those must not be reinterpreted as the reporting company's fiscal calendar.

One company-specific exception is already owner-confirmed in the Master Working Packet: Bank Saderat's reviewed sample has a fiscal year beginning ۱۴۰۳/۰۱/۰۱ and ending at the end of Esfand. This is usable as a company-specific approved fact, not as a default for other companies.

**Conclusion:** V1 needs exact, company-specific, evidence-backed fiscal-year intervals with historical preservation. It must not derive a universal fiscal calendar from Jalali year numbers, report publication dates, a single `fiscal_year_end` string, or the common Farvardin-to-Esfand pattern.

## 2. Existing implementation and model gap

Current repository models inspected:

- `src/models/entity.py`: `Company.fiscal_year_end` is a nullable `String(10)`. It is a single company-level scalar; it does not model a historical sequence of fiscal years, effective dates, transition years, source evidence, or approval/revision history.
- `src/models/period.py`: `FinancialPeriod` currently uses SQL `Date` for `start_date` / `end_date`, integer `fiscal_year`, optional `fiscal_quarter`, and `months_length`. It still contains legacy `is_ytd` and includes `TTM` in `PERIOD_TYPES`; both conflict with the accepted target contract and require a separate, evidence-based migration plan.
- No dedicated Company Fiscal Calendar / Company Fiscal Year model was found in the inspected ORM modules.
- The migration runner currently imports the legacy Company and FinancialPeriod models. Migration 9 lineage remains a separate blocker and was not resolved by this audit.

These are current-state observations only. No ORM changes are proposed in this audit.

## 3. Source evidence review

### 3.1 Owner-confirmed Bank Saderat sample

The Master Working Packet records that the sample `reports/saderat_seasonal_report_2.md` belongs to Bank Saderat, confirmed by the owner, and that its fiscal year runs from ۱۴۰۳/۰۱/۰۱ through the end of Esfand. The same entry identifies the current six-month period ending ۱۴۰۳/۰۶/۳۱, the comparative six-month period ending ۱۴۰۲/۰۶/۳۱, and the prior full year ending ۱۴۰۲/۱۲/۲۹.

**Assessment:** This is sufficient to register a company-specific, owner-confirmed calendar fact for the represented fiscal year, subject to preserving the cited source/owner confirmation. It does not establish that all Iranian issuers, all banks, or even every future fiscal year of Bank Saderat use the same boundaries.

### 3.2 Parsian periodic samples

The Parsian periodic reports contain six-month labels ending ۱۴۰۳/۰۶/۳۱ and prior full-year labels ending ۱۴۰۲/۱۲/۲۹. These labels support the reported interval classes and end dates. They do not, by themselves, explicitly establish the exact current fiscal-year start date or prove the issuer's full fiscal-calendar lifecycle. The workbook filename is not proof of issuer identity; the Master Working Packet itself notes that the second sample's issuer identity was not independently established.

**Assessment:** Do not register a company calendar from the filename or infer the exact start date solely from a six-month label and a prior year-end date.

### 3.3 Postbank-named periodic sample

`database/reports/postbank_periodic_report_1.md` records equity roll-forward opening/closing labels and nine-month YTD evidence. It also explicitly warns that the workbook's required title and file name disagree, workbook title/subject metadata are blank, and issuer identity remains unverified. The opening/closing evidence is limited to the represented period and cannot be generalized to an issuer-level calendar while identity is unresolved.

**Assessment:** Useful as a structural example of possible explicit opening-date evidence, but not an approved company-calendar record.

### 3.4 Real workbook temporal audit (DB-AUD-002)

DB-AUD-002 inspected four Excel workbooks:

- `fzar.xlsx`: headers explicitly say “from beginning of fiscal year” through ۱۴۰۵/۰۶/۳۱ and ۱۴۰۵/۰۷/۳۰, but do not print the fiscal-year start date.
- `cheshme.xlsx`: YTD labels are explicit, but the actual start date is not printed in the identified flow headers; prior full-year end labels do not prove the next fiscal-year start.
- `fzar2.xlsx`: workbook title and statement headers provide some period end/length evidence, but the report's own audit identifies missing start dates and conflicting local statement dates.
- `samanBank.xlsx`: six-month flow labels and balance-date pairs are explicit, but the actual start date is not printed in the identified headers.

DB-AUD-002's unresolved list explicitly includes exact fiscal-year start dates for YTD headers. It also documents that the same workbook can contain multiple issuers' fiscal-year dates (e.g. investee-company metadata), forecasts, snapshots, and unrelated dates.

**Assessment:** A YTD label alone is not enough to create a fiscal-year boundary. The ingestion layer must distinguish issuer calendar evidence from investee dates, comparative periods, forecast dates, and local table dates.

## 4. Evidence hierarchy for V1

Use the following evidence hierarchy when establishing a company's fiscal-year boundaries:

1. **Explicit official company/CODAL disclosure of the exact fiscal-year start and end dates**, including a formal notice or approved disclosure explaining a fiscal-year change.
2. **An official annual financial statement or report that explicitly identifies both the beginning and end dates of the company's fiscal year**, with issuer identity verified.
3. **An owner-confirmed company-specific calendar record**, tied to a cited official source or a documented reviewed sample. Owner confirmation can approve a record for V1 but must not be generalized to other companies.
4. **Other source evidence** may be retained as a candidate but cannot authorize automated YTD interpretation until reviewed and approved.

The following are insufficient on their own:

- a report's publication datetime;
- the workbook filename, worksheet name, creator metadata, or report title without verified issuer identity;
- a period end date alone;
- a six-/nine-/twelve-month label that omits the actual start date;
- “از ابتدای سال مالی” without an exact start date or a previously approved calendar covering that fiscal year;
- a date belonging to an investee, subsidiary, forecast, comparative column, or another table;
- a market-wide assumption that the fiscal year begins on Farvardin 1.

When an explicit source period conflicts with the approved calendar, do not silently overwrite the calendar or force the fact into the existing fiscal year. Stop admission for the affected report and reconcile the conflict.

## 5. Recommended logical lifecycle (design direction, not physical schema)

The data model should represent **actual fiscal-year instances**, not only a reusable month/day rule:

- Each record belongs to exactly one verified Company.
- Each record represents one actual fiscal year with exact Jalali start and end dates.
- The source fiscal-year label is retained separately from the exact date boundaries; it must not be assumed equal to the Jalali year of the end date.
- The record carries its evidence reference, evidence type, verification/approval state, and the time at which the application recorded/approved it.
- Historical fiscal-year records are immutable after approval. A correction creates a new auditable revision rather than silently rewriting history.
- A change in the company's financial year creates an explicitly bounded transition fiscal year (which may be shorter or longer than twelve months), followed by new fiscal-year instances. Do not force the transition into a standard 12-month year.
- A company's calendar may be considered continuous only when adjacent boundaries are supported by evidence. Do not auto-fill gaps or assume no gaps/overlaps.
- Company-level `fiscal_year_end` may remain as a legacy/display hint during transition, but it is not authoritative for historical periods and must not drive YTD assignment.

This direction allows a fiscal year to change without rewriting facts from earlier years. FinancialPeriod can then reference or resolve to the approved fiscal-year instance for its company and actual dates. The final FK/uniqueness design is deferred until the Migration 9 lineage and physical-model gates are closed.

## 6. Deterministic assignment rules

1. A FinancialPeriod's exact Jalali start/end dates remain authoritative for the observed interval.
2. `fiscal_year` and `fiscal_quarter` are assigned only when an approved company fiscal-year record and the source evidence establish them.
3. A DURATION FinancialFact receives `duration_basis=YTD` only when its actual start date equals the approved fiscal-year start date and the source semantics establish cumulative value.
4. A source-reported standalone value receives `duration_basis=STANDALONE` only when the source establishes its actual standalone interval.
5. A YTD label with no resolvable start date is unresolved. Do not manufacture the start date from publication date, report title, period length, or a guessed month.
6. A fiscal-year label or quarter number without exact dates cannot manufacture a FinancialPeriod.
7. A short/long transition year is valid only when supported by official source evidence; it must not be normalized to 12 months.
8. Unknown issuer identity blocks company-calendar assignment.
9. Conflicting or incomplete temporal evidence rejects the report under the existing all-or-nothing admission rule.
10. Comparative values remain attached to the ReportVersion that publishes them; their fiscal-year classification describes the period they represent, not the publishing version's current year.

## 7. Open evidence gates

Before physical schema/ORM/migration work:

- Verify and capture the official source supporting Bank Saderat's owner-confirmed ۱۴۰۳/۰۱/۰۱-to-Esfand fiscal year.
- Obtain an issuer-verified periodic/annual sample for at least one company with a non-Farvardin fiscal-year boundary, if such a company is in the V1 target set.
- Inspect at least one official source that documents an actual fiscal-year change, or explicitly record that transition-year behavior is not yet evidenced by the available V1 company set.
- Establish which CODAL/company metadata fields, official annual statements, and company notices are accessible and reliable enough to be admitted as source evidence.
- Resolve Migration 9 lineage before drafting a migration sequence.
- Reconcile legacy `Company.fiscal_year_end` and `FinancialPeriod` values against source evidence before any conversion. Do not bulk-convert legacy Gregorian SQL Date values by assumption.

## 8. Decision outcome

**Accepted design direction:** model exact, company-specific, evidence-backed fiscal-year instances with historical immutability and explicit transition years. A single mutable company-level fiscal-year-end string is insufficient as the authoritative historical calendar.

**Not decided by this audit:** exact physical table/column names, whether to introduce a separate calendar-definition/version parent, FK placement, fiscal-year label convention, and migration mechanics. Those require the remaining source and Migration 9 evidence.

**No implementation authorization:** this audit changes no ORM, migration, runtime code, database rows, workbook, or tests.
