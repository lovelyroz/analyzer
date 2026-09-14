# Stage 6 — Forecast Evaluation & Calibration

## Locked Specification — V1

### 1. هدف Stage 6

هدف Stage 6 ارزیابی عینی عملکرد Forecast Engine در Stage 5 است.

Stage 6 باید مشخص کند:

1. Forecast در گذشته چقدر به Actual نزدیک بوده است.
2. آیا Forecast دارای خطای سیستماتیک یا Bias بوده است.
3. آیا Forecast Engine از یک Baseline ساده بهتر عمل کرده است.
4. میزان اطمینان به Forecast چقدر است.
5. آیا برای اصلاح Forecast، Calibration لازم است یا خیر.
6. آیا Calibration واقعاً عملکرد Model Version جدید را بهبود داده است.
7. Reliability Forecast چگونه باید در Valuation و به‌خصوص Forward P/E مورد استفاده قرار گیرد.

Stage 6 **Forecast جدید تولید نمی‌کند**.

---

# 2. جایگاه Stage 6 در معماری سیستم

```text
Stage 1 → Stage 2 → Stage 3 → Stage 4 → Stage 5 → Stage 6
Data      KPI       Current    History   Future    Accuracy
                    Quality    +Trend    Outcomes
```

Stage 6:

```text
Forecast
    ↓
Actual
    ↓
Forecast Error
    ↓
Accuracy + Bias
    ↓
Baseline Comparison
    ↓
Reliability
    ↓
Calibration
    ↓
New Model Version
    ↓
Out-of-Sample Evaluation
```

---

# 3. قوانین معماری غیرقابل مذاکره

1. Stage 6 Forecast جدید تولید نمی‌کند.
2. Stage 6 Fundamental Score جدید تولید نمی‌کند.
3. Stage 6 KPI جدید تعریف نمی‌کند.
4. Stage 6 Valuation جدید محاسبه نمی‌کند.
5. Stage 6 Market Signal تولید نمی‌کند.
6. Forecast Version قبلی هرگز overwrite نمی‌شود.
7. تمام Evaluationها Point-in-Time هستند.
8. Baseline نیز مشمول Point-in-Time است.
9. هیچ اطلاعاتی که بعد از Forecast Cutoff منتشر شده باشد نباید در ارزیابی Forecast یا Baseline آن Forecast استفاده شود.
10. Calibration باعث ایجاد Model Version جدید می‌شود.
11. Reliability مقدار Forward P/E را مستقیماً تغییر نمی‌دهد.
12. Reliability فقط میزان اعتماد به Forecast مورد استفاده در Valuation را مشخص می‌کند.
13. تمام پارامترهای Accuracy، Reliability و Calibration باید به Model Version متصل و قابل Versioning باشند.
14. Accuracy و Reliability یک مفهوم نیستند.
15. Bias و Accuracy یک مفهوم نیستند.
16. TTM به‌عنوان Observation مستقل و اضافی نباید باعث Double Counting شود.
17. Horizonهای مختلف نباید بدون تفکیک با یکدیگر ترکیب شوند.

---

# 4. Forecast → Actual Mapping

هر Forecast باید به Actual متناظر خودش متصل شود.

کلید مفهومی Evaluation:

```text
Company
+
Metric
+
Financial Period
+
Forecast Horizon
+
Model Version
+
Forecast Cutoff
        ↓
Corresponding Actual
```

Actual باید:

* مربوط به همان Metric باشد.
* همان تعریف Metric را داشته باشد.
* مربوط به Financial Period متناظر باشد.
* از ReportVersion معتبر انتخاب شود.
* Publication Date آن مشخص باشد.
* از اطلاعاتی استفاده نکند که در زمان Forecast در دسترس نبوده‌اند.

Actual صرفاً «آخرین عدد موجود در دیتابیس» نیست.

---

# 5. Point-in-Time Evaluation

برای هر Forecast:

```text
Forecast Data Cutoff
        ↓
Information Available At Cutoff
        ↓
Forecast
        ↓
Later Publication of Actual
        ↓
Actual
        ↓
Evaluation
```

در Backtest:

> فقط اطلاعاتی که در Forecast Cutoff در دسترس بوده‌اند مجاز به استفاده هستند.

این قانون شامل:

* Financial Facts
* ReportVersion
* FX
* Baseline Inputs
* Historical Data
* Seasonal Data
* سایر Inputs مورد استفاده در Evaluation

است.

---

# 6. Forecast Error

تعریف اصلی:

$$
Error = Actual - Forecast
$$

مثال:

```text
Forecast EPS = 1100
Actual EPS   = 1180

Error = +80
```

تفسیر:

* Error مثبت → Under-Forecast
* Error منفی → Over-Forecast

---

# 7. Percentage Error

برای Forecastهای دارای مخرج معتبر:

$$
Percentage\ Error =
\frac{Actual-Forecast}{|Forecast|}\times100
$$

علامت حفظ می‌شود.

مثلاً:

```text
Forecast = 1100
Actual   = 1180

Percentage Error = +7.27%
```

---

# 8. Absolute Percentage Error — APE

برای سنجش اندازه خطا:

$$
APE =
\frac{|Actual-Forecast|}{|Forecast|}\times100
$$

APE جهت خطا را حذف می‌کند.

بنابراین:

* APE پایین → Forecast دقیق‌تر
* APE بالا → Forecast ضعیف‌تر

---

# 9. MAPE

برای مجموعه Observationهای معتبر:

$$
MAPE = Mean(APE)
$$

MAPE معیار اصلی Accuracy در V1 است.

هرچه MAPE پایین‌تر باشد، Accuracy بالاتر است.

اما MAPE برای موارد زیر به‌صورت معمول محاسبه نمی‌شود:

```text
ZERO_BASE
LOSS_TO_PROFIT
PROFIT_TO_LOSS
SIGN_CHANGE
```

در این شرایط:

```text
MAPE = NULL
Status = Appropriate Regime / Data Status
```

---

# 10. Bias

Bias جهت سیستماتیک خطا را اندازه‌گیری می‌کند.

تعریف V1:

$$
Bias =
Mean\left(
\frac{Actual-Forecast}{|Forecast|}
\right)
$$

تفسیر:

* Bias مثبت → Under-Forecast Bias
* Bias منفی → Over-Forecast Bias
* Bias نزدیک صفر → شواهدی از Bias سیستماتیک وجود ندارد.

مثال:

```text
Errors:
+10%
+10%
+10%
+10%

Bias = +10%
```

---

# 11. تفاوت Accuracy و Bias

این دو معیار مستقل هستند.

مثال:

```text
MAPE = 10%
Bias = +10%
```

یعنی مدل نسبتاً دقیق است اما دائماً در یک جهت خطا می‌کند.

در مقابل:

```text
MAPE = 20%
Bias = 0%
```

یعنی مدل Bias سیستماتیک ندارد ولی Accuracy ضعیف است.

بنابراین:

```text
Accuracy ≠ Bias
```

---

# 12. Zero Base و Sign Change

در شرایط زیر Percentage Error، APE، MAPE و Percentage Bias عادی نباید به‌صورت گمراه‌کننده محاسبه شوند:

```text
Forecast = 0
Loss → Profit
Profit → Loss
Sign Change
```

در این شرایط باید وضعیت اختصاصی ثبت شود.

مثال:

```text
APE = NULL
Percentage Bias = NULL
Status = LOSS_TO_PROFIT
```

خطای Absolute می‌تواند همچنان نگهداری شود.

---

# 13. Forecast Horizons

Stage 6 همان Horizonهای Stage 5 را ارزیابی می‌کند:

```text
1M
3M
6M
12M
```

هر Horizon مستقل ارزیابی می‌شود.

نباید Observationهای Horizonهای مختلف بدون تفکیک با هم ترکیب شوند.

مثلاً:

```text
EPS / 1M
EPS / 3M
EPS / 6M
EPS / 12M
```

