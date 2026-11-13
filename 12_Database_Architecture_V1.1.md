# Analyzer V1 — Database Architecture V1.3

## Status

**UNDER REVIEW — DATABASE CONTRACT V1.3 (REOPENED FOR ARCHITECTURAL REVIEW)**

**Database engine:** SQLite

**ORM:** SQLAlchemy

**Schema migration version:** 8

This document is reopened for review. The decisions explicitly recorded as reviewed/approved below are the current working contract; sections not yet audited remain provisional. Earlier V1 / V1.1 / V1.2 references are historical context and do not override the decisions recorded here. The database stores selected canonical financial inputs and minimal provenance, not raw financial statement rows; backend services own runtime calculations and analytical outputs. This contract supports Stages 2–9 without persisting calculated analytical results.

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
  ├─ CODAL financial reports (current PDF path; Excel adapter planned)
  ├─ Daily market data (CSV / XLSX / …)
  └─ FX data — FREE_MARKET & OPERATIONAL (CSV / XLSX / …)
          ↓
Format-specific acquisition / extraction adapters
  ├─ CODAL PDF adapter (existing; retain during Excel transition)
  ├─ CODAL Excel adapter (planned; emits the same common DTO contract)
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

### Company master information — current scope

The company master data needed for periodic-report organization includes:

- `company_id`: unique internal company identifier.
- `company_name`: official company name.
- `ticker`: stock-market symbol, where applicable.
- `industry_id`: the company's single assigned industry.
- `company_type`: company type, such as bank, investment company, petrochemical company, etc.
- `status`: company status, such as active or inactive.

Each company belongs to exactly one industry, as specified by the company/industry contract above. This list records the current logical information requirements; it does not yet define physical table columns, constraints, or implementation details.

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
   - Preserve the exact original CODAL wording/code and its source location/evidence used for classification. Do not infer the status from the report title or another version.
4. **Original/restated classification**
   - Normalized `revision_status`: `ORIGINAL`, `RESTATED`, or `UNKNOWN`.
   - Preserve the exact original CODAL wording/code and its source location/evidence used for classification. Do not infer restatement merely because a version is newer or because its values differ.
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

**Source and period integrity for persisted financial facts**

- Every persisted financial fact belongs to exactly one `ReportVersion`; it must never be linked only to the logical `Report` while leaving its source version ambiguous.
- Every persisted financial fact belongs to exactly one `FinancialPeriod`, identifying the period the value actually describes. This may be the report's primary period or a comparative period included in the same filing.
- The fact's `ReportVersion`, its parent `Report`, and its `FinancialPeriod` must resolve to the same company. A cross-company link is invalid and must be rejected.
- The fact's period must be supported by the source filing. A comparative prior-period value must link to the corresponding prior-period record; the system must not assign the current report period merely because it is the primary period.
- The source locator must identify the exact origin of the selected value within that specific report version (for Excel, workbook/sheet/cell or an equivalently precise locator). A locator from another version must not be reused as if it identified the current source.
- Re-ingestion of the same source item from the same immutable `ReportVersion` must be idempotent. Identify that source item using its exact source locator together with the report version; validate its metric classification, financial period, unit/measure semantics, and meaningful dimensions. Re-ingestion must not create a second copy or mutate the previously captured value.
- Do not identify duplicates by numeric equality alone. Equal amounts may describe different products, segments, periods, dimensions, or independently reported observations.
- If the same metric, period, unit, and dimensions appear at different source locators within one report version, do not silently merge, overwrite, discard, or add the observations merely because their values are equal. Preserve their distinct source identities as separate source observations when each is a valid source input. Their analytical relationship (for example, repeated presentation of the same amount versus separate components) must be resolved from report structure and meaning before analysis; unresolved observations must not be summed or treated as independent economic amounts.
- If the same source locator in the same report version is encountered with a different captured value or incompatible metadata, treat it as a source conflict. Do not overwrite the stored input; resolve whether the artifact/version identity is wrong before admitting a new snapshot.
- Do not impose a simplistic uniqueness rule on metric + period alone where the source legitimately reports multiple products, segments, or other dimensions.
- A fact whose report version, company, financial period, metric meaning, unit, or source locator cannot be validated must not be persisted. Ingestion must not leave partial report/version/fact writes when validation fails.

Additional rules:

- Persist independently meaningful inputs required for analysis, such as production quantity, sales quantity, selling rate, cost inputs, and other selected canonical measures, only after their meaning, unit, period, and provenance are resolved.
- Do not persist a total/subtotal when it is reproducible from sufficient validated inputs using a known, explicitly defined calculation rule. The backend computes it when needed.
- A reported aggregate that is not required as a distinct analytical input may be mapped into the relevant OTHER_* bucket rather than retained as a separate raw row. This includes an amount reported only as one figure, such as a miscellaneous asset sale, other income, or other expense. Preserve the useful amount in the simple bucket; do not preserve its raw accounting detail.
- When both components and an aggregate are present, avoid double counting. Use the components for metrics that require them; map only genuinely non-overlapping residual items to an OTHER_* bucket. Never add a total to its own components.
- Do not infer formulas from labels or visual proximity. A derived value may be calculated only when its formula/relationship is known and all required inputs are available and valid.
- Do not substitute one measure for another. For example, production quantity is not sales quantity.
- The published company report is the source of truth for reported financial values. The application is responsible for faithfully extracting, classifying, and storing those values; it must not independently judge or revise a reported financial figure based on its own arithmetic. Corrections are recognized through a newer published report version, not by changing the earlier version.
- **Product sales amount resolution:** a valid amount explicitly reported by the source is authoritative and must be persisted as a canonical input, even if it differs from quantity × selling rate. If the reported amount is blank or unusable, calculate quantity × selling rate at runtime only when both inputs are present, valid, and expressed on compatible units and periods. Do not persist this calculated fallback as a reported/source input.
- A blank or unusable source-reported product sales amount remains NULL/unknown. If quantity and selling rate are both present, valid, and compatible, their product may be calculated at runtime only. If they are not, the amount remains unavailable. Never insert a synthetic zero or any other substitute for a missing source value.
- An explicit, valid source-reported zero is stored as zero because that is what the source reported. It must not be replaced by quantity × rate.
- Do not infer missing inputs, totals, quantities, rates, units, periods, or labels.
- Persisted financial values must remain faithful to the source-reported input: do not recalculate, rebalance, round for convenience, fill blanks, replace values, or otherwise alter their financial amount. A new published correction/restatement is a separate immutable report version; it does not authorize editing the previously ingested version.
- Calculated values are runtime-only. They must not be inserted into financial-input, normalized, derived, cache, or history tables.
- Keep only minimal provenance with each persisted canonical input: at least the company/report identity, report version, financial period, and source locator sufficient to trace the value back to its origin (for example, source section/row for PDF or workbook/sheet/cell for Excel). Do not retain every original label, raw row payload, or unused source value merely for archival purposes.
- Runtime calculation results must retain enough in-memory lineage to explain their inputs and formula where auditability requires it, but this does not authorize persistence of the calculated result.

The existing raw_financial_facts table is incompatible with this target if it acts as a general raw-row archive. The existing normalized-input model may become the canonical persisted financial fact layer, but it must not duplicate a separate raw-value layer. Existing derived_financial_facts and derived_financial_fact_inputs are incompatible if they persist application-calculated financial values. Their future schema/migration treatment must inspect existing data first and be non-destructive until a safe migration is designed. Do not write new raw-row archives or calculated results during transition.

### Financial normalization and mapping

- `financial_metrics` is the small, controlled catalog of canonical analysis metrics and OTHER_* buckets; it is metadata, not a repository of calculated results.
- Ingestion-time mapping resolves source labels into canonical metrics or OTHER_* buckets before persistence. Unresolved mappings must not silently enter the financial-input tables.
- `mapping_rules` may retain concise, versioned mapping metadata needed to make this classification repeatable. Per-source-row raw mapping archives are not a target requirement.
- The target financial fact table is the canonical selected-input layer (the existing `normalized_financial_facts` is a candidate for redesign as that layer). It stores one resolved value per accepted metric/period/report version, with minimal provenance; it is not a second copy of raw facts.
- `normalized_financial_fact_inputs` is not automatically required; retain a composition/provenance relationship only if a concrete analysis or audit requirement cannot be met by the minimal source locator.
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

`market_daily` preserves raw close and adjusted close separately.

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

### Rate types (locked)

- `FREE_MARKET` — free-market dollar (e.g. دلار آزاد)
- `OPERATIONAL` — exchange / NIMA / مبادله‌ای
- `OFFICIAL`, `ESTIMATED`, `MANUAL_OPERATOR` — supporting types

FREE_MARKET and OPERATIONAL must never be silently substituted for each other.

### Jalali components and identity (CHANGE-006)

| Column | Type | Role |
|--------|------|------|
| `jalali_year` | INTEGER nullable | Source Jalali year |
| `jalali_month` | INTEGER nullable (1–12) | Source Jalali month |
| `jalali_day` | INTEGER nullable | Source Jalali day |
| `rate_date` | Date nullable | Gregorian; NULL for Jalali-sourced rows |

