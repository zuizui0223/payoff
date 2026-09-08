from fractions import Fraction as F
import random

import pytest

from src.endpoint_precision_allocation import compare_endpoint_precision_balance


def test_one_holdout_is_exactly_asymmetry_invariant_at_fixed_error_sum():
    for eu, ev in [(F(0), F(1,10)), (F(1,50), F(2,25)), (F(1,20), F(1,20))]:
        r = compare_endpoint_precision_balance(
            1, residual_lipschitz_bound=1,
            endpoint_u_error_halfwidth=eu,
            endpoint_v_error_halfwidth=ev,
            interior_error_halfwidth=F(1,50))
        assert r.asymmetry_penalty_exact == "0"
        assert not r.balancing_strictly_improves_finite_design
        assert r.one_holdout_asymmetry_invariant


def test_registered_asymmetry_has_positive_m2_penalty_and_dense_floor_penalty():
    r = compare_endpoint_precision_balance(
        2, residual_lipschitz_bound=1,
        endpoint_u_error_halfwidth=F(1,50),
        endpoint_v_error_halfwidth=F(2,25),
        interior_error_halfwidth=F(1,50))
    # Same total endpoint error gives balanced e_u=e_v=1/20 and B=7/50.
    assert r.balanced_endpoint_error_halfwidth_exact == "1/20"
    assert r.midpoint_nondetection_threshold_exact == "7/50"
    assert r.endpoint_asymmetry_exact == "3/25"
    assert r.actual_minimax_undetectable_amplitude_exact == "41/157"
    assert r.balanced_counterfactual_minimax_amplitude_exact == "13/50"
    assert F(r.asymmetry_penalty_exact) > 0
    assert r.actual_dense_error_floor_exact == "5/28"
    assert r.balanced_dense_error_floor_exact == "7/50"
    assert F(r.dense_floor_asymmetry_penalty_exact) > 0
    assert r.balancing_strictly_improves_finite_design
    assert r.balancing_strictly_improves_dense_floor
    assert r.balanced_precision_is_unique_minimizer


def test_swapping_endpoint_errors_preserves_penalties():
    for m in range(1, 9):
        a = compare_endpoint_precision_balance(
            m, residual_lipschitz_bound=F(6,5),
            endpoint_u_error_halfwidth=F(1,100),
            endpoint_v_error_halfwidth=F(9,100),
            interior_error_halfwidth=F(1,50))
        b = compare_endpoint_precision_balance(
            m, residual_lipschitz_bound=F(6,5),
            endpoint_u_error_halfwidth=F(9,100),
            endpoint_v_error_halfwidth=F(1,100),
            interior_error_halfwidth=F(1,50))
        assert a.actual_minimax_undetectable_amplitude_exact == b.actual_minimax_undetectable_amplitude_exact
        assert a.asymmetry_penalty_exact == b.asymmetry_penalty_exact
        assert a.actual_dense_error_floor_exact == b.actual_dense_error_floor_exact
        assert a.dense_floor_asymmetry_penalty_exact == b.dense_floor_asymmetry_penalty_exact


def test_balanced_endpoint_errors_have_zero_penalty_for_every_m():
    for m in range(1, 12):
        r = compare_endpoint_precision_balance(
            m, residual_lipschitz_bound=1,
            endpoint_u_error_halfwidth=F(1,20),
            endpoint_v_error_halfwidth=F(1,20),
            interior_error_halfwidth=F(1,40))
        assert r.endpoint_asymmetry_exact == "0"
        assert r.asymmetry_penalty_exact == "0"
        assert r.dense_floor_asymmetry_penalty_exact == "0"
        assert not r.balancing_strictly_improves_finite_design
        assert not r.balancing_strictly_improves_dense_floor
        assert r.balanced_precision_is_unique_minimizer == (m >= 2)


def test_fixed_sum_grid_has_unique_balanced_minimum_for_m_at_least_two():
    S = F(1,10)
    for m in (2, 3, 5, 9):
        rows = []
        for k in range(11):
            eu = S*F(k,10)
            ev = S-eu
            r = compare_endpoint_precision_balance(
                m, residual_lipschitz_bound=1,
                endpoint_u_error_halfwidth=eu,
                endpoint_v_error_halfwidth=ev,
                interior_error_halfwidth=F(1,50))
            rows.append((F(r.actual_minimax_undetectable_amplitude_exact), eu))
        best = min(v for v, _ in rows)
        winners = [eu for v, eu in rows if v == best]
        assert winners == [S/2]


def test_seeded_informative_asymmetry_never_beats_same_sum_balance():
    rng = random.Random(202609084)
    checked = 0
    while checked < 180:
        L = F(rng.randrange(6, 30), 10)
        eu = F(rng.randrange(0, 10), 100)
        ev = F(rng.randrange(0, 10), 100)
        eh = F(rng.randrange(0, 5), 100)
        if eu == ev or 2*eh+eu+ev >= L/2:
            continue
        m = rng.randrange(2, 9)
        r = compare_endpoint_precision_balance(
            m, residual_lipschitz_bound=L,
            endpoint_u_error_halfwidth=eu,
            endpoint_v_error_halfwidth=ev,
            interior_error_halfwidth=eh)
        assert F(r.asymmetry_penalty_exact) > 0
        assert F(r.dense_floor_asymmetry_penalty_exact) > 0
        checked += 1


def test_noise_dominated_regime_has_no_precision_balance_advantage():
    for m in (1, 2, 7):
        r = compare_endpoint_precision_balance(
            m, residual_lipschitz_bound=1,
            endpoint_u_error_halfwidth=F(1,10),
            endpoint_v_error_halfwidth=F(3,10),
            interior_error_halfwidth=F(1,10))
        assert r.noise_dominated
        assert r.actual_minimax_undetectable_amplitude_exact == "1/2"
        assert r.balanced_counterfactual_minimax_amplitude_exact == "1/2"
        assert r.asymmetry_penalty_exact == "0"
        assert r.dense_floor_asymmetry_penalty_exact == "0"
        assert not r.balanced_precision_is_unique_minimizer


def test_receipt_refuses_to_call_error_balance_a_replication_allocation():
    r = compare_endpoint_precision_balance(
        3, residual_lipschitz_bound=1,
        endpoint_u_error_halfwidth=F(1,50),
        endpoint_v_error_halfwidth=F(2,25),
        interior_error_halfwidth=F(1,50))
    assert not r.statistical_power_computed
    assert not r.biological_replication_allocation_identified


@pytest.mark.parametrize("kwargs", [
    dict(residual_lipschitz_bound=-1, endpoint_u_error_halfwidth=0,
         endpoint_v_error_halfwidth=0, interior_error_halfwidth=0),
    dict(residual_lipschitz_bound=1, endpoint_u_error_halfwidth=-1,
         endpoint_v_error_halfwidth=0, interior_error_halfwidth=0),
    dict(residual_lipschitz_bound=1, endpoint_u_error_halfwidth=0,
         endpoint_v_error_halfwidth=True, interior_error_halfwidth=0),
])
def test_invalid_inputs_rejected(kwargs):
    with pytest.raises(ValueError):
        compare_endpoint_precision_balance(2, **kwargs)
