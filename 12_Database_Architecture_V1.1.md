# Analyzer V1 — Database Architecture V1.3

## Status

**UNDER REVIEW — DATABASE CONTRACT V1.3 (REOPENED FOR ARCHITECTURAL REVIEW)**

**Database engine:** SQLite

**ORM:** SQLAlchemy

**Schema migration version:** 8

This document is reopened for review. The decisions explicitly recorded as reviewed/approved below are the current working contract; sections not yet audited remain provisional. Earlier V1 / V1.1 / V1.2 references are historical context and do not override the decisions recorded here. The database stores selected canonical financial inputs and minimal provenance, not raw financial statement rows; backend services own runtime calculations and analytical outputs. This contract supports Stages 2–9 without persisting calculated analytical results.

**Global source-data fidelity rule — applies to every input domain:** Preserve source identity, economic meaning, sign, unit, currency, quote/measurement basis, calendar representation, and publication/observation metadata. Owner numeric-storage decision (2026-11-13) is the sole V1 precision exception: all persisted numeric inputs are stored as SQLite INTEGER after parsing the source numeric text with decimal arithmetic and applying ROUND_HALF_UP to the nearest integer (ties away from zero). Do not use binary floating point. This deliberate loss of fractional precision applies consistently to financial statements, market prices, FX rates, share counts, and corporate-action numeric terms. No other conversion is authorized: in particular, do not convert Toman/Rial, rescale source units, change sign, recalculate, interpolate, replace, or adjust values. Keep source unit/basis metadata explicit; NULL, genuine zero, and ZERO_FALLBACK remain distinct.

---

## 1. Purpose

The database is the auditable Data Foundation. It stores only selected, classified, analysis-relevant financial inputs in canonical form, their minimal source provenance, report/version and period metadata, controlled metric definitions, market/FX/share foundations, and ingestion audit information. It does not retain a general raw financial-line archive. Source rows are classified and mapped at ingestion; irrelevant details are discarded rather than accumulated in the database.

The database must be:

- Point-in-Time correct;
- reproducible;
- source-traceable;
- tolerant of heterogeneous report titles and detail levels;
- safe against silent data loss, silent substitution, look-ahead bias, and aggregate/component double counting.

It is not a replacement for KPI, scoring, trend, forecast, evaluation, valuation, market, or decision engines.

---

## 2. Logical Architecture

```text
External Sources
  ├─ CODAL financial reports (Excel — target input format)
  ├─ Daily market data (CSV / XLSX / …)
  └─ Daily USD FX data — FREE_MARKET & EXCHANGE_CENTER (Toman; CSV / XLSX / …)
          ↓
Format-specific acquisition / extraction adapters
  ├─ CODAL Excel adapter (target adapter; emits the common DTO contract)
  ├─ OHLC parser → MarketDaily fields
  └─ FX parser → FxRateInput[]
          ↓
Common DTO boundary
          ↓
Core Ingestion (service.py)
  + IngestionRun audit
          ↓
Ingestion-time classification and mapping
  ├─ persist selected canonical financial inputs + minimal provenance
  └─ discard irrelevant / unneeded source rows
          ↓
Backend runtime calculations and analysis
          ↓
Stages 2–9 consume runtime results; calculated outputs are not persisted
```

Market and FX foundations remain separate branches and are consumed by their appropriate downstream stages.

**Persistence principle:** do not persist raw financial rows. Resolve each candidate source item at ingestion into a required canonical metric, a simple OTHER_* bucket, or an explicit discard/reject outcome. Persist only the selected canonical input value and minimal provenance. Do not persist redundant totals or system-generated calculations. See the financial fact policy in Section 3.

## 3. Core Domains

### Initial shared-core scope — owner decision (2026-11-14)

V1 will establish a shared, extensible database core before every industry-specific input standard is fully known. The core is expanded incrementally from real, reviewed source examples. Incomplete industry standards do not block core design; however, unknown or unapproved data must not be ingested by guessing.

The initial **logical domains** are:

| Logical domain | Responsibility in the initial core |
|---|---|
| Industry | Controlled industry catalog; initial seven industries, extensible without reusing existing codes |
| Company | Stable company identity and mandatory link to exactly one industry |
| ReportType | The two approved CODAL report families |
| Report | Logical identity of a company's report |
| ReportVersion | Each distinct publication/version, including independent audit and restatement attributes, publication identity and provenance |
| FinancialPeriod | Actual Jalali period described by each fact |
| FinancialFact | Canonical persisted financial input linked to company, report version, period, metric and applicable extraction/mapping standard |
| MarketDaily | Daily OHLC, raw close, adjusted close, volume and traded value |
| ShareCountHistory | Issued-share count history with its own effective date/validity and provenance |
| CorporateAction | Dated, sourced capital events when reliable event data is available |
| FXRate | Daily free-market and exchange-center USD rates; source Toman converted to canonical Rial under the approved FX exception |
| DataDictionary / IndustryStandard | Versioned definitions and mappings for source headers, metrics and input standards; industry-specific content grows incrementally |
| IngestionRun | Operational record of ingestion and validation status, counts, errors and warnings |

This list defines logical scope, **not final physical table names, columns, keys, constraints or a one-domain/one-table mapping**. Physical decomposition is determined during DB-DES design. Some logical domains may require multiple physical tables, and implementation details must preserve their distinct meanings.

The core must support controlled extension: new industries, source headers, metrics and event types are introduced through explicit catalog/standard updates and controlled migrations. Existing identifiers must not be repurposed, and persisted historical data must not be silently rewritten. Industry-specific tables and exhaustive metric catalogs are deferred until supported by real requirements.


### Entity

- `industries`
- `companies`
- `financial_periods`

#### Company and industry contract — reviewed

- Each company belongs to **exactly one industry** in this version.
- Subsidiary-company relationships, multiple industry assignments, and sub-industry classifications are out of scope.
- The seven V1 industry groups remain the initial catalog. The catalog is data-driven and may be extended with additional industry groups without redesigning the schema.
- A company's industry must be explicitly selected and validated before any report or financial data for that company is admitted.
- An absent, unknown, ambiguous, or guessed industry is a hard admission failure. The system must not assign a default or infer an industry.
- Company identity uses the stable internal `company_id`; it must never depend solely on the ticker.
- For V1, the ticker remains a fixed company attribute. A separate ticker-history table is not introduced: the current CODAL ingestion boundary receives an already-resolved `company_id`, so ticker history would add identity/mapping complexity without helping the extraction path. Any future need to support ticker changes must be separately designed around stable `company_id` and must not change historical report ownership.
- The optional national identifier may supplement identity matching but must not replace `company_id`.

The current implementation contains `parent_industry_id`, but parent/child industry classification is not part of the approved V1 contract. Its removal or migration treatment must be handled during schema implementation review, not by silently assigning sub-industries.

### Company master information — V1 scope confirmed by owner (2026-11-13)

The V1 company master information is limited to exactly these four items:

- `company_id`: unique stable internal company identifier generated by the system; it is not derived solely from the ticker.
- `company_name`: official company name.
- `ticker`: stock-market symbol; treated as fixed in V1.
- `industry_id`: mandatory reference to exactly one approved industry.

No additional company master attributes (including company type, active/inactive status, or national identifier) are included in this confirmed V1 list. This is a logical information decision only; physical columns, constraints, and implementation details remain deferred.


### Shared V1 master data — all industries

The following logical master data and report-control entities are shared by all seven industries. They belong in one SQLite database and one common schema; V1 must not create a separate database or duplicate table family for each industry.

#### Industry and company catalogs

- Industry: stable internal ID, unique immutable code, display name, and active/inactive status. Initial catalog: BANK — banking; INVESTMENT — investment; PETROCHEMICAL — petrochemical; METALS — metals; CEMENT — cement; FOOD — food; PHARMACEUTICAL — pharmaceuticals. The catalog is data-driven and extensible; codes are not recycled for a different meaning.
- Company: exactly four V1 master attributes — stable system-generated company_id, official company_name, ticker, and mandatory industry_id. Each company has exactly one industry assignment. No company_type, status, national-identifier field, or ticker-history table is included in the confirmed V1 company master list.
- A separate company_type field is not part of the V1 master contract because it would duplicate the industry classification. Add a distinct attribute only if a later requirement establishes a different meaning.

