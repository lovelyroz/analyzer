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


## 11. تکمیل محدود ممیزی مرز Transaction در کدهای موجود — 2026-11-18

**دامنهٔ این تکمیل:** بازخوانی مستقیم چهار فایل اجرایی/کمکی و یک مجموعه تست؛ این بخش inventory کامل repository یا call-siteها نیست.

فایل‌های بازبینی‌شده:
- `src/ingestion/service.py`
- `src/ingestion/market/ingestion.py`
- `src/ingestion/fx/ingestion.py`
- `src/ingestion/common/run_tracker.py`
- `src/tests/test_codal_extraction.py`

### 11.1 CODAL — `ingest_codal_report`

- Run با وضعیت STARTED به Session اضافه و flush می‌شود، اما پیش از پردازش در transaction مستقل commit نمی‌شود.
- در مسیر موفق، Report/ReportVersion، تمام RawFinancialFactها و COMPLETED شدن همان Run با یک `session.commit()` ثبت می‌شوند؛ این بخش از نظر موفقیت یک مرز transaction مشترک دارد، اما STARTED مستقل و پایدار نیست.
- در exception، کل Session rollback می‌شود؛ بنابراین Run اولیه نیز از بین می‌رود. سپس یک IngestionRun جدید با وضعیت FAILED ساخته و commit می‌شود. این رفتار با DB-DES-005 که حفظ همان Run را لازم می‌داند، منطبق نیست.
- replay بر اساس Report و publication_datetime تشخیص داده می‌شود؛ payload ورودی با payload ذخیره‌شده مقایسه نمی‌شود. در نتیجه، اجرای دوباره با محتوای متفاوت می‌تواند بدون conflict به مسیر COMPLETED برسد و تعداد RawFinancialFactهای موجود را به‌عنوان `records_updated` گزارش کند.
- `str(exc)` مستقیماً در `error_log` قرار می‌گیرد؛ sanitization خطا اثبات نشده است.

### 11.2 Market/OHLC — `ingest_ohlc_csv`

- Run ابتدا STARTED و flush می‌شود؛ commit نهایی، رکوردهای MarketDaily و وضعیت Run را با هم ثبت می‌کند.
- خطاهای parse، OHLC نامعتبر و شرکت ناشناخته به‌صورت ردیفی شمرده و از حلقه عبور داده می‌شوند؛ ردیف‌های معتبر دیگر همچنان ذخیره می‌شوند و Run با وضعیت COMPLETED حتی در صورت `records_failed > 0` commit می‌شود. این رفتار با قاعدهٔ رد کل Ingestion Unit در DB-DES-005 تعارض دارد.
- رکورد موجود با هویت شرکت و تاریخ جلالی update می‌شود؛ در این مسیر، source revision یا payload conflict بررسی نمی‌شود.
- در exception، Session rollback و Run جدید FAILED ساخته می‌شود؛ Run اولیه حفظ نمی‌شود. شمارنده‌های Run شکست‌خورده نیز صفر ثبت می‌شوند، حتی اگر parsing پیش از exception انجام شده باشد.

### 11.3 FX — `ingest_fx_rates` و adapter facade

- `src/ingestion/fx/ingestion.py` فایل XLSX را به DTO تبدیل می‌کند و سپس writer مشترک `ingest_fx_rates` را فراخوانی می‌کند؛ در facade مشاهده‌شده transaction مستقلی وجود ندارد.
- writer برای هر ورودی نامعتبر خطا را جمع می‌کند و به پردازش ورودی‌های بعدی ادامه می‌دهد؛ ورودی‌های معتبر می‌توانند persist شوند و Run با وضعیت COMPLETED، حتی با `records_failed > 0`، commit شود. این رفتار نیز با fail-whole-unit در DB-DES-005 ناسازگار است.
- رکورد موجود بر اساس هویت فعلی FX پیدا و مقدار/منبع آن overwrite می‌شود؛ source revision و payload conflict در این مسیر بررسی نمی‌شوند.
- در exception، Session rollback و Run جدید FAILED ثبت می‌شود؛ STARTED اولیه حفظ نمی‌شود. exception خام نیز در error_log نوشته می‌شود.

