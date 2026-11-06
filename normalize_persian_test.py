from pathlib import Path
import unicodedata

source = Path("pdf/extraction_test/Fzar_pymupdf_raw.txt")
output = Path("pdf/extraction_test/Fzar_normalized.txt")

text = source.read_text(encoding="utf-8")

# تبدیل اعداد فارسی و عربی به انگلیسی
digit_map = str.maketrans(
    "۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩",
    "01234567890123456789"
)

# استانداردسازی حروف و اعداد
normalized = unicodedata.normalize("NFKC", text)
normalized = normalized.translate(digit_map)

# یکسان‌سازی حروف عربی و فارسی
normalized = normalized.replace("ي", "ی")
normalized = normalized.replace("ك", "ک")

output.write_text(normalized, encoding="utf-8")

print(f"Saved: {output}")

# بررسی کلمات مورد انتظار
for word in ["تراورتن", "کانسنگ", "طلا", "فروش", "تن"]:
    count = normalized.count(word)
    print(f"{word}: {count} matches")

# بررسی نمونه متن ترکیبی
for line in normalized.splitlines():
    if "اصلاح" in line or "1405" in line:
        print("\n", line)