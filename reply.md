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
# گزارش ممیزی متمم پرامپت 1-B (Prompt 1-B Supplemental Audit Report)

**شناسه پرامپت:** Prompt 1-B  
**پرامپت والدی:** Prompt 1  
**شناسه‌های وظایف (Task IDs):** S7-T001, S7-T002, S7-T003, S7-T004, S7-T005  
**نوع وظیفه:** AUDIT ONLY + SUPPLEMENTAL REPORT CORRECTION (فقط ممیزی و ارزیابی شواهد سورس‌کد، بدون تغییر در کدهای اجرایی یا اجرای تست‌ها)

---

## ۱. شکاف‌های شواهد بررسی‌شده (Evidence Gaps Addressed)

در این گزارش، شکاف‌های شواهد ذکرشده در `PROMPT.md` برای وظایف ۵ گانه ممیزی Stage 7 بر اساس بررسی مستقیم سورسکدها، مدل‌ها، سرویس‌ها و تست‌های موجود در مخزن پروژه به شرح زیر بسته‌شده‌اند:

1. **S7-T001 (مسیر اجرای تولیدی):** تفکیک دقیق توابع موجود، فراخوانی‌های داخلی سرویس به سرویس، فراخواننده‌های تولیدی، و ارزیابی مسیر اجرایی سرتاسری پروژه همراه با مالکیت Session و ورودی‌های بالادستی.
2. **S7-T002 (ذخیره‌سازی Stage 9):** بررسی جامع تمامی مدل‌های SQLAlchemy، جداول دیتابیس، مخازن (Repositories) و سرویس‌ها برای تعیین وضعیت قطعیت وجود یا عدم وجود ماندگاری دیتابیسی برای `FinalDecisionResult`.
3. **S7-T003 (انتخاب و مصرف پارامترهای D9):** ردیابی نحوه انتخاب نسخه‌های پارامتر بر اساس تاریخ، بررسی مقادیر مصرف‌شده در محاسبات در برابر متادیتای ثبتی، و رفتار سیستم در صورت عدم وجود نسخه تاریخ‌دار مصوب.
4. **S7-T004 (عدم انحراف زمانی Point-in-Time و منشأ داده‌ها):** تدوین ماتریس جامع شواهد برای فیلدهای زمانی و اعتبارسنجی‌های انجام‌شده روی قیمت‌های بازار، ورودی‌های پیش‌بینی Stage 5، سری‌های بنچمارک P/E، سیگنال‌های بازار و خروجی‌های ارزش‌گذاری/تصمیم‌گیری.
5. **S7-T005 (ارزیابی انفرادی تصمیمات D1 تا D8):** بررسی تک‌تک تصمیمات D1 تا D8 به صورت جداگانه از منظر مستندات حاکم، وضعیت پیاده‌سازی، نمادهای دقیق سورس‌کد، تست‌ها و مصرف‌کنندگان خروجی.

---

## ۲. یافته‌های تفکیکی ممیزی به همراه مسیر دقیق فایل‌ها و توابع

### **S7-T001 — Production Execution Path**
* **رأی (Verdict):** **UNVERIFIED / GAP IDENTIFIED** (سرویس‌ها و اتصالات داخلی وجود دارند، اما هیچ نقطه ورود یا فراخواننده تولیدی سرتاسری در scope بررسی‌شده یافت نشد).
* **مسیرهای دقیق سورس و توابع/کلاس‌ها:**
  * `src/forecast/service.py` :: `generate_and_persist_forecast`
  * `src/valuation/service.py` :: `calculate_valuation_as_of_jalali`
  * `src/market/service.py` :: `analyze_market_as_of_jalali`
  * `src/decision/service.py` :: `calculate_decision_as_of_jalali`
  * `src/decision/engine.py` :: `DecisionEngine.make_decision`
  * `src/ingestion/market/queries.py` :: `select_market_price_as_of`, `select_market_history_as_of`
  * `src/core/database.py` :: `SessionLocal`
* **یافته‌ها و شواهد:**
  * *سرویس‌های موجود:* سرویس `calculate_valuation_as_of_jalali` قیمت روزانه را از دیتابیس استخراج کرده و به `ValuationEngine` می‌دهد. سرویس `analyze_market_as_of_jalali` سری OHLCV را از دیتابیس خوانده و به `MarketEngine` ارسال می‌کند. سرویس `calculate_decision_as_of_jalali` خروجی Stage 7 را مستقیم به `DecisionEngine.make_decision` متصل می‌کند.
  * *فراخوانی‌های داخلی:* تابع `calculate_decision_as_of_jalali` در `src/decision/service.py` صریحاً `calculate_valuation_as_of_jalali` را فراخوانی می‌کند.
  * *فراخواننده تولیدی سرتاسری (Production Caller):* **در scope بررسی‌شده یافت نشد (Not found in the inspected scope).** هیچ فایل CLI، API، Orchestrator یا Worker در مخزن وجود ندارد که مدیریت `SessionLocal` را بر عهده گرفته، خروجی‌های Stage 3 (Scoring)، Stage 5 (Forecast) و Stage 8 (Market) را استخراج نموده و زنجیره اجرایی را تا Stage 9 فراخوانی کند. جستجوی فراخواننده‌ها تنها به فایلهای تست محدود شد.

---

### **S7-T002 — Stage 9 Persistence**
* **رأی (Verdict):** **ABSENT (UNVERIFIED PERSISTENCE GAP)** (ذخیره‌سازی دیتابیسی خروجی تصمیم نهایی پیاده‌سازی نشده است).
* **مسیرهای دقیق سورس و توابع/کلاس‌ها:**
  * `src/decision/schema.py` :: `FinalDecisionResult`
  * `src/decision/engine.py` :: `DecisionEngine.make_decision`
  * `src/decision/service.py` :: `calculate_decision_as_of_jalali` -> `ValuationDecisionResult`
  * `src/core/database.py` :: `Base`
  * `src/models/` :: `report.py`, `normalized.py`, `market.py`, `entity.py`, `period.py`, `share_action.py`, `fx.py`, `audit.py`
* **یافته‌ها و شواهد:**
  * `FinalDecisionResult` صرفاً یک `@dataclass` پایتون جهت انباشت خروجی تصمیم‌گیری و ساخت داشبورد است.
  * تابع `calculate_decision_as_of_jalali` خروجی را در قالب داتاکلاس `ValuationDecisionResult` برمی‌گرداند.
  * در تمامی مدل‌های SQLAlchemy پروژه (`Base`)، هیچ جدول دیتابیسی، مدل ORM، کلاس Repository یا دستور `session.add()` / `session.commit()` برای ذخیره‌سازی `FinalDecisionResult` وجود ندارد.
  * سیستم فاقد لایه ماندگاری برای خروجی‌های Stage 9 است.

---

### **S7-T003 — D9 Parameter Selection and Consumption**
* **رأی (Verdict):** **PARTIALLY VERIFIED / D9 UNRESOLVED** (مکانیسم انتخاب فیل‌کلوز کار می‌کند، اما ثبت‌کننده فاقد نسخه‌های تاریخ‌دار مصوب است).
* **مسیرهای دقیق سورس و توابع/کلاس‌ها:**
  * `src/valuation/parameters.py` :: `ParameterRegistry`, `DEFAULT_REGISTRY`, `resolve_parameter_set`, `resolve_parameter_set_as_of`, `consume_parameter_set`, `ConsumedParameters`, `select_parameter_set_for_valuation`, `GENESIS_VERSION_KEY`
  * `src/valuation/engine.py` :: `ValuationEngine.calculate_valuation`, `_resolve_parameter_governing_timestamp`
  * `src/valuation/service.py` :: `calculate_valuation_as_of_jalali`
  * `src/tests/test_stage7_valuation.py` :: `test_p33_*`, `test_p35_*`, `test_p36_*`, `test_d9_*`
* **یافته‌ها و شواهد:**
  * *ردیابی انتخاب:* تاریخ قطع داده (`data_cutoff_datetime`) مبنای اصلی انتخاب پارامترهاست (`_resolve_parameter_governing_timestamp`).
  * *رفتار Fail-Closed:* اگر انتخاب تاریخ‌دار روی ثبت‌کننده پیش‌فرض (`DEFAULT_REGISTRY`) فراخوانی شود، به دلیل اینکه Genesis فاقد `effective_from` است، صریحاً خطای `LookupError` صادر می‌کند ("R8: historical selection requires R8-dated records").
  * *حالت میراثی:* در صورت عدم ارسال درخواست انتخاب تاریخ‌دار، موتور از مقادیر ثوابت پایتون استفاده کرده و متادیتای `mode: FIXED_GENESIS_LEGACY` و `point_in_time_selection_applied: False` را ثبت می‌کند.
  * *مصرف واقعی:* شیء `ConsumedParameters` دقیقاً مقادیر انتخاب‌شده را فریز می‌کند. ۳۳ پارامتر مستقیماً در فرمول‌ها مصرف می‌شوند و ۵ پارامتر غیرمصرفی به همراه ثوابت خارج از ثبت‌کننده (`LITERALS_OUTSIDE_REGISTRY`) در متادیتا گزارش می‌شوند.
  * *علت مفتوح ماندن D9:* انتخاب تاریخ‌دار پارامترهای تاریخی نیازمند امضا و ثبت سند تصمیم مالک پروژه (R8) شامل تعیین تاریخ‌های `effective_from` و مقادیر مربوطه است.

