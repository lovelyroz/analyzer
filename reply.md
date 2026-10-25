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

# P64 
### گزارش ممیزی شواهد معتبر برای تاریخ‌های اعتبار پارامترهای Stage 7 (P64)

این گزارش، ممیزی فنی و مستند شواهد پروژه `analyzer` در خصوص تاریخ اعتبار (Effective Date) و منشأ پارامترهای Stage 7 است که بر اساس الزامات پرامپت **P64** و بدون انجام هیچ‌گونه تغییر در کد، اجرا یا تغییر اسناد تنظیم شده است.

---

### ۱. جمع‌بندی اجرایی (Executive Conclusion)

**پاسخ صریح:** هیچ سند یا مشخصه رسمی و قفل‌شده‌ای در پروژه، **تاریخ اعتبار (Effective Date)** برای پارامترهای نسخه Genesis یا مقادیر عددی ثابت فعلی تعیین نکرده است.

1. **تاریخ پیشنهادی `2026-01-01T00:00:00Z` از نظر مشخصات فاقد پشتیبانی (UNSUPPORTED)** است. این تاریخ تنها یک مثال پیشنهادی در گزارش P63 بوده و در هیچ‌یک از اسناد رسمی مرجع (مانند `07_Stage7_Valuation.md` یا `stepsForStage7.md`) تصویب یا تعیین نگردیده است.
2. **مقادیر پارامترهای موجود در کد نیز از نظر منشأ تاریخی فاقد تصویب (UNRATIFIED)** هستند. مشخصات پروژه صریحاً حاشیه‌نویسی کرده که مقادیر موجود در `src/valuation/parameters.py` صرفاً ثوابت موتور کد هستند و توسط مشخصات ارزش‌گذاری تأیید (Ratify) نشده‌اند (تکلیف حل‌نشده D9).
3. **پیاده‌سازی فعلی رفتار Fail-Closed کاملاً صحیحی دارد**: هنگام درخواست ارزش‌گذاری تاریخی با `parameter_as_of` در صورتی که رکورد تاریخ‌دار R8 وجود نداشته باشد، به جای حدس زدن تاریخ یا Fallback خاموش به ثوابت جاری، صریحاً خطای `LookupError` صادر می‌کند (`zErrors.md`).
4. **اقدام فوری:** حفظ رفتار Fail-Closed فعلی و درخواست مصوبه/سیاست صریح از مالک سیستم برای تعیین تاریخ اعتبار پارامترها (Decision D9).

---

### ۲. شواهد مشخصات مرجع (Authoritative Specification Evidence)

بررسی دقیق سند قفل‌شده مشخصات (`07_Stage7_Valuation.md`) و سند برنامه اجرایی (`stepsForStage7.md`) شواهد زیر را نشان می‌دهد:

* **تاریخ اعتبار نسخه Genesis:** 
  * در بخش ۶۵ سند `07_Stage7_Valuation.md` فقط فیلدهای اسکیما شامل `model_version, parameter_name, parameter_value, effective_from, description` تعریف شده‌اند، اما **هیچ مقدار عددی یا تاریخی** برای `effective_from` تعیین نشده است.
  * در کد `src/valuation/parameters.py:260-269` نیز رکورد Genesis صریحاً با `effective_from = None` ثبت شده و در Docstring آن درج شده است: *"effective_from dates for the existing constants (unknowable from any evidence — inventing them is forbidden, so genesis records carry None)"*.
* **تاریخ اعتبار اولیه ۲۰۲۶:** 
  * در هیچ‌یک از اسناد `07_Stage7_Valuation.md` یا `stepsForStage7.md` به تاریخ `2026-01-01` به عنوان تاریخ اعتبار پارامترها اشاره نشده است.
* **الزامات تصویب و منشأ (Provenance):** 
  * در حاشیه‌نویسی‌های مستند مشخصات (`07_Stage7_Valuation.md` بخش‌های ۴۷، ۴۸ و ۸۵) صریحاً قید شده است: *"این رفتار پیاده‌سازی است، نه سیاست تأییدشده توسط مشخصات... تصمیم D9 (ثبت‌کننده پارامتر و مکانیزم انتخاب نسخه) هنوز حل‌نشده است"*.
