بر اساس بررسی کامل سند جدید **PROMPT.md** (تحت عنوان **P54 — Correct Stage 7 Historical Parameter Selection (D9)**) و تطبیق آن با فایل‌های منابع پروژه (`07_Stage7_Valuation.md`، `stepsForStage7.md`، `parameters.py`، `engine.py` و `test_stage7_valuation.py`)، تحلیل فنی، طرح تغییرات و دستورالعمل اجرایی به شرح زیر ارائه می‌شود:

---

## ۱. تحلیل مسئله D9 و تغییرات مورد نیاز کد

### **علت عدم تکمیل D9 در وضعیت فعلی**
در پیاده‌سازی موجود، در صورتی که انتخاب پارامتر بر اساس تاریخ انجام شود، متاداده خروجی همچنان مقدار زیر را به‌صورت هاردکدشده گزارش می‌کند:
```python
"data_cutoff_used_for_parameter_selection": False
```
علت این مسئله آن است که موتور ارزش‌گذاری (`engine.py`) تاریخ قطع داده‌ها (`data_cutoff_datetime`) را پیش از انتخاب مجموعه پارامترها تعیین نمی‌کرد و فرآیند انتخاب پارامتر صرفاً متکی بر `parameter_as_of` ورودی (یا مسیر پیش‌فرض Genesis) بود.

### **منطق جدید اصلاح D9 طبق PROMPT.md**
1. **تعیین تاریخ قطع داده‌ها (Governing Timestamp):** پیش از فراخوانی انتخاب پارامتر، تاریخ قطع داده‌ها به‌صورت زیر مشخص می‌شود:
   \\[\text{effective\_cutoff} = \text{normalize\_datetime}(\text{data\_cutoff\_datetime} \text{ or } \text{forecast\_result.data\_cutoff\_datetime})\\]
2. **مدیریت تعارض `parameter_as_of` با Cutoff:** اگر فراخواننده هم `parameter_as_of` و هم `data_cutoff_datetime` را ارسال کند و این دو تاریخ با یکدیگر تعارض داشته باشند (`normalize_datetime(parameter_as_of) != effective_cutoff`)، سیستم باید با خطای صریح `ValueError` درخواست را رد کند و اجازه انتخاب خاموش پارامتر با تاریخ متناقض را ندهد.
3. **انتخاب پارامتر بر اساس Cutoff:** در صورت وجود یک ثبت پارامتر تاریخ‌دار (Dated Registry)، انتخاب نسخه پارامتر با `resolve_parameter_set_as_of(effective_cutoff, registry)` انجام می‌شود.
4. **متاداده صادقانه:** 
   * اگر نسخه پارامتر تاریخ‌دار بر اساس `effective_cutoff` انتخاب شد:
     * `data_cutoff_used_for_parameter_selection` برابر `True` قرار می‌گیرد.
     * `as_of_source` برابر `"VALUATION_DATA_CUTOFF"` ثبت می‌شود.
     * `point_in_time_selection_applied` برابر `True` ثبت می‌شود.
   * اگر مسیر قدیمی Genesis (بدون تاریخ) استفاده شد:
     * `data_cutoff_used_for_parameter_selection` برابر `False` باقی می‌ماند.
     * `point_in_time_selection_applied` برابر `False` ثبت می‌شود.

---

## ۲. فایل‌های مجاز برای تغییر

مطابق الزامات صریح پرامپت، **تنها فایل‌های زیر** مجاز به تغییر هستند:
1. **`src/valuation/parameters.py`:** به‌روزرسانی تابع `select_parameter_set_for_valuation` جهت دریافت `data_cutoff_datetime` و اعمال منطق بررسی تعارض و ثبت صادقانه متاداده.
2. **`src/valuation/engine.py`:** تعیین اولیه‌ی `data_cutoff_datetime` و ارسال آن به تابع انتخاب پارامتر در `ValuationEngine.calculate_valuation`.
3. **`src/tests/test_stage7_valuation.py`:** افزودن تست‌های واحد هدفمند جهت پوشش سناریوهای D9.

*تذکر: هیچ فایل دیگری (از جمله فایل‌های مشخصات، گزارش‌ها یا سایر ماژول‌ها) تغییر نخواهد کرد.*

---

## ۳. محدودیت‌های باقی‌مانده (D9 Limitations)

* **عدم وجود تاریخ در مجموعه Genesis:** مجموعه پارامترهای پیش‌فرض اولیه (Genesis) فاقد `effective_from` بوده و همچنان بدون تاریخ می‌ماند. برای اجرای قدیمی (Legacy) با این مجموعه، ادعای اعتبار زمانی (PIT) نمی‌شود و `data_cutoff_used_for_parameter_selection=False` ثبت می‌گردد.
* **نیاز به ثبت تاریخ برای نسخه پارامترها در آینده (R8):** انتخاب پارامتر مبتنی بر Cutoff تنها زمانی کار می‌کند که نسخه‌های تاریخ‌دار در `ParameterRegistry` ثبت شده باشند.