### 11.4 Shared run tracker

- `start_run` فقط add/flush انجام می‌دهد.
- `complete_run` فقط فیلدهای همان Run را تغییر می‌دهد و commit ندارد.
- `fail_run` یک Run جدید می‌سازد و خودش `session.commit()` اجرا می‌کند؛ بنابراین اگر از داخل serviceای با transaction فعال فراخوانی شود، می‌تواند transaction ownership را از service خارج کند.
- GitHub code search برای یافتن call-siteهای این helperها و writerها در این نوبت نتیجه‌ای برنگرداند؛ بنابراین استفاده/عدم استفادهٔ آن‌ها در تمام repository اثبات نشده است.

### 11.5 شواهد تست و نتیجهٔ crosswalk

تست‌های خوانده‌شده در `test_codal_extraction.py` مسیر PDF→RawFinancialFact و برخی خطاهای acquisition/extraction را پوشش می‌دهند. این تست‌ها به‌تنهایی موارد زیر را اثبات نمی‌کنند: حفظ همان Run در failure، rollback کل batch پس از خطای یک ردیف، payload-based replay/conflict، concurrency، canonical Excel writer یا atomicity کامل مطابق DB-DES-005. تستی اجرا نشد.

**نتیجه:** در سه writer بازبینی‌شده (CODAL، OHLC و FX)، چند تعارض مستقیم با DB-DES-005 مشاهده شد؛ به‌ویژه دوام STARTED Run، ثبت FAILED روی همان Run و رد کامل batch در برابر خطای سخت. این یافته‌ها برای اثبات عدم انطباق همین مسیرهای بازبینی‌شده کافی‌اند، اما به معنی inventory کامل تمام ingestion call-siteها نیستند.

**وضعیت:** DB-DES-005 / Task 010 و DB-AUD-006 / Task 027 همچنان PARTIAL. این تکمیل صرفاً مستنداتی است؛ هیچ کد، ORM، schema، migration، دیتابیس یا داده‌ای تغییر نکرد و هیچ تستی اجرا نشد. گام بعدی برای بستن ممیزی، تکمیل inventory تمام callerها و transaction/session boundaries از روی repository tree و سپس دریافت schema/data inventory مجاز از محیط‌های واقعی است.

## 12. تکمیل Repository Inventory و اصلاح دامنهٔ نتیجه‌گیری بخش 11 — 2026-11-18

### 12.1 دامنه و روش
کاربر inventory محلی تمام فایل‌های Python زیر `src/` و خروجی جست‌وجوی عبارت‌های ingestion و transaction را ارائه کرد. inventory شامل مسیرهای core، CODAL، FX، Market، common، scripts و tests است. سپس wrapperها، pipelineها، writer مرکزی، run tracker و تست‌های مرتبط مستقیماً از مخزن بازبینی شدند. این بررسی static بود؛ هیچ تستی اجرا نشد.

