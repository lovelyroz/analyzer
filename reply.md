گزارش ممیزی شواهدمحور **Stage 7 — Prompt 1** مطابق با الزامات و قیود تعیین‌شده در فایل `PROMPT.md` تنظیم شده است. در این ممیزی، هیچ کدی تغییر نکرده، تستی اجرا نگردیده و دستوری در ترمینال یا گیت صادر نشده است.

---

### ۱. فایل‌های بررسی‌شده (Files Inspected)

**الف) نقشه راه و مشخصات (Roadmap & Specifications):**
* `stepsForStage7.md` (برنامه اجرایی و وضعیت D7/D9)
* `07_Stage7_Valuation.md` (سند مشخصات قفل‌شده Stage 7 V1)
* `05_Stage5_Forecast_Engine.md` (مشخصات مرزی Stage 5)
* `temp_report2.md` (گزارش‌های ممیزی فنی سابقه)
* `reply.md` (گزارش‌های ممیزی P63، P64، P65 و زنجیره‌های اجرا)

**ب) کدهای سورس و تست‌های Stage 7:**
* `src/valuation/engine.py` (موتور ارزش‌گذاری)
* `src/valuation/service.py` (مرز سرویس ارزش‌گذاری جلالی)
* `src/valuation/parameters.py` (پارامترها و ثبت‌کننده نسخه)
* `src/valuation/schema.py` (اسکیماهای خروجی و داده)
* `src/valuation/models.py` (مدل‌ها و توابع محاسباتی Forward P/E)
* `src/tests/test_stage7_valuation.py` (تست‌های واحد و مرزی Stage 7)

**ج) کدهای سورس Stage 5 و Stage 3:**
* `src/forecast/service.py` & `src/forecast/schema.py` (سرویس و اسکیمای پیش‌بینی)
* `src/scoring/engine.py` (موتور امتیازدهی بنیادی)

**د) کدهای سورس Stage 8 و داده‌های بازار:**
* `src/market/engine.py` (موتور حالت بازار)
* `src/market/service.py` (سرویس تحلیل بازار جلالی)
* `src/ingestion/market/queries.py` (کوئری‌های استخراج قیمت و تاریخچه بازار)
* `src/tests/test_stage8_market.py`
* `src/tests/test_stage8_market_service.py`
* `src/tests/test_stage8_market_parameters.py`

**هـ) کدهای سورس Stage 9 و مرز پایگاه داده:**
* `src/decision/service.py` (سرویس ارکستراسیون تصمیم‌گیری جلالی)
* `src/decision/engine.py` (موتور تلفیق شواهد و تصمیم‌گیری)
* `src/core/database.py` (مدیریت تراکنش پایگاه داده)
* `src/tests/test_stage9_decision.py`

**و) فایل‌های تکمیلی بررسی‌شده (Conditional Files):**
* `PROMPT.md` (جهت دریافت دستورالعمل دقیق اجرای Prompt 1)
* `src/core/jalali.py` (جهت اعتبارسنجی نحوه مدیریت تاریخ جلالی در دیتابیس)
* `src/market/schema.py` (جهت اعتبارسنجی ساختار `MarketSignalResult`)

---

### ۲. ماتریس شکاف‌ها (Gap Matrix)

