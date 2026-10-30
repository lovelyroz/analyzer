
# Stage 7 — Target 4: Parameter Registry

## 1. هدف

- نسخه‌بندی و مدیریت پارامترهای Valuation.
- انتخاب پارامترها بر اساس زمان مؤثر (Point-in-Time).
- تضمین قابلیت ردیابی، ممیزی و بازتولید نتایج.
- مشخص بودن مرز مسئولیت Caller و Valuation Engine.

## 2. وضعیت و قابلیت‌های موجود

- پیاده‌سازی `ParameterRecord`، `ParameterSetVersion` و `ParameterRegistry`.
- ایجاد Genesis شامل ۳۸ پارامتر:
  - ۳۳ پارامتر مصرف‌شده.
  - ۵ پارامتر ثبت‌شده ولی مصرف‌نشده.
- پشتیبانی از انتخاب نسخه با `version_key` و انتخاب تاریخ‌محور.
- اعتبارسنجی پارامترهای مصرف‌شده.
- پشتیبانی از Snapshot.
- برخی قواعد محاسباتی و مدل‌ها خارج از Registry باقی مانده‌اند.

## 3. اشکالات فنی تأییدشده

- Duplicate `version_key`:
  - Registry یکتایی `version_key` را تضمین نمی‌کند.
  - انتخاب نسخه با کلید دقیق ممکن است نسخه تکراری را پنهان کند.
  - باید کلیدهای تکراری هنگام ساخت Registry رد شوند.
- Deep Immutability:
  - `frozen=True` و `MappingProxyType` فقط سطح بیرونی را محافظت می‌کنند.
  - مقادیر تو‌در‌تو مانند `dict` و `list` همچنان ممکن است mutable باشند.
  - باید ساختارهای mutable به‌صورت بازگشتی محافظت شوند.

## 4. تناقضات و اصلاحات مستنداتی

- `data_cutoff_datetime` به‌تنهایی انتخاب تاریخی پارامترها را فعال نمی‌کند.
- انتخاب تاریخی زمانی فعال می‌شود که `registry` یا `parameter_as_of` ارائه شده باشد.
- در حالت Legacy، استفاده از Genesis زنده همچنان ممکن است.
- `valuation_date` به‌صورت خودکار جایگزین timestamp انتخاب پارامتر نمی‌شود.
- ترتیب صعودی Tuple نسخه‌ها الزام نیست؛ Resolver باید نسخه معتبر با بیشترین `effective_from` را انتخاب کند.
- R1 از نظر زیرساخت عملکردی عمدتاً انجام شده، اما نقص Duplicate Key باقی است.
- نقص Deep Immutability باید جداگانه ثبت شود.
- مسئله PIT و provenance زمانی Benchmark P/E مستقل از اشکالات داخلی Registry است.
- نبود ذخیره‌سازی دیتابیسی به‌تنهایی اثبات‌کننده نقص نیست؛ نیاز به آن باید با تصمیم معماری مشخص شود.

## 5. تصمیمات باز مالک پروژه

- R5: تصویب رسمی ۳۳ پارامتر مصرفی Genesis.
- R6: تعیین نیاز یا عدم نیاز به بازسازی تاریخی و Backtest؛ در صورت نیاز، مقادیر و تاریخ‌های مؤثر تاریخی باید مستند باشند.
- R7: تأیید Registry درون‌کدی برای V1 یا الزام ذخیره‌سازی پایدار خارجی.
- R8: تعیین اینکه وزن‌های Confidence، Driver Uncertainty و قواعد Rounding در Registry نسخه‌بندی شوند یا به‌صورت ثابت در مدل باقی بمانند.
- R9 / D7: تعیین مسئولیت PIT Benchmark P/E بین Caller و قرارداد داده‌ای Valuation.

## 6. موارد لازم برای تکمیل فنی

- افزودن اعتبارسنجی یکتایی `version_key`.
- پیاده‌سازی Deep Immutability برای داده‌های تو‌در‌تو.
- افزودن تست رد کلیدهای تکراری.
- افزودن تست جلوگیری از تغییر مقادیر تو‌در‌تو.
- تست انتخاب تاریخ‌محور با ترتیب‌های متفاوت Tuple.
- تست رد ابهام در تاریخ‌های مؤثر یکسان.
- تست رفتار Legacy و قواعد انتخاب timestamp.
- تست استقلال Snapshot از وضعیت اصلی Registry.

## 7. مبنای تهیه پرامپت نهایی

- فایل‌های اصلی بررسی:
  - `src/valuation/parameters.py`
  - `src/valuation/engine.py`
  - `src/tests/test_stage7_valuation.py`
  - `STAGE7_Target4.md`
