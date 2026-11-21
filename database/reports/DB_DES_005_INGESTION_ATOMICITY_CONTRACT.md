> **HISTORICAL / SUPERSEDED — 2026-11-21:** PDF-path observations and plans in this document describe the retired implementation and do not define current support or acceptance. File inputs are Excel/CSV only. See database/reports/DB_CODAL_RETIRE_001_EXCEL_CSV_ONLY_RETIREMENT.md.

# DB-DES-005 — قرارداد IngestionRun، تراکنش و Atomicity

**تاریخ:** 2026-11-15  
**وضعیت:** قرارداد منطقی اولیه — PARTIAL تا زمان تطبیق کامل با سرویس‌ها، مدل audit و تست‌ها  
**دامنه:** مرز پردازش یک واحد ورودی، ثبت audit، اعتبارسنجی، persistence اتمیک، idempotency، retry و failure handling برای CODAL، Market، FX و ورودی‌های آتی Share/CorporateAction.

## 1. هدف و اصل حاکم

هر واحد ورودی یا به‌طور کامل پذیرفته و ثبت می‌شود یا هیچ canonical write از آن باقی نمی‌ماند. ثبت سابقهٔ شکست در IngestionRun مجاز و مطلوب است، اما رکورد شکست‌خورده نباید بخشی از دادهٔ تحلیلی/Canonical شود.

سه لایه جدا هستند:
1. Acquisition/parsing: خواندن فایل یا feed و ساخت DTO؛ بدون نوشتن canonical.
2. Validation/admission: احراز هویت منبع، پروفایل، شرکت، صنعت، تاریخ، واحد، مقدار، کلید منطقی و duplicate/conflict.
3. Persistence transaction: ثبت تمام رکوردهای پذیرفته‌شدهٔ همان واحد به‌همراه وضعیت نهایی موفق IngestionRun در یک transaction.

## 2. تعریف Ingestion Unit و مرز اتمیک

Ingestion Unit یک بستهٔ ورودی مستقل و قابل‌شناسایی است که یک اجرای ingestion آن را پردازش می‌کند. در V1:
- یک فایل CSV/XLSX با یک source/feed profile و یک هدف ingestion، یک واحد است.
- یک پاسخ کامل API/feed snapshot که به‌عنوان یک batch دریافت شده، یک واحد است.
- برای CODAL، یک ReportVersion به‌همراه تمام FinancialFactهای متعلق به همان نسخه، یک واحد است.
- اگر ورودی عمداً به چند بستهٔ مستقل تقسیم شود، هر بسته باید پیش از ingestion هویت مستقل، محدودهٔ روشن و امکان پذیرش مستقل داشته باشد؛ تقسیم پس از مشاهدهٔ خطا برای دور زدن رد کل بسته مجاز نیست.
- یک فایل شامل چند شرکت یا چند تاریخ همچنان یک واحد است، مگر استاندارد Feed صریحاً آن را به چند batch مستقل تعریف کرده باشد.

مرز اتمیک بر اساس نوع فایل، تعداد ردیف یا اندازهٔ batch تغییر نمی‌کند. transactionهای قطعه‌ای که بخشی از یک واحد را commit کنند در V1 مجاز نیستند.

## 3. چرخهٔ عمر IngestionRun

وضعیت‌های منطقی V1:
- STARTED: واحد ورودی برای پردازش ثبت شده است.
- COMPLETED: کل واحد با موفقیت commit شده است؛ ممکن است شامل رکوردهای جدید، duplicateهای بی‌تغییر یا موارد صریحاً خارج از دامنه باشد.
- FAILED: واحد رد شده یا persistence آن rollback شده است؛ canonical write از آن واحد باقی نمانده است.

چرخهٔ مجاز: STARTED → COMPLETED یا STARTED → FAILED. وضعیت نهایی terminal است. یک Run تکمیل‌شده یا شکست‌خورده دوباره باز و بازنویسی نمی‌شود؛ retry یک Run جدید با ارجاع به همان source identity/fingerprint است.

### 3.1 حداقل فیلدهای audit

IngestionRun باید حداقل اطلاعات عملیاتی زیر را نگهداری کند، مشروط به وجود در مدل/نیاز اجرایی:
- شناسهٔ پایدار Run؛
- source/feed و نوع ingestion؛
- زمان شروع و پایان پردازش؛
- status؛
- تعداد رکوردهای کشف‌شده، پذیرفته‌شده/درج‌شده، بدون تغییر به‌علت duplicate، ردشده و در صورت کاربرد به‌روزشده؛
- خلاصهٔ خطاها و هشدارهای قابل‌اقدام؛
- شناسه یا fingerprint ورودی و نسخهٔ پروفایل/adapter/استاندارد، در حدی که برای idempotency و بازتولید مسیر لازم باشد.

این فیلدها audit عملیاتی‌اند؛ جایگزین source publication/availability time، تاریخ اقتصادی، تاریخ اثر، ReportVersion یا provenance هر دامنه نمی‌شوند.

### 3.2 محدودیت محتوای audit

- فایل خام، محتوای کامل ردیف‌ها، مقادیر مالی خام، payloadهای حجیم یا خروجی محاسباتی در error log کپی نمی‌شوند.
- خطا باید با شمارهٔ ردیف/شناسهٔ موقت، نوع خطا و توضیح کوتاه قابل اقدام ثبت شود؛ نگهداری locator دقیق دائمی الزام نیست.
- پیام exception نباید ناخواسته secrets، credential، مسیر خصوصی یا payload کامل منبع را وارد log کند.
- IngestionRun آرشیو منبع یا جایگزین provenance canonical نیست.

## 4. ترتیب اجرای استاندارد

1. ایجاد Run با status=STARTED و ثبت حداقل source identity؛ ثبت audit شروع باید مستقل و پایدار باشد.
2. خواندن کامل واحد ورودی و parse به DTOهای موقت؛ هیچ canonical write انجام نمی‌شود.
3. اعتبارسنجی ساختاری و معنایی کل واحد، شامل company/industry/source resolution، تقویم، units/basis، required fields، numeric range، logical identity و duplicate/conflict.
4. اگر هر خطای سخت یا ابهام حل‌نشده وجود داشت، کل واحد رد می‌شود؛ Run در transaction مستقل به FAILED می‌رود و canonical write انجام نمی‌شود.
5. در صورت عبور کامل validation، یک transaction واحد برای همهٔ canonical writes باز می‌شود.
6. uniqueness و FKهای دیتابیس در برابر race/concurrency مرجع نهایی‌اند؛ conflict constraint باید transaction را fail کند.
7. تغییرات canonical و تغییر status همان Run به COMPLETED در همان transaction commit می‌شوند.
8. اگر هر write، constraint، FK یا commit شکست خورد، کل transaction rollback می‌شود. سپس status همان Run در یک transaction مستقل به FAILED تغییر می‌کند و خلاصهٔ خطا ثبت می‌شود.