#### Shared CODAL report-type catalog

The common CODAL financial-report catalog contains exactly two report types across all industries:

| Code | Meaning |
|---|---|
| MONTHLY_ACTIVITY | Monthly activity / sales report |
| PERIODIC_FINANCIAL | Fiscal-year periodic financial report |

The extraction standard and accepted financial items may differ by industry and report type; the report-type identity itself is shared. Three-, six-, nine-, and twelve-month periods are not separate report types. YTD versus standalone describes the temporal meaning of values/columns inside a report, not a third report type.

#### Common report, period, provenance, and ingestion entities

- Report: logical identity of a company's report, linked to the company and one of the shared report types.
- ReportVersion: one distinct published source version of a logical report. It retains source identity/reference, valid publication time where available, and audit/restatement status as independent attributes. Earlier valid versions remain immutable and available for PIT selection.
- FinancialPeriod: the actual Jalali start/end period described by a source value, with fiscal-year/quarter and temporal attributes such as duration and YTD/standalone. Period identity is not inferred from filename or publication date; one report may contain multiple comparative periods.
- Source provenance: retain the source reference/identifier and a source artifact fingerprint or equivalent version identity. Workbook archival and permanent per-fact cell coordinates are not required.
- IngestionRun: operational processing status, timestamps, counts, and concise errors/warnings. A failed run must not leave partial report or financial-input persistence.

#### Shared foundation versus industry-specific standards

These entities are common infrastructure, not a claim that all industries publish identical report layouts or financial items. Industry-specific workbook layouts, source headers, mapping rules, extraction standards, and eligible financial items remain separate standards associated with the relevant industry and report type.

Do not predefine one universal metric catalog for all industries before reviewing real source examples. A metric may be shared only when its financial meaning is genuinely identical; otherwise it requires a distinct canonical identity. This section records the logical contract only and does not authorize ORM, schema, migration, data, or code changes.


### Final shared master-information taxonomy — owner-confirmed (2026-11-13)

The following nine categories are the final V1 taxonomy for shared master and operational-control information across all seven industries:

| # | Information category | Contract |
|---|---|---|
| 1 | Database | One shared SQLite database for all industries |
| 2 | Industries | Seven-industry catalog with ID, code, name, and status |
| 3 | Companies | Company identity and mandatory assignment to exactly one industry |
| 4 | Report types | The two shared CODAL types: monthly activity and periodic financial |
| 5 | Report | Logical identity of a company's report and report type |
| 6 | Report version | Each valid publication, including independent audit/restatement status and source identity |
| 7 | Financial period | Actual Jalali period and temporal attributes of the period/values |
| 8 | Information provenance | Source reference/identifier and source-artifact fingerprint |
| 9 | Ingestion run | Processing status, timestamps, counts, errors, and warnings |

This taxonomy is final for shared master and operational-control information in V1. No additional category is to be added to this list without a subsequent explicit owner decision.

The database itself is the shared storage container, not a data table. The nine categories do not imply nine physical tables; table boundaries and relationships are determined by logical and physical schema design.

Persisted financial facts, industry-specific extraction standards, and independent market/FX input domains are specialized input content/contracts, not additional categories in this shared master-information taxonomy. They remain governed by their respective architecture sections and tasks.

This is a documentation-level taxonomy decision only. It does not authorize code, ORM, schema, migration, or data changes.

### Periodic report category catalog — initial bank scope

The following 17 categories are the initial category catalog identified for periodic bank reports, based on the Parsian Bank sample structure. They define the report-information categories to be represented by the database architecture; they are not a claim that every industry uses the same categories.

1. صورت سود و زیان
2. صورت سود و زیان جامع
3. صورت وضعیت مالی
4. صورت تغییرات در حقوق مالکانه
5. صورت جریان‌های نقدی
6. مانده تسهیلات اعطایی و ذخیره مطالبات مشکوک‌الوصول
7. مانده سپرده‌های دریافتی از مشتریان
8. اقلام زیر خط
9. اطلاعات حق‌الوکاله و کفایت سرمایه
10. درآمد حاصل از تسهیلات اعطایی و سپرده‌گذاری
11. خالص سود (زیان) سرمایه‌گذاری‌ها
12. سایر درآمدها و هزینه‌های عملیاتی
13. خالص سایر درآمدها و هزینه‌ها
14. هزینه‌های اداری و عمومی
15. هزینه مالی
16. برنامه شرکت در خصوص تقسیم سود
17. وضعیت شرکت‌های سرمایه‌پذیر

This is a logical category list only. Physical database tables, field-level layouts, extraction rules, and other industry-specific category catalogs are outside the scope of this recorded decision.

### FinancialPeriod — reviewed and approved contract

A financial period describes the actual source reporting span, using Jalali calendar components. Do not use SQL/Gregorian `Date` fields as the authoritative financial-period dates.

Required date components:

- `start_jalali_year`, `start_jalali_month`, `start_jalali_day`
- `end_jalali_year`, `end_jalali_month`, `end_jalali_day`

Retain and define these period attributes:

- `fiscal_year`: the company's fiscal-year label, resolved from its actual fiscal calendar and source; do not assume it is always Farvardin-starting.
- `fiscal_quarter`: nullable where not applicable; otherwise an integer from 1 through 4.
- `period_type`: describes the duration/span of the source data, not how often the report is published.
- `months_length`: number of months represented by the source period.
- `is_ytd`: whether the source amount is cumulative from the start of that company's fiscal year.

The actual start of a fiscal year/period must be resolved from the source or a validated company fiscal calendar. Never infer Farvardin 1 or another start date from a market-wide convention.

For the usual cumulative quarterly filing pattern:

| Fiscal quarter | Source period type | months_length | is_ytd |
|---|---|---:|---|
| Q1 | `QUARTER` | 3 | true |
| Q2 | `SEMI_ANNUAL` | 6 | true |
| Q3 | `NINE_MONTH` | 9 | true |
| Q4 | `ANNUAL` | 12 | true |

Monthly source periods use `MONTH`, `months_length=1`, and `is_ytd=false`.

Standalone-quarter figures calculated from cumulative source periods are derived analytical results, not database inputs. This database architecture defines no standalone-quarter field, column, table, or stored record. The database retains the source-reported cumulative values and their source-period metadata exactly as admitted under the input/provenance rules. Any quarter-differencing logic belongs to the runtime analytical layer and is outside this database storage contract.
`TTM` is not a source `FinancialPeriod` type. TTM is a derived analytical window and is computed at runtime.

The logical period identity is the company plus the exact Jalali start date and end date. Enforce valid Jalali components, start date not after end date, quarter range 1–4, and consistency between dates, duration, period type, and YTD semantics. Reject unresolved or contradictory period metadata rather than guessing.

**Migration caution:** existing SQL `Date` values must be inspected before migration. Do not assume they represent Gregorian dates or Jalali dates and do not blindly convert them. Ambiguous/unresolvable records require an explicit migration report and safe resolution path.

### Report / ReportVersion / PIT

- `reports`
- `report_versions`

**Report identity and scope**

- `Report` identifies one logical company filing/disclosure, not an individual financial metric, statement line, or one of the report-information categories listed above.
- The report's classification must preserve the existing report types (monthly and periodic) and the applicable industry-specific report category. This metadata must not create, remove, merge, or split the approved report categories.
- A logical report must be tied to one company and its declared reporting period. Its identity must use a stable source identifier when the source provides one. If no stable source identifier exists, use a validated composite identity based on company, report classification/category, and the declared reporting period; titles alone are not a reliable identity.
- A different reporting period is a different logical report. A correction or restatement of the same filing is not a new logical report; it is a new version of that report.

**Report versions**

- `ReportVersion` identifies one published state/snapshot of its parent `Report`. Every version belongs to exactly one logical report.
- Publication datetime belongs to `ReportVersion`, not to `Report`. Preserve the source publication timestamp and any source version/revision identifier when available.
- Each version is an immutable source snapshot. A later correction must create a new version; it must never overwrite or delete an earlier version.
- A version must not silently change the parent report's company, report classification/category, or declared reporting period. If those identity attributes conflict, treat the source as a separate report or reject/quarantine it until its identity is resolved.

