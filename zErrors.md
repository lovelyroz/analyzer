(analyzer) PS D:\winprojects\analyzer> python -m pytest src/tests/test_stage7_valuation.py -q                           .F......                                                                                                         [100%]
====================================================== FAILURES =======================================================
______________________________ test_valuation_engine_forward_pe_and_expected_fair_value _______________________________

    def test_valuation_engine_forward_pe_and_expected_fair_value():
>       result = ValuationEngine().calculate_valuation(
            company_id=1,
            period_id=101,
            industry_code="PETROCHEMICAL",
            current_price=1000.0,
            forecast_result=make_forecast(),
            forecast_reliability_score=85.0,
            historical_pe_values=[6.5, 7.0, 8.0],
            probability_confidence=90.0,
        )

src\tests\test_stage7_valuation.py:42:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\valuation\engine.py:74: in calculate_valuation
    selected_version, selection_meta = select_parameter_set_for_valuation(
src\valuation\parameters.py:366: in select_parameter_set_for_valuation
    version = resolve_parameter_set_as_of(governing_timestamp, registry)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

as_of = datetime.datetime(2026, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)
registry = ParameterRegistry(versions=(ParameterSetVersion(model_version='STAGE7_V1', version_key='STAGE7_V1/GENESIS', effective_...unused in V1. Genesis record: temporal validity unknown; never valid for historical date selection (R8 pending).'))),))

    def resolve_parameter_set_as_of(
        as_of: Optional[datetime],
        registry: ParameterRegistry = DEFAULT_REGISTRY,
    ) -> ParameterSetVersion:
        if as_of is None:
            raise LookupError(
                "Stage 7 parameter as-of selection requires an as-of instant; "
                "refusing to guess one."
            )
        moment = normalize_datetime(as_of)
        candidates = [
            version for version in registry.versions
            if version.effective_from is not None and normalize_datetime(version.effective_from) <= moment
        ]
        if not candidates:
>           raise LookupError(
                f"No dated Stage 7 parameter version covers as_of={moment.isoformat()}; "
                "historical selection requires R8-dated records (genesis is undated "
                "and never stands in for history)."
            )
E           LookupError: No dated Stage 7 parameter version covers as_of=2026-01-01T00:00:00+00:00; historical selection requires R8-dated records (genesis is undated and never stands in for history).

src\valuation\parameters.py:192: LookupError
=============================================== short test summary info ===============================================
FAILED src/tests/test_stage7_valuation.py::test_valuation_engine_forward_pe_and_expected_fair_value - LookupError: No dated Stage 7 parameter version covers as_of=2026-01-01T00:00:00+00:00; historical selection requir...
1 failed, 7 passed in 1.23s
(analyzer) PS D:\winprojects\analyzer> python -m pytest src/tests/test_stage7_valuation.py src/tests/test_stage9_decision.py -q
.F.....................                                                                                          [100%]
====================================================== FAILURES =======================================================
______________________________ test_valuation_engine_forward_pe_and_expected_fair_value _______________________________

    def test_valuation_engine_forward_pe_and_expected_fair_value():
>       result = ValuationEngine().calculate_valuation(
            company_id=1,
            period_id=101,
            industry_code="PETROCHEMICAL",
            current_price=1000.0,
            forecast_result=make_forecast(),
            forecast_reliability_score=85.0,
            historical_pe_values=[6.5, 7.0, 8.0],
            probability_confidence=90.0,
        )

src\tests\test_stage7_valuation.py:42:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\valuation\engine.py:74: in calculate_valuation
    selected_version, selection_meta = select_parameter_set_for_valuation(
src\valuation\parameters.py:366: in select_parameter_set_for_valuation
    version = resolve_parameter_set_as_of(governing_timestamp, registry)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

as_of = datetime.datetime(2026, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)
registry = ParameterRegistry(versions=(ParameterSetVersion(model_version='STAGE7_V1', version_key='STAGE7_V1/GENESIS', effective_...unused in V1. Genesis record: temporal validity unknown; never valid for historical date selection (R8 pending).'))),))

    def resolve_parameter_set_as_of(
        as_of: Optional[datetime],
        registry: ParameterRegistry = DEFAULT_REGISTRY,
    ) -> ParameterSetVersion:
        if as_of is None:
            raise LookupError(
                "Stage 7 parameter as-of selection requires an as-of instant; "
                "refusing to guess one."
            )
        moment = normalize_datetime(as_of)
        candidates = [
            version for version in registry.versions
            if version.effective_from is not None and normalize_datetime(version.effective_from) <= moment
        ]
        if not candidates:
>           raise LookupError(
                f"No dated Stage 7 parameter version covers as_of={moment.isoformat()}; "
                "historical selection requires R8-dated records (genesis is undated "
                "and never stands in for history)."
            )
E           LookupError: No dated Stage 7 parameter version covers as_of=2026-01-01T00:00:00+00:00; historical selection requires R8-dated records (genesis is undated and never stands in for history).

src\valuation\parameters.py:192: LookupError
=============================================== short test summary info ===============================================
FAILED src/tests/test_stage7_valuation.py::test_valuation_engine_forward_pe_and_expected_fair_value - LookupError: No dated Stage 7 parameter version covers as_of=2026-01-01T00:00:00+00:00; historical selection requir...
1 failed, 22 passed in 1.13s