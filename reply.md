## 1. یافته دربارهٔ entry point

**نتیجه: MISSING در محدودهٔ بررسی‌شده.** entry pointای پیدا نکردم که اجرای تحلیل شرکت را از تهیهٔ ورودی‌ها تا Stage 9 هماهنگ کند.

در `src/scripts` سه اسکریپت قابل اجرا وجود دارد، اما کارشان نگهداری پایگاه داده است:

- `src/scripts/init_db.py:init_db()` ساخت جدول‌ها را اجرا می‌کند.
- `src/scripts/migrate_db.py:main()` مهاجرت پایگاه داده را اجرا می‌کند.
- `src/scripts/seed_data.py:seed_initial_data()` داده‌های اولیه را ثبت می‌کند.

`debug_alerts.py` هم یک اسکریپت نمایشیِ سطح ریشه است؛ مستقیماً `ValuationEngine` را با forecast نمونه اجرا می‌کند و مسیر تحلیل واقعی برنامه نیست. در فهرست سطح ریشه و جست‌وجوی هدفمند فایل‌های راه‌اندازی، README یا پیکربندی متعارف اجرای برنامه پیدا نشد. بنابراین نتیجه این است که entry point در **محدودهٔ بررسی‌شده** پیدا نشد، نه اینکه وجود آن در کل مخزن قطعاً ناممکن باشد.

## 2. ردیابی Stageها

- **Stage 3 — PARTIAL:** `KPIEngine.calculate_all_kpis_for_company` در `src/kpi/engine.py` یک دیکشنری مالیِ از قبل آماده‌شده می‌گیرد. `FundamentalScoringEngine.calculate_score` در `src/scoring/engine.py` از KPIهای آماده `FundamentalScoreResult` می‌سازد. فراخوانندهٔ تولیدی‌ای که داده‌ها را آماده و این دو مرحله را اجرا کند پیدا نشد.
- **Stage 4 — PARTIAL:** `TrendEngine.evaluate_trend` در `src/trend/engine.py` سری‌های تاریخیِ از قبل آماده‌شده و محدودشده به زمان ارزیابی را می‌گیرد. بارگذار یا فراخوانندهٔ تولیدی برای تهیهٔ این سری‌ها پیدا نشد.
- **Stage 5 — PARTIAL:** `generate_and_persist_forecast` در `src/forecast/service.py` داده‌های Stage 1 را از queryهای `src/forecast/queries.py` می‌خواند و `trend_result` و cutoff را از فراخواننده می‌گیرد. این تابع در کد تولیدی فراخوانی نمی‌شود؛ فراخوانندهٔ مستقیم پیدا‌شده‌ای برایش وجود ندارد. تابع forecast را برمی‌گرداند و در صورت فعال بودن `persist`، رکوردهای forecast را ذخیره می‌کند؛ مصرف‌کنندهٔ runtime برای نتیجه پیدا نشد.
- **Stage 7 → Stage 9 — CONFIRMED داخل سرویس، نه runtime:** `calculate_decision_as_of_jalali` در `src/decision/service.py` همان شیء valuation را که از `calculate_valuation_as_of_jalali` گرفته، به `DecisionEngine.make_decision` می‌دهد. هویت شرکت و دوره برای forecast و fundamental و شرکت برای market بررسی می‌شود. این اتصال داخلی سرویس، فراخوانی از entry point برنامه را ثابت نمی‌کند.
- **Stage 8 — PARTIAL:** `MarketEngine.analyze_market` در `src/market/engine.py` ردیف‌های بازار و benchmarkهای از قبل آماده‌شده می‌گیرد. `ingest_ohlc_csv` در `src/ingestion/market/ingestion.py` قیمت‌های شرکت را در `MarketDaily` ذخیره می‌کند؛ اما loader تولیدی برای خواندن تاریخچه و ساخت ورودی‌های Stage 8 پیدا نشد. منبع benchmarkهای بازار و صنعت نیز در مسیر بررسی‌شده مشخص نشد.
- **نتیجه Stage 9 — MISSING به‌عنوان خروجی برنامه:** orchestration سرویس، `ValuationDecisionResult` را برمی‌گرداند؛ مسیر runtime برای نمایش، مصرف یا ذخیرهٔ تصمیم پیدا نشد.