---

### **S7-T004 — Point-in-Time (PIT) and Provenance Evidence Matrix**
* **رأی (Verdict):** **PARTIALLY VERIFIED** (حفاظت PIT روی ورودی‌های پیش‌بینی Stage 5 اعمال می‌شود، اما سری‌های بنچمارک P/E فاقد شناسنامه زمانی هستند).

#### **ماتریس شواهد منشأ زمانی و PIT:**

| دسته‌بندی ورودی / خروجی | فیلدهای زمانی موجود | اعتبارسنجی انجام‌شده | منبع اثبات در کد | محدودیت و ریسک باقیمانده |
| :--- | :--- | :--- | :--- | :--- |
| **قیمت روزانه بازار** | `jalali_year`, `jalali_month`, `jalali_day`, `trade_date` (قابل NULL) | مقایسه عددی تاریخ جلالی `<=` تاریخ درخواست (`as_of_jalali_date`)؛ حذف مشاهدات آینده. | `src/ingestion/market/queries.py::select_market_price_as_of` | مقایسه بر اساس جلالی انجام می‌شود؛ اعتبارسنجی UTC Datetime مستقیم در برابر Cutoff پیش‌بینی ندارد. |
| **ورودی‌های پیش‌بینی Stage 5** | `available_at` (در `ForecastInputRef`), `publication_datetime` (در `ReportVersion`), `data_cutoff_datetime` | کوئری `_period_rows` شرط `publication_datetime <= cutoff_dt` را اعمال می‌کند. Stage 5 ورودی‌های بعد از Cutoff را حذف می‌کند. Stage 7 در `_reject_unverifiable_forecast_refs` ورودی‌های فاقد تاریخ یا بعد از Cutoff را رد می‌کند. | `src/forecast/queries.py`, `src/forecast/engine.py`, `src/valuation/engine.py` | منشأ زمانی برای ورودی‌ها opt-in است؛ اگر Stage 5 ورودی بدون ref ارسال کند، مسیر میراثی آن را می‌پذیرد. |
| **سری‌های بنچمارک تاریخی و صنعتی** | اعداد شناور بدون تاریخ (`historical_pe_values`, `industry_forward_pe_values`, `industry_ttm_pe_values`) | **هیچ اعتبارسنجی زمانی انجام نمی‌شود.** فقط فیلتر عددی `NaN`/`inf`/`<=0` اعمال می‌گردد. | `src/valuation/engine.py::calculate_valuation` | سری‌های بنچمارک P/E فاقد تاریخ مشاهده یا انتشار هستند؛ Stage 7 قادر به اعتبارسنجی PIT بودن بنچمارک‌ها نیست. |
| **سیگنال‌های بازار (Stage 8)** | تاپل `jalali_date` روی مشاهدات | `select_market_history_as_of` مشاهدات بعد از تاریخ جلالی درخواست را حذف می‌کند. | `src/ingestion/market/queries.py`, `src/market/service.py` | وابسته به ارسال داده توسط فراخواننده است؛ اعتبارسنجی UTC Datetime ندارد. |
| **خروجی‌های ارزش‌گذاری و تصمیم** | `calculation_timestamp` (UTC), `data_cutoff_datetime` (UTC), `valuation_date`, `market_price_date` | تاریخ‌های `valuation_date` و `market_price_date` نرمال‌سازی شده و در متادیتا منعکس می‌شوند. | `src/valuation/engine.py`, `src/decision/engine.py` | پذیرش `valuation_date > data_cutoff_datetime` بدون صادر شدن خطا یا هشدار (اثبات‌شده در تست `test_p6_cutoff_pit_limitation_pinned`). |

---

### **S7-T005 — Individual Decision Verification (D1–D8)**
* **رأی (Verdict):** **PARTIALLY IMPLEMENTED / POLICY OPEN**.

#### **ارزیابی تک‌تک تصمیمات D1 تا D8:**

1. **تصمیم D1 (Assessment Flip Risk):**
   * *سند حاکم:* `07_Stage7_Valuation.md` §50; `stepsForStage7.md` D1.
   * *وضعیت پیاده‌سازی:* **DEFERRED / UNRESOLVED** (صفر ارجاع به `ASSESSMENT_FLIP_RISK` در کل سورسکد `src/valuation/`).
   * *علت:* فرمول شوک، وضعیت‌های مشمول Flip، روش شوک (یک‌عاملی یا مشترک) و Severity تصویب نشده‌اند.
   * *تست‌های بررسی‌شده:* تست `test_p2_required_flip_dependence_alerts_missing` (در فایل `test_stage7_valuation.py:425` که به عنوان تست اثبات عدم پیاده‌سازی، Fail می‌ماند).
2. **تصمیم D2 (Multiple Dependence):**
   * *سند حاکم:* `07_Stage7_Valuation.md` §51; `stepsForStage7.md` D2.
   * *وضعیت پیاده‌سازی:* **DEFERRED / UNRESOLVED** (ثابت `ALERT_THRESHOLDS["high_dependence_share"] = 0.60` در `parameters.py:73` تعریف شده اما در `engine.py` معطل و بدون ارجاع است).
   * *علت:* فرمول سهم انحراف ارزش منصفانه از ضریب P/E در برابر EPS تصویب نشده است. ارزیابی P26 اثبات کرد که شوک‌های یک‌عاملی روی فرمول خطی ارزش، همواره سهم ۵۰/۵۰ تولید می‌کنند و آستانه 0.60 بدون تغییر فرمول غیرقابل دستیابی است.
3. **تصمیم D3 (EPS Dependence & Revision):**
   * *سند حاکم:* `07_Stage7_Valuation.md` §52; `stepsForStage7.md` D3.
   * *وضعیت پیاده‌سازی:* **DEFERRED / UNRESOLVED** (هیچ کدی برای `HIGH_EPS_DEPENDENCE` یا `FORECAST_RISK` در Stage 7 وجود ندارد).
   * *علت:* روند تجدیدنظر پیش‌بینی (`revision_trend`) در Stage 5 (`src/forecast/repo.py`) محاسبه شده و مستقیماً به Stage 9 (`src/decision/engine.py`) متصل می‌شود و از مرز Stage 7 عبور نمی‌کند.
4. **تصمیم D4 (Margin Assumption Risk):**
   * *سند حاکم:* `07_Stage7_Valuation.md` §53; `stepsForStage7.md` D4.
   * *وضعیت پیاده‌سازی:* **DEFERRED / UNRESOLVED** (مرز ورودی Stage 7 فاقد هرگونه سری حاشیه سود یا هزینه است).
   * *علت:* تابع `calculate_valuation` تنها سود پیش‌بینی‌شده (EPS) و ضریب P/E را ورودی می‌گیرد و بدون توسعه قرارداد ورودی، محاسبه هشدار حاشیه سود غیرممکن است.
5. **تصمیم D5 (High Impact + High Uncertainty):**
   * *سند حاکم:* `07_Stage7_Valuation.md` §45–47; `stepsForStage7.md` D5.
   * *وضعیت پیاده‌سازی:* **DEFERRED / UNRESOLVED** (مقادیر `driver_impact`، `driver_uncertainty` و `review_priority` برای دو متغیر EPS و Target P/E در `src/valuation/engine.py:469-498` محاسبه می‌شوند، اما هشدار متظاهر صادر نمی‌شود).
   * *علت:* خروجی `review_priority` صرفاً جنبه متادیتای اطلاع‌رسانی دارد و آستانه صریحی برای صدور هشدار تصویب نشده است.
6. **تصمیم D6 (Sector Driver Chains & P/NAV):**
   * *سند حاکم:* `07_Stage7_Valuation.md` §42–44; `stepsForStage7.md` D6.
   * *وضعیت پیاده‌سازی:* **DEFERRED / UNRESOLVED** (رتبه‌بندی درایورها در موتور همیشه منحصر به `["EPS", "TARGET_PE"]` است؛ `nav_per_share` در متادیتا ثبت می‌شود اما تابع `calculate_nav_fair_value` در `models.py` فراخوانی نمی‌شود).
   * *تست‌های بررسی‌شده:* تست `test_p2_sector_driver_decomposition_missing` (در فایل `test_stage7_valuation.py:406` به عنوان تست اثبات عدم پیاده‌سازی، Fail می‌ماند).
7. **تصمیم D7 (PIT Benchmark Provenance):**
   * *سند حاکم:* `07_Stage7_Valuation.md` §56–57, §85; `stepsForStage7.md` D7.
   * *وضعیت پیاده‌سازی:* **DEFERRED / UNRESOLVED**.
   * *علت:* ورودی‌های بنچمارک به صورت اعداد شناور فاقد تاریخ وارد می‌شوند و امکان اعتبارسنجی PIT بودن آنها در Stage 7 وجود ندارد.
8. **تصمیم D8 (Alert Vocabulary & Triggers):**
   * *سند حاکم:* `07_Stage7_Valuation.md` §10, §49, §54–55; `stepsForStage7.md` D8.
   * *وضعیت پیاده‌سازی:* **PARTIALLY IMPLEMENTED (VOCABULARY MISMATCH)**.
   * *علت:* هشدارهای انحراف بنچمارکی با نسبت 1.50 پیاده‌سازی شده‌اند اما به جای اسامی سند (`HISTORICAL/INDUSTRY_VALUATION_DIVERGENCE`) با اسامی `WATCH:FORWARD_PE_ABOVE/BELOW_*` صادر می‌شوند. همچنین `INSUFFICIENT_PEER_DATA` به عنوان Flag صادر می‌شود نه Alert.

