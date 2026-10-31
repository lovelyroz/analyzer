# Stage 7 — Valuation Engine

## Locked Specification — V1

### Status

DESIGNED → REVIEWED → STRESS TESTED → AUDITED → **LOCKED**

**Owner-Approved Amendment (2026-10-31):** See section **AMENDMENT-OA1** below. This amendment supersedes the industry-peer cheap/expensive assessment and the industry P/E fallback hierarchy for Target P/E. It does not unlock or re-open the V1 architecture; it records binding owner policy changes that implementation and later documentation must follow. Implementation of these policies is **not** complete merely because this document was updated.

---

# AMENDMENT-OA1 — Owner-Approved P/E, Complete-Input, Market-Price and Persistence Policies

**Authority:** Explicit project-owner decisions. Binding for V1 active policy.

**Effective for active policy:** Immediate for documentation and for all future implementation work. Historical sections that conflict remain in the document for audit trail and are marked **SUPERSEDED**.

## OA1.1 Primary relative valuation measure (cheap / expensive)

The primary question remains whether the share is cheap or expensive relative to its Forward P/E.

**Active rule:** The cheap/expensive relative assessment must be made **only against the same company’s own historical Forward P/E**.

- Compare current Forward P/E to the company’s own historical Forward P/E series (and supported statistics such as median where valid observations exist).
- Do **not** use industry peers or industry P/E (Forward or TTM) as the basis for deciding whether this company is cheap or expensive.
- Outputs must distinguish:
  - Current Forward P/E
  - Same-company historical Forward P/E series
  - Historical comparison statistic(s) (e.g. median) where supported
  - Resulting relative valuation assessment
  - Dates and provenance of the observations used

No new assessment thresholds or financial formulas are introduced by this amendment. Existing status labels and any numeric thresholds remain model parameters subject to separate owner approval; this amendment does not invent or ratify thresholds.

## OA1.2 Historical P/E is a derived calculation

Historical P/E must be calculated from the company’s own underlying financial and market data.

- It must **not** be accepted as a precomputed numeric input without underlying source data and provenance.
- Calculation uses the latest complete and valid input set available under the applicable date/cutoff rules (see OA1.5).
- If newer input data are incomplete: use the latest earlier complete and valid set; identify the actual date of data used; report that newer data are incomplete; list exact missing inputs.
- If no complete valid set exists: do not fabricate a P/E; report why calculation is unavailable and identify missing inputs.
- Historical P/E is reported separately from Forward P/E. It is **not** the primary cheap/expensive comparison measure (that is same-company historical Forward P/E per OA1.1).

Financial period date and publication/availability date are different concepts and must not be conflated.

## OA1.3 P/E is derived, not an independent input

Every P/E value is a runtime derived calculation from underlying observations. It must not be supplied as an unexplained numeric sequence or accepted as a standalone database input.

Required traceability for underlying observations (as applicable):

- Company identity
- Financial period or observation date
- Source identity
- Publication date/time
- Availability date/time or other evidence required by the approved temporal contract
- Market-price observation date and source
- Relevant forecast version and its input references (for Forward P/E)
- Analysis cutoff and Jalali date context

Do not claim full Point-in-Time correctness unless the required temporal evidence exists.

**Database rule:** No precomputed P/E values or analytical outputs may be persisted as independent database records. Raw source data may be persisted under existing source-data contracts. P/E is calculated at runtime.

## OA1.4 Industry P/E removed from cheap/expensive assessment and Target P/E hierarchy

**Superseded:** Previous V1 policy that used Industry Forward P/E Median as the primary Target P/E benchmark, Industry TTM P/E as fallback, and industry comparison for cheap/expensive assessment (former sections 10–13 and related hierarchy text).

**Active rule:**

- Industry Forward P/E and Industry TTM P/E are **removed** from the cheap/expensive assessment.
- Industry Forward P/E and Industry TTM P/E are **removed** from the Target P/E base/fallback hierarchy.
- Do not preserve old industry-benchmark fallback behavior as approved V1 policy.

