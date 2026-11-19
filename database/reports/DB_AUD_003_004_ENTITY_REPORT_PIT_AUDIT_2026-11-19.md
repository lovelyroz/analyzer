# DB-AUD-003 / DB-AUD-004 — Entity, ReportVersion and PIT implementation audit

**Date:** 2026-11-19  
**Branch:** `master`  
**Scope:** Read-only inspection of current tracked implementation. No ORM, schema, migration, data, code, or test changes. Tests were not run.

## Executive result

- **DB-AUD-003 — PARTIAL:** the current ORM materially exceeds or differs from the approved V1 Company/Industry contract. Industry parent-child support remains in the model; Company contains several fields excluded from the V1 fixed-identity list. The migration runner bootstraps current metadata but has no inspected dedicated Entity reconciliation/catalog-seed migration. Runtime catalog/data state was not accessible.
- **DB-AUD-004 — PARTIAL:** Report and ReportVersion have basic version numbering, publication timestamp, restatement flag, supersession pointer, and a one-current-version-per-report partial unique index. However, Report still owns a mandatory single FinancialPeriod; identity/idempotency is incomplete when CODAL tracking ID is absent; version ingestion makes the latest-ingested version current without comparing publication chronology; and no compliant PIT selector was evidenced in the inspected paths.

## Evidence inspected

1. `src/models/entity.py`
2. `src/models/report.py`
3. `src/migrations/runner.py`
4. `src/ingestion/service.py`
5. `src/ingestion/codal/adapter.py`
6. `src/ingestion/codal/ingestion.py`
7. `database/reports/DB_DES_003_REPORT_PERIOD_CONTRACT.md`
8. Master Packet §3.1, §3.3, §4.1–4.2 and Task definitions.

## DB-AUD-003 — Entity / Industry

### Observed implementation

- `Industry`: `industry_id`, unique non-null `industry_code`, non-null `industry_name`, and nullable self-FK `parent_industry_id` with `ON DELETE SET NULL`.
- `Company`: `company_id`, nullable unique `national_id`, non-null `ticker`, non-null `company_name`, non-null FK `industry_id`, nullable `codal_symbol`, nullable `fiscal_year_end`, non-null `status` defaulting to ACTIVE, non-null `is_active` defaulting true, and `created_at`.
- The approved V1 fixed Company identity is exactly `company_id`, `company_name`, `ticker`, and `industry_id`. The current model therefore has extra fields and overlapping status concepts (`status` and `is_active`); `national_id` and `codal_symbol` are not part of the approved fixed list.
- Industry's self-reference permits parent/sub-industry hierarchy even though parent/sub-industry is out of V1 scope.
- The model has no industry active/status field, despite the logical catalog description including a status attribute. This is a contract-to-model discrepancy to resolve in physical design; it is not permission to add a column.
- No uniqueness constraint on Company ticker was observed. The approved contract does not state that ticker itself is a stable company key; `company_id` is the stable identity.
- `src/migrations/runner.py` imports both models and baseline migration creates `Base.metadata`; the inspected migration list contains no explicit industry catalog seeding or Entity-contract reconciliation migration.
- The inspected CODAL persistence service accepts `company_id` and relies on a FinancialPeriod company match plus database FK behavior. No explicit pre-admission validation of an approved industry catalog or exact Company V1 identity was evidenced in this path.

### Impact / required follow-up

1. Decide how to reconcile legacy extra Company fields and Industry parent relation with the strict V1 contract without destructive deletion.
2. Confirm the authoritative seven-industry catalog seed and whether existing DBs contain unrecognized codes.
3. Inspect all Company/Industry readers, writers, imports, API/DTOs and existing database rows before proposing migration.
4. Verify that every ingestion entry point rejects missing/invalid Company and Industry, not only the CODAL persistence path inspected here.

### Data limitation

No live SQLite file, configured environment, schema snapshot, or row sample was available through this read-only GitHub file inspection. Existing parent rows, Company field population, duplicate tickers, invalid industry references, and actual catalog coverage remain unknown.

