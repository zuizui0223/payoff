"""State-dependent movement feedback on the explicit 2D tracking landscape.

This module adds an Aikens-like behavioral controller to the existing spatial
tracking model without changing the canonical fixed-rate simulator.

The base strategy still contains:
- baseline migration kernel rate m0;
- independent timing-axis phenology rate h.

A movement-rate controller responds to current abundance-weighted mismatch e:

    m_eff = clip(m0 + k_m e, m_min, m_max).

Positive mismatch means the population is lagging the moving environmental
demand along the declared climate coordinate, so positive controller gain
increases movement. Negative mismatch slows movement rather than reversing
direction. Direction itself remains controlled by the existing x/y movement
biases.

The controller gain k_m is not the local closed-loop feedback fraction q_m.
The latter is an induced correction effect. This explicit model is used to test
how state-dependent movement behaves once spatial geometry and demographic
costs are restored.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt

from src.moving_climate_landscape_2d import (
    MovingLandscape2DScenario,
    _one_species_generation_2d,
    _rms_abiotic_2d,
    _update_phenology_2d,
    _weighted_residual_2d,
    build_landscape_2d_geometry,
    centroid_2d,
    gaussian_initial_distribution_2d,
)
from src.spatiotemporal_tracking import TrackingStrategy


@dataclass(frozen=True)
class MovementRateFeedbackController:
    gain: float = 0.0
    min_migration_rate: float = 0.0
    max_migration_rate: float | None = None

    def __post_init__(self) -> None:
        if not isfinite(self.gain) or self.gain < 0.0:
            raise ValueError("gain must be non-negative and finite")
        if (
            not isfinite(self.min_migration_rate)
            or self.min_migration_rate < 0.0
        ):
            raise ValueError(
                "min_migration_rate must be non-negative and finite"
            )
        if self.max_migration_rate is not None:
            if (
                not isfinite(self.max_migration_rate)
                or self.max_migration_rate < self.min_migration_rate
            ):
                raise ValueError(
                    "max_migration_rate must be finite and >= minimum"
                )

    def effective_rate(
        self,
        baseline_rate: float,
        mismatch: float,
    ) -> tuple[float, bool, bool]:
        if not isfinite(baseline_rate) or baseline_rate < 0.0:
            raise ValueError(
                "baseline_rate must be non-negative and finite"
            )
        if not isfinite(mismatch):
            raise ValueError("mismatch must be finite")

        proposed = baseline_rate + self.gain * mismatch
        floor_hit = proposed < self.min_migration_rate
        rate = max(self.min_migration_rate, proposed)

        ceiling_hit = False
        if self.max_migration_rate is not None:
            ceiling_hit = rate > self.max_migration_rate
            rate = min(rate, self.max_migration_rate)

        return rate, floor_hit, ceiling_hit


@dataclass(frozen=True)
class ControlledLandscapeResult:
    strategy: TrackingStrategy
    controller: MovementRateFeedbackController
    mean_low_density_growth: float
    mean_realized_growth: float
    final_abundance: float
    minimum_abundance: float
    final_centroid_x: float
    final_centroid_y: float
    final_climate_centroid: float
    final_phenology_shift: float
    rms_abiotic_mismatch: float
    phenology_limit_fraction: float
    mean_precontrol_mismatch: float
    mean_effective_migration_rate: float
    minimum_effective_migration_rate: float
    maximum_effective_migration_rate: float
    controller_floor_fraction: float
    controller_ceiling_fraction: float
    persisted: bool


def simulate_controlled_moving_landscape_2d(
    strategy: TrackingStrategy,
    scenario: MovingLandscape2DScenario,
    controller: MovementRateFeedbackController,
    *,
    initial_abundance: tuple[float, ...] | None = None,
) -> ControlledLandscapeResult:
    """Simulate one focal species with mismatch-dependent movement rate."""

    geometry = build_landscape_2d_geometry(scenario)
    if initial_abundance is None:
        abundance = gaussian_initial_distribution_2d(
            scenario,
            geometry,
        )
    else:
        abundance = tuple(initial_abundance)
    if len(abundance) != scenario.width * scenario.height:
        raise ValueError(
            "initial_abundance length must equal width*height"
        )

    phenology = 0.0
    minimum_abundance = sum(abundance)

    low_growth_sum = 0.0
    realized_growth_sum = 0.0
    abiotic_sq_sum = 0.0
    precontrol_sum = 0.0
    effective_rate_sum = 0.0
    effective_rates: list[float] = []
    floor_count = 0
    ceiling_count = 0
    phenology_limit_count = 0
    observed = 0

    for step in range(1, scenario.steps + 1):
        demand = scenario.climate_velocity * step

        precontrol_mismatch = _weighted_residual_2d(
            abundance,
            phenology,
            demand,
            scenario,
            geometry,
        )
        (
            effective_migration_rate,
            floor_hit,
            ceiling_hit,
        ) = controller.effective_rate(
            strategy.migration_rate,
            precontrol_mismatch,
        )
        realized_strategy = TrackingStrategy(
            effective_migration_rate,
            strategy.phenology_rate,
        )

        phenology, at_limit = _update_phenology_2d(
            abundance,
            realized_strategy,
            phenology,
            demand,
            scenario,
            geometry,
        )

        (
            abundance,
            low_growth,
            realized_growth,
        ) = _one_species_generation_2d(
            abundance,
            realized_strategy,
            scenario.species_a,
            phenology,
            demand,
            0.0,
            scenario,
            geometry,
        )

        total = sum(abundance)
        minimum_abundance = min(minimum_abundance, total)

        if step > scenario.burn_in:
            observed += 1
            low_growth_sum += low_growth
            realized_growth_sum += realized_growth
            rms = _rms_abiotic_2d(
                abundance,
                phenology,
                demand,
                scenario,
                geometry,
            )
            abiotic_sq_sum += rms * rms
            precontrol_sum += precontrol_mismatch
            effective_rate_sum += effective_migration_rate
            effective_rates.append(effective_migration_rate)
            floor_count += int(floor_hit)
            ceiling_count += int(ceiling_hit)
            phenology_limit_count += int(at_limit)

    if observed <= 0:
        raise RuntimeError("no post-burn-in observations")

    centroid_x, centroid_y = centroid_2d(
        abundance,
        scenario,
        geometry,
    )
    ux, uy = scenario.climate_unit
    final_climate_centroid = (
        ux * centroid_x + uy * centroid_y
    )
    final_abundance = sum(abundance)

    return ControlledLandscapeResult(
        strategy=strategy,
        controller=controller,
        mean_low_density_growth=low_growth_sum / observed,
        mean_realized_growth=realized_growth_sum / observed,
        final_abundance=final_abundance,
        minimum_abundance=minimum_abundance,
        final_centroid_x=centroid_x,
        final_centroid_y=centroid_y,
        final_climate_centroid=final_climate_centroid,
        final_phenology_shift=phenology,
        rms_abiotic_mismatch=sqrt(
            abiotic_sq_sum / observed
        ),
        phenology_limit_fraction=(
            phenology_limit_count / observed
        ),
        mean_precontrol_mismatch=precontrol_sum / observed,
        mean_effective_migration_rate=(
            effective_rate_sum / observed
        ),
        minimum_effective_migration_rate=min(
            effective_rates
        ),
        maximum_effective_migration_rate=max(
            effective_rates
        ),
        controller_floor_fraction=floor_count / observed,
        controller_ceiling_fraction=ceiling_count / observed,
        persisted=(
            final_abundance > scenario.extinction_threshold
        ),
    )