## 3. منشأ session و تاریخ as-of

`src/core/database.py` پایگاه SQLite، `engine` و `SessionLocal` را تعریف می‌کند. در جست‌وجوی هدفمندِ ساخت session در `src`، نمونهٔ مستقیم `SessionLocal()` فقط در `src/scripts/seed_data.py` پیدا شد. سرویس‌های ارزش‌گذاری و تصمیم‌گیری session را از فراخواننده می‌گیرند؛ اما فراخوانندهٔ برنامه‌ای که آن را بسازد و تحویل دهد پیدا نشد.

`as_of_jalali_date` به شکل tuple به سرویس‌ها داده می‌شود. `src/ingestion/market/queries.py:_validate_jalali_date` آن را هنگام انتخاب قیمت اعتبارسنجی می‌کند. محل انتخاب این تاریخ و ارسال آن از یک رابط برنامه به سرویس پیدا نشد. وجود تاریخ as-of نیز به‌تنهایی دسترس‌پذیری تاریخی همهٔ ورودی‌های دیگر را ثابت نمی‌کند.

## 4. رابط‌ها و مسئولیت‌های مفقود

به‌ترتیب وابستگی‌ها:

1. **مرز اجرای برنامه:** باید شناسهٔ شرکت/دوره و تاریخ مورد درخواست را دریافت کند، session را مدیریت کند و خروجی تصمیم را به مصرف‌کنندهٔ برنامه برساند. سازوکار یا قرارداد ورودی این مرز هنوز مشخص نیست.
2. **تولید Stage 4 و Stage 3:** باید دادهٔ تاریخی مجاز در cutoff را به `TrendResult` و دادهٔ مالی/KPI معتبر را به `FundamentalScoreResult` تبدیل کند. داده‌های Stage 1 در پایگاه داده وجود دارند، اما مسیر تولیدی اتصال آن‌ها به این دو engine پیدا نشد؛ منبع peer/history موردنیاز Stage 3 نیز مشخص نیست.
3. **تولید ورودی Stage 8:** باید ردیف‌های `MarketDaily` و benchmarkهای مرجع را به ورودی‌های تاریخ‌دار `MarketEngine` تبدیل کند. منبع authoritative برای benchmarkها و قرارداد تقویمیِ هماهنگ با تاریخ ارزیابی باید روشن شود.
4. **اتصال نتیجه‌ها به مصرف‌کننده:** باید مشخص شود forecast و تصمیم در همان اجرای برنامه مصرف می‌شوند یا از پایگاه داده بازیابی/ذخیره خواهند شد. برای تصمیم Stage 9، مسیر مصرف یا persistence پیدا نشد.

## 5. آمادگی برای پیاده‌سازی

**اتصال واقعی هنوز آمادهٔ پیاده‌سازی امن نیست.** engineها و سرویس‌های محاسباتی موجودند و Stage 7→9 درون orchestration سرویس به هم متصل است، اما ورودی‌های Stage 3، Stage 4 و Stage 8 و مرز اجرایی‌ای که session و تاریخ را تأمین کند، به آن وصل نشده‌اند. ساختن این اتصالات بدون تعیین منابع و قراردادهای مفقود، مستلزم فرض‌کردن مسیر یا داده‌ای می‌شود که شواهد فعلی پشتیبانی نمی‌کنند.

## 6. گام بعدی پیشنهادی

ابتدا قرارداد entry point واقعی را مشخص کنید: ورودی درخواست، مسئولیت ساخت/بستن session، منبع تاریخ جلالی، و مصرف‌کنندهٔ خروجی تصمیم. سپس می‌توان رابط‌های تولید Stage 3/4/8 را به همان مرز متصل کرد.

### فایل‌های بررسی‌شده

`debug_alerts.py`؛ `src/core/database.py`؛ `src/scripts/init_db.py`؛ `src/scripts/migrate_db.py`؛ `src/scripts/seed_data.py`؛ `src/forecast/service.py`؛ `src/forecast/queries.py`؛ `src/trend/engine.py`؛ `src/kpi/engine.py`؛ `src/scoring/engine.py` و `src/scoring/schema.py`؛ `src/market/engine.py` و `src/market/schema.py`؛ `src/ingestion/market/ingestion.py` و `src/ingestion/market/queries.py`؛ `src/valuation/service.py`؛ `src/decision/service.py`؛ و `src/decision/engine.py`.

