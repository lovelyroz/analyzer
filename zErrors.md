(analyzer) PS D:\Winprojects\analyzer> .\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_db_impl_002_bridge_20261122 src/tests/test_canonical_stage5_adapter.py src/tests/test_canonical_stage6_adapter.py src/tests/test_canonical_queries.py src/tests/test_canonical_writer.py src/tests/test_stage5_forecast.py src/tests/test_stage2_kpis.py
F....F.F...F......F............................................................................................. [ 30%]
................................................................................................................ [ 60%]
................................................................................................................ [ 91%]
.................................                                                                                [100%]
====================================================== FAILURES =======================================================
__________________________ test_stage5_ytd_is_adapted_to_exact_runtime_quarters_with_lineage __________________________

    def test_stage5_ytd_is_adapted_to_exact_runtime_quarters_with_lineage():
        bindings = _bindings()
        facts = []
        for key in ("REVENUE", "OPERATING_PROFIT", "NET_PROFIT"):
            metric_id = bindings[key].metric_id
            facts.extend([
                _fact(metric_id, key, 3, 100, metric_id * 10 + 1),
>               _fact(metric_id, key, 6, 250, metric_id * 10 + 2),
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            ])

src\tests\test_canonical_stage5_adapter.py:52:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

metric_id = 3, key = 'NET_PROFIT', end_month = 6, value = 250, version = 32, temporal = 'DURATION', start_month = 1
report_type = 'PERIODIC_FINANCIAL', unit = None, dimensions = ()

    def _fact(metric_id, key, end_month, value, version, *, temporal=None, start_month=1,
              report_type="PERIODIC_FINANCIAL", unit=None, dimensions=()):
        temporal = temporal or ("INSTANT" if key == "TOTAL_EQUITY" else "DURATION")
        return CanonicalFactAtCutoff(
            company_id=1, report_type_id=report_type, metric_id=metric_id,
            period_id=metric_id * 100 + end_month, temporal_type=temporal,
            start_jalali=(1404, end_month, 31 if end_month <= 6 else 30) if temporal == "INSTANT" else (1404, start_month, 1),
            end_jalali=(1404, end_month, 31 if end_month <= 6 else 30),
            duration_basis=None if temporal == "INSTANT" else "YTD",
            value_integer=value, value_state="REPORTED_VALUE", scenario="ACTUAL",
            source_unit=unit or "unit-rial", source_currency="currency-irr",
            source_scale="scale-unit", report_version_id=version,
>           publication_datetime=datetime(2025, 1, version), is_audited=True,
                                 ^^^^^^^^^^^^^^^^^^^^^^^^^^
            is_restated=False, dimensions=dimensions, source_identity="source",
            revision_identity=str(version), source_coordinate="B2",
        )
E       ValueError: day is out of range for month

src\tests\test_canonical_stage5_adapter.py:39: ValueError
________________ test_stage5_keeps_latest_reported_null_period_missing_instead_of_using_older_quarter _________________

    def test_stage5_keeps_latest_reported_null_period_missing_instead_of_using_older_quarter():
        bindings = _bindings()
        missing_q2 = replace(
            _fact(1, "REVENUE", 6, None, 2), value_state="REPORTED_NULL",
        )
        adapted = build_stage5_input(
            [_fact(1, "REVENUE", 3, 100, 1), missing_q2],
            bindings, company_id=1, fiscal_year_start_month=1,
        )
>       assert adapted.periods[-1][1] == (1404, 6, 30)
E       assert (1404, 6, 31) == (1404, 6, 30)
E
E         At index 2 diff: 31 != 30
E         Use -v to get more diff

src\tests\test_canonical_stage5_adapter.py:132: AssertionError
____________________________ test_stage5_rejects_inconsistent_units_and_ytd_period_starts _____________________________

    def test_stage5_rejects_inconsistent_units_and_ytd_period_starts():
        bindings = _bindings()
        bindings["NET_PROFIT"] = CanonicalMetricBinding(
            "NET_PROFIT", 3, "DURATION", "unit-thousand-rial", "currency-irr",
            "scale-unit", duration_basis="YTD", duration_aggregation="ADDITIVE_YTD",
        )
        with pytest.raises(CanonicalReadError, match="CANONICAL_STAGE5_UNIT_CONTRACT_INCONSISTENT"):
            build_stage5_input([], bindings, company_id=1, fiscal_year_start_month=1)

        bindings = _bindings()
        facts = [
            _fact(1, "REVENUE", 3, 100, 1),
            _fact(2, "OPERATING_PROFIT", 3, 20, 2, start_month=2),
        ]
>       with pytest.raises(CanonicalReadError, match="CANONICAL_STAGE5_PERIOD_MISMATCH"):
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       AssertionError: Regex pattern did not match.
E         Expected regex: 'CANONICAL_STAGE5_PERIOD_MISMATCH'
E         Actual message: 'CANONICAL_STAGE5_YTD_PERIOD_INVALID'

src\tests\test_canonical_stage5_adapter.py:159: AssertionError
____________________ test_stage6_maps_explicit_bank_inputs_and_preserves_missing_zero_and_lineage _____________________

    def test_stage6_maps_explicit_bank_inputs_and_preserves_missing_zero_and_lineage():
        bindings = _bindings()
        selected = [
            _fact(bindings["revenue_curr"], 250, 1),
            _fact(bindings["revenue_prev"], 100, 2, end=(1404, 3, 31)),
            _fact(bindings["nii"], 0, 3, state="ZERO_FALLBACK"),
        ]

