"""Stage 6 Prompt 36: versioned artifact identity + provenance tests.

Proves the artifact contract end to end: distinct run_ids per execution,
version constants, purpose validation, supersedes linkage, frozen value
semantics, pipeline wiring (cutoff honesty, per-series ReportVersion
provenance, missing-provenance emptiness), the sensitivity path
(ESTIMATED excluded under a named reason, VALID still scores), scenario
isolation in provenance, and adversarial boundaries.
"""

from dataclasses import FrozenInstanceError
from datetime import datetime, timezone

import pytest

from src.evaluation.aggregate import (
    aggregate_observations,
    score_observation,
)
from src.evaluation.artifact import (
    ARTIFACT_CONTRACT_VERSION,
    ARTIFACT_PURPOSES,
    DATA_QUALITY_POLICY_VERSION,
    EvaluationArtifactIdentity,
    SeriesProvenance,
    build_artifact,
)
from src.evaluation.observation import build_observation, flag_duplicates
from src.evaluation.pipeline import (
    PIPELINE_PARAMETERS_VERSION,
    run_evaluation_pipeline,
)
from src.evaluation.schema import ActualObservation
from src.forecast.schema import ForecastRecord

CUTOFF = datetime(2024, 6, 30, tzinfo=timezone.utc)
CUTOFF_OTHER = datetime(2024, 3, 31, tzinfo=timezone.utc)
AFTER = datetime(2024, 9, 30, tzinfo=timezone.utc)
STAMP = datetime(2024, 7, 1, tzinfo=timezone.utc)

SCENARIOS = ("BEAR", "BASE", "BULL")


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


def _series_key(scenario="BASE", company=7, horizon="12M", version="V1.0"):
    return (company, "REVENUE", horizon, version, scenario)


def _run(records, actuals, **kwargs):
    return run_evaluation_pipeline(records, ["REVENUE"], actuals, **kwargs)


# --- L1: identity unit -------------------------------------------------------


def test_run_ids_distinct_on_identical_inputs():
    first = build_artifact(
        purpose="PRIMARY", methodology_version="STAGE6_V1"
    )
    second = build_artifact(
        purpose="PRIMARY", methodology_version="STAGE6_V1"
    )
    assert first.run_id != second.run_id
    assert first.run_id and second.run_id


def test_version_constants_distinct():
    assert ARTIFACT_CONTRACT_VERSION == "ARTIFACT_V1"
    assert PIPELINE_PARAMETERS_VERSION == "STAGE6_V1"
    assert DATA_QUALITY_POLICY_VERSION == "DATA_QUALITY_P25"
    assert len(
        {
            ARTIFACT_CONTRACT_VERSION,
            PIPELINE_PARAMETERS_VERSION,
            DATA_QUALITY_POLICY_VERSION,
        }
    ) == 3


def test_artifact_purposes_exact():
    assert ARTIFACT_PURPOSES == ("PRIMARY", "SENSITIVITY_ESTIMATED_EXCLUDED")


def test_build_artifact_bad_purpose_raises():
    with pytest.raises(ValueError):
        build_artifact(purpose="BOGUS", methodology_version="STAGE6_V1")


def test_build_artifact_malformed_purposes_raise():
    for bad in ("", "primary", "Primary", " PRIMARY", "PRIMARY "):
        with pytest.raises(ValueError):
            build_artifact(purpose=bad, methodology_version="STAGE6_V1")


def test_direct_constructor_bad_purpose_raises():
    with pytest.raises(ValueError):
        EvaluationArtifactIdentity(
            run_id="X",
            artifact_version=ARTIFACT_CONTRACT_VERSION,
            methodology_version="STAGE6_V1",
            quality_policy_version=DATA_QUALITY_POLICY_VERSION,
            purpose="BOGUS",
            evaluation_cutoff=None,
        )


def test_supersedes_preserved():
    artifact = build_artifact(
        purpose="PRIMARY",
        methodology_version="STAGE6_V1",
        supersedes="prior-run-id",
    )
    assert artifact.supersedes == "prior-run-id"


def test_self_supersede_raises():
    with pytest.raises(ValueError):
        build_artifact(
            purpose="PRIMARY",
            methodology_version="STAGE6_V1",
            run_id="FIXED",
            supersedes="FIXED",
        )


def test_empty_supersedes_raises():
    with pytest.raises(ValueError):
        build_artifact(
            purpose="PRIMARY", methodology_version="STAGE6_V1", supersedes=""
        )


