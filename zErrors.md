(analyzer) PS D:\Winprojects\analyzer>
>> .\.venv\Scripts\python.exe -m pytest -q --basetemp .pytest_task018_20261121 src/tests/test_excel_adapter.py src/tests/test_excel_canonical_input.py src/tests/test_canonical_ingestion_admission.py src/tests/test_codal_extraction.py src/tests/test_codal_pdf_extraction.py src/tests/test_market_fx_atomic_ingestion.py src/tests/test_stage6_p25_selection.py src/tests/test_stage6_p25_adversarial.py src/tests/test_stage6_evaluation_foundation.py
>>
........................................................sF...................................................... [ 41%]
........................................................................................................FFFFFFFF [ 83%]
FFFFFFFFFFFFFFFFFFFFFFF...FFFFFFFFFF......F                                                                      [100%]
====================================================== FAILURES =======================================================
__________________________ test_codal_validation_corpus_inventory_is_exactly_locked_19_pdfs ___________________________

    def test_codal_validation_corpus_inventory_is_exactly_locked_19_pdfs():
        """SCOPE gate: validation corpus must be exactly the locked 19-PDF set."""
        assert PDF_ROOT.is_dir(), f"SCOPE_ERROR: PDF root missing: {PDF_ROOT}"
        present = {path.name for path in PDF_ROOT.glob("*.pdf")}
        missing = LOCKED_CODAL_VALIDATION_CORPUS - present
        unexpected = present - LOCKED_CODAL_VALIDATION_CORPUS
>       assert not missing and not unexpected and len(present) == 19, (
            "SCOPE_ERROR: CODAL validation corpus drifted from the locked 19-PDF set. "
            f"expected_count=19 actual_count={len(present)} "
            f"missing={sorted(missing)} unexpected={sorted(unexpected)}"
        )
E       AssertionError: SCOPE_ERROR: CODAL validation corpus drifted from the locked 19-PDF set. expected_count=19 actual_count=20 missing=[] unexpected=['Fzar.pdf']
E       assert (not frozenset() and not {'Fzar.pdf'})

src\tests\test_codal_pdf_extraction.py:60: AssertionError
_______________________________________ test_key_is_7_tuple_with_scenario_last ________________________________________

    def test_key_is_7_tuple_with_scenario_last():
>       key = evaluation_key_for(_record(), "REVENUE")
                                 ^^^^^^^^^

src\tests\test_stage6_p25_selection.py:196:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_p25_selection.py:64: TypeError
_______________________________________ test_key_scenario_distinct_keys_differ ________________________________________

    def test_key_scenario_distinct_keys_differ():
        assert (
>           evaluation_key_for(_record(scenario="BASE"), "REVENUE").as_tuple()
                               ^^^^^^^^^^^^^^^^^^^^^^^^
            != evaluation_key_for(_record(scenario="BULL"), "REVENUE").as_tuple()
        )

src\tests\test_stage6_p25_selection.py:204:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'scenario': 'BASE'}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_p25_selection.py:64: TypeError
______________________________________ test_key_forecast_id_does_not_affect_key _______________________________________

    def test_key_forecast_id_does_not_affect_key():
        assert (
>           evaluation_key_for(_record(forecast_id=1), "REVENUE").as_tuple()
                               ^^^^^^^^^^^^^^^^^^^^^^
            == evaluation_key_for(_record(forecast_id=999), "REVENUE").as_tuple()
        )

src\tests\test_stage6_p25_selection.py:211:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_id': 1}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_p25_selection.py:64: TypeError
________________________________ test_build_observation_invalid_report_version_status _________________________________

    def test_build_observation_invalid_report_version_status():
        observation = build_observation(
>           _record(), "REVENUE", _actual(report_version_id=None)
            ^^^^^^^^^
        )

src\tests\test_stage6_p25_selection.py:221:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_p25_selection.py:64: TypeError
___________________________________ test_p25_01_multi_rv_earliest_publication_wins ____________________________________

    def test_p25_01_multi_rv_earliest_publication_wins():
