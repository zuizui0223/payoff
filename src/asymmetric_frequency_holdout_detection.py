"""Sharp asymmetric-endpoint holdout design for PAYOFF frequency validation.

This module extends the bounded-error Lipschitz design when the reciprocal endpoint
measurements have different deterministic error half-widths. It remains a
non-probabilistic measurement-design result, not statistical power.

For true residual r(p)=Delta_true(p)-Delta_canonical(p), r(0)=r(1)=0 and
|r(x)-r(y)| <= L|x-y|, an interior holdout at p has true-residual nondetection
threshold

    b(p)=2[e_h+(1-p)e_u+p e_v].

Write

    B = b(1/2) = 2 e_h + e_u + e_v,
    d = 2(e_v-e_u),
    delta = |d|.

If B >= L/2, no finite interior design improves the endpoint-only minimax ceiling
L/2. If B < L/2, then automatically delta < L and the m-point minimax design is
unique. Its minimax value depends only on (B, delta); swapping e_u and e_v merely
reflects the optimal frequencies around 1/2.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F

from .frequency_holdout_design import _nonnegative, _positive_int
from .frequency_holdout_detection import (
    comparison_nondetection_threshold,
    design_uniform_error_lipschitz_detection,
    worst_undetectable_lipschitz_amplitude,
)


@dataclass(frozen=True)
class AsymmetricEndpointLipschitzDetectionReceipt:
    holdout_count: int
    residual_lipschitz_bound_exact: str
    endpoint_u_error_halfwidth_exact: str
    endpoint_v_error_halfwidth_exact: str
    interior_error_halfwidth_exact: str
    midpoint_nondetection_threshold_exact: str
    signed_threshold_slope_exact: str
    absolute_threshold_slope_exact: str
    recommended_frequencies_exact: tuple[str, ...]
    minimax_undetectable_amplitude_exact: str
    irreducible_detection_floor_exact: str
    centroid_exact: str
    centroid_shift_from_half_exact: str
    shift_direction: str
    holdouts_improve_minimax_guarantee: bool
    design_unique: bool
    single_holdout_midpoint_invariant: bool
    guarantee: str = (
        "every_declared_L_lipschitz_residual_with_sup_abs_strictly_above_"
        "minimax_undetectable_amplitude_forces_at_least_one_holdout_rejection"
    )
    statistical_power_computed: bool = False
    probability_model_used: bool = False
    biological_replication_count_identified: bool = False


def design_asymmetric_endpoint_lipschitz_detection(
    holdout_count: int,
    *,
    residual_lipschitz_bound: object,
    endpoint_u_error_halfwidth: object,
    endpoint_v_error_halfwidth: object,
    interior_error_halfwidth: object,
) -> AsymmetricEndpointLipschitzDetectionReceipt:
    """Return the exact minimax design under unequal reciprocal-endpoint errors.

    The endpoint labels follow the existing PAYOFF convention:
      u = Delta(0), so e_u belongs to p=0;
      v = -Delta(1), so e_v contributes to prediction uncertainty at p=1.

    Let B=2 e_h+e_u+e_v and delta=2|e_v-e_u|. In the informative regime B<L/2,
    define q=(L-delta)/(L+delta). For delta>0 the exact minimax ceiling is

      U_m = L [ B(1-q^m) + (delta/2)(1+q^m) ]
                / [ (L+delta)(1-q^(m+1)) ].

    When e_v>e_u, construct the unique points from the right-noisier recurrence

      a = B-delta/2,
      p_1 = (2U_m-a)/(L+delta),
      p_{i+1} = [(L-delta)p_i + 2(U_m-a)]/(L+delta).

    When e_u>e_v, reflect that design: p_i -> 1-p_{m+1-i}. Equal endpoint errors
    reduce exactly to `design_uniform_error_lipschitz_detection`.

    The infinite-density deterministic floor is

      U_inf = L(B+delta/2)/(L+delta)
            = 2L(e_h+max(e_u,e_v))/(L+2|e_v-e_u|).

    A single holdout remains exactly p=1/2 regardless of endpoint asymmetry. For
    m>=2 in the informative unequal-error regime, the design centroid lies on the
    noisier-endpoint side of 1/2. This compensates for the wider endpoint-derived
    prediction band on that side.
    """
    m = _positive_int(holdout_count, "holdout_count")
    L = _nonnegative(residual_lipschitz_bound, "residual_lipschitz_bound")
    eu = _nonnegative(endpoint_u_error_halfwidth, "endpoint_u_error_halfwidth")
    ev = _nonnegative(endpoint_v_error_halfwidth, "endpoint_v_error_halfwidth")
    eh = _nonnegative(interior_error_halfwidth, "interior_error_halfwidth")

    B = 2*eh + eu + ev
    d = 2*(ev-eu)
    delta = abs(d)

    if L == 0:
        ps = tuple(F(i, m+1) for i in range(1, m+1))
        centroid = sum(ps, F(0))/m
        return AsymmetricEndpointLipschitzDetectionReceipt(
            m, "0", str(eu), str(ev), str(eh), str(B), str(d), str(delta),
            tuple(map(str, ps)), "0", "0", str(centroid), str(centroid-F(1,2)),
            "no_unique_shift_zero_lipschitz_class", False, False, m == 1,
        )

    if B >= L/2:
        # Every sample threshold lies on/above the endpoint triangle at its best
        # point (the midpoint), so no finite interior sample can improve L/2.
        ps = tuple(F(i, m+1) for i in range(1, m+1))
        centroid = sum(ps, F(0))/m
        thresholds = tuple(comparison_nondetection_threshold(
            p, endpoint_u_error_halfwidth=eu, endpoint_v_error_halfwidth=ev,
            interior_error_halfwidth=eh) for p in ps)
        oracle = worst_undetectable_lipschitz_amplitude(
            ps, thresholds, residual_lipschitz_bound=L)
        if oracle != L/2:
            raise ArithmeticError("noise-dominated asymmetric theorem failed oracle check")
        return AsymmetricEndpointLipschitzDetectionReceipt(
            m, str(L), str(eu), str(ev), str(eh), str(B), str(d), str(delta),
            tuple(map(str, ps)), str(L/2), str(L/2), str(centroid),
            str(centroid-F(1,2)), "no_unique_shift_noise_dominated", False, False,
            m == 1,
        )

    # B<L/2 implies eu+ev<L/2, hence delta=2|ev-eu|<L automatically.
    if not delta < L:
        raise ArithmeticError("informative asymmetric regime must have delta<L")

    if delta == 0:
        base = design_uniform_error_lipschitz_detection(
            m, residual_lipschitz_bound=L,
            endpoint_error_halfwidth=eu, interior_error_halfwidth=eh)
        ps = tuple(F(x) for x in base.recommended_frequencies_exact)
        centroid = sum(ps, F(0))/m
        return AsymmetricEndpointLipschitzDetectionReceipt(
            m, str(L), str(eu), str(ev), str(eh), str(B), "0", "0",
            tuple(map(str, ps)), base.minimax_undetectable_amplitude_exact,
            base.irreducible_detection_floor_exact, str(centroid),
            str(centroid-F(1,2)), "symmetric_endpoint_precision", True, True,
            m == 1,
        )

    q = (L-delta)/(L+delta)
    qm = q**m
    U = L*(B*(1-qm) + (delta/F(2))*(1+qm)) / (
        (L+delta)*(1-q**(m+1))
    )

    # Canonical orientation: p=1 endpoint is the noisier one.
    a = B-delta/F(2)
    right_noisier: list[F] = []
    p = (2*U-a)/(L+delta)
    right_noisier.append(p)
    for _ in range(1, m):
        p = ((L-delta)*p + 2*(U-a))/(L+delta)
        right_noisier.append(p)

    if ev > eu:
        ps = tuple(right_noisier)
        side = "toward_noisier_p1_v_endpoint" if m >= 2 else "midpoint_invariant"
    else:
        ps = tuple(1-p for p in reversed(right_noisier))
        side = "toward_noisier_p0_u_endpoint" if m >= 2 else "midpoint_invariant"

    if any(not F(0) < p < F(1) for p in ps) or tuple(sorted(ps)) != ps:
        raise ArithmeticError("closed-form asymmetric design produced invalid frequencies")

    thresholds = tuple(comparison_nondetection_threshold(
        p, endpoint_u_error_halfwidth=eu, endpoint_v_error_halfwidth=ev,
        interior_error_halfwidth=eh) for p in ps)
    oracle = worst_undetectable_lipschitz_amplitude(
        ps, thresholds, residual_lipschitz_bound=L)
    if oracle != U:
        raise ArithmeticError("closed-form asymmetric minimax design failed exact oracle")

    floor = L*(B+delta/F(2))/(L+delta)
    centroid = sum(ps, F(0))/m
    shift = centroid-F(1,2)
    if m == 1:
        if ps != (F(1,2),) or shift != 0:
            raise ArithmeticError("one-holdout asymmetric midpoint theorem failed")
    elif ev > eu and not shift > 0:
        raise ArithmeticError("right-noisier centroid-shift theorem failed")
    elif eu > ev and not shift < 0:
        raise ArithmeticError("left-noisier centroid-shift theorem failed")

    return AsymmetricEndpointLipschitzDetectionReceipt(
        m, str(L), str(eu), str(ev), str(eh), str(B), str(d), str(delta),
        tuple(map(str, ps)), str(U), str(floor), str(centroid), str(shift), side,
        True, True, m == 1,
    )
