"""Recurrent-mutation stationary extension of the PAYOFF Moran game.

States are i=0,...,N differentiated (D) individuals. Reproduction follows the
finite-population PAYOFF game with exponential payoff-to-fitness mapping.
Offspring mutate S->D with probability u_sd and D->S with probability u_ds,
then one uniformly random individual dies.

For u_sd,u_ds in (0,1), the finite birth-death chain is irreducible and has a
unique reversible stationary distribution.
"""

from __future__ import annotations

from math import exp, log
from typing import Dict, List, Sequence, Tuple

from src.finite_population import finite_payoffs


def mutation_transition_probabilities(
    i: int,
    n: int,
    phi: float,
    eta: float,
    beta: float,
    u_sd: float,
    u_ds: float,
) -> Tuple[float, float]:
    """Return (T_plus,T_minus) for the recurrent-mutation Moran chain."""

    _validate_population(n)
    _validate_state_including_boundaries(i, n)
    _validate_selection(beta)
    _validate_mutation(u_sd, u_ds, require_irreducible=False)

    if i == 0:
        return u_sd, 0.0
    if i == n:
        return 0.0, u_ds

    pi_s, pi_d = finite_payoffs(i, n, phi, eta)

    log_w_d = log(i) + beta * pi_d
    log_w_s = log(n - i) + beta * pi_s
    m = max(log_w_d, log_w_s)
    w_d = exp(log_w_d - m)
    w_s = exp(log_w_s - m)
    parent_d = w_d / (w_d + w_s)

    offspring_d = parent_d * (1.0 - u_ds) + (1.0 - parent_d) * u_sd
    offspring_s = 1.0 - offspring_d

    t_plus = offspring_d * (n - i) / n
    t_minus = offspring_s * i / n
    return t_plus, t_minus


def stationary_distribution(
    n: int,
    phi: float,
    eta: float,
    beta: float,
    u_sd: float,
    u_ds: float,
) -> List[float]:
    """Return the exact stationary distribution over i=0,...,N."""

    _validate_population(n)
    _validate_selection(beta)
    _validate_mutation(u_sd, u_ds, require_irreducible=True)

    log_weights = [0.0]
    for i in range(1, n + 1):
        t_plus_prev, _ = mutation_transition_probabilities(
            i - 1, n, phi, eta, beta, u_sd, u_ds
        )
        _, t_minus_i = mutation_transition_probabilities(
            i, n, phi, eta, beta, u_sd, u_ds
        )
        if t_plus_prev <= 0.0 or t_minus_i <= 0.0:
            raise ValueError("irreducible stationary chain requires positive neighboring transitions")
        log_weights.append(log_weights[-1] + log(t_plus_prev) - log(t_minus_i))

    return _normalize_log_weights(log_weights)


def stationary_summary(probabilities: Sequence[float]) -> Dict[str, float]:
    """Summarize a stationary distribution over 0,...,N D individuals."""

    if len(probabilities) < 2:
        raise ValueError("stationary distribution must contain at least two states")
    if any(p < 0.0 for p in probabilities):
        raise ValueError("stationary probabilities must be non-negative")
    total = sum(probabilities)
    if total <= 0.0:
        raise ValueError("stationary probabilities must have positive total")

    probs = [p / total for p in probabilities]
    n = len(probs) - 1
    mean_p = sum((i / n) * p for i, p in enumerate(probs))
    mean_heterozygosity = sum(2.0 * (i / n) * (1.0 - i / n) * p for i, p in enumerate(probs))
    boundary_mass = probs[0] + probs[-1]
    return {
        "mean_d_frequency": mean_p,
        "boundary_mass": boundary_mass,
        "interior_mass": 1.0 - boundary_mass,
        "mean_two_type_heterozygosity": mean_heterozygosity,
        "p_all_s": probs[0],
        "p_all_d": probs[-1],
    }


def stationary_modes(probabilities: Sequence[float], tol: float = 1e-15) -> List[int]:
    """Return state indices that are local stationary modes."""

    if not probabilities:
        raise ValueError("probabilities cannot be empty")
    modes: List[int] = []
    for i, value in enumerate(probabilities):
        left = probabilities[i - 1] if i > 0 else float("-inf")
        right = probabilities[i + 1] if i + 1 < len(probabilities) else float("-inf")
        if value + tol >= left and value + tol >= right:
            modes.append(i)
    return modes


