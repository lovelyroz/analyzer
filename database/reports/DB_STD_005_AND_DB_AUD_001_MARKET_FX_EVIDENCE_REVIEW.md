# DB-STD-005 / DB-AUD-001 — مرور شواهد ورودی‌های غیرصورت‌مالی و شکاف‌های ممیزی

**تاریخ:** 2026-11-15  
**وضعیت DB-STD-005:** PARTIAL — قرارداد معنایی سطح‌بالا موجود است؛ استاندارد فایل/Feed به‌دلیل نبود شواهد نمونه قابل تصویب نیست.  
**وضعیت بخش Market/FX از DB-AUD-001:** PARTIAL — یافته‌های اولیهٔ مدل و مسیرهای ingestion در Master Packet ثبت شده‌اند؛ این سند آن‌ها را یکپارچه می‌کند و ادعای ممیزی تازهٔ کد ندارد.  
**مبنای این گزارش:** اسناد Markdown موجود در مخزن، به‌ویژه Master Working Packet، Architecture و DB-DES-004. هیچ فایل XLSX/CSV منبعی در این مرحله باز یا بررسی نشده است.

## 1. نتیجهٔ اجرایی

قرارداد دامنه‌ای ورودی‌های غیرصورت‌مالی اکنون به‌اندازه‌ای روشن است که بتوان مرزهای معنایی و قواعد پذیرش را تثبیت کرد؛ اما شواهد موجود برای تصویب schema واقعی فایل‌ها کافی نیست.

سه سطح باید از هم جدا بمانند:

1. **قرارداد دامنه‌ای مصوب:** چه نوع داده‌ای پذیرفته می‌شود و معنای هر فیلد چیست.
2. **پروفایل Feed/فایل:** نام و ترتیب ستون‌ها، قالب تاریخ/عدد، encoding، واحد و قواعد اعتبارسنجی هر منبع.
3. **قرارداد persistence و runtime:** کلید یکتا، provenance، revision، PIT و انتخاب نرخ.

سطح اول در تصمیم‌های ثبت‌شده و DB-DES-004 پوشش دارد. سطح دوم هنوز فاقد شواهد کافی است. سطح سوم در سطح منطقی تعریف شده، ولی با ORM و مصرف‌کنندگان موجود تطبیق کامل نشده است.

## 2. شواهد قابل اتکا از اسناد فعلی

### 2.1 MarketDaily

دامنهٔ بازار در Master Packet و DB-DES-004 شامل دادهٔ روزانهٔ زیر است:

- Open، High، Low، Close؛
- قیمت پایانی خام؛
- قیمت پایانی تعدیل‌شدهٔ گزارش‌شده توسط منبع؛
- حجم معاملات؛
- ارزش معاملات.

این موارد فهرست مفهومی فیلدها هستند، نه اثبات نام یا ترتیب ستون‌های یک CSV مشخص. قرارداد فعلی می‌گوید قیمت تعدیل‌شده ورودی مستقل منبع است؛ برنامه نباید آن را از قیمت خام یا CorporateAction بازسازی کند. واحد، مقیاس و basis هر فیلد باید از پروفایل منبع معلوم باشد و تبدیل خودکار برای دادهٔ بازار مجاز نیست.

**هویت منطقی مصوب:** شرکت + تاریخ جلالی معامله.

### 2.2 FXRate

تصمیم‌های ثبت‌شده در Master Packet و Architecture:

- فقط FREE_MARKET و EXCHANGE_CENTER؛
- یک نرخ برای هر روز جلالی و هر نوع؛
- بدون تفکیک خرید/فروش؛
- مقدار منبع Toman به‌ازای USD؛
- مقدار canonical Rial به‌ازای USD؛
- تبدیل با Decimal(source_toman) × 10 و سپس یک ROUND_HALF_UP؛
- حفظ مقدار و واحد منبع برای provenance.

**هویت منطقی مصوب:** تاریخ جلالی + نوع نرخ.

نام ستون‌های فایل، شکل نماد نوع نرخ، قالب اعشار و نحوهٔ نمایش جداکنندهٔ هزارگان هنوز از نمونهٔ واقعی مستند نشده‌اند.

### 2.3 ShareCountHistory و CorporateAction

این دو حوزه از MarketDaily جدا هستند. تعداد سهام یک مشاهدهٔ stock با تاریخ اثر/as-of و مبنای شمارش است. CorporateAction یک رویداد مستقل با تاریخ‌های اعلام/تصویب/اثر در صورت وجود است. هیچ‌کدام نباید از دیگری یا از قیمت/حجم استنتاج شوند.

در اسناد Markdown فعلی، نمونهٔ واقعی فایل ورودی یا feed برای این دو حوزه ثبت نشده است. بنابراین قرارداد دامنه‌ای DB-DES-004 قابل استفاده است، اما استاندارد فایل/منبع برای آن‌ها هنوز تعریف نشده است.

### 2.4 شواهد نامرتبط که نباید بیش‌تفسیر شوند

گزارش DB-AUD-002_REAL_EXCEL_TEMPORAL_AUDIT.md ساختار زمانی workbookهای مالی CODAL را بررسی می‌کند. این گزارش نشان می‌دهد یک worksheet مالی ممکن است چند جدول و چند معنای زمانی داشته باشد؛ اما مدرکی دربارهٔ schema فایل CSV بازار یا فایل نرخ ارز نیست. از آن نباید نام ستون، ترتیب ستون، واحد یا قالب فایل بازار/FX استخراج کرد.

## 3. ماتریس وضعیت استاندارد ورودی

| حوزه | قرارداد دامنه‌ای | هویت منطقی | الزامات پروفایل منبع که هنوز باید اثبات شوند |
|---|---|---|---|
| MarketDaily | OHLC، خام/تعدیل‌شده، حجم، ارزش | شرکت + تاریخ معاملهٔ جلالی | نام و ترتیب ستون‌ها؛ تاریخ؛ واحد و scale هر فیلد؛ nullable بودن هر فیلد؛ encoding/delimiter؛ منبع و revision |
| FXRate | دو نوع روزانه، Toman/USD و canonical Rial/USD | تاریخ جلالی + نوع نرخ | ستون تاریخ/نرخ/نوع؛ نحوهٔ تشخیص دو نوع؛ قالب عددی؛ واحد منبع؛ منبع و زمان انتشار |
| ShareCountHistory | تعداد سهام با تاریخ اثر و basis | شرکت + تاریخ اثر + basis | نام ستون تعداد؛ تعریف دقیق basis؛ تاریخ اثر در برابر تاریخ انتشار؛ واحد شمارش؛ revision |
| CorporateAction | رویداد مستقل با تاریخ‌های معنایی | شناسهٔ منبع یا هویت رویداد قابل اثبات | کد/نوع رویداد؛ شناسه پایدار؛ تاریخ‌های اعلام/تصویب/اثر؛ شرایط و واحدها؛ status/revision |

**تفسیر:** ستون‌های لازم برای هر Feed را نمی‌توان فقط از فهرست دامنه‌ای بالا تصویب کرد. حتی اگر یک CSV نمونه دارای نام‌هایی مانند date، open یا close باشد، تا زمانی که منبع، تقویم، واحد و معنای آن‌ها مستند نشود، mapping معتبر نیست.

## 4. قواعد پذیرش سطح دامنه که همین حالا قابل تثبیت‌اند

1. شرکت بازار باید قبل از ingestion به company_id پایدار resolve شود؛ ticker به‌تنهایی شناسهٔ canonical نیست.
2. تاریخ‌های ایرانی باید با تقویم جلالی و بدون حدس دربارهٔ تقویم فایل parse شوند.
3. برای MarketDaily، تاریخ معامله؛ برای ShareCountHistory، تاریخ اثر/as-of؛ و برای CorporateAction، تاریخ اثر رویداد باید از زمان انتشار/اعلام جدا باشد.
4. واحد، scale و basis هر ستون باید در پروفایل Feed مشخص باشد. نبود این اطلاعات به معنی رد/توقف ورودی است، نه حدس یا تبدیل.
5. همهٔ اعداد canonical با Decimal و یک‌بار ROUND_HALF_UP به SQLite INTEGER تبدیل می‌شوند؛ برای FX ابتدا ضرب در ۱۰ و سپس گردکردن انجام می‌شود.
6. صفر واقعی از NULL/مفقود جداست. interpolation، carry-forward یا پرکردن مقدار مفقود در ingestion مجاز نیست.
7. تکرار همان ورودی idempotent است. تعارض برای هویت منطقی واحد بدون قاعدهٔ revision یا تقدم منبع مصوب، رد می‌شود.
8. در صورت وجود چند منبع بازار، انتخاب منبع بر اساس ترتیب فایل یا آخرین ingestion ممنوع است؛ باید سیاست تقدم منبع تصویب شود.
9. publication/availability time منبع با ingestion time متفاوت است. نبود زمان منبع، استفادهٔ تاریخی PIT را ناممکن می‌کند.
10. CSV/XLSX قالب adapter هستند؛ فایل خام لازم نیست به‌عنوان دادهٔ canonical ذخیره شود.

## 5. یافته‌های ممیزی فعلی مدل و مسیرها — برگرفته از Master Packet

این بخش بازنویسی/تجمیع یافته‌های ثبت‌شده در بخش‌های 4.3 و 4.5 Master Working Packet است؛ بازبینی مستقیم کد در این مرحله انجام نشده است.

### 5.1 MarketDaily

- جدول ORM فعال: market_daily؛ مدل: MarketDaily.
- مسیر نوشتن ثبت‌شده: src/ingestion/market/ingestion.py::ingest_ohlc_csv.
- upsert ثبت‌شده از طریق find_market_daily_existing در src/ingestion/common/identity.py.
- مسیر خواندن ثبت‌شده: src/ingestion/market/queries.py.
- شرکت در مسیر فعلی با ticker جست‌وجو می‌شود.
- تاریخ ورودی CSV در اجزای Jalali ذخیره می‌شود و trade_date=None است.
- unique constraint گزارش‌شدهٔ فعلی (company_id, trade_date) است؛ چون trade_date در مسیر جلالی NULL می‌ماند، این قید به‌تنهایی یکتایی روزانهٔ جلالی را تضمین نمی‌کند.
- نیاز به بررسی unique constraint مبتنی بر Jalali components و رفتار upsert در برابر آن ثبت شده است.

**ریسک:** یکتایی منطقی قرارداد DB-DES-004 و یکتایی فیزیکی گزارش‌شده در ممیزی فعلی هنوز هم‌راستا اثبات نشده‌اند.

### 5.2 FXRate

- جدول ORM فعال: fx_rates؛ مدل: FXRate.
- مسیر نوشتن ثبت‌شده: src/ingestion/service.py::ingest_fx_rates و facade در src/ingestion/fx/ingestion.py.
- upsert ثبت‌شده از طریق find_fx_existing.
- تاریخ جلالی به‌صورت سه جزء ذخیره می‌شود و rate_date=None است.
- unique constraint گزارش‌شدهٔ فعلی (rate_date, currency_from, currency_to, rate_type) است؛ در نتیجه وقتی rate_date NULL است، این قید لزوماً یکتایی منطقی روز/نوع را تضمین نمی‌کند.
- مسیرهای خواندن FX هنوز در ممیزی قبلی کامل فهرست نشده‌اند.

