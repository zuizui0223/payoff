from math import isclose, log

from src.mutation_stationary import (
    infer_phi_mutation_bias_from_population_sizes,
    infer_phi_mutation_bias_from_selection_intensities,
    mutation_shifted_environment_crossing,
    stationary_log_odds_from_components,
)


def test_two_population_sizes_identify_phi_and_mutation_bias():
    phi = 0.17
    mutation_log_bias = log(2.4)
    beta = 0.6
    n1, n2 = 20, 47

    y1 = stationary_log_odds_from_components(n1, beta, phi, mutation_log_bias)
    y2 = stationary_log_odds_from_components(n2, beta, phi, mutation_log_bias)

    phi_hat, bias_hat = infer_phi_mutation_bias_from_population_sizes(
        y1, n1, y2, n2, beta
    )
    assert isclose(phi_hat, phi, rel_tol=1e-12, abs_tol=1e-12)
    assert isclose(bias_hat, mutation_log_bias, rel_tol=1e-12, abs_tol=1e-12)


def test_two_selection_intensities_identify_phi_and_mutation_bias():
    phi = -0.08
    mutation_log_bias = log(0.7)
    n = 35
    beta1, beta2 = 0.2, 0.9

    y1 = stationary_log_odds_from_components(n, beta1, phi, mutation_log_bias)
    y2 = stationary_log_odds_from_components(n, beta2, phi, mutation_log_bias)

    phi_hat, bias_hat = infer_phi_mutation_bias_from_selection_intensities(
        y1, beta1, y2, beta2, n
    )
    assert isclose(phi_hat, phi, rel_tol=1e-12, abs_tol=1e-12)
    assert isclose(bias_hat, mutation_log_bias, rel_tol=1e-12, abs_tol=1e-12)


def test_mutation_shifted_environment_crossing_satisfies_equal_occupancy_condition():
    e0 = 3.2
    slope = 0.4
    n = 30
    beta = 0.5
    u_sd = 0.03
    u_ds = 0.01

    e_occ = mutation_shifted_environment_crossing(
        e0, slope, n, beta, u_sd, u_ds
    )
    phi_at_occ = slope * (e_occ - e0)
    log_odds = log(u_sd / u_ds) + beta * (n - 2) * phi_at_occ
    assert isclose(log_odds, 0.0, abs_tol=1e-12)


def test_symmetric_mutation_leaves_environment_crossing_unshifted():
    e0 = -1.1
    e_occ = mutation_shifted_environment_crossing(
        static_crossing=e0,
        phi_slope=-0.7,
        n=25,
        beta=0.4,
        u_sd=0.02,
        u_ds=0.02,
    )
    assert isclose(e_occ, e0, abs_tol=1e-12)
