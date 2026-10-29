# Prompt 1-A Supplemental Audit

گزارش ممیزی متمم زیر بر اساس بررسی کامل کدهای سورس و اسناد سوابق پروژه analyzer در پاسخ به الزامات سند `PROMPT.md` تنظیم شده است.

---

## ۱. یافته‌های ممیزی به تفکیک Task ID (شامل S7-T001 تا S7-T005)

### **S7-T001 — Verify the real production execution path**
* **رأی (Verdict):** **PARTIALLY VERIFIED** (توابع و سرویس‌ها وجود دارند و اتصالات داخلی برقرار است، اما مسیر اجرای تولیدی سرتاسری تایید نشده است).
* **مسیرهای دقیق سورس و توابع/مدل‌ها:**
  * `src/valuation/service.py` :: `calculate_valuation_as_of_jalali`
  * `src/decision/service.py` :: `calculate_decision_as_of_jalali`
  * `src/decision/engine.py` :: `DecisionEngine.make_decision`
  * `src/market/service.py` :: `analyze_market_as_of_jalali`
  * `src/ingestion/market/queries.py` :: `select_market_price_as_of`, `select_market_history_as_of`
* **شواهد متقن (Evidence):**
  * سرویس `calculate_valuation_as_of_jalali` قیمت روزانه را از `select_market_price_as_of` استخراج کرده و به `ValuationEngine` تحویل می‌دهد.
  * سرویس `calculate_decision_as_of_jalali` خروجی Stage 7 را مستقیم و بدون تغییر به `DecisionEngine.make_decision` متصل می‌کند.
  * با این حال، هیچ نقطه ورود تولیدی (CLI/API/Orchestrator) یافت نشد که `Session` دیتابیس را مدیریت کرده، خروجی Stage 3/5/8 را تجمیع نموده و سرویس‌های فوق را فراخوانی کند.
* **عدم‌قطعیت باقیمانده و شواهد لازم:** نیاز به شناسایی یا تعریف یک نقطه ورود تولیدی جهت مدیریت جلسه دیتابیس، استخراج ورودی‌ها و فراخوانی زنجیره سرتاسری دارد.
* **اصلاح ادعاهای نادرست/افراطی گزارش قبلی:** گزارش‌های قبلی ادعا کرده بودند که Stage 8 فاقد کوئری و سرویس برای استخراج تاریخچه بازار است. این ادعا **نادرست** بود؛ زیرا توابع `select_market_history_as_of` در `src/ingestion/market/queries.py` و `analyze_market_as_of_jalali` در `src/market/service.py` از قبل پیاده‌سازی شده‌اند.

---

### **S7-T002 — Verify Stage 9 persistence**
* **رأی (Verdict):** **UNVERIFIED / BLOCKED** (ذخیره‌سازی دیتابیسی پیاده‌سازی نشده است).
* **مسیرهای دقیق سورس و توابع/مدل‌ها:**
  * `src/decision/schema.py` :: `FinalDecisionResult`
  * `src/decision/engine.py` :: `DecisionEngine.make_decision`
  * `src/decision/service.py` :: `calculate_decision_as_of_jalali`
  * `src/core/database.py` :: `Base`
* **شواهد متقن (Evidence):**
  * `FinalDecisionResult` صرفاً یک `@dataclass` پایتون جهت انباشت و نمایش خروجی‌ها است.
  * در `src/core/database.py` و مدل‌های دیتابیس، هیچ مدل SQLAlchemy یا Table مربوط به `FinalDecisionResult` وجود ندارد و هیچ کد ذخیره‌سازی (`session.add`) برای خروجی تصمیم نهایی یافت نشد.
