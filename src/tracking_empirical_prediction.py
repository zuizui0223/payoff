"""Simulation-ready empirical prediction bridge for PAYOFF-B tracking.

This module keeps calibration and prediction separate.

Calibration identifies biological tracking controls:
- migration rate,
- x/y movement allocation,
- directional movement bias,
- phenology response rate when licensed,
- phenology scale and finite shift capacity.

Prediction can then change the external environmental forcing while freezing
those biological controls. Fitness terms must be supplied independently from
the matched-contrast identification layer.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite

from src.moving_climate_landscape_2d import (
    Landscape2DPairResult,
    MovingLandscape2DScenario,
    simulate_moving_landscape_2d_pair,
)
from src.spatiotemporal_tracking import TrackingStrategy
from src.tracking_coevolution import SpeciesTrackingParameters
from src.tracking_empirical_bridge import EmpiricalTrackingControls
from src.tracking_empirical_parameterization import (
    TrackingFitnessEstimate,
    climate_velocity_from_wave_speed,
)


@dataclass(frozen=True)
class EmpiricalLandscapeBundle:
    """Frozen biological controls plus one declared prediction environment."""

    controls: EmpiricalTrackingControls
    fitness: TrackingFitnessEstimate
    strategy: TrackingStrategy
    scenario: MovingLandscape2DScenario
    prediction_spatial_gradient: float
    prediction_wave_speed: float
    prediction_is_calibration_environment: bool

    @property
    def decision_interval_seconds(self) -> float:
        return self.controls.decision_interval_seconds


@dataclass(frozen=True)
class EmpiricalLandscapePrediction:
    """Single-species projection using the matched-duplicate landscape engine."""

    bundle: EmpiricalLandscapeBundle
    pair_result: Landscape2DPairResult

    @property
    def mean_low_density_growth(self) -> float:
        return self.pair_result.mean_log_growth_a

    @property
    def mean_realized_growth(self) -> float:
        return self.pair_result.mean_realized_log_growth_a

    @property
    def final_abundance(self) -> float:
        return self.pair_result.final_abundance_a

    @property
    def minimum_abundance(self) -> float:
        return self.pair_result.minimum_abundance_a

    @property
    def final_climate_centroid(self) -> float:
        return self.pair_result.final_climate_centroid_a

    @property
    def final_phenology_shift(self) -> float:
        return self.pair_result.final_phenology_a

    @property
    def rms_abiotic_mismatch(self) -> float:
        return self.pair_result.rms_abiotic_mismatch_a

    @property
    def phenology_limit_fraction(self) -> float:
        return self.pair_result.phenology_limit_fraction_a

    @property
    def persisted(self) -> bool:
        return self.pair_result.persisted_a


def species_parameters_from_tracking_fitness(
    fitness: TrackingFitnessEstimate,
) -> SpeciesTrackingParameters:
    """Map independently identified fitness terms to the landscape model."""

    return SpeciesTrackingParameters(
        abiotic_strength=fitness.abiotic_strength,
        interaction_strength=fitness.interaction_strength,
        migration_cost=fitness.migration_cost,
        phenology_cost=fitness.phenology_cost,
        joint_cost=fitness.joint_cost,
        baseline_growth=fitness.baseline_growth,
    )


def build_empirical_landscape_bundle(
    controls: EmpiricalTrackingControls,
    fitness: TrackingFitnessEstimate,
    *,
    width: int = 41,
    height: int = 21,
    prediction_spatial_gradient: float | None = None,
    prediction_wave_speed: float | None = None,
    initial_distribution_sd: float = 2.0,
    initial_total_abundance: float = 500.0,
    local_carrying_capacity: float = 100.0,
    density_coefficient: float = 0.30,
    extinction_threshold: float = 1.0,
    boundary_retention: float = 1.0,
    barrier_retention: float = 1.0,
    habitat_quality: tuple[float, ...] | None = None,
    steps: int = 120,
    burn_in: int = 30,
) -> EmpiricalLandscapeBundle:
    """Build a 2D prediction scenario without refitting biological controls.

    Full empirical prediction requires a licensed phenology rate. Movement-only
    controls remain useful diagnostics, but are not silently converted into h=0.
    """

    if not controls.full_tracking_controls_ready:
        raise ValueError(
            "full empirical landscape prediction requires a licensed "
            "timing-axis phenology rate; movement-only controls are partial"
        )
    assert controls.phenology_rate is not None

    gradient = (
        controls.spatial_gradient
        if prediction_spatial_gradient is None
        else prediction_spatial_gradient
    )
    wave_speed = (
        controls.environmental_wave_speed
        if prediction_wave_speed is None
        else prediction_wave_speed
    )
    for name, value in (
        ("prediction_spatial_gradient", gradient),
        ("prediction_wave_speed", wave_speed),
    ):
        if not isfinite(value):
            raise ValueError(f"{name} must be finite")
    if gradient <= 0.0:
        raise ValueError("prediction_spatial_gradient must be positive")

    parameters = species_parameters_from_tracking_fitness(fitness)
    strategy = TrackingStrategy(
        migration_rate=controls.migration_rate,
        phenology_rate=controls.phenology_rate,
    )
    scenario = MovingLandscape2DScenario(
        width=width,
        height=height,
        patch_spacing=controls.calibration_patch_spacing,
        spatial_gradient=gradient,
        climate_velocity=climate_velocity_from_wave_speed(
            gradient,
            wave_speed,
        ),
        climate_angle_degrees=controls.climate_axis_angle_degrees,
        phenology_scale=controls.phenology_scale,
        max_abs_phenology_shift=controls.max_abs_phenology_shift,
        initial_distribution_sd=initial_distribution_sd,
        initial_total_abundance=initial_total_abundance,
        local_carrying_capacity=local_carrying_capacity,
        density_coefficient=density_coefficient,
        extinction_threshold=extinction_threshold,
        boundary_retention=boundary_retention,
        barrier_retention=barrier_retention,
        dispersal_x_weight=controls.dispersal_x_weight,
        dispersal_y_weight=controls.dispersal_y_weight,
        dispersal_x_bias=controls.dispersal_x_bias,
        dispersal_y_bias=controls.dispersal_y_bias,
        habitat_quality=habitat_quality,
        steps=steps,
        burn_in=burn_in,
        species_a=parameters,
        species_b=parameters,
    )
    same_environment = (
        abs(gradient - controls.spatial_gradient) <= 1e-12
        and abs(wave_speed - controls.environmental_wave_speed) <= 1e-12
    )
    return EmpiricalLandscapeBundle(
        controls=controls,
        fitness=fitness,
        strategy=strategy,
        scenario=scenario,
        prediction_spatial_gradient=gradient,
        prediction_wave_speed=wave_speed,
        prediction_is_calibration_environment=same_environment,
    )


def simulate_empirical_landscape_prediction(
    bundle: EmpiricalLandscapeBundle,
) -> EmpiricalLandscapePrediction:
    """Run a focal-species projection with interaction mismatch identically zero.

    The pair engine is used with identical strategy, fitness and initial
    distribution for both copies. Their interaction distance is therefore zero
    by construction, so the returned A trajectory is exactly the focal
    single-species abiotic/demographic projection under the declared controls.
    """

    result = simulate_moving_landscape_2d_pair(
        bundle.strategy,
        bundle.strategy,
        bundle.scenario,
    )
    if result.rms_interaction_mismatch > 1e-10:
        raise RuntimeError(
            "matched-duplicate single-species projection developed "
            "non-zero interaction mismatch"
        )
    return EmpiricalLandscapePrediction(
        bundle=bundle,
        pair_result=result,
    )
