# DB-DES-006 — قرارداد منطقی مسیر CODAL تا FinancialFact canonical

**تاریخ:** 2026-11-15  
**وضعیت:** طراحی منطقی اولیه — PARTIAL  
**دامنه:** تعریف مسیر هدف CODAL Excel از دریافت فایل تا پذیرش ReportVersion و FinancialFactهای canonical؛ تفکیک صریح مسیر موجود از معماری هدف؛ تعیین مرز adapter، mapping، temporal interpretation، validation، persistence و audit.  
**نوع تغییر:** مستندسازی؛ بدون تغییر کد، ORM، schema، migration، داده یا تست.

## 1. مسئله و مبنای طراحی

ممیزی ایستای DB-AUD-001 بخش‌های 13 و 14 نشان داده است که مسیر تولیدی CODAL بررسی‌شده در `src/ingestion/service.py`، `ReportVersion` و `RawFinancialFact` می‌نویسد؛ در مقابل، مسیر Forecast/Stage 5 از `NormalizedFinancialFact` می‌خواند. در مسیرهای production بررسی‌شده، پل اجرایی متصل‌کنندهٔ استخراج به MappingRule/MappingDecision و سپس ساخت NormalizedFinancialFact و provenance متناظر پیدا نشد. این نتیجه محدود به مسیرها و literal references بررسی‌شده است و اثبات نبود هر مسیر پویا/غیرمستقیم در کل runtime نیست.

همچنین:
- replay فعلی CODAL بر اساس tracking identity/publication time تشخیص داده می‌شود، اما برابری payload canonical را اثبات نمی‌کند؛
- مسیر فعلی برای replay می‌تواند RawFinancialFactها را updated بشمارد، بدون آنکه سیاست conflict مبتنی بر payload را اجرا کند؛
- RawFinancialFact شامل داده‌هایی مانند raw label/unit/currency و locator ردیف/ستون است و با اصل عدم نگهداری دائمی raw financial-row archive تعارض دارد؛
- مدل NormalizedFinancialFact مشاهده‌شده Numeric(30,4) و کلید یکتای فاقد approved dimensions دارد و writer تولیدی آن در مسیر CODAL بررسی‌شده یافت نشد؛
- مدل‌های DerivedFinancialFact و DerivedFinancialFactInput با اصل runtime-only بودن محاسبات/خروجی‌ها ناسازگارند، مگر اینکه کاربرد معتبر دیگری جداگانه اثبات شود؛
- MappingRule/MappingDecision در مدل وجود دارند، اما اتصال production آن‌ها به مسیر CODAL در inventory محدود فعلی نشان داده نشده است.

این یافته‌ها بر بررسی کد و گزارش‌های Markdown متکی‌اند. فایل‌های XLSX منبع در این مرحله بازبینی نشده‌اند و هیچ ادعایی دربارهٔ مشاهدهٔ مستقیم محتوای workbook مطرح نیست.

## 2. اصول غیرقابل‌نقض

1. V1 ورودی صورت‌های مالی CODAL را از Excel می‌گیرد؛ PDF خارج از دامنهٔ این قرارداد است.
2. هر شرکت پیش از ingestion باید با company_id پایدار و دقیقاً یک industry_id معتبر resolve شده باشد؛ ticker به‌تنهایی هویت پایدار نیست.
3. هر گزارش به یکی از دو ReportType مصوب تعلق دارد: MONTHLY_ACTIVITY یا PERIODIC_FINANCIAL.
4. یک ReportVersion ممکن است چند دوره و چند مقدار را پوشش دهد؛ هر fact به دورهٔ واقعی خودش متصل می‌شود.
5. Header structural mapping، Metric mapping، Dimension resolution و temporal interpretation مراحل متمایزند؛ عنوان Header به‌تنهایی Metric را تعیین نمی‌کند.
6. هیچ fuzzy matching، حدس، catch-all، OTHER_* عمومی یا حذف مورد ناشناخته/مبهم مجاز نیست.
7. فقط موردی که استاندارد نسخه‌دار صریحاً out-of-scope اعلام کرده می‌تواند کنار گذاشته شود. هر unknown/ambiguous in-scope candidate کل Ingestion Unit را رد می‌کند.
8. فقط canonical financial inputs و حداقل provenance ذخیره می‌شوند؛ فایل Excel و raw source rows به‌صورت دائمی در DB آرشیو نمی‌شوند.
9. مقدار مالی با Decimal parse و یک‌بار ROUND_HALF_UP به SQLite INTEGER تبدیل می‌شود؛ signed 64-bit رعایت می‌شود. NULL، صفر واقعی و ZERO_FALLBACK متمایزند.
10. ReportVersion و تمام facts وابسته، provenance لازم و وضعیت COMPLETED همان Run یک واحد اتمیک‌اند.
11. ReportVersion، facts پذیرفته‌شده و استانداردهای تاریخی immutable هستند؛ اصلاح معنا با نسخهٔ جدید استاندارد انجام می‌شود، نه بازنویسی خاموش تاریخچه.
12. PIT cutoff پیش از ranking اعمال می‌شود؛ publication datetime معتبر برای eligibility تاریخی الزامی است.