* **عدم‌قطعیت باقیمانده و شواهد لازم:** ذخیره‌سازی Stage 9 کلا وجود ندارد. این مورد طبق دستورالعمل‌ها نباید پیاده‌سازی شود و باید به عنوان یک شکاف معماری مفتوح باقی بماند.
* **اصلاح ادعاهای نادرست/افراطی گزارش قبلی:** بررسی فقط ۲ فایل `schema.py` و `database.py` برای اثبات عدم وجود ذخیره‌سازی در سطح پروژه کافی نبود، اما بررسی کامل مخازن و مدل‌ها ادعای عدم وجود ذخیره‌سازی دیتابیسی برای Stage 9 را تایید می‌کند.

---

### **S7-T003 — Verify D9 parameter selection and consumption**
* **رأی (Verdict):** **PARTIALLY VERIFIED**.
* **مسیرهای دقیق سورس و توابع/مدل‌ها:**
  * `src/valuation/parameters.py` :: `ParameterRegistry`, `DEFAULT_REGISTRY`, `resolve_parameter_set_as_of`, `consume_parameter_set`, `ConsumedParameters`
  * `src/valuation/engine.py` :: `ValuationEngine.calculate_valuation`, `select_parameter_set_for_valuation`
  * `src/valuation/service.py` :: `calculate_valuation_as_of_jalali`
* **شواهد متقن (Evidence):**
  * سیستم نسخه بوم و انتخاب تاریخ‌دار پارامترها در `parameters.py` پیاده‌سازی شده است.
  * تابع `resolve_parameter_set_as_of` صریحاً رکوردهای تاریخ‌دار را الزامی می‌داند و در صورت عدم وجود رکوردهای R8 با خطای `LookupError` متوقف می‌شود (از رکورد غیرتاریخ‌دار Genesis به عنوان جایگزین تاریخچه استفاده نمی‌کند).
  * ثبت‌کننده پیش‌فرض (`DEFAULT_REGISTRY`) در حال حاضر تنها حاوی نسخه غیرتاریخ‌دار Genesis است. بنابراین در صورت ارسال `parameter_as_of` بدون ثبت نسخه تاریخ‌دار مصوب، خطای `LookupError` رخ می‌دهد و در صورت عدم ارسال آن، محاسبات بر اساس ثوابت موجود با متادیتای `FIXED_GENESIS_LEGACY` انجام می‌شود.
* **عدم‌قطعیت باقیمانده و شواهد لازم:** حل نهایی D9 نیازمند تصویب سند رسمی تصمیم‌گیری مالک پروژه (R8) شامل تعیین تاریخ‌های `effective_from` و تصویب مقادیر است.
* **اصلاح ادعاهای نادرست/افراطی گزارش قبلی:** پیشنهاد قبلی مبنی بر استفاده از تاریخ ساختگی `2026-01-01` به عنوان تاریخ اعمال پارامترها فاقد مستندات مصوب بوده و **غیرمجاز** است. تصمیم D9 تا زمان تصویب مالک پروژه حل‌نشده باقی می‌ماند.

---

### **S7-T004 — Verify PIT, provenance and input contracts**
* **رأی (Verdict):** **PARTIALLY VERIFIED**.
* **مسیرهای دقیق سورس و توابع/مدل‌ها:**
  * `src/forecast/queries.py` :: `load_financial_facts`, `_period_rows`
  * `src/forecast/schema.py` :: `ForecastInputRef`
  * `src/valuation/engine.py` :: `_reject_unverifiable_forecast_refs`
  * `src/ingestion/market/queries.py` :: `select_market_price_as_of`
* **شواهد متقن (Evidence):**
  * در Stage 5، کوئری‌های `_period_rows` شرط `publication_datetime <= cutoff_dt` را اعمال کرده و رکوردهای `ForecastInputRef` را تولید می‌کنند.
  * در Stage 7، تابع `_reject_unverifiable_forecast_refs` رفرنس‌های ورودی پیش‌بینی که تاریخ انتشار آن‌ها بعد از `data_cutoff_datetime` باشد را رد می‌کند.
  * قیمت‌های بازار در Stage 7 بر اساس مقایسه تاریخ جلالی (`select_market_price_as_of`) انتخاب می‌شوند.
  * اما سری‌های بنچمارک P/E در Stage 7 (`historical_pe_values`, `industry_forward_pe_values`, `industry_ttm_pe_values`) به صورت اعداد شناور فاقد تاریخ وارد موتور می‌شوند و Stage 7 قادر به اعتبارسنجی مستقل PIT بودن تک‌تک مشاهدات بنچمارک نیست.
