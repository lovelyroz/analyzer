### ۱. جمع‌بندی اجرایی (Executive Conclusion)

گزارش حاضر، خروجی تحلیلی اجرای پرامپت **P62 — تعیین کمینه‌ترین قرارداد یکپارچه‌سازی تولید برای Stage 7** است. بر اساس ممیزی P48 و تحلیل کد‌های موجود در پروژه `analyzer`، اتصال داخلی بین **Stage 5 ← Stage 7 ← Stage 9** از طریق مرز سرویس `src/decision/service.py::calculate_decision_as_of_jalali` به‌صورت ساختاری پیاده‌سازی شده و معتبر است. 

با این حال، **مسیر سرتاسری اجرایی (End-to-End Execution Path) از Stage 3 تا Stage 9 از یک نقطه ورود واقعی (مانند CLI یا API) اثبات نشده و مفقود است**. مهم‌ترین شکاف‌های شناسایی‌شده عبارتند از:
1. **Stage 8**: عدم وجود سرویس یا کوئری استخراج سری داده‌های روزانه بازار برای `MarketEngine.analyze_market` جهت تولید `MarketSignalResult`.
2. **Stage 3**: عدم وجود فراخواننده اجرایی برای استخراج KPIها و فراخوانی `FundamentalScoringEngine.calculate_score` جهت تأمین `FundamentalScoreResult`.
3. **Stage 9**: نبود مدل پایگاه‌داده و مخزن ذخیره‌سازی برای خروجی نهایی تصمیم (`FinalDecisionResult`).
4. **Stage 7 (P54)**: خطای عدم امکان انتخاب پارامترهای تاریخ‌دار تاریخی (`LookupError`) به دلیل نبود رکوردهای R8 در `ParameterRegistry`.

---

### ۲. ماتریس شواهد و قراردادهای یکپارچه‌سازی (Evidence and Contract Matrix)

| مرز (Boundary) | تابع / رابط موجود (Existing Function/Interface) | ورودی‌ها و ناورداهای شناسه (Required Inputs & Invariants) | خروجی (Output) | ماندگاری / بازیابی موجود (Persistence/Retrieval) | شواهد فراخواننده واقعی (Evidence of Real Caller) | قرارداد مفقود یا مانع (Missing Contract / Blocker) | طبقه‌بندی (Classification) |
|---|---|---|---|---|---|---|---|
| **Stage 3 ← downstream** | `FundamentalScoringEngine.calculate_score` در `src/scoring/engine.py:169` | `company_id: int`, `period_id: int`, `industry_code: str`, `kpi_results: List[KPIResult]`, `peer_values`, `historical_values` | `FundamentalScoreResult` | ندارد | تست‌های واحد در `test_stage3_scoring.py` | عدم وجود سرویس/فراخواننده برای گردآوری `KPIResult` از Stage 1 و ارسال به Stage 9 | **EXISTS BUT CALLER UNPROVEN** |
| **Stage 5 Forecast production/retrieval** | `generate_and_persist_forecast` در `src/forecast/service.py:137`؛ `ForecastRecordRepository.read_at_cutoff` در `src/forecast/repo.py:112` | `session: Session`, `company_id: int`, `forecast_period_id: int`, `data_cutoff_datetime: datetime`, `trend_result: Optional[TrendResult]` | `CompanyForecastResult` | `ForecastVersion` و `ForecastInputRefModel` در SQLite via `ForecastRecordRepository` | تست‌های واحد در `test_stage5_forecast.py` | عدم فراخوانی در یک مسیر برنامه‌ای سرتاسری و عدم وجود تبدیل انباره تاریخچه‌ای به `CompanyForecastResult` برای اجراهای گذشته | **EXISTS BUT CALLER UNPROVEN** |
| **Stage 7 Valuation** | `calculate_valuation_as_of_jalali` در `src/valuation/service.py:12` | `session: Session`, `company_id: int`, `period_id: int`, `forecast_result: CompanyForecastResult`, `as_of_jalali_date: JalaliDate`. **Invariants:** `forecast_result.company_id == company_id` و `period_id == period_id` | `ValuationResult` | خواندن قیمت بازار از `MarketDaily` via `select_market_price_as_of`. عدم وجود مدل ذخیره‌سازی برای `ValuationResult` | فراخوانی در `src/decision/service.py::calculate_decision_as_of_jalali` | عدم وجود ممیزی کامل Point-in-Time برای بنچمارک‌ها؛ خطای `LookupError` در انتخاب پارامترهای تاریخ‌دار تاریخی (P54) | **EXISTS AND CONNECTED** |
| **Stage 8 Market Analysis** | `MarketEngine.analyze_market` در `src/market/engine.py:145` | `company_id: int`, `as_of_date: datetime`, `market_data: Sequence[Dict[str, Any]]`, `industry_benchmark`, `market_benchmark`, `point_in_time: bool` | `MarketSignalResult` | ندارد | تست‌های واحد در `test_stage8_market.py` | نبود کوئری/سرویس استخراج داده‌های روزانه OHLCV بازار برای ساخت `market_data` و اجرای Stage 8 | **EXISTS BUT CALLER UNPROVEN** |
| **Stage 9 Decision** | `DecisionEngine.make_decision` در `src/decision/engine.py`؛ `calculate_decision_as_of_jalali` در `src/decision/service.py:12` | `session: Session`, `forecast_result: CompanyForecastResult`, `as_of_jalali_date: JalaliDate`, `fundamental_result: FundamentalScoreResult`, `market_result: MarketSignalResult`. **Invariants:** تطابق `company_id` و `period_id` در تمام ورودی‌ها | `ValuationDecisionResult` (شامل `ValuationResult` و `FinalDecisionResult`) | ندارد (مدل پایگاه‌داده/مخزن برای `FinalDecisionResult` وجود ندارد) | تست‌های یکپارچه‌سازی در `test_stage9_decision.py` | عدم وجود فراخواننده نهایی برنامه‌ای و نبود مقصدی برای ذخیره خروجی تصمیم | **EXISTS AND CONNECTED** |
| **Shared Execution Context** | مالکیت Session در `src/core/database.py` (`SessionLocal`) | `data_cutoff_datetime` (UTC datetime), `as_of_jalali_date` (Jalali tuple), `calculation_timestamp` (UTC datetime) | Session instance / Datetimes | SQLite database `tehran_stock.db` | سرویس‌های Stage 5, Stage 7, Stage 9 | نبود مدیریت‌کننده متمرکز جلسه (Session Owner) در یک مسیر تولیدی برای مدیریت تراکنش و زمان‌بندی تاریخ‌ها | **EXISTS BUT CALLER UNPROVEN** |

