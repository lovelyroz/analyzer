# Stage 5 — Forecast Engine

## Locked Specification

**Status:** DESIGNED → REVIEWED → STRESS TESTED → PASS → LOCKED

---

## 1. Purpose

Stage 5 وظیفه دارد بر اساس داده‌های مالی، وضعیت بنیادی، تاریخچه، فصل‌مندی، روند و محرک‌های معتبر، **عملکرد مالی آینده شرکت را Forecast کند**.

Stage 5 باید پاسخ دهد:

> «با توجه به وضعیت فعلی و مسیر حرکت شرکت، نتایج مالی محتمل آینده چیست؟»

Stage 5 یک Forecast Engine است و نباید وظایف Stage 3، Stage 4، Stage 6 یا Stage 7 را انجام دهد.

---

# 2. Position in System Architecture

```text
Stage 1
Data Foundation
      ↓
Stage 2
KPI Specification
      ↓
Stage 3
Fundamental Scoring
"Current Fundamental Quality"
      ↓
Stage 4
Historical / Seasonal / Trend
"Historical Context + Direction"
      ↓
Stage 5
Forecast Engine
"Future Financial Outcomes"
      ↓
Stage 6
Forecast Evaluation & Calibration
"Forecast Accuracy & Reliability"
      ↓
Stage 7
Valuation
```

Stage 3، Stage 4 و Stage 5 کاملاً در امتداد یکدیگر هستند اما وظایفشان متفاوت است:

* Stage 3 = وضعیت بنیادی فعلی
* Stage 4 = تاریخچه، فصل‌مندی و جهت حرکت
* Stage 5 = پیش‌بینی آینده
* Stage 6 = ارزیابی صحت پیش‌بینی

---

# 3. Non-Negotiable Separation Rules

Stage 5:

* Fundamental Score جدید تولید نمی‌کند.
* KPI جدید ایجاد نمی‌کند.
* Market Signal ایجاد نمی‌کند.
* Valuation انجام نمی‌دهد.
* P/E یا P/NAV محاسبه نمی‌کند.
* Technical Analysis انجام نمی‌دهد.
* Forecast Reliability نهایی تولید نمی‌کند.
* Stage 4 را دوباره محاسبه نمی‌کند.
* Stage 3 را دوباره محاسبه نمی‌کند.
* از Fundamental Score به‌عنوان یک ضریب مستقیم Forecast استفاده نمی‌کند.

Fundamental Score فقط می‌تواند **Context** باشد.

---

# 4. Industry Architecture

برای جلوگیری از پیچیدگی، V1 فقط دو خانواده Forecast دارد.

```text
                  STAGE 5
                     │
          ┌──────────┴──────────┐
          │                     │
     NON-FINANCIAL          FINANCIAL
          │                     │
     5 Industries          2 Industries
          │                     │
     ONE COMMON CORE       SPECIALIZED CORE
```

## Category A — Non-Financial

یک Core مشترک برای:

1. Petrochemical / Chemical
2. Metals / Mining
3. Cement
4. Food
5. Pharmaceutical

هیچ Forecast Engine جداگانه‌ای برای هر یک از این پنج صنعت در V1 ایجاد نمی‌شود.

## Category B — Financial / Investment

شامل:

1. Bank
2. Investment / Holding

این دو از منطق تخصصی مالی استفاده می‌کنند، اما همچنان در چارچوب یک معماری مشترک Stage 5 قرار دارند.

---

# 5. Non-Financial Forecast Core

Core اصلی:

```text
Revenue
   ↓
Operating Margin
   ↓
Operating Profit
   ↓
Net Profit
   ↓
EPS
   ↓
ROE
```

---

# 6. Revenue Forecast

Revenue Forecast از این سلسله‌مراتب استفاده می‌کند:

```text
1. Historical / Seasonal Baseline
2. Recent Run Rate
3. Driver-Based Adjustment
```

