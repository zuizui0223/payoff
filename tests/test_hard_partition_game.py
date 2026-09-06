from math import isclose

from src.hard_partition_game import (
    comembership_features,
    comembership_marginals,
    intrinsic_partition_payoff,
    pairwise_partition_payoff_parameters,
    partition_distance,
    population_potential,
    potential_from_comembership_marginals,
    registered_three_function_architectures,
    registered_three_function_effective_payoffs,
    registered_three_function_phase,
)


def test_registered_partition_comembership_features_and_distances():
    partitions, _ = registered_three_function_architectures()
    assert comembership_features(3, partitions["S"]) == (1, 1, 1)
    assert comembership_features(3, partitions["M"]) == (1, 0, 0)
    assert comembership_features(3, partitions["F"]) == (0, 0, 0)
    assert isclose(partition_distance(3, partitions["S"], partitions["M"]), 2.0)
    assert isclose(partition_distance(3, partitions["M"], partitions["F"]), 1.0)
    assert isclose(partition_distance(3, partitions["S"], partitions["F"]), 3.0)


def test_intrinsic_hard_partition_payoffs_match_registered_values():
    theta = [0.0, 1.0, 3.0]
    weights = [1.0, 1.0, 1.0]
    partitions, payoffs = registered_three_function_architectures()
    for name in ["S", "M", "F"]:
        observed = intrinsic_partition_payoff(
            theta, weights, partitions[name], extra_module_cost=1.0
        )
        assert isclose(observed, payoffs[name], rel_tol=1e-12, abs_tol=1e-12)


def test_pairwise_partition_game_maps_to_canonical_phi_eta():
    partitions, payoffs = registered_three_function_architectures()
    phi, eta = pairwise_partition_payoff_parameters(
        payoffs["M"],
        payoffs["F"],
        3,
        partitions["M"],
        partitions["F"],
        gamma=-1.0,
    )
    assert isclose(phi, -0.5, rel_tol=1e-12)
    assert isclose(eta, -1.0, rel_tol=1e-12)


def test_population_potential_matches_comembership_marginal_formula():
    partitions, payoffs = registered_three_function_architectures()
    names = ["S", "M", "F"]
    part_list = [partitions[name] for name in names]
    intrinsic = [payoffs[name] for name in names]
    frequencies = [0.2, 0.5, 0.3]
    gamma = -0.7
    direct = population_potential(
        intrinsic, part_list, frequencies, 3, gamma
    )
    marginals = comembership_marginals(3, part_list, frequencies)
    reduced = potential_from_comembership_marginals(
        intrinsic, frequencies, marginals, gamma
    )
    assert isclose(direct, reduced, rel_tol=1e-12, abs_tol=1e-12)


def test_registered_phase_boundaries_and_equilibria():
    phase0 = registered_three_function_phase(0.2)
    assert phase0["phase"] == "M_monomorphic"
    assert phase0["p_M"] == 1.0

    phase1 = registered_three_function_phase(1.0)
    assert phase1["phase"] == "M_F_coexistence"
    assert isclose(phase1["p_F"], 0.25, rel_tol=1e-12)
    assert isclose(phase1["p_M"], 0.75, rel_tol=1e-12)
    assert phase1["p_S"] == 0.0

    phase2 = registered_three_function_phase(2.0)
    assert phase2["phase"] == "S_M_F_coexistence"
    assert isclose(
        phase2["p_S"] + phase2["p_M"] + phase2["p_F"],
        1.0,
        rel_tol=1e-12,
    )
    assert phase2["p_S"] > 0.0
    assert phase2["p_M"] > 0.0
    assert phase2["p_F"] > 0.0


def test_equilibrium_effective_payoffs_equal_on_active_support():
    for h in [0.75, 1.2]:
        phase = registered_three_function_phase(h)
        frequencies = {
            "S": phase["p_S"],
            "M": phase["p_M"],
            "F": phase["p_F"],
        }
        payoffs = registered_three_function_effective_payoffs(h, frequencies)
        assert isclose(payoffs["M"], payoffs["F"], rel_tol=1e-12, abs_tol=1e-12)
        assert payoffs["S"] <= payoffs["M"] + 1e-12

    for h in [1.7, 2.0, 5.0]:
        phase = registered_three_function_phase(h)
        frequencies = {
            "S": phase["p_S"],
            "M": phase["p_M"],
            "F": phase["p_F"],
        }
        payoffs = registered_three_function_effective_payoffs(h, frequencies)
        assert isclose(payoffs["S"], payoffs["M"], rel_tol=1e-12, abs_tol=1e-12)
        assert isclose(payoffs["M"], payoffs["F"], rel_tol=1e-12, abs_tol=1e-12)


def test_shared_invades_MF_boundary_exactly_above_19_over_12():
    h0 = 19.0 / 12.0
    phase = registered_three_function_phase(h0)
    frequencies = {"S": phase["p_S"], "M": phase["p_M"], "F": phase["p_F"]}
    payoffs = registered_three_function_effective_payoffs(h0, frequencies)
    assert isclose(payoffs["S"], payoffs["M"], rel_tol=1e-12, abs_tol=1e-12)


def test_strong_feedback_limit_goes_to_shared_and_full_extremes():
    phase = registered_three_function_phase(1e6)
    assert isclose(phase["p_S"], 0.5, rel_tol=1e-5)
    assert phase["p_M"] < 2e-6
    assert isclose(phase["p_F"], 0.5, rel_tol=1e-5)