---

### ۳. شکاف‌های اثبات‌شده در برابر مجهولات (Confirmed Gaps vs Unknowns)

#### شکاف‌های اثبات‌شده (Confirmed Gaps):
1. **نبود نقطه ورود اصلی برنامه (No Main Entry Point / CLI / API)**: هیچ فایل اجرایی در ریشه پروژه یا `src/` برای اجرای کامل زنجیره تحلیل از Stage 3 تا Stage 9 وجود ندارد.
2. **عدم وجود سرویس استخراج داده‌های بازار برای Stage 8**: هیچ ماژولی داده‌های قیمت روزانه و حجم بازار را از `tehran_stock.db` استخراج نمی‌کند تا به‌عنوان `market_data` به `MarketEngine.analyze_market` تحویل دهد.
3. **عدم وجود سرویس استخراج و گردآوری KPIها برای Stage 3**: هیچ مسیری `KPIResult`ها را از صورت‌های مالی استخراج نمی‌کند تا به `FundamentalScoringEngine` داده شود.
4. **عدم ذخیره‌سازی تصمیم نهایی (No Persistence for FinalDecisionResult)**: هیچ جدول یا مدل SQLAlchemy برای ذخیره‌سازی `FinalDecisionResult` تعریف نشده است.
5. **خطای انتخاب پارامترهای تاریخی ارزش‌گذاری (P54 - Parameter Versioning Gap)**: متد `resolve_parameter_set_as_of` در صورت دریافت تاریخ تاریخی، به دلیل نبود رکوردهای تاریخ‌دار R8 در `ParameterRegistry` خطای `LookupError` صادر می‌کند.

#### مجهولات (Unknowns):
1. **سیاست کسب‌وکار برای ذخیره‌سازی تصمیم**: آیا خروجی Stage 9 باید در پایگاه‌داده ذخیره شود یا فقط به‌صورت یک گزارش موقت (Ephemeral) در حافظه/API بازگردانده شود؟
2. **نحوه تعیین `as_of_jalali_date` و `data_cutoff_datetime` در یک اجرای واقعی**: آیا کاربر این دو تاریخ را به‌صورت ورودی دستی CLI/API وارد می‌کند یا سیستم آن‌ها را از آخرین تاریخ گزارش/بازار استخراج می‌کند؟

---

### ۴. کمینه‌ترین تکلیف اجرایی پیشنهادی (Minimal Recommended Implementation Task)

* **نام مسئولیت و رابط/فایل هدف**: ایجاد یک سرویس استخراج داده‌های بازار برای Stage 8 (مانند `src/market/service.py::analyze_market_as_of_jalali`) و یک سرویس/کلاس هماهنگ‌کننده اجرایی کمینه (Application Boundary/Caller) که ورودی‌های لازم را گردآوری کرده و به `src/decision/service.py::calculate_decision_as_of_jalali` پاس دهد.
* **علت اولویت نخست بودن**: سرویس `src/decision/service.py::calculate_decision_as_of_jalali` هم‌اکنون اتصال Stage 5، Stage 7 و Stage 9 را به‌طور کامل و سالم مدیریت می‌کند. تنها مانع اجرایی شدن آن، تأمین ورودی‌های `MarketSignalResult` (از Stage 8) و `FundamentalScoreResult` (از Stage 3) است.
* **پیش‌نیازها و تصمیمات حل‌نشده**:
  * رفع محدودیت P54 با افزودن حداقل یک رکورد پارامتر تاریخ‌دار معتبر به `ParameterRegistry` جهت جلوگیری از `LookupError` در تحلیل‌های تاریخی.
  * تصمیم‌گیری درباره نحوه ذخیره‌سازی خروجی Stage 9 (در صورت نیاز به ذخیره‌سازی).
