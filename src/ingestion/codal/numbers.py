"""Persian and Arabic-Indic digit normalization for CODAL persistence."""

_PERSIAN_DIGITS = str.maketrans(
    "\u06f0\u06f1\u06f2\u06f3\u06f4\u06f5\u06f6\u06f7\u06f8\u06f9\u0660\u0661\u0662\u0663\u0664\u0665\u0666\u0667\u0668\u0669",
    "01234567890123456789",
)


def normalize_digits(text: str) -> str:
    """Map Persian and Arabic-Indic digits to ASCII/English digits."""
    return str(text).translate(_PERSIAN_DIGITS)
