> **Historical reference/status as of 2026-11-21:** Any PDF extraction implementation, test command, corpus, or pre-retirement status described here is superseded. Excel/CSV are the supported file inputs, and CODAL PDF extraction is retired. See database/reports/DB_CODAL_RETIRE_001_EXCEL_CSV_ONLY_RETIREMENT.md.

# DB-AUD-013 — ممیزی آمادگی Persistence برای CODAL Excel

**تاریخ:** 2026-11-18  
**وضعیت:** COMPLETE — بررسی قرارداد منطقی هدف در برابر ORM فعلی  
**نوع تغییر:** Audit/design-readiness؛ بدون تغییر کد، ORM، Migration، داده یا تست.

## 1. هدف و مبنا

این ممیزی Phase 0 از DB-PLAN-013 را آغاز می‌کند: مشخص‌کردن اینکه آیا می‌توان مسیر Excel را با مدل‌های persistence فعلی پیاده کرد و Report/ReportVersion فعلی تا چه حد قابل استفاده مجدد است.

مبنای تصمیم:
- معماری اصلی 12_Database_Architecture_V1.1.md، نسخه فعلی محتوایی V1.3 و بخش‌های DB-DES-001 و DB-DES-006؛
- قرارداد DTO/Reader اکسل و Company Table Layout Template؛
- ORM فعلی در src/models/normalized.py، normalized_provenance.py، period.py و report.py؛
- نتایج DB-AUD-009 تا DB-AUD-012.

فایل XLSX در این ممیزی باز نشده است. این بررسی فقط معماری و source code مخزن را مقایسه می‌کند.

## 2. قرارداد منطقی هدف

طبق DB-DES-001، FinancialFact هدف یک ورودی مالی canonical است، نه یک ردیف خام workbook. هر رکورد باید به این مفاهیم قابل انتساب باشد:

- ReportVersion دقیق منتشرکننده؛
- FinancialPeriod واقعی همان مقدار؛
- FinancialMetric پایدار؛
- نسخه دقیق extraction/interpretation standard؛
- مقدار منبع با unit/currency/measurement basis؛
- ابعاد value-defining مصوب، در صورت وجود؛
- state/origin برای تمایز مقدار گزارش‌شده، NULL/blank و ZERO_FALLBACK مجاز؛
- IngestionRun اختیاری برای audit عملیاتی.

فایل workbook و raw rows نباید به‌صورت دائمی آرشیو شوند. exact cell locator الزام عمومی برای persistence نیست. ReportVersion باید source artifact reference و content fingerprint داشته باشد.

DB-DES-006 نیز مسیر هدف را به‌صورت Excel observations موقت → structural mapping → semantic mapping → temporal/value interpretation → whole-report validation → canonical persistence در یک transaction تعریف می‌کند. این قرارداد هدف، به معنی انطباق ORM یا pipeline فعلی نیست.

## 3. مقایسه با مدل‌های موجود

### 3.1 Report

مدل فعلی src/models/report.py::Report شامل:
- company_id
- report_type به‌صورت VARCHAR آزاد، نه FK به ReportType catalog
- codal_tracking_id
- title
- financial_period_id به‌عنوان primary report period
- source_url
- original_report_id و is_correction

**قابل استفاده مجدد:** هویت منطقی report، company link، title، source URL و tracking identity می‌توانند بخشی از زیرساخت report باشند.

**شکاف‌ها:**
- report_type هنوز catalog/FK مصوب دو نوع MONTHLY_ACTIVITY و PERIODIC_FINANCIAL نیست.
- financial_period_id در مدل فعلی روی Report اجباری است، در حالی که قرارداد هدف می‌گوید یک ReportVersion می‌تواند چند FinancialPeriod داشته باشد و هر fact دوره واقعی خودش را تعیین کند؛ report-level period نباید دوره همه facts را تحمیل کند.
- source URL به‌تنهایی source artifact fingerprint/revision identity را پوشش نمی‌دهد.

**نتیجه:** Report قابل reuse کامل بدون تطبیق نیست؛ report type و primary-period semantics باید در طراحی فیزیکی اصلاح/محدود شوند.

### 3.2 ReportVersion

مدل فعلی شامل:
- report_id
- version_number
- publication_datetime
- is_current_version
- is_restated
- supersedes_version_id
- created_at

**قابل استفاده مجدد:** publication time، version sequencing، restatement، current/supersedes و uniqueness فعلی، پایه مناسبی برای ReportVersion هستند.

