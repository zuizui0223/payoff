"""Grid-refinement certificates for interaction-kernel accessibility barriers.

Finite-grid critical jump distances can represent either a genuine positive
continuum bottleneck or merely the one-bin resolution of an otherwise locally
accessible profile.  This module repeats the same resident accessibility audit
across increasingly fine regular grids and reports the tail envelope.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Sequence

from src.architecture_phase_atlas import regular_grid
from src.interaction_kernel_robustness import kernel_accessibility


@dataclass(frozen=True)
class BarrierResolutionCertificate:
    kernel: str
    gamma: float
    epsilon: float
    bins: tuple[int, ...]
    critical_jump_bins: tuple[int, ...]
    critical_jump_distances: tuple[float, ...]
    tail_lower: float
    tail_upper: float
    tail_spread: float
    finest_grid_step: float
    positive_barrier_resolved: bool
    resolution_limited: bool


def barrier_resolution_certificate(
    *,
    kernel: str,
    gamma: float,
    epsilon: float,
    alpha: float = 0.5,
    kappa: float = 1.0,
    length: float = 1.0,
    bins: Sequence[int] = (321, 641, 1281),
    tail_tolerance: float = 0.005,
) -> BarrierResolutionCertificate:
    """Audit critical jump distance over a prospectively declared grid sequence.

    ``positive_barrier_resolved`` requires a stable tail envelope whose lower
    edge exceeds two finest-grid cells.  ``resolution_limited`` means every
    audited grid is one-bin accessible, so the apparent critical distance
    shrinks exactly with numerical resolution rather than supporting a positive
    continuum bottleneck.
    """
    b = tuple(int(n) for n in bins)
    if len(b) < 2 or any(n < 3 for n in b) or any(y <= x for x, y in zip(b, b[1:])):
        raise ValueError("bins must be a strictly increasing sequence >= 3")
    if not isfinite(float(tail_tolerance)) or tail_tolerance < 0.0:
        raise ValueError("tail_tolerance must be finite and non-negative")

    critical_bins = []
    distances = []
    for n in b:
        grid = regular_grid(length, n)
        result = kernel_accessibility(
            grid,
            alpha=alpha,
            kappa=kappa,
            gamma=gamma,
            epsilon=epsilon,
            kernel=kernel,
            start_index=0,
        )
        critical_bins.append(result.critical_jump_bins)
        distances.append(result.critical_jump_distance)

    tail_lower = min(distances)
    tail_upper = max(distances)
    spread = tail_upper - tail_lower
    finest_step = float(length) / (b[-1] - 1)
    resolution_limited = all(value <= 1 for value in critical_bins)
    positive = (
        not resolution_limited
        and spread <= float(tail_tolerance) + 1e-15
        and tail_lower > 2.0 * finest_step
    )
    return BarrierResolutionCertificate(
        kernel=str(kernel).lower(),
        gamma=float(gamma),
        epsilon=float(epsilon),
        bins=b,
        critical_jump_bins=tuple(critical_bins),
        critical_jump_distances=tuple(distances),
        tail_lower=tail_lower,
        tail_upper=tail_upper,
        tail_spread=spread,
        finest_grid_step=finest_step,
        positive_barrier_resolved=positive,
        resolution_limited=resolution_limited,
    )