- در صورت نیاز به هماهنگی با برنامه کل Stage 7:
  - `stepsForStage7.md`
  - `tasksToDo.md`
- ترتیب اجرا:
  1. تعیین تکلیف تصمیمات باز.
  2. اصلاح اشکالات فنی.
  3. تکمیل تست‌های هدفمند.
  4. اصلاح مستندات متناقض.
  5. گزارش شواهد و وضعیت نهایی Target 4.
- هیچ تاریخ تاریخی، مقدار مالی، تأییدیه یا provenance نباید بدون مدرک ساخته شود.
- تست اجرا‌نشده نباید PASS گزارش شود.
- Target 4 تا رفع اشکالات فنی، تکمیل تست‌ها و تعیین تکلیف تصمیمات ضروری، بسته‌شده محسوب نمی‌شود.

# Reports
گزارش ممیزی و ارزیابی فنی **Stage 7 — Target 4: Parameter Registry Audit and Closure Planning** بر اساس فایل‌های منبع، کدها، تست‌ها و اسناد موجود در مخزن `lovelyroz/analyzer` در ادامه ارائه می‌شود. این ارزیابی در حالت **REPORT-ONLY** انجام شده و هیچ‌گونه تغییر کد، ساخت فایل یا اجرای دستوری در محیط صورت نگرفته است.

---

### 1. T4-A — Technical Defect Verification

#### ۱. پذیرش کلید تکراری (`version_key`) در `ParameterRegistry`
* **فایل و کلاس مربوطه**: `src/valuation/parameters.py`، کلاس `ParameterRegistry`.
* **شواهد کد و مسیر اجرا**:
  در خط ۱۰۰ فایل `parameters.py` کلاس `ParameterRegistry` به‌صورت `@dataclass(frozen=True)` تعریف شده و `versions: Tuple[ParameterSetVersion, ...]` را دریافت می‌کند. در این کلاس هیچ متد اعتبارسنجی مانند `__post_init__` برای چک کردن یکتایی `version_key` در نسخه متغیرها وجود ندارد.
  اگر `ParameterRegistry` با دو نسخه که کلید یکسان دارند (مثلاً `TEST/V1`) مقداردهی شود:
  - در تابع `resolve_parameter_set("TEST/V1", registry)`، اولین نسخه مطابقت‌یافته در پیمایش حلقه برگردانده شده و نسخه دوم پنهان می‌ماند.
  - در تابع `resolve_parameter_set_as_of`، اگر تاریخ `effective_from` هر دو نسخه یکسان باشد، خطای `LookupError("Ambiguous...")` صادر می‌شود؛ اما اگر تاریخ‌ها متفاوت باشند، متد تاریخ‌محور نسخه جدیدتر را انتخاب می‌کند، در حالی که متد کلید صریح نسخه اول لیست را برمی‌گرداند. این امر منجر به عدم انطباق رفتار سیستم در جستجوی کلیدی و تاریخ‌محور می‌گردد.
* **وضعیت تأیید**: **CONFIRMED DEFECT**.
* **پیشنهاد اصلاح کمینه و ایمن**: افزودن متد `__post_init__` به `ParameterRegistry` جهت بررسی یکتایی `version_key` در نسخه‌ها و صادر کردن `ValueError` در صورت وجود کلید تکراری.
* **ریسک سازگاری**: صفر. در حال حاضر `DEFAULT_REGISTRY` فقط شامل نسخه `GENESIS_VERSION` است و هیچ تستی کلید تکراری ثبت نمی‌کند.
* **نیاز به تصمیم مالک مالی/معماری**: خیر؛ این یک اصلاح فنی محض جهت ایمن‌سازی زمان ساخت (Constructor Validation) است.

