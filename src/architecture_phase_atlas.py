"""Finite-grid phase atlas for mesoscopic PAYOFF architecture dynamics.

The atlas deliberately separates two questions:

1. What population-level architecture distribution emerges under bounded
   interaction, selection and local mutation?
2. Is the globally best state in the *initial resident payoff landscape*
   reachable by a sequence of strictly uphill jumps no larger than the declared
   jump radius?

The second object is an accessibility diagnostic. It is not a statement that a
stochastic mutational process can never cross a valley over long time.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from math import isfinite
from typing import Iterable, Sequence

from src.mesoscopic_architecture import (
    architecture_payoff,
    mean_architecture,
    mesoscopic_step,
    variance_architecture,
)


def regular_grid(length: float = 1.0, bins: int = 41) -> tuple[float, ...]:
    """Return an equally spaced architecture grid on ``[0, length]``."""
    L = float(length)
    if not isfinite(L) or L <= 0.0:
        raise ValueError("length must be finite and positive")
    if bins < 3:
        raise ValueError("bins must be at least 3")
    return tuple(L * i / (bins - 1) for i in range(bins))


def _normalise(values: Sequence[float]) -> tuple[float, ...]:
    vals = tuple(float(v) for v in values)
    if not vals or any((not isfinite(v)) or v < 0.0 for v in vals):
        raise ValueError("density must be non-empty, finite and non-negative")
    total = sum(vals)
    if total <= 0.0:
        raise ValueError("density must have positive mass")
    return tuple(v / total for v in vals)


def intrinsic_optimum(length: float, alpha: float, kappa: float) -> float:
    """Quadratic intrinsic optimum projected to the feasible architecture interval."""
    L = float(length)
    a = float(alpha)
    k = float(kappa)
    if L <= 0.0:
        raise ValueError("length must be positive")
    if k < 0.0:
        raise ValueError("kappa must be non-negative")
    if k == 0.0:
        if a > 0.0:
            return L
        return 0.0
    return min(L, max(0.0, a / k))


def seed_density(
    grid: Sequence[float],
    center: float,
    *,
    half_width_bins: int = 1,
) -> tuple[float, ...]:
    """Create a symmetric local seed around the closest grid point to ``center``."""
    xs = tuple(float(x) for x in grid)
    if len(xs) < 3:
        raise ValueError("grid must contain at least three points")
    if half_width_bins < 0:
        raise ValueError("half_width_bins must be non-negative")
    center_index = min(range(len(xs)), key=lambda i: abs(xs[i] - float(center)))
    values = [0.0] * len(xs)
    lo = max(0, center_index - half_width_bins)
    hi = min(len(xs), center_index + half_width_bins + 1)
    for i in range(lo, hi):
        values[i] = 1.0
    return _normalise(values)


@dataclass(frozen=True)
class DynamicsResult:
    density: tuple[float, ...]
    steps: int
    last_l1_change: float
    mean: float
    variance: float


def iterate_dynamics(
    grid: Sequence[float],
    density: Sequence[float],
    *,
    alpha: float,
    kappa: float,
    gamma: float,
    epsilon: float | None,
    beta: float,
    mutation_rate: float,
    jump_radius_bins: int,
    steps: int,
) -> DynamicsResult:
    """Iterate the deterministic finite-grid mesoscopic update for a fixed horizon."""
    if steps < 1:
        raise ValueError("steps must be positive")
    f = _normalise(density)
    epsilon_effective = None if epsilon is None else float(epsilon) + 1e-12
    last_change = float("inf")
    for _ in range(steps):
        step = mesoscopic_step(
            grid,
            f,
            alpha=alpha,
            kappa=kappa,
            gamma=gamma,
            epsilon=epsilon_effective,
            beta=beta,
            mutation_rate=mutation_rate,
            jump_radius_bins=jump_radius_bins,
        )
        next_f = step.density_after_mutation
        last_change = sum(abs(a - b) for a, b in zip(f, next_f))
        f = next_f
    return DynamicsResult(
        density=f,
        steps=steps,
        last_l1_change=last_change,
        mean=mean_architecture(grid, f),
        variance=variance_architecture(grid, f),
    )


def major_peak_indices(
    density: Sequence[float],
    *,
    relative_floor: float = 0.20,
    merge_radius_bins: int = 1,
    tolerance: float = 1e-12,
) -> tuple[int, ...]:
    """Detect major local modes without scipy.

    Peaks below ``relative_floor * max(density)`` are ignored. Adjacent plateau
    candidates are merged to one representative mode.
    """
    f = _normalise(density)
    if not 0.0 <= relative_floor <= 1.0:
        raise ValueError("relative_floor must lie in [0, 1]")
    if merge_radius_bins < 0:
        raise ValueError("merge_radius_bins must be non-negative")
    threshold = relative_floor * max(f)
    candidates: list[int] = []
    n = len(f)
    for i, value in enumerate(f):
        if value + tolerance < threshold:
            continue
        left = f[i - 1] if i > 0 else float("-inf")
        right = f[i + 1] if i + 1 < n else float("-inf")
        if value + tolerance >= left and value + tolerance >= right:
            if value > left + tolerance or value > right + tolerance or n == 1:
                candidates.append(i)

    if not candidates:
        return ()

    groups: list[list[int]] = [[candidates[0]]]
    for index in candidates[1:]:
        if index - groups[-1][-1] <= max(1, merge_radius_bins):
            groups[-1].append(index)
        else:
            groups.append([index])

    representatives = []
    for group in groups:
        best = max(group, key=lambda i: (f[i], -abs(i - sum(group) / len(group))))
        representatives.append(best)
    return tuple(representatives)


@dataclass(frozen=True)
class DistributionPhase:
    regime: str
    peak_indices: tuple[int, ...]
    peak_locations: tuple[float, ...]
    left_endpoint_mass: float
    right_endpoint_mass: float
    monomorphic_like: bool


def classify_distribution(
    grid: Sequence[float],
    density: Sequence[float],
    *,
    endpoint_fraction: float = 0.10,
    endpoint_mass_floor: float = 0.10,
    monomorphic_variance_fraction: float = 0.0025,
) -> DistributionPhase:
    """Classify the final finite-grid distribution conservatively."""
    xs = tuple(float(x) for x in grid)
    f = _normalise(density)
    if len(xs) != len(f):
        raise ValueError("grid and density must have equal length")
    if not 0.0 < endpoint_fraction < 0.5:
        raise ValueError("endpoint_fraction must lie in (0, 0.5)")
    if not 0.0 <= endpoint_mass_floor <= 1.0:
        raise ValueError("endpoint_mass_floor must lie in [0, 1]")
    span = xs[-1] - xs[0]
    if span <= 0.0:
        raise ValueError("grid must be increasing")

    peaks = major_peak_indices(f)
    locations = tuple(xs[i] for i in peaks)
    left_cut = xs[0] + endpoint_fraction * span
    right_cut = xs[-1] - endpoint_fraction * span
    left_mass = sum(m for x, m in zip(xs, f) if x <= left_cut + 1e-12)
    right_mass = sum(m for x, m in zip(xs, f) if x >= right_cut - 1e-12)
    has_left_peak = any(x <= left_cut + 1e-12 for x in locations)
    has_right_peak = any(x >= right_cut - 1e-12 for x in locations)

    if (
        len(peaks) >= 2
        and has_left_peak
        and has_right_peak
        and left_mass >= endpoint_mass_floor
        and right_mass >= endpoint_mass_floor
    ):
        regime = "endpoint_coexistence"
    elif len(peaks) >= 2:
        regime = "interior_multicluster"
    elif len(peaks) == 1:
        regime = "single_cluster"
    else:
        regime = "diffuse_or_flat"

    variance = variance_architecture(xs, f)
    monomorphic_like = (
        len(peaks) == 1
        and variance <= monomorphic_variance_fraction * span * span
    )
    return DistributionPhase(
        regime=regime,
        peak_indices=peaks,
        peak_locations=locations,
        left_endpoint_mass=left_mass,
        right_endpoint_mass=right_mass,
        monomorphic_like=monomorphic_like,
    )


def uphill_reachable_indices(
    payoff: Sequence[float],
    start_index: int,
    *,
    jump_radius_bins: int,
    tolerance: float = 1e-12,
) -> tuple[int, ...]:
    """Return states reachable through strictly uphill jumps within the radius."""
    p = tuple(float(v) for v in payoff)
    if not p or any(not isfinite(v) for v in p):
        raise ValueError("payoff must be non-empty and finite")
    if not 0 <= start_index < len(p):
        raise IndexError("start_index out of range")
    if jump_radius_bins < 0:
        raise ValueError("jump_radius_bins must be non-negative")

    seen = {start_index}
    stack = [start_index]
    while stack:
        i = stack.pop()
        lo = max(0, i - jump_radius_bins)
        hi = min(len(p), i + jump_radius_bins + 1)
        for j in range(lo, hi):
            if j == i or j in seen:
                continue
            if p[j] > p[i] + tolerance:
                seen.add(j)
                stack.append(j)
    return tuple(sorted(seen))


def global_payoff_indices(
    payoff: Sequence[float], *, tolerance: float = 1e-12
) -> tuple[int, ...]:
    p = tuple(float(v) for v in payoff)
    if not p or any(not isfinite(v) for v in p):
        raise ValueError("payoff must be non-empty and finite")
    best = max(p)
    return tuple(i for i, value in enumerate(p) if value >= best - tolerance)


def minimum_uphill_jump_radius_to_global(
    payoff: Sequence[float],
    start_index: int,
    *,
    tolerance: float = 1e-12,
) -> int:
    """Smallest jump radius admitting an all-uphill path to a global payoff peak."""
    p = tuple(float(v) for v in payoff)
    targets = set(global_payoff_indices(p, tolerance=tolerance))
    if start_index in targets:
        return 0
    for radius in range(1, len(p)):
        reachable = set(
            uphill_reachable_indices(
                p,
                start_index,
                jump_radius_bins=radius,
                tolerance=tolerance,
            )
        )
        if reachable & targets:
            return radius
    # A direct jump to a strictly higher global maximum is always available at
    # radius n-1, so reaching this branch indicates inconsistent tolerances.
    raise RuntimeError("global payoff state was not reachable at maximal jump radius")


@dataclass(frozen=True)
class PhaseCell:
    gamma: float
    epsilon: float | None
    jump_radius_bins: int
    critical_uphill_jump_bins: int
    small_jump_trapped: bool
    dynamical_regime: str
    monomorphic_like: bool
    final_mean: float
    final_variance: float
    peak_locations: tuple[float, ...]
    left_endpoint_mass: float
    right_endpoint_mass: float
    last_l1_change: float

    def to_dict(self) -> dict:
        data = asdict(self)
        data["epsilon"] = "global" if self.epsilon is None else self.epsilon
        data["peak_locations"] = list(self.peak_locations)
        return data


def phase_cell(
    *,
    gamma: float,
    epsilon: float | None,
    jump_radius_bins: int,
    alpha: float = 0.5,
    kappa: float = 1.0,
    length: float = 1.0,
    bins: int = 41,
    beta: float = 1.5,
    mutation_rate: float = 0.03,
    steps: int = 800,
    seed_half_width_bins: int = 1,
    accessibility_start: float = 0.0,
) -> PhaseCell:
    """Evaluate one ``(gamma, epsilon, jump radius)`` atlas cell."""
    if jump_radius_bins < 0:
        raise ValueError("jump_radius_bins must be non-negative")
    xs = regular_grid(length, bins)

    # Population phase: begin near the intrinsic singular architecture so the
    # classification asks whether frequency feedback keeps one cluster, creates
    # interior clusters, or transports mass toward the endpoints.
    center = intrinsic_optimum(length, alpha, kappa)
    initial = seed_density(xs, center, half_width_bins=seed_half_width_bins)
    dynamics = iterate_dynamics(
        xs,
        initial,
        alpha=alpha,
        kappa=kappa,
        gamma=gamma,
        epsilon=epsilon,
        beta=beta,
        mutation_rate=mutation_rate,
        jump_radius_bins=jump_radius_bins,
        steps=steps,
    )
    phase = classify_distribution(xs, dynamics.density)

    # Accessibility overlay: ask whether a fully shared (or otherwise declared)
    # resident can reach the best state in its initial invasion-payoff landscape
    # by strictly uphill jumps no larger than the same radius.
    start_index = min(range(len(xs)), key=lambda i: abs(xs[i] - accessibility_start))
    resident = tuple(1.0 if i == start_index else 0.0 for i in range(len(xs)))
    epsilon_effective = None if epsilon is None else float(epsilon) + 1e-12
    resident_payoff = architecture_payoff(
        xs,
        resident,
        alpha=alpha,
        kappa=kappa,
        gamma=gamma,
        epsilon=epsilon_effective,
    )
    critical_radius = minimum_uphill_jump_radius_to_global(
        resident_payoff, start_index
    )

    return PhaseCell(
        gamma=float(gamma),
        epsilon=None if epsilon is None else float(epsilon),
        jump_radius_bins=int(jump_radius_bins),
        critical_uphill_jump_bins=critical_radius,
        small_jump_trapped=jump_radius_bins < critical_radius,
        dynamical_regime=phase.regime,
        monomorphic_like=phase.monomorphic_like,
        final_mean=dynamics.mean,
        final_variance=dynamics.variance,
        peak_locations=phase.peak_locations,
        left_endpoint_mass=phase.left_endpoint_mass,
        right_endpoint_mass=phase.right_endpoint_mass,
        last_l1_change=dynamics.last_l1_change,
    )


def build_phase_atlas(
    gammas: Iterable[float],
    epsilons: Iterable[float | None],
    jump_radii_bins: Iterable[int],
    **kwargs,
) -> tuple[PhaseCell, ...]:
    """Evaluate a deterministic cartesian phase grid."""
    cells = []
    for epsilon in epsilons:
        for gamma in gammas:
            for jump_radius in jump_radii_bins:
                cells.append(
                    phase_cell(
                        gamma=float(gamma),
                        epsilon=epsilon,
                        jump_radius_bins=int(jump_radius),
                        **kwargs,
                    )
                )
    return tuple(cells)


def phase_counts(cells: Iterable[PhaseCell]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for cell in cells:
        key = cell.dynamical_regime
        counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items()))
