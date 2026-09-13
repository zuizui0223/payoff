from itertools import product
from math import isclose, isfinite

from src.edgewise_modularity import (
    best_vertex_topology,
    edge_pressures,
    edge_release_receipt,
    enumerate_vertex_topologies,
    linear_system_condition_inf,
    net_gain_linear_cost,
    optimized_loss,
    optimized_phenotype,
    recovery_from_decoupling,
    recovery_gradient,
)


def example_problem():
    optima = [0.0, 1.2, 3.0]
    weights = [1.0, 2.0, 1.5]
    edges = [(0, 1), (1, 2), (0, 2)]
    couplings = [1.2, 0.8, 0.5]
    return optima, weights, edges, couplings


def test_optimized_phenotype_solves_a_sensible_compromise():
    optima, weights, edges, couplings = example_problem()
    x = optimized_phenotype(optima, weights, edges, couplings)
    assert len(x) == 3
    assert min(optima) <= min(x) <= max(x) <= max(optima)
    assert optimized_loss(optima, weights, edges, couplings) >= 0.0


def test_solver_is_invariant_to_common_problem_scale():
    optima, weights, edges, couplings = example_problem()
    expected = optimized_phenotype(optima, weights, edges, couplings)

    # The old absolute 1e-15 pivot threshold rejected the 1e-18 version even
    # though it is exactly the same optimization problem up to common scale.
    for scale in (1e-18, 1e18):
        observed = optimized_phenotype(
            optima,
            [scale * value for value in weights],
            edges,
            [scale * value for value in couplings],
        )
        assert all(
            isclose(value, target, rel_tol=2e-13, abs_tol=2e-13)
            for value, target in zip(observed, expected)
        )


def test_condition_number_is_scale_invariant_and_finite():
    optima, weights, edges, couplings = example_problem()
    expected = linear_system_condition_inf(optima, weights, edges, couplings)
    assert isfinite(expected)
    assert expected >= 1.0

    for scale in (1e-18, 1e18):
        observed = linear_system_condition_inf(
            optima,
            [scale * value for value in weights],
            edges,
            [scale * value for value in couplings],
        )
        assert isclose(observed, expected, rel_tol=2e-12, abs_tol=2e-12)


def test_best_vertex_receipt_records_condition_number():
    optima = [0.0, 1.0, 2.5]
    weights = [1.0, 1.0, 1.0]
    edges = [(0, 1), (1, 2)]
    reference = [1.0, 1.0]
    costs = [0.12, 0.3]
    best = best_vertex_topology(optima, weights, edges, reference, costs)
    condition = float(best["linear_system_condition_inf"])
    assert isfinite(condition)
    assert condition >= 1.0


def test_edge_pressure_matches_finite_difference_in_coupling():
    optima, weights, edges, couplings = example_problem()
    pressures = edge_pressures(optima, weights, edges, couplings)
    baseline = optimized_loss(optima, weights, edges, couplings)
    eps = 1e-6
    for edge_index, expected in enumerate(pressures):
        shifted = list(couplings)
        shifted[edge_index] += eps
        observed = (
            optimized_loss(optima, weights, edges, shifted) - baseline
        ) / eps
        assert isclose(observed, expected, rel_tol=2e-5, abs_tol=2e-6)


def test_recovery_gradient_matches_finite_difference_in_decoupling():
    optima, weights, edges, reference = example_problem()
    d = [0.2, 0.1, 0.05]
    gradient = recovery_gradient(optima, weights, edges, reference, d)
    baseline = recovery_from_decoupling(optima, weights, edges, reference, d)
    eps = 1e-6
    for edge_index, expected in enumerate(gradient):
        shifted = list(d)
        shifted[edge_index] += eps
        observed = (
            recovery_from_decoupling(optima, weights, edges, reference, shifted)
            - baseline
        ) / eps
        assert isclose(observed, expected, rel_tol=2e-5, abs_tol=2e-6)


def test_same_edge_marginal_recovery_increases_with_release():
    optima, weights, edges, reference = example_problem()
    # Vary only edge 1, holding the rest fixed. Convex recovery implies its
    # own marginal pressure is nondecreasing as that edge is released.
    pressures = []
    for release in [0.0, 0.1, 0.3, 0.5, 0.7]:
        d = [0.0, release, 0.0]
        pressures.append(
            recovery_gradient(optima, weights, edges, reference, d)[1]
        )
    assert all(
        pressures[i + 1] >= pressures[i] - 1e-12
        for i in range(len(pressures) - 1)
    )
    assert pressures[-1] > pressures[0]


def test_linear_cost_best_vertex_beats_dense_interior_grid():
    optima = [0.0, 1.0, 2.5]
    weights = [1.0, 1.0, 1.0]
    edges = [(0, 1), (1, 2)]
    reference = [1.0, 1.0]
    costs = [0.12, 0.3]

    best = best_vertex_topology(optima, weights, edges, reference, costs)
    best_gain = float(best["net_gain"])

    for d1, d2 in product([0.0, 0.2, 0.4, 0.6, 0.8, 1.0], repeat=2):
        gain = net_gain_linear_cost(
            optima,
            weights,
            edges,
            reference,
            [d1, d2],
            costs,
        )
        assert best_gain >= gain - 1e-10


def test_vertex_enumeration_has_all_binary_topologies():
    optima = [0.0, 1.0, 2.5]
    weights = [1.0, 1.0, 1.0]
    edges = [(0, 1), (1, 2), (0, 2)]
    reference = [1.0, 0.8, 0.4]
    costs = [0.1, 0.2, 0.3]
    rows = enumerate_vertex_topologies(
        optima, weights, edges, reference, costs
    )
    assert len(rows) == 8
    released = {row["released"] for row in rows}
    assert len(released) == 8


def test_edge_release_receipt_uses_pressure_minus_cost():
    optima = [0.0, 2.0]
    weights = [1.0, 1.0]
    edges = [(0, 1)]
    reference = [1.0]
    d = [0.2]
    pressure = recovery_gradient(optima, weights, edges, reference, d)[0]

    more = edge_release_receipt(
        optima, weights, edges, reference, d, [0.5 * pressure]
    )[0]
    less = edge_release_receipt(
        optima, weights, edges, reference, d, [2.0 * pressure]
    )[0]
    balance = edge_release_receipt(
        optima, weights, edges, reference, d, [pressure]
    )[0]

    assert more["direction"] == "favor_more_decoupling"
    assert less["direction"] == "favor_more_coupling"
    assert balance["direction"] == "marginal_balance"
