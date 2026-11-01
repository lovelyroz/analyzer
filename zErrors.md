_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_id': 1, 'forecast_period_id': 101, 'revenue': 1000.0}

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

src\tests\test_stage6_p40_duplicates.py:59: TypeError
________________________________________ test_p40_09_cross_scenario_separation ________________________________________

    def test_p40_09_cross_scenario_separation():
        records = [
>           _record(forecast_id=index + 1, scenario=scenario)
            for index, scenario in enumerate(("BEAR", "BASE", "BULL"))
        ]

src\tests\test_stage6_p40_duplicates.py:310:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_id': 1, 'scenario': 'BEAR'}

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

src\tests\test_stage6_p40_duplicates.py:59: TypeError
________________________________________ test_p40_10_cross_horizon_separation _________________________________________

    def test_p40_10_cross_horizon_separation():
        records = [
>           _record(forecast_id=1, forecast_horizon="12M"),
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            _record(forecast_id=2, forecast_horizon="6M"),
        ]

src\tests\test_stage6_p40_duplicates.py:323:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_id': 1, 'forecast_horizon': '12M'}

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

src\tests\test_stage6_p40_duplicates.py:59: TypeError
________________________________________ test_p40_11_cross_version_separation _________________________________________

    def test_p40_11_cross_version_separation():
        records = [
>           _record(forecast_id=1, model_version="V1.0"),
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            _record(forecast_id=2, model_version="V2.0"),
        ]

src\tests\test_stage6_p40_duplicates.py:336:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_id': 1, 'model_version': 'V1.0'}

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

src\tests\test_stage6_p40_duplicates.py:59: TypeError
_____________________________ test_p40_12_conflicting_same_identity_quarantines_wholesale _____________________________

    def test_p40_12_conflicting_same_identity_quarantines_wholesale():
        # Same canonical identity, DIFFERENT forecast values: no defensible
        # ordering exists, so both quarantine — never an arbitrary pick.
        records = [
>           _record(forecast_id=1, forecast_period_id=101, revenue=1000.0),
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            _record(forecast_id=2, forecast_period_id=101, revenue=1300.0),
        ]

src\tests\test_stage6_p40_duplicates.py:354:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_id': 1, 'forecast_period_id': 101, 'revenue': 1000.0}

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

src\tests\test_stage6_p40_duplicates.py:59: TypeError
____________________________________ test_p40_13_conflict_does_not_touch_neighbors ____________________________________

    def test_p40_13_conflict_does_not_touch_neighbors():
        records = [
>           _record(forecast_id=1, forecast_period_id=101, revenue=1000.0),
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            _record(forecast_id=2, forecast_period_id=101, revenue=1300.0),
            _record(forecast_id=3, forecast_period_id=102, revenue=1000.0),
            _record(forecast_id=4, forecast_period_id=103, revenue=1000.0),
        ]

src\tests\test_stage6_p40_duplicates.py:370:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_id': 1, 'forecast_period_id': 101, 'revenue': 1000.0}

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

src\tests\test_stage6_p40_duplicates.py:59: TypeError
__________________________________ test_p40_14_duplicates_cannot_inflate_sufficiency __________________________________

    def test_p40_14_duplicates_cannot_inflate_sufficiency():
        # 4 distinct scored observations + an exact-duplicate pair on a 5th
        # period: sufficiency must see 4 (INSUFFICIENT_DATA), never 6.
        records = [
>           _record(forecast_id=index + 1, forecast_period_id=period)
            for index, period in enumerate([101, 102, 103, 104])
        ]

src\tests\test_stage6_p40_duplicates.py:390:
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

src\tests\test_stage6_p40_duplicates.py:59: TypeError
________________________________ test_p40_15_duplicate_leaves_remaining_pairing_intact ________________________________

    def test_p40_15_duplicate_leaves_remaining_pairing_intact():
        # Doubling ONE record quarantines exactly that pair; the surviving
        # observations pair with baselines exactly as a clean run of survivors.
        survivor_periods = [102, 103]
        records = (
>           [_record(forecast_id=1, forecast_period_id=101)]
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            + [
                _record(forecast_id=index + 2, forecast_period_id=period)
                for index, period in enumerate(survivor_periods)
            ]
            + [_record(forecast_id=9, forecast_period_id=101)]
        )

src\tests\test_stage6_p40_duplicates.py:410:
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

src\tests\test_stage6_p40_duplicates.py:59: TypeError
______________________________ test_p40_16_primary_vs_sensitivity_independently_correct _______________________________

    def test_p40_16_primary_vs_sensitivity_independently_correct():
        records = [
>           _record(forecast_id=1, forecast_period_id=101),
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            _record(forecast_id=2, forecast_period_id=102),
            _record(forecast_id=3, forecast_period_id=103),
        ]

src\tests\test_stage6_p40_duplicates.py:444:
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

src\tests\test_stage6_p40_duplicates.py:59: TypeError
___________________________________ test_p40_17_cutoff_rejections_still_fail_closed ___________________________________

    def test_p40_17_cutoff_rejections_still_fail_closed():
        # Missing Forecast cutoff.
        with pytest.raises(ValueError, match="missing evaluation cutoff"):
            _run(
>               [_record(forecast_id=1, data_cutoff_datetime=None)],
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                _actual_map([101]),
            )

src\tests\test_stage6_p40_duplicates.py:485:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_id': 1, 'data_cutoff_datetime': None}

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

src\tests\test_stage6_p40_duplicates.py:59: TypeError
___________________________________ test_p40_18_ttm_only_empty_later_actual_intact ____________________________________

    def test_p40_18_ttm_only_empty_later_actual_intact():
        # TTM-only invocation still reports its cutoff.
>       ttm_only = _run([], _actual_map([201]), ttm=[_ttm(0, 201)])
                                                     ^^^^^^^^^^^^

