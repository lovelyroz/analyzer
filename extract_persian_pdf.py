from pathlib import Path
import unicodedata
import fitz

PDF = Path("pdf/Fzar.pdf")
OUT = Path("pdf/extraction_test")
OUT.mkdir(parents=True, exist_ok=True)

DIGIT_MAP = str.maketrans(
    "۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩",
    "01234567890123456789"
)

def normalize_persian(text):
    import unicodedata

    text = unicodedata.normalize("NFKC", text)

    # تبدیل اعداد فارسی و عربی به انگلیسی
    text = text.translate(DIGIT_MAP)

    # یکسان‌سازی حروف فارسی
    text = text.replace("ي", "ی")
    text = text.replace("ك", "ک")

    # حذف جداکننده هزارگان
    text = text.replace(",", "")
    text = text.replace("٬", "")
    text = text.replace("،", "")

    return text

doc = fitz.open(PDF)

raw_pages = []
normalized_pages = []

for page_number, page in enumerate(doc, start=1):
    # استخراج خام؛ بدون sort و بدون دستکاری
    raw = page.get_text("text", sort=False)

    # نرمال‌سازی بلافاصله بعد از استخراج
    normalized = normalize_persian(raw)

    raw_pages.append(
        f"\n===== PAGE {page_number} =====\n{raw}"
    )

    normalized_pages.append(
        f"\n===== PAGE {page_number} =====\n{normalized}"
    )

raw_text = "\n".join(raw_pages)
normalized_text = "\n".join(normalized_pages)

(OUT / "Fzar_raw.txt").write_text(raw_text, encoding="utf-8")
(OUT / "Fzar_normalized.txt").write_text(
    normalized_text, encoding="utf-8"
)

# گزارش مقایسه
words = ["تراورتن", "کانسنگ", "طلا", "فروش", "تن"]

report = []

report.append(f"PDF pages: {len(doc)}")

for word in words:
    raw_count = raw_text.count(word)
    normalized_count = normalized_text.count(word)

    report.append(
        f"{word}: raw={raw_count}, normalized={normalized_count}"
    )

report.append("\n--- Mixed Persian/Number lines ---")

for line in normalized_text.splitlines():
    if any(x in line for x in ["اصلاح", "1405", "1404"]):
        report.append(line)

(OUT / "Fzar_comparison.txt").write_text(
    "\n".join(report), encoding="utf-8"
)

print("\n".join(report))
print("\nExtraction completed.")