---

## ۳. فایلهای اضافی بررسی‌شده (Additional Files Inspected)

### **گروه‌بندی فایلهای بررسی‌شده به تفکیک Task ID:**

* **جهت S7-T001 (Production Execution Path):**
  * `src/scoring/engine.py`
  * `src/forecast/engine.py`, `src/forecast/service.py`
  * `src/valuation/service.py`
  * `src/market/service.py`
  * `src/decision/service.py`, `src/decision/engine.py`
  * `src/ingestion/market/queries.py`
  * `src/core/database.py`
* **جهت S7-T002 (Stage 9 Persistence):**
  * `src/decision/schema.py`, `src/decision/engine.py`, `src/decision/service.py`
  * `src/core/database.py`
  * `src/models/report.py`, `src/models/normalized.py`, `src/models/market.py`, `src/models/entity.py`, `src/models/period.py`, `src/models/share_action.py`, `src/models/fx.py`, `src/models/audit.py`
* **جهت S7-T003 (D9 Parameter Governance):**
  * `src/valuation/parameters.py`, `src/valuation/engine.py`, `src/valuation/service.py`
  * `src/tests/test_stage7_valuation.py`
* **جهت S7-T004 (PIT and Provenance):**
  * `src/forecast/queries.py`, `src/forecast/schema.py`, `src/forecast/engine.py`
  * `src/valuation/schema.py`, `src/valuation/service.py`, `src/valuation/engine.py`
  * `src/market/schema.py`, `src/market/service.py`, `src/ingestion/market/queries.py`
* **جهت S7-T005 (D1–D8 Policies):**
  * `07_Stage7_Valuation.md`, `stepsForStage7.md`, `reply.md` / `temp_report2.md`
  * `src/valuation/engine.py`, `src/valuation/parameters.py`, `src/valuation/schema.py`
  * `src/decision/engine.py`

---

## ۴. تست‌های بررسی‌شده و آنچه اثبات می‌کنند (Tests Inspected)

*(توضیح صریح: مطابق با دستورالعمل‌های اکید پرامپت، هیچ تستی در این نوبت اجرا نشده است و نتایج زیر بر اساس مستندات ثبت‌شده در مخزن است)*:

1. **`test_p33_genesis_snapshot_matches_live_constants`:** اثبات می‌کند که اسنپ‌شات Genesis دقیقاً ۳۸ پارامتر دارد و `effective_from` آنها `None` است.
2. **`test_p33_as_of_without_dated_records_raises`:** اثبات می‌کند که فراخوانی انتخاب تاریخ‌دار بر روی ثبت‌کننده پیش‌فرض منجر به صادر شدن خطای `LookupError` می‌شود.
3. **`test_p35_as_of_selection_governs_calculation_and_snapshot_matches`:** اثبات می‌کند که در صورت وجود ثبت‌کننده تاریخ‌دار، پارامتر انتخاب‌شده مستقیماً وضعیت ارزش‌گذاری و محاسبات را تغییر می‌دهد.
4. **`test_d9_effective_cutoff_governs_selection_not_valuation_date`:** اثبات می‌کند که `data_cutoff_datetime` (نه `valuation_date`) حاکم بر انتخاب پارامترها است.
5. **`test_p5_undated_benchmark_series_carry_no_provenance`:** اثبات می‌کند که ورودی‌های بنچمارک به صورت اعداد فاقد تاریخ پذیرفته می‌شوند و اعتبارسنجی PIT ندارند.
6. **`test_p6_cutoff_pit_limitation_pinned`:** اثبات می‌کند که پذیرش `valuation_date > data_cutoff_datetime` بدون خطای PIT انجام می‌شود.
7. **`test_p32_input_ref_after_cutoff_rejected_on_valuation_path`:** اثبات می‌کند که در صورت وجود شناسنامه زمانی در ورودی پیش‌بینی، ورودی‌های بعد از Cutoff رد می‌شوند.
8. **`test_p2_sector_driver_decomposition_missing` (تست Fail):** اثبات می‌کند که تجزیه درایورها بر اساس صنعت (REVENUE, NII, NAV) پیاده‌سازی نشده است.
9. **`test_p2_required_flip_dependence_alerts_missing` (تست Fail):** اثبات می‌کند که هشدارهای پنج‌گانه D1 تا D5 در کد صادر نمی‌شوند.

---

## ۵. عدم‌قطعیت‌های باقیمانده و شواهد یا تصمیمات لازم

1. **عدم‌قطعیت D9:** نیازمند تصویب رسمی "فرم تصمیم‌گیری مالک پروژه" (R8) شامل تعیین تاریخ‌های `effective_from` و مقادیر پارامترها جهت فعال‌سازی انتخاب تاریخ‌دار بر روی ثبت‌کننده عمومی.
2. **عدم‌قطعیت D1 تا D6:** نیازمند تصویب مشخصات مالی صریح برای فرمول‌های شوک، آستانه‌های وابستگی متغیرها، و نگاشت درایورهای صنعت.
3. **عدم‌قطعیت مسیر اجرای تولیدی (S7-T001):** نیازمند تعریف یا پیاده‌سازی یک نقطه ورود سرتاسری (CLI/API Orchestrator) برای مدیریت Session دیتابیس و پاس دادن ورودی‌های آماده‌شده بین Stageها.
4. **عدم‌قطعیت ماندگاری Stage 9 (S7-T002):** نیازمند تصمیم‌گیری معماری در خصوص ایجاد جدول دیتابیس برای ذخیره‌سازی `FinalDecisionResult`.

---

## ۶. فایلهای اصلاح‌شده (Files Modified)

* **فایلهای اصلاح‌شده در سورس‌کد پروژه:** **۰ فایل.**
* **توضیح:** مطابق با الزامات صریح پرامپت 1-B (`Audit and report only` / `Do not modify source code, tests, configuration`), هیچ فایل سورس‌کدی تغییر داده نشده است.

---

## ۷. توصیه‌های وضعیت وظایف (Recommended Task Statuses)

* **S7-T001 (Production Execution Path):** وضعیت **OPEN / GAP IDENTIFIED** (نیازمند ایجاد نقطه ورود اجرایی سرتاسری).
* **S7-T002 (Stage 9 Persistence):** وضعیت **OPEN / PERSISTENCE GAP** (فاقد مدل دیتابیس جهت ذخیره‌سازی).
* **S7-T003 (D9 Parameter Governance):** وضعیت **OPEN / R8 PENDING** (مکانیسم کد آمادگی دارد، اما نیازمند امضای سند تصمیم R8 است).
* **S7-T004 (Point-in-Time & Provenance):** وضعیت **PARTIALLY VERIFIED** (مرز Stage 5 حاکم است اما سری‌های بنچمارک فاقد تاریخ هستند).
* **S7-T005 (D1–D8 Alert Policies):** وضعیت **DEFERRED / POLICY OPEN** (تصمیمات D1 تا D6 مفتوح هستند و تا زمان تصویب نباید پیاده‌سازی شوند).

---

## ۸. تصمیم در خصوص احراز معیارهای پذیرش ممیزی پرامپت ۱ (Audit Acceptance Criteria Decision)

**نتیجه:** معیارهای پذیرش ممیزی کامل پرامپت ۱ به دلیل وجود **شکاف‌های ساختاری باقیمانده** زیر به طور کامل برآورده نشده است و پرامپت ۱ در مرحله ممیزی متوقف می‌ماند:

1. **عدم وجود نقطه ورود اجرایی تولیدی (S7-T001):** نبود CLI/API جهت هماهنگی Session و زنجیره سرتاسری Stage 3/5/7/8/9.
2. **عدم وجود ماندگاری دیتابیسی خروجی تصمیم نهایی (S7-T002):** نبود مدل ORM برای ذخیره‌سازی `FinalDecisionResult`.
3. **عدم امضای سند D9 (S7-T003):** نبود نسخه‌های تاریخ‌دار مصوب R8 در ثبت‌کننده پارامترها.
4. **مفتوح بودن تصمیمات مالی D1 تا D6 (S7-T005):** نبود فرمول‌ها و آستانه‌های مصوب برای هشدارهای شوک و درایورهای صنعتی.

---
# Prompt 1-C
# گزارش ممیزی Stage 7 (اجرای پرامپت Prompt 1-C)

**شناسه کارهای ممیزی:** S7-T001, S7-T002, S7-T005  
**نوع ممیزی:** صرفاً ممیزی و تحلیل خطوط لوله و کدها (Audit Only — بدون هیچ‌گونه تغییر در کد، تست یا پیکربندی).

---

### ۱. محدوده دقیق دسترسی و فایل‌های بررسیشده (Inspection Boundary)

مطابق با الزامات صریح پرامپت 1-C، صرفاً فایل‌های تامین‌شده و در دسترس مورد بازبینی قرار گرفتند:

#### فایل‌های الزامی بررسیشده:
* `stepsForStage7.md`
* `reply.md`
* `07_Stage7_Valuation.md`
* `src/core/database.py`
* `src/decision/schema.py`
* `src/decision/engine.py`
* `src/decision/service.py`
* `src/valuation/service.py`
* `src/valuation/parameters.py`
* `src/forecast/service.py`
* `src/market/service.py`
* `src/tests/test_stage7_valuation.py`

