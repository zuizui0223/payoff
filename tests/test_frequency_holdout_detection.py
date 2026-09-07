from fractions import Fraction as F
import random

import pytest

from src.frequency_holdout_detection import (
    comparison_nondetection_threshold,
    design_uniform_error_lipschitz_detection,
    required_holdout_count_for_amplitude,
    signed_curvature_midpoint_detection,
    worst_undetectable_lipschitz_amplitude,
)


def test_one_point_closed_band_threshold_has_exact_factor_two():
    # p=1/4, endpoint errors 1/10 and 1/5, interior error 1/20.
    p = F(1, 4)
    got = comparison_nondetection_threshold(
        p, endpoint_u_error_halfwidth=F(1,10),
        endpoint_v_error_halfwidth=F(1,5), interior_error_halfwidth=F(1,20))
    expected = 2*(F(1,20)+F(3,4)*F(1,10)+F(1,4)*F(1,5))
    assert got == expected == F(7,20)


def test_endpoint_only_lipschitz_envelope_is_L_over_two():
    assert worst_undetectable_lipschitz_amplitude(
        (), (), residual_lipschitz_bound=F(7,5)) == F(7,10)


def test_general_envelope_formula_bounds_dense_grid_and_is_attained_at_candidate():
    ps = (F(1,5), F(3,5), F(4,5))
    bs = (F(1,10), F(1,4), F(1,20))
    L = F(3,2)
    exact = worst_undetectable_lipschitz_amplitude(ps, bs, residual_lipschitz_bound=L)
    anchors = ((F(0), F(0)),) + tuple(zip(ps, bs)) + ((F(1), F(0)),)
    def env(p):
        return min(b+L*abs(p-x) for x,b in anchors)
    grid = [F(i, 4000) for i in range(4001)]
    brute = max(env(p) for p in grid)
    assert brute <= exact
    assert exact-brute <= L/F(8000)


def test_zero_error_reduces_exactly_to_previous_equal_spacing_law():
    for m in range(1, 12):
        r = design_uniform_error_lipschitz_detection(
            m, residual_lipschitz_bound=1,
            endpoint_error_halfwidth=0, interior_error_halfwidth=0)
        assert r.recommended_frequencies_exact == tuple(
            str(F(i,m+1)) for i in range(1,m+1))
        assert r.minimax_undetectable_amplitude_exact == str(F(1,2*(m+1)))
        assert r.irducible_detection_floor_exact if False else True
        assert r.irreducible_detection_floor_exact == "0"
        assert r.holdouts_improve_minimax_guarantee
        assert r.design_unique


def test_nonzero_uniform_error_pulls_optimal_points_inward():
    # L=1 and B=2(e_endpoint+e_holdout)=1/5.
    r = design_uniform_error_lipschitz_detection(
        2, residual_lipschitz_bound=1,
        endpoint_error_halfwidth=F(1,40), interior_error_halfwidth=F(3,40))
    assert r.sample_nondetection_threshold_exact == "1/5"
    assert r.recommended_frequencies_exact == ("2/5", "3/5")
    assert r.minimax_undetectable_amplitude_exact == "3/10"
    # Naive equal spacing is strictly worse once the sample bands have this floor.
    equal = worst_undetectable_lipschitz_amplitude(
        (F(1,3),F(2,3)), (F(1,5),F(1,5)), residual_lipschitz_bound=1)
    assert equal == F(11,30) > F(3,10)


def test_closed_form_noisy_design_matches_general_exact_oracle_randomly():
    rng = random.Random(202609077)
    for _ in range(100):
        m = rng.randrange(1, 8)
        L = F(rng.randrange(2, 20), 10)
        # Pick B strictly below L/2, then split B/2 into endpoint+holdout errors.
        B = L*F(rng.randrange(0, 9), 20)
        total_half = B/2
        ee = total_half*F(rng.randrange(0, 11), 10)
        eh = total_half-ee
        r = design_uniform_error_lipschitz_detection(
            m, residual_lipschitz_bound=L,
            endpoint_error_halfwidth=ee, interior_error_halfwidth=eh)
        ps = tuple(map(F, r.recommended_frequencies_exact))
        got = worst_undetectable_lipschitz_amplitude(
            ps, (B,)*m, residual_lipschitz_bound=L)
        assert got == F(r.minimax_undetectable_amplitude_exact)
        assert got == B+(L/2-B)/F(m+1)