Target P/E Base for active policy relies on same-company historical context consistent with OA1.1 and OA1.2. Exact Target P/E construction parameters remain subject to model-parameter rules already in the specification; this amendment does not invent new multiples or spreads.

Sections 10, 11, 12, and 13 below are retained for historical context and are marked SUPERSEDED by this amendment.

## OA1.5 Latest complete and valid input set

The engine must not automatically use the newest individual records if they do not form a complete and valid input set.

For each calculation:

1. Select the latest complete and valid input set that satisfies company identity, period, source, cutoff, and temporal validity requirements for that calculation.
2. If newer data are incomplete: use the latest earlier complete and valid set; perform the calculation on that set; identify the actual date/version of the selected inputs; warn that newer inputs are incomplete; list the exact missing inputs required to complete the newer set.
3. If no complete valid set exists: fail closed and explain the missing requirements.

Do not mix observations from different companies, incompatible periods, or incompatible forecast versions merely to create an apparently complete set.

Completeness is defined per calculation from its actual input contract; no universal completeness checklist is invented here.

## OA1.6 Market price — latest available observation and explicit alert

- Use the latest available market-price observation on or before the Jalali analysis date.
- Do not silently present an older market price as if it belonged to the analysis date.
- Report the actual Jalali date of the selected market-price observation.
- If the selected price date differs from the analysis date, emit a clear alert identifying both dates.
- If no eligible price exists, preserve fail-closed behavior unless a separate owner decision authorizes a change.

This is transparent latest-available-data behavior; it is not proof of complete PIT correctness.

## OA1.7 Analytical output persistence is prohibited

**Owner decision:** All analytical outputs are temporary runtime results. No analytical output or decision history may be persisted in the database.

Includes, without limitation:

- Forecast outputs
- Valuation outputs
- Calculated P/E values
- Fair values and valuation assessments
- Decision outputs
- Decision history

Stage 9 may receive `previous_decision` from its caller when available for runtime logic such as hysteresis. Stage 9 must not create or persist its own decision history.

Do not add database models, tables, repositories, or persistence mechanisms for analytical outputs.

**Unresolved conflict (implementation/documentation):** Stage 5 locked specification documents Forecast Versioning, Forecast Record, and preservation of prior Forecast versions (see `05_Stage5_Forecast_Engine.md` sections on Forecast Versioning and Forecast Record). Existing Forecast persistence models, if present in the codebase, must **not** be silently declared compliant with OA1.7. This conflict is recorded as an explicit unresolved implementation/documentation issue requiring a separate controlled audit and owner-authorized remediation. This documentation-only task does not delete or modify those models.

## OA1.8 What this amendment does not change

- Forward P/E remains the primary valuation axis formula (Price ÷ Forecast EPS).
- Bear / Base / Bull scenario structure.
- Invalid / negative / zero EPS rules (no artificial P/E).
- Separation of Valuation Status, Risk, and Confidence.
- Alerts are not Buy/Sell signals.
- Fundamental Score and Trend must not directly scale Target P/E.
- Forecast Reliability must not mathematically rescale Forward P/E or Fair Value.
- Scenario Probability sums to 100%.
- No invention of thresholds, formulas, sector mappings, or dated parameter values.

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
      ├── Historical Valuation (same-company; see AMENDMENT-OA1)
      ├── Target P/E (industry hierarchy SUPERSEDED by OA1.4)
      ├── Scenario Fair Value
      ├── Scenario Probability
      ├── Expected Fair Value
      ├── Valuation Assessment (cheap/expensive vs same-company hist. Fwd P/E)
      ├── Valuation Risk
      ├── Valuation Confidence
      └── Sensitivity / Alerts
      │
      ▼
