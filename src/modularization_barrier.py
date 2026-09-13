"""Local-versus-global edge decoupling thresholds for PAYOFF modularization."""

from __future__ import annotations

from math import isfinite
from sys import float_info
from typing import Dict, Tuple


_DEFAULT_REL_TOL = 64.0 * float_info.epsilon


def _finite_nonnegative(value: float, name: str) -> float:
    value = float(value)
    if not isfinite(value) or value < 0.0:
        raise ValueError(f"{name} must be finite and non-negative")
    return value


def _relative_close(left: float, right: float, rel_tol: float) -> bool:
    scale = max(abs(left), abs(right))
    if scale == 0.0:
        return left == right
    return abs(left - right) <= rel_tol * scale


def generic_decoupling_thresholds(
    initial_marginal_recovery: float,
    full_recovery: float,
    max_decoupling: float,
) -> Tuple[float, float]:
    """Return (k_local,k_global) for linear cost k*d.

    k_local=R'(0), k_global=R(dmax)/dmax.
    Caller should use this when recovery is known to be convex.
    """

    local = _finite_nonnegative(
        initial_marginal_recovery, "initial_marginal_recovery"
    )
    full_recovery = _finite_nonnegative(full_recovery, "full_recovery")
    max_decoupling = float(max_decoupling)
    if not isfinite(max_decoupling) or max_decoupling <= 0.0:
        raise ValueError("max_decoupling must be finite and positive")
    global_threshold = full_recovery / max_decoupling
    if not isfinite(global_threshold):
        raise ValueError("global threshold overflow; rescale inputs")
    if global_threshold < local and not _relative_close(
        global_threshold, local, _DEFAULT_REL_TOL
    ):
        raise ValueError("thresholds violate convex-recovery ordering")
    return local, global_threshold


def classify_linear_decoupling_cost(
    unit_cost: float,
    local_threshold: float,
    global_threshold: float,
    tol: float = _DEFAULT_REL_TOL,
) -> str:
    """Classify accessible release / finite jump / retained coupling.

    ``tol`` is a dimensionless relative numerical tolerance.  The scientific
    thresholds and unit cost share the same marginal-cost units, so no fixed
    physical-unit band enters the classification.
    """

    unit_cost = _finite_nonnegative(unit_cost, "unit_cost")
    local_threshold = _finite_nonnegative(local_threshold, "local_threshold")
    global_threshold = _finite_nonnegative(global_threshold, "global_threshold")
    tol = float(tol)
    if not isfinite(tol) or tol < 0.0:
        raise ValueError("tol must be finite and non-negative")
    if global_threshold < local_threshold and not _relative_close(
        global_threshold, local_threshold, tol
    ):
        raise ValueError("require 0<=local_threshold<=global_threshold")

    if _relative_close(unit_cost, local_threshold, tol):
        return "local_neutral_boundary"
    if unit_cost < local_threshold:
        return "locally_accessible_release"
    if _relative_close(unit_cost, global_threshold, tol):
        return "global_endpoint_neutral_boundary"
    if unit_cost < global_threshold:
        return "finite_jump_barrier"
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
