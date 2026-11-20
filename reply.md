# ممیزی محلی Feed بازار و نرخ ارز

- نوع کار: فقط گزارش؛ هیچ کد، فایل اصلی یا پایگاه‌داده‌ای تغییر نکرده است.
- تاریخ ممیزی: ۱۹ نوامبر ۲۰۲۶.
- روش: بررسی مستقیم CSV با کتابخانه csv و XLSX با openpyxl؛ آمار روی همهٔ رکوردهای واقعی محاسبه شد.

## 1. Executive Summary

| Feed | یافته | آمادگی |
|---|---|---|
| MarketDaily | ۱۲ ستون، ۲۱ رکورد؛ Headerهای تاریخ، OHLC، Final، Volume، Value، No، Ticker، Name و Market. | کافی نیست؛ منبع، واحد/مقیاس، معنی Close و Final، سیاست تکرار و نسخه نامعلوم است. |
| FXRate | یک Worksheet و ۱۹ رکورد؛ عنوان دلار امریکا و سرستون‌های خرید و فروش به ریال. | کافی نیست؛ نوع نرخ، منبع، تقویم، مبنای نرخ و زمان انتشار/نسخه روشن نیست. |

CSV دو ردیف خالی انتهایی دارد. Excel داده را در ردیف‌های ۴ تا ۲۲ دارد؛ max_row=503 از محدوده قالب‌بندی‌شده ناشی می‌شود، نه ۵۰۰ رکورد. بازه CSV برابر 1402-01-08 تا 1402-02-12؛ بازه Excel برابر 1405-08-28 تا 1405-08-10 و نزولی است.

## 2. File Identity and Integrity

| فایل | مسیر کامل | اندازه | آخرین تغییر محلی | SHA-256 |
|---|---|---:|---|---|
| CSV | D:\\winprojects\\analyzer\\saman_price_history.csv | 2,400 بایت | 2026-11-19 11:35:48 +03:30 | d94f27405f257b4010e1d2b7db4a554311484a6dde2b35a9c81c548f381c1413 |
| XLSX | D:\\winprojects\\analyzer\\dollar-history.xlsx | 14,349 بایت | 2026-11-19 11:42:50 +03:30 | eb85250100438335accb06ca1fdf364304887a71e361258b93836d3a90dd6fcf |

هر نام دقیق فقط یک بار در ریشه پروژه یافت شد. CSV دارای UTF-8 BOM (EF BB BF)، جداکننده کاما و CRLF است.

## 3. CSV Structural Audit

Header در سطر ۱، ۱۲ ستون، ۲۱ رکورد واقعی در سطرهای فیزیکی ۲ تا ۲۲، دو سطر خالی در ۲۳ و ۲۴. Header تکراری، سطر توضیحی، یا عرض ناسازگار مشاهده نشد. Headerهای دقیق: J-Date, Open, High, Low, Close, Final, Volume, Value, No, Ticker, Name, Market. تمام مقادیر عددی رشتهٔ ارقام صحیح ASCII هستند.

## 4. CSV Field-Level Audit

| Field | Header | نوع | نمونه | Null | صفر | Min | Max | تفسیر/ابهام |
|---|---|---|---|---:|---:|---:|---:|---|
| Date | J-Date | متن تاریخ | 1402-01-08 | 0 | — | — | — | Header جلالی را نشان می‌دهد؛ معامله بودن UNKNOWN. |
| Open | Open | عدد صحیح متنی | 3022 | 0 | 0 | 3022 | 4140 | واحد/مقیاس UNKNOWN. |
| High | High | عدد صحیح متنی | 3022 | 0 | 0 | 3022 | 4140 | واحد/مقیاس UNKNOWN. |
| Low | Low | عدد صحیح متنی | 3022 | 0 | 0 | 3022 | 4000 | واحد/مقیاس UNKNOWN. |
| Close | Close | عدد صحیح متنی | 3022 | 0 | 0 | 3022 | 4025 | خام/تعدیل‌شده UNKNOWN. |
| Final | Final | عدد صحیح متنی | 3022 | 0 | 0 | 3022 | 4025 | رابطه با Close UNKNOWN. |
| Volume | Volume | عدد صحیح متنی | 14738930 | 0 | 0 | 6853871 | 326247149 | واحد UNKNOWN. |
| Value | Value | عدد صحیح متنی | 44541046460 | 0 | 0 | 21966565555 | 1072602451231 | معنای دقیق/واحد UNKNOWN. |
| No | No | عدد صحیح متنی | 263 | 0 | 0 | 169 | 5223 | نقش UNKNOWN. |
| Ticker | Ticker | متن | سامان | 0 | — | — | — | برچسب نماد؛ شناسه پایدار UNKNOWN. |
| Name | Name | متن | بانک سامان | 0 | — | — | — | نام شرکت طبق منبع. |
| Market | Market | متن | پایه زرد | 0 | — | — | — | برچسب بازار؛ نگاشت UNKNOWN. |