فایل‌های سطح ریشه و نام فایل‌های پیکربندی/راه‌اندازی نیز بررسی شدند تا entry point یا مستندات اجرای برنامه پیدا شود. **هیچ کدی، تستی یا گزارشی را تغییر ندادم و هیچ تست یا runtimeای اجرا نکردم.**

=========================================================
# Report of P49 — Evidence-Based Data Source and Interface Mapping

## 1. Stage 3 — ردیابی داده‌ها

- **CONFIRMED:** `src/ingestion/service.py:ingest_codal_report` از `ReportVersion` و `RawFinancialFact` استفاده می‌کند. `src/ingestion/codal/ingestion.py:ingest_codal_pdf` مسیر استخراج PDF و ذخیرهٔ همان factهای خام را به آن می‌سپارد. منشأ خام، محتوای استخراج‌شده از گزارش CODAL است؛ زمان انتشار به‌صورت ورودی به ingestion داده می‌شود.
- **PARTIAL:** مدل‌های `NormalizedFinancialFact`, `FinancialMetric`, `MappingDecision` و `NormalizedFinancialFactInput` در [src/models/normalized.py](D:/winprojects/analyzer/src/models/normalized.py) و [src/models/normalized_provenance.py](D:/winprojects/analyzer/src/models/normalized_provenance.py) قرارداد ذخیره‌سازی fact نرمال‌شده، کیفیت و provenance را تعریف می‌کنند. اما جست‌وجوی هدفمند سازنده‌های این رکوردها در `src`، به‌جز تعریف مدل‌ها، نویسنده‌ای برای تبدیل fact خام به fact نرمال‌شده پیدا نکرد.
- **PARTIAL:** [src/forecast/queries.py](D:/winprojects/analyzer/src/forecast/queries.py) توابع `load_financial_fact_periods` و `load_financial_facts` را دارد. آن‌ها `NormalizedFinancialFact` را با `FinancialMetric`, `ReportVersion` و `FinancialPeriod` join می‌کنند، شرکت و metric code را فیلتر می‌کنند و انتشارهای بعد از cutoff را کنار می‌گذارند. خروجی شامل `period_id` و provenance است؛ اما این‌ها queryهای Stage 5 هستند، فیلتر کیفیت `NormalizedFinancialFact.quality_status` ندارند و ورودی Stage 3 را مستقیماً نمی‌سازند.
- **PARTIAL:** `KPIEngine.calculate_all_kpis_for_company` در [src/kpi/engine.py](D:/winprojects/analyzer/src/kpi/engine.py) دیکشنری آماده‌ای با کلیدهایی مانند `revenue_curr`, `gross_profit`, `avg_assets`, `financial_expenses`, `nii` و `nav` می‌خواهد. داده‌های ذخیره‌شده کدهای metric دارند؛ adapter تولیدی‌ای که آن‌ها را با حفظ کیفیت به این کلیدها تبدیل کند پیدا نشد. فهرست seed در `src/scripts/seed_data.py` شامل هشت metric پایه است؛ این فهرست به‌تنهایی همهٔ ورودی‌های KPI را تأمین نمی‌کند. وجود metricهای دیگر در یک منبع خارجی یا پایگاه دادهٔ دیگری از شواهد بررسی‌شده معلوم نیست.
- **PARTIAL:** `FundamentalScoringEngine.calculate_score` در [src/scoring/engine.py](D:/winprojects/analyzer/src/scoring/engine.py) `FundamentalScoreResult` را در حافظه می‌سازد. برای امتیازدهی هر KPI، کد به دادهٔ peer کافی یا `historical_values` نیاز دارد؛ منبع یا loader تولیدی این مقادیر پیدا نشد. `EARNINGS_QUALITY` نیز در `src/kpi/universal.py` عمداً با روش `DEFERRED` مقدار ندارد، پس نمی‌توان آن را با مقدار حدسی پر کرد.