* **الزامی بودن انتخاب تاریخی (Historical Selection Requirement):** 
  * بر اساس اصل ۱۷ و ۲۰ در بخش ۸۷ سند `07_Stage7_Valuation.md` و سیاست D9 در `stepsForStage7.md` (بخش ۲)، حدس زدن تاریخ اعتبار یا منشأ پارامترها صریحاً ممنوع است: *"شناسه نسخه مدل معادل تاریخچه کامل پارامترها نیست؛ تاریخ اعتبار یا منشأ پارامترها حدس زده نشود"*.
* **رفتار هنگام عدم وجود نسخه تاریخی:** 
  * طبق سیاست Fail-Closed قیدشده در مشخصات و D9، در صورت عدم وجود نسخه تاریخ‌دار، سیستم نباید به‌صورت خاموش به ثوابت جاری Fallback کند.

---

### ۳. ارزیابی منشأ تاریخ اعتبار و مقادیر پارامترها (Effective-Date & Provenance Assessment)

* **منشأ مقادیر فعلی:** ۳۸ پارامتر موجود در کد مستقیماً از ثابت‌های متغیر در `src/valuation/parameters.py` (مانند `VALUATION_THRESHOLDS`, `RISK_THRESHOLDS`, `ALERT_THRESHOLDS`) خوانده می‌شوند و به‌صورت برنامه‌ای در `_genesis_records()` بسته‌بندی شده‌اند (`parameters.py:262-269`).
* **عدم اتصال به تاریخ قطع داده‌ها (Cutoff Disconnection):** تابع `select_parameter_set_for_valuation` در `src/valuation/parameters.py:350-375` تاریخ `parameter_as_of` را مستقیماً از ورودی فراخواننده می‌گیرد و آن را از روی `data_cutoff_datetime` به‌طور خودکار استخراج یا حدس نمی‌زند.

---

### ۴. طبقه‌بندی تاریخ `2026-01-01T00:00:00Z` و مقادیر پارامترها

| موضوع مورد ارزیابی | طبقه‌بندی (Classification) | دلیل فنی و مستند |
|---|---|---|
| **تاریخ اعتبار `2026-01-01T00:00:00Z`** | **UNSUPPORTED (پشتیبانی‌نشده)** | هیچ سند مصوب، رکورد پایگاه‌داده یا تصمیم معمارانه‌ای این تاریخ را به عنوان تاریخ آغاز اعتبار پارامترها تعیین نکرده است. حضور این تاریخ در Fixture تست‌ها (`make_forecast()` در `test_stage7_valuation.py:104`) طبق قوانین P64 اثبات‌کننده تاریخ اعتبار نیست. |
| **اعتبار تاریخی مقادیر هاردکدشده فعلی از تاریخ فوق** | **UNSUPPORTED (پشتیبانی‌نشده)** | مقادیر هاردکدشده بر اساس حاشیه‌نویسی‌های بخش ۴۸ و ۸۵ در `07_Stage7_Valuation.md` و تعاریف `parameters.py:260-269` به عنوان "ثوابت تصویب‌نشده موتور" ثبت شده‌اند و هیچ مستندی معتبر بودن مالی آن‌ها را از ژانویه ۲۰۲۶ یا هر تاریخ دیگری اثبات نمی‌کند. |

---

### ۵. رفتار فعلی پیاده‌سازی و محدودیتهای باقیمانده Point-in-Time

1. **انتخاب تاریخی فقط از رکوردهای تاریخ‌دار:** 
   * تابع `resolve_parameter_set_as_of` در `src/valuation/parameters.py:271-294` فقط رکوردهایی را فیلتر می‌کند که `effective_from is not None` و `effective_from <= as_of` باشند.
2. **رفتار Fail-Closed:** 
   * در صورت عدم وجود رکورد تاریخ‌دار در ثبت‌کننده (مانند `DEFAULT_REGISTRY` که فقط شامل Genesis فاقد تاریخ است)، خطای صریح `LookupError("No dated Stage 7 parameter version covers as_of=...; historical selection requires R8-dated records")` صادر می‌شود (`zErrors.md` و `parameters.py:280-285`).
3. **حالت میراثی (Legacy Unverified Mode):** 
   * در صورتی که فراخواننده هر دو ورودی `parameter_registry` و `parameter_as_of` را `None` ارسال کند (`parameters.py:350-365`)، سیستم از ثابت‌های فعلی کد (`live_genesis_parameter_set()`) تحت حالت `FIXED_GENESIS_LEGACY` استفاده کرده و پرچم `point_in_time_selection_applied: False` به همراه هشدار صریح در متادیتای خروجی ثبت می‌کند: *"Undated genesis constants; temporal validity for historical valuation is NOT verified (R8/D9 pending)"*.
