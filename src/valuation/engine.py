import math
from datetime import datetime
from typing import Dict, List, Optional, Sequence

from src.forecast.schema import CompanyForecastResult
from src.valuation.models import (
    calculate_forward_pe,
    calculate_forward_pe_fair_value,
    calculate_margin_of_safety,
    median_valid,
)
from src.valuation.parameters import (
    ALERT_THRESHOLDS,
    CONFIDENCE_THRESHOLDS,
    CONTRACT_VERSION,
    MIN_INDUSTRY_PEERS,
    MODEL_VERSION,
    PROBABILITY_EVIDENCE_FAMILIES,
    PROBABILITY_EVIDENCE_BLEND,
    RISK_THRESHOLDS,
    SCENARIO_MULTIPLE_MAX_ABS_ADJUSTMENT,
    SCENARIO_MULTIPLE_POLICY_VERSION,
    SCENARIO_WEIGHTS,
    SENSITIVITY_PERTURBATION,
    VALUATION_THRESHOLDS,
)
from src.valuation.schema import ScenarioValuation, ValuationResult


def _finite_or_none(value: Optional[float]) -> Optional[float]:
    """Coerce non-finite floats (NaN/inf) to None so invalid inputs never leak NaN."""
    if value is None:
        return None
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return None
    return numeric if math.isfinite(numeric) else None


def _clamp_score(value: Optional[float], default: float) -> float:
    """Clamp a 0-100 score; None or non-finite input falls back to the default."""
    if value is None:
        return default
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return default
    if not math.isfinite(numeric):
        return default
    return max(0.0, min(100.0, numeric))