ممنوع: commit درون حلقهٔ رکوردها، ذخیرهٔ بخشی از batch، ثبت ReportVersion بدون تمام facts مربوط، یا اعلام COMPLETED پیش از commit قطعی.

اگر ثبت STARTED ممکن نباشد، persistence آغاز نمی‌شود. اگر ثبت audit شکست پس از rollback نیز ممکن نباشد، خطا باید به caller بازگردد؛ سیستم نباید موفقیت یا شکست auditنشده را به‌عنوان نتیجهٔ ثبت‌شده گزارش کند.

## 5. Validation و رفتار خطا

### 5.1 Hard admission / persistence failure

نمونه‌ها:
- source/feed profile ناشناخته یا ناسازگار؛
- شرکت/صنعت نامعلوم یا چندمعنا؛
- تاریخ، تقویم، واحد، scale یا basis نامشخص؛
- فیلد الزامی خالی یا مقدار عددی نامعتبر/خارج از signed 64-bit؛
- mapping یا Metric مبهم؛
- تضاد دو ردیف با یک logical identity؛
- تعارض با رکورد قبلی بدون revision/preference rule مصوب؛
- شکست FK، unique/check constraint یا transaction.

هر مورد بالا کل Ingestion Unit را FAILED می‌کند. skip کردن ردیف نامعتبر و commit بقیه مجاز نیست.

### 5.2 موارد صریحاً خارج از دامنه

فقط موردی که استاندارد نسخه‌دار آن را به‌صراحت out-of-scope اعلام کرده می‌تواند بدون canonical persistence کنار گذاشته شود. تعداد آن در audit ثبت می‌شود. مورد unknown یا ambiguous را نمی‌توان به‌عنوان out-of-scope پنهان کرد.

### 5.3 Warning

هشدار غیرمسدودکننده فقط وقتی مجاز است که استاندارد مصوب اجازهٔ پذیرش آن وضعیت را بدهد و معنای canonical داده تغییر نکند. هشدار نمی‌تواند جایگزین مقدار اجباری، publication time اجباری برای PIT یا mapping حل‌نشده شود.

## 6. Idempotency، duplicate و conflict

### 6.1 تعریف replay یکسان

تکرار همان source artifact/revision با همان source/feed profile و همان نسخهٔ mapping/extraction استاندارد باید نتیجهٔ canonical یکسان بدهد و رکورد canonical تازه نسازد.

Fingerprint فایل به‌تنهایی هویت revision اقتصادی نیست؛ باید همراه source identity، نوع feed، شرکت/دامنهٔ هدف و نسخهٔ قرارداد/استاندارد لازم تفسیر شود.

### 6.2 Duplicateهای داخل batch

- دو ورودی با logical identity یکسان و payload canonical یکسان، duplicate محسوب می‌شوند و حداکثر یک رکورد canonical تولید می‌کنند؛ تعداد duplicateها در audit ثبت می‌شود.
- دو ورودی با logical identity یکسان و payload متفاوت، conflict است و کل واحد را رد می‌کند.
- برابری numeric به‌تنهایی هویت دو رکورد را تعیین نمی‌کند؛ logical identity و dimensions مصوب ملاک‌اند.

### 6.3 برخورد با رکورد موجود

- اگر همان source revision و همان canonical payload قبلاً ثبت شده باشد، replay بدون تغییر canonical موفق و idempotent است.
- اگر logical identity یکسان ولی payload متفاوت باشد، overwrite خودکار ممنوع است.
- جایگزینی فقط با source revision صریح، publication/availability metadata معتبر و قاعدهٔ version/supersession مصوب همان دامنه مجاز است.
- در نبود revision identity یا تقدم منبع مصوب، conflict موجب رد کل واحد می‌شود.
- last-write-wins، جمع‌زدن مقادیر، انتخاب بر اساس ترتیب ردیف/فایل یا زمان ingestion ممنوع است.

برای MarketDaily و FXRate، قرارداد منبع و revision باید پیش از پذیرش چندمنبعی/اصلاح خودکار تکمیل شود. برای CODAL، ReportVersion جدید و facts وابسته باید در یک transaction ثبت شوند؛ ReportVersion موجود immutable است.

## 7. Retry و هم‌زمانی

- Retry پس از FAILED یک Run جدید است؛ Run قبلی برای audit حفظ می‌شود.
- Retry همان ورودی باید idempotent باشد.
- retry خودکار برای validation failure، unknown mapping یا conflict مجاز نیست؛ ابتدا علت باید اصلاح یا revision rule مصوب شود.
- خطاهای گذرای infrastructure می‌توانند با backoff در لایهٔ orchestration retry شوند، اما هر تلاش باید audit قابل‌ردیابی داشته باشد.
- اجرای هم‌زمان دو Run برای یک logical identity نباید دو رکورد canonical بسازد؛ unique constraint/index دیتابیس لازم است.
- اگر دو transaction هم‌زمان روی یک هویت رقابت کنند، یکی ممکن است با unique conflict شکست بخورد؛ پس از rollback، orchestration می‌تواند وجود رکورد canonical معادل را بررسی کند و فقط در صورت اثبات برابری کامل و همان revision، نتیجه را به‌عنوان replay بی‌تغییر طبقه‌بندی کند.
- هیچ راهکار application-level جایگزین constraint پایدار دیتابیس نیست.

## 8. Transaction ownership و مرز Session

- یک لایهٔ service/use-case مالک transaction هر Ingestion Unit است.
- adapter فقط parse می‌کند و transaction یا commit ندارد.
- helperهای repository/identity فقط query یا stage write انجام می‌دهند و حق commit مستقل ندارند.
- در یک واحد ingestion، transaction boundary تو‌در‌تو یا commit ضمنی در helperها ممنوع است.
- مالک transaction باید با caller contract روشن کند که Session از قبل transaction فعال دارد یا خیر؛ nested transaction/savepoint نباید به‌عنوان commit مستقل واحد تلقی شود.
- در صورت استفادهٔ مجدد از Session، پس از rollback باید وضعیت Session پاک/قابل استفادهٔ مجدد باشد و audit FAILED در transaction سالم جداگانه ثبت شود.

جزئیات API/ORM و پیاده‌سازی این قواعد در Task تطبیق سرویس و migration تعیین می‌شود؛ این سند نام فیزیکی ستون یا روش SQLAlchemy خاصی را تحمیل نمی‌کند.

## 9. دامنهٔ اتمیک به تفکیک خانوادهٔ داده

