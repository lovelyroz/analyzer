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
# گزارش اصلاح‌شده ممیزی شواهدمحور **Stage 7 Prompt 1 — Audit Corrections Only** بر اساس الزامات قیدشده در فایل `PROMPT.md` آماده شده است. در این اصلاحیه، تمام ادعاهای ممیزی قبلی با سورس‌کدها، اسناد مشخصات و تست‌های واقعی تطبیق داده شده و موارد نادرست اصلاح گردیده‌اند.

---

### ۱. ماتریس شکاف‌های اصلاح‌شده (Corrected Gap Matrix)

| عنوان موضوع / ادعای قبلی | شواهد دقیق سورس‌کد و تست‌ها | وضعیت واقعی و سطح اطمینان | اقدام اصلاحی / توصیه |
| :--- | :--- | :--- | :--- |
| **استخراج تاریخچه بازار Stage 8** | `src/ingestion/market/queries.py::select_market_history_as_of`<br>`src/market/service.py::analyze_market_as_of_jalali`<br>`src/tests/test_stage8_market_service.py` | **ALREADY IMPLEMENTED (پیاده‌سازی‌شده و موجود)**<br>ادعای مفقود بودن کوئری تاریخچه بازار نادرست بود. تابع کوئری `select_market_history_as_of` و سرویس آداپتور `analyze_market_as_of_jalali` کاملاً پیاده‌سازی و تست شده‌اند. | **عدم پیاده‌سازی مجدد**. این قابلیت موجود است؛ صرفاً فراخواننده ارکستریتور در نقطه ورود اصلی برنامه وجود ندارد. |
| **حاکمیت پارامترها و انتخاب تاریخی (D9 / P54)** | `src/valuation/parameters.py:resolve_parameter_set_as_of`<br>`src/valuation/service.py:calculate_valuation_as_of_jalali`<br>`src/valuation/engine.py:_resolve_parameter_governing_timestamp` | **UNRESOLVED OWNER POLICY (سیاست معوق مالک)**<br>پیشنهاد قبلی مبنی بر ثبت تاریخ فرضی `2026-01-01` **فاقد پشتیبانی مشخصات (UNSUPPORTED)** است. رفتار Fail-Closed سیستم با صدور `LookupError` هنگام درخواست تاریخ‌دار روی ثبت‌کننده Genesis کاملاً درست و قفل‌شده است. | **عدم حدس زدن تاریخ اعتبار فرضی**. تاریخ اعتبار و مقادیر پارامترها باید رسماً توسط مالک پروژه تصویب شوند. |
| **نقطه ورود اصلی برنامه (Main Entrypoint)** | بررسی کل سورس‌کد در `src/` | **CONFIRMED ABSENCE (عدم وجود قطعی)**<br>هیچ اسکریپت CLI، سرویس API یا حلقه ارکستراسیون اصلی در کد وجود ندارد که Session دیتابیس را مدیریت کرده و لوله‌ها را اجرا کند. | طراحی و پیاده‌سازی مرز نقطه ورود اصلی در فازهای بعدی. |
| **فراخواننده‌های تولیدی Stage 3 و Stage 5** | `src/scoring/engine.py:calculate_score`<br>`src/forecast/service.py:generate_and_persist_forecast` | **CONFIRMED ABSENCE OF PRODUCTION CALLER**<br>موتورها و سرویس‌ها وجود دارند اما فراخواننده‌ای در مسیر اجرایی برنامه برای ارسال خروجی‌های آن‌ها به Stage 7 و Stage 9 وجود ندارد. | اتصال فراخواننده‌ها در نقطه ورود اصلی برنامه. |
| **لایه ماندگاری تصمیمات Stage 9** | `src/decision/schema.py:FinalDecisionResult`<br>`src/core/database.py` | **CONFIRMED MISSING PERSISTENCE MODEL**<br>هیچ مدل دیتابیس (SQLAlchemy Table) یا ریپازیتوری برای ذخیره `FinalDecisionResult` در SQLite وجود ندارد. | ایجاد مدل ماندگاری دیتابیس برای Stage 9 در Scope مربوط به Prompt 2. |

---

### ۲. فایل‌های تغییریافته و دلیل تغییرات (Files Actually Modified)

