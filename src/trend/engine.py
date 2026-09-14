from typing import List, Dict, Optional
from datetime import datetime
from src.trend.schema import ComparisonResult, TrendResult
from src.trend.utils import calculate_pct_change, is_low_base, is_sign_change

class TrendEngine:

    def evaluate_trend(
        self, 
        company_id: int, 
        period_id: int, 
        metric_code: str,
        val_3m_curr: Optional[float], val_3m_prev: Optional[float],
        val_6m_curr: Optional[float], val_6m_prev: Optional[float],
        val_12m_curr: Optional[float], val_12m_prev: Optional[float]
    ) -> TrendResult:
        
        # ۱. محاسبه درصد تغییرات ۳ بازه زمانی اصلی
        p_3m = calculate_pct_change(val_3m_curr, val_3m_prev)
        p_6m = calculate_pct_change(val_6m_curr, val_6m_prev)
        p_12m = calculate_pct_change(val_12m_curr, val_12m_prev)

        valid_horizons = [p for p in [p_3m, p_6m, p_12m] if p is not None]
        
        # قانون داده کافی (حداقل ۲ بازه معتبر از ۳ بازه نیاز است)
        if len(valid_horizons) < 2:
            return TrendResult(
                company_id=company_id,
                period_id=period_id,
                metric_code=metric_code,
                trend_state="INSUFFICIENT_DATA",
                coverage="INSUFFICIENT",
                low_base_flag=is_low_base(val_3m_prev),
                sign_change_flag=is_sign_change(val_3m_curr, val_3m_prev),
                comparisons={},
                calculation_timestamp=datetime.utcnow()
            )

        coverage = "FULL" if len(valid_horizons) == 3 else "LIMITED"

        # ۲. منطق سناریوهای قفل‌شده معماری
        if p_3m is not None and p_6m is not None and p_12m is not None:
            if p_3m >= 10.0 and p_6m >= 10.0 and p_12m >= 0.0:
                trend_state = "Strong Improvement"
            elif p_3m <= -10.0 and p_6m <= -10.0 and p_12m <= 0.0:
                trend_state = "Strong Deterioration"
            elif all(p > 0 for p in valid_horizons):
                trend_state = "Improving"
            elif all(p < 0 for p in valid_horizons):
                trend_state = "Deteriorating"
            elif all(abs(p) <= 2.0 for p in valid_horizons):
                trend_state = "Stable"
            else:
                trend_state = "Improving" if p_3m > 0 else "Deteriorating"
        else:
            # دو افق معتبر
            if all(p > 0 for p in valid_horizons):
                trend_state = "Improving"
            elif all(p < 0 for p in valid_horizons):
                trend_state = "Deteriorating"
            else:
                trend_state = "Stable"

        comparisons = {
            "3M": ComparisonResult("3M", p_3m, "VALID" if p_3m is not None else "MISSING"),
            "6M": ComparisonResult("6M", p_6m, "VALID" if p_6m is not None else "MISSING"),
            "12M": ComparisonResult("12M", p_12m, "VALID" if p_12m is not None else "MISSING"),
        }

        return TrendResult(
            company_id=company_id,
            period_id=period_id,
            metric_code=metric_code,
            trend_state=trend_state,
            coverage=coverage,
            low_base_flag=is_low_base(val_3m_prev),
            sign_change_flag=is_sign_change(val_3m_curr, val_3m_prev),
            comparisons=comparisons,
            calculation_timestamp=datetime.utcnow()
        )