### 12.2 نقشهٔ callerها و wrapperها
- `src/ingestion/codal/ingestion.py::ingest_codal_report` صرفاً facade سازگاری است و به `src/ingestion/service.py::ingest_codal_report` delegate می‌کند؛ transaction مستقل ندارد.
- `src/ingestion/codal/ingestion.py::ingest_codal_pdf` extraction را اجرا می‌کند و سپس به facade بالا می‌رسد. در extraction failure، Session را rollback و یک Run جدید FAILED commit می‌کند؛ پیش از extraction یک Run پایدار STARTED ایجاد نمی‌کند.
- `src/ingestion/codal/pipeline.py::load_codal_pdf` و `load_codal_pdf_from_url` acquisition، extraction و validation را پیش از فراخوانی writer مرکزی اجرا می‌کنند. `_audit_failed_run` در failure یک Run جدید FAILED می‌سازد؛ pipeline پیش از acquisition/extraction یک Run پایدار STARTED ایجاد نمی‌کند.
- `src/ingestion/service.py::ingest_codal_report` writer اصلی Report/ReportVersion/RawFinancialFact است. این تابع Run را STARTED و flush می‌کند؛ در success همان Run و writes را commit می‌کند. در exception، transaction را rollback و Run اولیه را از بین می‌برد، سپس Run جدید FAILED می‌سازد و commit می‌کند.
- `src/ingestion/service.py::ingest_ohlc_csv` فقط facade به `src/ingestion/market/ingestion.py::ingest_ohlc_csv` است.
- `src/ingestion/fx/ingestion.py::ingest_fx_xlsx` و `src/ingestion/service.py::ingest_fx_xlsx` هر دو adapter را به `ingest_fx_rates` وصل می‌کنند؛ writer persistence در `src/ingestion/service.py` است.
- در inventory ارسالی، `start_run`، `complete_run` و `fail_run` فقط در تعریف‌های `src/ingestion/common/run_tracker.py` ظاهر شده‌اند؛ call-site/import مصرف‌کننده‌ای در `src/` مشاهده نشد. بنابراین این helperها فعلاً مسیر اجرایی اثبات‌شده نیستند و نباید در نقشهٔ runtime به‌عنوان caller فعال شمرده شوند.

### 12.3 دامنهٔ دقیق یافته‌های transaction و اصلاح بخش 11
1. عدم حفظ همان Run پس از rollback در writer مرکزی CODAL مشاهده شد: Run اولیه STARTED rollback می‌شود و Run تازه FAILED ساخته می‌شود.
2. در CODAL acquisition/extraction/validation wrappers، Run پایدار STARTED قبل از این مراحل ایجاد نمی‌شود؛ در failure صرفاً Run جدید FAILED ثبت می‌شود. این نیز با lifecycle هدف DB-DES-005 فاصله دارد، اما از نظر توالی با rollback یک Run اولیه یکسان نیست.
3. writerهای FX و OHLC نیز در کد خود Run ایجاد می‌کنند، در success commit می‌کنند و در exception پس از rollback Run جدید FAILED می‌سازند. FX و OHLC ورودی‌های نامعتبر را ردیفی جمع می‌کنند و ممکن است ورودی‌های معتبر دیگر را همراه COMPLETED و `records_failed > 0` commit کنند.
4. **اصلاح دامنه:** DB-DES-005 قرارداد ingestion مالی CODAL است. رفتار ردیفی FX/OHLC و upsertهای آن‌ها در این گزارش به‌عنوان رفتار مشاهده‌شده ثبت می‌شود، نه نقض اثبات‌شدهٔ DB-DES-005. برای قضاوت دربارهٔ مطلوب/نامطلوب بودن آن‌ها، قرارداد atomicity و revision مستقل FX و Market لازم است.
5. CODAL replay با کلید `(codal_tracking_id, publication_datetime)` نسخهٔ موجود و facts آن را دوباره استفاده می‌کند و payload ورودی جدید را با payload ذخیره‌شده مقایسه نمی‌کند. تست corpus موجود سه چرخهٔ تکراری با همان استخراج/ورودی را برای عدم duplication و عدم drift بررسی می‌کند؛ این تست، سناریوی همان کلید با payload متفاوت را پوشش نمی‌دهد. بنابراین replay یکسان از نظر دادهٔ تکراری تست شده، اما replay متعارض از نظر payload همچنان بدون guard اثبات‌شده است.
6. در مسیر CODAL، خطاهای acquisition/extraction/validation پیش از writer و خطاهای persistence داخل writer به Runهای FAILED منجر می‌شوند؛ اما Run lifecycle هدف که یک STARTED پایدار را پیش از کل پردازش ایجاد و همان Run را نهایی کند، در مسیرهای مشاهده‌شده پیاده نشده است.

