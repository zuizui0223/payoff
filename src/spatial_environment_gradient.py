"""Common environmental-gradient transform for heterogeneous PAYOFF landscapes.

Patch static gaps shift with one common environmental slope:
    phi_j(e)=phi0_j + alpha*(e-e0).
Local eta_j and the migration graph are held fixed.

Because a common shift adds a scalar multiple of the identity to each rare-type
invasion operator, the metapopulation invasion exponents and environmental
thresholds have exact closed forms.
"""

from __future__ import annotations

from math import hypot, isfinite
from typing import Dict, Sequence, Tuple

from src.environment_mosaic import invasion_exponent, invasion_margins
from src.numerical_tolerance import DEFAULT_RELATIVE_TOL, relative_band


def environmental_phis(
    base_phis: Sequence[float], environment: float, reference_environment: float, slope: float
) -> list[float]:
    """Return phi_j(e)=phi0_j+slope*(e-e0)."""

    shift = slope * (environment - reference_environment)
    return [phi + shift for phi in base_phis]


def environmental_invasion_exponents(
    base_phis: Sequence[float],
    etas: Sequence[float],
    adjacency: Sequence[Sequence[float]],
    migration_rate: float,
    environment: float,
    reference_environment: float,
    slope: float,
) -> Tuple[float, float]:
    """Return exact (Lambda_D,Lambda_S) under a common environmental shift."""

    shifted = environmental_phis(base_phis, environment, reference_environment, slope)
    d_margins, s_margins = invasion_margins(shifted, etas)
    return (
        invasion_exponent(d_margins, adjacency, migration_rate),
        invasion_exponent(s_margins, adjacency, migration_rate),
    )


def baseline_spatial_exponents(
    base_phis: Sequence[float],
    etas: Sequence[float],
    adjacency: Sequence[Sequence[float]],
    migration_rate: float,
) -> Tuple[float, float]:
    """Return (Lambda_D0,Lambda_S0) at the reference environment."""

    d_margins, s_margins = invasion_margins(base_phis, etas)
    return (
        invasion_exponent(d_margins, adjacency, migration_rate),
        invasion_exponent(s_margins, adjacency, migration_rate),
    )


def critical_environments(
    base_phis: Sequence[float],
    etas: Sequence[float],
    adjacency: Sequence[Sequence[float]],
    migration_rate: float,
    reference_environment: float,
    slope: float,
) -> Tuple[float, float]:
    """Return (e_D,e_S), the rare-D and rare-S neutral environments.

    With Lambda_D(e)=Lambda_D0+alpha(e-e0),
         Lambda_S(e)=Lambda_S0-alpha(e-e0),

        e_D=e0-Lambda_D0/alpha,
        e_S=e0+Lambda_S0/alpha.
    """

    if slope == 0.0:
        raise ValueError("slope must be non-zero")
    lambda_d0, lambda_s0 = baseline_spatial_exponents(
        base_phis, etas, adjacency, migration_rate
    )
    return (
        reference_environment - lambda_d0 / slope,
        reference_environment + lambda_s0 / slope,
    )


def signed_reciprocal_environment_width(
    base_phis: Sequence[float],
    etas: Sequence[float],
    adjacency: Sequence[Sequence[float]],
    migration_rate: float,
    slope: float,
) -> float:
    """Return e_S-e_D.

    For slope>0:
      positive -> reciprocal-invasion interval,
      negative -> mutual-non-invasion coordination interval,
      zero     -> one common spatial transition.
    """

    if slope == 0.0:
        raise ValueError("slope must be non-zero")
    lambda_d0, lambda_s0 = baseline_spatial_exponents(
        base_phis, etas, adjacency, migration_rate
    )
    return (lambda_d0 + lambda_s0) / slope


def strong_migration_thresholds(
    base_phis: Sequence[float],
    etas: Sequence[float],
    reference_environment: float,
    slope: float,
) -> Tuple[float, float]:
    """Return limiting (e_D,e_S) as symmetric migration -> infinity.

    The principal exponents approach mean(phi0-eta) and mean(-phi0-eta).
    """

    if not base_phis or len(base_phis) != len(etas):
        raise ValueError("base_phis and etas must have the same non-zero length")
    if slope == 0.0:
        raise ValueError("slope must be non-zero")
    mean_phi = sum(base_phis) / len(base_phis)
    mean_eta = sum(etas) / len(etas)
    lambda_d = mean_phi - mean_eta
    lambda_s = -mean_phi - mean_eta
    return (
        reference_environment - lambda_d / slope,
        reference_environment + lambda_s / slope,
    )