def test_direct_constructor_self_and_empty_supersede_raise():
    with pytest.raises(ValueError):
        EvaluationArtifactIdentity(
            run_id="X",
            artifact_version=ARTIFACT_CONTRACT_VERSION,
            methodology_version="STAGE6_V1",
            quality_policy_version=DATA_QUALITY_POLICY_VERSION,
            purpose="PRIMARY",
            evaluation_cutoff=None,
            supersedes="X",
        )
    with pytest.raises(ValueError):
        EvaluationArtifactIdentity(
            run_id="X",
            artifact_version=ARTIFACT_CONTRACT_VERSION,
            methodology_version="STAGE6_V1",
            quality_policy_version=DATA_QUALITY_POLICY_VERSION,
            purpose="PRIMARY",
            evaluation_cutoff=None,
            supersedes="",
        )


def test_frozen_immutability():
    artifact = build_artifact(
        purpose="PRIMARY", methodology_version="STAGE6_V1"
    )
    with pytest.raises(FrozenInstanceError):
        artifact.purpose = "SENSITIVITY_ESTIMATED_EXCLUDED"  # type: ignore[misc]
    provenance = SeriesProvenance(series=_series_key())
    with pytest.raises(FrozenInstanceError):
        provenance.series = _series_key("BEAR")  # type: ignore[misc]


def test_equality_by_value():
    kwargs = dict(
        purpose="PRIMARY",
        methodology_version="STAGE6_V1",
        evaluation_cutoff=CUTOFF,
        run_id="FIXED",
    )
    assert build_artifact(**kwargs) == build_artifact(**kwargs)


def test_series_provenance_defaults_empty():
    provenance = SeriesProvenance(series=_series_key())
    assert provenance.report_version_ids == ()
    assert provenance.publication_datetimes == ()
    assert provenance.data_quality_states == ()


def test_methodology_version_arrives_as_argument():
    artifact = build_artifact(
        purpose="PRIMARY", methodology_version="CUSTOM_V9"
    )
    assert artifact.methodology_version == "CUSTOM_V9"


def test_scenario_keys_intact_in_provenance():
    entries = [
        SeriesProvenance(series=_series_key(scenario)) for scenario in SCENARIOS
    ]
    artifact = build_artifact(
        purpose="PRIMARY",
        methodology_version="STAGE6_V1",
        series_provenance=entries,
    )
    assert {item.series[-1] for item in artifact.series_provenance} == set(
        SCENARIOS
    )


# --- L2: pipeline wiring -----------------------------------------------------


def test_pipeline_result_carries_artifact():
    result = _run([_record()], {(7, 101, "REVENUE"): _actual()})
    assert result.artifact is not None
    assert result.artifact.artifact_version == ARTIFACT_CONTRACT_VERSION
    assert result.artifact.methodology_version == PIPELINE_PARAMETERS_VERSION
    assert result.artifact.quality_policy_version == DATA_QUALITY_POLICY_VERSION
    assert result.artifact.purpose == "PRIMARY"
    assert result.artifact.supersedes is None


def test_cutoff_single_populated():
    result = _run([_record()], {(7, 101, "REVENUE"): _actual()})
    assert result.artifact is not None
    assert result.artifact.evaluation_cutoff == CUTOFF


def test_cutoff_mixed_raises_fail_closed():
    # Stage 6 Prompt 38 (Prompt 38 section 4): mixed distinct non-null
    # cutoffs fail closed before any scoring or artifact — no partial
    # successful result.
    records = [
        _record(forecast_id=1, data_cutoff_datetime=CUTOFF),
        _record(forecast_id=2, data_cutoff_datetime=CUTOFF_OTHER),
    ]
    with pytest.raises(ValueError, match="mixed evaluation cutoffs"):
        _run(records, {(7, 101, "REVENUE"): _actual()})


def test_cutoff_empty_records_none():
    result = run_evaluation_pipeline([], ["REVENUE"], {})
    assert result.artifact is not None
    assert result.artifact.evaluation_cutoff is None
    assert result.artifact.series_provenance == ()
    assert result.series_count == 0


def test_fabricated_default_check_missing_provenance_empty():
    result = _run([_record()], {})
    assert result.artifact is not None
    assert len(result.artifact.series_provenance) == 1
    entry = result.artifact.series_provenance[0]
    assert entry.series == _series_key()
    assert entry.report_version_ids == ()
    assert entry.publication_datetimes == ()
    assert entry.data_quality_states == ()


