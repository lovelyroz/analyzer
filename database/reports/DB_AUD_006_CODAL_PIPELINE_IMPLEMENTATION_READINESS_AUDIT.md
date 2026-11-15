# DB-AUD-006 — ممیزی آمادگی مسیر CODAL برای پیاده‌سازی canonical

**تاریخ:** 2026-11-15  
**وضعیت:** PARTIAL — ممیزی هدفمند کد و اسناد؛ نه inventory کامل repository و نه بررسی DB واقعی  
**وابستگی:** DB-DES-001 تا DB-DES-006، DB-DES-005 و گزارش DB-AUD-001  
**دامنهٔ این نوبت:** مسیر CODAL در adapter/pipeline/service، DTO و writer، مدل‌های مرتبط، دوره، audit، migration runner و تست‌های موجود.  
**محدودیت شواهد:** فقط فایل‌های متنی/کد مخزن بررسی شدند. فایل XLSX منبع، CSV، پایگاه‌دادهٔ عملیاتی و محیط production بازبینی نشدند. تست اجرا نشد.

## 1. جمع‌بندی اجرایی

مسیر اجرایی CODAL موجود هنوز مسیر V1 موردنیاز نیست. کد فعال بررسی‌شده صریحاً PDF-oriented است، در حالی که دامنهٔ V1 مصوب Excel است. Adapter و pipeline فعلی PDF را استخراج می‌کنند، خروجی `RawLineInput` می‌سازند و `ingest_codal_report()` آن را به `RawFinancialFact` ذخیره می‌کند. این مسیر mapping ساختاری/معنایی نسخه‌دار، ساخت FinancialMetric/approved dimensions، تخصیص مستقل دوره به هر fact، canonical INTEGER، provenance نسخهٔ استاندارد و writer متصل به NormalizedFinancialFact را در خود ندارد.

در تست‌های موجود نیز مسیر end-to-end تست‌شده PDF→RawFinancialFact است. تست Stage 1 یک مسیر نمونهٔ دستی Raw→MappingDecision→NormalizedFinancialFact→NormalizedFinancialFactInput می‌سازد، اما این fixture/test construction اثبات اتصال production pipeline نیست.

**نتیجه:** شروع migration یا بازنویسی ORM در این مرحله زودهنگام است. ابتدا باید قرارداد ورودی Excel و مدل source observation در حافظه، mapping/period interpretation و canonical writer به‌صورت مستقل طراحی و سپس به‌صورت vertical slice پیاده‌سازی شوند. داده و جدول legacy فعلاً نباید حذف یا بازنویسی شوند.

## 2. فایل‌ها و محدودهٔ بررسی‌شده

| حوزه | فایل | آنچه بررسی شد |
|---|---|---|
| CODAL service | `src/ingestion/service.py` | `RawLineInput`، `ingest_codal_report`، transaction و replay |
| CODAL adapter | `src/ingestion/codal/adapter.py` | ورودی/خروجی PDF و وابستگی به PDF extractor |
| CODAL parser | `src/ingestion/codal/numbers.py` | تبدیل ارقام و `parse_amount` |
| CODAL tests | `src/tests/test_codal_extraction.py` | PDF extraction، PDF pipeline، raw persistence و version chain |
| Model | `src/models/normalized.py` | Raw/Metric/Mapping/Normalized/Derived model definitions |
| Report | `src/models/report.py` | Report و ReportVersion |
| Period | `src/models/period.py` | FinancialPeriod |
| Audit | `src/models/audit.py`، `src/ingestion/common/run_tracker.py` | IngestionRun و lifecycle helperها |
| PIT | `src/core/point_in_time.py` | انتخاب ReportVersion |
| Migration | `src/migrations/runner.py` | metadata imports و migrationهای 1–8 |
| Architecture | `12_Database_Architecture_V1.1.md` و DB-DES-001..006 | قرارداد هدف |