def no_frequency_feedback_zero_migration_window(
    base_phis: Sequence[float], slope: float
) -> float:
    """Environmental reciprocal-invasion width at m=0 when eta_j=0.

    For slope>0 this is [max(phi0)-min(phi0)]/slope.
    """

    if not base_phis:
        raise ValueError("base_phis cannot be empty")
    if slope == 0.0:
        raise ValueError("slope must be non-zero")
    return (max(base_phis) - min(base_phis)) / slope


def common_eta_zero_migration_signed_width(
    base_phis: Sequence[float], eta: float, slope: float
) -> float:
    """Return signed reciprocal width at m=0 for one common eta.

    W(0)=[range(phi0)-2eta]/slope.
    """

    if not base_phis:
        raise ValueError("base_phis cannot be empty")
    if slope == 0.0:
        raise ValueError("slope must be non-zero")
    return (max(base_phis) - min(base_phis) - 2.0 * eta) / slope


def common_eta_window_switch_rate(
    base_phis: Sequence[float],
    eta: float,
    adjacency: Sequence[Sequence[float]],
    tol: float = 1e-10,
    max_iterations: int = 200,
) -> float:
    """Migration rate where a reciprocal environmental window collapses.

    Requires a connected graph, common eta>0, and range(phi0)>2eta. Under these
    conditions F(m)=Lambda_D(m)+Lambda_S(m) decreases strictly from
    range(phi0)-2eta>0 to -2eta<0, so one positive crossing exists.

    The root is solved in dimensionless coordinates
        phi'=phi/r_scale, eta'=eta/r_scale,
        W'=W/w_scale, mu=m*w_scale/r_scale,
    and converted back only after convergence.
    """

    if eta <= 0.0:
        raise ValueError("eta must be positive")
    if max_iterations <= 0:
        raise ValueError("max_iterations must be positive")
    _validate_connected_adjacency(adjacency)
    if len(base_phis) != len(adjacency) or not base_phis:
        raise ValueError("one base phi is required per patch")

    numeric_phis = [float(value) for value in base_phis]
    numeric_eta = float(eta)
    relative_band(tuple(numeric_phis) + (numeric_eta,), tol)
    if max(numeric_phis) - min(numeric_phis) <= 2.0 * numeric_eta:
        raise ValueError("requires range(base_phis) > 2 eta")

    rate_scale = max(max(abs(value) for value in numeric_phis), abs(numeric_eta))
    graph_scale = max(abs(float(value)) for row in adjacency for value in row)
    if graph_scale == 0.0:
        raise ValueError("window-switch theorem requires positive graph weights")

    normalized_phis = tuple(value / rate_scale for value in numeric_phis)
    normalized_eta = numeric_eta / rate_scale
    normalized_adjacency = tuple(
        tuple(float(value) / graph_scale for value in row) for row in adjacency
    )
    normalized_etas = (normalized_eta,) * len(normalized_phis)

    def signed_sum(mu: float) -> float:
        lambda_d, lambda_s = baseline_spatial_exponents(
            normalized_phis, normalized_etas, normalized_adjacency, mu
        )
        return lambda_d + lambda_s

    lower = 0.0
    upper = 1.0
    for _ in range(max_iterations):
        if signed_sum(upper) <= 0.0:
            break
        upper *= 2.0
        if not isfinite(upper):
            raise RuntimeError("failed to bracket dimensionless environmental window switch")
    else:
        raise RuntimeError("failed to bracket dimensionless environmental window switch")

    for _ in range(max_iterations):
        mid = 0.5 * (lower + upper)
        value = signed_sum(mid)
        width_band = relative_band((lower, upper), tol)
        if abs(value) <= tol or upper - lower <= width_band:
            return mid * rate_scale / graph_scale
        if value > 0.0:
            lower = mid
        else:
            upper = mid
    return 0.5 * (lower + upper) * rate_scale / graph_scale


