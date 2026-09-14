# Stage 9 — Decision Engine & Dashboard Contract

## LOCKED SPECIFICATION

**Status:** LOCKED
**Stage:** 9 of 9
**Purpose:** Final decision integration and compact company dashboard
**Architecture:** Rule-Based Evidence Integration
**Version:** V1

---

# 1. Stage Objective

Stage 9 آخرین لایه سیستم تحلیل شرکت است.

هدف:

> «با توجه به وضعیت بنیادی، روند آینده سود، ارزش‌گذاری و رفتار بازار، وضعیت این سهم برای سرمایه‌گذار چیست؟»

Stage 9 باید اطلاعات تولیدشده توسط مراحل قبلی را در یک تصمیم نهایی، قابل توضیح، قابل ردیابی و قابل مقایسه ترکیب کند.

Stage 9 نباید تحلیل‌های مراحل قبل را دوباره محاسبه کند.

---

# 2. Position in Architecture

Architecture:

```text
Stage 1  Data Foundation
    ↓
Stage 2  KPI Specification
    ↓
Stage 3  Fundamental Scoring
    ↓
Stage 4  Historical / Seasonal / Trend
    ↓
Stage 5  Forecast Engine
    ↓
Stage 6  Forecast Evaluation & Calibration
    ↓
Stage 7  Valuation Engine
    ↓
Stage 8  Market Engine
    ↓
Stage 9  Decision Engine & Dashboard
```

Stage 9 مصرف‌کننده خروجی مراحل قبلی است.

Stage 9 نباید مالک منطق داخلی مراحل قبلی باشد.

---

# 3. Core Architectural Principle

Stage 9 یک:

**Decision Integration Engine**

است، نه یک Analysis Engine جدید.

بنابراین:

* KPI جدید ایجاد نمی‌کند.
* Fundamental Score جدید محاسبه نمی‌کند.
* Forecast جدید ایجاد نمی‌کند.
* EPS جدید محاسبه نمی‌کند.
* Forward P/E جدید محاسبه نمی‌کند.
* Fair Value جدید محاسبه نمی‌کند.
* Volatility جدید محاسبه نمی‌کند.
* Relative Strength جدید محاسبه نمی‌کند.
* Market Score ایجاد نمی‌کند.
* Buy/Sell تکنیکال ایجاد نمی‌کند.

Stage 9 فقط شواهد معتبر مراحل قبلی را با قواعد مشخص ترکیب می‌کند.

---

# 4. Four Decision Evidence Families

Stage 9 چهار خانواده اصلی شواهد را مصرف می‌کند:

## A — Fundamental Quality

از Stage 3:

* Fundamental Score
* Growth Score
* Profitability Score
* Risk & Quality Score
* Data Coverage
* Fundamental Data Quality

---

## B — Fundamental Direction & Future

از Stage 4، 5 و 6:

* Trend State
* Momentum / Direction
* Forecast State
* Forecast EPS
* Forecast Revenue
* Forecast Profit
* Forecast Revision Trend
* Forecast Reliability
* Forecast Accuracy
* Forecast Bias
* Calibration Status

---

## C — Valuation

از Stage 7:

* Valuation Status
* Expected Upside
* Scenario Fair Values
* Scenario Probabilities
* Scenario Dispersion
* Valuation Risk
* Valuation Confidence
* Target P/E
* Historical P/E
* Industry P/E
* Valuation Alerts
* Valuation Driver Ranking

---

## D — Market State

از Stage 8:

* Market Trend
* Momentum
* Relative Strength
* Volatility
* Drawdown
* Liquidity
* Price/Volume State
* Market Regime
* Market Alerts

Market evidence در V1 نقش Context/Confirmation/Risk دارد و نباید به‌تنهایی Fundamentals را Override کند.

---

# 5. Decision States

V1 Decision States:

```text
STRONG_BUY
BUY
HOLD
WATCH
REDUCE
SELL
STRONG_SELL
```

تعریف کلی:

### STRONG_BUY

ترکیب قوی و هم‌راستا از:

* Fundamental Quality قوی
* Future/Forecast مثبت
* Valuation جذاب
* Forecast Reliability کافی
* Decision Confidence بالا
* نبود Conflict مهم

Market Support ترجیحی است ولی در V1 الزام مطلق نیست.

---

### BUY