**شکاف‌ها:**
- source artifact reference و SHA-256/fingerprint در ReportVersion فعلی وجود ندارد.
- template_version_id یا extraction-standard version binding وجود ندارد.
- source revision identity و replay/canonical payload identity هنوز در مدل کامل نیست.
- گزارش DB-AUD-009 پیشنهاد کرده بود template_version_id nullable برای provenance تاریخی در ReportVersion قرار گیرد؛ این هنوز proposal است و نباید بدون design review به migration تبدیل شود.

**نتیجه:** ReportVersion بهترین بخش قابل reuse است، اما برای source fingerprint و standard/template version باید طراحی و توسعه یابد. یک ReportVersion باید پیش از درج هر FinancialFact به نسخه استاندارد دقیق bind شود.

### 3.3 FinancialPeriod

مدل فعلی src/models/period.py از Gregorian SQL Date برای start_date/end_date استفاده می‌کند و period_typeهای MONTH، QUARTER، SEMI_ANNUAL، NINE_MONTH، ANNUAL و TTM دارد.

قرارداد معماری هدف:
- تاریخ‌های واقعی Jalali به‌عنوان authoritative components؛
- INSTANT در برابر DURATION؛
- months_length و fiscal_year/fiscal_quarter؛
- YTD فقط برای DURATION flow؛
- TTM و standalone مشتق‌شده runtime-only.

**شکاف:** مدل فعلی فیلدهای Jalali component و temporal shape/INSTANT را به‌صورت کامل پیاده نکرده و TTM را در catalog فعلی می‌پذیرد، در حالی که قرارداد هدف TTM را runtime-only می‌داند.

**نتیجه:** FinancialPeriod فعلی بدون اصلاح با قرارداد هدف Excel سازگار نیست. هیچ تاریخ Gregorian نباید به‌صورت حدسی از Jalali ساخته شود.

### 3.4 FinancialMetric

مدل فعلی دارای metric_code/name/category، industry_id، statement_type، value_type، flow_or_stock و sign_convention است.

**قابل استفاده مجدد:** هویت metric و بخشی از semantic constraints می‌توانند پایه catalog باشند.

**شکاف‌ها:** مدل فعلی value kind، unit/currency/basis expectation و تمام ابعاد مصوب را به‌صورت کافی/نسخه‌دار پوشش نمی‌دهد. نگاشت Source Header و Company Table Template نباید مستقیماً داخل FinancialMetric ادغام شوند.

**نتیجه:** catalog موجود قابل توسعه است، اما هنوز کل semantic contract را پیاده نمی‌کند.

### 3.5 NormalizedFinancialFact در برابر FinancialFact هدف

مدل فعلی NormalizedFinancialFact شامل:
- company_id، period_id، metric_id
- raw_fact_id و mapping_decision_id اختیاری
- value_irr از نوع Numeric(30,4)
- source_report_version_id
- normalization_rule_id
- quality_status
- unique(company_id, period_id, metric_id, source_report_version_id)

شکاف‌های اساسی:
1. مقدار ذخیره‌شده Numeric(30,4) است، در حالی که قرارداد هدف SQLite INTEGER با Decimal + ROUND_HALF_UP را مقرر کرده است.
2. کلید یکتا approved dimensions را شامل نمی‌شود؛ دو fact با یک metric/period ولی dimension متفاوت ممکن است به اشتباه با هم برخورد کنند.
3. نسخه دقیق extraction standard در fact یا رابطه اجباری قابل اثبات وجود ندارد.
4. source unit/currency/measurement basis و value state/origin به‌صورت کافی در خود مدل یا رابطه مشخص تعریف نشده‌اند.
5. raw_fact_id و mapping_decision_id به معماری قدیمی raw-row/mapping وابستگی ایجاد می‌کنند.
6. company_id تکراری باید با ReportVersion consistency کنترل شود؛ constraint فعلی این تطابق را به‌تنهایی اثبات نمی‌کند.
7. مدل فعلی value_irr فرض مقدار پولی Rial را دارد و برای quantity، rate، ratio یا سایر value kinds کافی نیست.

**نتیجه:** NormalizedFinancialFact می‌تواند موضوع بازطراحی به‌عنوان canonical fact table باشد، اما مدل فعلی را نمی‌توان بدون تغییر به‌عنوان مقصد آماده Excel انتخاب کرد. ساخت جدول دوم موازی نیز نباید بدون تصمیم فیزیکی و migration plan انجام شود.

### 3.6 Provenance bridge

NormalizedFinancialFactInput فعلی برای هر ورودی به raw_fact_id و mapping_decision_id غیرNULL نیاز دارد.

این الزام با هدف حذف دائمی raw rows و نگهداری حداقل provenance سازگار نیست. برای یک fact که از چند سلول/منبع مشاهده موقت ساخته می‌شود، provenance باید بتواند بدون ذخیره RawFinancialFact بیان شود؛ شکل دقیق آن هنوز طراحی نشده است.

