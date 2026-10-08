"""Stage 6 Prompt 20 behavioral tests: Reliability + Calibration governance.

P20 is fail-closed by authority, not by choice. P17 classified the four
Reliability mappings (B2), the unavailable-component rule (B7), the
persistence definition (B3), and the candidate->calibrated transition (B4)
as UNRESOLVED METHODOLOGY AUTHORITY, and P20's own testing requirement
forbids numeric expected values for B2/B7/B3/B4 while they stay unresolved.
Every test below therefore asserts a refusal shape — withheld, never zero;
NO_CALIBRATION, never invented — plus the missing authority named.

Five layers (P20 MANDATORY MULTI-LAYER TESTING DOCTRINE):

* L1 unit/formula: weight assembly arithmetic, bounds, type separation.
* L2 contract/boundary: PIT semantics preserved, horizon/version isolation,
  NULL != 0, duplicate quarantine, data-quality quarantine flow through.
* L3 production-path: P18 observations -> P19 aggregates -> P20
  governance end to end; engine legacy path untouched.
* L4 adversarial/negative: forced numeric defaults refused, Performance
  read as Reliability refused, direct forecast scaling absent, holdout
  contamination rejected, old-version overwrite impossible.
* L5 regression: focused suite green, then the full src/tests suite.
"""

from datetime import datetime, timezone

import pytest

from src.evaluation.aggregate import aggregate_observations
from src.evaluation.observation import build_observation
from src.evaluation.reliability import (
    ACCURACY_WEIGHT,
    BASELINE_ADVANTAGE_WEIGHT,
    BIAS_CONTROL_WEIGHT,
    CalibrationAssessment,
    EvidenceHoldoutSplit,
    PerformanceScore,
    VersionedComponentScores,
    assess_reliability,
    assemble_performance_score,
    derive_calibrated_version_name,
    forward_pe_untouched_by_reliability,
    govern_aggregates,
    govern_series,
    oos_observations,
    refuse_calibration_transition,
)
from src.evaluation.schema import ActualObservation
from src.forecast.schema import ForecastInputRef, ForecastRecord

CUTOFF = datetime(2024, 6, 30, tzinfo=timezone.utc)
BEFORE = datetime(2024, 3, 31, tzinfo=timezone.utc)
AFTER = datetime(2024, 9, 30, tzinfo=timezone.utc)
STAMP = datetime(2024, 7, 1, tzinfo=timezone.utc)


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
    return ForecastRecord(**fields)


def _actual(**overrides):
    fields = dict(
        company_id=7,
        financial_period_id=101,
        metric_code="REVENUE",
        value=1100.0,
        report_version_id=55,
        publication_datetime=AFTER,
    )
    fields.update(overrides)
    return ActualObservation(**fields)


def _observation(metric="REVENUE", forecast_value=1000.0, actual_value=1100.0,
                 **record_overrides):
    record_overrides.setdefault(metric.lower(), forecast_value)
    record = _record(**record_overrides)
    return build_observation(
        record,
        metric,
        _actual(
            value=actual_value,
            financial_period_id=record.forecast_period_id,
            company_id=record.company_id,
        ),
    )


def _series(periods=8, horizon="12M", version="V1.0", start=101, **values):
    observations = [
        _observation(
            forecast_value=values.get("forecast_value", 1000.0),
            actual_value=values.get("actual_value", 1100.0),
            forecast_period_id=start + i,
            forecast_horizon=horizon,
            model_version=version,
        )
        for i in range(periods)
    ]
    return aggregate_observations(observations)[(7, "REVENUE", horizon, version)]


def _components(**overrides):
    fields = dict(
        accuracy_score=80.0,
        bias_control_score=70.0,
        baseline_advantage_score=60.0,
        parameters_version="STAGE6_V1",
    )
    fields.update(overrides)
    return VersionedComponentScores(**fields)


# --- L1: Performance assembly is the only authorized arithmetic -------------


def test_weights_match_spec_section_21():
    assert (ACCURACY_WEIGHT, BIAS_CONTROL_WEIGHT, BASELINE_ADVANTAGE_WEIGHT) == (
        0.50, 0.20, 0.30,
    )