مطابق با قیود **AUDIT ONLY + LIMITED DOCS ONLY**، هیچ‌یک از کدهای سورس (`src/`) یا تست‌ها تغییر نکرده و تستی اجرا نشده است. اصلاحات مستنداتی شامل موارد زیر است:

1. **فایل `/workspace/out/WORKFLOW_RULES.md`**:
   - **دلیل تغییر**: شفاف‌سازی قوانین پروژه، به ویژه ممنوعیت حدس زدن تاریخ‌های فرضی (مانند `2026-01-01`)، تاکید بر عدم پیاده‌سازی مجدد توابع موجود (نظیر `select_market_history_as_of`) و الزام به لزوم تطبیق کدهای موجود پیش از ادعای کمبود.
2. **فایل `/workspace/out/stepsForStage7.md`**:
   - **دلیل تغییر**: تصحیح وضعیت Stage 8 (ثبت موجود بودن کوئری و سرویس تاریخچه بازار)، اصلاح وضعیت D9 (حفظ رفتار Fail-Closed و منع ساخت تاریخ فرضی)، و بروزرسانی محدوده پیشنهادی برای Prompt 2.

---

### ۳. تصمیمات سیاستی حل‌نشده و شواهد مفقود (Unresolved Policy Decisions)

* **تصویب و تاریخ اعتبار پارامترها (D9)**: ثبت‌کننده `DEFAULT_REGISTRY` فقط شامل رکورد Genesis با `effective_from = None` است. تعیین تاریخ اعتبار رسمی یا تصویب مقادیر عددی ۳۸ پارامتر نیازمند مصوبه مستقیم مالک سیستم است. ایجاد تاریخ فرضی بر خلاف اصول مالی و فنی پروژه است.
* **هشدارهای ۵ گانه تعویق‌افتاده (D1–D5)**: به دلیل عدم وجود فرمول مالی مصوب در اسناد مشخصات، هشدارهای `ASSESSMENT_FLIP_RISK` و ۴ هشدار دیگر در حالت تعویق (Deferred) باقی می‌مانند تا از ساخت فرمول‌های غیرمصوب جلوگیری شود.
* **درایورهای اختصاصی صنعت (D6)**: تحلیل درایورها بر اساس همان الگوی دوعاملی قفل‌شده `{EPS, TARGET_PE}` باقی می‌ماند و فرمول‌های ساختگی برای NII بانک یا NAV هولدینگ ایجاد نخواهد شد.

---

### ۴. محدوده اصلاح‌شده برای Prompt 2 (Revised Prompt 2 Scope)

محدوده Prompt 2 صرفاً بر اساس **یافته‌های قطعی و تاییدشده** تنظیم شده و تمامی موارد نادرست (مانند پیاده‌سازی مجدد کوئری بازار یا فرض تاریخ `2026-01-01`) از آن حذف گردیده‌اند:

1. **پیاده‌سازی لایه ماندگاری Stage 9 (Persistence Layer)**:
   * **فایل‌های هدف**: `src/decision/models.py` (جدید) یا `src/decision/schema.py` و `src/core/database.py`.
   * **تغییرات**: ایجاد مدل SQLAlchemy و ریپازیتوری ذخیره‌سازی برای `FinalDecisionResult` جهت امکان ثبت تصمیمات نهایی در دیتابیس SQLite.
   * **تست‌ها**: تست‌های واحد ذخیره و بازیابی تصمیمات Stage 9.

2. **طراحی مرز نقطه ورود تولیدی (Production Orchestrator Boundary)**:
   * **فایل‌های هدف**: ایجاد نقطه ورود / ارکستریتور اصلی پروژه.
   * **تغییرات**: فراخوانی یکپارچه و مستقیم سرویس‌های موجود (`src/forecast/service.py` ، `src/market/service.py` و `src/decision/service.py`) و مدیریت Session دیتابیس بدون دستکاری کد داخلی Stage 7.

3. **تست‌های رگرسیون مورد نیاز**:
   ```bash
   python -m pytest src/tests/test_stage7_valuation.py src/tests/test_stage9_decision.py src/tests/test_stage8_market_service.py -q
   ```

---

💡 **پیشنهاد گام بعدی**: در صورت تایید این گزارش ممیزی اصلاح‌شده، می‌توانیم آماده‌سازی الزامات ساختاری Prompt 2 (ایجاد مدل دیتابیس Stage 9 و ارکستریتور اصلی) را آغاز کنیم.