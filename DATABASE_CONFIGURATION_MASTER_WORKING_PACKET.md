# Database Configuration — Master Working Packet

## 1. Purpose and authority

این فایل **تنها مرجع اجرایی مسیر بازبینی، اصلاح و تکمیل پیکربندی دیتابیس** در مخزن `lovelyroz/analyzer` است.

وضعیت Taskها، ترتیب اجرا، وابستگی‌ها، تصمیم‌های تأییدشده، شواهد، موانع و معیارهای پایان این مسیر فقط در همین فایل تعیین می‌شوند. گزارش‌ها و گفتگوهای قدیمی صرفاً شواهد تاریخی/تکمیلی‌اند و مرجع مستقلی برای تعیین وضعیت نیستند.

این مسیر از Stage 7 مستقل است؛ با این حال، قرارداد دیتابیس باید نیازهای مراحل مصرف‌کننده، از جمله Stage 7، را پشتیبانی کند. این فایل جایگزین `STAGE7_MASTER_WORKING_PACKET.md` نیست و نباید وضعیت Taskهای Stage 7 را تغییر دهد.

**سند معماری مبنا:** `12_Database_Architecture_V1.1.md` (محتوای فعلی آن Database Contract V1.3 است). این سند قرارداد هدف و محل ثبت جزئیات معماری است؛ این Master Packet مرجع پیشرفت و اجرای کارهاست. هر تعارض باید ابتدا در این Packet ثبت و تعیین تکلیف شود؛ تغییر سند معماری یا کد بدون تصمیم روشن مجاز نیست.

آخرین بازنگری: 2026-11-08 — ایجاد Packet و ثبت یافته‌های اولیه ممیزی FinancialPeriod و مرز Report/Period.

## 2. قواعد مدیریت Taskها

- `[x]` فقط وقتی مجاز است که کل دامنه Task انجام شده، شواهد کافی ثبت شده و هیچ شرط یا اقدام باقی‌مانده‌ای در همان Task وجود نداشته باشد.
- `[~]` یعنی PARTIAL؛ بخشی از کار انجام شده اما بررسی، اقدام، مدرک یا شرطی باقی است.
- `[ ]` یعنی OPEN؛ `[!]` یعنی BLOCKED و ادامه به پیش‌نیاز یا تصمیمی خارج از اختیار/دسترسی فعلی وابسته است.
- تصمیم معماریِ ثبت‌شده در سند، به‌تنهایی اثبات نمی‌کند که مدل، migration، سرویس یا تست با آن منطبق است.
- بررسی کد به‌تنهایی اثبات نمی‌کند داده‌های پایگاه‌های موجود قابل مهاجرت‌اند؛ وضعیت دادهٔ واقعی باید جداگانه بررسی شود.
- هیچ migration مخرب، حذف جدول/ستون، تبدیل تاریخ یا بازنویسی داده‌ای بدون بررسی داده‌های موجود و طرح مهاجرت ایمن مجاز نیست.
- هر Task شناسه ثابت دارد. شناسه Task بسته‌شده یا حذف‌شده دوباره استفاده نمی‌شود.
- گزارش هر اجرا باید تمام شناسه‌های درخواستی را عیناً ذکر و برای هرکدام `DONE`، `PARTIAL`، `NOT DONE` یا `BLOCKED` را با شاهد اعلام کند.
- تست‌ها را کاربر اجرا می‌کند، مگر اینکه کاربر صریحاً دستور دیگری بدهد. Agent باید فرمان دقیق تست‌ها را ارائه کند و ادعای اجرای تست نداشته باشد.
- `WORKFLOW_RULES.md` فقط توسط مالک/دستیار مجاز به‌روزرسانی است؛ Agentها اجازهٔ ویرایش آن را ندارند.
- دامنهٔ هر Prompt باید فایل‌های مجاز، نوع کار (کدنویسی/تغییر یا گزارش‌محور/بدون تغییر)، Task IDها و خروجی مورد انتظار را دقیقاً مشخص کند.

## 3. اصول و تصمیم‌های قطعی مالک

