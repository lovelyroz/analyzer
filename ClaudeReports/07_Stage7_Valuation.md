# Stage 7 — Valuation Engine

## Specification — V1 (Requirements Baseline) — NOT FROZEN

### Status

~~DESIGNED → REVIEWED → STRESS TESTED → AUDITED → **LOCKED**~~

> **Status Correction (Documentation Reconciliation):** عبارت «LOCKED» و عنوان قبلی «Locked Specification — V1» وضعیت **طراحی/مشخصات** را توصیف می‌کردند، نه عبور Stage 7 از Freeze Gate. **Stage 7 در این سند FROZEN نیست.** متن الزامات این مشخصات حذف یا تضعیف نشده است؛ هر جا کد فعلی یک الزام را برآورده نمی‌کند، در حاشیه‌های «V1 Implementation Status» ثبت می‌شود و الزام همچنان به قوت خود باقی است.

**وضعیت فعلی Stage 7: IMPLEMENTATION PARTIAL — NOT FROZEN.**

### راهنمای خواندن حاشیه‌ها

| برچسب | معنا |
|---|---|
| **V1 Implementation Status (factual annotation)** | رفتار مشاهده‌شده در کد/آزمون‌های فعلی. «الزام» نیست و «سیاست» نیست. |
| **V1 Policy Record — Dn** | سیاست *مورد نظر* V1 برای تصمیم Dn. بیان‌کنندهٔ رفتار پیاده‌شده نیست مگر در همان رکورد به‌صراحت «Verified in code» قید شده باشد. |
| **Deferred beyond V1** | قابلیتی که در V1 صادر/پیاده نمی‌شود ولی الزام آن در این سند باقی است. |
| **Freeze blocker (Fn)** | شرطی که تا رفع آن Stage 7 نباید Frozen اعلام شود. |

### V1 Scope and Freeze Status Record

**مبنای ثبت.** سیاست‌های D1–D9 از `stepsForStage7.md` و تحلیل `reply.md` گرفته شده‌اند. `stepsForStage7.md` آن‌ها را صراحتاً «پیشنهادی» و «تأییدنشده در کد یا مشخصات» می‌نامد؛ این سند آن‌ها را بنا به دستور مستندسازی این مرحله به‌عنوان **سیاست مورد نظر V1** ثبت می‌کند. سند تأیید رسمی جداگانه‌ای در فایل‌های بررسی‌شده مشاهده نشد؛ تبدیل این سیاست‌ها به نیازمندی اجرایی و آزمون پذیرش مرحلهٔ بعد است.

**مبنای بررسی کد.** نسخهٔ فایل‌های `src/valuation/{engine,parameters,schema}.py` و `src/tests/test_stage7_valuation.py` پس از تحویل Final P35 (که مالک اعلام کرده تغییری نکرده‌اند). نسخهٔ خودِ مخزن مالک توسط ویرایشگر این سند دیده نشده است. هیچ pytest یا CI در این مرحله اجرا نشد. شمارهٔ خط‌های `engine.py` به‌دلیل ناپایداری حذف و با نام تابع جایگزین شده‌اند.

| شناسه | سیاست مورد نظر V1 | تأییدشده در کد فعلی | Deferred beyond V1 |
|---|---|---|---|
| **D1** | `ASSESSMENT_FLIP_RISK` تا تعریف معتبر شوک و آستانه صادر نشود. | صفر ارجاع در `src/valuation`. | Alert، تعریف Flip، اندازهٔ شوک، Severity. |
| **D2** | معیار فعلی وابستگی معتبر شمرده نمی‌شود؛ `HIGH_MULTIPLE_DEPENDENCE` فعال نشود. | صفر ارجاع؛ `high_dependence_share = 0.60` ثبت‌شده ولی مصرف‌نشده. | روش معتبر اندازه‌گیری وابستگی به P/E. |
| **D3** | `HIGH_EPS_DEPENDENCE` بدون تعریف معتبر اضافه نشود؛ EPS مرحلهٔ ۵ حفظ شود و در Stage 7 بازمحاسبه نشود. | صفر ارجاع؛ EPS مستقیماً از `forecast_result.scenario_forecasts` خوانده می‌شود. | Alert و قاعدهٔ اتصال مسیر تغییرات پیش‌بینی. |
| **D4** | `MARGIN_ASSUMPTION_RISK` تا وجود ورودی معتبر و تاریخ‌دار درآمد/هزینه/حاشیه به‌تعویق می‌افتد. | صفر ارجاع؛ امضای `calculate_valuation` چنین ورودی‌ای ندارد. | Alert و ورودی‌های لازم. |
| **D5** | خروجی‌های تحلیلی (`review_priority` و …) حفظ شوند؛ `HIGH_IMPACT_HIGH_UNCERTAINTY` بدون معیار مستقل صادر نشود. | `review_priority` محاسبه می‌شود؛ Alert مذکور صفر ارجاع. | Alert و معیارهای مستقل اثر/عدم‌قطعیت. |
| **D6** | فقط دو Driver فعلی (`EPS`, `TARGET_PE`)؛ بدون نگاشت یا فرمول ابداعی برای بانک/هلدینگ/غیرمالی. | `_driver_analysis` فقط همین دو را تولید می‌کند و شاخه‌ای بر اساس `industry_code` ندارد. | زنجیره‌های §42–§44 و نگاشت صنعت. |
| **D7** | محدودیت‌های Point-in-Time صریحاً اعلام شود؛ cutoff به‌تنهایی اثبات دسترس‌پذیری نیست. | بخش PIT در حاشیهٔ §56. | اجرای کامل provenance و انتخاب date-safe. |
| **D8** | نام‌های خروجی کد حفظ و رفتار واقعی مستند شود؛ بدون تغییر قرارداد خروجی. | فهرست alertهای واقعی در حاشیهٔ §49. | rename/alias (پس از بررسی مصرف‌کنندگان). |
| **D9** | نسخه‌بندی تاریخی کامل ادعا نشود. | مکانیزم و محدودیت‌ها در حاشیهٔ §65. | رکوردهای تاریخ‌دار، provenance پارامتر، قاعدهٔ تاریخ حاکم، بازسازی تاریخی. |

**Freeze blockers (باز):**

| شناسه | مانع | وضعیت شواهد |
|---|---|---|
| **F1** | مسیر فراخوانی تولیدی و آزمون یکپارچهٔ واقعی. | در فایل‌های بررسی‌شده هیچ فراخوان `calculate_valuation` خارج از آزمون دیده نشد (بررسی مخزن‌گستر انجام نشده است). `test_p6_production_path_real_stage5_forecast` زنجیرهٔ Stage 5→7 را داخل آزمون اجرا می‌کند اما فراخوان برنامه نیست؛ آزمون‌های Stage 9 `ValuationResult` دستی تزریق می‌کنند. وجود آزمون واحد ثابت نمی‌کند برنامهٔ واقعی Stage 7 را فراخوانی می‌کند. |
| **F2** | دو آزمون failing-first و تناقض آن‌ها با آزمون P3. | `test_p2_sector_driver_decomposition_missing` و `test_p2_required_flip_dependence_alerts_missing` عمداً حفظ شده‌اند؛ `test_p3_flip_dependence_alerts_remain_explicitly_unresolved` نبود همان پنج alert را assert می‌کند. تطبیق باید در گام جدا و بازبینی‌شده انجام شود؛ در این مرحله هیچ آزمونی تغییر نکرد. |
| **F3** | محدودیت‌های PIT (D7). | حاشیهٔ §56 و §85. |
| **F4** | نسخه‌بندی ناقص پارامترها (D9). | حاشیهٔ §65. |
| **F5** | تعیین تکلیف قرارداد نام alertها و بررسی مصرف‌کنندگان بیرون از مخزن (D8). | حاشیهٔ §49. |
| **F6** | شواهد اجرای تست و CI. | نتایج pytest واقعی را مالک گزارش کرده است (مشاهده‌نشده توسط ویرایشگر سند)؛ اجرای CI مشاهده نشده است. |

سیاست‌های D1–D6 «Deferred beyond V1» تا زمانی که تأیید رسمی و تطبیق آزمون‌ها (F2) انجام نشده، الزام باز محسوب می‌شوند؛ تعویق، رفع الزام نیست.

---

# 1. Purpose

Stage 7 وظیفه دارد به این سؤال پاسخ دهد:

**«با توجه به سود آینده شرکت، قیمت فعلی سهم نسبت به آن سود چقدر منطقی، ارزان یا گران است؟»**

Stage 7 یک **Valuation Engine** است، نه Decision Engine.

بنابراین:

* ارزش‌گذاری انجام می‌دهد.
* Fair Value محاسبه می‌کند.
* Forward P/E محاسبه می‌کند.
* وضعیت ارزندگی را ارزیابی می‌کند.
* ریسک و Confidence ارزش‌گذاری را مشخص می‌کند.
* Sensitivity و Alert تولید می‌کند.

اما:

* Buy / Sell / Hold صادر نمی‌کند.
* تحلیل تکنیکال انجام نمی‌دهد.
* Fundamental Score را تغییر نمی‌دهد.
* Forecast جدید تولید نمی‌کند.
* Forecast Reliability را دوباره محاسبه نمی‌کند.
* Market Signal ایجاد نمی‌کند.

تصمیم نهایی سرمایه‌گذاری متعلق به **Stage 9 — Decision Engine** است.

---

# 2. Position in Architecture

```text
Stage 5
Forecast Engine
      │
      ▼
Stage 6
Forecast Evaluation & Calibration
      │
      ▼
Stage 7
VALUATION ENGINE
      │
      ├── Forward P/E
      ├── Historical Valuation
      ├── Industry Valuation
      ├── Target P/E
      ├── Scenario Fair Value
      ├── Scenario Probability
      ├── Expected Fair Value
      ├── Valuation Assessment
      ├── Valuation Risk
      ├── Valuation Confidence
      └── Sensitivity / Alerts
      │
      ▼
Stage 9
Decision Engine
```

Stage 8 — Market Engine یک مسیر مستقل دارد و Fundamental/Valuation و Market تا Stage 9 با یکدیگر ادغام نمی‌شوند.

---

# 3. Core Architectural Rule

