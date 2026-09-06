"""Spatial/metapopulation extension of the PAYOFF architecture game.

Each patch j carries a differentiated-architecture frequency p_j in [0,1].
Local selection follows the deterministic PAYOFF game

    f(p)=p(1-p)[phi+eta(2p-1)],

while symmetric migration on an undirected weighted graph follows

    dp_j/dt = f(p_j) + m sum_k w_jk (p_k-p_j).

The module is dependency-free. Spectral results accept Laplacian eigenvalues
computed externally when needed.
"""

from __future__ import annotations

from math import sqrt
from typing import Dict, List, Optional, Sequence, Tuple


def selection_rhs(p: float, phi: float, eta: float) -> float:
    """Local PAYOFF replicator vector field."""

    _validate_frequency(p)
    return p * (1.0 - p) * (phi + eta * (2.0 * p - 1.0))


def selection_derivative(p: float, phi: float, eta: float) -> float:
    """Derivative f'(p) of the local selection field."""

    _validate_frequency(p)
    gap = phi + eta * (2.0 * p - 1.0)
    return (1.0 - 2.0 * p) * gap + 2.0 * eta * p * (1.0 - p)


def spatial_moments(frequencies: Sequence[float]) -> Tuple[float, float, float]:
    """Return (mean, variance, third central moment) across patches."""

    if not frequencies:
        raise ValueError("frequencies cannot be empty")
    for p in frequencies:
        _validate_frequency(p)
    n = len(frequencies)
    mean = sum(frequencies) / n
    variance = sum((p - mean) ** 2 for p in frequencies) / n
    third = sum((p - mean) ** 3 for p in frequencies) / n
    return mean, variance, third


def spatial_selection_coefficients(frequencies: Sequence[float]) -> Dict[str, float]:
    """Return exact coefficients A,B in mean selection = phi*A + eta*B.

    A=E[p(1-p)] is non-negative and measures the amount of within-patch
    polymorphism available for selection to act on. B=E[p(1-p)(2p-1)] is the
    frequency-feedback coefficient after spatial aggregation.
    """

    mu, variance, third = spatial_moments(frequencies)
    a_direct = sum(p * (1.0 - p) for p in frequencies) / len(frequencies)
    b_direct = sum(
        p * (1.0 - p) * (2.0 * p - 1.0) for p in frequencies
    ) / len(frequencies)
    a_moments = mu * (1.0 - mu) - variance
    b_moments = (
        mu * (1.0 - mu) * (2.0 * mu - 1.0)
        + variance * (3.0 - 6.0 * mu)
        - 2.0 * third
    )
    return {
        "mean_frequency": mu,
        "variance": variance,
        "third_central_moment": third,
        "A": a_direct,
        "B": b_direct,
        "A_from_moments": a_moments,
        "B_from_moments": b_moments,
    }


def aggregated_zero_growth_phi(
    frequencies: Sequence[float], eta: float, tol: float = 1e-15
) -> Optional[float]:
    """Return phi for zero instantaneous metapopulation mean change.

    Since d(mean p)/dt = phi*A + eta*B under symmetric conservative
    migration, the zero-growth value is phi=-eta*B/A whenever A>0.
    If A=0, every patch is at p=0 or p=1 and local selection is instantaneously
    zero for all phi,eta, so no unique zero-growth phi exists and None is
    returned.
    """

    coeffs = spatial_selection_coefficients(frequencies)
    a = coeffs["A"]
    if abs(a) <= tol:
        return None
    return -eta * coeffs["B"] / a


def infer_phi_from_spatial_mean_change(
    frequencies: Sequence[float], mean_change: float, eta: float, tol: float = 1e-15
) -> float:
    """Infer phi from short-term mean change when eta and patch frequencies are known.

    Uses mean_change=phi*A+eta*B. This is an algebraic identity for the
    deterministic conservative-migration model, not a statistical estimator
    with sampling error built in.
    """

    coeffs = spatial_selection_coefficients(frequencies)
    a = coeffs["A"]
    if abs(a) <= tol:
        raise ValueError("phi is not identifiable when A=0")
    return (mean_change - eta * coeffs["B"]) / a


def infer_eta_from_spatial_mean_change(
    frequencies: Sequence[float], mean_change: float, phi: float, tol: float = 1e-15
) -> float:
    """Infer eta from short-term mean change when phi and patch frequencies are known."""

    coeffs = spatial_selection_coefficients(frequencies)
    b = coeffs["B"]
    if abs(b) <= tol:
        raise ValueError("eta is not identifiable when B=0")
    return (mean_change - phi * coeffs["A"]) / b


def mean_selection_decomposition(
    frequencies: Sequence[float], phi: float, eta: float
) -> Dict[str, float]:
    """Exact decomposition of mean local selection across patches.

    If mu is the patch mean, V the variance and T the third central moment,

        mean_j f(p_j)
        = f(mu) + V[eta(3-6mu)-phi] - 2 eta T.
    """

    mu, variance, third = spatial_moments(frequencies)
    direct = sum(selection_rhs(p, phi, eta) for p in frequencies) / len(frequencies)
    well_mixed = selection_rhs(mu, phi, eta)
    correction = variance * (eta * (3.0 - 6.0 * mu) - phi) - 2.0 * eta * third
    return {
        "mean_frequency": mu,
        "variance": variance,
        "third_central_moment": third,
        "mean_selection": direct,
        "well_mixed_selection": well_mixed,
        "spatial_correction": correction,
        "reconstructed_mean_selection": well_mixed + correction,
    }