Stage 9
Decision Engine
```

> **Note (AMENDMENT-OA1):** Industry Valuation is no longer an active cheap/expensive or Target P/E benchmark path. Same-company historical Forward P/E is the sole relative basis for cheap/expensive assessment.

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

**Active policy (AMENDMENT-OA1.6):** Use the latest available market-price observation on or before the Jalali analysis date. Report the actual Jalali date of the selected observation. If that date differs from the analysis date, emit a clear alert identifying both dates. Do not silently present an older price as if it belonged to the analysis date. Absence of an eligible price remains fail-closed unless a separate owner decision changes that behavior. This is not a claim of complete PIT correctness.

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

**Active policy (AMENDMENT-OA1.2 / OA1.3):** Historical P/E is a **derived** calculation from the company’s own underlying financial and market observations. It must not be accepted as a precomputed numeric input. Financial period date and publication/availability date must not be conflated. Selection of inputs follows the latest-complete-and-valid-set rule (OA1.5). Historical P/E is reported separately from Forward P/E and is **not** the primary cheap/expensive comparison measure (primary relative measure is same-company historical **Forward** P/E per OA1.1).

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

**Active policy (AMENDMENT-OA1.1):** For the **cheap/expensive** relative assessment, the comparison basis is the same company’s historical **Forward** P/E series (and supported statistics such as median where valid). Historical TTM P/E series remains available as contextual/historical valuation information but is not the primary cheap/expensive measure. Series must be built from derived calculations with provenance; precomputed sequences without underlying data are not accepted.

---

# 10. Industry Valuation

> **SUPERSEDED by AMENDMENT-OA1 (OA1.4).**  
> Industry peer comparison is **not** part of the active cheap/expensive assessment or Target P/E hierarchy.  
> Text below is retained only for historical audit trail of the pre-amendment V1 design.

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

> **SUPERSEDED by AMENDMENT-OA1 (OA1.4).**  
> Industry Forward P/E is removed from active Target P/E hierarchy and from cheap/expensive assessment.

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

> **SUPERSEDED by AMENDMENT-OA1 (OA1.4).**  
> Industry TTM P/E is removed from active Target P/E fallback hierarchy and from cheap/expensive assessment.

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

> **SUPERSEDED by AMENDMENT-OA1 (OA1.4).**  
> Active Target P/E hierarchy no longer uses Industry Forward P/E or Industry TTM P/E.  
> Cheap/expensive relative assessment uses same-company historical Forward P/E only (OA1.1).  
> Historical Median P/E remains relevant as company-own context, not as an industry fallback.

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

**Active policy (AMENDMENT-OA1.1):** The primary cheap/expensive relative assessment compares Current Forward P/E only to the **same company’s historical Forward P/E** series (and supported statistics such as median where valid observations exist). Industry peers or Industry Forward/TTM P/E are **not** used for this assessment.

Comparisons performed for valuation context:

```text
Current Forward P/E
vs
Target Forward P/E

Current Forward P/E
vs
Same-company historical Forward P/E (primary relative basis)