>       record = _record(revenue=1000.0)
                 ^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage6_p25_adversarial.py:85:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'revenue': 1000.0}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_p25_adversarial.py:51: TypeError
_______________________________________ test_p25_02_same_publication_tie_break ________________________________________

    def test_p25_02_same_publication_tie_break():
>       record = _record(revenue=1000.0)
                 ^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage6_p25_adversarial.py:103:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'revenue': 1000.0}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_p25_adversarial.py:51: TypeError
_____________________________ test_p25_03_restated_later_publication_loses_to_first_known _____________________________

    def test_p25_03_restated_later_publication_loses_to_first_known():
        # A RESTATED Actual published later is hindsight, not the outcome:
        # first-known-outcome names the EARLY original as the winner.
>       record = _record(revenue=1000.0)
                 ^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage6_p25_adversarial.py:130:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'revenue': 1000.0}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_p25_adversarial.py:51: TypeError
___________________________________ test_p25_04_invalid_report_version_never_scores ___________________________________

    def test_p25_04_invalid_report_version_never_scores():
>       record = _record()
                 ^^^^^^^^^

src\tests\test_stage6_p25_adversarial.py:144:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_p25_adversarial.py:51: TypeError
____________________________________ test_p25_05_missing_actual_value_quarantines _____________________________________

    def test_p25_05_missing_actual_value_quarantines():
>       record = _record()
                 ^^^^^^^^^

src\tests\test_stage6_p25_adversarial.py:162:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_p25_adversarial.py:51: TypeError
__________________________________ test_p25_06_estimated_scores_with_limited_quality __________________________________

    def test_p25_06_estimated_scores_with_limited_quality():
>       record = _record()
                 ^^^^^^^^^

src\tests\test_stage6_p25_adversarial.py:173:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_p25_adversarial.py:51: TypeError
_____________________________________ test_p25_07_suspicious_quarantines_verbatim _____________________________________

    def test_p25_07_suspicious_quarantines_verbatim():
>       record = _record()
                 ^^^^^^^^^

src\tests\test_stage6_p25_adversarial.py:186:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_p25_adversarial.py:51: TypeError
______________________________________ test_p25_08_unmapped_quarantines_verbatim ______________________________________

    def test_p25_08_unmapped_quarantines_verbatim():
>       record = _record()
                 ^^^^^^^^^

src\tests\test_stage6_p25_adversarial.py:198:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_p25_adversarial.py:51: TypeError
___________________________________ test_p25_09_conflicting_duplicates_fail_closed ____________________________________

    def test_p25_09_conflicting_duplicates_fail_closed():
>       first = _record(forecast_id=1, forecast_period_id=101)
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage6_p25_adversarial.py:210:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_id': 1, 'forecast_period_id': 101}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_p25_adversarial.py:51: TypeError
________________________________ test_p25_10_dup_key_across_horizons_does_not_collide _________________________________

    def test_p25_10_dup_key_across_horizons_does_not_collide():
>       one = _record(forecast_period_id=101, forecast_horizon="12M")
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage6_p25_adversarial.py:223:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_period_id': 101, 'forecast_horizon': '12M'}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_p25_adversarial.py:51: TypeError
________________________________ test_p25_11_dup_key_across_versions_does_not_collide _________________________________

    def test_p25_11_dup_key_across_versions_does_not_collide():
>       one = _record(forecast_period_id=101, model_version="V1.0")
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage6_p25_adversarial.py:233:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_period_id': 101, 'model_version': 'V1.0'}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_p25_adversarial.py:51: TypeError
_________________________________ test_p25_12_dup_key_across_cutoffs_does_not_collide _________________________________

    def test_p25_12_dup_key_across_cutoffs_does_not_collide():
        # Stage 6 Prompt 38: distinct cutoffs never reach joint scoring — the
        # pipeline fails closed. The non-collision property itself is proved
        # at the flag_duplicates level (distinct 7-tuple identity keys).
        import pytest

        from src.evaluation.observation import flag_duplicates

