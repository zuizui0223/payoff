"""Precision-allocation theorem for reciprocal PAYOFF endpoint assays.

For a fixed sum of deterministic endpoint error half-widths e_u+e_v and fixed
interior error e_h, balancing the two endpoint precisions minimizes the sharp
m-point Lipschitz nondetection ceiling whenever the design is informative and
m>=2. This is a theorem about resulting error bounds, not about how many biological
replicates should be assigned to each assay.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as F

from .asymmetric_frequency_holdout_detection import (
    design_asymmetric_endpoint_lipschitz_detection,
)
from .frequency_holdout_design import _nonnegative, _positive_int
from .frequency_holdout_detection import design_uniform_error_lipschitz_detection


@dataclass(frozen=True)
class EndpointPrecisionBalanceReceipt:
    holdout_count: int
    residual_lipschitz_bound_exact: str
    endpoint_u_error_halfwidth_exact: str
    endpoint_v_error_halfwidth_exact: str
    endpoint_error_sum_exact: str
    balanced_endpoint_error_halfwidth_exact: str
    interior_error_halfwidth_exact: str
    midpoint_nondetection_threshold_exact: str
    endpoint_asymmetry_exact: str
    actual_minimax_undetectable_amplitude_exact: str
    balanced_counterfactual_minimax_amplitude_exact: str
    asymmetry_penalty_exact: str
    actual_dense_error_floor_exact: str
    balanced_dense_error_floor_exact: str
    dense_floor_asymmetry_penalty_exact: str
    balancing_strictly_improves_finite_design: bool
    balancing_strictly_improves_dense_floor: bool
    balanced_precision_is_unique_minimizer: bool
    one_holdout_asymmetry_invariant: bool
    noise_dominated: bool
    scope: str = "deterministic_error_halfwidth_allocation_two_reciprocal_PAYOFF_endpoints"
    statistical_power_computed: bool = False
    biological_replication_allocation_identified: bool = False


def compare_endpoint_precision_balance(
    holdout_count: int,
    *,
    residual_lipschitz_bound: object,
    endpoint_u_error_halfwidth: object,
    endpoint_v_error_halfwidth: object,
    interior_error_halfwidth: object,
) -> EndpointPrecisionBalanceReceipt:
    """Compare actual endpoint asymmetry with a same-total-error balanced design.

    Holding S=e_u+e_v fixed also holds

        B = 2 e_h + S

    fixed. Let delta=2|e_v-e_u|. In the informative regime B<L/2:

    - m=1: U_1=B/2+L/4 is exactly independent of delta;
    - every m>=2: U_m is uniquely minimized at delta=0, i.e. e_u=e_v=S/2;
    - the dense-design floor is also uniquely minimized at delta=0.

    The result says to equalize the *achieved deterministic error half-widths* if
    that quantity is under design control. It does not imply equal replicate counts
    unless an external precision-vs-replication model justifies that mapping.
    """
    m = _positive_int(holdout_count, "holdout_count")
    L = _nonnegative(residual_lipschitz_bound, "residual_lipschitz_bound")
    eu = _nonnegative(endpoint_u_error_halfwidth, "endpoint_u_error_halfwidth")
    ev = _nonnegative(endpoint_v_error_halfwidth, "endpoint_v_error_halfwidth")
    eh = _nonnegative(interior_error_halfwidth, "interior_error_halfwidth")

    S = eu+ev
    ebar = S/F(2)
    B = 2*eh+S
    delta = 2*abs(ev-eu)

    actual = design_asymmetric_endpoint_lipschitz_detection(
        m, residual_lipschitz_bound=L,
        endpoint_u_error_halfwidth=eu,
        endpoint_v_error_halfwidth=ev,
        interior_error_halfwidth=eh,
    )
    balanced = design_uniform_error_lipschitz_detection(
        m, residual_lipschitz_bound=L,
        endpoint_error_halfwidth=ebar,
        interior_error_halfwidth=eh,
    )

    Ua = F(actual.minimax_undetectable_amplitude_exact)
    Ub = F(balanced.minimax_undetectable_amplitude_exact)
    Fa = F(actual.irreducible_detection_floor_exact)
    Fb = F(balanced.irreducible_detection_floor_exact)
    penalty = Ua-Ub
    floor_penalty = Fa-Fb

    noise_dominated = L == 0 or B >= L/F(2)
    asymmetric = delta > 0
    finite_strict = (not noise_dominated) and asymmetric and m >= 2
    dense_strict = (not noise_dominated) and asymmetric

    if penalty < 0 or floor_penalty < 0:
        raise ArithmeticError("endpoint balancing theorem violated")
    if finite_strict and not penalty > 0:
        raise ArithmeticError("informative m>=2 asymmetry must have positive penalty")
    if (m == 1 or not asymmetric or noise_dominated) and penalty != 0:
        raise ArithmeticError("declared finite-design equality regime must have zero penalty")
    if dense_strict and not floor_penalty > 0:
        raise ArithmeticError("informative endpoint asymmetry must raise dense floor")
    if (not asymmetric or noise_dominated) and floor_penalty != 0:
        raise ArithmeticError("declared dense-floor equality regime must have zero penalty")

    return EndpointPrecisionBalanceReceipt(
        m, str(L), str(eu), str(ev), str(S), str(ebar), str(eh), str(B), str(delta),
        str(Ua), str(Ub), str(penalty), str(Fa), str(Fb), str(floor_penalty),
        finite_strict, dense_strict,
        (not noise_dominated) and m >= 2,
        m == 1, noise_dominated,
    )