| خانواده | مجموعه‌ای که باید با هم commit شود |
|---|---|
| CODAL | ReportVersion + تمام FinancialFactهای پذیرفته‌شده و provenanceهای وابسته + وضعیت COMPLETED همان Run |
| Market | تمام MarketDailyهای همان source/feed batch + وضعیت COMPLETED Run |
| FX | تمام FXRateهای همان batch + وضعیت COMPLETED Run |
| Share | تمام ShareCountHistoryهای همان batch + وضعیت COMPLETED Run |
| CorporateAction | تمام رویدادهای همان batch + وضعیت COMPLETED Run |

رکوردهای audit شکست خارج از transaction canonical ثبت می‌شوند تا پس از rollback باقی بمانند. اگر یک واحد چند خانواده را عمداً با هم حمل کند، تا وقتی قرارداد منبع و orchestration جداسازی مستقل را مجاز نکرده، کل واحد یک transaction دارد.

## 10. Counts و وضعیت نتیجه

تعریف counts باید در همهٔ ingestion resultها سازگار باشد:
- records_found: تعداد ردیف/مشاهده‌هایی که parser از واحد منبع تشخیص داده است.
- records_inserted: تعداد رکوردهای canonical جدیدی که commit شده‌اند.
- records_updated: فقط تعداد replacementهای revisionدار و صریح که با قرارداد همان دامنه مجاز و commit شده‌اند؛ در V1 پیش‌فرض صفر است.
- records_unchanged یا records_duplicate: رکوردهای replay/duplicate بدون تغییر؛ اگر مدل audit فیلد مستقل ندارد، حداقل در نتیجهٔ ingestion قابل گزارش باشد.
- records_rejected: تعداد ردیف‌های دارای hard error؛ وجود حتی یک مورد، کل واحد را FAILED می‌کند.
- records_ignored_out_of_scope: تعداد مواردی که استاندارد نسخه‌دار صریحاً خارج از دامنه شناخته است.

Counts نهایی باید با نتیجهٔ commit سازگار باشند. در FAILED، records_inserted/updated canonical committed برابر صفر است؛ counts تلاش/ردشده می‌توانند در audit ثبت شوند.

## 11. معیارهای پذیرش DB-DES-005

این قرارداد زمانی قابل‌بستن است که:
1. مرز Ingestion Unit برای هر خانواده و adapter روشن باشد.
2. چرخهٔ STARTED/COMPLETED/FAILED و دوام audit شکست تعریف شده باشد.
3. کل واحد پس از validation موفق در یک transaction commit شود.
4. هر hard error کل واحد را rollback کند؛ هیچ partial canonical write باقی نماند.
5. replay یکسان idempotent و تعارض بدون revision مصوب رد شود.
6. رقابت هم‌زمان با constraints پایگاه داده ایمن شود.
7. adapter و repository مالک commit نباشند؛ service boundary مالک transaction باشد.
8. Run audit حداقلی و بدون raw payload یا جایگزینی provenance باشد.
9. counts، retry و رفتار failure در نتیجه و audit معنای یکسان داشته باشند.
10. قواعد با CODAL/Market/FX تطبیق داده شوند و برای Share/CorporateAction پیش از writer جدید الزام‌آور باشند.

## 12. موارد باز و ارجاع‌ها

- DB-AUD-001: تکمیل inventory transaction/commit/rollback و تمام call-siteها؛ تطبیق مدل IngestionRun و migrationها.
- DB-STD-005: تثبیت Feed profile و تعریف Ingestion Unit برای هر منبع واقعی CSV/XLSX/API.
- DB-DES-004: source revision identity، publication time و source precedence برای Market/FX/Share/Action.
- DB-MIG-001: قیود unique/FK لازم برای concurrency و migration امن داده‌های قدیمی.
- Implementation follow-up: اصلاح partial commit در Market/FX، CODAL transaction/replay behavior، sanitized failure audit و تست‌های atomicity/idempotency/concurrency/boundary.

**محدودیت این Task:** این سند قرارداد منطقی است؛ هیچ ORM، schema، migration، داده، کد یا تستی را تغییر نمی‌دهد و به معنی اثبات رفتار فعلی سرویس‌ها نیست. DB-DES-005 تا زمان تطبیق با کد و تست‌ها PARTIAL باقی می‌ماند.


## 13. تطبیق خواندنی سرویس‌های فعلی با قرارداد — 2026-11-19

این بخش بر اساس snapshot شاخهٔ `master` و خواندن مستقیم فایل‌های `src/ingestion/service.py`, `src/ingestion/market/ingestion.py`, `src/ingestion/fx/ingestion.py`, `src/ingestion/codal/ingestion.py`, `src/ingestion/common/idempotency.py`, `src/ingestion/common/identity.py`, `src/ingestion/common/run_tracker.py` و مدل‌های audit/Market/FX تهیه شده است. این بررسی صرفاً خواندنی است و اجرای تست یا تغییر کد دربرندارد.

### 13.1 یافته‌های قطعی در Market

- `ingest_ohlc_csv` پس از parse، خطاهای parser و خطاهای validation/شرکت ناشناخته را در شمارندهٔ `failed` جمع می‌کند، اما ردیف‌های معتبر دیگر را همچنان stage می‌کند و در پایان با وجود `failed > 0`، Run را `COMPLETED` کرده و commit می‌کند. این partial acceptance صریحاً با §§4–5 قرارداد مغایر است.
- در صورت وجود رکورد با همان هویت، فیلدهای آن بدون source revision، publication/availability metadata یا fingerprint مقایسه/جایگزین می‌شوند؛ این رفتار overwrite/last-write-wins است، نه replay بی‌تغییر یا replacement مصوب.
- مسیر خطای exception کل transaction را rollback می‌کند و یک FAILED run جداگانه می‌سازد؛ اما در مسیر validation errors به‌جای rollback کامل، داده‌های معتبر commit می‌شوند.
- `MarketDaily` فقط `UniqueConstraint(company_id, trade_date)` دارد. رکوردهای جلالی این Feed با `trade_date=NULL` ثبت می‌شوند؛ در SQLite و بسیاری از DBها unique index چند مقدار NULL را مانع نمی‌شود. بنابراین این قید، uniqueness هویت جلالی `(company_id, jalali_year, jalali_month, jalali_day)` را تضمین نمی‌کند.

### 13.2 یافته‌های قطعی در FX

- `ingest_fx_rates` اعتبارسنجی هر عنصر را در حلقه انجام می‌دهد، اما موارد نامعتبر را فقط به `failed` و `errors` اضافه کرده و بقیهٔ batch را ادامه می‌دهد. در پایان حتی با `failed > 0`، Run را `COMPLETED` کرده و canonical rows معتبر را commit می‌کند؛ این نیز partial acceptance خلاف قرارداد است.
- اگر هویت موجود پیدا شود، `rate` و `source` بی‌قید revision/fingerprint/publication overwrite می‌شوند.
- مدل `FXRate` قید unique را بر `(rate_date, currency_from, currency_to, rate_type)` اعمال می‌کند. رکوردهای Jalali با `rate_date=NULL` هستند، بنابراین قید مذکور هویت جلالی `(jalali_year, jalali_month, jalali_day, currency_from, currency_to, rate_type)` را ایمن نمی‌کند.
- مسیر exception rollback و FAILED run جداگانه ایجاد می‌کند؛ اما خطاهای validation به‌صورت partial commit عبور می‌کنند.