**ReportVersion metadata contract — logical requirements**

Each version must preserve the following information. This is a logical contract, not a physical column layout; exact schema and storage types are deferred to implementation.

1. **Version identity and source reference**
   - Parent logical `report_id`.
   - Stable CODAL/source version or revision identifier, when supplied.
   - Original source document reference (such as the CODAL filing/document identifier or URL) when available.
   - A content fingerprint (for example, a cryptographic hash of the acquired source file) to support duplicate detection and prove which exact source artifact was ingested. A fingerprint supplements source identity; it does not replace a stable source identifier.
2. **Publication and ingestion timing**
   - Source publication datetime, including its original source representation and a normalized timestamp suitable for deterministic PIT comparison.
   - If publication datetime is absent, ambiguous, or cannot be reliably normalized, retain the source evidence but mark the version's PIT availability as unresolved. Do not substitute ingestion time, file-download time, report period end, or a guessed date for publication time; the version must not be selected for a PIT analysis until its publication time is resolved.
   - Ingestion/capture datetime belongs to ingestion audit metadata (for example, `IngestionRun`), not as a substitute for the source publication datetime.
3. **Audit classification**
   - Normalized `audit_status`: `AUDITED`, `UNAUDITED`, or `UNKNOWN`.
   - Preserve the exact original CODAL wording/code and the source evidence used for classification. Exact worksheet/cell coordinates may be used transiently when useful, but are not required as permanently stored per-fact provenance. Do not infer the status from the report title or another version.
4. **Original/restated classification**
   - Normalized `revision_status`: `ORIGINAL`, `RESTATED`, or `UNKNOWN`.
   - Preserve the exact original CODAL wording/code and the source evidence used for classification. Exact worksheet/cell coordinates may be used transiently when useful, but are not required as permanently stored per-fact provenance. Do not infer restatement merely because a version is newer or because its values differ.
5. **Classification confidence and unresolved states**
   - A normalized status may be assigned only when the source evidence supports an unambiguous mapping. Otherwise retain `UNKNOWN` and the original source label/evidence.
   - The source label must not be discarded after normalization. This permits later correction of a mapping without losing what CODAL actually supplied.
   - Do not assume that a CODAL letter/code (including C or D) has a fixed meaning unless its meaning is established by authoritative source documentation or validated source metadata for that filing.

**Version identity and duplicate handling**

- Prefer the source's stable report-version/revision identifier to identify a published version.
- If no stable version identifier exists, use a deterministic identity based on the parent report and the exact acquired source artifact fingerprint; retain publication datetime and original source reference as supporting evidence.
- If the same version is downloaded or ingested again, recognize it as the same version and process it idempotently. If two different artifacts claim the same source version identifier, do not overwrite either silently; flag the conflict for resolution.
- A changed content fingerprint without a source revision identifier is evidence of a potentially distinct source snapshot, not permission to overwrite an existing version. Resolve whether it is a new published version or a source replacement before admitting it as a new version.
- Do not use a locally assigned ingestion sequence as evidence of CODAL publication order.

**Ingestion versus analytical version selection**

- Ingestion must preserve every distinct, validly identified published version of a logical report, including original, corrected/restated, audited, and unaudited versions. The preference rules below must never be used to discard a valid source version during ingestion.
- Each version's selected canonical facts must remain linked to that exact immutable `ReportVersion`; facts from different versions must not be merged into one indistinguishable set or overwrite one another.
- Re-ingestion of the same source version must be idempotent: it may update ingestion audit state where appropriate, but must not create duplicate canonical facts or mutate the already captured source snapshot.
- Version selection is an analytical operation performed after ingestion. For a requested PIT cutoff, the selector considers only versions published on or before that cutoff, then applies the approved audit/restatement preference. The selector must return the chosen version and enough selection metadata to explain why it was chosen.
- If the selector cannot identify a version under the approved preference rules, it must return an explicit unresolved state; it must not silently fall back to whichever version happens to be latest or currently marked current.
- A newer version becoming preferred for a later analysis must not change the version or facts selected for an earlier PIT cutoff.
- Select one `ReportVersion` for each logical `Report` at the requested PIT cutoff and apply that selection consistently to all facts sourced from that report version. Do not select different versions of the same report independently for different metrics or line items.
- Do not fill a missing metric or line item in the selected version by silently borrowing it from another version of the same report. Preserve the missing/unavailable state; any future cross-version supplementation would require a separately defined and auditable policy.
- This report-level rule does not prevent an analysis from using different selected versions for different logical reports (for example, distinct reporting periods or report categories). Each logical report is selected independently under the same PIT and preference rules.

**Financial-period linkage and comparative data**

- A `Report` has one declared primary reporting period, represented by `FinancialPeriod`.
- Each persisted financial fact must link to the exact `ReportVersion` from which it was extracted and to the `FinancialPeriod` that the particular value actually describes.
- A single report version may contain values for more than one financial period, for example current-period and comparative prior-period figures. Those values remain attached to the same source `ReportVersion`, but each fact links to its own applicable `FinancialPeriod`. Do not force all facts in a filing into the report's primary period.
- The published company report is the authoritative financial source. Application calculations must not challenge, overwrite, or silently correct a value explicitly reported by the company.

**Comparative-period data contract**

- A value shown in a comparative column or comparative section is a fact reported by the current `ReportVersion`; it is not a fact from the earlier report version that originally reported that period.
- Store each comparative value against (a) the exact `ReportVersion` that contains it and (b) the `FinancialPeriod` it actually describes. Its availability for PIT analysis begins at the publication datetime of the containing `ReportVersion`, not at the end date of the comparative financial period.
- Preserve the distinction between the report's primary-period facts and comparative-period facts. Record the source-indicated period context (at minimum: `PRIMARY`, `COMPARATIVE`, or `UNKNOWN`) where it cannot be derived unambiguously from the report's primary period and source structure. Do not guess the period context.
- Comparative values must not overwrite, merge with, or be relabeled as primary-period facts from a separate logical report. Preserve both source observations and their separate provenance, even when they describe the same metric and financial period.
- By default, the selected version of the logical report whose primary period is being analyzed supplies that period's canonical analytical inputs. Comparative disclosures in another report are retained as separately attributable comparative observations; they are not silently substituted for or used to fill missing primary-period values.
- If a later filing presents a comparative value as restated, preserve that value and the containing version's audit/restatement metadata. It does not automatically revise the earlier period's canonical inputs. Any future policy that elects to use such a comparative restatement as the analytical value for the earlier period must explicitly define source precedence, PIT behavior, and conflict handling before implementation.
- When primary and comparative observations exist for the same metric and period, do not count both as separate economic amounts. They are alternative source observations for comparison/validation, not additive facts.
- Comparisons are valid only when metric meaning, unit, dimensions, currency, and period basis (including YTD versus standalone period) are compatible. If they differ or cannot be established, do not reconcile or compare them automatically.
- Conflicting primary and comparative values must both remain traceable. Do not average, overwrite, or silently choose one to conceal a discrepancy.

**Point-in-time selection**

- When the company publishes a correction or revised version of the same report, that newer version takes precedence only for analyses whose PIT cutoff includes the correction's publication datetime.
- Earlier versions remain preserved and must continue to be selected for PIT cutoffs before the correction became available.
- A later correction must never be retroactively applied to an earlier PIT snapshot. Version selection must be deterministic and based on publication availability at the requested cutoff; do not select a version merely because it is currently the latest.

**Audited / restated version preference**

- Preserve audit status and presentation/restatement status as separate, source-supported attributes of each `ReportVersion`. Retain the original CODAL labels or source evidence needed to explain how those attributes were classified.
- For analysis, the preferred version is one that is both **audited** and **restated**.
- If no audited-and-restated version is available within the requested PIT cutoff, the approved fallback is an **unaudited, original (not restated)** version.
- Within the applicable preferred or fallback class, select the latest version published on or before the PIT cutoff. Never use a version published after the cutoff.
- Do not infer audit or restatement status from the report title, publication order, or another version. If the source does not establish the status reliably, keep it unknown.
- The preference above does not define an ordering for mixed or otherwise unclassified combinations (for example, audited-original or unaudited-restated) when neither approved combination is available. Do not silently promote one of those combinations to the preferred/fallback position; flag the selection as unresolved for an explicit policy decision rather than guessing.
- Version preference affects which source version is selected for an analysis; it does not authorize deletion, overwriting, or loss of any published version. PIT history must remain reproducible.