def detailed_balance_residuals(
    probabilities: Sequence[float],
    n: int,
    phi: float,
    eta: float,
    beta: float,
    u_sd: float,
    u_ds: float,
) -> List[float]:
    """Return pi_i T_i^+ - pi_{i+1} T_{i+1}^- for adjacent states."""

    if len(probabilities) != n + 1:
        raise ValueError("probability vector length must equal n+1")
    residuals: List[float] = []
    for i in range(n):
        t_plus, _ = mutation_transition_probabilities(i, n, phi, eta, beta, u_sd, u_ds)
        _, t_minus_next = mutation_transition_probabilities(
            i + 1, n, phi, eta, beta, u_sd, u_ds
        )
        residuals.append(probabilities[i] * t_plus - probabilities[i + 1] * t_minus_next)
    return residuals


def rare_mutation_log_boundary_odds(
    n: int, phi: float, beta: float, u_sd: float, u_ds: float
) -> float:
    """Weak-mutation limit log(P_all_D/P_all_S)."""

    _validate_population(n)
    _validate_selection(beta)
    if u_sd <= 0.0 or u_ds <= 0.0:
        raise ValueError("rare-mutation odds require positive mutation rates")
    return log(u_sd / u_ds) + beta * phi * (n - 2)


def rare_mutation_boundary_probability_d(
    n: int, phi: float, beta: float, u_sd: float, u_ds: float
) -> float:
    """Weak-mutation two-state approximation to long-run all-D occupancy."""

    z = rare_mutation_log_boundary_odds(n, phi, beta, u_sd, u_ds)
    if z >= 0:
        ez = exp(-z)
        return 1.0 / (1.0 + ez)
    ez = exp(z)
    return ez / (1.0 + ez)


def mutation_shifted_static_crossing(
    n: int, beta: float, u_sd: float, u_ds: float
) -> float:
    """Return phi where rare-mutation all-D and all-S occupancies are equal."""

    if n <= 2:
        raise ValueError("mutation-shifted crossing requires n>2")
    if beta <= 0.0:
        raise ValueError("mutation-shifted crossing requires beta>0")
    if u_sd <= 0.0 or u_ds <= 0.0:
        raise ValueError("mutation rates must be positive")
    return -log(u_sd / u_ds) / (beta * (n - 2))


def mutation_shifted_cost_crossing(
    n: int, recovery: float, beta: float, u_sd: float, u_ds: float
) -> float:
    """Return K where rare-mutation all-D and all-S occupancies are equal."""

    if recovery < 0.0:
        raise ValueError("recovery must be non-negative")
    phi_mut = mutation_shifted_static_crossing(n, beta, u_sd, u_ds)
    return recovery - phi_mut


def mutation_shifted_environment_crossing(
    static_crossing: float,
    phi_slope: float,
    n: int,
    beta: float,
    u_sd: float,
    u_ds: float,
) -> float:
    """Return equal-occupancy environment for phi(e)=slope*(e-e0)."""

    if phi_slope == 0.0:
        raise ValueError("phi_slope must be non-zero")
    phi_mut = mutation_shifted_static_crossing(n, beta, u_sd, u_ds)
    return static_crossing + phi_mut / phi_slope


def stationary_log_odds_from_components(
    n: int, beta: float, phi: float, mutation_log_bias: float
) -> float:
    """Rare-mutation stationary log odds m+beta(N-2)phi."""

    _validate_population(n)
    _validate_selection(beta)
    return mutation_log_bias + beta * (n - 2) * phi


def infer_phi_mutation_bias_from_population_sizes(
    log_odds_1: float,
    n_1: int,
    log_odds_2: float,
    n_2: int,
    beta: float,
) -> Tuple[float, float]:
    """Infer (phi, mutation_log_bias) from two population sizes."""

    _validate_population(n_1)
    _validate_population(n_2)
    if n_1 == n_2:
        raise ValueError("population sizes must differ")
    if beta <= 0.0:
        raise ValueError("beta must be positive")
    phi = (log_odds_2 - log_odds_1) / (beta * (n_2 - n_1))
    mutation_log_bias = log_odds_1 - beta * (n_1 - 2) * phi
    return phi, mutation_log_bias