### 12.4 وضعیت inventory و محدودیت باقی‌مانده
خروجی محلی، فهرست تمام فایل‌های `*.py` زیر `src/` و تمام matchهای الگوی انتخاب‌شده در همان فایل‌ها را نشان می‌دهد؛ این برای inventory جست‌وجوشده در `src/` شواهد قوی‌تری از جست‌وجوی قبلی GitHub است. با این حال، این روش callهای پویا، reflection، entrypointهای خارج از `src/`، ابزارهای اجرایی بیرونی یا استفاده از SQL مستقیم بدون واژه‌های جست‌وجوشده را اثبات/رد نمی‌کند. بنابراین ادعای «تمام callerهای repository» فراتر از شواهد خواهد بود.

**نتیجهٔ اصلاح‌شده:** Task 010 / DB-DES-005 برای مسیر CODAL همچنان PARTIAL است؛ مهم‌ترین شکاف‌های مشاهده‌شده، پایدار نبودن Run در تمام مراحل acquisition-to-persistence، ایجاد Run جدید به‌جای حفظ همان Run در failure، و نبود payload-conflict check برای replay با همان identity هستند. رفتار FX/OHLC خارج از حکم انطباق DB-DES-005 نگه داشته می‌شود. Task 027 / DB-AUD-006 نیز به علت نبود schema/data inventory از محیط واقعی و محدودیت‌های فوق PARTIAL می‌ماند.

**تغییرات:** فقط همین سند ممیزی و Master Working Packet مستنداتی به‌روزرسانی می‌شوند. هیچ کد، ORM، schema، migration، دیتابیس یا داده‌ای تغییر نکرد و تستی اجرا نشد.
## 13. Crosswalk با ممیزی‌های قبلی دیتابیس و جلوگیری از تکرار کار — 2026-11-18

بازخوانی Master Working Packet پس از دریافت inventory محلی نشان می‌دهد بخش مهمی از schema/data و dependency auditها پیش‌تر انجام شده‌اند و نباید دوباره درخواست/اجرا شوند:

- **DB-AUD-011 / Master §8.44:** row-linkage دیتابیس محلی برای 505 `raw_financial_facts` انجام شد؛ سه جدول `mapping_decisions`، `normalized_financial_fact_inputs` و `normalized_financial_facts` در همان snapshot فاقد ردیف و فاقد ارجاع بودند.
- **DB-AUD-015 / Master §8.52:** هر چهار جدول Normalized/Derived در همان دیتابیس محلی صفر ردیف داشتند؛ referenceهای بررسی‌شده صفر، duplicate input-link groups صفر و `PRAGMA foreign_key_check` بدون violation بود.
- **Migration 9 / Master §8.64:** آثار قابل‌مشاهدهٔ migration 9 در دیتابیس محلی audit و cleanup شد؛ دو ستون اضافی و ledger row حذف شدند، 505 raw facts حفظ شدند و audit پس از cleanup موفق بود. implementation اصلی migration 9 و side effectهای ناشناخته تاریخی همچنان قابل اثبات نیستند.
- **DB-AUD-012 / Master §§8.45–8.46:** inventory وابستگی PDF در working tree کامل شد؛ 5,611 فایل اسکن، 26 فایل دارای match و مرز PDF-only/shared/schema/test مشخص شد.
- **DB-AUD-013 / Master §8.48:** gap audit آمادگی persistence اکسل انجام شد و نتیجه داد مسیر production Excel-to-canonical هنوز وجود ندارد؛ `NormalizedFinancialFact` مقصد آماده محسوب نمی‌شود.
- **DB-PLAN-013 / Master §8.47:** طرح مرحله‌ای بازنشستگی PDF تدوین شد؛ شرط اصلی آن ساخت و اثبات مسیر Excel persistence پیش از قطع مسیر PDF است.

