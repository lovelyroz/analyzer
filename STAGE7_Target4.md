
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