اگر Driver معتبر و قابل اتکا وجود داشته باشد، می‌تواند Forecast را اصلاح کند.

نمونه Driverها:

* Sales Volume
* Selling Price
* سایر محرک‌های رسمی و قابل اندازه‌گیری شرکت

Driverها در Stage 2 KPI جدید محسوب نمی‌شوند.

اگر Driver داده کافی نداشته باشد:

> Driver حذف می‌شود؛ مقدار ساختگی ایجاد نمی‌شود.

---

# 7. Operating Margin Forecast

Operating Margin:

```text
Operating Margin
=
Operating Profit / Revenue
```

سپس:

```text
Forecast Operating Profit
=
Forecast Revenue × Forecast Operating Margin
```

Margin باید به‌صورت مستقل از Revenue قابل تغییر باشد.

بنابراین مدل می‌تواند شرایطی مانند:

```text
Revenue ↑
Margin ↓
Operating Profit ↓
```

را تشخیص دهد.

---

# 8. Net Profit Forecast

اولویت محاسبه:

```text
1. Component-Based Forecast
        ↓
2. Operating Profit × Historical Net/Operating Conversion
        ↓
3. Revenue × Net Margin
        ↓
4. INSUFFICIENT_DATA
```

روش Component-Based می‌تواند شامل موارد زیر باشد:

```text
Operating Profit
± Non-Operating Items
- Financial Costs
- Tax
=
Net Profit
```

فقط اجزایی که داده کافی و قابل اتکا دارند وارد محاسبه می‌شوند.

اگر داده برای یک جزء وجود نداشته باشد، سیستم نباید عدد ساختگی ایجاد کند.

---

# 9. EPS Forecast

EPS مستقیماً Forecast نمی‌شود.

فرمول:

```text
Forecast EPS
=
Forecast Net Profit Attributable to Common Shareholders
/
Forecast Weighted Average Shares
```

تعداد سهام باید با استفاده از:

* ShareCountHistory
* CorporateAction

محاسبه شود.

افزایش سرمایه، کاهش سرمایه، Split یا سایر تغییرات مرتبط با تعداد سهام باید در EPS لحاظ شود.

---

# 10. ROE Forecast

در صورت وجود داده کافی:

```text
ROE
=
Forecast Net Profit
/
Average Equity
```

و:

```text
Average Equity
=
(Beginning Equity + Ending Equity) / 2
```

اگر Equity Forecast قابل اتکا نباشد:

```text
ROE = INSUFFICIENT_DATA
```

نباید مقدار ساختگی ایجاد شود.

---

# 11. Financial Forecast Core — Bank

ساختار اصلی بانک:

```text
Loans / Deposits
       ↓
NII / NIM
       ↓
Net Profit
       ↓
EPS
       ↓
ROE
```

Stage 5 می‌تواند از موارد زیر به‌عنوان Driver استفاده کند:

* Loan Growth
* Deposit Growth
* NIM
* NII
* Credit Quality / NPL Context

اما Driver نباید بدون مدل یا داده معتبر به ضریب دلخواه تبدیل شود.

NPL در صورت نبود رابطه معتبر و داده کافی، به‌عنوان Context باقی می‌ماند و نباید یک ضریب مصنوعی روی سود اعمال شود.

---

# 12. Financial / Investment Forecast Core — Holding

ساختار اصلی:

```text
NAV
 ↓
NAV Growth
 ↓
Net Profit
 ↓
EPS
 ↓
ROE
```

P/NAV در Stage 5 وارد Forecast نمی‌شود.

P/NAV متعلق به Stage 7 — Valuation Engine است.

---

# 13. Baseline Forecast Architecture

Stage 5 سه نوع Baseline را حفظ می‌کند:

### A. Recent Run Rate

بر اساس عملکرد اخیر.

### B. Historical / Seasonal Baseline

بر اساس تاریخچه و Seasonality شرکت.

### C. Seasonal Naive

