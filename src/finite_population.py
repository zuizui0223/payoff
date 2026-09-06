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


def moran_fixation_probability_d(
    n: int, phi: float, eta: float, beta: float = 1.0
) -> float:
    """Exact fixation probability of one D mutant in N-1 S residents.

    Uses a log-sum-exp evaluation of
        rho_D = 1 / sum_{k=0}^{N-1} exp[-beta C_k]
    where C_k is the cumulative finite-population payoff gap.
    """

    _validate_population_and_selection(n, beta)
    logs = [-beta * cumulative_gap(k, n, phi, eta) for k in range(n)]
    m = max(logs)
    log_denom = m + log(sum(exp(value - m) for value in logs))
    return exp(-log_denom)


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
    """Return neutral-fixation cost thresholds (K_D_fix, K_S_fix).

    D is favored over neutral drift when K < R-eta/3.
    S is favored over neutral drift when K > R+eta/3.
    """

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
