"""Global (alpha,gamma) phase diagram for quadratic continuous PAYOFF architectures."""

from __future__ import annotations

from typing import Tuple


def branching_feedback_threshold(curvature: float) -> float:
    """Return gamma_c=-kappa/2."""

    if curvature <= 0.0:
        raise ValueError("curvature must be positive")
    return -0.5 * curvature


def strong_feedback_alpha_boundaries(
    max_recovery: float, curvature: float, gamma: float
) -> Tuple[float, float]:
    """Return (alpha_S,alpha_D) for gamma<-kappa/2."""

    if max_recovery <= 0.0:
        raise ValueError("max_recovery must be positive")
    if curvature <= 0.0:
        raise ValueError("curvature must be positive")
    if gamma >= -0.5 * curvature:
        raise ValueError("requires gamma<-curvature/2")
    lower = 0.5 * (curvature + 2.0 * gamma) * max_recovery
    upper = 0.5 * (curvature - 2.0 * gamma) * max_recovery
    return lower, upper


def endpoint_polymorphism_width(
    max_recovery: float, curvature: float, gamma: float
) -> float:
    """Return alpha_D-alpha_S=2|gamma|L in the strong-feedback region."""

    lower, upper = strong_feedback_alpha_boundaries(
        max_recovery, curvature, gamma
    )
    return upper - lower


def endpoint_polymorphism_midpoint(max_recovery: float, curvature: float) -> float:
    """Return invariant alpha midpoint kappa*L/2."""

    if max_recovery <= 0.0:
        raise ValueError("max_recovery must be positive")
    if curvature <= 0.0:
        raise ValueError("curvature must be positive")
    return 0.5 * curvature * max_recovery


def classify_global_phase(
    alpha: float,
    max_recovery: float,
    curvature: float,
    gamma: float,
    tol: float = 1e-12,
) -> str:
    """Classify the exact quadratic continuous architecture phase."""

    if max_recovery <= 0.0:
        raise ValueError("max_recovery must be positive")
    if curvature <= 0.0:
        raise ValueError("curvature must be positive")
    threshold = -0.5 * curvature

    if gamma > threshold + tol:
        if alpha <= tol:
            return "shared_monomorph"
        if alpha >= curvature * max_recovery - tol:
            return "full_monomorph"
        return "partial_monomorph"

    if gamma >= threshold - tol:
        if alpha <= tol:
            return "shared_endpoint"
        if alpha >= curvature * max_recovery - tol:
            return "full_endpoint"
        return "neutral_variance_manifold"

    lower, upper = strong_feedback_alpha_boundaries(
        max_recovery, curvature, gamma
    )
    if alpha <= lower + tol:
        return "shared_endpoint"
    if alpha >= upper - tol:
        return "full_endpoint"
    return "endpoint_polymorphism"


def endpoint_frequency_from_alpha(
    alpha: float,
    max_recovery: float,
    curvature: float,
    gamma: float,
) -> float:
    """Return clipped differentiated endpoint frequency in strong-feedback region."""

    strong_feedback_alpha_boundaries(max_recovery, curvature, gamma)
    numerator = 2.0 * alpha - (curvature + 2.0 * gamma) * max_recovery
    denominator = -4.0 * gamma * max_recovery
    return max(0.0, min(1.0, numerator / denominator))