### 13.3 یافته‌های قطعی در CODAL

- `ingest_codal_report` یک STARTED run را flush می‌کند، اما شروع Run در transaction مستقل commit نمی‌شود. در مسیر موفق، canonical writes و COMPLETED در یک commit قرار می‌گیرند؛ در مسیر exception، rollback باعث حذف STARTED می‌شود و سپس FAILED run جدیدی در transaction بعدی ساخته می‌شود. بنابراین audit شروع پایدار و همان Run با transition نهایی مطابق قرارداد وجود ندارد.
- اگر `codal_tracking_id` موجود نباشد، Report جدید ساخته می‌شود و کلید پایدار replay در دسترس نیست؛ این با الزام مالک به stable source ID برای ingestion خودکار سازگار نیست.
- اگر tracking ID و publication datetime یکسان پیدا شود، کد فقط تعداد RawFinancialFactهای نسخهٔ قبلی را می‌شمارد، Run را COMPLETED می‌کند و همان نسخه را برمی‌گرداند. نه fingerprint ورودی و نه برابری payload بررسی نمی‌شود؛ حتی محتوای جدید متفاوت نیز ممکن است بی‌صدا به‌عنوان replay یکسان پذیرفته شود. مقدار `records_updated` نیز به‌اشتباه با تعداد facts قبلی پر می‌شود، در حالی‌که هیچ replacement انجام نشده است.
- در مسیر ساخت نسخهٔ جدید، نسخهٔ جاری قبلی پیش از تعیین chronology demote می‌شود و نسخهٔ جدید همیشه `is_current_version=True` می‌گیرد؛ این با تصمیم مالک دربارهٔ عدم current شدن خودکار late-arriving publication قدیمی ناسازگار است.
- تمام RawFinancialFactهای ورودی با یک `period_id` مشترک ساخته می‌شوند؛ این مغایرت مستقل DB-AUD-002 است و در اینجا به‌عنوان ورودی/DTO نامتناسب برای واحد اتمیک ثبت می‌شود.
- `error_log=str(exc)` ممکن است مسیر خصوصی یا جزئیات حساس exception را وارد audit کند؛ sanitization مطابق §3.2 اثبات نشده است.

### 13.4 مدل audit و helperهای مشترک

- `IngestionRun` فقط source، timestamp، status، counts و error_log را دارد؛ source/feed profile version، artifact fingerprint، stable source identity، duplicate/unchanged و out-of-scope counts در مدل موجود نیستند.
- `start_run` صرفاً add/flush می‌کند و transaction مستقل/commit نمی‌کند. `fail_run` commit مستقل دارد. این helperها خودشان تضمین‌کنندهٔ مرز transaction واحد نیستند.
- `common/idempotency.py` صرفاً یادداشت قراردادی است؛ اجرای fingerprint یا source-revision idempotency در آن وجود ندارد.

### 13.5 وضعیت قیود و نتیجهٔ تطبیق

| معیار | وضعیت مشاهده‌شده |
|---|---|
| Hard error موجب رد کل Market batch | FAIL — ردیف‌های معتبر commit می‌شوند |
| Hard error موجب رد کل FX batch | FAIL — ردیف‌های معتبر commit می‌شوند |
| Market/FX replay بدون تغییر | FAIL — رکورد موجود overwrite می‌شود |
| هویت یکتای Jalali در DB | NOT ENFORCED — قیدهای فعلی بر ستون تاریخ میلادی NULLپذیرند |
| CODAL stable ID اجباری | FAIL — tracking ID اختیاری است |
| CODAL replay با fingerprint | FAIL — فقط tracking ID + publication datetime بررسی می‌شود |
| CODAL late-arriving chronology | FAIL — آخرین ingest current می‌شود |
| STARTED پایدار و همان Run terminal | FAIL/NOT PROVEN — شروع commit مستقل ندارد و شکست Run جدید می‌سازد |
| sanitized error audit | NOT PROVEN — متن exception خام ذخیره می‌شود |
| Share/CorporateAction | NOT IMPLEMENTED/NOT AUDITED در این vertical slice |

**نتیجه:** DB-DES-005 قطعاً PARTIAL باقی می‌ماند و سرویس‌های Market، FX و CODAL با قرارداد اتمیک/idempotency مصوب منطبق نیستند. این یافته‌ها مجوز تغییر کد یا schema نیستند. اصلاحات اجرایی باید به Taskهای پیاده‌سازی/مهاجرت مجزا، preflight داده و تست‌های atomicity/idempotency/concurrency ارجاع شوند. هیچ کد، ORM، schema، migration، دیتابیس یا داده‌ای تغییر نکرد و هیچ تستی اجرا نشد.


### 13.6 تطبیق تست‌های موجود و قرارداد تست — 2026-11-19

خواندن تست‌های `src/tests/test_ingestion_ohlc.py`, `src/tests/test_ingestion_fx.py`, `src/tests/test_codal_pdf_extraction.py` و `src/tests/test_stage1_database_integrity.py` نشان می‌دهد بخشی از رفتار ناسازگار فعلی نه‌تنها پوشش داده نشده، بلکه صریحاً به‌عنوان رفتار مورد انتظار تثبیت شده است:

- `test_ingestion_fx.py::test_invalid_rate_type_and_non_positive_rate_fail_explicitly` انتظار دارد با سه ردیف نامعتبر و یک ردیف معتبر، نتیجه `COMPLETED`، سه failed و یک inserted باشد؛ این مستقیماً خلاف hard-fail کل batch در قرارداد است.
- `test_ingestion_fx.py::test_fx_idempotent_upsert_jalali` تغییر rate و source برای همان هویت جلالی را `records_updated=1` و موفقیت می‌داند؛ این همان overwrite بدون revision/fingerprint است که قرارداد ممنوع می‌کند.
- `test_ingestion_ohlc.py` سناریوی idempotent upsert را با `records_updated` برای همان هویت انتظار دارد؛ باید پس از تعیین revision contract به replay بی‌تغییر یا conflict/revision صریح بازتعریف شود.
- تست‌های CODAL در `test_codal_pdf_extraction.py` replay بر اساس tracking ID و publication datetime را idempotent می‌دانند و `records_updated` را برابر تعداد RawFinancialFactهای قبلی assert می‌کنند؛ fingerprint/content comparison در تست‌ها دیده نمی‌شود. همچنین زنجیرهٔ نسخه‌ها، supersession و is_current در این فایل پوشش دارد، اما آزمون late-arriving publication قدیمی‌تر در برابر نسخهٔ جدیدتر به‌عنوان یک adversarial chronology test در قسمت‌های بررسی‌شده یافت نشد.
- `test_stage1_database_integrity.py` migration runner را تا نسخهٔ ۸ تثبیت می‌کند؛ هیچ migration فعال برای unique constraint هویت جلالی Market/FX در این تست وجود ندارد.

