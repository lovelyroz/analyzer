# Report P63
### گزارش ممیزی نسخه بوم تاریخی پارامترها (P54) قبل از یکپارچه‌سازی Stage 7

این گزارش تخصصی مهندسی، ارزیابی جامعی از مکانیزم انتخاب و نسخه‌بندی تاریخی پارامترها (موضوع مسئله P54) در ماژول ارزش‌گذاری Stage 7 پروژه `analyzer` ارائه می‌دهد. این گزارش بدون ایجاد تغییر در کد، اجرا یا تغییر اسناد، بر اساس ممیزی دقیق کدهای سورس و مشخصات مالی تنظیم شده است.

---

### ۱. جمع‌بندی اجرایی (Executive Conclusion)

**پاسخ صریح:** بازیابی تاریخی پارامترها (Historical Parameter Resolution) در وضعیت فعلی سیستم **ناایمن (UNSAFE) و غیرقابل اثبات (NOT PROVABLE)** از روی شواهد موجود است.

**دلیل اصلی:**
1. ثبات‌بخش اصلی پارامترها (`DEFAULT_REGISTRY` در `src/valuation/parameters.py:263`) تنها شامل یک رکورد اولیه تحت عنوان `GENESIS_VERSION` (`version_key="STAGE7_V1/GENESIS"`) است.
2. مقدار تاریخ اعتبار این رکورد صریحاً برابر با `effective_from = None` (فاقد تاریخ اعتبار تاریخی) تنظیم شده است.
3. تابع انتخاب بر اساس تاریخ (`resolve_parameter_set_as_of`) به‌گونه‌ای طراحی شده که تمام رکوردهای فاقد تاریخ (از جمله نسخه Genesis) را از کاندیداهای انتخاب تاریخی حذف می‌کند. در نتیجه، هرگونه درخواست ارزش‌گذاری با مشخص کردن تاریخ پارامتر (`parameter_as_of`) منجر به صدور خطای صریح `LookupError` می‌شود (`zErrors.md`).
4. در سمت مقابل، اگر هیچ تاریخی ارسال نشود (`parameter_as_of=None`)، سیستم وارد حالت میراثی `FIXED_GENESIS_LEGACY` شده و ثابت‌های جاری کد را بدون بررسی صحت زمانی (Point-in-Time) اعمال می‌کند و پرچم `point_in_time_selection_applied=False` را ثبت می‌نماید.

بنابراین، سیستم هم‌اکنون بین دو حالت رفتار می‌کند: یا در درخواست‌های تاریخی با خطای `LookupError` متوقف می‌شود (Fail Closed)، یا در حالت میراثی ثوابت فعلی را بدون اثبات صحت تاریخی مصرف می‌کند.

---

### ۲. رفتار فعلی بر اساس شواهد کد (Evidence-Based Current Behavior)

#### ۱. توابع اصلی و رفتار آن‌ها:
* **`resolve_parameter_set_as_of`** (`src/valuation/parameters.py:263-294`):
  * **ورودی‌ها:** `as_of: Optional[datetime]`, `registry: ParameterRegistry = DEFAULT_REGISTRY`
  * **خروجی:** `ParameterSetVersion`
  * **رفتار:** ابتدا نرمال‌سازی تاریخ به UTC انجام می‌شود. اگر `as_of` برابر `None` باشد، خطای `LookupError` صادر می‌کند. سپس نسخه‌هایی را که `effective_from is not None` و `effective_from <= moment` هستند فیلتر می‌کند. اگر کاندیدایی یافت نشود، خطای `LookupError("No dated Stage 7 parameter version covers as_of=...")` صادر می‌گردد. در صورت وجود هم‌زمانی دقیق در جدیدترین تاریخ اعتبار، خطای `LookupError("Ambiguous...")` صادر می‌شود.
* **`resolve_parameter_set`** (`src/valuation/parameters.py:258-262`):
  * **ورودی‌ها:** `version_key: str`, `registry: ParameterRegistry = DEFAULT_REGISTRY`
  * **رفتار:** جستجوی دقیق بر اساس کلید نسخه (`version_key`). در صورت عدم وجود کلید، خطای `KeyError` صادر می‌کند (بدون Fallback خاموش).