جست‌وجوی literal از طریق GitHub code search برای نام‌های تابع/مدل در این نوبت نتیجهٔ قابل اتکا برنگرداند؛ بنابراین از آن به‌عنوان اثبات نبود caller استفاده نشده است. فهرست callerها در این گزارش کامل تلقی نمی‌شود.

## 3. یافته‌های مستقیم مسیر CODAL

### 3.1 Adapter و pipeline فعلی PDF است

- `src/ingestion/codal/adapter.py` مستنداً PDF extraction boundary است و تابع `extract_raw_lines_from_pdf()` دارد.
- این adapter از `pdf_extract.extract_cell_rows` استفاده می‌کند و خروجی `CodalExtractionResult` شامل `Sequence[RawLineInput]` است.
- `src/tests/test_codal_extraction.py` از `load_codal_pdf` و PDFهای fixture استفاده می‌کند.
- در inventory فایل‌های ingestion بررسی‌شده، adapter یا pipeline متناظر CODAL Excel مشاهده نشد.
- این نتیجه محدود به فایل‌ها و tree بررسی‌شده است؛ پیش از ادعای نبود مطلق باید کل repository و import/runtime call sites تکمیل شوند.

**اثر:** پیاده‌سازی V1 باید Excel-first باشد. مسیر PDF موجود نباید به‌عنوان implementation منطبق با V1 تلقی شود یا مبنای گسترش دامنه قرار گیرد.

### 3.2 DTO فعلی برای canonical input کافی نیست

`RawLineInput` شامل item_name، value به‌صورت Decimal، item_code، unit، currency، source_section، source_row و source_column است. این DTO:
- identity استاندارد Header و نسخهٔ استاندارد را حمل نمی‌کند؛
- context کافی برای table/header hierarchy و row/column role را به‌صورت قراردادمند تعریف نمی‌کند؛
- FinancialMetric و approved dimensions ندارد؛
- temporal identity مستقل هر value را ندارد؛
- distinction صریح Actual/Forecast/Plan، INSTANT/DURATION، YTD و value state را ندارد؛
- provenance canonical و source revision identity را تعریف نمی‌کند.

وجود source_row/source_column در DTO فعلی نیز به‌معنی الزام به نگهداری دائمی locator نیست؛ قرارداد هدف چنین الزامی ندارد.

### 3.3 Writer فقط RawFinancialFact می‌سازد

در `ingest_codal_report()`:
1. IngestionRun با STARTED ایجاد و flush می‌شود.
2. FinancialPeriod با period_id دریافت و company_id آن با company ورودی مقایسه می‌شود.
3. Report با codal_tracking_id پیدا یا ساخته می‌شود.
4. در صورت وجود ReportVersion با publication_datetime برابر، تعداد RawFinancialFactها شمرده و Run به‌صورت COMPLETED با records_updated ثبت می‌شود؛ payload ورودی با payload موجود مقایسه نمی‌شود.
5. در غیر این صورت نسخهٔ جدید ReportVersion ساخته و current version قبلی غیرفعال می‌شود.
6. برای هر RawLineInput یک RawFinancialFact ساخته می‌شود.
7. ReportVersion، raw rows و COMPLETED Run commit می‌شوند.

در این تابع ساخت FinancialMetric، MappingDecision، NormalizedFinancialFact یا NormalizedFinancialFactInput مشاهده نشد. بنابراین این تابع writer canonical نیست.

### 3.4 Replay و failure lifecycle با DB-DES-005 تعارض دارند

- Replay بر اساس tracking ID و publication datetime یکسان short-circuit می‌کند، نه بر اساس source revision و canonical payload equality.
- replay می‌تواند ورودی جدید و متفاوت را بدون conflict comparison به‌عنوان records_updated گزارش کند.
- در exception، transaction rollback می‌شود و یک IngestionRun جدید FAILED ساخته و commit می‌شود؛ STARTED run اولیه rollback شده است.
- این رفتار با قاعدهٔ DB-DES-005 که حفظ همان Run و ثبت FAILED در transaction مستقل را می‌خواهد، سازگار نیست.
- exception متن کامل `str(exc)` را در error_log می‌نویسد؛ طراحی log باید مراقب عدم نشت payload مالی یا دادهٔ حساس source باشد.