def network_rhs(
    frequencies: Sequence[float],
    adjacency: Sequence[Sequence[float]],
    migration_rate: float,
    phi: float,
    eta: float,
) -> List[float]:
    """Return spatial PAYOFF dynamics on a symmetric weighted patch graph."""

    _validate_network(frequencies, adjacency, migration_rate)
    out: List[float] = []
    for i, p_i in enumerate(frequencies):
        migration = 0.0
        for j, weight in enumerate(adjacency[i]):
            migration += weight * (frequencies[j] - p_i)
        out.append(selection_rhs(p_i, phi, eta) + migration_rate * migration)
    return out


def mean_network_rhs(
    frequencies: Sequence[float],
    adjacency: Sequence[Sequence[float]],
    migration_rate: float,
    phi: float,
    eta: float,
) -> float:
    """Return d(mean p)/dt; symmetric migration cancels exactly."""

    rhs = network_rhs(frequencies, adjacency, migration_rate, phi, eta)
    return sum(rhs) / len(rhs)


def synchronous_mode_rates(
    p_star: float,
    phi: float,
    eta: float,
    migration_rate: float,
    laplacian_eigenvalues: Sequence[float],
) -> List[float]:
    """Linear growth rates around a synchronous equilibrium.

    For graph Laplacian eigenvalue lambda_k,

        r_k = f'(p*) - m lambda_k.

    The zero Laplacian eigenvalue is the spatially uniform mode.
    """

    _validate_frequency(p_star)
    if migration_rate < 0.0:
        raise ValueError("migration_rate must be non-negative")
    if not laplacian_eigenvalues:
        raise ValueError("laplacian_eigenvalues cannot be empty")
    if any(value < -1e-12 for value in laplacian_eigenvalues):
        raise ValueError("Laplacian eigenvalues must be non-negative")
    fp = selection_derivative(p_star, phi, eta)
    return [fp - migration_rate * max(0.0, value) for value in laplacian_eigenvalues]


def synchronization_threshold(
    p_star: float, phi: float, eta: float, algebraic_connectivity: float
) -> float:
    """Migration rate needed to damp the slowest transverse graph mode.

    If f'(p*)<=0, transverse perturbations already decay and the threshold is
    zero. Otherwise m_sync=f'(p*)/lambda_2.
    """

    if algebraic_connectivity <= 0.0:
        raise ValueError("algebraic_connectivity must be positive")
    fp = selection_derivative(p_star, phi, eta)
    return max(0.0, fp / algebraic_connectivity)


def two_patch_polarized_equilibria(
    eta: float, migration_rate: float
) -> Optional[Tuple[float, float]]:
    """Exact polarized equilibria for phi=0 on two unit-coupled patches.

    Dynamics are
        dp1/dt=f(p1)+m(p2-p1)
        dp2/dt=f(p2)+m(p1-p2)
    with eta>0. On the invariant anti-symmetric manifold
        p1=1/2+x, p2=1/2-x,
    nonzero equilibria exist iff m<eta/4 and satisfy
        x^2=1/4-m/eta.
    """

    if eta <= 0.0:
        raise ValueError("eta must be positive for coordination polarization")
    if migration_rate < 0.0:
        raise ValueError("migration_rate must be non-negative")
    if migration_rate >= eta / 4.0:
        return None
    x = sqrt(0.25 - migration_rate / eta)
    return 0.5 - x, 0.5 + x


def two_patch_polarized_eigenvalues(
    eta: float, migration_rate: float
) -> Optional[Tuple[float, float]]:
    """Return (uniform_mode, transverse_mode) rates at polarized equilibria.

    For phi=0 and m<eta/4:
        r_uniform    = 6m-eta
        r_transverse = 4m-eta.
    """

    if two_patch_polarized_equilibria(eta, migration_rate) is None:
        return None
    return 6.0 * migration_rate - eta, 4.0 * migration_rate - eta


def classify_two_patch_polarization(eta: float, migration_rate: float, tol: float = 1e-12) -> str:
    """Classify the exact two-patch polarized branch for phi=0, eta>0."""

    if eta <= 0.0:
        raise ValueError("eta must be positive")
    if migration_rate < 0.0:
        raise ValueError("migration_rate must be non-negative")
    stable_cut = eta / 6.0
    existence_cut = eta / 4.0
    if migration_rate < stable_cut - tol:
        return "stable_polarized_patches"
    if abs(migration_rate - stable_cut) <= tol:
        return "polarized_stability_boundary"
    if migration_rate < existence_cut - tol:
        return "polarized_saddle"
    if abs(migration_rate - existence_cut) <= tol:
        return "polarization_pitchfork_boundary"
    return "no_polarized_equilibrium"


def _validate_network(
    frequencies: Sequence[float],
    adjacency: Sequence[Sequence[float]],
    migration_rate: float,
) -> None:
    if not frequencies:
        raise ValueError("frequencies cannot be empty")
    n = len(frequencies)
    if len(adjacency) != n or any(len(row) != n for row in adjacency):
        raise ValueError("adjacency must be square with one row per patch")
    if migration_rate < 0.0:
        raise ValueError("migration_rate must be non-negative")
    for p in frequencies:
        _validate_frequency(p)
    for i in range(n):
        for j in range(n):
            if adjacency[i][j] < 0.0:
                raise ValueError("adjacency weights must be non-negative")
            if abs(adjacency[i][j] - adjacency[j][i]) > 1e-12:
                raise ValueError("adjacency must be symmetric for mean-conserving migration")


def _validate_frequency(p: float) -> None:
    if not 0.0 <= p <= 1.0:
        raise ValueError("frequency must lie in [0,1]")