### Financial fact and calculation contract — reviewed and approved

The database does **not** retain raw financial statement rows or a general-purpose raw-fact archive. Every candidate item must be resolved at ingestion. The objective is an analysis-ready financial data foundation, not a reconstruction of each company's accounting ledger or a full copy of its statements.

At ingestion, each candidate item must receive one of these outcomes:

1. **Map to a required canonical metric** when it has clear analytical meaning and is needed by downstream analysis.
2. **Map to a simple, controlled OTHER_* bucket** when it is a genuine financial amount but its detailed accounting breakdown is not needed. Examples include OTHER_INCOME, OTHER_EXPENSE, and, if required by analysis, a similarly simple bucket for miscellaneous asset disposals. The bucket catalog should remain small and understandable; do not create a separate metric for every incidental disclosure.
3. **Discard** a source row that has no analytical use and is not needed for minimal provenance or audit.
4. **Reject or quarantine before financial persistence** when a required identity, metric meaning, unit, period, or source attribution cannot be resolved safely. Do not guess.

**Source-input fidelity and persistence boundary**

The persisted financial amount/quantity/rate must retain the source meaning, sign, and unit/basis. Under the owner-approved V1 numeric policy, fractional precision is rounded once to an integer with ROUND_HALF_UP during ingestion; no other numeric transformation or manufactured replacement is permitted.

- Persisted supporting metadata must follow the owner's minimum-provenance decision: company identity, report type and logical report/report-version identity, actual financial period, canonical metric identity, extraction-standard version, source-provided unit/currency and measure semantics, meaningful source dimensions, and source publication metadata. For market/FX/share/corporate-action inputs, retain source identity, observation/effective date, and domain-specific interpretation metadata. The source artifact reference and content fingerprint are retained at the ReportVersion level as defined by the ReportVersion identity contract, to identify the immutable published snapshot and support deterministic version identity/idempotency; they are not copied onto every fact. This does not require archiving the Excel file or attaching exact cell coordinates to every fact. Exact workbook/sheet/row/cell coordinates may be used transiently for extraction, mapping, debugging, or standard development, but are not generally required as permanently stored per-fact provenance.
- Assigning a controlled canonical metric identifier is classification metadata. It must not change the source meaning, sign, or unit/currency, recalculate it, or replace its original meaning. The one permitted precision change is the owner-approved ROUND_HALF_UP conversion to SQLite INTEGER; no other rounding or rescaling is permitted. If the source unit or meaning cannot be mapped without guessing, do not persist the financial input until the mapping is resolved.
- Source labels, extracted cell text, parser/adapter DTOs, intermediate extraction structures, debug artifacts, confidence scores, and application-generated reconciliation or calculation values are transient processing material, not additional financial inputs; do not persist them as financial data or as a general raw-data archive.
- Do not persist a second copy of a source value in a raw table alongside its selected financial-input record. The selected input record and its minimal provenance are the sole persisted representation of that accepted financial input.
- Technical schema-management metadata and the minimal ingestion audit record are operational controls, not financial inputs. They must not contain copied source rows, extracted financial values, or analytical results.

**Source and period integrity for persisted financial facts**

- Every persisted financial fact belongs to exactly one `ReportVersion`; it must never be linked only to the logical `Report` while leaving its source version ambiguous.
- Every persisted financial fact belongs to exactly one `FinancialPeriod`, identifying the period the value actually describes. This may be the report's primary period or a comparative period included in the same filing.
- The fact's `ReportVersion`, its parent `Report`, and its `FinancialPeriod` must resolve to the same company. A cross-company link is invalid and must be rejected.
- The fact's period must be supported by the source filing. A comparative prior-period value must link to the corresponding prior-period record; the system must not assign the current report period merely because it is the primary period.
- The source item must be attributable to its specific ReportVersion and the applicable extraction-standard version. Exact workbook/sheet/row/cell coordinates may help identify and validate an item during extraction, but they are not mandatory permanently stored locators for each canonical fact. A transient locator must never be reused across different source versions.
- Re-ingestion of the same immutable ReportVersion under the same extraction-standard version must be idempotent. Identify accepted inputs using report-version identity together with canonical metric, financial period, unit/measure semantics, meaningful dimensions, and any additional stable source identity available under the approved contract. Numeric equality alone is never a duplicate key. If available identity cannot distinguish repeated observations safely, resolve the ambiguity during extraction or reject the affected report rather than guessing.
- Do not identify duplicates by numeric equality alone. Equal amounts may describe different products, segments, periods, dimensions, or independently reported observations.
- If the same metric, period, unit, and dimensions appear more than once within one report version, do not silently merge, overwrite, discard, or add the observations merely because their values are equal. Determine from report structure and the extraction standard whether they are repeated presentations of one amount or distinct economic inputs. If their identity or analytical relationship cannot be resolved, ask for clarification or reject the report; do not invent a permanent locator or persist ambiguous duplicates.
- If re-ingestion of the same immutable report version and extraction-standard version yields a different value or incompatible metadata for an already identified canonical input, treat it as a source/extraction conflict. Do not overwrite the stored input; resolve whether the source version, extraction standard, or prior ingestion identity is wrong before admitting a changed snapshot.
- Do not impose a simplistic uniqueness rule on metric + period alone where the source legitimately reports multiple products, segments, or other dimensions.
- A fact whose report version, company, report type, financial period, canonical metric, extraction-standard version, unit, or other required interpretation metadata cannot be validated must not be persisted. An exact cell/row locator is not a general admission requirement. Ingestion must not leave partial report/version/fact writes when validation fails.

Additional rules:

- Persist independently meaningful inputs required for analysis, such as production quantity, sales quantity, selling rate, cost inputs, and other selected canonical measures, only after their meaning, unit, period, and provenance are resolved.
- Do not persist a total/subtotal when it is reproducible from sufficient validated inputs using a known, explicitly defined calculation rule. The backend computes it when needed.
- A reported aggregate that is not required as a distinct analytical input may be mapped into the relevant OTHER_* bucket rather than retained as a separate raw row. This includes an amount reported only as one figure, such as a miscellaneous asset sale, other income, or other expense. Preserve the useful amount in the simple bucket; do not preserve its raw accounting detail.
- When both components and an aggregate are present, avoid double counting. Use the components for metrics that require them; map only genuinely non-overlapping residual items to an OTHER_* bucket. Never add a total to its own components.
- Do not infer formulas from labels or visual proximity. A derived value may be calculated only when its formula/relationship is known and all required inputs are available and valid.
- Do not substitute one measure for another. For example, production quantity is not sales quantity.
- The published company report is the source of truth for reported financial values. The application is responsible for faithfully extracting, classifying, and storing those values; it must not independently judge or revise a reported financial figure based on its own arithmetic. Corrections are recognized through a newer published report version, not by changing the earlier version.
- **Product sales amount resolution (Master Packet Section 3.5 governs):** a valid amount explicitly reported by the source is authoritative and must be persisted as a canonical input, even if it differs from quantity × selling rate. If the reported amount is blank or unusable and quantity plus selling rate are both present, valid, and compatible in unit and period, their product may be calculated at runtime only and must not be persisted as a reported/source input. If the reported amount is blank/unusable and either quantity or selling rate is missing, invalid, or incompatible, the narrowly approved ZERO_FALLBACK resolves the product sales amount to zero, is stored with a distinct value origin/state, and produces an ingestion warning. This exception applies only to product sales amount.
- A blank or unusable source-reported product sales amount is not replaced by a persisted quantity × rate calculation. When both quantity and rate are valid and compatible, the amount remains NULL as a source input and the product is runtime-only. When either required input is missing, invalid, or incompatible, Section 3.5 permits only the distinct ZERO_FALLBACK state for this product-sales-amount metric, with a stored zero and ingestion warning. No other metric may use this fallback.
- An explicit, valid source-reported zero is stored as zero because that is what the source reported. It must not be replaced by quantity × rate.
- Do not infer missing inputs, totals, quantities, rates, units, periods, or labels.
- Persisted financial values must retain source meaning, sign, unit/basis, and report-version identity. The only permitted numeric precision change is the owner-approved one-time ROUND_HALF_UP integer conversion; do not recalculate, rebalance, fill blanks, replace values, or otherwise alter the economic meaning. A new published correction/restatement is a separate immutable report version; it does not authorize editing the previously ingested version.
- Calculated values are runtime-only. They must not be inserted into financial-input, normalized, derived, cache, or history tables.
- Keep only the owner's approved minimum provenance with each persisted canonical input: company identity, report type and logical report/report-version identity, actual financial period, canonical metric identity, and extraction-standard version. Preserve source publication metadata through the report version. Do not archive the Excel workbook or retain raw rows, unused source values, or exact cell coordinates as mandatory per-fact fields. Operational metadata such as IngestionRun identity, validation status, and error/warning summaries may be retained where useful.
- Runtime calculation results must retain enough in-memory lineage to explain their inputs and formula where auditability requires it, but this does not authorize persistence of the calculated result.