**ریسک:** باید کلید یکتا و upsert بر پایهٔ اجزای جلالی و rate_type با یکدیگر و با داده‌های موجود تطبیق داده شوند.

### 5.3 ShareCountHistory و CorporateAction

- جدول‌های ORM فعال: share_count_history و corporate_actions.
- ممیزی قبلی writer فعال در مسیرهای ingestion بررسی‌شده پیدا نکرده است.
- مدل‌ها هنوز از SQL Date استفاده می‌کنند؛ معنا و مهاجرت تاریخ‌ها باید با قرارداد Jalali و تفکیک effective date از publication time تطبیق داده شود.
- مصرف‌کنندگان downstream به‌طور کامل فهرست نشده‌اند.
- Master Packet یک مصرف‌کنندهٔ forecast را ثبت می‌کند که تاریخ‌های ShareCountHistory و CorporateAction را با normalize_datetime(cutoff).date() مقایسه می‌کند؛ این مسیر نیازمند تطبیق با قرارداد تقویم و PIT است.

**ریسک:** وجود جدول، به‌تنهایی وجود مسیر ingestion معتبر یا سازگاری مصرف‌کننده را اثبات نمی‌کند.

### 5.4 Migration و تست

- migration شمارهٔ ۵ سه جزء Jalali را به market_daily اضافه می‌کند.
- migration شمارهٔ ۶ سه جزء Jalali را به fx_rates اضافه می‌کند.
- تست‌های Market/FX و Jalali در tree گزارش شده‌اند، اما ماتریس پوشش و انطباق آن‌ها با قرارداد جدید در گزارش فعلی اثبات نشده است.
- تست‌های migration موجود در SQLite in-memory به‌تنهایی وضعیت نصب‌های واقعی یا داده‌های legacy را اثبات نمی‌کنند.
- هیچ migration یا تستی در این بررسی اجرا نشده است.

## 6. شواهد لازم برای تکمیل DB-STD-005

برای هر Feed باید یک نمونهٔ واقعی و قابل انتساب به منبع در اختیار ممیزی قرار گیرد؛ حداقل:

### Market CSV
- یک فایل نمونهٔ واقعی و نام/نسخهٔ منبع آن؛
- header دقیق و چند ردیف دادهٔ نماینده، شامل مقادیر خالی/صفر در صورت وجود؛
- تعریف واحد و scale برای OHLC، close خام/تعدیل‌شده، volume و value؛
- تقویم و قالب دقیق تاریخ؛
- timezone/زمان انتشار یا توضیح صریح اینکه منبع چنین زمانی ارائه نمی‌کند؛
- تعریف رفتار فایل تکراری و اصلاحیهٔ منبع.

### FX input
- یک نمونه برای هر یک از FREE_MARKET و EXCHANGE_CENTER؛
- تعریف صریح اینکه نوع نرخ در ستون است یا از منبع/فایل مشخص می‌شود؛
- قالب عددی و واحد Toman/USD؛
- تاریخ جلالی و زمان انتشار/دسترس‌پذیری؛
- رفتار اصلاحیه و duplicate.

### Share count و CorporateAction
- نمونهٔ منبع واقعی یا تصریح اینکه در V1 فعلاً ورودی دستی/منبع دیگری دارند؛
- تعریف تاریخ اثر در برابر تاریخ انتشار؛
- مبنای شمارش سهم؛
- شناسهٔ رویداد، نوع رویداد و تاریخ‌های آن در صورت وجود.

بدون این شواهد، نباید نام ستون، نوع دادهٔ ورودی، required/optional بودن فیلدها یا source priority را نهایی کرد.

## 7. اقدامات بعدی و معیار بستن

| اقدام | خروجی مورد انتظار | وضعیت |
|---|---|---|
| دریافت نمونهٔ واقعی Market CSV و مشخصات منبع | Feed profile بازار با header، تاریخ، واحد و validation | BLOCKED — نمونه/مشخصات در اسناد فعلی موجود نیست |
| دریافت نمونهٔ FX برای هر دو نوع | Feed profile FX و mapping قطعی نوع نرخ | BLOCKED — نمونه/مشخصات در اسناد فعلی موجود نیست |
| تعیین منبع و قالب ShareCount/CorporateAction | تصمیم ورودی V1 و معنای تاریخ‌ها | OPEN |
| تطبیق کلید یکتا و upsert Market/FX | تصمیم سازگار با Jalali components و دادهٔ legacy | OPEN — نیازمند ممیزی کد/schema |
| فهرست‌کردن readerها و writerهای Share/Action و FX | call-site map کامل | OPEN |
| تطبیق consumerهای Share/Action با Jalali/PIT | قرارداد cutoff و تاریخ معتبر | OPEN |
| بررسی migrationهای 5 و 6 و داده‌های موجود | طرح migration امن و گزارش موارد مبهم | OPEN |

**نتیجه DB-STD-005:** PARTIAL. قرارداد دامنه و قواعد عمومی پذیرش روشن است، ولی استاندارد فایل واقعی قابل تصویب نیست تا نمونه‌های واقعی و مشخصات منبع فراهم شوند.

**نتیجه بخش Market/FX از DB-AUD-001:** PARTIAL. دو شکاف روشن در unique constraintهای فعلی MarketDaily و FXRate و چند شکاف در مسیرهای Share/CorporateAction ثبت شده‌اند. این گزارش جایگزین ممیزی مستقیم کد و schema نیست.

هیچ XLSX/CSV منبعی بازبینی نشد. هیچ کد، ORM، schema، migration، داده یا تستی تغییر نکرد و هیچ تستی اجرا نشد.


## 8. تکمیل ممیزی مستقیم کد — 2026-11-15

**دامنهٔ بررسی مستقیم:** مدل‌های ORM و مسیرهای فعال زیر در شاخهٔ جاری خوانده شدند:
- `src/models/market.py`, `src/models/fx.py`, `src/models/share_action.py`
- `src/ingestion/market/adapter.py`, `src/ingestion/market/ingestion.py`, `src/ingestion/market/queries.py`
- `src/ingestion/fx/adapter.py`, `src/ingestion/fx/ingestion.py`, بخش `ingest_fx_rates` در `src/ingestion/service.py`
- `src/ingestion/common/identity.py`, `src/ingestion/common/validation.py`, `src/ingestion/common/parsing.py`
- `src/forecast/queries.py::load_share_history`

این مرور، کدهای فوق را مستقیماً بررسی می‌کند؛ اما هنوز inventory همهٔ migrationها، همهٔ call-siteها، queryهای FX و تمام تست‌ها نیست. هیچ تستی اجرا نشد.

### 8.1 یافته‌های قطعی مدل‌ها و قیود

| دامنه | وضعیت فعلی مشاهده‌شده | مغایرت/ریسک نسبت به قرارداد |
|---|---|---|
| MarketDaily | `trade_date` nullable؛ سه جزء Jalali nullable؛ unique فقط روی `(company_id, trade_date)` | برای رکوردهای Jalali با trade_date=NULL یکتایی روز/شرکت enforce نمی‌شود؛ اجزای تاریخ نیز constraint کامل/اجباری ندارند |
| MarketDaily numeric | قیمت‌ها و value از نوع Numeric؛ volume و trade_count از نوع Integer | با قرارداد persistence عددی INTEGER برای همهٔ ورودی‌های عددی هم‌راستا نیست |
| FXRate | `rate_date` nullable؛ Jalali components nullable؛ unique روی `(rate_date,currency_from,currency_to,rate_type)` | برای نرخ‌های Jalali با rate_date=NULL یکتایی روز/نوع/جفت ارز enforce نمی‌شود |
| FXRate rate types | CheckConstraint شامل FREE_MARKET و چهار نوع قدیمی دیگر است | EXCHANGE_CENTER در constraint مدل وجود ندارد و انواع خارج از قرارداد V1 هنوز مجازند |
| FXRate numeric/provenance | `rate` از نوع Numeric؛ فقط source label ذخیره می‌شود | INTEGER canonical و نگهداری مقدار/واحد Toman منبع و publication/availability metadata در مدل دیده نمی‌شود |
| ShareCountHistory | effective_date از نوع SQL Date؛ unique روی company_id/effective_date؛ shares_outstanding Integer و capital Numeric | تقویم/معنای تاریخ با قرارداد Jalali تطبیق ندارد؛ basis شمارش در هویت/مدل نیست؛ provenance و publication time موجود نیست |
| CorporateAction | announcement_date/effective_date از نوع SQL Date؛ unique روی company_id/effective_date/action_type | شناسهٔ پایدار منبع، approval date، revision/status و publication/availability metadata در مدل دیده نمی‌شود؛ دو رویداد هم‌نوع در یک تاریخ ممکن است به‌اشتباه یکی فرض شوند |

### 8.2 Market adapter و writer

1. `load_ohlc_csv_rows` فقط وجود ستون تاریخ و ticker را الزامی می‌کند؛ واحد، scale و basis ستون‌های عددی در adapter احراز نمی‌شود.
2. ستون تعدیل‌شدهٔ منبع با aliasهایی مانند `final`/`adjclose` خوانده می‌شود؛ اگر مقدار آن خالی باشد، adapter مقدار `close` را به‌عنوان `adjusted_close` کپی می‌کند. این fallback، دو ورودی مستقل را مخلوط می‌کند و با قرارداد منبع‌محور adjusted close ناسازگار است.
3. `to_int` مقدار Decimal را با `int(...)` تبدیل می‌کند؛ بخش اعشاری truncate می‌شود، نه اینکه ROUND_HALF_UP مصوب اعمال شود.
4. writer شرکت را با ticker جست‌وجو می‌کند و در رکورد موجود، تمام مقادیر و source را بی‌قیدوشرط overwrite می‌کند. منبع متفاوت، revision، publication time و conflict بررسی نمی‌شوند؛ این رفتار last-write-wins است.
5. فایل دارای خطاهای ردیفی می‌تواند با رکوردهای معتبر دیگر commit شود؛ بنابراین writer فعلی برای یک batch mixed-validity رفتار all-or-nothing ندارد.
6. writer یک IngestionRun را STARTED می‌کند و در exception rollback کرده و یک FAILED run تازه ثبت می‌کند؛ این الگو از باقی‌ماندن canonical writes در exception جلوگیری می‌کند، اما خطاهای ردیفیِ جمع‌آوری‌شده مانع commit بقیهٔ ردیف‌ها نیستند.

### 8.3 FX adapter و writer