Current Forward P/E
vs
Historical Median P/E (company-own TTM/contextual; not primary cheap/expensive measure)
```

Industry Median Forward P/E may appear only as **legacy/informational metadata** for contract compatibility. It is **not** an active input to cheap/expensive assessment or Target P/E selection (see OA1.4 and SUPERSEDED sections 10–13).

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

> **V1 Implementation Status (factual annotation — updated 2026-10-31 per S7-T007 decisions):**
>
> A code-level Parameter Registry **does exist** in `src/valuation/parameters.py` (classes `ParameterRegistry`, `ParameterSetVersion`, functions `resolve_parameter_set`, `resolve_parameter_set_as_of`, `select_parameter_set_for_valuation`). Genesis snapshot is built programmatically from live module constants; `effective_from` on genesis is `None`; undated genesis is **never** selected for historical as-of queries; missing dated versions raise `LookupError` (fail-closed). Thresholds remain the live constants mirrored into registry records.
>
> **Architectural decisions now resolved (S7-T007 / D9 policy):** V1 parameter registry is version-controlled in code (no DB-backed analytical parameter registry); parameter versions require genuine evidence-backed `effective_from` before historical participation; never invent or backdate `effective_from`; undated Genesis must not be selected as a historical version; missing historical versions fail closed (no silent substitution of today); historical backtests may only use authentic vintages and authentic PIT input evidence; all output-affecting parameters must be tied to an immutable model version; numerical Genesis values are **not** owner-approved merely by existing in source.
>
> **Still unavailable / unresolved:** authentic historical parameter vintages with evidence-backed effective dates; owner approval of numerical Genesis values (R5 / S7-T020); full source-level provenance and runtime validation for historical Forward P/E observations (implementation under OA1 tasks). Full PIT must not be claimed from observation dates alone.

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
>   industry_divergence_ratio  = 1.50  # LEGACY / INACTIVE for active cheap-expensive assessment under OA1.4
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
> این **رفتار پیاده‌سازی** است، نه سیاست تأییدشده توسط مشخصات. بخش‌های ۴۱ تا ۵۳ هیچ مقدار تریگری را تعیین نمی‌کنند. وضعیت تأیید آستانه‌های مربوط به مسیرهای فعال همچنان موضوع تصمیم D9 است؛ اما `industry_divergence_ratio` به‌دلیل OA1.4 از مسیر فعال ارزانی/گرانی خارج و صرفاً یک مقدار legacy/inactive است، بنابراین نباید به‌عنوان آستانهٔ فعال یا مبنای تصمیم ارزندگی ratify شود. این سند هیچ عددی را تأیید یا تغییر نمی‌دهد. آزمون‌های boundary، رفتار فعلی را pin می‌کنند، نه انطباق با مشخصات را.

---

# 49. V1 Alert and Flag Vocabulary

This section records the concrete vocabulary found in the V1 implementation for audit and contract-history purposes. It is not a declaration that every listed token belongs to the active post-OA1 vocabulary. Where earlier sections use generic divergence labels, the concrete above/below tokens below are the emitted names; directional pairs remain separate.

**`alerts` channel (severity-prefixed strings):**

```text
WARNING:HIGH_SCENARIO_DISPERSION
WARNING:LOW_FORECAST_RELIABILITY
CRITICAL:INSUFFICIENT_BENCHMARK_DATA
WATCH:VALUATION_ABOVE_TARGET_PE
WATCH:VALUATION_BELOW_TARGET_PE
WATCH:FORWARD_PE_ABOVE_HISTORICAL
WATCH:FORWARD_PE_BELOW_HISTORICAL
INFO:TOP_DRIVER:<driver>
```

**Legacy / informational tokens (excluded from the active post-OA1 vocabulary):**

```text
WATCH:FORWARD_PE_ABOVE_INDUSTRY
WATCH:FORWARD_PE_BELOW_INDUSTRY
```

The target and historical directional pairs describe active review context as applicable. The Industry directional pair above is retained only as LEGACY / INFORMATIONAL vocabulary for historical implementation and contract audit; it is not part of the active post-OA1 cheap/expensive vocabulary and must not be used as an active relative-valuation signal. `INSUFFICIENT_BENCHMARK_DATA` reports that no usable benchmark was selected; it is distinct from a low peer count. `TOP_DRIVER` is an informational driver note. These tokens describe review context and are not Buy/Sell signals.

**`valuation_risk_flags` channel (strings):**

The engine emits flag-only tokens including:

```text
INSUFFICIENT_PEER_DATA
NEGATIVE_EPS
SIGN_CHANGE
```

These are flags, not severity-prefixed alerts. `ValuationResult.alerts` and `ValuationResult.valuation_risk_flags` are separate `List[str]` fields. The engine also copies emitted alert strings into `valuation_risk_flags`; therefore the channels overlap for emitted alerts, but a flag-only token is not promoted into `alerts`.

**Deferred or undefined categories:**

- Deferred under V1 policy D1–D5; not emitted because the required criteria remain unapproved or the needed inputs are unavailable: `ASSESSMENT_FLIP_RISK`, `HIGH_MULTIPLE_DEPENDENCE`, `HIGH_EPS_DEPENDENCE`, `MARGIN_ASSUMPTION_RISK`, and `HIGH_IMPACT_HIGH_UNCERTAINTY`.
- `POOR_DATA_QUALITY` is not implemented because a valid trigger is not established. Its absence does not establish that input data is good.
- `POINT_IN_TIME_WARNING` is not implemented because a valid trigger is not established and D7 does not establish complete Point-in-Time evidence. Its absence does not establish Point-in-Time correctness.

This section documents the current V1 output vocabulary and its channels. It does not define new triggers, thresholds, severities, formulas, or financial policy.

---

# 50. Assessment Flip Risk

> **V1 status (D1): DEFERRED.** This section describes a policy category; the engine does not emit `ASSESSMENT_FLIP_RISK`. The perturbation, flip definition, severity, and missing-data behavior are not approved.



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

---

# 51. Multiple Dependence

> **V1 status (D2): DEFERRED.** The engine does not emit `HIGH_MULTIPLE_DEPENDENCE`; no approved dependence measure or trigger is defined.



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

---

# 52. EPS / Forecast Dependence

> **V1 status (D3): DEFERRED.** The engine does not emit `HIGH_EPS_DEPENDENCE`; no approved EPS-dependence measure, severity escalation, or precedence rule is defined. Stage 5 EPS remains unchanged.



اگر Valuation عمدتاً به Forecast EPS حساس باشد:

```text
HIGH_EPS_DEPENDENCE
```

فعال می‌شود.

اگر هم‌زمان Forecast Reliability پایین باشد، Severity می‌تواند افزایش پیدا کند.

---

# 53. Margin Assumption Risk

> **V1 status (D4): DEFERRED.** The engine does not emit `MARGIN_ASSUMPTION_RISK`; valid, dated margin inputs and an approved trigger are unavailable.



اگر Fair Value به شدت وابسته به Operating Margin یا Net Margin Forecast باشد:

```text
MARGIN_ASSUMPTION_RISK
```

ثبت می‌شود.

---

# 54. Historical Divergence Alert

اگر Current/Forward P/E فاصله قابل توجهی با Historical Median P/E داشته باشد:

```text
HISTORICAL_VALUATION_DIVERGENCE
```

قابل تولید است.

این Alert به خودی خود Cheap/Expensive Signal قطعی نیست.

> **V1 emitted vocabulary (D8 decision):** The specification adopts the current engine tokens; production output is unchanged.
>
> | Direction | Emitted alert token | Meaning |
> |---|---|---|
> | Above | `WATCH:FORWARD_PE_ABOVE_HISTORICAL` | Base Forward P/E is above the historical median benchmark. |
> | Below | `WATCH:FORWARD_PE_BELOW_HISTORICAL` | Base Forward P/E is below the historical median benchmark. |
>
> The above/below distinction is preserved. Trigger behavior remains the existing engine behavior; this documentation does not ratify its numeric threshold.

---

# 55. Industry Divergence Alert

> **SUPERSEDED / INACTIVE for relative assessment (AMENDMENT-OA1.4).**  
> Industry Forward P/E is removed from active cheap/expensive assessment and from the Target P/E hierarchy. Divergence against industry medians is **not** part of the primary relative valuation path.  
> Text below is retained for historical audit trail and for describing **legacy/informational** engine tokens that may still be emitted for contract compatibility. These tokens must **not** be treated as active cheap/expensive signals or as justification for Target P/E selection under OA1.

اگر Forward P/E شرکت فاصله قابل توجهی با Industry Forward P/E داشته باشد (مسیر legacy):

```text
INDUSTRY_VALUATION_DIVERGENCE
```

در سیاست فعال V1 پس از OA1، این مقایسه مبنای ارزانی/گرانی نیست.

> **V1 emitted vocabulary (D8 decision; legacy/informational post-OA1):** The specification adopts the current engine tokens; production output is unchanged until S7-T017 removes active dependence.
>
> | Direction | Emitted alert token | Meaning |
> |---|---|---|
> | Above | `WATCH:FORWARD_PE_ABOVE_INDUSTRY` | Base Forward P/E is above the industry Forward P/E median (legacy/informational). |
> | Below | `WATCH:FORWARD_PE_BELOW_INDUSTRY` | Base Forward P/E is below the industry Forward P/E median (legacy/informational). |
>
> The above/below distinction is preserved. Trigger behavior remains the existing engine behavior; this documentation does not ratify its numeric threshold. Under OA1 these tokens are **not** inputs to relative cheap/expensive assessment.
>
> The separate flag `INSUFFICIENT_PEER_DATA` reports that valid Forward P/E peer count is below `MIN_INDUSTRY_PEERS = 8`, when Forward peer values exist. `INDUSTRY_BENCHMARK_INSUFFICIENT` is emitted only when no usable target benchmark is available (`target_source` equals `INSUFFICIENT_DATA`). These conditions are not equivalent. Neither flag is a severity-prefixed alert. After OA1, industry peer count no longer governs Target P/E or cheap/expensive assessment.

---

# 56. Point-in-Time Requirement

> **V1 alert status:** `POINT_IN_TIME_WARNING` is not emitted. This absence is not evidence of Point-in-Time completeness or correctness.

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

مثلاً (active policy after AMENDMENT-OA1):

```text
Fair Value
→ Target P/E
→ Benchmark (same-company historical context; industry path SUPERSEDED for Target selection)
→ Company-own historical Forward / TTM observations with provenance

