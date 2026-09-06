"""Robustness of local architecture accessibility to interaction-kernel shape."""
from __future__ import annotations

from dataclasses import dataclass
from math import cos, exp, isfinite, pi
from typing import Iterable, Sequence

from src.architecture_phase_atlas import minimum_uphill_jump_radius_to_global


KERNELS = {"hard", "triangular", "cosine", "gaussian", "global"}


def kernel_weight(distance: float, *, epsilon: float | None, kernel: str) -> float:
    """Return a non-negative interaction weight for one architecture distance."""
    d = abs(float(distance))
    kind = str(kernel).lower()
    if kind not in KERNELS:
        raise ValueError(f"unknown kernel: {kernel!r}")
    if kind == "global":
        return 1.0
    if epsilon is None:
        raise ValueError("finite/smooth kernels require epsilon")
    e = float(epsilon)
    if not isfinite(e) or e <= 0.0:
        raise ValueError("epsilon must be finite and positive")

    if kind == "hard":
        return 1.0 if d <= e + 1e-12 else 0.0
    if kind == "triangular":
        return max(0.0, 1.0 - d / e)
    if kind == "cosine":
        if d >= e:
            return 0.0
        return 0.5 * (1.0 + cos(pi * d / e))
    if kind == "gaussian":
        return exp(-0.5 * (d / e) ** 2)
    raise AssertionError("unreachable kernel branch")


def kernel_interaction_payoff(
    grid: Sequence[float],
    density: Sequence[float],
    *,
    gamma: float,
    epsilon: float | None,
    kernel: str,
) -> tuple[float, ...]:
    xs = tuple(float(x) for x in grid)
    f = tuple(float(v) for v in density)
    if len(xs) != len(f) or not xs:
        raise ValueError("grid and density must be non-empty and equal length")
    if any(v < 0.0 or not isfinite(v) for v in f):
        raise ValueError("density must be finite and non-negative")
    total = sum(f)
    if total <= 0.0:
        raise ValueError("density must have positive mass")
    f = tuple(v / total for v in f)

    out = []
    for x in xs:
        value = 0.0
        for y, mass in zip(xs, f):
            w = kernel_weight(abs(x - y), epsilon=epsilon, kernel=kernel)
            value += -float(gamma) * (x - y) ** 2 * w * mass
        out.append(value)
    return tuple(out)


def kernel_architecture_payoff(
    grid: Sequence[float],
    density: Sequence[float],
    *,
    alpha: float,
    kappa: float,
    gamma: float,
    epsilon: float | None,
    kernel: str,
) -> tuple[float, ...]:
    if float(kappa) < 0.0:
        raise ValueError("kappa must be non-negative")
    interaction = kernel_interaction_payoff(
        grid,
        density,
        gamma=gamma,
        epsilon=epsilon,
        kernel=kernel,
    )
    return tuple(
        float(alpha) * float(x) - 0.5 * float(kappa) * float(x) ** 2 + h
        for x, h in zip(grid, interaction)
    )


@dataclass(frozen=True)
class KernelAccessibility:
    kernel: str
    gamma: float
    epsilon: float | None
    start_index: int
    critical_jump_bins: int
    grid_step: float
    critical_jump_distance: float
    one_bin_accessible: bool


def kernel_accessibility(
    grid: Sequence[float],
    *,
    alpha: float,
    kappa: float,
    gamma: float,
    epsilon: float | None,
    kernel: str,
    start_index: int = 0,
) -> KernelAccessibility:
    xs = tuple(float(x) for x in grid)
    if len(xs) < 3 or any(b <= a for a, b in zip(xs, xs[1:])):
        raise ValueError("grid must be strictly increasing with at least three points")
    if not 0 <= start_index < len(xs):
        raise IndexError("start_index out of range")
    resident = tuple(1.0 if i == start_index else 0.0 for i in range(len(xs)))
    payoff = kernel_architecture_payoff(
        xs,
        resident,
        alpha=alpha,
        kappa=kappa,
        gamma=gamma,
        epsilon=epsilon,
        kernel=kernel,
    )
    critical = minimum_uphill_jump_radius_to_global(payoff, start_index)
    step = xs[1] - xs[0]
    return KernelAccessibility(
        kernel=str(kernel).lower(),
        gamma=float(gamma),
        epsilon=None if epsilon is None else float(epsilon),
        start_index=start_index,
        critical_jump_bins=critical,
        grid_step=step,
        critical_jump_distance=critical * step,
        one_bin_accessible=critical <= 1,
    )


def compare_kernel_accessibility(
    grid: Sequence[float],
    kernels: Iterable[str],
    *,
    alpha: float,
    kappa: float,
    gamma: float,
    epsilon: float,
    start_index: int = 0,
) -> tuple[KernelAccessibility, ...]:
    return tuple(
        kernel_accessibility(
            grid,
            alpha=alpha,
            kappa=kappa,
            gamma=gamma,
            epsilon=epsilon,
            kernel=kernel,
            start_index=start_index,
        )
        for kernel in kernels
    )
