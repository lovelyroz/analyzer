from datetime import datetime
from statistics import median
from typing import Dict, Iterable, List, Optional, Sequence

from src.forecast.schema import CompanyForecastResult
from src.valuation.models import calculate_forward_pe, calculate_forward_pe_fair_value, calculate_margin_of_safety, median_valid
from src.valuation.parameters import MIN_INDUSTRY_PEERS, MODEL_VERSION, SCENARIO_PE_MULTIPLIER, SCENARIO_WEIGHTS
from src.valuation.schema import ScenarioValuation, ValuationResult


class ValuationEngine:
    """Stage 7 V1: Forward P/E valuation, benchmark hierarchy and scenario valuation."""

    def calculate_valuation(
        self,
        company_id: int,
        period_id: int,
        industry_code: str,
        current_price: float,
        forecast_result: CompanyForecastResult,
        forecast_reliability_score: Optional[float] = None,
        nav_per_share: Optional[float] = None,  # retained for caller compatibility; not used as primary V1 axis
        *,
        valuation_date: Optional[datetime] = None,
        market_price_date: Optional[datetime] = None,
        data_cutoff_datetime: Optional[datetime] = None,
        historical_pe_values: Optional[Sequence[Optional[float]]] = None,
        industry_forward_pe_values: Optional[Sequence[Optional[float]]] = None,
        industry_ttm_pe_values: Optional[Sequence[Optional[float]]] = None,
        probability_adjustments: Optional[Dict[str, float]] = None,
        probability_confidence: float = 50.0,
        data_quality_score: float = 100.0,
    ) -> ValuationResult:
        scenarios_input = {
            "bear": forecast_result.scenario_forecasts.bear,
            "base": forecast_result.scenario_forecasts.base,
            "bull": forecast_result.scenario_forecasts.bull,
        }

        historical_median = median_valid(historical_pe_values or [])
        industry_forward_median = median_valid(industry_forward_pe_values or [])
        industry_ttm_median = median_valid(industry_ttm_pe_values or [])

        target_pe_base, target_source = self._select_target_pe(
            industry_forward_median,
            historical_median,
            industry_ttm_median,
            len([x for x in (industry_forward_pe_values or []) if x is not None and x > 0]),
        )

        probabilities = self._resolve_probabilities(probability_adjustments)
        scenarios: Dict[str, ScenarioValuation] = {}
        flags: List[str] = []

        for name, chain in scenarios_input.items():
            eps = chain.eps
            scenario_flags = self._eps_flags(eps, forecast_result, name)
            target_pe = None if target_pe_base is None else target_pe_base * SCENARIO_PE_MULTIPLIER[name]
            forward_pe = calculate_forward_pe(eps, current_price)
            fair_value = calculate_forward_pe_fair_value(eps, target_pe)
            upside = calculate_margin_of_safety(fair_value, current_price)
            scenarios[name] = ScenarioValuation(
                scenario_name=name,
                target_pe=None if target_pe is None else round(target_pe, 4),
                eps_forecast=eps,
                forward_pe=None if forward_pe is None else round(forward_pe, 4),
                fair_value=fair_value,
                upside_downside_pct=upside,
                probability=probabilities[name],
                flags=scenario_flags,
            )
            flags.extend(scenario_flags)

        expected_fv = self._expected_fair_value(scenarios)
        expected_upside = calculate_margin_of_safety(expected_fv, current_price)
        base_upside = scenarios["base"].upside_downside_pct
        scenario_dispersion = self._scenario_dispersion(scenarios)

        if target_pe_base is None or expected_fv is None or base_upside is None:
            status = "INSUFFICIENT_DATA"
        else:
            status = self._valuation_status(expected_upside, base_upside)

        reliability = forecast_reliability_score
        if reliability is not None and reliability < 40:
            flags.append("LOW_FORECAST_RELIABILITY")
        if len([x for x in (industry_forward_pe_values or []) if x is not None and x > 0]) < MIN_INDUSTRY_PEERS and industry_forward_pe_values:
            flags.append("INSUFFICIENT_PEER_DATA")
        if scenario_dispersion is not None and scenario_dispersion > 0.50:
            flags.append("HIGH_SCENARIO_DISPERSION")
        if target_source == "INSUFFICIENT_DATA":
            flags.append("INDUSTRY_BENCHMARK_INSUFFICIENT")

        confidence = self._valuation_confidence(
            forecast_reliability_score=reliability,
            probability_confidence=probability_confidence,
            data_quality_score=data_quality_score,
            benchmark_available=target_pe_base is not None,
            scenario_dispersion=scenario_dispersion,
        )
        risk = self._valuation_risk(scenarios, confidence, flags, scenario_dispersion)
        confidence_label = self._confidence_label(confidence)

        if any(flag in flags for flag in ("NEGATIVE_EPS", "ZERO_EPS", "SIGN_CHANGE")):
            if expected_fv is None:
                status = "NOT_APPLICABLE"

        return ValuationResult(
            company_id=company_id,
            period_id=period_id,
            current_price=current_price,
            expected_fair_value=expected_fv,
            margin_of_safety_pct=expected_upside,
            valuation_status=status,
            valuation_confidence=round(confidence, 4),
            valuation_risk_level=risk,
            scenarios=scenarios,
            model_version=MODEL_VERSION,
            calculation_timestamp=datetime.utcnow(),
            valuation_date=valuation_date,
            market_price_date=market_price_date,
            data_cutoff_datetime=data_cutoff_datetime or forecast_result.data_cutoff_datetime,
            target_pe_source=target_source,
            historical_median_pe=historical_median,
            industry_forward_pe_median=industry_forward_median,
            industry_ttm_pe_median=industry_ttm_median,
            forecast_reliability_score=reliability,
            probability_confidence=probability_confidence,
            valuation_confidence_label=confidence_label,
            valuation_risk_flags=sorted(set(flags)),
            alerts=self._alerts(scenarios, target_source, reliability, scenario_dispersion),
            metadata={
                "expected_upside": expected_upside,
                "scenario_dispersion": scenario_dispersion,
                "benchmark_peer_minimum": MIN_INDUSTRY_PEERS,
                "scenario_probability_sum": sum(probabilities.values()),
                "probability_adjustments_applied": probability_adjustments or {},
            },
        )

    @staticmethod
    def _select_target_pe(
        industry_forward: Optional[float],
        historical: Optional[float],
        industry_ttm: Optional[float],
        forward_peer_count: int,
    ) -> tuple[Optional[float], str]:
        if industry_forward is not None and forward_peer_count >= MIN_INDUSTRY_PEERS:
            return industry_forward, "INDUSTRY_FORWARD_PE"
        if historical is not None:
            return historical, "HISTORICAL_MEDIAN_PE"
        if industry_ttm is not None and forward_peer_count < MIN_INDUSTRY_PEERS:
            return industry_ttm, "INDUSTRY_TTM_PE"
        return None, "INSUFFICIENT_DATA"

    @staticmethod
    def _resolve_probabilities(adjustments: Optional[Dict[str, float]]) -> Dict[str, float]:
        values = dict(SCENARIO_WEIGHTS)
        if adjustments:
            for name in values:
                values[name] += adjustments.get(name, 0.0)
        values = {name: max(0.0, value) for name, value in values.items()}
        total = sum(values.values())
        if total <= 0:
            return dict(SCENARIO_WEIGHTS)
        return {name: value / total for name, value in values.items()}

    @staticmethod
    def _eps_flags(eps: Optional[float], forecast_result: CompanyForecastResult, scenario: str) -> List[str]:
        if eps is None:
            return ["NOT_APPLICABLE"]
        if eps < 0:
            return ["NEGATIVE_EPS", "NOT_APPLICABLE"]
        if eps == 0:
            return ["ZERO_EPS", "NOT_APPLICABLE"]
        return []

    @staticmethod
    def _expected_fair_value(scenarios: Dict[str, ScenarioValuation]) -> Optional[float]:
        valid = [s for s in scenarios.values() if s.fair_value is not None]
        if len(valid) != 3:
            return None
        return round(sum(s.fair_value * s.probability for s in valid), 2)

    @staticmethod
    def _scenario_dispersion(scenarios: Dict[str, ScenarioValuation]) -> Optional[float]:
        values = [s.fair_value for s in scenarios.values() if s.fair_value is not None]
        if len(values) != 3:
            return None
        base = scenarios["base"].fair_value
        if base is None or base <= 0:
            return None
        return (max(values) - min(values)) / base

    @staticmethod
    def _valuation_status(expected_upside: float, base_upside: float) -> str:
        if expected_upside >= 30.0 and base_upside >= 15.0:
            return "VERY_ATTRACTIVE"
        if expected_upside >= 15.0 and base_upside >= 5.0:
            return "ATTRACTIVE"
        if expected_upside <= -25.0 and base_upside <= -10.0:
            return "VERY_EXPENSIVE"
        if expected_upside <= -10.0 and base_upside < 0.0:
            return "EXPENSIVE"
        return "FAIR"

    @staticmethod
    def _valuation_confidence(
        forecast_reliability_score: Optional[float],
        probability_confidence: float,
        data_quality_score: float,
        benchmark_available: bool,
        scenario_dispersion: Optional[float],
    ) -> float:
        reliability = 50.0 if forecast_reliability_score is None else max(0.0, min(100.0, forecast_reliability_score))
        probability = max(0.0, min(100.0, probability_confidence))
        quality = max(0.0, min(100.0, data_quality_score))
        benchmark = 100.0 if benchmark_available else 25.0
        dispersion_penalty = 0.0 if scenario_dispersion is None else min(40.0, scenario_dispersion * 50.0)
        return max(0.0, min(100.0, 0.40 * reliability + 0.20 * probability + 0.20 * quality + 0.20 * benchmark - dispersion_penalty))

    @staticmethod
    def _confidence_label(score: float) -> str:
        if score >= 90:
            return "VERY_HIGH"
        if score >= 75:
            return "HIGH"
        if score >= 60:
            return "MODERATE"
        if score >= 40:
            return "LOW"
        return "VERY_LOW"

    @staticmethod
    def _valuation_risk(
        scenarios: Dict[str, ScenarioValuation],
        confidence: float,
        flags: List[str],
        dispersion: Optional[float],
    ) -> str:
        if confidence < 40 or "NEGATIVE_EPS" in flags or "SIGN_CHANGE" in flags:
            return "EXTREME"
        bear = scenarios["bear"].upside_downside_pct
        if dispersion is not None and dispersion > 0.50:
            return "HIGH"
        if bear is not None and bear < -30:
            return "HIGH"
        if confidence < 60 or (bear is not None and bear < -15):
            return "MEDIUM"
        return "LOW"

    @staticmethod
    def _alerts(
        scenarios: Dict[str, ScenarioValuation],
        target_source: str,
        reliability: Optional[float],
        dispersion: Optional[float],
    ) -> List[str]:
        alerts: List[str] = []
        if dispersion is not None and dispersion > 0.50:
            alerts.append("HIGH_SCENARIO_DISPERSION")
        if reliability is not None and reliability < 40:
            alerts.append("LOW_FORECAST_RELIABILITY")
        if target_source == "INSUFFICIENT_DATA":
            alerts.append("INSUFFICIENT_PEER_DATA")
        if scenarios["base"].target_pe is not None and scenarios["base"].forward_pe is not None:
            if scenarios["base"].forward_pe > scenarios["base"].target_pe * 1.5:
                alerts.append("VALUATION_BENCHMARK_DIVERGENCE")
        return sorted(set(alerts))