### 3.5 هویت Report و period در سطح مدل محدود است

- `Report` دارای یک `financial_period_id` است، درحالی‌که قرارداد منطقی می‌گوید یک ReportVersion می‌تواند چند دوره و هر FinancialFact دورهٔ خودش را داشته باشد.
- `ingest_codal_report()` یک period_id برای کل فایل می‌گیرد و همان را به همهٔ RawFinancialFactها اختصاص می‌دهد.
- ReportVersion publication_datetime اجباری و is_restated دارد، اما audit status لازم برای ranking چهارسطحی DB-DES-001 در مدل ReportVersion مشاهده نشد.
- current-version pointer با is_current_version نگهداری می‌شود؛ این فیلد به‌تنهایی جایگزین PIT ranking مبتنی بر cutoff و چهار سطح priority نیست.
- `select_report_version()` در `src/core/point_in_time.py` بر اساس publication_datetime و version_number مرتب می‌کند؛ priority چهارسطحی در آن دیده نشد.

### 3.6 FinancialPeriod فعلی با قرارداد Jalali INSTANT/DURATION منطبق نیست

مدل `src/models/period.py`:
- start_date/end_date از نوع SQL Date (Gregorian representation) است؛
- period_type محدود به MONTH، QUARTER، SEMI_ANNUAL، NINE_MONTH، ANNUAL و TTM است؛
- is_ytd Boolean و months_length عددی دارد؛
- INSTANT/DURATION و Jalali start/end به‌صورت native در مدل مشاهده نشد؛
- TTM به‌عنوان period_type ذخیره‌پذیر است، درحالی‌که قرارداد DB-DES-003 آن را runtime-only می‌داند.

این گزارش راه‌حل migration یا تبدیل تاریخ پیشنهاد نمی‌کند؛ قبل از آن باید دادهٔ موجود و همهٔ consumerها بررسی شوند.

## 4. شکاف مدل‌های canonical و mapping

### 4.1 RawFinancialFact

مدل `raw_financial_facts` متن raw_item_name، raw_item_code، value Numeric(30,4)، unit/currency، source_section و source_row/source_column را نگه می‌دارد. این ساختار یک raw-row archive پایدار است و با سیاست هدف DB-DES-001/006 مبنی بر عدم نگهداری دائمی raw financial rows تعارض دارد.

بااین‌حال، تا وقتی دادهٔ موجود، مصرف‌کننده‌ها و migration path بررسی نشده‌اند، حذف جدول/مدل یا داده مجاز نیست.

### 4.2 NormalizedFinancialFact

مدل فعلی:
- value_irr از نوع Numeric(30,4) است، نه SQLite INTEGER canonical؛
- uniqueness برابر company_id + period_id + metric_id + source_report_version_id است و approved dimension identity را ندارد؛
- raw_fact_id و mapping_decision_id nullable هستند؛
- source unit/basis و canonical state/NULL semantics در خود fact به شکل قرارداد هدف کامل نیستند؛
- رابطهٔ شرکت/دوره/ReportVersion باید consistency قوی‌تری داشته باشد.

این مدل را نمی‌توان صرفاً با تغییر نام معادل FinancialFact هدف دانست. سازگاری یا جایگزینی آن نیازمند طراحی جداگانه و audit داده است.

### 4.3 MappingRule / MappingDecision

- MappingRule دارای rule_code، rule_version و is_active است.
- MappingDecision به raw_fact_id وابسته است و metric_id و mapping_rule_id می‌توانند nullable باشند.
- mapping_method فعلی شامل PATTERN و POSITION نیز هست؛ وجود این گزینه‌ها مجوز استفاده از fuzzy/positional guess در قرارداد جدید نیست.
- مدل‌ها به‌تنهایی structural Header dictionary، industry/report-family scope، exact standard version، temporal interpretation و approved dimension resolution را کامل بیان نمی‌کنند.
- تست Stage 1 این مدل‌ها را دستی می‌سازد؛ مسیر production CODAL بررسی‌شده آن‌ها را فراخوانی/ثبت نمی‌کند.