چهار مجموعه Evaluation مستقل هستند.

عملکرد خوب در 1M به‌صورت خودکار عملکرد خوب در 12M محسوب نمی‌شود.

---

# 14. Minimum Observation

فقط Observationهای معتبر و غیرتکراری وارد Evaluation می‌شوند.

طبقه‌بندی V1:

| Valid Observations | Status              |
| -----------------: | ------------------- |
|                < 5 | INSUFFICIENT_DATA   |
|                5–7 | LOW_CONFIDENCE      |
|               8–11 | MODERATE_CONFIDENCE |
|               ≥ 12 | ADEQUATE            |

Observation Count باید برای هر ترکیب زیر محاسبه شود:

```text
Company
+
Metric
+
Horizon
+
Model Version
```

---

# 15. Model Version Evaluation

Model Versionها باید جداگانه ارزیابی شوند.

مثلاً:

```text
EPS / 3M / Model V1
EPS / 3M / Model V2
```

نباید Observationهای V1 و V2 بدون تفکیک ترکیب شوند.

هر Model Version باید قابل Audit باشد.

---

# 16. Baseline

هدف Baseline این است که مشخص شود Forecast Engine واقعاً ارزش افزوده ایجاد کرده است یا خیر.

Baseline اصلی V1:

**Seasonal Naive**

Baseline باید:

* ساده باشد.
* شفاف باشد.
* قابل تکرار باشد.
* Point-in-Time باشد.
* از اطلاعات آینده استفاده نکند.

Baseline یک Benchmark است و Forecast Engine را به‌طور خودکار تغییر نمی‌دهد.

---

# 17. Baseline Comparison

Forecast Engine و Baseline با معیارهای قابل‌مقایسه ارزیابی می‌شوند:

```text
Forecast Engine
    ↓
MAPE + Bias

Baseline
    ↓
MAPE + Bias
```

بهبود نسبی:

$$
Improvement =
\frac{Baseline\ Error - Model\ Error}
{Baseline\ Error}
$$

مثال:

```text
Baseline MAPE = 12%
Model MAPE    = 9%

Improvement = 25%
```

اگر مقدار منفی باشد، Model از Baseline ضعیف‌تر بوده است.

---

# 18. Model Underperformance

اگر Forecast Engine به‌طور پایدار از Baseline ضعیف‌تر باشد:

```text
MODEL_UNDERPERFORMS_BASELINE
```

ثبت می‌شود.

پیچیده‌تر بودن Model دلیل کافی برای اعتماد بیشتر نیست.

اگر مدل پیچیده به‌صورت پایدار از Baseline ضعیف‌تر باشد، باید مورد بازبینی یا Revision قرار گیرد.

Stage 6 خودش Stage 5 را مستقیماً تغییر نمی‌دهد.

---

# 19. Forecast Reliability

Forecast Reliability امتیازی بین:

```text
0 – 100
```

است.

Reliability نشان می‌دهد:

> «چقدر می‌توان به Forecast فعلی اعتماد کرد؟»

Reliability با Accuracy یکی نیست.

---

# 20. Reliability Architecture

ساختار:

```text
Accuracy
+
Bias Control
+
Baseline Advantage
        ↓
Performance Score
        ↓
Confidence Adjustment
        ↓
Final Reliability 0–100
```

---

# 21. Performance Score

ساختار V1:

| Component          | Weight |
| ------------------ | -----: |
| Accuracy           |    50% |
| Bias Control       |    20% |
| Baseline Advantage |    30% |

بنابراین:

$$
PerformanceScore =
0.50(AccuracyScore)
+
0.20(BiasScore)
+
0.30(BaselineAdvantageScore)
$$

تمام اجزا در بازه 0–100 هستند.

---

# 22. Accuracy Score Parameters

MAPE باید به Accuracy Score تبدیل شود.

اما آستانه‌های دقیق تبدیل MAPE به Score نباید به‌عنوان حقیقت دائمی معماری Hard-Code شوند.