#### ۲. عدم قفل عمیق کامل (Incomplete Deep Immutability) برای مقادیر تودرتو
* **فایل و کلاس/تابع مربوطه**: `src/valuation/parameters.py`، کلاس‌های `ParameterRecord`، `ConsumedParameters` و تابع `consume_parameter_set()`.
* **شواهد کد و مسیر اجرا**:
  - کلاس `ParameterRecord` با `@dataclass(frozen=True)` تعریف شده و فیلد `parameter_value: object` دارد. گرچه متد `_rec` از `copy.deepcopy` استفاده می‌کند، اما اگر مقدار پارامتر یک دیکشنری متغیر پایتونی (مانند `INDUSTRY_TARGET_PE: Dict[str, float]`) باشد، دکوراتور `frozen=True` فقط ارجاع سطح اول را قفل می‌کند و مانع تغییر عناصر داخلی دیکشنری (`record.parameter_value["KEY"] = val`) نمی‌شود.
  - در `ConsumedParameters`، دیکشنری اصلی `values` و گروه‌ها با `MappingProxyType` پوشانده شده‌اند که مانع تغییر کلیدهای سطح اول می‌شود (`test_p35_isolation...`). اما اگر یک مقدار درون `values` خود یک دیکشنری متغیر باشد (`consumed.values["INDUSTRY_TARGET_PE"]`)، فراخوانی آن ارجاع متغیر داخلی را برمی‌گرداند و عناصر آن قابل ویرایش هستند.
  - در متد `snapshot()`، دستور `return copy.deepcopy(dict(self.values))` یک نسخه عمیق مستقل ارائه می‌دهد، بنابراین دستکاری snapshot بر شیء اصلی یا ثوابت ماژول تاثیری ندارد.
* **وضعیت تأیید**: **CONFIRMED DEFECT** (برای دیکشنری‌های متغیر تودرتو).
* **پیشنهاد اصلاح کمینه و ایمن**: در تابع `consume_parameter_set()`، دیکشنری‌های درون‌لایه متغیر پیش از ذخیره در `values` به‌صورت عمیق به `MappingProxyType` تبدیل شوند.
* **ریسک سازگاری**: صفر. خروجی‌های عمومی و دسترسی‌های محاسباتی تغییر نمی‌کنند.
* **نیاز به تصمیم مالک مالی/معماری**: خیر؛ اصلاح فنی جهت تضمین ۱۰۰٪ عدم تغییرپذیری است.

---

### 2. T4-B — Resolver and Timestamp Verification

۱. **جستجوی کلید صریح (`resolve_parameter_set`)**:
   حلقه پیمایش روی `registry.versions` اولین نسخه‌ای که `version.version_key == version_key` باشد را برمی‌گرداند. در صورت عدم وجود، خطای صریح `KeyError` صادر شده و هیچ جایگزینی پنهانی صورت نمی‌گیرد.
۲. **جستجوی تاریخ‌محور (`resolve_parameter_set_as_of`)**:
   تاریخ `as_of` به UTC نرمال‌سازی شده و فقط نسخه‌های دارای `effective_from <= moment` فیلتر می‌شوند. نسخه Genesis دارای `effective_from = None` است، بنابراین کلاً از چرخه جستجوی تاریخی کنار گذاشته می‌شود.
۳. **برخورد با تاریخ‌های اعتبار همزمان**:
   اگر چند نسخه واجد شرایط دارای تاریخ `effective_from` یکسان و بیشینه باشند، سیستم با خطای `LookupError("Ambiguous Stage 7 parameter versions...")` متوقف می‌شود (`test_p33_as_of_overlap_raises_ambiguity`).
۴. **تأثیر ترتیب Tuple بر جستجو**:
   جستجو بر اساس انتخاب بیشینه تاریخ (`max(..., key=lambda v: v.effective_from)`) انجام می‌شود و ترتیب قرارگیری نسخه‌ها در Tuple تاثیری در خروجی ندارد (`test_d9_overlapping_eligible_versions_are_deterministic`).
۵. **انتخاب مسیر قدیمی (Legacy Genesis)**:
   در تابع `select_parameter_set_for_valuation`، اگر `parameter_registry` و `parameter_as_of` هر دو `None` باشند، نسخه `live_genesis_parameter_set()` فراخوانی شده و متاداده با حالت `"FIXED_GENESIS_LEGACY"` و `point_in_time_selection_applied: False` افشا می‌شود (`test_p35_legacy_path_provenance...`).
۶. **حاکمیت `data_cutoff_datetime` بر انتخاب پارامتر**:
   در `ValuationEngine.calculate_valuation`، متد `_resolve_parameter_governing_timestamp` تاریخ قطع داده‌ها را بر انتخاب پارامتر حاکم می‌سازد (`as_of_source: "EFFECTIVE_DATA_CUTOFF"`) (`test_d9_effective_cutoff_governs_selection...`).
۷. **مغایرت صریح `parameter_as_of` با `data_cutoff_datetime`**:
   در صورت ارسال هر دو و وجود مغایرت زمانی بین آن‌ها، متد `_resolve_parameter_governing_timestamp` خطای صریح `ValueError("Stage 7 parameter_as_of conflicts with...")` صادر کرده و از ادامه محاسبه جلوگیری می‌کند (`test_d9_conflicting_parameter_as_of_is_rejected`).
