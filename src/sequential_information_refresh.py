"""Sequential information refresh for prospective PAYOFF-B theory.

For a standardized Markov chain with local correlations rho_j,

    Corr(X_i, X_k) = product(rho_i, ..., rho_{k-1}).

A later checkpoint observation removes upstream correlation factors from the
remaining forecast horizon.  This module records that exact reduced geometry.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Sequence


@dataclass(frozen=True)
class RefreshPoint:
    checkpoint: int
    remaining_predictability: float
    observation_reliability: float
    predictive_information: float
    retained_actionability: float
    usable_information: float


def _valid_rhos(rhos: Sequence[float]) -> tuple[float, ...]:
    out = tuple(float(value) for value in rhos)
    if not out:
        raise ValueError("at least one route correlation is required")
    for value in out:
        if not isfinite(value) or abs(value) > 1.0:
            raise ValueError("route correlations must be finite and lie in [-1, 1]")
    return out


def direct_predictability(rhos: Sequence[float]) -> float:
    """Absolute origin-to-destination correlation in the Markov chain."""

    values = _valid_rhos(rhos)
    product = 1.0
    for value in values:
        product *= value
    return abs(product)


def checkpoint_predictability(
    rhos: Sequence[float],
    checkpoint: int,
) -> float:
    """Absolute correlation from checkpoint state to final state.

    checkpoint=0 recovers direct_predictability.
    checkpoint=len(rhos) represents observation at the destination itself and
    therefore has remaining state correlation one.
    """

    values = _valid_rhos(rhos)
    m = int(checkpoint)
    if m < 0 or m > len(values):
        raise ValueError("checkpoint must lie between 0 and len(rhos)")
    product = 1.0
    for value in values[m:]:
        product *= value
    return abs(product)


def noisy_predictive_information(
    rhos: Sequence[float],
    checkpoint: int,
    *,
    observation_noise_variance: float,
) -> float:
    """Squared destination-predictive correlation of a noisy checkpoint cue."""

    noise = float(observation_noise_variance)
    if not isfinite(noise) or noise < 0.0:
        raise ValueError("observation_noise_variance must be finite and non-negative")
    q = checkpoint_predictability(rhos, checkpoint)
    reliability = 1.0 / (1.0 + noise)
    return reliability * q * q


def refresh_path(
    rhos: Sequence[float],
    *,
    observation_noise_variances: Sequence[float],
    retained_actionability: Sequence[float],
) -> tuple[RefreshPoint, ...]:
    """Return sequential prediction and usable-information coordinates.

    One observation/noise and one actionability value are required for every
    checkpoint from 0 through the final state.
    """

    values = _valid_rhos(rhos)
    expected = len(values) + 1
    noises = tuple(float(v) for v in observation_noise_variances)
    recourse = tuple(float(v) for v in retained_actionability)
    if len(noises) != expected or len(recourse) != expected:
        raise ValueError("noise and actionability paths must have len(rhos)+1 values")

    out = []
    for checkpoint, (noise, r) in enumerate(zip(noises, recourse)):
        if not isfinite(noise) or noise < 0.0:
            raise ValueError("noise variances must be finite and non-negative")
        if not isfinite(r) or not 0.0 <= r <= 1.0:
            raise ValueError("retained_actionability must lie in [0, 1]")
        q = checkpoint_predictability(values, checkpoint)
        reliability = 1.0 / (1.0 + noise)
        info = reliability * q * q
        out.append(
            RefreshPoint(
                checkpoint=checkpoint,
                remaining_predictability=q,
                observation_reliability=reliability,
                predictive_information=info,
                retained_actionability=r,
                usable_information=r * info,
            )
        )
    return tuple(out)