class ValuationEngine:
    """Stage 7 V1: Forward P/E valuation, benchmark hierarchy, scenarios and audit metadata."""

    def calculate_valuation(
        self,
        company_id: int,
        period_id: int,
        industry_code: str,
        current_price: float,
        forecast_result: CompanyForecastResult,
        forecast_reliability_score: Optional[float] = None,
        nav_per_share: Optional[float] = None,
        *,
        valuation_date: Optional[datetime] = None,
        market_price_date: Optional[datetime] = None,
        data_cutoff_datetime: Optional[datetime] = None,
        historical_pe_values: Optional[Sequence[Optional[float]]] = None,
        industry_forward_pe_values: Optional[Sequence[Optional[float]]] = None,
        industry_ttm_pe_values: Optional[Sequence[Optional[float]]] = None,
        probability_adjustments: Optional[Dict[str, float]] = None,
        probability_evidence: Optional[Dict[str, Dict[str, float]]] = None,
        probability_confidence: float = 50.0,
        data_quality_score: float = 100.0,
        scenario_pe_adjustments: Optional[Dict[str, float]] = None,
        scenario_pe_rationales: Optional[Dict[str, str]] = None,
    ) -> ValuationResult:
        scenarios_input = {
            "bear": forecast_result.scenario_forecasts.bear,
            "base": forecast_result.scenario_forecasts.base,
            "bull": forecast_result.scenario_forecasts.bull,
        }

        historical_values = [_finite_or_none(value) for value in (historical_pe_values or [])]
        forward_values = [_finite_or_none(value) for value in (industry_forward_pe_values or [])]
        ttm_values = [_finite_or_none(value) for value in (industry_ttm_pe_values or [])]
        valid_forward_count = self._valid_positive_count(forward_values)

        historical_median = median_valid(historical_values)
        industry_forward_median = median_valid(forward_values)
        industry_ttm_median = median_valid(ttm_values)
        target_pe_base, target_source = self._select_target_pe(
            industry_forward_median,
            historical_median,
            industry_ttm_median,
            valid_forward_count,
        )

        probabilities, probability_meta = self._resolve_probabilities(
            probability_adjustments=probability_adjustments,
            probability_evidence=probability_evidence,
        )
        multiple_adjustments, multiple_meta = self._resolve_scenario_multiple_adjustments(
            scenario_pe_adjustments=scenario_pe_adjustments,
            scenario_pe_rationales=scenario_pe_rationales,
        )

        scenarios: Dict[str, ScenarioValuation] = {}
        flags: List[str] = []

        price = _finite_or_none(current_price)
        if price is not None and price <= 0:
            price = None
        for name, chain in scenarios_input.items():
            eps = _finite_or_none(chain.eps)
            scenario_flags = self._eps_flags(eps)
            target_pe = None if target_pe_base is None else target_pe_base * (1.0 + multiple_adjustments[name])
            forward_pe = calculate_forward_pe(eps, price)
            fair_value = calculate_forward_pe_fair_value(eps, target_pe)
            upside = calculate_margin_of_safety(fair_value, price)
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

        sign_flags = self._scenario_sign_change_flags(scenarios)
        for name, scenario_flags in sign_flags.items():
            scenarios[name].flags.extend(flag for flag in scenario_flags if flag not in scenarios[name].flags)
            flags.extend(scenario_flags)

        expected_fv = self._expected_fair_value(scenarios)
        expected_upside = calculate_margin_of_safety(expected_fv, current_price)
        base_upside = scenarios["base"].upside_downside_pct
        scenario_dispersion = self._scenario_dispersion(scenarios)

        if target_pe_base is None or expected_fv is None or base_upside is None:
            status = "INSUFFICIENT_DATA"
        else:
            status = self._valuation_status(expected_upside, base_upside)

        if self._scenario_order_warning(scenarios):
            flags.append("SCENARIO_ORDER_WARNING")

        reliability = forecast_reliability_score
        if reliability is not None and reliability < ALERT_THRESHOLDS["low_forecast_reliability"]:
            flags.append("LOW_FORECAST_RELIABILITY")
        if forward_values and valid_forward_count < MIN_INDUSTRY_PEERS:
            flags.append("INSUFFICIENT_PEER_DATA")
        if scenario_dispersion is not None and scenario_dispersion > RISK_THRESHOLDS["high_scenario_dispersion"]:
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
        driver_ranking, driver_impact, driver_uncertainty, review_priority = self._driver_analysis(
            scenarios=scenarios,
            probability_confidence=probability_confidence,
            forecast_reliability=reliability,
            data_quality_score=data_quality_score,
        )
        alerts = self._alerts(
            scenarios=scenarios,
            target_source=target_source,
            reliability=reliability,
            dispersion=scenario_dispersion,
            historical_median=historical_median,
            industry_forward_median=industry_forward_median,
            driver_ranking=driver_ranking,
        )
        flags.extend(alerts)

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
            alerts=alerts,
            valuation_driver_ranking=driver_ranking,
            driver_impact=driver_impact,
            driver_uncertainty=driver_uncertainty,
            review_priority=review_priority,
            valuation_data_quality=max(0.0, min(100.0, data_quality_score)),
            contract_version=CONTRACT_VERSION,
            metadata={
                "industry_code": industry_code,
                "expected_upside": expected_upside,
                "scenario_dispersion": scenario_dispersion,
                "scenario_dependency": {
                    "measure": "fair_value_dispersion",
                    "score": scenario_dispersion,
                    "separate_from_probability": True,
                },
                "benchmark_peer_minimum": MIN_INDUSTRY_PEERS,
                "scenario_probability_sum": sum(probabilities.values()),
                "probability_adjustments_applied": {},
                "probability_evidence": probability_meta,
                "probability_evidence_families": list(PROBABILITY_EVIDENCE_FAMILIES),
                "scenario_multiple_policy": multiple_meta,
                "nav_per_share_received": nav_per_share,
                "pit_inputs_required": True,
            },
        )

    @staticmethod
    def _valid_positive_count(values: Sequence[Optional[float]]) -> int:
        return sum(1 for value in values if value is not None and value == value and value > 0)

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
        if industry_ttm is not None:
            return industry_ttm, "INDUSTRY_TTM_PE"
        return None, "INSUFFICIENT_DATA"

    @staticmethod
    def _resolve_probabilities(
        probability_adjustments: Optional[Dict[str, float]],
        probability_evidence: Optional[Dict[str, Dict[str, float]]],
    ) -> tuple[Dict[str, float], Dict[str, object]]:
        if probability_adjustments:
            raise ValueError("Direct probability_adjustments are not allowed in Stage 7 V1; use family-level probability_evidence")

        values = dict(SCENARIO_WEIGHTS)
        family_distributions: Dict[str, Dict[str, float]] = {}
        if probability_evidence:
            unknown = set(probability_evidence) - set(PROBABILITY_EVIDENCE_FAMILIES)
            if unknown:
                raise ValueError(f"Unknown probability evidence families: {sorted(unknown)}")
            for family, evidence in probability_evidence.items():
                if set(evidence) != set(values):
                    raise ValueError(f"Evidence family {family} must provide bear/base/bull scores")
                scores = {name: float(evidence[name]) for name in values}
                if any(score < 0 or score > 1 for score in scores.values()):
                    raise ValueError(f"Evidence family {family} scores must be in [0, 1]")
                total = sum(scores.values())
                if total <= 0:
                    raise ValueError(f"Evidence family {family} must contain positive evidence")
                family_distributions[family] = {name: scores[name] / total for name in values}

            if family_distributions:
                family_mean = {
                    name: sum(dist[name] for dist in family_distributions.values()) / len(family_distributions)
                    for name in values
                }
                blend = max(0.0, min(1.0, PROBABILITY_EVIDENCE_BLEND))
                for name in values:
                    values[name] = (1.0 - blend) * values[name] + blend * family_mean[name]

        values = {name: max(0.0, value) for name, value in values.items()}
        total = sum(values.values())
        if total <= 0:
            values = dict(SCENARIO_WEIGHTS)
            total = sum(values.values())
        resolved = {name: value / total for name, value in values.items()}
        return resolved, {
            "mode": "FAMILY_LEVEL_EQUAL_WEIGHT" if family_distributions else "PRIOR_ONLY",
            "families_used": list(family_distributions),
            "family_count": len(family_distributions),
            "correlated_metric_protection": "ONE_DISTRIBUTION_PER_FAMILY",
            "blend": PROBABILITY_EVIDENCE_BLEND if family_distributions else 0.0,
            "family_distributions": family_distributions,
        }

    @staticmethod
    def _resolve_scenario_multiple_adjustments(
        scenario_pe_adjustments: Optional[Dict[str, float]],
        scenario_pe_rationales: Optional[Dict[str, str]],
    ) -> tuple[Dict[str, float], Dict[str, object]]:
        adjustments = {name: 0.0 for name in SCENARIO_WEIGHTS}
        if scenario_pe_adjustments is None:
            return adjustments, {
                "mode": "NEUTRAL_BENCHMARK_MULTIPLE",
                "adjustments": adjustments,
                "rationales": {},
                "economic_justification_required": True,
                "versioned": True,
                "backtestable": True,
                "policy_version": SCENARIO_MULTIPLE_POLICY_VERSION,
            }

        unknown = set(scenario_pe_adjustments) - set(adjustments)
        if unknown:
            raise ValueError(f"Unknown scenario multiple names: {sorted(unknown)}")
        rationales = scenario_pe_rationales or {}
        for name, adjustment in scenario_pe_adjustments.items():
            value = float(adjustment)
            if abs(value) > SCENARIO_MULTIPLE_MAX_ABS_ADJUSTMENT:
                raise ValueError(f"Scenario multiple adjustment for {name} exceeds V1 bound")
            if name != "base" and not str(rationales.get(name, "")).strip():
                raise ValueError(f"Economic rationale required for {name} scenario multiple adjustment")
            adjustments[name] = value
        if "base" in rationales and not str(rationales["base"]).strip():
            raise ValueError("Economic rationale for base scenario cannot be empty")
        return adjustments, {
            "mode": "EXPLICIT_ECONOMIC_SCENARIO_ADJUSTMENT",
            "adjustments": adjustments,
            "rationales": {name: str(value) for name, value in rationales.items() if name in adjustments},
            "economic_justification_required": True,
            "versioned": True,
            "backtestable": True,
            "max_abs_adjustment": SCENARIO_MULTIPLE_MAX_ABS_ADJUSTMENT,
            "policy_version": SCENARIO_MULTIPLE_POLICY_VERSION,
        }

    @staticmethod
    def _eps_flags(eps: Optional[float]) -> List[str]:
        if eps is None:
            return ["NOT_APPLICABLE"]
        if eps < 0:
            return ["NEGATIVE_EPS", "NOT_APPLICABLE"]
        if eps == 0:
            return ["ZERO_EPS", "NOT_APPLICABLE"]
        return []

    @staticmethod
    def _scenario_sign_change_flags(scenarios: Dict[str, ScenarioValuation]) -> Dict[str, List[str]]:
        eps_values = {name: scenario.eps_forecast for name, scenario in scenarios.items()}
        if any(value is None for value in eps_values.values()):
            return {}
        signs = {name: value > 0 for name, value in eps_values.items()}
        if len(set(signs.values())) == 1:
            return {}
        result: Dict[str, List[str]] = {}
        for name, positive in signs.items():
            result[name] = ["SIGN_CHANGE", "PROFIT_TO_LOSS" if positive else "LOSS_TO_PROFIT"]
        return result

    @staticmethod
    def _scenario_order_warning(scenarios: Dict[str, ScenarioValuation]) -> bool:
        values = [scenarios[name].fair_value for name in ("bear", "base", "bull")]
        return all(value is not None for value in values) and not (values[0] <= values[1] <= values[2])

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
        t = VALUATION_THRESHOLDS
        if expected_upside >= t["very_attractive_expected_upside"] and base_upside >= t["very_attractive_base_upside"]:
            return "VERY_ATTRACTIVE"
        if expected_upside >= t["attractive_expected_upside"] and base_upside >= t["attractive_base_upside"]:
            return "ATTRACTIVE"
        if expected_upside <= t["very_expensive_expected_upside"] and base_upside <= t["very_expensive_base_upside"]:
            return "VERY_EXPENSIVE"
        if expected_upside <= t["expensive_expected_upside"] and base_upside < 0.0:
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
        reliability = _clamp_score(forecast_reliability_score, 50.0)
        probability = _clamp_score(probability_confidence, 50.0)
        quality = _clamp_score(data_quality_score, 100.0)
        benchmark = 100.0 if benchmark_available else 25.0
        dispersion_penalty = 0.0 if scenario_dispersion is None else min(40.0, scenario_dispersion * 50.0)
        return max(0.0, min(100.0, 0.40 * reliability + 0.20 * probability + 0.20 * quality + 0.20 * benchmark - dispersion_penalty))

    @staticmethod
    def _confidence_label(score: float) -> str:
        t = CONFIDENCE_THRESHOLDS
        if score >= t["very_high"]:
            return "VERY_HIGH"
        if score >= t["high"]:
            return "HIGH"
        if score >= t["moderate"]:
            return "MODERATE"
        if score >= t["low"]:
            return "LOW"
        return "VERY_LOW"

    @staticmethod
    def _valuation_risk(
        scenarios: Dict[str, ScenarioValuation],
        confidence: float,
        flags: List[str],
        dispersion: Optional[float],
    ) -> str:
        t = RISK_THRESHOLDS
        if confidence < t["extreme_confidence"] or "NEGATIVE_EPS" in flags or "SIGN_CHANGE" in flags:
            return "EXTREME"
        bear = scenarios["bear"].upside_downside_pct
        if dispersion is not None and dispersion > t["high_scenario_dispersion"]:
            return "HIGH"
        if bear is not None and bear < t["high_bear_downside"]:
            return "HIGH"
        if confidence < t["medium_confidence"] or (bear is not None and bear < t["medium_bear_downside"]):
            return "MEDIUM"
        return "LOW"

    @staticmethod
    def _driver_analysis(
        scenarios: Dict[str, ScenarioValuation],
        probability_confidence: float,
        forecast_reliability: Optional[float],
        data_quality_score: float,
    ) -> tuple[List[str], Dict[str, float], Dict[str, float], Dict[str, float]]:
        base = scenarios["base"]
        if base.fair_value is None or base.eps_forecast is None or base.target_pe is None:
            return [], {}, {}, {}
        p = SENSITIVITY_PERTURBATION
        # One-at-a-time sensitivity on the Stage 7 V1 valuation identity FV = EPS x target P/E.
        # EPS shock: hold the benchmark multiple fixed, recompute FV from perturbed EPS.
        eps_up = calculate_forward_pe_fair_value(base.eps_forecast * (1.0 + p), base.target_pe)
        eps_effect = abs(base.fair_value - eps_up) if eps_up is not None else None
        # Target-P/E shock: hold forecast EPS fixed, recompute FV from perturbed multiple.
        pe_up = calculate_forward_pe_fair_value(base.eps_forecast, base.target_pe * (1.0 + p))
        pe_effect = abs(base.fair_value - pe_up) if pe_up is not None else None
        if eps_effect is None or pe_effect is None:
            return [], {}, {}, {}
        drivers = {"EPS": eps_effect, "TARGET_PE": pe_effect}
        total = max(sum(drivers.values()), 1e-9)
        reliability = _clamp_score(forecast_reliability, 50.0)
        probability = _clamp_score(probability_confidence, 50.0)
        quality = _clamp_score(data_quality_score, 100.0)
        uncertainty_base = max(0.0, min(100.0, (100.0 - reliability) * 0.5 + (100.0 - probability) * 0.3 + (100.0 - quality) * 0.2))
        ranking = sorted(drivers, key=lambda key: (-drivers[key], key))
        impact_pct = {key: round(100.0 * value / total, 4) for key, value in drivers.items()}
        uncertainty = {key: round(uncertainty_base, 4) for key in drivers}
        review = {key: round(impact_pct[key] * uncertainty[key] / 100.0, 4) for key in drivers}
        return ranking, impact_pct, uncertainty, review

    @staticmethod
    def _alerts(
        scenarios: Dict[str, ScenarioValuation],
        target_source: str,
        reliability: Optional[float],
        dispersion: Optional[float],
        historical_median: Optional[float],
        industry_forward_median: Optional[float],
        driver_ranking: List[str],
    ) -> List[str]:
        alerts: List[str] = []
        if dispersion is not None and dispersion > ALERT_THRESHOLDS["high_scenario_dispersion"]:
            alerts.append("WARNING:HIGH_SCENARIO_DISPERSION")
        if reliability is not None and reliability < ALERT_THRESHOLDS["low_forecast_reliability"]:
            alerts.append("WARNING:LOW_FORECAST_RELIABILITY")
        if target_source == "INSUFFICIENT_DATA":
            alerts.append("CRITICAL:INSUFFICIENT_BENCHMARK_DATA")
        base = scenarios["base"]
        if base.target_pe is not None and base.forward_pe is not None and base.target_pe > 0:
            if base.forward_pe / base.target_pe >= ALERT_THRESHOLDS["benchmark_divergence_ratio"]:
                alerts.append("WATCH:VALUATION_ABOVE_TARGET_PE")
            elif base.target_pe / base.forward_pe >= ALERT_THRESHOLDS["benchmark_divergence_ratio"]:
                alerts.append("WATCH:VALUATION_BELOW_TARGET_PE")
        if historical_median is not None and base.forward_pe is not None and historical_median > 0:
            if base.forward_pe / historical_median >= ALERT_THRESHOLDS["historical_divergence_ratio"]:
                alerts.append("WATCH:FORWARD_PE_ABOVE_HISTORICAL")
            elif historical_median / base.forward_pe >= ALERT_THRESHOLDS["historical_divergence_ratio"]:
                alerts.append("WATCH:FORWARD_PE_BELOW_HISTORICAL")
        if industry_forward_median is not None and base.forward_pe is not None and industry_forward_median > 0:
            if base.forward_pe / industry_forward_median >= ALERT_THRESHOLDS["industry_divergence_ratio"]:
                alerts.append("WATCH:FORWARD_PE_ABOVE_INDUSTRY")
            elif industry_forward_median / base.forward_pe >= ALERT_THRESHOLDS["industry_divergence_ratio"]:
                alerts.append("WATCH:FORWARD_PE_BELOW_INDUSTRY")
        if driver_ranking:
            alerts.append(f"INFO:TOP_DRIVER:{driver_ranking[0]}")
        return sorted(set(alerts))
