"""Identify constant per-extra-module cost from direct hard-module worldlines."""

from __future__ import annotations

from typing import Dict, Sequence, Tuple


def partition_cost_receipt(
    recovery: float,
    direct_margin: float,
    module_count: int,
) -> Dict[str, float]:
    """Return kappa=(R-Delta_W)/(k-1) for one nontrivial partition."""

    if recovery < 0.0:
        raise ValueError("recovery must be non-negative")
    if module_count <= 1:
        raise ValueError("module_count must exceed one")
    q = module_count - 1
    implied_total_cost = recovery - direct_margin
    return {
        "recovery": recovery,
        "direct_margin": direct_margin,
        "extra_module_count": float(q),
        "implied_total_cost": implied_total_cost,
        "implied_kappa": implied_total_cost / q,
    }


def weighted_constant_kappa_fit(
    recoveries: Sequence[float],
    direct_margins: Sequence[float],
    module_counts: Sequence[int],
    analysis_weights: Sequence[float] | None = None,
) -> Dict[str, object]:
    """Fit y_j=kappa*q_j by zero-intercept weighted least squares.

    y_j = recovery_j - direct_margin_j
    q_j = module_count_j - 1
    """

    n = len(recoveries)
    if n == 0 or len(direct_margins) != n or len(module_counts) != n:
        raise ValueError("all input sequences must have same non-zero length")
    if any(recovery < 0.0 for recovery in recoveries):
        raise ValueError("recoveries must be non-negative")
    if any(count <= 1 for count in module_counts):
        raise ValueError("all module_counts must exceed one")

    if analysis_weights is None:
        weights = [1.0] * n
    else:
        if len(analysis_weights) != n:
            raise ValueError("analysis_weights must match input length")
        if any(weight <= 0.0 for weight in analysis_weights):
            raise ValueError("analysis_weights must be positive")
        weights = [float(weight) for weight in analysis_weights]

    q = [count - 1 for count in module_counts]
    y = [recovery - margin for recovery, margin in zip(recoveries, direct_margins)]
    denominator = sum(weight * qi * qi for weight, qi in zip(weights, q))
    numerator = sum(weight * qi * yi for weight, qi, yi in zip(weights, q, y))
    kappa = numerator / denominator

    predicted_margins = [
        recovery - kappa * qi for recovery, qi in zip(recoveries, q)
    ]
    residuals = [
        observed - predicted
        for observed, predicted in zip(direct_margins, predicted_margins)
    ]
    implied_kappas = [yi / qi for yi, qi in zip(y, q)]
    weighted_sse = sum(
        weight * residual * residual for weight, residual in zip(weights, residuals)
    )

    return {
        "kappa_hat": kappa,
        "implied_kappas": tuple(implied_kappas),
        "predicted_margins": tuple(predicted_margins),
        "residuals": tuple(residuals),
        "weighted_sse": weighted_sse,
        "extra_module_counts": tuple(float(qi) for qi in q),
    }


def constant_kappa_max_abs_residual(
    recoveries: Sequence[float],
    direct_margins: Sequence[float],
    module_counts: Sequence[int],
    analysis_weights: Sequence[float] | None = None,
) -> float:
    """Return max absolute bridge residual after fitting constant kappa."""

    fit = weighted_constant_kappa_fit(
        recoveries,
        direct_margins,
        module_counts,
        analysis_weights,
    )
    return max(abs(float(value)) for value in fit["residuals"])