موارد زیر تصمیم‌های مصوب‌اند و در بازبینی پیاده‌سازی نباید دوباره به‌عنوان موضوع باز مطرح شوند، مگر اینکه شواهد فنی تناقض یا عدم امکان اجرا را نشان دهد؛ در آن صورت ابتدا مسئله و گزینه‌ها برای تصمیم مالک گزارش شود.

### 3.1 هویت شرکت و صنعت
- هر شرکت در V1 دقیقاً یک صنعت دارد؛ رابطهٔ شرکت‌های تابعه، چندصنعتی و زیرصنعت خارج از دامنه است.
- هویت پایدار شرکت `company_id` است؛ نماد معاملاتی شناسهٔ شرکت نیست.
- صنعت شرکت باید صریح و معتبر تعیین شود. شرکت/صنعت نامشخص یا مبهم نباید با حدس یا مقدار پیش‌فرض وارد داده‌های مالی شود.
- تغییر/تاریخچهٔ نماد معاملاتی در V1 جدول مستقل نمی‌خواهد.
- هفت گروه اولیهٔ صنعت: BANK، INVESTMENT، PETROCHEMICAL، METALS، CEMENT، FOOD، PHARMACEUTICAL؛ فهرست قابل توسعه است.

### 3.2 FinancialPeriod
- تاریخ‌های دورهٔ مالی با اجزای تقویم جلالی ذخیره می‌شوند: سال، ماه و روز شروع و پایان. SQL/Gregorian Date مرجع نهایی تاریخ دورهٔ مالی نیست.
- تاریخ واقعی شروع/پایان باید از گزارش منبع یا تقویم مالی معتبر همان شرکت تعیین شود؛ شروع سال مالی را فروردین ۱ فرض نکنید.
- `fiscal_year` برچسب سال مالی شرکت است؛ `fiscal_quarter` در صورت کاربرد ۱ تا ۴ است.
- `period_type` طول/ماهیت دورهٔ دادهٔ منبع را توصیف می‌کند، نه تناوب انتشار گزارش.
- `months_length` طول دوره و `is_ytd` تجمعی بودن از ابتدای سال مالی را مشخص می‌کند.
- الگوی متداول گزارش‌های تجمعی: Q1 = QUARTER/3/YTD، Q2 = SEMI_ANNUAL/6/YTD، Q3 = NINE_MONTH/9/YTD، Q4 = ANNUAL/12/YTD؛ اما این الگو نباید بدون شواهد به هر گزارش تحمیل شود.
- گزارش منتشرشده در پایان فصل الزاماً مقدار مستقل همان فصل را ندارد؛ ممکن است مقدار YTD یا standalone باشد. از عنوان/زمان انتشار به‌تنهایی نتیجه‌گیری نکنید.
- مقادیر مستقل فصل که از تفاضل گزارش‌های YTD به دست می‌آیند فقط در runtime محاسبه می‌شوند و به‌عنوان fact منبع ذخیره نمی‌شوند. تفاضل باید از نسخه‌های سازگار در زنجیرهٔ همان سال مالی استفاده کند.
- TTM دورهٔ منبع نیست؛ پنجرهٔ تحلیلی مشتق‌شده و runtime-only است.
- هویت منطقی دوره: شرکت + تاریخ دقیق جلالی شروع + تاریخ دقیق جلالی پایان.
- داده‌های موجود در ستون‌های Date باید پیش از migration بررسی شوند؛ تقویم/معنای آن‌ها را حدس نزنید و تبدیل کور انجام ندهید.

### 3.3 گزارش، نسخه و PIT
- `Report` هویت گزارش منطقی و `ReportVersion` یک نسخهٔ منتشرشده از آن را نشان می‌دهد؛ زمان انتشار متعلق به نسخه است.
- گزارش منتشرشدهٔ شرکت مرجع ارقام گزارش‌شده است. برنامه باید ارقام را درست استخراج و طبقه‌بندی کند و نباید با محاسبات خودش رقم گزارش‌شده را زیر سؤال ببرد یا بی‌صدا اصلاح کند.
- فقط نسخهٔ اصلاحی/تجدیدنظرشدهٔ منتشرشده توسط شرکت بر نسخهٔ قبلی همان گزارش اولویت دارد.
- نسخهٔ قبلی باید حفظ شود؛ نسخهٔ اصلاحی فقط برای PITهایی اعمال می‌شود که زمان انتشار آن را شامل می‌شوند و نباید به PIT گذشته نشت کند.