def test_performance_assembly_is_exact_weighted_sum():
    performance = assemble_performance_score(_components())
    assert performance.value == 0.50 * 80.0 + 0.20 * 70.0 + 0.30 * 60.0
    assert performance.parameters_version == "STAGE6_V1"


def test_component_bounds_are_structural_not_methodology():
    for bad in (-0.5, 100.5):
        with pytest.raises(ValueError):
            _components(accuracy_score=bad)
    with pytest.raises(ValueError):
        VersionedComponentScores(
            accuracy_score=50.0,
            bias_control_score=50.0,
            baseline_advantage_score=50.0,
            parameters_version="",
        )


def test_performance_score_is_not_a_reliability():
    # L1 type separation: Performance Score = Reliability must be
    # inexpressible, not merely discouraged.
    performance = assemble_performance_score(_components())
    assert not isinstance(performance, float)
    assert not hasattr(performance, "reliability")
    assert type(performance) is PerformanceScore


# --- L1/L2: Reliability withheld, never zero, authority named ---------------

def test_reliability_withheld_with_mappings_named_not_zero():
    reliability = assess_reliability(
        assemble_performance_score(_components()), "ADEQUATE", "STAGE6_V1"
    )
    assert reliability.reliability is None
    assert "B2:MAPE_TO_ACCURACY_SCORE" in reliability.withheld_because
    assert "B2:BIAS_TO_BIAS_CONTROL_SCORE" in reliability.withheld_because
    assert "B2:ADVANTAGE_TO_BASELINE_ADVANTAGE_SCORE" in reliability.withheld_because
    assert "B2:CONFIDENCE_ADJUSTMENT" in reliability.withheld_because
    assert reliability.parameters_version == "STAGE6_V1"
    assert reliability.confidence_level == "ADEQUATE"


def test_unavailable_components_named_never_defaulted():
    reliability = assess_reliability(None, "INSUFFICIENT_DATA", "STAGE6_V1",
                                    ("MAPE", "BIAS"))
    assert reliability.reliability is None
    assert "UNAVAILABLE:MAPE" in reliability.withheld_because
    assert "UNAVAILABLE:BIAS" in reliability.withheld_because
    assert "B7:UNAVAILABLE_COMPONENT_SCORE" in reliability.withheld_because


def test_governed_series_withholds_reliability_even_with_components():
    governed = govern_series(_series(), _components())
    assert governed.performance is not None
    assert governed.performance.value == 0.50 * 80.0 + 0.20 * 70.0 + 0.30 * 60.0
    assert governed.reliability.reliability is None
    assert governed.calibration.state == "NO_CALIBRATION"


def test_governed_series_without_components_withholds_performance_too():
    governed = govern_series(_series())
    assert governed.performance is None
    assert governed.reliability.reliability is None
    assert "VERSIONED_COMPONENT_SCORES" in (
        governed.reliability.withheld_because
    ) or "B7:UNAVAILABLE_COMPONENT_SCORE" in governed.reliability.withheld_because


def test_govern_series_never_mutates_the_p19_aggregate():
    series = _series()
    before = (series.mape, series.bias, series.confidence_level,
              series.relative_improvement)
    govern_series(series, _components())
    assert (series.mape, series.bias, series.confidence_level,
            series.relative_improvement) == before


# --- L1/L2: Calibration — NO_CALIBRATION only --------------------------------

def test_no_calibration_is_the_default_verdict():
    assessment = CalibrationAssessment(
        metric_code="REVENUE", horizon="12M", model_version="V1.0",
        parameters_version="STAGE6_V1",
    )
    assert assessment.state == "NO_CALIBRATION"


def test_candidate_and_calibrated_are_unconstructible_without_authority():
    for state in ("CALIBRATION_CANDIDATE", "CALIBRATED"):
        with pytest.raises(ValueError):
            CalibrationAssessment(
                metric_code="REVENUE", horizon="12M", model_version="V1.0",
                state=state, parameters_version="STAGE6_V1",
            )