هر ۲۱ مقدار هر ستون پر است. تاریخ‌ها قالب YYYY-MM-DD و صعودی‌اند؛ بازه 1402-01-08 تا 1402-02-12؛ تاریخ تکراری/ناقص/نامعتبر صفر. Open/High/Low/Close و Final موجودند. Volume و Value نیز موجودند، اما واحد/مقیاس تأیید نشده. دو ستون Close و Final به‌تنهایی تمایز خام/تعدیل را ثابت نمی‌کنند.

## 5. Excel Workbook Audit

Workbook یک شیت visible با نام Sheet دارد؛ ابعاد گزارش‌شده A1:C503 و محدودهٔ دارای مقدار A1:C22. ردیف ۱ عنوان، ۲ خالی در محدوده ادغام، ۳ Header و ردیف‌های داده ۴ تا ۲۲ (۱۹ ردیف). ۴۸۱ ردیف بعدی بدون مقدار است. Merge: A1:C2؛ Formula و Excel Table ندارد؛ rightToLeft=None. عنوان A1 «دلار امريکا».

## 6. Excel Worksheet and Field-Level Audit

Header ردیف ۳: «تاریخ»، «خرید (ریال)»، «فروش (ریال)». سه ستون در ۱۹ ردیف کامل‌اند. تاریخ و نرخ‌ها رشته متنی‌اند، نه مقادیر Date/number اکسل.

| Field | Header | نوع | نمونه | Null | صفر | Min | Max | تفسیر/ابهام |
|---|---|---|---|---:|---:|---:|---:|---|
| Rate date | تاریخ | متن | 1405-08-28 | 0 | — | — | — | قالب YYYY-MM-DD؛ تقویم UNKNOWN. |
| Buy | خرید (ریال) | عدد صحیح متنی | 1918902 | 0 | 0 | 1858528 | 1918902 | ریال در Header؛ مبنای نرخ UNKNOWN. |
| Sell | فروش (ریال) | عدد صحیح متنی | 1936329 | 0 | 0 | 1875407 | 1936329 | ریال در Header؛ مبنای نرخ UNKNOWN. |

## 7. Date and Numeric Format Analysis

CSV: J-Date شاهد جلالی و قالب YYYY-MM-DD است؛ ترتیب صعودی. Excel: رشته‌های YYYY-MM-DD نزولی، اما تقویم UNKNOWN. اعداد در هر دو فایل ارقام صحیح ASCII و بدون اعشار یا جداکننده‌اند. نرخ Excel در Header ریال دارد؛ قرارداد صریح Rial per USD و دقت منبع/گردکردن UNKNOWN. عنوان دلار فقط قرینهٔ نوع ارز است و نوع نرخ آزاد/مرکز مبادله را تعیین نمی‌کند. هیچ تبدیل تومان به ریال اجرا نشد.

## 8. Data Quality Findings

CSV: High < Low صفر؛ Open، Close و Final خارج از Low..High هرکدام صفر؛ تاریخ نامعتبر/تکراری، Null، صفر، منفی، مقدار غیرعددی، عرض ناسازگار و ترتیب نامنظم صفر. دو ردیف خالی انتهایی جدا از داده‌اند. Close و Final در ۱۶ ردیف متفاوت و در ۵ ردیف برابرند؛ سطر ۵ (1402-01-15): 3254/3288؛ سطر ۲۲ (1402-02-12): 3820/3864. با معیار Tukey (مرز 1.5×IQR) در مقادیر قیمتی outlier مشاهده نشد؛ در Volume، Value و No ریکورد 1402-01-15 برای هر سه ستون به‌عنوان مقدار پرت آماری علامت می‌خورد (به‌ترتیب 326247149، 1072602451231 و 5223)؛ این تشخیص خطای منبع را اثبات نمی‌کند و بدون واحد/معنای ستون‌ها اصلاحی انجام نشد.

Excel: ۱۹ رکورد کامل؛ تاریخ تکراری، Null، صفر/منفی/غیرعددی یا فرمول دیده نشد. نرخ‌های دو روز پیاپی برابرند: 1405-08-22 و 1405-08-21 هر دو 1896036/1913255؛ 1405-08-15 و 1405-08-14 هر دو 1873442/1890456. این به‌تنهایی خطا را ثابت نمی‌کند.