بنابراین صرف اصلاح سرویس کافی نیست: تست‌های موجودی که semantics قدیمیِ partial acceptance و overwrite را تثبیت می‌کنند نیز باید با قرارداد مالک بازنگری شوند. تست‌های لازمِ مفقود/ناکافی شامل failure injection در میانهٔ batch و commit، اثبات صفر ماندن canonical rows پس از هر hard error، duplicate/conflict درون batch، replay fingerprint یکسان/متفاوت، رقابت هم‌زمان روی هویت جلالی، failure در ثبت audit، و late-arriving CODAL publication هستند. هیچ تستی در این ممیزی اجرا نشده است؛ نتیجه صرفاً از خواندن assertionهای موجود به‌دست آمده است.


## 13. تطبیق کد جاری با قرارداد — ممیزی 2026-11-19

**وضعیت: PARTIAL؛ اختلاف اجرایی عمده با قرارداد §§4–10.** بررسی مستقیم مدل و سرویس‌ها:

| موضوع | رفتار فعلی مشاهده‌شده | نتیجه نسبت به قرارداد |
|---|---|---|
| Audit Run | فقط source/status/timestamps و counts پایه/error_log؛ بدون artifact fingerprint، profile/adapter version، duplicate count یا retry reference | ناقص |
| STARTED durability | Run و canonical writes در همان Session آغاز می‌شوند؛ ثبت مستقل و پایدار STARTED پیش از parse/validation اثبات نشده | مغایر §4 |
| CODAL identity | tracking ID اختیاری؛ replay فقط tracking ID + publication_datetime، بدون content fingerprint | مغایر §§6.1–6.4 |
| CODAL chronology | هر نسخهٔ جدید current می‌شود و قبلی demote؛ مقایسهٔ chronology برای late arrival دیده نشد | مغایر قرارداد PIT |
| Market batch | ردیف‌های invalid/parser errors شمرده می‌شوند، اما معتبرهای همان فایل commit می‌شوند؛ تست‌ها این رفتار را assert می‌کنند | مغایر fail-whole-unit §5 |
| Market correction | کلید شرکت + تاریخ جلالی؛ مقدار و source در برخورد با رکورد موجود بی‌قیدوشرط overwrite می‌شوند | مغایر §6.3 |
| FX batch | ردیف‌های نامعتبر skip و معتبرها commit می‌شوند؛ تست invalid-rate انتظار COMPLETED با partial insertion دارد | مغایر §5 |
| FX correction | همان کلید تاریخ/ارز/نوع نرخ با rate/source جدید overwrite می‌شود؛ تست آن را update idempotent می‌نامد | مغایر §6.3 |
| Exception API | CODAL پس از audit FAILED exception را raise می‌کند؛ Market/FX نتیجه FAILED برمی‌گردانند | ناهمگون |

تست‌های موجود صرفاً وجود audit و upsert را در چند حالت تأیید می‌کنند؛ failure injection برای اثبات rollback کل batch، race/unique conflict، durable STARTED، یا replay fingerprint یافت/اثبات نشد. در نتیجه، قرارداد مستند به‌تنهایی evidence پیاده‌سازی نیست.

**تصمیم اجرایی/محدودیت:** این یافته‌ها مجوز تغییر سرویس یا تست نیستند. پیش از implementation باید revision identity و fingerprint scope برای هر Feed و رفتار correction تأیید شود. هیچ کد، مدل، schema، migration یا DB تغییر نکرده و تستی اجرا نشده است.


### 8.99 — قیود یکتایی Jalali و اتلاف diagnostics در adapterها (2026-11-19)

**نتیجه: PARTIAL؛ دو نقص مستقل در هویت فیزیکی و مرز parse کشف شد.**

1. `MarketDaily` unique فعلی `(company_id, trade_date)` است، در حالی که مسیر Jalali مقدار `trade_date=NULL` می‌نویسد. `FXRate` unique فعلی `(rate_date,currency_from,currency_to,rate_type)` است، در حالی که مسیر Jalali `rate_date=NULL` می‌نویسد. SQLite چند NULL را در UNIQUE می‌پذیرد؛ بنابراین این قیود duplicateهای Jalali را متوقف نمی‌کنند. lookupهای `.one_or_none()` ممکن است با duplicateهای موجود شکست بخورند و قید DB مانع race نیست.
2. Market adapter diagnostics را برمی‌گرداند ولی service بخشی از ردیف‌های سالم را با وجود خطا commit می‌کند. FX adapter تعدادی ردیف malformed/blank را پیش از ساخت DTO بی‌صدا حذف می‌کند و service نیز DTOهای نامعتبر را skip می‌کند؛ این هم count خطا را ناقص می‌کند و هم با fail-whole-unit تعارض دارد.

اقدام امن بعدی فقط audit خواندنی duplicateهای فعلی روی کلیدهای Jalali و inventory نسخهٔ SQLite/migration chain است. هرگونه unique migration باید پس از duplicate preflight و تصمیم دربارهٔ داده‌های موجود طراحی شود؛ merge/delete خودکار ممنوع. هیچ کد، ORM، schema، migration یا DB تغییر نکرده و تستی اجرا نشده است.


### 13.7 دفتر تصمیم‌های باز برای Revision Identity و Fingerprint — 2026-11-19

این دفتر، ورودی لازم پیش از هر vertical-slice اجرایی را از هم جدا می‌کند. موارد زیر **پیشنهاد مصوب یا سیاست نهایی نیستند**؛ فقط تصمیم‌هایی‌اند که بدون آن‌ها پیاده‌سازی idempotency/correction قابل اتکا نیست.

