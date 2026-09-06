from math import exp, isclose

from src.finite_population import reciprocal_fixation_probabilities
from src.three_function_example import (
    FULLY_RELEASED,
    TWO_MODULE,
    intrinsic_topology_payoffs,
)
from src.topology_game import (
    classify_pairwise_topology_game,
    pairwise_payoff_parameters,
    reciprocal_invasion_margins,
)
from src.topology_mutation import symmetric_mutation_stationary_distribution


EDGE_COST = 0.4
GAMMA = -0.25
N = 20
BETA = 0.4


def test_best_module_and_full_release_have_exact_canonical_pair():
    payoffs = intrinsic_topology_payoffs(EDGE_COST)
    phi, eta = pairwise_payoff_parameters(
        payoffs[TWO_MODULE],
        payoffs[FULLY_RELEASED],
        TWO_MODULE,
        FULLY_RELEASED,
        GAMMA,
    )
    assert isclose(phi, -1.0 / 15.0, abs_tol=1e-12)
    assert isclose(eta, -1.0 / 4.0, abs_tol=1e-12)
    assert abs(phi) < abs(eta)
    assert (
        classify_pairwise_topology_game(
            payoffs[TWO_MODULE],
            payoffs[FULLY_RELEASED],
            TWO_MODULE,
            FULLY_RELEASED,
            GAMMA,
        )
        == "stable_pairwise_coexistence"
    )


def test_full_release_equilibrium_frequency_is_eleven_thirtieth():
    payoffs = intrinsic_topology_payoffs(EDGE_COST)
    phi, eta = pairwise_payoff_parameters(
        payoffs[TWO_MODULE],
        payoffs[FULLY_RELEASED],
        TWO_MODULE,
        FULLY_RELEASED,
        GAMMA,
    )
    p_full = 0.5 * (1.0 - phi / eta)
    assert isclose(p_full, 11.0 / 30.0, abs_tol=1e-12)


def test_only_full_release_reciprocally_invades_best_module():
    payoffs = intrinsic_topology_payoffs(EDGE_COST)
    for topology, payoff in payoffs.items():
        if topology == TWO_MODULE:
            continue
        classification = classify_pairwise_topology_game(
            payoffs[TWO_MODULE],
            payoff,
            TWO_MODULE,
            topology,
            GAMMA,
        )
        if topology == FULLY_RELEASED:
            assert classification == "stable_pairwise_coexistence"
        else:
            assert classification == "s_dominance"


def test_exact_finite_population_fixation_separates_neutral_and_reciprocal_ordering():
    payoffs = intrinsic_topology_payoffs(EDGE_COST)
    phi, eta = pairwise_payoff_parameters(
        payoffs[TWO_MODULE],
        payoffs[FULLY_RELEASED],
        TWO_MODULE,
        FULLY_RELEASED,
        GAMMA,
    )
    rho_full, rho_module = reciprocal_fixation_probabilities(N, phi, eta, BETA)
    assert rho_full > 1.0 / N
    assert rho_module > 1.0 / N
    assert rho_module > rho_full
    assert isclose(
        rho_full / rho_module,
        exp(BETA * (N - 2) * phi),
        rel_tol=1e-11,
        abs_tol=1e-12,
    )


def test_rare_mutation_stationary_mass_is_concentrated_on_module_and_full_release():
    payoffs = intrinsic_topology_payoffs(EDGE_COST)
    stationary = symmetric_mutation_stationary_distribution(payoffs, N, BETA)
    assert stationary[TWO_MODULE] > stationary[FULLY_RELEASED]
    assert stationary[TWO_MODULE] + stationary[FULLY_RELEASED] > 0.999
    assert isclose(
        stationary[TWO_MODULE] / stationary[FULLY_RELEASED],
        exp(BETA * (N - 2) / 15.0),
        rel_tol=1e-11,
        abs_tol=1e-12,
    )


def test_deterministic_invasion_margins_are_both_positive_for_module_full_pair():
    payoffs = intrinsic_topology_payoffs(EDGE_COST)
    full_into_module, module_into_full = reciprocal_invasion_margins(
        payoffs[TWO_MODULE],
        payoffs[FULLY_RELEASED],
        TWO_MODULE,
        FULLY_RELEASED,
        GAMMA,
    )
    assert isclose(full_into_module, 11.0 / 60.0, abs_tol=1e-12)
    assert isclose(module_into_full, 19.0 / 60.0, abs_tol=1e-12)
    assert full_into_module > 0.0
    assert module_into_full > 0.0
