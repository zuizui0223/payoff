"""Reference implementation for the PAYOFF evolutionary architecture game.

The module mirrors the analytic statements in theory/THEOREMS.md and
THEORY/ENVIRONMENTAL_PHASE_DIAGRAM.md using only Python's standard library so
that the core identities remain easy to audit.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import inf
from typing import Optional, Sequence, Tuple


@dataclass(frozen=True)
class QuadraticTraitArchitecture:
    """Two-function quadratic shared-vs-differentiated architecture model."""

    a: float
    b: float
    theta1: float
    theta2: float
    coupling: float = 0.0
    architecture_cost: float = 0.0

    def __post_init__(self) -> None:
        if self.a <= 0 or self.b <= 0:
            raise ValueError("a and b must be positive")
        if self.coupling < 0:
            raise ValueError("coupling must be non-negative")
        if self.architecture_cost < 0:
            raise ValueError("architecture_cost must be non-negative")

    @property
    def d(self) -> float:
        return self.theta1 - self.theta2

    @property
    def shared_optimum(self) -> float:
        return (self.a * self.theta1 + self.b * self.theta2) / (self.a + self.b)

    @property
    def conflict_load(self) -> float:
        return (self.a * self.b / (self.a + self.b)) * self.d**2

    @property
    def q(self) -> float:
        c = self.coupling
        return self.a * self.b + c * (self.a + self.b)

    @property
    def differentiated_optima(self) -> Tuple[float, float]:
        a, b, c = self.a, self.b, self.coupling
        q = self.q
        x = (a * (b + c) * self.theta1 + b * c * self.theta2) / q
        y = (a * c * self.theta1 + b * (a + c) * self.theta2) / q
        return x, y

    @property
    def separation_fraction(self) -> float:
        """Algebraic release fraction s=ab/[ab+c(a+b)]."""

        return self.a * self.b / self.q

    @property
    def differentiated_loss(self) -> float:
        a, b, c = self.a, self.b, self.coupling
        return (a * b * c / self.q) * self.d**2

    @property
    def recovered_loss(self) -> float:
        return self.conflict_load - self.differentiated_loss

    @property
    def recovered_loss_via_bridge(self) -> float:
        return self.separation_fraction * self.conflict_load

    @property
    def phi(self) -> float:
        """Optimized D-minus-S architecture payoff gap."""

        return self.recovered_loss - self.architecture_cost

    def critical_coupling(self) -> Optional[float]:
        """Return c where phi=0 when a non-negative crossing exists.

        For L>0:
        - K=0: crossing is approached only at c -> infinity, so return inf.
        - 0<K<=L: return the finite non-negative crossing.
        - K>L: even full release cannot pay, so return None.
        For L=0 there is no conflict-driven crossing, so return None.
        """

        L = self.conflict_load
        K = self.architecture_cost
        if L == 0:
            return None
        if K == 0:
            return inf
        if K > L:
            return None
        return self.a * self.b * (L - K) / (K * (self.a + self.b))


def n_function_conflict(
    weights: Sequence[float], optima: Sequence[float]
) -> Tuple[float, float, float]:
    """Return (shared optimum, weighted-variance load, pairwise load).

    The last two values are analytically identical and are returned separately
    so tests and empirical pipelines can audit the identity.
    """

    if len(weights) != len(optima) or not weights:
        raise ValueError("weights and optima must have the same non-zero length")
    if any(w <= 0 for w in weights):
        raise ValueError("all weights must be positive")

    total = sum(weights)
    z = sum(w * t for w, t in zip(weights, optima)) / total
    variance_load = sum(w * (t - z) ** 2 for w, t in zip(weights, optima))

    pairwise_sum = 0.0
    for i in range(len(weights)):
        for j in range(i + 1, len(weights)):
            pairwise_sum += weights[i] * weights[j] * (optima[i] - optima[j]) ** 2
    pairwise_load = pairwise_sum / total
    return z, variance_load, pairwise_load


def architecture_phi(
    conflict_load: float, separation_fraction: float, architecture_cost: float
) -> float:
    """Return the frequency-independent architecture gap phi=sL-K."""

    _validate_bridge(conflict_load, separation_fraction, architecture_cost)
    return separation_fraction * conflict_load - architecture_cost


def invasion_margins(
    conflict_load: float,
    separation_fraction: float,
    architecture_cost: float,
    eta: float,
) -> Tuple[float, float]:
    """Return reciprocal rare-architecture invasion margins (I_D, I_S).

    I_D is the payoff advantage of rare D in an S resident population:
        I_D = Delta(0) = phi-eta.

    I_S is the payoff advantage of rare S in a D resident population:
        I_S = -Delta(1) = -phi-eta.
    """

    phi = architecture_phi(conflict_load, separation_fraction, architecture_cost)
    return phi - eta, -phi - eta


def invasion_cost_surfaces(
    conflict_load: float, separation_fraction: float, eta: float
) -> Tuple[float, float]:
    """Return neutral cost thresholds (K_D, K_S).

    K_D=R-eta makes rare D neutral in an S population.
    K_S=R+eta makes rare S neutral in a D population.
    Their signed separation is K_S-K_D=2*eta.
    """

    _validate_bridge(conflict_load, separation_fraction, 0.0)
    recovery = separation_fraction * conflict_load
    return recovery - eta, recovery + eta


def middle_cost_interval(
    conflict_load: float, separation_fraction: float, eta: float
) -> Tuple[float, float]:
    """Return the ordered cost interval with |phi|<|eta|.

    Its raw mathematical width is exactly 2|eta|. The biologically feasible
    portion additionally intersects K>=0.
    """

    _validate_bridge(conflict_load, separation_fraction, 0.0)
    recovery = separation_fraction * conflict_load
    h = abs(eta)
    return recovery - h, recovery + h


def infer_recovery_feedback_from_cost_thresholds(
    k_d_neutral: float, k_s_neutral: float
) -> Tuple[float, float]:
    """Invert reciprocal neutral-cost thresholds into (R, eta)."""

    recovery = 0.5 * (k_d_neutral + k_s_neutral)
    eta = 0.5 * (k_s_neutral - k_d_neutral)
    return recovery, eta


def classify_lke_phase(
    conflict_load: float,
    separation_fraction: float,
    architecture_cost: float,
    eta: float,
    tol: float = 1e-12,
) -> str:
    """Classify the architecture game directly from (L,s,K,eta)."""

    phi = architecture_phi(conflict_load, separation_fraction, architecture_cost)
    return classify_phase(phi, eta, tol=tol)


def linear_environment_thresholds(
    static_crossing: float, phi_slope: float, eta: float
) -> Tuple[float, float, float]:
    """Return (e_low, e0, e_high) for phi(e)=slope*(e-e0).

    The two game boundaries satisfy phi=+-|eta| and are separated by
    2|eta|/|slope|. When eta=0, all three values equal e0.
    """

    if phi_slope == 0:
        raise ValueError("phi_slope must be non-zero")
    h = abs(eta)
    e1 = static_crossing - h / phi_slope
    e2 = static_crossing + h / phi_slope
    return min(e1, e2), static_crossing, max(e1, e2)


def game_matrix(phi: float, eta: float) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """Symmetric 2x2 payoff matrix generating the declared payoff gap.

    Rows and columns are ordered (S, D):

        [[0,       phi-eta],
         [phi-eta, 2*phi  ]]

    With differentiated frequency p this gives
    pi_D-pi_S = phi+eta(2p-1).
    """

    return ((0.0, phi - eta), (phi - eta, 2.0 * phi))


def architecture_payoffs(p: float, phi: float, eta: float) -> Tuple[float, float]:
    """Return (pi_S, pi_D) at differentiated frequency p."""

    _validate_frequency(p)
    off_diag = phi - eta
    pi_s = off_diag * p
    pi_d = off_diag * (1.0 - p) + 2.0 * phi * p
    return pi_s, pi_d


def payoff_gap(p: float, phi: float, eta: float) -> float:
    """Return Delta(p)=pi_D-pi_S=phi+eta(2p-1)."""

    _validate_frequency(p)
    return phi + eta * (2.0 * p - 1.0)


def replicator_rhs(p: float, phi: float, eta: float) -> float:
    """Two-strategy replicator vector field."""

    _validate_frequency(p)
    return p * (1.0 - p) * payoff_gap(p, phi, eta)


def interior_equilibrium(phi: float, eta: float, tol: float = 1e-12) -> Optional[float]:
    """Return the strict interior equilibrium, otherwise None."""

    if abs(eta) <= tol:
        return None
    p_star = 0.5 * (1.0 - phi / eta)
    if tol < p_star < 1.0 - tol:
        return p_star
    return None


def classify_phase(phi: float, eta: float, tol: float = 1e-12) -> str:
    """Classify the deterministic replicator phase."""

    if abs(eta) <= tol:
        if phi < -tol:
            return "shared_dominance"
        if phi > tol:
            return "differentiated_dominance"
        return "neutral_architecture_boundary"

    h = abs(eta)
    if phi < -h - tol:
        return "shared_dominance"
    if phi > h + tol:
        return "differentiated_dominance"
    if abs(phi + h) <= tol or abs(phi - h) <= tol:
        return "nonhyperbolic_phase_boundary"

    if eta < 0:
        return "stable_architecture_coexistence"
    return "coordination_bistability"


def pure_ess(phi: float, eta: float) -> Tuple[bool, bool]:
    """Return strict ESS flags (S_is_ESS, D_is_ESS)."""

    s_ess = payoff_gap(0.0, phi, eta) < 0.0
    d_ess = payoff_gap(1.0, phi, eta) > 0.0
    return s_ess, d_ess


def switching_hysteresis_band(
    c_sd: float, c_ds: float, horizon: float
) -> Tuple[float, float]:
    """Return lower/upper Delta bounds in which either inherited state can persist."""

    if c_sd < 0 or c_ds < 0:
        raise ValueError("switching costs must be non-negative")
    if horizon <= 0:
        raise ValueError("horizon must be positive")
    return -c_ds / horizon, c_sd / horizon


def switching_action(
    current: str,
    p: float,
    phi: float,
    eta: float,
    c_sd: float,
    c_ds: float,
    horizon: float,
) -> str:
    """Return 'S' or 'D' under strict payoff-improvement switching."""

    if current not in {"S", "D"}:
        raise ValueError("current must be 'S' or 'D'")
    lower, upper = switching_hysteresis_band(c_sd, c_ds, horizon)
    delta = payoff_gap(p, phi, eta)
    if current == "S" and delta > upper:
        return "D"
    if current == "D" and delta < lower:
        return "S"
    return current


def _validate_bridge(
    conflict_load: float, separation_fraction: float, architecture_cost: float
) -> None:
    if conflict_load < 0:
        raise ValueError("conflict_load must be non-negative")
    if not 0.0 <= separation_fraction <= 1.0:
        raise ValueError("separation_fraction must lie in [0,1]")
    if architecture_cost < 0:
        raise ValueError("architecture_cost must be non-negative")


def _validate_frequency(p: float) -> None:
    if not 0.0 <= p <= 1.0:
        raise ValueError("p must lie in [0,1]")
