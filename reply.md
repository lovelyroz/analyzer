(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_stage9_decision.py::test_jalali_orchestration_passes_stage7_result_to_stage9
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\winprojects\analyzer
collected 1 item

src\tests\test_stage9_decision.py .                                                                              [100%]

================================================== warnings summary ===================================================
src/tests/test_stage9_decision.py::test_jalali_orchestration_passes_stage7_result_to_stage9
  D:\winprojects\analyzer\src\tests\test_stage9_decision.py:39: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    calculation_timestamp=datetime.utcnow(),

src/tests/test_stage9_decision.py::test_jalali_orchestration_passes_stage7_result_to_stage9
  D:\winprojects\analyzer\src\tests\test_stage9_decision.py:20: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    calculation_timestamp=datetime.utcnow(),

src/tests/test_stage9_decision.py::test_jalali_orchestration_passes_stage7_result_to_stage9
  D:\winprojects\analyzer\src\tests\test_stage9_decision.py:49: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    as_of_date=datetime.utcnow(),

src/tests/test_stage9_decision.py::test_jalali_orchestration_passes_stage7_result_to_stage9
  D:\winprojects\analyzer\src\decision\engine.py:260: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    calculation_timestamp = datetime.utcnow()

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
============================================ 1 passed, 4 warnings in 0.66s
(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_stage9_decision.py::test_jalali_orchestration_rejects_mismatched_fundamental_and_market_identity
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\winprojects\analyzer
collected 1 item

src\tests\test_stage9_decision.py .                                                                              [100%]

================================================== warnings summary ===================================================
src/tests/test_stage9_decision.py::test_jalali_orchestration_rejects_mismatched_fundamental_and_market_identity
src/tests/test_stage9_decision.py::test_jalali_orchestration_rejects_mismatched_fundamental_and_market_identity
  D:\winprojects\analyzer\src\tests\test_stage9_decision.py:20: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    calculation_timestamp=datetime.utcnow(),

src/tests/test_stage9_decision.py::test_jalali_orchestration_rejects_mismatched_fundamental_and_market_identity
src/tests/test_stage9_decision.py::test_jalali_orchestration_rejects_mismatched_fundamental_and_market_identity
  D:\winprojects\analyzer\src\tests\test_stage9_decision.py:49: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    as_of_date=datetime.utcnow(),

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
============================================ 1 passed, 4 warnings in 0.65s
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
============================================ 1 passed, 1 warning in 0.68s
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
============================================ 1 passed, 1 warning in 0.63s
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
============================================ 1 passed, 1 warning in 0.64s
(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_ingestion_ohlc.py::test_market_price_as_of_selects_exact_date_and_preserves_provenance
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\winprojects\analyzer
collected 1 item

src\tests\test_ingestion_ohlc.py .                                                                               [100%]

================================================== warnings summary ===================================================
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_selects_exact_date_and_preserves_provenance
  D:\winprojects\analyzer\src\migrations\runner.py:175: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    {"version": 1, "name": "legacy_baseline", "applied_at": datetime.utcnow()},

src/tests/test_ingestion_ohlc.py::test_market_price_as_of_selects_exact_date_and_preserves_provenance
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_selects_exact_date_and_preserves_provenance
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_selects_exact_date_and_preserves_provenance
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_selects_exact_date_and_preserves_provenance
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_selects_exact_date_and_preserves_provenance
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_selects_exact_date_and_preserves_provenance
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_selects_exact_date_and_preserves_provenance
  D:\winprojects\analyzer\Lib\site-packages\sqlalchemy\engine\default.py:952: DeprecationWarning: The default datetime adapter is deprecated as of Python 3.12; see the sqlite3 documentation for suggested replacement recipes
    cursor.execute(statement, parameters)

src/tests/test_ingestion_ohlc.py::test_market_price_as_of_selects_exact_date_and_preserves_provenance
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_selects_exact_date_and_preserves_provenance
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_selects_exact_date_and_preserves_provenance
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_selects_exact_date_and_preserves_provenance
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_selects_exact_date_and_preserves_provenance
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_selects_exact_date_and_preserves_provenance
  D:\winprojects\analyzer\src\migrations\runner.py:186: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    {"version": migration.version, "name": migration.name, "applied_at": datetime.utcnow()},

src/tests/test_ingestion_ohlc.py::test_market_price_as_of_selects_exact_date_and_preserves_provenance
  D:\winprojects\analyzer\Lib\site-packages\sqlalchemy\sql\schema.py:3627: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return util.wrap_callable(lambda ctx: fn(), fn)  # type: ignore

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================================== 1 passed, 15 warnings in 0.90s
(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_ingestion_ohlc.py::test_market_price_as_of_uses_latest_prior_date_across_year_boundary
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\winprojects\analyzer
collected 1 item

src\tests\test_ingestion_ohlc.py .                                                                               [100%]

================================================== warnings summary ===================================================
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_uses_latest_prior_date_across_year_boundary
  D:\winprojects\analyzer\src\migrations\runner.py:175: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    {"version": 1, "name": "legacy_baseline", "applied_at": datetime.utcnow()},

src/tests/test_ingestion_ohlc.py::test_market_price_as_of_uses_latest_prior_date_across_year_boundary
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_uses_latest_prior_date_across_year_boundary
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_uses_latest_prior_date_across_year_boundary
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_uses_latest_prior_date_across_year_boundary
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_uses_latest_prior_date_across_year_boundary
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_uses_latest_prior_date_across_year_boundary
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_uses_latest_prior_date_across_year_boundary
  D:\winprojects\analyzer\Lib\site-packages\sqlalchemy\engine\default.py:952: DeprecationWarning: The default datetime adapter is deprecated as of Python 3.12; see the sqlite3 documentation for suggested replacement recipes
    cursor.execute(statement, parameters)

src/tests/test_ingestion_ohlc.py::test_market_price_as_of_uses_latest_prior_date_across_year_boundary
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_uses_latest_prior_date_across_year_boundary
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_uses_latest_prior_date_across_year_boundary
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_uses_latest_prior_date_across_year_boundary
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_uses_latest_prior_date_across_year_boundary
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_uses_latest_prior_date_across_year_boundary
  D:\winprojects\analyzer\src\migrations\runner.py:186: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    {"version": migration.version, "name": migration.name, "applied_at": datetime.utcnow()},

src/tests/test_ingestion_ohlc.py::test_market_price_as_of_uses_latest_prior_date_across_year_boundary
  D:\winprojects\analyzer\Lib\site-packages\sqlalchemy\sql\schema.py:3627: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return util.wrap_callable(lambda ctx: fn(), fn)  # type: ignore

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================================== 1 passed, 15 warnings in 0.58s
(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_ingestion_ohlc.py::test_market_price_as_of_returns_none_when_no_eligible_price
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\winprojects\analyzer
collected 1 item

src\tests\test_ingestion_ohlc.py .                                                                               [100%]

================================================== warnings summary ===================================================
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_returns_none_when_no_eligible_price
  D:\winprojects\analyzer\src\migrations\runner.py:175: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    {"version": 1, "name": "legacy_baseline", "applied_at": datetime.utcnow()},

src/tests/test_ingestion_ohlc.py::test_market_price_as_of_returns_none_when_no_eligible_price
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_returns_none_when_no_eligible_price
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_returns_none_when_no_eligible_price
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_returns_none_when_no_eligible_price
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_returns_none_when_no_eligible_price
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_returns_none_when_no_eligible_price
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_returns_none_when_no_eligible_price
  D:\winprojects\analyzer\Lib\site-packages\sqlalchemy\engine\default.py:952: DeprecationWarning: The default datetime adapter is deprecated as of Python 3.12; see the sqlite3 documentation for suggested replacement recipes
    cursor.execute(statement, parameters)

src/tests/test_ingestion_ohlc.py::test_market_price_as_of_returns_none_when_no_eligible_price
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_returns_none_when_no_eligible_price
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_returns_none_when_no_eligible_price
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_returns_none_when_no_eligible_price
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_returns_none_when_no_eligible_price
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_returns_none_when_no_eligible_price
  D:\winprojects\analyzer\src\migrations\runner.py:186: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    {"version": migration.version, "name": migration.name, "applied_at": datetime.utcnow()},

src/tests/test_ingestion_ohlc.py::test_market_price_as_of_returns_none_when_no_eligible_price
  D:\winprojects\analyzer\Lib\site-packages\sqlalchemy\sql\schema.py:3627: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return util.wrap_callable(lambda ctx: fn(), fn)  # type: ignore

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================================== 1 passed, 15 warnings in 0.60s
(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_ingestion_ohlc.py::test_market_price_as_of_rejects_duplicate_latest_jalali_observations
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\winprojects\analyzer
collected 1 item

src\tests\test_ingestion_ohlc.py .                                                                               [100%]

================================================== warnings summary ===================================================
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_rejects_duplicate_latest_jalali_observations
  D:\winprojects\analyzer\src\migrations\runner.py:175: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    {"version": 1, "name": "legacy_baseline", "applied_at": datetime.utcnow()},

src/tests/test_ingestion_ohlc.py::test_market_price_as_of_rejects_duplicate_latest_jalali_observations
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_rejects_duplicate_latest_jalali_observations
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_rejects_duplicate_latest_jalali_observations
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_rejects_duplicate_latest_jalali_observations
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_rejects_duplicate_latest_jalali_observations
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_rejects_duplicate_latest_jalali_observations
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_rejects_duplicate_latest_jalali_observations
  D:\winprojects\analyzer\Lib\site-packages\sqlalchemy\engine\default.py:952: DeprecationWarning: The default datetime adapter is deprecated as of Python 3.12; see the sqlite3 documentation for suggested replacement recipes
    cursor.execute(statement, parameters)

src/tests/test_ingestion_ohlc.py::test_market_price_as_of_rejects_duplicate_latest_jalali_observations
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_rejects_duplicate_latest_jalali_observations
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_rejects_duplicate_latest_jalali_observations
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_rejects_duplicate_latest_jalali_observations
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_rejects_duplicate_latest_jalali_observations
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_rejects_duplicate_latest_jalali_observations
  D:\winprojects\analyzer\src\migrations\runner.py:186: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    {"version": migration.version, "name": migration.name, "applied_at": datetime.utcnow()},

src/tests/test_ingestion_ohlc.py::test_market_price_as_of_rejects_duplicate_latest_jalali_observations
  D:\winprojects\analyzer\Lib\site-packages\sqlalchemy\sql\schema.py:3627: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return util.wrap_callable(lambda ctx: fn(), fn)  # type: ignore

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================================== 1 passed, 15 warnings in 0.59s