## 9. DB-STD-005 Compatibility Matrix

| Domain / ویژگی | وضعیت | شواهد و محدودیت |
|---|---|---|
| MarketDaily: Source identity | UNKNOWN | منبع درج نشده. |
| Company identity | PARTIALLY_CONFIRMED | Name/Ticker موجود؛ شناسه پایدار نامعلوم. |
| Trading date | PARTIALLY_CONFIRMED | J-Date جلالی؛ معامله‌بودن صریح نیست. |
| OHLC | PARTIALLY_CONFIRMED | ستون‌ها موجود؛ واحد/مقیاس نامعلوم. |
| Raw/Adjusted | UNKNOWN | Close/Final تعریف نشده. |
| Volume / Trading value | PARTIALLY_CONFIRMED | ستون‌ها هستند؛ واحد/معنا کامل نیست. |
| Unit and scale | UNKNOWN | در CSV درج نشده. |
| Nullability | CONFIRMED_FROM_FILE | ۲۱ رکورد فعلی کامل‌اند؛ سیاست آتی نامعلوم. |
| Duplicate policy | UNKNOWN | قاعده‌ای در فایل نیست. |
| Revision/publication metadata | NOT_PRESENT | مشاهده نشد. |
| FXRate: Source identity, Rate type | UNKNOWN | ناشر و آزاد/مرکز مبادله مشخص نیست. |
| Rate date | PARTIALLY_CONFIRMED | تاریخ متنی هست؛ تقویم/معنا نامعلوم. |
| Currency / source unit | PARTIALLY_CONFIRMED | عنوان دلار و ریال در Header؛ کد و مبنای نرخ صریح نیست. |
| Canonical unit compatibility | PARTIALLY_CONFIRMED | Rial per USD تأیید مالک می‌خواهد. |
| Decimal precision | CONFIRMED_FROM_FILE | رشته‌های صحیح؛ دقت منبع/rounding UNKNOWN. |
| Duplicate policy | UNKNOWN | قاعده‌ای مشخص نشده. |
| Publication time / revision | NOT_PRESENT | مشاهده نشد. |

## 10. Unresolved Questions

مالک باید منبع و روش استخراج، شناسه پایدار شرکت/دارایی، نگاشت Market، تعریف Close و Final، واحد/مقیاس OHLC و Volume/Value، معنی No، تقویم و ماهیت تاریخ‌ها، نوع نرخ ارز، مبنای Rial per USD، precision/rounding، زمان انتشار، نسخه‌بندی و سیاست تکرار/Null را تأیید کند. همچنین مشخص شود بازه‌های ۱۴۰۲ و ۱۴۰۵ دوره‌های مورد انتظار Task 025 هستند.

## 11. Final Readiness Assessment

| Domain | تأییدشده | حل‌نشده / مانع | آمادگی |
|---|---|---|---|
| MarketDaily | ساختار، ۲۱ ردیف، J-Date، نام شرکت/نماد/بازار، کنترل OHLC | منبع، شناسه، واحد، Close/Final، سیاست‌ها | آماده پذیرش نیست. |
| FXRate | یک شیت، ۱۹ ردیف، خرید/فروش و برچسب ریال، عنوان دلار | منبع، نوع نرخ، تقویم، مبنای واحد، زمان/نسخه | آماده پذیرش نیست. |

برای بستن Task 025 مالک باید موارد حل‌نشده را تأیید کند. mapping مبهم Close/Final قطعی نشود؛ تبدیل تومان به ریال تا تأیید واحد منبع انجام نشود.

## 12. Evidence Appendix

نمونه‌ها عیناً از فایل‌ها درج می‌شوند: ۱۰ رکورد اول و آخر CSV، و تمام رکوردهای واقعی Excel.

### CSV: ده رکورد نخست