| عنوان مسأله / شکاف | شواهد (فایل / تابع / تست) | وضعیت و سطح اطمینان | اقدام بعدی پیشنهادی |
| :--- | :--- | :--- | :--- |
| **عدم وجود نسخه پارامتر تاریخ‌دار معتبر (D9 / P54)** | `src/valuation/parameters.py:260-269`<br>`src/valuation/service.py:12` | **Confirmed Defect / Open Policy Gap**<br>ثبت‌کننده پیش‌فرض فقط شامل رکورد Genesis با `effective_from = None` است. فراخوانی‌های دارای `parameter_as_of` با `LookupError` متوقف می‌شوند. | تصویب رسمی ۳۸ پارامتر و تعیین تاریخ اعتبار (مانند `2026-01-01`) توسط مالک پروژه و ثبت نسخه تاریخ‌دار جدید در `DEFAULT_REGISTRY`. |
| **محدودیت عدم اعتبارسنجی PIT بنچمارک‌ها (D7)** | `07_Stage7_Valuation.md` (بخش ۸۵)<br>`src/valuation/engine.py` | **Confirmed Limitation / Unresolved Contract**<br>سری‌های بنچمارک به صورت float بدون تاریخ وارد می‌شوند و مقایسه‌ای بین `valuation_date` و `cutoff` صورت نمی‌گیرد. | پذیرش مستند محدودیت V1 یا تعیین ساختار تاریخ‌دار برای سری‌های بنچمارک توسط مالک پروژه. |
| **عدم پیاده‌سازی کوئری استخراج سری زمانی بازار Stage 8** | `src/ingestion/market/queries.py`<br>`src/market/service.py:12` | **Confirmed Missing Implementation**<br>کوئری استخراج سری چندروزه OHLCV بر اساس تقویم جلالی وجود ندارد؛ مسئولیت ارسال `MarketSignalResult` بر عهده فراخواننده است. | پیاده‌سازی کوئری استخراج سری زمانی بازار جلالی در `src/ingestion/market/queries.py`. |
| **تعویق هشدارهای ۵ گانه (D1–D5)** | `src/valuation/engine.py`<br>`src/tests/test_stage7_valuation.py` | **Deferred Capability**<br>هشدارهای `ASSESSMENT_FLIP_RISK` و ۴ هشدار دیگر به دلیل نبود فرمول مصوب مالی صادر نمی‌شوند. | عدم پیاده‌سازی فرمول‌های ساختگی؛ حفظ الگوهای تعویق‌یافته تا زمان تصویب مشخصات. |
| **عدم تفکیک درایورهای اختصاصی صنعت (D6)** | `src/valuation/engine.py:250`<br>`07_Stage7_Valuation.md` (بخش ۴۷) | **Deferred Capability**<br>تحلیل درایورها برای همه صنایع به صورت یکسان به `{EPS, TARGET_PE}` محدود است و زنجیره‌های NII و NAV پیاده‌سازی نشده‌اند. | حفظ الگوی دوعاملی فعلی و عدم ایجاد ضریب‌های مستقیم صنعتی غیرمصوب. |
| **فقدان نقطه ورود اصلی و فراخواننده‌های تولیدی (Main Entrypoint)** | `src/decision/service.py`<br>`src/scoring/engine.py`<br>`src/forecast/service.py` | **Confirmed Missing Callers**<br>هیچ CLI/API یا فراخواننده عملیاتی که زنجیره Stage 1 → 3 → 5 → 7 → 8 → 9 را به صورت سرتاسری اجرا کند وجود ندارد. | طراحی نقطه ورود اصلی برنامه و مدیریت متمرکز جلسه دیتابیس در فازهای بعدی. |
| **فقدان مدل ذخیره‌سازی تصمیمات Stage 9** | `src/decision/schema.py`<br>`src/core/database.py` | **Confirmed Missing Persistence Model**<br>هیچ مدل دیتابیس برای نگهداری و ذخیره‌سازی خروجی `FinalDecisionResult` در پایگاه داده پیاده‌سازی نشده است. | ایجاد Table/Model اختصاصی در SQLAlchemy برای ذخیره‌سازی تصمیمات Stage 9. |

---

### ۳. زنجیره اجرای اعتبارسنجی‌شده (Verified Execution Path)

#### ۱) اتصالات و لینک‌های تاییدشده (Confirmed Connected Links):
* **Stage 7 Valuation → Stage 9 Decision Boundary**:
  تابع `calculate_decision_as_of_jalali` در فایل `src/decision/service.py` خروجی ارزش‌گذاری جلالی (`calculate_valuation_as_of_jalali`) را به همراه شواهد بنیادی (`FundamentalScoreResult`) و سیگنال بازار (`MarketSignalResult`) دریافت کرده و مستقیماً به `DecisionEngine.make_decision` ارسال می‌کند. هر دو خروجی در قالب `ValuationDecisionResult` تحویل داده می‌شوند.
* **Database Market Daily → Stage 7 Valuation Service**:
  تابع `calculate_valuation_as_of_jalali` در `src/valuation/service.py` قیمت روز بازار را از طریق `select_market_price_as_of` و جدول `MarketDaily` بر اساس تقویم جلالی استخراج کرده و به موتور ارزش‌گذاری تحویل می‌دهد.
* **Database Market History → Stage 8 Market Engine Service**:
  تابع `analyze_market_as_of_jalali` در `src/market/service.py` مشاهدات تاریخچه بازار را از دیتابیس استخراج و سطر به سطر نگاشت کرده و به `MarketEngine.analyze_market` تحویل می‌دهد.
* **Stage 5 Forecast EPS → Stage 7 Valuation Engine**:
  موتور ارزش‌گذاری پیش‌بینی EPS سناریوها را مستقیماً از `CompanyForecastResult` دریافت کرده و بدون محاسبه مجدد سود خالص، فرمول ارزش منصفانه را محاسبه می‌کند.

#### ۲) اتصالات مفقود یا تاییدنشده (Missing or Unverified Links):
* **عدم وجود نقطه ورود اصلی (Main Entrypoint / CLI / API)**: هیچ نقطه ورودی در پروژه برای اجرای سرتاسری لوله‌ها وجود ندارد.
* **فقدان فراخواننده تولیدی Stage 3 Scoring**: سرویسی که KPIهای مالی Stage 1 را استخراج کرده و به `FundamentalScoreResult` تبدیل و به Stage 9 ارسال کند در کد موجود نیست.
* **فقدان فراخواننده تولیدی Stage 5 Forecast**: سرویس `generate_and_persist_forecast` خروجی را در دیتابیس ذخیره می‌کند اما فراخواننده متصل به Stage 7 در خط لوله اصلی وجود ندارد.
* **فقدان لایه ماندگاری Stage 9**: هیچ مدل SQLAlchemy برای ذخیره‌سازی خروجی نهایی تصمیم در پایگاه داده ایجاد نشده است.

---