شرایط کلی:

* Fundamentals قابل قبول یا قوی
* آینده مثبت یا Improving
* Valuation جذاب یا منطقی
* Risk قابل مدیریت
* Reliability و Data Quality کافی

---

### HOLD

شرایط معمول:

* شرکت خوب است اما Valuation کاملاً جذاب نیست
* یا Fundamental/Forecast مناسب است ولی Confirmation کافی برای افزایش موقعیت وجود ندارد
* یا شرایط فعلی بیشتر مناسب نگهداری است تا خرید جدید

HOLD یک Decision معتبر و اصلی است، نه حالت شکست سیستم.

---

### WATCH

برای شرایطی مانند:

* Turnaround
* Forecast مثبت ولی هنوز تأیید نشده
* Valuation ناقص
* Data ناقص
* Conflict قابل توجه
* Market Confirmation ناکافی
* فرصت بالقوه‌ای که هنوز به تأیید کافی نرسیده است

---

### REDUCE

برای شرایطی مانند:

* Risk/Reward در حال بدتر شدن
* Valuation نامناسب
* Fundamental deterioration
* Forecast deterioration
* افزایش ریسک بدون نیاز به خروج کامل

---

### SELL

وقتی شواهد منفی معنادار در چند خانواده وجود دارد:

* Fundamentals ضعیف
* Future/Forecast منفی
* Valuation نامناسب
* Risk بالا

---

### STRONG_SELL

حالت نادر و شدید.

معمولاً ترکیب چند مورد از:

* Fundamental بسیار ضعیف
* Strong Deterioration
* Forecast منفی
* Valuation بسیار گران
* Reliability مناسب برای اعتماد به شواهد منفی
* Market Confirmation منفی
* ریسک شدید

---

# 6. Decision Is Not a Simple Weighted Score

Stage 9 نباید:

```text
Fundamental Score × X
+
Valuation Score × Y
+
Market Score × Z
```

انجام دهد.

به‌خصوص:

**Market Score در V1 وجود ندارد.**

Decision باید به صورت:

```text
Rule-Based Evidence Integration
```

باشد.

علت:

* جلوگیری از Double Counting
* امکان Overrideهای شفاف
* کنترل Value Trap
* کنترل Negative EPS
* کنترل Forecast Reliability
* کنترل Scenario Risk
* توضیح‌پذیری بهتر

---

# 7. Double Counting Control

یک واقعیت اقتصادی ممکن است در چند Stage ظاهر شود.

مثلاً:

```text
Revenue Growth
    ↓
Fundamental Score

Revenue Growth
    ↓
Trend

Revenue Growth
    ↓
Forecast

Forecast EPS
    ↓
Forward P/E
```

این به معنی چهار رأی مستقل نیست.

Stage 9 نباید این موارد را دوباره جمع کند.

Evidence باید به صورت Family-Level تفسیر شود.

---

# 8. Fundamental Dominance Rule

Fundamentals و Future نسبت به Market Context اولویت بنیادی دارند.

مثلاً:

```text
Fundamental = WEAK
Market = STRONG
```

نباید صرفاً به دلیل Market Rally تبدیل به STRONG_BUY شود.

همچنین:

```text
Fundamental = STRONG
Market = WEAK
```

نباید خودکار SELL شود.

Market می‌تواند:

* Confirmation
* Warning
* Conflict
* Execution Risk

باشد.

---

# 9. Value Trap Control

سناریوی مهم:

```text
Cheap
+
Weak Fundamentals
+
Negative Trend
+
Negative Forecast
```

باید بتواند Conflict زیر را ایجاد کند:

```text
CHEAP_BUT_WEAK
```

Decision نباید صرفاً به دلیل پایین بودن P/E یا Expected Upside مثبت، BUY شود.

---

# 10. Strong but Expensive

سناریو:

```text
Strong Fundamentals
+
Positive Forecast
+
Very Expensive Valuation
```

می‌تواند منجر به:

```text
HOLD
```

یا

```text
REDUCE
```

شود.

Conflict:

```text
STRONG_BUT_EXPENSIVE
```

ثبت شود.

---

# 11. Strong Fundamentals + Negative Future

اگر:

```text
Fundamental = STRONG
Trend = DETERIORATING
Forecast = NEGATIVE
```