**وضع دادهٔ محلی:** فایل تنظیم‌شدهٔ `tehran_stock.db` را فقط‌خواندنی بررسی کردم؛ فهرست schema آن هیچ table یا view نداشت. بنابراین این workspace شواهدی از رکوردهای مالی ذخیره‌شده برای اثبات کفایت داده ندارد. این موضوع پایگاه‌های دادهٔ خارجی یا محیط‌های دیگر را نفی نمی‌کند.

## 2. Stage 4/5 — ردیابی روند و forecast

- **PARTIAL:** مدل‌های normalized و query دوره‌ای Stage 5 می‌توانند، در صورت وجود رکوردهای نرمال‌شده، سری‌های چنددوره‌ای با provenance انتشار و cutoff زمانی فراهم کنند. اما نویسندهٔ normalized در کد بررسی‌شده پیدا نشد و پایگاه دادهٔ محلی هم schema نداشت.
- **PARTIAL:** `TrendEngine.evaluate_trend` در [src/trend/engine.py](D:/winprojects/analyzer/src/trend/engine.py) سری‌های زمانیِ از قبل آماده و محدودشده به cutoff را می‌گیرد. loader یا adapter تولیدی‌ای که queryهای Stage 1 را به این ورودی‌ها تبدیل و `TrendResult` تولید کند پیدا نشد.
- **CONFIRMED:** `generate_and_persist_forecast` در [src/forecast/service.py](D:/winprojects/analyzer/src/forecast/service.py) session، شناسه‌های شرکت و دوره، `trend_result` و `data_cutoff_datetime` را می‌گیرد؛ خودش داده‌های normalized را می‌خواند و `CompanyForecastResult` برمی‌گرداند. در جست‌وجوی callerهای مستقیم در کد تولیدی، callerای برای این تابع پیدا نشد.
- **CONFIRMED با محدودیت:** اگر یک caller در همان اجرا نتیجهٔ برگشتی را نگه دارد، می‌تواند همان `CompanyForecastResult` را به Stage 7 بدهد و محاسبه را تکرار نکند. اما [src/forecast/repo.py](D:/winprojects/analyzer/src/forecast/repo.py) رکوردها را جداگانه بر اساس سناریو به صورت `ForecastRecord` می‌خواند؛ تابعی برای بازسازی یک `CompanyForecastResult` کامل از رکوردهای ذخیره‌شده پیدا نشد.

## 3. Stage 8 — داده‌های بازار

- **CONFIRMED:** [src/ingestion/market/ingestion.py](D:/winprojects/analyzer/src/ingestion/market/ingestion.py) داده‌های OHLC را در `MarketDaily` ذخیره می‌کند. مدل [src/models/market.py](D:/winprojects/analyzer/src/models/market.py) تاریخ جلالی را در اجزای `jalali_year/month/day` نگه می‌دارد و `trade_date` را nullable تعریف کرده است؛ مسیر CSV جلالی در رکورد جدید `trade_date=None` می‌نویسد.
- **CONFIRMED:** `select_market_price_as_of` در [src/ingestion/market/queries.py](D:/winprojects/analyzer/src/ingestion/market/queries.py) قیمت مثبت و آخرین مشاهدهٔ یک شرکت را در تاریخ جلالی یا پیش از آن انتخاب می‌کند. این query برای قیمت واحد Stage 7 است؛ تاریخچهٔ ردیف‌های لازم برای Stage 8 را نمی‌سازد.
- **PARTIAL:** `MarketEngine.analyze_market` در [src/market/engine.py](D:/winprojects/analyzer/src/market/engine.py) فهرستی از ردیف‌ها با کلید `date` و تاریخ `datetime` می‌گیرد، به‌علاوهٔ benchmarkهای اختیاری با همان قرارداد زمانی. query یا adapter تولیدی برای تبدیل ردیف‌های persisted به این ورودی پیدا نشد. [src/ingestion/common/parsing.py](D:/winprojects/analyzer/src/ingestion/common/parsing.py) تاریخ جلالی را اعتبارسنجی می‌کند و صریحاً آن را به میلادی تبدیل نمی‌کند.
- **MISSING در محدودهٔ بررسی‌شده:** مدل یا ingestion source برای benchmark بازار و صنعت پیدا نشد. `MarketDaily` هم رکورد یک شرکت را نگه می‌دارد، نه سری شاخص مرجع. بدون این منبع، خروجی‌های وابسته به relative strength/regime نمی‌توانند بر دادهٔ benchmark معتبر متکی باشند.

