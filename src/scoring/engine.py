from typing import Dict, List, Optional, Sequence, Tuple
from datetime import datetime
from statistics import median

from src.kpi.schema import KPIResult
from src.scoring.schema import KPIScoreResult, CategoryScoreResult, FundamentalScoreResult


class FundamentalScoringEngine:
    """Stage 3 contract-aligned Fundamental Scoring Engine."""

    AXIS_WEIGHTS = {"GROWTH": 0.30, "PROFITABILITY": 0.45, "RISK_QUALITY": 0.25}
    MIN_PEER_COUNT = 8
    MIN_AXIS_COVERAGE = 0.60

    KPI_PROFILES: Dict[str, Tuple[str, str, float]] = {
        "REVENUE_GROWTH": ("GROWTH", "HIGHER_IS_BETTER", 0.15),
        "OP_PROFIT_GROWTH": ("GROWTH", "HIGHER_IS_BETTER", 0.25),
        "NET_PROFIT_GROWTH": ("GROWTH", "HIGHER_IS_BETTER", 0.30),
        "EPS_GROWTH": ("GROWTH", "HIGHER_IS_BETTER", 0.30),
        "GROSS_MARGIN": ("PROFITABILITY", "HIGHER_IS_BETTER", 0.10),
        "OPERATING_MARGIN": ("PROFITABILITY", "HIGHER_IS_BETTER", 0.25),
        "NET_MARGIN": ("PROFITABILITY", "HIGHER_IS_BETTER", 0.20),
        "ROA": ("PROFITABILITY", "HIGHER_IS_BETTER", 0.20),
        "ROE": ("PROFITABILITY", "HIGHER_IS_BETTER", 0.25),
        "CASH_CONVERSION": ("RISK_QUALITY", "HIGHER_IS_BETTER", 0.40),
        "EARNINGS_QUALITY": ("RISK_QUALITY", "HIGHER_IS_BETTER", 0.60),
        "BANK_LOAN_GROWTH": ("GROWTH", "HIGHER_IS_BETTER", 0.0),
        "BANK_DEPOSIT_GROWTH": ("GROWTH", "HIGHER_IS_BETTER", 0.0),
        "BANK_NII": ("PROFITABILITY", "HIGHER_IS_BETTER", 0.0),
        "BANK_NIM": ("PROFITABILITY", "HIGHER_IS_BETTER", 0.0),
        "BANK_NPL": ("RISK_QUALITY", "LOWER_IS_BETTER", 0.0),
        "HOLDING_NAV": ("PROFITABILITY", "HIGHER_IS_BETTER", 0.0),
        "HOLDING_NAV_GROWTH": ("GROWTH", "HIGHER_IS_BETTER", 0.0),
        "HOLDING_P_NAV": ("EXCLUDED", "HIGHER_IS_BETTER", 0.0),
    }

    @staticmethod
    def _percentile_score(value: float, peers: Sequence[float], direction: str) -> Optional[float]:
        vals = [float(v) for v in peers if v is not None]
        if value is None or not vals:
            return None
        ordered = sorted(vals)
        if len(ordered) == 1:
            percentile = 50.0
        else:
            less = sum(v < value for v in ordered)
            equal = sum(v == value for v in ordered)
            percentile = ((less + 0.5 * equal) / (len(ordered) - 1)) * 100.0
        if direction == "LOWER_IS_BETTER":
            percentile = 100.0 - percentile
        return max(0.0, min(100.0, percentile))

    @staticmethod
    def _historical_score(value: float, history: Sequence[float], direction: str) -> Optional[float]:
        vals = [float(v) for v in history if v is not None]
        if value is None or not vals:
            return None
        benchmark = median(vals)
        if benchmark == value:
            return 50.0
        if benchmark == 0:
            better = value > 0 if direction == "HIGHER_IS_BETTER" else value < 0
            return 100.0 if better else 0.0
        if direction == "HIGHER_IS_BETTER":
            raw = 50.0 + 50.0 * ((value - benchmark) / abs(benchmark))
        elif direction == "LOWER_IS_BETTER":
            raw = 50.0 + 50.0 * ((benchmark - value) / abs(benchmark))
        else:
            raw = 50.0
        return max(0.0, min(100.0, raw))

    def _score_kpi(self, result: KPIResult, peers: Optional[Sequence[float]], history: Optional[Sequence[float]]) -> Tuple[Optional[float], str]:
        profile = self.KPI_PROFILES.get(result.kpi_code)
        if profile is None or profile[0] == "EXCLUDED":
            return None, "EXCLUDED"
        if result.value is None or result.quality_status in {"MISSING", "UNMAPPED", "SUSPICIOUS"}:
            return None, result.quality_status
        axis, direction, _ = profile
        peer_values = list(peers or [])
        if len(peer_values) >= self.MIN_PEER_COUNT:
            return self._percentile_score(result.value, peer_values, direction), "INDUSTRY_PERCENTILE"
        score = self._historical_score(result.value, list(history or []), direction)
        if score is not None:
            return score, "HISTORICAL_FALLBACK"
        return None, "INSUFFICIENT_DATA"

    def calculate_score(self, company_id: int, period_id: int, industry_code: str, kpi_results: List[KPIResult], peer_values: Optional[Dict[str, Sequence[float]]] = None, historical_values: Optional[Dict[str, Sequence[float]]] = None) -> FundamentalScoreResult:
        peer_values = peer_values or {}
        historical_values = historical_values or {}
        kpi_scores: List[KPIScoreResult] = []
        axis_items: Dict[str, List[Tuple[KPIScoreResult, float]]] = {axis: [] for axis in self.AXIS_WEIGHTS}

        for kpi in kpi_results:
            profile = self.KPI_PROFILES.get(kpi.kpi_code)
            if profile is None or profile[0] == "EXCLUDED":
                continue
            axis, direction, base_weight = profile
            score, benchmark_method = self._score_kpi(kpi, peer_values.get(kpi.kpi_code), historical_values.get(kpi.kpi_code))
            item = KPIScoreResult(
                kpi_code=kpi.kpi_code,
                raw_value=kpi.value,
                score=score,
                weight=base_weight,
                effective_weight=0.0,
                quality_status=kpi.quality_status,
                benchmark_method=benchmark_method,
                direction=direction,
                axis=axis,
            )
            if score is not None and base_weight > 0:
                axis_items[axis].append((item, base_weight))
            kpi_scores.append(item)

        category_scores: Dict[str, CategoryScoreResult] = {}
        axis_scores: Dict[str, float] = {}
        axis_coverages: Dict[str, float] = {}
        for axis, axis_weight in self.AXIS_WEIGHTS.items():
            items = axis_items[axis]
            full_weight = sum(profile[2] for profile in self.KPI_PROFILES.values() if profile[0] == axis and profile[2] > 0)
            available_weight = sum(weight for _item, weight in items)
            coverage = available_weight / full_weight if full_weight else 0.0
            axis_coverages[axis] = coverage
            if coverage < self.MIN_AXIS_COVERAGE:
                category_scores[axis] = CategoryScoreResult(axis, None, axis_weight, coverage)
                continue
            for item, weight in items:
                item.effective_weight = weight / available_weight
            axis_score = sum(item.score * item.effective_weight for item, _weight in items if item.score is not None)
            axis_scores[axis] = axis_score
            category_scores[axis] = CategoryScoreResult(axis, axis_score, axis_weight, coverage)

        if not axis_scores:
            overall_score = None
        else:
            available_axis_weight = sum(self.AXIS_WEIGHTS[axis] for axis in axis_scores)
            overall_score = sum(self.AXIS_WEIGHTS[axis] * axis_scores[axis] for axis in axis_scores) / available_axis_weight
            overall_score = max(0.0, min(100.0, overall_score))

        quality_values = [k.quality_status for k in kpi_scores if k.score is not None]
        score_quality = "VALID" if quality_values and all(v == "VALID" for v in quality_values) else ("INSUFFICIENT_DATA" if not axis_scores else "LIMITED")
        return FundamentalScoreResult(
            company_id=company_id,
            period_id=period_id,
            overall_score=round(overall_score, 2) if overall_score is not None else None,
            category_scores=category_scores,
            kpi_scores=kpi_scores,
            calculation_timestamp=datetime.utcnow(),
            score_data_quality=score_quality,
            scoring_method_version="STAGE3_V1",
        )