Stage 7 فقط از طریق **Input/Output Contract** با Stageهای دیگر ارتباط دارد.

منطق داخلی Stage 7 می‌تواند در آینده تغییر کند بدون اینکه معماری Stageهای دیگر تغییر کند، مشروط بر اینکه Contract معتبر حفظ شود.

مثال:

```text
Valuation Model v1.0
        ↓
Valuation Model v1.1
        ↓
Valuation Model v2.0
```

نسخه قبلی حذف یا overwrite نمی‌شود.

هر خروجی Stage 7 باید دارای:

```text
valuation_timestamp
valuation_model_version
data_cutoff_datetime
```

باشد.

---

# 4. Primary Valuation Axis

محور اصلی Valuation در V1:

**Forward P/E**

فرمول:

```text
Forward P/E =
Current Market Price
÷
Forecast EPS
```

Forecast EPS از Stage 5 دریافت می‌شود.

Forecast Reliability از Stage 6 دریافت می‌شود.

---

# 5. Scenario Forward P/E

سه Scenario داریم:

```text
Bear
Base
Bull
```

محاسبات:

```text
Bear Forward P/E =
Current Price / Bear EPS

Base Forward P/E =
Current Price / Base EPS

Bull Forward P/E =
Current Price / Bull EPS
```

Forward P/E باید برای هر Scenario مستقل محاسبه شود.

---

# 6. Invalid EPS Rule

اگر:

```text
EPS < 0
EPS = 0
SIGN_CHANGE
```

باشد، سیستم نباید P/E مصنوعی تولید کند.

خروجی:

```text
Forward P/E = NULL
```

و یکی از Flagهای مناسب:

```text
NEGATIVE_EPS
ZERO_EPS
LOSS_TO_PROFIT
PROFIT_TO_LOSS
SIGN_CHANGE
NOT_APPLICABLE
```

اعمال می‌شود.

در این شرایط نباید از P/E برای تولید Fair Price مصنوعی استفاده شود.

---

# 7. Current Market Price

Current Price از MarketDaily در Stage 1 دریافت می‌شود.

قیمت مورد استفاده باید دارای تاریخ مشخص باشد:

```text
valuation_date
market_price_date
```

Valuation باید بتواند مشخص کند دقیقاً از چه قیمت بازار استفاده شده است.

---

# 8. Historical P/E

تعریف اصلی Historical P/E در V1:

```text
Point-in-Time TTM P/E =
Point-in-Time Market Price
÷
Point-in-Time TTM EPS
```

اصل Point-in-Time اجباری است.

در هر تاریخ تاریخی فقط داده‌هایی مجاز هستند که تا همان تاریخ واقعاً منتشر و در دسترس بوده‌اند.

بنابراین استفاده از اطلاعات گزارش‌های آینده ممنوع است.

---

# 9. Historical Valuation Series

در صورت وجود داده کافی، Historical P/E باید به شکل Time Series نگهداری شود.

خلاصه‌های قابل استخراج:

```text
Historical Median P/E
Historical Min P/E
Historical Max P/E
Historical P/E Percentile
Current vs Historical Median
```

معیار اصلی V1:

**Historical Median P/E**

Median بر Mean اولویت دارد.

---

# 10. Industry Valuation

مقایسه شرکت با شرکت‌های **هم‌صنعت** انجام می‌شود.

حداقل Peer Count:

```text
8 valid peers
```

در صورت کمتر از 8 Peer معتبر:

```text
INDUSTRY_BENCHMARK_INSUFFICIENT
```

---

# 11. Industry Forward P/E

Benchmark اصلی صنعت در صورت وجود داده معتبر:

```text
Industry Forward P/E Median
```

شرایط:

* EPS Forecast معتبر
* Market Price معتبر
* حداقل 8 Peer
* Point-in-Time compatibility
* عدم ترکیب داده‌های Forward و TTM

---

# 12. Industry TTM P/E

اگر Industry Forward P/E قابل محاسبه نباشد، Industry TTM P/E می‌تواند به‌عنوان Fallback استفاده شود.

Forward P/E و TTM P/E نباید در یک Population مخلوط شوند.

مثلاً این کار ممنوع است:

```text
5 companies Forward P/E
+
6 companies TTM P/E
→ Median
```

---

# 13. Benchmark Hierarchy

Target P/E Base باید از این سلسله‌مراتب استفاده کند:

```text
1. Industry Forward P/E Median
        ↓
2. Historical Median P/E
        ↓
3. Industry TTM P/E Median
        ↓
4. INSUFFICIENT_DATA
```

Fallback باید در خروجی ثبت شود.

مثلاً:

```text
target_pe_source =
INDUSTRY_FORWARD_PE
```

یا:

```text
target_pe_source =
HISTORICAL_MEDIAN_PE
```

---

# 14. Fundamental Score Rule

Fundamental Score نباید مستقیماً Target P/E را ضرب یا Scale کند.

مثلاً این روش ممنوع است:

```text
Target P/E =
Industry P/E × Fundamental Score Factor
```

زیرا می‌تواند Double Counting ایجاد کند.

Fundamental Quality می‌تواند روی:

```text
Valuation Assessment
Valuation Confidence
Risk
Alerts
```

اثر بگذارد، نه مستقیماً بر Multiple در V1.

---

# 15. Trend Rule

Trend Stage 4 نباید مستقیماً Target P/E را تغییر دهد.

مثلاً:

```text
Strong Improvement
→ P/E +20%
```

ممنوع است.

Trend می‌تواند:

* Scenario Probability
* Risk
* Confidence
* Alerts

را تحت تأثیر قرار دهد.

---

# 16. Forecast Reliability Rule

Forecast Reliability از Stage 6 دریافت می‌شود.

Forecast Reliability نباید Forward P/E را به‌صورت ریاضی تغییر دهد.

ممنوع:

```text
Adjusted P/E =
Forward P/E × Reliability
```

یا:

```text
Fair Value =
EPS × P/E × Reliability
```

Reliability بیانگر میزان اعتماد ما به Forecast است، نه بخشی از فرمول P/E.

---

# 17. Target P/E

Stage 7 سه Target Multiple ایجاد می‌کند:

```text
Target P/E Bear
Target P/E Base
Target P/E Bull
```

Base Target P/E بر Benchmark معتبر متکی است.

Bear و Bull باید بر اساس شرایط اقتصادی Scenario تعریف شوند.

استفاده از یک فاصله ثابت و دلخواه مانند:

```text
Bear = Base × 0.8
Bull = Base × 1.2
```

به‌عنوان قانون معماری ممنوع است.

پارامترهای Scenario Multiple باید:

* Explainable
* Versioned
* Backtestable
* Economically justified

باشند.

---

# 18. Scenario Ordering

در شرایط عادی:

```text
Bear Fair Value
≤
Base Fair Value
≤
Bull Fair Value
```

انتظار می‌رود.

اما سیستم نباید برای حفظ ظاهری ترتیب، داده‌ها را مصنوعی Reorder کند.

اگر ترتیب از نظر اقتصادی منطقی نباشد:

```text
SCENARIO_ORDER_WARNING
```

ثبت می‌شود.

---

# 19. Fair Value

برای هر Scenario:

```text
Fair Value =
Forecast EPS
×
Target P/E
```

بنابراین:

```text
Bear Fair Value =
Bear EPS × Bear Target P/E

Base Fair Value =
Base EPS × Base Target P/E

Bull Fair Value =
Bull EPS × Bull Target P/E
```

---

# 20. Scenario Upside / Downside

```text
Scenario Upside =
Scenario Fair Value
÷
Current Price
−
1
```

سه خروجی مستقل:

```text
Bear Upside / Downside
Base Upside / Downside
Bull Upside / Downside
```

---

# 21. Scenario Probability

سه احتمال:

```text
Bear Probability
Base Probability
Bull Probability
```

شرط دائمی:

```text
Bear + Base + Bull = 100%
```

---

# 22. Initial V1 Scenario Prior

Prior اولیه V1:

```text
Bear = 20%
Base = 60%
Bull = 20%
```

این Prior یک Architecture Constant غیرقابل تغییر نیست.

بلکه:

```text
Model Version Parameter
```

است.

بعداً می‌تواند با Backtest و Calibration اصلاح شود.

---

# 23. Probability Evidence Families

برای جلوگیری از Double Counting، Probability Adjustment در چهار Evidence Family انجام می‌شود.

## Family 1 — Fundamental Direction

شامل:

```text
Revenue Trend
Operating Profit Trend
Net Profit Trend
EPS Trend
```

---

## Family 2 — Forecast Direction

شامل:

```text
Forecast Revision Trend
Forecast Dispersion
Forecast Reliability
```

---

## Family 3 — Profitability Assumption Risk

شامل:

```text
Operating Margin
Net Margin
Financial Costs
Tax
Other material profitability assumptions
```

---

## Family 4 — Data / Structural Risk

شامل:

```text
Data Quality
Low Base
Sign Change
Insufficient History
Share Count Risk
Corporate Action Risk
```

---

# 24. No Probability Double Counting

متغیرهای بسیار همبسته نباید چند بار در Probability اثر داده شوند.

مثلاً:

```text
Net Profit Growth
EPS Growth
Net Profit Momentum
EPS Momentum
```

نباید چهار رأی مستقل تلقی شوند اگر عملاً یک اتفاق اقتصادی را بیان می‌کنند.

ابتدا باید Family-level evidence ساخته شود.

---

# 25. Trend and Scenario Probability

Stage 4 Trend می‌تواند Probability را جابه‌جا کند.

مثلاً:

```text
Strong Improvement
→ Bull Probability ↑
→ Bear Probability ↓
```

یا:

```text
Strong Deterioration
→ Bear Probability ↑
→ Bull Probability ↓
```

اما مقدار Adjustment باید:

* محدود
* قابل توضیح
* Versioned
* Backtestable

باشد.

---

# 26. Forecast Revision Trend

Forecastهای جدید Stage 5 جای Forecast قبلی را overwrite نمی‌کنند.

مثال:

```text
EPS Forecast
1100
→
1180
→
1270
```

این وضعیت می‌تواند:

```text
POSITIVE_FORECAST_REVISION
```

ایجاد کند و به‌عنوان Evidence برای Scenario Probability استفاده شود.