1. adapter فعلی ورودی XLSX دو ستونی (تاریخ و نرخ) است؛ این با قرارداد سطح دامنه‌ای CSV/XLSX قابل‌تعویض تعارض ندارد، اما Feed profile واقعی هنوز اثبات نشده است.
2. `rates_in_toman=True` مقدار نرخ را در adapter در ۱۰ ضرب می‌کند؛ DTO فقط `rate` canonical را حمل می‌کند و مقدار خام Toman/واحد آن را جداگانه حفظ نمی‌کند. بنابراین provenance تبدیل طبق قرارداد جدید کامل نیست.
3. FX DTO و adapter فقط rate_type را از whitelist فعلی می‌پذیرند؛ whitelist فعلی FREE_MARKET، OPERATIONAL، OFFICIAL، ESTIMATED و MANUAL_OPERATOR است و EXCHANGE_CENTER را نمی‌پذیرد. این با دو نوع مصوب V1 وارونه/ناسازگار است.
4. writer برای Jalali components یا Gregorian rate_date هویت می‌سازد، اما تاریخ Gregorian را برای Jalali row NULL می‌گذارد؛ این با unique constraint فعلی مشکل بند 5.2 را ایجاد می‌کند.
5. در صورت یافتن رکورد موجود، rate و source بدون بررسی مقدار متعارض، منبع یا revision overwrite می‌شوند؛ رفتار last-write-wins است.
6. آیتم‌های نامعتبر به failed count افزوده می‌شوند، ولی سایر آیتم‌ها commit می‌شوند؛ batch all-or-nothing نیست.
7. FXConversionRule model نیز rate_typeهای قدیمی را در CheckConstraint مجاز می‌داند و EXCHANGE_CENTER را در فهرست ندارد.
8. زمان انتشار/دسترس‌پذیری منبع و مقدار خام Toman در مدل/DTO بررسی‌شده مشاهده نشد.

### 8.4 Share / CorporateAction و مصرف‌کننده

1. در مدل‌های بررسی‌شده، ShareCountHistory و CorporateAction تعریف شده‌اند؛ در مسیرهای ingestion بررسی‌شده writer فعال برای آن‌ها مشاهده نشد. این نتیجه محدود به مسیرهای بررسی‌شده است و ادعای نبود writer در کل repository نیست.
2. `load_share_history` در `src/forecast/queries.py` تاریخ cutoff را با `normalize_datetime(cutoff).date()` به Gregorian date تبدیل می‌کند و با `effective_date` و `announcement_date` مقایسه می‌کند.
3. فیلتر CorporateAction از `coalesce(announcement_date, cutoff_date) <= cutoff_date` استفاده می‌کند؛ وقتی announcement_date NULL است، شرط عملاً آن رویداد را صرفاً بر اساس effective_date عبور می‌دهد. این رفتار با قاعدهٔ PIT قرارداد DB-DES-004 که زمان انتشار/دسترس‌پذیری نامعلوم را برای historical PIT غیرواجد شرایط می‌داند، سازگار نیست.
4. این consumer هنوز بر SQL Date تکیه دارد؛ تا تعیین طرح تاریخ Jalali و publication-time، تبدیل یا مهاجرت دادهٔ موجود نباید حدس زده شود.

### 8.5 شکاف‌های اولویت‌دار برای طراحی/اصلاح بعدی

| اولویت | شکاف | تصمیم/کار لازم |
|---|---|---|
| P0 | کلید یکتای Jalali در MarketDaily و FXRate | طراحی constraint/index و تطبیق با NULLها و legacy rows در DB-MIG-001؛ پیش از آن upsert قابل اتکا نیست |
| P0 | overwrite تعارض در Market و FX | قرارداد revision/source precedence و conflict handling؛ ممنوعیت last-write-wins |
| P0 | FX type catalog ناسازگار | هم‌راستاسازی constraint، validator، DTO و adapter با FREE_MARKET و EXCHANGE_CENTER |
| P0 | adjusted_close fallback به close | حذف fallback معنایی؛ NULL مستقل بماند مگر منبع adjusted close داده باشد |
| P1 | عددهای Numeric و truncation | پیاده‌سازی INTEGER + Decimal + ROUND_HALF_UP در مرز persistence و طرح migration |
| P1 | نبود provenance منبع FX و publication time | DTO/model contract برای source amount/unit و availability time |
| P1 | Share/Action تاریخ Gregorian و نبود PIT metadata | تعیین ورودی/تقویم/زمان انتشار و سپس طراحی migration و consumer |
| P1 | batch partial commit در Market/FX | هماهنگی transaction boundary و atomicity در DB-DES-005 |
| P2 | coverage کامل readerها/writerها/migrations/tests | ادامهٔ inventory repository و مقایسهٔ schema migration با ORM |

**نتیجهٔ به‌روزشدهٔ بخش Market/FX از DB-AUD-001:** PARTIAL. این گزارش اکنون یافته‌های مستقیم مدل‌ها و مسیرهای فوق را ثبت می‌کند؛ inventory کامل migrationها، همهٔ call-siteها، queryهای FX، schema واقعی DB و تست‌ها هنوز انجام نشده است.

**نتیجه DB-STD-005:** PARTIAL/BLOCKED در سطح Feed profile باقی می‌ماند؛ کد فعلی adapterها، نمونهٔ واقعی feed یا سند منبع محسوب نمی‌شود و header/واحد/scale را برای منبع ناشناخته تصویب نمی‌کند.

هیچ فایل XLSX/CSV منبعی بازبینی نشد. هیچ کد، ORM، schema، migration یا داده‌ای تغییر نکرد و هیچ تستی اجرا نشد.


## 9. ممیزی مستقیم Migration Runner و مرزهای تراکنش — 2026-11-15

**دامنهٔ بررسی مستقیم:** `src/migrations/runner.py`، `src/core/database.py`، `src/models/audit.py`، `src/ingestion/common/run_tracker.py`، `src/ingestion/codal/ingestion.py`، `src/ingestion/codal/pipeline.py`، مسیرهای CODAL و FX در `src/ingestion/service.py` و `src/ingestion/market/ingestion.py` خوانده شدند. این بررسی، inventory کامل تمام 128 فایل Python یا تمام callerهای Session نیست؛ فقط call-siteهای صریحاً بررسی‌شده در زیر مبنای نتیجه‌اند. هیچ migration یا تستی اجرا نشد.

### 9.1 Migration Runner — نسخه‌های 1 تا 8

Migrationها به‌صورت توابع Python در یک فایل `src/migrations/runner.py` تعریف شده‌اند؛ فایل مستقل migration برای هر نسخه در tree جاری دیده نشد. فهرست اجرایی:

| Version | Name | رفتار مشاهده‌شده |
|---|---|---|
| 1 | `baseline_schema` | `Base.metadata.create_all(bind=engine)` |
| 2 | `mapping_and_derived_schema` | چند `ALTER TABLE` از طریق helperهای جداگانه و سپس `create_all` برای چهار جدول |
| 3 | `normalized_fact_multi_source_provenance` | `create_all` برای جدول provenance |
| 4 | `one_current_report_version` | بررسی duplicate در connection و سپس ساخت partial unique index در `engine.begin()` |
| 5 | `market_daily_jalali_components` | افزودن سه ستون Jalali به‌صورت additive |
| 6 | `fx_rates_jalali_components` | افزودن سه ستون Jalali به‌صورت additive |
| 7 | `forecast_version_repository` | ساخت دو جدول legacy forecast |
| 8 | `remove_forecast_output_persistence` | حذف دو جدول forecast با `DROP TABLE IF EXISTS` |

**یافته‌های تراکنشی مهم:**

1. `MigrationRunner.upgrade()` هر migration را اجرا می‌کند و پس از بازگشت تابع `apply`، رکورد `schema_migrations` را در یک `engine.begin()` جداگانه درج می‌کند. بنابراین تغییر schema و ثبت شمارهٔ migration یک تراکنش واحد نیستند. اگر DDL موفق شود ولی درج version marker شکست بخورد، اجرای بعدی ممکن است migration را دوباره اجرا کند؛ idempotency برخی عملیات این خطر را کاهش می‌دهد، اما atomicity کلی را تضمین نمی‌کند.
2. Migration 2 چند عملیات مستقل دارد: هر `_add_column_if_missing` در تراکنش جداگانه اجرا می‌شود و سپس `create_all` انجام می‌شود. شکست میانی می‌تواند schema نیمه‌اعمال‌شده باقی بگذارد، درحالی‌که version هنوز ثبت نشده است.
3. Migration 4 بررسی duplicate را خارج از تراکنش ساخت index انجام می‌دهد. این جدایی، فاصله‌ای میان precondition check و enforce شدن قید ایجاد می‌کند.
4. Migration 1 و برخی `create_all`ها در سطح فراخوانی `engine.begin()` واحد با درج version marker قرار ندارند.
5. Migration 8 حذف جدول انجام می‌دهد؛ این تغییر از نظر داده برگشت‌پذیر نیست مگر backup/restore یا بازسازی داده از منبع موجود باشد. وجود آن در تاریخچه، نیاز به backup/rollback strategy پیش از اجرای محیط واقعی را برجسته می‌کند.
6. Runner نسخه‌ها را به‌ترتیب اجرا می‌کند و در پایان شمارهٔ آخر را برمی‌گرداند؛ اما سازوکار ثبت checksum، قفل اجرای هم‌زمان migration، downgrade یا rollback عملیاتی در فایل بررسی‌شده مشاهده نشد. نبود آن‌ها در این فایل به‌تنهایی اثبات نبود در کل سامانه نیست.

### 9.2 Session و IngestionRun

- `SessionLocal` با `autocommit=False` و `autoflush=False` ساخته شده است؛ در فایل `src/core/database.py` وابستگی/مدیریت چرخهٔ عمر Session یا context manager مخصوص ingestion دیده نشد.
- مدل `IngestionRun` فقط `source`، زمان شروع/پایان، status، شمارنده‌های found/inserted/updated/failed و `error_log` را دارد. fingerprint منبع، source revision، adapter/profile/standard version، شمارندهٔ unchanged/out_of_scope/rejected و ساختار خطا در مدل مشاهده نشد.
- `start_run()` در `run_tracker.py` فقط add و flush می‌کند و commit نمی‌کند؛ `complete_run()` فقط فیلدها را تغییر می‌دهد و commit نمی‌کند؛ اما `fail_run()` خودش commit می‌کند. این APIها مرز تراکنش یکنواختی ندارند.
- مقدار `finished_at` در برخی مسیرها با `datetime.utcnow()` و در مسیرهای دیگر با UTC-aware سپس حذف timezone ساخته می‌شود؛ قرارداد زمانی و convention باید یکسان شود.

### 9.3 Call-siteهای تراکنش که مستقیماً مشاهده شدند