سیستم نباید فقط Fundamental Score را ببیند.

Decision می‌تواند:

```text
HOLD
```

یا

```text
WATCH
```

شود، بسته به Valuation و Risk.

---

# 12. Weak Fundamentals + Improving Future

این حالت Turnaround است.

مثلاً:

```text
Fundamental = WEAK
Trend = IMPROVING
Forecast = POSITIVE
Valuation = ATTRACTIVE
```

Decision می‌تواند:

```text
WATCH
```

یا در صورت تأیید کافی:

```text
BUY
```

باشد.

Weak current fundamentals نباید به‌تنهایی آینده مثبت را حذف کند.

---

# 13. Forecast Reliability Constraint

Forecast Reliability از Stage 6 وارد Stage 9 می‌شود.

Reliability:

* اعتماد به Forecast را تعیین می‌کند.
* مستقیماً P/E را تغییر نمی‌دهد.
* مستقیماً Expected Upside را تغییر نمی‌دهد.
* مستقیماً Decision را به SELL تبدیل نمی‌کند.

اما Reliability پایین باید:

* Decision Confidence را کاهش دهد.
* امکان STRONG_BUY/STRONG_SELL را محدود کند.
* Risk/Warning ایجاد کند.

---

# 14. Negative EPS / Sign Change

اگر Stage 7 اعلام کند:

```text
Valuation = NOT_APPLICABLE
```

به دلیل:

* Negative EPS
* Zero EPS
* Sign Change

Stage 9 نباید P/E مصنوعی ایجاد کند.

در این حالت Decision باید بر اساس:

* Fundamentals
* Trend
* Forecast
* Forecast Reliability
* Market Context
* سایر Valuation evidenceهای معتبر

انجام شود.

---

# 15. Scenario Dispersion

Expected Upside نباید Bear Case بسیار بد را پنهان کند.

مثلاً:

```text
Expected Upside = +30%
Bear Upside = -50%
Base Upside = +15%
Bull Upside = +80%
```

این سهم ممکن است Attractive باشد اما:

```text
Valuation Risk = HIGH / EXTREME
```

و Decision Confidence محدود شود.

Expected Value به‌تنهایی معیار کافی نیست.

---

# 16. Decision Conflict

Stage 9 باید Conflictهای مهم را به‌صورت ساختاری ثبت کند.

نمونه‌ها:

```text
CHEAP_BUT_WEAK
STRONG_BUT_EXPENSIVE
STRONG_FUNDAMENTAL_WEAK_MARKET
WEAK_FUNDAMENTAL_STRONG_MARKET
POSITIVE_FX_NEGATIVE_FUNDAMENTAL
POSITIVE_FORECAST_LOW_RELIABILITY
HIGH_EXPECTED_UPSIDE_HIGH_BEAR_RISK
VALUATION_NOT_APPLICABLE
LOW_LIQUIDITY
INSUFFICIENT_DATA
```

Conflict توضیح‌دهنده وضعیت است و الزاماً Decision را تعیین نمی‌کند.

---

# 17. Holding Status

Holding Status از Decision جدا است.

V1:

```text
STRONG_HOLD
HOLD
HOLD_WITH_CAUTION
REVIEW_HOLD
EXIT_CANDIDATE
```

Holding Status مشخص می‌کند اگر سرمایه‌گذار سهم را در اختیار داشته باشد، وضعیت نگهداری آن چگونه است.

Position Sizing در V1 وجود ندارد.

---

# 18. Holding Logic

نمونه:

```text
Good Company
+
Fair Valuation
+
Stable Fundamentals
=
HOLD
```

یا:

```text
Good Company
+
Deteriorating Forecast
+
Expensive Valuation
=
HOLD_WITH_CAUTION
```

یا:

```text
Weak Fundamentals
+
Strong Deterioration
+
Poor Valuation
=
EXIT_CANDIDATE
```

Holding Status نباید صرفاً از Decision کپی شود.

---

# 19. Decision Confidence

Decision Confidence جدا از Decision است.

مثلاً:

```text
Decision = BUY
Confidence = 82
```

یا:

```text
Decision = BUY
Confidence = 48
```

Decision Confidence تحت تأثیر مواردی مانند:

* Data Quality
* Evidence Agreement
* Forecast Reliability
* Valuation Confidence
* Scenario Dispersion
* Decision Conflict
* Market Confirmation
* Sufficiency