## 3. مسیر هدف در سطح منطقی

```text
CODAL Excel artifact
    ↓
Acquisition / Excel adapter
    ↓
Temporary source observations (memory only)
    ↓
Source + Company + Industry + ReportType resolution
    ↓
Structural interpretation
    Raw Header / approved alias → Standard Database Header
    ↓
Semantic interpretation
    row/column/table context → FinancialMetric + approved dimensions
    ↓
Temporal interpretation
    source columns/labels → actual Jalali FinancialPeriod + temporal basis
    ↓
Value interpretation
    source text → Decimal → validated canonical INTEGER + unit/basis/state
    ↓
Whole-unit admission validation
    ↓
Canonical identity + duplicate/conflict/revision checks
    ↓
One transaction:
    Report / ReportVersion
    + all FinancialFacts
    + required provenance
    + IngestionRun = COMPLETED
```

هیچ مرحله‌ای در این زنجیره نباید به‌صورت مستقل بخشی از canonical unit را commit کند.

## 4. مرحله‌ها و مسئولیت‌ها

### 4.1 Acquisition و adapter

Adapter مسئول دریافت/خواندن Excel و تولید ساختار موقت source observations است. این ساختار می‌تواند در حافظه شامل sheet/table/header/row/column context و متن خام مقدار باشد، اما به‌خودی‌خود دادهٔ canonical یا مجوز persistence نیست.

Adapter:
- فایل را parse می‌کند و ساختار قابل‌تفسیر را به لایهٔ core می‌دهد؛
- نام و مقدار خام مشاهده‌شده را تا پایان interpretation در حافظه نگه می‌دارد؛
- هیچ DB commit، mapping تصمیم‌گیر، Metric assignment یا تغییر معنای عدد انجام نمی‌دهد؛
- فایل منبع را در DB ذخیره نمی‌کند؛ fingerprint و source artifact reference در حد provenance/audit مجازند؛
- خطاهای parse و ساختار ناقص را به‌صورت diagnostic کنترل‌شده گزارش می‌کند، بدون کپی payload مالی کامل در log.

### 4.2 Resolution هویت و نوع گزارش

پیش از interpretation مالی باید منبع CODAL، شرکت، صنعت و ReportType به‌طور قطعی resolve شوند. عدم تطبیق یا چندمعنایی هرکدام hard failure است. ReportType از روی شواهد و انتخاب/قرارداد ورودی تعیین می‌شود؛ سیستم نباید MONTHLY_ACTIVITY و PERIODIC_FINANCIAL را خودکار به‌جای یکدیگر تفسیر کند.

### 4.3 Structural interpretation

Raw Header یا alias تأییدشده، با توجه به industry، ReportType، report-family standard و context ساختاری، به Standard Database Header نگاشت می‌شود. این مرحله صرفاً هویت بخش/جدول/ساختار را تعیین می‌کند.

- یک Raw Header ممکن است با context متفاوت به Header استاندارد متفاوت برسد.
- چند Raw Header فقط در صورت هم‌معنایی ساختاری تأییدشده می‌توانند به یک Header برسند.
- یک Standard Header ممکن است چند Metric داشته باشد.
- Header ناشناخته یا مبهم که در دامنهٔ گزارش candidate است، گزارش را رد می‌کند؛ از نام نزدیک یا موقعیت صفحه‌ای حدس زده نمی‌شود.
- دیکشنری ۱۷ Header نمونهٔ PERIODIC_FINANCIAL بانک، فقط نمونهٔ ساختاری همان استاندارد است و به گزارش ماهانه یا صنایع دیگر تعمیم داده نمی‌شود.

