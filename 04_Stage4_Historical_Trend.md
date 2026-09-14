# Stage 4 — Historical, Seasonal & Trend Engine

## Locked Specification

**Status:** DESIGNED → AUDITED → CORRECTED → SCENARIO TESTED → PASS → LOCKED

---

## 1. Objective

Stage 4 باید به این سؤال پاسخ دهد:

> «عملکرد بنیادی فعلی شرکت نسبت به تاریخچه خودش چگونه است و در چه جهتی حرکت می‌کند؟»

Stage 4 فقط **Context + Direction** تولید می‌کند.

Stage 4 نباید:

* Fundamental Score را تغییر دهد.
* KPI جدیدی به Stage 2 اضافه کند.
* قیمت، P/E یا Valuation را وارد کند.
* Forecast تولید کند.
* Market Signal تولید کند.
* یک Score مستقل برای Trend بسازد.

---

# 2. Position in Architecture

Stage 4 بعد از Fundamental Scoring قرار دارد:

```text
Stage 1 → Data Foundation
Stage 2 → KPI Specification
Stage 3 → Fundamental Scoring
Stage 4 → Historical / Seasonal / Trend
Stage 5 → Forecast
```

تفکیک مفهومی:

```text
Fundamental Score = Current Condition

Stage 4 = Historical Context + Direction
```

Stage 4 مستقل از Fundamental Score باقی می‌ماند.

---

# 3. Four Layers

Stage 4 دارای چهار لایه است:

1. Historical Comparison
2. Seasonal Analysis
3. Momentum / Trend
4. Context Flags

---

# 4. Historical Comparison

خروجی‌های اصلی:

* MoM
* QoQ
* YoY
* Same-Period Multi-Year
* Multi-Year Trend

## MoM

```text
MoM = Current Month / Previous Month - 1
```

## QoQ

```text
QoQ = Current Quarter / Previous Quarter - 1
```

## YoY

```text
YoY = Current Period / Same Period Previous Year - 1
```

## Same-Period Multi-Year

مقدار دوره فعلی با همان دوره در سال‌های گذشته مقایسه می‌شود.

مثلاً:

```text
Q2 1404
vs
Q2 1403
vs
Q2 1402
```

هدف، تشخیص رفتار ساختاری و الگوی تاریخی است.

## Multi-Year Trend

توصیف جهت ساختاری عملکرد در چند سال است.

این مورد یک KPI یا رأی مستقل نیست.

---

# 5. Seasonal Analysis

در V1 از مدل‌های پیچیده مانند:

* STL
* Fourier
* X13

استفاده نمی‌شود.

مدل ساده و Robust استفاده می‌شود.

## Seasonal Baseline

برای هر دوره:

```text
Seasonal Baseline =
Median(same period across historical years)
```

حداقل:

```text
3 valid historical observations
```

برای ساخت Seasonal Baseline رسمی لازم است.

اگر کمتر از 3 مشاهده معتبر وجود داشته باشد:

```text
Seasonal Baseline = INSUFFICIENT_DATA
```

اما سایر تحلیل‌های تاریخی همچنان می‌توانند اجرا شوند.

## Seasonal Surprise

```text
Seasonal Surprise =
Current Value / Seasonal Baseline - 1
```

اگر:

```text
Seasonal Baseline = 0
```

یا علامت Base و Current متفاوت باشد:

```text
Seasonal Surprise = NULL
```

و Context Flag مناسب ثبت شود:

* ZERO_BASE
* SIGN_CHANGE

Median بر Mean ترجیح دارد، زیرا در برابر Outlier مقاوم‌تر است.

Seasonal Baseline در V1 بر اساس تاریخچه خود شرکت است و Industry Adjustment ندارد.

---

# 6. Momentum / Trend

## 6.1 Flow Variables

برای متغیرهای Flow مانند:

* Revenue
* Operating Profit
* Net Profit
* Operating Cash Flow

### 3M Momentum

```text
3M Momentum =
Current 3M Sum / Previous 3M Sum - 1
```

### 6M Momentum

```text
6M Momentum =
Current 6M Sum / Previous 6M Sum - 1
```

### 12M Trend

تعریف نهایی و غیرقابل‌ابهام:

```text
12M Trend =
Current TTM /
TTM ending 12 months earlier
- 1
```

**توجه بسیار مهم:**

12M Trend نباید Current TTM را با TTM ماه قبل مقایسه کند.

مثلاً:

```text
Current TTM = TTM ending Aug-1404

Comparison TTM =
TTM ending Aug-1403
```

این مقایسه یک Trend واقعی 12 ماهه است.

---

# 7. Stock Variables

برای متغیرهای Stock مانند:

* Assets
* Equity
* Debt
* Loans
* Deposits

نباید مقادیر را Sum کرد.

فرمول‌ها:

```text
3M =
Current period-end value /
value 3 months earlier - 1
```

```text
6M =
Current period-end value /
value 6 months earlier - 1
```