| مسیر | رفتار مشاهده‌شده | مغایرت با DB-DES-005 |
|---|---|---|
| `service.py::ingest_codal_report` | STARTED با flush؛ ساخت Report/ReportVersion/Facts؛ COMPL​ETED و canonical writes با یک commit؛ در exception rollback و سپس FAILED در commit جداگانه | الگوی کلی به atomicity نزدیک است؛ اما Run شروع‌شده در rollback از بین می‌رود و به‌جای update همان Run، رکورد FAILED جدید ساخته می‌شود. مسیر idempotent موجود بر اساس tracking ID و publication datetime، payload را مقایسه نمی‌کند و در صورت یافتن نسخه، شمارنده را در `records_updated` ثبت می‌کند |
| `service.py::ingest_fx_rates` | STARTED با flush؛ ردیف‌های نامعتبر فقط به شمارنده اضافه و از حلقه عبور می‌کنند؛ ردیف‌های معتبر upsert می‌شوند؛ در پایان COM​PLETED با commit؛ exception باعث rollback و درج FAILED جداگانه می‌شود | batch دارای ردیف نامعتبر همچنان با status=COMPLETED و بخشی از داده commit می‌شود؛ برخلاف رد کامل Ingestion Unit. تعارض موجود نیز overwrite می‌شود |
| `market/ingestion.py::ingest_ohlc_csv` | STARTED با flush؛ خطاهای parse/validation/company به شمارنده افزوده و ادامه می‌یابد؛ رکوردهای موجود overwrite می‌شوند؛ در پایان COMPLETED و داده با هم commit می‌شوند؛ exception rollback و FAILED جدید | پذیرش جزئی در حضور خطای ردیف؛ overwrite بدون revision/conflict؛ خطای empty/invalid CSV نیز FAILED را commit می‌کند ولی `records_failed=0` ثبت می‌شود |
| `codal/ingestion.py::ingest_codal_pdf` و `codal/pipeline.py` | در خطای acquisition/extraction/validation، rollback و سپس درج FAILED و commit؛ مسیر PDF legacy است | audit شکست مستقل است، اما مسیر جاری V1 نیست و نباید مبنای قرارداد Excel تلقی شود |

**نتیجه:** مسیر CODAL service از نظر یک commit برای Report/Version/Facts و FAILED audit جداگانه، به الگوی منطقی نزدیک‌تر است؛ اما lifecycle و idempotency آن کامل نیست. مسیرهای FX و Market صریحاً پذیرش جزئی و overwrite دارند و با DB-DES-005 ناسازگارند. این ناسازگاری‌ها فعلاً یافتهٔ ممیزی‌اند، نه مجوز اصلاح خودکار کد.

### 9.4 شکاف‌های مهم برای بستن ممیزی

1. تکمیل inventory تمام callerهای Session و همهٔ `commit()`/`rollback()` در کل `src/`، به‌ویژه seed، scripts، forecast و سایر سرویس‌های مصرف‌کننده.
2. تطبیق تمام مدل‌ها و ORM metadata با migration history و schema واقعی دیتابیس‌های موجود؛ این مرحله به دسترسی و snapshot از DB واقعی نیاز دارد و با خواندن کد جایگزین نمی‌شود.
3. تعیین راهبرد atomicity برای خود migrationها: transaction-per-migration شامل DDL و version marker در حد پشتیبانی SQLite، قفل اجرای هم‌زمان، تشخیص migration نیمه‌اعمال‌شده و backup/restore.
4. بازطراحی IngestionRun و tracker برای lifecycle واحد STARTED→COMPLETED/FAILED، حفظ audit شکست بدون partial canonical writes و ثبت metadata لازم.
5. حذف row-level partial acceptance در Market/FX و پیاده‌سازی duplicate/conflict/revision مطابق DB-DES-005.
6. بررسی تست‌های موجود به‌صورت ایستا و تدوین ماتریس تست؛ تست‌ها اجرا نشدند.

**وضعیت DB-AUD-001:** PARTIAL. Migration runner نسخه‌های 1–8 و چند مرز تراکنش مهم مستقیماً بررسی شدند؛ اما inventory کامل call-siteها، schema واقعی پایگاه‌های موجود، تمام readerها و تست‌ها هنوز بسته نشده‌اند. هیچ XLSX/CSV منبعی بررسی نشد. هیچ کد، ORM، schema، migration یا داده‌ای تغییر نکرد و هیچ تستی اجرا نشد.


## 10. مرور ایستای call-siteهای تکمیلی و تست‌های موجود — 2026-11-15

### 10.1 Session lifecycle و write entry points تکمیلی

- `src/scripts/seed_data.py` تنها مصرف مستقیم `SessionLocal` در فایل‌های اجرایی تکمیلیِ این مرحله بود: یک Session می‌سازد، صنایع و Metricهای پایه را با check-before-insert اضافه می‌کند، در پایان یک `commit()` دارد، در exception یک `rollback()` انجام می‌دهد و در `finally` می‌بندد. این الگو برای seed یک batch واحد است، اما مدیریت خطا exception را پس از rollback جذب و فقط چاپ می‌کند؛ بنابراین caller ممکن است از شکست seed با exit status موفق مطلع نشود.
- `src/scripts/init_db.py` از نظر call-site صریح commit/rollback ندارد؛ migration را از مسیر runner انجام می‌دهد.
- `src/scripts/migrate_db.py` صرفاً `MigrationRunner.upgrade()` را فراخوانی می‌کند و transaction دیگری در خود script ندارد.
- در فایل‌های `forecast/queries.py`، readهای مستقیم با `session.execute()` برای queryهای history/share/action مشاهده شدند؛ این مسیرها read-only هستند و transaction write در آن‌ها مشاهده نشد. وجود read call-siteهای دیگر در تمام forecast/market/valuation و سایر 128 فایل هنوز به‌صورت exhaustively خط‌به‌خط بسته نشده است.
- فایل‌های `src/ingestion/fx/ingestion.py` و `src/ingestion/market/queries.py` در بررسی صریح این مرحله commit/rollback نداشتند؛ writer FX در `src/ingestion/service.py` و writer Market در `src/ingestion/market/ingestion.py` قرار دارند.
- helperهای `src/ingestion/common/idempotency.py` و `identity.py` در نسخه‌های بررسی‌شده transaction boundary ندارند؛ identity helpers queryهای موجود را پیدا می‌کنند و خودشان commit نمی‌کنند.

### 10.2 شواهد تستیِ ناسازگار با قرارداد جدید

تست‌ها اجرا نشدند؛ فقط source آن‌ها خوانده شد.

| تست/فایل | رفتاری که تست فعلی تثبیت می‌کند | ارزیابی در برابر DB-DES-005 |
|---|---|---|
| `test_ingestion_fx.py::test_fx_idempotent_upsert_jalali` | ارسال دوبارهٔ همان هویت با نرخ متفاوت باید رکورد قبلی را overwrite کند و `records_updated=1` شود | این رفتار last-write-wins است و با duplicate/conflict و immutable revision ناسازگار است |
| `test_ingestion_fx.py::test_invalid_rate_type_and_non_positive_rate_fail_explicitly` | از چهار ردیف، سه ردیف نامعتبر می‌شوند اما یک ردیف معتبر commit می‌شود؛ status همچنان COMPLETED است | صریحاً partial acceptance را به‌عنوان رفتار مورد انتظار تثبیت می‌کند؛ باید در بازطراحی تست به رد کل batch تبدیل شود |
| `test_ingestion_ohlc.py::test_ingest_ohlc_idempotent` | اجرای دوبارهٔ همان CSV رکوردها را update می‌کند؛ تعداد ردیف ثابت می‌ماند | idempotency با overwrite پیاده شده، نه unchanged/no-op برای payload یکسان و conflict برای payload متفاوت |
| `test_codal_extraction.py` | acquisition/extraction failure بدون Report/RawFinancialFact را می‌سنجد؛ نسخهٔ دوم با publication date متفاوت، ReportVersion جدید می‌سازد | پوشش PDF legacy است؛ fingerprint/replay یک source revision یکسان با payload متفاوت، atomicity چند fact در failure میانی و حفظ همان Run در FAILED را کامل نمی‌آزماید |
| `test_stage1_database_integrity.py` | migration از صفر به نسخهٔ 8 و اجرای مجدد بدون تغییر نسخه را بررسی می‌کند؛ Migration 8 جدول‌های legacy forecast را حذف می‌کند و برخی داده‌های دیگر را حفظ می‌کند | happy-path/idempotent upgrade را پوشش می‌دهد؛ crash بین DDL و version marker، migration نیمه‌اعمال‌شده، اجرای هم‌زمان و recovery/backup آزموده نشده‌اند |
| `test_stage1_database_architecture.py` | ساخت دادهٔ normalized و روابط provenance را با commit مستقیم در تست انجام می‌دهد | تست integrity دامنه‌ای است، نه آزمون transaction boundary سرویس ingestion |

**نتیجهٔ تستی:** بخشی از تست‌های فعلی نه‌فقط فاقد پوشش قرارداد جدیدند، بلکه رفتارهای قدیمیِ partial acceptance و overwrite را به‌عنوان انتظار صحیح ثبت کرده‌اند. این تست‌ها هنگام اجرای مرحلهٔ implementation باید بازنویسی شوند؛ در این مرحله هیچ تستی تغییر یا اجرا نشد.

### 10.3 ماتریس مغایرت اجراییِ فعلی با DB-DES-005

| الزام قرارداد | وضعیت مشاهده‌شده | اولویت پیگیری |
|---|---|---|
| یک Ingestion Unit اتمیک؛ hard error کل batch را رد کند | Market و FX ردیف‌های نامعتبر را کنار می‌گذارند و بقیه را commit می‌کنند | بحرانی |
| identical identity + identical payload = no-op | Market/FX در اجرای مجدد شمارندهٔ updated دارند؛ FX تست مقدار را overwrite می‌کند | بحرانی |
| identical identity + different payload = conflict؛ بدون overwrite | Market/FX مقدار موجود را بازنویسی می‌کنند | بحرانی |
| audit STARTED/COMPLETED/FAILED برای همان Run | مسیرهای اصلی در rollback رکورد STARTED را از دست می‌دهند و FAILED جدید می‌سازند؛ tracker نیز fail_run را جداگانه commit می‌کند | بالا |
| audit metadata شامل source fingerprint/revision و standard/adapter version | مدل فعلی این فیلدها را ندارد | بالا |
| شمارنده‌های دقیق inserted/updated/unchanged/rejected/out_of_scope | مدل فعلی فقط found/inserted/updated/failed دارد؛ معنای updated در CODAL نیز برای replay به‌کار رفته است | متوسط |
| migration و version marker با recovery امن | migration runner این دو را در تراکنش واحد تضمین نمی‌کند؛ crash recovery و concurrency coverage وجود ندارد | بالا |
| caller واحد مالک transaction باشد | writerها خودشان commit/rollback می‌کنند؛ helperهای audit مرز یکنواخت ندارند | بالا |
| تست‌های failure injection، rollback و retry | در تست‌های بررسی‌شده پوشش کافی مشاهده نشد؛ تست‌ها اجرا نشده‌اند | بالا |

### 10.4 حدود نتیجه‌گیری و موارد باز

این مرحله یک مرور هدفمند از فایل‌های اجرایی و تست‌های مرتبط با DB/ingestion بود، نه ادعای اثبات نبود هر commit یا query در کل مخزن. GitHub tree شامل 128 فایل Python در `src/` است؛ همهٔ آن‌ها از نظر تمام read/write call-siteها خط‌به‌خط ممیزی نشده‌اند. همچنین هیچ فایل DB واقعی، XLSX یا CSV منبع بررسی نشده است. برای تکمیل قطعی inventory باید همهٔ مسیرهای فراخوانی Session در سرویس‌ها و مصرف‌کنندگان و schema واقعی DBهای عملیاتی جداگانه بررسی شوند.

