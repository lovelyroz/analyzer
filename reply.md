فایل کدی تغییر نکرد و تستی اضافه یا ویرایش نشد. با قراردادهای فعلی، پر کردن trade_date برای تاریخ‌های CSV کار امنی نیست.

CSV صراحتاً تاریخ جلالی می‌گیرد: ستون J-Date یا Date را با parse_jalali_components می‌خواند. اما ابزار موجود فقط اجزای تاریخ جلالی را استخراج می‌کند و طبق توضیحش تبدیل تقویمی انجام نمی‌دهد. مدل، trade_date را فیلد Date سازگار با تاریخ میلادی تعریف کرده و برای ردیف‌های جلالی تهی می‌گذارد؛ همین قاعده در سیاست مهاجرت و تست test_null_not_zero نیز ثبت شده است. ابزار تبدیل معتبر دیگری هم در کد یا وابستگی‌ها پیدا نشد.

بنابراین اطلاعات مفقود، سیاست و ابزار موردتأیید پروژه برای تبدیل تاریخ جلالی CSV به تاریخ میلادی trade_date است. تا وقتی این قرارداد مشخص نشود، تبدیل‌کردن تاریخ یا تغییر رفتار فعلی حدس‌زدن و نقض قرارداد موجود خواهد بود. در نتیجه، ادعایی مبنی بر رفع عیب نمی‌کنم.

(analyzer) PS D:\winprojects\analyzer> .venv\Scripts\python.exe -m pytest src/tests/test_ingestion_ohlc.py::test_null_not_zero -v
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0 -- D:\winprojects\analyzer\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: D:\winprojects\analyzer
collected 1 item

src/tests/test_ingestion_ohlc.py::test_null_not_zero PASSED                                                      [100%]

================================================== warnings summary ===================================================
src/tests/test_ingestion_ohlc.py::test_null_not_zero
  D:\winprojects\analyzer\src\migrations\runner.py:175: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    {"version": 1, "name": "legacy_baseline", "applied_at": datetime.utcnow()},

src/tests/test_ingestion_ohlc.py::test_null_not_zero
src/tests/test_ingestion_ohlc.py::test_null_not_zero
src/tests/test_ingestion_ohlc.py::test_null_not_zero
src/tests/test_ingestion_ohlc.py::test_null_not_zero
src/tests/test_ingestion_ohlc.py::test_null_not_zero
src/tests/test_ingestion_ohlc.py::test_null_not_zero
src/tests/test_ingestion_ohlc.py::test_null_not_zero
  D:\winprojects\analyzer\.venv\Lib\site-packages\sqlalchemy\engine\default.py:952: DeprecationWarning: The default datetime adapter is deprecated as of Python 3.12; see the sqlite3 documentation for suggested replacement recipes
    cursor.execute(statement, parameters)

src/tests/test_ingestion_ohlc.py::test_null_not_zero
src/tests/test_ingestion_ohlc.py::test_null_not_zero
src/tests/test_ingestion_ohlc.py::test_null_not_zero
src/tests/test_ingestion_ohlc.py::test_null_not_zero
src/tests/test_ingestion_ohlc.py::test_null_not_zero
src/tests/test_ingestion_ohlc.py::test_null_not_zero
  D:\winprojects\analyzer\src\migrations\runner.py:186: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    {"version": migration.version, "name": migration.name, "applied_at": datetime.utcnow()},

src/tests/test_ingestion_ohlc.py::test_null_not_zero
src/tests/test_ingestion_ohlc.py::test_null_not_zero
  D:\winprojects\analyzer\.venv\Lib\site-packages\sqlalchemy\sql\schema.py:3627: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return util.wrap_callable(lambda ctx: fn(), fn)  # type: ignore

src/tests/test_ingestion_ohlc.py::test_null_not_zero
  D:\winprojects\analyzer\src\ingestion\market\ingestion.py:132: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    run.finished_at = datetime.utcnow()

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================================== 1 passed, 17 warnings in 1.35s
(analyzer) PS D:\winprojects\analyzer> .venv\Scripts\python.exe -m pytest src/tests/test_ingestion_ohlc.py -v
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0 -- D:\winprojects\analyzer\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: D:\winprojects\analyzer
collected 5 items

src/tests/test_ingestion_ohlc.py::test_parse_jalali_components PASSED                                            [ 20%]
src/tests/test_ingestion_ohlc.py::test_null_not_zero PASSED                                                      [ 40%]
src/tests/test_ingestion_ohlc.py::test_same_month_across_years PASSED                                            [ 60%]
src/tests/test_ingestion_ohlc.py::test_ingest_ohlc_idempotent PASSED                                             [ 80%]
src/tests/test_ingestion_ohlc.py::test_migration_5_adds_jalali_columns PASSED                                    [100%]

================================================== warnings summary ===================================================
src/tests/test_ingestion_ohlc.py::test_null_not_zero
src/tests/test_ingestion_ohlc.py::test_same_month_across_years
src/tests/test_ingestion_ohlc.py::test_ingest_ohlc_idempotent
src/tests/test_ingestion_ohlc.py::test_migration_5_adds_jalali_columns
  D:\winprojects\analyzer\src\migrations\runner.py:175: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    {"version": 1, "name": "legacy_baseline", "applied_at": datetime.utcnow()},

src/tests/test_ingestion_ohlc.py: 28 warnings
  D:\winprojects\analyzer\.venv\Lib\site-packages\sqlalchemy\engine\default.py:952: DeprecationWarning: The default datetime adapter is deprecated as of Python 3.12; see the sqlite3 documentation for suggested replacement recipes
    cursor.execute(statement, parameters)

src/tests/test_ingestion_ohlc.py: 24 warnings
  D:\winprojects\analyzer\src\migrations\runner.py:186: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    {"version": migration.version, "name": migration.name, "applied_at": datetime.utcnow()},

src/tests/test_ingestion_ohlc.py::test_null_not_zero
src/tests/test_ingestion_ohlc.py::test_null_not_zero
src/tests/test_ingestion_ohlc.py::test_same_month_across_years
src/tests/test_ingestion_ohlc.py::test_same_month_across_years
src/tests/test_ingestion_ohlc.py::test_ingest_ohlc_idempotent
src/tests/test_ingestion_ohlc.py::test_ingest_ohlc_idempotent
src/tests/test_ingestion_ohlc.py::test_ingest_ohlc_idempotent
  D:\winprojects\analyzer\.venv\Lib\site-packages\sqlalchemy\sql\schema.py:3627: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return util.wrap_callable(lambda ctx: fn(), fn)  # type: ignore

src/tests/test_ingestion_ohlc.py::test_null_not_zero
src/tests/test_ingestion_ohlc.py::test_same_month_across_years
src/tests/test_ingestion_ohlc.py::test_ingest_ohlc_idempotent
src/tests/test_ingestion_ohlc.py::test_ingest_ohlc_idempotent
  D:\winprojects\analyzer\src\ingestion\market\ingestion.py:132: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    run.finished_at = datetime.utcnow()

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================================== 5 passed, 67 warnings in 0.75s