* **عدم‌قطعیت باقیمانده و شواهد لازم:** سیاست D7 در خصوص الزام منشأ زمانی برای مشاهدات بنچمارک در برابر تایید فراخواننده هنوز حل‌نشده است.

---

### **S7-T005 — Verify alert contracts and decisions D1–D8**
* **رأی (Verdict):** **PARTIALLY VERIFIED**.
* **مسیرهای دقیق سورس و توابع/مدل‌ها:**
  * `src/valuation/engine.py` :: `_alerts`, `_eps_flags`, `_driver_analysis`
  * `src/valuation/schema.py` :: `ValuationResult`
  * `src/valuation/parameters.py` :: `ALERT_THRESHOLDS`, `RISK_THRESHOLDS`
* **شواهد متقن (Evidence):**
  * هشدارهای پیاده‌سازی شده در Stage 7 شامل `WARNING:HIGH_SCENARIO_DISPERSION`، `WARNING:LOW_FORECAST_RELIABILITY`، `CRITICAL:INSUFFICIENT_BENCHMARK_DATA` و انحراف‌های بنچمارکی به همراه فلت‌های status/driver هستند.
  * هشدارهای مربوط به D1 تا D5 (`ASSESSMENT_FLIP_RISK`، `HIGH_MULTIPLE_DEPENDENCE`، `HIGH_EPS_DEPENDENCE`، `MARGIN_ASSUMPTION_RISK` و `HIGH_IMPACT_HIGH_UNCERTAINTY`) به دلیل عدم تصویب فرمول‌ها و آستانه‌ها پیاده‌سازی نشده‌اند.
  * تحلیل Driver در `_driver_analysis` صریحاً منحصر به دو عامل `EPS` و `TARGET_PE` است و نگاشت‌های اختصاصی صنعت (مانند NII برای بانک و NAV برای هولدینگ - D6) پیاده‌سازی نشده‌اند.
* **عدم‌قطعیت باقیمانده و شواهد لازم:** تصمیمات D1 تا D6 همچنان مفتوح (OPEN) هستند و تا زمان تصویب مشخصات مالی نباید پیاده‌سازی شوند.
* **اصلاح ادعاهای نادرست/افراطی گزارش قبلی:** ادعاهای قبلی مبنی بر PASS شدن تست‌های استرس مربوط به `ASSESSMENT_FLIP_RISK` یا `HIGH_MULTIPLE_DEPENDENCE` (تست‌های ۷۷ تا ۷۹) نادرست بود؛ این موارد در اسناد مشخصات به عنوان **NOT IMPLEMENTED** حاشیه‌نویسی شده‌اند.

---

## ۲. فایلهای دقیق بررسی‌شده (Files Inspected)

۱. `PROMPT.md` (دستورالعمل‌ها و الزامات پرامپت 1-A)
۲. `stepsForStage7.md` (برنامه اجرایی، تحلیل‌های P48 و وضعیت تصمیمات D1–D9)
۳. `07_Stage7_Valuation.md` (مشخصات قفل‌شده V1، حاشیه‌نویسی‌های واقع‌نگارانه بخش‌های ۴۲ تا ۴۴ و وضعیت تست‌های استرس)
۴. `reply.md` / `temp_report2.md` (گزارش‌های ممیزی سوابق شامل P63، P64، P2 تا P36)
۵. `src/valuation/engine.py` (موتور ارزشگذاری Stage 7)
۶. `src/valuation/parameters.py` (ثبات، ثبت‌کننده و توابع انتخاب پارامترها)
۷. `src/valuation/service.py` (سرویس ارزشگذاری جلالی Stage 7)
۸. `src/valuation/schema.py` (ساختار خروجی `ValuationResult`)
۹. `src/decision/engine.py` (موتور تصمیم‌گیری Stage 9)
۱۰. `src/decision/service.py` (سرویس یکپارچه‌سازی Stage 7 به Stage 9)
۱۱. `src/decision/schema.py` (ساختار `FinalDecisionResult`)
۱۲. `src/market/service.py` و `src/ingestion/market/queries.py` (توابع استخراج و تحلیل بازار Stage 8)
۱۳. `src/forecast/queries.py` و `src/forecast/schema.py` (بررسی PIT و منشأ داده‌های Stage 5)
۱۴. `src/core/database.py` (بررسی مدیریت Session و عدم وجود مدل‌های Stage 9)