src\tests\test_stage6_p40_duplicates.py:518:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage6_p40_duplicates.py:85: in _ttm
    _record(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_id': 100, 'forecast_period_id': 201, 'data_cutoff_datetime': datetime.datetime(2024, 6, 30, 0, 0, tzinfo=datetime.timezone.utc)}

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

src\tests\test_stage6_p40_duplicates.py:59: TypeError
___________________________________ test_p40_19_rejections_return_no_partial_result ___________________________________

    def test_p40_19_rejections_return_no_partial_result():
        records = [
>           _record(forecast_id=1, data_cutoff_datetime=CUTOFF),
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            _record(forecast_id=2, data_cutoff_datetime=CUTOFF_OTHER),
        ]

src\tests\test_stage6_p40_duplicates.py:536:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_id': 1, 'data_cutoff_datetime': datetime.datetime(2024, 6, 30, 0, 0, tzinfo=datetime.timezone.utc)}

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

src\tests\test_stage6_p40_duplicates.py:59: TypeError
_______________________________ test_p41_01_naive_and_aware_same_instant_share_identity _______________________________

    def test_p41_01_naive_and_aware_same_instant_share_identity():
        naive_key = evaluation_key_for(
>           _record(forecast_id=1, data_cutoff_datetime=NAIVE_CUTOFF), "REVENUE"
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        )

src\tests\test_stage6_p41_cutoff_identity.py:76:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_id': 1, 'data_cutoff_datetime': datetime.datetime(2024, 6, 30, 0, 0)}

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

src\tests\test_stage6_p41_cutoff_identity.py:58: TypeError
__________________________________ test_p41_02_tz_offset_equivalent_shares_identity ___________________________________

    def test_p41_02_tz_offset_equivalent_shares_identity():
        offset_key = evaluation_key_for(
>           _record(forecast_id=1, data_cutoff_datetime=OFFSET_CUTOFF), "REVENUE"
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        )

src\tests\test_stage6_p41_cutoff_identity.py:88:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_id': 1, 'data_cutoff_datetime': datetime.datetime(2024, 6, 30, 2, 0, tzinfo=datetime.timezone(datetime.timedelta(seconds=7200)))}

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

src\tests\test_stage6_p41_cutoff_identity.py:58: TypeError
__________________________________ test_p41_03_iso_string_equivalent_shares_identity __________________________________

    def test_p41_03_iso_string_equivalent_shares_identity():
        iso_key = evaluation_key_for(
>           _record(forecast_id=1, data_cutoff_datetime=ISO_CUTOFF), "REVENUE"
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        )

src\tests\test_stage6_p41_cutoff_identity.py:98:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_id': 1, 'data_cutoff_datetime': '2024-06-30T00:00:00+00:00'}

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

src\tests\test_stage6_p41_cutoff_identity.py:58: TypeError
_____________________________________ test_p41_04_distinct_instants_stay_distinct _____________________________________

    def test_p41_04_distinct_instants_stay_distinct():
>       key = evaluation_key_for(_record(data_cutoff_datetime=CUTOFF), "REVENUE")
                                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage6_p41_cutoff_identity.py:107:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'data_cutoff_datetime': datetime.datetime(2024, 6, 30, 0, 0, tzinfo=datetime.timezone.utc)}

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

src\tests\test_stage6_p41_cutoff_identity.py:58: TypeError
_____________________________ test_p41_05_equivalent_cutoffs_collide_quarantine_wholesale _____________________________

    def test_p41_05_equivalent_cutoffs_collide_quarantine_wholesale():
        observations = [
            build_observation(
>               _record(forecast_id=1, data_cutoff_datetime=NAIVE_CUTOFF),
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                "REVENUE",
                _actual(),
            ),
            build_observation(
                _record(forecast_id=2, data_cutoff_datetime=CUTOFF),
                "REVENUE",
                _actual(),
            ),
        ]

src\tests\test_stage6_p41_cutoff_identity.py:117:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_id': 1, 'data_cutoff_datetime': datetime.datetime(2024, 6, 30, 0, 0)}

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

src\tests\test_stage6_p41_cutoff_identity.py:58: TypeError
__________________________ test_p41_06_pipeline_guard_accepts_equivalent_pair_single_cutoff ___________________________

    def test_p41_06_pipeline_guard_accepts_equivalent_pair_single_cutoff():
        result = run_evaluation_pipeline(
            [
>               _record(forecast_id=1, forecast_period_id=101,
                        data_cutoff_datetime=NAIVE_CUTOFF),
                _record(forecast_id=2, forecast_period_id=102,
                        data_cutoff_datetime=OFFSET_CUTOFF),
            ],
            ["REVENUE"],
            {
                (7, 101, "REVENUE"): _actual(period=101),
                (7, 102, "REVENUE"): _actual(period=102),
            },
        )

src\tests\test_stage6_p41_cutoff_identity.py:146:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_id': 1, 'forecast_period_id': 101, 'data_cutoff_datetime': datetime.datetime(2024, 6, 30, 0, 0)}

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

src\tests\test_stage6_p41_cutoff_identity.py:58: TypeError
_________________________ test_p41_07_three_equivalent_forms_collide_wholesale_no_winner_pick _________________________

    def test_p41_07_three_equivalent_forms_collide_wholesale_no_winner_pick():
        observations = [
            build_observation(
>               _record(forecast_id=1, data_cutoff_datetime=NAIVE_CUTOFF),
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                "REVENUE",
                _actual(),
            ),
            build_observation(
                _record(forecast_id=2, data_cutoff_datetime=OFFSET_CUTOFF),
                "REVENUE",
                _actual(),
            ),
            build_observation(
                _record(forecast_id=3, data_cutoff_datetime=ISO_CUTOFF),
                "REVENUE",
                _actual(),
            ),
        ]

src\tests\test_stage6_p41_cutoff_identity.py:215:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_id': 1, 'data_cutoff_datetime': datetime.datetime(2024, 6, 30, 0, 0)}

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

src\tests\test_stage6_p41_cutoff_identity.py:58: TypeError
_____________________________ test_p41_08_reordered_equivalent_cutoffs_decide_identically _____________________________

    def test_p41_08_reordered_equivalent_cutoffs_decide_identically():
>       first = _record(forecast_id=1, forecast_period_id=101,
                        data_cutoff_datetime=NAIVE_CUTOFF)