برعکس:

```text
1270
→
1180
→
1100
```

می‌تواند Evidence منفی باشد.

---

# 27. Reliability and Probability

Forecast Reliability بالا به معنی Bull Probability بالا نیست.

Reliability فقط می‌گوید:

**چقدر می‌توانیم به Forecast Engine اعتماد کنیم؟**

بنابراین:

```text
High Reliability
+
Negative Forecast
```

کاملاً ممکن است.

در چنین حالتی ممکن است Bear Probability حتی بیشتر شود.

---

# 28. Probability Confidence

یک خروجی مستقل تعریف می‌شود:

```text
Probability Confidence
```

این مفهوم با Forecast Reliability متفاوت است.

```text
Forecast Reliability:
Forecast Engine historically چقدر دقیق بوده؟

Probability Confidence:
شواهد فعلی برای Probability Distribution چقدر قوی هستند؟
```

ممکن است:

```text
Forecast Reliability = High
Probability Confidence = Low
```

باشد.

---

# 29. Scenario Dependency

Scenario Probability با Scenario Dependency متفاوت است.

Probability می‌گوید:

```text
این Scenario چقدر محتمل است؟
```

Dependency می‌گوید:

```text
این Scenario بیشتر به چه فرضی وابسته است؟
```

مثلاً Bull Case:

```text
Operating Margin Expansion     45%
Revenue Growth                 30%
Target Multiple Expansion      25%
```

این اعداد Probability نیستند.

---

# 30. Expected Fair Value

پس از تعیین Probability:

```text
Expected Fair Value =
Bear Probability × Bear Fair Value
+
Base Probability × Base Fair Value
+
Bull Probability × Bull Fair Value
```

Probabilityها در محاسبه به شکل Decimal استفاده می‌شوند.

---

# 31. Expected Upside

```text
Expected Upside =
Expected Fair Value
÷
Current Price
−
1
```

Expected Fair Value جای Scenario Range را نمی‌گیرد.

Dashboard باید هر دو را حفظ کند.

---

# 32. Valuation Assessment Architecture

Valuation Assessment از سه لایه تشکیل می‌شود:

```text
1. Relative Valuation
2. Fair Value Upside / Downside
3. Confidence & Risk
```

هیچ‌یک به تنهایی برای Assessment کافی نیست.

---

# 33. Relative Valuation

مقایسه‌هایی مانند:

```text
Current Forward P/E
vs
Target Forward P/E

Current Forward P/E
vs
Historical Median P/E

Current Forward P/E
vs
Industry Median Forward P/E
```

انجام می‌شوند.

---

# 34. Valuation Status

Statusهای استاندارد:

```text
VERY_ATTRACTIVE
ATTRACTIVE
FAIR
EXPENSIVE
VERY_EXPENSIVE
```

Special States:

```text
INSUFFICIENT_DATA
NOT_APPLICABLE
UNRELIABLE_VALUATION
```

---

# 35. Assessment Thresholds

Thresholdهای دقیق Valuation Status جزو Architecture Constant نیستند.

مثال اولیه‌ای که می‌تواند برای V1 تست شود:

```text
Very Attractive:
Expected Upside ≥ +30%
AND
Base Upside ≥ +15%

Attractive:
Expected Upside ≥ +15%
AND
Base Upside ≥ +5%

Fair:
Expected Upside approximately
-10% to +15%

Expensive:
Expected Upside ≤ -10%
AND
Base Upside < 0%

Very Expensive:
Expected Upside ≤ -25%
AND
Base Upside ≤ -10%
```

اما این Thresholdها باید به‌عنوان:

```text
Valuation Model Parameters
```

ذخیره شوند.

آنها بعداً با Backtest قابل اصلاح هستند.

---

# 36. Valuation Risk

Valuation Risk از Valuation Status مستقل است.

Risk Levels:

```text
LOW
MEDIUM
HIGH
EXTREME
```

Valuation Risk می‌تواند تحت تأثیر موارد زیر قرار گیرد:

```text
Bear Downside
Scenario Dispersion
Forecast Risk
EPS Risk
Multiple Risk
Margin Risk
Data Quality
Structural Risk
Assessment Flip Risk
```

---

# 37. Attractive Does Not Mean Low Risk

مثلاً:

```text
Expected Upside = +30%
Bear Downside = -50%
```

سیستم نباید فقط:

```text
ATTRACTIVE
```

نمایش دهد.

بلکه چیزی مانند:

```text
Valuation Status = ATTRACTIVE
Valuation Risk = HIGH
```

یا:

```text
EXTREME
```

ممکن است صحیح باشد.

---

# 38. Valuation Confidence

خروجی مستقل:

```text
Valuation Confidence = 0–100
```

عوامل احتمالی:

```text
Forecast Reliability
Probability Confidence
Data Quality
Benchmark Availability
Historical Valuation Depth
Peer Count
Scenario Dispersion
Point-in-Time Validity
```

Confidence با Risk یکی نیست.

---

# 39. Confidence Labels

Labelهای اولیه:

```text
90–100  VERY_HIGH
75–89   HIGH
60–74   MODERATE
40–59   LOW
0–39    VERY_LOW
```

این Thresholdها نیز Model Version Parameters هستند و نه Architecture Constants.

---

# 40. Scenario Dispersion

Stage 7 باید میزان فاصله بین Scenarioها را اندازه‌گیری کند.

مثلاً می‌تواند بر اساس:

```text
Bear Fair Value
Base Fair Value
Bull Fair Value
```

محاسبه شود.

Scenario Dispersion زیاد نشان‌دهنده عدم قطعیت بیشتر Valuation است.

فرمول دقیق Dispersion باید Versioned باشد.

---

# 41. Sensitivity Engine

Sensitivity Engine بررسی می‌کند که Fair Value نسبت به تغییر Assumptionها چقدر حساس است.

در سطح بالا:

```text
EPS Sensitivity
Target P/E Sensitivity
```

تحلیل می‌شوند.

---

# 42. EPS Driver Decomposition

برای شرکت‌های Non-Financial:

```text
Revenue
→
Operating Margin
→
Operating Profit
→
Net Profit
→
EPS
→
Fair Value
```

---

# 43. Bank Driver Decomposition

برای Bank:

```text
Loans / Deposits
→
NII / NIM
→
Net Profit
→
EPS
→
Fair Value
```

---

# 44. Holding Driver Decomposition

برای Investment / Holding:

```text
NAV
→
NAV Growth
→
Net Profit
→
EPS
→
Fair Value
```

P/NAV تحلیل Valuation است و متعلق به Stage 7 است، نه Forecast Stage.

> **V1 Implementation Status (factual annotation — بخش‌های ۴۲ تا ۴۴):**
>
> **این زنجیره‌های Driver در V1 پیاده‌سازی نشده‌اند.** تحلیل Driver فعلی (`_driver_analysis` در `src/valuation/engine.py`) دقیقاً دو Driver را تولید می‌کند:
>
> ```text
> EPS
> TARGET_PE
> ```
>
> و هیچ شاخه‌گیری بر اساس `industry_code` وجود ندارد (این فیلد فقط در metadata بازنویسی می‌شود). `nav_per_share` نیز فقط در metadata به‌صورت `nav_per_share_received` ثبت می‌شود و در هیچ فرمولی مصرف نمی‌شود. تابع `calculate_nav_fair_value` در `src/valuation/models.py` صرفاً یک export متصل‌نشده است.
>
> در نتیجه `valuation_driver_ranking` برای یک شرکت غیرمالی، یک Bank و یک Holding یکسان است. **تصمیم D6 (نگاشت industry و فرمول‌های sector-specific) هنوز حل‌نشده است.**

> **V1 Policy Record — D6 (intended policy):** در V1 فقط قرارداد دو Driver (`EPS` و `TARGET_PE`) حفظ می‌شود. هیچ نگاشت صنعت یا فرمول اختصاصی برای بانک، هلدینگ یا شرکت غیرمالی ابداع نمی‌شود؛ زنجیره‌های §42–§44 **Deferred beyond V1** هستند و الزامشان باقی است. **Verified in code:** `_driver_analysis` فقط `{"EPS", "TARGET_PE"}` را می‌سازد؛ `industry_code` و `nav_per_share` فقط در `metadata` بازنویسی می‌شوند (`industry_code`، `nav_per_share_received`)؛ `calculate_nav_fair_value` در `models.py`/`__init__.py` export شده ولی توسط `engine.py` فراخوانی نمی‌شود. آزمون `test_p2_sector_driver_decomposition_missing` همچنان نبود این زنجیره‌ها را آشکار می‌کند (F2).

---

# 45. Driver Impact

برای هر Driver:

```text
Driver Impact
```

محاسبه می‌شود.

Impact نشان می‌دهد تغییر معقول در Driver چه مقدار Fair Value را تغییر می‌دهد.

---

# 46. Driver Uncertainty

برای هر Driver:

```text
Driver Uncertainty
```

نیز تخمین زده می‌شود.

Uncertainty می‌تواند بر اساس:

* Forecast Error
* Historical Volatility
* Scenario Range
* Data Quality
* Model Stability

تعیین شود.

---

# 47. Review Priority

برای اولویت‌بندی بررسی:

```text
Review Priority
≈
Impact × Uncertainty
```

فرمول دقیق و Normalization باید Model Version Parameter باشد.

