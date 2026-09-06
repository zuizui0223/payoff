from math import isclose

from src.edgewise_modularity import edge_pressures, optimized_loss
from src.modularization_barrier import (
    classify_linear_decoupling_cost,
    generic_decoupling_thresholds,
    two_function_classify_cost,
    two_function_release_thresholds,
)


def test_generic_threshold_classification():
    local, global_threshold = generic_decoupling_thresholds(0.2, 0.6, 2.0)
    assert isclose(local, 0.2)
    assert isclose(global_threshold, 0.3)
    assert classify_linear_decoupling_cost(0.1, local, global_threshold) == "locally_accessible_release"
    assert classify_linear_decoupling_cost(0.25, local, global_threshold) == "finite_jump_barrier"
    assert classify_linear_decoupling_cost(0.4, local, global_threshold) == "retained_coupling"


def test_two_function_closed_form_matches_edgewise_model():
    a, b = 2.0, 3.0
    theta1, theta2 = 0.0, 2.5
    gap = theta1 - theta2
    c0 = 1.4
    summary = two_function_release_thresholds(a, b, gap, c0)

    optima = [theta1, theta2]
    weights = [a, b]
    edges = [(0, 1)]
    couplings = [c0]

    pressure = edge_pressures(optima, weights, edges, couplings)[0]
    assert isclose(pressure, summary["local_threshold"], rel_tol=1e-12, abs_tol=1e-12)

    reference_loss = optimized_loss(optima, weights, edges, couplings)
    released_loss = optimized_loss(optima, weights, edges, [0.0])
    global_threshold = (reference_loss - released_loss) / c0
    assert isclose(global_threshold, summary["global_threshold"], rel_tol=1e-12, abs_tol=1e-12)


def test_two_function_barrier_width_identity():
    summary = two_function_release_thresholds(
        a=2.0,
        b=3.0,
        theta_gap=2.0,
        reference_coupling=1.0,
    )
    s = summary["separation_fraction"]
    expected = s * (1.0 - s) * 4.0
    assert isclose(summary["barrier_width"], expected, rel_tol=1e-12, abs_tol=1e-12)
    assert isclose(summary["threshold_ratio"], 1.0 / s, rel_tol=1e-12, abs_tol=1e-12)


def test_intermediate_cost_is_global_but_not_locally_accessible():
    summary = two_function_release_thresholds(
        a=1.0,
        b=1.0,
        theta_gap=2.0,
        reference_coupling=1.0,
    )
    local = summary["local_threshold"]
    global_threshold = summary["global_threshold"]
    assert local < global_threshold
    cost = 0.5 * (local + global_threshold)
    assert (
        two_function_classify_cost(1.0, 1.0, 2.0, 1.0, cost)
        == "finite_jump_barrier"
    )


def test_barrier_width_maximum_as_function_of_separation_fraction():
    gap2 = 9.0
    # Algebraic check of s(1-s) Delta^2 peak at s=1/2.
    center = 0.5 * (1.0 - 0.5) * gap2
    for s in [0.1, 0.25, 0.4, 0.6, 0.75, 0.9]:
        assert center >= s * (1.0 - s) * gap2 - 1e-12
    assert isclose(center, gap2 / 4.0)
