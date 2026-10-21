
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