Fair Value
→ Forecast EPS
→ Forecast Version
→ Forecast Inputs
→ Financial Facts
→ ReportVersion
→ Publication Date
```

Industry series fields, if present in outputs, are legacy/informational metadata only and must not be treated as the active Target or cheap/expensive benchmark.

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
# same-company historical Forward P/E series / statistics (primary relative basis per OA1.1)
# — exact field names for the historical Forward series remain subject to schema contract;
#   they must carry provenance and must not be precomputed independent DB records (OA1.2/OA1.3)

industry_forward_pe          # LEGACY / INFORMATIONAL metadata only (OA1.4)
industry_ttm_pe              # LEGACY / INFORMATIONAL metadata only (OA1.4)
industry_peer_count          # LEGACY / INFORMATIONAL metadata only (OA1.4)
# Industry fields may remain for contract compatibility. They MUST NOT be used as the
# active basis for cheap/expensive assessment or for Target P/E selection under OA1.

target_pe_bear
target_pe_base
target_pe_bull
target_pe_source             # must reflect same-company historical context after OA1; not INDUSTRY_*

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

Same-company historical Forward P/E (primary relative basis)
Historical Median P/E (company-own contextual)

Forecast Reliability
Valuation Confidence
Valuation Risk
Valuation Status

Top Valuation Drivers
Critical Alerts
```