**Identity:**

- Jalali-sourced: `(jalali_year, jalali_month, jalali_day, currency_from, currency_to, rate_type)`
- Gregorian-only: `(rate_date, currency_from, currency_to, rate_type)`

Same calendar day may hold both FREE_MARKET and OPERATIONAL rows.

### Unit storage policy (CHANGE-006)

- Persisted `rate` is always **IRR (Rial) per 1 unit of `currency_from`**.
- Free-market sources quoted in **Toman** are converted ×10 at the **adapter** boundary (explicit flag, e.g. `rates_in_toman=True`).
- Operational / NIMA rates already in Rial are stored as-is.
- Downstream stages consume IRR rates only; they do not re-apply unit conversion.

### Conversion rules

`fx_conversion_rules` remains the home of FLOW / STOCK / MARKET_VALUE methods and preferred `rate_type`. Defaults:

- FLOW → period-average FX
- STOCK → period-end FX
- MARKET_VALUE → same-date FREE_MARKET FX

---

## 14. Ingestion Boundary (CHANGE-007)

### Layering

```text
Source file / PDF / Excel / API
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
- Preserve the established `RawLineInput` semantics and compatibility. Any required Excel provenance extension (such as workbook/sheet/cell coordinates) must be additive and must not break existing PDF callers.
- Excel workbooks are heterogeneous. Do not assume fixed worksheet names, row numbers, column numbers, or identical layouts across companies or report types.
- Use original source labels and raw numeric values transiently during extraction and mapping, but do not persist a general archive of them. Persist only the resolved canonical metric/bucket value and its minimal provenance. For Excel, the source locator should identify at least workbook/source identity, worksheet, and row/cell where available.
- Do not guess mappings, units, period boundaries, company identity, report type, or source attribution. Unresolved required metadata is an admission failure or must remain outside the analytical database until resolved.
- Read cached formula results from the workbook; do not evaluate spreadsheet formulas in the extraction adapter. If a formula cell has no usable cached result, emit an explicit warning/rejection/unknown state; never fabricate a value.
- Classify each source row during ingestion as a canonical metric, an OTHER_* bucket item, or discard/reject. Do not persist the original row merely because it exists in the workbook. Reproducible aggregates are calculated at runtime; miscellaneous amounts that matter only as broad totals are mapped into the relevant OTHER_* bucket. Application-generated calculations remain runtime-only.
- Blank/unusable source input cells remain NULL/unknown, not zero. No synthetic fallback value (including zero) may be persisted for a missing source input. A valid source-reported product sales amount is retained as reported; when it is blank, quantity × selling rate may be calculated at runtime only if both inputs are valid and compatible.
- Quarterly CODAL filings commonly report cumulative year-to-date values. Q1/Q2/Q3/Q4 source periods must follow the FinancialPeriod contract in Section 3. Standalone-quarter values are derived at runtime, using compatible report versions; they are not source facts to persist.
- Do not remove or disable the existing PDF acquisition/extraction path until the Excel adapter has been implemented and passed end-to-end validation against representative reports. During transition, both adapters may coexist and feed the same common DTO/persistence path.
- The current implementation uses PDF acquisition/extraction and `pypdf`; image-only/no-text PDFs are explicitly rejected and OCR is not silently substituted. This describes the current path, not the target format policy.

### OHLC / FX formats

- CSV, Excel, or future formats are interchangeable at the adapter layer only.
- Core persistence does not depend on file extension.
- Architecture completion does **not** require loading production data into the database.

### Failure, admission gates, and audit

- Company identity and the company's single industry must be resolved and validated before report/canonical-financial-input persistence.
- Unknown or ambiguous company identity, industry, report type, financial period, or source attribution is a hard admission failure. The system must not guess, silently default, or persist a partially identified record.
- Failed financial ingestion must not leave partial report or canonical-financial-input writes.
- The failed `IngestionRun` remains auditable, but failed source data must not be inserted into the report or financial-fact tables.
- NULL ≠ 0 is mandatory. No `ZERO_FALLBACK` or other synthetic financial value is permitted in the database. A zero may be stored only when the source explicitly reports a valid zero.
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

Approved/reviewed decisions recorded in this revision: company/industry admission contract; FinancialPeriod Jalali/YTD contract; selected canonical-input persistence without raw financial-row retention, simple OTHER_* buckets, minimal provenance, and runtime calculation policy; Excel adapter direction with common DTO/persistence boundary and safe PDF transition; migration history corrected through version 8. CHANGE-003, CHANGE-005, CHANGE-006, CHANGE-007 remain historical amendment references pending a complete section-by-section audit.