۸. **عدم جایگزینی خودکار `valuation_date`**:
   تاریخ ارزش‌گذاری (`valuation_date`) هرگز به عنوان تاریخ مبنای انتخاب پارامتر استفاده نمی‌شود (`test_d9_effective_cutoff_governs_selection_not_valuation_date`).
۹. **استقلال Snapshot**:
   متد `ConsumedParameters.snapshot()` کپی عمیق برمی‌گرداند و تغییر در دیکشنری خروجی هیچ تاثیری بر محاسبات بعدی ندارد.

---

### 3. T4-C — Test Coverage Matrix

| رفتار / اصل حاکم (Invariant) | وضعیت پوشش | تست‌های موجود / شواهد | سناریوی تست غایب و ادعای مورد انتظار |
|---|---|---|---|
| **رد کلید تکراری در `ParameterRegistry`** | **NOT COVERED** | هیچ تستی وجود ندارد. | سناریو: ساخت `ParameterRegistry` با دو نسخه دارای `version_key` یکسان. انتظار: صدور `ValueError("Duplicate version_key...")`. |
| **جلوگیری از تغییر عمیق مقادیر تودرتو** | **PARTIALLY COVERED** | `test_p35_isolation...` تغییرات سطح اول را تست می‌کند (`TypeError` و `FrozenInstanceError`). | سناریو: تلاش برای ویرایش دیکشنری تودرتو درون `consumed.values["INDUSTRY_TARGET_PE"]["LEAK"] = 1.0`. انتظار: صدور `TypeError`. |
| **انتخاب تاریخ‌محور مستقل از ترتیب Tuple** | **COVERED** | `test_d9_overlapping_eligible_versions_are_deterministic` (ترتیب‌های `(older, newer)` و `(newer, older)` ارزیابی شده‌اند). | نیازی ندارد. |
| **رد تاریخ‌های اعتبار همزمان و مبهم** | **COVERED** | `test_p33_as_of_overlap_raises_ambiguity` و `test_d9_overlapping_eligible_versions_are_deterministic`. | نیازی ندارد. |
| **رفتار مسیر Legacy** | **COVERED** | `test_p35_legacy_path_provenance...` و `test_d9_legacy_path_stays_backward_compatible...`. | نیازی ندارد. |
| **حاکمیت cutoff و رد مغایرت timestamp** | **COVERED** | `test_d9_effective_cutoff_governs_selection...` و `test_d9_conflicting_parameter_as_of_is_rejected`. | نیازی ندارد. |
| **استقلال Snapshot** | **COVERED** | `test_p35_isolation_from_global_mutation_and_snapshot_aliasing`. | نیازی ندارد. |

---

### 4. T4-D — Owner Decisions R5–R9

* **R5: تصویب رسمی ۳۳ پارامتر پایه Genesis**:
  - *وضعیت کد/اسناد*: پارامترهای Genesis با `effective_from = None` و یادداشت عدم تأیید زمانی ثبت شده‌اند.
  - *مورد نامشخص/غیرمصوب*: تصویب رسمی و حقوقی ۳۳ پارامتر مالی توسط مالک پروژه.
  - *تصمیم صریح مالک*: ابلاغ مصوبه رسمی تصویب ۳۳ پارامتر پایه.
  - *مانع اصلاحات T4-A است؟*: خیر.
  - *وضعیت*: **OPEN**.

* **R6: نیاز به بازسازی تاریخی و بک‌تست**:
  - *وضعیت کد/اسناد*: ثبت پیش‌فرض فقط Genesis بدون تاریخ دارد و جستجوی تاریخی خطای `LookupError` می‌دهد.
  - *مورد نامشخص/غیرمصوب*: ارائه جدول نسخه‌های تاریخی پارامترها به همراه تاریخ‌های شروع اعتبار (`effective_from`).
  - *تصمیم صریح مالک*: ارائه نسخه‌های تاریخی و تاریخ‌های اعتبار.
  - *مانع اصلاحات T4-A است؟*: خیر.
  - *وضعیت*: **BLOCKED**.

* **R7: معماری ذخیره‌سازی ثبت پارامترها (In-Code vs Database)**:
  - *وضعیت کد/اسناد*: ساختار غیرقابل‌تغییر ثبت درون‌کدی در `parameters.py` پیاده‌سازی شده و هیچ جدول دیتابیس وجود ندارد.
  - *مورد نامشخص/غیرمصوب*: تأیید رسمی استفاده از ثبت درون‌کدی (Option A) برای V1.
  - *تصمیم صریح مالک*: اتخاذ تصمیم صریح درباره تایید Option A یا الزام دیتابیس (Option B).
  - *مانع اصلاحات T4-A است؟*: خیر.
  - *وضعیت*: **OPEN**.