Industry P/E (if shown) is **legacy/informational only** and must not be presented as the active cheap/expensive or Target benchmark (OA1.4). جزئیات بیشتر باید Drill-Down باشند.

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
> ترکیب قابل‌دستیابی در V1 عبارت است از `ATTRACTIVE` به‌همراه `valuation_confidence` / `valuation_confidence_label` در سطح LOW یا VERY_LOW، به‌همراه flag تحت عنوان `LOW_FORECAST_RELIABILITY` و alert تحت عنوان `WARNING:LOW_FORECAST_RELIABILITY` (`engine.py:162-163,514`). مقدار Reliability ورودی تابع `_valuation_status` نیست و Fair Value را تغییر نمی‌دهد. توکن تحت‌اللفظی `FORECAST RISK WARNING` / `FORECAST_RISK` هرگز صادر نمی‌شود (صفر ارجاع در کل `src` — رکوع بخش ۷۹). **تصمیم D3 هنوز حل‌نشده است.** ادعای PASS بالا فقط برای ترکیب قابل‌دستیابی صادق است، نه برای توکن تحت‌اللفظی.

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

> **HISTORICAL / SUPERSEDED by AMENDMENT-OA1.4 — NOT an active V1 valuation rule.**  
> This stress-test snapshot documents the pre-OA1 industry-peer Target P/E fallback design and its historical implementation evidence only. Industry peer count and Industry P/E no longer determine active cheap/expensive assessment or Target P/E selection. The historical result below is retained for audit traceability; it must not be read as a current acceptance criterion or active fallback policy.

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
> رفتار fallback واقعی و تست‌شده به این صورت است: با کمتر از ۸ peer معتبر، بنچمارک industry-forward برای انتخاب **رد** می‌شود (`target_pe_source` به `HISTORICAL_MEDIAN_PE` می‌رود؛ `_select_target_pe` در `engine.py:263-267` و `MIN_INDUSTRY_PEERS = 8`) و flag تحت عنوان `INSUFFICIENT_PEER_DATA` صادر می‌شود (`engine.py:164-165`). در همین حالت، فیلد `industry_forward_pe_median` همچنان median مقادیر موجود را گزارش می‌کند (مثلاً با ۷ peer مقدار 6.0) — صرفاً برای انتخاب بنچمارک استفاده نمی‌شود. برچسب `INDUSTRY_FORWARD_PE = INSUFFICIENT_DATA` در متن بالا دقیق نیست و باید به سیگنال واقعی `INSUFFICIENT_PEER_DATA` ارجاع داده شود. flag تحت عنوان `INDUSTRY_BENCHMARK_INSUFFICIENT` تنها زمانی صادر می‌شود که `target_source == "INSUFFICIENT_DATA"` باشد (یعنی هیچ بنچمارک قابل‌استفاده‌ای موجود نباشد) و نباید با `INSUFFICIENT_PEER_DATA` یکی گرفته شود — همان تفکیک ثبت‌شده در اصلاحیه P21 بخش ۵۵.

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
> نام `FORECAST_RISK` در هیچ فایل تولیدی یا آزمونی تعریف نشده و از واژگان خروجی V1 که در D8 پذیرفته شد نیست. این نام alias برای `HIGH_EPS_DEPENDENCE` محسوب نمی‌شود؛ هر دو trigger مربوط به این دسته تا تعیین معیارهای D3 غیرفعال می‌مانند. این مستندسازی trigger یا severity تازه‌ای اضافه نمی‌کند.
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
> ممنوعیت scale مستقیم Target P/E برقرار است (ساختاری): امضای `calculate_valuation` (`engine.py:57-79`) هیچ ورودی trend ندارد. نیمه مثبت ادعا فقط از طریق کانال family-evidence صادق است — یک trend از نوع `Strong Improvement` در Stage 4 مستقیماً وارد مرز Stage 7 نمی‌شود و نمی‌تواند مستقیماً احتمال‌ها را جابه‌جا کند؛ ابتدا باید در بالادست (upstream) داخل family scoreها (بخش‌های ۲۳–۲۴، `probability_evidence`) تجمیع شود و سپس caller آن را به Stage 7 بدهد. **تصمیم D6 (در صورت ورود ورودی‌های sector/trend به مرز) هنوز حل‌نشده است.**

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
> عدم تولید growth/P/E گمراه‌کننده و flagهای sign-change واقعی و تست‌شده‌اند: EPS منفی → fpe/fv برابر None (مدل‌ها) و وضعیت `NOT_APPLICABLE` (`engine.py:197-199`). برچسب‌های `LOSS_TO_PROFIT` / `PROFIT_TO_LOSS` گذارهای علامت **بین‌سناریویی** هستند (نسبت به سناریوهای دیگر در همان اجرا؛ `_scenario_sign_change_flags` در `engine.py:374-384`)، نه برچسب‌های revision زمانی؛ خوانش `-100 → +120` با مجموعه flagها بازنمایی می‌شود، نه با یک سری زمانی.

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
Point-in-Time (design; full runtime proof requires temporal provenance — OA1 / D7)
Historically contextualized (same-company historical Forward P/E as primary relative basis)
Reliability-aware
Risk-aware
Explainable
Auditable
Versioned
Modular
Backtestable
```

Industry-relative comparison for cheap/expensive and Target P/E is **SUPERSEDED by OA1.4** and is not an active architectural principle.

---

# 87. Non-Negotiable Rules

موارد زیر در Stage 7 V1 غیرقابل نقض هستند:

1. Forward P/E محور اصلی Valuation است.
2. Bear/Base/Bull مستقل محاسبه می‌شوند.
3. Negative/Zero EPS نباید P/E مصنوعی ایجاد کند.
4. Historical Valuation باید Point-in-Time باشد (subject to available temporal evidence; full PIT is not claimed without publication/availability evidence — AMENDMENT-OA1).
5. **SUPERSEDED by AMENDMENT-OA1.4:** Industry comparison for cheap/expensive and Target P/E hierarchy is removed. Active relative cheap/expensive assessment uses **same-company historical Forward P/E only**.
6. **SUPERSEDED by AMENDMENT-OA1.4:** Industry Peer Count minimum no longer governs Target P/E or cheap/expensive assessment.
7. Median بر Mean اولویت دارد (for same-company historical series statistics where used).
8. Forward و TTM must not be mixed in a single population (still valid if any dual series are retained for context).
9. Fundamental Score مستقیماً Target P/E را Scale نمی‌کند.
10. Trend مستقیماً Target P/E را Scale نمی‌کند.
11. Forecast Reliability مستقیماً P/E یا Fair Value را ضرب نمی‌کند.
12. Scenario Probability همیشه مجموعاً 100% است.
13. Probability و Dependency دو مفهوم مستقل هستند.
14. Expected Fair Value جای Scenario Range را نمی‌گیرد.
15. Valuation Status، Risk و Confidence مستقل هستند.
16. Alerts توصیه Buy/Sell نیستند.
17. Point-in-Time و Versioning اجباری هستند (within available evidence; see OA1).
18. Old Model Versions overwrite نمی‌شوند.
19. تغییر منطق داخلی Stage تا حد ممکن نباید Contract Stage را بشکند.
20. تمام Thresholdهای قابل Calibration باید Model Version Parameters باشند.
21. **AMENDMENT-OA1:** P/E is derived at runtime; no precomputed P/E or analytical outputs may be persisted as independent DB records. Latest-complete-input selection and market-price date alert are required. Analytical-output persistence is prohibited (Forecast persistence models remain an unresolved conflict pending separate audit).

---

# 88. Final Status

**Stage 7 — Valuation Engine: LOCKED** (architecture), with **AMENDMENT-OA1** binding for active P/E / complete-input / persistence policy.

**Architecture status (design review):**

Architecture:
PASS

Scenario Framework:
PASS

Forward P/E Framework:
PASS

Historical Benchmarking (same-company design):
PASS (design); Industry benchmarking path **SUPERSEDED by OA1.4**

Probability Framework:
PASS

Risk / Confidence Separation:
PASS

Sensitivity Engine:
PASS (within implemented V1 scope; deferred alerts remain deferred)

Alert Engine:
PASS (within implemented V1 vocabulary; OA1-related alert paths pending S7-T013–T017)

Double-Counting Control:
PASS

Auditability:
PASS (design)

Versioning:
PASS

Modular Upgradeability:
PASS

**Point-in-Time status (must not be conflated):**

- Architecture / design review for PIT intent: PASS where supported by the locked design.
- Runtime PIT implementation and verification: **OPEN / BLOCKED** until actual temporal provenance evidence (publication/availability, per-observation dates, complete-input selection under OA1.5) exists and is exercised. Full PIT must **never** be claimed based solely on Jalali observation dates.
- See OA1.2, OA1.5, OA1.6 and unresolved D7.

**Implementation and Stage readiness (clarification):**

- **Ready for implementation:** Architecture and OA1 policy are documented and locked for design purposes. This does **not** mean OA1 policies (S7-T013–S7-T018), runtime PIT, or analytical-output persistence rules are implemented in code. Implementation tasks remain OPEN until code and user-run test evidence exist.
- **Ready for Stage 8:** Stage 8 may proceed on the existing Stage 7 contract boundary. This does **not** prove that OA1 implementation, runtime PIT, Stage 7 completion, or E2E production path has been achieved. Stage 7 itself remains **OPEN**.
- Analytical-output persistence remains prohibited (OA1.7). Existing Forecast persistence models must not be deleted or modified by documentation work; conflict is tracked under S7-T019.