قرار می‌گیرد.

Confidence نباید به‌صورت ساده میانگین چند Score باشد مگر اینکه Model Version صراحتاً چنین فرمولی را تعریف کند.

---

# 20. Insufficient Data

اگر داده کافی نباشد:

```text
WATCH
```

یا Decision محدودشده مشابه باید تولید شود.

سیستم نباید با داده ناکافی:

```text
STRONG_BUY
```

یا

```text
STRONG_SELL
```

با Confidence بالا تولید کند.

---

# 21. Transparent Overrides

Override فقط برای شرایط مشخص و قابل توضیح مجاز است.

نمونه:

### Valuation N/A

P/E-based Buy نباید فعال شود.

### Very Low Forecast Reliability

Strong Forecast-driven Decision محدود شود.

### Insufficient Data

Strong Decision محدود شود.

### Extreme Valuation Risk

Decision محافظه‌کارانه‌تر شود.

### Severe Fundamental Deterioration

Valuation ارزان نباید به‌تنهایی Buy ایجاد کند.

### Cheap + Weak

Valuation-only Buy ممنوع است.

تمام Overrideها باید:

* Explicit
* Auditable
* Versioned
* Explainable

باشند.

---

# 22. Hysteresis / Decision Stability

برای جلوگیری از Oscillation تصمیم‌ها، Decision Engine باید Hysteresis داشته باشد.

مثلاً:

```text
BUY
→ HOLD
```

نباید با یک تغییر بسیار کوچک در یک KPI رخ دهد.

Entry و Exit Thresholdها می‌توانند متفاوت باشند.

مثلاً یک سهم برای ورود به BUY به سطح مشخصی از شواهد نیاز داشته باشد، اما برای خروج از BUY لازم باشد شرایط به شکل معنادارتری بدتر شود.

فاصله‌های دقیق Hysteresis:

**Model Version Parameters**

هستند، نه Architecture Constants.

---

# 23. Decision History

Stage 9 باید تاریخچه Decision را نگهداری کند.

حداقل:

```text
Previous Decision
Current Decision
Decision Change
Change Date
Change Reasons
```

نمونه:

```text
Jun → BUY
Jul → BUY
Aug → BUY
Sep → HOLD
```

Decision Trend از Fundamental Trend مستقل است.

---

# 24. Ranking

Ranking در V1 یک **Ranking Score جدید** ایجاد نمی‌کند.

Ranking باید Risk-Aware باشد.

اولویت:

```text
1. Decision State / Tier
2. Decision Confidence
3. Expected Upside
4. Valuation Risk
5. Forecast Reliability
6. Fundamental Quality
```

Primary Ranking:

**Within Industry**

است.

Cross-Industry Ranking در V1 فقط در صورت نیاز به‌صورت Secondary/Optional قابل ارائه است.

Ranking نباید تحلیل جدید تولید کند.

---

# 25. Ranking Eligibility

شرکتی که:

```text
INSUFFICIENT_DATA
```

یا Valuation بسیار غیرقابل‌اعتماد دارد، نباید در رتبه‌بندی با شرکت‌های کاملاً معتبر به‌صورت عادی مقایسه شود.

بنابراین Ranking باید Data Quality و Eligibility را رعایت کند.

---

# 26. FX Context

FX یک Decision مستقل نیست.

Stage 9 می‌تواند Contextهای زیر را مصرف کند:

```text
fx_regime
fx_company_impact
usd_relative_valuation_context
free_market_fx
operational_fx
fx_gap
```

در صورت وجود داده.

---

# 27. Free-Market vs Operational FX

دو نرخ باید کاملاً جدا باقی بمانند.

## Operational / Exchange FX

برای مواردی مانند:

* Company Sales
* Export Revenue
* FX-linked Operating Earnings
* Forecast Earnings Exposure

در صورت ارتباط اقتصادی معتبر.

## Free-Market FX

برای:

* Market Cap USD
* Share Price USD
* USD-adjusted Return
* Historical Company Value USD
* USD-relative Market Valuation Context

---

# 28. FX Must Not Be Double Counted

اگر:

```text
Operational FX ↑
→ Forecast EPS ↑
→ Forward P/E ↓
```

Stage 9 نباید علاوه بر این مسیر، یک FX Buy Bonus اضافه کند.