| Row | J-Date | Open | High | Low | Close | Final | Volume | Value | No | Ticker | Name | Market |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| 2 | 1402-01-08 | 3022 | 3022 | 3022 | 3022 | 3022 | 14738930 | 44541046460 | 263 | سامان | بانک سامان | پایه زرد |
| 3 | 1402-01-09 | 3112 | 3112 | 3112 | 3112 | 3112 | 10918715 | 33979041080 | 208 | سامان | بانک سامان | پایه زرد |
| 4 | 1402-01-14 | 3205 | 3205 | 3205 | 3205 | 3205 | 6853871 | 21966656555 | 169 | سامان | بانک سامان | پایه زرد |
| 5 | 1402-01-15 | 3301 | 3301 | 3205 | 3254 | 3288 | 326247149 | 1072602451231 | 5223 | سامان | بانک سامان | پایه زرد |
| 6 | 1402-01-16 | 3249 | 3386 | 3195 | 3386 | 3359 | 104154742 | 349843581079 | 2077 | سامان | بانک سامان | پایه زرد |
| 7 | 1402-01-19 | 3400 | 3450 | 3302 | 3335 | 3365 | 107774424 | 362649702532 | 2608 | سامان | بانک سامان | پایه زرد |
| 8 | 1402-01-20 | 3305 | 3449 | 3301 | 3390 | 3383 | 77622414 | 262562412711 | 1812 | سامان | بانک سامان | پایه زرد |
| 9 | 1402-01-21 | 3383 | 3484 | 3298 | 3349 | 3407 | 65834443 | 224275643918 | 1591 | سامان | بانک سامان | پایه زرد |
| 10 | 1402-01-22 | 3399 | 3399 | 3310 | 3363 | 3335 | 63971513 | 213366619095 | 1121 | سامان | بانک سامان | پایه زرد |
| 11 | 1402-01-26 | 3400 | 3435 | 3360 | 3435 | 3433 | 54881290 | 188416747098 | 832 | سامان | بانک سامان | پایه زرد |

### CSV: ده رکورد انتهایی

| Row | J-Date | Open | High | Low | Close | Final | Volume | Value | No | Ticker | Name | Market |
|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| 13 | 1402-01-28 | 3599 | 3632 | 3500 | 3632 | 3627 | 100339604 | 363936087392 | 1616 | سامان | بانک سامان | پایه زرد |
| 14 | 1402-01-29 | 3735 | 3735 | 3700 | 3735 | 3735 | 31021654 | 115852158005 | 546 | سامان | بانک سامان | پایه زرد |
| 15 | 1402-01-30 | 3847 | 3847 | 3681 | 3847 | 3813 | 66422735 | 253256754007 | 1689 | سامان | بانک سامان | پایه زرد |
| 16 | 1402-02-04 | 3890 | 3927 | 3839 | 3927 | 3908 | 32251027 | 126033590915 | 833 | سامان | بانک سامان | پایه زرد |
| 17 | 1402-02-05 | 4025 | 4025 | 4000 | 4025 | 4025 | 47467746 | 191046354343 | 859 | سامان | بانک سامان | پایه زرد |
| 18 | 1402-02-06 | 4140 | 4140 | 3905 | 3950 | 3996 | 48334345 | 193124863601 | 1538 | سامان | بانک سامان | پایه زرد |
| 19 | 1402-02-09 | 3950 | 3989 | 3877 | 3920 | 3902 | 83642317 | 326369438567 | 1922 | سامان | بانک سامان | پایه زرد |
| 20 | 1402-02-10 | 4000 | 4010 | 3877 | 3901 | 3937 | 25980468 | 102287320767 | 570 | سامان | بانک سامان | پایه زرد |
| 21 | 1402-02-11 | 3980 | 3980 | 3819 | 3936 | 3843 | 97572277 | 374941422663 | 1979 | سامان | بانک سامان | پایه زرد |
| 22 | 1402-02-12 | 3900 | 3950 | 3781 | 3820 | 3864 | 59390437 | 229512565736 | 1677 | سامان | بانک سامان | پایه زرد |

### Excel: all records in Sheet!A4:C22

| Range | Date | Buy (Rial) | Sell (Rial) |
|---|---|---:|---:|
| Sheet!A4:C4 | 1405-08-28 | 1918902 | 1936329 |
| Sheet!A5:C5 | 1405-08-27 | 1915072 | 1932464 |
| Sheet!A6:C6 | 1405-08-26 | 1911250 | 1928607 |
| Sheet!A7:C7 | 1405-08-25 | 1907435 | 1924758 |
| Sheet!A8:C8 | 1405-08-24 | 1903628 | 1920916 |
| Sheet!A9:C9 | 1405-08-23 | 1899828 | 1917082 |
| Sheet!A10:C10 | 1405-08-22 | 1896036 | 1913255 |
| Sheet!A11:C11 | 1405-08-21 | 1896036 | 1913255 |
| Sheet!A12:C12 | 1405-08-20 | 1892251 | 1909436 |
| Sheet!A13:C13 | 1405-08-19 | 1888474 | 1905625 |
| Sheet!A14:C14 | 1405-08-18 | 1884705 | 1901821 |
| Sheet!A15:C15 | 1405-08-17 | 1880943 | 1898025 |
| Sheet!A16:C16 | 1405-08-16 | 1877189 | 1894237 |
| Sheet!A17:C17 | 1405-08-15 | 1873442 | 1890456 |
| Sheet!A18:C18 | 1405-08-14 | 1873442 | 1890456 |
| Sheet!A19:C19 | 1405-08-13 | 1869702 | 1886682 |
| Sheet!A20:C20 | 1405-08-12 | 1865971 | 1882917 |
| Sheet!A21:C21 | 1405-08-11 | 1862246 | 1879158 |
| Sheet!A22:C22 | 1405-08-10 | 1858528 | 1875407 |
=======================================================