بنابراین عبارت بخش 12 مبنی بر اینکه schema/data inventory محلی هنوز انجام نشده، بیش از حد کلی بود. **ممیزی‌های هدفمند فوق برای snapshot محلی انجام شده‌اند**؛ آنچه هنوز اثبات نشده، وضعیت سایر محیط‌ها/backupها و مصرف‌کنندگان بیرون از working tree بررسی‌شده است. این گزارش درخواست تکرار آن ممیزی‌های محلی را نمی‌دهد.

**مسیر بعدی پروژه:** ادامهٔ Phase 0 از DB-PLAN-013 و بستن gateهای طراحی DB-DES-009 است؛ نه تکرار PDF dependency audit، RawFact linkage یا Normalized/Derived local linkage. اولین gate اجرایی-مستندی که باید بسته شود، inventory تمام مصرف‌کنندگان `reports.financial_period_id` پیش از nullable کردن/جابه‌جایی آن است. سپس gateهای ReportVersion source revision/standard binding، dimension scope، company-consistency و provenance granularity به‌ترتیب بررسی می‌شوند.

هیچ کد، ORM، schema، migration، دیتابیس یا داده‌ای در این crosswalk تغییر نکرد و تستی اجرا نشد.

## 14. بررسی مصرف‌کنندگان `reports.financial_period_id` و مسیرهای فراخوانی CODAL — 2026-11-18

### 14.1 تفکیک شناسه‌های هم‌نام
خروجی جست‌وجوی محلی کاربر برای `financial_period_id|FinancialPeriod` در کل فایل‌های `*.py` و `*.sql` زیر repository، موارد زیر را نشان داد:
- `src/models/report.py`: ستون `Report.financial_period_id` با `nullable=False` و FK به `financial_periods.period_id`.
- `src/ingestion/service.py`: writer مرکزی CODAL، هم period شرکت را validate می‌کند و هم شناسه را در Report و تمام RawFinancialFactهای نسخهٔ گزارش می‌نویسد.
- `src/forecast/queries.py`: query تولیدی Forecast، دوره را از `NormalizedFinancialFact.period_id` به `FinancialPeriod` join می‌کند؛ در این query از `Report.financial_period_id` استفاده نشده است.
- `src/evaluation/*` و بسیاری از تست‌های Stage 5/6: نام `financial_period_id` در DTOها و مدل‌های ارزیابی به‌عنوان شناسهٔ دورهٔ observation/forecast استفاده شده است؛ این موارد به‌تنهایی مصرف ستون `reports.financial_period_id` نیستند.
- تست‌های Stage 1 و CODAL، ساخت Report و قرارداد قدیمی را با `financial_period_id` اجباری می‌آزمایند؛ تست‌های PDF نیز رابطهٔ Report با FinancialPeriod را assert می‌کنند.

### 14.2 مسیرهای فراخوانی مشاهده‌شده
بررسی فایل‌های کامل زیر:
- `src/ingestion/codal/ingestion.py`: تابع عمومی `ingest_codal_report` یک facade سازگار با گذشته است و به `src.ingestion.service.ingest_codal_report` delegate می‌کند. تابع `ingest_codal_pdf` پس از extraction همین facade را فراخوانی می‌کند.
- `src/ingestion/codal/pipeline.py`: توابع `load_codal_pdf` و `load_codal_pdf_from_url` پس از acquisition/extraction/validation، writer مرکزی `src.ingestion.service.ingest_codal_report` را فراخوانی می‌کنند.
- `src/ingestion/excel/reader.py` و `src/ingestion/excel/dto.py`: در نسخهٔ بررسی‌شده، reader/DTO اکسل هیچ فراخوانی writer CODAL و هیچ ارجاعی به `financial_period_id` ندارند؛ این با یافتهٔ قبلی DB-AUD-013 مبنی بر نبود production Excel-to-canonical persistence هم‌راستا است.
- تست‌های `test_codal_extraction.py`، `test_codal_pdf_extraction.py` و تست‌های Stage 1 مستقیماً writer یا مدل Report را با قرارداد فعلی می‌آزمایند.