مسیر صحیح:

```text
FX
↓
Forecast
↓
EPS
↓
Valuation
↓
Decision
```

FX Context می‌تواند دلیل/توضیح اضافی باشد، اما رأی مستقل جدید نیست.

---

# 29. FX Gap

تعریف:

```text
FX Gap = Free Market FX / Operational FX - 1
```

می‌تواند به‌عنوان Context استفاده شود.

States:

```text
FX_GAP_WIDENING
FX_GAP_STABLE
FX_GAP_NARROWING
```

FX Gap به‌تنهایی Buy/Sell Signal نیست.

---

# 30. FX Stress Rules

### Free FX ↑ + Operational FX ↑

در شرکت دارای Exposure مثبت:

* احتمال رشد Earnings
* احتمال USD-relative opportunity

اما فقط پس از بررسی EPS، Valuation و Fundamentals.

---

### Free FX ↑ + Operational FX Flat

نباید اثر مثبت Earnings فرض شود.

---

### Free FX ↑ سریع‌تر از Operational FX

اثر Valuation و Earnings باید جداگانه تحلیل شود.

---

### Operational FX ↑ + Free FX Flat

Earnings می‌تواند بهتر شود بدون اینکه Market Value USD الزاماً تغییر زیادی کند.

---

### Free FX ↓ + Operational FX ↑

اثر Earnings می‌تواند همچنان مثبت باقی بماند.

---

### Unknown FX Exposure

اثر مثبت یا منفی نباید فرض شود.

---

### Operational FX Missing

```text
MISSING
```

و نه Free Market Proxy مخفی.

اگر Proxy استفاده شد:

```text
FX_ASSUMPTION = ESTIMATED
SOURCE = FREE_MARKET_PROXY
CONFIDENCE = LOW
```

---

# 31. USD Relative Performance

اگر:

```text
Stock Return < Free Market USD Return
```

سهم از نظر USD عقب مانده است.

این فقط یک Opportunity Context است.

Decision باید بررسی کند:

```text
Fundamental
Forecast EPS
Forecast Reliability
Forward P/E
Valuation Risk
Market
```

---

# 32. FX + Value Trap

مثلاً:

```text
Stock/USD ↓
+
EPS ↓
+
Fundamental Trend ↓
```

این وضعیت نباید صرفاً به دلیل USD-relative cheapness فرصت تلقی شود.

Decision باید بتواند:

```text
CHEAP_BUT_WEAK
```

را ثبت کند.

---

# 33. FX + Ideal Opportunity

سناریوی بسیار قوی:

```text
Free Market FX ↑
+
Operational FX ↑
+
Positive Company FX Exposure
+
Stock lagging USD
+
Forecast EPS ↑
+
Forecast Reliability High
+
Forward P/E ↓
+
Fundamentals Strong/Improving
```

این می‌تواند یکی از قوی‌ترین Opportunity Contextها باشد.

ولی همچنان Decision توسط Evidence Integration تعیین می‌شود.

---

# 34. Market Confirmation

Market در Stage 9 به‌عنوان Confirmation/Risk استفاده می‌شود.

مثلاً:

```text
Fundamental Strong
Forecast Positive
Valuation Attractive
Market Uptrend
Relative Strength Strong
```

Alignment بسیار قوی است.

اما:

```text
Fundamental Strong
Forecast Positive
Valuation Attractive
Market Downtrend
```

می‌تواند:

```text
Decision Conflict
```

ایجاد کند بدون اینکه الزاماً Sell شود.

---

# 35. Liquidity

Low Liquidity:

* Execution Risk است.
* Decision را الزاماً به SELL تبدیل نمی‌کند.
* می‌تواند Confidence یا Risk را تحت تأثیر قرار دهد.
* در Dashboard نمایش داده می‌شود.

---

# 36. Decision ≠ Trading Signal

این قانون Non-Negotiable است.

Decision Stage 9:

> وضعیت سرمایه‌گذاری سهم را ارزیابی می‌کند.

این با:

> Trading Signal

برای معاملات کوتاه‌مدت یا Intraday متفاوت است.

Stage 9 در V1 سیستم Intraday Trading Signal نیست.

---

# 37. Dashboard Contract

Dashboard باید Compact باشد.

## سطح اول