* **R8: نسخه گذاری وزنی فرمول‌ها و قواعد گردکردن**:
  - *وضعیت کد/اسناد*: وزن‌های فرمول Confidence، Driver Uncertainty و قواعد گردکردن در کد سخت‌افزارانه هستند و در متاداده افشا می‌شوند.
  - *مورد نامشخص/غیرمصوب*: تصمیم‌گیری درباره پارامتری شدن این وزن‌ها یا حفظ آن‌ها به عنوان ثوابت نسخه مدل (`MODEL_VERSION = "STAGE7_V1"`).
  - *تصمیم صریح مالک*: تعیین تکلیف دامنه پارامترهای قابل تنظیم.
  - *مانع اصلاحات T4-A است؟*: خیر.
  - *وضعیت*: **OPEN**.

* **R9/D7: اصالت زمانی مشاهدات بنچمارک بازار (PIT Provenance)**:
  - *وضعیت کد/اسناد*: ورودی‌های بنچمارک بازار به‌صورت اعداد بدون تاریخ وارد می‌شوند.
  - *مورد نامشخص/غیرمصوب*: تعیین این‌که اصالت زمانی بنچمارک‌ها بر عهده فراخوان‌کننده (Caller) است یا باید ساختار داده‌ای ورودی تغییر کند.
  - *تصمیم صریح مالک*: تصویب قرارداد اصالت زمانی داده‌های بنچمارک.
  - *مانع اصلاحات T4-A است؟*: خیر.
  - *وضعیت*: **BLOCKED**.

---

### 5. T4-E — Recommended Closure Sequence

۱. **اصلاحات فنی ایمن (بدون نیاز به تصمیم مالک)**:
   - افزودن اعتبارسنجی یکتایی `version_key` در `ParameterRegistry.__post_init__`.
   - قفل کردن عمیق دیکشنری‌های تودرتو در `consume_parameter_set`.
۲. **تصمیمات مالک پروژه (باید پیش از Freeze نهایی اخذ شوند)**:
   - دریافت مصوبه R5 (تصویب پارامترهای Genesis).
   - دریافت مصوبه R7 (تأیید ثبت درون‌کدی Option A).
   - تعیین تکلیف R8 (حفظ وزن فرمول‌ها به عنوان ثوابت نسخه مدل).
   - تعیین تکلیف R9/D7 (مسئولیت صحت زمانی بنچمارک‌ها بر عهده Caller).
۳. **تست‌های مورد نیاز برای افزودن**:
   - افزودن تست اعتبارسنجی ثبت کلیدهای تکراری در `ParameterRegistry`.
   - افزودن تست عدم امکان تغییر عمیق در `ConsumedParameters.values`.
۴. **اصلاحات اسنادی پس از پیاده‌سازی**:
   - بهروزرسانی اسناد `STAGE7_Target4.md` و `temp_report2.md` جهت ثبت اعتبارسنجی جدید زمان ساخت و قفل عمیق پارامترها.
۵. **شواهد لازم پیش از اعلام اتمام Target 4**:
   - پاس شدن تمامی تست‌های جدید در اجرای محلی توسط کاربر (`pytest src/tests/test_stage7_valuation.py`).
   - ثبت تصمیمات صریح مالک پروژه برای R5 تا R9 در `tasksToDo.md`.

---

### 6. Required Additional Files (if any)

هیچ فایل اضافی دیگری نیاز نیست. تمامی شواهد فنی و اسنادی مورد نیاز مستقیماً از فایل‌های منبع تصریح‌شده (`parameters.py`، `engine.py`، `test_stage7_valuation.py`، `STAGE7_Target4.md`، `stepsForStage7.md`، `WORKFLOW_RULES.md`، `tasksToDo.md` و `temp_report2.md`) استخراج گردیده‌اند.

---

### 7. Final Target 4 Status

**PARTIALLY BLOCKED**

**توضیح**: زیرساخت فنی انتخاب دقیق، انتخاب تاریخ‌محور، ایزوله‌سازی snapshot و نگهداری متاداده‌های ممیزی کاملاً عملیاتی و معتبر است. با این حال، Target 4 در وضعیت **PARTIALLY BLOCKED** قرار دارد زیرا:
1. دو اصلاح فنی کمینه (اعتبارسنجی یکتایی کلیدها در زمان ساخت ثبت و قفل عمیق دیکشنری‌های تودرتو) نیازمند اعمال در کد و افزودن تست هستند.
2. اتمام نهایی ممیزی و بسته شدن کامل Target 4 نیازمند ابلاغ تصمیمات صریح و مصوبات مدیریتی مالک پروژه در خصوص R5، R6، R7، R8 و R9/D7 می‌باشد.

