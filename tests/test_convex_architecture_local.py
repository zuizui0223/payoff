from math import isclose

from src.convex_architecture_local import (
    branching_threshold_gamma,
    convergence_rate_from_cost_curvature,
    local_branching_regime,
    mutant_fitness_curvature,
    selection_gradient_from_cost_slope,
    singular_condition_residual,
)


def test_general_selection_gradient_is_one_minus_cost_slope():
    assert isclose(selection_gradient_from_cost_slope(0.4), 0.6)
    assert isclose(selection_gradient_from_cost_slope(1.0), 0.0)
    assert isclose(selection_gradient_from_cost_slope(1.4), -0.4)
    assert isclose(singular_condition_residual(1.0), 0.0)


def test_general_branching_threshold_is_minus_half_cost_curvature():
    for curvature in [0.2, 1.0, 3.4]:
        assert isclose(branching_threshold_gamma(curvature), -0.5 * curvature)
        assert isclose(convergence_rate_from_cost_curvature(curvature), -curvature)


def test_local_branching_classification_matches_mutant_curvature():
    curvature = 1.6
    threshold = branching_threshold_gamma(curvature)
    assert local_branching_regime(curvature, threshold + 0.1) == "local_ess"
    assert local_branching_regime(curvature, threshold) == "second_order_neutral"
    assert local_branching_regime(curvature, threshold - 0.1) == "branching_compatible"

    assert mutant_fitness_curvature(curvature, threshold + 0.1) < 0.0
    assert isclose(mutant_fitness_curvature(curvature, threshold), 0.0, abs_tol=1e-12)
    assert mutant_fitness_curvature(curvature, threshold - 0.1) > 0.0
