from math import isclose

from src.topology_mutation import (
    best_bottleneck_payoff,
    detailed_balance_max_residual,
    intrinsic_valley_depth,
    is_single_edge_local_optimum,
    single_edge_mutation_graph,
    single_edge_neighbors,
    symmetric_mutation_stationary_distribution,
    symmetric_single_edge_generator,
    topology_substitution_rate,
)


def full_hypercube(edge_count: int):
    states = []
    for value in range(2**edge_count):
        states.append(
            tuple((value >> bit) & 1 for bit in range(edge_count))
        )
    return tuple(states)


def test_single_edge_neighbors_and_hypercube_graph():
    assert set(single_edge_neighbors((0, 1, 0))) == {
        (1, 1, 0),
        (0, 0, 0),
        (0, 1, 1),
    }
    graph = single_edge_mutation_graph(full_hypercube(3))
    assert all(len(neighbors) == 3 for neighbors in graph.values())


def test_symmetric_mutation_stationary_distribution_is_gibbs_in_intrinsic_payoff():
    payoffs = {
        (0, 0): 0.0,
        (1, 0): 0.2,
        (0, 1): -0.1,
        (1, 1): 0.8,
    }
    n = 15
    beta = 0.4
    stationary = symmetric_mutation_stationary_distribution(payoffs, n, beta)
    assert isclose(sum(stationary.values()), 1.0, abs_tol=1e-12)
    assert stationary[(1, 1)] > stationary[(1, 0)] > stationary[(0, 0)] > stationary[(0, 1)]


def test_topology_feedback_changes_rates_but_not_stationary_detailed_balance():
    payoffs = {
        (0, 0): 0.0,
        (1, 0): 0.2,
        (0, 1): -0.1,
        (1, 1): 0.8,
    }
    n = 12
    beta = 0.6
    mutation_rate = 0.01
    stationary = symmetric_mutation_stationary_distribution(payoffs, n, beta)

    rates = []
    for gamma in [-1.5, 0.0, 1.5]:
        states, generator = symmetric_single_edge_generator(
            payoffs,
            mutation_rate,
            n,
            beta,
            gamma,
        )
        assert detailed_balance_max_residual(states, generator, stationary) < 1e-12
        rates.append(generator[states.index((0, 0))][states.index((1, 0))])

    # Absolute substitution kinetics change with topology feedback.
    assert len({round(rate, 14) for rate in rates}) > 1


def test_pair_substitution_ratio_matches_intrinsic_gap_only():
    payoffs = {(0, 0): 0.0, (1, 0): 0.3}
    n = 20
    beta = 0.5
    mutation_rate = 0.02
    for gamma in [-2.0, -0.2, 0.0, 0.8, 3.0]:
        forward = topology_substitution_rate(
            (0, 0),
            (1, 0),
            payoffs,
            mutation_rate,
            n,
            beta,
            gamma,
        )
        reverse = topology_substitution_rate(
            (1, 0),
            (0, 0),
            payoffs,
            mutation_rate,
            n,
            beta,
            gamma,
        )
        expected_log_ratio = beta * (n - 2) * 0.3
        from math import exp
        assert isclose(forward / reverse, exp(expected_log_ratio), rel_tol=1e-11)


def test_intrinsic_valley_depth_zero_when_nonlower_path_exists():
    payoffs = {
        (0, 0): 0.0,
        (1, 0): 0.3,
        (0, 1): -0.5,
        (1, 1): 0.8,
    }
    # Path 00 -> 10 -> 11 never drops below source payoff.
    assert isclose(best_bottleneck_payoff((0, 0), (1, 1), payoffs), 0.0)
    assert isclose(intrinsic_valley_depth((0, 0), (1, 1), payoffs), 0.0)


def test_positive_valley_depth_when_every_single_edge_route_dips():
    payoffs = {
        (0, 0): 0.4,
        (1, 0): 0.1,
        (0, 1): 0.2,
        (1, 1): 1.0,
    }
    assert is_single_edge_local_optimum((0, 0), payoffs)
    # Best route goes through payoff 0.2 rather than 0.1.
    assert isclose(best_bottleneck_payoff((0, 0), (1, 1), payoffs), 0.2)
    assert isclose(intrinsic_valley_depth((0, 0), (1, 1), payoffs), 0.2)


def test_global_best_can_coexist_with_single_edge_local_trap():
    payoffs = {
        (0, 0, 0): 0.5,
        (1, 0, 0): 0.4,
        (0, 1, 0): 0.45,
        (0, 0, 1): 0.3,
        (1, 1, 0): 0.2,
        (1, 0, 1): 0.25,
        (0, 1, 1): 0.35,
        (1, 1, 1): 1.2,
    }
    assert is_single_edge_local_optimum((0, 0, 0), payoffs)
    assert payoffs[(1, 1, 1)] > payoffs[(0, 0, 0)]
    assert intrinsic_valley_depth((0, 0, 0), (1, 1, 1), payoffs) > 0.0