## Target 4 — Documentation Update After T4-1 to T4-3 Verification
### بر اساس دستورالعمل‌های **PROMPT.md** و قواعد کاری تدوین‌شده در **WORKFLOW_RULES.md**، اجرای بخش **Target 4 — Documentation Update After T4-1 to T4-3 Verification** به صورت ساختاریافته در دو بلوک (بخش ایجنت و بخش کاربر) به همراه متن کامل به‌روزرسانی مستندات آماده گردیده است:

---

### **Block 1: Agent Specification (دستورالعمل ایجنت)**

```markdown
### TASK SPECIFICATION FOR AGENT: Target 4 — Documentation Update After T4-1 to T4-3 Verification

#### Task Type
DOCS ONLY. Do NOT modify source code, tests, configuration, or application behavior. Do NOT execute tests or Git commands.

#### Explicitly Authorized Files
Read and modify ONLY these files:
1. STAGE7_Target4.md
2. temp_report2.md

Read-only reference files (do NOT modify):
3. src/valuation/parameters.py
4. src/tests/test_stage7_valuation.py
5. WORKFLOW_RULES.md
6. stepsForStage7.md
7. tasksToDo.md

#### Verified Evidence Context
- SHA of src/valuation/parameters.py: d3b8d50ba26544417d13c261bc85c0c810cc2887
- Implementation changes verified:
  * T4-1: ParameterRegistry.__post_init__ rejects duplicate version_key values via ParameterRegistryInvalidError.
  * T4-2: ParameterRecord.__post_init__ recursively freezes values using freeze_parameter_value.
  * ParameterSetVersion.__post_init__ normalizes records to a tuple.
  * consume_parameter_set freezes consumed parameter values.
- Executed Test Evidence:
  Command: pytest src/tests/test_stage7_valuation.py -k "t4_1 or t4_2 or t4_3" -q
  Result: 15 passed, 90 deselected in 3.15s.

#### Execution Tasks

##### 1. T4-DOC-1 — Correct Technical Defect Status in STAGE7_Target4.md
Update STAGE7_Target4.md to mark the two previously confirmed technical defects as RESOLVED/VERIFIED with test evidence:
- Duplicate version_key rejection.
- Deep immutability of nested parameter values.

##### 2. T4-DOC-2 — Correct Test Coverage Section in STAGE7_Target4.md
Record the 15 passing targeted tests and the exact test command executed by the user. Explicitly state that this result applies only to the selected tests in that command and does not certify the entire test suite.

##### 3. T4-DOC-3 — Preserve Unresolved Owner Decisions in STAGE7_Target4.md
Maintain OPEN/BLOCKED status for owner decisions R5, R6, R7, R8, and R9/D7:
- R5: Formal approval of Genesis base parameters.
- R6: Provision of historical dated parameter versions.
- R7: Storage architecture approval (In-code Option A vs DB Option B).
- R8: Constant formula weights vs parameterization.
- R9/D7: Market P/E benchmark temporal provenance and PIT contract.
Reiterate that technical immutability and duplicate-key validation do NOT constitute owner approval of historical parameters, storage architecture, or benchmark PIT provenance.

##### 4. T4-DOC-4 — Append Evidence Report to temp_report2.md
Append a dated report to temp_report2.md recording:
- Code SHA: d3b8d50ba26544417d13c261bc85c0c810cc2887.
- Verified implementation changes (T4-1 and T4-2).
- Exact user test command and result (15 passed, 90 deselected in 3.15s).
- Limits of test evidence.
- Unresolved decisions R5–R9.
- Conclusion: Technical T4-1/T4-3 work is verified; full Target 4 closure remains conditional on owner decisions.

#### Strict Constraints
- Only modify STAGE7_Target4.md and temp_report2.md.
- Do not run tests, Git commands, or create/invent dates or financial values.
```

---

### **Block 2: User Specification (دستورالعمل کاربر به زبان فارسی)**

**فایل‌های مورد نیاز:**
1. `STAGE7_Target4.md` (جهت اصلاح و به‌روزرسانی وضعیت نقص‌های فنی و پوشش تست‌ها)
2. `temp_report2.md` (جهت الحاق گزارش شواهد ممیزی جدید)
3. `src/valuation/parameters.py` (مرجع برسی کد - فقط خواندنی)
4. `src/tests/test_stage7_valuation.py` (مرجع تست‌ها - فقط خواندنی)
5. `tasksToDo.md` (مرجع وضعیت کارهای فعال - فقط خواندنی)
6. `stepsForStage7.md` (مرجع نقشه راه - فقط خواندنی)
7. `WORKFLOW_RULES.md` (مرجع قواعد کاری - فقط خواندنی)

