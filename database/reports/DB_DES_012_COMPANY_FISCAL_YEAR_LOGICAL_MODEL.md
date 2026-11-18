# DB-DES-012 — Company Fiscal Year Logical Model

**Status:** LOGICAL DESIGN PROPOSAL — recommended model defined; source and migration gates remain open  
**Date:** 2026-11-18  
**Mode:** Documentation only. No ORM, migration, runtime code, database, workbook, or test changes.  
**Depends on:** Architecture V1.3, DB-DES-003, DB-DES-009, DB-DES-011, DB-AUD-002, DB-AUD-016, DB-AUD-017

## 1. Decision summary

Use **one explicit record for each actual fiscal-year interval of a company**, with exact Jalali start and end dates and evidence-backed approval. Do not model the authoritative calendar as a single mutable company field such as Company.fiscal_year_end, and do not assume that one recurring month/day rule covers every historical year.

A fiscal-year change is represented by new actual fiscal-year intervals, including an explicitly evidenced short/long transition year where applicable. Previously approved fiscal-year records are not silently rewritten.

This is a logical target, not an ORM or migration instruction. Migration 9 and source evidence remain implementation gates.

## 2. Why one record per actual fiscal year

The evidence audit DB-AUD-017 found:
- one owner-confirmed company-specific example (Bank Saderat) with a Farvardin-to-Esfand year;
- several workbooks with explicit YTD wording but no printed fiscal-year start date;
- a workbook with unresolved issuer identity;
- no evidence sufficient to establish one universal pattern or a full history of company fiscal-year changes.

A reusable rule such as “month 1 through month 12” would encode assumptions not supported for every company/year. A single current fiscal_year_end value cannot explain historical years or transition years. Actual fiscal-year instances are therefore the smallest reliable source of truth.

## 3. Logical entities

### 3.1 CompanyFiscalYear

One record represents one actual fiscal year for one verified company.

Required logical attributes:
- stable fiscal-year record identity;
- company_id;
- source/company fiscal-year label (fiscal_year_label), preserved as a label and not used as a substitute for dates;
- exact start_jalali_year, start_jalali_month, start_jalali_day;
- exact end_jalali_year, end_jalali_month, end_jalali_day;
- approval state (at minimum: candidate/unverified versus approved);
- source/evidence linkage;
- recorded/approved timestamp.

Optional operational attributes:
- supersedes_fiscal_year_id for an explicit correction/replacement of a previously registered boundary;
- concise correction reason;
- source-issued fiscal-year label when it differs from the application's canonical label.

The logical identity is the company plus the exact start and end Jalali dates. The label is descriptive and may be retained for source matching. Do not use only the Jalali end year as the unique identity.

### 3.2 Fiscal-year evidence

A fiscal-year record must have at least one attributable evidence item before approval. Evidence may include:
- official CODAL report/disclosure;
- official company notice/resolution about the fiscal year or its change;
- owner-confirmed company-specific calendar, tied to a reviewed source.

Logical evidence attributes:
- evidence type;
- source system and source reference (e.g. CODAL tracking identifier where available);
- source URL/reference;
- source publication/effective date where available;
- source artifact fingerprint when the exact source artifact was reviewed;
- verification/approval state and timestamp.

One fiscal-year record may have multiple evidence items. Do not archive the workbook or PDF merely to retain evidence linkage; keep source references and integrity metadata according to the existing artifact policy. If a source is an existing ReportVersion, link it where the final physical model can do so without forcing every notice into the financial-report entity.

### 3.3 Relationship to FinancialPeriod

FinancialPeriod continues to represent the actual interval described by a particular source value. It may resolve to one CompanyFiscalYear when the company and actual dates fit that fiscal year.

Recommended relationship:
- FinancialPeriod has an optional reference to the approved CompanyFiscalYear record during transition/legacy compatibility.
- A FinancialPeriod used to assert duration_basis=YTD must resolve to an approved fiscal-year record.
- A period assigned a fiscal_year or fiscal_quarter must be consistent with the referenced approved fiscal-year record and the source evidence.
- A duration interval classified as a quarter/month must be contained within the relevant fiscal-year interval. An interval that crosses a fiscal-year boundary is not forced into one year; it requires an explicit supported classification or rejection.
- INSTANT observations can be classified against the fiscal year containing their observation date when needed, but the balance date itself remains the period identity.

The final FK shape and whether a direct FK or deterministic service resolution is used are physical design questions for the later ORM proposal. The approved calendar record used for interpretation must nevertheless be identifiable and auditable.

## 4. Immutability, corrections, and fiscal-year changes

Distinguish three cases:

1. **Normal next fiscal year:** create a new CompanyFiscalYear record with its exact dates and evidence. Do not copy dates by adding 12 months unless the source/approved calendar establishes them.
2. **Actual company fiscal-year change:** create an explicitly bounded transition fiscal year, which may be shorter or longer than 12 months, followed by the new fiscal-year sequence. Preserve all prior years unchanged.
3. **Correction of a previously registered boundary:** do not update the approved record in place. Create a replacement/superseding record, retain the previous record and its evidence, and make the correction reason and source publication/effective date traceable.