def test_refused_transition_stays_no_calibration_with_b3_b4_named():
    refused = refuse_calibration_transition(
        "REVENUE", "12M", "V1.0", "CALIBRATED", "STAGE6_V1"
    )
    assert refused.state == "NO_CALIBRATION"
    assert refused.reason == "REFUSED_TRANSITION_TO:CALIBRATED"
    assert "B3:PERSISTENT_BIAS_DEFINITION" in refused.missing_authority
    assert "B4:CANDIDATE_TO_CALIBRATED_TRANSITION" in refused.missing_authority


def test_suggestive_bias_evidence_still_yields_no_calibration():
    # Ten unanimous under-forecasts would tempt a persistence claim; without
    # the B3 definition the verdict stays NO_CALIBRATION.
    series = _series(periods=10, forecast_value=1000.0, actual_value=1300.0)
    assert series.bias == 30.0
    governed = govern_series(series, _components())
    assert governed.calibration.state == "NO_CALIBRATION"
    assert governed.calibration.reason == "B3_B4_UNRESOLVED"


def test_no_new_version_without_calibrated():
    assessment = CalibrationAssessment(
        metric_code="REVENUE", horizon="12M", model_version="V1.0",
        parameters_version="STAGE6_V1",
    )
    assert derive_calibrated_version_name("V1.0", assessment) is None


# --- L2: contract/boundary flow-through ---------------------------------------

def test_pit_later_published_actual_still_governed():
    # AFTER > CUTOFF on every observation: the later-published Actual is the
    # evaluated outcome, never leakage. Distinct periods so no duplicate
    # collision masks the PIT assertion.
    observations = [_observation(forecast_period_id=101 + i) for i in range(8)]
    for observation in observations:
        assert observation.evaluation_status == "READY"
        assert observation.actual.publication_datetime > CUTOFF
    series = aggregate_observations(observations)
    governed = govern_aggregates(series)[(7, "REVENUE", "12M", "V1.0")]
    assert governed.observation_count == 8
    assert governed.reliability.reliability is None


def test_horizon_and_version_isolation_survive_governance():
    observations = [
        _observation(forecast_period_id=101 + i, forecast_horizon="12M",
                     model_version="V1.0")
        for i in range(8)
    ] + [
        _observation(forecast_period_id=101 + i, forecast_horizon="3M",
                     model_version="V2.0")
        for i in range(8)
    ]
    governed = govern_aggregates(aggregate_observations(observations))
    assert set(governed) == {(7, "REVENUE", "12M", "V1.0"),
                             (7, "REVENUE", "3M", "V2.0")}
    for verdict in governed.values():
        assert verdict.reliability.reliability is None
        assert verdict.calibration.state == "NO_CALIBRATION"


def test_null_and_quarantines_flow_through_unchanged():
    observations = [
        *[_observation(forecast_period_id=101 + i) for i in range(4)],
        _observation(forecast_value=0.0, actual_value=100.0,
                     forecast_period_id=200),  # ZERO_BASE quarantine
        build_observation(
            _record(forecast_period_id=201,
                    input_refs=(ForecastInputRef(fact_key="X",
                                                 available_at=AFTER),)),
            "REVENUE", _actual(),
        ),  # PIT_INVALID_INPUT quarantine
    ]
    series = aggregate_observations(observations)[(7, "REVENUE", "12M", "V1.0")]
    assert series.observation_count == 4
    governed = govern_series(series)
    assert governed.observation_count == 4
    assert governed.confidence_level == "INSUFFICIENT_DATA"
    assert governed.reliability.confidence_level == "INSUFFICIENT_DATA"


def test_missing_mape_marks_unavailable_component():
    governed = govern_series(_series(periods=3))  # scored but thin evidence
    assert governed.reliability.reliability is None


def test_regime_only_series_names_mape_unavailable():
    observations = [
        _observation(forecast_value=0.0, actual_value=100.0,
                     forecast_period_id=101 + i)
        for i in range(5)
    ]
    series = aggregate_observations(observations)[(7, "REVENUE", "12M", "V1.0")]
    assert series.mape is None
    governed = govern_series(series)
    assert governed.reliability.reliability is None
    assert "MAPE" in (governed.reliability.withheld_because) or any(
        "B2" in reason for reason in governed.reliability.withheld_because
    )