>       adapted = build_stage6_input(
            selected, bindings, company_id=7, period_id=22, period_end_jalali=(1404, 6, 30), fiscal_year_start_month=1
        )

src\tests\test_canonical_stage6_adapter.py:65:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\kpi\canonical_adapter.py:133: in build_stage6_input
    validate_periodic_ytd_identity(fact, fiscal_year_start_month)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

fact = CanonicalFactAtCutoff(company_id=7, report_type_id='PERIODIC_FINANCIAL', metric_id=10, period_id=103, temporal_type='D...udited=True, is_restated=False, dimensions=(), source_identity='source', revision_identity='3', source_coordinate='C5')
fiscal_year_start_month = 1

    def validate_periodic_ytd_identity(
        fact: CanonicalFactAtCutoff,
        fiscal_year_start_month: int,
    ) -> None:
        start, end = fact.start_jalali, fact.end_jalali
        months = (end[0] - start[0]) * 12 + end[1] - start[1] + 1
        if (start[2] != 1 or start[1] != fiscal_year_start_month
                or not is_valid_jalali_components(*start)
                or not _is_jalali_month_end(end)
                or months not in {3, 6, 9, 12}):
>           raise CanonicalReadError("CANONICAL_STAGE5_YTD_PERIOD_INVALID")
E           src.forecast.canonical_adapter.CanonicalReadError: CANONICAL_STAGE5_YTD_PERIOD_INVALID

src\forecast\canonical_adapter.py:239: CanonicalReadError
________________________ test_stage6_opt_in_loader_is_bank_only_and_queries_periodic_pit_facts ________________________

monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x000001E1D5A47050>

    def test_stage6_opt_in_loader_is_bank_only_and_queries_periodic_pit_facts(monkeypatch):
        from src.kpi import canonical_adapter

        bindings = _bindings()
        facts = [
            _fact(bindings["revenue_curr"], 250, 1),
            _fact(bindings["revenue_prev"], 100, 2, end=(1404, 3, 31)),
        ]
        seen = {}
        monkeypatch.setattr(canonical_adapter, "load_industry_code", lambda *_: "BANK")
        monkeypatch.setattr(canonical_adapter, "validate_active_bank_metric_bindings", lambda *_: None)
        monkeypatch.setattr(canonical_adapter, "load_approved_bank_fiscal_start_month", lambda *_: 1)

        def read(_session, company_id, **kwargs):
            seen["company_id"] = company_id
            seen.update(kwargs)
            return facts

        monkeypatch.setattr(canonical_adapter, "load_canonical_financial_facts", read)
>       results, adapted = calculate_stage6_kpis_from_canonical(
            object(), 7, period_id=22, period_end_jalali=(1404, 6, 30),
            cutoff=datetime(2025, 8, 1), bindings=bindings,
        )

src\tests\test_canonical_stage6_adapter.py:228:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\kpi\canonical_adapter.py:196: in calculate_stage6_kpis_from_canonical
    adapted = build_stage6_input(
src\kpi\canonical_adapter.py:133: in build_stage6_input
    validate_periodic_ytd_identity(fact, fiscal_year_start_month)
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

fact = CanonicalFactAtCutoff(company_id=7, report_type_id='PERIODIC_FINANCIAL', metric_id=15, period_id=101, temporal_type='D...udited=True, is_restated=False, dimensions=(), source_identity='source', revision_identity='1', source_coordinate='C5')
fiscal_year_start_month = 1

    def validate_periodic_ytd_identity(
        fact: CanonicalFactAtCutoff,
        fiscal_year_start_month: int,
    ) -> None:
        start, end = fact.start_jalali, fact.end_jalali
        months = (end[0] - start[0]) * 12 + end[1] - start[1] + 1
        if (start[2] != 1 or start[1] != fiscal_year_start_month
                or not is_valid_jalali_components(*start)
                or not _is_jalali_month_end(end)
                or months not in {3, 6, 9, 12}):
>           raise CanonicalReadError("CANONICAL_STAGE5_YTD_PERIOD_INVALID")
E           src.forecast.canonical_adapter.CanonicalReadError: CANONICAL_STAGE5_YTD_PERIOD_INVALID

src\forecast\canonical_adapter.py:239: CanonicalReadError
=============================================== short test summary info ===============================================
FAILED src/tests/test_canonical_stage5_adapter.py::test_stage5_ytd_is_adapted_to_exact_runtime_quarters_with_lineage - ValueError: day is out of range for month
FAILED src/tests/test_canonical_stage5_adapter.py::test_stage5_keeps_latest_reported_null_period_missing_instead_of_using_older_quarter - assert (1404, 6, 31) == (1404, 6, 30)
FAILED src/tests/test_canonical_stage5_adapter.py::test_stage5_rejects_inconsistent_units_and_ytd_period_starts - AssertionError: Regex pattern did not match.
FAILED src/tests/test_canonical_stage6_adapter.py::test_stage6_maps_explicit_bank_inputs_and_preserves_missing_zero_and_lineage - src.forecast.canonical_adapter.CanonicalReadError: CANONICAL_STAGE5_YTD_PERIOD_INVALID
FAILED src/tests/test_canonical_stage6_adapter.py::test_stage6_opt_in_loader_is_bank_only_and_queries_periodic_pit_facts - src.forecast.canonical_adapter.CanonicalReadError: CANONICAL_STAGE5_YTD_PERIOD_INVALID
5 failed, 364 passed in 385.00s (0:06:24)