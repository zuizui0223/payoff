"""Explicit patch landscape for migration--phenology tracking.

A one-dimensional landscape contains fixed spatial patches x_j. Environmental
demand increases through time,

    D_t = v t,

while local climatic offset is g x_j. A lineage can therefore reduce mismatch

    e_j = D_t - g x_j - s z

either by shifting its spatial abundance distribution toward larger x or by
changing phenology z.

Spatial tracking is not imposed directly. Local reproduction favors better
matched patches and offspring disperse between adjacent patches at a heritable
rate. Phenological tracking follows an abundance-weighted mismatch correction
and can be bounded by a finite seasonal shift limit.

Two interacting species are simulated on the same landscape. Their interaction
penalty uses the climate-equivalent distance between spatial centroids and the
phenological gap, preserving the geometry of the nonspatial tracking model.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, expm1, isfinite, sqrt
from statistics import mean

from src.spatiotemporal_tracking import TrackingStrategy
from src.tracking_coevolution import SpeciesTrackingParameters


_EPS = 1e-12


@dataclass(frozen=True)
class MovingLandscapeScenario:
    patches: int = 41
    patch_spacing: float = 1.0
    spatial_gradient: float = 0.20
    climate_velocity: float = 0.06
    phenology_scale: float = 1.0
    max_abs_phenology_shift: float = 2.0
    initial_distribution_sd: float = 2.0
    carrying_capacity: float = 1000.0
    density_coefficient: float = 0.30
    extinction_threshold: float = 1.0
    boundary_retention: float = 1.0
    long_distance_fraction: float = 0.0
    long_distance_step: int = 2
    steps: int = 160
    burn_in: int = 40
    species_a: SpeciesTrackingParameters = SpeciesTrackingParameters(
        baseline_growth=0.30,
    )
    species_b: SpeciesTrackingParameters = SpeciesTrackingParameters(
        baseline_growth=0.30,
    )

    def __post_init__(self) -> None:
        if self.patches < 3:
            raise ValueError("patches must be at least 3")
        if self.patches % 2 == 0:
            raise ValueError("patches must be odd so the initial optimum is centered")
        for name in (
            "patch_spacing",
            "spatial_gradient",
            "phenology_scale",
            "max_abs_phenology_shift",
            "initial_distribution_sd",
            "carrying_capacity",
            "density_coefficient",
            "extinction_threshold",
            "boundary_retention",
            "long_distance_fraction",
        ):
            value = float(getattr(self, name))
            if not isfinite(value):
                raise ValueError(f"{name} must be finite")
        if self.patch_spacing <= 0.0:
            raise ValueError("patch_spacing must be positive")
        if self.spatial_gradient <= 0.0:
            raise ValueError("spatial_gradient must be positive")
        if self.phenology_scale <= 0.0:
            raise ValueError("phenology_scale must be positive")
        if self.max_abs_phenology_shift < 0.0:
            raise ValueError("max_abs_phenology_shift must be non-negative")
        if self.initial_distribution_sd <= 0.0:
            raise ValueError("initial_distribution_sd must be positive")
        if self.carrying_capacity <= 0.0:
            raise ValueError("carrying_capacity must be positive")
        if self.density_coefficient < 0.0:
            raise ValueError("density_coefficient must be non-negative")
        if self.extinction_threshold < 0.0:
            raise ValueError("extinction_threshold must be non-negative")
        if not 0.0 <= self.boundary_retention <= 1.0:
            raise ValueError("boundary_retention must lie in [0,1]")
        if not 0.0 <= self.long_distance_fraction <= 1.0:
            raise ValueError("long_distance_fraction must lie in [0,1]")
        if self.long_distance_step < 2:
            raise ValueError("long_distance_step must be at least 2")
        if not isfinite(self.climate_velocity):
            raise ValueError("climate_velocity must be finite")
        if self.steps <= 0:
            raise ValueError("steps must be positive")
        if not 0 <= self.burn_in < self.steps:
            raise ValueError("burn_in must satisfy 0 <= burn_in < steps")

    @property
    def positions(self) -> tuple[float, ...]:
        middle = self.patches // 2
        return tuple(
            (index - middle) * self.patch_spacing
            for index in range(self.patches)
        )

    @property
    def right_edge_climate_offset(self) -> float:
        return self.spatial_gradient * self.positions[-1]


@dataclass(frozen=True)
class LandscapePairResult:
    strategy_a: TrackingStrategy
    strategy_b: TrackingStrategy
    mean_log_growth_a: float
    mean_log_growth_b: float
    mean_realized_log_growth_a: float
    mean_realized_log_growth_b: float
    final_abundance_a: float
    final_abundance_b: float
    minimum_abundance_a: float
    minimum_abundance_b: float
    final_centroid_a: float
    final_centroid_b: float
    final_phenology_a: float
    final_phenology_b: float
    mean_centroid_a: float
    mean_centroid_b: float
    mean_phenology_a: float
    mean_phenology_b: float
    mean_effective_tracking_a: float
    mean_effective_tracking_b: float
    rms_abiotic_mismatch_a: float
    rms_abiotic_mismatch_b: float
    rms_interaction_mismatch: float
    phenology_limit_fraction_a: float
    phenology_limit_fraction_b: float
    right_edge_mass_fraction_a: float
    right_edge_mass_fraction_b: float
    persisted_a: bool
    persisted_b: bool

    @property
    def joint_persisted(self) -> bool:
        return self.persisted_a and self.persisted_b

    @property
    def mean_joint_growth(self) -> float:
        return 0.5 * (
            self.mean_log_growth_a + self.mean_log_growth_b
        )


def architecture_cost(
    strategy: TrackingStrategy,
    parameters: SpeciesTrackingParameters,
) -> float:
    m = strategy.migration_rate
    h = strategy.phenology_rate
    return (
        parameters.migration_cost * m * m
        + parameters.phenology_cost * h * h
        + parameters.joint_cost * m * h
    )


def dispersal_fraction(migration_rate: float) -> float:
    if migration_rate < 0.0 or not isfinite(migration_rate):
        raise ValueError("migration_rate must be non-negative and finite")
    if migration_rate == 0.0:
        return 0.0
    return -expm1(-migration_rate)


def nearest_neighbor_dispersal(
    abundance: tuple[float, ...] | list[float],
    migration_rate: float,
    *,
    boundary_retention: float = 1.0,
) -> tuple[float, ...]:
    """Nearest-neighbor dispersal with continuously tunable edge leakage.

    boundary_retention=1 gives reflecting boundaries: all outward-moving edge
    mass is returned to the boundary patch.

    boundary_retention=0 gives absorbing/leaky boundaries: outward-moving edge
    mass leaves the modeled landscape.

    Intermediate values retain the declared fraction and lose the remainder.
    Interior movement is always conservative.
    """

    if len(abundance) < 2:
        raise ValueError("abundance must contain at least two patches")
    if any(value < 0.0 or not isfinite(value) for value in abundance):
        raise ValueError("abundance values must be finite and non-negative")
    if not 0.0 <= boundary_retention <= 1.0:
        raise ValueError("boundary_retention must lie in [0,1]")

    fraction = dispersal_fraction(migration_rate)
    if fraction == 0.0:
        return tuple(float(value) for value in abundance)

    out = [0.0] * len(abundance)
    for index, value in enumerate(abundance):
        moving = fraction * value
        staying = value - moving
        out[index] += staying

        left = 0.5 * moving
        right = 0.5 * moving
        if index == 0:
            out[index] += boundary_retention * left
        else:
            out[index - 1] += left

        if index == len(abundance) - 1:
            out[index] += boundary_retention * right
        else:
            out[index + 1] += right

    return tuple(out)


def reflect_nearest_neighbor_dispersal(
    abundance: tuple[float, ...] | list[float],
    migration_rate: float,
) -> tuple[float, ...]:
    """Backward-compatible reflecting-boundary dispersal wrapper."""

    return nearest_neighbor_dispersal(
        abundance,
        migration_rate,
        boundary_retention=1.0,
    )


def mixed_range_dispersal(
    abundance: tuple[float, ...] | list[float],
    migration_rate: float,
    *,
    boundary_retention: float = 1.0,
    long_distance_fraction: float = 0.0,
    long_distance_step: int = 2,
) -> tuple[float, ...]:
    """Disperse moving mass across nearest and longer-distance steps.

    A fraction long_distance_fraction of the moving mass uses
    long_distance_step patches per directional move; the remainder moves one
    patch. Out-of-landscape mass is retained at the nearest boundary according
    to boundary_retention and otherwise lost.
    """

    if len(abundance) < 2:
        raise ValueError("abundance must contain at least two patches")
    if any(value < 0.0 or not isfinite(value) for value in abundance):
        raise ValueError("abundance values must be finite and non-negative")
    if not 0.0 <= boundary_retention <= 1.0:
        raise ValueError("boundary_retention must lie in [0,1]")
    if not 0.0 <= long_distance_fraction <= 1.0:
        raise ValueError("long_distance_fraction must lie in [0,1]")
    if long_distance_step < 2:
        raise ValueError("long_distance_step must be at least 2")

    fraction = dispersal_fraction(migration_rate)
    if fraction == 0.0:
        return tuple(float(value) for value in abundance)

    out = [0.0] * len(abundance)
    last = len(abundance) - 1

    def deposit(
        source_index: int,
        target_index: int,
        mass: float,
    ) -> None:
        if 0 <= target_index <= last:
            out[target_index] += mass
            return
        boundary = 0 if target_index < 0 else last
        out[boundary] += boundary_retention * mass

    for index, value in enumerate(abundance):
        moving = fraction * value
        out[index] += value - moving

        nearest_mass = moving * (1.0 - long_distance_fraction)
        long_mass = moving * long_distance_fraction
        for direction in (-1, 1):
            deposit(
                index,
                index + direction,
                0.5 * nearest_mass,
            )
            deposit(
                index,
                index + direction * long_distance_step,
                0.5 * long_mass,
            )

    return tuple(out)


def gaussian_initial_distribution(
    scenario: MovingLandscapeScenario,
    total_abundance: float | None = None,
) -> tuple[float, ...]:
    """Return a normalized Gaussian abundance centered at the initial optimum."""

    if total_abundance is None:
        total_abundance = scenario.carrying_capacity
    if total_abundance < 0.0 or not isfinite(total_abundance):
        raise ValueError("total_abundance must be non-negative and finite")

    weights = tuple(
        exp(
            -0.5
            * (position / scenario.initial_distribution_sd) ** 2
        )
        for position in scenario.positions
    )
    total_weight = sum(weights)
    return tuple(
        total_abundance * weight / total_weight
        for weight in weights
    )


def spatial_centroid(
    abundance: tuple[float, ...] | list[float],
    positions: tuple[float, ...] | list[float],
) -> float:
    if len(abundance) != len(positions) or not abundance:
        raise ValueError("abundance and positions must have equal non-zero length")
    total = sum(abundance)
    if total <= 0.0:
        return 0.0
    return sum(
        value * position
        for value, position in zip(abundance, positions)
    ) / total


def _weighted_climate_residual(
    abundance: tuple[float, ...],
    positions: tuple[float, ...],
    demand: float,
    phenology_shift: float,
    scenario: MovingLandscapeScenario,
) -> float:
    total = sum(abundance)
    if total <= 0.0:
        return 0.0
    return sum(
        value
        * (
            demand
            - scenario.spatial_gradient * position
            - scenario.phenology_scale * phenology_shift
        )
        for value, position in zip(abundance, positions)
    ) / total


def _update_phenology(
    abundance: tuple[float, ...],
    strategy: TrackingStrategy,
    current_shift: float,
    demand: float,
    scenario: MovingLandscapeScenario,
) -> tuple[float, bool]:
    if strategy.phenology_rate <= 0.0:
        return current_shift, False

    residual = _weighted_climate_residual(
        abundance,
        scenario.positions,
        demand,
        current_shift,
        scenario,
    )
    correction_fraction = -expm1(-strategy.phenology_rate)
    proposed = (
        current_shift
        + correction_fraction
        * residual
        / scenario.phenology_scale
    )
    limit = scenario.max_abs_phenology_shift
    clipped = min(limit, max(-limit, proposed))
    at_limit = (
        limit > 0.0
        and abs(clipped) >= limit - 1e-12
    )
    return clipped, at_limit


def _rms_abiotic_mismatch(
    abundance: tuple[float, ...],
    phenology_shift: float,
    demand: float,
    scenario: MovingLandscapeScenario,
) -> float:
    total = sum(abundance)
    if total <= 0.0:
        return 0.0
    value = sum(
        abundance_value
        * (
            demand
            - scenario.spatial_gradient * position
            - scenario.phenology_scale * phenology_shift
        )
        ** 2
        for abundance_value, position in zip(
            abundance,
            scenario.positions,
        )
    ) / total
    return sqrt(value)


def _edge_mass_fraction(abundance: tuple[float, ...]) -> float:
    total = sum(abundance)
    if total <= 0.0:
        return 0.0
    return abundance[-1] / total


def _one_species_generation(
    abundance: tuple[float, ...],
    strategy: TrackingStrategy,
    parameters: SpeciesTrackingParameters,
    phenology_shift: float,
    demand: float,
    interaction_sq: float,
    scenario: MovingLandscapeScenario,
) -> tuple[tuple[float, ...], float, float]:
    total = sum(abundance)
    density_penalty = (
        scenario.density_coefficient
        * total
        / scenario.carrying_capacity
    )
    cost = architecture_cost(strategy, parameters)

    reproduced = []
    weighted_low_density_numerator = 0.0
    weighted_realized_numerator = 0.0
    if total <= 0.0:
        return tuple(0.0 for _ in abundance), 0.0, 0.0

    for value, position in zip(abundance, scenario.positions):
        mismatch = (
            demand
            - scenario.spatial_gradient * position
            - scenario.phenology_scale * phenology_shift
        )
        low_density_growth = (
            parameters.baseline_growth
            - cost
            - 0.5
            * parameters.abiotic_strength
            * mismatch
            * mismatch
            - 0.5
            * parameters.interaction_strength
            * interaction_sq
        )
        realized_growth = low_density_growth - density_penalty
        weighted_low_density_numerator += (
            value * low_density_growth
        )
        weighted_realized_numerator += value * realized_growth
        reproduced.append(value * exp(realized_growth))

    dispersed = mixed_range_dispersal(
        reproduced,
        strategy.migration_rate,
        boundary_retention=scenario.boundary_retention,
        long_distance_fraction=scenario.long_distance_fraction,
        long_distance_step=scenario.long_distance_step,
    )
    return (
        dispersed,
        weighted_low_density_numerator / total,
        weighted_realized_numerator / total,
    )


def simulate_moving_landscape_pair(
    strategy_a: TrackingStrategy,
    strategy_b: TrackingStrategy,
    scenario: MovingLandscapeScenario,
    *,
    initial_abundance_a: tuple[float, ...] | None = None,
    initial_abundance_b: tuple[float, ...] | None = None,
) -> LandscapePairResult:
    """Simulate two interacting populations on an explicit moving landscape."""

    if initial_abundance_a is None:
        abundance_a = gaussian_initial_distribution(scenario)
    else:
        abundance_a = tuple(initial_abundance_a)
    if initial_abundance_b is None:
        abundance_b = gaussian_initial_distribution(scenario)
    else:
        abundance_b = tuple(initial_abundance_b)

    if len(abundance_a) != scenario.patches:
        raise ValueError("initial_abundance_a must match patch count")
    if len(abundance_b) != scenario.patches:
        raise ValueError("initial_abundance_b must match patch count")

    positions = scenario.positions
    phenology_a = 0.0
    phenology_b = 0.0
    minimum_a = sum(abundance_a)
    minimum_b = sum(abundance_b)

    sum_growth_a = 0.0
    sum_growth_b = 0.0
    sum_realized_growth_a = 0.0
    sum_realized_growth_b = 0.0
    sum_centroid_a = 0.0
    sum_centroid_b = 0.0
    sum_phenology_a = 0.0
    sum_phenology_b = 0.0
    sum_tracking_a = 0.0
    sum_tracking_b = 0.0
    sum_abiotic_sq_a = 0.0
    sum_abiotic_sq_b = 0.0
    sum_interaction_sq = 0.0
    limit_count_a = 0
    limit_count_b = 0
    edge_mass_sum_a = 0.0
    edge_mass_sum_b = 0.0
    observed = 0

    for step in range(1, scenario.steps + 1):
        demand = scenario.climate_velocity * step

        phenology_a, at_limit_a = _update_phenology(
            abundance_a,
            strategy_a,
            phenology_a,
            demand,
            scenario,
        )
        phenology_b, at_limit_b = _update_phenology(
            abundance_b,
            strategy_b,
            phenology_b,
            demand,
            scenario,
        )

        centroid_a = spatial_centroid(abundance_a, positions)
        centroid_b = spatial_centroid(abundance_b, positions)
        spatial_gap = (
            scenario.spatial_gradient
            * (centroid_a - centroid_b)
        )
        phenology_gap = (
            scenario.phenology_scale
            * (phenology_a - phenology_b)
        )
        interaction_sq = (
            spatial_gap * spatial_gap
            + phenology_gap * phenology_gap
        )

        abundance_a, growth_a, realized_growth_a = _one_species_generation(
            abundance_a,
            strategy_a,
            scenario.species_a,
            phenology_a,
            demand,
            interaction_sq,
            scenario,
        )
        abundance_b, growth_b, realized_growth_b = _one_species_generation(
            abundance_b,
            strategy_b,
            scenario.species_b,
            phenology_b,
            demand,
            interaction_sq,
            scenario,
        )

        total_a = sum(abundance_a)
        total_b = sum(abundance_b)
        minimum_a = min(minimum_a, total_a)
        minimum_b = min(minimum_b, total_b)

        if step > scenario.burn_in:
            observed += 1
            new_centroid_a = spatial_centroid(abundance_a, positions)
            new_centroid_b = spatial_centroid(abundance_b, positions)
            effective_a = (
                scenario.spatial_gradient * new_centroid_a
                + scenario.phenology_scale * phenology_a
            )
            effective_b = (
                scenario.spatial_gradient * new_centroid_b
                + scenario.phenology_scale * phenology_b
            )
            rms_a = _rms_abiotic_mismatch(
                abundance_a,
                phenology_a,
                demand,
                scenario,
            )
            rms_b = _rms_abiotic_mismatch(
                abundance_b,
                phenology_b,
                demand,
                scenario,
            )

            sum_growth_a += growth_a
            sum_growth_b += growth_b
            sum_realized_growth_a += realized_growth_a
            sum_realized_growth_b += realized_growth_b
            sum_centroid_a += new_centroid_a
            sum_centroid_b += new_centroid_b
            sum_phenology_a += phenology_a
            sum_phenology_b += phenology_b
            sum_tracking_a += effective_a
            sum_tracking_b += effective_b
            sum_abiotic_sq_a += rms_a * rms_a
            sum_abiotic_sq_b += rms_b * rms_b
            sum_interaction_sq += interaction_sq
            limit_count_a += int(at_limit_a)
            limit_count_b += int(at_limit_b)
            edge_mass_sum_a += _edge_mass_fraction(abundance_a)
            edge_mass_sum_b += _edge_mass_fraction(abundance_b)

    if observed <= 0:
        raise RuntimeError("no post-burn-in observations")

    final_centroid_a = spatial_centroid(abundance_a, positions)
    final_centroid_b = spatial_centroid(abundance_b, positions)
    final_a = sum(abundance_a)
    final_b = sum(abundance_b)

    return LandscapePairResult(
        strategy_a=strategy_a,
        strategy_b=strategy_b,
        mean_log_growth_a=sum_growth_a / observed,
        mean_log_growth_b=sum_growth_b / observed,
        mean_realized_log_growth_a=(
            sum_realized_growth_a / observed
        ),
        mean_realized_log_growth_b=(
            sum_realized_growth_b / observed
        ),
        final_abundance_a=final_a,
        final_abundance_b=final_b,
        minimum_abundance_a=minimum_a,
        minimum_abundance_b=minimum_b,
        final_centroid_a=final_centroid_a,
        final_centroid_b=final_centroid_b,
        final_phenology_a=phenology_a,
        final_phenology_b=phenology_b,
        mean_centroid_a=sum_centroid_a / observed,
        mean_centroid_b=sum_centroid_b / observed,
        mean_phenology_a=sum_phenology_a / observed,
        mean_phenology_b=sum_phenology_b / observed,
        mean_effective_tracking_a=sum_tracking_a / observed,
        mean_effective_tracking_b=sum_tracking_b / observed,
        rms_abiotic_mismatch_a=sqrt(sum_abiotic_sq_a / observed),
        rms_abiotic_mismatch_b=sqrt(sum_abiotic_sq_b / observed),
        rms_interaction_mismatch=sqrt(
            sum_interaction_sq / observed
        ),
        phenology_limit_fraction_a=limit_count_a / observed,
        phenology_limit_fraction_b=limit_count_b / observed,
        right_edge_mass_fraction_a=edge_mass_sum_a / observed,
        right_edge_mass_fraction_b=edge_mass_sum_b / observed,
        persisted_a=final_a > scenario.extinction_threshold,
        persisted_b=final_b > scenario.extinction_threshold,
    )


def optimize_matched_landscape_strategy(
    scenario: MovingLandscapeScenario,
    *,
    max_migration_rate: float = 1.0,
    max_phenology_rate: float = 1.0,
    migration_points: int = 11,
    phenology_points: int = 11,
) -> LandscapePairResult:
    """Find the best matched strategy for the two-species landscape."""

    if max_migration_rate < 0.0 or max_phenology_rate < 0.0:
        raise ValueError("maximum rates must be non-negative")
    if migration_points < 2 or phenology_points < 2:
        raise ValueError("grid points must be at least 2")

    migration_values = [
        max_migration_rate * i / (migration_points - 1)
        for i in range(migration_points)
    ]
    phenology_values = [
        max_phenology_rate * i / (phenology_points - 1)
        for i in range(phenology_points)
    ]

    best: LandscapePairResult | None = None
    for migration in migration_values:
        for phenology in phenology_values:
            strategy = TrackingStrategy(
                migration,
                phenology,
            )
            candidate = simulate_moving_landscape_pair(
                strategy,
                strategy,
                scenario,
            )
            if best is None:
                best = candidate
                continue
            candidate_score = candidate.mean_joint_growth
            best_score = best.mean_joint_growth
            if candidate_score > best_score:
                best = candidate
            elif candidate_score == best_score:
                if strategy.total_rate < best.strategy_a.total_rate:
                    best = candidate

    assert best is not None
    return best


def landscape_strategy_sweep(
    scenario: MovingLandscapeScenario,
    climate_velocities: tuple[float, ...] | list[float],
    phenology_limits: tuple[float, ...] | list[float],
    *,
    max_migration_rate: float = 1.0,
    max_phenology_rate: float = 1.0,
    migration_points: int = 9,
    phenology_points: int = 9,
) -> list[dict[str, float | str | int]]:
    """Map best matched tracking architecture over climate speed and time limit."""

    rows: list[dict[str, float | str | int]] = []
    for velocity in climate_velocities:
        for limit in phenology_limits:
            cell = MovingLandscapeScenario(
                patches=scenario.patches,
                patch_spacing=scenario.patch_spacing,
                spatial_gradient=scenario.spatial_gradient,
                climate_velocity=velocity,
                phenology_scale=scenario.phenology_scale,
                max_abs_phenology_shift=limit,
                initial_distribution_sd=scenario.initial_distribution_sd,
                carrying_capacity=scenario.carrying_capacity,
                density_coefficient=scenario.density_coefficient,
                extinction_threshold=scenario.extinction_threshold,
                boundary_retention=scenario.boundary_retention,
                long_distance_fraction=scenario.long_distance_fraction,
                long_distance_step=scenario.long_distance_step,
                steps=scenario.steps,
                burn_in=scenario.burn_in,
                species_a=scenario.species_a,
                species_b=scenario.species_b,
            )
            best = optimize_matched_landscape_strategy(
                cell,
                max_migration_rate=max_migration_rate,
                max_phenology_rate=max_phenology_rate,
                migration_points=migration_points,
                phenology_points=phenology_points,
            )
            migration = best.strategy_a.migration_rate
            phenology = best.strategy_a.phenology_rate
            total = migration + phenology
            share = migration / total if total > 0.0 else 0.5
            if not best.joint_persisted:
                outcome = "failure"
            elif share >= 2.0 / 3.0:
                outcome = "migration"
            elif share <= 1.0 / 3.0:
                outcome = "phenology"
            else:
                outcome = "mixed"

            rows.append(
                {
                    "climate_velocity": velocity,
                    "phenology_limit": limit,
                    "migration_rate": migration,
                    "phenology_rate": phenology,
                    "migration_share": share,
                    "outcome": outcome,
                    "mean_joint_growth": best.mean_joint_growth,
                    "joint_persisted": int(best.joint_persisted),
                    "mean_centroid": 0.5
                    * (
                        best.mean_centroid_a
                        + best.mean_centroid_b
                    ),
                    "mean_phenology_shift": 0.5
                    * (
                        best.mean_phenology_a
                        + best.mean_phenology_b
                    ),
                    "mean_effective_tracking": 0.5
                    * (
                        best.mean_effective_tracking_a
                        + best.mean_effective_tracking_b
                    ),
                    "rms_abiotic_mismatch": 0.5
                    * (
                        best.rms_abiotic_mismatch_a
                        + best.rms_abiotic_mismatch_b
                    ),
                    "phenology_limit_fraction": 0.5
                    * (
                        best.phenology_limit_fraction_a
                        + best.phenology_limit_fraction_b
                    ),
                    "right_edge_mass_fraction": 0.5
                    * (
                        best.right_edge_mass_fraction_a
                        + best.right_edge_mass_fraction_b
                    ),
                }
            )
    return rows



def landscape_persistence_frontier(
    rows: list[dict[str, float | str | int]],
) -> list[dict[str, float | int | str | None]]:
    """Summarize the finite-horizon persistence frontier by phenology limit.

    The function does not assume monotonic persistence. It reports whether
    persistence is monotone non-increasing with climate velocity and gives the
    highest persisted velocity plus the first sampled failure above it.
    """

    if not rows:
        return []

    limits = sorted(
        {
            float(row["phenology_limit"])
            for row in rows
        }
    )
    out: list[dict[str, float | int | str | None]] = []

    for limit in limits:
        subset = sorted(
            (
                row
                for row in rows
                if float(row["phenology_limit"]) == limit
            ),
            key=lambda row: float(row["climate_velocity"]),
        )
        velocities = [
            float(row["climate_velocity"])
            for row in subset
        ]
        persisted = [
            int(row["joint_persisted"]) == 1
            for row in subset
        ]

        seen_failure = False
        monotone = True
        for value in persisted:
            if not value:
                seen_failure = True
            elif seen_failure:
                monotone = False

        persisted_rows = [
            row
            for row in subset
            if int(row["joint_persisted"]) == 1
        ]
        if persisted_rows:
            max_row = max(
                persisted_rows,
                key=lambda row: float(row["climate_velocity"]),
            )
            max_velocity = float(max_row["climate_velocity"])
            outcome_at_frontier = str(max_row["outcome"])
            migration_at_frontier = float(max_row["migration_rate"])
            phenology_at_frontier = float(max_row["phenology_rate"])
            edge_mass_at_frontier = float(
                max_row["right_edge_mass_fraction"]
            )
            limit_fraction_at_frontier = float(
                max_row["phenology_limit_fraction"]
            )
        else:
            max_velocity = None
            outcome_at_frontier = "none"
            migration_at_frontier = None
            phenology_at_frontier = None
            edge_mass_at_frontier = None
            limit_fraction_at_frontier = None

        failed_above = [
            row
            for row in subset
            if int(row["joint_persisted"]) == 0
            and (
                max_velocity is None
                or float(row["climate_velocity"]) > max_velocity
            )
        ]
        first_failed_velocity = (
            min(
                float(row["climate_velocity"])
                for row in failed_above
            )
            if failed_above
            else None
        )

        out.append(
            {
                "phenology_limit": limit,
                "sampled_velocity_min": min(velocities),
                "sampled_velocity_max": max(velocities),
                "max_persisted_velocity": max_velocity,
                "first_failed_velocity_above": first_failed_velocity,
                "monotone_persistence": int(monotone),
                "outcome_at_frontier": outcome_at_frontier,
                "migration_rate_at_frontier": migration_at_frontier,
                "phenology_rate_at_frontier": phenology_at_frontier,
                "right_edge_mass_at_frontier": edge_mass_at_frontier,
                "phenology_limit_fraction_at_frontier": (
                    limit_fraction_at_frontier
                ),
            }
        )

    return out



def geometric_tracking_capacity(
    scenario: MovingLandscapeScenario,
) -> float:
    """Maximum climate-equivalent offset available from space plus phenology."""

    edge_offset = (
        scenario.spatial_gradient
        * max(abs(position) for position in scenario.positions)
    )
    phenology_offset = (
        scenario.phenology_scale
        * scenario.max_abs_phenology_shift
    )
    return edge_offset + phenology_offset


def zero_mismatch_velocity_ceiling(
    scenario: MovingLandscapeScenario,
) -> float:
    """Velocity whose final demand exactly equals geometric tracking capacity.

    Above this value, no patch/phenology combination can have zero mismatch at
    the final simulated time. This is a geometric perfect-tracking ceiling, not
    a persistence threshold.
    """

    return geometric_tracking_capacity(scenario) / scenario.steps


def terminal_nonnegative_growth_velocity_ceiling(
    scenario: MovingLandscapeScenario,
    strategy: TrackingStrategy,
    parameters: SpeciesTrackingParameters,
) -> float | None:
    """Best-case final velocity compatible with nonnegative low-density growth.

    This assumes a matched interaction partner, placement at the favorable
    landscape edge, and phenology at its allowed bound. Density regulation is
    excluded because this is a low-density fitness ceiling.

    The value is not a persistence threshold: finite populations can remain
    present for a while even after terminal low-density growth becomes negative.
    """

    cost = architecture_cost(strategy, parameters)
    intrinsic = parameters.baseline_growth - cost
    if intrinsic < 0.0:
        return None
    if parameters.abiotic_strength == 0.0:
        return float("inf")

    mismatch_tolerance = sqrt(
        2.0 * intrinsic / parameters.abiotic_strength
    )
    return (
        geometric_tracking_capacity(scenario)
        + mismatch_tolerance
    ) / scenario.steps