## DB-AUD-004 — Report / ReportVersion / PIT

### Observed implementation

- `Report` has `company_id`, free-text `report_type`, optional unique `codal_tracking_id`, title, mandatory `financial_period_id`, source URL, optional self-reference `original_report_id`, `is_correction`, and creation timestamp.
- The mandatory Report-level `financial_period_id` conflicts with the approved multi-period contract: a single ReportVersion can publish multiple FinancialPeriods and each FinancialFact must attach to its own actual period. The Report primary period may remain descriptive only if separately reconciled; it cannot substitute for per-fact period identity.
- `ReportVersion` has `report_id`, `version_number`, non-null `publication_datetime`, `is_current_version`, `is_restated`, optional `supersedes_version_id`, and creation timestamp.
- A unique constraint exists on `(report_id, version_number)`; a partial unique index enforces at most one current version per report.
- Migration 4 checks for multiple current versions and fails rather than silently resolving them, then creates the partial unique index. This is a useful fail-closed migration guard.
- In `ingest_codal_report`, report lookup is by `codal_tracking_id` only when that ID is supplied. Without it, each call creates a new Report; no alternate logical identity/deduplication is applied in the inspected code.
- Existing-version replay detection requires a tracking ID and matches publication datetime; it does not compare a source payload fingerprint/content hash.
- When a new version is ingested, the previous current version is demoted and the newly ingested version is marked current. The code does not compare publication datetime against existing versions before changing current status. A late-arriving older publication can therefore become current.
- `supersedes_version_id` is assigned to the last version by version_number, not based on an explicit source correction/supersession identity check. `is_restated` is a caller-supplied boolean; the inspected adapter accepts it as metadata.
- The inspected paths did not establish a PIT query that first filters by `publication_datetime <= cutoff`, then applies the approved audit/restatement rank and publication-time tie-breaker, while selecting one coherent version per Report. No claim is made that no such query exists elsewhere; full repository call-site discovery remains open.
- `src/ingestion/codal/adapter.py` remains PDF-oriented and passes report metadata into the persistence facade; this audit does not alter the separate Excel-pivot work.

### Impact / required follow-up

1. Reconcile Report's primary-period field with the approved per-Fact FinancialPeriod contract.
2. Define and enforce stable logical Report identity when CODAL tracking ID is absent, and replay identity using source fingerprint/revision evidence.
3. Make current-version semantics independent from ingestion arrival order; preserve late-arriving historical versions without incorrectly replacing the current publication.
4. Audit all PIT/read/query consumers and prove cutoff-first filtering, quality ranking, publication tie-break, unknown-status handling, and coherent per-Report version selection.
5. Inspect existing report/version rows before any migration; retain all historical versions.

## Owner decisions required — consolidated batch

مالک در 2026-11-19 به موارد زیر پاسخ داده است؛ تصمیم‌ها در ادامه به‌عنوان قرارداد مالک ثبت می‌شوند.

