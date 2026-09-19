"""Two-dimensional moving-climate landscapes with heterogeneous habitat.

The one-dimensional moving-landscape result is generalized to a rectangular
grid. Climate moves along a declared spatial direction, while dispersal occurs
among the four cardinal neighbors. Habitat quality controls local carrying
capacity and can also create fully blocked cells.

This makes two-dimensional geometry scientifically non-redundant: a vertical
barrier with a finite gap creates a corridor bottleneck that cannot be reduced
to a one-dimensional climate projection.

Evolutionary fitness remains abundance-weighted low-density growth. Local
density regulation affects demographic abundance only.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import cos, exp, expm1, isfinite, pi, sin, sqrt

from src.spatiotemporal_tracking import TrackingStrategy
from src.tracking_coevolution import SpeciesTrackingParameters


@dataclass(frozen=True)
class MovingLandscape2DScenario:
    width: int = 41
    height: int = 21
    patch_spacing: float = 1.0
    spatial_gradient: float = 0.20
    climate_velocity: float = 0.03
    climate_angle_degrees: float = 0.0
    phenology_scale: float = 1.0
    max_abs_phenology_shift: float = 2.0
    initial_distribution_sd: float = 2.0
    initial_total_abundance: float = 500.0
    local_carrying_capacity: float = 100.0
    density_coefficient: float = 0.30
    extinction_threshold: float = 1.0
    boundary_retention: float = 1.0
    barrier_retention: float = 1.0
    monitor_climate_coordinate: float | None = None
    habitat_quality: tuple[float, ...] | None = None
    steps: int = 120
    burn_in: int = 30
    species_a: SpeciesTrackingParameters = SpeciesTrackingParameters(
        baseline_growth=0.30,
    )
    species_b: SpeciesTrackingParameters = SpeciesTrackingParameters(
        baseline_growth=0.30,
    )

    def __post_init__(self) -> None:
        if self.width < 3 or self.height < 3:
            raise ValueError("width and height must be at least 3")
        if self.width % 2 == 0 or self.height % 2 == 0:
            raise ValueError(
                "width and height must be odd so the initial optimum is centered"
            )
        for name in (
            "patch_spacing",
            "spatial_gradient",
            "phenology_scale",
            "max_abs_phenology_shift",
            "initial_distribution_sd",
            "initial_total_abundance",
            "local_carrying_capacity",
            "density_coefficient",
            "extinction_threshold",
            "boundary_retention",
            "barrier_retention",
            "climate_velocity",
            "climate_angle_degrees",
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
        if self.initial_total_abundance < 0.0:
            raise ValueError("initial_total_abundance must be non-negative")
        if self.local_carrying_capacity <= 0.0:
            raise ValueError("local_carrying_capacity must be positive")
        if self.density_coefficient < 0.0:
            raise ValueError("density_coefficient must be non-negative")
        if self.extinction_threshold < 0.0:
            raise ValueError("extinction_threshold must be non-negative")
        if not 0.0 <= self.boundary_retention <= 1.0:
            raise ValueError("boundary_retention must lie in [0,1]")
        if not 0.0 <= self.barrier_retention <= 1.0:
            raise ValueError("barrier_retention must lie in [0,1]")
        if self.monitor_climate_coordinate is not None and not isfinite(
            self.monitor_climate_coordinate
        ):
            raise ValueError(
                "monitor_climate_coordinate must be finite when supplied"
            )
        if self.steps <= 0:
            raise ValueError("steps must be positive")
        if not 0 <= self.burn_in < self.steps:
            raise ValueError("burn_in must satisfy 0 <= burn_in < steps")

        quality = self.quality
        if len(quality) != self.width * self.height:
            raise ValueError("habitat_quality length must equal width*height")
        if any(
            (not isfinite(value)) or value < 0.0 or value > 1.0
            for value in quality
        ):
            raise ValueError("habitat qualities must lie in [0,1]")
        if not any(value > 0.0 for value in quality):
            raise ValueError("at least one habitat cell must be available")
        center = self.index(self.width // 2, self.height // 2)
        if quality[center] <= 0.0:
            raise ValueError("the centered initial optimum must be habitable")

    @property
    def quality(self) -> tuple[float, ...]:
        if self.habitat_quality is None:
            return (1.0,) * (self.width * self.height)
        return tuple(float(value) for value in self.habitat_quality)

    @property
    def climate_unit(self) -> tuple[float, float]:
        angle = self.climate_angle_degrees * pi / 180.0
        return cos(angle), sin(angle)

    def index(self, x_index: int, y_index: int) -> int:
        if not 0 <= x_index < self.width:
            raise ValueError("x_index out of bounds")
        if not 0 <= y_index < self.height:
            raise ValueError("y_index out of bounds")
        return y_index * self.width + x_index

    def coordinate_indices(self, index: int) -> tuple[int, int]:
        if not 0 <= index < self.width * self.height:
            raise ValueError("cell index out of bounds")
        return index % self.width, index // self.width

    def position(self, index: int) -> tuple[float, float]:
        x_index, y_index = self.coordinate_indices(index)
        x = (
            x_index - self.width // 2
        ) * self.patch_spacing
        y = (
            y_index - self.height // 2
        ) * self.patch_spacing
        return x, y

    def climate_coordinate(self, index: int) -> float:
        x, y = self.position(index)
        ux, uy = self.climate_unit
        return ux * x + uy * y


@dataclass(frozen=True)
class Landscape2DGeometry:
    x_positions: tuple[float, ...]
    y_positions: tuple[float, ...]
    climate_coordinates: tuple[float, ...]
    neighbor_targets: tuple[tuple[int, int, int, int], ...]


def build_landscape_2d_geometry(
    scenario: MovingLandscape2DScenario,
) -> Landscape2DGeometry:
    """Precompute static geometry once for repeated strategy evaluation."""

    quality = scenario.quality
    ux, uy = scenario.climate_unit
    x_positions: list[float] = []
    y_positions: list[float] = []
    climate_coordinates: list[float] = []
    neighbors: list[tuple[int, int, int, int]] = []
    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))

    for index in range(scenario.width * scenario.height):
        x_index, y_index = scenario.coordinate_indices(index)
        x = (
            x_index - scenario.width // 2
        ) * scenario.patch_spacing
        y = (
            y_index - scenario.height // 2
        ) * scenario.patch_spacing
        x_positions.append(x)
        y_positions.append(y)
        climate_coordinates.append(ux * x + uy * y)

        local_neighbors: list[int] = []
        for dx, dy in directions:
            target_x = x_index + dx
            target_y = y_index + dy
            if (
                target_x < 0
                or target_x >= scenario.width
                or target_y < 0
                or target_y >= scenario.height
            ):
                local_neighbors.append(-1)  # outer boundary
                continue
            target = target_y * scenario.width + target_x
            if quality[target] <= 0.0:
                local_neighbors.append(-2)  # habitat barrier
            else:
                local_neighbors.append(target)
        neighbors.append(tuple(local_neighbors))

    return Landscape2DGeometry(
        x_positions=tuple(x_positions),
        y_positions=tuple(y_positions),
        climate_coordinates=tuple(climate_coordinates),
        neighbor_targets=tuple(neighbors),
    )


@dataclass(frozen=True)
class Landscape2DPairResult:
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
    final_centroid_x_a: float
    final_centroid_y_a: float
    final_centroid_x_b: float
    final_centroid_y_b: float
    final_climate_centroid_a: float
    final_climate_centroid_b: float
    final_phenology_a: float
    final_phenology_b: float
    rms_abiotic_mismatch_a: float
    rms_abiotic_mismatch_b: float
    rms_interaction_mismatch: float
    phenology_limit_fraction_a: float
    phenology_limit_fraction_b: float
    final_monitor_fraction_a: float
    final_monitor_fraction_b: float
    mean_monitor_fraction_a: float
    mean_monitor_fraction_b: float
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


def vertical_barrier_habitat(
    width: int,
    height: int,
    *,
    barrier_x_index: int,
    gap_width: int,
    gap_center_y_index: int | None = None,
    background_quality: float = 1.0,
) -> tuple[float, ...]:
    """Return habitat with a one-cell vertical wall and centered passable gap."""

    if width < 3 or height < 3:
        raise ValueError("width and height must be at least 3")
    if not 0 <= barrier_x_index < width:
        raise ValueError("barrier_x_index out of bounds")
    if gap_width < 0 or gap_width > height:
        raise ValueError("gap_width must lie between 0 and height")
    if not 0.0 < background_quality <= 1.0:
        raise ValueError("background_quality must lie in (0,1]")

    quality = [background_quality] * (width * height)
    if gap_width >= height:
        return tuple(quality)

    center = (
        height // 2
        if gap_center_y_index is None
        else gap_center_y_index
    )
    if not 0 <= center < height:
        raise ValueError("gap_center_y_index out of bounds")
    if gap_width == 0:
        gap_rows: set[int] = set()
    else:
        lower = center - (gap_width - 1) // 2
        upper = lower + gap_width
        if lower < 0 or upper > height:
            raise ValueError("gap does not fit inside the landscape height")
        gap_rows = set(range(lower, upper))

    for y_index in range(height):
        if y_index not in gap_rows:
            quality[y_index * width + barrier_x_index] = 0.0
    return tuple(quality)


def dispersal_fraction(migration_rate: float) -> float:
    if migration_rate < 0.0 or not isfinite(migration_rate):
        raise ValueError("migration_rate must be non-negative and finite")
    if migration_rate == 0.0:
        return 0.0
    return -expm1(-migration_rate)


def grid_dispersal_2d(
    abundance: tuple[float, ...] | list[float],
    migration_rate: float,
    scenario: MovingLandscape2DScenario,
    geometry: Landscape2DGeometry | None = None,
) -> tuple[float, ...]:
    """Four-neighbor dispersal respecting boundaries and blocked habitat."""

    if len(abundance) != scenario.width * scenario.height:
        raise ValueError("abundance length must match the 2D landscape")
    if any(value < 0.0 or not isfinite(value) for value in abundance):
        raise ValueError("abundance must be finite and non-negative")

    fraction = dispersal_fraction(migration_rate)
    if fraction == 0.0:
        return tuple(float(value) for value in abundance)

    if geometry is None:
        geometry = build_landscape_2d_geometry(scenario)
    out = [0.0] * len(abundance)

    for index, value in enumerate(abundance):
        if value <= 0.0:
            continue
        moving = fraction * value
        out[index] += value - moving
        directional_mass = moving / 4.0

        for target in geometry.neighbor_targets[index]:
            if target == -1:
                out[index] += (
                    scenario.boundary_retention
                    * directional_mass
                )
            elif target == -2:
                out[index] += (
                    scenario.barrier_retention
                    * directional_mass
                )
            else:
                out[target] += directional_mass

    return tuple(out)


def gaussian_initial_distribution_2d(
    scenario: MovingLandscape2DScenario,
    geometry: Landscape2DGeometry | None = None,
) -> tuple[float, ...]:
    quality = scenario.quality
    if geometry is None:
        geometry = build_landscape_2d_geometry(scenario)
    weights = []
    variance = scenario.initial_distribution_sd ** 2
    for index in range(scenario.width * scenario.height):
        x = geometry.x_positions[index]
        y = geometry.y_positions[index]
        weights.append(
            quality[index]
            * exp(-0.5 * (x * x + y * y) / variance)
        )
    total_weight = sum(weights)
    if total_weight <= 0.0:
        raise ValueError("initial habitat contains no usable mass")
    return tuple(
        scenario.initial_total_abundance
        * weight
        / total_weight
        for weight in weights
    )


def centroid_2d(
    abundance: tuple[float, ...] | list[float],
    scenario: MovingLandscape2DScenario,
    geometry: Landscape2DGeometry | None = None,
) -> tuple[float, float]:
    total = sum(abundance)
    if total <= 0.0:
        return 0.0, 0.0
    if geometry is None:
        geometry = build_landscape_2d_geometry(scenario)
    x_sum = 0.0
    y_sum = 0.0
    for index, value in enumerate(abundance):
        x_sum += value * geometry.x_positions[index]
        y_sum += value * geometry.y_positions[index]
    return x_sum / total, y_sum / total


def climate_centroid_2d(
    abundance: tuple[float, ...] | list[float],
    scenario: MovingLandscape2DScenario,
    geometry: Landscape2DGeometry | None = None,
) -> float:
    x, y = centroid_2d(abundance, scenario, geometry)
    ux, uy = scenario.climate_unit
    return ux * x + uy * y


def monitor_fraction_2d(
    abundance: tuple[float, ...] | list[float],
    scenario: MovingLandscape2DScenario,
    geometry: Landscape2DGeometry | None = None,
) -> float:
    threshold = scenario.monitor_climate_coordinate
    if threshold is None:
        return 0.0
    total = sum(abundance)
    if total <= 0.0:
        return 0.0
    if geometry is None:
        geometry = build_landscape_2d_geometry(scenario)
    beyond = sum(
        value
        for index, value in enumerate(abundance)
        if geometry.climate_coordinates[index] > threshold
    )
    return beyond / total


def _weighted_residual_2d(
    abundance: tuple[float, ...],
    phenology_shift: float,
    demand: float,
    scenario: MovingLandscape2DScenario,
    geometry: Landscape2DGeometry,
) -> float:
    total = sum(abundance)
    if total <= 0.0:
        return 0.0
    return sum(
        value
        * (
            demand
            - scenario.spatial_gradient
            * geometry.climate_coordinates[index]
            - scenario.phenology_scale * phenology_shift
        )
        for index, value in enumerate(abundance)
    ) / total


def _update_phenology_2d(
    abundance: tuple[float, ...],
    strategy: TrackingStrategy,
    current_shift: float,
    demand: float,
    scenario: MovingLandscape2DScenario,
    geometry: Landscape2DGeometry,
) -> tuple[float, bool]:
    if strategy.phenology_rate <= 0.0:
        return current_shift, False
    residual = _weighted_residual_2d(
        abundance,
        current_shift,
        demand,
        scenario,
        geometry,
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


def _architecture_cost(
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


def _one_species_generation_2d(
    abundance: tuple[float, ...],
    strategy: TrackingStrategy,
    parameters: SpeciesTrackingParameters,
    phenology_shift: float,
    demand: float,
    interaction_sq: float,
    scenario: MovingLandscape2DScenario,
    geometry: Landscape2DGeometry,
) -> tuple[tuple[float, ...], float, float]:
    total = sum(abundance)
    if total <= 0.0:
        return (
            tuple(0.0 for _ in abundance),
            0.0,
            0.0,
        )

    quality = scenario.quality
    cost = _architecture_cost(strategy, parameters)
    reproduced = [0.0] * len(abundance)
    low_sum = 0.0
    realized_sum = 0.0

    for index, value in enumerate(abundance):
        if value <= 0.0:
            continue
        local_quality = quality[index]
        if local_quality <= 0.0:
            continue
        mismatch = (
            demand
            - scenario.spatial_gradient
            * geometry.climate_coordinates[index]
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
        local_capacity = (
            scenario.local_carrying_capacity
            * local_quality
        )
        density_penalty = (
            scenario.density_coefficient
            * value
            / local_capacity
        )
        realized_growth = (
            low_density_growth - density_penalty
        )
        low_sum += value * low_density_growth
        realized_sum += value * realized_growth
        reproduced[index] = value * exp(realized_growth)

    dispersed = grid_dispersal_2d(
        reproduced,
        strategy.migration_rate,
        scenario,
        geometry,
    )
    return (
        dispersed,
        low_sum / total,
        realized_sum / total,
    )


def _rms_abiotic_2d(
    abundance: tuple[float, ...],
    phenology_shift: float,
    demand: float,
    scenario: MovingLandscape2DScenario,
    geometry: Landscape2DGeometry,
) -> float:
    total = sum(abundance)
    if total <= 0.0:
        return 0.0
    value = sum(
        abundance_value
        * (
            demand
            - scenario.spatial_gradient
            * geometry.climate_coordinates[index]
            - scenario.phenology_scale * phenology_shift
        ) ** 2
        for index, abundance_value in enumerate(abundance)
    ) / total
    return sqrt(value)


def simulate_moving_landscape_2d_pair(
    strategy_a: TrackingStrategy,
    strategy_b: TrackingStrategy,
    scenario: MovingLandscape2DScenario,
    *,
    initial_abundance_a: tuple[float, ...] | None = None,
    initial_abundance_b: tuple[float, ...] | None = None,
    _geometry: Landscape2DGeometry | None = None,
) -> Landscape2DPairResult:
    geometry = (
        build_landscape_2d_geometry(scenario)
        if _geometry is None
        else _geometry
    )
    if initial_abundance_a is None:
        abundance_a = gaussian_initial_distribution_2d(
            scenario,
            geometry,
        )
    else:
        abundance_a = tuple(initial_abundance_a)
    if initial_abundance_b is None:
        abundance_b = gaussian_initial_distribution_2d(
            scenario,
            geometry,
        )
    else:
        abundance_b = tuple(initial_abundance_b)

    expected_length = scenario.width * scenario.height
    if len(abundance_a) != expected_length:
        raise ValueError("initial_abundance_a length mismatch")
    if len(abundance_b) != expected_length:
        raise ValueError("initial_abundance_b length mismatch")

    phenology_a = 0.0
    phenology_b = 0.0
    minimum_a = sum(abundance_a)
    minimum_b = sum(abundance_b)

    low_growth_a_sum = 0.0
    low_growth_b_sum = 0.0
    realized_growth_a_sum = 0.0
    realized_growth_b_sum = 0.0
    abiotic_sq_a_sum = 0.0
    abiotic_sq_b_sum = 0.0
    interaction_sq_sum = 0.0
    monitor_a_sum = 0.0
    monitor_b_sum = 0.0
    limit_a_count = 0
    limit_b_count = 0
    observed = 0

    for step in range(1, scenario.steps + 1):
        demand = scenario.climate_velocity * step

        phenology_a, at_limit_a = _update_phenology_2d(
            abundance_a,
            strategy_a,
            phenology_a,
            demand,
            scenario,
            geometry,
        )
        phenology_b, at_limit_b = _update_phenology_2d(
            abundance_b,
            strategy_b,
            phenology_b,
            demand,
            scenario,
            geometry,
        )

        centroid_x_a, centroid_y_a = centroid_2d(
            abundance_a,
            scenario,
            geometry,
        )
        centroid_x_b, centroid_y_b = centroid_2d(
            abundance_b,
            scenario,
            geometry,
        )
        dx = scenario.spatial_gradient * (
            centroid_x_a - centroid_x_b
        )
        dy = scenario.spatial_gradient * (
            centroid_y_a - centroid_y_b
        )
        dz = scenario.phenology_scale * (
            phenology_a - phenology_b
        )
        interaction_sq = dx * dx + dy * dy + dz * dz

        (
            abundance_a,
            low_growth_a,
            realized_growth_a,
        ) = _one_species_generation_2d(
            abundance_a,
            strategy_a,
            scenario.species_a,
            phenology_a,
            demand,
            interaction_sq,
            scenario,
            geometry,
        )
        (
            abundance_b,
            low_growth_b,
            realized_growth_b,
        ) = _one_species_generation_2d(
            abundance_b,
            strategy_b,
            scenario.species_b,
            phenology_b,
            demand,
            interaction_sq,
            scenario,
            geometry,
        )

        total_a = sum(abundance_a)
        total_b = sum(abundance_b)
        minimum_a = min(minimum_a, total_a)
        minimum_b = min(minimum_b, total_b)

        if step > scenario.burn_in:
            observed += 1
            low_growth_a_sum += low_growth_a
            low_growth_b_sum += low_growth_b
            realized_growth_a_sum += realized_growth_a
            realized_growth_b_sum += realized_growth_b
            rms_a = _rms_abiotic_2d(
                abundance_a,
                phenology_a,
                demand,
                scenario,
                geometry,
            )
            rms_b = _rms_abiotic_2d(
                abundance_b,
                phenology_b,
                demand,
                scenario,
                geometry,
            )
            abiotic_sq_a_sum += rms_a * rms_a
            abiotic_sq_b_sum += rms_b * rms_b
            interaction_sq_sum += interaction_sq
            monitor_a_sum += monitor_fraction_2d(
                abundance_a,
                scenario,
                geometry,
            )
            monitor_b_sum += monitor_fraction_2d(
                abundance_b,
                scenario,
                geometry,
            )
            limit_a_count += int(at_limit_a)
            limit_b_count += int(at_limit_b)

    if observed <= 0:
        raise RuntimeError("no post-burn-in observations")

    final_x_a, final_y_a = centroid_2d(
        abundance_a,
        scenario,
        geometry,
    )
    final_x_b, final_y_b = centroid_2d(
        abundance_b,
        scenario,
        geometry,
    )
    ux, uy = scenario.climate_unit
    final_climate_a = ux * final_x_a + uy * final_y_a
    final_climate_b = ux * final_x_b + uy * final_y_b
    final_a = sum(abundance_a)
    final_b = sum(abundance_b)

    return Landscape2DPairResult(
        strategy_a=strategy_a,
        strategy_b=strategy_b,
        mean_log_growth_a=low_growth_a_sum / observed,
        mean_log_growth_b=low_growth_b_sum / observed,
        mean_realized_log_growth_a=(
            realized_growth_a_sum / observed
        ),
        mean_realized_log_growth_b=(
            realized_growth_b_sum / observed
        ),
        final_abundance_a=final_a,
        final_abundance_b=final_b,
        minimum_abundance_a=minimum_a,
        minimum_abundance_b=minimum_b,
        final_centroid_x_a=final_x_a,
        final_centroid_y_a=final_y_a,
        final_centroid_x_b=final_x_b,
        final_centroid_y_b=final_y_b,
        final_climate_centroid_a=final_climate_a,
        final_climate_centroid_b=final_climate_b,
        final_phenology_a=phenology_a,
        final_phenology_b=phenology_b,
        rms_abiotic_mismatch_a=sqrt(
            abiotic_sq_a_sum / observed
        ),
        rms_abiotic_mismatch_b=sqrt(
            abiotic_sq_b_sum / observed
        ),
        rms_interaction_mismatch=sqrt(
            interaction_sq_sum / observed
        ),
        phenology_limit_fraction_a=limit_a_count / observed,
        phenology_limit_fraction_b=limit_b_count / observed,
        final_monitor_fraction_a=monitor_fraction_2d(
            abundance_a,
            scenario,
            geometry,
        ),
        final_monitor_fraction_b=monitor_fraction_2d(
            abundance_b,
            scenario,
            geometry,
        ),
        mean_monitor_fraction_a=monitor_a_sum / observed,
        mean_monitor_fraction_b=monitor_b_sum / observed,
        persisted_a=final_a > scenario.extinction_threshold,
        persisted_b=final_b > scenario.extinction_threshold,
    )


def optimize_matched_2d_strategy(
    scenario: MovingLandscape2DScenario,
    *,
    max_migration_rate: float = 1.0,
    max_phenology_rate: float = 1.0,
    migration_points: int = 7,
    phenology_points: int = 7,
) -> Landscape2DPairResult:
    if max_migration_rate < 0.0 or max_phenology_rate < 0.0:
        raise ValueError("maximum rates must be non-negative")
    if migration_points < 2 or phenology_points < 2:
        raise ValueError("grid points must be at least 2")

    migration_values = [
        max_migration_rate * index / (migration_points - 1)
        for index in range(migration_points)
    ]
    phenology_values = [
        max_phenology_rate * index / (phenology_points - 1)
        for index in range(phenology_points)
    ]

    geometry = build_landscape_2d_geometry(scenario)
    best: Landscape2DPairResult | None = None
    for migration in migration_values:
        for phenology in phenology_values:
            strategy = TrackingStrategy(
                migration,
                phenology,
            )
            candidate = simulate_moving_landscape_2d_pair(
                strategy,
                strategy,
                scenario,
                _geometry=geometry,
            )
            if best is None:
                best = candidate
                continue
            if candidate.mean_joint_growth > best.mean_joint_growth:
                best = candidate
            elif (
                candidate.mean_joint_growth
                == best.mean_joint_growth
                and strategy.total_rate
                < best.strategy_a.total_rate
            ):
                best = candidate

    assert best is not None
    return best
