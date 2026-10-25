(analyzer) PS D:\winprojects\analyzer> python -m pytest src/tests/test_stage7_valuation.py -v
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0 -- D:\winprojects\analyzer\Scripts\python.exe
cachedir: .pytest_cache
rootdir: D:\winprojects\analyzer
collected 91 items

src/tests/test_stage7_valuation.py::test_jalali_service_uses_selected_price_and_preserves_provenance PASSED      [  1%]
src/tests/test_stage7_valuation.py::test_jalali_service_fails_closed_without_eligible_observation PASSED         [  2%]
src/tests/test_stage7_valuation.py::test_jalali_service_rejects_forecast_from_another_company PASSED             [  3%]
src/tests/test_stage7_valuation.py::test_valuation_models PASSED                                                 [  4%]
src/tests/test_stage7_valuation.py::test_valuation_engine_forward_pe_and_expected_fair_value PASSED              [  5%]
src/tests/test_stage7_valuation.py::test_industry_forward_pe_requires_eight_valid_peers PASSED                   [  6%]
src/tests/test_stage7_valuation.py::test_industry_ttm_is_fallback_after_historical_median PASSED                 [  7%]
src/tests/test_stage7_valuation.py::test_negative_eps_does_not_create_fake_pe_or_fair_value PASSED               [  8%]
src/tests/test_stage7_valuation.py::test_reliability_does_not_change_forward_pe_or_fair_value PASSED             [  9%]
src/tests/test_stage7_valuation.py::test_direct_probability_adjustments_are_rejected_in_favor_of_family_evidence PASSED [ 10%]
src/tests/test_stage7_valuation.py::test_probability_evidence_is_family_level_and_equal_weighted PASSED          [ 12%]
src/tests/test_stage7_valuation.py::test_probability_evidence_rejects_unknown_or_incomplete_family_data PASSED   [ 13%]
src/tests/test_stage7_valuation.py::test_scenario_multiple_adjustments_require_economic_rationale_and_are_bounded PASSED [ 14%]
src/tests/test_stage7_valuation.py::test_alerts_include_severity_and_driver_focus PASSED                         [ 15%]
src/tests/test_stage7_valuation.py::test_p2_sensitivity_drivers_present_and_bounded PASSED                       [ 16%]
src/tests/test_stage7_valuation.py::test_p2_sensitivity_missing_data_empty_drivers PASSED                        [ 17%]
src/tests/test_stage7_valuation.py::test_p2_sensitivity_deterministic_repeated_runs PASSED                       [ 18%]
src/tests/test_stage7_valuation.py::test_p2_alert_severity_levels_valid PASSED                                   [ 19%]
src/tests/test_stage7_valuation.py::test_p2_alert_low_reliability_threshold_boundaries PASSED                    [ 20%]
src/tests/test_stage7_valuation.py::test_p2_alert_high_dispersion_threshold_boundaries PASSED                    [ 21%]
src/tests/test_stage7_valuation.py::test_p2_alert_divergence_ratios_boundaries PASSED                            [ 23%]
src/tests/test_stage7_valuation.py::test_v1_sector_examples_use_only_eps_and_target_pe_drivers PASSED            [ 24%]
src/tests/test_stage7_valuation.py::test_v1_uses_stage5_eps_without_recalculating_from_net_profit PASSED         [ 25%]
src/tests/test_stage7_valuation.py::test_v1_defers_undefined_flip_dependence_and_assumption_alerts PASSED        [ 26%]
src/tests/test_stage7_valuation.py::test_p3_sensitivity_recomputes_from_valuation_identity PASSED                [ 27%]
src/tests/test_stage7_valuation.py::test_p3_nan_eps_is_guarded_as_invalid PASSED                                 [ 28%]
src/tests/test_stage7_valuation.py::test_p3_zero_and_negative_price_guarded PASSED                               [ 29%]
src/tests/test_stage7_valuation.py::test_p3_nonfinite_benchmark_series_filtered PASSED                           [ 30%]
src/tests/test_stage7_valuation.py::test_p3_nonfinite_scores_fall_back_to_defaults PASSED                        [ 31%]
src/tests/test_stage7_valuation.py::test_p3_flip_dependence_alerts_remain_explicitly_unresolved PASSED           [ 32%]
src/tests/test_stage7_valuation.py::test_p4_peer_count_below_minimum_falls_back PASSED                           [ 34%]
src/tests/test_stage7_valuation.py::test_p4_peer_count_at_minimum_selects_industry_forward PASSED                [ 35%]
src/tests/test_stage7_valuation.py::test_p4_peer_count_above_minimum_and_median_provenance PASSED                [ 36%]
src/tests/test_stage7_valuation.py::test_p4_peer_count_filters_invalid_values PASSED                             [ 37%]
src/tests/test_stage7_valuation.py::test_p4_peer_count_empty_data_reports_zero_and_falls_back PASSED             [ 38%]
src/tests/test_stage7_valuation.py::test_p4_benchmark_fallback_ignores_forward_count_for_ttm PASSED              [ 39%]
src/tests/test_stage7_valuation.py::test_p5_nonfinite_price_yields_null_outputs PASSED                           [ 40%]
src/tests/test_stage7_valuation.py::test_p5_missing_eps_is_not_applicable_not_zero PASSED                        [ 41%]
src/tests/test_stage7_valuation.py::test_p5_nonfinite_reliability_echo_sanitized PASSED                          [ 42%]
src/tests/test_stage7_valuation.py::test_p5_nonfinite_probability_confidence_echo_finite PASSED                  [ 43%]
src/tests/test_stage7_valuation.py::test_p5_missing_data_quality_does_not_crash PASSED                           [ 45%]
src/tests/test_stage7_valuation.py::test_p5_nonfinite_multiple_adjustment_rejected PASSED                        [ 46%]
src/tests/test_stage7_valuation.py::test_p5_nan_probability_evidence_rejected PASSED                             [ 47%]
src/tests/test_stage7_valuation.py::test_p5_datetime_echoes_normalized_to_utc PASSED                             [ 48%]
src/tests/test_stage7_valuation.py::test_p5_default_cutoff_inherits_forecast_cutoff_normalized PASSED            [ 49%]
src/tests/test_stage7_valuation.py::test_p5_undated_benchmark_series_carry_no_provenance PASSED                  [ 50%]
src/tests/test_stage7_valuation.py::test_p6_production_path_real_stage5_forecast PASSED                          [ 51%]
src/tests/test_stage7_valuation.py::test_p6_cutoff_pit_limitation_pinned PASSED                                  [ 52%]
src/tests/test_stage7_valuation.py::test_p6_missing_benchmarks_yield_guarded_nulls PASSED                        [ 53%]
src/tests/test_stage7_valuation.py::test_p6_scenario_ordering_flag_and_probability_normalization PASSED          [ 54%]
src/tests/test_stage7_valuation.py::test_p6_invalid_eps_variants_never_fabricate_values PASSED                   [ 56%]
src/tests/test_stage7_valuation.py::test_p6_repeat_runs_identical_on_full_contract PASSED                        [ 57%]
src/tests/test_stage7_valuation.py::test_p6_regression_prior_behavior_preserved PASSED                           [ 58%]
src/tests/test_stage7_valuation.py::test_p10_expensive_base_upside_parameterized_outputs_unchanged PASSED        [ 59%]
src/tests/test_stage7_valuation.py::test_p10_expensive_threshold_consumed_from_parameters PASSED                 [ 60%]
src/tests/test_stage7_valuation.py::test_p12_calculation_timestamp_utc_aware_and_deterministic PASSED            [ 61%]
src/tests/test_stage7_valuation.py::test_p32_input_refs_before_cutoff_leave_results_unchanged PASSED             [ 62%]
src/tests/test_stage7_valuation.py::test_p32_input_ref_after_cutoff_rejected_on_valuation_path PASSED            [ 63%]
src/tests/test_stage7_valuation.py::test_p32_input_ref_at_cutoff_boundary_accepted PASSED                        [ 64%]
src/tests/test_stage7_valuation.py::test_p32_input_ref_missing_date_rejected PASSED                              [ 65%]
src/tests/test_stage7_valuation.py::test_p32_input_refs_absent_preserves_legacy_path PASSED                      [ 67%]
src/tests/test_stage7_valuation.py::test_p53_embedded_forecast_input_ref_at_cutoff_is_enforced_and_accepted PASSED [ 68%]
src/tests/test_stage7_valuation.py::test_p53_stage5_dropped_future_input_is_not_reintroduced_to_stage7 PASSED    [ 69%]
src/tests/test_stage7_valuation.py::test_p53_embedded_forecast_input_ref_without_availability_is_rejected PASSED [ 70%]
src/tests/test_stage7_valuation.py::test_p53_explicit_empty_refs_do_not_bypass_embedded_forecast_provenance PASSED [ 71%]
src/tests/test_stage7_valuation.py::test_p53_stage5_forecast_without_provenance_preserves_legacy_path PASSED     [ 72%]
src/tests/test_stage7_valuation.py::test_p33_genesis_snapshot_matches_live_constants PASSED                      [ 73%]
src/tests/test_stage7_valuation.py::test_p33_result_carries_parameter_audit PASSED                               [ 74%]
src/tests/test_stage7_valuation.py::test_p33_resolve_exact_key_and_missing_raises PASSED                         [ 75%]
src/tests/test_stage7_valuation.py::test_p33_as_of_without_dated_records_raises PASSED                           [ 76%]
src/tests/test_stage7_valuation.py::test_p33_as_of_selection_mechanics PASSED                                    [ 78%]
src/tests/test_stage7_valuation.py::test_p33_as_of_overlap_raises_ambiguity PASSED                               [ 79%]
src/tests/test_stage7_valuation.py::test_p35_legacy_path_provenance_is_truthful_and_unchanged PASSED             [ 80%]
src/tests/test_stage7_valuation.py::test_p35_snapshot_reports_values_actually_consumed_when_module_constant_changes PASSED [ 81%]
src/tests/test_stage7_valuation.py::test_p35_as_of_selection_governs_calculation_and_snapshot_matches FAILED     [ 82%]
src/tests/test_stage7_valuation.py::test_p35_selected_set_governs_peers_alerts_and_scenario_weights FAILED       [ 83%]
src/tests/test_stage7_valuation.py::test_p35_missing_or_ambiguous_as_of_selection_fails_closed FAILED            [ 84%]
src/tests/test_stage7_valuation.py::test_p35_invalid_parameter_set_raises_without_fallback_to_constants FAILED   [ 85%]
src/tests/test_stage7_valuation.py::test_p35_isolation_from_global_mutation_and_snapshot_aliasing FAILED         [ 86%]
src/tests/test_stage7_valuation.py::test_p35_repeated_as_of_calculations_are_deterministic FAILED                [ 87%]
src/tests/test_stage7_valuation.py::test_p54_cutoff_governs_parameter_selection PASSED                           [ 89%]
src/tests/test_stage7_valuation.py::test_p54_valuation_date_does_not_substitute_for_cutoff PASSED                [ 90%]
src/tests/test_stage7_valuation.py::test_p54_effective_from_boundary_accepted_exactly PASSED                     [ 91%]
src/tests/test_stage7_valuation.py::test_p54_future_effective_version_never_selected PASSED                      [ 92%]
src/tests/test_stage7_valuation.py::test_p54_missing_eligible_dated_version_raises PASSED                        [ 93%]
src/tests/test_stage7_valuation.py::test_p54_overlapping_eligible_versions_raise PASSED                          [ 94%]
src/tests/test_stage7_valuation.py::test_p54_conflicting_explicit_as_of_and_cutoff_rejected PASSED               [ 95%]
src/tests/test_stage7_valuation.py::test_p54_matching_as_of_and_cutoff_accepted PASSED                           [ 96%]
src/tests/test_stage7_valuation.py::test_p54_metadata_distinguishes_dated_from_legacy PASSED                     [ 97%]
src/tests/test_stage7_valuation.py::test_p54_repeated_cutoff_calculations_deterministic PASSED                   [ 98%]
src/tests/test_stage7_valuation.py::test_p54_legacy_path_backward_compatible_without_pit_claim PASSED            [100%]

====================================================== FAILURES =======================================================
__________________________ test_p35_as_of_selection_governs_calculation_and_snapshot_matches __________________________

    def test_p35_as_of_selection_governs_calculation_and_snapshot_matches():
        from datetime import datetime as dt

        v1 = _p35_version("TEST/V1", dt(2025, 1, 1))
        v2 = _p35_version(
            "TEST/V2", dt(2026, 1, 1),
            overrides={"VALUATION_THRESHOLDS.expensive_base_upside": -50.0, "MODEL_VERSION": "TEST_MODEL_V2"},
        )
        registry = _p35_registry(v1, v2)
        # D9: parameter_as_of must agree with the effective data cutoff (2026-01-01
        # from make_forecast). Use cutoff-matching as_of values so the cutoff and
        # the caller-supplied instant are identical.
        historical = _p35_call(
            parameter_registry=registry,
            parameter_as_of=dt(2026, 1, 1),
            data_cutoff_datetime=dt(2026, 1, 1),
        )
        # For V2-effective selection, provide a matching cutoff at V2's effective date.
        current = _p35_call(
            parameter_registry=registry,
            parameter_as_of=dt(2026, 6, 1),
            data_cutoff_datetime=dt(2026, 6, 1),
        )
        # At cutoff=2026-01-01, V2 (effective 2026-01-01) is selected; the value
        # override changes the classification relative to the pre-V2 semantics
        # only for expected upside at the same cutoff.
        assert historical.metadata["parameter_set_version"] == "TEST/V2"
        assert current.metadata["parameter_set_version"] == "TEST/V2"
        assert historical.metadata["parameter_snapshot"]["VALUATION_THRESHOLDS.expensive_base_upside"] == -50.0
        assert current.metadata["parameter_snapshot"]["VALUATION_THRESHOLDS.expensive_base_upside"] == -50.0
        # To demonstrate V1 vs V2 divergence, use a cutoff before V2's effective date.
        pre_v2 = _p35_call(
            parameter_registry=registry,
            parameter_as_of=dt(2025, 6, 1),
            data_cutoff_datetime=dt(2025, 6, 1),
        )
        assert pre_v2.metadata["parameter_set_version"] == "TEST/V1"
        assert pre_v2.valuation_status == "EXPENSIVE"
        assert pre_v2.model_version == "STAGE7_V1"
        selection = current.metadata["parameter_selection"]
        assert selection["mode"] == "AS_OF_EFFECTIVE_DATED"
        assert selection["point_in_time_selection_applied"] is True
        # assert selection["as_of_requested"] == "2026-06-01T00:00:00+00:00"