### A. Completion

**COMPLETE** برای ممیزی و اصلاح مستندات. تصمیم‌های مصوب مالک حفظ شدند و شکاف‌های provenance به‌صورت صریح باز ماندند؛ هیچ Feed به‌عنوان آمادهٔ تولید یا فعال اعلام نشد.

### B. Changes

- [گزارش شواهد Market/FX](/D:/winprojects/analyzer/database/reports/DB_STD_005_AND_DB_AUD_001_MARKET_FX_EVIDENCE_REVIEW.md): اصلاح وضعیت فعلی artifactها در §10.1؛ افزودن ماتریس تطبیق و رجیستر ۱۰ موردی در §19.
- [Master Working Packet](/D:/winprojects/analyzer/database/DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md): افزودن خلاصهٔ وضعیت منبع، mapping، provenance و ارجاع به §19 در §9.30.
- [قرارداد DB-DES-005](/D:/winprojects/analyzer/database/reports/DB_DES_005_INGESTION_ATOMICITY_CONTRACT.md): ثبت تصمیم‌های مالک و تفکیک source identity از artifact/revision identity در §13.10؛ تأکید بر موقتی‌بودن guardrailها و پیشنهادی‌بودن test plan §13.8.

### C. Evidence verification

هر دو artifact در checkout موجود و tracked بودند؛ hashها مستقیماً محاسبه و با مقدار مورد انتظار تطبیق داده شدند:

- `D:\winprojects\analyzer\saman_price_history.csv` — مورد انتظار و واقعی: `d94f27405f257b4010e1d2b7db4a554311484a6dde2b35a9c81c548f381c1413` — **تطبیق دارد**؛ ۲۱ رکورد.
- `D:\winprojects\analyzer\dollar-history.xlsx` — مورد انتظار و واقعی: `eb85250100438335accb06ca1fdf364304887a71e361258b93836d3a90dd6fcf` — **تطبیق دارد**؛ یک Worksheet و ۱۹ رکورد.

نمونهٔ واقعی FREE_MARKET در checkout یافت نشد؛ جایگزینی انتخاب نشد.

### D. Remaining blockers

- **CODAL:** زمان انتشار رسمی، نخستین زمان دسترس‌پذیری و شواهد revision/correction نداریم. برای بستن، مدرک قابل‌ردیابی همان خروجی به انتشار CODAL و metadata زمانی/اصلاحیه لازم است.
- **EXCHANGE_CENTER:** mapping فروش به Rial/USD مصوب است و hash فایل تأیید شد؛ پیوند قابل‌ردیابی همین artifact به Feed profile، زمان‌های انتشار/دسترس‌پذیری و شواهد اصلاحیه هنوز موجود نیست.
- **FREE_MARKET:** artifact واقعی و ممیزی منبع، header، تقویم و provenance لازم است؛ تبدیل Toman/USD × 10 به‌تنهایی برای فعال‌سازی کافی نیست.
- سیاست نهایی fingerprint و رتبه‌بندی revision تعیین نشده است؛ payload متفاوت بدون revision معتبر همچنان conflict/review است.

هر سه Feed برای activation همچنان **BLOCKED / not production-ready** هستند. DB-DES-005 و DB-STD-005 نیز **PARTIAL** باقی می‌مانند.

### E. Validation

- سه سند هدف و بخش‌های مرتبط، از جمله acceptance criteria §11 و test plan پیشنهادی §13.8، تطبیق داده شدند.
- hashها، mappingها، تاریخ‌ها، کلیدهای اقتصادی و ارجاع‌های جدید بین اسناد کنترل شدند؛ جدول‌های افزوده‌شده معتبرند و `git diff --check` گذشت.
- `origin/master` پیش از تغییر با شاخهٔ محلی هم‌تراز بود. commit فقط شامل سه سند مجاز است.
- هیچ کد، تست، ORM، schema، migration یا دیتابیسی تغییر نکرد؛ هیچ تستی اجرا نشد.
- یک جدول قدیمی نامتوازن در بخش نامرتبط Master Working Packet در بررسی کلی دیده شد؛ خارج از دامنه نگه داشته شد.
- تغییر محلیِ موجود در `prompt.md` دست‌نخورده و خارج از commit باقی ماند.