* **`select_parameter_set_for_valuation`** (`src/valuation/parameters.py:350-380`):
  * **حالت ۱ (`FIXED_GENESIS_LEGACY`):** اگر هر دو آرگومان `parameter_registry` و `parameter_as_of` برابر `None` باشند، نسخه `live_genesis_parameter_set()` فراخوانی شده و متادیتای `point_in_time_selection_applied: False` ثبت می‌شود.
  * **حالت ۲ (`AS_OF_EFFECTIVE_DATED`):** اگر یکی از آرگومان‌ها ارسال شود، تابع `resolve_parameter_set_as_of` فراخوانی می‌شود که در صورت عدم وجود رکوردهای تاریخ‌دار در ثبت‌کننده، به خطای `LookupError` می‌انجامد.

#### ۲. منبع واقعی رکوردهای پارامتر:
رکوردهای پارامتر مستقیماً از ثابت‌های موجود در ماژول `src/valuation/parameters.py` (مانند `SCENARIO_WEIGHTS`, `VALUATION_THRESHOLDS`, `CONFIDENCE_THRESHOLDS`, `RISK_THRESHOLDS`, `ALERT_THRESHOLDS`, `SENSITIVITY_PERTURBATION`, `MIN_INDUSTRY_PEERS`) به‌صورت برنامه‌ای در تابع `_genesis_records()` ساخته می‌شوند. هیچ جدول پایگاه‌داده، فایل Seed یا دایرکتوری جداگانه‌ای برای نگهداری نسخه پارامترها وجود ندارد.

#### ۳. متادیتای زمانی (Temporal Metadata):
* `ParameterRecord` شامل فیلدهای `parameter_name`, `parameter_value`, `effective_from: Optional[datetime]`, `description` است.
* `ParameterSetVersion` شامل `model_version`, `version_key`, `effective_from: Optional[datetime]`, `records` است.
* فیلد `effective_end` در ساختار داده وجود ندارد؛ بازه اعتبار به‌صورت باز از `effective_from` تا زمان ثبت نسخه بعدی محاسبه می‌شود.

#### ۴. نحوه ارتباط پارامتر با خروجی ارزش‌گذاری:
موتور ارزش‌گذاری (`ValuationEngine.calculate_valuation` در `src/valuation/engine.py:215-219`) مقادیر مصرف‌شده را در فیلد `metadata` خروجی `ValuationResult` ثبت می‌کند:
* `metadata["parameter_set_version"]`: کلید نسخه مانند `"STAGE7_V1/GENESIS"` یا `"TEST/V1"`.
* `metadata["parameter_snapshot"]`: اسنپ‌شات کامل از ۳۸ پارامتر مصرف‌شده.
* `metadata["parameter_selection"]`: مشخصات حالت انتخاب (`mode`, `point_in_time_selection_applied`, `as_of_requested`, `effective_from` و ...).
* `metadata["parameter_consumption"]`: اسامی پارامترهای مصرف‌شده (`consumed_names`) و پارامترهای ثبت‌شده اما مصرف‌نشده (`recorded_not_consumed_names`).

---

### ۳. مدل داده‌های زمانی و ارزیابی Point-in-Time

در سنجش صحت زمانی پارامترها، سه مفهوم به تفکیک بررسی شدند:

1. **زمان اعتبار عملیاتی (Effective Time):** زمانی که پارامتر از نظر مالی و کسب‌وکار معتبر شناخته می‌شود (`effective_from`). در نسخه `GENESIS_VERSION` این فیلد برابر `None` است و بنابراین فاقد زمان اعتبار تاریخی است.
2. **زمان ثبت / آگاهی سیستم (Recorded/Knowledge Time):** سیستم فاقد قابلیت Bitemporal است و فیلدی برای ثبت زمان دقیق درج یا آگاهی سیستم از پارامتر در دیتابیس/کد وجود ندارد.
3. **نقطه قطع تحلیل (Analysis Cutoff / `data_cutoff_datetime`):** تاریخ پایانی که داده‌های شرکت و گزارش‌ها تا آن زمان مجاز به ورود هستند.