```text
12M =
Current period-end value /
value 12 months earlier - 1
```

---

# 8. EPS

EPS نباید به‌صورت کورکورانه Sum شود.

مقایسه باید بر اساس Period Definition یکسان انجام شود.

برای Trend بلندمدت:

```text
TTM EPS Growth =
Current TTM EPS /
TTM EPS 12 months earlier
- 1
```

محاسبه EPS باید با Stage 1 هماهنگ باشد و موارد زیر را لحاظ کند:

* ShareCountHistory
* CorporateAction
* تغییر تعداد سهام

---

# 9. Sign Change

اگر Base:

```text
<= 0
```

باشد یا تغییر علامت رخ دهد، درصد رشد استاندارد نباید تولید شود.

مثال:

```text
-100 → +120
```

نباید به‌صورت یک درصد رشد گمراه‌کننده نمایش داده شود.

در عوض:

```text
Growth = NULL
Context = LOSS_TO_PROFIT
```

مثال دوم:

```text
+100 → -50
```

خروجی:

```text
Growth = NULL
Context = PROFIT_TO_LOSS
```

Context Flags:

* LOSS_TO_PROFIT
* PROFIT_TO_LOSS
* SIGN_CHANGE
* ZERO_BASE

---

# 10. Low Base

Low Base یک Context Flag است، نه Score.

مثلاً:

```text
100 → 500 = +400%
```

رشد +400% باید حفظ شود، اما اگر 100 مقدار غیرعادی پایینی بوده باشد:

```text
LOW_BASE = TRUE
```

نباید از رشد امتیاز کم یا زیاد شود.

## Robust Detection

حداقل 3 مشاهده تاریخی مشابه لازم است.

```text
Historical Median =
Median(comparable historical bases)
```

```text
MAD =
Median(
abs(Historical Value - Historical Median)
)
```

```text
Robust Z =
(Base Value - Historical Median) /
(1.4826 × MAD)
```

اگر:

```text
Robust Z <= -2.5
```

آنگاه:

```text
LOW_BASE = TRUE
```

اگر داده کافی وجود نداشته باشد:

```text
LOW_BASE = UNKNOWN
```

و نه False.

---

# 11. Relative Trend Strength

Trend State نباید با Threshold ثابت جهانی تعریف شود.

مثلاً نباید گفت:

```text
+10% = Strong
```

زیرا +10% برای یک شرکت ممکن است بسیار زیاد و برای شرکت دیگر عادی باشد.

بنابراین برای هر شرکت و هر Horizon:

```text
Current Momentum
```

با توزیع تاریخی Momentum همان شرکت و همان Horizon مقایسه می‌شود.

برای Formal Relative Strength حداقل:

```text
8 historical observations
```

لازم است.

بر اساس Percentile قدر مطلق Momentum:

```text
Percentile < 50
→ Weak

50 ≤ Percentile < 75
→ Normal

Percentile ≥ 75
→ Strong
```

این Strength، **Company-Relative** است.

Industry Trend می‌تواند به‌عنوان Context نمایش داده شود اما مبنای اصلی Trend State نیست.

---

# 12. Trend Direction

برای هر Horizon:

```text
Positive
Negative
Near / Weak
```

سپس سه Horizon:

* 3M
* 6M
* 12M

با هم ترکیب می‌شوند.

---

# 13. Final Trend State

## Strong Improvement

اگر:

```text
ALL valid horizons = Positive
```

و حداقل:

```text
2 horizons = Strong
```

آنگاه:

```text
Strong Improvement
```

## Improving

اگر اکثریت Horizonهای معتبر مثبت باشند ولی شرایط Strong Improvement برقرار نباشد:

```text
Improving
```

## Stable

اگر:

```text
ALL valid horizons = Weak
```

یا Majority Direction وجود نداشته باشد:

```text
Stable
```

## Deteriorating

اگر اکثریت Horizonهای معتبر منفی باشند ولی Strong Deterioration برقرار نباشد:

```text
Deteriorating
```

## Strong Deterioration

اگر:

```text
ALL valid horizons = Negative
```

و حداقل:

```text
2 horizons = Strong
```

آنگاه:

```text
Strong Deterioration
```

---

# 14. Missing Horizons

اگر فقط یک Horizon معتبر باشد:

```text
Trend State = INSUFFICIENT_DATA
```

اگر دو مورد از سه Horizon معتبر باشند:

```text
Trend State may be calculated
```

اما:

```text
Coverage / Confidence = LIMITED
```

Missing هرگز صفر در نظر گرفته نمی‌شود.

---

# 15. Tested Examples

### Scenario 1 — Strong Growth

```text
3M  = +15% Strong
6M  = +11% Strong
12M = +9% Normal
```

نتیجه:

```text
Strong Improvement
```

### Scenario 2 — Moderate Improvement

```text
3M  = +8%
6M  = +5%
12M = -2%
```

