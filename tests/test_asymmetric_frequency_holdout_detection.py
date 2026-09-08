from fractions import Fraction as F
import random

import pytest

from src.asymmetric_frequency_holdout_detection import (
    design_asymmetric_endpoint_lipschitz_detection,
)
from src.frequency_holdout_detection import (
    comparison_nondetection_threshold,
    design_uniform_error_lipschitz_detection,
    worst_undetectable_lipschitz_amplitude,
)


def test_single_holdout_is_midpoint_even_with_asymmetric_endpoint_errors():
    r = design_asymmetric_endpoint_lipschitz_detection(
        1, residual_lipschitz_bound=1,
        endpoint_u_error_halfwidth=F(1,50),
        endpoint_v_error_halfwidth=F(2,25),
        interior_error_halfwidth=F(1,50),
    )
    assert r.midpoint_nondetection_threshold_exact == "7/50"
    assert r.signed_threshold_slope_exact == "3/25"
    assert r.recommended_frequencies_exact == ("1/2",)
    assert r.minimax_undetectable_amplitude_exact == "8/25"
    assert r.irreducible_detection_floor_exact == "5/28"
    assert r.centroid_shift_from_half_exact == "0"
    assert r.shift_direction == "midpoint_invariant"
    assert r.single_holdout_midpoint_invariant


def test_two_point_right_noisier_design_has_exact_shift_and_oracle_value():
    r = design_asymmetric_endpoint_lipschitz_detection(
        2, residual_lipschitz_bound=1,
        endpoint_u_error_halfwidth=F(1,50),
        endpoint_v_error_halfwidth=F(2,25),
        interior_error_halfwidth=F(1,50),
    )
    assert r.recommended_frequencies_exact == ("62/157", "199/314")
    assert r.minimax_undetectable_amplitude_exact == "41/157"
    assert F(r.centroid_shift_from_half_exact) > 0
    assert r.shift_direction == "toward_noisier_p1_v_endpoint"

    ps = tuple(map(F, r.recommended_frequencies_exact))
    bs = tuple(comparison_nondetection_threshold(
        p, endpoint_u_error_halfwidth=F(1,50),
        endpoint_v_error_halfwidth=F(2,25),
        interior_error_halfwidth=F(1,50)) for p in ps)
    assert worst_undetectable_lipschitz_amplitude(
        ps, bs, residual_lipschitz_bound=1) == F(41,157)


def test_swapping_endpoint_precisions_reflects_design_without_changing_minimax_value():
    for m in range(1, 8):
        right = design_asymmetric_endpoint_lipschitz_detection(
            m, residual_lipschitz_bound=1,
            endpoint_u_error_halfwidth=F(1,50),
            endpoint_v_error_halfwidth=F(2,25),
            interior_error_halfwidth=F(1,50))
        left = design_asymmetric_endpoint_lipschitz_detection(
            m, residual_lipschitz_bound=1,
            endpoint_u_error_halfwidth=F(2,25),
            endpoint_v_error_halfwidth=F(1,50),
            interior_error_halfwidth=F(1,50))
        rp = tuple(map(F, right.recommended_frequencies_exact))
        lp = tuple(map(F, left.recommended_frequencies_exact))
        assert lp == tuple(1-p for p in reversed(rp))
        assert left.minimax_undetectable_amplitude_exact == right.minimax_undetectable_amplitude_exact
        assert left.irreducible_detection_floor_exact == right.irreducible_detection_floor_exact
        assert F(left.centroid_shift_from_half_exact) == -F(right.centroid_shift_from_half_exact)


def test_equal_endpoint_errors_reduce_exactly_to_uniform_error_theorem():
    for m in range(1, 10):
        asym = design_asymmetric_endpoint_lipschitz_detection(
            m, residual_lipschitz_bound=F(7,5),
            endpoint_u_error_halfwidth=F(1,20),
            endpoint_v_error_halfwidth=F(1,20),
            interior_error_halfwidth=F(1,40))
        uniform = design_uniform_error_lipschitz_detection(
            m, residual_lipschitz_bound=F(7,5),
            endpoint_error_halfwidth=F(1,20),
            interior_error_halfwidth=F(1,40))
        assert asym.recommended_frequencies_exact == uniform.recommended_frequencies_exact
        assert asym.minimax_undetectable_amplitude_exact == uniform.minimax_undetectable_amplitude_exact
        assert asym.irreducible_detection_floor_exact == uniform.irreducible_detection_floor_exact
        assert asym.shift_direction == "symmetric_endpoint_precision"