**شکاف‌های شناسایی‌شده در صحت زمانی (PIT):**
* تابع `select_parameter_set_for_valuation` تاریخ `parameter_as_of` را به‌صورت مجزا از ورودی دریافت می‌کند و آن را به طور خودکار از روی `data_cutoff_datetime` نگاشت نمی‌کند.
* در حالت میراثی (`FIXED_GENESIS_LEGACY`)، حتی اگر `data_cutoff_datetime` متعلق به چند سال قبل (مثلاً ۲۰۲۰) باشد، سیستم ثابت‌های فعلی کد (سال ۲۰۲۶) را اعمال می‌کند که این امر نقض صریح اصل Point-in-Time است.
* در حالت انتخابی (`AS_OF_EFFECTIVE_DATED`)، به دلیل عدم وجود تاریخ اعتبار برای Genesis، امکان ارزش‌گذاری تاریخی وجود ندارد و سیستم با `LookupError` متوقف می‌شود.

---

### ۴. ارزیابی پوشش تست‌ها (Test Coverage Assessment)

تست‌های مربوط به نسخه پارامترها در فایل `src/tests/test_stage7_valuation.py` بررسی شدند:

* **تست‌های اثبات‌شده در کد:**
  1. `test_p33_genesis_snapshot_matches_live_constants` (خط ۱۷۳۰ به بعد): اثبات می‌کند که اسنپ‌شات Genesis دقیقاً شامل ۳۸ پارامتر و مطابق با ثابت‌های جاری کد بوده و `effective_from is None` است.
  2. `test_p33_resolve_exact_key_and_missing_raises`: اثبات می‌کند جستجوی کلید دقیق کار می‌کند و کلید ناموجود خطای `KeyError` می‌دهد.
  3. `test_p33_as_of_without_dated_records_raises`: اثبات می‌کند که فراخوانی `resolve_parameter_set_as_of` روی `DEFAULT_REGISTRY` خطای `LookupError` صادر می‌کند.
  4. `test_p33_as_of_selection_mechanics`: مکانیسم انتخاب بر اساس تاریخ را با استفاده از یک ثبت‌کننده ساختگی (`_p33_synthetic_registry`) شامل نسخه‌های `TEST/V1` و `TEST/V2` تست می‌کند.
  5. `test_p33_as_of_overlap_raises_ambiguity`: اثبات می‌کند تاریخ‌های اعتبار هم‌زمان منجر به خطای عدم قطعیت (`Ambiguous`) می‌شوند.
  6. `test_p35_legacy_path_provenance_is_truthful_and_unchanged`: صحت متادیتای حالت میراثی و شفافیت عدم تایید PIT را اثبات می‌کند.
  7. `test_p35_as_of_selection_governs_calculation_and_snapshot_matches`: اثبات می‌کند که در صورت تعریف ثبت‌کننده دارای تاریخ، تغییر پارامترها بر روی محاسبات و خروجی وضعیت ارزش‌گذاری اثر مستقیم می‌گذارد.
  8. `test_p35_missing_or_ambiguous_as_of_selection_fails_closed`: رفتار Fail-Closed را در حالت عدم وجود نسخه معتبر تأیید می‌کند.

* **تست‌های مفقود (Missing Coverage):**
  * هیچ تستی برای بازیابی پارامترهای تاریخی از پایگاه‌داده وجود ندارد (زیرا لایه ماندگاری برای پارامترها پیاده‌سازی نشده است).
  * هیچ تستی برای پیوند خودکار بین `data_cutoff_datetime` و `parameter_as_of` در لایه سرویس وجود ندارد.

---

### ۵. مقایسه گزینه‌های اصلاحی (Remediation Options Comparison)

