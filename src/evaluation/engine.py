from __future__ import annotations

from dataclasses import replace
from datetime import datetime
from typing import Iterable, List, Optional, Sequence, Tuple

from src.evaluation.metrics import (
    accuracy_score_from_mape,
    baseline_advantage_score,
    bias_score,
    calculate_ape,
    calculate_bias,
    calculate_error,
    calculate_mape,
    calculate_percentage_error,
    calculate_relative_improvement,
    confidence_multiplier,
    detect_persistent_bias,
    is_underperforming_baseline,
    observation_confidence,
)
from src.evaluation.schema import ForecastEvaluationResult, ReliabilityAssessment


class ForecastEvaluationEngine:
    """Stage 6 evaluator. It evaluates forecasts; it never creates forecasts."""

    def build_evaluation(
        self,
        *,
        company_id: int,
        period_id: int,
        metric_code: str,
        forecast_value: float,
        actual_value: float,
        horizon: str,
        model_version: str,
        forecast_cutoff_datetime: datetime,
        actual_publication_datetime: Optional[datetime] = None,
        actual_report_version_id: Optional[int] = None,
        baseline_value: Optional[float] = None,
        point_in_time_valid: bool = True,
    ) -> ForecastEvaluationResult:
        """Create one PIT-safe evaluation observation."""
        if actual_publication_datetime is not None and actual_publication_datetime < forecast_cutoff_datetime:
            # An actual published before the cutoff is not a later realized outcome.
            point_in_time_valid = False

        regime = None
        if forecast_value == 0:
            regime = "ZERO_BASE"
        elif forecast_value < 0 < actual_value:
            regime = "LOSS_TO_PROFIT"
        elif forecast_value > 0 > actual_value:
            regime = "PROFIT_TO_LOSS"
        elif forecast_value * actual_value < 0:
            regime = "SIGN_CHANGE"

        percentage_error = None if regime else calculate_percentage_error(forecast_value, actual_value)
        ape = None if regime else calculate_ape(forecast_value, actual_value)

        baseline_error = None
        baseline_pe = None
        baseline_ape = None
        if baseline_value is not None and not regime:
            baseline_error = calculate_error(baseline_value, actual_value)
            baseline_pe = calculate_percentage_error(baseline_value, actual_value)
            baseline_ape = calculate_ape(baseline_value, actual_value)

        return ForecastEvaluationResult(
            company_id=company_id,
            period_id=period_id,
            metric_code=metric_code,
            forecast_value=forecast_value,
            actual_value=actual_value,
            error_amount=calculate_error(forecast_value, actual_value),
            percentage_error=percentage_error,
            absolute_percentage_error=ape,
            horizon=horizon,
            model_version=model_version,
            forecast_cutoff_datetime=forecast_cutoff_datetime,
            actual_publication_datetime=actual_publication_datetime,
            regime_status=regime,
            actual_report_version_id=actual_report_version_id,
            point_in_time_valid=point_in_time_valid,
            baseline_value=baseline_value,
            baseline_error_amount=baseline_error,
            baseline_percentage_error=baseline_pe,
            baseline_absolute_percentage_error=baseline_ape,
        )

    @staticmethod
    def select_point_in_time_actual(
        actual_candidates: Sequence[Tuple[datetime, int, float]],
        forecast_cutoff_datetime: datetime,
    ) -> Optional[Tuple[datetime, int, float]]:
        """Select the latest valid published actual at/after the forecast cutoff.

        Candidate tuples are (publication_datetime, report_version_id, value).
        Selection is deliberately based on explicit publication timestamps rather
        than on whichever record happens to be latest in the database.
        """
        valid = [item for item in actual_candidates if item[0] > forecast_cutoff_datetime]
        if not valid:
            return None
        return max(valid, key=lambda item: item[0])

    @staticmethod
    def seasonal_naive_forecast(history: Sequence[float], seasonal_lag: int) -> Optional[float]:
        """Return the last value from the same seasonal position available at cutoff."""
        if seasonal_lag <= 0 or len(history) < seasonal_lag:
            return None
        return history[-seasonal_lag]

    @staticmethod
    def _deduplicate(evaluations: Iterable[ForecastEvaluationResult]) -> List[ForecastEvaluationResult]:
        unique = {}
        for evaluation in evaluations:
            key = (
                evaluation.company_id,
                evaluation.metric_code,
                evaluation.period_id,
                evaluation.horizon,
                evaluation.model_version,
                evaluation.forecast_cutoff_datetime,
            )
            if key not in unique:
                unique[key] = evaluation
        return list(unique.values())

    def evaluate_forecasts(
        self,
        company_id: int,
        metric_code: str,
        evaluations: List[ForecastEvaluationResult],
        baseline_mape: Optional[float] = None,
        *,
        horizon: Optional[str] = None,
        model_version: Optional[str] = None,
        parameter_version: str = "STAGE6_V1",
        accuracy_poor_mape: float = 50.0,
        bias_unacceptable: float = 25.0,
        baseline_full_advantage: float = 0.50,
    ) -> ReliabilityAssessment:
        """Aggregate one Company + Metric + Horizon + Model Version evaluation set."""
        filtered = [
            item for item in evaluations
            if item.company_id == company_id
            and item.metric_code == metric_code
            and item.point_in_time_valid
            and (horizon is None or item.horizon == horizon)
            and (model_version is None or item.model_version == model_version)
        ]
        filtered = self._deduplicate(filtered)

        resolved_horizon = horizon or (filtered[0].horizon if filtered else "12M")
        resolved_version = model_version or (filtered[0].model_version if filtered else "UNKNOWN")
        count = len(filtered)
        confidence = observation_confidence(count)

        percentage_errors = [item.percentage_error for item in filtered]
        apes = [item.absolute_percentage_error for item in filtered]
        mape = calculate_mape(apes)
        bias = calculate_bias(percentage_errors)
        persistent_bias = detect_persistent_bias(percentage_errors)

        baseline_apes = [item.baseline_absolute_percentage_error for item in filtered]
        computed_baseline_mape = calculate_mape(baseline_apes)
        if baseline_mape is None:
            baseline_mape = computed_baseline_mape

        improvement = calculate_relative_improvement(baseline_mape, mape)
        underperforms = is_underperforming_baseline(mape, baseline_mape, persistent=(count >= 5))

        accuracy = accuracy_score_from_mape(mape, poor_mape=accuracy_poor_mape)
        bias_component = bias_score(bias, unacceptable_bias=bias_unacceptable)
        advantage_component = baseline_advantage_score(improvement, full_advantage=baseline_full_advantage)
        performance = 0.50 * accuracy + 0.20 * bias_component + 0.30 * advantage_component
        reliability = max(0.0, min(100.0, performance * confidence_multiplier(confidence)))

        calibration_state = "NO_CALIBRATION"
        calibration_reason = None
        if persistent_bias != "NEUTRAL":
            calibration_state = "CALIBRATION_CANDIDATE"
            calibration_reason = "PERSISTENT_SYSTEMATIC_BIAS"

        if underperforms:
            calibration_reason = (calibration_reason + ";" if calibration_reason else "") + "MODEL_UNDERPERFORMS_BASELINE"

        return ReliabilityAssessment(
            company_id=company_id,
            metric_code=metric_code,
            horizon=resolved_horizon,
            model_version=resolved_version,
            observation_count=count,
            confidence_level=confidence,
            mape=None if mape is None else round(mape, 4),
            bias=None if bias is None else round(bias, 4),
            persistent_bias=persistent_bias,
            baseline_mape=None if baseline_mape is None else round(baseline_mape, 4),
            relative_improvement=None if improvement is None else round(improvement, 6),
            model_underperforms_baseline=underperforms,
            accuracy_score=round(accuracy, 4),
            bias_score=round(bias_component, 4),
            baseline_advantage_score=round(advantage_component, 4),
            performance_score=round(performance, 4),
            reliability_score=round(reliability, 4),
            calibration_state=calibration_state,
            calibration_reason=calibration_reason,
            model_parameters_version=parameter_version,
        )

    @staticmethod
    def calibration_model_version(
        current_model_version: str,
        calibration_state: str,
        holdout_passed: bool,
    ) -> Optional[str]:
        """Create a new version only after candidate evidence and holdout success."""
        if calibration_state != "CALIBRATION_CANDIDATE" or not holdout_passed:
            return None
        return f"{current_model_version}.CAL1"