## 4. قرارداد Stage 7/9

- **CONFIRMED:** `calculate_valuation_as_of_jalali` در [src/valuation/service.py](D:/winprojects/analyzer/src/valuation/service.py) نیازمند session، شناسهٔ شرکت و دوره، `CompanyForecastResult` و تاریخ جلالی tuple است. هویت شرکت/دورهٔ forecast را کنترل می‌کند، ورودی‌های رزروشده را از override منع می‌کند و در نبود قیمت واجد شرایط خطا می‌دهد. provenance قیمت منتخب را به metadata ارزش‌گذاری اضافه می‌کند.
- **CONFIRMED:** `calculate_decision_as_of_jalali` در [src/decision/service.py](D:/winprojects/analyzer/src/decision/service.py) علاوه بر این‌ها، `FundamentalScoreResult` و `MarketSignalResult` می‌خواهد؛ هویت شرکت/دورهٔ fundamental و شرکت market را کنترل می‌کند. همان شیء valuation که از Stage 7 دریافت کرده، به `DecisionEngine.make_decision` می‌دهد.
- **UNKNOWN/ناقص در قرارداد زمانی:** سرویس Stage 9 بررسی نمی‌کند که `market_result.as_of_date` با تاریخ جلالی استفاده‌شده برای قیمت Stage 7 متناظر باشد. تاریخ Stage 8 از نوع `datetime` است و تاریخ Stage 7 tuple جلالی؛ تبدیل یا قاعدهٔ تطبیق آن‌ها در مسیر بررسی‌شده وجود ندارد.
- **CONFIRMED:** `ValuationDecisionResult` در `src/decision/service.py` هر دو نتیجهٔ valuation و decision را در حافظه برمی‌گرداند. مدل persistence یا مصرف‌کنندهٔ برنامه برای `FinalDecisionResult` در محدودهٔ جست‌وجو پیدا نشد.

## 5. قرارداد اجرایی مشترک

برای اجرای قابل‌ردیابی، entry point آینده دست‌کم به این قراردادها نیاز دارد: `company_id` و `period_id`؛ منبع مشروع تاریخ جلالی ارزیابی؛ مالکیت و چرخهٔ عمر session؛ تولید و اعتبارسنجی نتیجه‌های upstream؛ و مقصد خروجی تصمیم.

`SessionLocal` در `src/core/database.py` تعریف شده، اما در جست‌وجوی ساخت session در `src` فقط `src/scripts/seed_data.py` آن را ایجاد می‌کند. سرویس‌های Stage 7/9 session را از caller می‌گیرند. Stage 5 هم cutoff زمانی مستقل و از نوع `datetime` می‌گیرد؛ رابطهٔ معتبر آن cutoff با تاریخ جلالی Stage 7 در runtime موجود مشخص نشده است.

## 6. طبقه‌بندی شکاف‌ها

- **قابل استفاده مجدد — CONFIRMED:** مدل‌های raw/normalized، queryهای PIT Stage 5، تابع انتخاب قیمت جلالی Stage 7، سرویس Stage 5 که نتیجه را برمی‌گرداند، و orchestration داخلی Stage 7→9.
- **مفقود در کد بررسی‌شده — MISSING:** نویسندهٔ `RawFinancialFact` به `NormalizedFinancialFact`؛ adapter ورودی Stage 3 همراه با وضعیت کیفیت؛ loader/adapter تولید `TrendResult`؛ loader تاریخچهٔ `MarketDaily` برای Stage 8؛ منبع/مدل benchmark؛ entry point هماهنگ‌کننده؛ و مقصد مصرف یا ذخیرهٔ Stage 9.
- **نامعلوم — UNKNOWN:** اینکه محیط خارجی/دیتابیس دیگری normalized factها یا benchmarkها را فراهم می‌کند؛ کفایت واقعی metricها در آن محیط؛ و مرجع کسب‌وکاری انتخاب تاریخ as-of.

## 7. آمادگی پیاده‌سازی

اتصال کامل runtime را نمی‌توان بر اساس شواهد موجود بدون فرض بسازم. بخش‌های میانی قابل‌استفاده‌اند، اما دادهٔ محلی فعلی خالی است و مسیر تولید normalized و ورودی‌های Stage 3/4/8 کامل نیست.