| گزینه | پیش‌نیازها | ریسک‌های مالی و PIT | پیامدهای سازگاری | متادیتای ممیزی موردنیاز | حکم ممیزی |
|---|---|---|---|---|---|
| **۱. افزودن تاریخ به رکورد موجود Genesis** | اختصاص یک تاریخ فرضی (مثلاً ۲۰۲۰-۰۱-۰۱) به Genesis | **بسیار بالا:** انتساب فرضی تاریخ اعتبار به ثابت‌های جاری بدون مصوبه رسمی، ادعای کاذب PIT ایجاد می‌کند. | باعث سبز شدن ظاهر تست‌های تاریخ‌دار می‌شود. | ثبت تاریخ فرضی در `effective_from` | **رد می‌شود** (با سیاست عدم حدس حقایق تاریخی منافات دارد). |
| **۲. تکمیل نسخه‌بندی تاریخ‌دار صریح با رکورد R8** | تصویب رسمی پارامترهای پایه سال ۲۰۲۶ توسط مالک سیستم با تاریخ `2026-01-01` | **پایین:** صحت مالی حفظ شده و تاریخ اعتبار مشخصات رسماً ثبت می‌شود. | کاملاً با مکانیسم موجود `ParameterRegistry` سازگار است. | `effective_from: "2026-01-01T00:00:00Z"` | **توصیه می‌شود** (مسیر استاندارد مهندسی). |
| **۳. توقف صریح (Fail Closed) برای تحلیل تاریخی** | حفظ رفتار فعلی در عدم انتخاب پارامتر تاریخی تا زمان ارائه ثبت‌کننده معتبر | **صفر:** از محاسبات گمراه‌کننده تاریخی با پارامترهای نامعتبر جلوگیری می‌کند. | در صورت ارسال `parameter_as_of` بدون دیتابیس/ثبت‌کننده تاریخ‌دار، خطای `LookupError` می‌دهد. | ثبت علل توقف در متادیتای خطا | **توصیه می‌شود** (حالت امن فعلی). |
| **۴. الزامی کردن پاس دادن ثبت‌کننده یا پذیرش صریح حالت میراثی** | فراخواننده باید یا ثبت‌کننده تاریخ‌دار بدهد یا حالت `FIXED_GENESIS_LEGACY` را بپذیرد | **پایین:** شفافیت کامل برای فراخواننده ایجاد می‌کند. | نیاز به تنظیم شفاف ورودی‌های سرویس دارد. | `point_in_time_selection_applied: False` | **پایین‌ترین ریسک عملیاتی**. |

---

### ۶. اقدام بعدی پیشنهادی (Recommended Next Action)

**کوچک‌ترین اقدام امن:**
ثبت حداقل یک نسخه پارامتر تاریخ‌دار معتبر و رسمی برای سال ۲۰۲۶ (مثلاً `version_key = "STAGE7_V1/INITIAL_2026"` با `effective_from = datetime(2026, 1, 1, tzinfo=timezone.utc)`) در `DEFAULT_REGISTRY` پس از تایید مالک سیستم/مشخصات.

* **پیش‌نیازها:** تایید رسمی که مقادیر ثابت فعلی کد، از تاریخ اول ژانویه ۲۰۲۶ معتبر و قابل اتکا هستند.
* **غیر‌اهداف (Non-goals):**
  * عدم حدس زدن تاریخ‌های اعتبار برای قبل از سال ۲۰۲۶.
  * عدم بازطراحی فایل `src/valuation/engine.py`.
  * عدم ایجاد اسکیما یا جداول غیرضروری پایگاه‌داده برای پارامترها در این مرحله.

---

### ۷. معیارهای پذیرش (Acceptance Criteria)

