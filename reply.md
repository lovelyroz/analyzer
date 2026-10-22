(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_stage9_decision.py::test_jalali_orchestration_passes_stage7_result_to_stage9
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\winprojects\analyzer
collected 1 item

src\tests\test_stage9_decision.py F                                                                              [100%]

====================================================== FAILURES =======================================================
______________________________ test_jalali_orchestration_passes_stage7_result_to_stage9 _______________________________

monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x00000186E1412D20>

    def test_jalali_orchestration_passes_stage7_result_to_stage9(monkeypatch):
        valuation = make_valuation()
        monkeypatch.setattr(
            decision_service,
            "calculate_valuation_as_of_jalali",
            lambda *args, **kwargs: valuation,
        )
        original_make_decision = DecisionEngine.make_decision
        received = {}

        def capture_valuation(self, company_id, period_id, fundamental, valuation_result, market, reliability=None, **kwargs):
            received["valuation"] = valuation_result
            return original_make_decision(
                self, company_id, period_id, fundamental, valuation_result, market, reliability, **kwargs
            )

        monkeypatch.setattr(DecisionEngine, "make_decision", capture_valuation)
        forecast = SimpleNamespace(company_id=1, forecast_period_id=10)

        result = decision_service.calculate_decision_as_of_jalali(
            session=None,
            forecast_result=forecast,
            as_of_jalali_date=(1405, 2, 11),
            fundamental_result=make_fundamental(85),
            market_result=make_market(),
        )

        assert result.valuation is valuation
        assert received["valuation"] is valuation
        assert result.decision.valuation_status == valuation.valuation_status
>       assert result.metadata["market_score_used"] is False
               ^^^^^^^^^^^^^^^
E       AttributeError: 'ValuationDecisionResult' object has no attribute 'metadata'

src\tests\test_stage9_decision.py:97: AttributeError
================================================== warnings summary ===================================================
src/tests/test_stage9_decision.py::test_jalali_orchestration_passes_stage7_result_to_stage9
  D:\winprojects\analyzer\src\tests\test_stage9_decision.py:37: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    calculation_timestamp=datetime.utcnow(),

src/tests/test_stage9_decision.py::test_jalali_orchestration_passes_stage7_result_to_stage9
  D:\winprojects\analyzer\src\tests\test_stage9_decision.py:18: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    calculation_timestamp=datetime.utcnow(),

src/tests/test_stage9_decision.py::test_jalali_orchestration_passes_stage7_result_to_stage9
  D:\winprojects\analyzer\src\tests\test_stage9_decision.py:47: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    as_of_date=datetime.utcnow(),

src/tests/test_stage9_decision.py::test_jalali_orchestration_passes_stage7_result_to_stage9
  D:\winprojects\analyzer\src\decision\engine.py:260: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    calculation_timestamp = datetime.utcnow()

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=============================================== short test summary info ===============================================
FAILED src/tests/test_stage9_decision.py::test_jalali_orchestration_passes_stage7_result_to_stage9 - AttributeError: 'ValuationDecisionResult' object has no attribute 'metadata'
============================================ 1 failed, 4 warnings in 1.33s
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
============================================ 1 passed, 1 warning in 0.66s
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
=========================================== 1 passed, 15 warnings in 0.91s
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
(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_ingestion_ohlc.py::test_market_price_as_of_isolates_company_and_ignores_undated_rows
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\winprojects\analyzer
collected 1 item

src\tests\test_ingestion_ohlc.py .                                                                               [100%]

================================================== warnings summary ===================================================
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_isolates_company_and_ignores_undated_rows
  D:\winprojects\analyzer\src\migrations\runner.py:175: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    {"version": 1, "name": "legacy_baseline", "applied_at": datetime.utcnow()},

src/tests/test_ingestion_ohlc.py::test_market_price_as_of_isolates_company_and_ignores_undated_rows
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_isolates_company_and_ignores_undated_rows
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_isolates_company_and_ignores_undated_rows
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_isolates_company_and_ignores_undated_rows
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_isolates_company_and_ignores_undated_rows
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_isolates_company_and_ignores_undated_rows
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_isolates_company_and_ignores_undated_rows
  D:\winprojects\analyzer\Lib\site-packages\sqlalchemy\engine\default.py:952: DeprecationWarning: The default datetime adapter is deprecated as of Python 3.12; see the sqlite3 documentation for suggested replacement recipes
    cursor.execute(statement, parameters)

src/tests/test_ingestion_ohlc.py::test_market_price_as_of_isolates_company_and_ignores_undated_rows
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_isolates_company_and_ignores_undated_rows
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_isolates_company_and_ignores_undated_rows
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_isolates_company_and_ignores_undated_rows
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_isolates_company_and_ignores_undated_rows
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_isolates_company_and_ignores_undated_rows
  D:\winprojects\analyzer\src\migrations\runner.py:186: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    {"version": migration.version, "name": migration.name, "applied_at": datetime.utcnow()},

src/tests/test_ingestion_ohlc.py::test_market_price_as_of_isolates_company_and_ignores_undated_rows
src/tests/test_ingestion_ohlc.py::test_market_price_as_of_isolates_company_and_ignores_undated_rows
  D:\winprojects\analyzer\Lib\site-packages\sqlalchemy\sql\schema.py:3627: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    return util.wrap_callable(lambda ctx: fn(), fn)  # type: ignore

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=========================================== 1 passed, 16 warnings in 0.59s
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
=========================================== 1 passed, 15 warnings in 0.58s
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
(analyzer) PS D:\winprojects\analyzer> pytest src/tests/test_stage9_decision.py
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0
rootdir: D:\winprojects\analyzer
collected 14 items

src\tests\test_stage9_decision.py .F............                                                                 [100%]

====================================================== FAILURES =======================================================
______________________________ test_jalali_orchestration_passes_stage7_result_to_stage9 _______________________________

monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x00000246B1462ED0>

    def test_jalali_orchestration_passes_stage7_result_to_stage9(monkeypatch):
        valuation = make_valuation()
        monkeypatch.setattr(
            decision_service,
            "calculate_valuation_as_of_jalali",
            lambda *args, **kwargs: valuation,
        )
        original_make_decision = DecisionEngine.make_decision
        received = {}

        def capture_valuation(self, company_id, period_id, fundamental, valuation_result, market, reliability=None, **kwargs):
            received["valuation"] = valuation_result
            return original_make_decision(
                self, company_id, period_id, fundamental, valuation_result, market, reliability, **kwargs
            )

        monkeypatch.setattr(DecisionEngine, "make_decision", capture_valuation)
        forecast = SimpleNamespace(company_id=1, forecast_period_id=10)

        result = decision_service.calculate_decision_as_of_jalali(
            session=None,
            forecast_result=forecast,
            as_of_jalali_date=(1405, 2, 11),
            fundamental_result=make_fundamental(85),
            market_result=make_market(),
        )

        assert result.valuation is valuation
        assert received["valuation"] is valuation
        assert result.decision.valuation_status == valuation.valuation_status
>       assert result.metadata["market_score_used"] is False
               ^^^^^^^^^^^^^^^
E       AttributeError: 'ValuationDecisionResult' object has no attribute 'metadata'

src\tests\test_stage9_decision.py:97: AttributeError
================================================== warnings summary ===================================================
src/tests/test_stage9_decision.py: 14 warnings
  D:\winprojects\analyzer\src\tests\test_stage9_decision.py:18: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    calculation_timestamp=datetime.utcnow(),

src/tests/test_stage9_decision.py: 14 warnings
  D:\winprojects\analyzer\src\tests\test_stage9_decision.py:37: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    calculation_timestamp=datetime.utcnow(),

src/tests/test_stage9_decision.py: 14 warnings
  D:\winprojects\analyzer\src\tests\test_stage9_decision.py:47: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    as_of_date=datetime.utcnow(),

src/tests/test_stage9_decision.py: 14 warnings
  D:\winprojects\analyzer\src\decision\engine.py:260: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
    calculation_timestamp = datetime.utcnow()

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
=============================================== short test summary info ===============================================
FAILED src/tests/test_stage9_decision.py::test_jalali_orchestration_passes_stage7_result_to_stage9 - AttributeError: 'ValuationDecisionResult' object has no attribute 'metadata'
====================================== 1 failed, 13 passed, 56 warnings