### 3.4 ذخیره‌سازی دادهٔ مالی
- هدف، ذخیرهٔ ردیف خام صورت مالی یا آرشیو عمومی raw facts نیست. داده‌ها هنگام ingestion طبقه‌بندی می‌شوند.
- هر قلم منبع باید به یکی از این سرانجام‌ها برسد: metric استاندارد موردنیاز تحلیل، یک bucket محدود و ساده از نوع `OTHER_*`، discard، یا reject/quarantine پیش از ذخیرهٔ مالی در صورت ابهام ضروری.
- فقط ورودی‌های canonical انتخاب‌شده به‌همراه حداقل provenance ذخیره می‌شوند: شرکت، گزارش/نسخه، دوره و locator منبع (برای نمونه بخش/ردیف PDF یا workbook/sheet/cell در Excel).
- جزئیات خام و بی‌استفاده، برچسب‌های اصلی همهٔ ردیف‌ها و payload کامل منبع برای آرشیو ذخیره نمی‌شوند.
- جدول canonical نباید کپی دومِ جدول raw باشد. `normalized_financial_facts` فقط یک نامزد برای بازطراحی به‌عنوان لایهٔ ورودی canonical است.
- `normalized_financial_fact_inputs` فقط در صورت اثبات نیاز مشخص تحلیلی/ممیزی حفظ می‌شود.
- خروجی‌های محاسباتی، KPI، forecast، valuation و decision در DB ذخیره نمی‌شوند؛ runtime-only هستند. ذخیرهٔ انتخابی خروجی، در صورت نیاز، خارج از DB و از مسیر UI است.
- `NULL` با صفر برابر نیست؛ استثنای محدود ZERO_FALLBACK فقط برای مبلغ فروش محصول است.

### 3.5 سیاست مبلغ فروش محصول
1. مبلغ معتبر گزارش‌شده توسط شرکت مرجع است و حتی اگر با حاصل‌ضرب مقدار فروش در نرخ فروش تفاوت داشته باشد ذخیره می‌شود.
2. اگر مبلغ گزارش‌شده خالی/غیرقابل استفاده باشد و مقدار فروش و نرخ فروش هر دو معتبر و از نظر واحد و دوره سازگار باشند، حاصل‌ضرب فقط در runtime محاسبه می‌شود و به‌عنوان مبلغ گزارش‌شده ذخیره نمی‌شود.
3. اگر مبلغ گزارش‌شده قابل استفاده نباشد و مقدار یا نرخ فروش خالی/نامعتبر/ناسازگار باشد، مبلغ فروش محصول با وضعیت متمایز `ZERO_FALLBACK` به صفر resolve می‌شود و هشدار ingestion ثبت می‌گردد.
4. صفر گزارش‌شدهٔ واقعی باید از ZERO_FALLBACK قابل تشخیص باشد.
5. این استثنا فقط پس از حل قطعی هویت، معنی metric، واحد، دوره و provenance مجاز است و برای سایر metricها تعمیم داده نمی‌شود.
6. ممیزی اختلاف مبلغ گزارش‌شده با مقدار × نرخ یا هشدار محاسباتی برای چنین اختلافی جزو نیازمندی نیست.

### 3.6 Excel و انتقال از PDF
- هدف، جایگزینی مسیر دریافت/استخراج CODAL PDF با Excel است؛ اما مسیر PDF تا پیاده‌سازی و اعتبارسنجی end-to-end نمونه‌های نماینده حذف یا غیرفعال نمی‌شود.
- adapterهای PDF و Excel باید به یک مرز ingestion مشترک و format-independent برسند.
- فایل‌های Excel ناهمگون‌اند؛ نام sheet، ردیف، ستون یا قالب ثابت فرض نشود.
- فرمول‌های Excel ارزیابی نمی‌شوند؛ فقط cached result معتبر خوانده می‌شود. نبود cached result نباید با مقدار ساختگی پر شود.
- برچسب و مقدار خام فقط در زمان استخراج/طبقه‌بندی استفاده می‌شوند؛ ذخیرهٔ نهایی مطابق سیاست canonical-input است.
- هر مقدار باید به دورهٔ درست خودش متصل شود؛ یک گزارش ممکن است چند ستون زمانی/دوره‌ای داشته باشد.