> **V1 Implementation Status (factual annotation — به‌روزشده در Documentation Reconciliation؛ جایگزین حاشیهٔ قبلی P19 که پیش از P33/P35 نوشته شده بود):**
>
> فرمول Review Priority **یک پارامتر نسخه‌دار رجیستری نیست.** `_driver_analysis` در `src/valuation/engine.py` برای هر Driver مقدار `review_priority = driver_impact × driver_uncertainty / 100` را حساب می‌کند؛ عدم‌قطعیت از ترکیب ثابت `0.5 / 0.3 / 0.2` (reliability / probability confidence / data quality) و کف `1e-9` ساخته می‌شود. این اعداد در `LITERALS_OUTSIDE_REGISTRY` فهرست شده‌اند و در `parameter_snapshot` نیستند.
>
> *تصحیح:* حاشیهٔ قبلی می‌گفت هیچ رکورد پارامتر نسخه‌دار و هیچ مکانیزم selection در کد وجود ندارد. این دیگر صحیح نیست؛ `src/valuation/parameters.py` شامل `ParameterRecord`، `ParameterSetVersion`، `ParameterRegistry` و resolver تاریخ‌دار است. جزئیات و محدودیت‌ها در حاشیهٔ §65.
>
> **V1 Policy Record — D5 (intended policy):** خروجی‌های تحلیلی `review_priority`، `driver_impact` و `driver_uncertainty` حفظ می‌شوند، اما `HIGH_IMPACT_HIGH_UNCERTAINTY` تا تعریف معیارهای مستقل و معنادار اثر و عدم‌قطعیت صادر نمی‌شود (**Deferred beyond V1**). **Verified in code:** صفر ارجاع به این نام؛ `driver_uncertainty` برای همهٔ Driverها یک مقدار مشترک است (`{key: uncertainty_base for key in drivers}`)؛ و چون اثر هر دو Driver از شوک نسبیِ یکسان روی هویت `FV = EPS × target P/E` به‌دست می‌آید، `driver_impact` در probe روی کپی مرجع (۶ پیکربندی ورودی، بدون pytest) برای هر دو ۵۰٪ بود و ترتیب Driverها با نام شکسته می‌شود (`EPS` اول). در همین حالت alert اطلاعاتی `INFO:TOP_DRIVER:<driver>` صادر می‌شود که با `HIGH_IMPACT_HIGH_UNCERTAINTY` یکی نیست. بنابراین معیارهای فعلی برای تفکیک Driverها و صدور هشدار ریسک کافی نیستند.

هدف:

Driverهایی که هم:

```text
High Impact
+
High Uncertainty
```

دارند، در اولویت بررسی باشند.

---

# 48. Alert Engine

Severity Levels:

```text
INFO
WATCH
WARNING
CRITICAL
```

Alerts فقط Risk/Review Alert هستند.

آنها Buy/Sell Signal نیستند.

> **V1 Threshold Provenance (factual annotation):**
>
> این سند **هیچ مقدار آستانه‌ای برای تریگرهای Alert یا Risk تعریف نکرده است**. مقادیری که موتور فعلی استفاده می‌کند ثابت‌های کد در `src/valuation/parameters.py` هستند:
>
> ```text
> ALERT_THRESHOLDS:
>   high_scenario_dispersion   = 0.50
>   low_forecast_reliability   = 40.0
>   benchmark_divergence_ratio = 1.50
>   historical_divergence_ratio = 1.50
>   industry_divergence_ratio  = 1.50
>   high_dependence_share      = 0.60   (استفاده‌نشده — D2)
>
> RISK_THRESHOLDS:
>   extreme_confidence         = 40.0
>   high_scenario_dispersion   = 0.50
>   high_bear_downside         = -30.0
>   medium_confidence          = 60.0
>   medium_bear_downside       = -15.0
> ```
>
> این **رفتار پیاده‌سازی** است، نه سیاست تأییدشده توسط مشخصات. بخش‌های ۴۱ تا ۵۳ هیچ مقدار تریگری را تعیین نمی‌کنند. آیا این اعداد در مشخصات تأیید (ratify) شوند یا به‌عنوان «مقادیر انتخاب‌شده توسط موتور بدون پشتوانه مشخصاتی» حاشیه‌نویسی شوند، خود یک تصمیم باز است (D9) — این سند هیچ عددی را تأیید یا تغییر نمی‌دهد. آزمون‌های boundary، رفتار فعلی را pin می‌کنند، نه انطباق با مشخصات را.

---

# 49. Required Alert Categories

Stage 7 باید قابلیت تولید Alert برای موارد زیر را داشته باشد:

```text
HIGH_IMPACT_HIGH_UNCERTAINTY
HIGH_SCENARIO_DISPERSION
LOW_FORECAST_RELIABILITY
VALUATION_BENCHMARK_DIVERGENCE
ASSESSMENT_FLIP_RISK
HIGH_MULTIPLE_DEPENDENCE
HIGH_EPS_DEPENDENCE
MARGIN_ASSUMPTION_RISK
INSUFFICIENT_PEER_DATA
POOR_DATA_QUALITY
NEGATIVE_EPS
SIGN_CHANGE
POINT_IN_TIME_WARNING
```

> **V1 Implementation-Status Annotation (factual — بدون تغییر نام، بدون ادغام، بدون تصمیم)**
>
> این فهرست الزامات نام‌گذاری را حفظ می‌کند. جدول زیر فقط وضعیت فعلی موتور را ثبت می‌کند و هیچ تصمیمی نمی‌گیرد.
>
> | نام الزامی (این سند) | وضعیت در V1 | توضیح مستند |
> |---|---|---|
> | `HIGH_SCENARIO_DISPERSION` | **IMPLEMENTED** | به‌صورت severity-bearing از `_alerts` صادر می‌شود (`WARNING:HIGH_SCENARIO_DISPERSION`) و هم در flag channel. |
> | `LOW_FORECAST_RELIABILITY` | **IMPLEMENTED** | به‌صورت severity-bearing از `_alerts` صادر می‌شود (`WARNING:LOW_FORECAST_RELIABILITY`) و هم در flag channel. |
> | `INSUFFICIENT_PEER_DATA` | **FLAG-LEVEL ONLY** | فقط در `valuation_risk_flags` صادر می‌شود (`calculate_valuation` در `engine.py`، شاخهٔ `INSUFFICIENT_PEER_DATA`)، نه به‌عنوان severity-bearing alert. آیا این برای «قابلیت Alert» کافی است، بخشی از تصمیم D8 است. |
> | `NEGATIVE_EPS` | **FLAG-LEVEL ONLY** | فقط از `_eps_flags` در flag channel. |
> | `SIGN_CHANGE` | **FLAG-LEVEL ONLY** | فقط از `_scenario_sign_change_flags` در flag channel. |
> | `VALUATION_BENCHMARK_DIVERGENCE` | **NAME MISMATCH** | نامی که موتور صادر می‌کند `WATCH:VALUATION_ABOVE_TARGET_PE` / `WATCH:VALUATION_BELOW_TARGET_PE` است. عدم تطابق در بخش ۵۴ ثبت شده. |
> | `HISTORICAL_VALUATION_DIVERGENCE` | **NAME MISMATCH** | نامی که موتور صادر می‌کند `WATCH:FORWARD_PE_ABOVE_HISTORICAL` / `WATCH:FORWARD_PE_BELOW_HISTORICAL` است (بخش ۵۴). |
> | `INDUSTRY_VALUATION_DIVERGENCE` | **NAME MISMATCH** | نامی که موتور صادر می‌کند `WATCH:FORWARD_PE_ABOVE_INDUSTRY` / `WATCH:FORWARD_PE_BELOW_INDUSTRY` است (بخش ۵۵). |
> | `ASSESSMENT_FLIP_RISK` | **ABSENT** | صفر ارجاع در `src/valuation` — **D1 حل‌نشده**. |
> | `HIGH_MULTIPLE_DEPENDENCE` | **ABSENT** | صفر ارجاع در `src/valuation` — **D2 حل‌نشده**. |
> | `HIGH_EPS_DEPENDENCE` | **ABSENT** | صفر ارجاع در `src/valuation` — **D3 حل‌نشده**. |
> | `MARGIN_ASSUMPTION_RISK` | **ABSENT** | صفر ارجاع در `src/valuation` — **D4 حل‌نشده**. |
> | `HIGH_IMPACT_HIGH_UNCERTAINTY` | **ABSENT** | صفر ارجاع در `src/valuation` — **D5 حل‌نشده**. |
> | `POOR_DATA_QUALITY` | **ABSENT** | در مشخصات هیچ تعریف تریگری وجود ندارد و صفر ارجاع در کد. |
> | `POINT_IN_TIME_WARNING` | **ABSENT** | صفر ارجاع در کد؛ تریگر آن به تصمیم D7 گره خورده است. |
>
> **تفاوت مهم:** یک flag بدون Severity معادل یک severity-bearing Alert نیست. فهرست بالا این دو را به‌طور جداگانه نشان می‌دهد و هیچ تصمیمی درباره اینکه آیا flag-level کافی است یا خیر، نمی‌گیرد (D8).
>
> **تصمیم باز (D8):** انتخاب بین rename، alias، یا پذیرش نام‌های فعلی در مشخصات، و همچنین اینکه آیا emission در سطح flag برای قابلیت بخش ۴۹ کافی است، هنوز انجام نشده و در این سند اتخاذ نشده است.

> **V1 Policy Record — D8 (intended policy):** نام‌های خروجی موجود در کد در V1 حفظ می‌شوند؛ هیچ rename، alias یا ادغامی اعمال نشده و هیچ فیلد خروجی تغییر نکرده است. نام الزامی بخش ۴۹ معادل alert پیاده‌شده فرض نمی‌شود.
>
> **Verified in code — alertهای واقعاً صادرشده توسط `_alerts` و شرط تولید:**
>
> | Alert صادرشده | شرط تولید |
> |---|---|
> | `WARNING:HIGH_SCENARIO_DISPERSION` | `scenario_dispersion > ALERT_THRESHOLDS.high_scenario_dispersion` |
> | `WARNING:LOW_FORECAST_RELIABILITY` | `reliability < ALERT_THRESHOLDS.low_forecast_reliability` |
> | `CRITICAL:INSUFFICIENT_BENCHMARK_DATA` | `target_source == "INSUFFICIENT_DATA"` |
> | `WATCH:VALUATION_ABOVE_TARGET_PE` / `WATCH:VALUATION_BELOW_TARGET_PE` | `forward_pe / target_pe` (یا معکوس) در سناریوی Base ≥ `benchmark_divergence_ratio`، با `target_pe > 0` |
> | `WATCH:FORWARD_PE_ABOVE_HISTORICAL` / `WATCH:FORWARD_PE_BELOW_HISTORICAL` | نسبت Forward P/E سناریوی Base به Historical Median (یا معکوس) ≥ `historical_divergence_ratio`، با median > 0 |
> | `WATCH:FORWARD_PE_ABOVE_INDUSTRY` / `WATCH:FORWARD_PE_BELOW_INDUSTRY` | همان منطق نسبت با Industry Forward Median و `industry_divergence_ratio` |
> | `INFO:TOP_DRIVER:<driver>` | `valuation_driver_ranking` غیرخالی باشد |
>
> دو مورد `CRITICAL:INSUFFICIENT_BENCHMARK_DATA` و `INFO:TOP_DRIVER:<driver>` در فهرست الزامی بخش ۴۹ نیامده‌اند و تکلیفشان تعیین نشده است. flag بخش ۵۵ با نام `INDUSTRY_BENCHMARK_INSUFFICIENT` نیز جدا از alert `CRITICAL:INSUFFICIENT_BENCHMARK_DATA` صادر می‌شود. هر alert در `valuation_risk_flags` هم تکرار می‌شود (`flags.extend(alerts)`).
>
> **Compatibility:** فیلد خروجی در `schema.py` با نام `alerts` است در حالی که قرارداد بخش ۶۹ نام `valuation_alerts` را می‌آورد؛ سایر تفاوت‌های نام فیلد بخش ۶۹ در این مرحله بررسی نشده‌اند. در `src/decision/engine.py` (Stage 9) هیچ استفاده‌ای از `alerts`، `valuation_risk_flags`، `valuation_driver_ranking`، `driver_impact` یا `review_priority` دیده نشد. مصرف‌کنندگان بیرون از مخزن و گزارش‌های ذخیره‌شده بررسی نشده‌اند؛ هر rename باید پس از بررسی آن‌ها و با Migration صریح (§66–§67) انجام شود (F5).