* **قراردادهای موجود که باید بدون تغییر باقی بمانند**:
  * `src/valuation/engine.py` (طبق محدودیت‌های P62 و P48 نباید بازطراحی شود).
  * امضا و ناورداهای شناسه در `src/decision/service.py::calculate_decision_as_of_jalali`.
  * فرمول‌های مالی، آستانه‌های P/E و منطق ریسک/اعتماد.
* **شواهد اثبات‌کننده تکمیل**:
  * اجرای یک اسکریپت آزمایشی غیرتولیدی که برای یک شناسه شرکت و تاریخ جلالی واقعی، تمام ورودی‌ها را فراخوانی کرده و خروجی `ValuationDecisionResult` معتبر و کامل تولید کند.
* **تست‌هایی که کاربر باید بعداً اجرا کند (بدون اجرای توسط Agent)**:
  * `python -m pytest src/tests/test_stage7_valuation.py`
  * `python -m pytest src/tests/test_stage9_decision.py`
  * `python -m pytest src/tests/test_stage5_forecast.py`
  * `python -m pytest src/tests/test_stage3_scoring.py`
  * `python -m pytest src/tests/test_stage8_market.py`

---

### ۵. طرح اعتبارسنجی قابل اجرا توسط کاربر (User-Run Validation Plan)

کاربر گرامی، جهت اعتبارسنجی پیشرفت‌ها و اطمینان از سلامت قراردادها، دستورات زیر را در محیط PowerShell اجرا فرمایید:

```powershell
# ۱. اجرای تست‌های ارزش‌گذاری Stage 7
python -m pytest src/tests/test_stage7_valuation.py -v

# ۲. اجرای تست‌های تصمیم‌گیری Stage 9
python -m pytest src/tests/test_stage9_decision.py -v

# ۳. اجرای یکپارچه پنج مجموعه تست اصلی پروژه
python -m pytest src/tests/test_stage3_scoring.py src/tests/test_stage5_forecast.py src/tests/test_stage7_valuation.py src/tests/test_stage8_market.py src/tests/test_stage9_decision.py -q
```

---

### ۶. فایل‌های بررسی‌شده و دلایل دسترسی (Files Inspected)

بر اساس دستورالعمل P62، دقیقاً فایل‌های مجاز و حداقل بررسی شدند:
1. `PROMPT.md` / `prompt.md`: بررسی دستورالعمل P62 و الزامات P54.
2. `stepsForStage7.md`: بررسی برنامه اجرایی، یافته‌های ممیزی P48 و سیاست‌های D1–D9.
3. `reply.md` / `temp_report2.md`: بررسی نتایج ممیزی P61 در خصوص آستانه‌های پراکندگی سناریوها.
4. `zErrors.md`: بررسی جزئیات خطای pytest و لئک‌آپ پارامترها (`LookupError` در P54).
5. `07_Stage7_Valuation.md`: بررسی مشخصات قفل‌شده Stage 7.
6. `src/scoring/engine.py`: بررسی متد `calculate_score` و ورودی‌های Stage 3.
7. `src/forecast/service.py`, `src/forecast/schema.py`, `src/forecast/repo.py`: بررسی مسیر تولید و بازیابی پیش‌بینی Stage 5.
8. `src/valuation/service.py`, `src/valuation/schema.py`: بررسی مرز سرویس ارزش‌گذاری جلالی Stage 7.
9. `src/market/engine.py`, `src/market/schema.py`: بررسی متد `analyze_market` و قرارداد Stage 8.
10. `src/decision/service.py`, `src/decision/schema.py`: بررسی متد `calculate_decision_as_of_jalali` و ساختار Stage 9.
11. `src/core/database.py`: بررسی الگوی مدیریت جلسه SQLAlchemy (`SessionLocal`).

---

### ۷. تأییدیه صریح عدم تغییر کد و عدم اجرای تست‌ها/CI (Explicit Statement)

**بدین‌وسیله صریحاً تأیید می‌شود که در طول انجام این گزارش تحلیلی (P62):**
1. هیچ‌گونه تغییری در کدهای سورس برنامه، فایل‌های تست، مشخصات معمارانه یا فایل‌های برنامه‌ریزی پروژه ایجاد نشده است.
2. هیچ دستور تستی (pytest)، ابزار CI یا دستور اجرایی کد توسط سیستم/Agent اجرا نگردیده است.
3. گزارش فوق تماماً تحلیلی و مستند بر شواهد موجود در منابع پروژه می‌باشد.

💡 *آیا تمایل دارید پس از بررسی این گزارش تحلیلی، درباره پیاده‌سازی سرویس استخراج داده‌های بازار برای Stage 8 یا تعریف رکوردهای تاریخ‌دار پارامترها (P54) تصمیم‌گیری کنیم؟*