این پارامترها:

```text
Model Version Parameters
```

هستند و قابل Calibration هستند.

در نتیجه:

```text
MAPE
↓
Versioned Accuracy Mapping
↓
Accuracy Score
```

---

# 23. Bias Score

Bias Control بر اساس اندازه Bias سنجیده می‌شود:

$$
|Bias|
$$

هرچه:

```text
|Bias| ↓
```

باشد:

```text
Bias Score ↑
```

و برعکس.

جهت Bias همچنان جداگانه حفظ می‌شود.

مثلاً:

```text
Bias = +5%
```

و:

```text
Bias = -5%
```

از نظر Bias Control می‌توانند شدت مشابهی داشته باشند، اما Direction آنها متفاوت است.

---

# 24. Baseline Advantage Score

Baseline Advantage میزان برتری Forecast Engine نسبت به Baseline را اندازه‌گیری می‌کند.

مثلاً:

```text
Baseline MAPE = 12%
Model MAPE    = 9%
```

مدل 25٪ بهبود نسبی نسبت به Baseline دارد.

اگر Model از Baseline بدتر باشد، Advantage منفی خواهد بود.

---

# 25. Confidence Adjustment

Performance Score به‌تنهایی Reliability نیست.

تعداد Observation باید در Confidence لحاظ شود.

مثلاً:

```text
Performance Score = 90
Observations = 4
```

نباید به Reliability=90 منجر شود.

برای همین:

```text
Performance Score
        ↓
Observation Sufficiency
        ↓
Confidence Adjustment
        ↓
Final Reliability
```

---

# 26. Reliability Confidence Levels

طبقه‌بندی:

```text
<5
→ INSUFFICIENT_DATA

5–7
→ LOW_CONFIDENCE

8–11
→ MODERATE_CONFIDENCE

≥12
→ ADEQUATE
```

Performance عالی با Observation بسیار کم نباید باعث False Confidence شود.

Reliability نهایی باید تحت Confidence Adjustment قرار گیرد.

---

# 27. Reliability Parameters

تمام موارد زیر باید Versioned باشند:

* MAPE → Accuracy Score Mapping
* Bias → Bias Score Mapping
* Baseline Advantage Mapping
* Observation Confidence Parameters
* Reliability Calculation Parameters
* Calibration Parameters

بنابراین:

```text
Model V1
Model V2
...
```

می‌توانند پارامترهای متفاوت ولی کاملاً قابل Audit داشته باشند.

---

# 28. Calibration

Calibration زمانی استفاده می‌شود که Evaluation نشان دهد Forecast دارای Bias سیستماتیک و تکرارشونده است.

Calibration نباید بر اساس یک Observation منفرد انجام شود.

ساختار:

```text
Historical Evaluation
        ↓
Persistent Bias Detection
        ↓
Calibration Candidate
        ↓
Calibration Parameter
        ↓
New Model Version
```

---

# 29. Calibration States

سه وضعیت:

### NO_CALIBRATION

شواهد کافی برای اصلاح وجود ندارد.

### CALIBRATION_CANDIDATE

شواهدی از Bias وجود دارد اما برای اصلاح قطعی کافی نیست.

### CALIBRATED

Bias پایدار تأیید شده و اصلاح در Model Version جدید اعمال شده است.

---

# 30. Calibration Scope

Calibration باید تا حد امکان محدود و مشخص باشد.

مثلاً اگر:

```text
EPS / 6M
```

مشکل دارد، نباید بدون دلیل کل Forecast Engine تغییر کند.

Calibration باید در صورت امکان بر اساس:

```text
Metric
+
Horizon
+
Model Version
```

انجام شود.

---

# 31. Calibration نباید Forecast را مستقیماً دستکاری کند

این روش ممنوع است:

```text
Bias = +8%
↓
Forecast × 1.08
```

به‌صورت مستقیم و بدون ایجاد Version جدید.

روش صحیح:

```text
Model V1
↓
Evaluation
↓
Persistent Bias
↓
Calibration
↓
Model V2
↓
Future Forecasts
```

---

# 32. Out-of-Sample Calibration Evaluation

Calibration باید Out-of-Sample ارزیابی شود.

ساختار:

```text
Calibration Period
        ↓
Model V2
        ↓
Future / Holdout Period
        ↓
Actual
        ↓
Evaluation
```

اگر Model V2 بهتر شد:

```text
Calibration Improvement
```

اگر بدتر شد:

```text
Calibration Rejected / Revision Required
```

---

# 33. Baseline بعد از Calibration

Baseline همیشه باقی می‌ماند.

می‌توان عملکرد زیر را مقایسه کرد:

```text
Model V1
Model V2
Baseline
```

مثال:

```text
V1       MAPE = 12%
V2       MAPE = 8%
Baseline MAPE = 10%
```

V2 نسبت به V1 و Baseline بهتر است.

اما:

```text
V1       MAPE = 12%
V2       MAPE = 11%
Baseline MAPE = 8%
```

Calibration هنوز مدل را به سطح Baseline نرسانده است.

---

# 34. Overfitting Prevention

Calibration نباید باعث Overfitting شود.

ممنوع:

* اصلاح بر اساس یک Observation
* اصلاح بر اساس یک شرکت بدون شواهد کافی
* اصلاح صرفاً برای یک دوره خاص
* استفاده از اطلاعات آینده
* حذف Baseline
* Overwrite کردن Model Version قبلی

---

# 35. Reliability → Forward P/E

Reliability در Stage 7 برای سنجش اعتماد به Forecast EPS استفاده می‌شود.

اصل غیرقابل مذاکره:

> Reliability مقدار Forward P/E را مستقیماً تغییر نمی‌دهد.

مثلاً:

```text
Current Price = 12,000
Forecast EPS  = 1,500

Forward P/E = 8.0x
```

اگر:

```text
Reliability = 90
```

باشد:

```text
Forward P/E = 8.0x
High Forecast Confidence
```

و اگر:

```text
Reliability = 35
```

باشد:

```text
Forward P/E = 8.0x
Low Forecast Confidence
```

P/E همچنان 8x است.

---

# 36. ممنوعیت اصلاح مصنوعی P/E

این روش‌ها ممنوع هستند:

```text
Forward P/E × Reliability
Forward P/E × (100 / Reliability)
Forward P/E / Reliability
```

Reliability نباید به‌صورت مصنوعی P/E را ارزان‌تر یا گران‌تر کند.

---

# 37. Scenario + Reliability

Stage 5 دارای:

```text
Bear
Base
Bull
```

است.

بنابراین Stage 7 می‌تواند:

```text
Bear EPS → Bear Forward P/E
Base EPS → Base Forward P/E
Bull EPS → Bull Forward P/E
```

را محاسبه کند.

Reliability کنار این Forecastها قرار می‌گیرد.

مثلاً:

```text
Base Forward P/E = 6.1x
Forecast Reliability = 48/100
```

نتیجه:

```text
Forward P/E = 6.1x
Valuation Confidence = Low
```

---

# 38. Reliability تنها عامل Valuation Confidence نیست

در Stage 7 عوامل دیگری نیز می‌توانند وارد Valuation Confidence شوند:

* Forecast Reliability
* Scenario Dispersion
* Historical P/E
* Industry Valuation
* Point-in-Time Validity
* سایر شواهد Valuation که در Stage 7 تعریف خواهند شد.

بنابراین:

```text
Reliability
        +
Other Valuation Evidence
        ↓
Valuation Confidence
```

نه:

```text
Reliability
        ↓
Valuation Score
```

---

# 39. خروجی Evaluation

برای هر:

```text
Company
+
Metric
+
Horizon
+
Model Version
```

باید حداقل این اطلاعات قابل ثبت باشد:

```text
forecast_id
company_id
metric
financial_period
horizon
model_version
forecast_timestamp
data_cutoff_datetime
actual_period
actual_report_version
forecast_value
actual_value
absolute_error
percentage_error
ape
bias_component
evaluation_status
baseline_value
baseline_error
baseline_mape
model_mape
relative_baseline_improvement
observation_count
performance_score
confidence_level
reliability_score
calibration_status
calibration_version
evaluation_timestamp
```

نام فیلدها در Implementation قابل تغییر است، ولی مفهوم آنها نباید تغییر کند.

---

# 40. Auditability

هر Reliability باید قابل ردیابی باشد:

```text
Reliability
    ↓
Performance Score
    ↓
Accuracy / Bias / Baseline
    ↓
Evaluation Observations
    ↓
Forecast
    ↓
Model Version
    ↓
Inputs
    ↓
Financial Facts
    ↓
ReportVersion
    ↓
Publication Date
```

هیچ Reliability نباید بدون امکان بازسازی محاسبه تولید شود.

---

# 41. Data Quality

Observationهای دارای مشکلات جدی Data Quality نباید بدون کنترل وارد Evaluation شوند.

وضعیت‌هایی مانند:

```text
MISSING
ESTIMATED
SUSPICIOUS
UNMAPPED
RESTATED
```

باید طبق قواعد Data Foundation تفسیر شوند.

Actual نامعتبر نباید مانند Actual معتبر وارد MAPE و Bias شود.

---

# 42. No Double Counting

Stage 6 نباید:

* Fundamental Score را دوباره وارد Forecast Accuracy کند.
* TTM را چند بار به‌عنوان Observation حساب کند.
* Horizonهای مختلف را مخلوط کند.
* Trend را دوباره به‌عنوان KPI مستقل وارد Evaluation کند.
* Baseline را به Forecast Engine تبدیل کند.
* Reliability را به P/E مصنوعی تبدیل کند.

---

# 43. Stage 6 Final Output

Stage 6 باید در نهایت این چهار خروجی مفهومی را فراهم کند:

### 1. Forecast Accuracy

```text
MAPE
```

### 2. Forecast Bias

```text
Bias
```

### 3. Forecast Reliability

```text
0–100
```

### 4. Forecast Model Control

```text
Calibration Status
+
Model Version
+
Out-of-Sample Result
```

---

# 44. Final Stage 6 Architecture

```text
                 STAGE 5
              Forecast Engine
                     │
                     ▼
                  Actual
                     │
                     ▼
             Forecast Error
                ┌────┴────┐
                ▼         ▼
             Accuracy     Bias
                │         │
                └────┬────┘
                     ▼
             Baseline Comparison
                     │
                     ▼
            Observation Sufficiency
                     │
                     ▼
             Performance Score
                     │
                     ▼
             Confidence Adjustment
                     │
                     ▼
          Forecast Reliability 0–100
                     │
                     ▼
          Persistent Bias Detection
                     │
              ┌──────┴──────┐
              ▼             ▼
      No Calibration    Calibration
                            │
                            ▼
                     New Model Version
                            │
                            ▼
                  Out-of-Sample Test
                            │
                     ┌──────┴──────┐
                     ▼             ▼
                   Accept        Reject
                     │
                     ▼
                   STAGE 7
                 Valuation
                     │
                     ▼
              Forward P/E
                     +
           Forecast Reliability
                     │
                     ▼
           Valuation Confidence
```

---

# 45. Stage 6 Locked Decision

پس از Audit نهایی:

```text
Stage 6
Forecast Evaluation & Calibration

STATUS = LOCKED
VERSION = V1
```

Stage 6 اکنون از نظر معماری با:

* Stage 1 — Data Foundation
* Stage 2 — KPI Specification
* Stage 3 — Fundamental Scoring
* Stage 4 — Historical / Seasonal / Trend
* Stage 5 — Forecast Engine

سازگار است.

هر تغییر آینده در پارامترهای Accuracy، Reliability یا Calibration باید از طریق **Model Versioning** انجام شود و نباید معماری Locked Stage 6 را بدون بررسی رسمی تغییر دهد.