### 4.4 NormalizedFinancialFactInput و Derived*

تست Stage 1 نمونه‌ای از اتصال دو RawFinancialFact به یک NormalizedFinancialFact از طریق NormalizedFinancialFactInput می‌سازد. این نمونه یک الگوی test fixture است، نه شواهدی از writer تولیدی.

DerivedFinancialFact و DerivedFinancialFactInput در ORM تعریف شده‌اند و migration 2 جدول‌های آن‌ها را ایجاد می‌کند. طبق DB-DES-001/006 محاسبات downstream runtime-only هستند؛ اما پیش از retirement مدل/جدول باید کل consumer inventory و دادهٔ واقعی بررسی شود.

## 5. Migration و schema readiness

- Migration runner در `src/migrations/runner.py` نسخه‌های 1 تا 8 را دارد.
- Migration 1 از `Base.metadata.create_all` برای baseline استفاده می‌کند.
- Migration 2 ستون‌هایی به financial_metrics و normalized_financial_facts اضافه و mapping/derived tables را ایجاد می‌کند.
- Migration 3 جدول provenance مربوط به NormalizedFinancialFactInput را ایجاد می‌کند.
- Migration 7 جدول‌های LegacyForecast را می‌سازد و Migration 8 آن‌ها را drop می‌کند.
- migration runner مدل‌های Raw/Normalized/Derived/Mapping و Report/Period را import می‌کند تا metadata در دسترس باشد.
- هیچ migration اختصاصی برای انتقال RawFinancialFact به canonical FinancialFact یا اصلاح period semantics/INTEGER/dimensions در این مرحله طراحی نشده است.
- schema واقعی DBهای موجود، حجم/کیفیت داده، محیط‌ها، backupها و وضعیت migration هر DB قابل مشاهده نبود.

**نتیجه:** هنوز migration plan امن و قابل تصویب نداریم. migration 1–8 نباید بازنویسی شوند؛ هر اصلاح آینده باید forward-only و مبتنی بر schema/data inventory باشد.

## 6. تست‌های موجود و پوشش اثباتی

تست‌های خوانده‌شده مسیر PDF را پوشش می‌دهند: استخراج متن، NULL در برابر صفر در parser، ساخت ReportVersion و RawFinancialFact، acquisition/extraction failure و زنجیرهٔ نسخه‌ها. تست Stage 1 معماری mapping و provenance را با ساخت دستی رکوردها پوشش می‌دهد.

مواردی که از این تست‌ها اثبات نمی‌شوند:
- Excel adapter واقعی و cached values؛
- structural Header mapping نسخه‌دار؛
- Metric/dimension resolution از context؛
- تخصیص چند دوره به factهای یک ReportVersion؛
- INSTANT/DURATION و Jalali calendar semantics؛
- Decimal→INTEGER با ROUND_HALF_UP و signed 64-bit؛
- duplicate identity و payload conflict؛
- source revision و supersession؛
- ReportVersion + all facts + same Run atomicity و حفظ همان Run در failure؛
- PIT چهارسطحی با cutoff پیش از ranking؛
- عدم persistence raw rows و derived outputs؛
- end-to-end Excel→canonical facts→downstream consumer.

**تست اجرا نشد.** این بخش فقط پوشش قابل مشاهده در فایل‌های تست را توصیف می‌کند.

## 7. ماتریس اولویت شکاف‌ها