کوچک‌ترین گام فنیِ پشتیبانی‌شده، پیش از نوشتن orchestration، **تعیین و اثبات مسیر مجاز از fact خام CODAL به fact نرمال‌شده** است: metric mapping، وضعیت کیفیت، provenance و publication time باید منبع و قرارداد مشخص داشته باشند. schemaها بخشی از مقصد را تعریف می‌کنند، اما mapping یا writer موجود در کد پیدا نشد؛ بنابراین مقداردهی آن‌ها نباید حدس زده شود. پس از آن می‌توان adapterهای Stage 3/4 را بر query PIT موجود بنا کرد. Stage 8 نیز جداگانه به قرارداد تاریخ و منبع benchmark نیاز دارد.

## 8. فایل‌های بررسی‌شده

- مدل‌ها و provenance مالی: [src/models/normalized.py](D:/winprojects/analyzer/src/models/normalized.py)، [src/models/normalized_provenance.py](D:/winprojects/analyzer/src/models/normalized_provenance.py)، [src/models/report.py](D:/winprojects/analyzer/src/models/report.py)، [src/models/period.py](D:/winprojects/analyzer/src/models/period.py).
- ورود و خواندن دادهٔ مالی: [src/ingestion/service.py](D:/winprojects/analyzer/src/ingestion/service.py)، [src/ingestion/codal/ingestion.py](D:/winprojects/analyzer/src/ingestion/codal/ingestion.py)، [src/ingestion/codal/pipeline.py](D:/winprojects/analyzer/src/ingestion/codal/pipeline.py)، [src/forecast/queries.py](D:/winprojects/analyzer/src/forecast/queries.py)، [src/core/point_in_time.py](D:/winprojects/analyzer/src/core/point_in_time.py)، [src/scripts/seed_data.py](D:/winprojects/analyzer/src/scripts/seed_data.py).
- Stage 3/4/5: [src/kpi/engine.py](D:/winprojects/analyzer/src/kpi/engine.py)، [src/kpi/universal.py](D:/winprojects/analyzer/src/kpi/universal.py)، [src/kpi/conditional.py](D:/winprojects/analyzer/src/kpi/conditional.py)، [src/kpi/industry.py](D:/winprojects/analyzer/src/kpi/industry.py)، [src/scoring/engine.py](D:/winprojects/analyzer/src/scoring/engine.py)، [src/trend/engine.py](D:/winprojects/analyzer/src/trend/engine.py)، [src/forecast/service.py](D:/winprojects/analyzer/src/forecast/service.py)، [src/forecast/repo.py](D:/winprojects/analyzer/src/forecast/repo.py).
- Stage 7/8/9: [src/models/market.py](D:/winprojects/analyzer/src/models/market.py)، [src/ingestion/market/ingestion.py](D:/winprojects/analyzer/src/ingestion/market/ingestion.py)، [src/ingestion/market/queries.py](D:/winprojects/analyzer/src/ingestion/market/queries.py)، [src/ingestion/common/parsing.py](D:/winprojects/analyzer/src/ingestion/common/parsing.py)، [src/market/engine.py](D:/winprojects/analyzer/src/market/engine.py)، [src/market/schema.py](D:/winprojects/analyzer/src/market/schema.py)، [src/valuation/service.py](D:/winprojects/analyzer/src/valuation/service.py)، [src/decision/service.py](D:/winprojects/analyzer/src/decision/service.py)، [src/decision/schema.py](D:/winprojects/analyzer/src/decision/schema.py).
- برای منشأ session به بررسی P48 از [src/core/database.py](D:/winprojects/analyzer/src/core/database.py) و `src/scripts/seed_data.py` اتکا کردم. فایل `tehran_stock.db` فقط‌خواندنی از نظر جدول‌ها و viewها بررسی شد؛ schema خالی بود.

هیچ کد، تست یا گزارشی را تغییر ندادم و هیچ تستی اجرا نکردم. **نکتهٔ اجرایی:** دستور ابتدایی workspace من شامل `git status --short` هم بود؛ آن را قبل از اینکه متن P49 را بخوانم اجرا کردم. این عملیات فقط‌خواندنی بود و پس از آن هیچ عملیات Git دیگری انجام ندادم.