---

# 50. Assessment Flip Risk

یکی از مهم‌ترین Alertهای Stage 7:

```text
ASSESSMENT_FLIP_RISK
```

اگر یک تغییر نسبتاً کوچک و منطقی در Assumption باعث شود:

```text
ATTRACTIVE
→
FAIR
```

یا:

```text
ATTRACTIVE
→
EXPENSIVE
```

سیستم باید این موضوع را برجسته کند.

این وضعیت نشان می‌دهد Valuation شکننده است.

> **V1 Policy Record — D1 (intended policy):** `ASSESSMENT_FLIP_RISK` در V1 صادر نمی‌شود تا تعریف Flip، اندازهٔ شوک‌ها، آستانه‌ها و Severity به‌صورت معتبر مشخص شوند. الزام این بخش حذف نشده و **Deferred beyond V1** و بخشی از F2 است. **Verified in code:** صفر ارجاع به این نام در `src/valuation` و `src/decision/engine.py`؛ `SENSITIVITY_PERTURBATION = 0.10` فقط به `_driver_analysis` می‌رسد و سیاست شوک Flip نیست. هیچ شوک یا آستانه‌ای در این سند ابداع نمی‌شود.

---

# 51. Multiple Dependence

اگر Fair Value بیش از حد به Target P/E وابسته باشد و نه رشد EPS:

```text
HIGH_MULTIPLE_DEPENDENCE
```

فعال می‌شود.

مثلاً:

```text
EPS تقریباً Stable
ولی
Bull Case فقط با P/E Expansion بسیار بالا ایجاد شده
```

باید Alert شود.

> **V1 Policy Record — D2 (intended policy):** معیار فعلی وابستگی به Target P/E به‌عنوان اندازه‌گیری معتبر پذیرفته نمی‌شود و `HIGH_MULTIPLE_DEPENDENCE` فعال نمی‌شود؛ آستانهٔ `0.60` بدون معیار معتبر به کار نمی‌رود (**Deferred beyond V1**). **Verified in code:** صفر ارجاع به alert؛ `ALERT_THRESHOLDS.high_dependence_share = 0.60` در رجیستری ثبت است ولی مصرف نمی‌شود (در `parameter_consumption.recorded_not_consumed_names` فهرست می‌شود). معیار موجود در `_driver_analysis` (اثر مطلق شوک نسبی یکسان `p` بر EPS و بر TARGET_PE روی `FV = EPS × target P/E`) ساختاراً برای دو عامل اثر یکسان می‌دهد؛ probe روی کپی مرجع (نه pytest) برای ۶ پیکربندی ورودی `driver_impact = {EPS: 50, TARGET_PE: 50}` داد.

---

# 52. EPS / Forecast Dependence

اگر Valuation عمدتاً به Forecast EPS حساس باشد:

```text
HIGH_EPS_DEPENDENCE
```

فعال می‌شود.

اگر هم‌زمان Forecast Reliability پایین باشد، Severity می‌تواند افزایش پیدا کند.

> **V1 Policy Record — D3 (intended policy):** `HIGH_EPS_DEPENDENCE` بدون تعریف معتبر اضافه نمی‌شود (**Deferred beyond V1**). EPS ورودی از Stage 5 حفظ می‌شود و Stage 7 آن را بازمحاسبه نمی‌کند و داده‌ای به آن نمی‌افزاید. **Verified in code:** صفر ارجاع به `HIGH_EPS_DEPENDENCE` و `FORECAST_RISK`؛ EPS هر سناریو مستقیماً از `forecast_result.scenario_forecasts` خوانده می‌شود؛ Stage 7 هیچ revision-evidence تولید نمی‌کند (§83) و قاعدهٔ اتصال جدیدی برای مسیر تغییرات پیش‌بینی تعریف نشده است.

---

# 53. Margin Assumption Risk

اگر Fair Value به شدت وابسته به Operating Margin یا Net Margin Forecast باشد:

```text
MARGIN_ASSUMPTION_RISK
```

ثبت می‌شود.

> **V1 Policy Record — D4 (intended policy):** `MARGIN_ASSUMPTION_RISK` تا وجود ورودی‌های معتبر و تاریخ‌دار درآمد، هزینه و حاشیهٔ سود پیاده‌سازی نمی‌شود (**Deferred beyond V1**). نبود ورودی با مقدار ساختگی یا تخمین پنهان جبران نمی‌شود. **Verified in code:** صفر ارجاع؛ امضای `calculate_valuation` هیچ ورودی revenue/cost/margin ندارد.

---

# 54. Historical Divergence Alert

اگر Current/Forward P/E فاصله قابل توجهی با Historical Median P/E داشته باشد:

```text
HISTORICAL_VALUATION_DIVERGENCE
```

قابل تولید است.

این Alert به خودی خود Cheap/Expensive Signal قطعی نیست.

> **V1 Name Mapping (factual — بدون rename، بدون alias، بدون تغییر contract)**
>
> | نام الزامی این سند | نامی که موتور فعلی صادر می‌کند | کانال | تمایز بالا/پایین حفظ شده؟ |
> |---|---|---|---|
> | `HISTORICAL_VALUATION_DIVERGENCE` | `WATCH:FORWARD_PE_ABOVE_HISTORICAL` | severity-bearing alert | بله — بالا مجزا از پایین |
> | `HISTORICAL_VALUATION_DIVERGENCE` | `WATCH:FORWARD_PE_BELOW_HISTORICAL` | severity-bearing alert | بله — پایین مجزا از بالا |
>
> **تصمیم باز (D8):** آیا spec نام‌های فعلی را می‌پذیرد، یا rename یا alias معرفی می‌شود، هنوز اتخاذ نشده است. این سند فقط عدم تطابق را ثبت می‌کند و خروجی‌های مصرف‌کننده را تغییر نمی‌دهد.

---

# 55. Industry Divergence Alert

اگر Forward P/E شرکت فاصله قابل توجهی با Industry Forward P/E داشته باشد:

```text
INDUSTRY_VALUATION_DIVERGENCE
```

ایجاد می‌شود.

علت Divergence باید قابل بررسی باشد.

> **V1 Name Mapping (factual — بدون rename، بدون alias، بدون تغییر contract)**
>
> | نام الزامی این سند | نامی که موتور فعلی صادر می‌کند | کانال | تمایز بالا/پایین حفظ شده؟ |
> |---|---|---|---|
> | `INDUSTRY_VALUATION_DIVERGENCE` | `WATCH:FORWARD_PE_ABOVE_INDUSTRY` | severity-bearing alert | بله — بالا مجزا از پایین |
> | `INDUSTRY_VALUATION_DIVERGENCE` | `WATCH:FORWARD_PE_BELOW_INDUSTRY` | severity-bearing alert | بله — پایین مجزا از بالا |
>
> علاوه بر این، تریگر `INDUSTRY_BENCHMARK_INSUFFICIENT` (بخش ۱۰، «کمتر از ۸ Peer معتبر») در کد تحت **شرط متفاوتی** صادر می‌شود. موتور این flag را **صادر می‌کند**، اما تنها زمانی که `target_source == "INSUFFICIENT_DATA"` باشد — یعنی هیچ Industry Forward P/E با حداقل ۸ Peer معتبر، هیچ Historical Median معتبر و هیچ Industry TTM P/E معتبر در دسترس نباشد (`_select_target_pe` در `src/valuation/engine.py`).
>
> این شرط emission با شرط Peer Count بخش ۱۰ **معادل نیست**: با ۷ Peer معتبر ولی یک Historical Median معتبر، `target_source` برابر `HISTORICAL_MEDIAN_PE` می‌شود، در نتیجه `INDUSTRY_BENCHMARK_INSUFFICIENT` صادر **نمی‌شود** — حتی اگر یک benchmark جایگزین و قابل‌استفاده انتخاب شده باشد. بنابراین یک مورد «کمتر از ۸ Peer معتبر» می‌تواند یک benchmark قابل‌استفاده داشته باشد و باز هم این flag را دریافت نکند. تریگر کامل بخش ۱۰ (مبتنی بر Peer Count) در کد پیاده‌سازی نشده است.
>
> `INSUFFICIENT_PEER_DATA` یک سیگنال **مجزا** است و نباید با `INDUSTRY_BENCHMARK_INSUFFICIENT` یکی گرفته شود: اولی زمانی صادر می‌شود که `forward_values` موجود باشد و تعداد peerهای Forward معتبر کمتر از `MIN_INDUSTRY_PEERS = 8` باشد (`calculate_valuation` در `engine.py`) و صرفاً کمبود تعداد Peer را گزارش می‌کند، دومی صرفاً نبود هر گونه benchmark قابل‌استفاده را گزارش می‌کند. این دو flag هم می‌توانند هم‌زمان صادر شوند و هم می‌توانند مستقل از یکدیگر صادر شوند.
>
> **تصمیم باز (D8):** انتخاب rename / alias / پذیرش spec، هنوز اتخاذ نشده است.