| Feed | هویت پایدار منبع/رکورد | هویت revision یا correction | دامنهٔ fingerprint که باید تعیین تکلیف شود | رفتار تعارض حل‌نشده |
|---|---|---|---|---|
| CODAL Report | Stable source ID متعلق به گزارش منطقی (مانند CODAL tracking ID یا معادل مستند) برای ingestion خودکار الزامی است؛ عنوان/تاریخ/شرکت به‌تنهایی جایگزین مجاز نیست | شناسه/ترتیب نسخهٔ منتشرشده و publication identity؛ ارتباط نسخهٔ اصلاحی با نسخهٔ قبلی باید از metadata معتبر منبع یا review صریح بیاید | fingerprint کل artifact ورودی در برابر fingerprint محتوای canonicalized؛ باید روشن شود تغییرات غیرمالی، metadata انتشار، ترتیب sheet/table و تغییرات صرفاً formatting چه اثری دارند | stable ID یا publication identity مفقود/متناقض، یا payload متفاوت با identity یکسان: توقف و review؛ replay یکسان فقط پس از مقایسهٔ fingerprint قابل اعلام است |
| MarketDaily CSV | کلید مشاهدهٔ اقتصادی مصوب: Company + تاریخ جلالی؛ Feed/source identity نیز باید مشخص باشد | شناسه یا شواهد معتبر برای اصلاح/بازنشر همان روز؛ publication/availability و chronology هنوز تعیین نشده‌اند | fingerprint کل CSV در برابر fingerprint هر رکورد normalized؛ باید رفتار تغییر ترتیب ردیف‌ها، تغییر ترتیب ستون‌ها، ردیف تکراری و metadata غیرمؤثر مشخص شود | یک کلید روزانه با مقدار متفاوت، بدون revision معتبر، conflict است؛ overwrite یا انتخاب آخرین فایل مجاز نیست |
| FX daily workbook/feed | کلید اقتصادی مصوب: تاریخ جلالی + ارز مبدأ/مقصد + rate type؛ Feed profile و provenance artifact باید مشخص باشد | شناسه یا شواهد معتبر اصلاح/بازنشر همان تاریخ و نوع نرخ؛ publication/availability و تقویم کامل هنوز باز است | fingerprint artifact در برابر fingerprint نرخ normalized؛ اثر تغییر sheet/row order، formatting و مقدار منبع پس از تبدیل واحد باید تعیین شود | مقدار متفاوت برای کلید موجود، بدون revision معتبر، conflict است؛ overwrite یا انتخاب آخرین فایل مجاز نیست |

**تصمیم‌های مشترک که باید پیش از implementation بسته شوند:**
1. آیا fingerprint بر bytes خام artifact، محتوای معنایی parseشده، یا هر دو بنا می‌شود؛ و نسخهٔ الگوریتم/serialization چگونه ثبت می‌شود.
2. کدام metadata در fingerprint وارد می‌شود: source/feed profile، company identity، calendar/unit، publication/availability، parser/mapping version و revision identity.
3. replay دقیقاً چه زمانی UNCHANGED است؛ تغییر payload با stable identity یکسان چه زمانی correction معتبر و چه زمانی conflict است.
4. واحد اتمیک پذیرش برای هر Feed چیست (کل workbook/CSV، یک گزارش منطقی، یا batch مشخص) و کدام diagnosticها hard error، out-of-scope یا warning محسوب می‌شوند. تا تعیین این مرز، رفتار فعلی partial acceptance معیار قابل قبول نیست.
5. duplicate داخل یک artifact، duplicate بین artifactها، و دو ورودی هم‌زمان با identity یکسان چگونه fail-closed و audit می‌شوند.
6. در CODAL، publication chronology، supersession و رتبهٔ کیفیت مصوب مالک باید مستقل اعمال شوند؛ arrival order هرگز جای chronology نیست.

تا زمان پاسخ به این تصمیم‌ها، هیچ fingerprint scope، revision key، conflict winner یا batch policy در این دفتر تصویب نمی‌شود. نتیجهٔ اجرایی ثابت فعلی فقط این است: identity ناقص یا تعارض غیرقابل توضیح نباید به overwrite، partial commit یا پذیرش خودکار منجر شود؛ کل واحد ورودی متوقف و برای review گزارش شود. این بخش مستنداتی است؛ هیچ کد، تست، ORM، schema، migration، دیتابیس یا داده‌ای تغییر نکرده و تستی اجرا نشده است.


### 13.8 ماتریس پذیرش آزمون برای اصلاح DB-DES-005 — 2026-11-19

این ماتریس، رفتار موردنیاز را به سناریوهای مستقل و قابل‌اثبات تبدیل می‌کند. این‌ها **آزمون‌های پیشنهادی پذیرش** هستند، نه ادعای وجود یا اجرای تست. هر سناریو باید روی دیتابیس تست ایزوله اجرا شود و وضعیت canonical، Run audit و transaction را جداگانه assert کند.

| ID | حوزه | سناریو | انتظار canonical | انتظار audit / نتیجه |
|---|---|---|---|---|
| AT-01 | Run lifecycle | ثبت STARTED موفق، سپس پردازش موفق | فقط پس از validation کامل و در transaction نهایی نوشته شود | همان Run از STARTED به COMPLETED؛ یک Run جدید ساخته نشود |
| AT-02 | Run lifecycle | شکست parse/validation پس از ثبت STARTED | صفر canonical write | همان Run به FAILED؛ خطا خلاصه و sanitized |
| AT-03 | Run lifecycle | شکست ثبت STARTED | هیچ ingestion/persistence آغاز نشود | خطا به caller؛ Run جعلی یا نتیجهٔ موفق گزارش نشود |
| AT-04 | Atomicity | خطای hard در آخرین رکورد Market/FX batch | هیچ رکورد canonical از کل batch باقی نماند | Run برابر FAILED؛ rejected count و locatorهای امن ثبت شوند |
| AT-05 | Atomicity | exception پس از stage شدن چند write و پیش از commit | تمام writeهای همان واحد rollback شوند | همان Run در transaction مستقل FAILED شود |
| AT-06 | Atomicity | شکست commit یا constraint در میانهٔ flush | صفر canonical write از واحد | audit شکست باقی بماند؛ نتیجه COMPLETED نباشد |
| AT-07 | Adapter boundary | ردیف malformed یا تاریخ خالی در FX adapter | adapter نباید مورد را بی‌صدا حذف کند؛ کل واحد در صورت hard error رد شود | diagnostic و records_found/rejected با ورودی منبع قابل reconcile باشد |
| AT-08 | Adapter boundary | خطای parse در Market adapter همراه ردیف سالم | ردیف سالم نیز commit نشود | FAILED کل batch؛ partial acceptance ممنوع |
| AT-09 | Intra-batch identity | دو ردیف با logical identity و payload یکسان | حداکثر یک canonical record | duplicate/unchanged count دقیق |
| AT-10 | Intra-batch conflict | دو ردیف با logical identity یکسان و payload متفاوت | صفر canonical write از کل واحد | FAILED با conflict قابل‌تشخیص |
| AT-11 | Replay | همان artifact/revision و fingerprint یکسان | canonical state بدون تغییر | Run جدید برای تلاش جدید؛ نتیجهٔ unchanged، نه inserted/updated |
| AT-12 | Replay conflict | stable identity یکسان و fingerprint/payload متفاوت، بدون revision معتبر | canonical state قبلی دست‌نخورده | FAILED یا review-required طبق API مصوب؛ هرگز overwrite خاموش |
| AT-13 | Correction | revision معتبر و قاعدهٔ supersession مصوب | فقط replacement/versioning مجاز همان دامنه | updated فقط برای replacement واقعی؛ تاریخچهٔ نسخه حفظ شود |
| AT-14 | Concurrency | دو Run هم‌زمان برای یک logical identity و payload برابر | یک canonical identity یکتا | loser پس از rollback فقط با اثبات revision و payload برابر unchanged تلقی شود |
| AT-15 | Concurrency | دو Run هم‌زمان برای یک logical identity و payload متفاوت | حداکثر یک وضعیت canonical؛ هیچ last-write-wins | conflict ثبت و تصمیم winner خودکار انجام نشود |
| AT-16 | CODAL chronology | ورود نسخهٔ جدیدتر، سپس نسخهٔ قدیمی‌تر با arrival دیرتر | نسخهٔ قدیمی‌تر current نشود | chronology/supersession از publication evidence پیروی کند |
| AT-17 | CODAL completeness | ReportVersion به‌همراه چند fact؛ شکست یک fact در persistence | نه ReportVersion و نه هیچ fact وابسته باقی نماند | همان Run FAILED |
| AT-18 | Audit safety | exception شامل مسیر محلی، token یا payload نمونه | canonical outcome مطابق rollback | هیچ secret/path/payload خام در error_log نباشد |
| AT-19 | Counts | واحد FAILED پس از چند write موقت | committed inserted/updated برابر صفر | attempted/rejected از committed جدا باشد؛ counts معنای ثابت داشته باشند |
| AT-20 | Retry | retry پس از FAILED با همان ورودی اصلاح‌نشده | رفتار deterministic؛ validation/conflict دوباره canonical ننویسد | Run جدید با ارجاع به تلاش قبلی/source identity؛ retry خودکار خطای معنایی ممنوع |