#### فایل‌های تکمیلی در دسترس و بررسی‌شده:
* `PROMPT.md`, `temp_report2.md`, `src/valuation/engine.py`, `src/valuation/models.py`, `src/valuation/schema.py`, `src/market/engine.py`, `src/market/parameters.py`, `src/market/schema.py`, `src/forecast/engine.py`, `src/forecast/schema.py`, `src/forecast/queries.py`, `src/ingestion/market/queries.py`, `src/scoring/engine.py`, `src/scoring/schema.py`, `src/tests/test_stage9_decision.py`, `src/tests/test_stage8_market_service.py`, `src/tests/test_stage8_market_parameters.py`, `src/ingestion/codal/pipeline.py`, `src/ingestion/service.py`, `.github/workflows/tests.yml`, `05_Stage5_Forecast_Engine.md`.

#### فایل‌های مستثنی‌شده (فاقد دسترسی در ورودی ممیزی):
* `src/models/market.py`, `src/models/normalized.py`, `src/models/report.py`, `src/tests/test_codal_extraction.py`, `src/tests/test_market_history_query.py`, `src/tests/test_stage3_scoring.py`, `src/tests/test_stage5_forecast.py`, `src/tests/test_stage8_market.py`, `zErrors.md`.

---

### ۲. S7-T001 — تحلیل مسیر اجرای تولیدی (Production Execution Path)

بررسی دقیق سرویس‌های مراحل مختلف در فایل‌های موجود، نتایج زیر را به دست می‌دهد:

1. **Stage 5 Forecast Service (`src/forecast/service.py`):**
   * **توابع:** تابع `generate_and_persist_forecast` خروجی `CompanyForecastResult` را تولید کرده و رکوردهای پیش‌بینی را در `ForecastRecordRepository` ذخیره می‌کند.
   * **وضعیت فراخوانی:** این سرویس در فایل‌های تست (مانند `test_stage7_valuation.py`) فراخوانی شده است؛ اما **هیچ فایل نقطه ورود اصلی (CLI، API یا Pipeline Runner)** در فایل‌های تامین‌شده وجود ندارد که فراخوانی آن را در مسیر اجرای برنامه ثبت کند.
   * **طبقه بندی:** **Partially verified / Exists but caller unproven** (سرویس وجود دارد اما فراخواننده تولیدی آن اثبات نشده است).

2. **Stage 7 Valuation Service (`src/valuation/service.py`):**
   * **توابع:** تابع `calculate_valuation_as_of_jalali` با استخراج قیمت روزانه بازار از `select_market_price_as_of` (`src/ingestion/market/queries.py`) و ارسال آن به `ValuationEngine.calculate_valuation` خروجی ارزش‌گذاری را محاسبه می‌کند.
   * **وضعیت فراخوانی:** این تابع در `src/decision/service.py` (داخل `calculate_decision_as_of_jalali`) فراخوانی می‌شود. با این حال، خود `calculate_decision_as_of_jalali` فاقد فراخواننده در نقطه ورود اصلی برنامه است.
   * **طبقه بندی:** **Partially verified** (اتصال داخلی به Stage 9 برقرار است، اما نقطه ورود اجرایی برنامه تامین نشده است).

3. **Stage 8 Market Service (`src/market/service.py`):**
   * **توابع:** تابع `analyze_market_as_of_jalali` داده‌های تاریخی را از `select_market_history_as_of` خوانده و به `MarketEngine.analyze_market` ارسال می‌کند.
   * **وضعیت فراخوانی:** این سرویس به صورت مستقیم در `src/decision/service.py` ارکستره نشده است؛ سرویس Stage 9 خروجی آماده `market_result` را به عنوان ورودی دریافت می‌کند. هیچ فراخواننده اجرایی جهت خواندن داده بازار و پاس دادن آن به Stage 9 در کد تامین‌شده مشاهده نشد.
   * **طبقه بندی:** **Partially verified / Exists but caller unproven**.

4. **Stage 9 Decision Service (`src/decision/service.py`):**
   * **توابع:** تابع `calculate_decision_as_of_jalali` نتایج Stage 5 (`forecast_result`)، Stage 3 (`fundamental_result`) و Stage 8 (`market_result`) را دریافت کرده و متغیرهای Stage 7 و Stage 9 را ارکستره می‌کند.
   * **طبقه بندی:** **Partially verified** (زنجیره داخلی Stage 5 → Stage 7 → Stage 9 برقرار است، اما زنجیره سرتاسری تولیدی Stage 3 → 5 → 7 → 8 → 9 از نقطه ورود واقعی برنامه اثبات نشده است).

---

### ۳. S7-T002 — تحلیل ماندگاری داده‌های تصمیم در Stage 9 (Persistence Analysis)

بررسی دقیق ساختار پایگاه‌داده، مدل‌ها و سرویس‌های مرتبط با Stage 9 نتایج زیر را روشن می‌سازد:

1. **ساختار کلاس خروجی (`src/decision/schema.py`):**
   * کلاس `FinalDecisionResult` یک Dataclass استاندارد پایتون است و از `Base` در SQLAlchemy ارث‌بری نمی‌کند.
2. **رفتار موتور تصمیم (`src/decision/engine.py`):**
   * متد `DecisionEngine.make_decision` یک نمونه از `FinalDecisionResult` را در حافظه ساخته و برمی‌گرداند؛ هیچ عملیات دیتابیسی انجام نمی‌دهد.
3. **رفتار سرویس ارکستراسیون (`src/decision/service.py`):**
   * تابع `calculate_decision_as_of_jalali` پارامتر `session: Session` را دریافت کرده و خروجی `ValuationDecisionResult(valuation=valuation, decision=decision)` را برمی‌گرداند.
   * در این مرز هیچ‌گونه متد `session.add()`، `session.commit()` یا متد ذخیره‌سازی برای `FinalDecisionResult` وجود ندارد.
4. **ساختار پایگاه‌داده (`src/core/database.py`):**
   * صرفاً شامل تعاریف `engine` SQLite، `SessionLocal` و `Base` است و فاقد جدول یا مدل برای Stage 9 است.

#### طبقه‌بندی رسمی:
* **NOT FOUND IN SUPPLIED FILES** (هیچ مسیر ماندگاری برای خروجی تصمیم Stage 9 در فایل‌های تامین‌شده پیدا نشد).

#### فایل‌های دقیق مورد نیاز جهت اثبات ماندگاری در صورت وجود در مخزن:
* مدل ORM مربوط به جدول تصمیمات Stage 9 (مانند `src/models/decision.py` یا مخزن `src/decision/repo.py` در صورت وجود در کل پروژه).
* فایل‌های مایگریشن دیتابیس (Alembic یا اسکریپت‌های SQL).
* سرویس‌ها یا فراخواننده‌های ماندگاری که خروجی `FinalDecisionResult` را به دیتابیس منتقل کنند.

---

### ۴. S7-T005 — تفسیر تست‌های مربوط به سیاست‌های D1 و D6

بررسی فایل `src/tests/test_stage7_valuation.py` و فایل‌های پیاده‌سازی مرتبط (`src/valuation/engine.py`, `src/valuation/parameters.py`, `src/valuation/models.py`) موارد زیر را اثبات می‌کند:

#### الف) تفکیک تعاملات صنعت و Driverهای اختصاصی (D6 Analysis):
* **مشخصات در سند:** در سند `07_Stage7_Valuation.md` بخش‌های ۴۲ تا ۴۴ زنجیره‌های Driver اختصاصی صنعت (درآمد برای غیرمالی، تسهیلات/NII برای بانک، و NAV/P/NAV برای هولدینگ) مطرح شده است.
* **کد پیاده‌سازی:** در `src/valuation/engine.py` محور اصلی محاسبات ارزش‌گذاری Forward P/E (\\(Fair Value = Forecast EPS \times Target PE\\)) است. متد `_driver_analysis` خروجی `valuation_driver_ranking` را دائماً برابر با `["EPS", "TARGET_PE"]` تنظیم می‌کند. پارامتر `nav_per_share` صرفاً در متادیتای خروجی ثبت می‌شود و تاثیری در ارزش منصفانه ندارد.
* **اثبات منطقی تست‌ها:** تست‌های `test_v1_sector_examples_use_only_eps_and_target_pe_drivers` و `test_v1_uses_stage5_eps_without_recalculating_from_net_profit` اثبات می‌کنند که تحت سیاست V1، ارزش‌گذاری تمامی صنایع صرفاً بر پایه دو Driver اصلی (`EPS` و `TARGET_PE`) و مستقیم از EPS پیش‌بینی‌شده Stage 5 انجام می‌شود و هیچ فرمول ساختگی بدون مشخصات برای تفکیک صنایع اعمال نمی‌گردد.
* **وابستگی‌های معوق:** پیاده‌سازی زنجیره‌های اختصاصی صنعت (D6) نیازمند تصمیم مالک پروژه در خصوص فرمول‌ها، ورودی‌های جدید زنجیره و نگاشت صنایع است.

