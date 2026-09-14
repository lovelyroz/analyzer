from typing import List, Optional
from datetime import datetime
from src.evaluation.schema import ForecastEvaluationResult, ReliabilityAssessment
from src.evaluation.metrics import calculate_pe, calculate_mape, detect_persistent_bias

class ForecastEvaluationEngine:

    def evaluate_forecasts(
        self,
        company_id: int,
        metric_code: str,
        evaluations: List[ForecastEvaluationResult],
        baseline_mape: Optional[float] = None
    ) -> ReliabilityAssessment:
        
        if not evaluations:
            return ReliabilityAssessment(
                company_id=company_id,
                metric_code=metric_code,
                mape=0.0,
                persistent_bias="NEUTRAL",
                reliability_score=50.0,
                calibration_state="NO_CALIBRATION",
                underperforms_baseline=False,
                calculation_timestamp=datetime.utcnow()
            )

        pe_list = [e.percentage_error for e in evaluations]
        mape = calculate_mape(pe_list)
        bias = detect_persistent_bias(pe_list)

        # محاسبه امتیاز Reliability (۱۰۰ - MAPE) با کف ۱۰ و سقف ۱۰۰
        reliability = max(10.0, min(100.0, 100.0 - mape))

        # ارزیابی وضعیت کالیبراسیون (Calibration State)
        if len(evaluations) >= 4 and bias != "NEUTRAL":
            calibration_state = "CALIBRATION_CANDIDATE"
        else:
            calibration_state = "NO_CALIBRATION"

        # بررسی عملکرد نسبت به Baseline ساده
        underperforms = False
        if baseline_mape is not None and mape > baseline_mape:
            underperforms = True

        return ReliabilityAssessment(
            company_id=company_id,
            metric_code=metric_code,
            mape=round(mape, 2),
            persistent_bias=bias,
            reliability_score=round(reliability, 2),
            calibration_state=calibration_state,
            underperforms_baseline=underperforms,
            calculation_timestamp=datetime.utcnow()
        )