---

# 56. Point-in-Time Requirement

تمام Historical Valuation و Backtestها باید Point-in-Time باشند.

در هر تاریخ:

```text
Price Date
Forecast Cutoff
Report Publication Date
Report Version
Historical EPS Availability
```

باید رعایت شوند.

استفاده از داده‌ای که بعداً منتشر شده برای تحلیل تاریخ گذشته ممنوع است.

> **V1 Policy Record — D7 (intended policy: disclosure of current limitations):** تا قابل‌اثبات‌شدن تاریخ مشاهده و زمان انتشار/دسترس‌پذیری ورودی‌ها، نباید ادعا شود که محاسبه فقط از اطلاعات موجود در تاریخ مبنا استفاده کرده است. ثبت `data_cutoff_datetime` به‌تنهایی کافی نیست.
>
> **Verified in code (V1 limitations):**
>
> * سری‌های benchmark (`historical_pe_values`، `industry_forward_pe_values`، `industry_ttm_pe_values`) floatهای بدون تاریخ‌اند؛ Price Date، Report Publication Date، Report Version و Historical EPS Availability آن‌ها به Stage 7 داده نمی‌شود (`test_p5_undated_benchmark_series_carry_no_provenance`).
> * `valuation_date` و `data_cutoff_datetime` فقط نرمالایز می‌شوند و ترتیبی بین آن‌ها اعمال نمی‌شود (`test_p6_cutoff_pit_limitation_pinned`).
> * تنها بررسی PIT اجراشده: اگر caller `forecast_input_refs` بدهد، `_reject_unverifiable_forecast_refs` مرجع بدون تاریخ یا با `available_at` بعد از cutoff را رد می‌کند. بدون ارسال refs هیچ بررسی‌ای اجرا نمی‌شود و `data_cutoff_datetime = None` مرجع تاریخ‌دار را می‌پذیرد.
> * `metadata["pit_inputs_required"] = True` فقط نشانگر اطلاعاتی است؛ `POINT_IN_TIME_WARNING` صادر نمی‌شود (صفر ارجاع).
> * انتخاب پارامتر در مسیر پیش‌فرض point-in-time نیست و cutoff در آن نقشی ندارد؛ رجیستری پیش‌فرض رکورد تاریخ‌دار ندارد (حاشیهٔ §65).
>
> **نتیجه:** هیچ خروجی Stage 7 نباید «محاسبهٔ اثبات‌شدهٔ PIT» معرفی شود. رفع این محدودیت برای استفادهٔ تولیدی یا بازآزمایی تاریخی قابل‌اتکا شرط لازم است (F3).

---

# 57. Restatement Rule

Historical valuation باید از ReportVersion صحیح استفاده کند.

Current Analysis:

```text
Latest Valid Version
```

Historical Backtest:

```text
Version actually available on that historical date
```

استفاده می‌شود.

---

# 58. Share Count Rule

EPS Forecast باید از Stage 5 دریافت شود که ShareCountHistory و CorporateAction را رعایت کرده است.

Stage 7 نباید مجدداً EPS را با Share Count جدید بازسازی کند مگر اینکه یک Validation Check انجام دهد.

---

# 59. Currency Rule

Valuation Equity Price و EPS باید از نظر Currency/Unit سازگار باشند.

اگر تحلیل USD نیز ارائه شود، Conversion باید مطابق Stage 1 قابل Trace باشد.

IRR داده پایه مالی است.

USD خروجی Derived است.

---

# 60. No Double Counting

Stage 7 باید اصول زیر را رعایت کند:

```text
Fundamental Score
≠ Target P/E multiplier

Trend
≠ direct P/E multiplier

Forecast Reliability
≠ P/E multiplier

Scenario Probability
≠ Scenario Dependency

Risk
≠ Confidence

Expected Fair Value
≠ replacement for Scenario Range
```

---

# 61. Data Quality

Stage 7 باید Data Quality inherited از Stageهای قبل را حفظ کند.

حالت‌های مهم:

```text
VALID
MISSING
ESTIMATED
RESTATED
SUSPICIOUS
UNMAPPED
INSUFFICIENT_DATA
```

SUSPICIOUS data نباید بدون Flag وارد valuation نهایی شود.

---

# 62. Valuation Data Quality

خروجی مستقل:

```text
valuation_data_quality
```

باید کیفیت کلی داده‌های استفاده‌شده در Valuation را نشان دهد.

---

# 63. Auditability

هر Fair Value باید قابل Trace باشد.

مثلاً:

```text
Fair Value
→ Target P/E
→ Benchmark
→ Industry / Historical Data

Fair Value
→ Forecast EPS
→ Forecast Version
→ Forecast Inputs
→ Financial Facts
→ ReportVersion
→ Publication Date
```

---

# 64. Model Versioning

هر تغییر در موارد زیر باید Model Version جدید ایجاد کند:

```text
Target P/E Method
Scenario Probability Method
Probability Priors
Valuation Thresholds
Confidence Formula
Risk Formula
Sensitivity Parameters
Alert Thresholds
Driver Priority Formula
```

نسخه قبلی overwrite نمی‌شود.

---

# 65. Parameter Versioning

تمام Thresholdهای قابل تنظیم باید بیرون از منطق Hard-Code شوند.

نمونه:

```text
valuation_model_parameters

model_version
parameter_name
parameter_value
effective_from
description
```

> **V1 Implementation Status (factual annotation — Documentation Reconciliation):**
>
> * `src/valuation/parameters.py` شامل `ParameterRecord` (name, value, `effective_from`, description)، `ParameterSetVersion` (با `effective_from` در سطح نسخه)، `ParameterRegistry` و `resolve_parameter_set_as_of` است. resolver فقط نسخه‌های تاریخ‌دار با `effective_from <= as_of` را می‌پذیرد؛ as-of تهی، نسخهٔ بدون تاریخ، ثبت‌نشده یا مبهم `LookupError` می‌دهد.
> * `DEFAULT_REGISTRY` فقط مجموعهٔ genesis (`STAGE7_V1/GENESIS`) را دارد و **خود نسخه و همهٔ رکوردها `effective_from = None`** هستند؛ تاریخ شروع اعتبار حدس زده نشده است. بنابراین as-of روی رجیستری پیش‌فرض همیشه خطا می‌دهد.
> * مسیر پیش‌فرض `calculate_valuation` (بدون `parameter_registry` و `parameter_as_of`) با ثابت‌های زندهٔ ماژول (genesis بدون تاریخ) محاسبه می‌کند و در `metadata["parameter_selection"]` با `mode = "FIXED_GENESIS_LEGACY"` و `point_in_time_selection_applied = False` برچسب می‌خورد؛ `data_cutoff_datetime` در انتخاب پارامتر نقشی ندارد (`data_cutoff_used_for_parameter_selection = False`).
> * انتخاب as-of فقط با ارسال صریح `parameter_registry` یا `parameter_as_of` فعال می‌شود. تاریخ حاکم بر انتخاب (cutoff، valuation_date یا مورد دیگر) توسط موتور استنباط نمی‌شود و ورودی caller است؛ تعیین آن همچنان تصمیم باز D9 است.
> * مقادیر مصرف‌شده از یک شیء immutable (`ConsumedParameters`) خوانده می‌شوند و `parameter_snapshot` از همان مقادیر ساخته می‌شود. پنج رکورد ثبت‌شده ولی مصرف‌نشده و چند literal هاردکد بیرون رجیستری (فرمول confidence، پیش‌فرض‌های score، وزن‌های uncertainty، rounding) در `metadata["parameter_consumption"]` فهرست شده‌اند.
> * `MODEL_VERSION = "STAGE7_V1"` رشتهٔ ثابت است؛ هیچ مکانیزمی تغییر آستانه را به افزایش model version گره نمی‌زند (الزام §64 اعمال‌شده نیست).
> * رفتار قطعی با ورودی و تنظیمات یکسان توسط آزمون‌های موجود pin شده است (از جمله `test_p35_repeated_as_of_calculations_are_deterministic` و digest طلایی P10).
>
> **V1 Policy Record — D9 (intended policy):** شناسهٔ نسخهٔ مدل و قرارداد فعلی حفظ می‌شود، اما معادل سابقهٔ کامل نسخه‌های تاریخی پارامترها نیست. **تاریخ شروع اعتبار پارامترهای قدیمی حدس زده نمی‌شود.** طراحی نسخه‌بندی تاریخی پس از روشن‌شدن قاعدهٔ تاریخ حاکم و منشأ پارامترها انجام می‌شود (**Deferred beyond V1**).
>
> **ادعای ممنوع در V1:** بازسازی نتایج تاریخی با پارامترهای نسخه‌بندی‌شده پشتیبانی نمی‌شود، چون رکورد تاریخ‌دار، provenance پارامتر، قاعدهٔ انتخاب تاریخ حاکم و بازسازی تاریخی وجود ندارد (F4).

---

# 66. Stage Contract Stability

اصل مهم معماری:

**Internal Logic may change; external Contract should remain stable whenever possible.**

اگر Stage 7 v2 الگوریتم Target P/E را تغییر دهد ولی خروجی‌های قراردادی همان باشند:

Stage 8 و Stage 9 نباید نیاز به طراحی مجدد داشته باشند.

---

# 67. Contract Versioning

اگر در آینده تغییر Contract اجتناب‌ناپذیر باشد:

```text
Valuation Contract v1
→
Valuation Contract v2
```

ایجاد می‌شود.

Stageهای مصرف‌کننده نباید silently شکسته شوند.

Migration باید Explicit باشد.

---

# 68. V1 Complexity Limits

در V1 استفاده از موارد زیر ضروری نیست:

```text
Neural Networks
Complex Machine Learning
Monte Carlo
Black-box Valuation
Large Regression Systems
Automatic Macro Prediction
Technical Analysis
```

مدل V1 باید:

```text
Transparent
Explainable
Auditable
Backtestable
Versionable
```

باشد.