>       one = _record(forecast_period_id=101)
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage6_p25_adversarial.py:250:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_period_id': 101}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_p25_adversarial.py:51: TypeError
__________________________________ test_p25_13_zero_actual_positive_forecast_scores ___________________________________

    def test_p25_13_zero_actual_positive_forecast_scores():
        # Stage 6 Prompt 38 (spec §9 D4-pointer + §12 D4): A=0/F=1000 stays
        # scored with absolute error retained and the Bias term eligible, but
        # is excluded from ordinary MAPE with the dedicated ACTUAL_ZERO code.
>       record = _record(revenue=1000.0)
                 ^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage6_p25_adversarial.py:272:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'revenue': 1000.0}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_p25_adversarial.py:51: TypeError
__________________________________ test_p25_14_zero_actual_negative_forecast_scores ___________________________________

    def test_p25_14_zero_actual_negative_forecast_scores():
        # Stage 6 Prompt 38 (§10 RB-2 (1)): A=0/F<0 stays Bias-eligible with
        # term exactly +100%, while MAPE-excluded with ACTUAL_ZERO.
>       record = _record(revenue=-500.0)
                 ^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage6_p25_adversarial.py:289:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'revenue': -500.0}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_p25_adversarial.py:51: TypeError
_______________________________________ test_p25_15_zero_over_zero_is_zero_base _______________________________________

    def test_p25_15_zero_over_zero_is_zero_base():
>       record = _record(revenue=0.0)
                 ^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage6_p25_adversarial.py:304:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'revenue': 0.0}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_p25_adversarial.py:51: TypeError
_______________________________________ test_p25_16_zero_forecast_is_zero_base ________________________________________

    def test_p25_16_zero_forecast_is_zero_base():
>       record = _record(revenue=0.0)
                 ^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage6_p25_adversarial.py:319:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'revenue': 0.0}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_p25_adversarial.py:51: TypeError
________________________________ test_p25_17_positive_forecast_zero_actual_regime_none ________________________________

    def test_p25_17_positive_forecast_zero_actual_regime_none():
        # classify_regime requires f*a < 0 for SIGN_CHANGE; here f*a = 0, so no
        # regime fires even though a naive sign reading sees "positive to zero".
>       record = _record(revenue=1000.0)
                 ^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage6_p25_adversarial.py:336:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'revenue': 1000.0}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_p25_adversarial.py:51: TypeError
___________________________________ test_p25_restated_series_flags_limited_quality ____________________________________

    def test_p25_restated_series_flags_limited_quality():
        observations = [
            build_observation(
>               _record(forecast_period_id=101 + i),
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                "REVENUE",
                _actual(financial_period_id=101 + i,
                        data_quality_state="RESTATED", restated=True),
            )
            for i in range(8)
        ]

src\tests\test_stage6_p25_adversarial.py:355:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_period_id': 101}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_p25_adversarial.py:51: TypeError
_____________________________________ test_identity_key_carries_full_mapping_key ______________________________________

    def test_identity_key_carries_full_mapping_key():
>       key = evaluation_key_for(_record(), "REVENUE")
                                 ^^^^^^^^^

src\tests\test_stage6_evaluation_foundation.py:92:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_evaluation_foundation.py:66: TypeError
____________________________________ test_identity_scenario_isolates_observations _____________________________________

    def test_identity_scenario_isolates_observations():
        assert (
>           evaluation_key_for(_record(scenario="BASE"), "REVENUE").as_tuple()
                               ^^^^^^^^^^^^^^^^^^^^^^^^
            != evaluation_key_for(_record(scenario="BULL"), "REVENUE").as_tuple()
        )

src\tests\test_stage6_evaluation_foundation.py:100:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'scenario': 'BASE'}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_evaluation_foundation.py:66: TypeError
___________________________________________ test_identity_differs_by_metric ___________________________________________

    def test_identity_differs_by_metric():
        assert (
>           evaluation_key_for(_record(), "REVENUE").as_tuple()
                               ^^^^^^^^^
            != evaluation_key_for(_record(), "NET_PROFIT").as_tuple()
        )

