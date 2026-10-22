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