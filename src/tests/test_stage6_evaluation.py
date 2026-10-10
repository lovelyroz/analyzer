"""Stage 6 Prompt 23 — legacy methodology de-authorization proofs.

P23 §7: the legacy tests that asserted unauthorized methodology as
correct were converted into tests proving the legacy methodology is no
longer executable or authoritative. Nothing here assigns numeric
expected values to unresolved methodology (B1–B9); the only numbers
asserted are AUTHORITATIVE P18/P19 behaviors proving the new path
survived the removal intact.

Layers (P20 doctrine, P23 scope):

* L1 unit: each legacy symbol is gone from its home module.
* L2 contract/boundary: no legacy token survives in any production
  source; the package surface exports no legacy methodology.
* L3 production-path: the authorized pipeline still withholds
  Reliability and stays NO_CALIBRATION after the surgery.
* L4 adversarial: attempts to reach legacy scoring, legacy Seasonal
  Naive, legacy calibration minting, or the only remaining ``.CAL1``
  site all fail closed or are unreachable.
"""

import importlib.util
from datetime import datetime, timezone
from pathlib import Path

import pytest

import src.evaluation.metrics as metrics
import src.evaluation.schema as schema
from src.evaluation.pipeline import run_evaluation_pipeline
from src.evaluation.reliability import (
    CalibrationAssessment,
    derive_calibrated_version_name,
    refuse_calibration_transition,
)
from src.evaluation.schema import ActualObservation
from src.forecast.schema import ForecastRecord

LEGACY_SCORE_FUNCTIONS = (
    "accuracy_score_from_mape",
    "bias_score",
    "baseline_advantage_score",
    "confidence_multiplier",
    "detect_persistent_bias",
    "is_underperforming_baseline",
)

PRODUCTION_SOURCES = (
    "metrics.py",
    "observation.py",
    "aggregate.py",
    "reliability.py",
    "pipeline.py",
    "schema.py",
)

# Tokens of unauthorized methodology. Full ``def ...`` form where an
# authorized identifier shares a prefix (P20 ``VersionedComponentScores``
# fields are caller-supplied scores, not these mappings).
LEGACY_TOKENS = (
    "def accuracy_score_from_mape",
    "def bias_score(",
    "def baseline_advantage_score(",
    "def confidence_multiplier(",
    "def detect_persistent_bias(",
    "def is_underperforming_baseline(",
    "seasonal_naive_forecast",
    "history[-",
    "holdout_passed",
    "poor_mape",
    "unacceptable_bias",
    "full_advantage",
    "minimum_observations",
    "bias_threshold",
)


def _evaluation_source(name: str) -> str:
    return (Path(__file__).parent.parent / "evaluation" / name).read_text(
        encoding="utf-8"
    )


# --- L1: legacy symbols are gone --------------------------------------------

def test_legacy_score_functions_not_importable():
    for name in LEGACY_SCORE_FUNCTIONS:
        assert getattr(metrics, name, None) is None, name


def test_legacy_engine_module_removed():
    assert importlib.util.find_spec("src.evaluation.engine") is None
    with pytest.raises(ImportError):
        import src.evaluation.engine  # noqa: F401


def test_legacy_carriers_removed_from_schema():
    assert getattr(schema, "ForecastEvaluationResult", None) is None
    assert getattr(schema, "ReliabilityAssessment", None) is None


def test_package_surface_exports_no_legacy_methodology():
    import src.evaluation as package

    exported = set(getattr(package, "__all__", ()))
    assert "ForecastEvaluationEngine" not in exported
    assert "detect_persistent_bias" not in exported
    with pytest.raises(ImportError):
        from src.evaluation import ForecastEvaluationEngine  # noqa: F401


# --- L2: no legacy token in any production source ----------------------------

def test_production_sources_contain_no_legacy_tokens():
    for name in PRODUCTION_SOURCES:
        source = _evaluation_source(name)
        for token in LEGACY_TOKENS:
            assert token not in source, (name, token)


# --- L3: the authorized path survives intact ----------------------------------

CUTOFF = datetime(2024, 6, 30, tzinfo=timezone.utc)
AFTER = datetime(2024, 9, 30, tzinfo=timezone.utc)
STAMP = datetime(2024, 7, 1, tzinfo=timezone.utc)


def _record(period_id: int) -> ForecastRecord:
    return ForecastRecord(
        forecast_id=1,
        forecast_version=1,
        company_id=7,
        forecast_period_id=period_id,
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


def test_production_path_withholds_after_removal():
    periods = list(range(101, 109))
    records = [_record(period) for period in periods]
    actuals = {
        (7, period, "REVENUE"): ActualObservation(
            company_id=7,
            financial_period_id=period,
            metric_code="REVENUE",
            value=1100.0,
            report_version_id=55,
            publication_datetime=AFTER,
        )
        for period in periods
    }
    result = run_evaluation_pipeline(
        records=records, metric_codes=["REVENUE"], actuals=actuals
    )
    verdict = result.verdicts[(7, "REVENUE", "12M", "V1.0", "BASE")]
    assert verdict.series.mape == 10.0
    assert verdict.governance.reliability.reliability is None
    assert verdict.governance.calibration.state == "NO_CALIBRATION"


# --- L4: adversarial — legacy behavior is unreachable -------------------------

def test_legacy_calibration_minting_unreachable():
    with pytest.raises(ImportError):
        from src.evaluation.engine import (  # noqa: F401
            calibration_model_version,
        )
    refused = refuse_calibration_transition(
        "REVENUE", "12M", "V1.0", "CALIBRATION_CANDIDATE", "STAGE6_V1"
    )
    assert refused.state == "NO_CALIBRATION"
    assert derive_calibrated_version_name("V1.0", refused) is None
    default = CalibrationAssessment(
        metric_code="REVENUE",
        horizon="12M",
        model_version="V1.0",
        parameters_version="STAGE6_V1",
    )
    assert derive_calibrated_version_name("V1.0", default) is None