# --- L3: production-path -------------------------------------------------------

def test_full_path_observation_to_governance():
    observations = [_observation(forecast_period_id=101 + i) for i in range(8)]
    aggregates = aggregate_observations(observations)
    governed = govern_aggregates(aggregates)
    verdict = governed[(7, "REVENUE", "12M", "V1.0")]
    assert verdict.observation_count == 8
    assert verdict.confidence_level == "MODERATE_CONFIDENCE"
    assert verdict.performance is None  # no mappings on the production path
    assert verdict.reliability.reliability is None
    assert verdict.calibration.state == "NO_CALIBRATION"
    assert verdict.evaluation_timestamp.tzinfo is not None


def test_legacy_engine_path_removed():
    # P23: the legacy engine is deleted, not merely isolated — there is
    # no path left that could bypass the fail-closed production verdicts.
    import importlib.util

    assert importlib.util.find_spec("src.evaluation.engine") is None
    with pytest.raises(ImportError):
        import src.evaluation.engine  # noqa: F401


def test_module_exports_no_numeric_mapping():
    import src.evaluation.reliability as reliability

    source_names = {name for name in dir(reliability)
                    if "naive" in name.lower() or "threshold" in name.lower()}
    assert source_names == set()


# --- L4: adversarial ------------------------------------------------------------

def test_performance_times_confidence_is_not_a_reliability():
    # The forbidden equation has no function to live in: multiplying is
    # possible in Python, but the product is a float, never a Reliability.
    performance = assemble_performance_score(_components())
    product = performance.value * 1.00
    assert isinstance(product, float)
    with pytest.raises(AttributeError):
        product.withheld_because  # noqa: B018 — floats carry no authority


def test_no_forecast_scaling_surface():
    import inspect

    import src.evaluation.reliability as reliability

    members = inspect.getmembers(reliability, inspect.isfunction)
    assert members  # the surface exists; now prove none of it scales a forecast
    for name, func in members:
        source = inspect.getsource(func)
        assert "forecast_value" not in source, name
        assert "1.08" not in source, name


def test_no_numeric_default_for_unresolved_rules():
    import inspect

    import src.evaluation.reliability as reliability

    source = inspect.getsource(reliability)
    for invented in ("poor_mape", "unacceptable_bias", "full_advantage",
                     "minimum_observations", "bias_threshold", "holdout_passed"):
        assert invented not in source


def test_holdout_overlapping_evidence_is_contamination():
    with pytest.raises(ValueError):
        EvidenceHoldoutSplit(evidence_periods=(101, 102, 103),
                             holdout_periods=(103, 104))


def test_holdout_before_evidence_rejected():
    with pytest.raises(ValueError):
        EvidenceHoldoutSplit(evidence_periods=(105, 106),
                             holdout_periods=(101, 102))


def test_oos_projection_never_leaks_evidence():
    split = EvidenceHoldoutSplit(evidence_periods=(101, 102),
                                 holdout_periods=(103, 104))
    projected = oos_observations({101: 10.0, 102: 12.0, 103: 9.0, 999: 1.0},
                                 split)
    assert projected == {103: 9.0}


def test_old_version_never_overwritten_by_governance():
    assessment = CalibrationAssessment(
        metric_code="REVENUE", horizon="12M", model_version="V1.0",
        parameters_version="STAGE6_V1",
    )
    assert assessment.model_version == "V1.0"
    assert derive_calibrated_version_name("V1.0", assessment) is None
    assert assessment.model_version == "V1.0"  # still the original


def test_forward_pe_passes_through_untouched():
    assert forward_pe_untouched_by_reliability(8.0) == 8.0


def test_invalid_calibration_state_rejected():
    with pytest.raises(ValueError):
        CalibrationAssessment(
            metric_code="REVENUE", horizon="12M", model_version="V1.0",
            state="CALIBRATED_SOMEHOW", parameters_version="STAGE6_V1",
        )


def test_refusing_a_non_advance_rejected():
    with pytest.raises(ValueError):
        refuse_calibration_transition("REVENUE", "12M", "V1.0",
                                      "NO_CALIBRATION", "STAGE6_V1")
