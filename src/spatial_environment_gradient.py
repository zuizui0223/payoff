"""Common environmental-gradient transform for heterogeneous PAYOFF landscapes.

Patch static gaps shift with one common environmental slope:
    phi_j(e)=phi0_j + alpha*(e-e0).
Local eta_j and the migration graph are held fixed.

Because a common shift adds a scalar multiple of the identity to each rare-type
invasion operator, the metapopulation invasion exponents and environmental
thresholds have exact closed forms.
"""

from __future__ import annotations

from typing import Dict, Sequence, Tuple

from src.environment_mosaic import invasion_exponent, invasion_margins


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