## 4. وضعیت اولیه و شواهد شناخته‌شده

این بخش ثبت وضعیت اولیه است، نه تأیید انطباق کل دیتابیس.

### 4.1 شواهد اولیهٔ کد
- `src/models/period.py`: مدل فعلی `FinancialPeriod` از `start_date` و `end_date` با SQL Date استفاده می‌کند؛ `PERIOD_TYPES` شامل `TTM` است؛ UniqueConstraint فعلی `(company_id, fiscal_year, period_type, end_date)` است؛ محدودیت‌های صریح Jalali، quarter range و سازگاری duration/YTD در مدل دیده نشد.
- `src/ingestion/service.py`: ورودی `ingest_codal_report` یک `period_id` برای کل گزارش می‌گیرد و همان را به همهٔ `RawFinancialFact`ها نسبت می‌دهد. `RawLineInput` فعلی اطلاعات دورهٔ مستقل برای هر مقدار/سلول ندارد.
- `src/models/normalized.py`: مدل‌های فعلی شامل `RawFinancialFact`، `NormalizedFinancialFact`، `DerivedFinancialFact` و `DerivedFinancialFactInput` هستند. این ساختار فعلی با قرارداد هدفِ عدم آرشیو raw و عدم persistence محاسبات باید تطبیق داده شود.
- `src/models/entity.py`: `Company` دارای `fiscal_year_end` متنی است؛ وجود و کفایت سازوکار تقویم مالی شرکت هنوز کامل ممیزی نشده است.
- `src/kpi/period_utils.py`: تابع فعلی `calculate_ttm` چهار مقدار آخر را جمع می‌کند؛ قرارداد ورودی آن از نظر standalone در برابر YTD و ترتیب/سازگاری دوره‌ها هنوز ممیزی نشده است.

### 4.2 نتیجهٔ اولیهٔ مهم
رابطهٔ فعلی Report و FinancialPeriod هنوز تعیین تکلیف نشده است: گزارش منطقی ممکن است در یک انتشار چند ستون زمانی داشته باشد، در حالی که سرویس فعلی یک `financial_period_id` را به کل Report و همهٔ ردیف‌های آن متصل می‌کند. پیش از تغییر مدل یا DTO باید تصمیم گرفته شود که هر مقدار canonical چگونه به دورهٔ واقعی خودش وصل می‌شود و نقش احتمالی دورهٔ اصلی گزارش چیست.

### 4.3 Inventory اولیهٔ schema و migrationها — DB-AUD-001

**مبنای بررسی:** snapshot شاخهٔ `master` با commit/tree SHA برابر `950d4b07ffb446c5188e2133e6ffa223ecacf753` در 2026-11-08. این بررسی فقط خواندنی بوده است.

#### جدول‌های ثبت‌شده در ORM فعال

| حوزه | مدل | جدول |
|---|---|---|
| Audit | `IngestionRun` | `ingestion_runs` |
| Entity | `Industry`, `Company` | `industries`, `companies` |
| Period | `FinancialPeriod` | `financial_periods` |
| Report | `Report`, `ReportVersion` | `reports`, `report_versions` |
| Financial input / mapping | `RawFinancialFact`, `FinancialMetric`, `MappingRule`, `MappingDecision`, `NormalizedFinancialFact`, `DerivedFinancialFact`, `DerivedFinancialFactInput` | `raw_financial_facts`, `financial_metrics`, `mapping_rules`, `mapping_decisions`, `normalized_financial_facts`, `derived_financial_facts`, `derived_financial_fact_inputs` |
| Provenance bridge | `NormalizedFinancialFactInput` | `normalized_financial_fact_inputs` |
| Market | `MarketDaily` | `market_daily` |
| FX | `FXRate`, `FXConversionRule` | `fx_rates`, `fx_conversion_rules` |
| Shares / actions | `ShareCountHistory`, `CorporateAction` | `share_count_history`, `corporate_actions` |

