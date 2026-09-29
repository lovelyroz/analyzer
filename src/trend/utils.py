"""Stage 4 historical, seasonal and trend calculation primitives.

Every function here is deterministic and free of look-ahead bias: they only
ever consume observation series that the caller has already restricted to
information available at the evaluation point in time.
"""

from typing import Optional, Sequence, List, Tuple

import math

# Horizons combined into the Stage 4 trend state.
TREND_HORIZONS: Tuple[str, ...] = ("3M", "6M", "12M")

# Stage 4 direction classification. This is a *direction* threshold only:
# it decides whether momentum is clearly positive, clearly negative, or
# near zero. It must never be used as a global threshold for Strong Trend,
# Strong Improvement or Strong Deterioration - those come exclusively from
# the company-relative percentile rule in `relative_strength`.
DIRECTION_THRESHOLD = 2.0

# Minimum historical observations required before a Stage 4 derived flag
# may be asserted (rather than reported as UNKNOWN / INSUFFICIENT_DATA).
SEASONAL_MIN_OBSERVATIONS = 3
LOW_BASE_MIN_OBSERVATIONS = 3
RELATIVE_STRENGTH_MIN_OBSERVATIONS = 8


def _finite(value: object) -> Optional[float]:
    """Return value as float, or None when missing / non-finite.

    Stage 4 rule: MISSING != 0. A None observation never becomes 0.
    """
    if value is None:
        return None
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(result) or math.isinf(result):
        return None
    return result


