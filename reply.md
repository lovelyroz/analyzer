(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_codal_extraction.py::test_codal_ingestion_rejects_period_owned_by_another_company
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\winprojects\analyzer
collected 1 item

src\tests\test_codal_extraction.py .                                                                             [100%]

================================================== 1 passed in 0.60s ==================================================
(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_codal_extraction.py::test_codal_tracking_id_cannot_be_reused_for_another_company_or_period
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\winprojects\analyzer
collected 1 item

src\tests\test_codal_extraction.py .                                                                             [100%]

================================================== 1 passed in 0.58s ==================================================
(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_codal_extraction.py
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\winprojects\analyzer
collected 13 items

src\tests\test_codal_extraction.py ............s                                                                 [100%]

============================================ 12 passed, 1 skipped in 0.93s