### 4.4 Semantic interpretation و Dimensions

Metric از محتوای واقعی ردیف/ستون/جدول، نقش سطر، نوع مقدار و context اقتصادی تعیین می‌شود؛ نه از Header به‌تنهایی. خروجی هر candidate پذیرفته‌شده باید شامل این مفاهیم باشد:
- FinancialMetric با هویت پایدار و تعریف اقتصادی روشن؛
- value kind مانند amount، quantity، rate/ratio، stock یا flow؛
- unit/currency/basis منبع و canonical موردنیاز؛
- فقط dimensions مصوب و value-defining؛
- نقش presentation در صورت لزوم: detail، subtotal، total، summary، forecast یا plan.

Actual، Forecast و Plan باید از هم قابل‌تمایز باشند. Stock/Flow/Rate/Ratio/Quantity ویژگی معنایی مقدارند، نه نوع گزارش مستقل. ردیف‌های جزئیات و جمع/خلاصه نباید هم‌زمان به‌گونه‌ای پذیرفته شوند که یک مقدار اقتصادی دوباره‌شماری شود. اگر استاندارد روشن نکند کدام ردیف canonical است، کل گزارش رد می‌شود.

Dimensionهای فاقد استاندارد یا هویت پایدار، با رشتهٔ خام یا ترتیب ردیف ساخته نمی‌شوند. تا زمان تصویب Dimension، candidate وابسته به آن قابل‌پذیرش نیست.

### 4.5 Temporal interpretation

هر مقدار به FinancialPeriod واقعی خود متصل می‌شود:
- تقویم Jalali و fiscal calendar واقعی شرکت ملاک است؛
- INSTANT برای مانده‌های نقطه‌ای و DURATION برای جریان‌های بازه‌ای؛
- YTD فقط برای جریان‌های DURATION؛
- سال مالی، fiscal quarter، تاریخ شروع/پایان و months_length از شواهد معتبر تعیین می‌شوند؛
- comparative value به دوره‌ای متصل می‌شود که توصیف می‌کند، ولی ReportVersion منتشرکنندهٔ همان مقدار باقی می‌ماند؛
- source-reported standalone quarter یک fact مستقل است؛ standalone حاصل تفاضل YTD و TTM محاسبهٔ runtime هستند و در ingestion ساخته/ذخیره نمی‌شوند؛
- publication date یا ترتیب ستون‌ها به‌تنهایی دورهٔ اقتصادی را تعیین نمی‌کند.

اگر period، temporal basis یا fiscal calendar مبهم باشد، کل واحد رد می‌شود.

### 4.6 Value normalization و validation

مقدار خام فقط در حافظه parse می‌شود. مسیر canonical:
1. تشخیص وضعیت مقدار: reported numeric، explicit blank/NULL، genuine zero یا ZERO_FALLBACK مجاز؛
2. parse متن عددی با Decimal و قواعد locale/جداکنندهٔ مصوب؛
3. اعتبارسنجی sign، unit، currency، scale و basis؛
4. تبدیل مجاز فقط طبق قرارداد domain؛
5. یک‌بار ROUND_HALF_UP به INTEGER؛
6. بررسی signed 64-bit؛
7. نگهداری مقدار canonical و metadata لازم برای تفسیر آن.

ZERO_FALLBACK فقط برای product sales amount و تحت شروط مصوب مجاز است. مقدار خالی به صفر تبدیل نمی‌شود. تبدیل FX تومان به ریال استثنای دامنهٔ FX است و به FinancialFact تعمیم ندارد. هیچ rescale عمومی یا تبدیل خودکار واحد برای CODAL مجاز نیست.

### 4.7 Admission و duplicate/conflict resolution

قبل از شروع canonical write، کل واحد بررسی می‌شود:
- required identity و provenance؛
- mapping و Metric و dimensions؛
- period و temporal basis؛
- unit/value و numeric range؛
- uniqueness identity: ReportVersion + actual period + Metric + approved dimension identity؛
- تکرارهای درون فایل و برخورد با facts موجود؛
- source revision و supersession rule، در صورت وجود.

داخل batch:
- هویت یکسان + payload canonical یکسان = duplicate بی‌تغییر؛ فقط یک fact نهایی؛
- هویت یکسان + payload متفاوت = hard conflict و رد کل فایل؛
- عدد برابر به‌تنهایی duplicate identity نمی‌سازد.

