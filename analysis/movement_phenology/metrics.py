"""Dimensionless movement–phenology matching metrics.

These functions encode the empirical analogue used by the PAYOFF-B macro programme.
They do not assert that observed front-speed ratios are literally equal to m*tau in
all biological systems.
"""

from __future__ import annotations

import math


WEAK_CONTRAST_U_LIMIT = 1.60611529880277
STRONG_CONTRAST_U_LIMIT = 1.0


def speed_ratio(animal_speed: float, environment_speed: float) -> float:
    """Return animal/environment front-speed ratio on a common spatial scale."""
    a = float(animal_speed)
    e = float(environment_speed)
    if not math.isfinite(a) or not math.isfinite(e):
        raise ValueError("speeds must be finite")
    if a <= 0.0 or e <= 0.0:
        raise ValueError("speeds must be strictly positive")
    return a / e


def log_speed_ratio(animal_speed: float, environment_speed: float) -> float:
    """Return log of the positive dimensionless speed ratio."""
    return math.log(speed_ratio(animal_speed, environment_speed))


def directional_alignment(animal_angle_rad: float, environment_angle_rad: float) -> float:
    """Cosine alignment of two velocity directions, in [-1, 1]."""
    a = float(animal_angle_rad)
    e = float(environment_angle_rad)
    if not math.isfinite(a) or not math.isfinite(e):
        raise ValueError("angles must be finite")
    return math.cos(a - e)


def directional_alignment_degrees(animal_angle_deg: float, environment_angle_deg: float) -> float:
    """Cosine alignment when source angles are stored in degrees."""
    a = float(animal_angle_deg)
    e = float(environment_angle_deg)
    if not math.isfinite(a) or not math.isfinite(e):
        raise ValueError("angles must be finite")
    return math.cos(math.radians(a - e))


def normalized_vector_mismatch(
    animal_speed: float,
    environment_speed: float,
    animal_angle_rad: float,
    environment_angle_rad: float,
) -> float:
    """Return |v_animal-v_environment| / |v_environment|."""
    u = speed_ratio(animal_speed, environment_speed)
    align = directional_alignment(animal_angle_rad, environment_angle_rad)
    value = 1.0 + u * u - 2.0 * u * align
    return math.sqrt(max(0.0, value))


def quadratic_optimum(beta_linear: float, beta_quadratic: float) -> tuple[float, float]:
    """Return (q*, exp(q*)) for a convex beta1*q + beta2*q^2 response."""
    b1 = float(beta_linear)
    b2 = float(beta_quadratic)
    if not math.isfinite(b1) or not math.isfinite(b2):
        raise ValueError("coefficients must be finite")
    if b2 <= 0.0:
        raise ValueError("quadratic coefficient must be positive for a finite minimum")
    q_star = -b1 / (2.0 * b2)
    return q_star, math.exp(q_star)


def payoff_b_reference_interval() -> tuple[float, float]:
    """Return theorem endpoint constants for descriptive reference only."""
    return STRONG_CONTRAST_U_LIMIT, WEAK_CONTRAST_U_LIMIT
