سلام! مشکل شما دو بخش دارد و هر کدام راه‌حل جدا دارد.

## تشخیص مشکل

**۱. فارسی به هم‌ریخته:** PDF متن را به‌صورت ترتیب بصری (چپ‌به‌راست) ذخیره می‌کند، نه ترتیب منطقی. در نتیجه کلمات و حروف برعکس یا جابجا استخراج می‌شوند. در فایل شما هم همین را می‌بینید: ستون‌ها از راست به چپ هستند ولی متن استخراج‌شده ترتیب سلول‌ها را به‌هم می‌ریزد.

**۲. ارتباط اعداد با جدول:** استخراج متن خام (`extract_text`) ساختار جدول را از بین می‌برد. باید از **استخراج جدول بر اساس مختصات** استفاده کرد. نکته مهم در این گزارش‌ها (گزارش‌های کدال) این است که جدول RTL است، پس ستون اول در سمت راست قرار دارد.

## راه‌حل پیشنهادی

### نصب
```bash
pip install pdfplumber pandas arabic-reshaper python-bidi
```

### ۱. تبدیل اعداد فارسی/عربی به انگلیسی

نکته‌ی مهم در فایل شما: اعداد با ارقام فارسی (`۰-۹`) و عربی (`٠-٩`) **مخلوط** هستند (مثلاً `٢,١۴٨` که `٢` عربی و `۴` فارسی است). پس باید هر دو را پوشش داد. همچنین ممیز اعشاری (`٫`) و جداکننده هزارگان (`٬` و `,`) را هم باید مدیریت کرد.

```python
import re

_DIGITS = str.maketrans(
    "۰۱۲۳۴۵۶۷۸۹" "٠١٢٣٤٥٦٧٨٩",
    "0123456789" "0123456789",
)

def to_en_digits(s: str) -> str:
    return s.translate(_DIGITS)

def parse_number(s):
    """رشته عددی فارسی/عربی را به float/int تبدیل می‌کند."""
    if s is None:
        return None
    s = to_en_digits(str(s)).strip()
    s = s.replace("٬", ",").replace("٫", ".").replace("−", "-")
    s = re.sub(r"[,\s]", "", s)
    if s.startswith("(") and s.endswith(")"):   # اعداد منفی داخل پرانتز
        s = "-" + s[1:-1]
    try:
        f = float(s)
        return int(f) if f.is_integer() else f
    except ValueError:
        return None   # سلول متنی است
```

### ۲. استخراج جدول با pdfplumber

```python
import pdfplumber
import pandas as pd

def extract_tables(pdf_path):
    results = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_no, page in enumerate(pdf.pages, 1):
            tables = page.extract_tables({
                "vertical_strategy": "lines",      # اگر خط جدول ندارد: "text"
                "horizontal_strategy": "lines",
                "snap_tolerance": 3,
                "join_tolerance": 3,
                "intersection_tolerance": 5,
            })
            for t_idx, table in enumerate(tables):
                results.append((page_no, t_idx, table))
    return results
```

### ۳. اصلاح ترتیب فارسی و پاکسازی سلول‌ها

```python
def clean_cell(cell):
    if cell is None:
        return ""
    # حذف شکستگی خط داخل سلول (مثل «سنگ\nپلاک\nتراورتن»)
    text = " ".join(str(cell).split("\n")).strip()
    return to_en_digits(text)

def fix_persian_text(text: str) -> str:
    """
    اگر متن فارسی برعکس استخراج شد، این تابع را روی آن بزنید.
    اگر درست بود، نیازی به آن نیست؛ اول تست کنید.
    """
    return text[::-1]
```

> **نکته:** در فایل شما متن فارسی از نظر ترتیب کلمات عمدتاً درست استخراج می‌شود (فقط ترتیب ستون‌ها مشکل دارد). پس قبل از اعمال معکوس‌سازی، خروجی را چک کنید؛ معکوس‌کردن روی متن درست آن را خراب می‌کند.