---

## ۴. بیانیه عدم اجرای تست

> **توجه:** تست‌ها توسط این هوش مصنوعی اجرا نشده‌اند. تمام اعتبارسنجی‌ها پس از اعمال تغییرات توسط کاربر در محیط محلی صورت خواهد گرفت.

---

## ۵. پرامپت آماده برای ارسال به Claude

می‌توانید متن زیر را کپی کرده و مستقیماً برای Claude ارسال کنید تا تغییرات را روی کد اعمال کند:

```text
لطفاً بر اساس سند PROMPT.md (مربوط به P54 - Correct Stage 7 Historical Parameter Selection / D9)، تغییرات زیر را دقیقاً و به‌صورت حداقل در ۳ فایل تعیین‌شده اعمال کن:

۱. فایل src/valuation/parameters.py:
- تابع select_parameter_set_for_valuation را طوری به‌روزرسانی کن که علاوه بر parameter_registry و parameter_as_of، ورودی data_cutoff_datetime را نیز بپذیرد.
- اگر هم parameter_as_of و هم data_cutoff_datetime ارسال شده باشند و پس از normalize_datetime متناقض باشند (نابرابر باشند)، خطای ValueError صریح صادر شود.
- اگر یک registry تاریخ‌دار یا درخواست انتخاب اسناد تاریخ‌دار وجود داشته باشد، تاریخ قطع داده‌ها (data_cutoff_datetime) به‌عنوان Governing Timestamp استفاده شود.
- متاداده متناسب با نحوه انتخاب تنظیم شود: اگر بر اساس data_cutoff_datetime انتخابی صورت گرفت، data_cutoff_used_for_parameter_selection=True و as_of_source="VALUATION_DATA_CUTOFF" ثبت شود.
- مسیر Legacy Genesis همچنان point_in_time_selection_applied=False و data_cutoff_used_for_parameter_selection=False را به شکل صادقانه گزارش کند.

۲. فایل src/valuation/engine.py:
- در ابتدای calculate_valuation، ابتدا data_cutoff_datetime استخراج و نرمال‌سازی شود (data_cutoff_datetime = normalize_datetime(data_cutoff_datetime or forecast_result.data_cutoff_datetime)).
- فراخوانی select_parameter_set_for_valuation با ارسال data_cutoff_datetime انجام شود.
- مقدار data_cutoff_used_for_parameter_selection در خروجی parameter_selection مستقیم از selection_meta خوانده شود و دیگر روی False هاردکد نباشد.

۳. فایل src/tests/test_stage7_valuation.py:
تست‌های رگرسیون زیر را اضافه کن:
- test_p54_parameter_selection_governed_by_data_cutoff: انتخاب موفق نسخه تاریخ‌دار بر اساس data_cutoff_datetime و تایید True بودن data_cutoff_used_for_parameter_selection.
- test_p54_exact_effective_from_boundary: تایید پذیرش exact boundary (تاریخ effective_from مساوی cutoff).
- test_p54_future_effective_version_rejected: رد نسخه‌ای که effective_from آن بعد از cutoff است.
- test_p54_conflicting_parameter_as_of_and_cutoff_rejected: صدور ValueError در صورت تعارض parameter_as_of و cutoff.
- test_p54_legacy_genesis_path_reports_false_for_pit: تایید False بودن متاداده PIT برای مسیر Genesis.
- test_p54_deterministic_repeated_selection: تایید رفتار قطعی در اجراهای مکرر.

نکات مهم:
- هیچ فرمول مالی، آستانه، Alert یا منطق ارزش‌گذاری تغییر نکند.
- فایل‌های دیگر را ویرایش نکن.
```

---

## ۶. دستور اجرای تست در PowerShell

پس از اعمال تغییرات توسط Claude، دستورات زیر را در PowerShell اجرا کنید:

```powershell
# ۱. اجرای تست‌های هدفمند Stage 7 جهت بررسی حل D9
python -m pytest src/tests/test_stage7_valuation.py -q

# ۲. اجرای هم‌زمان تست‌های Stage 7 و Stage 9 جهت سنجش عدم بروز رگرسیون
python -m pytest src/tests/test_stage7_valuation.py src/tests/test_stage9_decision.py -q

# ۳. اجرای کلیه تست‌های پروژه
python -m pytest src/tests -q
```

---

💡 **پیشنهاد گام بعدی:** پرامپت بخش ۵ را برای Claude ارسال کنید، سپس خروجی اجرای دستور PowerShell بالا را برای بررسی نهایی در پاسخ بعدی قرار دهید.