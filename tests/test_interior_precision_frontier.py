from fractions import Fraction as F
import random

import pytest

from src.asymmetric_frequency_holdout_detection import (
    design_asymmetric_endpoint_lipschitz_detection,
)
from src.interior_precision_frontier import required_interior_precision_for_amplitude


def frontier(m, A, *, L=1, eu=F(1,50), ev=F(2,25)):
    return required_interior_precision_for_amplitude(
        m, A, residual_lipschitz_bound=L,
        endpoint_u_error_halfwidth=eu,
        endpoint_v_error_halfwidth=ev,
    )


def test_registered_asymmetric_m2_target_has_exact_precision_frontier():
    r = frontier(2, F(3,10))
    assert r.endpoint_error_sum_exact == "1/10"
    assert r.endpoint_asymmetry_exact == "3/25"
    assert r.zero_interior_error_minimax_amplitude_exact == "221/942"
    assert r.critical_midpoint_nondetection_threshold_excluded_exact == "1241/6250"
    assert r.critical_interior_error_halfwidth_excluded_exact == "154/3125"
    assert r.status == "finite_strict_interior_precision_frontier_identified"
    assert r.boundary_is_excluded
    assert not r.statistical_power_computed
    assert not r.biological_replication_count_identified


def test_existing_eh_boundary_is_exactly_excluded_for_A_equal_current_U2():
    # At e_h=1/50 the registered asymmetric U_2 is 41/157.
    r = frontier(2, F(41,157))
    assert r.critical_interior_error_halfwidth_excluded_exact == "1/50"
    assert r.critical_midpoint_nondetection_threshold_excluded_exact == "7/50"

    at_boundary = design_asymmetric_endpoint_lipschitz_detection(
        2, residual_lipschitz_bound=1,
        endpoint_u_error_halfwidth=F(1,50),
        endpoint_v_error_halfwidth=F(2,25),
        interior_error_halfwidth=F(1,50))
    assert at_boundary.minimax_undetectable_amplitude_exact == "41/157"


def test_symmetric_limit_matches_simple_affine_inversion():
    r = frontier(2, F(3,10), eu=F(1,20), ev=F(1,20))
    # U_2=[2B+1/2]/3; U_2<3/10 iff B<1/5, hence e_h<(1/5-1/10)/2=1/20.
    assert r.endpoint_asymmetry_exact == "0"
    assert r.critical_midpoint_nondetection_threshold_excluded_exact == "1/5"
    assert r.critical_interior_error_halfwidth_excluded_exact == "1/20"


def test_fixed_total_endpoint_error_asymmetry_reduces_allowable_interior_error_for_m2():
    asym = frontier(2, F(3,10), eu=F(1,50), ev=F(2,25))
    bal = frontier(2, F(3,10), eu=F(1,20), ev=F(1,20))
    assert F(asym.endpoint_error_sum_exact) == F(bal.endpoint_error_sum_exact) == F(1,10)
    assert F(asym.critical_interior_error_halfwidth_excluded_exact) < F(
        bal.critical_interior_error_halfwidth_excluded_exact)


def test_zero_interior_error_boundary_still_has_no_guaranteed_nonnegative_precision():
    # Symmetric m=2, endpoints sum=1/10: U_2(e_h=0)=7/30.
    r = frontier(2, F(7,30), eu=F(1,20), ev=F(1,20))
    assert r.zero_interior_error_minimax_amplitude_exact == "7/30"
    assert r.critical_midpoint_nondetection_threshold_excluded_exact == "1/10"
    assert r.critical_interior_error_halfwidth_excluded_exact == "0"
    assert r.status == "no_nonnegative_interior_error_halfwidth_can_guarantee_target_for_fixed_count"


def test_target_below_zero_error_ceiling_has_no_nonnegative_solution():
    r = frontier(2, F(1,5), eu=F(1,20), ev=F(1,20))
    assert r.critical_interior_error_halfwidth_excluded_exact is None
    assert r.status == "no_nonnegative_interior_error_halfwidth_can_guarantee_target_for_fixed_count"


def test_endpoint_precision_alone_can_be_noise_dominated():
    r = frontier(3, F(2,5), eu=F(1,5), ev=F(3,10))
    assert r.endpoint_error_sum_exact == "1/2"
    assert r.zero_interior_error_minimax_amplitude_exact == "1/2"
    assert r.critical_interior_error_halfwidth_excluded_exact is None
    assert r.status == "endpoint_precision_alone_is_noise_dominated"


def test_target_outside_lipschitz_class_is_explicit():
    r = frontier(2, F(3,5))
    assert r.status == "target_amplitude_not_attainable_in_declared_endpoint_zero_Lipschitz_class"
    assert r.critical_interior_error_halfwidth_excluded_exact is None


def test_seeded_current_error_boundary_roundtrips_exactly():
    rng = random.Random(202609085)
    checked = 0
    while checked < 140:
        m = rng.randrange(1, 8)
        L = F(rng.randrange(8, 30), 10)
        eu = F(rng.randrange(0, 8), 100)
        ev = F(rng.randrange(0, 8), 100)
        eh = F(rng.randrange(1, 5), 100)
        if 2*eh+eu+ev >= L/2:
            continue
        d = design_asymmetric_endpoint_lipschitz_detection(
            m, residual_lipschitz_bound=L,
            endpoint_u_error_halfwidth=eu,
            endpoint_v_error_halfwidth=ev,
            interior_error_halfwidth=eh)
        A = F(d.minimax_undetectable_amplitude_exact)
        r = required_interior_precision_for_amplitude(
            m, A, residual_lipschitz_bound=L,
            endpoint_u_error_halfwidth=eu,
            endpoint_v_error_halfwidth=ev)
        assert r.status == "finite_strict_interior_precision_frontier_identified"
        assert F(r.critical_interior_error_halfwidth_excluded_exact) == eh
        checked += 1


def test_more_holdout_settings_relax_required_interior_precision_for_same_target():
    vals = []
    for m in (1, 2, 3, 5, 10):
        r = frontier(m, F(3,10))
        vals.append(F(r.critical_interior_error_halfwidth_excluded_exact))
    assert vals == sorted(vals)
    assert len(set(vals)) == len(vals)


@pytest.mark.parametrize("kwargs", [
    dict(holdout_count=0, target_sup_residual_amplitude=F(1,4), residual_lipschitz_bound=1,
         endpoint_u_error_halfwidth=0, endpoint_v_error_halfwidth=0),
    dict(holdout_count=2, target_sup_residual_amplitude=0, residual_lipschitz_bound=1,
         endpoint_u_error_halfwidth=0, endpoint_v_error_halfwidth=0),
    dict(holdout_count=2, target_sup_residual_amplitude=F(1,4), residual_lipschitz_bound=-1,
         endpoint_u_error_halfwidth=0, endpoint_v_error_halfwidth=0),
    dict(holdout_count=2, target_sup_residual_amplitude=F(1,4), residual_lipschitz_bound=1,
         endpoint_u_error_halfwidth=True, endpoint_v_error_halfwidth=0),
])
def test_invalid_inputs_rejected(kwargs):
    with pytest.raises(ValueError):
        required_interior_precision_for_amplitude(**kwargs)