```text
COMPANY
Current Price

DECISION
CONFIDENCE
```

## سطح دوم

```text
Fundamental
Trend
Forecast
Forecast Reliability
Valuation
Expected Upside
Valuation Risk
Market
Relative Strength
Liquidity
FX Context
```

## سطح سوم

```text
Why?
Risks
Scenario Summary
Decision History
```

---

# 38. Dashboard Example

```text
COMPANY
Current Price

DECISION: BUY
CONFIDENCE: 82

Fundamental       STRONG
Fundamental Score 84

Trend             IMPROVING

Forecast          POSITIVE
Forecast Rel.     78

Valuation         ATTRACTIVE
Expected Upside   +27%
Valuation Risk    MEDIUM

Market             UPTREND
Relative Strength  STRONG
Liquidity          NORMAL

FX Regime          RISING
FX Impact          POSITIVE
USD Context        STOCK LAGGING USD
```

---

# 39. Why Section

حداکثر 3 تا 5 دلیل اصلی.

مثلاً:

```text
WHY?

1. Fundamental quality remains strong.
2. EPS forecast is improving with acceptable reliability.
3. Forward P/E is below the relevant benchmark.
4. Stock has underperformed free-market USD while earnings outlook improves.
5. Market trend is supportive.
```

Reasons باید از خروجی‌های موجود استخراج شوند و تحلیل جدید تولید نکنند.

---

# 40. Risk Section

حداکثر چند Risk مهم:

```text
RISKS

- Bear scenario has material downside.
- Valuation depends heavily on margin assumptions.
- Forecast reliability is moderate.
- Market trend is weakening.
- Operational FX assumption has limited history.
```

---

# 41. Scenario Summary

Dashboard می‌تواند نمایش دهد:

```text
Bear
Base
Bull

Probability
Fair Value
Upside/Downside
```

و:

```text
Expected Upside
Scenario Dispersion
```

---

# 42. Decision History

Dashboard:

```text
Decision History

Jun   BUY
Jul   BUY
Aug   BUY
Sep   HOLD
```

همراه با:

```text
Decision Change
Change Date
Change Reasons
```

---

# 43. Data Quality

Stage 9 باید Data Quality را نمایش دهد.

نمونه:

```text
GOOD
LIMITED
WARNING
INSUFFICIENT
```

Decision Confidence نباید از کیفیت داده جدا باشد.

---

# 44. Point-in-Time Requirement

Stage 9 نیز باید Point-in-Time باشد.

Decision در تاریخ T فقط می‌تواند از اطلاعاتی استفاده کند که در تاریخ T قابل دسترس بوده‌اند.

این شامل:

* Codal
* ReportVersion
* Forecast
* Forecast Evaluation
* Valuation
* Market Data
* Free FX
* Operational FX

است.

Look-Ahead Bias ممنوع است.

---

# 45. Versioning

Stage 9 باید Model Version داشته باشد.

حداقل:

```text
decision_model_version
decision_contract_version
```

تمام:

* Thresholds
* Hysteresis Parameters
* Override Rules
* Ranking Parameters
* Confidence Parameters

باید در Model Version قابل ردیابی باشند.

---

# 46. Modular Contract Rule

Stage 9 نباید به Implementation داخلی مراحل قبلی وابسته باشد.

اگر Stage 3، 5، 7 یا 8 در آینده اصلاح شوند، تا زمانی که Contract خروجی حفظ شود، Stage 9 نباید نیاز به بازطراحی داشته باشد.

اگر Contract تغییر کرد:

```text
Contract Version Change
→ Migration
→ Validation
```

و نه تغییر مخفی.

---

# 47. Final Output Contract

Stage 9 باید حداقل خروجی‌های زیر را ارائه کند:

```text
company_id
decision_date

fundamental_state
fundamental_score

trend_state
forecast_state
forecast_reliability

valuation_status
expected_upside
valuation_risk
valuation_confidence

market_trend_state
market_momentum_state
relative_strength_state
liquidity_state

fx_regime
fx_company_impact
usd_relative_valuation_context
free_market_fx
operational_fx
fx_gap

decision
decision_confidence

decision_conflict

decision_reasons
decision_risks

holding_status

previous_decision
decision_change
decision_change_reasons

decision_ranking_eligibility
decision_rank_within_industry

decision_data_quality

decision_timestamp
decision_model_version
decision_contract_version
```