src\tests\test_stage6_p41_cutoff_identity.py:258:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_id': 1, 'forecast_period_id': 101, 'data_cutoff_datetime': datetime.datetime(2024, 6, 30, 0, 0)}

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

src\tests\test_stage6_p41_cutoff_identity.py:58: TypeError
______________________________ test_p41_09_repeated_ttm_equivalent_forms_inflate_nothing ______________________________

    def test_p41_09_repeated_ttm_equivalent_forms_inflate_nothing():
        periods = [101, 102, 103]
        records = [
>           _record(forecast_id=index + 1, forecast_period_id=period)
            for index, period in enumerate(periods)
        ]

src\tests\test_stage6_p41_cutoff_identity.py:293:
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

src\tests\test_stage6_p41_cutoff_identity.py:58: TypeError
________________________________ test_p41_10_forecast_ttm_overlap_on_cutoff_form_only _________________________________

    def test_p41_10_forecast_ttm_overlap_on_cutoff_form_only():
        records = [
>           _record(forecast_id=1, forecast_period_id=101),
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            _record(forecast_id=2, forecast_period_id=102),
            _record(forecast_id=3, forecast_period_id=201,
                    data_cutoff_datetime=NAIVE_CUTOFF),
        ]

src\tests\test_stage6_p41_cutoff_identity.py:339:
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

src\tests\test_stage6_p41_cutoff_identity.py:58: TypeError
__________________________ test_p41_11_distinct_periods_same_canonical_instant_stay_distinct __________________________

    def test_p41_11_distinct_periods_same_canonical_instant_stay_distinct():
        records = [
>           _record(forecast_id=1, forecast_period_id=101,
                    data_cutoff_datetime=NAIVE_CUTOFF),
            _record(forecast_id=2, forecast_period_id=102,
                    data_cutoff_datetime=OFFSET_CUTOFF),
            _record(forecast_id=3, forecast_period_id=103,
                    data_cutoff_datetime=ISO_CUTOFF),
        ]

src\tests\test_stage6_p41_cutoff_identity.py:361:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_id': 1, 'forecast_period_id': 101, 'data_cutoff_datetime': datetime.datetime(2024, 6, 30, 0, 0)}

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

src\tests\test_stage6_p41_cutoff_identity.py:58: TypeError
_____________________________ test_p41_12_scenario_isolation_with_mixed_equivalent_forms ______________________________

    def test_p41_12_scenario_isolation_with_mixed_equivalent_forms():
        records = [
>           _record(forecast_id=1, scenario="BEAR", data_cutoff_datetime=NAIVE_CUTOFF),
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            _record(forecast_id=2, scenario="BASE", data_cutoff_datetime=ISO_CUTOFF),
            _record(forecast_id=3, scenario="BULL", data_cutoff_datetime=OFFSET_CUTOFF),
        ]

src\tests\test_stage6_p41_cutoff_identity.py:383:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_id': 1, 'scenario': 'BEAR', 'data_cutoff_datetime': datetime.datetime(2024, 6, 30, 0, 0)}

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

src\tests\test_stage6_p41_cutoff_identity.py:58: TypeError
__________________________ test_p41_13_horizon_version_isolation_with_mixed_equivalent_forms __________________________

    def test_p41_13_horizon_version_isolation_with_mixed_equivalent_forms():
        records = [
>           _record(forecast_id=1, forecast_horizon="12M",
                    data_cutoff_datetime=NAIVE_CUTOFF),
            _record(forecast_id=2, forecast_horizon="6M",
                    data_cutoff_datetime=ISO_CUTOFF),
        ]

src\tests\test_stage6_p41_cutoff_identity.py:400:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_id': 1, 'forecast_horizon': '12M', 'data_cutoff_datetime': datetime.datetime(2024, 6, 30, 0, 0)}

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

src\tests\test_stage6_p41_cutoff_identity.py:58: TypeError
_______________________________ test_p41_14_missing_invalid_mixed_instants_fail_closed ________________________________

    def test_p41_14_missing_invalid_mixed_instants_fail_closed():
        with pytest.raises(ValueError, match="missing evaluation cutoff"):
            run_evaluation_pipeline(
>               [_record(forecast_id=1, data_cutoff_datetime=None)],
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
                ["REVENUE"],
                _actual_map([101]),
            )

src\tests\test_stage6_p41_cutoff_identity.py:434:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_id': 1, 'data_cutoff_datetime': None}

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

src\tests\test_stage6_p41_cutoff_identity.py:58: TypeError
________________________________ test_p41_15_empty_and_ttm_only_with_equivalent_forms _________________________________

    def test_p41_15_empty_and_ttm_only_with_equivalent_forms():
        empty = run_evaluation_pipeline([], ["REVENUE"], {})
        assert empty.artifact is not None
        assert empty.artifact.evaluation_cutoff is None
        assert empty.series_count == 0
        ttm_only = run_evaluation_pipeline(
            [], ["REVENUE"], _actual_map([201]),
>           ttm_observations=[_ttm(0, 201, cutoff=ISO_CUTOFF)],
                              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        )

src\tests\test_stage6_p41_cutoff_identity.py:477:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage6_p41_cutoff_identity.py:171: in _ttm
    _record(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_id': 100, 'forecast_period_id': 201, 'data_cutoff_datetime': '2024-06-30T00:00:00+00:00'}

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

src\tests\test_stage6_p41_cutoff_identity.py:58: TypeError
__________________________________ test_p41_16_later_published_actual_stays_eligible __________________________________

    def test_p41_16_later_published_actual_stays_eligible():
        assert AFTER > CUTOFF
        result = run_evaluation_pipeline(
>           [_record(data_cutoff_datetime=NAIVE_CUTOFF)],
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            ["REVENUE"],
            _actual_map([101]),
        )

src\tests\test_stage6_p41_cutoff_identity.py:490:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'data_cutoff_datetime': datetime.datetime(2024, 6, 30, 0, 0)}

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

src\tests\test_stage6_p41_cutoff_identity.py:58: TypeError
_________________________ test_p41_17_rejected_equivalent_mixed_invocation_returns_no_partial _________________________

    def test_p41_17_rejected_equivalent_mixed_invocation_returns_no_partial():
        records = [
>           _record(forecast_id=1, data_cutoff_datetime=ISO_CUTOFF),
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            _record(forecast_id=2, data_cutoff_datetime=OTHER),
        ]