**شرایط اجرای معتبر ماتریس:**
- هر تست باید با snapshot اولیه و query پس از پایان، تعداد و شناسهٔ canonical rows را مقایسه کند؛ صرفاً بررسی return value کافی نیست.
- برای failure injection، نقطهٔ شکست باید پس از حداقل یک write موقت stage‌شده باشد تا rollback واقعی اثبات شود.
- تست concurrency باید از دو Session/transaction مستقل استفاده کند؛ اجرای ترتیبی جایگزین رقابت نیست.
- تست Jalali uniqueness باید پس از preflight داده و migration طراحی‌شده اجرا شود؛ تا آن زمان AT-14/15 در وضعیت نیازمند constraint فیزیکی باقی می‌مانند.
- آزمون CODAL chronology به publication identity معتبر و rule ranking/supersession مصوب نیاز دارد؛ با timestamp ورود جایگزین نشود.
- تست‌های قدیمی که partial acceptance یا overwrite را موفقیت تلقی می‌کنند باید بازنویسی شوند؛ تا وقتی قرارداد revision نهایی نشده، AT-12/13 را فقط می‌توان در سطح fail-closed/conflict آزمود و replacement را نباید حدس زد.

**وضعیت:** هیچ‌یک از سناریوهای این ماتریس در این مرحله اجرا نشده‌اند. ماتریس، مجوز تغییر تست یا implementation نیست؛ ابتدا تصمیم‌های §13.7، preflight هویت جلالی DB-DES-004 §15 و قراردادهای Feed باید بسته شوند. DB-DES-005 همچنان PARTIAL است.

### 13.9 حداقل قرارداد provenance و رفتار fail-closed موقت برای Market/FX — 2026-11-20

این بخش میان metadata قابل ثبت در لحظهٔ بارگذاری و metadataای که فقط از ناشر/منبع قابل دریافت است تفکیک می‌کند. هدف، جلوگیری از جعل chronology یا revision با استفاده از زمان ورود فایل است. موارد زیر guardrail موقت مستنداتی‌اند؛ الگوریتم fingerprint، مدل نهایی revision و سیاست supersession را تصویب نمی‌کنند.

#### الف) سه زمان مستقل

| فیلد مفهومی | معنای دقیق | منبع مجاز | قاعده |
|---|---|---|---|
| source_published_at | زمان انتشار رسمی artifact/داده توسط ناشر | metadata رسمی منبع یا شواهد قابل استناد همان انتشار | اگر ارائه نشده، NULL/UNKNOWN؛ از تاریخ داخل فایل یا زمان بارگذاری استنتاج نشود |
| source_available_at | نخستین زمان قابل اثبات دسترسی به همان artifact/نسخه | timestamp معتبر منبع یا ثبت قابل اثبات دریافت | با published_at یکی فرض نشود؛ اگر نامعلوم است NULL/UNKNOWN |
| ingested_at | زمان دریافت/ثبت فایل در سامانه | ساعت سامانه هنگام upload/ingestion | زمان عملیاتی مستقل؛ هرگز جانشین publication/availability نیست |

برای upload کاربر، uploader/actor و زمان upload باید در audit ثبت شوند، اما این دو مقدار publication evidence نیستند. زمان فایل‌سیستم، زمان تغییر workbook و تاریخ ردیف‌ها به‌تنهایی شواهد انتشار رسمی محسوب نمی‌شوند.

#### ب) حداقل provenance artifact

برای هر تلاش بارگذاری، تا حدی که واقعاً معلوم است، این شواهد باید قابل ثبت/بازسازی باشند:
- feed/profile identity و نسخهٔ قرارداد parser/mapping؛
- source identity و روش دریافت اعلام‌شده؛
- نام artifact صرفاً به‌عنوان نام ارائه‌شده، نه شناسهٔ پایدار؛
- SHA-256 بایت‌های artifact دقیقاً همان‌طور که دریافت شده، بدون normalize یا بازذخیره؛
- اندازهٔ بایت، زمان دریافت، actor/uploader و شناسهٔ Run؛
- source_published_at و source_available_at همراه evidence reference و وضعیت KNOWN/UNKNOWN؛
- تقویم، واحد و شرکت/نوع نرخ resolveشده که هنگام parse اعمال شده‌اند؛
- parser/mapping version و نتیجهٔ validation.

ثبت hash فایل، به‌تنهایی هویت انتشار یا revision رسمی را اثبات نمی‌کند؛ فقط برابری بایت‌های دو artifact را می‌سنجد. نگهداری artifact خام و محل امن آن باید در سیاست retention/security جداگانه تعیین شود؛ این بخش مجوز ذخیره‌سازی payload یا تغییر schema نیست.

#### ج) حداقل قواعد موقت replay و conflict

