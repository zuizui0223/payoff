"""Kernel-family robustness envelope for local architecture accessibility."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from src.interaction_kernel_robustness import (
    KernelAccessibility,
    compare_kernel_accessibility,
)


@dataclass(frozen=True)
class KernelAccessibilityEnvelope:
    declared_jump_radius_bins: int
    declared_jump_distance: float
    min_critical_jump_distance: float
    max_critical_jump_distance: float
    accessible_kernels: tuple[str, ...]
    trapped_kernels: tuple[str, ...]
    robustness_class: str
    results: tuple[KernelAccessibility, ...]


def kernel_accessibility_envelope(
    grid: Sequence[float],
    kernels: Iterable[str],
    *,
    alpha: float,
    kappa: float,
    gamma: float,
    epsilon: float,
    declared_jump_radius_bins: int,
    start_index: int = 0,
) -> KernelAccessibilityEnvelope:
    """Classify accessibility invariance across a declared kernel family.

    The three possible classes are:

    ``all_accessible``
        every kernel permits an all-uphill path at the declared jump radius;
    ``all_trapped``
        every kernel requires a larger jump;
    ``kernel_sensitive``
        accessibility changes with kernel shape.
    """
    if declared_jump_radius_bins < 0:
        raise ValueError("declared_jump_radius_bins must be non-negative")
    xs = tuple(float(x) for x in grid)
    if len(xs) < 3:
        raise ValueError("grid must contain at least three points")
    step = xs[1] - xs[0]
    results = compare_kernel_accessibility(
        xs,
        tuple(kernels),
        alpha=alpha,
        kappa=kappa,
        gamma=gamma,
        epsilon=epsilon,
        start_index=start_index,
    )
    if not results:
        raise ValueError("kernel family must be non-empty")

    accessible = tuple(
        result.kernel
        for result in results
        if declared_jump_radius_bins >= result.critical_jump_bins
    )
    trapped = tuple(
        result.kernel
        for result in results
        if declared_jump_radius_bins < result.critical_jump_bins
    )
    if accessible and not trapped:
        robustness = "all_accessible"
    elif trapped and not accessible:
        robustness = "all_trapped"
    else:
        robustness = "kernel_sensitive"

    critical_distances = tuple(result.critical_jump_distance for result in results)
    return KernelAccessibilityEnvelope(
        declared_jump_radius_bins=int(declared_jump_radius_bins),
        declared_jump_distance=declared_jump_radius_bins * step,
        min_critical_jump_distance=min(critical_distances),
        max_critical_jump_distance=max(critical_distances),
        accessible_kernels=accessible,
        trapped_kernels=trapped,
        robustness_class=robustness,
        results=results,
    )