**وضعیت DB-AUD-001:** PARTIAL. مرور هدفمند transaction entry points، seed script، readerهای مشخص و تست‌های مرتبط اضافه شد. شکاف‌های مهم قرارداد با تست‌های فعلی شناسایی و اولویت‌بندی شدند؛ اما inventory کامل تمام 128 فایل، تمام readerها و schema واقعی DB هنوز باز است. هیچ کد، ORM، schema، migration یا داده‌ای تغییر نکرد و هیچ تستی اجرا نشد.



## 11. مرور هدفمند مصرف‌کنندگان downstream و انتخاب PIT — 2026-11-15

### 11.1 مسیرهای خواندن مالی و انتخاب نسخه

فایل‌های `src/forecast/queries.py`، `src/core/point_in_time.py`، مدل‌های `report.py`، `normalized.py` و `period.py` مستقیماً خوانده شدند.

1. **PIT مالی در Forecast:** تابع `_period_rows()` در `forecast/queries.py` شرط `ReportVersion.publication_datetime <= cutoff` را پیش از گروه‌بندی اعمال می‌کند؛ بنابراین در همین query نسخه‌های منتشرشده بعد از cutoff وارد نمی‌شوند. این نکته مثبت است، اما ترتیب انتخاب نسخه با قرارداد چهارسطحی DB-DES-001 منطبق نیست.
2. **اولویت نسخه:** `_latest_per_metric()` برای هر Metric و Period صرفاً بیشترین `publication_datetime` را انتخاب می‌کند. `ReportVersion` دارای `is_restated` است، اما مدل مشاهده‌شده فیلد وضعیت حسابرسی ندارد؛ query نیز هیچ رتبه‌بندی AUDITED/UNAUDITED و RESTATED/ORIGINAL انجام نمی‌دهد. در نتیجه «جدیدترین انتشار» ممکن است بر نسخه‌ای با اولویت قراردادی پایین‌تر غلبه کند. این مغایرت در انتخاب نسخهٔ Forecast مشاهده شد؛ رفتار نهایی باید با چهار سطح مصوب و قواعد tie-break همسو شود.
3. **ترتیب Period:** `load_financial_fact_periods()` دوره‌ها را با `sorted(period_id)` مرتب می‌کند و `load_financial_facts()` آخرین عضو فهرست را به‌عنوان آخرین دوره برمی‌دارد. قرارداد DB-DES-003 ترتیب واقعی زمانی/تقویم مالی شرکت را می‌خواهد؛ شناسهٔ افزایشی به‌تنهایی شاهد ترتیب زمانی نیست. باید ترتیب بر اساس تاریخ پایان واقعی و قواعد دورهٔ شرکت باشد و ابهام/تعارض دوره‌ها fail-closed شود.
4. **انتخاب عمومی ReportVersion:** `src/core/point_in_time.py::select_report_version()` نسخه‌ها را فقط با `publication_datetime DESC` و سپس `version_number DESC` مرتب می‌کند؛ چهار سطح اولویت مصوب را اعمال نمی‌کند. این helper در فایل‌های بررسی‌شده call-site downstream مشخصی نداشت؛ وجود helper به‌تنهایی اثبات استفاده در همهٔ مسیرها نیست.
5. **دامنهٔ Fact:** query Forecast از `NormalizedFinancialFact.company_id` و `ReportVersion` استفاده می‌کند، اما در این query سازگاری company گزارش/نسخه با company fact و period با شرکت/گزارش به‌صورت join condition یا assertion مستقل بررسی نمی‌شود. این invariant باید در schema/service/query enforce شود؛ این مرور فقط نبود کنترل صریح در همین مسیر را ثبت می‌کند.

### 11.2 Share/CorporateAction و PIT

- `load_share_history()` cutoff را با `normalize_datetime(cutoff).date()` به تاریخ Gregorian تبدیل می‌کند و آن را با `effective_date` در مدل‌های Share/Action مقایسه می‌کند؛ این با قرارداد Jalali-native DB-DES-003/004 سازگار نیست، مگر آنکه قرارداد مستقل و معتبر برای همین ستون‌ها اثبات شود.
- مدل‌های `ShareCountHistory` و `CorporateAction` که خوانده شدند، `effective_date` دارند اما timestamp انتشار/اعلان قابل اتکای PIT و revision metadata ندارند. در CorporateAction، `announcement_date` از نوع Date و nullable است، نه publication timestamp.
- شرط `coalesce(CorporateAction.announcement_date, cutoff_date) <= cutoff_date` مقدار announcement_date تهی را به cutoff جاری تبدیل می‌کند؛ در نتیجه ردیفی با زمان اعلان نامعلوم از فیلتر زمانی عبور می‌کند. این دقیقاً fail-closed نیست و می‌تواند اطلاعاتی را که زمان در دسترس‌شدنش معلوم نیست در محاسبه وارد کند.
- Share history نیز فقط بر اساس effective_date فیلتر می‌شود؛ تاریخ اثر اقتصادی، زمان انتشار/قابل‌دسترس‌شدن اطلاعات را اثبات نمی‌کند. بدون publication/availability metadata، PIT تاریخی قابل تضمین نیست.

### 11.3 Market، Valuation و Decision

- `ingestion/market/queries.py` قیمت و تاریخچه را با اجزای Jalali و شرط on-or-before انتخاب می‌کند؛ duplicate Jalali date را صریحاً رد می‌کند و adjusted close را در صورت وجود بر close ترجیح می‌دهد. این read-side با تقویم Jalali سازگار است.
- بااین‌حال، `MarketDaily` در مدل بررسی‌شده timestamp انتشار/قابل‌دسترس‌شدن منبع یا revision ندارد. انتخاب Market بر اساس تاریخ معامله/مشاهدهٔ Jalali است، نه زمان انتشار داده؛ بنابراین انتخاب تاریخیِ «آنچه در cutoff واقعاً در دسترس بوده» هنوز قابل اثبات نیست. این محدودیت جدا از شرط trade-date <= as-of است.
- `valuation/service.py` از `select_market_price_as_of()` استفاده می‌کند و Jalali as-of/source date و price basis را در metadata خروجی نگه می‌دارد؛ ولی helper بازار، مطابق قرارداد موجود، آخرین قیمت dated on-or-before را برمی‌گزیند و publication-time PIT ندارد.
- `decision/service.py` تطابق company و period بین Forecast و FundamentalScore و تطابق company در MarketResult را بررسی می‌کند؛ اما timestamp/cutoff و as-of Jalali مشترک میان MarketResult، Forecast، Score و Valuation را در این boundary تطبیق نمی‌دهد. این orchestration boundary به‌تنهایی تضمین نمی‌کند ورودی‌هایش از یک PIT snapshot مشترک آمده باشند.

### 11.4 ماژول‌های محاسباتی pure/in-memory

- `trend/engine.py` تصریح می‌کند که caller باید سری دادهٔ PIT-filtered را تحویل دهد؛ engine خود query یا فیلتر انتشار انجام نمی‌دهد.
- `scoring/engine.py` و `market/engine.py` موتورهای محاسباتی‌اند و persistence ندارند. `market/service.py` تاریخچه را از query Jalali می‌گیرد و آن را به engine می‌دهد.
- `evaluation/pipeline.py` داده‌های Forecast/Actual را از ورودی‌های از پیش آماده‌شده دریافت می‌کند و منطق selection/validation داخلی Stage 6 خودش را دارد؛ این مسیر جایگزین ReportVersion selector مالی DB-DES-001 نیست و نباید قواعد outcome publication آن با PIT ورودی‌های Forecast یکی فرض شود.
- در فایل‌های مصرف‌کنندهٔ بررسی‌شده write/commit دیتابیسی مشاهده نشد؛ این نتیجه محدود به همین فایل‌هاست، نه تمام 128 فایل Python.

### 11.5 جمع‌بندی مغایرت‌ها و اقدام بعدی

| موضوع | شاهد مستقیم | اثر/ریسک | اقدام لازم |
|---|---|---|---|
| رتبه‌بندی نسخهٔ مالی | `_latest_per_metric()` و `select_report_version()` فقط جدیدترین publication را می‌گیرند | عدم رعایت چهار سطح AUDITED/RESTATED | تعریف یک selector مشترک، fail-closed برای status نامعلوم و tie-break مصوب |
| وضعیت حسابرسی | `ReportVersion` فیلد `is_restated` دارد اما audit status مشاهده نشد | اجرای اولویت چهارگانه با مدل فعلی کامل نیست | تعیین منبع/فیلد وضعیت حسابرسی در مدل هدف؛ بدون حدس از نبود فیلد |
| آخرین Period | مرتب‌سازی `period_id` | انتخاب اشتباه آخرین دوره در صورت عدم تطابق ID و chronology | مرتب‌سازی بر تاریخ/تقویم واقعی و enforce هویت دوره |
| PIT سهام/اقدام شرکتی | Gregorian cutoff در برابر Dateهای مدل؛ announcement تهی با coalesce پذیرفته می‌شود | look-ahead یا تقویم ناسازگار | Jalali-native effective dates و publication/availability timestamp اجباری؛ missing = ineligible |
| PIT بازار | MarketDaily فاقد publication timestamp در مدل بررسی‌شده | تاریخ معامله، زمان دسترسی تاریخی را ثابت نمی‌کند | ثبت source availability/publication metadata یا محدودکردن صریح ادعای PIT |
| هم‌ترازی Stage 9 | کنترل identity دارد، نه cutoff/as-of مشترک | ترکیب خروجی‌های متعلق به زمان‌های متفاوت | قرارداد snapshot/cutoff مشترک در boundary |
| Trend/Scoring engines | caller-owned PIT filtering | امکان ورودی ناسازگار در caller | audit call-siteهای باقی‌مانده و تست مرزی در implementation |

**محدودیت دامنه:** این بخش مرور هدفمند 9 فایل downstream و مدل‌های مرتبط است؛ نه inventory کامل تمام queryها، call-siteها یا تمام 128 فایل Python. فایل‌های XLSX/CSV منبع و دیتابیس عملیاتی بررسی نشده‌اند. در نتیجه دربارهٔ داده‌های واقعی، وضعیت تاریخی نسخه‌ها یا صحت مقادیر منبع ادعایی نمی‌شود.

**وضعیت DB-AUD-001:** PARTIAL. این مرحله مصرف‌کنندگان اصلی Forecast/Market/Valuation/Decision و helper PIT را در سطح فایل‌های مشخص بررسی کرد و چند مغایرت مهم با DB-DES-001/003/004 ثبت شد. هنوز inventory کامل همهٔ readerها و writerها، تطبیق schema واقعی DB، و بررسی تمام call-siteهای Session باقی است. هیچ کد، ORM، schema، migration یا داده‌ای تغییر نکرد و هیچ تستی اجرا نشد.



## 12. مرور تکمیلی Stage 2 KPI، Stage 5 Share PIT و مرزهای runtime — 2026-11-15

### 12.1 Forecast و دادهٔ سهام: مغایرت PIT تأییدشده در query، builder و تست

فایل‌های `src/forecast/queries.py`، `src/forecast/builder.py`، `src/forecast/service.py` و بخش‌های مرتبط `src/tests/test_stage5_forecast.py` بررسی شدند.

