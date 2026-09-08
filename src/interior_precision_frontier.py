"""Exact interior-measurement precision frontier for PAYOFF holdout validation.

Given a fixed number of distinct interior frequency settings m, a target nonlinear
residual amplitude A, a Lipschitz bound L, and reciprocal endpoint error half-widths
(e_u,e_v), this module returns the sharp excluded upper bound on the common
interior holdout error half-width e_h that guarantees detection under the existing
minimax design.

This is deterministic measurement-design infrastructure, not statistical power and
not a biological replicate calculation.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F

from .frequency_holdout_design import _nonnegative, _positive_int
from .reciprocal_invasion_identification import _q


def _positive(value: object, name: str) -> F:
    x = _q(value)
    if x <= 0:
        raise ValueError(f"{name} must be positive")
    return x


def _minimax_from_B(m: int, L: F, B: F, delta: F) -> F:
    """Sharp m-point minimax ceiling for a supplied midpoint threshold B."""
    if delta == 0:
        return B + (L/F(2)-B)/F(m+1)
    q = (L-delta)/(L+delta)
    qm = q**m
    return L*(B*(1-qm)+(delta/F(2))*(1+qm)) / (
        (L+delta)*(1-q**(m+1))
    )


@dataclass(frozen=True)
class InteriorPrecisionFrontierReceipt:
    holdout_count: int
    residual_lipschitz_bound_exact: str
    target_sup_residual_amplitude_exact: str
    endpoint_u_error_halfwidth_exact: str
    endpoint_v_error_halfwidth_exact: str
    endpoint_error_sum_exact: str
    endpoint_asymmetry_exact: str
    zero_interior_error_minimax_amplitude_exact: str | None
    critical_midpoint_nondetection_threshold_excluded_exact: str | None
    critical_interior_error_halfwidth_excluded_exact: str | None
    guarantee: str | None
    status: str
    boundary_is_excluded: bool = True
    frequency_tuple_instantiated: bool = False
    statistical_power_computed: bool = False
    biological_replication_count_identified: bool = False


def required_interior_precision_for_amplitude(
    holdout_count: int,
    target_sup_residual_amplitude: object,
    *,
    residual_lipschitz_bound: object,
    endpoint_u_error_halfwidth: object,
    endpoint_v_error_halfwidth: object,
) -> InteriorPrecisionFrontierReceipt:
    """Return the sharp strict upper bound on common interior error half-width.

    Let S=e_u+e_v, delta=2|e_v-e_u| and B=2e_h+S. For fixed m,L,delta the sharp
    minimax nondetection ceiling U_m is affine in B. Solving U_m<A yields a unique
    critical B and hence

        e_h < e_h,crit = (B_crit-S)/2.

    Equality is excluded because U_m=A permits closed-band contact.

    For delta>0, q=(L-delta)/(L+delta) and

        B_crit = { A(L+delta)(1-q^(m+1))/L
                   - (delta/2)(1+q^m) }
                 / (1-q^m).

    For delta=0 the exact continuous reduction is

        B_crit = [(m+1)A-L/2]/m.

    If B_crit<=S, even perfect interior measurement e_h=0 cannot guarantee the
    target with the declared finite count and endpoint errors. If A>L/2 (or L=0),
    the requested target is outside the nontrivial endpoint-zero L-Lipschitz class.
    """
    m = _positive_int(holdout_count, "holdout_count")
    A = _positive(target_sup_residual_amplitude, "target_sup_residual_amplitude")
    L = _nonnegative(residual_lipschitz_bound, "residual_lipschitz_bound")
    eu = _nonnegative(endpoint_u_error_halfwidth, "endpoint_u_error_halfwidth")
    ev = _nonnegative(endpoint_v_error_halfwidth, "endpoint_v_error_halfwidth")
    S = eu+ev
    delta = 2*abs(ev-eu)

    if L == 0 or A > L/F(2):
        return InteriorPrecisionFrontierReceipt(
            m, str(L), str(A), str(eu), str(ev), str(S), str(delta),
            None, None, None, None,
            "target_amplitude_not_attainable_in_declared_endpoint_zero_Lipschitz_class",
        )

    # If endpoint uncertainty alone already places the midpoint threshold at or
    # above L/2, no nonnegative interior error can restore an informative finite
    # holdout design.
    if S >= L/F(2):
        return InteriorPrecisionFrontierReceipt(
            m, str(L), str(A), str(eu), str(ev), str(S), str(delta),
            str(L/F(2)), None, None, None,
            "endpoint_precision_alone_is_noise_dominated",
        )

    if not delta < L:
        raise ArithmeticError("S<L/2 must imply endpoint asymmetry delta<L")

    U0 = _minimax_from_B(m, L, S, delta)

    if delta == 0:
        Bcrit = (F(m+1)*A-L/F(2))/F(m)
    else:
        q = (L-delta)/(L+delta)
        qm = q**m
        Bcrit = (
            A*(L+delta)*(1-q**(m+1))/L
            - (delta/F(2))*(1+qm)
        )/(1-qm)

    # A<=U_m(e_h=0) is exactly equivalent to Bcrit<=S. Equality is still
    # impossible because the required guarantee is strict U_m<A.
    if Bcrit <= S:
        if not A <= U0:
            raise ArithmeticError("precision-frontier zero-error boundary mismatch")
        return InteriorPrecisionFrontierReceipt(
            m, str(L), str(A), str(eu), str(ev), str(S), str(delta),
            str(U0), str(Bcrit), "0" if Bcrit == S else None, None,
            "no_nonnegative_interior_error_halfwidth_can_guarantee_target_for_fixed_count",
        )

    if not U0 < A:
        raise ArithmeticError("positive precision budget requires zero-error target feasibility")

    ehcrit = (Bcrit-S)/2
    if ehcrit <= 0:
        raise ArithmeticError("critical interior precision must be positive")

    # Exact audit: at the boundary the minimax ceiling must equal A; just below it
    # is strictly smaller because U_m is strictly increasing in B in this regime.
    U_boundary = _minimax_from_B(m, L, Bcrit, delta)
    if U_boundary != A:
        raise ArithmeticError("critical interior precision does not land on exact boundary")

    return InteriorPrecisionFrontierReceipt(
        m, str(L), str(A), str(eu), str(ev), str(S), str(delta), str(U0),
        str(Bcrit), str(ehcrit),
        "guaranteed_for_every_common_interior_error_halfwidth_strictly_below_critical_value",
        "finite_strict_interior_precision_frontier_identified",
    )