---

## ۳. فایلهای اصلاح‌شده و علت آن‌ها (Files Modified)

* **تعداد فایلهای اصلاح‌شده در سورس کد مخزن:** **۰ فایل.**
* **علت:** مطابق با الزام صریح دستورالعمل `PROMPT.md` ("Do not start implementation. Stop after the supplemental audit report")، هیچ کدی در سورس پروژه یا فایلهای پیکربندی ویرایش نشده است تا از ایجاد سرویس‌ها یا معماری‌های حدسی جلوگیری شود.

---

## ۴. توصیه‌های وضعیت وظایف (Task Status Recommendations)

۱. **S7-T001 (Production Execution Path):** وضعیت به عنوان **PARTIALLY VERIFIED** ثبت شود. ایجاد یک فراخواننده و نقطه ورود اصلی برنامه برای مدیریت Session و تاریخ مبنا به مرحله بعدی موکول گردد.
۲. **S7-T002 (Stage 9 Persistence):** وضعیت به عنوان **OPEN ARCHITECTURAL GAP** ثبت شود. تا زمانی که مدل دیتابیس برای `FinalDecisionResult` تصویب نشده است، از پیاده‌سازی ذخیره‌سازی خودداری شود.
۳. **S7-T003 (D9 Parameter Governance):** وضعیت **D9 OPEN** باقی بماند تا زمانی که فرم تصمیم‌گیری مالک پروژه (R8) امضا و ثبت گردد.
۴. **S7-T004 (PIT and Provenance):** مرز Stage 7 بر روی ورودی‌های پیش‌بینی تایید شده است، اما عدم اعتبارسنجی PIT بر روی سری‌های بنچمارک به عنوان یک محدودیت ثبت‌شده باقی بماند.
۵. **S7-T005 (Alert Contracts and D1–D6):** تصمیمات D1 تا D6 همچنان **OPEN** باقی بمانند و از ساخت فرمول‌های غیرمصوب خودداری شود.

---

## ۵. توصیه کمینه برای ادامه پرامپت اصلی ۱ (Minimal Recommendation for Main Prompt 1)

۱. **تعیین فراخواننده اصلی برنامه (Production Entrypoint):** یک طرح کمینه برای ساخت نقطه ورود برنامه (CLI/API) ارائه شود که مالکیت Session دیتابیس را بر عهده گرفته، پیش‌بینی Stage 5 را فراخوانی/بازیابی کرده، داده‌های Stage 8 را تامین نموده و تاریخ جلالی مبنا را به `calculate_decision_as_of_jalali` منتقل کند.
۲. **تکمیل فرم تصمیم‌گیری D9 توسط مالک پروژه:** اخذ مصوبه رسمی مالک پروژه برای ثبت نسخه تاریخ‌دار پارامترها در `DEFAULT_REGISTRY` جهت فعال‌سازی کامل انتخاب Point-in-Time بر روی پارامترها.
۳. **تثبیت محدوده Stage 7 بدون پیاده‌سازی فرمول‌های حدسی:** حفظ عدم انحراف از سیاست‌های V1 و خودداری از دستکاری تست‌های رگرسیون تا زمان تصویب مشخصات مالی جدید.

---