### Common source-provenance contract for persisted inputs — aligned with owner decision 3.11

Provenance identifies the origin, meaning, and processing standard of a persisted input. It is metadata only and must never alter, normalize, convert, or replace the source-reported value. This section is governed by the owner's explicit minimum-provenance decision in Master Packet Section 3.11; it does not impose a permanent exact-cell locator or source-workbook archive.

**Minimum provenance for CODAL financial inputs**

Each persisted canonical financial input must be connectable to, at minimum:

- The validated company identity (company_id).
- The report type/classification and logical Report identity.
- The exact published ReportVersion containing the value, including its source publication metadata and available stable CODAL/source reference.
- The actual FinancialPeriod described by the value, including primary/comparative context where required.
- The canonical metric identity assigned during ingestion.
- The version/identity of the extraction standard used to interpret and map the source report.
- Source-provided unit, currency, measure semantics, and meaningful dimensions needed to interpret the value without changing it.

The report version must preserve the source publication datetime and source version/revision identity when available. The source artifact reference and content fingerprint are retained at the ReportVersion level as defined by the ReportVersion identity contract, to identify the immutable published snapshot and support deterministic version identity/idempotent ingestion. They are not copied onto every fact. This does not require retaining/archiving the Excel workbook.

**Extraction locators are not mandatory persisted fact fields**

- Worksheet names, row/column numbers, cell addresses, ranges, and equivalent source coordinates may be used transiently during extraction, mapping, standard development, validation, or debugging when operationally useful.
- Under the owner's Section 3.11 decision, an exact workbook/sheet/cell locator is not a general requirement for permanent storage with every canonical financial input.
- The location of a value in a worksheet or cell does not itself establish the financial meaning of that value. Meaning must be resolved through the approved extraction standard and canonical metric mapping.
- Do not archive the source workbook, raw worksheet rows, copied cell payloads, or unused source values as a workaround for the absence of permanent cell locators.
- Any future requirement for stronger per-value audit location must be presented as a separate owner decision, taking into account that the source workbook is not archived.

**Market, FX, share-count, and corporate-action inputs**

These inputs must retain their validated source identity/reference, source observation or effective date/time in the source's original calendar representation where applicable, the integer-stored numeric value produced by the owner-approved ROUND_HALF_UP rule, and the source unit/basis or event semantics required to interpret it. Source publication/observation time must not be replaced by ingestion time. Exact row/cell/file coordinates may be used transiently where useful, but are not a universal mandatory persisted locator for every observation.

**Operational ingestion audit**

An IngestionRun identifier, processing timestamp, validation status, and concise error/warning information may be retained to support operational control and explain how an ingestion was handled. These operational fields do not substitute for source publication/observation metadata and must not contain copied source rows, raw financial payloads, or calculated analytical outputs.

**Admission, identity, and fidelity**

A persisted input is inadmissible when any required identity or interpretation metadata is missing or ambiguous: company, report type, report/version, actual financial period, canonical metric, extraction-standard version, unit/measure semantics, or relevant source identity/date for non-CODAL inputs. Do not guess these fields. Resolve ambiguity during extraction or reject the affected report/input before analytical persistence. The absence of an exact cell locator alone is not an admission failure.

Source-reported amount, quantity, rate, sign, unit, currency, and measurement basis remain the semantic source of truth; numeric values are stored as integers under the owner-approved ROUND_HALF_UP policy. Provenance metadata must not authorize any other transformation or substitution. The existing raw_financial_facts table is incompatible with this target if it acts as a general raw-row archive. The existing normalized-input model may become the canonical persisted financial fact layer, but it must not duplicate a separate raw-value layer. Existing derived_financial_facts and derived_financial_fact_inputs are incompatible if they persist application-calculated financial values. Their future schema/migration treatment must inspect existing data first and remain non-destructive until a safe migration is designed. Do not write new raw-row archives or calculated results during transition.

### Canonical financial-input contract — DB-DES-001 (logical design)

This section defines the logical target for persisted CODAL financial inputs. It is a design contract, not an ORM or migration instruction. Existing tables are not assumed to satisfy it, and no existing data may be deleted or rewritten merely to make the current schema appear compliant.

**1. Canonical CODAL financial-input record**

The canonical financial fact represents one accepted financial input reported by a company through CODAL. It is not a generic container for every kind of database input. The target is one long-form record per accepted canonical metric, actual financial period, published report version, and approved value-defining dimensions.

Each logical record must be attributable to:

- company identity — the validated company to which the fact belongs. It must agree with the company referenced by the ReportVersion. The physical model may obtain this identity through ReportVersion rather than duplicate it as a stored fact column, provided company consistency is enforced.
- report_version_id — the exact published ReportVersion that contains/publishes the value. Report type/classification is obtained through its parent Report.
- period_id — the actual FinancialPeriod described by this particular value, not a period inferred from the report title, publication date, column position, or another value.
- metric_id — the stable canonical metric identity assigned after approved classification.
- extraction_standard_version — the exact version of the approved extraction/interpretation standard used to produce the canonical input.
- source-reported value, source unit/currency and measurement basis, plus only those approved value-defining dimensions needed to distinguish genuinely separate inputs.
- explicit value state/origin sufficient to distinguish a source-reported value, a known blank/NULL, and the narrowly permitted ZERO_FALLBACK.
- optional operational IngestionRun link for processing audit. It does not replace report publication metadata or required source provenance.

The logical company, report-version, actual-period, metric, and extraction-standard identities are mandatory. A physical implementation need not duplicate an identity already unambiguously reachable through a required relationship, but it must enforce the corresponding consistency invariant.

This record contract applies to CODAL financial facts only. Market prices, FX rates, share-count observations, and corporate actions are separate input domains with their own temporal and source semantics; they must not be forced into FinancialFact. Their logical domains were established in the initial database scope and will be designed under their respective contracts.

Exact worksheet, row, column, cell, or range coordinates are not mandatory persisted fields. Source artifact reference and content fingerprint belong to ReportVersion, not to each fact. The Excel workbook itself and general raw-row payloads are not archived.

**2. FinancialMetric catalog and source-label mapping boundary**

FinancialMetric is a controlled catalog of stable canonical financial input identities. It is not a copy of every source Header, a prebuilt inventory of every possible industry metric, or a store of calculated outputs.

