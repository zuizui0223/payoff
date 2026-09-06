"""Finite-population Moran extension of the PAYOFF architecture game.

The deterministic game uses
    Delta(p) = phi + eta(2p-1)
with symmetric payoff matrix
    [[0, phi-eta], [phi-eta, 2phi]]
for strategies (S, D).

This module uses self-excluding pairwise interactions and exponential
payoff-to-fitness mapping f=exp(beta*pi), which guarantees positive fitness.
"""

from __future__ import annotations

from math import exp, log
from typing import Tuple


def finite_payoffs(i: int, n: int, phi: float, eta: float) -> Tuple[float, float]:
    """Return (pi_S, pi_D) with i differentiated individuals in population n."""

    _validate_state(i, n)
    denom = n - 1
    off_diag = phi - eta
    pi_d = (2.0 * phi * (i - 1) + off_diag * (n - i)) / denom
    pi_s = off_diag * i / denom
    return pi_s, pi_d


def finite_payoff_gap(i: int, n: int, phi: float, eta: float) -> float:
    """Exact self-excluding finite-population gap pi_D-pi_S."""

    _validate_state(i, n)
    return (phi * (n - 2) + eta * (2 * i - n)) / (n - 1)


def finite_zero_gap_count(n: int, phi: float, eta: float) -> float:
    """Continuous D-count at which the finite-population payoff gap is zero."""

    if n < 2:
        raise ValueError("n must be at least 2")
    if eta == 0:
        raise ValueError("eta must be non-zero")
    return 0.5 * (n - phi * (n - 2) / eta)


def cumulative_gap(k: int, n: int, phi: float, eta: float) -> float:
    """Return sum_{j=1}^k Delta_N(j), including k=0."""

    if n < 2:
        raise ValueError("n must be at least 2")
    if not 0 <= k <= n - 1:
        raise ValueError("k must lie in [0,n-1]")
    if k == 0:
        return 0.0
    return k * (phi * (n - 2) + eta * (k + 1 - n)) / (n - 1)


def moran_log_fixation_ratio_d_over_s(n: int, phi: float, beta: float) -> float:
    """Return log(rho_D/rho_S)=beta*phi*(n-2) under exponential fitness."""

    _validate_population_and_selection(n, beta)
    return beta * phi * (n - 2)


def moran_fixation_probability_from_i(
    initial_d: int,
    n: int,
    phi: float,
    eta: float,
    beta: float = 1.0,
) -> float:
    """Exact probability that D fixates from an arbitrary initial D count."""

    _validate_population_and_selection(n, beta)
    if not 0 <= initial_d <= n:
        raise ValueError("initial_d must lie in [0,n]")
    if initial_d == 0:
        return 0.0
    if initial_d == n:
        return 1.0

    logs = _fixation_log_weights(n, phi, eta, beta)
    log_denom = _logsumexp(logs)
    log_numer = _logsumexp(logs[:initial_d])
    return exp(log_numer - log_denom)


def moran_fixation_probability_d(
    n: int, phi: float, eta: float, beta: float = 1.0
) -> float:
    """Exact fixation probability of one D mutant in N-1 S residents."""

    return moran_fixation_probability_from_i(1, n, phi, eta, beta)


def moran_fixation_probability_s(
    n: int, phi: float, eta: float, beta: float = 1.0
) -> float:
    """Exact fixation probability of one S mutant in N-1 D residents."""

    return moran_fixation_probability_d(n, -phi, eta, beta)


def reciprocal_fixation_probabilities(
    n: int, phi: float, eta: float, beta: float = 1.0
) -> Tuple[float, float]:
    """Return (rho_D, rho_S)."""

    return (
        moran_fixation_probability_d(n, phi, eta, beta),
        moran_fixation_probability_s(n, phi, eta, beta),
    )


def minimum_initial_d_for_fixation_probability(
    n: int,
    phi: float,
    eta: float,
    beta: float = 1.0,
    target: float = 0.5,
) -> int:
    """Smallest initial D count whose fixation probability reaches target.

    This is an exact weighted-quantile diagnostic for the declared Moran model.
    At neutrality it reduces to ceil(target*N).
    """

    _validate_population_and_selection(n, beta)
    if not 0.0 < target <= 1.0:
        raise ValueError("target must lie in (0,1]")

    logs = _fixation_log_weights(n, phi, eta, beta)
    m = max(logs)
    weights = [exp(value - m) for value in logs]
    total = sum(weights)
    cumulative = 0.0
    for initial_d in range(1, n + 1):
        cumulative += weights[initial_d - 1]
        if cumulative / total >= target:
            return initial_d
    return n


def weak_selection_scores(phi: float, eta: float) -> Tuple[float, float]:
    """Return first-order mutant-advantage scores for (D, S).

    For N>2 under weak selection:
        rho_D > 1/N iff 3phi-eta > 0
        rho_S > 1/N iff -3phi-eta > 0.
    """

    return 3.0 * phi - eta, -3.0 * phi - eta


def weak_selection_advantage_flags(phi: float, eta: float) -> Tuple[bool, bool]:
    """Return strict weak-selection advantage flags (D_adv, S_adv)."""

    d_score, s_score = weak_selection_scores(phi, eta)
    return d_score > 0.0, s_score > 0.0


def weak_selection_cost_thresholds(recovery: float, eta: float) -> Tuple[float, float]:
    """Return neutral-fixation cost thresholds (K_D_fix, K_S_fix)."""

    if recovery < 0:
        raise ValueError("recovery must be non-negative")
    return recovery - eta / 3.0, recovery + eta / 3.0


def classify_weak_selection_mutant_advantage(phi: float, eta: float) -> str:
    """Classify which reciprocal single mutants exceed neutral fixation."""

    d_adv, s_adv = weak_selection_advantage_flags(phi, eta)
    if d_adv and s_adv:
        return "both_mutants_advantageous"
    if d_adv:
        return "d_mutant_advantageous"
    if s_adv:
        return "s_mutant_advantageous"
    return "neither_mutant_advantageous"


def deterministic_coordination_threshold(phi: float, eta: float) -> float:
    """Return p* for a strict coordination game (eta>0 and |phi|<eta)."""

    if eta <= 0:
        raise ValueError("eta must be positive for a coordination threshold")
    if not abs(phi) < eta:
        raise ValueError("coordination threshold requires |phi|<eta")
    return 0.5 * (1.0 - phi / eta)


def _fixation_log_weights(n: int, phi: float, eta: float, beta: float):
    return [-beta * cumulative_gap(k, n, phi, eta) for k in range(n)]


def _logsumexp(values) -> float:
    m = max(values)
    return m + log(sum(exp(value - m) for value in values))


def _validate_state(i: int, n: int) -> None:
    if n < 2:
        raise ValueError("n must be at least 2")
    if not 1 <= i <= n - 1:
        raise ValueError("i must lie in [1,n-1]")


def _validate_population_and_selection(n: int, beta: float) -> None:
    if n < 2:
        raise ValueError("n must be at least 2")
    if beta < 0:
        raise ValueError("beta must be non-negative")