def two_patch_midpoint_exponent(
    phi_1: float, phi_2: float, eta: float, migration_rate: float
) -> float:
    """Reciprocal D/S invasion exponent at the mean-static-gap environment.

    After a common environmental shift makes the two patch gaps
        +Delta_phi/2 and -Delta_phi/2,
    both reciprocal architecture invasion exponents equal
        -eta-m + hypot(Delta_phi/2,m).
    """

    if eta <= 0.0:
        raise ValueError("eta must be positive for the coordination-switch theorem")
    if migration_rate < 0.0:
        raise ValueError("migration_rate must be non-negative")
    delta_phi = phi_1 - phi_2
    return -eta - migration_rate + hypot(0.5 * delta_phi, migration_rate)


def two_patch_coordination_switch_rate(phi_1: float, phi_2: float, eta: float) -> float:
    """Exact migration rate where reciprocal invasion becomes mutual non-invasion.

    Requires eta>0 and |phi1-phi2|>2eta.  The standard squared expression is
    evaluated through the dimensionless ratio z=2eta/|Delta_phi|:
        m_switch=|Delta_phi| (1-z)(1+z)/(4z).
    """

    if eta <= 0.0:
        raise ValueError("eta must be positive")
    delta = abs(phi_1 - phi_2)
    twice_eta = 2.0 * eta
    if delta <= twice_eta:
        raise ValueError("requires |phi_1-phi_2| > 2 eta")
    z = twice_eta / delta
    if z == 0.0:
        return float("inf")
    return delta * ((1.0 - z) * (1.0 + z) / (4.0 * z))


def classify_two_patch_midpoint(
    phi_1: float,
    phi_2: float,
    eta: float,
    migration_rate: float,
    tol: float = DEFAULT_RELATIVE_TOL,
) -> str:
    """Classify reciprocal landscape invasibility at the mean-static-gap environment.

    ``tol`` is dimensionless.  The numerical boundary band is set relative to
    the commensurate rate terms ``Delta_phi/2``, ``eta``, and migration, so a
    common payoff baseline or a common rate-unit rescaling cannot change the
    phase label.
    """

    delta_phi = float(phi_1) - float(phi_2)
    numeric_eta = float(eta)
    numeric_migration = float(migration_rate)
    band = relative_band((0.5 * delta_phi, numeric_eta, numeric_migration), tol)
    value = two_patch_midpoint_exponent(
        float(phi_1), float(phi_2), numeric_eta, numeric_migration
    )
    if value > band:
        return "reciprocal_spatial_invasion"
    if value < -band:
        return "mutual_spatial_noninvasion"
    return "spatial_coordination_switch_boundary"


def spatial_environment_summary(
    base_phis: Sequence[float],
    etas: Sequence[float],
    adjacency: Sequence[Sequence[float]],
    migration_rate: float,
    reference_environment: float,
    slope: float,
) -> Dict[str, float]:
    """Return the main spatial environmental threshold diagnostics."""

    lambda_d0, lambda_s0 = baseline_spatial_exponents(
        base_phis, etas, adjacency, migration_rate
    )
    e_d, e_s = critical_environments(
        base_phis,
        etas,
        adjacency,
        migration_rate,
        reference_environment,
        slope,
    )
    return {
        "lambda_d_reference": lambda_d0,
        "lambda_s_reference": lambda_s0,
        "environment_d_neutral": e_d,
        "environment_s_neutral": e_s,
        "signed_reciprocal_width": e_s - e_d,
    }


def _validate_connected_adjacency(adjacency: Sequence[Sequence[float]]) -> None:
    n = len(adjacency)
    if n == 0 or any(len(row) != n for row in adjacency):
        raise ValueError("adjacency must be non-empty and square")
    numeric = [[float(adjacency[i][j]) for j in range(n)] for i in range(n)]
    for row in numeric:
        for value in row:
            relative_band((value,))
            if value < 0.0:
                raise ValueError("adjacency weights must be non-negative")
    for i in range(n):
        for j in range(i + 1, n):
            left = numeric[i][j]
            right = numeric[j][i]
            if abs(left - right) > relative_band((left, right)):
                raise ValueError("adjacency must be symmetric")
    seen = {0}
    stack = [0]
    while stack:
        i = stack.pop()
        for j, weight in enumerate(numeric[i]):
            if weight > 0.0 and j not in seen:
                seen.add(j)
                stack.append(j)
    if len(seen) != n:
        raise ValueError("adjacency must be connected")