به‌عنوان Baseline ساده و Benchmark.

این سه روش الزاماً با یکدیگر ترکیب نمی‌شوند.

---

# 14. Baseline Selection Rule

اگر Seasonality معتبر و داده کافی وجود داشته باشد:

```text
Historical / Seasonal Baseline
```

اولویت دارد.

اگر Seasonality کافی نباشد:

```text
Recent Run Rate
```

استفاده می‌شود.

Seasonal Naive به‌عنوان Benchmark حفظ می‌شود.

انتخاب بهترین مدل در طول زمان، در Stage 6 با مقایسه Forecast و Actual ارزیابی خواهد شد.

---

# 15. Stage 4 Integration

Stage 5 از خروجی‌های Stage 4 استفاده می‌کند:

* Historical Comparison
* Seasonal Baseline
* Seasonal Surprise
* 3M Momentum
* 6M Momentum
* 12M Trend
* Trend Direction
* Trend State
* Relative Strength
* Low Base
* Sign Change
* Data Sufficiency

Stage 5 این موارد را دوباره محاسبه نمی‌کند.

---

# 16. Trend Integration Rule

Trend و Momentum می‌توانند باعث Forecast Adjustment شوند، اما Stage 4 مستقیماً Forecast تولید نمی‌کند.

غلط:

```text
Momentum = +10%
→ Forecast Growth = +10%
```

صحیح:

```text
Stage 4 Trend Evidence
        ↓
Forecast Adjustment
        ↓
Stage 5 Forecast
```

Adjustment باید:

* محدود
* قابل توضیح
* قابل ثبت
* قابل Backtest

باشد.

محدوده Adjustment باید به‌صورت Model Parameter ذخیره شود و عدد ثابت و غیرقابل تغییر معماری نباشد.

Stage 6 می‌تواند در آینده بر اساس خطای Forecast این پارامترها را Calibration کند.

---

# 17. Forecast Hierarchy

Stage 5 از ساده‌ترین روش قابل اتکا شروع می‌کند:

```text
Level 1
Baseline

      ↓

Level 2
Baseline + Seasonality / Trend

      ↓

Level 3
Driver-Based Fundamental Forecast
```

اگر داده برای Level 3 کافی نباشد، به Level 2 برمی‌گردد.

اگر Level 2 نیز قابل استفاده نباشد، Level 1 استفاده می‌شود.

کمبود داده نباید الزاماً کل Forecast را متوقف کند.

بلکه:

```text
Less Data
   ↓
Simpler Model
   ↓
Lower Forecast Quality
```

---

# 18. Low Base Control

اگر Stage 4:

```text
LOW_BASE = TRUE
```

را گزارش کند، Stage 5 نباید رشد تاریخی غیرعادی را به آینده به‌صورت مکانیکی extrapolate کند.

مثال:

```text
100 → 500
```

نباید به‌صورت خودکار منجر به Forecast مشابه برای دوره بعد شود.

Low Base یک Context / Control است، نه KPI و نه Score.

---

# 19. Sign Change Control

در شرایط:

```text
Loss → Profit
```

یا:

```text
Profit → Loss
```

Growth Rate معمولی نباید برای Forecast به‌صورت مکانیکی استفاده شود.

این تغییرات باید به‌عنوان تغییر وضعیت اقتصادی / Regime Change در نظر گرفته شوند.

Stage 4 Contextهایی مانند:

* LOSS_TO_PROFIT
* PROFIT_TO_LOSS
* SIGN_CHANGE
* ZERO_BASE

باید در Stage 5 مورد احترام قرار گیرند.

---

# 20. Bear / Base / Bull

Stage 5 سه سناریو تولید می‌کند:

```text
Bear
Base
Bull
```

## Base

بهترین برآورد مدل بر اساس:

* Baseline
* Seasonality
* Trend
* Fundamental Drivers

## Bear

سناریوی محافظه‌کارانه با فرض شرایط نامساعدتر و/یا عدم‌قطعیت بیشتر.

