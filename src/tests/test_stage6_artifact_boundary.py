"""Stage 6 Prompt 37: production-boundary artifact presence (Case A).

Proves the production invariant: every successful `run_evaluation_pipeline`
return carries a valid artifact, including explicitly empty evaluations.
The Optional/None default on `EvaluationPipelineResult` exists only for
legacy direct construction — pinned here as a documented limitation, not
as a production path.
"""

from datetime import datetime, timezone

from src.evaluation.artifact import (
    ARTIFACT_CONTRACT_VERSION,
    DATA_QUALITY_POLICY_VERSION,
)
from src.evaluation.pipeline import (
    PIPELINE_PARAMETERS_VERSION,
    EvaluationPipelineResult,
    run_evaluation_pipeline,
)
from src.evaluation.schema import ActualObservation
from src.forecast.schema import ForecastRecord

CUTOFF = datetime(2024, 6, 30, tzinfo=timezone.utc)
CUTOFF_OTHER = datetime(2024, 3, 31, tzinfo=timezone.utc)
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


def _assert_valid_production_artifact(result, purpose):
    assert result.artifact is not None
    artifact = result.artifact
    assert artifact.run_id
    assert artifact.artifact_version == ARTIFACT_CONTRACT_VERSION
    assert artifact.methodology_version == PIPELINE_PARAMETERS_VERSION
    assert artifact.quality_policy_version == DATA_QUALITY_POLICY_VERSION
    assert artifact.purpose == purpose


def test_production_primary_result_carries_valid_artifact():
    result = run_evaluation_pipeline(
        [_record()], ["REVENUE"], {(7, 101, "REVENUE"): _actual()}
    )
    _assert_valid_production_artifact(result, "PRIMARY")
    assert result.artifact.evaluation_cutoff == CUTOFF


def test_production_empty_result_carries_explicit_empty_artifact():
    result = run_evaluation_pipeline([], ["REVENUE"], {})
    _assert_valid_production_artifact(result, "PRIMARY")
    assert result.artifact.evaluation_cutoff is None
    assert result.artifact.series_provenance == ()


def test_production_sensitivity_result_carries_valid_artifact():
    result = run_evaluation_pipeline(
        [_record()],
        ["REVENUE"],
        {(7, 101, "REVENUE"): _actual()},
        exclude_estimated=True,
    )
    _assert_valid_production_artifact(
        result, "SENSITIVITY_ESTIMATED_EXCLUDED"
    )


def test_production_mixed_cutoff_result_still_carries_artifact():
    records = [
        _record(forecast_id=1, data_cutoff_datetime=CUTOFF),
        _record(forecast_id=2, data_cutoff_datetime=CUTOFF_OTHER),
    ]
    result = run_evaluation_pipeline(
        records, ["REVENUE"], {(7, 101, "REVENUE"): _actual()}
    )
    assert result.artifact is not None
    # Honest None cutoff is never fabricated; the artifact is still present.
    assert result.artifact.evaluation_cutoff is None


def test_production_rerun_result_carries_artifact_with_supersedes():
    first = run_evaluation_pipeline(
        [_record()], ["REVENUE"], {(7, 101, "REVENUE"): _actual()}
    )
    assert first.artifact is not None
    second = run_evaluation_pipeline(
        [_record()],
        ["REVENUE"],
        {(7, 101, "REVENUE"): _actual()},
        supersedes=first.artifact.run_id,
    )
    _assert_valid_production_artifact(second, "PRIMARY")
    assert second.artifact.supersedes == first.artifact.run_id


def test_production_multi_scenario_result_carries_per_scenario_provenance():
    shared = _actual()
    records = [
        _record(forecast_id=i + 1, scenario=scenario)
        for i, scenario in enumerate(("BEAR", "BASE", "BULL"))
    ]
    result = run_evaluation_pipeline(
        records, ["REVENUE"], {(7, 101, "REVENUE"): shared}
    )
    _assert_valid_production_artifact(result, "PRIMARY")
    assert {
        item.series[-1] for item in result.artifact.series_provenance
    } == {"BEAR", "BASE", "BULL"}


def test_legacy_direct_construction_default_is_none_documented():
    # Compatibility limitation (Prompt 37 Case A): the None default exists
    # solely for legacy direct construction. No production path builds
    # results this way — run_evaluation_pipeline always attaches an artifact.
    assert EvaluationPipelineResult().artifact is None