- The catalog is built incrementally. Only metrics whose financial meaning has been sufficiently defined and approved are admitted. Completing all seven industry standards is not a prerequisite for establishing or using the shared database core.
- Each metric has a stable, unique code and a definition precise enough to distinguish economically different measures. For example, a sales amount and a sales quantity are separate metrics even when they appear in the same source table.
- A metric's value kind and interpretation properties must be explicit where relevant, including whether it represents an amount, quantity, rate, ratio, flow, or stock. Applicable unit/currency and measurement-basis expectations must be defined sufficiently to validate interpretation. These properties do not authorize automatic conversion or rescaling.
- The source unit, currency, and measurement basis actually reported remain attached to the accepted fact. The metric definition may specify compatible expectations or validation rules, but must not silently replace the source unit or imply an unapproved canonical conversion.
- Metric identity is independent of report version, financial period, audit/restatement status, source Header wording, and worksheet position. A metric may be used by more than one industry or report family when the underlying economic meaning is genuinely the same; industry/report applicability and source-specific recognition belong to the approved, versioned mapping/standard context.
- Source Header → approved label/standard Header → canonical metric is a controlled, versioned mapping path defined by DB-DES-002 and the relevant report-family/industry standards. Mapping must consider sufficient context (including company industry, report family, table/section, period or column meaning where relevant); matching Header text alone is not proof of equivalent financial meaning.
- A source label that is unknown, ambiguous, or not covered by an approved mapping must not be assigned to the nearest-looking metric. It remains unresolved and is handled by the applicable admission/rejection rules until its meaning and mapping are approved.
- Catalog entries and mapping/standard versions are controlled metadata. A metric must not be silently redefined in place in a way that changes the meaning of previously persisted inputs. A genuinely different meaning requires a new stable metric identity; any compatibility or mapping change must be explicitly versioned and must not reinterpret previously persisted facts silently.

**3. OTHER_* handling**

OTHER_* is an explicit, controlled canonical bucket mechanism for in-scope miscellaneous amounts whose meaning is sufficiently understood to be grouped under an approved broad concept but does not warrant a dedicated metric.

- OTHER_* is not a catch-all for unknown, ambiguous, unmapped, or merely similar-looking source labels.
- A source item may enter an OTHER_* bucket only when its report scope, economic meaning, period, unit, and mapping destination are resolved under an approved standard.
- Items outside the approved extraction scope are discarded from financial persistence; unresolved in-scope items block/reject the report according to the applicable report-family admission rules.
- The exact bucket codes, permitted parent/scope relationships, and mapping policy are deferred to DB-DES-002 and the relevant report standards. This task does not invent an expanded taxonomy.

**4. Value, NULL, and ZERO_FALLBACK semantics**

The canonical layer stores source-selected inputs, not recalculated amounts.

- A usable source-reported value is authoritative as to its financial meaning, sign, and source unit/currency/basis. **Owner numeric-storage decision (2026-11-13): V1 does not require fractional precision; SQLite3 is the target database and persisted numeric inputs use SQLite INTEGER.** During ingestion, parse source numeric text without binary floating point and round to the nearest integer using decimal ROUND_HALF_UP (ties away from zero), then persist the integer. This is an explicit owner-approved precision reduction; it supersedes the earlier requirement to preserve source fractional scale/precision. A reported zero remains distinguishable from a fallback.
- A known blank/unusable source value is NULL/unknown; it must never be silently coerced to zero. If the canonical contract records an expected-but-blank input, its state must explicitly identify it as missing and its value must remain NULL.
- ZERO_FALLBACK is the only approved synthetic-value exception and is restricted to product sales amount under Master Packet Section 3.5. It resolves to numeric zero only under the exact approved conditions and must carry a distinct origin/state plus an ingestion warning. It must not be generalized to other metrics.
- Quantity × selling rate, totals, subtotals, ratios, adjusted values, and all other application calculations remain runtime-only. A runtime calculation must not be persisted as a source-reported or canonical input.
- The current fixed Numeric(30,4) / value_irr shape is not an acceptable target contract: it imposes a four-decimal scale and assumes IRR. The target is a SQLite INTEGER-backed numeric value, with SQLAlchemy mapping and signed 64-bit range validation finalized in DB-MIG-001. Source numeric text must be parsed using decimal arithmetic (never binary float), rounded once at ingestion using ROUND_HALF_UP, and persisted as an integer. Values outside SQLite's signed 64-bit integer range must be rejected rather than wrapped or stored approximately. DB-MIG-001 must add round-trip and boundary tests; this logical decision does not authorize rewriting existing values without a safe migration plan.
- Unit and currency remain explicit source metadata. No automatic Toman/Rial, unit, currency, scale, or sign conversion is authorized.

**5. Uniqueness and duplicate identity**

The logical uniqueness key is:

(report_version_id, period_id, metric_id, approved_dimension_identity)

where the dimension component is empty for a non-dimensional input and represents only approved value-defining dimensions when they are genuinely required. The exact dimension model/key is coordinated with DB-DES-002 and DB-DES-003.

- A ReportVersion may contain the same metric for multiple actual periods, such as comparative columns; those are distinct inputs.
- The same metric and period may appear in different ReportVersions; those are distinct immutable source observations and must be retained.
- If one ReportVersion contains repeated occurrences of the same metric/period, they must not be summed, overwritten, or deduplicated by numeric equality. Their meaning and dimensional identity must be resolved before persistence; otherwise reject the ambiguous report/input.
- Source cell coordinates, raw Header strings, ingestion timestamps, and numeric equality are not substitutes for canonical identity and must not be used as the permanent uniqueness key.
- Company consistency is a required integrity invariant even though company identity is also reachable through ReportVersion and FinancialPeriod. The database/service design must prevent a fact from linking a report from one company to a period belonging to another.

**6. Immutable report-version and PIT behavior**

- Every valid, distinct published ReportVersion is retained with its own canonical inputs. Re-ingestion of the same source version under the same extraction-standard version is idempotent; it must not create duplicate facts or mutate previously accepted values.
- A correction/restatement is a new ReportVersion. It never overwrites facts belonging to an earlier version.
- A comparative value is attached to the ReportVersion that actually contains/publishes it, while its period_id identifies the comparative financial period it describes. It does not automatically replace the primary fact for that period from another ReportVersion.
- All source versions remain available to PIT queries. A version is ineligible before its source publication time. The approved audit/restatement quality ranking and tie-break rules are applied by the analysis/version-selection layer after the PIT cutoff; they do not erase or rewrite stored versions.
- Audit status and restatement status remain independent attributes at their approved source scope. They must not be collapsed into a generic fact-quality flag or inferred from each other.
- RESTATED, ESTIMATED, and UNMAPPED are not interchangeable value states: restatement belongs to report/version or source-value status as explicitly defined by the approved report contract; calculated/estimated outputs are runtime-only; unresolved/unmapped inputs are not admitted to canonical persistence.

**7. Separation of canonical input, mapping, and operational audit**

- The canonical input layer must not depend on a persisted raw-row archive. A mandatory raw_fact_id foreign key is therefore incompatible with the target contract.
- Mapping/extraction standards are versioned metadata used to make classification reproducible. DB-DES-002 defines whether compact mapping decisions/rules need their own persisted records; no per-source-row mapping archive is required by this task.
- normalized_financial_fact_inputs is not a required bridge to raw rows. Retain a relationship only if a concrete approved use case proves it necessary without reintroducing raw-row archival or exact-cell locator requirements.
- derived_financial_facts and derived_financial_fact_inputs must not be used to persist application-calculated financial amounts or analytical outputs. Any retirement/migration must be handled separately and non-destructively after inspecting existing data.
- IngestionRun may retain processing status, timestamps, counts, and concise errors/warnings. Failed ingestion may retain operational audit but must not leave partial ReportVersion/canonical-input writes.

**8. Logical acceptance criteria for DB-DES-001**

The design is acceptable only when the final model can demonstrate all of the following: one canonical long-form input contract; stable metric identity separated from source Header mapping; controlled OTHER_* behavior; source meaning/sign/unit/basis fidelity with the owner-approved integer rounding policy; explicit NULL versus genuine zero versus the approved ZERO_FALLBACK; uniqueness that permits multiple periods and immutable versions without duplicate/ambiguous observations; immutable correction/comparative version behavior compatible with PIT; minimum owner-approved provenance without mandatory cell locators; and no raw-row archive or persisted calculated facts.

Physical ORM constraints, the final dimension identity, exact metric/OTHER_* catalog contents, mapping-rule schema, and migration of existing tables remain coordinated follow-on work under DB-DES-002, DB-DES-003, DB-MIG-001, and DB-ING-002. DB-DES-001 does not authorize code, schema, migration, or data changes.

### Financial normalization and mapping