4. **ثبت متادیتای مصرف:** 
   * سیستم اسنپ‌شات کامل ۳۸ پارامتر مصرف‌شده و حالت انتخاب را در `ValuationResult.metadata` ثبت می‌کند (`engine.py:223-227`).
5. **تفکیک ثبت مقادیر با اثبات صحت تاریخی:** 
   * *ثبت متادیتای اسنپ‌شات:* شفاف‌سازی کامل درباره این‌که چه عددی در محاسبه استفاده شده است.
   * *اثبات صحت تاریخی:* نیازمند سند یا رکورد رگولاتوری/مالی تاریخ‌داری است که معتبر بودن آن عدد در آن نقطه از زمان را اثبات کند (که در حال حاضر وجود ندارد).

---

### ۶. تک‌اقدام بعدی پیشنهادی (Single Recommended Next Action)

**اقدام پیشنهادی:** **درخواست مصوبه صریح سیاستی/مدیریتی برای تعیین تاریخ اعتبار و تصویب مقادیر پارامترها (Option 2).**

* **علت منطقی:** از آنجا که هیچ سند پروژه یا داده منطقی در کد، تاریخ اعتبار اول ژانویه ۲۰۲۶ یا هر تاریخ دیگری را تصویب نکرده است، ایجاد یک رکورد تاریخ‌دار توسط Agent بدون مصوبه مالک سیستم، نقض صریح اصل عدم حدس حقایق تاریخی (D9 و P64) خواهد بود.
* **ترتیب اجرا:** 
  1. صادر کردن استعلام صریح از مالک سیستم/پروژه جهت تعیین و تصویب رسمی تاریخ شروع اعتبار (Effective Date) و مقادیر پارامترهای Stage 7 (تکلیف D9).
  2. تا زمان دریافت این مصوبه، سیستم رفتار امن فعلی (Fail-Closed در درخواست‌های تاریخی `parameter_as_of` و اعلام عدم تایید PIT در حالت میراثی) را حفظ نماید.

---

### ۷. معیارهای پذیرش عینی برای حل نهایی P54 (Acceptance Criteria)

تکلیف P54 زمانی کاملاً حل‌شده تلقی می‌شود که:
1. تصویب‌نامه رسمی شامل تاریخ اعتبار (مثلاً `2026-01-01T00:00:00Z`) و اسامی/مقادیر پارامترهای معتبر توسط مالک پروژه ارائه شده باشد.
2. یک نسخه پارامتر تاریخ‌دار (مانند `STAGE7_V1/INITIAL_2026`) با `effective_from` مشخص به `DEFAULT_REGISTRY` در `src/valuation/parameters.py` اضافه شود.
3. فراخوانی `resolve_parameter_set_as_of(datetime(2026, 1, 1, tzinfo=timezone.utc))` بدون صدور `LookupError` رکورد مربوطه را بازگرداند.
4. در محاسبات ارزش‌گذاری تاریخی با ارسال `parameter_as_of` معتبر، خروجی شامل `mode: "AS_OF_EFFECTIVE_DATED"` و `point_in_time_selection_applied: True` باشد.
5. تمامی تست‌های موجود در `src/tests/test_stage7_valuation.py` پاس شوند.

---

### ۸. فایل‌های بررسی‌شده (Files Inspected)