>       assert selection["as_of_requested"] == "2026-01-01T00:00:00+00:00"
E       AssertionError: assert '2026-06-01T00:00:00+00:00' == '2026-01-01T00:00:00+00:00'
E
E         - 2026-01-01T00:00:00+00:00
E         ?       ^
E         + 2026-06-01T00:00:00+00:00
E         ?       ^

src\tests\test_stage7_valuation.py:1685: AssertionError
___________________________ test_p35_selected_set_governs_peers_alerts_and_scenario_weights ___________________________

    def test_p35_selected_set_governs_peers_alerts_and_scenario_weights():
        from datetime import datetime as dt

        kwargs = dict(
            forecast_result=make_forecast(),
            forecast_reliability_score=50.0,
            industry_forward_pe_values=[10.0, 10.0, 10.0],
            historical_pe_values=[7.0],
        )
        default = _p35_call(**kwargs)
        assert default.target_pe_source == "HISTORICAL_MEDIAN_PE"
        assert "INSUFFICIENT_PEER_DATA" in default.valuation_risk_flags
        assert "LOW_FORECAST_RELIABILITY" not in default.valuation_risk_flags
        v2 = _p35_version(
            "TEST/V2", dt(2026, 1, 1),
            overrides={
                "MIN_INDUSTRY_PEERS": 3,
                "ALERT_THRESHOLDS.low_forecast_reliability": 60.0,
                "SCENARIO_WEIGHTS.bear": 0.5, "SCENARIO_WEIGHTS.base": 0.3, "SCENARIO_WEIGHTS.bull": 0.2,
            },
        )