- `financial_metrics` is the small, controlled catalog of canonical analysis metrics and OTHER_* buckets; it is metadata, not a repository of calculated results.
- Ingestion-time mapping resolves source labels into canonical metrics or OTHER_* buckets before persistence. Unresolved mappings must not silently enter the financial-input tables.
- `mapping_rules` may retain concise, versioned mapping metadata needed to make this classification repeatable. Per-source-row raw mapping archives are not a target requirement.
- The target financial fact table is the canonical selected-input layer (the existing `normalized_financial_facts` is a candidate for redesign as that layer). It stores one resolved value per accepted metric/period/report version, with minimal provenance; it is not a second copy of raw facts.
- `normalized_financial_fact_inputs` is not automatically required; retain a composition/provenance relationship only if a concrete analysis or audit requirement cannot be met by the owner's approved minimum provenance.
- Mapping and normalization must not silently create or persist calculated financial amounts.

### Market / FX / ownership

- `market_daily`
- `fx_rates`
- `fx_conversion_rules`
- `share_count_history`
- `corporate_actions`

### Audit

- `ingestion_runs`
- `schema_migrations`

---

## 4–11. (Unchanged principles from V1.1)

Metric catalog, ingestion-time mapping, canonical selected-input facts, minimal provenance, periods, ReportVersion PIT rules, and base FX architecture remain subject to the locked Stage 1 principles where compatible (NULL ≠ 0, PIT versioning, IRR base currency). Raw financial-row retention is explicitly not part of the target contract.

---

## 12. Market and Share Foundations

### Market data database placement — owner decision (2026-11-14)

All V1 application data, including CODAL financial inputs and market inputs, will be stored in **one shared SQLite database**. Market data will not use a separate database in V1. Market information remains logically separated from financial-report data through its own domain tables (for example, `market_daily`, `share_count_history`, and `corporate_actions`); sharing the database file does not mean combining these different data concepts into one table.

This choice keeps company references and cross-domain analysis straightforward while retaining clear table-level separation. A separate market database may be reconsidered only if a future, evidenced scale or operational requirement justifies it; it is not part of the approved V1 design. This is a documentation-level owner decision and does not authorize code, ORM, schema, migration, data, or test changes.


### Market CSV acquisition and persistence — owner decision (2026-11-13)

CSV is an acquisition/file format, not the permanent storage model. Market data downloaded as CSV is to be parsed, validated, and admitted as structured records in the appropriate database tables (for example, `market_daily` for daily OHLC observations), rather than kept only as CSV files for application use. Preserve source identity/reference, original date/calendar meaning, units, quote basis, and source-reported numeric meaning under the global numeric-storage policy. Do not silently admit malformed, ambiguous, duplicate, or unresolved observations.

The downloaded CSV itself is not required to be archived in the database or retained as a permanent raw-data copy. The database stores the validated canonical market inputs and their minimal provenance. Keeping a user's original download outside the database is optional operational file management and is not a database persistence requirement. This decision does not authorize schema or code changes.

`market_daily` preserves source-reported OHLC values, including raw close and adjusted close, as separate inputs. Numeric values are stored as integers under the owner-approved ROUND_HALF_UP policy; ingestion must not recalculate adjusted prices, apply corporate-action adjustments, rescale source units, or otherwise alter their economic meaning. Any analytical transformation is runtime-only.

For market observations, retain the source date in its original calendar representation or unambiguous Jalali components, plus source identity/reference. Exact row/cell coordinates may be used transiently where useful but are not a mandatory persisted locator. A date or price that cannot be resolved unambiguously must not be guessed or admitted as a valid dated observation.

Historical share-count observations must preserve the source-reported share count after the owner-approved integer storage rule, its effective/as-of date or period, and provenance. Corporate-action records must preserve source event terms after the same integer storage rule and the effective date; adjusted share counts, restated historical series, and other derived values are runtime-only. Do not infer or manufacture share counts from corporate-action terms during ingestion.

### Jalali components (CHANGE-005 / V1.2)

Source OHLC from the Iranian market uses Jalali dates. To support correct **same-month comparisons across years** (e.g. all Ordibehesht / month 2, all Esfand / month 12) without depending on Gregorian month identity:

| Column | Type | Role |
|--------|------|------|
| `jalali_year` | INTEGER nullable | Source Jalali year |
| `jalali_month` | INTEGER nullable (1–12) | Source Jalali month — **independent of year** |
| `jalali_day` | INTEGER nullable | Source Jalali day |
| `trade_date` | Date nullable | Retained for backward compatibility; may be NULL for Jalali-sourced rows |

- Ingestion parses the source Jalali string into components only (no Jalali→Gregorian calendar conversion).
- Cross-year same-month analysis must use `jalali_month` (and optionally `jalali_year`).
- Upsert identity for Jalali-sourced rows: `(company_id, jalali_year, jalali_month, jalali_day)`.
- Stage 8 owns market analysis; Stage 1 only stores the foundation.

Historical share counts and corporate actions are preserved so EPS comparability and historical valuation can account for changes in shares outstanding.

---

## 13. FX Foundation (CHANGE-001 + CHANGE-006)

### V1 owner-confirmed FX input contract (2026-11-14)

The V1 FX input consists only of daily US dollar rates, with exactly two rate types:

- `FREE_MARKET` — دلار آزاد
- `EXCHANGE_CENTER` — دلار مرکز مبادله

For each Jalali calendar day and each rate type, the source provides exactly **one rate value**. Separate buy and sell quotes are not part of this V1 input contract. No additional rate categories (including generic operational, official, estimated, or manual-operator types) are included in the confirmed V1 source catalog.

The source quote unit is **Toman per one US dollar**. At ingestion, the application must automatically convert the source rate to **Rial per one US dollar** using the exact factor `1 Toman = 10 Rial`. The canonical rate value used and persisted for analysis is in Rial. Retain the original source amount and its Toman unit/basis in provenance so the conversion is auditable. This Toman-to-Rial conversion is the sole owner-approved automatic unit conversion in the current V1 input scope; it does not authorize conversion or rescaling of CODAL, market-price, volume, transaction-value, or other inputs. The source is daily, and the observation date must be retained using Jalali calendar components.

The logical record therefore identifies one USD rate by its Jalali date and rate type, with the rate value and minimal source provenance. For a given date, the FREE_MARKET and EXCHANGE_CENTER records are distinct and both may exist. Neither rate type may be silently substituted for the other.

This is an owner-approved logical input contract only. It does not authorize changes to ORM models, physical schema, migrations, ingestion code, existing data, or tests. Any mismatch between this V1 contract and legacy implementation names/fields must be handled explicitly during DB-DES-004 / DB-MIG-001 review; do not silently reinterpret or migrate existing records.

### Jalali components and identity (CHANGE-006)

| Logical attribute | Type / meaning |
|--------|------|
| `jalali_year` | INTEGER; source Jalali year |
| `jalali_month` | INTEGER 1–12; source Jalali month |
| `jalali_day` | INTEGER; source Jalali day |
| `rate_type` | `FREE_MARKET` or `EXCHANGE_CENTER` |
| `currency_from` / `currency_to` | USD quoted in Rial for the canonical stored value; source quote basis is Toman |
| `rate_value` | One integer-stored canonical rate in Rial for the date/type |
| source provenance | Original source rate in Toman and source unit, retained to audit the ×10 conversion |

**Logical identity:** `(jalali_year, jalali_month, jalali_day, rate_type)`. There is at most one accepted rate for each date/type combination. If a source supplies duplicate or conflicting values for the same identity, ingestion must reject or explicitly resolve the conflict under a documented source rule; it must not silently choose one.

### Source-value fidelity and quote units

- Preserve the original source quote as Toman per one USD in provenance. Convert it exactly once at ingestion to Rial per one USD by multiplying by 10; persist the canonical rate in Rial as an integer using the owner-approved ROUND_HALF_UP rule.
- The ×10 Toman-to-Rial conversion is the only automatic unit conversion authorized by the owner in the current V1 input scope. Do not apply it to any other input domain. Do not interpolate, average, calculate a synthetic rate, or apply any other rescaling or rewriting.
- Retain observation date, source identity/reference, and any source-specific timestamp needed to interpret the rate. Exact row/cell locators may be used transiently but are not mandatory persisted fields.
- Unknown or ambiguous dates, rate types, quote units, or source values must not be guessed or admitted as valid observations.