1. **Company V1 strictness — DECIDED:** در کنار چهار فیلد هویتی ثابت (`company_id`, `company_name`, `ticker`, `industry_id`)، فقط `codal_symbol` و `fiscal_year_end` از فیلدهای اضافهٔ فعلی برای V1 حفظ شوند. `national_id`, `status`, `is_active`, `created_at` جزو قرارداد هدف V1 نیستند. این تصمیم مجوز حذف فوری داده/ستون نیست؛ پیش از هر migration باید مصرف‌کنندگان و دادهٔ موجود بررسی و برنامهٔ سازگاری/انتقال جداگانه تصویب شود.
2. **Industry catalog lifecycle — DECIDED:** seed نسخه‌دار و idempotent برای هفت کد اولیه تأیید شد؛ Industry فیلد active/status جداگانه نخواهد داشت. کدهای seed پس از استفاده نباید بی‌سروصدا تغییر معنا دهند.
3. **Company ticker uniqueness — DECIDED:** چون `company_id` کلید پایدار شرکت است و قرارداد V1 برای ticker تاریخچه/دامنهٔ بازار تعریف نکرده، روی `ticker` قید UNIQUE سراسری اعمال نمی‌شود. ticker شناسهٔ نمایشی/بازاری است، نه کلید هویت؛ هرجا تطبیق بازار لازم باشد باید از زمینهٔ بازار و نگاشت معتبر استفاده شود.
4. **Report primary period — DECIDED:** `Report.financial_period_id` در مدل هدف فقط به‌صورت اشاره‌گر اختیاری/توصیفی به دورهٔ اصلی گزارش باقی می‌ماند؛ دورهٔ هر مقدار فقط از FinancialFact/RawFact مربوط به همان مقدار تعیین می‌شود. این فیلد مرجع همهٔ Factهای گزارش نیست.
5. **Missing CODAL tracking ID — DECIDED BY TECHNICAL OWNER:** برای جلوگیری از ادغام اشتباه دو گزارش یا ساخت نسخهٔ تکراری، `codal_tracking_id` یا شناسهٔ یکتای پایدار و مستند منبع شرط پذیرش و replay خودکار است. اگر وجود نداشته باشد، سیستم نباید از عنوان/تاریخ/شرکت یک کلید ترکیبی حدسی بسازد؛ گزارش برای تعیین هویت متوقف و به صف بررسی/رفع نقص metadata هدایت می‌شود. پس از شناسایی شناسهٔ پایدار، replay باید علاوه بر شناسه و publication identity، fingerprint محتوای ورودی را نیز مقایسه کند تا payload متفاوت با replay یکسان اشتباه نشود.
6. **Late-arriving publication — DECIDED:** بله؛ نسخهٔ قدیمی‌تر که دیرتر دریافت شده حفظ می‌شود، اما صرفاً به‌دلیل زمان ingestion نباید current شود. انتخاب جاری/PIT بر اساس publication معتبر و رتبه‌بندی مصوب انجام می‌شود.
7. **Unknown audit/restatement metadata — DECIDED:** بله؛ اگر وضعیت نامعلوم بتواند نتیجهٔ رتبه‌بندی را تغییر دهد، انتخاب خودکار unresolved می‌ماند و حدس مجاز نیست.

## Completion criteria

DB-AUD-003 and DB-AUD-004 remain PARTIAL until repository-wide call-site/read-write inventory, actual DB/schema/data inspection, and PIT selector evidence are complete. No code, ORM, schema, migration, data, or test changes were made; tests were not run.


## Owner decision addendum — 2026-11-19

تصمیم‌های بالا از سوی مالک دریافت و نهایی شد. خلاصهٔ اجرایی:

- Company: فیلدهای ثابت هویتی چهارگانه به‌علاوهٔ فقط codal_symbol و fiscal_year_end در V1؛ سایر فیلدهای اضافهٔ فعلی جزو قرارداد هدف نیستند، اما حذف فیزیکی بدون inventory و migration plan مجاز نیست.
- Industry: seed نسخه‌دار/idempotent برای هفت کد تأیید؛ active/status جداگانه لازم نیست.
- Ticker: قید یکتایی سراسری ندارد؛ company_id هویت پایدار است.
- Report: primary period اختیاری و صرفاً توصیفی است؛ هر Fact دورهٔ مستقل خودش را دارد.
- Report identity: شناسهٔ پایدار منبع لازم است؛ در نبود آن fail-closed، بدون composite key حدسی. Replay باید fingerprint محتوا را نیز مقایسه کند.
- نسخهٔ دیررس: حفظ تاریخی، بدون ارتقای خودکار به current صرفاً بر مبنای زمان ورود.
- audit/restatement نامعلوم: در صورت اثرگذاری بر برنده، انتخاب unresolved.

این تصمیم‌ها قرارداد مستنداتی را می‌بندند، نه ممیزی پیاده‌سازی را. DB-AUD-003/004 تا تکمیل inventory تمام call-siteها، بررسی DB واقعی و اثبات PIT selector همچنان PARTIAL می‌مانند. هیچ کد، ORM، schema، migration یا داده‌ای تغییر نکرد و تستی اجرا نشد.