#### ب) هشدارها و تحلیل حساسیت (D1–D5 Analysis):
* **مشخصات در سند:** در سند مشخصات پنج هشدار پیش‌فرض شامل `ASSESSMENT_FLIP_RISK` ،`HIGH_MULTIPLE_DEPENDENCE` ،`HIGH_EPS_DEPENDENCE` ،`MARGIN_ASSUMPTION_RISK` و `HIGH_IMPACT_HIGH_UNCERTAINTY` درج شده است.
* **کد پیاده‌سازی:** در `src/valuation/engine.py` هشدارها به هشدارهای با مشخصات روشن (مانند عدم قطعیت سناریو، قابلیت اطمینان پایین، انحراف از بنچمارک و وضعیت‌های قیمتی) محدود شده‌اند. ثابت `high_dependence_share = 0.60` در `src/valuation/parameters.py` تعریف شده اما در موتور ارزش‌گذاری استفاده نشده است (فاقد مرجع کاربردی).
* **اثبات منطقی تست‌ها:** تست‌های `test_v1_defers_undefined_flip_dependence_and_assumption_alerts` و `test_p3_flip_dependence_alerts_remain_explicitly_unresolved` اثبات می‌کنند که هشدارهای تعریف‌نشده D1–D5 به طور صریح از لیست‌های `alerts` و `valuation_risk_flags` حذف شده‌اند تا از انتشار هشدارهای غیرمصوب و فاقد فرمول شفاف جلوگیری شود. تغییر وضعیت ارزش‌گذاری (مثلا از ATTRACTIVE به FAIR) بر اساس محاسبات آستانه‌ای رخ می‌دهد، اما هشدار `ASSESSMENT_FLIP_RISK` تولید نمی‌شود.
* **وابستگی‌های معوق:** پیاده‌سازی این هشدارها مستلزم تصویب صریح آستانه‌ها، اندازه شوک، و فرمول سهم وابستگی توسط مالک پروژه است.

---

### ۵. خلاصه محدودیت‌های دسترسی و نتایج ممیزی (Summary Report)

1. **فایل‌های بررسیشده:** ۱۲ فایل اصلی الزامی در پرامپت 1-C به همراه ۲۱ فایل تکمیلی موجود در لیست پروپوزال ممیزی شدند.
2. **فایل‌های مفقود جهت تکمیل ارزیابی کلی:**
   * فایل نقطه ورود اصلی اجرای برنامه (مانند `main.py` یا اسکریپت CLI ارکستراسیون سرتاسری) جهت اثبات اجرا در تولید.
   * مدل‌های ORM دیتابیس برای Stage 9 جهت بررسی امکان ماندگاری نتایج تصمیم.
3. **نتایج تاییدشده در کد:**
   * مرزهای ارکستراسیون سرویس Stage 7 به Stage 9 در `src/decision/service.py` درست و متصل است.
   * مدل ارزش‌گذاری Stage 7 بر روی محور اصلی Forward P/E منطبق بر مشخصات مصوب V1 به صورت کاملاً قطعی و Backtestable عمل می‌کند.


---

# Prompt 1-C-B — Final Evidence Closure Report (S7-T001, S7-T002)

**Prompt ID:** Prompt 1-C-B  
**Task IDs:** S7-T001, S7-T002  
**Work type:** AUDIT ONLY + REPORT/DOCUMENTATION UPDATES  

## Exact files supplied and actually inspected

### Supplied and inspected (production Python and tests under the extracted tree; paths shown as present on disk, corresponding to the `src/...` names in the prompt):

