from typing import Optional, Sequence, Dict, List
from datetime import datetime

from src.trend.schema import (
    ComparisonResult,
    TrendResult,
    HistoricalResult,
    SeasonalResult,
    MomentumResult,
    ContextFlags,
    PeriodComparison,
)
from src.trend.utils import (
    DIRECTION_THRESHOLD,
    calculate_pct_change,
    classify_direction,
    detect_one_off,
    determine_trend_state,
    flow_momentum,
    historical_percentile_abs,
    is_low_base,
    is_zero_base,
    momentum_history,
    multi_year_trend,
    period_comparison,
    relative_strength,
    same_period_multi_year,
    seasonal_baseline,
    seasonal_surprise,
    sign_change_kind,
    stock_momentum,
    trend_12m,
)


class TrendEngine:
    """Stage 4 - Historical, Seasonal & Trend Engine.

    Stage 4 owns the company's own historical data layer. It consumes an
    already point-in-time-restricted observation series for one company and
    one metric, and derives every historical, seasonal and momentum
    comparison from it: MoM / QoQ / YoY, same-period multi-year,
    multi-year trend, the seasonal baseline and surprise, and the
    3M / 6M / 12M momentum horizons that feed the trend state.

    The caller is responsible for the Stage 1 point-in-time selection, i.e.
    for passing only observations published at or before the evaluation
    cutoff. This engine never reaches beyond the supplied series, so no
    future observation can enter a historical or trend calculation.

    Stage 4 produces context and direction only. Fundamental scoring,
    forecasting, valuation and market signals are outside this engine, and
    Stage 4 produces no score of its own.
    """

    def evaluate_trend(
        self,
        company_id: int,
        period_id: int,
        metric_code: str,
        val_3m_curr: Optional[float], val_3m_prev: Optional[float],
        val_6m_curr: Optional[float], val_6m_prev: Optional[float],
        val_12m_curr: Optional[float], val_12m_prev: Optional[float],
        historical_3m: Optional[Sequence[float]] = None,
        historical_6m: Optional[Sequence[float]] = None,
        historical_12m: Optional[Sequence[float]] = None,
        historical_low_base_values: Optional[Sequence[float]] = None,
        *,
        # --- Explicit pre-computed historical comparisons (layer 1) ---
        val_mom: Optional[tuple] = None,
        val_qoq: Optional[tuple] = None,
        val_yoy: Optional[tuple] = None,
        same_period_history: Optional[Sequence[float]] = None,
        annual_history: Optional[Sequence[float]] = None,
        seasonal_history: Optional[Sequence[float]] = None,
        # --- Raw series, flow vs stock treated separately (sections 6-7) ---
        flow_series: Optional[Sequence[Optional[float]]] = None,
        stock_series: Optional[Sequence[Optional[float]]] = None,
        period_months: int = 3,
    ) -> TrendResult:
        """Evaluate the four Stage 4 layers for one company / metric / period.

        `flow_series` / `stock_series` are chronological observation series
        (oldest first) already restricted to information available at the
        evaluation point in time. Exactly one should be supplied; when both
        are given, the flow series wins and the stock series is ignored.
        """
        flow = flow_series if flow_series is not None else stock_series
        is_flow = flow_series is not None

        # ---------------- Layer 3: Momentum / Trend ----------------
        changes: Dict[str, Optional[float]] = {}
        strengths: Dict[str, Optional[str]] = {}
        percentiles: Dict[str, Optional[float]] = {}
        momentum: Dict[str, MomentumResult] = {}

        explicit = {
            "3M": (val_3m_curr, val_3m_prev),
            "6M": (val_6m_curr, val_6m_prev),
            "12M": (val_12m_curr, val_12m_prev),
        }
        explicit_histories = {
            "3M": historical_3m,
            "6M": historical_6m,
            "12M": historical_12m,
        }

        for horizon, months in (("3M", 3), ("6M", 6), ("12M", 12)):
            if flow is not None:
                if horizon == "12M":
                    # The 12M horizon splits by variable class: FLOW 12M is the
                    # TTM-vs-TTM reading (section 6.1), while STOCK 12M is a
                    # plain period-end ratio and must never be aggregated like
                    # a flow (section 7).
                    change = (
                        trend_12m(flow, period_months)
                        if is_flow
                        else stock_momentum(flow, months, period_months)
                    )
                else:
                    change = (
                        flow_momentum(flow, months, period_months)
                        if is_flow
                        else stock_momentum(flow, months, period_months)
                    )
            else:
                curr, prev = explicit[horizon]
                change = calculate_pct_change(curr, prev)

            changes[horizon] = change

            history = explicit_histories[horizon]
            if history is None and flow is not None:
                history = momentum_history(flow, months, is_flow, period_months)
            strengths[horizon] = relative_strength(change, history)
            percentiles[horizon] = historical_percentile_abs(change, history)

            momentum[horizon] = MomentumResult(
                pct_change=change,
                direction=classify_direction(change),
                relative_strength=strengths[horizon],
                percentile=percentiles[horizon],
                status="VALID" if change is not None else "MISSING",
            )

        directions = {h: momentum[h].direction for h in momentum}
        state, valid_count = determine_trend_state(directions, strengths)
        coverage = (
            "FULL" if valid_count == 3
            else "LIMITED" if valid_count == 2
            else "INSUFFICIENT"
        )

        # ---------------- Layer 1: Historical Comparison ----------------
        historical = self._historical_layer(
            val_mom, val_qoq, val_yoy,
            same_period_history, annual_history,
            period_months, flow,
        )

        # ---------------- Layer 2: Seasonal Analysis ----------------
        seasonal = self._seasonal_layer(
            flow, seasonal_history, same_period_history, is_flow,
            period_months,
        )

        # ---------------- Layer 4: Context Flags ----------------
        # Low Base judges the *base* of the growth calculation, i.e. the
        # prior-period observation, against comparable historical bases.
        base_value = val_3m_prev
        if base_value is None and flow is not None and len(flow) >= 2:
            base_value = flow[-2]
        low_base = is_low_base(base_value, historical_low_base_values)

        primary = (val_3m_curr, val_3m_prev)
        sign_kind = sign_change_kind(*primary)
        if sign_kind is None and seasonal.flag == "SIGN_CHANGE":
            sign_kind = "SIGN_CHANGE"

        zero_base = is_zero_base(*primary)
        if not zero_base and seasonal.flag == "ZERO_BASE":
            zero_base = True

        one_off_history = historical_low_base_values
        if one_off_history is None:
            one_off_history = same_period_history
        if one_off_history is None and flow is not None and len(flow) > 1:
            one_off_history = list(flow)[:-1]
        one_off, one_off_reason = detect_one_off(val_3m_curr, one_off_history)

        # Data quality judges whether enough *analytical* input existed to
        # produce a meaningful Stage 4 result. It is not merely "no series was
        # passed": explicit horizon pairs alone are a legitimate input mode,
        # so the question is whether any horizon actually resolved.
        has_history = (
            historical_low_base_values is not None
            or same_period_history is not None
            or seasonal_history is not None
            or flow is not None
        )
        data_quality = "OK"
        if not any(changes[h] is not None for h in changes):
            data_quality = "MISSING_INPUT"
        elif not has_history:
            data_quality = "INSUFFICIENT_HISTORY"

        context = ContextFlags(
            low_base=low_base,
            sign_change=sign_kind,
            zero_base=zero_base,
            one_off=one_off,
            one_off_reason=one_off_reason,
            data_quality=data_quality,
            data_sufficiency=coverage,
        )

        comparisons = {
            h: ComparisonResult(
                h,
                changes[h],
                "VALID" if changes[h] is not None else "MISSING",
            )
            for h in ("3M", "6M", "12M")
        }

        return TrendResult(
            company_id=company_id,
            period_id=period_id,
            metric_code=metric_code,
            trend_state=state,
            coverage=coverage,
            low_base_flag=low_base,
            sign_change_flag=sign_kind is not None,
            comparisons=comparisons,
            calculation_timestamp=datetime.utcnow(),
            historical=historical,
            seasonal=seasonal,
            momentum=momentum,
            context=context,
            trend_coverage=coverage,
            trend_confidence=(
                "HIGH" if valid_count == 3
                else "MEDIUM" if valid_count == 2
                else "LOW"
            ),
        )

    # ------------------------------------------------------------------
    # Layer 1 - Historical Comparison
    # ------------------------------------------------------------------
    def _historical_layer(
        self,
        val_mom: Optional[tuple],
        val_qoq: Optional[tuple],
        val_yoy: Optional[tuple],
        same_period_history: Optional[Sequence[float]],
        annual_history: Optional[Sequence[float]],
        period_months: int,
        series: Optional[Sequence[Optional[float]]],
    ) -> HistoricalResult:
        """MoM / QoQ / YoY / Same-Period Multi-Year / Multi-Year Trend.

        MoM / QoQ / YoY resolve from the supplied series when the caller does
        not pass explicit pairs, using calendar alignment against the series
        granularity; the explicit pairs win when both are given.
        """
        mom = calculate_pct_change(*val_mom) if val_mom else None
        qoq = calculate_pct_change(*val_qoq) if val_qoq else None
        yoy = calculate_pct_change(*val_yoy) if val_yoy else None

        if series is not None and series:
            if mom is None:
                mom = period_comparison(series, 1, period_months)
            if qoq is None:
                qoq = period_comparison(series, 3, period_months)
            if yoy is None:
                yoy = period_comparison(series, 12, period_months)

        if same_period_history is not None:
            current = same_period_history[-1] if len(same_period_history) else None
            # The final entry IS the current period; it must not be compared
            # against itself, which would emit a spurious 0% "Y-n" row. The
            # remaining history is oldest-first, but the specification's
            # example lists the most recent year first, so reverse it before
            # comparing: Y-1 is the immediately preceding same period.
            detail_rows = same_period_multi_year(
                current, list(reversed(list(same_period_history)[:-1]))
            )
        elif series is not None and len(series) >= 1:
            current = series[-1]
            detail_rows = same_period_multi_year(current, list(series)[:-1])
        else:
            detail_rows = []

        detail: List[PeriodComparison] = []
        for offset, change, flag in detail_rows:
            label = f"Y-{int(offset)}"
            detail.append(PeriodComparison(label=label, pct_change=change, flag=flag))

        latest = detail[0].pct_change if detail else None
        valid_changes = [d.pct_change for d in detail if d.pct_change is not None]
        average = sum(valid_changes) / len(valid_changes) if valid_changes else None

        annual = annual_history
        if annual is None and series is not None:
            annual = list(series)

        resolved = [v for v in (mom, qoq, yoy) if v is not None]
        sufficiency = (
            "FULL" if len(resolved) == 3
            else "LIMITED" if resolved
            else "INSUFFICIENT"
        )

        return HistoricalResult(
            mom=mom,
            qoq=qoq,
            yoy=yoy,
            same_period_detail=detail,
            same_period_latest=latest,
            same_period_average=average,
            multi_year_trend=multi_year_trend(annual),
            period_months=period_months,
            sufficiency=sufficiency,
        )

    # ------------------------------------------------------------------
    # Layer 2 - Seasonal Analysis
    # ------------------------------------------------------------------
    def _seasonal_layer(
        self,
        series: Optional[Sequence[Optional[float]]],
        seasonal_history: Optional[Sequence[float]],
        same_period_history: Optional[Sequence[float]],
        is_flow: bool,
        period_months: int = 3,
    ) -> SeasonalResult:
        """Seasonal Baseline (median), Seasonal Surprise, sufficiency.

        Explicit `seasonal_history` / `same_period_history` win when given.
        Otherwise the same-period series is reconstructed from the observation
        series by stepping back one full year at a time.
        """
        candidates = [seasonal_history, same_period_history]
        for candidate in candidates:
            if candidate is None:
                continue
            current = candidate[-1] if len(candidate) else None
            history = list(candidate)[:-1]
            baseline = seasonal_baseline(history)
            surprise, flag = seasonal_surprise(current, baseline)
            usable = [v for v in history if v is not None]
            if baseline is not None:
                return SeasonalResult(
                    baseline=baseline,
                    surprise=surprise,
                    data_sufficiency="FULL",
                    observation_count=len(usable),
                    flag=flag,
                )
            return SeasonalResult(
                baseline=None,
                surprise=None,
                data_sufficiency="INSUFFICIENT_DATA",
                observation_count=len(usable),
                flag=flag,
            )

        if series is None or not len(series):
            return SeasonalResult(
                baseline=None,
                surprise=None,
                data_sufficiency="INSUFFICIENT_DATA",
                observation_count=0,
                flag=None,
            )

        # Same-period history for the latest observation, stepped back one
        # full year at a time: 12 months / period_months periods per step.
        # For a quarterly series this is Q(t-4), Q(t-8), Q(t-12), ...
        seasonal_lag = max(1, 12 // period_months)
        current = series[-1]
        history = [
            series[i]
            for i in range(len(series) - 1 - seasonal_lag, -1, -seasonal_lag)
        ]
        baseline = seasonal_baseline(history)
        surprise, flag = seasonal_surprise(current, baseline)
        usable = [v for v in history if v is not None]
        if baseline is not None:
            return SeasonalResult(
                baseline=baseline,
                surprise=surprise,
                data_sufficiency="FULL",
                observation_count=len(usable),
                flag=flag,
            )
        return SeasonalResult(
            baseline=None,
            surprise=None,
            data_sufficiency="INSUFFICIENT_DATA",
            observation_count=len(usable),
            flag=flag,
        )