۱. `PROMPT.md`: الزامات پرامپت P64  
۲. `stepsForStage7.md`: بخش ۲ (سیاست‌های D7 و D9)، بخش ۳ (مرحله ۵ - نسخه‌بندی تاریخی پارامترها)  
۳. `reply.md` / `temp_report.md`: گزارش ممیزی P63 و نتایج سابقه  
۴. `07_Stage7_Valuation.md`: بخش‌های ۳۵، ۴۷، ۴۸، ۶۴، ۶۵، ۸۵، ۸۷ (الزامات نسخه‌بندی و حاشیه‌نویسی‌های D9)  
۵. `src/valuation/parameters.py`: خطوط ۱ تا ۵۰ (ثابت‌ها)، خطوط ۲۶۰-۲۶۹ (`GENESIS_VERSION`)، خطوط ۲۷۱-۲۹۴ (`resolve_parameter_set_as_of`)، خطوط ۳۵۰-۳۸۰ (`select_parameter_set_for_valuation`)  
۶. `src/valuation/engine.py`: خطوط ۷۰-۷۵ (`calculate_valuation`)، خطوط ۲۲۳-۲۲۷ (`metadata`)  
۷. `src/valuation/service.py`: خطوط ۱۲-۶۸ (`calculate_valuation_as_of_jalali`)  
۸. `src/valuation/schema.py`: خطوط ۱-۵۰ (`ValuationResult`)  
۹. `src/tests/test_stage7_valuation.py`: خط ۱۰۴ (`make_forecast`)، خطوط ۱۷۳۰-۱۷۴۰ (`test_p33_genesis_snapshot_matches_live_constants`)، خطوط ۱۸۲۰-۱۸۳۰ (`test_p33_as_of_without_dated_records_raises`)، خطوط ۱۸۵۰-۱۹۱۰ (`test_p35_legacy_path_provenance`)  
۱۰. `zErrors.md`: تریس‌بک کامل خطای `LookupError` در اجرای pytest  

---

### ۹. تأییدیه صریح عدم تغییر کد و عدم اجرای تست‌ها (Execution Confirmation)

**بدین‌وسیله صریحاً تأیید می‌شود که:**
1. هیچ‌یک از فایل‌های سورس کد برنامه، تست‌ها، تنظیمات، مشخصات یا اسناد برنامه‌ریزی پروژه تغییر نکرده‌اند.
2. هیچ دستور تستی (pytest)، اسکریپت اجرایی، عملیات دیتابیس، مایگریشن یا فرایند CI در طول این ممیزی توسط Agent اجرا نشده است.
3. تمام نتایج این گزارش مستند بر ممیزی دقیق شواهد موجود در کدهای سورس پروژه می‌باشد.

---
# P65
### گزارش ممیزی حاکمیت پارامترهای Stage 7 (D9) — آماده‌سازی تصمیم‌گیری (P65)

این گزارش، خروجی ممیزی تخصصی و شواهد‌محور در خصوص **شکاف حاکمیت پارامترهای Stage 7 (تصمیم D9)** در پروژه `analyzer` است. این سند بر اساس الزامات **P65** و بدون اعمال هیچ‌گونه تغییر در کد، اسناد، مایگریشن‌ها یا اجرای تست‌ها تنظیم شده است.

---

### ۱. الزامات و شواهد تصمیم D9 (D9 Requirement and Evidence)

#### تعریف صریح D9 در اسناد مرجع:
* **در `stepsForStage7.md` (بخش ۲ - سیاست D9):**  
  *"شناسهٔ نسخهٔ مدل معادل تاریخچهٔ کامل پارامترها نیست؛ تاریخ اعتبار یا منشأ پارامترها حدس زده نشود."*
* **در `07_Stage7_Valuation.md` (بخش ۶۵):**  
  *"تمام آستانه‌های قابل تنظیم باید بیرون از منطق کد نگهداری و نسخه بوم شوند (`valuation_model_parameters` شامل `model_version, parameter_name, parameter_value, effective_from, description`)."*
* **در `07_Stage7_Valuation.md` (بخش‌های ۴۷، ۴۸ و ۸۵):**  
  آستانه‌های عددی موجود در کد (`src/valuation/parameters.py`) صرفاً ثوابت اولیه موتور هستند و توسط مشخصات مالی پروژه تأیید (Ratify) نشده‌اند.

#### آنچه D9 تضمین می‌کند:
D9 تضمین می‌کند که هر ارزشیابی انجام‌شده، پارامترهای مصرفی خود را از یک نسخهٔ مشخص، تاریخ‌دار و دارای **منشأ و تاییدیه رسمی (Provenance & Approval)** دریافت کرده است و سیستم به‌صورت خاموش ثوابت جاری کد را به جای مقادیر معتبر تاریخی جایگزین نمی‌کند.

#### تفکیک الزامات فنی و تصمیمات مالی/کسب‌وکار:
1. **الزامات فنی پیاده‌سازی‌شده (Technical Implementation Requirements):**
   * مکانیسم ثبت‌کننده (`ParameterRegistry`)، جستجوی کلید دقیق (`resolve_parameter_set`)، انتخاب تاریخ‌دار (`resolve_parameter_set_as_of`) و ساختار شکست صریح (Fail-Closed) با خطای `LookupError` (`src/valuation/parameters.py:271-294`).
   * انجماد غیرقابل‌تغییر پارامترهای مصرفی (`ConsumedParameters`) و ثبت اسنپ‌شات کامل ۳۸ پارامتر در متادیتای خروجی `ValuationResult` (`src/valuation/engine.py:228-232`).