**فهرست تکالیف و کارهای انجام‌شده:**
1. **تکلیف T4-DOC-1:** به‌روزرسانی وضعیت دو نقص فنی قبلی در سند `STAGE7_Target4.md` از حالت غیرقطعی/باز به وضعیت **برطرف‌شده و اعتبارسنجی‌شده با تست**.
2. **تکلیف T4-DOC-2:** ثبت دقیق دستور اجراشده توسط کاربر (`pytest src/tests/test_stage7_valuation.py -k "t4_1 or t4_2 or t4_3" -q`) و نتیجه **15 passed, 90 deselected** در سند `STAGE7_Target4.md` با تصریح محدودیت محدوده تست‌ها.
3. **تکلیف T4-DOC-3:** حفظ وضعیت **باز/مسدود (OPEN / BLOCKED)** برای تصمیمات پنج‌گانه مالک پروژه (**R5 تا R9**) و تاکید بر اینکه اصلاحات فنی اخیر به معنای تصویب معماری یا داده‌های تاریخی نیست.
4. **تکلیف T4-DOC-4:** الحاق گزارش ممیزی جدید و تاریخ‌دار به انتهای سند `temp_report2.md` شامل SHA کد، شواهد تست، محدودیت‌ها و وضعیت تصمیمات مالک.

**نتیجه مورد انتظار:**
به‌روزرسانی صرفاً مستنداتی (`DOCS ONLY`) بدون تغییر در کد اجرایی یا تست‌ها، ثبت دقیق شواهد فنی T4-1 تا T4-3 و باز نگه داشتن موانع مربوط به تصمیمات مالک پروژه.

---

### **متن به‌روزرسانی‌های اعمال‌شده در فایل‌ها**

#### **۱. تغییرات سند `STAGE7_Target4.md` (بخش‌های T4-DOC-1 تا T4-DOC-3)**

```markdown
### به‌روزرسانی وضعیت نقص‌های فنی و شواهد آزمون (Target 4 — T4-1 to T4-3 Verification)

#### ۱. وضعیت نقص‌های فنی قبلی (تکلیف T4-DOC-1)
با توجه به بازبینی کد در SHA: `d3b8d50ba26544417d13c261bc85c0c810cc2887` و اجرای تست‌های مربوطه، دو نقص فنی برطرف شده و تایید گردیدند:
- **عدم پذیرش version_key تکراری (T4-1):** تابع `ParameterRegistry.__post_init__` وجود کلیدهای تکراری را اعتبارسنجی کرده و در صورت بروز، خطای صریح `ParameterRegistryInvalidError` صادر می‌کند.
- **انجماد عمیق مقادیر پارامترها (T4-2):** کلاس `ParameterRecord.__post_init__` به صورت بازگشتی مقادیر را با تابع `freeze_parameter_value` منجمد می‌کند. همچنین `ParameterSetVersion.__post_init__` رکوردهای ورودی را به `tuple` تبدیل کرده و `consume_parameter_set` مقادیر مصرفی را انجماد عمیق می‌نماید.

#### ۲. پوشش و نتایج آزمون‌های هدف‌گذاری‌شده (تکلیف T4-DOC-2)
دستور اجرای تست توسط کاربر:
`pytest src/tests/test_stage7_valuation.py -k "t4_1 or t4_2 or t4_3" -q`

نتیجه واقعی آزمون:
`15 passed, 90 deselected in 3.15s`

*ملاحظه مهم:* این نتیجه صرفاً مربوط به ۱۵ تست انتخاب‌شده در دستور فوق است و اثبات‌کننده پاس شدن کل مجموعه تست‌های پروژه یا ثبت تاریخچه PIT نمی‌باشد.

#### ۳. وضعیت تصمیمات باز مالک پروژه (تکلیف T4-DOC-3)
تصمیمات مدیریتی و سیاست‌گذاری زیر همچنان در وضعیت **OPEN / BLOCKED** باقی مانده‌اند و تغییرات فنی فوق باعث بسته‌شدن آن‌ها نمی‌شود:
- **R5 (تصویب مقادیر Genesis):** مقادیر Genesis همچنان فاقد تاریخ اعتبار معتبر (`effective_from = None`) هستند.
- **R6 (نسخه‌های تاریخی پارامترها):** ثبت تاریخ‌دار برای گذشته ارائه نشده است.
- **R7 (معماری ذخیره‌سازی):** پیاده‌سازی درونکدی صرفاً مکانیسم V1 است و تایید معماری دیتابیس/فایل توسط مالک انجام نشده است.
- **R8 (ثوابت خارج از ثبت):** تعیین تکلیف ثوابت فرمول‌ها همچنان نیازمند تصمیم مالک است.
- **R9 / D7 (اصالت زمانی P/E بنچمارک):** داده‌های بنچمارک همچنان فاقد متاداده‌های زمانی اصیل هستند.
```