در DB:
- replay همان source revision و همان canonical payload idempotent است؛
- هویت یکسان با payload متفاوت بدون revision صریح و قاعدهٔ supersession مصوب، conflict است؛
- last-write-wins، overwrite، جمع‌زدن یا انتخاب بر اساس ترتیب workbook ممنوع است؛
- uniqueness نهایی باید در DB نیز enforce شود تا concurrency را پوشش دهد.

## 5. Persistence و provenance

### 5.1 حداقل اطلاعات canonical

هر FinancialFact پذیرفته‌شده باید به‌طور قابل‌اثبات به موارد زیر متصل باشد:
- ReportVersion منتشرکننده؛
- FinancialPeriod واقعی؛
- FinancialMetric؛
- approved dimension identity، در صورت وجود؛
- canonical INTEGER value و state؛
- source unit/currency/basis و هر canonical unit/basis مجاز؛
- exact version of industry/report-family extraction and mapping standard used.

Company از ReportVersion قابل‌استنتاج است، مشروط بر آنکه consistency به‌طور پایدار enforce شود. ذخیرهٔ company_id تکراری در fact تصمیم فیزیکی جداگانه است و در این قرارداد الزامی نیست.

ReportVersion باید source artifact reference/fingerprint و publication metadata لازم را داشته باشد. fingerprint به‌تنهایی هویت revision اقتصادی نیست. IngestionRun باید adapter/profile/standard versions و source identity کافی برای audit و replay را ثبت کند.

### 5.2 عدم نگهداری raw archive

RawFinancialFact نباید به‌عنوان مخزن دائمی ردیف‌های Excel در معماری هدف باقی بماند. source observations فقط در حافظه تا پایان validation نگهداری می‌شوند. اگر نیاز موقت staging یا debugging مطرح شود، باید در تصمیمی مستقل با retention، access control و حذف تضمین‌شده بررسی شود؛ این قرارداد staging پایدار را مجاز نمی‌کند.

Locator دقیق workbook/sheet/cell برای هر fact الزام نیست. اگر adapter برای diagnostics شناسهٔ موقت ردیف/ستون تولید کند، این شناسه جایگزین provenance canonical نیست و الزام به ذخیرهٔ دائمی ندارد.

### 5.3 Derived data

DerivedFinancialFact و DerivedFinancialFactInput برای خروجی‌های محاسباتی تحلیلی در DB هدف استفاده نمی‌شوند. خروجی‌های KPI، standalone مشتق‌شده، TTM، forecast و سایر محاسبات downstream در runtime تولید می‌شوند. هر نیاز متفاوت باید با دامنه و مالکیت دادهٔ مستقل اثبات شود؛ وجود مدل legacy به‌تنهایی مجوز persistence نیست.

## 6. Atomicity و Run lifecycle

DB-DES-005 بر این مسیر حاکم است:
1. یک IngestionRun پایدار با STARTED ایجاد می‌شود.
2. parse، interpretation و validation کل فایل بدون canonical write انجام می‌شود.
3. اگر هر hard error وجود داشت، هیچ ReportVersion یا FinancialFact نوشته نمی‌شود؛ همان Run در transaction مستقل FAILED می‌شود.
4. در صورت پذیرش کامل، یک transaction واحد Report/ReportVersion، تمام FinancialFacts، provenanceهای وابسته و status=COMPLETED همان Run را commit می‌کند.
5. اگر هر write/constraint/commit شکست خورد، همهٔ canonical writes rollback می‌شوند؛ سپس همان Run در transaction مستقل FAILED می‌شود.
6. retry یک Run جدید است؛ Run قبلی immutable audit می‌ماند.

رفتار فعلی ثبت‌شده در ممیزی، که در rollback یک Run جدید FAILED می‌سازد، با این قرارداد هدف هم‌راستا نیست. این قرارداد رفتار هدف را مشخص می‌کند، نه اینکه ادعا کند implementation فعلی آن را انجام می‌دهد.

## 7. مرز مفهومی با مدل‌های legacy فعلی