جمعاً ۱۹ جدول در metadata فعال ORM شناسایی شد. (دو جدول Forecast legacy در metadata جداگانه‌اند و در این شمارش نیستند.) جدول `schema_migrations` را خود migration runner ایجاد می‌کند و در metadata مدل‌های فعال تعریف نشده است.

دو جدول `forecast_versions` و `forecast_input_refs` فقط در `LegacyForecastBase` جداگانه تعریف شده‌اند تا migration تاریخی شمارهٔ ۷ قابل اجرا باشد؛ migration شمارهٔ ۸ آن‌ها را حذف می‌کند. این دو جدول نباید توسط `Base.metadata.create_all()` در schema فعال بازسازی شوند.

#### Migration runner

فایل `src/migrations/runner.py` تمام migrationها را به‌صورت توابع داخل همان فایل تعریف می‌کند؛ پوشهٔ جداگانه‌ای برای فایل‌های migration شماره‌دار وجود ندارد.

| Version | Name | رفتار مشاهده‌شده |
|---:|---|---|
| 1 | `baseline_schema` | ایجاد جدول‌ها از `Base.metadata.create_all()` |
| 2 | `mapping_and_derived_schema` | افزودن ستون‌های mapping به‌صورت شرطی و ایجاد mapping/derived tables |
| 3 | `normalized_fact_multi_source_provenance` | ایجاد `normalized_financial_fact_inputs` |
| 4 | `one_current_report_version` | بررسی وجود چند نسخهٔ current و سپس ایجاد unique partial index |
| 5 | `market_daily_jalali_components` | افزودن سه ستون Jalali به `market_daily` |
| 6 | `fx_rates_jalali_components` | افزودن سه ستون Jalali به `fx_rates` |
| 7 | `forecast_version_repository` | ایجاد دو جدول legacy Forecast |
| 8 | `remove_forecast_output_persistence` | حذف `forecast_input_refs` و `forecast_versions` |

Runner در صورت وجود جدول‌های قبلی و نبود رکورد migration، آن وضعیت را به‌عنوان baseline legacy نسخهٔ ۱ ثبت می‌کند. `upgrade()` نسخه‌ها را به‌ترتیب اجرا می‌کند. تست موجود، رسیدن به نسخهٔ ۸ و idempotency را روی SQLite in-memory بررسی می‌کند.

#### مسیرهای bootstrap و تنظیم اتصال

- `src/core/database.py`: اتصال فعلی hard-coded به `sqlite:///./tehran_stock.db` است؛ مسیر نسبی به working directory زمان اجرا وابسته است. `PRAGMA foreign_keys=ON` فقط روی connectionهای همین engine فعال می‌شود.
- `src/scripts/init_db.py`: مستقیماً `Base.metadata.create_all()` را اجرا می‌کند و guard اجرایی برای اطمینان از خالی/توسعه‌ای بودن DB ندارد؛ این با سیاست معماری که create_all را فقط برای empty development/bootstrap مجاز می‌داند، نیازمند بررسی و اصلاح آتی است.
- `src/scripts/migrate_db.py`: `MigrationRunner(engine).upgrade()` را اجرا می‌کند.
- `src/scripts/seed_data.py`: هفت industry و هشت metric پایه را seed می‌کند. خطا را rollback و چاپ می‌کند اما در همان مسیر exception را دوباره raise نمی‌کند؛ رفتار عملیاتی آن باید در ممیزی admission/seed بررسی شود.

#### تست‌های مرتبط شناسایی‌شده

- `src/tests/test_stage1_database_architecture.py`: ساخت schema با `Base.metadata.create_all()` روی SQLite in-memory و آزمون روابط raw→mapping→normalized و bridge چندورودی.
- `src/tests/test_stage1_database_integrity.py`: آزمون migration تا نسخهٔ ۸، idempotency، عدم بازسازی Forecast output tables، حذف legacy Forecast tables و حفظ چند جدول/رکورد ورودی در سناریوی migration، و unique current ReportVersion.
- تست‌های جداگانهٔ ingestion/market/FX و Jalali نیز در tree موجودند؛ ماتریس دقیق پوشش آن‌ها و call-siteهای تمام مدل‌ها هنوز تکمیل نشده است.