def test_rerun_distinct_run_ids_same_inputs():
    records = [_record()]
    actuals = {(7, 101, "REVENUE"): _actual()}
    first = _run(records, actuals)
    second = _run(records, actuals)
    assert first.artifact is not None and second.artifact is not None
    assert first.artifact.run_id != second.artifact.run_id


def test_primary_vs_sensitivity_purposes_differ():
    records = [_record()]
    actuals = {(7, 101, "REVENUE"): _actual()}
    primary = _run(records, actuals)
    sensitivity = _run(records, actuals, exclude_estimated=True)
    assert primary.artifact is not None and sensitivity.artifact is not None
    assert primary.artifact.purpose == "PRIMARY"
    assert (
        sensitivity.artifact.purpose == "SENSITIVITY_ESTIMATED_EXCLUDED"
    )
    assert primary.artifact.run_id != sensitivity.artifact.run_id


def test_rerun_without_supersedes_has_none():
    result = _run([_record()], {(7, 101, "REVENUE"): _actual()})
    assert result.artifact is not None
    assert result.artifact.supersedes is None


# --- L3: real pipeline behavior ----------------------------------------------


def test_primary_estimated_scores_with_limited_quality():
    actual = _actual(data_quality_state="ESTIMATED")
    result = _run([_record()], {(7, 101, "REVENUE"): actual})
    verdict = result.verdicts[_series_key()]
    assert verdict.series.observation_count == 1
    assert verdict.series.limited_quality is True
    assert "SENSITIVITY_ESTIMATED_EXCLUDED" not in result.quarantined


def test_sensitivity_estimated_quarantined_valid_scores():
    estimated_record = _record(forecast_id=1, forecast_period_id=101)
    valid_record = _record(forecast_id=2, forecast_period_id=102)
    actuals = {
        (7, 101, "REVENUE"): _actual(
            financial_period_id=101, data_quality_state="ESTIMATED"
        ),
        (7, 102, "REVENUE"): _actual(
            financial_period_id=102,
            report_version_id=77,
            publication_datetime=STAMP,
        ),
    }
    result = _run(
        [estimated_record, valid_record], actuals, exclude_estimated=True
    )
    assert result.artifact is not None
    assert result.artifact.purpose == "SENSITIVITY_ESTIMATED_EXCLUDED"
    verdict = result.verdicts[_series_key()]
    assert verdict.series.observation_count == 1
    assert (
        verdict.series.quarantined.get("SENSITIVITY_ESTIMATED_EXCLUDED") == 1
    )
    assert verdict.series.limited_quality is False


def test_multi_scenario_separate_provenance_entries():
    shared = _actual()
    records = [_record(forecast_id=i + 1, scenario=scenario) for i, scenario in enumerate(SCENARIOS)]
    result = _run(records, {(7, 101, "REVENUE"): shared})
    assert result.artifact is not None
    # Counterfactual pin: scenario must stay in provenance grouping — one
    # entry per scenario track, never pooled.
    assert len(result.artifact.series_provenance) == 3
    assert {item.series[-1] for item in result.artifact.series_provenance} == set(
        SCENARIOS
    )


def test_report_version_id_and_publication_surfaced():
    result = _run([_record()], {(7, 101, "REVENUE"): _actual()})
    assert result.artifact is not None
    assert len(result.artifact.series_provenance) == 1
    entry = result.artifact.series_provenance[0]
    assert entry.report_version_ids == (55,)
    assert entry.publication_datetimes == (AFTER,)
    assert entry.data_quality_states == ("VALID",)


def test_multi_period_series_keeps_distinct_report_versions():
    records = [
        _record(forecast_id=1, forecast_period_id=101),
        _record(forecast_id=2, forecast_period_id=102),
    ]
    actuals = {
        (7, 101, "REVENUE"): _actual(financial_period_id=101),
        (7, 102, "REVENUE"): _actual(
            financial_period_id=102,
            report_version_id=77,
            publication_datetime=STAMP,
        ),
    }
    result = _run(records, actuals)
    assert result.artifact is not None
    assert len(result.artifact.series_provenance) == 1
    entry = result.artifact.series_provenance[0]
    assert entry.report_version_ids == (55, 77)
    assert entry.publication_datetimes == (STAMP, AFTER)


def test_rerun_with_supersedes_preserved():
    records = [_record()]
    actuals = {(7, 101, "REVENUE"): _actual()}
    first = _run(records, actuals)
    assert first.artifact is not None
    second = _run(records, actuals, supersedes=first.artifact.run_id)
    assert second.artifact is not None
    assert second.artifact.supersedes == first.artifact.run_id
    assert second.artifact.run_id != first.artifact.run_id