src\tests\test_stage6_evaluation_foundation.py:108:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_evaluation_foundation.py:66: TypeError
________________________________________ test_identity_stable_for_same_series _________________________________________

    def test_identity_stable_for_same_series():
        assert (
>           evaluation_key_for(_record(), "REVENUE").as_tuple()
                               ^^^^^^^^^
            == evaluation_key_for(_record(), "REVENUE").as_tuple()
        )

src\tests\test_stage6_evaluation_foundation.py:115:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_evaluation_foundation.py:66: TypeError
_______________________________________ test_later_published_actual_binds_ready _______________________________________

    def test_later_published_actual_binds_ready():
>       observation = build_observation(_record(), "REVENUE", _actual())
                                        ^^^^^^^^^

src\tests\test_stage6_evaluation_foundation.py:124:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_evaluation_foundation.py:66: TypeError
__________________________________________ test_historical_actual_also_binds __________________________________________

    def test_historical_actual_also_binds():
        observation = build_observation(
>           _record(), "REVENUE", _actual(publication_datetime=BEFORE)
            ^^^^^^^^^
        )

src\tests\test_stage6_evaluation_foundation.py:132:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_evaluation_foundation.py:66: TypeError
______________________________________ test_unbound_observation_waits_for_actual ______________________________________

    def test_unbound_observation_waits_for_actual():
>       observation = build_observation(_record(), "REVENUE")
                                        ^^^^^^^^^

src\tests\test_stage6_evaluation_foundation.py:138:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_evaluation_foundation.py:66: TypeError
________________________________________ test_leaked_input_freezes_observation ________________________________________

    def test_leaked_input_freezes_observation():
>       record = _record(input_refs=(_ref(at=AFTER),))
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage6_evaluation_foundation.py:147:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'input_refs': (ForecastInputRef(fact_key='REVENUE', report_version_id=9, available_at=datetime.datetime(2024, 9, 30, 0, 0, tzinfo=datetime.timezone.utc), source='stage1'),)}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_evaluation_foundation.py:66: TypeError
__________________________________________ test_later_actual_is_not_leakage ___________________________________________

    def test_later_actual_is_not_leakage():
        refs = (_ref(at=BEFORE),)
        assert detect_pit_leakage(CUTOFF, refs) == []
        observation = build_observation(
>           _record(input_refs=refs), "REVENUE", _actual(publication_datetime=AFTER)
            ^^^^^^^^^^^^^^^^^^^^^^^^
        )

src\tests\test_stage6_evaluation_foundation.py:156:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'input_refs': (ForecastInputRef(fact_key='REVENUE', report_version_id=9, available_at=datetime.datetime(2024, 3, 31, 0, 0, tzinfo=datetime.timezone.utc), source='stage1'),)}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_evaluation_foundation.py:66: TypeError
______________________________________ test_restated_actual_carried_not_decided _______________________________________

    def test_restated_actual_carried_not_decided():
        actual = _actual(data_quality_state="RESTATED", restated=True)
        assert actual.data_quality_state == "RESTATED"
        assert actual.restated is True
>       observation = build_observation(_record(), "REVENUE", actual)
                                        ^^^^^^^^^

src\tests\test_stage6_evaluation_foundation.py:185:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_evaluation_foundation.py:66: TypeError
_________________________________________ test_missing_report_version_carried _________________________________________

    def test_missing_report_version_carried():
        # Stage 6 Prompt 25 (Part A): an Actual without a ReportVersion id is
        # INVALID_REPORT_VERSION — carried (actual attached for audit) but
        # quarantined downstream, never scored.
        actual = _actual(report_version_id=None)
        assert actual.report_version_id is None
>       observation = build_observation(_record(), "REVENUE", actual)
                                        ^^^^^^^^^