---

# 69. Stage 7 Output Contract

حداقل Output Contract:

```text
company_id

valuation_date
current_price
market_price_date

bear_eps
base_eps
bull_eps

bear_forward_pe
base_forward_pe
bull_forward_pe

historical_ttm_pe
historical_median_pe

industry_forward_pe
industry_ttm_pe
industry_peer_count

target_pe_bear
target_pe_base
target_pe_bull
target_pe_source

fair_price_bear
fair_price_base
fair_price_bull

bear_probability
base_probability
bull_probability

probability_confidence

expected_fair_value
expected_upside

bear_upside_downside
base_upside_downside
bull_upside_downside

scenario_dispersion

forecast_reliability
valuation_confidence
valuation_risk
valuation_status

valuation_driver_ranking
driver_impact
driver_uncertainty
review_priority

valuation_alerts

valuation_data_quality

data_cutoff_datetime
valuation_timestamp
valuation_model_version
valuation_contract_version
```

---

# 70. Dashboard Minimum View

Dashboard نباید همه جزئیات Stage 7 را به‌صورت پیش‌فرض نشان دهد.

Decision Layer حداقل باید بتواند نمایش دهد:

```text
Current Price

Bear Fair Value
Base Fair Value
Bull Fair Value

Expected Fair Value
Expected Upside

Base Forward P/E
Target P/E

Historical Median P/E
Industry P/E

Forecast Reliability
Valuation Confidence
Valuation Risk
Valuation Status

Top Valuation Drivers
Critical Alerts
```

جزئیات بیشتر باید Drill-Down باشند.

---

# 71. Stress Test — Cheap Company

شرکت واقعاً ارزان با:

```text
Current Price << Fair Value
Positive EPS
Valid Benchmark
Adequate Reliability
```

باید:

```text
ATTRACTIVE
یا
VERY_ATTRACTIVE
```

شود.

PASS.

---

# 72. Stress Test — Low P/E / Poor Reliability

اگر:

```text
Forward P/E بسیار پایین
ولی
Forecast Reliability پایین
```

سیستم نباید صرفاً Very Attractive اعلام کند.

باید چیزی مانند:

```text
ATTRACTIVE
+
LOW CONFIDENCE
+
FORECAST RISK WARNING
```

امکان‌پذیر باشد.

PASS.

> **V1 Implementation Status (factual annotation — P24, per P23 audit):**
>
> ترکیب قابل‌دستیابی در V1 عبارت است از `ATTRACTIVE` به‌همراه `valuation_confidence` / `valuation_confidence_label` در سطح LOW یا VERY_LOW، به‌همراه flag تحت عنوان `LOW_FORECAST_RELIABILITY` و alert تحت عنوان `WARNING:LOW_FORECAST_RELIABILITY` (`calculate_valuation` و `_alerts` در `engine.py`). مقدار Reliability ورودی تابع `_valuation_status` نیست و Fair Value را تغییر نمی‌دهد. توکن تحت‌اللفظی `FORECAST RISK WARNING` / `FORECAST_RISK` هرگز صادر نمی‌شود (صفر ارجاع در کل `src` — رکوع بخش ۷۹). **تصمیم D3/D8 هنوز حل‌نشده است.** ادعای PASS بالا فقط برای ترکیب قابل‌دستیابی صادق است، نه برای توکن تحت‌اللفظی.

---

# 73. Stress Test — Negative EPS

```text
EPS < 0
```

نتیجه:

```text
Forward P/E = NULL
P/E Valuation = NOT_APPLICABLE
```

بدون Fair Price مصنوعی.

PASS.

---

# 74. Stress Test — Insufficient Industry Peers

```text
Valid Peers < 8
```

نتیجه:

```text
Industry Forward P/E = INSUFFICIENT_DATA
```

و Benchmark Hierarchy به Historical Median منتقل می‌شود.

PASS.

> **V1 Implementation Status (factual annotation — P24, per P23 audit):**
>
> رفتار fallback واقعی و تست‌شده به این صورت است: با کمتر از ۸ peer معتبر، بنچمارک industry-forward برای انتخاب **رد** می‌شود (`target_pe_source` به `HISTORICAL_MEDIAN_PE` می‌رود؛ `_select_target_pe` در `engine.py` و `MIN_INDUSTRY_PEERS = 8`) و flag تحت عنوان `INSUFFICIENT_PEER_DATA` صادر می‌شود (`calculate_valuation` در `engine.py`). در همین حالت، فیلد `industry_forward_pe_median` همچنان median مقادیر موجود را گزارش می‌کند (مثلاً با ۷ peer مقدار 6.0) — صرفاً برای انتخاب بنچمارک استفاده نمی‌شود. برچسب `INDUSTRY_FORWARD_PE = INSUFFICIENT_DATA` در متن بالا دقیق نیست و باید به سیگنال واقعی `INSUFFICIENT_PEER_DATA` ارجاع داده شود. flag تحت عنوان `INDUSTRY_BENCHMARK_INSUFFICIENT` تنها زمانی صادر می‌شود که `target_source == "INSUFFICIENT_DATA"` باشد (یعنی هیچ بنچمارک قابل‌استفاده‌ای موجود نباشد) و نباید با `INSUFFICIENT_PEER_DATA` یکی گرفته شود — همان تفکیک ثبت‌شده در اصلاحیه P21 بخش ۵۵.

---

# 75. Stress Test — Historical Divergence

Current Forward P/E فاصله زیادی با Historical Median دارد.

نتیجه:

```text
Historical Valuation Divergence Alert
```

PASS.

---

# 76. Stress Test — Scenario Probability

مثال:

```text
Bear = 20%
Base = 60%
Bull = 20%
```

مجموع:

```text
100%
```

Expected Fair Value باید Weighted Average صحیح باشد.

PASS.

---

# 77. Stress Test — Assessment Flip

تغییر کوچک Margin یا EPS:

```text
ATTRACTIVE → FAIR
```

نتیجه مورد انتظار:

```text
ASSESSMENT_FLIP_RISK
```

> **V1 Implementation Status (factual annotation):** **NOT IMPLEMENTED.**
>
> موتور فعلی Stage 7 هرگز `ASSESSMENT_FLIP_RISK` تولید نمی‌کند (صفر ارجاع در کل `src/valuation`). آزمون `test_p2_required_flip_dependence_alerts_missing` نشان می‌دهد که یک شوک ۱۰٪ در EPS، وضعیت را از `ATTRACTIVE` به `FAIR` تغییر می‌دهد بدون اینکه هیچ Alertای صادر شود.
>
> **تصمیم D1 (اندازه شوک، تعریف Flip، فرمول، Severity) هنوز حل‌نشده است.** ادعای PASS بالا نامعتبر است و تا زمان پیاده‌سازی یا تعویق صریح به V2، باید به‌عنوان الزام حل‌نشده در نظر گرفته شود.

> **Test contradiction (documented, unresolved — F2):** `test_p2_required_flip_dependence_alerts_missing` اجرای هر پنج نام `ASSESSMENT_FLIP_RISK`، `HIGH_MULTIPLE_DEPENDENCE`، `HIGH_EPS_DEPENDENCE`، `MARGIN_ASSUMPTION_RISK` و `HIGH_IMPACT_HIGH_UNCERTAINTY` را (در اتحاد خروجی چهار سناریو) الزامی می‌کند، در حالی که `test_p3_flip_dependence_alerts_remain_explicitly_unresolved` نبود همین پنج نام را برای خروجی `flip_base` assert می‌کند (با این مبنا که تا تعریف فرمول، نباید alert ابداع شود). این دو آزمون از نظر سیاست در تعارض‌اند و با سیاست پیشنهادی V1 (D1–D5: عدم صدور) فقط آزمون P3 هم‌راستاست. آزمون `test_p2_sector_driver_decomposition_missing` نیز وجود Driverهای `REVENUE`/`NII`/`NAV` را می‌طلبد که طبق D6 در V1 تولید نمی‌شوند. هیچ‌کدام در این مرحله تغییر، حذف، skip یا تضعیف نشدند؛ تطبیق باید در گام جدا و صریحاً بازبینی‌شده انجام شود و نباید الزام مشخصات را پنهان کند.

---

# 78. Stress Test — Multiple Risk

EPS Forecast پایدار است ولی Fair Value عمدتاً به افزایش Target P/E وابسته است.

نتیجه مورد انتظار:

```text
HIGH_MULTIPLE_DEPENDENCE
```

> **V1 Implementation Status (factual annotation):** **NOT IMPLEMENTED.**
>
> هیچ فرمول وابستگی به Multiple در مشخصات یا کد وجود ندارد. تعریف `high_dependence_share = 0.60` در `src/valuation/parameters.py` یک تعریف مرده است: تنها ارجاع در کل `src` همین خط است و به هیچ فرمول تولیدی متصل نیست (هیچ کدی این مقدار را نمی‌خواند).
>
> **تصمیم D2 (تعریف سهم وابستگی، نحوه استفاده از آستانه، Severity) هنوز حل‌نشده است.** ادعای PASS بالا نامعتبر است.

---

# 79. Stress Test — Forecast Risk

Target Multiple پایدار است ولی EPS Forecast بسیار نامطمئن است.

نتیجه مورد انتظار:

```text
HIGH_EPS_DEPENDENCE
یا
FORECAST_RISK
```

> **V1 Implementation Status (factual annotation):** **NOT IMPLEMENTED.**
>
> `HIGH_EPS_DEPENDENCE` هیچ‌گاه صادر نمی‌شود (صفر ارجاع در `src/valuation`)؛ هیچ فرمول سهم EPS، قانون تشدید Severity بر اساس Reliability، و قانون تقدم D2/D3 وجود ندارد.
>
> نام `FORECAST_RISK` در هیچ فایل تولیدی یا آزمونی تعریف نشده است (صفر ارجاع در کل `src`) و هیچ مصرف‌کننده‌ای ندارد. این سند نام `FORECAST_RISK` را تعریف نکرده و هیچ تصمیمی درباره حذف، نگه‌داشتن یا جایگزینی آن نمی‌گیرد — تعیین اینکه آیا این نام به‌عنوان جایگزین `HIGH_EPS_DEPENDENCE` مورد قبول است، بخشی از تصمیم D3/D8 است.
>
> **تصمیم D3 هنوز حل‌نشده است.** ادعای PASS بالا نامعتبر است.