این بررسی یک نقشهٔ محدود و مبتنی بر فایل‌های کامل نام‌برده و خروجی جست‌وجوی محلی است؛ به علت ناموفق بودن GitHub code search و محدودیت inventory بیرون از `src/`، ادعای اثبات تمام call-siteهای پویا یا بیرونی نمی‌شود.

### 14.3 نتیجهٔ معماری برای gate فعلی
1. `Report.financial_period_id` در حال حاضر یک فیلد الزامی و بخشی از قرارداد writer قدیمی CODAL است؛ حذف یا nullable کردن آن بدون جایگزینی قرارداد legacy باعث شکستن مسیر موجود و تست‌های مربوط می‌شود.
2. writer فعلی یک `period_id` واحد می‌گیرد و آن را به تمام `RawFinancialFact`های یک ReportVersion نسبت می‌دهد. این رفتار برای ورودی Excel چندستونی/چنددوره‌ای قابل تعمیم نیست و نباید به‌عنوان قرارداد ingestion جدید حفظ شود.
3. `RawFinancialFact.period_id` و `NormalizedFinancialFact.period_id` دورهٔ هر Fact را نگه می‌دارند؛ Forecast نیز از دورهٔ Normalized Fact استفاده می‌کند. این شواهد از مدل fact-level period پشتیبانی می‌کنند.
4. بنابراین مسیر جدید Excel باید writer/contract مستقل یا نسخهٔ توسعه‌یافته‌ای داشته باشد که برای هر Fact دورهٔ خودش را دریافت و اعتبارسنجی کند. `Report.financial_period_id` تا زمان تعیین تکلیف و بازنشستگی کنترل‌شدهٔ مسیر legacy باید حفظ شود؛ اگر در مدل نهایی باقی بماند، نقش آن باید صرفاً metadata دورهٔ اصلی/نمایشی گزارش باشد و نباید مرجع دورهٔ مقادیر تلقی شود.
5. هنوز دربارهٔ nullable شدن نهایی ستون، migration، backfill یا تغییر ORM تصمیم اجرایی گرفته نشده است. تصمیم به این موارد موکول به تکمیل gateهای DB-DES-009 و طراحی coexistence/retirement مسیر legacy است.

**وضعیت این گام:** شواهد لازم برای تفکیک مسیر legacy CODAL از نیاز جدید Excel به‌دست آمده، اما gate کامل inventory مصرف‌کنندگان repository-wide هنوز به‌دلیل محدودیت‌های بالا «محدود/مشروط» است. هیچ کد، ORM، schema، migration، دیتابیس یا داده‌ای تغییر نکرد و هیچ تستی اجرا نشد.


## 14. تکمیل بررسی Report.financial_period_id و مرز writer قدیمی — 2026-11-18

در ادامهٔ Gate 5 از DB-DES-009، فایل‌های `src/ingestion/service.py`، `src/ingestion/codal/ingestion.py`، `src/ingestion/codal/pipeline.py` و `src/models/report.py` مستقیماً بازبینی شدند.

یافته‌های قطعی:
- تنها writer مرکزی CODAL که در این مسیر مشاهده شد `src/ingestion/service.py::ingest_codal_report` است؛ facade در `codal/ingestion.py` به همین تابع delegate می‌کند و pipeline نیز همین writer را صدا می‌زند.
- ورودی writer یک `period_id` اجباری دارد. تابع FinancialPeriod را load می‌کند و company_id را تطبیق می‌دهد.
- برای Report موجود، company_id و `Report.financial_period_id` با ورودی مقایسه می‌شوند؛ اختلاف باعث رد عملیات می‌شود.
- برای Report جدید، `financial_period_id=period_id` ثبت می‌شود.
- همان `period_id` به تمام RawFinancialFactهای ساخته‌شده برای ReportVersion داده می‌شود.
- مدل Report نیز این ستون را `nullable=False` تعریف می‌کند.
- facade و pipeline هر دو پارامتر period_id را عبور می‌دهند؛ pipeline فعلی PDF-oriented است.
- GitHub code search در این نوبت callerهای بیرونی/سایر فایل‌ها را برنگرداند؛ بنابراین inventory کامل callerها هنوز از این بررسی حاصل نشده است.

