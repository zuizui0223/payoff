from fractions import Fraction as F
from itertools import combinations

import pytest

from src.frequency_holdout_design import (
    covering_radius,
    design_lipschitz_holdouts,
    design_one_point_for_signed_curvature,
)


def test_equal_spacing_exact_designs_match_expected_small_cases():
    assert design_lipschitz_holdouts(1).optimal_frequencies_exact == ("1/2",)
    assert design_lipschitz_holdouts(2).optimal_frequencies_exact == ("1/3", "2/3")
    assert design_lipschitz_holdouts(3).optimal_frequencies_exact == ("1/4", "1/2", "3/4")
    assert design_lipschitz_holdouts(3).minimax_covering_radius_exact == "1/8"
    assert design_lipschitz_holdouts(3).maximum_gap_exact == "1/4"


def test_lipschitz_envelope_scales_exactly_with_bound():
    r = design_lipschitz_holdouts(3, residual_lipschitz_bound=F(2, 5))
    assert r.worst_unsampled_residual_envelope_exact == "1/20"
    assert not r.holdout_outcomes_used_for_design
    assert not r.arbitrary_nonlinearity_identified


def test_equal_spacing_attains_formula_for_many_counts():
    for m in range(1, 30):
        r = design_lipschitz_holdouts(m)
        ps = tuple(map(F, r.optimal_frequencies_exact))
        assert covering_radius(ps) == F(1, 2*(m+1))


def test_grid_enumeration_finds_no_better_design_for_small_m():
    # Independent finite-grid oracle. The theorem is continuous; this only checks
    # that exact designs beat every candidate on dense rational grids containing them.
    for m, denominator in [(1, 12), (2, 12), (3, 12)]:
        optimal = F(1, 2*(m+1))
        grid = [F(i, denominator) for i in range(1, denominator)]
        best = min(covering_radius(c) for c in combinations(grid, m))
        assert best == optimal


def test_perturbing_equal_spacing_increases_covering_radius():
    base = (F(1,4), F(1,2), F(3,4))
    assert covering_radius(base) == F(1,8)
    for perturbed in [
        (F(1,5), F(1,2), F(3,4)),
        (F(1,4), F(9,20), F(3,4)),
        (F(1,4), F(1,2), F(4,5)),
    ]:
        assert covering_radius(perturbed) > F(1,8)


def test_midpoint_maximizes_uniform_signed_curvature_guarantee():
    r = design_one_point_for_signed_curvature(F(3, 2))
    assert r.optimal_frequency_exact == "1/2"
    assert r.guaranteed_departure_at_optimum_exact == "3/16"
    # Direct exact comparison of kappa*p*(1-p)/2 over a fine rational grid.
    kappa = F(3,2)
    values = [(p, kappa*p*(1-p)/2) for p in (F(i,100) for i in range(1,100))]
    assert max(y for _, y in values) == F(3,16)
    assert [p for p, y in values if y == F(3,16)] == [F(1,2)]


def test_zero_curvature_bound_is_valid_but_has_no_detection_margin():
    r = design_one_point_for_signed_curvature(0)
    assert r.guaranteed_departure_at_optimum_exact == "0"


@pytest.mark.parametrize("count", [0, -1, True, 1.5])
def test_bad_counts_rejected(count):
    with pytest.raises(ValueError):
        design_lipschitz_holdouts(count)


@pytest.mark.parametrize("value", [-1, "-1/3", True, "nan", float("nan")])
def test_bad_bounds_rejected(value):
    with pytest.raises(ValueError):
        design_lipschitz_holdouts(1, residual_lipschitz_bound=value)
    with pytest.raises(ValueError):
        design_one_point_for_signed_curvature(value)


@pytest.mark.parametrize("points", [
    (), (0,), (1,), (F(1,2), F(1,2)), (F(3,4), F(1,4)), (True,),
])
def test_invalid_design_points_rejected(points):
    with pytest.raises((ValueError, TypeError)):
        covering_radius(points)