def test_noise_dominated_regime_has_no_minimax_improvement():
    # L/2=1/2 and B=3/5, so endpoint smoothness alone is tighter than samples.
    for m in (1, 2, 5):
        r = design_uniform_error_lipschitz_detection(
            m, residual_lipschitz_bound=1,
            endpoint_error_halfwidth=F(1,10), interior_error_halfwidth=F(1,5))
        assert r.sample_nondetection_threshold_exact == "3/5"
        assert r.minimax_undetectable_amplitude_exact == "1/2"
        assert r.irreducible_detection_floor_exact == "1/2"
        assert not r.holdouts_improve_minimax_guarantee
        assert not r.design_unique


def test_required_count_respects_strict_closed_band_boundary():
    # L=1, B=1/5, target A=3/10. m=2 gives U exactly 3/10, which is NOT
    # enough because contact is compatible. m=3 gives 11/40 < 3/10.
    r = required_holdout_count_for_amplitude(
        F(3,10), residual_lipschitz_bound=1,
        endpoint_error_halfwidth=F(1,40), interior_error_halfwidth=F(3,40))
    assert r.required_holdout_count == 3
    assert r.achieved_minimax_undetectable_amplitude_exact == "11/40"
    assert r.strict_boundary
    assert not r.statistical_power_computed
    assert not r.sample_size_recommendation


def test_required_count_stays_constant_memory_for_large_answer():
    # Exact zero-error inversion: U_m=1/[2(m+1)]. A=1/1000001 requires
    # m=500000 because m=499999 gives 1/1000000, still above the target.
    r = required_holdout_count_for_amplitude(
        F(1,1000001), residual_lipschitz_bound=1,
        endpoint_error_halfwidth=0, interior_error_halfwidth=0)
    assert r.required_holdout_count == 500000
    assert r.achieved_minimax_undetectable_amplitude_exact == "1/1000002"


def test_required_count_refuses_below_noise_floor_and_impossible_amplitude():
    floor = required_holdout_count_for_amplitude(
        F(1,5), residual_lipschitz_bound=1,
        endpoint_error_halfwidth=F(1,40), interior_error_halfwidth=F(3,40))
    assert floor.required_holdout_count is None
    assert floor.status == "no_finite_holdout_count_can_guarantee_detection_at_declared_error_floor"
    impossible = required_holdout_count_for_amplitude(
        F(3,5), residual_lipschitz_bound=1,
        endpoint_error_halfwidth=0, interior_error_halfwidth=0)
    assert impossible.required_holdout_count is None
    assert impossible.status == "target_amplitude_not_attainable_in_declared_endpoint_zero_Lipschitz_class"


def test_signed_curvature_error_threshold_is_strict_and_exact():
    # eu=ev=eh=1/100 => midpoint W=1/50, nondetection threshold Bmid=1/25.
    boundary = signed_curvature_midpoint_detection(
        F(8,25), endpoint_u_error_halfwidth=F(1,100),
        endpoint_v_error_halfwidth=F(1,100), interior_error_halfwidth=F(1,100))
    assert boundary.midpoint_nondetection_threshold_exact == "1/25"
    assert boundary.midpoint_guaranteed_departure_exact == "1/25"
    assert boundary.critical_curvature_excluded_boundary_exact == "8/25"
    assert not boundary.guaranteed_midpoint_rejection
    above = signed_curvature_midpoint_detection(
        F(33,100), endpoint_u_error_halfwidth=F(1,100),
        endpoint_v_error_halfwidth=F(1,100), interior_error_halfwidth=F(1,100))
    assert above.guaranteed_midpoint_rejection


@pytest.mark.parametrize("kwargs", [
    {"residual_lipschitz_bound": -1, "endpoint_error_halfwidth": 0, "interior_error_halfwidth": 0},
    {"residual_lipschitz_bound": 1, "endpoint_error_halfwidth": -1, "interior_error_halfwidth": 0},
    {"residual_lipschitz_bound": 1, "endpoint_error_halfwidth": 0, "interior_error_halfwidth": True},
])
def test_invalid_uniform_design_inputs_rejected(kwargs):
    with pytest.raises(ValueError):
        design_uniform_error_lipschitz_detection(2, **kwargs)


@pytest.mark.parametrize("target", [0, -1, True, "nan", float("nan")])
def test_invalid_target_amplitudes_rejected(target):
    with pytest.raises(ValueError):
        required_holdout_count_for_amplitude(
            target, residual_lipschitz_bound=1,
            endpoint_error_halfwidth=0, interior_error_halfwidth=0)