نتیجهٔ معماری:
1. period در سطح هر Fact باید مرجع temporal identity باشد؛ یک period واحد نباید به تمام مقادیر یک workbook چنددوره‌ای تحمیل شود.
2. حذف یا nullable کردن ستون Report اکنون مجاز نیست؛ legacy writer به آن وابستگی اجرایی و هویتی دارد.
3. تغییر قرارداد باید با تفکیک writer legacy و writer جدید Excel انجام شود؛ نه با تغییر ناگهانی امضای تابع مشترک.
4. نقش نهایی Report.financial_period_id (حذف تدریجی، nullable و descriptive، یا جایگزینی با primary-period metadata) پس از inventory کامل call-siteها و physical design تعیین می‌شود.

محدودیت: این بررسی static و read-only بود؛ تست اجرا نشد و هیچ کد، ORM، schema، migration یا دیتابیسی تغییر نکرد.


## 15. تکمیل inventory ایستا در فایل‌های Python برای Gate 5 — 2026-11-18

پس از اصلاح دستور PowerShell، خروجی جست‌وجوی تمام فایل‌های *.py در repository (با حذف .git، محیط‌های مجازی و __pycache__) بررسی شد. این خروجی دامنهٔ فایل‌های Python را پوشش می‌دهد؛ نه فایل‌های غیر Python، کدهای خارج از repository یا فراخوانی‌های پویا در زمان اجرا.

نتایج مرتبط:
- تعریف و پیاده‌سازی writer مرکزی: src/ingestion/service.py::ingest_codal_report.
- API سازگاری src/ingestion/codal/ingestion.py::ingest_codal_report به writer مرکزی delegate می‌کند؛ ingest_codal_pdf نیز پس از استخراج آن API را صدا می‌زند.
- src/ingestion/codal/pipeline.py، تابع‌های load_codal_pdf و load_codal_pdf_from_url را دارد و هر دو مسیر در نهایت writer مرکزی را فراخوانی می‌کنند.
- src/ingestion/__init__.py و src/ingestion/codal/__init__.py توابع را export می‌کنند؛ export به‌تنهایی caller اجرایی محسوب نمی‌شود.
- جست‌وجوی financial_period_id کاربردهای جداگانه‌ای در src/evaluation نشان داد. در فایل‌های بازبینی‌شده، این شناسه در DTOها و قراردادهای observation/evaluation به دورهٔ داده اشاره دارد؛ نباید صرفاً به‌دلیل یکسان بودن نام، آن را مصرف ستون Report.financial_period_id تلقی کرد.
- در خروجی جست‌وجو، ارجاع‌های تستی به writer و ساخت Report با period نیز وجود دارد؛ این‌ها قراردادهای آزمون/سازگاری را نشان می‌دهند، نه caller تولیدی مستقل.

### نتیجهٔ Gate 5 پس از این گام
در محدودهٔ کدهای Python زیر src/ که با جست‌وجو و بازبینی فایل‌های مرتبط بررسی شدند، وابستگی اجرایی مستقیم ستون Report.financial_period_id در writer قدیمی متمرکز است؛ facadeها و pipelineهای PDF آن را از طریق همان writer به ارث می‌برند. مصرف‌کنندهٔ تولیدی مستقلی که جداگانه این ستون را بخواند، از شواهد این خروجی احراز نشد. این نتیجه را نباید به تمام محیط‌ها، اسکریپت‌های بیرونی، SQL یا فراخوانی‌های پویا تعمیم داد.