1. `load_share_history()` تاریخ cutoff را با `normalize_datetime(cutoff).date()` به Gregorian تبدیل می‌کند و برای `ShareCountHistory` فقط `effective_date <= cutoff_date` را اعمال می‌کند. هیچ publication/availability timestamp برای ShareCountHistory در این مدل/فیلتر دیده نشد؛ تاریخ اثر، زمان آگاهی از داده را ثابت نمی‌کند.
2. برای CorporateAction، query از `coalesce(announcement_date, cutoff_date) <= cutoff_date` استفاده می‌کند؛ مقدار اعلان تهی عملاً با خود cutoff جایگزین و واجد شرایط می‌شود.
3. `build_weighted_average_shares()` نیز فقط وقتی اقدام را رد می‌کند که `announcement_date` یک `date` باشد و بعد از cutoff قرار گیرد. مقدار None رد نمی‌شود.
4. نکتهٔ مهم‌تر: تست `test_null_announcement_action_is_treated_as_knowable_in_production_path` این رفتار را صریحاً تأیید می‌کند و انتظار دارد اقدام شرکتی بدون announcement date در EPS اعمال شود. این تست صرفاً پوشش ناکافی نیست؛ رفتار مغایر با اصل PIT fail-closed را به‌عنوان رفتار مطلوب تثبیت کرده است.
5. این رفتار با قرارداد مصوب DB-DES-001/003 و قاعدهٔ DB-DES-004 که زمان انتشار/قابل‌دسترس‌شدن نامعلوم را برای PIT تاریخی غیرواجدشرایط می‌داند، ناسازگار است. تا زمانی که مالک قاعدهٔ معتبر دیگری تصویب نکند، missing announcement/publication باید از PIT تاریخی حذف شود؛ نباید تاریخ cutoff به‌عنوان زمان انتشار فرض شود.
6. `build_weighted_average_shares()` تاریخ‌های `date` را به‌صورت عمومی می‌پذیرد و معنای تقویم را در type/argument مشخص نمی‌کند. اتصال آن به مدل‌های Share/Action فعلی که Gregorian Date دارند با قرارداد Jalali-native هدف نیازمند تعیین تکلیف صریح است.

### 12.2 Stage 2 KPI و محاسبات دوره‌ای

- `src/kpi/engine.py`، `industry.py` و `schema.py` در مسیر بررسی‌شده موتورهای pure هستند: دادهٔ مالی و `period_id` را از caller می‌گیرند؛ Session یا query ندارند و persistence مشاهده نشد. بنابراین اعتبار زمانی/نسخه‌ای دادهٔ ورودی مسئولیت caller است و از خود KPI engine تضمین نمی‌شود.
- `KPIResult` فقط `company_id`، `period_id`، کد، مقدار، واحد، quality و calculation timestamp دارد؛ cutoff، report_version provenance، دورهٔ دقیق یا temporal basis در خود نتیجه دیده نشد.
- `src/kpi/period_utils.py::calculate_ttm()` صرفاً چهار مقدار آخر فهرست را جمع می‌کند و نوع دوره، پیوستگی فصل‌ها، YTD در برابر standalone، تاریخ پایان، یا duplicate/missing quarter را کنترل نمی‌کند. این تابع با قرارداد TTM runtime-only تناقضی از نظر persistence ندارد، اما ورودی‌های آن باید از caller به‌صورت چهار جریان فصلی مستقل و معتبر آماده شوند؛ استفادهٔ مستقیم از چهار YTD یا چهار مقدار غیرمتوالی نتیجهٔ نادرست می‌دهد.
- در فایل‌های KPI بررسی‌شده، اتصال مستقیم به FinancialFact/ReportVersion یا selector PIT یافت نشد. این امر به معنی نبود چنین اتصال در کل repository نیست؛ تنها مسیرهای خوانده‌شده pure و caller-fed هستند.
- زمان محاسبهٔ KPI در `industry.py` با UTC تولید و timezone آن حذف می‌شود. این timestamp محاسبه است، نه publication/availability time داده و نباید جای cutoff یا provenance منبع استفاده شود.

### 12.3 مرز سرویس و persistence خروجی‌ها

- `forecast/service.py` صریحاً Session را از caller می‌گیرد و commit نمی‌کند؛ queryها خواندنی‌اند و ForecastResult در runtime برگردانده می‌شود.
- `valuation/service.py` قیمت را از MarketDaily می‌خواند، نتیجهٔ Valuation را در حافظه می‌سازد و provenance قیمت را در metadata خروجی می‌گذارد؛ write/commit مشاهده نشد.
- `market/service.py` تاریخچهٔ Jalali را به MarketEngine می‌دهد و persistence ندارد.
- `decision/service.py` Forecast، FundamentalScore و MarketSignal را orchestrate می‌کند؛ identity شرکت/دوره را برای برخی ورودی‌ها کنترل می‌کند، اما هیچ cutoff یا availability timestamp مشترک را در خود اشیای ورودی تطبیق نمی‌دهد.
- `models/forecast.py` هنوز مدل‌های جداگانهٔ LegacyForecast را در `LegacyForecastBase` تعریف می‌کند، درحالی‌که migrationهای بررسی‌شده جدول‌های forecast legacy را در نسخهٔ 8 حذف می‌کنند. در مسیرهای سرویس Stage 5 که اینجا بررسی شدند، استفاده از این مدل legacy مشاهده نشد؛ inventory import/reference کل repository برای تعیین اینکه آیا کد مرده یا وابستگی پنهان باقی مانده، هنوز کامل نیست.

### 12.4 شواهد تست و اقدام‌های ضروری

| موضوع | شاهد | نتیجهٔ ممیزی | اقدام لازم |
|---|---|---|---|
| Announcement تهی | query coalesce + builder شرطی + تست `test_null_announcement_action_is_treated_as_knowable_in_production_path` | رفتار صریحاً PIT را با فرض دسترس‌پذیری نامعلوم نقض می‌کند | تغییر سیاست به fail-closed؛ بازنگری تست و مدل metadata |
| PIT ShareCountHistory | فقط effective_date فیلتر می‌شود | دادهٔ backdated می‌تواند look-ahead ایجاد کند | publication/availability timestamp اجباری و فیلتر پیش از انتخاب |
| تقویم Share/Action | Gregorian Date و `date()` cutoff | با Jalali-native هدف ناهم‌راستا | تعیین مدل تاریخ canonical و migration strategy؛ بدون تبدیل ضمنی |
| TTM | جمع چهار عدد آخر بدون temporal metadata | خطر جمع YTD، فصل نامتوالی یا دوره‌های نامتجانس | ورودی چهارتایی با quarter identity/standalone basis معتبر یا helper سخت‌گیرتر |
| KPI provenance | خروجی فقط period_id و calculation timestamp دارد | قابلیت بازسازی PIT از KPIResult به‌تنهایی کافی نیست | انتقال provenance/cutoff در runtime result یا قرارداد صریح caller |
| Legacy Forecast ORM | `LegacyForecastBase` در برابر migration حذف جدول | احتمال مدل بلااستفاده یا reference باقی‌مانده | inventory تمام importها و references پیش از حذف/تغییر |

**محدودیت دامنه:** این مرحله فقط فایل‌های مشخص‌شده و تست مرتبط Stage 5 را مرور کرد؛ تستی اجرا نشد. هیچ XLSX/CSV منبع، دیتابیس عملیاتی، یا تمام import/referenceهای repository بررسی نشده است. بنابراین دربارهٔ داده‌های واقعی یا نبود قطعی استفاده از LegacyForecast در کل برنامه ادعایی نمی‌شود.

**وضعیت DB-AUD-001:** PARTIAL. این مرحله مغایرت PIT در اقدام شرکتی بدون تاریخ اعلان را با شاهد query، builder و تست مشخص کرد و محدودیت‌های دوره‌ای KPI/TTM را ثبت کرد. inventory کامل read/write و importها، schema واقعی DB، و مسیر migration ایمن همچنان باز است. هیچ کد، ORM، schema، migration یا داده‌ای تغییر نکرد و هیچ تستی اجرا نشد.


## 13. ردیابی مدل‌های نرمال‌شده، مسیر CODAL و مدل‌های Legacy Forecast — 2026-11-15

### 13.1 مسیر واقعی CODAL در برابر مصرف‌کنندهٔ Stage 5

فایل‌های `src/ingestion/service.py`، `src/forecast/queries.py`، `src/models/normalized.py` و تست معماری Stage 1 بررسی شدند.

1. مسیر خواندن Stage 5 در `forecast/queries.py` مستقیماً از `NormalizedFinancialFact` به‌همراه `FinancialMetric`، `FinancialPeriod` و `ReportVersion` می‌خواند؛ فیلتر `publication_datetime <= cutoff` پیش از انتخاب اعمال می‌شود. این مسیر به `RawFinancialFact` متصل نیست.
2. مسیر CODAL در `ingestion/service.py::ingest_codal_report` (تابع persistence گزارش CODAL) یک `ReportVersion` و مجموعه‌ای از `RawFinancialFact` ایجاد می‌کند. در همین تابع، ایجاد `MappingDecision`، ساخت `NormalizedFinancialFact` یا ایجاد bridgeهای `NormalizedFinancialFactInput` مشاهده نشد.
3. بنابراین در مسیر بررسی‌شده، خروجی ingestion مستقیماً به ورودی Stage 5 تبدیل نمی‌شود. تست `test_stage1_database_architecture.py` ساخت دستی Raw facts، MappingDecision و Normalized fact را برای آزمون مدل نشان می‌دهد؛ این تست مسیر production end-to-end را اثبات نمی‌کند.
4. تابع CODAL برای tracking ID و publication datetime یکسان، وجود ReportVersion را بررسی می‌کند و سپس شمارش RawFinancialFactهای آن را در `records_updated` می‌گذارد و COMPLETED برمی‌گرداند؛ مقایسهٔ payload ورودی با payload ذخیره‌شده در این شاخه دیده نشد. این رفتار با DB-DES-001/005 که identical replay را unchanged/no-op و payload متعارض را reject می‌کند، هم‌راستا نیست.
5. همین تابع پس از exception، transaction را rollback و یک IngestionRun جدید FAILED می‌سازد؛ بنابراین STARTED audit اولیه حفظ نمی‌شود. این مورد با یافته‌های بخش 9 دربارهٔ lifecycle ناسازگار Run سازگار است.

### 13.2 تعارض مدل‌های ORM با قرارداد منطقی

