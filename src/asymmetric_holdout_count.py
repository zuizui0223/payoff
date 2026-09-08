"""Exact holdout-count inversion for asymmetric PAYOFF endpoint precision.

This module inverts the sharp asymmetric minimax law without constructing the
m-point frequency tuple. The returned count is the number of distinct interior
frequency settings needed for a deterministic worst-case guarantee; it is not a
biological replicate count and not statistical power.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F

from .frequency_holdout_design import _nonnegative
from .frequency_holdout_detection import required_holdout_count_for_amplitude
from .reciprocal_invasion_identification import _q


def _positive(value: object, name: str) -> F:
    x = _q(value)
    if x <= 0:
        raise ValueError(f"{name} must be positive")
    return x


def _asymmetric_minimax_value(m: int, L: F, B: F, delta: F) -> F:
    if type(m) is not int or m < 1:
        raise ValueError("m must be a positive integer")
    if not (F(0) < delta < L):
        raise ValueError("asymmetric closed form requires 0<delta<L")
    q = (L-delta)/(L+delta)
    qm = q**m
    return L*(B*(1-qm)+(delta/F(2))*(1+qm)) / (
        (L+delta)*(1-q*qm)
    )


def _minimal_integer_power_below(q: F, threshold: F) -> int:
    """Return min m>=1 with q**m < threshold, exactly.

    Preconditions: 0<q<1 and 0<threshold<=1. The implementation uses exact
    rational comparisons, so the excluded equality boundary is never rounded
    into a false guarantee. Exponential bracketing plus binary search uses O(log m)
    power comparisons and does not instantiate the optimal frequency tuple.
    """
    if not F(0) < q < F(1):
        raise ValueError("q must lie strictly between zero and one")
    if not F(0) < threshold <= F(1):
        raise ValueError("threshold must lie in (0,1]")
    if q < threshold:
        return 1
    lo, hi = 1, 2
    while not q**hi < threshold:
        lo, hi = hi, 2*hi
    while hi-lo > 1:
        mid = (lo+hi)//2
        if q**mid < threshold:
            hi = mid
        else:
            lo = mid
    return hi


@dataclass(frozen=True)
class AsymmetricRequiredHoldoutCountReceipt:
    residual_lipschitz_bound_exact: str
    target_sup_residual_amplitude_exact: str
    endpoint_u_error_halfwidth_exact: str
    endpoint_v_error_halfwidth_exact: str
    interior_error_halfwidth_exact: str
    midpoint_nondetection_threshold_exact: str
    absolute_threshold_slope_exact: str
    irreducible_detection_floor_exact: str
    geometric_ratio_exact: str | None
    power_threshold_exact: str | None
    required_holdout_count: int | None
    achieved_minimax_undetectable_amplitude_exact: str | None
    status: str
    strict_boundary: bool = True
    endpoint_swap_count_invariant: bool = True
    frequency_tuple_instantiated: bool = False
    statistical_power_computed: bool = False
    biological_replication_count_identified: bool = False


def required_asymmetric_holdout_count_for_amplitude(
    target_sup_residual_amplitude: object,
    *,
    residual_lipschitz_bound: object,
    endpoint_u_error_halfwidth: object,
    endpoint_v_error_halfwidth: object,
    interior_error_halfwidth: object,
) -> AsymmetricRequiredHoldoutCountReceipt:
    """Return the exact minimum distinct-frequency count for target amplitude A.

    In the informative asymmetric regime define

        B = 2 e_h + e_u + e_v,
        delta = 2 |e_v-e_u|,
        q = (L-delta)/(L+delta),
        U_inf = L(B+delta/2)/(L+delta).

    For U_inf < A <= L/2, the sharp m-point minimax law U_m<A is equivalent to

        q**m < T(A),

    where

        T(A) = [A(L+delta)-L(B+delta/2)]
               / [A(L-delta)+L(delta/2-B)].

    Thus, mathematically,

        m_min = floor(log(T)/log(q)) + 1,

    with the strict +1 also applying when T is an exact power of q. The software
    does NOT use floating logarithms; it finds the minimum integer using exact
    rational power comparisons so closed-band equality is never promoted.

    Equal endpoint errors delegate to the already-verified uniform-error inversion.
    Swapping e_u and e_v leaves B, delta, q, T and therefore the count unchanged.
    """
    A = _positive(target_sup_residual_amplitude, "target_sup_residual_amplitude")
    L = _nonnegative(residual_lipschitz_bound, "residual_lipschitz_bound")
    eu = _nonnegative(endpoint_u_error_halfwidth, "endpoint_u_error_halfwidth")
    ev = _nonnegative(endpoint_v_error_halfwidth, "endpoint_v_error_halfwidth")
    eh = _nonnegative(interior_error_halfwidth, "interior_error_halfwidth")

    B = 2*eh + eu + ev
    delta = 2*abs(ev-eu)

    if L == 0 or A > L/2:
        return AsymmetricRequiredHoldoutCountReceipt(
            str(L), str(A), str(eu), str(ev), str(eh), str(B), str(delta), "0",
            None, None, None, None,
            "target_amplitude_not_attainable_in_declared_endpoint_zero_Lipschitz_class",
        )

    if B >= L/2:
        return AsymmetricRequiredHoldoutCountReceipt(
            str(L), str(A), str(eu), str(ev), str(eh), str(B), str(delta), str(L/2),
            None, None, None, None,
            "no_finite_holdout_count_can_improve_noise_dominated_endpoint_ceiling",
        )

    if delta == 0:
        base = required_holdout_count_for_amplitude(
            A, residual_lipschitz_bound=L,
            endpoint_error_halfwidth=eu, interior_error_halfwidth=eh)
        # In the informative symmetric regime its irreducible floor is B.
        return AsymmetricRequiredHoldoutCountReceipt(
            str(L), str(A), str(eu), str(ev), str(eh), str(B), "0", str(B),
            None, None, base.required_holdout_count,
            base.achieved_minimax_undetectable_amplitude_exact,
            base.status,
        )

    if not delta < L:
        raise ArithmeticError("informative asymmetric regime must have delta<L")

    q = (L-delta)/(L+delta)
    floor = L*(B+delta/F(2))/(L+delta)
    if A <= floor:
        return AsymmetricRequiredHoldoutCountReceipt(
            str(L), str(A), str(eu), str(ev), str(eh), str(B), str(delta), str(floor),
            str(q), None, None, None,
            "no_finite_holdout_count_can_guarantee_detection_at_asymmetric_error_floor",
        )

    numerator = A*(L+delta)-L*(B+delta/F(2))
    denominator = A*(L-delta)+L*(delta/F(2)-B)
    if numerator <= 0 or denominator <= 0:
        raise ArithmeticError("asymmetric inversion threshold must be positive")
    T = numerator/denominator
    if not F(0) < T <= F(1):
        raise ArithmeticError("asymmetric inversion threshold must lie in (0,1]")

    m = _minimal_integer_power_below(q, T)
    U = _asymmetric_minimax_value(m, L, B, delta)
    if not U < A:
        raise ArithmeticError("asymmetric holdout-count inversion failed strict guarantee")
    if m > 1:
        previous = _asymmetric_minimax_value(m-1, L, B, delta)
        if previous < A:
            raise ArithmeticError("reported asymmetric holdout count is not minimal")

    return AsymmetricRequiredHoldoutCountReceipt(
        str(L), str(A), str(eu), str(ev), str(eh), str(B), str(delta), str(floor),
        str(q), str(T), m, str(U), "finite_asymmetric_deterministic_holdout_count_identified",
    )