#### یافته‌های ساختاری اولیه (صرفاً ثبت، بدون تغییر)

1. `FinancialPeriod` هنوز تاریخ SQL Date و نوع TTM دارد؛ قیود Jalali و duration/YTD در مدل وجود ندارند.
2. `Report.financial_period_id` اجباری است و `ingest_codal_report` یک period_id واحد را به تمام RawFinancialFactهای یک report version اختصاص می‌دهد.
3. `RawFinancialFact` و `DerivedFinancialFact` همچنان در metadata و مدل فعال هستند؛ این با قرارداد هدف عدم آرشیو raw و عدم persistence محاسبات هم‌تراز نیست.
4. `NormalizedFinancialFact` هنوز FK اختیاری به raw fact و mapping decision دارد؛ bridge provenance نیز به raw rows وابسته است.
5. `init_db.py` و migration baseline هر دو از metadata فعال create_all استفاده می‌کنند؛ تفاوت رفتار bootstrap و migration برای DBهای موجود باید روشن شود.
6. مدل `MarketDaily` unique constraint را بر `(company_id, trade_date)` دارد، در حالی که trade_date برای دادهٔ Jalali می‌تواند NULL باشد؛ uniqueness مبتنی بر Jalali components در مدل دیده نمی‌شود.
7. مدل `FXRate` unique constraint را بر `(rate_date, currency_from, currency_to, rate_type)` دارد، در حالی که rate_date برای دادهٔ Jalali می‌تواند NULL باشد؛ uniqueness مبتنی بر Jalali components در مدل دیده نمی‌شود. باید رفتار upsert و DB constraint جداگانه تطبیق داده شود.
8. مدل‌های share/corporate action هنوز از Date استفاده می‌کنند؛ قرارداد تقویم و معنای این تاریخ‌ها باید در Task مربوط به Market/FX/Share بررسی شود، نه اینکه خودکار به Jalali تبدیل شوند.
9. تست‌های Stage 1 از SQLite in-memory و `Base.metadata.create_all()` استفاده می‌کنند؛ این تست‌ها به‌تنهایی schema نصب‌های موجود یا داده‌های واقعی را اثبات نمی‌کنند.

### 4.4 محدودیت شواهد
- این یافته‌ها از بررسی اولیهٔ فایل‌های فوق به دست آمده‌اند و جایگزین ممیزی کامل مدل‌ها، migrationها، call siteها، تست‌ها و دادهٔ واقعی DB نیستند.
- هنوز هیچ کد، schema یا داده‌ای برای این مسیر تغییر نکرده است.
- هنوز migration یا تستی برای این Packet اجرا نشده است.
- تاریخ‌ها و رکوردهای واقعی DB هنوز برای معنای تقویمی و قابلیت مهاجرت بررسی نشده‌اند.

## 5. نقشهٔ کار و Taskهای اجرایی

ترتیب زیر ترتیب پیشنهادی اجراست؛ تغییر ترتیب فقط با ثبت دلیل و وابستگی انجام شود.

### فاز A — تثبیت وضع موجود

- [~] **001 · DB-AUD-001 — Inventory کامل schema و مسیرهای DB:** فهرست مدل‌ها، جدول‌ها، FKها، unique/check constraints، indexها، migrationهای 1 تا 8، runner، همهٔ repository/serviceهای read/write و تست‌های مرتبط تهیه شود. تفاوت schema تعریف‌شده در ORM با schema حاصل از migrationها مشخص شود. هیچ تغییری در کد/DB انجام نشود.
- [~] **002 · DB-AUD-002 — ممیزی FinancialPeriod و رابطهٔ Report/Period:** یافته‌های اولیهٔ بخش 4 تکمیل شود؛ تمام مصرف‌کنندگان period، گزارش‌های چندستونه/چنددوره‌ای، DTOها، adapterها و تست‌ها بررسی شوند. پیشنهاد نهایی دربارهٔ هویت دوره، تخصیص period به هر مقدار و نقش period در Report ارائه شود. هیچ migration یا تغییر کد قبل از تأیید قرارداد انجام نشود.
- [ ] **003 · DB-AUD-003 — ممیزی Entity/Industry:** مدل، قیود، catalog، ingestion admission و migrationها با تصمیم‌های بخش 3.1 تطبیق داده شوند؛ وضعیت parent/sub-industry و داده‌های موجود روشن شود.
- [ ] **004 · DB-AUD-004 — ممیزی Report/ReportVersion/PIT:** هویت گزارش، نسخه‌ها، correction/supersession، publication timestamps، uniqueness و queryهای انتخاب نسخه در PIT بررسی شود.
- [ ] **005 · DB-AUD-005 — ممیزی واقعی داده‌های موجود و محیط‌ها:** مسیرهای DB/config، schema version، حجم و نمونهٔ داده‌های حساس به migration شناسایی شوند. داده‌ها فقط خوانده شوند؛ هیچ داده‌ای حذف/تبدیل نشود. اگر دسترسی به DB واقعی وجود ندارد، دقیقاً محدودیت و دادهٔ لازم از کاربر اعلام شود.