**تصمیم فعلی بدون تغییر:** ستون و قرارداد legacy دست‌نخورده می‌مانند. طراحی writer اکسل باید period هر observation/fact را مستقل تعیین کند و نباید period واحد Report را به همهٔ factها تعمیم دهد. تعیین نقش نهایی ستون Report و هرگونه nullable/remove فقط پس از بررسی وابستگی‌های باقی‌مانده و طراحی coexistence/retirement انجام می‌شود.

این گام فقط جست‌وجو و بازبینی ایستا بود؛ هیچ کد، ORM، schema، migration، دیتابیس یا داده‌ای تغییر نکرد و تستی اجرا نشد.


## 16. بررسی ایستای فایل‌های غیر Python برای Gate 5 — 2026-11-19

کاربر جست‌وجوی repository-wide را در فایل‌های غیر Python شامل SQL، Markdown، اسکریپت‌ها و فایل‌های پیکربندی اجرا و خروجی را در `reply.md` ثبت کرد. الگوی جست‌وجو شامل `financial_period_id`، `reports.financial_period_id`، `financial_periods` و نام writerها و loaderهای قدیمی CODAL بود.

نتیجهٔ تفکیک مسیرهای منطبق:
- مسیرهای منطبقِ غیر Python که در خروجی قابل شناسایی بودند، همگی مستندات Markdown بودند: گزارش‌های DB-AUD/DB-DES/DB-PLAN/DB-STD، Master Working Packet، مستندات Stage، دستورالعمل handoff و implementation status.
- هیچ فایل SQL یا اسکریپت اجرایی غیر Python در فهرست مسیرهای منطبق مشاهده نشد.
- ارجاع‌های مستنداتی به `financial_period_id`، `ingest_codal_report` و `financial_periods` توصیف قراردادها و تصمیم‌های معماری‌اند و به‌تنهایی مصرف‌کنندهٔ اجرایی ستون `reports.financial_period_id` محسوب نمی‌شوند.
- اسناد معماری هدف، از جمله `DB_DES_009_CANONICAL_FINANCIAL_FACT_PHYSICAL_MODEL.md` و `12_Database_Architecture_V1.1.md`، period در سطح Fact را مرجع دورهٔ مقدار می‌دانند و period در سطح Report را metadata توصیفی/اصلی تلقی می‌کنند؛ این تصمیم طراحی، وابستگی writer legacy موجود را حذف نمی‌کند.

محدودیت مهم خروجی: دستور جست‌وجو فایل مقصد `reply.md` را از دامنهٔ جست‌وجو خارج نکرده بود؛ بنابراین بخشی از خروجی شامل بازجست‌وجوی محتوای قبلی و تکرار نتایج است. مسیرهای تکراری `reply.md` به‌عنوان شاهد مستقل شمرده نشدند. این ممیزی فقط static search در working tree و فایل‌های متنیِ مشمول الگوی دستور است و فراخوانی پویا، فایل‌های خارج از repository، داده‌های runtime یا مصرف‌کنندگان بیرونی را اثباتاً پوشش نمی‌دهد.

### نتیجهٔ Gate 5 پس از بررسی غیر Python

در شواهد فعلی، مصرف‌کنندهٔ اجرایی مستقل دیگری برای ستون `Report.financial_period_id` از فایل‌های غیر Python احراز نشد؛ شواهد اجرایی مستقیم همچنان به writer قدیمی CODAL و facade/pipelineهای متصل به آن محدود است. این نتیجه، به‌معنای اثبات نبود هرگونه مصرف‌کننده در تمام محیط‌ها نیست.

**تصمیم بدون تغییر:** ستون و قرارداد legacy فعلاً حفظ می‌شوند. writer جدید Excel باید دوره را برای هر observation/fact تعیین کند. nullable/remove یا تغییر نقش ستون Report تا تکمیل بررسی callerهای بیرونی و طرح coexistence/retirement مجاز نیست. این گام read-only بود؛ هیچ کد، ORM، schema، migration، دیتابیس یا داده‌ای تغییر نکرد و تستی اجرا نشد.
