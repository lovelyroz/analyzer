from typing import Optional, Sequence


def calculate_pct_change(current_val: Optional[float], prior_val: Optional[float]) -> Optional[float]:
    """Calculate percentage change without fabricating zero-base/sign-change growth."""
    if current_val is None or prior_val is None or prior_val == 0:
        return None
    if (current_val < 0 <= prior_val) or (current_val >= 0 > prior_val):
        return None
    return ((current_val - prior_val) / abs(prior_val)) * 100.0


def is_low_base(
    base_val: Optional[float],
    historical_bases: Optional[Sequence[float]] = None,
) -> Optional[bool]:
    """Detect Low Base using the Stage 4 median/MAD robust-z rule.

    At least three comparable historical observations are required. With
    insufficient observations the result is UNKNOWN (None), not False.
    """
    if base_val is None or historical_bases is None or len(historical_bases) < 3:
        return None

    values = [float(v) for v in historical_bases if v is not None]
    if len(values) < 3:
        return None

    ordered = sorted(values)
    n = len(ordered)
    median = ordered[n // 2] if n % 2 else (ordered[n // 2 - 1] + ordered[n // 2]) / 2
    deviations = sorted(abs(v - median) for v in ordered)
    m = len(deviations)
    mad = deviations[m // 2] if m % 2 else (deviations[m // 2 - 1] + deviations[m // 2]) / 2

    if mad == 0:
        return bool(base_val < median)

    robust_z = (base_val - median) / (1.4826 * mad)
    return robust_z <= -2.5


def is_sign_change(current_val: Optional[float], prior_val: Optional[float]) -> bool:
    """Detect a transition between profit and loss regimes."""
    if current_val is None or prior_val is None:
        return False
    return (current_val >= 0 and prior_val < 0) or (current_val < 0 and prior_val >= 0)


def historical_percentile_abs(current_change: Optional[float], historical_changes: Optional[Sequence[float]]) -> Optional[float]:
    """Percentile rank of absolute momentum using the company's own history."""
    if current_change is None or historical_changes is None:
        return None
    values = [abs(float(v)) for v in historical_changes if v is not None]
    if len(values) < 8:
        return None
    current = abs(current_change)
    less_or_equal = sum(v <= current for v in values)
    return 100.0 * less_or_equal / len(values)


def relative_strength(current_change: Optional[float], historical_changes: Optional[Sequence[float]]) -> Optional[str]:
    """Return Weak/Normal/Strong from the Stage 4 historical percentile rule."""
    percentile = historical_percentile_abs(current_change, historical_changes)
    if percentile is None:
        return None
    if percentile < 50:
        return "Weak"
    if percentile < 75:
        return "Normal"
    return "Strong"