Approval is company-specific and interval-specific. Approval for one company or one fiscal year does not authorize another company or another year.

A repeated pattern may be used as a validation expectation only after multiple actual years have been evidenced. It must not silently generate missing historical or future fiscal-year records.

## 5. Deterministic assignment and validation

- A company must be resolved and verified before assigning a fiscal-year record.
- The fiscal-year start and end must be exact valid Jalali dates, with start <= end.
- Overlapping approved fiscal years for the same company are prohibited unless a separately approved exceptional model explicitly represents the overlap; V1 should reject such a conflict.
- Gaps between consecutive fiscal years are not automatically filled. A gap requires source reconciliation; it may represent missing evidence or a genuine transition.
- A short/long year is valid only when explicitly supported by evidence.
- fiscal_year_label does not determine exact dates. Preserve the source label and do not infer boundaries from the label.
- A fiscal quarter is assigned only when exact dates and the approved company calendar establish it. Do not assume that every fiscal year can be divided into four equal three-month quarters, especially in a transition year.
- YTD is valid only if the FinancialFact is DURATION, its source semantics establish accumulation, and its actual start date equals the approved fiscal-year start date.
- STANDALONE must retain the actual source start/end dates and must not be rewritten to begin at the fiscal-year start.
- A conflict between an approved calendar and explicit report dates blocks the report; do not silently alter the calendar or the fact.
- If issuer identity, calendar evidence, or date boundaries are unresolved, fiscal classification remains unresolved and the all-or-nothing report admission rule applies.

## 6. Why not store only a recurring fiscal-calendar rule?

A recurring rule (e.g. start month/day and end month/day) may be useful as a derived validation profile after multiple actual years have been evidenced. It is not sufficient as the authoritative historical record because:
- the company may change its year-end;
- the change may create a short or long transition year;
- a one-off extension or shortened year may be approved;
- historical reports may require a corrected boundary with a traceable publication/effective date;
- the company may have gaps in source evidence.

V1 should store actual fiscal-year instances first. A separate recurring calendar-definition/version entity is deferred unless real source requirements prove it necessary.

## 7. Legacy compatibility and migration restrictions

- Company.fiscal_year_end is a legacy scalar and is not authoritative for historical assignment. Keep it unchanged until all readers/writers and existing values have been audited.
- Existing FinancialPeriod.start_date / end_date SQL Date values must not be assumed to be Jalali or Gregorian equivalents of Jalali values. No bulk conversion is authorized.
- Existing fiscal_year / fiscal_quarter labels must not be treated as verified calendar records without source evidence.
- Do not backfill CompanyFiscalYear rows from publication dates, report titles, a guessed Farvardin start, or the current fiscal_year_end scalar.
- Resolve Migration 9 lineage and inspect all target databases before drafting a migration.
- Legacy RawFinancialFact and normalized/derived tables remain outside this design and must not be deleted or repurposed.

## 8. Worked examples

### Example A — approved ordinary fiscal year

For the owner-confirmed Bank Saderat sample, a record may be registered for the exact approved fiscal year beginning ۱۴۰۳/۰۱/۰۱ and ending at the end of Esfand ۱۴۰۳. The evidence and owner confirmation must be linked. This record does not create a default for other companies.

### Example B — unknown start date

A monthly report says “از ابتدای سال مالی تا تاریخ ۱۴۰۵/۰۷/۳۰” but no approved CompanyFiscalYear covers that company and year. The pipeline cannot create a YTD FinancialFact with an invented start date. It must request/resolve evidence or reject the report.

### Example C — fiscal-year change

A company formally changes its year-end and the transition period runs for fewer or more than twelve months. Register the exact transition interval from the official notice and statements. Keep the preceding fiscal year unchanged. Assign quarter labels only if the source/calendar explicitly supports them.

## 9. Remaining gates before physical schema

1. Capture and retain the official source supporting the owner-confirmed Bank Saderat ۱۴۰۳ fiscal-year interval.
2. If a non-Farvardin company is in the V1 target population, obtain an issuer-verified sample and its authoritative fiscal-year source. Do not widen the audit to all listed companies without a defined V1 company set.
3. Identify the CODAL source fields/notice types and official company documents that can reliably evidence a fiscal-year change.
4. Resolve Migration 9 and legacy date semantics.
5. Decide whether approved fiscal-year corrections require PIT-effective version selection in addition to immutable superseding records; the default is to preserve source publication/effective dates and never retroactively rewrite prior analytical results without an explicit version rule.

## 10. Outcome

**Recommended logical model:** CompanyFiscalYear actual interval records + attributable evidence; immutable after approval; explicit superseding corrections; explicit transition fiscal years; optional FinancialPeriod relationship resolved under company/date consistency.

This design is sufficient to guide the later physical schema proposal, but not to start ORM/migration work. The source-evidence and Migration 9 gates above remain open.

No ORM, migration, runtime code, database row, workbook, or test was changed.