def infer_phi_mutation_bias_from_selection_intensities(
    log_odds_1: float,
    beta_1: float,
    log_odds_2: float,
    beta_2: float,
    n: int,
) -> Tuple[float, float]:
    """Infer (phi, mutation_log_bias) from two selection intensities."""

    if n <= 2:
        raise ValueError("selection-intensity identification requires n>2")
    _validate_selection(beta_1)
    _validate_selection(beta_2)
    if beta_1 == beta_2:
        raise ValueError("selection intensities must differ")
    phi = (log_odds_2 - log_odds_1) / ((beta_2 - beta_1) * (n - 2))
    mutation_log_bias = log_odds_1 - beta_1 * (n - 2) * phi
    return phi, mutation_log_bias


def neutral_beta_binomial_parameters(
    n: int, u_sd: float, u_ds: float
) -> Tuple[float, float]:
    """Return exact neutral beta-binomial parameters (alpha,beta_param)."""

    _validate_population(n)
    _validate_mutation(u_sd, u_ds, require_irreducible=True)
    q = 1.0 - u_sd - u_ds
    if q <= 0.0:
        raise ValueError("beta-binomial form requires u_sd+u_ds<1")
    return n * u_sd / q, n * u_ds / q


def neutral_beta_binomial_distribution(
    n: int, u_sd: float, u_ds: float
) -> List[float]:
    """Return the exact neutral stationary distribution in beta-binomial form."""

    alpha, beta_param = neutral_beta_binomial_parameters(n, u_sd, u_ds)
    log_weights = [0.0]
    for i in range(1, n + 1):
        ratio = (
            (n - i + 1) / i
            * (alpha + i - 1)
            / (beta_param + n - i)
        )
        log_weights.append(log_weights[-1] + log(ratio))
    return _normalize_log_weights(log_weights)


def neutral_expected_d_frequency(u_sd: float, u_ds: float) -> float:
    """Return exact neutral stationary mean D frequency u_sd/(u_sd+u_ds)."""

    if u_sd <= 0.0 or u_ds <= 0.0:
        raise ValueError("neutral stationary mean requires positive mutation rates")
    return u_sd / (u_sd + u_ds)


def neutral_symmetric_mutation_critical_rate(n: int) -> float:
    """Return mu_c=1/(N+2), the exact neutral symmetric shape threshold."""

    _validate_population(n)
    return 1.0 / (n + 2.0)


def neutral_symmetric_stationary_shape(
    n: int, mutation_rate: float, tol: float = 1e-12
) -> str:
    """Classify the exact neutral symmetric stationary shape for 0<mu<1/2."""

    _validate_population(n)
    if not 0.0 < mutation_rate < 0.5:
        raise ValueError("neutral symmetric shape classification requires 0<mutation_rate<1/2")
    critical = neutral_symmetric_mutation_critical_rate(n)
    if mutation_rate < critical - tol:
        return "boundary_biased"
    if mutation_rate > critical + tol:
        return "interior_biased"
    return "uniform"


def _normalize_log_weights(log_weights: Sequence[float]) -> List[float]:
    m = max(log_weights)
    weights = [exp(value - m) for value in log_weights]
    total = sum(weights)
    return [value / total for value in weights]


def _validate_population(n: int) -> None:
    if n < 2:
        raise ValueError("n must be at least 2")


def _validate_state_including_boundaries(i: int, n: int) -> None:
    if not 0 <= i <= n:
        raise ValueError("i must lie in [0,n]")


def _validate_selection(beta: float) -> None:
    if beta < 0.0:
        raise ValueError("beta must be non-negative")


def _validate_mutation(u_sd: float, u_ds: float, require_irreducible: bool) -> None:
    for value, name in [(u_sd, "u_sd"), (u_ds, "u_ds")]:
        if not 0.0 <= value <= 1.0:
            raise ValueError(f"{name} must lie in [0,1]")
    if require_irreducible and not (0.0 < u_sd < 1.0 and 0.0 < u_ds < 1.0):
        raise ValueError("unique stationary distribution requires 0<u_sd,u_ds<1")