def median(values: Sequence[float]) -> Optional[float]:
    """Median of a sequence. Returns None when fewer than 1 observation.

    The median is preferred over the mean throughout Stage 4 because it is
    robust to the outliers that dominate low-base / one-off situations.
    """
    numbers = [v for v in (_finite(x) for x in values) if v is not None]
    if not numbers:
        return None
    ordered = sorted(numbers)
    n = len(ordered)
    if n % 2:
        return ordered[n // 2]
    return (ordered[n // 2 - 1] + ordered[n // 2]) / 2.0


def mean_absolute_deviation(values: Sequence[float], center: float) -> Optional[float]:
    """MAD = Median(abs(value - center)) around an already-computed center."""
    if center is None:
        return None
    deviations = [abs(v - center) for v in (_finite(x) for x in values) if v is not None]
    return median(deviations)


def calculate_pct_change(
    current_val: Optional[float],
    prior_val: Optional[float],
) -> Optional[float]:
    """Percentage change Current / Previous - 1, as a percentage.

    Returns None (never a fabricated growth number) when:
      * either observation is missing (MISSING != 0), or
      * the base is exactly zero (ZERO_BASE), or
      * the two observations straddle zero (SIGN_CHANGE / LOSS_TO_PROFIT /
        PROFIT_TO_LOSS).

    The abs() denominator keeps negative-but-same-sign growth meaningful,
    e.g. -120 vs -100 reports -20%, not +20%.
    """
    current = _finite(current_val)
    prior = _finite(prior_val)
    if current is None or prior is None:
        return None
    if prior == 0:
        return None
    if (current < 0 < prior) or (current > 0 > prior):
        return None
    return ((current - prior) / abs(prior)) * 100.0


def sign_change_kind(
    current_val: Optional[float],
    prior_val: Optional[float],
) -> Optional[str]:
    """Classify a regime transition, or None when no transition occurred.

    LOSS_TO_PROFIT and PROFIT_TO_LOSS are the profit/loss-specific labels;
    SIGN_CHANGE covers any other sign reversal (both-negative magnitudes
    flip through zero are impossible without a zero observation).
    """
    current = _finite(current_val)
    prior = _finite(prior_val)
    if current is None or prior is None:
        return None
    if prior == 0 or current == 0:
        return None
    if current > 0 and prior < 0:
        return "LOSS_TO_PROFIT"
    if current < 0 and prior > 0:
        return "PROFIT_TO_LOSS"
    return None


def is_sign_change(current_val: Optional[float], prior_val: Optional[float]) -> bool:
    """Detect a transition between profit and loss regimes."""
    return sign_change_kind(current_val, prior_val) is not None


def is_zero_base(current_val: Optional[float], prior_val: Optional[float]) -> bool:
    """True when the base of a comparison is exactly zero."""
    prior = _finite(prior_val)
    if prior is None or prior != 0:
        return False
    return _finite(current_val) is not None


def is_low_base(
    base_val: Optional[float],
    historical_bases: Optional[Sequence[float]] = None,
) -> Optional[bool]:
    """Detect Low Base using the Stage 4 median/MAD robust-z rule.

    Robust Z = (Base - Median) / (1.4826 x MAD); LOW_BASE when Z <= -2.5.

    At least three comparable historical observations are required. With
    insufficient observations the result is UNKNOWN (None), not False.
    """
    base = _finite(base_val)
    if base is None:
        return None
    if historical_bases is None or len(historical_bases) < LOW_BASE_MIN_OBSERVATIONS:
        return None

    values = [v for v in (_finite(x) for x in historical_bases) if v is not None]
    if len(values) < LOW_BASE_MIN_OBSERVATIONS:
        return None

    med = median(values)
    if med is None:
        return None

    mad = mean_absolute_deviation(values, med)
    if mad is None or mad == 0:
        # Degenerate history (all identical, or a single point): no scale
        # exists for a robust score, so fall back to the plain ordinal rule.
        return bool(base < med)

    robust_z = (base - med) / (1.4826 * mad)
    return robust_z <= -2.5


def detect_one_off(
    current_val: Optional[float],
    historical_values: Optional[Sequence[float]],
) -> Tuple[bool, Optional[str]]:
    """Detect a one-off / abnormal observation, only when reliably detectable.

    Returns (flag, reason). Detection is deliberately conservative and
    mirrors the robust statistics already mandated for Low Base: it fires
    only when the observation is an extreme outlier against at least three
    comparable historical observations with a non-degenerate scale. Anything
    less is reported as not-a-one-off rather than guessed at.
    """
    current = _finite(current_val)
    if current is None or historical_values is None:
        return False, None

    values = [v for v in (_finite(x) for x in historical_values) if v is not None]
    if len(values) < SEASONAL_MIN_OBSERVATIONS:
        return False, None

    med = median(values)
    if med is None:
        return False, None
    mad = mean_absolute_deviation(values, med)
    if mad is None or mad == 0:
        return False, None

    robust_z = (current - med) / (1.4826 * mad)
    if abs(robust_z) > 4.0:
        return True, "ROBUST_Z_GT_4"
    return False, None


def historical_percentile_abs(
    current_change: Optional[float],
    historical_changes: Optional[Sequence[float]],
) -> Optional[float]:
    """Percentile rank [0, 100] of absolute momentum in company history."""
    if current_change is None or historical_changes is None:
        return None
    values = [v for v in (_finite(x) for x in historical_changes) if v is not None]
    if len(values) < RELATIVE_STRENGTH_MIN_OBSERVATIONS:
        return None
    current = abs(_finite(current_change))
    less_or_equal = sum(v <= current for v in values)
    return 100.0 * less_or_equal / len(values)


def relative_strength(
    current_change: Optional[float],
    historical_changes: Optional[Sequence[float]],
) -> Optional[str]:
    """Weak / Normal / Strong from the Stage 4 company-relative percentile.

    Strength is defined by the company's own momentum distribution for the
    same horizon, never by a fixed global growth threshold.
    """
    percentile = historical_percentile_abs(current_change, historical_changes)
    if percentile is None:
        return None
    if percentile < 50:
        return "Weak"
    if percentile < 75:
        return "Normal"
    return "Strong"


def classify_direction(
    pct_change: Optional[float],
    threshold: float = DIRECTION_THRESHOLD,
) -> Optional[str]:
    """Classify momentum direction: Positive / Negative / Weak.

    Only magnitude-vs-zero direction. Relative strength is a separate
    concept and must not be inferred from this classification.
    """
    value = _finite(pct_change)
    if value is None:
        return None
    if value > threshold:
        return "Positive"
    if value < -threshold:
        return "Negative"
    return "Weak"


def seasonal_baseline(
    same_period_history: Optional[Sequence[float]],
) -> Optional[float]:
    """Seasonal Baseline = Median(same period across historical years).

    Requires at least 3 valid historical observations; otherwise the
    baseline is formally INSUFFICIENT_DATA and this returns None.
    """
    if same_period_history is None:
        return None
    values = [v for v in (_finite(x) for x in same_period_history) if v is not None]
    if len(values) < SEASONAL_MIN_OBSERVATIONS:
        return None
    return median(values)


def seasonal_surprise(
    current_val: Optional[float],
    baseline: Optional[float],
) -> Tuple[Optional[float], Optional[str]]:
    """Seasonal Surprise = Current / Seasonal Baseline - 1.

    Returns (surprise, flag). Surprise is None with a ZERO_BASE or
    SIGN_CHANGE flag whenever the baseline is zero or the signs disagree.
    """
    current = _finite(current_val)
    if current is None or baseline is None:
        return None, None
    if baseline == 0:
        return None, "ZERO_BASE"
    if (current < 0 < baseline) or (current > 0 > baseline):
        return None, "SIGN_CHANGE"
    return ((current - baseline) / abs(baseline)) * 100.0, None


def same_period_multi_year(
    current_val: Optional[float],
    same_period_history: Optional[Sequence[float]],
) -> List[Tuple[float, Optional[float], Optional[str]]]:
    """Compare the current period with the same period in prior years.

    Returns one (year_offset, pct_change, flag) tuple per historical
    observation, ordered from the most recent year backwards. Each entry
    carries the ZERO_BASE / SIGN_CHANGE flag when the comparison is not
    expressible as a percentage change.
    """
    current = _finite(current_val)
    if current is None or same_period_history is None:
        return []

    rows: List[Tuple[float, Optional[float], Optional[str]]] = []
    for offset, raw in enumerate(same_period_history, start=1):
        prior = _finite(raw)
        if prior is None:
            rows.append((float(offset), None, "MISSING"))
            continue
        change = calculate_pct_change(current, prior)
        flag = None
        if change is None:
            if prior == 0:
                flag = "ZERO_BASE"
            else:
                flag = sign_change_kind(current, prior) or "SIGN_CHANGE"
        rows.append((float(offset), change, flag))
    return rows


def multi_year_trend(
    annual_values: Optional[Sequence[float]],
) -> Optional[float]:
    """Describe structural multi-year direction as a CAGR-style rate.

    Computed strictly between the earliest and latest *annual* observation,
    so it describes structural direction across years and is deliberately
    independent of the 3M/6M/12M momentum horizons. Returns None when fewer
    than two annual observations exist or the comparison is not expressible.
    """
    if annual_values is None:
        return None
    values = [v for v in (_finite(x) for x in annual_values) if v is not None]
    if len(values) < 2:
        return None

    earliest, latest = values[0], values[-1]
    return calculate_pct_change(latest, earliest)


def period_comparison(
    series: Sequence[Optional[float]],
    months: int,
    period_months: int = 3,
    position: Optional[int] = None,
) -> Optional[float]:
    """Percentage change between two calendar-aligned observations.

    Generic layer-1 primitive backing MoM (1 month), QoQ (3 months) and YoY
    (12 months): it resolves the observation `months` before the evaluation
    point and applies the same MISSING != 0, zero-base and sign-change rules
    as every other Stage 4 comparison. Returns None when either side of the
    comparison falls before the start of the series or is absent.

    This compares observation *levels*, so it is valid for both flow and
    stock variables; window aggregation is a layer-3 concern (section 6).
    """
    values = [(_finite(x) if x is not None else None) for x in series]
    if position is None:
        position = len(values)
    lag = _periods(months, period_months)
    current_idx = position - 1
    prior_idx = current_idx - lag
    if current_idx < 0 or prior_idx < 0:
        return None
    return calculate_pct_change(values[current_idx], values[prior_idx])


def _window_sum(series: Sequence[Optional[float]], end: int, length: int) -> Optional[float]:
    """Sum of `length` consecutive observations ending at index `end` (exclusive)."""
    if end < 0 or end - length < -1:
        return None
    window = list(series[max(0, end - length):end])
    if len(window) < length:
        return None
    if any(v is None for v in window):
        return None
    return float(sum(window))


def _periods(months: int, period_months: int) -> int:
    """Convert a calendar horizon in months into a count of series periods.

    A quarterly series (period_months=3) turns a 3M/6M/12M horizon into a
    1/2/4 period window; a monthly series keeps 3/6/12 periods.
    """
    if period_months <= 0:
        period_months = 3
    return max(1, int(math.ceil(months / float(period_months))))


def flow_momentum(
    series: Sequence[Optional[float]],
    months: int,
    period_months: int = 3,
    position: Optional[int] = None,
) -> Optional[float]:
    """Flow momentum: current window sum / previous window sum - 1.

    Flow variables (Revenue, Operating Profit, Net Profit, Operating Cash
    Flow) are summed across the window. `position` indexes the observation
    *ending* the current window; None means the latest available
    observation. Everything after `position` is ignored, which is what keeps
    this function free of look-ahead bias.
    """
    values = list(series)
    if position is None:
        position = len(values)
    length = _periods(months, period_months)
    current = _window_sum(values, position, length)
    previous = _window_sum(values, position - length, length)
    return calculate_pct_change(current, previous)


def stock_momentum(
    series: Sequence[Optional[float]],
    months: int,
    period_months: int = 3,
    position: Optional[int] = None,
) -> Optional[float]:
    """Stock momentum: period-end value / value `months` earlier - 1.

    Stock variables (Assets, Equity, Debt, Loans, Deposits) are never summed.
    """
    values = [(_finite(x) if x is not None else None) for x in series]
    if position is None:
        position = len(values)
    offset = _periods(months, period_months)
    end = position - 1
    earlier = end - offset
    if end < 0 or earlier < 0:
        return None
    current = values[end]
    prior = values[earlier]
    return calculate_pct_change(current, prior)


def ttm(series: Sequence[Optional[float]], position: Optional[int] = None) -> Optional[float]:
    """Trailing twelve months for a flow variable: sum of the last 4 quarters."""
    values = list(series)
    if position is None:
        position = len(values)
    return _window_sum(values, position, 4)


def trend_12m(
    series: Sequence[Optional[float]],
    period_months: int = 3,
    position: Optional[int] = None,
) -> Optional[float]:
    """12M Trend = Current TTM / TTM ending 12 months earlier - 1.

    Not prior-month TTM. For a quarterly series this means the TTM ending
    at `position` against the TTM ending four quarters earlier.
    """
    values = list(series)
    if position is None:
        position = len(values)
    lag = _periods(12, period_months)
    current = ttm(values, position)
    prior = ttm(values, position - lag)
    return calculate_pct_change(current, prior)


def momentum_history(
    series: Sequence[Optional[float]],
    months: int,
    flow: bool,
    period_months: int = 3,
) -> List[Optional[float]]:
    """Historical momentum series for one horizon, for percentile ranking.

    Walks every point with enough history and evaluates the same momentum
    formula at that point. The result is ordered chronologically and never
    includes the final observation, so the current reading can be ranked
    against it without contaminating the distribution.
    """
    values = list(series)
    results: List[Optional[float]] = []
    if flow:
        start = 2 * _periods(months, period_months)
        # range end is len(values), not len(values) + 1: the position that
        # reads the final (current) observation is excluded so the current
        # reading is never part of its own comparison population (PIT).
        for pos in range(start, len(values)):
            results.append(flow_momentum(values, months, period_months, pos))
    else:
        start = _periods(months, period_months) + 1
        for pos in range(start, len(values)):
            results.append(stock_momentum(values, months, period_months, pos))
    return [r for r in results if r is not None]


def determine_trend_state(
    directions: dict,
    strengths: dict,
) -> Tuple[str, int]:
    """Resolve the Stage 4 trend state from per-horizon evidence.

    Follows section 13 exactly. Strong Improvement / Strong Deterioration
    require *all* valid horizons to agree in direction *and* at least two
    horizons to be Strong (a company-relative measure, not a threshold).
    Returns (state, valid_horizon_count).
    """
    valid = {h: d for h, d in directions.items() if d is not None}
    if len(valid) < 2:
        return "INSUFFICIENT_DATA", len(valid)

    positive = sum(1 for d in valid.values() if d == "Positive")
    negative = sum(1 for d in valid.values() if d == "Negative")
    all_positive = positive == len(valid)
    all_negative = negative == len(valid)
    all_weak = all(d == "Weak" for d in valid.values())

    strong_positive = sum(
        1 for h in valid if valid[h] == "Positive" and strengths.get(h) == "Strong"
    )
    strong_negative = sum(
        1 for h in valid if valid[h] == "Negative" and strengths.get(h) == "Strong"
    )

    # Strong states additionally require full horizon coverage. Section 14
    # caps any two-horizon state at LIMITED coverage/confidence, and the
    # section 15 scenario table confirms a two-horizon all-positive-strong
    # case resolves to Improving, not Strong Improvement.
    if all_positive and len(valid) == 3 and strong_positive >= 2:
        return "Strong Improvement", len(valid)
    if all_negative and len(valid) == 3 and strong_negative >= 2:
        return "Strong Deterioration", len(valid)
    if all_weak or positive == negative:
        return "Stable", len(valid)
    if positive > negative:
        return "Improving", len(valid)
    if negative > positive:
        return "Deteriorating", len(valid)
    return "Stable", len(valid)