### Conversion rules

`fx_conversion_rules` remains the home of FLOW / STOCK / MARKET_VALUE methods and preferred `rate_type`. Defaults:

- FLOW → period-average FX
- STOCK → period-end FX
- MARKET_VALUE → same-date FREE_MARKET FX

---

### FX V1 owner decision record (2026-11-14)

The V1 FX source contract was confirmed by the owner on 2026-11-14: daily USD rates, two types only (`FREE_MARKET` and `EXCHANGE_CENTER`), one value per date/type (no separate buy/sell values), source quote in Toman per USD, and Jalali observation dates. The owner further confirmed on 2026-11-14 that ingestion must automatically convert this FX quote to Rial using the exact factor ×10. The canonical persisted/analytical rate is in Rial; the original Toman source amount and unit must remain in provenance for auditability. This is the sole authorized automatic unit conversion in the current V1 input scope. This decision narrows the older generic FX taxonomy above for V1. Legacy implementation compatibility is not implied; any required model/schema/migration alignment must be reviewed explicitly in DB-DES-004 / DB-MIG-001. Documentation-only decision; no code, ORM, schema, migration, data, or test changes.

## 14. Ingestion Boundary (CHANGE-007)

### Layering

```text
Source file / Excel / API
        ↓
Format-specific acquisition and extraction adapter
        ↓
Common DTOs (RawLineInput, FxRateInput, OHLC field map)
        ↓
ingest_codal_report / ingest_ohlc_* / ingest_fx_rates
        ↓
DB foundation tables + IngestionRun
```

### CODAL source formats and Excel transition

The intended direction is to replace CODAL PDF acquisition/extraction with Excel acquisition/extraction, while preserving the common ingestion and persistence contract.

- The Excel adapter must emit the same common financial input DTO contract consumed by `ingest_codal_report`; the existing downstream persistence boundary must remain format-independent.
- The Excel adapter must emit the common financial-input DTO contract required by the canonical ingestion boundary. DTO fields for transient extraction diagnostics may be added only when justified; permanent workbook/sheet/cell coordinates are not a required persisted contract. No compatibility requirement to preserve or maintain a PDF ingestion caller is imposed by V1.
- Excel workbooks are heterogeneous. Do not assume fixed worksheet names, row numbers, column numbers, or identical layouts across companies or report types.
- Use original source labels, worksheet structure, and raw numeric values transiently during extraction and mapping. Do not archive the workbook or persist a general archive of raw rows/labels. Persist only the resolved canonical metric/bucket value and the minimum provenance defined by owner decision 3.11: company, report type/version, actual period, canonical metric, and extraction-standard version. Exact workbook/sheet/row/cell coordinates may assist extraction and debugging but are not mandatory persisted per-fact fields.
- Do not guess mappings, units, period boundaries, company identity, report type, or source attribution. Unresolved required metadata is an admission failure or must remain outside the analytical database until resolved.
- Read cached formula results from the workbook; do not evaluate spreadsheet formulas in the extraction adapter. If a formula cell has no usable cached result, emit an explicit warning/rejection/unknown state; never fabricate a value.
- Classify each source row during ingestion as a canonical metric, an OTHER_* bucket item, or discard/reject. Do not persist the original row merely because it exists in the workbook. Reproducible aggregates are calculated at runtime; miscellaneous amounts that matter only as broad totals are mapped into the relevant OTHER_* bucket. Application-generated calculations remain runtime-only.
- Blank/unusable source input cells remain NULL/unknown, not zero. A valid source-reported product sales amount is stored as an integer using ROUND_HALF_UP. If that amount is blank and quantity plus selling rate are valid and compatible, their product is runtime-only and is not persisted. Only when the product sales amount is blank/unusable and quantity or rate is missing, invalid, or incompatible may the narrowly approved ZERO_FALLBACK be persisted as integer zero with a distinct origin/state and ingestion warning, strictly under Master Packet Section 3.5. No other metric may use a synthetic fallback.
- Quarterly CODAL filings commonly report cumulative year-to-date values. Q1/Q2/Q3/Q4 source periods must follow the FinancialPeriod contract in Section 3. Standalone-quarter values are derived at runtime, using compatible report versions; they are not source facts to persist.
- CODAL PDF acquisition/extraction is outside the V1 target scope and is not a supported input path or acceptance criterion. V1 requires neither creating nor preserving a PDF adapter, nor maintaining PDF compatibility during the Excel implementation. Any PDF-related code that remains in the repository is historical legacy implementation only; its continued existence must not create a transition dependency or additional maintenance requirement.
- Historical implementation note only: legacy PDF-related code may exist in the repository, but it is outside the V1 supported input architecture and creates no requirement to preserve, maintain, or validate that path.

### OHLC / FX formats

- CSV, Excel, or future formats are interchangeable at the adapter layer only.
- Core persistence does not depend on file extension.
- Architecture completion does **not** require loading production data into the database.

### Failure, admission gates, and audit

- Company identity and the company's single industry must be resolved and validated before report/canonical-financial-input persistence.
- Unknown or ambiguous company identity, industry, report type, financial period, or source attribution is a hard admission failure. The system must not guess, silently default, or persist a partially identified record.
- Failed financial ingestion must not leave partial report or canonical-financial-input writes.
- The failed `IngestionRun` remains auditable, but failed source data must not be inserted into the report or financial-fact tables.
- NULL ≠ 0 is mandatory. Synthetic financial values are prohibited except for the narrowly approved `ZERO_FALLBACK` for product sales amount under Master Packet Section 3.5, and only under its specified conditions with a distinct origin/state and ingestion warning. For every other metric, zero may be stored only when the source explicitly reports a valid zero.
- Validation must distinguish a known-but-blank source value from an unknown label, unknown unit, unresolved period, or unresolved company/industry. The latter cases must be rejected or quarantined outside the analytical database until resolved.

## 15. Migration Policy

`Base.metadata.create_all()` is permitted only for an empty development/bootstrap database.

Production/schema evolution uses the versioned migration runner:

`python -m src.scripts.migrate_db`

The repository migration runner currently reaches schema version **8**. The architecture document must stay synchronized with the executable migration history:

| Version | Name |
|---|---|
| 1 | `baseline_schema` |
| 2 | `mapping_and_derived_schema` |
| 3 | `normalized_fact_multi_source_provenance` |
| 4 | `one_current_report_version` |
| 5 | `market_daily_jalali_components` |
| 6 | `fx_rates_jalali_components` |
| 7 | `forecast_version_repository` |
| 8 | `remove_forecast_output_persistence` |

Migrations are ordered and idempotent. Existing source values must not be silently rewritten. Any future migration implementing the Jalali FinancialPeriod contract or removing/deprecating calculated-fact persistence must first inspect existing rows, report ambiguous data, and avoid destructive or guessed conversions. Migration 8's removal of forecast-output persistence is consistent with the runtime-only analytical-output policy.

---

## 16. Ownership Boundaries

Database owns selected canonical financial inputs, minimal provenance, controlled metric/bucket catalogs and mapping metadata, market/FX/share foundations, and ingestion audit. Ingestion services own source-row classification and mapping before persistence. Backend services own runtime calculations, reconciliation, KPI/scoring, trends, forecasts, valuation, and decisions. Raw financial-row archives, calculated financial values, and analytical/decision outputs are not persisted.

---

## 17. Version

`database_contract_version = DATABASE_CONTRACT_V1.3`

Overall Analyzer architecture remains **V1** with exactly nine analytical stages.

Approved/reviewed decisions recorded in this revision: company/industry admission contract; FinancialPeriod Jalali/YTD contract; selected canonical-input persistence without raw financial-row retention, simple OTHER_* buckets, minimal provenance, and runtime calculation policy; Excel adapter direction with common DTO/persistence boundary and Excel-only input scope and exclusion of PDF; migration history corrected through version 8. CHANGE-003, CHANGE-005, CHANGE-006, CHANGE-007 remain historical amendment references pending a complete section-by-section audit.