| اولویت | شکاف | پیامد | پیش‌نیاز اقدام |
|---|---|---|---|
| P0 | V1 Excel adapter/pipeline مشاهده نشد؛ مسیر فعلی PDF است | ورودی V1 هنوز وجود ندارد | قرارداد Excel source observation و adapter مستقل |
| P0 | CODAL writer فقط RawFinancialFact می‌نویسد | canonical facts تولید نمی‌شوند | طراحی canonical DTO/mapper/writer |
| P0 | replay payload comparison ندارد | overwrite/conflict خاموش ممکن است | source revision + canonical payload identity |
| P0 | failure Run اولیه حفظ نمی‌شود | audit lifecycle ناقص است | transaction boundary مطابق DB-DES-005 |
| P1 | یک period_id برای کل فایل | چنددوره‌ای واقعی پشتیبانی نمی‌شود | per-observation temporal assignment |
| P1 | Normalized model فاقد INTEGER/dimensions کامل است | uniqueness و canonical contract نقض می‌شود | تصمیم physical design پس از logical mapping |
| P1 | mapping مدل‌ها از production path جداست | وجود ORM به معنی mapping اجرایی نیست | mapping engine/use-case و versioned standards |
| P1 | ReportVersion status و selector چهارسطحی کامل نیست | PIT ranking نادرست/ناقص | Report status semantics و selector alignment |
| P2 | raw/derived legacy schema وجود دارد | خطر migration/retirement ناایمن | data inventory و consumer audit |
| P2 | migration/DB واقعی در دسترس نیست | مهاجرت قابل برآورد/تصویب نیست | schema snapshots، DB inventory و backup evidence |

## 8. توالی پیشنهادی قبل از migration

1. **تثبیت ورودی Excel:** قرارداد source observations در حافظه، فایل‌های مجاز، cached values، merged/header/table context و خطاهای parse؛ بدون persistence.
2. **طراحی canonical interpretation DTO:** هویت company/industry/report type، Standard Header، Metric، dimensions، period و value state/basis.
3. **تکمیل استانداردهای لازم بر اساس شواهد:** نه ساختن catalog همهٔ صنایع؛ فقط استانداردهایی که برای vertical slice واقعی لازم‌اند.
4. **طراحی canonical writer و transaction boundary:** ReportVersion + facts + provenance + same IngestionRun؛ payload-based idempotency/conflict.
5. **انتخاب یک vertical slice محدود و اثبات‌پذیر:** یک گزارش Excel واقعی با استاندارد مصوب و دوره/مقادیر قابل بررسی؛ بدون ادعای پوشش همهٔ بانک‌ها یا صنایع.
6. **تکمیل call-site و consumer inventory:** readerهای Forecast/KPI/Valuation و importهای dynamic/alias پیش از تغییر مدل.
7. **دریافت schema/data inventory از محیط‌های واقعی و طرح migration غیرمخرب:** تنها پس از مراحل فوق.

## 9. مواردی که هنوز اثبات نشده‌اند

- تمام callerها و importهای dynamic/alias برای CODAL و مدل‌های مرتبط؛
- تمام فایل‌های repository و تمام test modules؛
- schema و دادهٔ واقعی SQLite در محیط‌های توسعه/production؛
- حجم و کیفیت RawFinancialFact/NormalizedFinancialFact و وابستگی مصرف‌کنندگان؛
- فایل‌های واقعی Excel و نگاشت‌های دقیق سطر/ستون؛
- source revision/fingerprint semantics واقعی CODAL؛
- اجرای transaction تحت concurrency و crash recovery.

## 10. نتیجه و معیار خروج

DB-AUD-006 در این نوبت **PARTIAL** باقی می‌ماند. این ممیزی برای رد ادعای آمادگی implementation فعلی کافی است، اما برای تصویب migration یا حذف مدل legacy کافی نیست.

خروج از این Task مستلزم تکمیل inventory call-siteها، دریافت schema/data inventory از محیط واقعی، شواهد Excel مجاز، و یک طرح forward-only غیرمخرب است. تا آن زمان:
- هیچ raw/normalized/derived table حذف نشود؛
- هیچ داده‌ای overwrite یا backfill نشود؛
- migration تاریخی تغییر نکند؛
- مسیر PDF به‌عنوان مسیر V1 Excel معرفی نشود.

**تست اجرا نشد؛ هیچ کد، ORM، schema، migration یا داده‌ای در این Task تغییر نکرد.**