---

# 80. Stress Test — Fundamental Score Double Counting

Fundamental Score بالا نباید مستقیماً Target P/E را افزایش دهد.

PASS.

---

# 81. Stress Test — Trend

```text
Strong Improvement
```

می‌تواند Scenario Probability را تغییر دهد، اما Target P/E را مستقیماً Scale نمی‌کند.

PASS.

> **V1 Implementation Status (factual annotation — P24, per P23 audit):**
>
> ممنوعیت scale مستقیم Target P/E برقرار است (ساختاری): امضای `calculate_valuation` (`calculate_valuation` در `engine.py`) هیچ ورودی trend ندارد. نیمه مثبت ادعا فقط از طریق کانال family-evidence صادق است — یک trend از نوع `Strong Improvement` در Stage 4 مستقیماً وارد مرز Stage 7 نمی‌شود و نمی‌تواند مستقیماً احتمال‌ها را جابه‌جا کند؛ ابتدا باید در بالادست (upstream) داخل family scoreها (بخش‌های ۲۳–۲۴، `probability_evidence`) تجمیع شود و سپس caller آن را به Stage 7 بدهد. **تصمیم D6 (در صورت ورود ورودی‌های sector/trend به مرز) هنوز حل‌نشده است.**

---

# 82. Stress Test — Probability Confidence

سیستم می‌تواند Probability عددی داشته باشد:

```text
20 / 60 / 20
```

ولی Evidence ضعیف باشد.

بنابراین:

```text
Probability Confidence = LOW
```

امکان‌پذیر است.

PASS.

---

# 83. Stress Test — Forecast Revision

```text
EPS Forecast
1100 → 1180 → 1270
```

می‌تواند Positive Revision Evidence ایجاد کند.

> **V1 Implementation Status (factual annotation — P24, per P23 audit):** **NOT PRODUCED IN STAGE 7 V1.**
>
> لایه Stage 7 در V1 هیچ خروجی revision-evidence تولید نمی‌کند: توکن `POSITIVE_FORECAST_REVISION` صفر ارجاع در کل `src` دارد. جهت revision در Stage 5 محاسبه می‌شود (`revision_trend` در `src/forecast/repo.py:137-148` با مقادیر `UPWARD` / `DOWNWARD` / `MIXED`) و در Stage 9 مصرف می‌شود (`src/decision/engine.py`)، اما هیچ‌چیز وارد `src/valuation` نمی‌شود. Stage 7 فقط family-level probability evidence دریافت می‌کند و هیچ توکن revision-evidence تولید نمی‌کند.
>
> **اینکه آیا revision evidence اصلاً باید به لایه valuation برسد — و اگر بله، از چه مسیری (تجمیع family-evidence توسط caller یا ورودی revision تاریخ‌دار جدید) و با چه نامی — یک سؤال سیاستی باز است (مرتبط با D3/D8 و الزام بخش ۲۶).** این سند deferral به V2 را اعلام نمی‌کند؛ تنها ثبت می‌کند که رفتار فوق در V1 پیاده‌سازی نشده است.

~~PASS.~~ → **وضعیت: در V1 صدق نمی‌کند — Stage 7 هیچ Positive Revision Evidence تولید نمی‌کند (مرتبط با D3/D8 حل‌نشده).**

---

# 84. Stress Test — Loss to Profit

```text
EPS:
-100 → +120
```

نباید Growth/P/E تاریخی گمراه‌کننده ایجاد کند.

Sign-change handling اعمال می‌شود.

PASS.

> **V1 Implementation Status (factual annotation — P24, per P23 audit):**
>
> عدم تولید growth/P/E گمراه‌کننده و flagهای sign-change واقعی و تست‌شده‌اند: EPS منفی → fpe/fv برابر None (مدل‌ها) و وضعیت `NOT_APPLICABLE` (`calculate_valuation` در `engine.py`). برچسب‌های `LOSS_TO_PROFIT` / `PROFIT_TO_LOSS` گذارهای علامت **بین‌سناریویی** هستند (نسبت به سناریوهای دیگر در همان اجرا؛ `_scenario_sign_change_flags` در `engine.py`)، نه برچسب‌های revision زمانی؛ خوانش `-100 → +120` با مجموعه flagها بازنمایی می‌شود، نه با یک سری زمانی.

---

# 85. Stress Test — Point-in-Time

> **V1 Implementation Status (factual annotation):** **NOT ACHIEVABLE IN V1 — این ادعای PASS برداشته شد.**
>
> مرز ورودی Stage 7 این آزمون را اجرا نمی‌کند. در `calculate_valuation` سری‌های بنچمارک (`historical_pe_values`، `industry_forward_pe_values`، `industry_ttm_pe_values`) به‌صورت floatهای ساده و بدون تاریخ وارد می‌شوند؛ هیچ مقایسه‌ای بین `valuation_date` و `data_cutoff_datetime` انجام نمی‌شود (این دو فقط نرمالایز و در خروجی بازنویسی می‌شوند)؛ و `metadata["pit_inputs_required"]` صرفاً یک نشانگر اطلاعاتی است، نه یک اعمال قانون.
>
> بنابراین Stage 7 در V1 **اصل publication/version provenance و انتخاب date-safe بنچمارک را اجرا نمی‌کند**. این یک محدودیت ثبت‌شده است، نه یک تأیید correctness.
>
> **تصمیم D7 (provenance هر مشاهده در برابر تأیید caller در برابر محدودیت ثبت‌شده) هنوز حل‌نشده است** — این سند مسئولیت caller را به‌عنوان سیاست تأییدشده معرفی نمی‌کند؛ تنها ثبت می‌کند که خود Stage 7 آن را اجرا نمی‌کند.

گزارشی که بعد از Valuation Date منتشر شده نباید وارد Historical Valuation شود.

~~PASS.~~ → **وضعیت: در V1 صدق نمی‌کند — مرز Stage 7 این قانون را اجرا نمی‌کند (D7 حل‌نشده).**

---

# 86. Final Architectural Principles

Stage 7 باید همیشه این اصول را حفظ کند:

```text
Forward-looking
Scenario-based
Point-in-Time
Industry-relative
Historically contextualized
Reliability-aware
Risk-aware
Explainable
Auditable
Versioned
Modular
Backtestable
```

---

# 87. Non-Negotiable Rules

موارد زیر در Stage 7 V1 غیرقابل نقض هستند:

1. Forward P/E محور اصلی Valuation است.
2. Bear/Base/Bull مستقل محاسبه می‌شوند.
3. Negative/Zero EPS نباید P/E مصنوعی ایجاد کند.
4. Historical Valuation باید Point-in-Time باشد.
5. Industry comparison فقط با Peerهای هم‌صنعت انجام می‌شود.
6. حداقل Industry Peer Count برابر 8 است.
7. Median بر Mean اولویت دارد.
8. Forward و TTM benchmark نباید مخلوط شوند.
9. Fundamental Score مستقیماً Target P/E را Scale نمی‌کند.
10. Trend مستقیماً Target P/E را Scale نمی‌کند.
11. Forecast Reliability مستقیماً P/E یا Fair Value را ضرب نمی‌کند.
12. Scenario Probability همیشه مجموعاً 100% است.
13. Probability و Dependency دو مفهوم مستقل هستند.
14. Expected Fair Value جای Scenario Range را نمی‌گیرد.
15. Valuation Status، Risk و Confidence مستقل هستند.
16. Alerts توصیه Buy/Sell نیستند.
17. Point-in-Time و Versioning اجباری هستند.
18. Old Model Versions overwrite نمی‌شوند.
19. تغییر منطق داخلی Stage تا حد ممکن نباید Contract Stage را بشکند.
20. تمام Thresholdهای قابل Calibration باید Model Version Parameters باشند.

> **V1 Implementation Status (factual annotation — Documentation Reconciliation):** قواعد ۴ و ۱۷ (Point-in-Time) و ۱۸ و ۲۰ (Versioning / Model Version Parameters) در V1 به‌طور کامل اعمال نمی‌شوند؛ نگاه کنید به حاشیه‌های §56 و §65 و فهرست Freeze blockers در ابتدای سند. این قواعد همچنان غیرقابل نقض و الزام‌آورند؛ حاشیه فقط شکاف پیاده‌سازی را ثبت می‌کند.

---

# 88. Final Status


> **Status Correction (Documentation Reconciliation):** بلوک «Final Status» زیر یک چک‌لیست زمان طراحی است و **حکم Freeze نیست**. عبارت «LOCKED» و ردیف‌های PASS/YES مشخص‌شده با خط‌خوردگی، با شواهد فعلی سازگار نبودند و اصلاح شدند. ردیف‌های اصلاح‌نشده در این مرحله دوباره ممیزی نشده‌اند. **Stage 7 FROZEN نیست؛ Freeze blockers F1–F6 در ابتدای سند باز هستند.**

~~**Stage 7 — Valuation Engine: LOCKED**~~

Architecture:
PASS

Point-in-Time:
~~PASS~~ → **NOT ACHIEVED in V1** (D7/F3)

Scenario Framework:
PASS

Forward P/E Framework:
PASS

Historical / Industry Benchmarking:
PASS

Probability Framework:
PASS

Risk / Confidence Separation:
PASS

Sensitivity Engine:
PASS

Alert Engine:
~~PASS~~ → **PARTIAL** (alertهای §49: ۵ مورد ABSENT، ۳ مورد NAME MISMATCH، ۳ مورد FLAG-LEVEL ONLY، `POOR_DATA_QUALITY` و `POINT_IN_TIME_WARNING` ABSENT)

Double-Counting Control:
PASS

Auditability:
~~PASS~~ → **PARTIAL** (provenance پارامتر موجود؛ provenance گزارش/نسخه/تاریخ انتشار در Stage 7 اعمال نمی‌شود)

Versioning:
~~PASS~~ → **PARTIAL** (D9/F4)

Modular Upgradeability:
PASS

Ready for implementation:
YES

Ready for Stage 8:
~~YES~~ → **NOT ASSERTED** — Freeze Gate عبور نکرده است