نتیجه:

```text
Improving
```

### Scenario 3 — Stable

```text
3M  = +1%
6M  = +1%
12M = +1%
```

نتیجه:

```text
Stable
```

### Scenario 4 — Gradual Deterioration

```text
3M  = -4%
6M  = -6%
12M = -7%
```

نتیجه:

```text
Deteriorating
```

### Scenario 5 — Severe Deterioration

```text
3M  = -16% Strong
6M  = -13% Strong
12M = -11% Normal
```

نتیجه:

```text
Strong Deterioration
```

### Scenario 6 — Mixed

```text
3M  = +15% Strong
6M  = -5% Normal
12M = +8% Strong
```

نتیجه:

```text
Improving
```

نه Strong Improvement، زیرا همه Horizonها مثبت نیستند.

### Scenario 7 — Two Valid Horizons

```text
3M  = +10%
6M  = +7%
12M = NULL
```

نتیجه:

```text
Improving
Coverage = LIMITED
```

### Scenario 8 — One Valid Horizon

```text
3M  = +10%
6M  = NULL
12M = NULL
```

نتیجه:

```text
INSUFFICIENT_DATA
```

---

# 16. Industry Context

Stage 4 می‌تواند Company Trend و Industry Trend را کنار هم نمایش دهد:

```text
Company Trend   = Improving
Industry Trend  = Deteriorating
```

اما Industry Trend:

* Score مستقل نیست.
* رأی اضافی نیست.
* Fundamental Score را تغییر نمی‌دهد.

---

# 17. Double Counting Prevention

این موارد نباید به‌عنوان چهار سیگنال مستقل شمرده شوند:

```text
YoY
TTM
12M Trend
Annual Growth
```

TTM یک روش Aggregation / Rolling Context است، نه KPI جدید.

12M Trend نیز یک مقایسه تاریخی مشخص است.

Stage 4 هیچ Vote جدیدی به Fundamental Score اضافه نمی‌کند.

---

# 18. Data Sufficiency

حداقل نیازها:

### 3M

دو Window قابل مقایسه.

### 6M

دو Window قابل مقایسه.

### 12M

دو TTM / 12M Observation قابل مقایسه.

### Seasonal Baseline

حداقل 3 مشاهده تاریخی مشابه.

### Relative Strength

حداقل 8 Observation تاریخی برای همان Horizon.

### Trend State

حداقل 2 Horizon معتبر از 3 Horizon.

---

# 19. Stage 4 Output Contract

خروجی Stage 4 باید حداقل شامل موارد زیر باشد:

### Historical

* MoM
* QoQ
* YoY
* Same-Period Multi-Year
* Multi-Year Trend

### Seasonal

* Seasonal Baseline
* Seasonal Surprise
* Seasonal Data Sufficiency

### Trend

* 3M Momentum
* 6M Momentum
* 12M Trend
* Trend Direction
* Relative Trend Strength
* Trend State

### Context

* Low Base
* Sign Change
* Zero Base
* One-Off / Abnormal Context، فقط در صورت تشخیص قابل‌اعتماد
* Data Quality
* Data Sufficiency
* Trend Coverage
* Trend Confidence

---

# 20. Non-Negotiable Rules

1. Missing ≠ Zero.
2. Stage 4 Fundamental Score را تغییر نمی‌دهد.
3. Stage 4 KPI جدید ایجاد نمی‌کند.
4. 12M Trend یعنی Current TTM در برابر TTM پایان‌یافته 12 ماه قبل.
5. Flow و Stock هرگز با یک منطق Aggregation یکسان محاسبه نمی‌شوند.
6. EPS باید با ShareCountHistory و CorporateAction سازگار باشد.
7. Sign Change نباید با درصد رشد معمولی نمایش داده شود.
8. Low Base فقط Context است.
9. Relative Strength باید تا حد امکان Company-Relative باشد.
10. Thresholdهای ثابت جهانی برای Strong Trend ممنوع است.
11. TTM رأی مستقل نیست.
12. Industry Trend رأی مستقل نیست.
13. داده ناکافی باید صریحاً اعلام شود.
14. Stage 4 نباید Look-Ahead Bias ایجاد کند.
15. تمام محاسبات باید با Point-in-Time Data Model در Stage 1 سازگار باشند.
16. خروجی‌های Stage 4 باید قابل Audit و Reproduce باشند.

---

# 21. Final Status

**Stage 4 = LOCKED**

زنجیره فعلی:

```text
Stage 1 — LOCKED
Stage 2 — LOCKED
Stage 3 — LOCKED
Stage 4 — LOCKED
```

Stage 5 هنوز طراحی نشده است.

مرحله بعدی سیستم:

```text
Stage 5 — Forecast Engine
```

و Stage 5 باید بدون بازکردن معماری Stageهای 1 تا 4 طراحی شود، مگر اینکه یک تناقض واقعی و اثبات‌شده معماری کشف شود.