- core/database.py, core/jalali.py, core/point_in_time.py
- decision/__init__.py, decision/engine.py, decision/rules.py, decision/schema.py, decision/service.py
- evaluation/* (all listed modules)
- forecast/* (all listed modules including service.py, repo.py)
- ingestion/* (service, codal/*, common/*, fx/*, market/*)
- kpi/* (all listed)
- market/__init__.py, market/engine.py, market/indicators.py, market/parameters.py, market/schema.py, market/service.py
- migrations/__init__.py, migrations/runner.py
- models/* (audit, entity, forecast, fx, market, normalized, normalized_provenance, period, report, share_action)
- scoring/* (all listed)
- scripts/init_db.py, scripts/migrate_db.py, scripts/seed_data.py
- trend/* (all listed)
- debug_alerts.py, requirements.txt, .github/workflows/tests.yml
- tests/test_stage789_service_interface.py, test_stage9_decision.py, test_stage7_valuation.py, test_stage5_forecast.py, test_market_history_query.py, test_stage3_scoring.py, test_stage1_database_architecture.py, test_stage1_database_integrity.py, test_codal_extraction.py, test_stage8_market.py, test_stage8_market_parameters.py
- Documentation: WORKFLOW_RULES.md, tasksToDo.md, stepsForStage7.md, reply.md, 00_a_Master_Architecture.md, 05_Stage5_Forecast_Engine.md, 07_Stage7_Valuation.md, 08_Stage8_Market_Engine.md, 09_Stage9_Decision_Dashboard.md, 10_Production_Codal_Extraction_and_Data_Load.md, 11_Database_Architecture_Stage1.md, 12_Database_Architecture_V1.1.md, 99_Architecture_Change_Log.md, PROJECT_HANDOFF_INSTRUCTIONS.md

### Explicitly missing from the supplied set (not inspected; conclusions involving them are UNVERIFIED where dependent):

- src/valuation/__init__.py
- src/valuation/engine.py
- src/valuation/models.py
- src/valuation/parameters.py
- src/valuation/schema.py
- src/valuation/service.py
- src/tests/test_stage8_market_service.py (file not present; test_stage8_market.py is present instead)
- temp_report2.md (listed in mandatory workflow documents; not present in the three zip archives)

Because the entire `valuation/` package is absent, any call chain that depends on the body of `calculate_valuation_as_of_jalali`, its imports, or its internal session/price/parameter usage cannot be fully re-verified from source in this delivery. Import statements and call sites that name those symbols were still examined in the supplied files that reference them.

## S7-T001 Verdict

**Verdict: NOT FOUND IN THE COMPLETE SUPPLIED SOURCE SET** for a real end-to-end production execution path connecting Stage 3 → 5 → 7 → 8 → 9.

Service definitions and limited service-to-service links exist; production callers and a complete upstream-to-Stage-9 path do not appear in the supplied files. Test-only callers are present. Database session ownership is defined (`SessionLocal`) but never shown in a production orchestrator within the supplied set.

### Evidence table (S7-T001)

| Connection | Caller / call site | Upstream input | Downstream consumer | Caller classification | Evidence | Limitation |
|---|---|---|---|---|---|---|
| Stage 5 production function | Definition: `forecast/service.py` :: `generate_and_persist_forecast` | Session (caller-owned), Stage 1 facts + TrendResult via internal queries/adapter | Returns `CompanyForecastResult`; persists via `ForecastRecordRepository.save` | Service definition + internal persistence; no production caller | Function at line ~294; repository save at ~408–410; only non-test references are exports in `forecast/__init__.py` | No production caller found in supplied set |
| Stage 5 callers | Only in `tests/test_stage5_forecast.py` (multiple call sites) | Test fixtures / in-memory session | Test assertions | Test-only | Multiple `generate_and_persist_forecast(...)` calls inside test functions | Bounded to supplied tests |
| Stage 8 production function | Definition: `market/service.py` :: `analyze_market_as_of_jalali` | Session (caller-owned), company_id, as_of_jalali_date; optional benchmarks | Returns `MarketSignalResult` from `MarketEngine.analyze_market` | Service definition; no production caller | Function lines 51–82; uses `select_market_history_as_of` then engine | No production caller found |
| Stage 8 callers | Only in tests (`test_stage8_market.py`, interface tests supply MarketSignalResult directly) | Test data | Test assertions | Test-only | No non-test call sites outside definition | Bounded to supplied set |
| Stage 9 orchestration service | Definition: `decision/service.py` :: `calculate_decision_as_of_jalali` | Session, `CompanyForecastResult`, Jalali date, `FundamentalScoreResult`, `MarketSignalResult` | Calls `calculate_valuation_as_of_jalali` then `DecisionEngine.make_decision`; returns `ValuationDecisionResult` | Service-to-service call (to missing valuation module) + engine | Lines 26–74; explicit call at 56–64 and 65–73 | Body of valuation service not in supplied files → partial UNVERIFIED |
| Stage 9 engine | `decision/engine.py` :: `DecisionEngine.make_decision` | Fundamental, ValuationResult, MarketSignalResult, optional reliability etc. | Returns `FinalDecisionResult` dataclass | Service definition | Lines 31–50+; constructs `FinalDecisionResult` | No production caller |
| Stage 9 callers | `tests/test_stage9_decision.py`, `tests/test_stage789_service_interface.py` | Test fixtures / in-memory Session | Test assertions | Test-only | e.g. `_run` → `calculate_decision_as_of_jalali` in interface test; many direct `make_decision` in decision tests | No production caller |
| Stage 3 scoring | Definition: `scoring/engine.py` :: `FundamentalScoringEngine.calculate_score` | company_id, period_id, industry, kpi_results, optional peers/history | Returns `FundamentalScoreResult` | Service definition; no production caller | Class and method present | No production caller found in supplied set |
| Database session ownership | `core/database.py` :: `SessionLocal` | N/A | Used by `scripts/seed_data.py` and tests | Utility / test / seed only | `SessionLocal = sessionmaker(...)`; seed script opens session and commits seed data | No production pipeline owns a Session for valuation/decision |
| Executable entrypoints | `scripts/init_db.py`, `scripts/migrate_db.py`, `scripts/seed_data.py` (`if __name__ == "__main__"`) | N/A | DB init / migrate / seed | Utility-only (ingestion infrastructure, not valuation/decision pipeline) | Explicit `__main__` blocks | Do not invoke Stage 3/5/7/8/9 decision path |
| Other entrypoints | `debug_alerts.py` | Hard-coded test-like inputs | Prints valuation alerts | Debug utility (imports missing valuation) | Top-level script using `ValuationEngine` | Not a production orchestrator; depends on missing valuation package |
| Complete E2E production path Stage 3/5/7/8/9 | — | — | — | **Not found** | Exhaustive search of all supplied `.py` for callers of the named symbols and for CLI/API/worker/orchestrator patterns yielded only tests + DB utilities | Entire valuation package missing; no main/CLI/API in supplied set |

**Conclusion for S7-T001:** Within the complete supplied production source set there is no verified production caller that (a) owns a Session, (b) obtains real upstream Stage 3/5/8 outputs, and (c) drives them through Stage 7 into Stage 9. Service boundaries and one internal call (decision → valuation) exist as definitions. The path is therefore **not found** as a real production execution path. Remaining uncertainty is limited to the missing valuation package body and any non-supplied deployment/config files outside the declared scope.

## S7-T002 Verdict

**Verdict: NOT FOUND IN SUPPLIED FILES** for persistence of `FinalDecisionResult` or `ValuationDecisionResult`.

### Evidence table (S7-T002)

| Output object | Persistence mechanism checked | Exact write site if present | Stored fields/identity if present | Conclusion | Limitation |
|---|---|---|---|---|---|
| `FinalDecisionResult` (decision/schema.py) | SQLAlchemy ORM models under models/, Base registration in init_db.py / migrations/runner.py | None | N/A | No ORM model or table for decision results | MappingDecision exists but is ingestion mapping, unrelated |
| `ValuationDecisionResult` (decision/service.py) | Same models + all session.add/commit sites | None | N/A | Returned only as in-memory dataclass | — |
| `DecisionEngine.make_decision` return | Trace through decision/service.py and all non-test callers | No write after return | N/A | Result leaves the service as return value only | Callers are tests only |
| `calculate_decision_as_of_jalali` return | Same | No write | N/A | No session.add of the result | Session is input parameter; never used for decision write in this service |
| Forecast persistence (contrast) | forecast/repo.py :: ForecastRecordRepository.save | `self.session.add(row)` + input-ref adds | ForecastVersion / ForecastInputRef | PRESENT for Stage 5 only | Shows the reusable pattern exists but is not applied to Stage 9 |
| Ingestion persistence (contrast) | ingestion/service.py, codal/pipeline, market/ingestion, common/run_tracker | Multiple session.add + commit | Reports, facts, runs, market rows | PRESENT for ingestion | Unrelated to decision |
| File / serialization writers for decision | Search of all supplied .py for dump/json/write of FinalDecisionResult | None | N/A | NOT FOUND | Bounded to supplied files |
| Migrations / model bootstrap | migrations/runner.py, scripts/init_db.py | Registers entity, period, report, normalized, market, forecast, etc.; no decision table | N/A | No decision persistence schema | — |

**Conclusion for S7-T002:** No concrete persistence path (database or other) for the Stage 9 decision result exists in the supplied source set. A clear contrast exists with Stage 5 forecast persistence and ingestion persistence. Architectural decision on whether persistence is required remains with the owner; this audit does not implement any model or repository.

## Second-pass verification

- Re-checked every call site of `generate_and_persist_forecast`, `analyze_market_as_of_jalali`, `calculate_decision_as_of_jalali`, `make_decision`, and `SessionLocal` via full-text search across all supplied `.py` files.
- Confirmed absence of non-test callers for the decision/valuation/market analysis path.
- Confirmed no `session.add` / repository save of `FinalDecisionResult` or `ValuationDecisionResult`.
- Confirmed `MappingDecision` is an ingestion mapping table, not Stage 9.
- Corrected any prior over-broad language that implied valuation source had been re-inspected in this delivery: the valuation package was not supplied and was not inspected.
- No contradiction found in the supplied files that would reverse the “no production caller” or “no Stage 9 persistence” findings.

## Earlier report corrections

Material over-broad or now-unverifiable claims from prior sections of `reply.md` (Prompt 1-A / 1-C style reports):

1. Prior claim that `src/valuation/service.py :: calculate_valuation_as_of_jalali` was inspected and that it “extracts daily price via select_market_price_as_of and hands it to ValuationEngine”.  
   **Corrected:** That file was not present in the three supplied archives for this prompt. Only the import and the call site inside `decision/service.py` were examined. Internal behavior of the valuation service is **UNVERIFIED** in this delivery.

2. Prior language treating service existence + internal decision→valuation call as “PARTIALLY VERIFIED” production path.  
   **Corrected:** Per current acceptance criteria, a production execution path requires an actual production caller and end-to-end supply of upstream outputs. None was found; verdict is therefore **NOT FOUND IN THE COMPLETE SUPPLIED SOURCE SET**.

3. Any implication that absence of a model proves the application “could never” persist decisions outside the repo.  
   **Corrected:** Conclusion is strictly “not found in the supplied source set”. External deployment, unpublished modules, or configuration outside the declared file list are not claimed.

## Acceptance criteria (PASS / NOT PASS)

### S7-T001
- Every supplied production Python file considered for callers/entrypoints → **PASS** (full search performed).
- Actual caller chain traced from source, not inferred → **PASS**.
- Test callers separated from production callers → **PASS**.
- Database session/transaction ownership evidenced or explicitly unverified → **PASS** (SessionLocal defined; no production pipeline ownership shown).
- Every claimed absence bounded to exact supplied source set → **PASS**.
- Report states whether real Stage 3/5/7/8/9 E2E production path is verified / partially verified / not found → **PASS** (not found).
- Remaining uncertainty identifies exact missing file → **PASS** (valuation package + any external entrypoint outside scope).

### S7-T002
- FinalDecisionResult / ValuationDecisionResult traced to every caller in supplied production source → **PASS**.
- All supplied ORM models, migrations, repositories checked → **PASS**.
- Distinguishes database vs other persistence → **PASS**.
- Any persistence claim supported by actual write call → **PASS** (none claimed).
- Absence bounded to supplied source set → **PASS**.
- Conclusion is one of PRESENT / PARTIAL / NOT FOUND IN SUPPLIED FILES / UNVERIFIED → **PASS** (NOT FOUND IN SUPPLIED FILES).

## Task status changes

| Task ID | Previous status | New status | Reason |
|---|---|---|---|
| S7-T001 | OPEN | DONE | Audit acceptance criteria satisfied. Implementation gap (no production caller / E2E path) is documented; the audit task itself is complete. |
| S7-T002 | OPEN | DONE | Audit acceptance criteria satisfied. Persistence is NOT FOUND IN SUPPLIED FILES; architectural gap left for owner decision. No model/repository created. |

(Unrelated tasks left unchanged.)

## Remaining blockers and exact owner decisions / files required

1. **Owner decision – production entrypoint (S7-T001 / S7-T009):** Whether a CLI, API, worker, or other orchestrator should own `SessionLocal`, assemble Stage 3/5/8 outputs, and invoke `calculate_decision_as_of_jalali`. No such component exists in the supplied set.
2. **Owner decision – Stage 9 persistence (S7-T002):** Whether `FinalDecisionResult` (or a subset) must be stored. If yes, a model + migration + write path are required; none exist today.
3. **Missing source for full Stage 7 re-audit:** The complete `src/valuation/` package must be supplied before any further claims about the body of `calculate_valuation_as_of_jalali`, parameter consumption, or PIT internals can be closed.
4. **temp_report2.md** was listed in the mandatory workflow set but was not among the supplied archives; any statements that depended exclusively on it remain un-rechecked.

Stage 7 remains OPEN; this prompt does not close it.

## Files modified

- `reply.md` (appended this final evidence-closure section only)
- `tasksToDo.md` (S7-T001 and S7-T002 status updated to DONE with reasons)

## Tests and commands

No tests or application/database commands were run by the agent.


---

# Prompt 1-C-B — Addendum: Valuation Package Now Supplied and Re-Verified

**Date of addendum:** 2026-10-29  
**Reason:** User supplied the previously missing files via `src4.zip` (`valuation/*`, `tests/test_stage8_market_service.py`, `temp_report2.md`).

## Files newly inspected

- valuation/__init__.py
- valuation/engine.py
- valuation/models.py
- valuation/parameters.py
- valuation/schema.py
- valuation/service.py
- tests/test_stage8_market_service.py
- temp_report2.md (historical evidence only; not treated as authoritative over current source)

## Re-verification of S7-T001 after valuation inspection

**Updated chain evidence for Stage 7:**

| Connection | Caller / call site | Upstream input | Downstream consumer | Caller classification | Evidence | Limitation |
|---|---|---|---|---|---|---|
| Stage 7 production function | Definition: `valuation/service.py` :: `calculate_valuation_as_of_jalali` | Session (caller-owned), company_id, period_id, CompanyForecastResult, as_of_jalali_date, **valuation_options | Calls `select_market_price_as_of` then `ValuationEngine().calculate_valuation`; returns `ValuationResult` with market_price_observation metadata | Service definition | Lines 18–70 of valuation/service.py; no commit/add | No production caller |
| Stage 7 → Stage 9 | `decision/service.py` lines 56–64 | Same Session + forecast + fundamentals + market | Feeds ValuationResult into `DecisionEngine.make_decision` | Service-to-service | Explicit call site | Still no outer production orchestrator |
| Stage 7 callers outside tests | None found after full re-search including valuation package | — | — | **Not found** | grep across all .py excluding tests shows only definition + export + the decision service call | — |

**S7-T001 final verdict remains unchanged:**  
**NOT FOUND IN THE COMPLETE SUPPLIED SOURCE SET** for a real end-to-end production execution path.  

The valuation service body is now verified: it is a pure boundary that reads a market price observation and delegates to `ValuationEngine`. It owns no transaction, persists nothing, and has no production caller. Combined with the absence of any CLI/API/worker that assembles Stage 3/5/8 outputs and drives `calculate_decision_as_of_jalali`, the E2E production path is still not present.

## Re-verification of S7-T002 after valuation inspection

- `valuation/service.py` contains zero `session.add`, `session.commit`, or repository writes.
- `valuation/engine.py`, `valuation/schema.py`, `valuation/models.py`, `valuation/parameters.py` contain no persistence of `ValuationResult` or decision objects.
- `FinalDecisionResult` / `ValuationDecisionResult` still have no write path anywhere in the now-complete supplied set.

**S7-T002 final verdict remains unchanged:**  
**NOT FOUND IN SUPPLIED FILES**.

## Corrections relative to the first pass of this prompt

- Previous “UNVERIFIED” notes that depended solely on the absence of the valuation package are resolved for the service definition and its immediate call to the engine.
- No claim that previously overstated a production path was restored; the stricter “not found” conclusion is retained and strengthened by the additional evidence.
- `temp_report2.md` was scanned for historical statements about callers/persistence; none reverse the source-based findings above.

## Task status

S7-T001 and S7-T002 remain **DONE** (audit criteria satisfied). The documented architecture gaps (missing production entrypoint; missing Stage 9 persistence) are owner decisions, not incomplete audit work.

## Files modified in this addendum step

- `reply.md` only (this addendum section).

## Tests and commands

No tests or application/database commands were run by the agent.


---

# Prompt 1-D — Stage 7 Evidence Audit and Documentation Alignment

**Prompt ID:** Prompt 1-D  
**Task IDs:** S7-T003, S7-T004, S7-T005, S7-T006  
**Work type:** AUDIT + DOCS ONLY  
**Code changes:** none  
**Test changes:** none  
**Test execution:** none (prohibited)

## Exact files actually inspected

### Workflow / prior evidence
WORKFLOW_RULES.md, tasksToDo.md, stepsForStage7.md, reply.md, temp_report2.md, PROJECT_HANDOFF_INSTRUCTIONS.md

### Specifications
05_Stage5_Forecast_Engine.md, 07_Stage7_Valuation.md, 08_Stage8_Market_Engine.md, 09_Stage9_Decision_Dashboard.md, 00_a_Master_Architecture.md

### Valuation package
valuation/__init__.py, valuation/engine.py, valuation/models.py, valuation/parameters.py, valuation/schema.py, valuation/service.py

### Forecast / scoring / market / decision / PIT
forecast/schema.py, forecast/service.py, forecast/repo.py, scoring/engine.py, market/engine.py, market/schema.py, market/parameters.py, market/service.py, ingestion/market/queries.py, core/point_in_time.py, core/jalali.py, core/database.py, decision/engine.py, decision/rules.py, decision/schema.py, decision/service.py

### Direct tests
tests/test_stage7_valuation.py, test_stage9_decision.py, test_stage789_service_interface.py, test_stage5_forecast.py, test_stage8_market.py, test_stage8_market_service.py, test_stage8_market_parameters.py, test_market_history_query.py

No listed required file was missing for this prompt after src4.zip.

---

## S7-T003 — D9 and versioned parameter consumption

### Verdict
**Mechanism implemented and evidenced; D9 remains UNRESOLVED as a policy/contract item** (no R8-dated parameter versions exist; historical selection fails closed).

### How parameters are represented and versioned
- Live module constants in `valuation/parameters.py` (SCENARIO_WEIGHTS, VALUATION_THRESHOLDS, CONFIDENCE_THRESHOLDS, RISK_THRESHOLDS, ALERT_THRESHOLDS, etc.).
- `ParameterRecord` / `ParameterSetVersion` / `ParameterRegistry` / `DEFAULT_REGISTRY` with a single genesis set: `GENESIS_VERSION_KEY = "STAGE7_V1/GENESIS"`, `effective_from=None` for every genesis record (`_UNVERSIONED_GENESIS_NOTE` states temporal validity is unknown and never valid for historical selection).
- Genesis is built programmatically from live constants so recorded values cannot drift from executed values (`_genesis_records`, `GENESIS_VERSION`).

### Selection when an as-of date is supplied
- `resolve_parameter_set_as_of(as_of, registry)` (parameters.py ~239–280): only versions with non-None `effective_from <= as_of` participate; newest wins; overlaps raise `LookupError`; undated genesis never participates; `as_of=None` raises.
- With only DEFAULT_REGISTRY (genesis only) this **always** raises `LookupError` naming missing R8-dated records.
- `select_parameter_set_for_valuation(parameter_registry, parameter_as_of)` (parameters.py ~451+):
  - Neither registry nor as-of → `FIXED_GENESIS_LEGACY`, `point_in_time_selection_applied=False`.
  - Dated path → `resolve_parameter_set_as_of`; missing version fails closed (no silent fallback to current constants).
- Engine (`ValuationEngine.calculate_valuation`, engine.py ~72–90, `_resolve_parameter_governing_timestamp` ~314–347): data_cutoff (from forecast or explicit) governs; conflicting `parameter_as_of` raises; no cutoff + caller as-of labelled `CALLER_SUPPLIED`; otherwise fails closed. No invention of valuation_date as as-of.

### What happens when no valid version can be selected
- Loud `LookupError` from `resolve_parameter_set_as_of` (message requires R8-dated records). Proven by implementation and tests:
  - `test_p33_as_of_without_dated_records_raises`
  - `test_p35_missing_or_ambiguous_as_of_selection_fails_closed`
  - `test_d9_missing_eligible_dated_version_fails_closed_without_genesis_fallback`

### Do selected values actually influence calculation?
**Yes.** `consume_parameter_set` freezes a `ConsumedParameters` object; the engine reads **only** from it for registry-governed values (scenario weights, valuation/confidence/risk/alert thresholds, min_industry_peers, sensitivity_perturbation, probability blend/families, scenario multiple bounds, model/contract version). Metadata snapshot is produced from the same `values` mapping (`ConsumedParameters.snapshot`), so recorded and consumed cannot disagree.

Evidence of real consumption (not metadata-only):
- engine.py uses `params.valuation_thresholds`, `params.alert_thresholds`, `params.scenario_weights`, `params.min_industry_peers`, etc. in status, alerts, probabilities, peer checks.
- Tests: `test_p35_as_of_selection_governs_calculation_and_snapshot_matches`, `test_p35_selected_set_governs_peers_alerts_and_scenario_weights`, `test_p10_expensive_threshold_consumed_from_parameters`, `test_p35_legacy_path_provenance_is_truthful_and_unchanged` (33 consumed names, 5 recorded-not-consumed including dead `ALERT_THRESHOLDS.high_dependence_share` and empty `INDUSTRY_TARGET_PE`).

### Metadata / model-version / effective-date correspondence
- Legacy path metadata: `mode=FIXED_GENESIS_LEGACY`, `point_in_time_selection_applied=False`, version_key genesis, effective_from=None — truthful; does not claim PIT.
- Dated path: `point_in_time_selection_applied=True`, `as_of_source` in {EFFECTIVE_DATA_CUTOFF, CALLER_SUPPLIED}, snapshot matches selected set.
- Tests: `test_d9_metadata_distinguishes_dated_selection_from_legacy_genesis`, `test_d9_effective_cutoff_governs_selection_not_valuation_date`, `test_d9_exact_effective_from_boundary_is_accepted`, `test_d9_future_effective_version_is_rejected`, `test_d9_conflicting_parameter_as_of_is_rejected`.

### Test coverage of real selection + consumption + missing historical version
Covered by the p33 / p35 / d9 tests listed above. Synthetic registries exercise dated selection mechanics without inventing production R8 dates.

### What remains for the owner (D9 policy)
- No R8-dated parameter versions exist in DEFAULT_REGISTRY. Inventing `effective_from` dates is forbidden.
- D9 is **not** resolved merely because a version identifier and selection mechanism exist. Historical backtests require owner-approved dated records (or an explicit approved contract that undated genesis is never used for history — already the code behaviour).

**Acceptance criterion:** PASS (path, consumption, fail-closed behaviour, and tests reported with evidence). D9 policy remains open for owner.

---

## S7-T004 — PIT, provenance, and input contracts

### Verdict
**PARTIAL.** Market-price Jalali as-of selection and forecast cutoff/parameter governance are evidenced. Benchmark PE series and full publication-time evidence for several inputs remain caller-supplied without temporal provenance inside Stage 7.

### Input-by-input evidence matrix

| Input | Identity | Observation / report date | Availability / publication time | As-of filtering rule | Provenance link | Behaviour when temporal evidence absent | Status |
|---|---|---|---|---|---|---|---|
| Stage 5 forecast (`CompanyForecastResult`) | company_id, forecast_period_id, industry_code, scenario EPS chains | `data_cutoff_datetime` on result | Optional `ForecastInputRef.available_at` when refs supplied | Engine defaults cutoff from forecast; `_reject_unverifiable_forecast_refs` blocks undated or post-cutoff refs | `ForecastInputRef` sequence optional on engine call | Raises if refs present but undated/post-cutoff; no refs → no extra PIT claim | Proven for cutoff identity; full publication chain depends on upstream Stage 5 refs being supplied |
| Market price (valuation) | company_id, market_data_id, price, price_basis | `source_jalali_date` on `MarketPriceObservation` | **Not stored** on MarketDaily rows in supplied models | `select_market_price_as_of`: latest valid positive price on or before Jalali as-of; duplicate same-date raises | Metadata `market_price_observation` written by valuation/service.py | `MarketPriceUnavailableError` if none | Observation date + as-of filter proven; publication/availability time **not** in supplied market schema |
| Historical PE benchmark | Caller-supplied sequence `historical_pe_values` | None in Stage 7 | None | Non-finite filtered; empty → insufficient benchmark path | None inside Stage 7 | Continues with reduced evidence; alert `CRITICAL:INSUFFICIENT_BENCHMARK_DATA` when peer count low | **Gap:** no timestamps/provenance on benchmark series |
| Industry forward / TTM PE | Caller-supplied `industry_forward_pe_values`, `industry_ttm_pe_values` | None | None | Same filtering; peer minimum from params | None | Same | **Gap:** caller must supply; no repository-backed PIT series in supplied code |
| Stage 8 market signals | `MarketSignalResult` from `analyze_market_as_of_jalali` | as_of_date (Jalali) on result; history rows have jalali_date | Not on MarketDaily | `select_market_history_as_of` then engine | service maps observation fields | Empty history → engine INSUFFICIENT_DATA | As-of filter proven; publication time absent |
| Parameter set (D9) | version_key, effective_from | effective_from on dated versions | N/A | resolve_parameter_set_as_of | selection metadata | LookupError | Proven fail-closed |
| Report versions (Stage 1 path) | ReportVersion | publication_datetime | publication_datetime ≤ cutoff | `core/point_in_time.py::select_report_version` | Direct | Returns None | Proven for report path; not wired into valuation engine call in supplied production path |

### Key limitations (explicit)
1. **Cutoff alone is not full PIT** — policy in stepsForStage7.md §2; code does not claim otherwise for benchmarks.
2. Market daily rows lack a publication/availability timestamp; Jalali calendar date of the bar is the only temporal field.
3. Benchmark PE series are pure caller inputs with no Stage 7-side temporal contract.
4. Production caller that would assemble these inputs under a single as-of is still absent (S7-T001).

**Acceptance criterion:** PASS (matrix with contracts, evidence, gaps, and required owner/file decisions).

---

## S7-T005 — Alert and decision contracts D1–D8

### Per-decision status

| ID | Approved policy (stepsForStage7.md) | Current implementation | Direct tests | Consumer evidence | Status |
|---|---|---|---|---|---|
| **D1** ASSESSMENT_FLIP_RISK | No new alert without valid criterion for assumption/status change | Not produced by `_alerts` (engine.py ~639–675). No symbol emits this name. | `test_v1_defers_undefined_flip_dependence_and_assumption_alerts`, `test_p3_flip_dependence_alerts_remain_explicitly_unresolved` assert name absent from alerts and valuation_risk_flags | Decision engine does not read this alert name | **Intentionally deferred** — matches policy |
| **D2** HIGH_MULTIPLE_DEPENDENCE | Current dependence criterion not approved; keep disabled | `ALERT_THRESHOLDS.high_dependence_share = 0.60` recorded in genesis but listed in `recorded_not_consumed_names`; **not read** by `_alerts` or formulas. Comment in parameters.py: "Declared but unwired dead definition; must not be activated without D2" | Same deferral tests | None | **Intentionally deferred** |
| **D3** HIGH_EPS_DEPENDENCE | No new alert without valid criterion; preserve Stage 5 EPS | Not emitted. EPS taken from Stage 5 forecast chains only (`test_v1_uses_stage5_eps_without_recalculating_from_net_profit`) | Deferral tests + EPS preservation tests | None for this alert | **Intentionally deferred**; EPS contract preserved |
| **D4** MARGIN_ASSUMPTION_RISK | Outside V1 until valid dated input exists | Not emitted | Deferral tests | None | **Intentionally deferred** |
| **D5** HIGH_IMPACT_HIGH_UNCERTAINTY | Preserve `review_priority`; no extra alert without independent criterion | `review_priority` computed and returned on `ValuationResult`; no additional alert of this name | Deferral tests; driver analysis path present | Decision uses valuation status/risk/confidence, not this alert name | **Intentionally deferred** for alert; review_priority preserved |
| **D6** Industry-specific models | Keep EPS + TARGET_PE drivers; do not invent industry formulas | `INDUSTRY_TARGET_PE = {}` unused; fair value from Stage 5 EPS × target PE hierarchy; NAV accepted as optional input only | `test_v1_sector_examples_use_only_eps_and_target_pe_drivers` | N/A | **Implemented as V1 policy** — no invented industry chains |
| **D7** PIT | Examine temporal evidence per input; cutoff alone insufficient | See S7-T004 matrix. Parameter selection fail-closed; market price Jalali as-of; forecast ref rejection; benchmarks lack timestamps | d9/p33/p35 tests; market query tests | N/A | **Partially evidenced**; remaining gaps explicit (benchmarks, market publication time) |
| **D8** Alert contract | Verify real names, producers, consumers before treating as operational | **Produced names** (engine `_alerts`): `WARNING:HIGH_SCENARIO_DISPERSION`, `WARNING:LOW_FORECAST_RELIABILITY`, `CRITICAL:INSUFFICIENT_BENCHMARK_DATA`, `WATCH:VALUATION_ABOVE_TARGET_PE`, `WATCH:VALUATION_BELOW_TARGET_PE`, `WATCH:FORWARD_PE_ABOVE_HISTORICAL`, `WATCH:FORWARD_PE_BELOW_HISTORICAL`, `WATCH:FORWARD_PE_ABOVE_INDUSTRY`, `WATCH:FORWARD_PE_BELOW_INDUSTRY`, `INFO:TOP_DRIVER:...`. Stored on `ValuationResult.alerts` and folded into `valuation_risk_flags`. | Stage 7 tests exercise dispersion/reliability/benchmark paths | `decision/engine.py` consumes `valuation_status`, `valuation_risk_level`, `valuation_confidence`, expected upside — **not** the individual alert strings. No other consumer of alert strings found in supplied decision path | **Operational for valuation output schema**; limited downstream consumption (risk/status fields, not alert name list) |

No genuine discrepancy that would reclassify a deferred D1–D5 item as a defect requiring implementation. Deferred remains deferred.

**Acceptance criterion:** PASS.

---

## S7-T006 — Documentation alignment

### Changes made
1. **reply.md** — this Prompt 1-D report appended (historical sections retained; corrections only where current evidence requires).
2. **stepsForStage7.md** — status notes for D9/PIT/alerts and package-1 audit completion updated to match T001–T005 evidence; Stage 7 remains OPEN; four-package order preserved; no completion claim.
3. **tasksToDo.md** — S7-T003, S7-T004, S7-T005, S7-T006 marked DONE with audit results; other tasks unchanged.

### Corrections to earlier statements
- Prior language that could be read as “D9 resolved because a version key exists” is corrected: mechanism exists; policy/R8-dated records do not; D9 remains open for owner.
- Prior implication that benchmark PE series carry PIT evidence inside Stage 7 is corrected: they are caller-supplied sequences without timestamps in the supplied contract.
- Deferred alerts D1–D5 remain deferred; not reported as missing bugs.

### Acceptance criterion
PASS for documentation alignment to the completed audits.

---

## Acceptance criteria summary

| Task | Outcome |
|---|---|
| S7-T003 | **PASS** (audit complete; D9 policy still owner-blocked) |
| S7-T004 | **PASS** (matrix delivered; residual PIT gaps explicit) |
| S7-T005 | **PASS** (every D1–D8 status evidence-backed) |
| S7-T006 | **PASS** (docs aligned to evidence only) |

## Owner decisions / contracts still required

1. **R8 / D9:** Approve and register dated parameter versions (`effective_from` + values) if historical parameter selection is a product requirement; or formally accept that only the legacy undated genesis path is used for current runs.
2. **Benchmark PIT:** Decide whether historical/industry PE series must carry observation dates and availability timestamps, and who supplies them.
3. **Market publication time:** Decide whether MarketDaily needs an availability/publication field for stricter PIT (currently only Jalali bar date exists).
4. **Production entrypoint** (from S7-T001): still required before E2E path can be claimed.
5. **Stage 9 persistence** (from S7-T002): still an owner product decision.

## Files changed
- reply.md (this report)
- stepsForStage7.md (roadmap status alignment only)
- tasksToDo.md (T003–T006 status → DONE)

## Tests and commands
No tests, application code, database commands, or Git commands were run by the agent. No production or test code was modified.

## Recommended next Task IDs
- **S7-T009** (owner decision on real integrated path) once production-entrypoint intent is clear.
- **S7-T007** remains BLOCKED until owner supplies R8-dated parameter policy (or explicit acceptance of legacy-only).
- Do **not** advance to S7-T011 (final engine review) until package-2/3 blockers above are resolved.

**Stage 7 remains OPEN.**
