"""Local-versus-global edge decoupling thresholds for PAYOFF modularization."""

from __future__ import annotations

from typing import Dict, Tuple


def generic_decoupling_thresholds(
    initial_marginal_recovery: float,
    full_recovery: float,
    max_decoupling: float,
) -> Tuple[float, float]:
    """Return (k_local,k_global) for linear cost k*d.

    k_local=R'(0), k_global=R(dmax)/dmax.
    Caller should use this when recovery is known to be convex.
    """

    if initial_marginal_recovery < 0.0:
        raise ValueError("initial_marginal_recovery must be non-negative")
    if full_recovery < 0.0:
        raise ValueError("full_recovery must be non-negative")
    if max_decoupling <= 0.0:
        raise ValueError("max_decoupling must be positive")
    local = initial_marginal_recovery
    global_threshold = full_recovery / max_decoupling
    if global_threshold + 1e-12 < local:
        raise ValueError("thresholds violate convex-recovery ordering")
    return local, global_threshold


def classify_linear_decoupling_cost(
    unit_cost: float,
    local_threshold: float,
    global_threshold: float,
    tol: float = 1e-12,
) -> str:
    """Classify accessible release / finite jump / retained coupling."""

    if unit_cost < 0.0:
        raise ValueError("unit_cost must be non-negative")
    if local_threshold < 0.0 or global_threshold < local_threshold - tol:
        raise ValueError("require 0<=local_threshold<=global_threshold")
    if unit_cost < local_threshold - tol:
        return "locally_accessible_release"
    if abs(unit_cost - local_threshold) <= tol:
        return "local_neutral_boundary"
    if unit_cost < global_threshold - tol:
        return "finite_jump_barrier"
    if abs(unit_cost - global_threshold) <= tol:
        return "global_endpoint_neutral_boundary"
    return "retained_coupling"


def two_function_release_thresholds(
    a: float,
    b: float,
    theta_gap: float,
    reference_coupling: float,
) -> Dict[str, float]:
    """Return exact two-function local/global full-release thresholds.

    s0=ab/[ab+c0(a+b)]
    k_local=s0^2*Delta^2
    k_global=s0*Delta^2
    width=s0(1-s0)Delta^2.
    """

    if a <= 0.0 or b <= 0.0:
        raise ValueError("a and b must be positive")
    if reference_coupling <= 0.0:
        raise ValueError("reference_coupling must be positive")
    gap2 = theta_gap * theta_gap
    q0 = a * b + reference_coupling * (a + b)
    s0 = a * b / q0
    local = s0 * s0 * gap2
    global_threshold = s0 * gap2
    return {
        "separation_fraction": s0,
        "local_threshold": local,
        "global_threshold": global_threshold,
        "barrier_width": global_threshold - local,
        "threshold_ratio": float("inf") if local == 0.0 else global_threshold / local,
        "max_possible_width_at_fixed_gap": 0.25 * gap2,
    }


def two_function_classify_cost(
    a: float,
    b: float,
    theta_gap: float,
    reference_coupling: float,
    unit_cost: float,
) -> str:
    """Classify unit decoupling cost in the exact two-function model."""

    summary = two_function_release_thresholds(
        a, b, theta_gap, reference_coupling
    )
    return classify_linear_decoupling_cost(
        unit_cost,
        summary["local_threshold"],
        summary["global_threshold"],
    )