---

#### **۲. گزارش الحاقی به انتهای سند `temp_report2.md` (تکلیف T4-DOC-4)**

```markdown
====================================================================
### Target 4 — Verification and Documentation Update Report
Date (UTC): 2026-10-30
Scope: Documentation update after T4-1 to T4-3 technical verification.
Code SHA: d3b8d50ba26544417d13c261bc85c0c810cc2887

#### 1. Verified Implementation Changes
- **T4-1 (Duplicate Version Key Protection):** `ParameterRegistry.__post_init__` verifies version_key uniqueness across parameter sets and raises `ParameterRegistryInvalidError` upon duplication.
- **T4-2 (Deep Immutability):** `ParameterRecord.__post_init__` recursively freezes parameter value structures using `freeze_parameter_value`. `ParameterSetVersion.__post_init__` normalizes record collections to immutable tuples. `consume_parameter_set` enforces immutability on consumed values.

#### 2. User Executed Test Evidence
Exact command executed by user:
`pytest src/tests/test_stage7_valuation.py -k "t4_1 or t4_2 or t4_3" -q`

Execution result:
`15 passed, 90 deselected in 3.15s`

#### 3. Evidence Limits
This test evidence confirms the technical functionality of duplicate version key rejection and deep value immutability within the 15 targeted test cases. It does not certify unexecuted tests, end-to-end integration, historical PIT correctness, or project owner policy approvals.

#### 4. Status of Owner Decisions (R5–R9)
The following decisions remain OPEN / BLOCKED pending formal project owner direction:
- **R5:** Formal ratification of Genesis parameter values (currently `effective_from = None`).
- **R6:** Provision of historical effective-dated parameter versions for backtesting.
- **R7:** Approval of parameter storage architecture (In-code Option A vs Database Option B).
- **R8:** Policy on formula weights and hardcoded thresholds outside the registry.
- **R9 / D7:** Temporal provenance and PIT validation rules for benchmark P/E observations.

#### 5. Conclusion
Technical implementation for T4-1 through T4-3 is fully verified by user test evidence. Full closure of Target 4 remains conditional upon resolving owner decisions R5 through R9.
====================================================================

### ### گزارش تأیید تست Target 4

- **Task:** بررسی اصلاحات فنی Parameter Registry
- **فرمان اجراشده:** `pytest src/tests/test_stage7_valuation.py -k "t4_1 or t4_2 or t4_3" -q`
- **نتیجه:** `15 passed, 90 deselected`
- **وضعیت:** PASS

اصلاحات مربوط به یکتایی `version_key`، تغییرناپذیری عمیق داده‌ها، استقلال Snapshot و انتخاب تاریخ‌محور پارامترها در تست‌های هدفمند تأیید شدند.

**نتیجه:** نقص‌های فنی بررسی‌شده در Target 4 برطرف شده‌اند. نیازی به اصلاح مجدد کد نیست.
================================================
### گزارش نتیجه تست‌های S7-T012

در تاریخ 2026-10-30، تست‌های زیر توسط کاربر و در محیط محلی پروژه اجرا شدند:

- تست‌های متمرکز Stage 7/8/9 و رابط سرویس‌ها: **857 passed**
- کل مجموعه تست‌های `src/tests`: **1898 passed, 2 skipped**
- هیچ تستی شکست نخورده است.
- تعداد 153 هشدار `DeprecationWarning`، عمدتاً مربوط به استفاده از `datetime.utcnow()`، ثبت شده است.

**نتیجه:** اجرای تست‌های هدفمند و مجموعه کامل پروژه موفق بود. بااین‌حال، به دلیل بازماندن وابستگی‌های S7-T007 تا S7-T011، این نتیجه به‌تنهایی موجب تکمیل S7-T012 یا بسته‌شدن Stage 7 نمی‌شود.

**وضعیت فعلی:** تست‌ها PASS؛ تسک‌های T007 تا T011 همچنان BLOCKED؛ تسک T012 و کل Stage 7 همچنان OPEN هستند.