### ۴. ساخت DataFrame با ترتیب درست ستون‌ها

```python
def table_to_df(table, rtl=True):
    rows = [[clean_cell(c) for c in row] for row in table]
    if rtl:
        rows = [row[::-1] for row in rows]   # ستون اول = سمت راست
    df = pd.DataFrame(rows)
    return df

def numeric_df(df):
    return df.map(lambda x: parse_number(x) if parse_number(x) is not None else x)
```

### ۵. اجرا

```python
tables = extract_tables("Fzar.pdf")
for page_no, idx, tbl in tables:
    df = numeric_df(table_to_df(tbl, rtl=True))
    df.to_csv(f"table_p{page_no}_{idx}.csv", index=False, encoding="utf-8-sig")
    print(df.head())
```

`utf-8-sig` باعث می‌شود Excel فارسی را درست نمایش دهد.

## اگر pdfplumber جدول را درست پیدا نکرد

گزارش شما سرستون‌های چندسطحی و سلول‌های ادغام‌شده دارد (مثل «از ابتدای سال مالی تا تاریخ ...» که روی ۴ ستون کشیده شده). در این حالت دو راه دارید:

**الف) استخراج بر اساس مختصات کلمات**، که قابل‌اعتمادترین روش است:

```python
def extract_by_words(pdf_path, y_tol=4):
    rows_all = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            words = page.extract_words(keep_blank_chars=False, use_text_flow=False)
            # گروه‌بندی کلمات بر اساس خط (y)
            words.sort(key=lambda w: (round(w["top"] / y_tol), -w["x1"]))
            current, last_y = [], None
            for w in words:
                y = round(w["top"] / y_tol)
                if last_y is not None and y != last_y:
                    rows_all.append(current); current = []
                current.append((w["x0"], w["x1"], w["text"]))
                last_y = y
            if current:
                rows_all.append(current)
    return rows_all
```

سپس هر عدد را با مختصات `x` به نزدیک‌ترین ستون سرستون نسبت دهید. این روش ارتباط عدد با ستون را تضمین می‌کند.

**ب) استفاده از camelot** (برای جدول‌های بدون خط): `pip install camelot-py` و `camelot.read_pdf(path, flavor="stream")`.

## نکات مهم برای فایل‌های شما

1. **ثابت‌بودن ساختار:** چون همه گزارش‌ها ساختار یکسان دارند، یک بار سرستون‌ها را دستی تعریف کنید (مثلاً `ytd_prev_month`, `adjustment`, `month`, `ytd_current`, `ytd_last_year`) و فقط مقادیر را استخراج کنید.
2. **ستون‌های هر بلوک:** در جدول تولید و فروش، هر دوره ۴ ستون دارد: تعداد تولید، تعداد فروش، نرخ فروش، مبلغ فروش. پس با گروه‌های ۴تایی می‌توانید معنا بدهید.
3. **اعداد کاذب:** مقادیری مثل `٨۶۵,٠٧۶.۵٩٠٠٠٠٠٠٠١` خطای ممیز شناور در خود گزارش هستند؛ بعد از تبدیل، با `round(x, 2)` گرد کنید.
4. **اعتبارسنجی:** مجموع ردیف‌ها را با ردیف «جمع» مقایسه کنید تا اشتباه در نگاشت ستون را سریع بفهمید.
5. **اگر PDF اسکن‌شده بود** (متن قابل انتخاب نبود)، باید OCR بزنید، مثلاً با `pytesseract` و بسته‌ی زبان `fas`.

اگر بخواهید، می‌توانم با همین فایل نمونه یک اسکریپت کامل بنویسم که جدول «تولید و فروش» را با نام ستون‌های انگلیسی و اعداد تمیز خروجی بدهد. فقط بگویید خروجی را CSV می‌خواهید یا Excel.