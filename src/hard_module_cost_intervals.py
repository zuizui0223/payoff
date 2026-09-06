"""Interval identification for constant hard-module architecture cost."""

from __future__ import annotations

from typing import Dict, Sequence, Tuple

Interval = Tuple[float, float]


def partition_kappa_interval(
    recovery_interval: Interval,
    direct_margin_interval: Interval,
    module_count: int,
    constrain_nonnegative: bool = True,
) -> Interval:
    """Return interval for kappa=(R-Delta)/(module_count-1)."""

    r_lo, r_hi = _validate_interval(recovery_interval, "recovery_interval")
    d_lo, d_hi = _validate_interval(direct_margin_interval, "direct_margin_interval")
    if r_lo < 0.0:
        raise ValueError("recovery interval must be non-negative")
    if module_count <= 1:
        raise ValueError("module_count must exceed one")
    q = module_count - 1
    lower = (r_lo - d_hi) / q
    upper = (r_hi - d_lo) / q
    if constrain_nonnegative:
        lower = max(0.0, lower)
    return lower, upper


def common_kappa_interval(
    recovery_intervals: Sequence[Interval],
    direct_margin_intervals: Sequence[Interval],
    module_counts: Sequence[int],
    constrain_nonnegative: bool = True,
) -> Dict[str, object]:
    """Intersect partition-specific kappa intervals."""

    n = len(recovery_intervals)
    if n == 0 or len(direct_margin_intervals) != n or len(module_counts) != n:
        raise ValueError("all input sequences must have same non-zero length")
    intervals = tuple(
        partition_kappa_interval(r, d, k, constrain_nonnegative)
        for r, d, k in zip(
            recovery_intervals, direct_margin_intervals, module_counts
        )
    )
    lower = max(interval[0] for interval in intervals)
    upper = min(interval[1] for interval in intervals)
    return {
        "partition_intervals": intervals,
        "common_lower": lower,
        "common_upper": upper,
        "compatible": lower <= upper,
    }


def predicted_margin_interval(
    recovery_interval: Interval,
    kappa_interval: Interval,
    module_count: int,
) -> Interval:
    """Propagate R interval and frozen kappa interval into Delta=R-q*kappa."""

    r_lo, r_hi = _validate_interval(recovery_interval, "recovery_interval")
    k_lo, k_hi = _validate_interval(kappa_interval, "kappa_interval")
    if module_count <= 1:
        raise ValueError("module_count must exceed one")
    q = module_count - 1
    return r_lo - q * k_hi, r_hi - q * k_lo


def intervals_overlap(left: Interval, right: Interval) -> bool:
    """Return whether two closed intervals overlap."""

    l_lo, l_hi = _validate_interval(left, "left")
    r_lo, r_hi = _validate_interval(right, "right")
    return max(l_lo, r_lo) <= min(l_hi, r_hi)


def interval_gap(left: Interval, right: Interval) -> float:
    """Return zero for overlap, otherwise distance between two intervals."""

    l_lo, l_hi = _validate_interval(left, "left")
    r_lo, r_hi = _validate_interval(right, "right")
    if intervals_overlap((l_lo, l_hi), (r_lo, r_hi)):
        return 0.0
    if l_hi < r_lo:
        return r_lo - l_hi
    return l_lo - r_hi


def _validate_interval(interval: Interval, name: str) -> Interval:
    if len(interval) != 2:
        raise ValueError(f"{name} must have two values")
    lower = float(interval[0])
    upper = float(interval[1])
    if lower > upper:
        raise ValueError(f"{name} lower bound must not exceed upper bound")
    return lower, upper