- `RawFinancialFact` ستون‌های raw label، unit، currency و حتی source_row/source_column را در مدل دائمی نگه می‌دارد. قرارداد منطقی فعلی DB-DES-001/002 می‌گوید raw Excel rows و locatorهای دقیق جزو canonical persistence نیستند. باید روشن شود این جدول legacy/موقت است یا هنوز بخشی از طرح فعال؛ این ممیزی به‌تنهایی حذف فیزیکی آن را تجویز نمی‌کند.
- `NormalizedFinancialFact` مقدار را در `Numeric(30,4)` با نام `value_irr` ذخیره می‌کند، درحالی‌که قرارداد جدید canonical input بر SQLite INTEGER، حفظ unit/basis منبع و هویت کلید شامل ReportVersion + period + metric + approved dimensions تأکید دارد. مدل فعلی unique key شامل company/period/metric/source version است و هیچ approved dimension identity در آن دیده نشد؛ precision و naming نیز با قرارداد جدید هم‌راستا نیست.
- `DerivedFinancialFact` و `DerivedFinancialFactInput` جداول persistence برای خروجی محاسبه و lineage مشتق دارند؛ این با تصمیم runtime-only بودن محاسبات/خروجی‌ها تعارض دارد. پیش از migration باید مصرف‌کنندگان و دادهٔ موجود مشخص شوند؛ این گزارش وضعیت DB واقعی را بررسی نکرده است.
- `MappingRule` و `MappingDecision` نسخه و وضعیت review دارند، اما مدل نشان‌داده‌شده به‌تنهایی تضمین نمی‌کند هر Fact به نسخهٔ دقیق IndustryStandard/ExtractionStandard متصل باشد. `normalization_rule_id` نیز Integer nullable بدون FK قابل مشاهده است.
- `ReportVersion` publication datetime و is_restated دارد، اما audit status موردنیاز اولویت چهارگانه در مدل بررسی‌شده وجود ندارد؛ بخش 11 این محدودیت انتخاب PIT را نیز ثبت کرده است.
- `FinancialPeriod` از Gregorian SQL Date و انواع MONTH/QUARTER/SEMI_ANNUAL/NINE_MONTH/ANNUAL/TTM استفاده می‌کند؛ با DB-DES-003 که Jalali-native، INSTANT/DURATION و TTM runtime-only را می‌خواهد، نیازمند بازطراحی/مهاجرت است. این مشاهده مدل ORM است، نه بررسی مقادیر واقعی DB.

### 13.3 مدل‌های Forecast قدیمی

- `src/models/forecast.py`، `ForecastVersion` و `ForecastInputRefModel` را در `LegacyForecastBase` مجزا تعریف می‌کند و docstring می‌گوید این metadata برای اجرای migration تاریخی 7 است؛ migration 8 جداول forecast را حذف می‌کند.
- در مسیرهای Stage 5 service بررسی‌شده، import یا query این ORMها مشاهده نشد. اما inventory کامل تمام importها/references در کل repository در این مرحله انجام نشده؛ بنابراین حکم حذف قطعی یا dead code صادر نمی‌شود.

### 13.4 ماتریس شکاف و اقدام لازم

| شکاف | شاهد مستقیم | پیامد | اقدام بعدی |
|---|---|---|---|
| CODAL فقط Raw می‌نویسد | `ingest_codal_report` و Stage 5 query | Stage 5 مصرف‌کنندهٔ مستقیم خروجی CODAL نیست | طراحی/پیاده‌سازی pipeline استخراج، mapping و canonical validation مطابق DB-DES-001/002 |
| replay CODAL به‌عنوان update | شاخهٔ existing ReportVersion | مغایر idempotency و conflict policy | fingerprint/payload identity و source revision؛ duplicate unchanged، conflict reject |
| raw rows دائمی | RawFinancialFact ORM و writer | تعارض با حداقل canonical persistence | تعیین نقش legacy/staging و طرح گذار؛ بدون حذف شتاب‌زده |
| normalized fact schema | Numeric value_irr و unique key فاقد dimensions | عدم انطباق با INTEGER، unit/basis و uniqueness contract | طراحی physical schema/migration پس از تکمیل استانداردها |
| derived facts persisted | DerivedFinancialFact tables | تعارض با runtime-only outputs | inventory مصرف‌کننده و migration/deprecation plan |
| FinancialPeriod و ReportVersion | Gregorian dates، TTM type، نبود audit status | عدم انطباق زمانی و version ranking | physical design منطبق با DB-DES-001/003 |
| LegacyForecast ORM | isolated metadata و migration 7/8 | احتمال import/reference باقی‌مانده | inventory کامل import/reference قبل از پاک‌سازی |

**محدودیت دامنه:** این مرحله مسیر CODAL، Stage 5 query، مدل‌های ORM منتخب و یک تست معماری را بررسی کرد. تمام import/referenceهای repository، migrationهای اجرایی روی DB واقعی، محتوای دیتابیس عملیاتی و فایل‌های XLSX/CSV بررسی نشده‌اند. هیچ نتیجه‌ای دربارهٔ نبود قطعی استفاده از LegacyForecast یا وضعیت داده‌های موجود اعلام نمی‌شود.

**وضعیت DB-AUD-001:** PARTIAL. یک شکاف اتصال مهم بین CODAL raw persistence و Stage 5 normalized reader، به‌علاوهٔ تعارض‌های مدل ORM با قراردادهای جدید ثبت شد. inventory کامل read/write/importها، تطبیق schema واقعی، و طرح migration هنوز باز است. هیچ کد، ORM، schema، migration یا داده‌ای تغییر نکرد و هیچ تستی اجرا نشد.



## 14. Inventory سراسری referenceهای مدل‌های FinancialFact و LegacyForecast — 2026-11-15

### 14.1 دامنه و روش

- Tree شاخهٔ master شامل 128 فایل Python زیر src/ و دو فایل Python در ریشهٔ repository بود؛ هر 130 فایل برای symbolهای RawFinancialFact، NormalizedFinancialFact، DerivedFinancialFact، DerivedFinancialFactInput، NormalizedFinancialFactInput، FinancialMetric، MappingRule، MappingDecision، LegacyForecastBase، ForecastVersion و ForecastInputRefModel اسکن شد.
- این inventory جست‌وجوی literal symbolها در Python است؛ reflection، import پویا، aliasهای ناشناخته، کد خارج از Python، runtime database و migrationهای اجراشده روی DB واقعی را پوشش نمی‌دهد. «مصرف‌کننده‌ای یافت نشد» فقط به همین دامنهٔ اسکن اشاره دارد.

### 14.2 ماتریس reference و مصرف

| مدل/خانواده | تعریف/ثبت schema | مصرف production مشاهده‌شده | تست‌ها/مصرف غیرproduction | نتیجه |
|---|---|---|---|---|
| RawFinancialFact | تعریف در models/normalized.py؛ import در migration runner و init_db.py | writer و lookup شمارشی در ingestion/service.py؛ reader تحلیلی دیگری در اسکن پیدا نشد | CODAL extraction/PDF extraction، Stage 1 architecture/rules، Stage 5 fixtures؛ docstring در CODAL ingestion/pipeline | جدول raw هنوز مسیر فعال CODAL است؛ Stage 5 آن را نمی‌خواند |
| NormalizedFinancialFact | تعریف در models/normalized.py؛ import در migration runner و init_db.py | reader اصلی در forecast/queries.py | Stage 1 architecture/rules و Stage 5 tests آن را به‌عنوان fixture می‌سازند؛ integrity test import/schema را بررسی می‌کند | مصرف production خواندنی پیدا شد؛ writer production در اسکن پیدا نشد |
| DerivedFinancialFact و DerivedFinancialFactInput | تعریف در models/normalized.py؛ import برای metadata در migration runner و init_db.py | writer یا reader production در اسکن پیدا نشد | import در Stage 1 architecture/integrity/rules؛ assertion عملیاتی مصرف در این فایل‌ها محدود است | مدل/schema ثبت‌شده بدون مسیر مصرف production مشاهده‌شده |
| NormalizedFinancialFactInput | تعریف در models/normalized_provenance.py؛ import در migration runner و init_db.py | writer/reader production در اسکن پیدا نشد | Stage 1 architecture test دو provenance link می‌سازد و query می‌کند | مدل provenance فعلاً در مسیر تست/metadata دیده شد، نه pipeline ingestion |
| FinancialMetric | تعریف در models/normalized.py؛ ثبت در migration و init | seed در scripts/seed_data.py؛ reader در forecast/queries.py | Stage 1 و Stage 5 tests fixture می‌سازند | مصرف production دوطرفهٔ روشن (seed/read) دارد |
| MappingRule و MappingDecision | تعریف در models/normalized.py؛ import در migration و init | writer/reader production در اسکن پیدا نشد | Stage 1 architecture/rules tests رکورد نمونه می‌سازند | زیرساخت mapping در ORM وجود دارد، اما به CODAL production path متصل نیست |
| LegacyForecastBase، ForecastVersion، ForecastInputRefModel | تعریف در models/forecast.py؛ migration runner آن‌ها را import می‌کند | migration 7 دو جدول را ایجاد می‌کند؛ migration 8 هر دو جدول را drop می‌کند؛ مصرف runtime در service/query پیدا نشد | Stage 1 database integrity test، metadata را create_all می‌کند | مدل‌ها برای migration تاریخی نگه داشته شده‌اند؛ تست می‌تواند جداول legacy را دوباره در DB تستی بسازد |

### 14.3 یافته‌های تکمیلی از migration و initialization

1. src/migrations/runner.py مدل‌های Raw/Normalized/Derived، metric/mapping و provenance را import می‌کند تا metadata برای migrationها در دسترس باشد؛ این import به‌تنهایی اثبات نمی‌کند برای هر مدل جدول فعال یا مسیر production وجود دارد.
2. src/scripts/init_db.py همین مدل‌ها را import می‌کند و سپس Base.metadata.create_all را اجرا می‌کند. جدول‌هایی که هنوز در Base فعال تعریف شده‌اند می‌توانند در initialization تازه ایجاد شوند؛ این مسیر باید با migrationهای versioned جداگانه بررسی شود.
3. Migration 7 جدول‌های forecast_versions و forecast_input_refs را از LegacyForecastBase ایجاد می‌کند؛ migration 8 هر دو را حذف می‌کند. بااین‌حال test_stage1_database_integrity.py از LegacyForecastBase.metadata.create_all استفاده می‌کند و در محیط تست می‌تواند schema قدیمی را مجدداً بسازد. این رفتار با فعال بودن runtime legacy در production یکی نیست.
4. دو فایل Python ریشهٔ repository (debug_alerts.py و normalize_persian_test.py) هیچ‌یک از symbolهای اسکن‌شده را ارجاع نمی‌دهند.

### 14.4 نقشهٔ وابستگی و ترتیب امن اقدام

- مسیر ورودی: CODAL ingestion → RawFinancialFact (فعلی) → هنوز mapping/normalization production bridge شناسایی نشده است.
- مسیر مصرف: NormalizedFinancialFact → forecast/queries.py → Forecast Stage 5.
- گسست اصلی: writer فعلی و reader فعلی روی دو مدل متفاوت قرار دارند؛ تست‌های Stage 5 با ساخت مستقیم Normalized facts این گسست را پنهان می‌کنند و اثبات end-to-end محسوب نمی‌شوند.
- MappingRule/Decision، NormalizedFinancialFactInput و DerivedFinancialFact/Input در ORM و metadata وجود دارند اما writer/reader production در اسکن symbolهای Python پیدا نشد.
- Legacy Forecast فقط از طریق migration و تست integrity ظاهر شد؛ پیش از حذف کلاس‌ها باید importهای خارج از literal scan، مسیرهای migration و اثر تست‌ها بازبینی شود. همچنین create_all تست نباید ناخواسته schema حذف‌شده را احیا کند.