src\tests\test_stage6_p41_cutoff_identity.py:505:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_id': 1, 'data_cutoff_datetime': '2024-06-30T00:00:00+00:00'}

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

src\tests\test_stage6_p41_cutoff_identity.py:58: TypeError
___________________________ test_governed_series_withholds_reliability_even_with_components ___________________________

    def test_governed_series_withholds_reliability_even_with_components():
>       governed = govern_series(_series(), _components())
                                 ^^^^^^^^^

src\tests\test_stage6_reliability_governance.py:198:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage6_reliability_governance.py:113: in _series
    _observation(
src\tests\test_stage6_reliability_governance.py:99: in _observation
    record = _record(**record_overrides)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_period_id': 101, 'forecast_horizon': '12M', 'model_version': 'V1.0', 'revenue': 1000.0}

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

src\tests\test_stage6_reliability_governance.py:80: TypeError
__________________________ test_governed_series_without_components_withholds_performance_too __________________________

    def test_governed_series_without_components_withholds_performance_too():
>       governed = govern_series(_series())
                                 ^^^^^^^^^

src\tests\test_stage6_reliability_governance.py:206:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage6_reliability_governance.py:113: in _series
    _observation(
src\tests\test_stage6_reliability_governance.py:99: in _observation
    record = _record(**record_overrides)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_period_id': 101, 'forecast_horizon': '12M', 'model_version': 'V1.0', 'revenue': 1000.0}

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

src\tests\test_stage6_reliability_governance.py:80: TypeError
_________________________________ test_govern_series_never_mutates_the_p19_aggregate __________________________________

    def test_govern_series_never_mutates_the_p19_aggregate():
>       series = _series()
                 ^^^^^^^^^

src\tests\test_stage6_reliability_governance.py:215:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage6_reliability_governance.py:113: in _series
    _observation(
src\tests\test_stage6_reliability_governance.py:99: in _observation
    record = _record(**record_overrides)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_period_id': 101, 'forecast_horizon': '12M', 'model_version': 'V1.0', 'revenue': 1000.0}

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

src\tests\test_stage6_reliability_governance.py:80: TypeError
______________________________ test_suggestive_bias_evidence_still_yields_no_calibration ______________________________

    def test_suggestive_bias_evidence_still_yields_no_calibration():
        # Ten unanimous under-forecasts would tempt a persistence claim; without
        # the B3 definition the verdict stays NO_CALIBRATION.
>       series = _series(periods=10, forecast_value=1000.0, actual_value=1300.0)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage6_reliability_governance.py:255:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage6_reliability_governance.py:113: in _series
    _observation(
src\tests\test_stage6_reliability_governance.py:99: in _observation
    record = _record(**record_overrides)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_period_id': 101, 'forecast_horizon': '12M', 'model_version': 'V1.0', 'revenue': 1000.0}

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

src\tests\test_stage6_reliability_governance.py:80: TypeError
___________________________________ test_pit_later_published_actual_still_governed ____________________________________

    def test_pit_later_published_actual_still_governed():
        # AFTER > CUTOFF on every observation: the later-published Actual is the
        # evaluated outcome, never leakage. Distinct periods so no duplicate
        # collision masks the PIT assertion.
>       observations = [_observation(forecast_period_id=101 + i) for i in range(8)]
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage6_reliability_governance.py:276:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage6_reliability_governance.py:99: in _observation
    record = _record(**record_overrides)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_period_id': 101, 'revenue': 1000.0}

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

src\tests\test_stage6_reliability_governance.py:80: TypeError
________________________________ test_horizon_and_version_isolation_survive_governance ________________________________

    def test_horizon_and_version_isolation_survive_governance():
        observations = [
>           _observation(forecast_period_id=101 + i, forecast_horizon="12M",
                         model_version="V1.0")
            for i in range(8)
        ] + [
            _observation(forecast_period_id=101 + i, forecast_horizon="3M",
                         model_version="V2.0")
            for i in range(8)
        ]

src\tests\test_stage6_reliability_governance.py:288:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage6_reliability_governance.py:99: in _observation
    record = _record(**record_overrides)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_period_id': 101, 'forecast_horizon': '12M', 'model_version': 'V1.0', 'revenue': 1000.0}

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

src\tests\test_stage6_reliability_governance.py:80: TypeError
__________________________________ test_null_and_quarantines_flow_through_unchanged ___________________________________

    def test_null_and_quarantines_flow_through_unchanged():
        observations = [
>           *[_observation(forecast_period_id=101 + i) for i in range(4)],
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            _observation(forecast_value=0.0, actual_value=100.0,
                         forecast_period_id=200),  # ZERO_BASE quarantine
            build_observation(
                _record(forecast_period_id=201,
                        input_refs=(ForecastInputRef(fact_key="X",
                                                     available_at=AFTER),)),
                "REVENUE", _actual(),
            ),  # PIT_INVALID_INPUT quarantine
        ]

src\tests\test_stage6_reliability_governance.py:306:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage6_reliability_governance.py:99: in _observation
    record = _record(**record_overrides)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_period_id': 101, 'revenue': 1000.0}

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

src\tests\test_stage6_reliability_governance.py:80: TypeError
____________________________________ test_missing_mape_marks_unavailable_component ____________________________________

    def test_missing_mape_marks_unavailable_component():
>       governed = govern_series(_series(periods=3))  # scored but thin evidence
                                 ^^^^^^^^^^^^^^^^^^

src\tests\test_stage6_reliability_governance.py:325:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage6_reliability_governance.py:113: in _series
    _observation(
src\tests\test_stage6_reliability_governance.py:99: in _observation
    record = _record(**record_overrides)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_period_id': 101, 'forecast_horizon': '12M', 'model_version': 'V1.0', 'revenue': 1000.0}

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

src\tests\test_stage6_reliability_governance.py:80: TypeError
___________________________________ test_regime_only_series_names_mape_unavailable ____________________________________

    def test_regime_only_series_names_mape_unavailable():
        observations = [
>           _observation(forecast_value=0.0, actual_value=100.0,
                         forecast_period_id=101 + i)
            for i in range(5)
        ]

src\tests\test_stage6_reliability_governance.py:331:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage6_reliability_governance.py:99: in _observation
    record = _record(**record_overrides)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_period_id': 101, 'revenue': 0.0}

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

src\tests\test_stage6_reliability_governance.py:80: TypeError
______________________________________ test_full_path_observation_to_governance _______________________________________

    def test_full_path_observation_to_governance():
>       observations = [_observation(forecast_period_id=101 + i) for i in range(8)]
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage6_reliability_governance.py:347:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage6_reliability_governance.py:99: in _observation
    record = _record(**record_overrides)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'forecast_period_id': 101, 'revenue': 1000.0}

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

src\tests\test_stage6_reliability_governance.py:80: TypeError
__________________________________________ test_keys_all_three_pairs_unequal __________________________________________

    def test_keys_all_three_pairs_unequal():
        keys = {
>           scenario: evaluation_key_for(_record(scenario=scenario), "REVENUE")
                                         ^^^^^^^^^^^^^^^^^^^^^^^^^^
            for scenario in SCENARIOS
        }

src\tests\test_stage6_scenario_isolation.py:98:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'scenario': 'BEAR'}

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

src\tests\test_stage6_scenario_isolation.py:59: TypeError
________________________________________ test_keys_preserve_canonical_scenario ________________________________________

    def test_keys_preserve_canonical_scenario():
        for scenario in SCENARIOS:
>           key = evaluation_key_for(_record(scenario=scenario), "REVENUE")
                                     ^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage6_scenario_isolation.py:109:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'scenario': 'BEAR'}

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

src\tests\test_stage6_scenario_isolation.py:59: TypeError
__________________________________________ test_keys_hash_set_dict_behavior ___________________________________________

    def test_keys_hash_set_dict_behavior():
        keys = [
>           evaluation_key_for(_record(scenario=scenario), "REVENUE")
                               ^^^^^^^^^^^^^^^^^^^^^^^^^^
            for scenario in SCENARIOS
        ]

src\tests\test_stage6_scenario_isolation.py:116:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'scenario': 'BEAR'}

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

src\tests\test_stage6_scenario_isolation.py:59: TypeError
_______________________________________ test_three_scenarios_yield_three_series _______________________________________

    def test_three_scenarios_yield_three_series():
>       observations = [_observation(scenario=scenario) for scenario in SCENARIOS]
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage6_scenario_isolation.py:137:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage6_scenario_isolation.py:77: in _observation
    record = _record(**record_overrides)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'scenario': 'BEAR', 'revenue': 1000.0}

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

