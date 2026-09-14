from typing import List, Optional
from datetime import datetime
from src.scoring.schema import FundamentalScoreResult
from src.valuation.schema import ValuationResult
from src.market.schema import MarketSignalResult
from src.decision.schema import FinalDecisionResult
from src.decision.rules import map_score_to_recommendation

class DecisionEngine:

    def make_decision(
        self,
        company_id: int,
        period_id: int,
        fundamental_result: FundamentalScoreResult,
        valuation_result: ValuationResult,
        market_result: MarketSignalResult,
        forecast_reliability_score: float = 80.0
    ) -> FinalDecisionResult:
        
        pros: List[str] = []
        cons: List[str] = []

        # ۱. استخراج امتیازات کلیدی
        fund_score = fundamental_result.overall_score or 50.0
        val_status = valuation_result.valuation_status
        mos = valuation_result.margin_of_safety_pct
        tech_score = market_result.technical_score

        # ۲. محاسبه امتیاز تلفیقی وزنی (۵۰٪ بنیادی، ۳۰٪ ارزش‌گذاری، ۲۰٪ تکنیکال)
        val_score_contrib = 50.0
        if val_status == "UNDERVALUED":
            val_score_contrib = 85.0
            pros.append(f"حاشیه امنیت مثبت و ارزشمندی سهم (MoS: {mos}%)")
        elif val_status == "OVERVALUED":
            val_score_contrib = 15.0
            cons.append(f"قیمت فراتر از ارزش ذاتی (MoS: {mos}%)")
        else:
            pros.append("قیمت در محدوده منصفانه (Fairly Valued)")

        if fund_score >= 70.0:
            pros.append(f"امتیاز بنیادی قوی ({fund_score})")
        elif fund_score <= 40.0:
            cons.append(f"ضعف در شاخص‌های بنیادی ({fund_score})")

        if market_result.trend_alignment == "BULLISH":
            pros.append("روند تکنیکال صعودی است")
        elif market_result.trend_alignment == "BEARISH":
            cons.append("روند تکنیکال نزولی است")

        if forecast_reliability_score < 60.0:
            cons.append(f"اعتبار پایین پیش‌بینی‌ها (Reliability: {forecast_reliability_score})")

        composite_score = (fund_score * 0.50) + (val_score_contrib * 0.30) + (tech_score * 0.20)
        composite_score = round(composite_score, 2)

        # ۳. صدور سیگنال و تعیین وزن تخصیص
        recommendation, alloc_pct = map_score_to_recommendation(composite_score, mos)

        # تعیین سطح ریسک کلی
        if forecast_reliability_score >= 75 and valuation_result.valuation_risk_level == "LOW":
            risk_level = "LOW"
        elif forecast_reliability_score < 55 or valuation_result.valuation_risk_level == "HIGH":
            risk_level = "HIGH"
        else:
            risk_level = "MEDIUM"

        return FinalDecisionResult(
            company_id=company_id,
            period_id=period_id,
            recommendation=recommendation,
            composite_score=composite_score,
            suggested_allocation_pct=alloc_pct,
            risk_level=risk_level,
            rationale_pros=pros,
            rationale_cons=cons,
            model_version="V1.0",
            calculation_timestamp=datetime.utcnow()
        )