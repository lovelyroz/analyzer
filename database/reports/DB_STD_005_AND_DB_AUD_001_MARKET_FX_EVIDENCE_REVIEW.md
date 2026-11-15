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