src\tests\test_stage6_evaluation_foundation.py:195:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_evaluation_foundation.py:66: TypeError
____________________________________________ test_horizon_isolates_series _____________________________________________

    def test_horizon_isolates_series():
        assert (
>           evaluation_key_for(_record(forecast_horizon="12M"), "REVENUE").as_tuple()
                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            != evaluation_key_for(_record(forecast_horizon="3M"), "REVENUE").as_tuple()
        )

src\tests\test_stage6_evaluation_foundation.py:205:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_horizon': '12M'}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_evaluation_foundation.py:66: TypeError
_________________________________________ test_model_version_isolates_series __________________________________________

    def test_model_version_isolates_series():
        assert (
>           evaluation_key_for(_record(model_version="V1.0"), "REVENUE").as_tuple()
                               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            != evaluation_key_for(_record(model_version="V2.0"), "REVENUE").as_tuple()
        )

src\tests\test_stage6_evaluation_foundation.py:212:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'model_version': 'V1.0'}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_evaluation_foundation.py:66: TypeError
_____________________________________ test_duplicate_keys_share_flag_and_survive ______________________________________

    def test_duplicate_keys_share_flag_and_survive():
>       first = build_observation(_record(), "REVENUE", _actual())
                                  ^^^^^^^^^

src\tests\test_stage6_evaluation_foundation.py:221:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_evaluation_foundation.py:66: TypeError
_________________________________________ test_unique_observations_unflagged __________________________________________

    def test_unique_observations_unflagged():
        observations = [
>           build_observation(_record(forecast_horizon="3M"), "REVENUE"),
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            build_observation(_record(forecast_horizon="6M"), "REVENUE"),
        ]

src\tests\test_stage6_evaluation_foundation.py:233:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_horizon': '3M'}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_evaluation_foundation.py:66: TypeError
_____________________________________ test_missing_actual_value_is_none_not_zero ______________________________________

    def test_missing_actual_value_is_none_not_zero():
        observation = build_observation(
>           _record(), "REVENUE", _actual(value=None, data_quality_state="MISSING")
            ^^^^^^^^^
        )

src\tests\test_stage6_evaluation_foundation.py:245:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_evaluation_foundation.py:66: TypeError
_________________________________________ test_zero_actual_preserved_as_zero __________________________________________

    def test_zero_actual_preserved_as_zero():
>       observation = build_observation(_record(), "REVENUE", _actual(value=0.0))
                                        ^^^^^^^^^

src\tests\test_stage6_evaluation_foundation.py:252:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_evaluation_foundation.py:66: TypeError
________________________________________ test_missing_forecast_metric_is_none _________________________________________

    def test_missing_forecast_metric_is_none():
>       record = _record(revenue=None)
                 ^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage6_evaluation_foundation.py:258:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'revenue': None}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_evaluation_foundation.py:66: TypeError
____________________________________ test_unknown_metric_code_is_missing_not_zero _____________________________________

    def test_unknown_metric_code_is_missing_not_zero():
>       observation = build_observation(_record(), "NO_SUCH_METRIC")
                                        ^^^^^^^^^

src\tests\test_stage6_evaluation_foundation.py:265:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_evaluation_foundation.py:66: TypeError
________________________________________ test_metadata_counts_without_scoring _________________________________________

    def test_metadata_counts_without_scoring():
        observations = flag_duplicates([
>           build_observation(_record(), "REVENUE", _actual()),
                              ^^^^^^^^^
            build_observation(_record(forecast_horizon="3M"), "REVENUE"),
            build_observation(_record(input_refs=(_ref(at=AFTER),)), "REVENUE"),
        ])