### F. Git

- شاخه: `master`
- commit: `a0f0ce811d2058345b93c1239ce0e936c4dcb298`
- وضعیت پس از commit: فقط `prompt.md` همچنان با تغییر محلیِ قبلی مشخص است؛ فایل staged باقی نمانده.
- commit محلی است و push انجام نشد.

### G. Next action

بالاترین اولویت بعدی، تهیهٔ بستهٔ provenance قابل‌ردیابی برای artifactهای بررسی‌شدهٔ CODAL و EXCHANGE_CENTER است: اتصال هر فایل به منبع/profile و شواهد زمان انتشار، نخستین دسترس‌پذیری و رفتار اصلاحیه.
# DB-IMP-003 Market/FX preflight validator — 2026-11-20

- Implemented the read-only validator, CLI, usage guide, JSON sample report, and 12 temporary-fixture tests. Tests: `python -m pytest -q src/tests/test_market_fx_preflight.py` — **12 passed**.
- Ran CLI against the real artifacts. Results: MarketDaily **BLOCKED** (21 rows; stable company key not supplied), EXCHANGE_CENTER **WARNING** (19 rows; one sheet named `Sheet`), FREE_MARKET **BLOCKED_NO_SAMPLE**; overall **BLOCKED**. This is a preflight result, not a production-readiness assertion. Source publisher linkage, source publication/availability times, and revision identities remain unverified; timestamps are not guessed.
- Source hashes before and after execution are identical: CSV `d94f27405f257b4010e1d2b7db4a554311484a6dde2b35a9c81c548f381c1413`; XLSX `eb85250100438335accb06ca1fdf364304887a71e361258b93836d3a90dd6fcf`. No database connection, ingestion, or source-file write occurred. `git diff --check` passed.
- Deliverables: [validator](../src/preflight/market_fx.py), [CLI](../src/scripts/market_fx_preflight.py), [tests](../src/tests/test_market_fx_preflight.py), [usage](../docs/market_fx_preflight.md), [sample report](./reports/market_fx_preflight_sample.json), [implementation report](./reports/DB_IMP_003_MARKET_FX_PREFLIGHT_VALIDATOR.md).

# TASK 3-CORRECTION — 2026-11-20

- Completed the CLI and validator corrections. `Ticker` is now used as `codal_symbol` when present, non-empty, and consistent. Date, numeric, required-field, and CSV row-width checks run independently of symbol resolution. FX duplicate keys are checked across worksheets and retain both cell references; conflicting payloads have no selected winner.
- Test command: `python -m pytest -q src/tests/test_market_fx_preflight.py` — **20 passed in 2.24s**.
- Real-artifact CLI command: `python -m src.scripts.market_fx_preflight --market saman_price_history.csv --fx dollar-history.xlsx --json-out database/reports/market_fx_preflight_sample.json`. Output: `MarketDaily: WARNING`; `EXCHANGE_CENTER: WARNING`; `FREE_MARKET: BLOCKED`; `Overall: BLOCKED`; exit code **1**. MarketDaily used CSV `Ticker` `سامان` as `codal_symbol` (21 rows); EXCHANGE_CENTER had 19 observations on `Sheet`; FREE_MARKET had no sample.
- Source SHA-256 values before and after remained unchanged: CSV `d94f27405f257b4010e1d2b7db4a554311484a6dde2b35a9c81c548f381c1413`; XLSX `eb85250100438335accb06ca1fdf364304887a71e361258b93836d3a90dd6fcf`. No database connection/write or ingestion occurred.
- Files changed for this correction: `.gitignore`, `src/preflight/market_fx.py`, `src/scripts/market_fx_preflight.py`, `src/tests/test_market_fx_preflight.py`, `docs/market_fx_preflight.md`, `database/reports/DB_IMP_003_MARKET_FX_PREFLIGHT_VALIDATOR.md`, and `database/reports/market_fx_preflight_sample.json`; this completion note was appended to `reply.md`. The pre-existing change to `prompt.md` was left untouched.

# TASK 4 — Market/FX source provenance dossier — 2026-11-20