**نتیجه:** این bridge در شکل فعلی نباید مقصد provenance مسیر Excel فرض شود. نیاز به بازطراحی جداگانه دارد؛ exact cell locator همچنان الزام عمومی ذخیره نیست.

### 3.7 Company Table Layout Template

پیشنهاد DB-DES-008 ساختار فیزیکی template، worksheet، layout node، range، header binding، column slot و extraction span را تعریف می‌کند؛ اما صراحتاً schema canonical FinancialFact و semantic mapping را خارج از دامنه می‌گذارد.

بنابراین template فقط مشخص می‌کند کدام محدوده/سلول‌ها از workbook مشاهده و استخراج شوند؛ به‌تنهایی مشخص نمی‌کند کدام metric، period، dimension، unit یا value state باید persist شود.

**نتیجه:** پیش از persistence باید template structural output به semantic/temporal/value interpretation استاندارد و نسخه‌دار متصل شود.

## 4. جمع‌بندی آمادگی

| موجودیت/لایه | وضعیت برای Excel target | اقدام لازم |
|---|---|---|
| Report | PARTIAL | ReportType catalog و semantics دوره اصلی |
| ReportVersion | PARTIAL / بهترین reuse | source artifact fingerprint و binding به standard/template version |
| FinancialPeriod | NOT READY | Jalali components و INSTANT/DURATION و قواعد fiscal |
| FinancialMetric | PARTIAL | تکمیل value kind/unit/basis و mapping boundary |
| NormalizedFinancialFact | NOT READY | INTEGER، dimensions، source value semantics، standard version و حذف وابستگی الزامی به RawFact |
| NormalizedFinancialFactInput | NOT READY | provenance بدون RawFinancialFact و MappingDecision اجباری |
| Company Table Layout Template | PROPOSED | approval، matcher و integration با semantic mapping |
| Excel Reader/DTO | IMPLEMENTED PARTIAL | observation reader موجود؛ persistence end-to-end احراز نشده |
| IngestionRun | PARTIAL | lifecycle اتمیک و metadata نسخه‌های adapter/standard بررسی شود |

## 5. تصمیم پیشنهادی

1. Report و ReportVersion را به‌عنوان پایه قابل reuse نگه داریم، نه اینکه از صفر مدل جایگزین بسازیم.
2. قبل از هر code/migration، مدل فیزیکی canonical FinancialFact را در یک DB-DES مستقل طراحی کنیم؛ انتخاب قطعی میان بازطراحی NormalizedFinancialFact و ساخت مدل جایگزین باید در همان design با مقایسه هزینه migration/compatibility انجام شود.
3. ReportVersion باید source artifact fingerprint و exact extraction/template standard version را حفظ کند.
4. FinancialPeriod فعلی باید با Jalali/INSTANT/DURATION contract تطبیق یابد.
5. provenance جدید نباید برای هر fact به RawFinancialFact یا cell archive وابسته باشد.
6. DB-DES-008 template ساختاری و semantic mapping نسخه‌دار باید جدا ولی با کلیدهای روشن به canonical fact متصل شوند.
7. هیچ داده، مدل، جدول، FK یا migration legacy در این مرحله حذف یا تغییر نکند.
8. تا زمانی که canonical target و end-to-end persistence طراحی و آزموده نشده، PDF production path قطع نشود.

## 6. موانع مستقل قبل از migration

- مغایرت Migration 9 دیتابیس محلی با runner مخزن همچنان باید حل شود.
- وضعیت واقعی schema و data تمام محیط‌های هدف باید پیش از migration معلوم باشد.
- DB-AUD-011/012 فقط وضعیت local snapshot و source مخزن را پوشش می‌دهند؛ نبود consumer بیرونی یا backup dependency اثبات نشده است.
- اجرای تست‌ها بر عهده مالک است؛ در این ممیزی هیچ تستی اجرا نشده است.

## 7. گام بعدی

تهیه DB-DES برای canonical FinancialFact physical model + provenance contract با پوشش:
- کلید یکتا شامل dimension identity؛
- ReportVersion/FinancialPeriod/Metric/standard-version links؛
- value kind و source unit/currency/basis/state؛
- provenance حداقلی بدون raw rows؛
- INTEGER storage و Decimal rounding؛
- atomic ingestion/idempotency/conflict;
- migration compatibility با مدل‌های موجود، بدون اجرای migration.

**وضعیت:** ممیزی آمادگی COMPLETE؛ مسیر Excel persistence هنوز NOT ESTABLISHED؛ هیچ کد، ORM، Migration، داده یا تست تغییر نکرده است.