FX fields may be NULL when valid data is unavailable.

---

# 48. Ranking Contract

Ranking must remain separate from Decision itself.

```text
Decision State
    ↓
Ranking Eligibility
    ↓
Decision Tier
    ↓
Decision Confidence
    ↓
Expected Upside
    ↓
Valuation Risk
    ↓
Forecast Reliability
    ↓
Fundamental Quality
```

Primary comparison:

```text
Within Industry
```

No new Ranking Score in V1.

---

# 49. Non-Negotiable Rules

The following rules are permanently locked for V1:

1. Stage 9 does not create new KPIs.
2. Stage 9 does not recalculate upstream analytics.
3. Fundamental Score comes from Stage 3.
4. Trend comes from Stage 4.
5. Forecast comes from Stage 5.
6. Forecast Reliability comes from Stage 6.
7. Valuation comes from Stage 7.
8. Market State comes from Stage 8.
9. Decision is Rule-Based Evidence Integration.
10. Decision is not a simple weighted score.
11. Market Score does not exist in V1.
12. Decision ≠ Trading Signal.
13. HOLD is a legitimate primary Decision.
14. Holding Status is separate from Decision.
15. Cheap + Weak must not automatically produce BUY.
16. Strong + Expensive must not automatically produce BUY.
17. Negative EPS must not create artificial P/E.
18. Scenario dispersion must not be hidden by Expected Upside.
19. Low Forecast Reliability reduces confidence; it does not automatically mean SELL.
20. Insufficient data prevents high-confidence decisions.
21. Hysteresis is mandatory.
22. Decision History is mandatory.
23. Ranking is Risk-Aware.
24. Ranking is primarily within Industry.
25. Ranking does not create a new V1 score.
26. Free Market FX and Operational FX remain separate.
27. Operational FX must not silently default to Free Market FX.
28. FX Context is not a standalone Buy/Sell signal.
29. FX effects must not be double-counted.
30. USD-relative cheapness does not equal value.
31. Point-in-Time is mandatory.
32. Look-Ahead Bias is prohibited.
33. All decision logic is versioned.
34. All important decisions must be explainable.
35. Dashboard displays upstream outputs; it does not recreate their calculations.

---

# 50. V1 Explicit Exclusions

The following are NOT part of Stage 9 V1:

* Intraday trading signals
* Technical Buy/Sell systems
* Market Score
* Position sizing
* Portfolio optimization
* ML decision models
* Neural networks
* Black-box decision models
* Arbitrary FX Buy/Sell rules
* Hidden FX bonuses
* Complex Bayesian probability engine
* Monte Carlo decision engine
* Automatic investment execution

---

# 51. Final Stage 9 Architecture

```text
                 STAGE 3
            FUNDAMENTAL QUALITY
                    │
                    ▼
                 STAGE 4
            FUNDAMENTAL DIRECTION
                    │
                    ▼
                 STAGE 5
              FUTURE / FORECAST
                    │
                    ▼
                 STAGE 6
          FORECAST RELIABILITY
                    │
                    ▼
                 STAGE 7
                VALUATION
                    │
                    ▼
                 STAGE 8
              MARKET STATE
                    │
                    ▼
              FX CONTEXT
                    │
                    ▼
          ┌─────────────────────┐
          │   STAGE 9           │
          │ DECISION ENGINE     │
          │                     │
          │ Evidence Integration│
          │ Conflict Control    │
          │ Confidence          │
          │ Holding             │
          │ Ranking             │
          │ History             │
          └──────────┬──────────┘
                     │
              ┌──────┴──────┐
              ▼             ▼
          DECISION       DASHBOARD
```

---

# 52. Final Status

```text
Stage 9
DESIGNED          ✓
REVIEWED          ✓
STRESS TEST 1    ✓ PASS
STRESS TEST 2    ✓ PASS
FX/USD TEST       ✓ PASS
FINAL AUDIT       ✓ PASS
LOCKED            ✓
```

**Stage 9 is LOCKED.**

The complete 9-stage conceptual architecture is now frozen for V1.

Future work must move to implementation rather than redesigning the conceptual architecture, unless a genuine implementation-level contradiction is discovered. Any such contradiction must be explicitly identified, justified, versioned, and assessed for downstream impact.
