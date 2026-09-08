from fractions import Fraction as F
import random

import pytest

from src.asymmetric_frequency_holdout_detection import (
    design_asymmetric_endpoint_lipschitz_detection,
)
from src.asymmetric_holdout_count import (
    required_asymmetric_holdout_count_for_amplitude,
)
from src.frequency_holdout_detection import required_holdout_count_for_amplitude


def req(A, *, L=1, eu=F(1,50), ev=F(2,25), eh=F(1,50)):
    return required_asymmetric_holdout_count_for_amplitude(
        A, residual_lipschitz_bound=L,
        endpoint_u_error_halfwidth=eu,
        endpoint_v_error_halfwidth=ev,
        interior_error_halfwidth=eh,
    )


def test_strict_boundary_exact_power_requires_one_more_holdout():
    # Registered asymmetric example: q=11/14 and U_2=41/157.
    # At A=U_2, contact remains compatible, so m=2 is not enough; m=3 is.
    r = req(F(41,157))
    assert r.geometric_ratio_exact == "11/14"
    assert r.power_threshold_exact == "121/196"  # q^2 exactly
    assert r.required_holdout_count == 3
    assert r.achieved_minimax_undetectable_amplitude_exact == "1843/7925"
    assert r.strict_boundary
    assert not r.frequency_tuple_instantiated
    assert not r.statistical_power_computed
    assert not r.biological_replication_count_identified


def test_target_at_endpoint_ceiling_needs_one_holdout_in_informative_regime():
    r = req(F(1,2))
    assert r.power_threshold_exact == "1"
    assert r.required_holdout_count == 1
    assert r.achieved_minimax_undetectable_amplitude_exact == "8/25"


def test_target_at_or_below_dense_floor_has_no_finite_count():
    floor = req(F(5,28))
    assert floor.irreducible_detection_floor_exact == "5/28"
    assert floor.required_holdout_count is None
    assert floor.status == "no_finite_holdout_count_can_guarantee_detection_at_asymmetric_error_floor"
    below = req(F(1,6))
    assert below.required_holdout_count is None
    assert below.status == floor.status


def test_swapping_endpoint_errors_leaves_count_threshold_and_value_invariant():
    targets = (F(49,100), F(8,25), F(3,10), F(1,4), F(1,5))
    for A in targets:
        right = req(A, eu=F(1,50), ev=F(2,25))
        left = req(A, eu=F(2,25), ev=F(1,50))
        assert left.required_holdout_count == right.required_holdout_count
        assert left.geometric_ratio_exact == right.geometric_ratio_exact
        assert left.power_threshold_exact == right.power_threshold_exact
        assert left.achieved_minimax_undetectable_amplitude_exact == right.achieved_minimax_undetectable_amplitude_exact
        assert left.endpoint_swap_count_invariant and right.endpoint_swap_count_invariant


def test_equal_endpoint_errors_reduce_exactly_to_uniform_count_inversion():
    rng = random.Random(202609082)
    for _ in range(100):
        L = F(rng.randrange(4, 30), 10)
        ee = F(rng.randrange(0, 5), 100)
        eh = F(rng.randrange(0, 5), 100)
        B = 2*(ee+eh)
        if B >= L/2:
            continue
        floor = B
        A = floor + (L/2-floor)*F(rng.randrange(1, 10), 10)
        asym = required_asymmetric_holdout_count_for_amplitude(
            A, residual_lipschitz_bound=L,
            endpoint_u_error_halfwidth=ee,
            endpoint_v_error_halfwidth=ee,
            interior_error_halfwidth=eh)
        uniform = required_holdout_count_for_amplitude(
            A, residual_lipschitz_bound=L,
            endpoint_error_halfwidth=ee,
            interior_error_halfwidth=eh)
        assert asym.required_holdout_count == uniform.required_holdout_count
        assert asym.achieved_minimax_undetectable_amplitude_exact == uniform.achieved_minimax_undetectable_amplitude_exact
        assert asym.status == uniform.status