>       selected = _p35_call(parameter_registry=_p35_registry(v2), parameter_as_of=dt(2026, 6, 1), **kwargs)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage7_valuation.py:1713:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage7_valuation.py:1597: in _p35_call
    return ValuationEngine().calculate_valuation(**base)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\valuation\engine.py:85: in calculate_valuation
    selected_version, selection_meta = select_parameter_set_for_valuation(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

parameter_registry = ParameterRegistry(versions=(ParameterSetVersion(model_version='STAGE7_V1', version_key='TEST/V2', effective_from=datet...unused in V1. Genesis record: temporal validity unknown; never valid for historical date selection (R8 pending).'))),))
parameter_as_of = datetime.datetime(2026, 6, 1, 0, 0)
effective_data_cutoff = datetime.datetime(2026, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)

    def select_parameter_set_for_valuation(
        parameter_registry: Optional[ParameterRegistry] = None,
        parameter_as_of: Optional[datetime] = None,
        *,
        effective_data_cutoff: Optional[datetime] = None,
    ) -> Tuple[ParameterSetVersion, Dict[str, object]]:
        """Choose the parameter set for one valuation, with truthful provenance.

        Selection precedence (D9):

        * No registry and no as-of: legacy Genesis path, labelled
          ``FIXED_GENESIS_LEGACY``; ``data_cutoff_used_for_parameter_selection``
          is ``False`` and the caveat states that temporal validity is NOT
          verified. This never claims historical validity.
        * A caller-supplied ``parameter_as_of`` that disagrees with
          ``effective_data_cutoff`` raises ``ValueError`` — no silent selection
          using a conflicting timestamp.
        * When ``effective_data_cutoff`` is present it is the governing timestamp
          for dated selection; ``data_cutoff_used_for_parameter_selection`` is
          ``True`` and ``as_of_source`` is ``DATA_CUTOFF``.
        * With no cutoff but an explicit ``parameter_as_of``, selection proceeds
          on the caller-supplied instant and the provenance records
          ``as_of_source == "CALLER_SUPPLIED"`` and
          ``data_cutoff_used_for_parameter_selection == False`` — no cutoff is
          invented.
        * With neither cutoff nor as-of (but a registry), a ``LookupError`` is
          raised; selection without a governing instant is undefined.

        Dated selection is delegated to ``resolve_parameter_set_as_of``:
        undated genesis records never stand in for history, future-effective
        versions never leak in, and overlapping effective dates raise instead of
        picking silently.

        Which date governs selection in production (cutoff, valuation date, or
        another instant) remains the R8/D9 decision; the caller supplies
        ``effective_data_cutoff`` explicitly and provenance records it as such.
        """
        cutoff_norm: Optional[datetime] = (
            None if effective_data_cutoff is None else normalize_datetime(effective_data_cutoff)
        )
        as_of_norm: Optional[datetime] = (
            None if parameter_as_of is None else normalize_datetime(parameter_as_of)
        )

        if parameter_registry is None and as_of_norm is None:
            # Legacy Genesis path (backward compatible). If the caller supplied a
            # cutoff but no registry, we still cannot select a dated set (the
            # default registry only contains undated genesis); the honest answer
            # is the legacy path with an explicit unverified marker.
            live = live_genesis_parameter_set()
            live_values = {r.parameter_name: r.parameter_value for r in live.records}
            import_values = {r.parameter_name: r.parameter_value for r in GENESIS_VERSION.records}
            return live, {
                "mode": "FIXED_GENESIS_LEGACY",
                "point_in_time_selection_applied": False,
                "as_of_requested": None if cutoff_norm is None else cutoff_norm.isoformat(),
                "as_of_source": None,
                "data_cutoff_used_for_parameter_selection": False,
                "module_constants_modified_since_import": live_values != import_values,
                "caveat": (
                    "Undated genesis constants; temporal validity for historical "
                    "valuation is NOT verified (R8/D9 pending)."
                ),
            }

        registry = DEFAULT_REGISTRY if parameter_registry is None else parameter_registry

        # Conflict detection: an explicitly-supplied as-of must agree with the
        # effective data cutoff, otherwise we would be selecting parameters using
        # a timestamp that contradicts the governing data cutoff.
        if as_of_norm is not None and cutoff_norm is not None and as_of_norm != cutoff_norm:
>           raise ValueError(
                "parameter_as_of conflicts with the effective valuation data cutoff "
                f"(parameter_as_of={as_of_norm.isoformat()}, "
                f"effective_data_cutoff={cutoff_norm.isoformat()}); refusing to "
                "select parameters using a conflicting timestamp."
            )
E           ValueError: parameter_as_of conflicts with the effective valuation data cutoff (parameter_as_of=2026-06-01T00:00:00+00:00, effective_data_cutoff=2026-01-01T00:00:00+00:00); refusing to select parameters using a conflicting timestamp.

src\valuation\parameters.py:522: ValueError
_____________________________ test_p35_missing_or_ambiguous_as_of_selection_fails_closed ______________________________

    def test_p35_missing_or_ambiguous_as_of_selection_fails_closed():
        from datetime import datetime as dt

        v1 = _p35_version("TEST/V1", dt(2025, 1, 1))
        # Cutoff before every dated version → LookupError from resolve.
        with pytest.raises(LookupError):
            _p35_call(
                parameter_registry=_p35_registry(v1),
                parameter_as_of=dt(2024, 1, 1),
                data_cutoff_datetime=dt(2024, 1, 1),
            )
        # Registry supplied with no cutoff and no as-of: no governing instant →
        # LookupError (none is inferred).
>       with pytest.raises(LookupError, match="effective_data_cutoff|as-of"):
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       Failed: DID NOT RAISE LookupError

src\tests\test_stage7_valuation.py:1736: Failed
_________________________ test_p35_invalid_parameter_set_raises_without_fallback_to_constants _________________________

    def test_p35_invalid_parameter_set_raises_without_fallback_to_constants():
        from datetime import datetime as dt
        from src.valuation.parameters import ParameterSetInvalidError

        when = dt(2026, 6, 1)
        cases = (
            _p35_version("TEST/MISSING", dt(2026, 1, 1), drop=("MIN_INDUSTRY_PEERS",)),
            _p35_version("TEST/NAN", dt(2026, 1, 1), overrides={"RISK_THRESHOLDS.high_bear_downside": float("nan")}),
            _p35_version("TEST/BOOL", dt(2026, 1, 1), overrides={"SENSITIVITY_PERTURBATION": True}),
            _p35_version("TEST/DUP", dt(2026, 1, 1), duplicate="MIN_INDUSTRY_PEERS"),
        )
        for version in cases:
            with pytest.raises(ParameterSetInvalidError):
>               _p35_call(parameter_registry=_p35_registry(version), parameter_as_of=when)

src\tests\test_stage7_valuation.py:1764:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage7_valuation.py:1597: in _p35_call
    return ValuationEngine().calculate_valuation(**base)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\valuation\engine.py:85: in calculate_valuation
    selected_version, selection_meta = select_parameter_set_for_valuation(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

parameter_registry = ParameterRegistry(versions=(ParameterSetVersion(model_version='STAGE7_V1', version_key='TEST/MISSING', effective_from=...unused in V1. Genesis record: temporal validity unknown; never valid for historical date selection (R8 pending).'))),))
parameter_as_of = datetime.datetime(2026, 6, 1, 0, 0)
effective_data_cutoff = datetime.datetime(2026, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)

    def select_parameter_set_for_valuation(
        parameter_registry: Optional[ParameterRegistry] = None,
        parameter_as_of: Optional[datetime] = None,
        *,
        effective_data_cutoff: Optional[datetime] = None,
    ) -> Tuple[ParameterSetVersion, Dict[str, object]]:
        """Choose the parameter set for one valuation, with truthful provenance.

        Selection precedence (D9):

        * No registry and no as-of: legacy Genesis path, labelled
          ``FIXED_GENESIS_LEGACY``; ``data_cutoff_used_for_parameter_selection``
          is ``False`` and the caveat states that temporal validity is NOT
          verified. This never claims historical validity.
        * A caller-supplied ``parameter_as_of`` that disagrees with
          ``effective_data_cutoff`` raises ``ValueError`` — no silent selection
          using a conflicting timestamp.
        * When ``effective_data_cutoff`` is present it is the governing timestamp
          for dated selection; ``data_cutoff_used_for_parameter_selection`` is
          ``True`` and ``as_of_source`` is ``DATA_CUTOFF``.
        * With no cutoff but an explicit ``parameter_as_of``, selection proceeds
          on the caller-supplied instant and the provenance records
          ``as_of_source == "CALLER_SUPPLIED"`` and
          ``data_cutoff_used_for_parameter_selection == False`` — no cutoff is
          invented.
        * With neither cutoff nor as-of (but a registry), a ``LookupError`` is
          raised; selection without a governing instant is undefined.

        Dated selection is delegated to ``resolve_parameter_set_as_of``:
        undated genesis records never stand in for history, future-effective
        versions never leak in, and overlapping effective dates raise instead of
        picking silently.

        Which date governs selection in production (cutoff, valuation date, or
        another instant) remains the R8/D9 decision; the caller supplies
        ``effective_data_cutoff`` explicitly and provenance records it as such.
        """
        cutoff_norm: Optional[datetime] = (
            None if effective_data_cutoff is None else normalize_datetime(effective_data_cutoff)
        )
        as_of_norm: Optional[datetime] = (
            None if parameter_as_of is None else normalize_datetime(parameter_as_of)
        )

        if parameter_registry is None and as_of_norm is None:
            # Legacy Genesis path (backward compatible). If the caller supplied a
            # cutoff but no registry, we still cannot select a dated set (the
            # default registry only contains undated genesis); the honest answer
            # is the legacy path with an explicit unverified marker.
            live = live_genesis_parameter_set()
            live_values = {r.parameter_name: r.parameter_value for r in live.records}
            import_values = {r.parameter_name: r.parameter_value for r in GENESIS_VERSION.records}
            return live, {
                "mode": "FIXED_GENESIS_LEGACY",
                "point_in_time_selection_applied": False,
                "as_of_requested": None if cutoff_norm is None else cutoff_norm.isoformat(),
                "as_of_source": None,
                "data_cutoff_used_for_parameter_selection": False,
                "module_constants_modified_since_import": live_values != import_values,
                "caveat": (
                    "Undated genesis constants; temporal validity for historical "
                    "valuation is NOT verified (R8/D9 pending)."
                ),
            }

        registry = DEFAULT_REGISTRY if parameter_registry is None else parameter_registry

        # Conflict detection: an explicitly-supplied as-of must agree with the
        # effective data cutoff, otherwise we would be selecting parameters using
        # a timestamp that contradicts the governing data cutoff.
        if as_of_norm is not None and cutoff_norm is not None and as_of_norm != cutoff_norm:
>           raise ValueError(
                "parameter_as_of conflicts with the effective valuation data cutoff "
                f"(parameter_as_of={as_of_norm.isoformat()}, "
                f"effective_data_cutoff={cutoff_norm.isoformat()}); refusing to "
                "select parameters using a conflicting timestamp."
            )
E           ValueError: parameter_as_of conflicts with the effective valuation data cutoff (parameter_as_of=2026-06-01T00:00:00+00:00, effective_data_cutoff=2026-01-01T00:00:00+00:00); refusing to select parameters using a conflicting timestamp.

src\valuation\parameters.py:522: ValueError
____________________________ test_p35_isolation_from_global_mutation_and_snapshot_aliasing ____________________________

    def test_p35_isolation_from_global_mutation_and_snapshot_aliasing():
        import dataclasses

        from src.valuation import parameters as params
        from src.valuation.parameters import consume_parameter_set, live_genesis_parameter_set

        v2 = _p35_version("TEST/V2", datetime(2026, 1, 1))
        kwargs = dict(parameter_registry=_p35_registry(v2), parameter_as_of=datetime(2026, 6, 1))
>       before = _p35_call(**kwargs)
                 ^^^^^^^^^^^^^^^^^^^

src\tests\test_stage7_valuation.py:1777:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage7_valuation.py:1597: in _p35_call
    return ValuationEngine().calculate_valuation(**base)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\valuation\engine.py:85: in calculate_valuation
    selected_version, selection_meta = select_parameter_set_for_valuation(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

parameter_registry = ParameterRegistry(versions=(ParameterSetVersion(model_version='STAGE7_V1', version_key='TEST/V2', effective_from=datet...unused in V1. Genesis record: temporal validity unknown; never valid for historical date selection (R8 pending).'))),))
parameter_as_of = datetime.datetime(2026, 6, 1, 0, 0)
effective_data_cutoff = datetime.datetime(2026, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)

    def select_parameter_set_for_valuation(
        parameter_registry: Optional[ParameterRegistry] = None,
        parameter_as_of: Optional[datetime] = None,
        *,
        effective_data_cutoff: Optional[datetime] = None,
    ) -> Tuple[ParameterSetVersion, Dict[str, object]]:
        """Choose the parameter set for one valuation, with truthful provenance.

        Selection precedence (D9):

        * No registry and no as-of: legacy Genesis path, labelled
          ``FIXED_GENESIS_LEGACY``; ``data_cutoff_used_for_parameter_selection``
          is ``False`` and the caveat states that temporal validity is NOT
          verified. This never claims historical validity.
        * A caller-supplied ``parameter_as_of`` that disagrees with
          ``effective_data_cutoff`` raises ``ValueError`` — no silent selection
          using a conflicting timestamp.
        * When ``effective_data_cutoff`` is present it is the governing timestamp
          for dated selection; ``data_cutoff_used_for_parameter_selection`` is
          ``True`` and ``as_of_source`` is ``DATA_CUTOFF``.
        * With no cutoff but an explicit ``parameter_as_of``, selection proceeds
          on the caller-supplied instant and the provenance records
          ``as_of_source == "CALLER_SUPPLIED"`` and
          ``data_cutoff_used_for_parameter_selection == False`` — no cutoff is
          invented.
        * With neither cutoff nor as-of (but a registry), a ``LookupError`` is
          raised; selection without a governing instant is undefined.

        Dated selection is delegated to ``resolve_parameter_set_as_of``:
        undated genesis records never stand in for history, future-effective
        versions never leak in, and overlapping effective dates raise instead of
        picking silently.

        Which date governs selection in production (cutoff, valuation date, or
        another instant) remains the R8/D9 decision; the caller supplies
        ``effective_data_cutoff`` explicitly and provenance records it as such.
        """
        cutoff_norm: Optional[datetime] = (
            None if effective_data_cutoff is None else normalize_datetime(effective_data_cutoff)
        )
        as_of_norm: Optional[datetime] = (
            None if parameter_as_of is None else normalize_datetime(parameter_as_of)
        )

        if parameter_registry is None and as_of_norm is None:
            # Legacy Genesis path (backward compatible). If the caller supplied a
            # cutoff but no registry, we still cannot select a dated set (the
            # default registry only contains undated genesis); the honest answer
            # is the legacy path with an explicit unverified marker.
            live = live_genesis_parameter_set()
            live_values = {r.parameter_name: r.parameter_value for r in live.records}
            import_values = {r.parameter_name: r.parameter_value for r in GENESIS_VERSION.records}
            return live, {
                "mode": "FIXED_GENESIS_LEGACY",
                "point_in_time_selection_applied": False,
                "as_of_requested": None if cutoff_norm is None else cutoff_norm.isoformat(),
                "as_of_source": None,
                "data_cutoff_used_for_parameter_selection": False,
                "module_constants_modified_since_import": live_values != import_values,
                "caveat": (
                    "Undated genesis constants; temporal validity for historical "
                    "valuation is NOT verified (R8/D9 pending)."
                ),
            }

        registry = DEFAULT_REGISTRY if parameter_registry is None else parameter_registry

        # Conflict detection: an explicitly-supplied as-of must agree with the
        # effective data cutoff, otherwise we would be selecting parameters using
        # a timestamp that contradicts the governing data cutoff.
        if as_of_norm is not None and cutoff_norm is not None and as_of_norm != cutoff_norm:
>           raise ValueError(
                "parameter_as_of conflicts with the effective valuation data cutoff "
                f"(parameter_as_of={as_of_norm.isoformat()}, "
                f"effective_data_cutoff={cutoff_norm.isoformat()}); refusing to "
                "select parameters using a conflicting timestamp."
            )
E           ValueError: parameter_as_of conflicts with the effective valuation data cutoff (parameter_as_of=2026-06-01T00:00:00+00:00, effective_data_cutoff=2026-01-01T00:00:00+00:00); refusing to select parameters using a conflicting timestamp.

src\valuation\parameters.py:522: ValueError
_______________________________ test_p35_repeated_as_of_calculations_are_deterministic ________________________________

    def test_p35_repeated_as_of_calculations_are_deterministic():
        import dataclasses

        registry = _p35_registry(_p35_version("TEST/V1", datetime(2025, 1, 1)))
        runs = []
        for _ in range(3):
>           result = _p35_call(parameter_registry=registry, parameter_as_of=datetime(2025, 6, 1))
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage7_valuation.py:1811:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage7_valuation.py:1597: in _p35_call
    return ValuationEngine().calculate_valuation(**base)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\valuation\engine.py:85: in calculate_valuation
    selected_version, selection_meta = select_parameter_set_for_valuation(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

parameter_registry = ParameterRegistry(versions=(ParameterSetVersion(model_version='STAGE7_V1', version_key='TEST/V1', effective_from=datet...unused in V1. Genesis record: temporal validity unknown; never valid for historical date selection (R8 pending).'))),))
parameter_as_of = datetime.datetime(2025, 6, 1, 0, 0)
effective_data_cutoff = datetime.datetime(2026, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)

    def select_parameter_set_for_valuation(
        parameter_registry: Optional[ParameterRegistry] = None,
        parameter_as_of: Optional[datetime] = None,
        *,
        effective_data_cutoff: Optional[datetime] = None,
    ) -> Tuple[ParameterSetVersion, Dict[str, object]]:
        """Choose the parameter set for one valuation, with truthful provenance.

        Selection precedence (D9):

        * No registry and no as-of: legacy Genesis path, labelled
          ``FIXED_GENESIS_LEGACY``; ``data_cutoff_used_for_parameter_selection``
          is ``False`` and the caveat states that temporal validity is NOT
          verified. This never claims historical validity.
        * A caller-supplied ``parameter_as_of`` that disagrees with
          ``effective_data_cutoff`` raises ``ValueError`` — no silent selection
          using a conflicting timestamp.
        * When ``effective_data_cutoff`` is present it is the governing timestamp
          for dated selection; ``data_cutoff_used_for_parameter_selection`` is
          ``True`` and ``as_of_source`` is ``DATA_CUTOFF``.
        * With no cutoff but an explicit ``parameter_as_of``, selection proceeds
          on the caller-supplied instant and the provenance records
          ``as_of_source == "CALLER_SUPPLIED"`` and
          ``data_cutoff_used_for_parameter_selection == False`` — no cutoff is
          invented.
        * With neither cutoff nor as-of (but a registry), a ``LookupError`` is
          raised; selection without a governing instant is undefined.

        Dated selection is delegated to ``resolve_parameter_set_as_of``:
        undated genesis records never stand in for history, future-effective
        versions never leak in, and overlapping effective dates raise instead of
        picking silently.

        Which date governs selection in production (cutoff, valuation date, or
        another instant) remains the R8/D9 decision; the caller supplies
        ``effective_data_cutoff`` explicitly and provenance records it as such.
        """
        cutoff_norm: Optional[datetime] = (
            None if effective_data_cutoff is None else normalize_datetime(effective_data_cutoff)
        )
        as_of_norm: Optional[datetime] = (
            None if parameter_as_of is None else normalize_datetime(parameter_as_of)
        )

        if parameter_registry is None and as_of_norm is None:
            # Legacy Genesis path (backward compatible). If the caller supplied a
            # cutoff but no registry, we still cannot select a dated set (the
            # default registry only contains undated genesis); the honest answer
            # is the legacy path with an explicit unverified marker.
            live = live_genesis_parameter_set()
            live_values = {r.parameter_name: r.parameter_value for r in live.records}
            import_values = {r.parameter_name: r.parameter_value for r in GENESIS_VERSION.records}
            return live, {
                "mode": "FIXED_GENESIS_LEGACY",
                "point_in_time_selection_applied": False,
                "as_of_requested": None if cutoff_norm is None else cutoff_norm.isoformat(),
                "as_of_source": None,
                "data_cutoff_used_for_parameter_selection": False,
                "module_constants_modified_since_import": live_values != import_values,
                "caveat": (
                    "Undated genesis constants; temporal validity for historical "
                    "valuation is NOT verified (R8/D9 pending)."
                ),
            }

        registry = DEFAULT_REGISTRY if parameter_registry is None else parameter_registry

        # Conflict detection: an explicitly-supplied as-of must agree with the
        # effective data cutoff, otherwise we would be selecting parameters using
        # a timestamp that contradicts the governing data cutoff.
        if as_of_norm is not None and cutoff_norm is not None and as_of_norm != cutoff_norm:
>           raise ValueError(
                "parameter_as_of conflicts with the effective valuation data cutoff "
                f"(parameter_as_of={as_of_norm.isoformat()}, "
                f"effective_data_cutoff={cutoff_norm.isoformat()}); refusing to "
                "select parameters using a conflicting timestamp."
            )
E           ValueError: parameter_as_of conflicts with the effective valuation data cutoff (parameter_as_of=2025-06-01T00:00:00+00:00, effective_data_cutoff=2026-01-01T00:00:00+00:00); refusing to select parameters using a conflicting timestamp.

src\valuation\parameters.py:522: ValueError
=============================================== short test summary info ===============================================
FAILED src/tests/test_stage7_valuation.py::test_p35_as_of_selection_governs_calculation_and_snapshot_matches - AssertionError: assert '2026-06-01T00:00:00+00:00' == '2026-01-01T00:00:00+00:00'
FAILED src/tests/test_stage7_valuation.py::test_p35_selected_set_governs_peers_alerts_and_scenario_weights - ValueError: parameter_as_of conflicts with the effective valuation data cutoff (parameter_as_of=2026-06-01T00:00:00...
FAILED src/tests/test_stage7_valuation.py::test_p35_missing_or_ambiguous_as_of_selection_fails_closed - Failed: DID NOT RAISE LookupError
FAILED src/tests/test_stage7_valuation.py::test_p35_invalid_parameter_set_raises_without_fallback_to_constants - ValueError: parameter_as_of conflicts with the effective valuation data cutoff (parameter_as_of=2026-06-01T00:00:00...
FAILED src/tests/test_stage7_valuation.py::test_p35_isolation_from_global_mutation_and_snapshot_aliasing - ValueError: parameter_as_of conflicts with the effective valuation data cutoff (parameter_as_of=2026-06-01T00:00:00...
FAILED src/tests/test_stage7_valuation.py::test_p35_repeated_as_of_calculations_are_deterministic - ValueError: parameter_as_of conflicts with the effective valuation data cutoff (parameter_as_of=2025-06-01T00:00:00...
============================================ 6 failed, 85 passed in 3.16s =============================================
(analyzer) PS D:\winprojects\analyzer> python -m pytest src/tests/test_stage7_valuation.py -v -k "p54 or p35"
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0 -- D:\winprojects\analyzer\Scripts\python.exe
cachedir: .pytest_cache
rootdir: D:\winprojects\analyzer
collected 91 items / 72 deselected / 19 selected

src/tests/test_stage7_valuation.py::test_p35_legacy_path_provenance_is_truthful_and_unchanged PASSED             [  5%]
src/tests/test_stage7_valuation.py::test_p35_snapshot_reports_values_actually_consumed_when_module_constant_changes PASSED [ 10%]
src/tests/test_stage7_valuation.py::test_p35_as_of_selection_governs_calculation_and_snapshot_matches FAILED     [ 15%]
src/tests/test_stage7_valuation.py::test_p35_selected_set_governs_peers_alerts_and_scenario_weights FAILED       [ 21%]
src/tests/test_stage7_valuation.py::test_p35_missing_or_ambiguous_as_of_selection_fails_closed FAILED            [ 26%]
src/tests/test_stage7_valuation.py::test_p35_invalid_parameter_set_raises_without_fallback_to_constants FAILED   [ 31%]
src/tests/test_stage7_valuation.py::test_p35_isolation_from_global_mutation_and_snapshot_aliasing FAILED         [ 36%]
src/tests/test_stage7_valuation.py::test_p35_repeated_as_of_calculations_are_deterministic FAILED                [ 42%]
src/tests/test_stage7_valuation.py::test_p54_cutoff_governs_parameter_selection PASSED                           [ 47%]
src/tests/test_stage7_valuation.py::test_p54_valuation_date_does_not_substitute_for_cutoff PASSED                [ 52%]
src/tests/test_stage7_valuation.py::test_p54_effective_from_boundary_accepted_exactly PASSED                     [ 57%]
src/tests/test_stage7_valuation.py::test_p54_future_effective_version_never_selected PASSED                      [ 63%]
src/tests/test_stage7_valuation.py::test_p54_missing_eligible_dated_version_raises PASSED                        [ 68%]
src/tests/test_stage7_valuation.py::test_p54_overlapping_eligible_versions_raise PASSED                          [ 73%]
src/tests/test_stage7_valuation.py::test_p54_conflicting_explicit_as_of_and_cutoff_rejected PASSED               [ 78%]
src/tests/test_stage7_valuation.py::test_p54_matching_as_of_and_cutoff_accepted PASSED                           [ 84%]
src/tests/test_stage7_valuation.py::test_p54_metadata_distinguishes_dated_from_legacy PASSED                     [ 89%]
src/tests/test_stage7_valuation.py::test_p54_repeated_cutoff_calculations_deterministic PASSED                   [ 94%]
src/tests/test_stage7_valuation.py::test_p54_legacy_path_backward_compatible_without_pit_claim PASSED            [100%]

====================================================== FAILURES =======================================================
__________________________ test_p35_as_of_selection_governs_calculation_and_snapshot_matches __________________________

    def test_p35_as_of_selection_governs_calculation_and_snapshot_matches():
        from datetime import datetime as dt

        v1 = _p35_version("TEST/V1", dt(2025, 1, 1))
        v2 = _p35_version(
            "TEST/V2", dt(2026, 1, 1),
            overrides={"VALUATION_THRESHOLDS.expensive_base_upside": -50.0, "MODEL_VERSION": "TEST_MODEL_V2"},
        )
        registry = _p35_registry(v1, v2)
        # D9: parameter_as_of must agree with the effective data cutoff (2026-01-01
        # from make_forecast). Use cutoff-matching as_of values so the cutoff and
        # the caller-supplied instant are identical.
        historical = _p35_call(
            parameter_registry=registry,
            parameter_as_of=dt(2026, 1, 1),
            data_cutoff_datetime=dt(2026, 1, 1),
        )
        # For V2-effective selection, provide a matching cutoff at V2's effective date.
        current = _p35_call(
            parameter_registry=registry,
            parameter_as_of=dt(2026, 6, 1),
            data_cutoff_datetime=dt(2026, 6, 1),
        )
        # At cutoff=2026-01-01, V2 (effective 2026-01-01) is selected; the value
        # override changes the classification relative to the pre-V2 semantics
        # only for expected upside at the same cutoff.
        assert historical.metadata["parameter_set_version"] == "TEST/V2"
        assert current.metadata["parameter_set_version"] == "TEST/V2"
        assert historical.metadata["parameter_snapshot"]["VALUATION_THRESHOLDS.expensive_base_upside"] == -50.0
        assert current.metadata["parameter_snapshot"]["VALUATION_THRESHOLDS.expensive_base_upside"] == -50.0
        # To demonstrate V1 vs V2 divergence, use a cutoff before V2's effective date.
        pre_v2 = _p35_call(
            parameter_registry=registry,
            parameter_as_of=dt(2025, 6, 1),
            data_cutoff_datetime=dt(2025, 6, 1),
        )
        assert pre_v2.metadata["parameter_set_version"] == "TEST/V1"
        assert pre_v2.valuation_status == "EXPENSIVE"
        assert pre_v2.model_version == "STAGE7_V1"
        selection = current.metadata["parameter_selection"]
        assert selection["mode"] == "AS_OF_EFFECTIVE_DATED"
        assert selection["point_in_time_selection_applied"] is True
        # assert selection["as_of_requested"] == "2026-06-01T00:00:00+00:00"
>       assert selection["as_of_requested"] == "2026-01-01T00:00:00+00:00"
E       AssertionError: assert '2026-06-01T00:00:00+00:00' == '2026-01-01T00:00:00+00:00'
E
E         - 2026-01-01T00:00:00+00:00
E         ?       ^
E         + 2026-06-01T00:00:00+00:00
E         ?       ^

src\tests\test_stage7_valuation.py:1685: AssertionError
___________________________ test_p35_selected_set_governs_peers_alerts_and_scenario_weights ___________________________

    def test_p35_selected_set_governs_peers_alerts_and_scenario_weights():
        from datetime import datetime as dt

        kwargs = dict(
            forecast_result=make_forecast(),
            forecast_reliability_score=50.0,
            industry_forward_pe_values=[10.0, 10.0, 10.0],
            historical_pe_values=[7.0],
        )
        default = _p35_call(**kwargs)
        assert default.target_pe_source == "HISTORICAL_MEDIAN_PE"
        assert "INSUFFICIENT_PEER_DATA" in default.valuation_risk_flags
        assert "LOW_FORECAST_RELIABILITY" not in default.valuation_risk_flags
        v2 = _p35_version(
            "TEST/V2", dt(2026, 1, 1),
            overrides={
                "MIN_INDUSTRY_PEERS": 3,
                "ALERT_THRESHOLDS.low_forecast_reliability": 60.0,
                "SCENARIO_WEIGHTS.bear": 0.5, "SCENARIO_WEIGHTS.base": 0.3, "SCENARIO_WEIGHTS.bull": 0.2,
            },
        )
>       selected = _p35_call(parameter_registry=_p35_registry(v2), parameter_as_of=dt(2026, 6, 1), **kwargs)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage7_valuation.py:1713:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage7_valuation.py:1597: in _p35_call
    return ValuationEngine().calculate_valuation(**base)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\valuation\engine.py:85: in calculate_valuation
    selected_version, selection_meta = select_parameter_set_for_valuation(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

parameter_registry = ParameterRegistry(versions=(ParameterSetVersion(model_version='STAGE7_V1', version_key='TEST/V2', effective_from=datet...unused in V1. Genesis record: temporal validity unknown; never valid for historical date selection (R8 pending).'))),))
parameter_as_of = datetime.datetime(2026, 6, 1, 0, 0)
effective_data_cutoff = datetime.datetime(2026, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)

    def select_parameter_set_for_valuation(
        parameter_registry: Optional[ParameterRegistry] = None,
        parameter_as_of: Optional[datetime] = None,
        *,
        effective_data_cutoff: Optional[datetime] = None,
    ) -> Tuple[ParameterSetVersion, Dict[str, object]]:
        """Choose the parameter set for one valuation, with truthful provenance.

        Selection precedence (D9):

        * No registry and no as-of: legacy Genesis path, labelled
          ``FIXED_GENESIS_LEGACY``; ``data_cutoff_used_for_parameter_selection``
          is ``False`` and the caveat states that temporal validity is NOT
          verified. This never claims historical validity.
        * A caller-supplied ``parameter_as_of`` that disagrees with
          ``effective_data_cutoff`` raises ``ValueError`` — no silent selection
          using a conflicting timestamp.
        * When ``effective_data_cutoff`` is present it is the governing timestamp
          for dated selection; ``data_cutoff_used_for_parameter_selection`` is
          ``True`` and ``as_of_source`` is ``DATA_CUTOFF``.
        * With no cutoff but an explicit ``parameter_as_of``, selection proceeds
          on the caller-supplied instant and the provenance records
          ``as_of_source == "CALLER_SUPPLIED"`` and
          ``data_cutoff_used_for_parameter_selection == False`` — no cutoff is
          invented.
        * With neither cutoff nor as-of (but a registry), a ``LookupError`` is
          raised; selection without a governing instant is undefined.

        Dated selection is delegated to ``resolve_parameter_set_as_of``:
        undated genesis records never stand in for history, future-effective
        versions never leak in, and overlapping effective dates raise instead of
        picking silently.

        Which date governs selection in production (cutoff, valuation date, or
        another instant) remains the R8/D9 decision; the caller supplies
        ``effective_data_cutoff`` explicitly and provenance records it as such.
        """
        cutoff_norm: Optional[datetime] = (
            None if effective_data_cutoff is None else normalize_datetime(effective_data_cutoff)
        )
        as_of_norm: Optional[datetime] = (
            None if parameter_as_of is None else normalize_datetime(parameter_as_of)
        )

        if parameter_registry is None and as_of_norm is None:
            # Legacy Genesis path (backward compatible). If the caller supplied a
            # cutoff but no registry, we still cannot select a dated set (the
            # default registry only contains undated genesis); the honest answer
            # is the legacy path with an explicit unverified marker.
            live = live_genesis_parameter_set()
            live_values = {r.parameter_name: r.parameter_value for r in live.records}
            import_values = {r.parameter_name: r.parameter_value for r in GENESIS_VERSION.records}
            return live, {
                "mode": "FIXED_GENESIS_LEGACY",
                "point_in_time_selection_applied": False,
                "as_of_requested": None if cutoff_norm is None else cutoff_norm.isoformat(),
                "as_of_source": None,
                "data_cutoff_used_for_parameter_selection": False,
                "module_constants_modified_since_import": live_values != import_values,
                "caveat": (
                    "Undated genesis constants; temporal validity for historical "
                    "valuation is NOT verified (R8/D9 pending)."
                ),
            }

        registry = DEFAULT_REGISTRY if parameter_registry is None else parameter_registry

        # Conflict detection: an explicitly-supplied as-of must agree with the
        # effective data cutoff, otherwise we would be selecting parameters using
        # a timestamp that contradicts the governing data cutoff.
        if as_of_norm is not None and cutoff_norm is not None and as_of_norm != cutoff_norm:
>           raise ValueError(
                "parameter_as_of conflicts with the effective valuation data cutoff "
                f"(parameter_as_of={as_of_norm.isoformat()}, "
                f"effective_data_cutoff={cutoff_norm.isoformat()}); refusing to "
                "select parameters using a conflicting timestamp."
            )
E           ValueError: parameter_as_of conflicts with the effective valuation data cutoff (parameter_as_of=2026-06-01T00:00:00+00:00, effective_data_cutoff=2026-01-01T00:00:00+00:00); refusing to select parameters using a conflicting timestamp.

src\valuation\parameters.py:522: ValueError
_____________________________ test_p35_missing_or_ambiguous_as_of_selection_fails_closed ______________________________

    def test_p35_missing_or_ambiguous_as_of_selection_fails_closed():
        from datetime import datetime as dt

        v1 = _p35_version("TEST/V1", dt(2025, 1, 1))
        # Cutoff before every dated version → LookupError from resolve.
        with pytest.raises(LookupError):
            _p35_call(
                parameter_registry=_p35_registry(v1),
                parameter_as_of=dt(2024, 1, 1),
                data_cutoff_datetime=dt(2024, 1, 1),
            )
        # Registry supplied with no cutoff and no as-of: no governing instant →
        # LookupError (none is inferred).
>       with pytest.raises(LookupError, match="effective_data_cutoff|as-of"):
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       Failed: DID NOT RAISE LookupError

src\tests\test_stage7_valuation.py:1736: Failed
_________________________ test_p35_invalid_parameter_set_raises_without_fallback_to_constants _________________________

    def test_p35_invalid_parameter_set_raises_without_fallback_to_constants():
        from datetime import datetime as dt
        from src.valuation.parameters import ParameterSetInvalidError

        when = dt(2026, 6, 1)
        cases = (
            _p35_version("TEST/MISSING", dt(2026, 1, 1), drop=("MIN_INDUSTRY_PEERS",)),
            _p35_version("TEST/NAN", dt(2026, 1, 1), overrides={"RISK_THRESHOLDS.high_bear_downside": float("nan")}),
            _p35_version("TEST/BOOL", dt(2026, 1, 1), overrides={"SENSITIVITY_PERTURBATION": True}),
            _p35_version("TEST/DUP", dt(2026, 1, 1), duplicate="MIN_INDUSTRY_PEERS"),
        )
        for version in cases:
            with pytest.raises(ParameterSetInvalidError):
>               _p35_call(parameter_registry=_p35_registry(version), parameter_as_of=when)

src\tests\test_stage7_valuation.py:1764:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage7_valuation.py:1597: in _p35_call
    return ValuationEngine().calculate_valuation(**base)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\valuation\engine.py:85: in calculate_valuation
    selected_version, selection_meta = select_parameter_set_for_valuation(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

parameter_registry = ParameterRegistry(versions=(ParameterSetVersion(model_version='STAGE7_V1', version_key='TEST/MISSING', effective_from=...unused in V1. Genesis record: temporal validity unknown; never valid for historical date selection (R8 pending).'))),))
parameter_as_of = datetime.datetime(2026, 6, 1, 0, 0)
effective_data_cutoff = datetime.datetime(2026, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)

    def select_parameter_set_for_valuation(
        parameter_registry: Optional[ParameterRegistry] = None,
        parameter_as_of: Optional[datetime] = None,
        *,
        effective_data_cutoff: Optional[datetime] = None,
    ) -> Tuple[ParameterSetVersion, Dict[str, object]]:
        """Choose the parameter set for one valuation, with truthful provenance.

        Selection precedence (D9):

        * No registry and no as-of: legacy Genesis path, labelled
          ``FIXED_GENESIS_LEGACY``; ``data_cutoff_used_for_parameter_selection``
          is ``False`` and the caveat states that temporal validity is NOT
          verified. This never claims historical validity.
        * A caller-supplied ``parameter_as_of`` that disagrees with
          ``effective_data_cutoff`` raises ``ValueError`` — no silent selection
          using a conflicting timestamp.
        * When ``effective_data_cutoff`` is present it is the governing timestamp
          for dated selection; ``data_cutoff_used_for_parameter_selection`` is
          ``True`` and ``as_of_source`` is ``DATA_CUTOFF``.
        * With no cutoff but an explicit ``parameter_as_of``, selection proceeds
          on the caller-supplied instant and the provenance records
          ``as_of_source == "CALLER_SUPPLIED"`` and
          ``data_cutoff_used_for_parameter_selection == False`` — no cutoff is
          invented.
        * With neither cutoff nor as-of (but a registry), a ``LookupError`` is
          raised; selection without a governing instant is undefined.

        Dated selection is delegated to ``resolve_parameter_set_as_of``:
        undated genesis records never stand in for history, future-effective
        versions never leak in, and overlapping effective dates raise instead of
        picking silently.

        Which date governs selection in production (cutoff, valuation date, or
        another instant) remains the R8/D9 decision; the caller supplies
        ``effective_data_cutoff`` explicitly and provenance records it as such.
        """
        cutoff_norm: Optional[datetime] = (
            None if effective_data_cutoff is None else normalize_datetime(effective_data_cutoff)
        )
        as_of_norm: Optional[datetime] = (
            None if parameter_as_of is None else normalize_datetime(parameter_as_of)
        )

        if parameter_registry is None and as_of_norm is None:
            # Legacy Genesis path (backward compatible). If the caller supplied a
            # cutoff but no registry, we still cannot select a dated set (the
            # default registry only contains undated genesis); the honest answer
            # is the legacy path with an explicit unverified marker.
            live = live_genesis_parameter_set()
            live_values = {r.parameter_name: r.parameter_value for r in live.records}
            import_values = {r.parameter_name: r.parameter_value for r in GENESIS_VERSION.records}
            return live, {
                "mode": "FIXED_GENESIS_LEGACY",
                "point_in_time_selection_applied": False,
                "as_of_requested": None if cutoff_norm is None else cutoff_norm.isoformat(),
                "as_of_source": None,
                "data_cutoff_used_for_parameter_selection": False,
                "module_constants_modified_since_import": live_values != import_values,
                "caveat": (
                    "Undated genesis constants; temporal validity for historical "
                    "valuation is NOT verified (R8/D9 pending)."
                ),
            }

        registry = DEFAULT_REGISTRY if parameter_registry is None else parameter_registry

        # Conflict detection: an explicitly-supplied as-of must agree with the
        # effective data cutoff, otherwise we would be selecting parameters using
        # a timestamp that contradicts the governing data cutoff.
        if as_of_norm is not None and cutoff_norm is not None and as_of_norm != cutoff_norm:
>           raise ValueError(
                "parameter_as_of conflicts with the effective valuation data cutoff "
                f"(parameter_as_of={as_of_norm.isoformat()}, "
                f"effective_data_cutoff={cutoff_norm.isoformat()}); refusing to "
                "select parameters using a conflicting timestamp."
            )
E           ValueError: parameter_as_of conflicts with the effective valuation data cutoff (parameter_as_of=2026-06-01T00:00:00+00:00, effective_data_cutoff=2026-01-01T00:00:00+00:00); refusing to select parameters using a conflicting timestamp.

src\valuation\parameters.py:522: ValueError
____________________________ test_p35_isolation_from_global_mutation_and_snapshot_aliasing ____________________________

    def test_p35_isolation_from_global_mutation_and_snapshot_aliasing():
        import dataclasses

        from src.valuation import parameters as params
        from src.valuation.parameters import consume_parameter_set, live_genesis_parameter_set

        v2 = _p35_version("TEST/V2", datetime(2026, 1, 1))
        kwargs = dict(parameter_registry=_p35_registry(v2), parameter_as_of=datetime(2026, 6, 1))
>       before = _p35_call(**kwargs)
                 ^^^^^^^^^^^^^^^^^^^

src\tests\test_stage7_valuation.py:1777:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage7_valuation.py:1597: in _p35_call
    return ValuationEngine().calculate_valuation(**base)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\valuation\engine.py:85: in calculate_valuation
    selected_version, selection_meta = select_parameter_set_for_valuation(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

parameter_registry = ParameterRegistry(versions=(ParameterSetVersion(model_version='STAGE7_V1', version_key='TEST/V2', effective_from=datet...unused in V1. Genesis record: temporal validity unknown; never valid for historical date selection (R8 pending).'))),))
parameter_as_of = datetime.datetime(2026, 6, 1, 0, 0)
effective_data_cutoff = datetime.datetime(2026, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)

    def select_parameter_set_for_valuation(
        parameter_registry: Optional[ParameterRegistry] = None,
        parameter_as_of: Optional[datetime] = None,
        *,
        effective_data_cutoff: Optional[datetime] = None,
    ) -> Tuple[ParameterSetVersion, Dict[str, object]]:
        """Choose the parameter set for one valuation, with truthful provenance.

        Selection precedence (D9):

        * No registry and no as-of: legacy Genesis path, labelled
          ``FIXED_GENESIS_LEGACY``; ``data_cutoff_used_for_parameter_selection``
          is ``False`` and the caveat states that temporal validity is NOT
          verified. This never claims historical validity.
        * A caller-supplied ``parameter_as_of`` that disagrees with
          ``effective_data_cutoff`` raises ``ValueError`` — no silent selection
          using a conflicting timestamp.
        * When ``effective_data_cutoff`` is present it is the governing timestamp
          for dated selection; ``data_cutoff_used_for_parameter_selection`` is
          ``True`` and ``as_of_source`` is ``DATA_CUTOFF``.
        * With no cutoff but an explicit ``parameter_as_of``, selection proceeds
          on the caller-supplied instant and the provenance records
          ``as_of_source == "CALLER_SUPPLIED"`` and
          ``data_cutoff_used_for_parameter_selection == False`` — no cutoff is
          invented.
        * With neither cutoff nor as-of (but a registry), a ``LookupError`` is
          raised; selection without a governing instant is undefined.

        Dated selection is delegated to ``resolve_parameter_set_as_of``:
        undated genesis records never stand in for history, future-effective
        versions never leak in, and overlapping effective dates raise instead of
        picking silently.

        Which date governs selection in production (cutoff, valuation date, or
        another instant) remains the R8/D9 decision; the caller supplies
        ``effective_data_cutoff`` explicitly and provenance records it as such.
        """
        cutoff_norm: Optional[datetime] = (
            None if effective_data_cutoff is None else normalize_datetime(effective_data_cutoff)
        )
        as_of_norm: Optional[datetime] = (
            None if parameter_as_of is None else normalize_datetime(parameter_as_of)
        )

        if parameter_registry is None and as_of_norm is None:
            # Legacy Genesis path (backward compatible). If the caller supplied a
            # cutoff but no registry, we still cannot select a dated set (the
            # default registry only contains undated genesis); the honest answer
            # is the legacy path with an explicit unverified marker.
            live = live_genesis_parameter_set()
            live_values = {r.parameter_name: r.parameter_value for r in live.records}
            import_values = {r.parameter_name: r.parameter_value for r in GENESIS_VERSION.records}
            return live, {
                "mode": "FIXED_GENESIS_LEGACY",
                "point_in_time_selection_applied": False,
                "as_of_requested": None if cutoff_norm is None else cutoff_norm.isoformat(),
                "as_of_source": None,
                "data_cutoff_used_for_parameter_selection": False,
                "module_constants_modified_since_import": live_values != import_values,
                "caveat": (
                    "Undated genesis constants; temporal validity for historical "
                    "valuation is NOT verified (R8/D9 pending)."
                ),
            }

        registry = DEFAULT_REGISTRY if parameter_registry is None else parameter_registry

        # Conflict detection: an explicitly-supplied as-of must agree with the
        # effective data cutoff, otherwise we would be selecting parameters using
        # a timestamp that contradicts the governing data cutoff.
        if as_of_norm is not None and cutoff_norm is not None and as_of_norm != cutoff_norm:
>           raise ValueError(
                "parameter_as_of conflicts with the effective valuation data cutoff "
                f"(parameter_as_of={as_of_norm.isoformat()}, "
                f"effective_data_cutoff={cutoff_norm.isoformat()}); refusing to "
                "select parameters using a conflicting timestamp."
            )
E           ValueError: parameter_as_of conflicts with the effective valuation data cutoff (parameter_as_of=2026-06-01T00:00:00+00:00, effective_data_cutoff=2026-01-01T00:00:00+00:00); refusing to select parameters using a conflicting timestamp.

src\valuation\parameters.py:522: ValueError
_______________________________ test_p35_repeated_as_of_calculations_are_deterministic ________________________________

    def test_p35_repeated_as_of_calculations_are_deterministic():
        import dataclasses

        registry = _p35_registry(_p35_version("TEST/V1", datetime(2025, 1, 1)))
        runs = []
        for _ in range(3):
>           result = _p35_call(parameter_registry=registry, parameter_as_of=datetime(2025, 6, 1))
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage7_valuation.py:1811:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage7_valuation.py:1597: in _p35_call
    return ValuationEngine().calculate_valuation(**base)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\valuation\engine.py:85: in calculate_valuation
    selected_version, selection_meta = select_parameter_set_for_valuation(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

parameter_registry = ParameterRegistry(versions=(ParameterSetVersion(model_version='STAGE7_V1', version_key='TEST/V1', effective_from=datet...unused in V1. Genesis record: temporal validity unknown; never valid for historical date selection (R8 pending).'))),))
parameter_as_of = datetime.datetime(2025, 6, 1, 0, 0)
effective_data_cutoff = datetime.datetime(2026, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)

    def select_parameter_set_for_valuation(
        parameter_registry: Optional[ParameterRegistry] = None,
        parameter_as_of: Optional[datetime] = None,
        *,
        effective_data_cutoff: Optional[datetime] = None,
    ) -> Tuple[ParameterSetVersion, Dict[str, object]]:
        """Choose the parameter set for one valuation, with truthful provenance.

        Selection precedence (D9):

        * No registry and no as-of: legacy Genesis path, labelled
          ``FIXED_GENESIS_LEGACY``; ``data_cutoff_used_for_parameter_selection``
          is ``False`` and the caveat states that temporal validity is NOT
          verified. This never claims historical validity.
        * A caller-supplied ``parameter_as_of`` that disagrees with
          ``effective_data_cutoff`` raises ``ValueError`` — no silent selection
          using a conflicting timestamp.
        * When ``effective_data_cutoff`` is present it is the governing timestamp
          for dated selection; ``data_cutoff_used_for_parameter_selection`` is
          ``True`` and ``as_of_source`` is ``DATA_CUTOFF``.
        * With no cutoff but an explicit ``parameter_as_of``, selection proceeds
          on the caller-supplied instant and the provenance records
          ``as_of_source == "CALLER_SUPPLIED"`` and
          ``data_cutoff_used_for_parameter_selection == False`` — no cutoff is
          invented.
        * With neither cutoff nor as-of (but a registry), a ``LookupError`` is
          raised; selection without a governing instant is undefined.

        Dated selection is delegated to ``resolve_parameter_set_as_of``:
        undated genesis records never stand in for history, future-effective
        versions never leak in, and overlapping effective dates raise instead of
        picking silently.

        Which date governs selection in production (cutoff, valuation date, or
        another instant) remains the R8/D9 decision; the caller supplies
        ``effective_data_cutoff`` explicitly and provenance records it as such.
        """
        cutoff_norm: Optional[datetime] = (
            None if effective_data_cutoff is None else normalize_datetime(effective_data_cutoff)
        )
        as_of_norm: Optional[datetime] = (
            None if parameter_as_of is None else normalize_datetime(parameter_as_of)
        )

        if parameter_registry is None and as_of_norm is None:
            # Legacy Genesis path (backward compatible). If the caller supplied a
            # cutoff but no registry, we still cannot select a dated set (the
            # default registry only contains undated genesis); the honest answer
            # is the legacy path with an explicit unverified marker.
            live = live_genesis_parameter_set()
            live_values = {r.parameter_name: r.parameter_value for r in live.records}
            import_values = {r.parameter_name: r.parameter_value for r in GENESIS_VERSION.records}
            return live, {
                "mode": "FIXED_GENESIS_LEGACY",
                "point_in_time_selection_applied": False,
                "as_of_requested": None if cutoff_norm is None else cutoff_norm.isoformat(),
                "as_of_source": None,
                "data_cutoff_used_for_parameter_selection": False,
                "module_constants_modified_since_import": live_values != import_values,
                "caveat": (
                    "Undated genesis constants; temporal validity for historical "
                    "valuation is NOT verified (R8/D9 pending)."
                ),
            }

        registry = DEFAULT_REGISTRY if parameter_registry is None else parameter_registry

        # Conflict detection: an explicitly-supplied as-of must agree with the
        # effective data cutoff, otherwise we would be selecting parameters using
        # a timestamp that contradicts the governing data cutoff.
        if as_of_norm is not None and cutoff_norm is not None and as_of_norm != cutoff_norm:
>           raise ValueError(
                "parameter_as_of conflicts with the effective valuation data cutoff "
                f"(parameter_as_of={as_of_norm.isoformat()}, "
                f"effective_data_cutoff={cutoff_norm.isoformat()}); refusing to "
                "select parameters using a conflicting timestamp."
            )
E           ValueError: parameter_as_of conflicts with the effective valuation data cutoff (parameter_as_of=2025-06-01T00:00:00+00:00, effective_data_cutoff=2026-01-01T00:00:00+00:00); refusing to select parameters using a conflicting timestamp.

src\valuation\parameters.py:522: ValueError
=============================================== short test summary info ===============================================
FAILED src/tests/test_stage7_valuation.py::test_p35_as_of_selection_governs_calculation_and_snapshot_matches - AssertionError: assert '2026-06-01T00:00:00+00:00' == '2026-01-01T00:00:00+00:00'
FAILED src/tests/test_stage7_valuation.py::test_p35_selected_set_governs_peers_alerts_and_scenario_weights - ValueError: parameter_as_of conflicts with the effective valuation data cutoff (parameter_as_of=2026-06-01T00:00:00...
FAILED src/tests/test_stage7_valuation.py::test_p35_missing_or_ambiguous_as_of_selection_fails_closed - Failed: DID NOT RAISE LookupError
FAILED src/tests/test_stage7_valuation.py::test_p35_invalid_parameter_set_raises_without_fallback_to_constants - ValueError: parameter_as_of conflicts with the effective valuation data cutoff (parameter_as_of=2026-06-01T00:00:00...
FAILED src/tests/test_stage7_valuation.py::test_p35_isolation_from_global_mutation_and_snapshot_aliasing - ValueError: parameter_as_of conflicts with the effective valuation data cutoff (parameter_as_of=2026-06-01T00:00:00...
FAILED src/tests/test_stage7_valuation.py::test_p35_repeated_as_of_calculations_are_deterministic - ValueError: parameter_as_of conflicts with the effective valuation data cutoff (parameter_as_of=2025-06-01T00:00:00...
===================================== 6 failed, 13 passed, 72 deselected in 1.32s =====================================
(analyzer) PS D:\winprojects\analyzer> python -m pytest src/tests/test_stage7_valuation.py -v
================================================= test session starts =================================================
platform win32 -- Python 3.12.9, pytest-9.1.1, pluggy-1.6.0 -- D:\winprojects\analyzer\Scripts\python.exe
cachedir: .pytest_cache
rootdir: D:\winprojects\analyzer
collected 91 items

src/tests/test_stage7_valuation.py::test_jalali_service_uses_selected_price_and_preserves_provenance PASSED      [  1%]
src/tests/test_stage7_valuation.py::test_jalali_service_fails_closed_without_eligible_observation PASSED         [  2%]
src/tests/test_stage7_valuation.py::test_jalali_service_rejects_forecast_from_another_company PASSED             [  3%]
src/tests/test_stage7_valuation.py::test_valuation_models PASSED                                                 [  4%]
src/tests/test_stage7_valuation.py::test_valuation_engine_forward_pe_and_expected_fair_value PASSED              [  5%]
src/tests/test_stage7_valuation.py::test_industry_forward_pe_requires_eight_valid_peers PASSED                   [  6%]
src/tests/test_stage7_valuation.py::test_industry_ttm_is_fallback_after_historical_median PASSED                 [  7%]
src/tests/test_stage7_valuation.py::test_negative_eps_does_not_create_fake_pe_or_fair_value PASSED               [  8%]
src/tests/test_stage7_valuation.py::test_reliability_does_not_change_forward_pe_or_fair_value PASSED             [  9%]
src/tests/test_stage7_valuation.py::test_direct_probability_adjustments_are_rejected_in_favor_of_family_evidence PASSED [ 10%]
src/tests/test_stage7_valuation.py::test_probability_evidence_is_family_level_and_equal_weighted PASSED          [ 12%]
src/tests/test_stage7_valuation.py::test_probability_evidence_rejects_unknown_or_incomplete_family_data PASSED   [ 13%]
src/tests/test_stage7_valuation.py::test_scenario_multiple_adjustments_require_economic_rationale_and_are_bounded PASSED [ 14%]
src/tests/test_stage7_valuation.py::test_alerts_include_severity_and_driver_focus PASSED                         [ 15%]
src/tests/test_stage7_valuation.py::test_p2_sensitivity_drivers_present_and_bounded PASSED                       [ 16%]
src/tests/test_stage7_valuation.py::test_p2_sensitivity_missing_data_empty_drivers PASSED                        [ 17%]
src/tests/test_stage7_valuation.py::test_p2_sensitivity_deterministic_repeated_runs PASSED                       [ 18%]
src/tests/test_stage7_valuation.py::test_p2_alert_severity_levels_valid PASSED                                   [ 19%]
src/tests/test_stage7_valuation.py::test_p2_alert_low_reliability_threshold_boundaries PASSED                    [ 20%]
src/tests/test_stage7_valuation.py::test_p2_alert_high_dispersion_threshold_boundaries PASSED                    [ 21%]
src/tests/test_stage7_valuation.py::test_p2_alert_divergence_ratios_boundaries PASSED                            [ 23%]
src/tests/test_stage7_valuation.py::test_v1_sector_examples_use_only_eps_and_target_pe_drivers PASSED            [ 24%]
src/tests/test_stage7_valuation.py::test_v1_uses_stage5_eps_without_recalculating_from_net_profit PASSED         [ 25%]
src/tests/test_stage7_valuation.py::test_v1_defers_undefined_flip_dependence_and_assumption_alerts PASSED        [ 26%]
src/tests/test_stage7_valuation.py::test_p3_sensitivity_recomputes_from_valuation_identity PASSED                [ 27%]
src/tests/test_stage7_valuation.py::test_p3_nan_eps_is_guarded_as_invalid PASSED                                 [ 28%]
src/tests/test_stage7_valuation.py::test_p3_zero_and_negative_price_guarded PASSED                               [ 29%]
src/tests/test_stage7_valuation.py::test_p3_nonfinite_benchmark_series_filtered PASSED                           [ 30%]
src/tests/test_stage7_valuation.py::test_p3_nonfinite_scores_fall_back_to_defaults PASSED                        [ 31%]
src/tests/test_stage7_valuation.py::test_p3_flip_dependence_alerts_remain_explicitly_unresolved PASSED           [ 32%]
src/tests/test_stage7_valuation.py::test_p4_peer_count_below_minimum_falls_back PASSED                           [ 34%]
src/tests/test_stage7_valuation.py::test_p4_peer_count_at_minimum_selects_industry_forward PASSED                [ 35%]
src/tests/test_stage7_valuation.py::test_p4_peer_count_above_minimum_and_median_provenance PASSED                [ 36%]
src/tests/test_stage7_valuation.py::test_p4_peer_count_filters_invalid_values PASSED                             [ 37%]
src/tests/test_stage7_valuation.py::test_p4_peer_count_empty_data_reports_zero_and_falls_back PASSED             [ 38%]
src/tests/test_stage7_valuation.py::test_p4_benchmark_fallback_ignores_forward_count_for_ttm PASSED              [ 39%]
src/tests/test_stage7_valuation.py::test_p5_nonfinite_price_yields_null_outputs PASSED                           [ 40%]
src/tests/test_stage7_valuation.py::test_p5_missing_eps_is_not_applicable_not_zero PASSED                        [ 41%]
src/tests/test_stage7_valuation.py::test_p5_nonfinite_reliability_echo_sanitized PASSED                          [ 42%]
src/tests/test_stage7_valuation.py::test_p5_nonfinite_probability_confidence_echo_finite PASSED                  [ 43%]
src/tests/test_stage7_valuation.py::test_p5_missing_data_quality_does_not_crash PASSED                           [ 45%]
src/tests/test_stage7_valuation.py::test_p5_nonfinite_multiple_adjustment_rejected PASSED                        [ 46%]
src/tests/test_stage7_valuation.py::test_p5_nan_probability_evidence_rejected PASSED                             [ 47%]
src/tests/test_stage7_valuation.py::test_p5_datetime_echoes_normalized_to_utc PASSED                             [ 48%]
src/tests/test_stage7_valuation.py::test_p5_default_cutoff_inherits_forecast_cutoff_normalized PASSED            [ 49%]
src/tests/test_stage7_valuation.py::test_p5_undated_benchmark_series_carry_no_provenance PASSED                  [ 50%]
src/tests/test_stage7_valuation.py::test_p6_production_path_real_stage5_forecast PASSED                          [ 51%]
src/tests/test_stage7_valuation.py::test_p6_cutoff_pit_limitation_pinned PASSED                                  [ 52%]
src/tests/test_stage7_valuation.py::test_p6_missing_benchmarks_yield_guarded_nulls PASSED                        [ 53%]
src/tests/test_stage7_valuation.py::test_p6_scenario_ordering_flag_and_probability_normalization PASSED          [ 54%]
src/tests/test_stage7_valuation.py::test_p6_invalid_eps_variants_never_fabricate_values PASSED                   [ 56%]
src/tests/test_stage7_valuation.py::test_p6_repeat_runs_identical_on_full_contract PASSED                        [ 57%]
src/tests/test_stage7_valuation.py::test_p6_regression_prior_behavior_preserved PASSED                           [ 58%]
src/tests/test_stage7_valuation.py::test_p10_expensive_base_upside_parameterized_outputs_unchanged PASSED        [ 59%]
src/tests/test_stage7_valuation.py::test_p10_expensive_threshold_consumed_from_parameters PASSED                 [ 60%]
src/tests/test_stage7_valuation.py::test_p12_calculation_timestamp_utc_aware_and_deterministic PASSED            [ 61%]
src/tests/test_stage7_valuation.py::test_p32_input_refs_before_cutoff_leave_results_unchanged PASSED             [ 62%]
src/tests/test_stage7_valuation.py::test_p32_input_ref_after_cutoff_rejected_on_valuation_path PASSED            [ 63%]
src/tests/test_stage7_valuation.py::test_p32_input_ref_at_cutoff_boundary_accepted PASSED                        [ 64%]
src/tests/test_stage7_valuation.py::test_p32_input_ref_missing_date_rejected PASSED                              [ 65%]
src/tests/test_stage7_valuation.py::test_p32_input_refs_absent_preserves_legacy_path PASSED                      [ 67%]
src/tests/test_stage7_valuation.py::test_p53_embedded_forecast_input_ref_at_cutoff_is_enforced_and_accepted PASSED [ 68%]
src/tests/test_stage7_valuation.py::test_p53_stage5_dropped_future_input_is_not_reintroduced_to_stage7 PASSED    [ 69%]
src/tests/test_stage7_valuation.py::test_p53_embedded_forecast_input_ref_without_availability_is_rejected PASSED [ 70%]
src/tests/test_stage7_valuation.py::test_p53_explicit_empty_refs_do_not_bypass_embedded_forecast_provenance PASSED [ 71%]
src/tests/test_stage7_valuation.py::test_p53_stage5_forecast_without_provenance_preserves_legacy_path PASSED     [ 72%]
src/tests/test_stage7_valuation.py::test_p33_genesis_snapshot_matches_live_constants PASSED                      [ 73%]
src/tests/test_stage7_valuation.py::test_p33_result_carries_parameter_audit PASSED                               [ 74%]
src/tests/test_stage7_valuation.py::test_p33_resolve_exact_key_and_missing_raises PASSED                         [ 75%]
src/tests/test_stage7_valuation.py::test_p33_as_of_without_dated_records_raises PASSED                           [ 76%]
src/tests/test_stage7_valuation.py::test_p33_as_of_selection_mechanics PASSED                                    [ 78%]
src/tests/test_stage7_valuation.py::test_p33_as_of_overlap_raises_ambiguity PASSED                               [ 79%]
src/tests/test_stage7_valuation.py::test_p35_legacy_path_provenance_is_truthful_and_unchanged PASSED             [ 80%]
src/tests/test_stage7_valuation.py::test_p35_snapshot_reports_values_actually_consumed_when_module_constant_changes PASSED [ 81%]
src/tests/test_stage7_valuation.py::test_p35_as_of_selection_governs_calculation_and_snapshot_matches FAILED     [ 82%]
src/tests/test_stage7_valuation.py::test_p35_selected_set_governs_peers_alerts_and_scenario_weights FAILED       [ 83%]
src/tests/test_stage7_valuation.py::test_p35_missing_or_ambiguous_as_of_selection_fails_closed FAILED            [ 84%]
src/tests/test_stage7_valuation.py::test_p35_invalid_parameter_set_raises_without_fallback_to_constants FAILED   [ 85%]
src/tests/test_stage7_valuation.py::test_p35_isolation_from_global_mutation_and_snapshot_aliasing FAILED         [ 86%]
src/tests/test_stage7_valuation.py::test_p35_repeated_as_of_calculations_are_deterministic FAILED                [ 87%]
src/tests/test_stage7_valuation.py::test_p54_cutoff_governs_parameter_selection PASSED                           [ 89%]
src/tests/test_stage7_valuation.py::test_p54_valuation_date_does_not_substitute_for_cutoff PASSED                [ 90%]
src/tests/test_stage7_valuation.py::test_p54_effective_from_boundary_accepted_exactly PASSED                     [ 91%]
src/tests/test_stage7_valuation.py::test_p54_future_effective_version_never_selected PASSED                      [ 92%]
src/tests/test_stage7_valuation.py::test_p54_missing_eligible_dated_version_raises PASSED                        [ 93%]
src/tests/test_stage7_valuation.py::test_p54_overlapping_eligible_versions_raise PASSED                          [ 94%]
src/tests/test_stage7_valuation.py::test_p54_conflicting_explicit_as_of_and_cutoff_rejected PASSED               [ 95%]
src/tests/test_stage7_valuation.py::test_p54_matching_as_of_and_cutoff_accepted PASSED                           [ 96%]
src/tests/test_stage7_valuation.py::test_p54_metadata_distinguishes_dated_from_legacy PASSED                     [ 97%]
src/tests/test_stage7_valuation.py::test_p54_repeated_cutoff_calculations_deterministic PASSED                   [ 98%]
src/tests/test_stage7_valuation.py::test_p54_legacy_path_backward_compatible_without_pit_claim PASSED            [100%]

====================================================== FAILURES =======================================================
__________________________ test_p35_as_of_selection_governs_calculation_and_snapshot_matches __________________________

    def test_p35_as_of_selection_governs_calculation_and_snapshot_matches():
        from datetime import datetime as dt

        v1 = _p35_version("TEST/V1", dt(2025, 1, 1))
        v2 = _p35_version(
            "TEST/V2", dt(2026, 1, 1),
            overrides={"VALUATION_THRESHOLDS.expensive_base_upside": -50.0, "MODEL_VERSION": "TEST_MODEL_V2"},
        )
        registry = _p35_registry(v1, v2)
        # D9: parameter_as_of must agree with the effective data cutoff (2026-01-01
        # from make_forecast). Use cutoff-matching as_of values so the cutoff and
        # the caller-supplied instant are identical.
        historical = _p35_call(
            parameter_registry=registry,
            parameter_as_of=dt(2026, 1, 1),
            data_cutoff_datetime=dt(2026, 1, 1),
        )
        # For V2-effective selection, provide a matching cutoff at V2's effective date.
        current = _p35_call(
            parameter_registry=registry,
            parameter_as_of=dt(2026, 6, 1),
            data_cutoff_datetime=dt(2026, 6, 1),
        )
        # At cutoff=2026-01-01, V2 (effective 2026-01-01) is selected; the value
        # override changes the classification relative to the pre-V2 semantics
        # only for expected upside at the same cutoff.
        assert historical.metadata["parameter_set_version"] == "TEST/V2"
        assert current.metadata["parameter_set_version"] == "TEST/V2"
        assert historical.metadata["parameter_snapshot"]["VALUATION_THRESHOLDS.expensive_base_upside"] == -50.0
        assert current.metadata["parameter_snapshot"]["VALUATION_THRESHOLDS.expensive_base_upside"] == -50.0
        # To demonstrate V1 vs V2 divergence, use a cutoff before V2's effective date.
        pre_v2 = _p35_call(
            parameter_registry=registry,
            parameter_as_of=dt(2025, 6, 1),
            data_cutoff_datetime=dt(2025, 6, 1),
        )
        assert pre_v2.metadata["parameter_set_version"] == "TEST/V1"
        assert pre_v2.valuation_status == "EXPENSIVE"
        assert pre_v2.model_version == "STAGE7_V1"
        selection = current.metadata["parameter_selection"]
        assert selection["mode"] == "AS_OF_EFFECTIVE_DATED"
        assert selection["point_in_time_selection_applied"] is True
        # assert selection["as_of_requested"] == "2026-06-01T00:00:00+00:00"
>       assert selection["as_of_requested"] == "2026-01-01T00:00:00+00:00"
E       AssertionError: assert '2026-06-01T00:00:00+00:00' == '2026-01-01T00:00:00+00:00'
E
E         - 2026-01-01T00:00:00+00:00
E         ?       ^
E         + 2026-06-01T00:00:00+00:00
E         ?       ^

src\tests\test_stage7_valuation.py:1685: AssertionError
___________________________ test_p35_selected_set_governs_peers_alerts_and_scenario_weights ___________________________

    def test_p35_selected_set_governs_peers_alerts_and_scenario_weights():
        from datetime import datetime as dt

        kwargs = dict(
            forecast_result=make_forecast(),
            forecast_reliability_score=50.0,
            industry_forward_pe_values=[10.0, 10.0, 10.0],
            historical_pe_values=[7.0],
        )
        default = _p35_call(**kwargs)
        assert default.target_pe_source == "HISTORICAL_MEDIAN_PE"
        assert "INSUFFICIENT_PEER_DATA" in default.valuation_risk_flags
        assert "LOW_FORECAST_RELIABILITY" not in default.valuation_risk_flags
        v2 = _p35_version(
            "TEST/V2", dt(2026, 1, 1),
            overrides={
                "MIN_INDUSTRY_PEERS": 3,
                "ALERT_THRESHOLDS.low_forecast_reliability": 60.0,
                "SCENARIO_WEIGHTS.bear": 0.5, "SCENARIO_WEIGHTS.base": 0.3, "SCENARIO_WEIGHTS.bull": 0.2,
            },
        )
>       selected = _p35_call(parameter_registry=_p35_registry(v2), parameter_as_of=dt(2026, 6, 1), **kwargs)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage7_valuation.py:1713:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage7_valuation.py:1597: in _p35_call
    return ValuationEngine().calculate_valuation(**base)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\valuation\engine.py:85: in calculate_valuation
    selected_version, selection_meta = select_parameter_set_for_valuation(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

parameter_registry = ParameterRegistry(versions=(ParameterSetVersion(model_version='STAGE7_V1', version_key='TEST/V2', effective_from=datet...unused in V1. Genesis record: temporal validity unknown; never valid for historical date selection (R8 pending).'))),))
parameter_as_of = datetime.datetime(2026, 6, 1, 0, 0)
effective_data_cutoff = datetime.datetime(2026, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)

    def select_parameter_set_for_valuation(
        parameter_registry: Optional[ParameterRegistry] = None,
        parameter_as_of: Optional[datetime] = None,
        *,
        effective_data_cutoff: Optional[datetime] = None,
    ) -> Tuple[ParameterSetVersion, Dict[str, object]]:
        """Choose the parameter set for one valuation, with truthful provenance.

        Selection precedence (D9):

        * No registry and no as-of: legacy Genesis path, labelled
          ``FIXED_GENESIS_LEGACY``; ``data_cutoff_used_for_parameter_selection``
          is ``False`` and the caveat states that temporal validity is NOT
          verified. This never claims historical validity.
        * A caller-supplied ``parameter_as_of`` that disagrees with
          ``effective_data_cutoff`` raises ``ValueError`` — no silent selection
          using a conflicting timestamp.
        * When ``effective_data_cutoff`` is present it is the governing timestamp
          for dated selection; ``data_cutoff_used_for_parameter_selection`` is
          ``True`` and ``as_of_source`` is ``DATA_CUTOFF``.
        * With no cutoff but an explicit ``parameter_as_of``, selection proceeds
          on the caller-supplied instant and the provenance records
          ``as_of_source == "CALLER_SUPPLIED"`` and
          ``data_cutoff_used_for_parameter_selection == False`` — no cutoff is
          invented.
        * With neither cutoff nor as-of (but a registry), a ``LookupError`` is
          raised; selection without a governing instant is undefined.

        Dated selection is delegated to ``resolve_parameter_set_as_of``:
        undated genesis records never stand in for history, future-effective
        versions never leak in, and overlapping effective dates raise instead of
        picking silently.

        Which date governs selection in production (cutoff, valuation date, or
        another instant) remains the R8/D9 decision; the caller supplies
        ``effective_data_cutoff`` explicitly and provenance records it as such.
        """
        cutoff_norm: Optional[datetime] = (
            None if effective_data_cutoff is None else normalize_datetime(effective_data_cutoff)
        )
        as_of_norm: Optional[datetime] = (
            None if parameter_as_of is None else normalize_datetime(parameter_as_of)
        )

        if parameter_registry is None and as_of_norm is None:
            # Legacy Genesis path (backward compatible). If the caller supplied a
            # cutoff but no registry, we still cannot select a dated set (the
            # default registry only contains undated genesis); the honest answer
            # is the legacy path with an explicit unverified marker.
            live = live_genesis_parameter_set()
            live_values = {r.parameter_name: r.parameter_value for r in live.records}
            import_values = {r.parameter_name: r.parameter_value for r in GENESIS_VERSION.records}
            return live, {
                "mode": "FIXED_GENESIS_LEGACY",
                "point_in_time_selection_applied": False,
                "as_of_requested": None if cutoff_norm is None else cutoff_norm.isoformat(),
                "as_of_source": None,
                "data_cutoff_used_for_parameter_selection": False,
                "module_constants_modified_since_import": live_values != import_values,
                "caveat": (
                    "Undated genesis constants; temporal validity for historical "
                    "valuation is NOT verified (R8/D9 pending)."
                ),
            }

        registry = DEFAULT_REGISTRY if parameter_registry is None else parameter_registry

        # Conflict detection: an explicitly-supplied as-of must agree with the
        # effective data cutoff, otherwise we would be selecting parameters using
        # a timestamp that contradicts the governing data cutoff.
        if as_of_norm is not None and cutoff_norm is not None and as_of_norm != cutoff_norm:
>           raise ValueError(
                "parameter_as_of conflicts with the effective valuation data cutoff "
                f"(parameter_as_of={as_of_norm.isoformat()}, "
                f"effective_data_cutoff={cutoff_norm.isoformat()}); refusing to "
                "select parameters using a conflicting timestamp."
            )
E           ValueError: parameter_as_of conflicts with the effective valuation data cutoff (parameter_as_of=2026-06-01T00:00:00+00:00, effective_data_cutoff=2026-01-01T00:00:00+00:00); refusing to select parameters using a conflicting timestamp.

src\valuation\parameters.py:522: ValueError
_____________________________ test_p35_missing_or_ambiguous_as_of_selection_fails_closed ______________________________

    def test_p35_missing_or_ambiguous_as_of_selection_fails_closed():
        from datetime import datetime as dt

        v1 = _p35_version("TEST/V1", dt(2025, 1, 1))
        # Cutoff before every dated version → LookupError from resolve.
        with pytest.raises(LookupError):
            _p35_call(
                parameter_registry=_p35_registry(v1),
                parameter_as_of=dt(2024, 1, 1),
                data_cutoff_datetime=dt(2024, 1, 1),
            )
        # Registry supplied with no cutoff and no as-of: no governing instant →
        # LookupError (none is inferred).
>       with pytest.raises(LookupError, match="effective_data_cutoff|as-of"):
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       Failed: DID NOT RAISE LookupError

src\tests\test_stage7_valuation.py:1736: Failed
_________________________ test_p35_invalid_parameter_set_raises_without_fallback_to_constants _________________________

    def test_p35_invalid_parameter_set_raises_without_fallback_to_constants():
        from datetime import datetime as dt
        from src.valuation.parameters import ParameterSetInvalidError

        when = dt(2026, 6, 1)
        cases = (
            _p35_version("TEST/MISSING", dt(2026, 1, 1), drop=("MIN_INDUSTRY_PEERS",)),
            _p35_version("TEST/NAN", dt(2026, 1, 1), overrides={"RISK_THRESHOLDS.high_bear_downside": float("nan")}),
            _p35_version("TEST/BOOL", dt(2026, 1, 1), overrides={"SENSITIVITY_PERTURBATION": True}),
            _p35_version("TEST/DUP", dt(2026, 1, 1), duplicate="MIN_INDUSTRY_PEERS"),
        )
        for version in cases:
            with pytest.raises(ParameterSetInvalidError):
>               _p35_call(parameter_registry=_p35_registry(version), parameter_as_of=when)

src\tests\test_stage7_valuation.py:1764:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage7_valuation.py:1597: in _p35_call
    return ValuationEngine().calculate_valuation(**base)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\valuation\engine.py:85: in calculate_valuation
    selected_version, selection_meta = select_parameter_set_for_valuation(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

parameter_registry = ParameterRegistry(versions=(ParameterSetVersion(model_version='STAGE7_V1', version_key='TEST/MISSING', effective_from=...unused in V1. Genesis record: temporal validity unknown; never valid for historical date selection (R8 pending).'))),))
parameter_as_of = datetime.datetime(2026, 6, 1, 0, 0)
effective_data_cutoff = datetime.datetime(2026, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)

    def select_parameter_set_for_valuation(
        parameter_registry: Optional[ParameterRegistry] = None,
        parameter_as_of: Optional[datetime] = None,
        *,
        effective_data_cutoff: Optional[datetime] = None,
    ) -> Tuple[ParameterSetVersion, Dict[str, object]]:
        """Choose the parameter set for one valuation, with truthful provenance.

        Selection precedence (D9):

        * No registry and no as-of: legacy Genesis path, labelled
          ``FIXED_GENESIS_LEGACY``; ``data_cutoff_used_for_parameter_selection``
          is ``False`` and the caveat states that temporal validity is NOT
          verified. This never claims historical validity.
        * A caller-supplied ``parameter_as_of`` that disagrees with
          ``effective_data_cutoff`` raises ``ValueError`` — no silent selection
          using a conflicting timestamp.
        * When ``effective_data_cutoff`` is present it is the governing timestamp
          for dated selection; ``data_cutoff_used_for_parameter_selection`` is
          ``True`` and ``as_of_source`` is ``DATA_CUTOFF``.
        * With no cutoff but an explicit ``parameter_as_of``, selection proceeds
          on the caller-supplied instant and the provenance records
          ``as_of_source == "CALLER_SUPPLIED"`` and
          ``data_cutoff_used_for_parameter_selection == False`` — no cutoff is
          invented.
        * With neither cutoff nor as-of (but a registry), a ``LookupError`` is
          raised; selection without a governing instant is undefined.

        Dated selection is delegated to ``resolve_parameter_set_as_of``:
        undated genesis records never stand in for history, future-effective
        versions never leak in, and overlapping effective dates raise instead of
        picking silently.

        Which date governs selection in production (cutoff, valuation date, or
        another instant) remains the R8/D9 decision; the caller supplies
        ``effective_data_cutoff`` explicitly and provenance records it as such.
        """
        cutoff_norm: Optional[datetime] = (
            None if effective_data_cutoff is None else normalize_datetime(effective_data_cutoff)
        )
        as_of_norm: Optional[datetime] = (
            None if parameter_as_of is None else normalize_datetime(parameter_as_of)
        )

        if parameter_registry is None and as_of_norm is None:
            # Legacy Genesis path (backward compatible). If the caller supplied a
            # cutoff but no registry, we still cannot select a dated set (the
            # default registry only contains undated genesis); the honest answer
            # is the legacy path with an explicit unverified marker.
            live = live_genesis_parameter_set()
            live_values = {r.parameter_name: r.parameter_value for r in live.records}
            import_values = {r.parameter_name: r.parameter_value for r in GENESIS_VERSION.records}
            return live, {
                "mode": "FIXED_GENESIS_LEGACY",
                "point_in_time_selection_applied": False,
                "as_of_requested": None if cutoff_norm is None else cutoff_norm.isoformat(),
                "as_of_source": None,
                "data_cutoff_used_for_parameter_selection": False,
                "module_constants_modified_since_import": live_values != import_values,
                "caveat": (
                    "Undated genesis constants; temporal validity for historical "
                    "valuation is NOT verified (R8/D9 pending)."
                ),
            }

        registry = DEFAULT_REGISTRY if parameter_registry is None else parameter_registry

        # Conflict detection: an explicitly-supplied as-of must agree with the
        # effective data cutoff, otherwise we would be selecting parameters using
        # a timestamp that contradicts the governing data cutoff.
        if as_of_norm is not None and cutoff_norm is not None and as_of_norm != cutoff_norm:
>           raise ValueError(
                "parameter_as_of conflicts with the effective valuation data cutoff "
                f"(parameter_as_of={as_of_norm.isoformat()}, "
                f"effective_data_cutoff={cutoff_norm.isoformat()}); refusing to "
                "select parameters using a conflicting timestamp."
            )
E           ValueError: parameter_as_of conflicts with the effective valuation data cutoff (parameter_as_of=2026-06-01T00:00:00+00:00, effective_data_cutoff=2026-01-01T00:00:00+00:00); refusing to select parameters using a conflicting timestamp.

src\valuation\parameters.py:522: ValueError
____________________________ test_p35_isolation_from_global_mutation_and_snapshot_aliasing ____________________________

    def test_p35_isolation_from_global_mutation_and_snapshot_aliasing():
        import dataclasses

        from src.valuation import parameters as params
        from src.valuation.parameters import consume_parameter_set, live_genesis_parameter_set

        v2 = _p35_version("TEST/V2", datetime(2026, 1, 1))
        kwargs = dict(parameter_registry=_p35_registry(v2), parameter_as_of=datetime(2026, 6, 1))
>       before = _p35_call(**kwargs)
                 ^^^^^^^^^^^^^^^^^^^

src\tests\test_stage7_valuation.py:1777:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage7_valuation.py:1597: in _p35_call
    return ValuationEngine().calculate_valuation(**base)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\valuation\engine.py:85: in calculate_valuation
    selected_version, selection_meta = select_parameter_set_for_valuation(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

parameter_registry = ParameterRegistry(versions=(ParameterSetVersion(model_version='STAGE7_V1', version_key='TEST/V2', effective_from=datet...unused in V1. Genesis record: temporal validity unknown; never valid for historical date selection (R8 pending).'))),))
parameter_as_of = datetime.datetime(2026, 6, 1, 0, 0)
effective_data_cutoff = datetime.datetime(2026, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)

    def select_parameter_set_for_valuation(
        parameter_registry: Optional[ParameterRegistry] = None,
        parameter_as_of: Optional[datetime] = None,
        *,
        effective_data_cutoff: Optional[datetime] = None,
    ) -> Tuple[ParameterSetVersion, Dict[str, object]]:
        """Choose the parameter set for one valuation, with truthful provenance.

        Selection precedence (D9):

        * No registry and no as-of: legacy Genesis path, labelled
          ``FIXED_GENESIS_LEGACY``; ``data_cutoff_used_for_parameter_selection``
          is ``False`` and the caveat states that temporal validity is NOT
          verified. This never claims historical validity.
        * A caller-supplied ``parameter_as_of`` that disagrees with
          ``effective_data_cutoff`` raises ``ValueError`` — no silent selection
          using a conflicting timestamp.
        * When ``effective_data_cutoff`` is present it is the governing timestamp
          for dated selection; ``data_cutoff_used_for_parameter_selection`` is
          ``True`` and ``as_of_source`` is ``DATA_CUTOFF``.
        * With no cutoff but an explicit ``parameter_as_of``, selection proceeds
          on the caller-supplied instant and the provenance records
          ``as_of_source == "CALLER_SUPPLIED"`` and
          ``data_cutoff_used_for_parameter_selection == False`` — no cutoff is
          invented.
        * With neither cutoff nor as-of (but a registry), a ``LookupError`` is
          raised; selection without a governing instant is undefined.

        Dated selection is delegated to ``resolve_parameter_set_as_of``:
        undated genesis records never stand in for history, future-effective
        versions never leak in, and overlapping effective dates raise instead of
        picking silently.

        Which date governs selection in production (cutoff, valuation date, or
        another instant) remains the R8/D9 decision; the caller supplies
        ``effective_data_cutoff`` explicitly and provenance records it as such.
        """
        cutoff_norm: Optional[datetime] = (
            None if effective_data_cutoff is None else normalize_datetime(effective_data_cutoff)
        )
        as_of_norm: Optional[datetime] = (
            None if parameter_as_of is None else normalize_datetime(parameter_as_of)
        )

        if parameter_registry is None and as_of_norm is None:
            # Legacy Genesis path (backward compatible). If the caller supplied a
            # cutoff but no registry, we still cannot select a dated set (the
            # default registry only contains undated genesis); the honest answer
            # is the legacy path with an explicit unverified marker.
            live = live_genesis_parameter_set()
            live_values = {r.parameter_name: r.parameter_value for r in live.records}
            import_values = {r.parameter_name: r.parameter_value for r in GENESIS_VERSION.records}
            return live, {
                "mode": "FIXED_GENESIS_LEGACY",
                "point_in_time_selection_applied": False,
                "as_of_requested": None if cutoff_norm is None else cutoff_norm.isoformat(),
                "as_of_source": None,
                "data_cutoff_used_for_parameter_selection": False,
                "module_constants_modified_since_import": live_values != import_values,
                "caveat": (
                    "Undated genesis constants; temporal validity for historical "
                    "valuation is NOT verified (R8/D9 pending)."
                ),
            }

        registry = DEFAULT_REGISTRY if parameter_registry is None else parameter_registry

        # Conflict detection: an explicitly-supplied as-of must agree with the
        # effective data cutoff, otherwise we would be selecting parameters using
        # a timestamp that contradicts the governing data cutoff.
        if as_of_norm is not None and cutoff_norm is not None and as_of_norm != cutoff_norm:
>           raise ValueError(
                "parameter_as_of conflicts with the effective valuation data cutoff "
                f"(parameter_as_of={as_of_norm.isoformat()}, "
                f"effective_data_cutoff={cutoff_norm.isoformat()}); refusing to "
                "select parameters using a conflicting timestamp."
            )
E           ValueError: parameter_as_of conflicts with the effective valuation data cutoff (parameter_as_of=2026-06-01T00:00:00+00:00, effective_data_cutoff=2026-01-01T00:00:00+00:00); refusing to select parameters using a conflicting timestamp.

src\valuation\parameters.py:522: ValueError
_______________________________ test_p35_repeated_as_of_calculations_are_deterministic ________________________________

    def test_p35_repeated_as_of_calculations_are_deterministic():
        import dataclasses

        registry = _p35_registry(_p35_version("TEST/V1", datetime(2025, 1, 1)))
        runs = []
        for _ in range(3):
>           result = _p35_call(parameter_registry=registry, parameter_as_of=datetime(2025, 6, 1))
                     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

src\tests\test_stage7_valuation.py:1811:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
src\tests\test_stage7_valuation.py:1597: in _p35_call
    return ValuationEngine().calculate_valuation(**base)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
src\valuation\engine.py:85: in calculate_valuation
    selected_version, selection_meta = select_parameter_set_for_valuation(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

parameter_registry = ParameterRegistry(versions=(ParameterSetVersion(model_version='STAGE7_V1', version_key='TEST/V1', effective_from=datet...unused in V1. Genesis record: temporal validity unknown; never valid for historical date selection (R8 pending).'))),))
parameter_as_of = datetime.datetime(2025, 6, 1, 0, 0)
effective_data_cutoff = datetime.datetime(2026, 1, 1, 0, 0, tzinfo=datetime.timezone.utc)

    def select_parameter_set_for_valuation(
        parameter_registry: Optional[ParameterRegistry] = None,
        parameter_as_of: Optional[datetime] = None,
        *,
        effective_data_cutoff: Optional[datetime] = None,
    ) -> Tuple[ParameterSetVersion, Dict[str, object]]:
        """Choose the parameter set for one valuation, with truthful provenance.

        Selection precedence (D9):

        * No registry and no as-of: legacy Genesis path, labelled
          ``FIXED_GENESIS_LEGACY``; ``data_cutoff_used_for_parameter_selection``
          is ``False`` and the caveat states that temporal validity is NOT
          verified. This never claims historical validity.
        * A caller-supplied ``parameter_as_of`` that disagrees with
          ``effective_data_cutoff`` raises ``ValueError`` — no silent selection
          using a conflicting timestamp.
        * When ``effective_data_cutoff`` is present it is the governing timestamp
          for dated selection; ``data_cutoff_used_for_parameter_selection`` is
          ``True`` and ``as_of_source`` is ``DATA_CUTOFF``.
        * With no cutoff but an explicit ``parameter_as_of``, selection proceeds
          on the caller-supplied instant and the provenance records
          ``as_of_source == "CALLER_SUPPLIED"`` and
          ``data_cutoff_used_for_parameter_selection == False`` — no cutoff is
          invented.
        * With neither cutoff nor as-of (but a registry), a ``LookupError`` is
          raised; selection without a governing instant is undefined.

        Dated selection is delegated to ``resolve_parameter_set_as_of``:
        undated genesis records never stand in for history, future-effective
        versions never leak in, and overlapping effective dates raise instead of
        picking silently.

        Which date governs selection in production (cutoff, valuation date, or
        another instant) remains the R8/D9 decision; the caller supplies
        ``effective_data_cutoff`` explicitly and provenance records it as such.
        """
        cutoff_norm: Optional[datetime] = (
            None if effective_data_cutoff is None else normalize_datetime(effective_data_cutoff)
        )
        as_of_norm: Optional[datetime] = (
            None if parameter_as_of is None else normalize_datetime(parameter_as_of)
        )

        if parameter_registry is None and as_of_norm is None:
            # Legacy Genesis path (backward compatible). If the caller supplied a
            # cutoff but no registry, we still cannot select a dated set (the
            # default registry only contains undated genesis); the honest answer
            # is the legacy path with an explicit unverified marker.
            live = live_genesis_parameter_set()
            live_values = {r.parameter_name: r.parameter_value for r in live.records}
            import_values = {r.parameter_name: r.parameter_value for r in GENESIS_VERSION.records}
            return live, {
                "mode": "FIXED_GENESIS_LEGACY",
                "point_in_time_selection_applied": False,
                "as_of_requested": None if cutoff_norm is None else cutoff_norm.isoformat(),
                "as_of_source": None,
                "data_cutoff_used_for_parameter_selection": False,
                "module_constants_modified_since_import": live_values != import_values,
                "caveat": (
                    "Undated genesis constants; temporal validity for historical "
                    "valuation is NOT verified (R8/D9 pending)."
                ),
            }

        registry = DEFAULT_REGISTRY if parameter_registry is None else parameter_registry

        # Conflict detection: an explicitly-supplied as-of must agree with the
        # effective data cutoff, otherwise we would be selecting parameters using
        # a timestamp that contradicts the governing data cutoff.
        if as_of_norm is not None and cutoff_norm is not None and as_of_norm != cutoff_norm:
>           raise ValueError(
                "parameter_as_of conflicts with the effective valuation data cutoff "
                f"(parameter_as_of={as_of_norm.isoformat()}, "
                f"effective_data_cutoff={cutoff_norm.isoformat()}); refusing to "
                "select parameters using a conflicting timestamp."
            )
E           ValueError: parameter_as_of conflicts with the effective valuation data cutoff (parameter_as_of=2025-06-01T00:00:00+00:00, effective_data_cutoff=2026-01-01T00:00:00+00:00); refusing to select parameters using a conflicting timestamp.

src\valuation\parameters.py:522: ValueError
=============================================== short test summary info ===============================================
FAILED src/tests/test_stage7_valuation.py::test_p35_as_of_selection_governs_calculation_and_snapshot_matches - AssertionError: assert '2026-06-01T00:00:00+00:00' == '2026-01-01T00:00:00+00:00'
FAILED src/tests/test_stage7_valuation.py::test_p35_selected_set_governs_peers_alerts_and_scenario_weights - ValueError: parameter_as_of conflicts with the effective valuation data cutoff (parameter_as_of=2026-06-01T00:00:00...
FAILED src/tests/test_stage7_valuation.py::test_p35_missing_or_ambiguous_as_of_selection_fails_closed - Failed: DID NOT RAISE LookupError
FAILED src/tests/test_stage7_valuation.py::test_p35_invalid_parameter_set_raises_without_fallback_to_constants - ValueError: parameter_as_of conflicts with the effective valuation data cutoff (parameter_as_of=2026-06-01T00:00:00...
FAILED src/tests/test_stage7_valuation.py::test_p35_isolation_from_global_mutation_and_snapshot_aliasing - ValueError: parameter_as_of conflicts with the effective valuation data cutoff (parameter_as_of=2026-06-01T00:00:00...
FAILED src/tests/test_stage7_valuation.py::test_p35_repeated_as_of_calculations_are_deterministic - ValueError: parameter_as_of conflicts with the effective valuation data cutoff (parameter_as_of=2025-06-01T00:00:00...
============================================ 6 failed, 85 passed in 1.56s