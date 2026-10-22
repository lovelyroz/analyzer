(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_stage9_decision.py::test_jalali_orchestration_passes_stage7_result_to_stage9
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\winprojects\analyzer
collected 1 item

src\tests\test_stage9_decision.py .                                                                              [100%]

================================================== 1 passed in 1.02s
(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_stage7_valuation.py
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\winprojects\analyzer
collected 75 items

src\tests\test_stage7_valuation.py ...........................................................................   [100%]

================================================= 75 passed in 0.84s ==================================================
(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_ingestion_ohlc.py
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\winprojects\analyzer
collected 14 items

src\tests\test_ingestion_ohlc.py ..............                                                                  [100%]

================================================= 14 passed in 0.87s