def test_seeded_targets_between_successive_minimax_values_return_next_count():
    rng = random.Random(202609083)
    checked = 0
    while checked < 100:
        L = F(rng.randrange(8, 30), 10)
        eu = F(rng.randrange(0, 8), 100)
        ev = F(rng.randrange(0, 8), 100)
        eh = F(rng.randrange(0, 4), 100)
        if eu == ev or 2*eh+eu+ev >= L/2:
            continue
        k = rng.randrange(1, 8)
        uk = F(design_asymmetric_endpoint_lipschitz_detection(
            k, residual_lipschitz_bound=L,
            endpoint_u_error_halfwidth=eu,
            endpoint_v_error_halfwidth=ev,
            interior_error_halfwidth=eh).minimax_undetectable_amplitude_exact)
        uk1 = F(design_asymmetric_endpoint_lipschitz_detection(
            k+1, residual_lipschitz_bound=L,
            endpoint_u_error_halfwidth=eu,
            endpoint_v_error_halfwidth=ev,
            interior_error_halfwidth=eh).minimax_undetectable_amplitude_exact)
        A = (uk+uk1)/2
        r = required_asymmetric_holdout_count_for_amplitude(
            A, residual_lipschitz_bound=L,
            endpoint_u_error_halfwidth=eu,
            endpoint_v_error_halfwidth=ev,
            interior_error_halfwidth=eh)
        assert r.required_holdout_count == k+1
        assert F(r.achieved_minimax_undetectable_amplitude_exact) == uk1
        checked += 1


def test_exact_U_k_boundary_returns_k_plus_one_for_many_k():
    args = dict(
        residual_lipschitz_bound=1,
        endpoint_u_error_halfwidth=F(1,50),
        endpoint_v_error_halfwidth=F(2,25),
        interior_error_halfwidth=F(1,50),
    )
    for k in range(1, 15):
        A = F(design_asymmetric_endpoint_lipschitz_detection(
            k, **args).minimax_undetectable_amplitude_exact)
        r = required_asymmetric_holdout_count_for_amplitude(A, **args)
        assert r.required_holdout_count == k+1


def test_noise_dominated_regime_and_impossible_target_are_explicit():
    noisy = required_asymmetric_holdout_count_for_amplitude(
        F(2,5), residual_lipschitz_bound=1,
        endpoint_u_error_halfwidth=F(1,10),
        endpoint_v_error_halfwidth=F(3,10),
        interior_error_halfwidth=F(1,10))
    assert noisy.required_holdout_count is None
    assert noisy.irreducible_detection_floor_exact == "1/2"
    assert noisy.status == "no_finite_holdout_count_can_improve_noise_dominated_endpoint_ceiling"

    impossible = req(F(3,5))
    assert impossible.required_holdout_count is None
    assert impossible.status == "target_amplitude_not_attainable_in_declared_endpoint_zero_Lipschitz_class"


@pytest.mark.parametrize("kwargs", [
    dict(target_sup_residual_amplitude=0, residual_lipschitz_bound=1,
         endpoint_u_error_halfwidth=0, endpoint_v_error_halfwidth=0,
         interior_error_halfwidth=0),
    dict(target_sup_residual_amplitude=F(1,4), residual_lipschitz_bound=-1,
         endpoint_u_error_halfwidth=0, endpoint_v_error_halfwidth=0,
         interior_error_halfwidth=0),
    dict(target_sup_residual_amplitude=F(1,4), residual_lipschitz_bound=1,
         endpoint_u_error_halfwidth=-1, endpoint_v_error_halfwidth=0,
         interior_error_halfwidth=0),
    dict(target_sup_residual_amplitude=F(1,4), residual_lipschitz_bound=1,
         endpoint_u_error_halfwidth=0, endpoint_v_error_halfwidth=True,
         interior_error_halfwidth=0),
])
def test_invalid_inputs_rejected(kwargs):
    with pytest.raises(ValueError):
        required_asymmetric_holdout_count_for_amplitude(**kwargs)