### ۴. محدوده پیاده‌سازی Prompt 2 (Prompt 2 Implementation Scope)

**توجه**: بر اساس قیود Prompt 1، هیچ تغییری در کد تولیدی یا تست‌ها نباید در این مرحله انجام شود. محدوده پیشنهادی برای گام بعدی (Prompt 2) عبارت است از:

1. **فایل‌های هدف (Target Files):**
   * `src/valuation/parameters.py`: ثبت نسخه پارامتر تاریخ‌دار جدید (مانند `STAGE7_V1/INITIAL_2026`) با `effective_from = datetime(2026, 1, 1, tzinfo=timezone.utc)` پس از اخذ مصوبه رسمی D9 از مالک پروژه.
   * `src/ingestion/market/queries.py` یا `src/market/service.py`: پیاده‌سازی کوئری استخراج سری زمانی روزانه بازار برای پوشش کامل ورودی‌های Stage 8.
   * `stepsForStage7.md`: بروزرسانی وضعیت D9 به RESOLVED پس از اعمال مصوبه.

2. **تغییرات مورد نظر (Intended Changes):**
   * رفع مسأله P54 با فراهم کردن امکان فراخوانی تاریخ‌دار بدون بروز `LookupError`.
   * پرهیز از ساخت فرمول‌های غیرمصوب برای هشدارهای تعویق‌شده D1–D5 و درایورهای صنعتی D6.
   * عدم دستکاری یا بازطراحی منطق داخلی `src/valuation/engine.py` تا گام بسته نهایی Stage 7.

3. **تست‌های رگرسیون مورد نیاز (Required Regression Tests):**
   * تمامی تست‌های زیر باید بدون خطا پاس شوند:
     * `python -m pytest src/tests/test_stage7_valuation.py -q` (۷۵ تست)
     * `python -m pytest src/tests/test_stage9_decision.py -q` (۱۹ تست)
     * `python -m pytest src/tests/test_stage8_market.py src/tests/test_stage8_market_service.py src/tests/test_stage8_market_parameters.py -q`
     * `python -m pytest src/tests/test_stage5_forecast.py -q`
     * `python -m pytest src/tests/test_stage3_scoring.py -q`

---

### ۵. تغییرات مستندات (Documentation Changes)

1. **فایل `WORKFLOW_RULES.md`**:
   * **اقدام**: بر اساس قید Prompt 1، فایل `WORKFLOW_RULES.md` در `/workspace/scratch/WORKFLOW_RULES.md` ایجاد و به `/workspace/out/WORKFLOW_RULES.md` منتقل شد.
   * **دلیل**: تدوین قوانین باثبات و پایدار پروژه شامل عدم تغییر کد در فاز ممیزی، حفظ انواریانت‌های مالی و تقویم جلالی، سیاست‌های Fail-Closed در حاکمیت پارامترها (D9)، تفکیک مسئولیت‌های Stage 7 و Stage 9، و ممنوعیت ساخت داده‌ها یا تاریخ‌های فرضی.

2. **فایل `stepsForStage7.md`**:
   * **اقدام**: برنامه اجرایی Stage 7 در `/workspace/scratch/stepsForStage7.md` بروزرسانی شده و به `/workspace/out/stepsForStage7.md` منتقل گردید.
   * **دلیل**: انعکاس شفاف نتایج ممیزی Prompt 1، ثبت وضعیت‌های D1–D9، و مشخص کردن اتصالات واقعی و حلقه‌های مفقود خط لوله بدون علامت‌گذاری Stage 7 به عنوان نهایی یا تکمیل‌شده.

3. **سایر فایل‌ها**:
   * فایل‌های `temp_report2.md`، `reply.md`، اسناد مشخصات فنی، سورسکد برنامه‌ها و تست‌ها طبق دستورالعمل کاملاً دست‌نخورده باقی ماندند.

---

### ۶. دستورات اجرایی برای کاربر (Commands for me to run later)

جهت اعتبارسنجی کامل مجموعه تست‌های پروژه، دستورهای زیر را می‌توانید بعداً در محیط توسعه خود اجرا کنید (**ایجنت این دستورها را اجرا نکرده است**):

```bash
# ۱. اجرای تست‌های یکپارچه‌سازی و مرزی Stage 7 Valuation
python -m pytest src/tests/test_stage7_valuation.py -q

# ۲. اجرای تست‌های ارکستراسیون و تصمیم‌گیری Stage 9 Decision
python -m pytest src/tests/test_stage9_decision.py -q

# ۳. اجرای تست‌های آداپتور و سرویس داده‌های بازار Stage 8
python -m pytest src/tests/test_stage8_market.py src/tests/test_stage8_market_service.py src/tests/test_stage8_market_parameters.py -q

# ۴. اجرای یکجای تمامی تست‌های خط لوله پنج‌گانه جهت اطمینان از عدم رگرسیون
python -m pytest src/tests/test_stage3_scoring.py src/tests/test_stage5_forecast.py src/tests/test_stage7_valuation.py src/tests/test_stage8_market.py src/tests/test_stage9_decision.py -q
```

---
