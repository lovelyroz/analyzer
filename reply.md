(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_stage7_valuation.py::test_jalali_service_uses_selected_price_and_preserves_provenance
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\winprojects\analyzer
collected 1 item

src\tests\test_stage7_valuation.py .                                                                             [100%]

================================================== warnings summary ===================================================
src/tests/test_stage7_valuation.py::test_jalali_service_uses_selected_price_and_preserves_provenance
  D:\winprojects\analyzer\Lib\site-packages\sqlalchemy\sql\schema.py:3627: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return util.wrap_callable(lambda ctx: fn(), fn)  # type: ignore

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
============================================ 1 passed, 1 warning in 1.83s
(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_stage7_valuation.py::test_jalali_service_fails_closed_without_eligible_observation
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\winprojects\analyzer
collected 1 item

src\tests\test_stage7_valuation.py .                                                                             [100%]

================================================== warnings summary ===================================================
src/tests/test_stage7_valuation.py::test_jalali_service_fails_closed_without_eligible_observation
  D:\winprojects\analyzer\Lib\site-packages\sqlalchemy\sql\schema.py:3627: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return util.wrap_callable(lambda ctx: fn(), fn)  # type: ignore

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
============================================ 1 passed, 1 warning in 0.61s
(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_stage7_valuation.py::test_jalali_service_rejects_forecast_from_another_company
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\winprojects\analyzer
collected 1 item

src\tests\test_stage7_valuation.py .                                                                             [100%]

================================================== warnings summary ===================================================
src/tests/test_stage7_valuation.py::test_jalali_service_rejects_forecast_from_another_company
  D:\winprojects\analyzer\Lib\site-packages\sqlalchemy\sql\schema.py:3627: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return util.wrap_callable(lambda ctx: fn(), fn)  # type: ignore

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
============================================ 1 passed, 1 warning in 0.61s
(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_stage7_valuation.py
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\winprojects\analyzer
collected 75 items

src\tests\test_stage7_valuation.py ...........................................................................   [100%]

================================================== warnings summary ===================================================
src/tests/test_stage7_valuation.py::test_jalali_service_uses_selected_price_and_preserves_provenance
src/tests/test_stage7_valuation.py::test_jalali_service_fails_closed_without_eligible_observation
src/tests/test_stage7_valuation.py::test_jalali_service_rejects_forecast_from_another_company
  D:\winprojects\analyzer\Lib\site-packages\sqlalchemy\sql\schema.py:3627: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return util.wrap_callable(lambda ctx: fn(), fn)  # type: ignore

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================================== 75 passed, 3 warnings in 0.76s