src\tests\test_stage6_scenario_isolation.py:59: TypeError
__________________________________ test_mape_bias_inputs_not_pooled_across_scenarios __________________________________

    def test_mape_bias_inputs_not_pooled_across_scenarios():
        # Scenario-specific forecast values against a shared Actual: each series
        # must report its own MAPE/Bias, never a pooled mean.
        observations = [
>           _observation(forecast_value=900.0, actual_value=1100.0, scenario="BEAR"),
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            _observation(forecast_value=1000.0, actual_value=1100.0, scenario="BASE"),
            _observation(forecast_value=1100.0, actual_value=1100.0, scenario="BULL"),
        ]

src\tests\test_stage6_scenario_isolation.py:153:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage6_scenario_isolation.py:77: in _observation
    record = _record(**record_overrides)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'scenario': 'BEAR', 'revenue': 900.0}

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

src\tests\test_stage6_scenario_isolation.py:59: TypeError
_______________________________________ test_series_evaluation_carries_scenario _______________________________________

    def test_series_evaluation_carries_scenario():
>       observations = [_observation(scenario=scenario) for scenario in SCENARIOS]
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage6_scenario_isolation.py:174:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage6_scenario_isolation.py:77: in _observation
    record = _record(**record_overrides)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'scenario': 'BEAR', 'revenue': 1000.0}

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

src\tests\test_stage6_scenario_isolation.py:59: TypeError
_____________________________________ test_baseline_pairing_stays_within_scenario _____________________________________

    def test_baseline_pairing_stays_within_scenario():
>       observations = [_observation(scenario=scenario) for scenario in SCENARIOS]
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage6_scenario_isolation.py:187:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage6_scenario_isolation.py:77: in _observation
    record = _record(**record_overrides)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'scenario': 'BEAR', 'revenue': 1000.0}

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

src\tests\test_stage6_scenario_isolation.py:59: TypeError
_______________________________________ test_baseline_absent_in_other_scenarios _______________________________________

    def test_baseline_absent_in_other_scenarios():
>       observations = [_observation(scenario=scenario) for scenario in SCENARIOS]
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage6_scenario_isolation.py:204:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage6_scenario_isolation.py:77: in _observation
    record = _record(**record_overrides)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'scenario': 'BEAR', 'revenue': 1000.0}

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

src\tests\test_stage6_scenario_isolation.py:59: TypeError
____________________________________ test_empty_scenario_record_raises_fail_closed ____________________________________

    def test_empty_scenario_record_raises_fail_closed():
        # Never silently Base: the key construction itself refuses.
        with pytest.raises(ValueError):
>           evaluation_key_for(_record(scenario=""), "REVENUE")
                               ^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage6_scenario_isolation.py:234:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'scenario': ''}

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

src\tests\test_stage6_scenario_isolation.py:59: TypeError
_____________________________ test_noncanonical_scenario_preserved_verbatim_and_isolated ______________________________

    def test_noncanonical_scenario_preserved_verbatim_and_isolated():
        # A non-empty unknown scenario is not collapsed into any canonical one:
        # it stays verbatim and aggregates alone.
>       key = evaluation_key_for(_record(scenario="SIDEWAYS"), "REVENUE")
                                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage6_scenario_isolation.py:240:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'scenario': 'SIDEWAYS'}

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

src\tests\test_stage6_scenario_isolation.py:59: TypeError
________________________________________ test_single_scenario_values_unchanged ________________________________________

    def test_single_scenario_values_unchanged():