| مفهوم فعلی مشاهده‌شده | تصمیم معماری هدف |
|---|---|
| RawFinancialFact | raw-row archive دائمی نباشد؛ دادهٔ موقت در حافظه تا پایان mapping/validation |
| NormalizedFinancialFact | فقط در صورت انطباق با FinancialFact canonical، INTEGER، dimensions، provenance و uniqueness قرارداد هدف قابل استفاده است؛ مدل فعلی به‌خودی‌خود تأیید نمی‌شود |
| MappingRule / MappingDecision | باید در مسیر interpretation نسخه‌دار و قابل‌ردیابی باشند؛ وجود مدل بدون writer/consumer متصل کافی نیست |
| NormalizedFinancialFactInput | فقط اگر provenance واقعی و ضروری را بدون ذخیرهٔ raw rows اضافه کند؛ شکل فیزیکی باز است |
| DerivedFinancialFact / DerivedFinancialFactInput | برای محاسبات تحلیلی persistence نشوند؛ runtime-only |
| ReportVersion | مرجع publication/revision و اتصال facts؛ immutable و دارای metadata لازم PIT |
| IngestionRun | audit یک واحد اتمیک و متصل به منبع/نسخه‌های پردازش |

این جدول دستور حذف فوری مدل/جدول یا migration نیست. پیش از هر حذف/تغییر باید usage کامل، schema و دادهٔ واقعی موجود، migration path و سازگاری consumerها بررسی شود.

## 8. مواردی که این قرارداد عمداً تعیین نمی‌کند

- نام فیزیکی جدول‌ها، ستون‌ها، foreign keyها و indexها؛
- اینکه ساختار canonical فعلی NormalizedFinancialFact با migration قابل تطبیق است یا باید جایگزین شود؛
- شکل فیزیکی mapping rules/decisions و استانداردهای versioned؛
- catalog کامل Metric و dimensionهای هر صنعت/گزارش؛
- mapping ردیف/ستون برای ۱۷ Header گزارش دوره‌ای بانک؛
- روش دقیق artifact fingerprint و source revision CODAL؛
- نحوهٔ migration یا نگهداری/انتقال داده‌های RawFinancialFact و NormalizedFinancialFact موجود؛
- retirement مدل‌های Derived* و NormalizedFinancialFactInput؛
- جزئیات error codeها و APIهای adapter/service.

این موارد نیازمند شواهد و Taskهای مستقل‌اند؛ این سند هیچ migration مخرب یا تغییر داده‌ای را مجاز نمی‌کند.

## 9. معیارهای پذیرش DB-DES-006

1. مسیر هدف از Excel adapter تا canonical FinancialFact، همهٔ مراحل interpretation و validation را بدون شکاف مفهومی پوشش دهد.
2. Source Header، Standard Header، Metric، Dimension، temporal meaning و value semantics از هم تفکیک باشند.
3. هیچ unknown/ambiguous in-scope candidate به‌صورت حدسی یا با fallback پذیرفته/حذف نشود.
4. هر fact پذیرفته‌شده exact ReportVersion، FinancialPeriod، Metric، approved dimensions و standard version را داشته باشد.
5. Raw Excel rows به‌صورت دائمی ذخیره نشوند و محاسبات derived در DB نوشته نشوند.
6. INTEGER/Decimal/ROUND_HALF_UP، NULL/zero/ZERO_FALLBACK و unit/basis fidelity رعایت شوند.
7. replay، duplicate و conflict مطابق DB-DES-001 و DB-DES-005 باشند.
8. ReportVersion، همهٔ facts و provenance و COMPLETED Run در یک transaction واحد commit شوند.
9. تفاوت مسیر فعلی و مسیر هدف و نیاز به تطبیق مدل‌ها/consumerها صریح باقی بماند.

## 10. موارد باقی‌مانده و گام بعدی

DB-DES-006 در سطح منطقی اولیه PARTIAL است؛ زیرا هنوز شواهد مستقیم workbook و mappingهای واقعی کامل در دسترس/بررسی نیست و طراحی فیزیکی خارج از دامنه است.

گام بعدی پیشنهادی، **DB-AUD-006 / implementation-readiness audit** است: inventory دقیق call-siteهای CODAL و مدل/readerهای مرتبط، تعیین منبع واقعی هر فیلد و transaction، بررسی schema و دادهٔ موجود (با دسترسی مجاز)، سپس ارائهٔ گزینهٔ migration غیرمخرب از Raw/Normalized legacy به canonical target. تا پیش از آن، هیچ مدل یا جدول legacy حذف و هیچ داده‌ای بازنویسی نشود.

**تست اجرا نشد.** این Task مستندسازی/طراحی است؛ تست‌ها را کاربر اجرا می‌کند و این سند به‌تنهایی شواهد انطباق اجرایی فراهم نمی‌کند.