## Bull

سناریوی مساعدتر با فرض شرایط مطلوب‌تر.

سناریوها باید بر اساس Driver و Uncertainty ساخته شوند و نباید با درصدهای کاملاً دلخواه مانند ±20% تعریف شوند.

---

# 21. Scenario Ordering

برای خروجی‌هایی که ترتیب اقتصادی مشخص دارند:

```text
Bear ≤ Base ≤ Bull
```

باید برقرار باشد.

اگر ساختار اقتصادی خاصی باعث شود این ترتیب معنی نداشته باشد، سیستم نباید اعداد را مصنوعی مرتب کند؛ بلکه باید وضعیت را Flag کند.

---

# 22. Driver-Based Scenarios

در صورت وجود Driver معتبر، سناریوها می‌توانند از اختلاف در Driverها ساخته شوند.

مثال:

```text
              Bear       Base       Bull

Volume        Weak       Base       Strong
Price         Weak       Base       Strong
Margin        Lower      Base       Higher
Financial
Cost          Higher     Base       Lower
```

اما اگر Driver قابل اندازه‌گیری یا قابل اتکا نباشد:

> مقدار فرضی ساخته نمی‌شود.

در این حالت Scenario Range بر اساس Historical Dispersion و Model Uncertainty تعیین می‌شود.

---

# 23. Forecast Outputs

برای هر Forecast، خروجی‌های اصلی عبارت‌اند از:

* Revenue
* Operating Profit
* Operating Margin
* Net Profit
* EPS
* ROE

برای بانک و Holding، خروجی‌های تخصصی لازم نیز طبق Core مربوطه حفظ می‌شوند.

سناریوها:

```text
Bear
Base
Bull
```

افق‌های Forecast می‌توانند شامل:

```text
1M
3M
6M
12M
```

باشند، مشروط به کفایت داده.

---

# 24. Forecast Versioning

> **HISTORICAL / SUPERSEDED (by R-05 / Owner Decision / AMENDMENT-OA1.7)**  
> The former design required that no previous Forecast be overwritten and that every Forecast version be retained so that a Version History (and derived indicators such as Earnings Revision Trend) could be maintained inside the application database. That persistence model is **no longer active architecture**.

**Active architecture (R-05):**

- Stage 5 generates Forecast outputs **at runtime**.
- Forecast outputs (including Bear / Base / Bull scenarios) are **consumed at runtime** by downstream stages.
- The application database stores **only inputs and source data**. No Forecast output, Forecast version, scenario record, or output-dependent provenance may be persisted in application database tables.
- If a user wishes to retain a specific Forecast output, retention occurs solely through the UI’s explicit save functionality, **outside** the application’s database tables.
- No alternative history store, cache, or persistence mechanism is introduced by this specification.

Former illustrative sequence (August EPS = 1100 → September = 1180 → October = 1270) remains useful only as an example of successive runtime Forecasts; it does **not** authorize database version history or stored revision trends.

---

# 25. Point-in-Time Rule

Forecast فقط می‌تواند از اطلاعاتی استفاده کند که در زمان Forecast در دسترس بوده‌اند.

مثال:

اگر گزارش در:

```text
10 Mehr
```

منتشر شده باشد، Forecast مورخ:

```text
5 Mehr
```

حق استفاده از آن گزارش را ندارد.

این قانون برای جلوگیری از:

```text
Look-Ahead Bias
```

اجباری است.

---

# 26. Forecast Reliability Separation

Stage 5 مقدار نهایی:

```text
Forecast Reliability
```

را تعیین نمی‌کند.

Stage 5 may return **runtime** information required for downstream evaluation (for example, the Forecast outputs themselves, the forecast method used, and data-quality metadata). This information is produced and consumed at runtime.

Stage 5 does **not** persist Forecast outputs or analytical evaluation records in the application database (R-05).

Stage 6 performs the evaluation flow:

```text
Runtime Forecast
   ↓
Actual (source / input data)
   ↓
Error
   ↓
Accuracy / Bias
   ↓
Reliability
   ↓
Calibration
```

Forecast Quality (characteristics of the runtime Forecast produced by Stage 5) and Forecast Reliability (the evaluated reliability produced by Stage 6) remain two distinct concepts. No new persistence requirement is introduced for actuals, errors, reliability scores, or calibration outputs.

---

# 27. Data Quality

در صورت نبود داده کافی:

```text
INSUFFICIENT_DATA
```

استفاده می‌شود.

هیچ مقدار Missing نباید به‌صورت خودکار:

```text
0
```

تفسیر شود.

The Forecast method used and data-quality metadata may be returned as **runtime output** information (for example: Baseline, Seasonal, Trend Adjusted, Driver Based). This does **not** imply that analytical results must be stored in the application database.

---

# 28. Forecast Record (Runtime Output Contract)

> **Clarification:** The structure below is a **runtime Forecast result / output contract**. It is **not** a database record or persisted entity. Under R-05, these fields are produced and consumed at runtime; they are not written to application database tables.

هر Forecast runtime output باید حداقل شامل موارد زیر باشد:

```text
company_id
financial_period
forecast_horizon
forecast_timestamp
data_cutoff_datetime
model_version
scenario

revenue
operating_profit
operating_margin
net_profit
eps
roe

forecast_method
data_quality
assumptions
```

برای مدل‌های تخصصی Bank/Holding، خروجی‌های تخصصی مربوطه نیز به‌صورت runtime output حفظ می‌شوند (بدون persistence در DB برنامه).

---

# 29. Auditability and Provenance

Traceability requirements are preserved without persisting analytical outputs.

The active documentation distinguishes:

1. **Raw source data and input records** — governed by their existing source/input persistence contracts (Stage 1 and related input contracts). These remain persistable.
2. **Runtime Forecast outputs and their runtime provenance** — available while the Forecast result exists in memory / runtime; sufficient to identify the relevant inputs, financial facts, model version, and cutoff where those data are supplied to Stage 5.
3. **Output-dependent provenance records** — must **not** be persisted in the application database (R-05). Linking provenance permanently to a stored Forecast version/row is prohibited.

A runtime Forecast result should retain enough information to identify the inputs and financial facts used where available, for example:

```text
Runtime Forecast
   ↓
Model Version
   ↓
Inputs (references / facts available at runtime)
   ↓
Financial Facts
   ↓
Report Version / Publication Date (from source data)
```

Runtime traceability does **not** by itself prove full Point-in-Time correctness; full PIT claims require the temporal evidence defined by the applicable input contracts.

---

# 30. No Double Counting

Stage 5 نباید یک مفهوم را چند بار وارد Forecast کند.

خصوصاً:

* Fundamental Score نباید دوباره به‌عنوان KPI وارد شود.
* TTM نباید به‌عنوان رأی مستقل وارد شود.
* Trend و Momentum نباید چند بار یک اثر یکسان را اعمال کنند.
* Industry KPI نباید دوباره به‌عنوان Universal KPI وارد شود.

---

# 31. Complexity Control

V1 نباید شامل موارد زیر باشد:

* Forecast Engine جدا برای هر یک از 7 صنعت
* Machine Learning پیچیده
* Neural Network
* Monte Carlo
* ده‌ها مدل Regression
* Technical Analysis داخل Forecast
* External Data Dependency اجباری
* Driverهای متعدد بدون داده معتبر

مدل V1:

```text
Baseline
+
Trend / Seasonality
+
Fundamental Drivers
+
Scenario
```

است.

---

# 32. Stress-Test Results

Stage 5 با سناریوهای زیر تست شده و PASS شده است:

1. رشد عادی
2. Low Base
3. Loss → Profit
4. Profit → Loss
5. Revenue Growth + Margin Deterioration
6. افزایش سرمایه / تغییر تعداد سهام
7. Fundamental Score بالا + Trend منفی
8. Fundamental Score پایین + Trend مثبت
9. Missing Data
10. Missing Driver
11. Insufficient Seasonality
12. Bear / Base / Bull Ordering
13. Forecast Versioning — **HISTORICAL / SUPERSEDED** (former persistence / version-history behavior; not an active acceptance criterion under R-05)
14. Point-in-Time Cutoff
15. Bank Forecast
16. Holding Forecast

نتایج تست‌های فعال (به‌جز مورد 13 که به‌عنوان HISTORICAL / SUPERSEDED علامت‌گذاری شده):

**PASS**

The former Forecast Versioning stress-test claim described persistence and retention of version history. That behavior is superseded by R-05; the historical test result is retained only for audit trail and must not be read as proof of compliance with the active no-persistence architecture.

---

# 33. Final Stage 5 Logic

```text
                  STAGE 5
                     │
          ┌──────────┴──────────┐
          │                     │
     NON-FINANCIAL          FINANCIAL
          │                     │
     Common Core          Bank / Holding
          │                     │
          └──────────┬──────────┘
                     ▼
                  BASELINE
                     │
             Seasonality / Trend
                     │
             Fundamental Drivers
                     │
                     ▼
              Forecast Chain
                     │
              ┌──────┼──────┐
              ▼      ▼      ▼
            Bear    Base    Bull
                     │
                     ▼
          Runtime Forecast Output
                     │
                     ▼
                  Stage 6
```

(Active path produces Bear / Base / Bull as **runtime outputs** consumed by Stage 6. No database versioning or persistent Forecast store is part of the active architecture.)

---

# 34. Final Architectural Contract

Stage 5 باید:

* آینده را Forecast کند.
* از داده‌های Stage 1 استفاده کند.
* از تعریف‌های Stage 2 پیروی کند.
* وضعیت Stage 3 را به‌عنوان Context در نظر بگیرد.
* Trend و Seasonality Stage 4 را به‌عنوان Evidence استفاده کند.
* Forecast را به‌صورت زنجیره‌ای و سازگار تولید کند.
* برای 5 صنعت غیرمالی یک Core مشترک داشته باشد.
* برای Bank/Holding Core تخصصی داشته باشد.
* Bear/Base/Bull را به‌صورت **runtime outputs** تولید کند.
* Point-in-Time را رعایت کند.
* Missing Data را با Zero اشتباه نگیرد.
* از Low Base و Sign Change محافظت کند.
* Share Count و Corporate Actions را در EPS لحاظ کند.
* روش Forecast و کیفیت داده را به‌صورت runtime metadata بازگرداند.

**Active architecture (R-05):** The application database stores only inputs and source data. Stage 5 generates Forecast outputs at runtime; downstream stages consume those runtime outputs. Optional user retention of a selected output occurs only via UI save functionality outside application database tables. No analytical Forecast output or output-dependent provenance is persisted in the application database.

> **HISTORICAL / SUPERSEDED:** The former requirement to “preserve Forecast versions” / maintain Version History inside the application database is no longer part of the active contract.

Stage 5 نباید:

* Fundamental Score جدید بسازد.
* Valuation انجام دهد.
* Market Analysis انجام دهد.
* Reliability نهایی تعیین کند.
* برای هر صنعت یک Forecast Engine مستقل بسازد.
* بدون داده معتبر مقدار فرضی تولید کند.
* خروجی تحلیلی Forecast را در دیتابیس برنامه persist کند.
* از اطلاعات آینده استفاده کند.

---

## STATUS

**STAGE 5 = LOCKED**

Stages 1–5 اکنون:

```text
Stage 1  LOCKED
Stage 2  LOCKED
Stage 3  LOCKED
Stage 4  LOCKED
Stage 5  LOCKED
```

Stages 6–9 هنوز طراحی نشده‌اند.