### فاز B — تثبیت مدل دادهٔ مالی

- [ ] **006 · DB-DES-001 — قرارداد canonical financial input:** طرح نهایی جدول/مدل ورودی canonical، metric catalog، OTHER_*، provenance، NULL و ZERO_FALLBACK، uniqueness و رفتار نسخه‌های گزارش تدوین شود. raw archive و calculated facts در طرح هدف جایی ندارند.
- [ ] **007 · DB-DES-002 — قرارداد Metric و Mapping:** catalog محدود metricها، قواعد mapping نسخه‌دار، برخورد با labelهای ناشناخته، discard/reject و جلوگیری از double counting تعریف شود؛ mapping حدسی مجاز نیست.
- [ ] **008 · DB-DES-003 — قرارداد Report/Period و چنددوره‌ای:** قرارداد مصوبی برای اتصال هر مقدار به دورهٔ صحیح در گزارش‌های دارای چند ستون/دوره تهیه شود و با PIT و correction versions سازگار باشد.
- [ ] **009 · DB-DES-004 — قرارداد Market/FX/Share:** مدل‌های market_daily، FX، conversion rules، share count و corporate actions با سیاست تاریخ جلالی، واحد IRR، نوع نرخ و PIT بررسی شوند.
- [ ] **010 · DB-DES-005 — قرارداد IngestionRun و atomicity:** مرز transaction، idempotency، خطای ingestion، عدم ثبت partial financial writes، provenance و audit failureها تعریف و با سرویس واقعی تطبیق داده شود.

### فاز C — طراحی و اجرای migration ایمن

- [ ] **011 · DB-MIG-001 — طرح migration و سازگاری داده:** migrationهای forward-only لازم، ترتیب تغییرات، FK dependency، حفظ نسخه‌های گزارش، داده‌های قدیمی، rollback/backup strategy و گزارش رکوردهای مبهم طراحی شود. پیش از تصویب طرح هیچ داده‌ای حذف نشود.
- [ ] **012 · DB-MIG-002 — پیاده‌سازی migrationهای مصوب:** فقط پس از تأیید طرح و scope؛ migrationها idempotent و سازگار با runner باشند. migration تاریخی بازنویسی/حذف نشود.
- [ ] **013 · DB-MIG-003 — تطبیق ORM و schema نهایی:** مدل‌ها، constraints، indexes، relationships و migration result با قرارداد هدف همسان شوند؛ هیچ persistence ممنوعی در مسیر تولیدی باقی نماند.

### فاز D — هم‌ترازی ingestion و adapterها

- [ ] **014 · DB-ING-001 — بازطراحی مرز DTO و تخصیص دوره:** DTOها باید امکان اتصال هر مقدار به metric، واحد، دوره و locator واقعی را داشته باشند؛ برای گزارش چندستونه، هر مقدار به دورهٔ خودش متصل شود. مرز مشترک PDF/Excel حفظ شود.
- [ ] **015 · DB-ING-002 — هم‌ترازی ingestion با canonical persistence:** طبقه‌بندی در زمان ingestion، نگهداری حداقل provenance، OTHER_*، ZERO_FALLBACK، correction versions و atomicity پیاده‌سازی شود؛ raw rows و calculated facts persist نشوند.
- [ ] **016 · DB-ING-003 — آمادگی Excel بدون حذف زودهنگام PDF:** adapter Excel با cached values و provenance workbook/sheet/cell به قرارداد مشترک متصل شود؛ نمونه‌های متنوع واقعی end-to-end بررسی شوند؛ PDF تا قبولی این معیارها حفظ شود.