2. **تصمیمات مالی و سیاستی حل‌نشده (Financial / Business Decisions Required):**
   * تصویب/تأیید مالی ۳۸ مقدار عددی پارامترهای موجود.
   * تعیین و تصویب تاریخ اعتبار رسمی (`effective_from`) برای نخستین نسخه پارامترها.
   * تعیین سیاست پوشش تاریخی (آیا پارامترهای مصوب برای تاریخ‌های گذشته نیز معتبرند یا خیر).

#### معیارهای پذیرش قابل سنجش فعلی در برابر معیارهای نیازمند مصوبه:
* **قابل سنجش در حال حاضر:** رفتار Fail-Closed هنگام نبود نسخه تاریخ‌دار؛ تطابق اسنپ‌شات متادیتا با مقادیر مصرف‌شده واقعی؛ عدم نشت تغییرات متغیرهای سراسری به محاسبه.
* **نیازمند مصوبه مالک پروژه:** سبز شدن تست‌های انتخاب تاریخی پارامتر در `DEFAULT_REGISTRY` بدون صدور `LookupError`؛ اثبات صحت Point-in-Time برای ارزشیابی‌های تاریخی.

#### بررسی الزام زمانی Bitemporal (Effective Time vs Knowledge Time):
مشخصه قفل‌شده `07_Stage7_Valuation.md` (بخش ۶۵) تنها فیلد زمانی **`effective_from` (زمان اعتبار اقتصادی)** را تعریف کرده است. مشخصات پروژه درباره **Knowledge/Recorded Time** (زمان آگاهی یا ثبت در سیستم) ساکت است. بنابراین، D9 تنها الزامی بر روی **نسخه‌بندی تاریخ‌دار اعتبار (`effective_from`)** دارد و فرض الزام بایتامپورال بدون سند صریح ممنوع است.

---

### ۲. ماتریس تصمیم‌گیری (Decision Matrix — Questions A–F)

| پرسش سیاستی | وضعیت (Status) | شواهد کد / مشخصات (Evidence) | تصمیم و اقدام موردنیاز (Required Resolution) |
|---|---|---|---|
| **A. تصویب مقادیر پارامترها** | **Unresolved** | `07_Stage7_Valuation.md` بخش ۴۸؛ Docstringهای `src/valuation/parameters.py:269-274` ("spec-unratified D9"). | مالک پروژه باید ۳۸ مقدار عددی موجود را رسماً تصویب یا اصلاح کند. |
| **B. تعیین تاریخ اعتبار (`effective_from`)** | **Unresolved** | `src/valuation/parameters.py:265` (`effective_from = None` در Genesis)؛ ممیزی P63/P64 در `reply.md`. | مالک پروژه باید تاریخ و زمان دقیق شروع اعتبار (مانند `2026-01-01T00:00:00Z`) را تعیین کند. |
| **C. پوشش تاریخی (Historical Coverage)** | **Unresolved** | `stepsForStage7.md` سیاست D9؛ `src/valuation/parameters.py:276` (`LookupError` برای تاریخ‌های قبل از `effective_from`). | مالک پروژه باید مشخص کند آیا نسخه مصوب برای تاریخ‌های قبل از `effective_from` نیز معتبر است یا خیر. |
| **D. زمان آگاهی/ثبت (Knowledge Time)** | **Explicitly Specified (Not Required)** | `07_Stage7_Valuation.md` بخش ۶۵ فقط `effective_from` را تعریف می‌کند. اسکیما تک‌زمانی است. | نیازی به اقدام ندارد مگر این‌که مالک پروژه ارتقا به اسکیما Bitemporal را تصویب کند. |
| **E. سطح نسخه‌بندی (Set vs Parameter Level)** | **Partially Specified** | `07_Stage7_Valuation.md` بخش ۶۵ و `src/valuation/parameters.py` نسخه را در سطح مجموعه (Set-level) بسته‌بندی می‌کنند. | مالک پروژه باید تایید کند که نسخه‌بندی یکپارچه ۳۸ پارامتر در یک مجموعه (Set) کافی است. |
| **F. رفتار در عدم وجود نسخه تاریخی** | **Explicitly Specified (Fail-Closed)** | `src/valuation/parameters.py:276-290` (`LookupError`)؛ تست `test_p33_as_of_without_dated_records_raises`. | رفتار Fail-Closed فعلی به عنوان سیاست دائمی برای درخواست‌های تاریخ‌دار فاقد نسخه ثبت شود. |