>       results = aggregate_observations([_observation(scenario="BASE")])
                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage6_scenario_isolation.py:254:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage6_scenario_isolation.py:77: in _observation
    record = _record(**record_overrides)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'scenario': 'BASE', 'revenue': 1000.0}

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

src\tests\test_stage6_scenario_isolation.py:59: TypeError
____________________________ test_three_scenarios_not_three_observations_in_shared_series _____________________________

    def test_three_scenarios_not_three_observations_in_shared_series():
>       observations = [_observation(scenario=scenario) for scenario in SCENARIOS]
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage6_scenario_isolation.py:267:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage6_scenario_isolation.py:77: in _observation
    record = _record(**record_overrides)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'scenario': 'BEAR', 'revenue': 1000.0}

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

src\tests\test_stage6_scenario_isolation.py:59: TypeError
______________________________________ test_insertion_order_all_six_permutations ______________________________________

    def test_insertion_order_all_six_permutations():
>       observations = [_observation(scenario=scenario) for scenario in SCENARIOS]
                        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage6_scenario_isolation.py:284:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage6_scenario_isolation.py:77: in _observation
    record = _record(**record_overrides)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'scenario': 'BEAR', 'revenue': 1000.0}

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

src\tests\test_stage6_scenario_isolation.py:59: TypeError
________________________________________ test_interleaved_multi_company_inputs ________________________________________

    def test_interleaved_multi_company_inputs():
        interleaved = [
>           _observation(scenario="BEAR", company_id=7),
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            _observation(scenario="BULL", company_id=9),
            _observation(scenario="BASE", company_id=7),
            _observation(scenario="BEAR", company_id=9),
            _observation(scenario="BULL", company_id=7),
            _observation(scenario="BASE", company_id=9),
        ]

src\tests\test_stage6_scenario_isolation.py:298:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage6_scenario_isolation.py:77: in _observation
    record = _record(**record_overrides)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'scenario': 'BEAR', 'company_id': 7, 'revenue': 1000.0}

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

src\tests\test_stage6_scenario_isolation.py:59: TypeError
__________________________ test_duplicate_within_one_scenario_quarantines_only_that_scenario __________________________

    def test_duplicate_within_one_scenario_quarantines_only_that_scenario():
        # Two identical BASE observations collide; the BULL observation must be
        # untouched: same-scenario keys collide, cross-scenario keys never do.
>       first = _observation(scenario="BASE")
                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage6_scenario_isolation.py:320:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage6_scenario_isolation.py:77: in _observation
    record = _record(**record_overrides)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'scenario': 'BASE', 'revenue': 1000.0}

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

src\tests\test_stage6_scenario_isolation.py:59: TypeError
________________________________ test_identical_values_across_scenarios_still_separate ________________________________

    def test_identical_values_across_scenarios_still_separate():
        observations = [
>           _observation(forecast_value=1000.0, actual_value=1100.0, scenario=scenario)
            for scenario in SCENARIOS
        ]

src\tests\test_stage6_scenario_isolation.py:339:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage6_scenario_isolation.py:77: in _observation
    record = _record(**record_overrides)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'scenario': 'BEAR', 'revenue': 1000.0}

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

src\tests\test_stage6_scenario_isolation.py:59: TypeError
________________________________________ test_single_scenario_input_one_series ________________________________________

    def test_single_scenario_input_one_series():
>       results = aggregate_observations([_observation(scenario="BULL")])
                                          ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage6_scenario_isolation.py:356:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage6_scenario_isolation.py:77: in _observation
    record = _record(**record_overrides)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'scenario': 'BULL', 'revenue': 1000.0}

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

src\tests\test_stage6_scenario_isolation.py:59: TypeError
______________________________________ test_pipeline_three_scenarios_end_to_end _______________________________________

    def test_pipeline_three_scenarios_end_to_end():
        records = [
>           _record(scenario="BEAR", revenue=900.0),
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
            _record(scenario="BASE", revenue=1000.0),
            _record(scenario="BULL", revenue=1100.0),
        ]

src\tests\test_stage6_scenario_isolation.py:375:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'scenario': 'BEAR', 'revenue': 900.0}

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

src\tests\test_stage6_scenario_isolation.py:59: TypeError
_____________________________________ test_pipeline_baseline_pairing_per_scenario _____________________________________

    def test_pipeline_baseline_pairing_per_scenario():
>       records = [_record(scenario=scenario) for scenario in SCENARIOS]
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage6_scenario_isolation.py:392:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

overrides = {'scenario': 'BEAR'}

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

