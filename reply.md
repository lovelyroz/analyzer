
=====================================
وضعیت فایل‌های تست

test_p2_sector_driver_decomposition_missing.py:  ناموجود

test_p2_required_flip_dependence_alerts_missing.py: ناموجود

----------------------------------------

من چیزی به اسم Sector Driver Decomposition پیدا نکردم ولی موارد زیر را پیدا کردم
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

----------------------------------------------------------------
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

==================================

sector_driver_decomposition : No result

required_flip_dependence : # 77. Stress Test — Assessment Flip

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
ASSESSMENT_FLIP_RISK : 
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
> | `INSUFFICIENT_PEER_DATA` | **FLAG-LEVEL ONLY** | فقط در `valuation_risk_flags` صادر می‌شود (`engine.py:165`)، نه به‌عنوان severity-bearing alert. آیا این برای «قابلیت Alert» کافی است، بخشی از تصمیم D8 است. |
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


valuation_driver_ranking :
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