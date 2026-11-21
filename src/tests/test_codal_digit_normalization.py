from src.ingestion.codal.numbers import normalize_digits


def test_normalize_digits_maps_persian_and_arabic_indic_to_ascii():
    persian = "\u06f1\u06f2\u06f3\u06f4\u06f5\u06f6\u06f7\u06f8\u06f9\u06f0"
    arabic = "\u0661\u0662\u0663\u0664\u0665\u0666\u0667\u0668\u0669\u0660"
    assert normalize_digits(persian + " " + arabic) == "1234567890 1234567890"