ترتیب منطقی بعدی:
1. تثبیت قرارداد pipeline واقعی CODAL از source adapter تا mapping/versioned standard و canonical fact؛ بدون افزودن writer جدید تا مشخص شدن قرارداد فیزیکی DB-DES-001/002.
2. تعیین تکلیف RawFinancialFact: staging موقت، operational audit محدود، یا حذف از persistence؛ این تصمیم باید با ممنوعیت ذخیرهٔ raw rows در DB-DES-001 سازگار باشد.
3. طراحی writer canonical برای NormalizedFinancialFact و provenance، با INTEGER، approved dimensions، exact standard version، atomicity و idempotency DB-DES-005.
4. تصمیم رسمی دربارهٔ deprecation یا حذف DerivedFinancialFact/Input و NormalizedFinancialFactInputهای بدون consumer، پس از بررسی data migration واقعی.
5. جداکردن LegacyForecast ORM از initialization/test metadata و اطمینان از عدم بازسازی جدول‌های حذف‌شده.

**محدودیت:** این inventory کامل literal references در 130 فایل Python است، نه اثبات نبود مصرف پویا یا خارج از Python. XLSX/CSV، دیتابیس عملیاتی و اجرای تست‌ها بررسی/اجرا نشدند. هیچ کد، ORM، schema، migration یا داده‌ای تغییر نکرد.

**وضعیت DB-AUD-001:** PARTIAL. inventory literal references تکمیل شد و شکاف مسیر CODAL→Raw در برابر Stage 5→Normalized به نقشهٔ وابستگی تبدیل شد. بررسی alias/dynamic imports، schema واقعی DB، و migration plan همچنان باز است.


## 9. Reconciliation of available sample files — 2026-11-19

A recursive inventory of the tracked `master` repository tree found no tracked `.csv`, `.xlsx`, or `.xls` source files. A Library search for actual MarketDaily CSV, both FX-rate samples, ShareCountHistory and CorporateAction source files returned no relevant source sample; returned items were unrelated project notes/reports. This does not prove that no local files exist on the owner's computer, but it confirms that the current repository evidence cannot establish real Feed headers, units, scales, date/number formats, or revision metadata.

Therefore the following evidence requests remain exact and unchanged:
- one authentic MarketDaily CSV with source identity and representative rows;
- one authentic daily FX sample for FREE_MARKET and one for EXCHANGE_CENTER (or one source file containing both with an explicit discriminator);
- an owner decision whether ShareCountHistory and CorporateAction are V1 file imports, manually entered records, or deferred.

No parser, code, ORM, schema, migration, database, or test was changed/run. This section closes only the repository/library sample-availability check; it does not close DB-STD-005.


## 10. ممیزی نمونه‌های محلی CSV بازار و XLSX نرخ ارز — 2026-11-19

### 10.1 منشأ و تمامیت فایل‌ها

مالک گزارش ممیزی مستقیم دو فایل محلی را از مسیر `D:\\winprojects\\analyzer` ارائه کرد. فایل‌ها در repository ثبت نشده‌اند؛ بنابراین شواهد این بخش بر اساس گزارش محلی مالک/Agent است و محتوای باینری فایل‌ها در این نوبت مستقلاً توسط دستیار بازگشایی نشده است.

| دامنه | فایل | اندازه | SHA-256 | رکورد |
|---|---|---:|---|---:|
| MarketDaily candidate | `saman_price_history.csv` | 2,400 bytes | `d94f27405f257b4010e1d2b7db4a554311484a6dde2b35a9c81c548f381c1413` | 21 |
| FX candidate | `dollar-history.xlsx` | 14,349 bytes | `eb85250100438335accb06ca1fdf364304887a71e361258b93836d3a90dd6fcf` | 19 |

### 10.2 MarketDaily — آنچه از فایل اثبات شده است

- CSV دارای UTF-8 BOM، delimiter کاما، CRLF، یک header دوازده‌ستونی و ۲۱ ردیف داده است؛ دو ردیف خالی انتهایی داده محسوب نمی‌شوند.
- Headerها عیناً: `J-Date, Open, High, Low, Close, Final, Volume, Value, No, Ticker, Name, Market`.
- تاریخ‌ها در قالب متنی `YYYY-MM-DD`، صعودی و بدون تکرار/مقدار نامعتبر گزارش شده‌اند؛ عنوان `J-Date` شاهد مستقیم تقویم جلالی است. بازهٔ مشاهده‌شده 1402-01-08 تا 1402-02-12 است.
- ۲۱ ردیف برای همهٔ ۱۲ ستون مقدار دارند. اعداد صحیح متنی ASCII و بدون اعشار/جداکننده‌اند.
- کنترل‌های گزارش‌شدهٔ OHLC معتبرند: High کمتر از Low و Open/Close/Final خارج از بازهٔ Low..High مشاهده نشد.
- `Close` و `Final` در ۱۶ ردیف متفاوت و در ۵ ردیف برابرند. این تفاوت، معنای خام/تعدیل‌شده یا هر معنای canonical دیگر را به‌تنهایی اثبات نمی‌کند.
- `Volume`، `Value` و `No` موجودند، اما واحد/مقیاس و معنای دقیق آن‌ها مشخص نیست. مقادیر پرت آماری گزارش‌شده در 1402-01-15 صرفاً هشدار بررسی‌اند و خطای داده را اثبات نمی‌کنند.
- `Ticker=سامان` و `Name=بانک سامان` شواهد متنی هویت‌اند، اما جایگزین resolve شدن به `company_id` و تأیید صنعت نیستند. `Market=پایه زرد` هنوز به catalog بازار canonical نگاشت نشده است.
- منبع/ناشر Feed، روش استخراج، نسخه/اصلاحیه، زمان انتشار/دسترس‌پذیری، واحد و scale قیمت‌ها، و سیاست duplicate/conflict در فایل اثبات نشده‌اند.

**نتیجهٔ mapping:** وجود ستون‌های `Open/High/Low/Close/Final/Volume/Value` با خانوادهٔ MarketDaily هم‌خوانی ساختاری دارد؛ بااین‌حال `Close` را نمی‌توان بدون تأیید به raw close و `Final` را به adjusted close نگاشت کرد. تا تأیید معنای فیلدها و واحدها، Feed profile قابل فعال‌سازی نیست. هیچ تبدیل واحد یا fallback انجام نشود.

### 10.3 FX — آنچه از فایل اثبات شده است

- Workbook یک Worksheet قابل مشاهده با نام `Sheet` دارد؛ دادهٔ واقعی در `Sheet!A4:C22` و شامل ۱۹ ردیف است. عنوان در A1 «دلار امريکا» و Headerها در ردیف ۳ «تاریخ»، «خرید (ریال)»، «فروش (ریال)» هستند.
- تاریخ‌ها متن `YYYY-MM-DD`، نزولی و بدون تکرار گزارش شده‌اند؛ بازهٔ فایل 1405-08-28 تا 1405-08-10 است. با وجود ظاهر تاریخ، گزارش تقویم را UNKNOWN اعلام کرده؛ صرف عدد سال برای تصویب parser کافی نیست.
- هر ۱۹ ردیف برای هر سه ستون مقدار دارد. خرید و فروش اعداد صحیح متنی‌اند؛ Header واحد «ریال» را صریحاً درج می‌کند.
- فایل یک سری خرید/فروش دارد؛ هیچ ستون یا نشانهٔ صریحی برای تفکیک `FREE_MARKET` و `EXCHANGE_CENTER`، نام منبع، زمان انتشار، revision یا نوع مرجع نرخ گزارش نشده است.
- دو ستون خرید/فروش با قرارداد دامنه‌ای فعلی FXRate که یک مقدار روزانه برای هر `rate_type` و بدون تفکیک buy/sell تعریف کرده، مستقیماً قابل انطباق نیستند.
- Header واحد ریال دارد، درحالی‌که قرارداد منطقی فعلی منبع FX را Toman/USD و canonical را Rial/USD تعریف کرده است. این فایل با آن فرض منبعی سازگار اثبات نشده؛ نباید مقدار را در ۱۰ ضرب کرد یا بدون تصمیم مالک به یک مقدار canonical فروکاست.
- عنوان «دلار امريکا» به‌تنهایی اثبات نمی‌کند نرخ آزاد است یا مرکز مبادله؛ نوع نرخ و معنای خرید/فروش نیازمند تأیید مالک/منبع است.

**نتیجهٔ mapping:** این فایل نمونهٔ ساختاری واقعی برای بررسی است، اما در وضعیت فعلی نه به `FREE_MARKET` و نه به `EXCHANGE_CENTER` قابل انتساب نیست. دو ستون خرید/فروش و واحد ریال، با قرارداد canonical موجود تعارض/فاصله دارند؛ Feed profile نباید فعال شود تا منشأ، نوع نرخ، تقویم، basis، معنای buy/sell و رابطهٔ واحد با قرارداد Toman/USD روشن شود.

### 10.4 مقایسه و اثر بر Taskها

| نیاز DB-STD-005 | شاهد تازه | نتیجه |
|---|---|---|
| یک نمونهٔ واقعی MarketDaily | یک CSV با ۲۱ ردیف و Header مشخص | نمونهٔ ساختاری دریافت شد؛ مشخصات معنایی/منبع ناقص است |
| نمونهٔ FREE_MARKET | فایل FX بدون نوع نرخ اثبات‌شده | تأمین نشده |
| نمونهٔ EXCHANGE_CENTER | فایل FX بدون نوع نرخ اثبات‌شده | تأمین نشده |
| ShareCountHistory / CorporateAction | در این دو فایل داده‌ای ارائه نشده | روش ورود V1 هنوز نیازمند تصمیم مالک است |
| source/revision/publication metadata | در فایل‌ها مشاهده نشده | پروفایل PIT و revision ناقص است |

بنابراین، موجودی قبلی §9 دربارهٔ نبود فایل‌های tracked در Git/Library همچنان درست در همان دامنه است، اما اکنون با دو نمونهٔ محلی تکمیل شده و دیگر نباید گفته شود هیچ نمونهٔ محلی در دسترس نیست. DB-STD-005 از «نبود نمونه» به «وجود نمونه‌های ساختاری با blockerهای معنایی/منبع» پیشرفت کرده است؛ وضعیت همچنان PARTIAL است. DB-STD-001/Task 021 نیز به همین دلیل PARTIAL باقی می‌ماند.

**اقدام بعدی محدود و مشخص:** تأیید مالک/منبع برای (۱) تعریف دقیق Close و Final و واحد/scale همهٔ ستون‌های عددی CSV، (۲) هویت منبع و روش استخراج CSV، (۳) تقویم، منبع و نوع نرخ فایل دلار، (۴) علت وجود Buy/Sell و واحد ریال در برابر قرارداد Toman/USD، و (۵) تصمیم ورود V1 برای ShareCountHistory و CorporateAction. تا آن زمان هیچ Feed profile فعال، mapping قطعی، تبدیل واحد یا ingestion مجاز نیست.

هیچ کد، ORM، schema، migration، دیتابیس یا داده‌ای تغییر نکرد و هیچ تستی اجرا نشد.
