(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_ingestion_ohlc.py::test_market_price_as_of_rejects_missing_or_invalid_requested_date
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\winprojects\analyzer
collected 1 item

src\tests\test_ingestion_ohlc.py .                                                                               [100%]

================================================== 1 passed in 0.98s
(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_ingestion_ohlc.py::test_market_price_as_of_discards_impossible_stored_date
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\winprojects\analyzer
collected 1 item

src\tests\test_ingestion_ohlc.py .                                                                               [100%]

================================================== 1 passed in 0.60s
(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_ingestion_ohlc.py::test_market_price_as_of_accepts_valid_jalali_month_end_and_leap_boundary
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\winprojects\analyzer
collected 1 item

src\tests\test_ingestion_ohlc.py .                                                                               [100%]

================================================== 1 passed in 0.61s
(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_ingestion_ohlc.py::test_market_price_as_of_accepts_valid_jalali_month_end_and_leap_boundary
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\winprojects\analyzer
collected 1 item

src\tests\test_ingestion_ohlc.py .                                                                               [100%]

================================================== 1 passed in 0.61s ==================================================
(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_ingestion_ohlc.py::test_market_price_as_of_selects_exact_date_and_preserves_provenance
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\winprojects\analyzer
collected 1 item

src\tests\test_ingestion_ohlc.py .                                                                               [100%]

================================================== 1 passed in 0.60s
(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_ingestion_ohlc.py::test_market_price_as_of_uses_latest_prior_date_across_year_boundary
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\winprojects\analyzer
collected 1 item

src\tests\test_ingestion_ohlc.py .                                                                               [100%]

================================================== 1 passed in 0.60s
(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_ingestion_ohlc.py::test_market_price_as_of_isolates_company_and_ignores_undated_rows
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\winprojects\analyzer
collected 1 item

src\tests\test_ingestion_ohlc.py .                                                                               [100%]

================================================== 1 passed in 0.95s
(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_ingestion_ohlc.py::test_migration_5_adds_jalali_columns
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\winprojects\analyzer
collected 1 item

src\tests\test_ingestion_ohlc.py .                                                                               [100%]

================================================== 1 passed in 0.63s
(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_ingestion_ohlc.py
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\winprojects\analyzer
collected 14 items

src\tests\test_ingestion_ohlc.py ..............                                                                  [100%]

================================================= 14 passed in 0.87s