def test_invalid_report_version_yields_empty_provenance():
    bad = _actual(report_version_id=None)
    observation = build_observation(_record(), "REVENUE", bad)
    assert observation.evaluation_status == "INVALID_REPORT_VERSION"
    result = _run([_record()], {(7, 101, "REVENUE"): bad})
    assert result.artifact is not None
    assert len(result.artifact.series_provenance) == 1
    entry = result.artifact.series_provenance[0]
    assert entry.report_version_ids == ()
    assert entry.publication_datetimes == ()
    assert entry.data_quality_states == ()


def test_shared_actual_across_scenarios_no_pooling():
    shared = _actual()
    records = [_record(forecast_id=i + 1, scenario=scenario) for i, scenario in enumerate(SCENARIOS)]
    result = _run(records, {(7, 101, "REVENUE"): shared})
    assert result.series_count == 3
    assert result.observation_count == 3
    for scenario in SCENARIOS:
        assert result.verdicts[_series_key(scenario)].series.total_observations == 1


def test_partial_provenance_valid_plus_pending():
    records = [
        _record(forecast_id=1, forecast_period_id=101),
        _record(forecast_id=2, forecast_period_id=102),
    ]
    result = _run(records, {(7, 101, "REVENUE"): _actual()})
    assert result.artifact is not None
    assert len(result.artifact.series_provenance) == 1
    entry = result.artifact.series_provenance[0]
    assert entry.report_version_ids == (55,)
    # The PENDING_ACTUAL observation quarantines inside the same series; the
    # missing outcome is empty provenance, never an invented id.
    assert result.quarantined.get("PENDING_ACTUAL") == 1


def test_forced_duplicate_run_id_distinguishable_by_purpose():
    primary = build_artifact(
        purpose="PRIMARY", methodology_version="STAGE6_V1", run_id="FIXED"
    )
    sensitivity = build_artifact(
        purpose="SENSITIVITY_ESTIMATED_EXCLUDED",
        methodology_version="STAGE6_V1",
        run_id="FIXED",
    )
    assert primary.run_id == sensitivity.run_id
    assert primary.purpose != sensitivity.purpose


def test_self_referential_supersedes_raises_in_pipeline():
    records = [_record()]
    actuals = {(7, 101, "REVENUE"): _actual()}
    first = _run(records, actuals)
    assert first.artifact is not None
    # A rerun pointing at itself is rejected at the construction boundary.
    with pytest.raises(ValueError):
        build_artifact(
            purpose="PRIMARY",
            methodology_version="STAGE6_V1",
            run_id="FIXED",
            supersedes="FIXED",
        )


# --- L4: sensitivity ordering + aggregation threading ------------------------


def test_sensitivity_exclusion_order_after_ready_and_duplicate():
    invalid = _actual(
        report_version_id=None, data_quality_state="ESTIMATED"
    )
    observation = build_observation(_record(), "REVENUE", invalid)
    scored = score_observation(observation, exclude_estimated=True)
    assert scored.scored is False
    assert scored.exclusion_reason == "INVALID_REPORT_VERSION"


def test_duplicate_beats_sensitivity_exclusion():
    estimated = _actual(data_quality_state="ESTIMATED")
    observations = flag_duplicates(
        [
            build_observation(_record(), "REVENUE", estimated),
            build_observation(_record(), "REVENUE", estimated),
        ]
    )
    scored = [
        score_observation(item, exclude_estimated=True)
        for item in observations
    ]
    assert all(item.exclusion_reason == "DUPLICATE_QUARANTINED" for item in scored)


def test_aggregate_observations_threads_exclude_estimated():
    estimated = _actual(data_quality_state="ESTIMATED")
    observations = [
        build_observation(_record(), "REVENUE", estimated),
    ]
    primary = aggregate_observations(observations)
    sensitivity = aggregate_observations(observations, exclude_estimated=True)
    assert primary[_series_key()].observation_count == 1
    series = sensitivity[_series_key()]
    assert series.observation_count == 0
    assert series.quarantined.get("SENSITIVITY_ESTIMATED_EXCLUDED") == 1


def test_aggregate_default_path_unchanged():
    observations = [build_observation(_record(), "REVENUE", _actual())]
    result = aggregate_observations(observations)
    assert result[_series_key()].observation_count == 1
    assert result[_series_key()].quarantined == {}