تکلیف P54 تنها زمانی حل‌شده تلقی می‌شود که شرایط عینی زیر برقرار باشد:
1. ثبت‌کننده پیش‌فرض (`DEFAULT_REGISTRY`) حداقل شامل یک نسخه پارامتر با `effective_from` معتبر و غیر `None` باشد.
2. فراخوانی `resolve_parameter_set_as_of(datetime(2026, 1, 1, tzinfo=timezone.utc))` بدون صدور `LookupError` نسخه معتبر را بازگرداند.
3. در صورت فراخوانی سرویس ارزش‌گذاری با `parameter_as_of` معتبر، متادیتای خروجی شامل `mode: "AS_OF_EFFECTIVE_DATED"` و `point_in_time_selection_applied: True` باشد.
4. تمام ۷۵ تست موجود در `src/tests/test_stage7_valuation.py` بدون خطا پاس شوند.

---

### ۸. اثر بر یکپارچه‌سازی Stage 7 (Stage 7 Integration Impact)

* **موارد مسدودشده:**
  * سرویس `calculate_valuation_as_of_jalali` در `src/valuation/service.py` به `ValuationEngine` متصل است. اگر فراخواننده قصد داشته باشد نسخه پارامترها را بر اساس تاریخ جلالی/تاریخ قطع انتخاب کند و `parameter_as_of` را ارسال نماید، به دلیل نبود رکورد تاریخ‌دار R8 با `LookupError` متوقف می‌شود.
  * در صورتی که `parameter_as_of` ارسال نشود، ارزش‌گذاری انجام می‌شود اما متادیتای خروجی صریحاً اعلام می‌کند که انتخاب Point-in-Time بر روی پارامترها اعمال نشده است (`FIXED_GENESIS_LEGACY`).

* **آنچه این ممیزی اثبات نمی‌کند:**
  * این ممیزی هیچ‌گونه کدی برای استخراج داده‌های Stage 3 یا Stage 8 پیاده‌سازی نمی‌کند.
  * هیچ مدلی برای ذخیره‌سازی خروجی نهایی تصمیم در Stage 9 ایجاد نمی‌کند.

---

### ۹. فایل‌های بررسی‌شده (Files Inspected)

۱. `stepsForStage7.md` (برنامه اجرایی و یافته‌های P48)  
۲. `reply.md` / `temp_report.md` (گزارش‌های ممیزی P62 و خطوط لوله)  
۳. `src/valuation/parameters.py` (تعریف پارامترها، ثبت‌کننده و توابع انتخاب)  
۴. `src/valuation/engine.py` (نحوه فراخوانی و مصرف پارامترها در `calculate_valuation`)  
۵. `src/valuation/service.py` (مرز سرویس ارزش‌گذاری جلالی)  
۶. `src/valuation/schema.py` (ساختار داده‌ای `ValuationResult`)  
۷. `src/valuation/models.py` (مدل‌های محاسباتی ارزش‌گذاری)  
۸. `src/tests/test_stage7_valuation.py` (تست‌های مربوط به P33 و P35 در خصوص نسخه‌بندی پارامترها)  
۹. `07_Stage7_Valuation.md` (بخش ۶۵ — مشخصات قفل‌شده نسخه‌بندی پارامترها)  
۱۰. `zErrors.md` (جزئیات تریس‌بک خطای `LookupError`)  

---

### ۱۰. تأییدیه صریح عدم تغییر کد و عدم اجرای تست‌ها (Execution Confirmation)

**بدین‌وسیله صریحاً تأیید می‌شود که:**
1. هیچ‌یک از فایل‌های سورس برنامه، تست‌ها، تنظیمات، مشخصات یا اسناد برنامه‌ریزی پروژه ویرایش یا تغییر داده نشده‌اند.
2. هیچ دستور تستی (pytest)، کد برنامه‌نویسی، تغییر دیتابیس، مایگریشن یا فرایند CI توسط سیستم/Agent اجرا نگردیده است.
3. این گزارش تماماً خروجی تحلیل و ممیزی کدهای موجود پروژه بر اساس قوانین P63 می‌باشد.

---
💡 *آیا پس از بررسی این گزارش ممیزی، تمایل دارید درباره ثبت اولین نسخه تاریخ‌دار پارامتر برای سال ۲۰۲۶ (جهت رفع محدودیت P54) یا پرداختن به سایر پیش‌نیازهای یکپارچه‌سازی تصمیم‌گیری کنیم؟*