### فاز E — اثبات و بستن کار

- [ ] **017 · DB-TEST-001 — تست‌های مدل و migration:** constraints، Jalali validation، uniqueness، FK، upgrade از schemaهای پشتیبانی‌شده، idempotency و حفظ داده‌ها اثبات شوند.
- [ ] **018 · DB-TEST-002 — تست‌های ingestion و PIT:** گزارش چنددوره‌ای، YTD/standalone، correction version، provenance، atomicity، mapping، NULL/ZERO_FALLBACK و عدم raw/calculated persistence پوشش داده شوند.
- [ ] **019 · DB-TEST-003 — تست یکپارچهٔ PDF/Excel و downstream contracts:** adapterها به ورودی canonical یکسان برسند و مصرف‌کنندگان downstream بدون تغییر معنای دوره/مقدار کار کنند.
- [ ] **020 · DB-EXIT-001 — تأیید نهایی Database Configuration:** تمام معیارهای خروج این Packet با PASS/BLOCKED/OPEN و شواهد واقعی ارزیابی شوند. تکمیل این مسیر فقط با بسته‌شدن معیارهای حیاتی اعلام شود.

## 6. معیارهای خروج کلی

مسیر پیکربندی دیتابیس فقط زمانی تکمیل است که:

1. قرارداد معماری با تصمیم‌های مصوب مالک سازگار و تمام بخش‌های در دامنه ممیزی شده باشد.
2. ORM models و schema واقعی migrationها با قرارداد هدف منطبق باشند.
3. دوره‌های مالی جلالی، YTD/standalone، TTM runtime-only و تخصیص دوره در گزارش‌های چندستونه بدون حدس و ابهام کار کنند.
4. ReportVersion و correction/PIT بدون نشت اطلاعات به گذشته درست عمل کنند.
5. فقط canonical selected inputs و حداقل provenance ذخیره شوند؛ raw financial-row archive و calculated financial facts/output persistence در مسیر تولیدی وجود نداشته باشد.
6. Entity/Industry admission، metric mapping، OTHER_*، NULL و ZERO_FALLBACK طبق قرارداد عمل کنند.
7. Market/FX/share foundations با تاریخ و واحد معتبر و سیاست‌های مصوب سازگار باشند.
8. migrationها روی schemaهای موجودِ در دامنه، ایمن، قابل تکرار و بدون تبدیل/حذف حدسی داده اجرا شوند.
9. ingestion اتمیک و قابل ممیزی باشد و PDF/Excel از مرز مشترک canonical استفاده کنند.
10. تست‌های هدفمند و یکپارچه با نتایج اجراشده توسط کاربر PASS باشند؛ محدودیت‌ها و موارد BLOCKED صریح ثبت شوند.

## 7. ثبت تغییرات و شواهد

| Date | Change | Evidence / Commit |
|---|---|---|
| 2026-11-08 | ایجاد Master Working Packet؛ ثبت اصول مصوب و یافته‌های اولیه FinancialPeriod/Report-period | Initial repository audit; no code/schema changes |
| 2026-11-08 | Inventory اولیهٔ ۱۹ جدول ORM، migrationهای ۱ تا ۸، bootstrap scripts و تست‌های Stage 1؛ DB-AUD-001 همچنان PARTIAL | Tree snapshot `950d4b07ffb446c5188e2133e6ffa223ecacf753`; source files inspected; no code/schema/data changes |

**یادآوری:** این Packet سند زنده است. پس از هر ممیزی یا تغییر مصوب، وضعیت Taskها، شواهد، تصمیم‌ها و نقشهٔ کار باید همین‌جا به‌روز شود. گزارش‌های اجرایی می‌توانند در فایل‌های جداگانه باشند، اما نتیجهٔ پذیرفته‌شده و وضعیت نهایی هر Task باید به این فایل منتقل شود.