- Created `database/reports/DB_AUD_011_MARKET_FX_SOURCE_PROVENANCE_DOSSIER.md` and `database/reports/market_fx_source_evidence.json`. Local trace found no producer/download script or configuration linking either artifact to a source response. The unrelated CODAL fiscal-year audit script uses CODAL search endpoints for filings, not this MarketDaily CSV.
- Current SHA-256: CSV `d94f27405f257b4010e1d2b7db4a554311484a6dde2b35a9c81c548f381c1413` (2,400 bytes, 21 records); XLSX `eb85250100438335accb06ca1fdf364304887a71e361258b93836d3a90dd6fcf` (14,349 bytes, 19 rate records). No source files changed.
- MarketDaily: source identity CODAL is locally documented as owner-approved, but exact endpoint/query, publication record ID, extraction method, transformations, publication/availability times, and revision remain unknown or blocked. All 21 rows are individually listed as not comparable because no official source record can be selected without a producer manifest/record identity.
- EXCHANGE_CENTER: official market-view page is identified, but no local download profile or accessible official dated archive/record IDs link it to this workbook. All 19 rows are listed with sheet/cell references and official comparison outcome. One row (1405-08-28, sell `1936329`) matches a secondary public mirror; this is recorded as corroboration only, not proof of official artifact provenance. Embedded Excel core properties are recorded as self-asserted artifact metadata, not source timestamps or independent creation evidence.
- `source_published_at`, `source_available_at`, `source_revision_identity`, and `ingested_at` remain UNKNOWN. The exact next prerequisites and remaining Task 025 / DB-STD-005 and Task 009 / DB-DES-004 gaps are in the dossier. No database access or ingestion was performed.

# TASK 034 — DB-ING-007 Market/FX File Adapters — 2026-11-20

- Market CSV adapter now requires and maps only `J-Date`, `Ticker`, `Close`, `Volume`, `No`, and `Value`. `Open`, `High`, `Low`, and `Final` are ignored and never populated into its DTO; malformed rows and duplicate/conflicting economic keys produce explicit parser errors.
- Added shared workbook parser used by the adapter and read-only preflight. It finds date/sell headers across worksheet rows, maps sell only, diagnoses invalid dates/rates and duplicates, preserves EXCHANGE_CENTER Rial values, and applies FREE_MARKET Toman × 10 using Decimal arithmetic. CLI accepts `--fx-rate-type EXCHANGE_CENTER|FREE_MARKET`.
- Updated [preflight guide](docs/market_fx_preflight.md) with exact user acceptance command and FREE_MARKET fixture test command. User acceptance was not claimed.
- Automated isolated test command: `.\.venv\Scripts\python.exe -m pytest -q src/tests/test_market_fx_adapters.py src/tests/test_market_fx_preflight.py` — **23 passed**, 0 failed, in 4.75s.
- Real-artifact read-only preflight command: `.\.venv\Scripts\python.exe -m src.scripts.market_fx_preflight --root . --market saman_price_history.csv --fx dollar-history.xlsx --fx-rate-type EXCHANGE_CENTER --json-out $env:TEMP\\market_fx_acceptance_preflight.json` — output `MarketDaily: WARNING`, `EXCHANGE_CENTER: WARNING`, `Overall: WARNING (read-only; no DB/ingestion)`, exit code 0. Warnings are provenance related; no FREE_MARKET real artifact was supplied.
- `git diff --check` passed (Git reported only LF-to-CRLF normalization notices). No ORM, schema, migration, database, UI, or persistence changes were made; no DB was opened and no data was ingested.
- Changed files: `src/ingestion/market/adapter.py`, `src/ingestion/fx/adapter.py`, `src/preflight/market_fx.py`, `src/scripts/market_fx_preflight.py`, `src/tests/test_market_fx_adapters.py`, and `docs/market_fx_preflight.md`. Pre-existing local modification `prompt.md` remains untouched.

# TASK 034 follow-up verification — 2026-11-20

- A second audit corrected FX preflight observation reporting: source sell values and canonical values are now distinct, with sheet and cell coordinates. FREE_MARKET applies ×10 only to the canonical value; EXCHANGE_CENTER leaves the value unchanged.
- Identical FX duplicates now produce WARNING; conflicting duplicate payloads remain FAIL. Provenance identifies the selected rate type. CLI `--root` help text no longer claims a FREE_MARKET scan.
- Added assertions for raw/canonical rates and identical duplicate severity.
- Final isolated test command: `.\.venv\Scripts\python.exe -m pytest -q src/tests/test_market_fx_adapters.py src/tests/test_market_fx_preflight.py` — **24 passed**, 0 failed, in 4.68s.
- Final real-artifact command: `.\.venv\Scripts\python.exe -m src.scripts.market_fx_preflight --root . --market saman_price_history.csv --fx dollar-history.xlsx --fx-rate-type EXCHANGE_CENTER --json-out $env:TEMP\\market_fx_acceptance_preflight.json` — `MarketDaily: WARNING`, `EXCHANGE_CENTER: WARNING`, overall `WARNING`, exit code 0. JSON confirms FX headers at row 3, sell column C, with `source_sell_rate=1936329`, `canonical_rate=1936329`, and sell cell `C4`.
- `git diff --check` passed with only Git LF-to-CRLF normalization notices. No DB/production access or user acceptance was performed.