src\tests\test_stage6_evaluation_foundation.py:283:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {}

    def _record(**overrides):
        fields = dict(
            forecast_id=1,
            forecast_version=1,
            company_id=7,
            forecast_period_id=101,
            industry_code="PETROCHEMICAL",
            forecast_horizon="12M",
            scenario="BASE",
            forecast_timestamp=STAMP,
            data_cutoff_datetime=CUTOFF,
            model_version="V1.0",
            forecast_method="M1",
            data_quality="VALID",
            baseline_method="SEASONAL_NAIVE",
            revenue=1000.0,
            operating_profit=200.0,
            operating_margin=0.2,
            net_profit=150.0,
            eps=15.0,
            roe=0.1,
            input_refs=(),
        )
        fields.update(overrides)
>       return ForecastRecord(**fields)
               ^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'

src\tests\test_stage6_evaluation_foundation.py:66: TypeError
=============================================== short test summary info ===============================================
FAILED src/tests/test_codal_pdf_extraction.py::test_codal_validation_corpus_inventory_is_exactly_locked_19_pdfs - AssertionError: SCOPE_ERROR: CODAL validation corpus drifted from the locked 19-PDF set. expected_count=19 actual_c...
FAILED src/tests/test_stage6_p25_selection.py::test_key_is_7_tuple_with_scenario_last - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p25_selection.py::test_key_scenario_distinct_keys_differ - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p25_selection.py::test_key_forecast_id_does_not_affect_key - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p25_selection.py::test_build_observation_invalid_report_version_status - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p25_adversarial.py::test_p25_01_multi_rv_earliest_publication_wins - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p25_adversarial.py::test_p25_02_same_publication_tie_break - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p25_adversarial.py::test_p25_03_restated_later_publication_loses_to_first_known - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p25_adversarial.py::test_p25_04_invalid_report_version_never_scores - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p25_adversarial.py::test_p25_05_missing_actual_value_quarantines - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p25_adversarial.py::test_p25_06_estimated_scores_with_limited_quality - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p25_adversarial.py::test_p25_07_suspicious_quarantines_verbatim - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p25_adversarial.py::test_p25_08_unmapped_quarantines_verbatim - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p25_adversarial.py::test_p25_09_conflicting_duplicates_fail_closed - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p25_adversarial.py::test_p25_10_dup_key_across_horizons_does_not_collide - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p25_adversarial.py::test_p25_11_dup_key_across_versions_does_not_collide - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p25_adversarial.py::test_p25_12_dup_key_across_cutoffs_does_not_collide - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p25_adversarial.py::test_p25_13_zero_actual_positive_forecast_scores - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p25_adversarial.py::test_p25_14_zero_actual_negative_forecast_scores - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p25_adversarial.py::test_p25_15_zero_over_zero_is_zero_base - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p25_adversarial.py::test_p25_16_zero_forecast_is_zero_base - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p25_adversarial.py::test_p25_17_positive_forecast_zero_actual_regime_none - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p25_adversarial.py::test_p25_restated_series_flags_limited_quality - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_foundation.py::test_identity_key_carries_full_mapping_key - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_foundation.py::test_identity_scenario_isolates_observations - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_foundation.py::test_identity_differs_by_metric - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_foundation.py::test_identity_stable_for_same_series - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_foundation.py::test_later_published_actual_binds_ready - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_foundation.py::test_historical_actual_also_binds - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_foundation.py::test_unbound_observation_waits_for_actual - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_foundation.py::test_leaked_input_freezes_observation - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_foundation.py::test_later_actual_is_not_leakage - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_foundation.py::test_restated_actual_carried_not_decided - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_foundation.py::test_missing_report_version_carried - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_foundation.py::test_horizon_isolates_series - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_foundation.py::test_model_version_isolates_series - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_foundation.py::test_duplicate_keys_share_flag_and_survive - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_foundation.py::test_unique_observations_unflagged - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_foundation.py::test_missing_actual_value_is_none_not_zero - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_foundation.py::test_zero_actual_preserved_as_zero - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_foundation.py::test_missing_forecast_metric_is_none - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_foundation.py::test_unknown_metric_code_is_missing_not_zero - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_foundation.py::test_metadata_counts_without_scoring - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
43 failed, 223 passed, 1 skipped in 196.03s (0:03:16)