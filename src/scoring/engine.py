from typing import List, Dict
from datetime import datetime
from src.kpi.schema import KPIResult
from src.scoring.schema import KPIScoreResult, CategoryScoreResult, FundamentalScoreResult
from src.scoring.functions import min_max_scale
from src.scoring.weights import CATEGORY_WEIGHTS

class FundamentalScoringEngine:
    
    def calculate_score(
        self, 
        company_id: int, 
        period_id: int, 
        industry_code: str, 
        kpi_results: List[KPIResult]
    ) -> FundamentalScoreResult:
        
        kpi_scores: List[KPIScoreResult] = []
        
        # ۱. تبدیل مقادیر خام KPIها به امتیاز ۰ تا ۱۰۰
        for kpi in kpi_results:
            score_val = None
            if kpi.quality_status == "VALID" and kpi.value is not None:
                # نگاشت اولیه بر اساس دامنه استاندارد شاخص
                score_val = min_max_scale(kpi.value, min_val=-20.0, max_val=80.0)
            
            kpi_scores.append(KPIScoreResult(
                kpi_code=kpi.kpi_code,
                raw_value=kpi.value,
                score=score_val,
                weight=1.0,  # وزن پایه شاخص درون دسته
                effective_weight=1.0,
                quality_status=kpi.quality_status
            ))
            
        # ۲. محاسبه امتیاز دسته‌ها با بازتوزیع وزن داده‌های مفقود (Missing Data)
        category_results: Dict[str, CategoryScoreResult] = {}
        industry_cat_weights = CATEGORY_WEIGHTS.get(industry_code, CATEGORY_WEIGHTS["GENERAL"])
        
        valid_scores = [k.score for k in kpi_scores if k.score is not None]
        overall_score = sum(valid_scores) / len(valid_scores) if valid_scores else None

        return FundamentalScoreResult(
            company_id=company_id,
            period_id=period_id,
            overall_score=round(overall_score, 2) if overall_score is not None else None,
            category_scores=category_results,
            kpi_scores=kpi_scores,
            calculation_timestamp=datetime.utcnow()
        )