# TASK 034 re-run — 2026-11-20

- Re-read the current `PROMPT.md` and revalidated the Market/FX adapter work. Tightened MarketDaily numeric validation: `Volume` and `No` must be integer-valued, all numeric fields must be finite, and duplicate approved headers are diagnosed/rejected. Updated the guide and added isolated tests for fractional integer fields and duplicate headers.
- First pytest attempt printed 26 passing tests but failed during pytest's Windows temporary-directory cleanup with `PermissionError` (`pytest-current`). Re-ran with an isolated workspace-local basetemp; final command `.\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_task034_20261120 src/tests/test_market_fx_adapters.py src/tests/test_market_fx_preflight.py` completed successfully: **26 passed**, 0 failed, in 5.15s. The temporary directory was removed after verifying it was inside the project.
- Re-ran real-artifact preflight: `.\.venv\Scripts\python.exe -m src.scripts.market_fx_preflight --root . --market saman_price_history.csv --fx dollar-history.xlsx --fx-rate-type EXCHANGE_CENTER --json-out .task034_preflight.json` — MarketDaily WARNING (21 rows), EXCHANGE_CENTER WARNING (19 rows), overall WARNING; exit code 0. Verified workbook header row 3, sell column C, and `Sheet!C4` raw/canonical rate `1936329`. Temporary report was removed after inspection.
- `git diff --check` passed; Git emitted LF-to-CRLF normalization notices only. No database, ORM, schema, migrations, or production state was touched. User acceptance remains for the user to run using the command in `docs/market_fx_preflight.md`.

# TASK 034 and TASK 035 — status correction and atomic ingestion — 2026-11-20

## Task 034 / DB-ING-007 — DONE (owner UAT accepted)

- Owner-confirmed UAT: `24 passed`; preflight `MarketDaily: WARNING`, `EXCHANGE_CENTER: WARNING`, `Overall: WARNING`. The remaining provenance warnings are not blockers under the owner decision recorded in Master Packet §9.31.
- Corrected the Master Packet current status and explicitly marked the old §9.32 “not done” conclusion as a historical pre-implementation snapshot.

## Task 035 / DB-ING-008 — PARTIAL (implementation and isolated tests complete; schema/concurrency boundaries remain)

- Implemented whole-batch validation and atomic canonical writes for Market and supported FX types; identical duplicates do not modify existing data; differing payloads reject the batch. Failure rollback and separate FAILED audit handling are covered. `Value` remains independent, unsupported Market OHLC/Final fields are not persisted, and FX rates are not multiplied by 10 a second time.
- `EXCHANGE_CENTER` ingestion is explicitly rejected with `SCHEMA_RATE_TYPE_UNSUPPORTED` because the existing FX type constraint omits it. Jalali concurrent uniqueness cannot be guaranteed by the existing Gregorian-date unique constraints. No ORM, schema, migration, real DB, or real ingestion was changed or used. These limitations keep the task PARTIAL.
- Changed/added files: `src/ingestion/common/atomic.py`, `src/ingestion/market/ingestion.py`, `src/ingestion/service.py`, `src/tests/test_market_fx_atomic_ingestion.py`, `src/tests/test_ingestion_ohlc.py`, `src/tests/test_ingestion_fx.py`, `database/reports/DB_ING_008_MARKET_FX_ATOMIC_INGESTION.md`, `database/DATABASE_CONFIGURATION_MASTER_WORKING_PACKET.md`, and this `reply.md`. `src/ingestion/fx/adapter.py` was already modified by Task 034 and was not changed for Task 035. Pre-existing user edit `prompt.md` was left untouched.
- Automated test command: `.\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_task035_final_20261120 src/tests/test_market_fx_atomic_ingestion.py src/tests/test_ingestion_ohlc.py src/tests/test_ingestion_fx.py src/tests/test_market_fx_adapters.py src/tests/test_market_fx_preflight.py`
- Actual output: `61 passed in 78.16s (0:01:18)` (exit code 0).
- Owner acceptance command, not run by the agent: `.\.venv\Scripts\python.exe -m pytest -q src/tests/test_market_fx_atomic_ingestion.py`. It uses isolated temporary test databases. Task 035 owner UAT has not been claimed.
- `git diff --check` passed. Git reported only LF-to-CRLF normalization notices.