---

### ۳. ارزیابی شواهد موردنیاز برای تصویب (Evidence Needed for Approval)

1. **مشخصات پروژه یا سیاست مالی امضاشده (Project Specification / Signed Policy):**  
   * *آنچه اثبات می‌کند:* صحت مالی، منطق کسب‌وکار و نیت معماران سیستم.  
   * *آنچه اثبات نمی‌کند:* عدم وجود باگ یا صحت رفتار کد در زمان اجرا.
2. **منبع مالی معتبر یا محاسبات مستندشده (Authoritative Financial Source):**  
   * *آنچه اثبات می‌کند:* توجیه اقتصادی آستانه‌ها و وزن‌های سناریو.  
   * *آنچه اثبات نمی‌کند:* نحوه پیاده‌سازی و مصرف آن در تابع‌های Python.
3. **ثابت‌ها و تست‌های پیاده‌سازی (Implementation Constants & Tests):**  
   * *آنچه اثبات می‌کند:* رفتار قطعی برنامه و پایداری کدهای سورس.  
   * *آنچه اثبات نمی‌کند:* **صحت مالی یا اعتبار تاریخی پارامترها.** (تست‌های boundary ثوابت فعلی کد را pin می‌کنند، نه انطباق با مشخصات مالی را).
4. **داده‌ها یا رکوردهای تاریخی منبع (Historical Source Data):**  
   * *آنچه اثبات می‌کند:* حقایق بازار در تاریخ‌های گذشته.  
   * *آنچه اثبات نمی‌کند:* سیاست‌های داخلی سیستم برای رتبه‌بندی یا آستانه‌های ریسک.
5. **تاییدیه صریح مالک پروژه (Project Owner Approval Statement):**  
   * *تنها ارکان لازم:* برای تبدیل ثوابت موقت کد به نسخه‌های رسمی و تاریخ‌دار معتبر.

---

### ۴. فرم ساختاریافته تصمیم‌گیری مالک پروژه (Project-Owner Decision Record Template)

این فرم برای تکمیل توسط مالک پروژه جهت حل نهایی D9 طراحی شده است:

```markdown
================================================================================
          PROJECT-OWNER DECISION RECORD: STAGE 7 PARAMETER GOVERNANCE (D9)
================================================================================

1. PARAMETER SET IDENTIFIER [Mandatory]:
   - Version Key: STAGE7_V1/INITIAL_2026 (or custom key)
   - Model Version: STAGE7_V1

2. APPROVAL OF PARAMETER VALUES [Mandatory]:
   [ ] Option A: Ratify the 38 current code constants in src/valuation/parameters.py as-is.
   [ ] Option B: Approve modified parameter values (attach schedule of changes).

3. APPROVED EFFECTIVE-FROM TIMESTAMP [Mandatory]:
   - Effective Date/Time (UTC): YYYY-MM-DDTHH:MM:SSZ (e.g., 2026-01-01T00:00:00Z)
   - Evidentiary Basis: [Specify formal policy / launch date reference]

4. HISTORICAL VALIDITY SCOPE [Mandatory]:
   [ ] Prospective Only: Valid strictly for valuation dates >= Effective Date.
   [ ] Historical Coverage: Approved for historical valuations back to YYYY-MM-DD.

5. POLICY FOR REQUESTS BEFORE EFFECTIVE DATE [Mandatory]:
   [ ] Fail Closed: Raise LookupError when parameter_as_of < Effective Date.
   [ ] Explicit Legacy Flag: Allow calculation with FIXED_GENESIS_LEGACY flag (PIT unverified).

6. VERSIONING GRANULARITY & TEMPORAL MODEL [Confirmed]:
   - Set-level versioning (38 parameters frozen together): [X] APPROVED
   - Single temporal dimension (effective_from only): [X] APPROVED

7. APPROVAL AUTHORITY & SIGN-OFF [Mandatory]:
   - Approving Authority (Name / Role): _______________________________________
   - Approval Date: YYYY-MM-DD
   - Reference / Document ID: __________________________________________________
================================================================================
```