1. Artifact با SHA-256 و feed/profile identity یکسان، فقط byte-identical replay candidate است. اعلام UNCHANGED نهایی مستلزم تطبیق identity، scope و نتیجهٔ parse با قرارداد مصوب است.
2. Hash متفاوت برای artifact، به‌تنهایی correction معتبر نیست؛ ممکن است صرفاً formatting، ترتیب ردیف/ستون یا metadata غیرمؤثر تغییر کرده باشد.
3. برای MarketDaily، کلید اقتصادی هر مشاهده همان Company + تاریخ جلالی است. برای FX، تاریخ جلالی + جفت ارز + rate_type است. مقدار متفاوت روی کلید موجود، بدون evidence معتبر revision، conflict است؛ overwrite و last-arrival-wins ممنوع‌اند.
4. اگر همان کلید در یک artifact چند بار بیاید، payloadهای یکسان duplicate داخلی و payloadهای متفاوت conflict داخلی‌اند؛ تا تعیین سیاست نهایی، هر دو حالت باید diagnostic کامل داشته باشند و هیچ انتخاب ردیف برنده خودکار انجام نشود.
5. اگر ناشر revision ID/sequence رسمی ارائه نکند، ترتیب دریافت فایل‌ها ترتیب نسخه‌ها نیست. زمان upload، mtime فایل و ترتیب ردیف‌ها مجوز supersession نیستند.
6. اگر publication/availability ناشناخته باشد، داده می‌تواند از نظر محتوایی بررسی شود، اما chronology/PIT و current-winner نباید از آن زمان‌سازی شود. پذیرش canonical نیز تابع gateهای identity، uniqueness و atomicity مستقل است.
7. برای FX workbook، hash فعلی eb85250100438335accb06ca1fdf364304887a71e361258b93836d3a90dd6fcf فقط به artifact بررسی‌شده متصل است؛ تا provenance منبع و profile identity آن ثبت نشود، این hash به‌تنهایی EXCHANGE_CENTER بودن یا revision رسمی را اثبات نمی‌کند.
8. برای Market CSV سامان، منبع CODAL و روش دریافت با اسکریپت اختصاصی مالک ثبت شده‌اند؛ اما publication/availability و revision metadata همچنان UNKNOWN هستند. نباید از تاریخ جلالی معاملات به‌عنوان زمان انتشار استفاده کرد.

#### د) evidence checklist برای بستن Feedها

| Feed | شواهد لازم بعدی | در صورت نبود شواهد |
|---|---|---|
| MarketDaily / CODAL | نمونهٔ metadata انتشار یا صفحه/شناسهٔ رسمی مرتبط با همان خروجی؛ زمان انتشار/دسترس‌پذیری؛ توضیح مستند CODAL دربارهٔ اصلاح/بازنشر یا تصریح نبود revision ID | هر تغییر مقدار روی Company+Jalali date conflict/review؛ chronology و supersession حل‌نشده |
| FX / EXCHANGE_CENTER | تأیید قابل ردیابی اینکه artifact با hash فوق متعلق به profile مرکز مبادله است؛ منبع/صفحهٔ دریافت؛ metadata زمان انتشار/دسترس‌پذیری؛ رفتار اصلاحیه | artifact در سطح provenance unverified؛ مقدار متعارض روی تاریخ/نوع نرخ conflict/review |
| FX / FREE_MARKET | artifact واقعی و قابل انتساب به منبع، header و نمونهٔ داده، واحد، تقویم، زمان انتشار و رفتار revision | Feed profile غیرفعال؛ هیچ schema یا mapping از EXCHANGE_CENTER کپی نشود |

**وضعیت تصمیم:** این بخش فقط حداقل شواهد و fail-closed guardrail را مشخص می‌کند. هیچ fingerprint algorithm، revision key، retention policy، schema، batch boundary یا conflict winner نهایی تصویب نشده است. DB-DES-005 و DB-STD-005 همچنان PARTIAL هستند. هیچ کد، ORM، schema، migration، دیتابیس، داده یا تستی تغییر/اجرا نشده است.

### 13.10 تطبیق دفتر provenance با تصمیم‌های مالک و رجیستر evidence — 2026-11-20

این یادداشت، ابهام ارجاع §13.7 به «تعیین Feed/source identity» را با تصمیم‌های مالک روشن می‌کند؛ هویت کلی منبع با stable artifact/revision identity یکسان نیست.

- MarketDaily نمونهٔ سامان: source برابر CODAL و دریافت با اسکریپت مالک OWNER-APPROVED است. J-Date جلالی YYYY-MM-DD؛ Close قیمت روزانه به Rial/share؛ Volume تعداد سهم؛ No تعداد معامله؛ Value مقدار مستقل منبع به Rial است. Final/Open/High/Low خارج mapping مصوب‌اند. فایل CSV با SHA-256 برابر d94f27405f257b4010e1d2b7db4a554311484a6dde2b35a9c81c548f381c1413 در checkout قابل مشاهده و hash آن مستقلاً match شده است. stable publisher artifact ID، source_published_at، source_available_at و evidence اصلاح/بازنشر هنوز اثبات نشده‌اند.
- FX: source/type کلی EXCHANGE_CENTER و قرارداد استفاده از sell column تنها با Rial/USD و بدون تبدیل OWNER-APPROVED است. فایل dollar-history.xlsx موجود و hash آن eb85250100438335accb06ca1fdf364304887a71e361258b93836d3a90dd6fcf است. این تطبیق بایت‌ها به‌تنهایی اتصال provenance همین artifact به profile، ناشر، زمان انتشار/دسترس‌پذیری یا revision رسمی را اثبات نمی‌کند؛ پیوند قابل ردیابی همچنان لازم است.
- FREE_MARKET: ورودی Toman/USD و تبدیل canonical با ضریب دقیق ۱۰ OWNER-APPROVED است؛ نمونهٔ واقعی و audit کامل source/header/calendar/provenance/revision در checkout وجود ندارد. پروفایل نباید فعال شود و mapping EXCHANGE_CENTER نباید کپی شود.
- source_published_at، source_available_at و ingested_at مفاهیم جدا هستند. upload، mtime و row date جای publication/availability نیستند. SHA-256 فقط byte equality را نشان می‌دهد.
- کلیدهای اقتصادی مستند: MarketDaily برابر Company + تاریخ جلالی؛ FX برابر تاریخ جلالی + جفت ارز + rate_type. payload متفاوت روی کلید موجود بدون evidence revision معتبر conflict/review می‌ماند؛ overwrite و last-arrival-wins مجاز نیست. fingerprint scope، revision ranking و conflict winner نهایی تصویب نشده‌اند.

برای ماتریس و closure register نهایی به DB_STD_005_AND_DB_AUD_001_MARKET_FX_EVIDENCE_REVIEW.md §19 و خلاصهٔ Master Working Packet §9.30 مراجعه شود. §13.8 همچنان test plan پیشنهادی است، نه ادعای اجرای تست یا سیاست implementation نهایی؛ acceptance criteria §11 نیز به‌تنهایی evidence اجرای کد نیست. DB-DES-005 همچنان PARTIAL است و هیچ feed با این note production-ready اعلام نمی‌شود. این یادداشت مستنداتی است؛ کد، ORM، schema، migration، database و داده تغییر نکرده و تستی اجرا نشده است.