src\tests\test_stage6_scenario_isolation.py:59: TypeError
=============================================== short test summary info ===============================================
FAILED src/tests/test_codal_extraction.py::test_real_codal_monthly_activity_pdf - assert False
FAILED src/tests/test_codal_pdf_extraction.py::test_codal_validation_corpus_inventory_is_exactly_locked_19_pdfs - AssertionError: SCOPE_ERROR: CODAL validation corpus drifted from the locked 19-PDF set. expected_count=19 actual_c...
FAILED src/tests/test_ingestion_fx.py::test_ingest_fx_xlsx_toman_and_rial - ModuleNotFoundError: No module named 'openpyxl'
FAILED src/tests/test_stage1_rules.py::test_migration_runner_upgrades_empty_database_and_is_idempotent - assert 8 == 7
FAILED src/tests/test_stage1_rules.py::test_migration_runner_upgrades_legacy_stage1_schema - assert 8 == 7
FAILED src/tests/test_stage6_artifact_boundary.py::test_production_primary_result_carries_valid_artifact - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_artifact_boundary.py::test_production_sensitivity_result_carries_valid_artifact - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_artifact_boundary.py::test_production_mixed_cutoff_fails_closed_with_no_result - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_artifact_boundary.py::test_production_mixed_cutoff_returns_no_partial_result - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_artifact_boundary.py::test_production_rerun_result_carries_artifact_with_supersedes - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_artifact_boundary.py::test_production_multi_scenario_result_carries_per_scenario_provenance - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_artifact_identity.py::test_pipeline_result_carries_artifact - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_artifact_identity.py::test_cutoff_single_populated - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_artifact_identity.py::test_cutoff_mixed_raises_fail_closed - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_artifact_identity.py::test_fabricated_default_check_missing_provenance_empty - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_artifact_identity.py::test_rerun_distinct_run_ids_same_inputs - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_artifact_identity.py::test_primary_vs_sensitivity_purposes_differ - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_artifact_identity.py::test_rerun_without_supersedes_has_none - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_artifact_identity.py::test_primary_estimated_scores_with_limited_quality - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_artifact_identity.py::test_sensitivity_estimated_quarantined_valid_scores - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_artifact_identity.py::test_multi_scenario_separate_provenance_entries - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_artifact_identity.py::test_report_version_id_and_publication_surfaced - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_artifact_identity.py::test_multi_period_series_keeps_distinct_report_versions - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_artifact_identity.py::test_rerun_with_supersedes_preserved - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_artifact_identity.py::test_invalid_report_version_yields_empty_provenance - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_artifact_identity.py::test_shared_actual_across_scenarios_no_pooling - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_artifact_identity.py::test_partial_provenance_valid_plus_pending - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_artifact_identity.py::test_self_referential_supersedes_raises_in_pipeline - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_artifact_identity.py::test_sensitivity_exclusion_order_after_ready_and_duplicate - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_artifact_identity.py::test_duplicate_beats_sensitivity_exclusion - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_artifact_identity.py::test_aggregate_observations_threads_exclude_estimated - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_artifact_identity.py::test_aggregate_default_path_unchanged - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation.py::test_production_path_withholds_after_removal - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
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
FAILED src/tests/test_stage6_evaluation_metrics.py::test_error_sign_under_and_over_forecast - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_metrics.py::test_mape_and_bias_match_spec_formulas - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_metrics.py::test_zero_forecast_keeps_absolute_error_drops_percentages - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_metrics.py::test_sign_change_regimes_quarantined_with_absolute_error - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_metrics.py::test_zero_actual_excluded_from_mape_with_reason_code - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_metrics.py::test_zero_actual_negative_forecast_bias_term_is_plus_one - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_metrics.py::test_each_horizon_evaluated_independently - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_metrics.py::test_model_versions_never_combine - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_metrics.py::test_duplicate_collision_quarantines_both - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_metrics.py::test_duplicate_scenario_distinct_pair_scores_separately - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_metrics.py::test_pit_leaked_inputs_never_score - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_metrics.py::test_later_published_actual_is_the_scored_outcome - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_metrics.py::test_invalid_actual_states_quarantined_verbatim - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_metrics.py::test_missing_values_are_none_not_zero - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_metrics.py::test_missing_baseline_value_means_missing_baseline_metrics - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_metrics.py::test_baseline_zero_value_never_fabricates_baseline_ape - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_metrics.py::test_baseline_comparison_matches_section_17_formula - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_metrics.py::test_model_worse_than_baseline_reports_negative_improvement - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_metrics.py::test_baseline_uses_same_scored_set_not_a_wider_one - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_metrics.py::test_insufficient_history_bands_match_spec_section_14 - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_metrics.py::test_only_scored_observations_drive_the_band - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_evaluation_metrics.py::test_series_carries_no_reliability_or_calibration - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
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
FAILED src/tests/test_stage6_p25_selection.py::test_key_is_7_tuple_with_scenario_last - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p25_selection.py::test_key_scenario_distinct_keys_differ - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p25_selection.py::test_key_forecast_id_does_not_affect_key - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p25_selection.py::test_build_observation_invalid_report_version_status - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p38_closure.py::test_p38_mixed_cutoff_raises_before_scoring_no_partial_result - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p38_closure.py::test_p38_single_cutoff_still_evaluates - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p38_closure.py::test_p38_mixed_cutoff_multi_scenario_raises - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p38_closure.py::test_p38_actual_zero_mape_excluded_error_retained - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p38_closure.py::test_p38_actual_zero_negative_forecast_bias_plus_one - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p38_closure.py::test_p38_actual_zero_series_mape_null_bias_kept - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p38_closure.py::test_p38_zero_zero_is_bias_undefined_with_status - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p38_closure.py::test_p38_bias_undefined_zero_zero_excluded_from_bias_mean - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p38_closure.py::test_p38_mape_bias_independent_counts_mixed_series - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p38_closure.py::test_p38_baseline_bias_paired_same_event_set - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p38_closure.py::test_p38_three_scenarios_share_one_actual_no_pooling - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p38_closure.py::test_p38_mixed_scenarios_plus_duplicates - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p38_closure.py::test_p38_actual_zero_with_independent_eligibility_mixed - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p38_closure.py::test_p38_reordered_observations_stable - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p38_closure.py::test_p38_reliability_stays_none_and_sufficiency_bands - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p38_closure.py::test_p38_exact_actual_tie_fails_closed_version_order_still_works - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p39_cutoff.py::test_p39_01_single_valid_cutoff_succeeds - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p39_cutoff.py::test_p39_02_multiple_same_cutoff_succeeds - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p39_cutoff.py::test_p39_03_equivalent_tz_aware_cutoffs_succeed - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p39_cutoff.py::test_p39_04_distinct_non_null_cutoffs_fail - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p39_cutoff.py::test_p39_05_valid_plus_missing_forecast_cutoff_fails - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p39_cutoff.py::test_p39_06_all_missing_cutoffs_fail - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p39_cutoff.py::test_p39_07_valid_forecast_plus_missing_ttm_cutoff_fails - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p39_cutoff.py::test_p39_08_distinct_forecast_ttm_cutoffs_fail - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p39_cutoff.py::test_p39_09_matching_forecast_ttm_succeeds_correct_cutoff - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p39_cutoff.py::test_p39_10_ttm_only_valid_reports_cutoff - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p39_cutoff.py::test_p39_11_ttm_only_missing_cutoff_fails - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p39_cutoff.py::test_p39_13_rejected_invocation_returns_no_partial_result - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p39_cutoff.py::test_p39_14_reordered_interleaved_inputs_same_decision - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p39_cutoff.py::test_p39_15_three_scenarios_one_cutoff_stay_separate - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p39_cutoff.py::test_p39_16_multi_scenario_mixed_fails_closed_no_partial - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p39_cutoff.py::test_p39_17_later_published_actual_stays_eligible - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p39_cutoff.py::test_p39_18_provenance_purpose_supersession_unchanged - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p39_cutoff.py::test_p39_19_ttm_conservation_and_duplicates_intact - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p40_duplicates.py::test_p40_01_single_ttm_counted_once - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p40_duplicates.py::test_p40_02_two_distinct_ttm_counted_twice - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p40_duplicates.py::test_p40_03_exact_repeat_ttm_inflates_nothing - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p40_duplicates.py::test_p40_04_triple_repeat_still_counts_once - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p40_duplicates.py::test_p40_05_reordered_duplicates_same_decision - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p40_duplicates.py::test_p40_06_forecast_ttm_same_identity_overlap_not_double_counted - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p40_duplicates.py::test_p40_07_distinct_periods_stay_distinct - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p40_duplicates.py::test_p40_08_same_numbers_different_keys_not_deduped - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p40_duplicates.py::test_p40_09_cross_scenario_separation - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p40_duplicates.py::test_p40_10_cross_horizon_separation - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p40_duplicates.py::test_p40_11_cross_version_separation - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p40_duplicates.py::test_p40_12_conflicting_same_identity_quarantines_wholesale - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p40_duplicates.py::test_p40_13_conflict_does_not_touch_neighbors - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p40_duplicates.py::test_p40_14_duplicates_cannot_inflate_sufficiency - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p40_duplicates.py::test_p40_15_duplicate_leaves_remaining_pairing_intact - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p40_duplicates.py::test_p40_16_primary_vs_sensitivity_independently_correct - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p40_duplicates.py::test_p40_17_cutoff_rejections_still_fail_closed - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p40_duplicates.py::test_p40_18_ttm_only_empty_later_actual_intact - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p40_duplicates.py::test_p40_19_rejections_return_no_partial_result - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p41_cutoff_identity.py::test_p41_01_naive_and_aware_same_instant_share_identity - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p41_cutoff_identity.py::test_p41_02_tz_offset_equivalent_shares_identity - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p41_cutoff_identity.py::test_p41_03_iso_string_equivalent_shares_identity - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p41_cutoff_identity.py::test_p41_04_distinct_instants_stay_distinct - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p41_cutoff_identity.py::test_p41_05_equivalent_cutoffs_collide_quarantine_wholesale - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p41_cutoff_identity.py::test_p41_06_pipeline_guard_accepts_equivalent_pair_single_cutoff - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p41_cutoff_identity.py::test_p41_07_three_equivalent_forms_collide_wholesale_no_winner_pick - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p41_cutoff_identity.py::test_p41_08_reordered_equivalent_cutoffs_decide_identically - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p41_cutoff_identity.py::test_p41_09_repeated_ttm_equivalent_forms_inflate_nothing - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p41_cutoff_identity.py::test_p41_10_forecast_ttm_overlap_on_cutoff_form_only - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p41_cutoff_identity.py::test_p41_11_distinct_periods_same_canonical_instant_stay_distinct - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p41_cutoff_identity.py::test_p41_12_scenario_isolation_with_mixed_equivalent_forms - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p41_cutoff_identity.py::test_p41_13_horizon_version_isolation_with_mixed_equivalent_forms - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p41_cutoff_identity.py::test_p41_14_missing_invalid_mixed_instants_fail_closed - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p41_cutoff_identity.py::test_p41_15_empty_and_ttm_only_with_equivalent_forms - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p41_cutoff_identity.py::test_p41_16_later_published_actual_stays_eligible - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_p41_cutoff_identity.py::test_p41_17_rejected_equivalent_mixed_invocation_returns_no_partial - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_reliability_governance.py::test_governed_series_withholds_reliability_even_with_components - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_reliability_governance.py::test_governed_series_without_components_withholds_performance_too - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_reliability_governance.py::test_govern_series_never_mutates_the_p19_aggregate - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_reliability_governance.py::test_suggestive_bias_evidence_still_yields_no_calibration - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_reliability_governance.py::test_pit_later_published_actual_still_governed - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_reliability_governance.py::test_horizon_and_version_isolation_survive_governance - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_reliability_governance.py::test_null_and_quarantines_flow_through_unchanged - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_reliability_governance.py::test_missing_mape_marks_unavailable_component - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_reliability_governance.py::test_regime_only_series_names_mape_unavailable - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_reliability_governance.py::test_full_path_observation_to_governance - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_scenario_isolation.py::test_keys_all_three_pairs_unequal - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_scenario_isolation.py::test_keys_preserve_canonical_scenario - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_scenario_isolation.py::test_keys_hash_set_dict_behavior - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_scenario_isolation.py::test_three_scenarios_yield_three_series - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_scenario_isolation.py::test_mape_bias_inputs_not_pooled_across_scenarios - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_scenario_isolation.py::test_series_evaluation_carries_scenario - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_scenario_isolation.py::test_baseline_pairing_stays_within_scenario - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_scenario_isolation.py::test_baseline_absent_in_other_scenarios - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_scenario_isolation.py::test_empty_scenario_record_raises_fail_closed - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_scenario_isolation.py::test_noncanonical_scenario_preserved_verbatim_and_isolated - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_scenario_isolation.py::test_single_scenario_values_unchanged - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_scenario_isolation.py::test_three_scenarios_not_three_observations_in_shared_series - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_scenario_isolation.py::test_insertion_order_all_six_permutations - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_scenario_isolation.py::test_interleaved_multi_company_inputs - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_scenario_isolation.py::test_duplicate_within_one_scenario_quarantines_only_that_scenario - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_scenario_isolation.py::test_identical_values_across_scenarios_still_separate - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_scenario_isolation.py::test_single_scenario_input_one_series - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_scenario_isolation.py::test_pipeline_three_scenarios_end_to_end - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
FAILED src/tests/test_stage6_scenario_isolation.py::test_pipeline_baseline_pairing_per_scenario - TypeError: ForecastRecord.__init__() got an unexpected keyword argument 'forecast_id'
196 failed, 1687 passed in 234.54s (0:03:54)