---

### ۵. رفتار امن تا زمان اخذ تصمیمات (Safe Behavior Until Approval)

تا زمانی که تصمیمات فوق توسط مالک پروژه ابلاغ نشده است، سیستم باید رفتارهای زیر را بدون تغییر حفظ کند:

1. **مسیر انتخاب بر اساس تاریخ (`parameter_as_of` مقداردهی‌شده):**  
   مکانیسم انتخاب باید **کاملاً متوقف‌شونده (Fail-Closed)** باقی بماند. تابع `resolve_parameter_set_as_of` در صورت فراخوانی روی ثبت‌کننده پیش‌فرض (`DEFAULT_REGISTRY` که فقط شامل Genesis فاقد تاریخ است)، صریحاً خطای `LookupError` صادر می‌کند (`src/valuation/parameters.py:280-285`). **از انتصاب فرضی تاریخ اعتبار به Genesis یا Fallback خاموش اکیداً خودداری شود.**
2. **مسیر میراثی (`parameter_as_of=None` و `parameter_registry=None`):**  
   سیستم از ثوابت جاری کد استفاده کرده و حالت `FIXED_GENESIS_LEGACY` با پرچم `point_in_time_selection_applied: False` را ثبت می‌کند. متادیتای خروجی حاوی هشدار شفاف است:  
   *"Undated genesis constants; temporal validity for historical valuation is NOT verified (R8/D9 pending)"*.

---

### ۶. معیارهای خروج D9 و دروازه بعدی پیاده‌سازی (D9 Exit Criteria & Next Gate)

پیش از این‌که یکپارچه‌سازی تولیدی به ثبت‌کننده پارامترها تکیه کند، باید شرایط زیر احراز شوند:

1. **پیش‌نیازهای تصویب مالک پروژه:**  
   تکمیل و امضای "فرم ساختاریافته تصمیم‌گیری مالک پروژه" (بخش ۴) شامل تصویب مقادیر و تعیین `effective_from`.
2. **پیش‌نیازهای مستندات و مشخصات:**  
   تغییر وضعیت D9 در سند `stepsForStage7.md` از `OPEN` به `RESOLVED` با ارجاع به سند تصمیم مصوب.
3. **تغییرات کد (تنها پس از اخذ مصوبه):**  
   افزودن نسخه پارامتر تاریخ‌دار جدید (مثلاً `STAGE7_V1/INITIAL_2026`) به `DEFAULT_REGISTRY` در `src/valuation/parameters.py`.
4. **تست‌هایی که کاربر باید بعداً اجرا کند (توسط Agent اجرا نشود):**  
   * `python -m pytest src/tests/test_stage7_valuation.py -q`

---

### ۷. فایل‌های بررسی‌شده و محدودیت‌های اعتبارسنجی (Files Inspected & Verification Limits)

* `stepsForStage7.md` (برنامه اجرایی Stage 7 و وضعیت D9)
* `07_Stage7_Valuation.md` (بخش‌های ۴۷، ۴۸، ۶۵، ۸۵، ۸۷)
* `src/valuation/parameters.py` (خطوط ۱–۵۰، ۲۶۰–۲۹۵، ۳۵۰–۳۸۰)
* `src/valuation/engine.py` (خطوط ۷۰–۸۰، ۲۲۵–۲۳۵)
* `src/valuation/schema.py` (`ValuationResult`)
* `src/valuation/service.py` (`calculate_valuation_as_of_jalali`)
* `src/tests/test_stage7_valuation.py` (تست‌های P33 و P35)
* `zErrors.md` (تریس‌بک خطای `LookupError`)
* `reply.md` (گزارش‌های ممیزی P63 و P64)

---

### بیانیه پایانی صریح (Explicit Declarations):

1. **وضعیت D9:** **همچنان باز (OPEN)** است.
2. **تصمیمات خاص موردنیاز از مالک پروژه:** تصویب رسمی ۳۸ مقدار عددی پارامترها، تعیین تاریخ اعتبار صریح (`effective_from`)، تعیین سیاست پوشش تاریخی و تعیین تکالیف درخواست‌های قبل از تاریخ اعتبار.
3. **تاییدیه اجرای عملیات:** **هیچ فایلی تغییر داده نشده و هیچ تستی اجرا نگردیده است (No files changed and no tests run).**