def test_closed_form_asymmetric_design_matches_general_exact_oracle_seeded():
    rng = random.Random(202609081)
    checked = 0
    while checked < 180:
        m = rng.randrange(1, 8)
        L = F(rng.randrange(5, 30), 10)
        eu = F(rng.randrange(0, 10), 100)
        ev = F(rng.randrange(0, 10), 100)
        eh = F(rng.randrange(0, 5), 100)
        if 2*eh+eu+ev >= L/2:
            continue
        r = design_asymmetric_endpoint_lipschitz_detection(
            m, residual_lipschitz_bound=L,
            endpoint_u_error_halfwidth=eu,
            endpoint_v_error_halfwidth=ev,
            interior_error_halfwidth=eh)
        ps = tuple(map(F, r.recommended_frequencies_exact))
        bs = tuple(comparison_nondetection_threshold(
            p, endpoint_u_error_halfwidth=eu, endpoint_v_error_halfwidth=ev,
            interior_error_halfwidth=eh) for p in ps)
        got = worst_undetectable_lipschitz_amplitude(
            ps, bs, residual_lipschitz_bound=L)
        assert got == F(r.minimax_undetectable_amplitude_exact)
        if m == 1:
            assert ps == (F(1,2),)
        elif ev > eu:
            assert F(r.centroid_shift_from_half_exact) > 0
        elif eu > ev:
            assert F(r.centroid_shift_from_half_exact) < 0
        checked += 1


def test_infinite_density_floor_is_below_every_finite_informative_design_and_approached():
    args = dict(
        residual_lipschitz_bound=1,
        endpoint_u_error_halfwidth=F(1,50),
        endpoint_v_error_halfwidth=F(2,25),
        interior_error_halfwidth=F(1,50),
    )
    small = design_asymmetric_endpoint_lipschitz_detection(2, **args)
    large = design_asymmetric_endpoint_lipschitz_detection(80, **args)
    floor = F(small.irreducible_detection_floor_exact)
    assert F(small.minimax_undetectable_amplitude_exact) > F(large.minimax_undetectable_amplitude_exact) > floor
    assert F(large.minimax_undetectable_amplitude_exact)-floor < F(1,10**6)


def test_noise_dominated_midpoint_threshold_makes_all_finite_designs_non_improving():
    # B_mid=2eh+eu+ev=3/5 >= L/2.
    for m in (1, 2, 6):
        r = design_asymmetric_endpoint_lipschitz_detection(
            m, residual_lipschitz_bound=1,
            endpoint_u_error_halfwidth=F(1,10),
            endpoint_v_error_halfwidth=F(3,10),
            interior_error_halfwidth=F(1,10))
        assert r.midpoint_nondetection_threshold_exact == "3/5"
        assert r.minimax_undetectable_amplitude_exact == "1/2"
        assert r.irreducible_detection_floor_exact == "1/2"
        assert not r.holdouts_improve_minimax_guarantee
        assert not r.design_unique
        assert r.shift_direction == "no_unique_shift_noise_dominated"


@pytest.mark.parametrize("kwargs", [
    dict(residual_lipschitz_bound=-1, endpoint_u_error_halfwidth=0,
         endpoint_v_error_halfwidth=0, interior_error_halfwidth=0),
    dict(residual_lipschitz_bound=1, endpoint_u_error_halfwidth=-1,
         endpoint_v_error_halfwidth=0, interior_error_halfwidth=0),
    dict(residual_lipschitz_bound=1, endpoint_u_error_halfwidth=0,
         endpoint_v_error_halfwidth=True, interior_error_halfwidth=0),
    dict(residual_lipschitz_bound=1, endpoint_u_error_halfwidth=0,
         endpoint_v_error_halfwidth=0, interior_error_halfwidth=-1),
])
def test_invalid_asymmetric_inputs_rejected(kwargs):
    with pytest.raises(ValueError):
        design_asymmetric_endpoint_lipschitz_detection(2, **kwargs)
