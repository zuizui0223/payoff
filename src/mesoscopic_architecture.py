"""Mesoscopic architecture dynamics with bounded interaction and small jumps.

This module is intentionally dependency-free. It implements a finite-grid
replicator-mutator approximation. The continuous Fokker--Planck equation is a
theoretical scaling limit, not something solved here.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import exp, isfinite
from typing import Sequence


def _normalise(values: Sequence[float]) -> tuple[float, ...]:
    vals = tuple(float(v) for v in values)
    if not vals:
        raise ValueError("density must be non-empty")
    if any((not isfinite(v)) or v < 0.0 for v in vals):
        raise ValueError("density must be finite and non-negative")
    total = sum(vals)
    if total <= 0.0:
        raise ValueError("density must have positive mass")
    return tuple(v / total for v in vals)


def _validate_grid(grid: Sequence[float]) -> tuple[float, ...]:
    xs = tuple(float(x) for x in grid)
    if len(xs) < 2:
        raise ValueError("grid must contain at least two points")
    if any(not isfinite(x) for x in xs):
        raise ValueError("grid must be finite")
    if any(b <= a for a, b in zip(xs, xs[1:])):
        raise ValueError("grid must be strictly increasing")
    return xs


def intrinsic_payoff(r: float, alpha: float, kappa: float) -> float:
    """Quadratic PAYOFF intrinsic architecture value b(r)."""
    if kappa < 0.0:
        raise ValueError("kappa must be non-negative")
    return float(alpha) * float(r) - 0.5 * float(kappa) * float(r) ** 2


def bounded_interaction_payoff(
    grid: Sequence[float],
    density: Sequence[float],
    *,
    gamma: float,
    epsilon: float | None,
) -> tuple[float, ...]:
    """Return H_epsilon(r_i,f) on a finite architecture grid.

    H_epsilon(r,q) = -gamma (r-q)^2 1{|r-q| <= epsilon}.
    ``epsilon=None`` gives the global-interaction kernel.
    """
    xs = _validate_grid(grid)
    f = _normalise(density)
    if len(xs) != len(f):
        raise ValueError("grid and density must have equal length")
    if epsilon is not None and epsilon < 0.0:
        raise ValueError("epsilon must be non-negative or None")

    out = []
    for x in xs:
        value = 0.0
        for y, mass in zip(xs, f):
            if epsilon is None or abs(x - y) <= epsilon:
                value += -float(gamma) * (x - y) ** 2 * mass
        out.append(value)
    return tuple(out)


def architecture_payoff(
    grid: Sequence[float],
    density: Sequence[float],
    *,
    alpha: float,
    kappa: float,
    gamma: float = 0.0,
    epsilon: float | None = None,
) -> tuple[float, ...]:
    xs = _validate_grid(grid)
    interaction = bounded_interaction_payoff(
        xs, density, gamma=gamma, epsilon=epsilon
    )
    return tuple(
        intrinsic_payoff(x, alpha, kappa) + h
        for x, h in zip(xs, interaction)
    )


def selection_step(
    density: Sequence[float],
    payoff: Sequence[float],
    *,
    beta: float = 1.0,
) -> tuple[float, ...]:
    """Exponentially reweight mass by payoff, preserving total mass."""
    f = _normalise(density)
    p = tuple(float(v) for v in payoff)
    if len(f) != len(p):
        raise ValueError("density and payoff must have equal length")
    if beta < 0.0:
        raise ValueError("beta must be non-negative")
    if any(not isfinite(v) for v in p):
        raise ValueError("payoff must be finite")
    anchor = max(p)
    weighted = tuple(m * exp(beta * (v - anchor)) for m, v in zip(f, p))
    return _normalise(weighted)


def small_jump_mutation(
    density: Sequence[float],
    *,
    radius_bins: int = 1,
    mutation_rate: float = 0.0,
) -> tuple[float, ...]:
    """Redistribute a fraction of mass only within ``radius_bins``.

    For each source bin, mutated mass is spread uniformly over all *other*
    grid bins within the radius. Boundary rows are renormalised rather than
    leaking mass. ``radius_bins=0`` or ``mutation_rate=0`` is the identity.
    """
    f = _normalise(density)
    if radius_bins < 0:
        raise ValueError("radius_bins must be non-negative")
    if not 0.0 <= mutation_rate <= 1.0:
        raise ValueError("mutation_rate must lie in [0, 1]")
    if radius_bins == 0 or mutation_rate == 0.0:
        return f

    n = len(f)
    out = [0.0] * n
    for i, mass in enumerate(f):
        out[i] += (1.0 - mutation_rate) * mass
        neighbours = [
            j
            for j in range(max(0, i - radius_bins), min(n, i + radius_bins + 1))
            if j != i
        ]
        if not neighbours:
            out[i] += mutation_rate * mass
            continue
        share = mutation_rate * mass / len(neighbours)
        for j in neighbours:
            out[j] += share
    return _normalise(out)


@dataclass(frozen=True)
class MesoscopicStep:
    density_before: tuple[float, ...]
    payoff: tuple[float, ...]
    density_after_selection: tuple[float, ...]
    density_after_mutation: tuple[float, ...]


def mesoscopic_step(
    grid: Sequence[float],
    density: Sequence[float],
    *,
    alpha: float,
    kappa: float,
    gamma: float = 0.0,
    epsilon: float | None = None,
    beta: float = 1.0,
    mutation_rate: float = 0.0,
    jump_radius_bins: int = 1,
) -> MesoscopicStep:
    """One finite-grid selection + local-mutation update."""
    xs = _validate_grid(grid)
    f0 = _normalise(density)
    if len(xs) != len(f0):
        raise ValueError("grid and density must have equal length")
    p = architecture_payoff(
        xs, f0, alpha=alpha, kappa=kappa, gamma=gamma, epsilon=epsilon
    )
    selected = selection_step(f0, p, beta=beta)
    mutated = small_jump_mutation(
        selected, radius_bins=jump_radius_bins, mutation_rate=mutation_rate
    )
    return MesoscopicStep(f0, p, selected, mutated)


def mean_architecture(grid: Sequence[float], density: Sequence[float]) -> float:
    xs = _validate_grid(grid)
    f = _normalise(density)
    if len(xs) != len(f):
        raise ValueError("grid and density must have equal length")
    return sum(x * m for x, m in zip(xs, f))


def variance_architecture(grid: Sequence[float], density: Sequence[float]) -> float:
    xs = _validate_grid(grid)
    f = _normalise(density)
    if len(xs) != len(f):
        raise ValueError("grid and density must have equal length")
    mean = sum(x * m for x, m in zip(xs, f))
    return sum((x - mean) ** 2 * m for x, m in zip(xs, f))


def minimum_jump_to_better_state(
    grid: Sequence[float],
    payoff: Sequence[float],
    start_index: int,
) -> int | None:
    """Smallest bin distance to any strictly higher-payoff state.

    This is a local accessibility diagnostic, not a fixation probability.
    """
    xs = _validate_grid(grid)
    p = tuple(float(v) for v in payoff)
    if len(xs) != len(p):
        raise ValueError("grid and payoff must have equal length")
    if not 0 <= start_index < len(xs):
        raise IndexError("start_index out of range")
    better = [abs(j - start_index) for j, v in enumerate(p) if v > p[start_index]]
    return min(better) if better else None
