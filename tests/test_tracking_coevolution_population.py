from src.spatiotemporal_tracking import TrackingStrategy
from src.tracking_coevolution import (
    CoevolutionScenario,
    SpeciesTrackingParameters,
)
from src.tracking_coevolution_population import (
    coordination_barrier_population_consequence,
    pair_population_ensemble,
    simulate_pair_population,
)
from src.tracking_population import PopulationDynamics


def test_benign_matched_pair_can_persist():
    parameters = SpeciesTrackingParameters(
        interaction_strength=0.4,
        migration_cost=0.02,
        phenology_cost=0.02,
        baseline_growth=0.3,
    )
    scenario = CoevolutionScenario(
        climate_velocity=0.03,
        steps=100,
        burn_in=20,
        species_a=parameters,
        species_b=parameters,
    )
    population = PopulationDynamics(
        initial_population=150,
        carrying_capacity=300.0,
        density_coefficient=0.3,
    )
    result = simulate_pair_population(
        TrackingStrategy(0.4, 0.0),
        TrackingStrategy(0.4, 0.0),
        scenario,
        population,
        population,
        seed=1,
    )
    assert result.joint_persisted
    assert result.first_extinction_step is None
    assert result.final_population_a > 0
    assert result.final_population_b > 0


def test_axis_mismatch_can_cause_joint_system_loss():
    parameters = SpeciesTrackingParameters(
        interaction_strength=1.2,
        migration_cost=0.01,
        phenology_cost=0.01,
        baseline_growth=0.25,
    )
    scenario = CoevolutionScenario(
        climate_velocity=0.05,
        steps=120,
        burn_in=20,
        species_a=parameters,
        species_b=parameters,
    )
    population = PopulationDynamics(
        initial_population=100,
        carrying_capacity=220.0,
        density_coefficient=0.25,
    )
    ensemble = pair_population_ensemble(
        TrackingStrategy(0.5, 0.0),
        TrackingStrategy(0.0, 0.5),
        scenario,
        population,
        population,
        replicates=24,
        seed=300,
    )
    assert (
        ensemble.summary()["joint_extinction_fraction"]
        > 0.8
    )


def test_barrier_population_consequence_uses_same_local_and_matched_solutions():
    parameters = SpeciesTrackingParameters(
        interaction_strength=0.3,
        migration_cost=0.01,
        phenology_cost=0.12,
        baseline_growth=0.12,
    )
    scenario = CoevolutionScenario(
        climate_velocity=0.04,
        steps=140,
        burn_in=20,
        species_a=parameters,
        species_b=parameters,
    )
    population = PopulationDynamics(
        initial_population=50,
        carrying_capacity=100.0,
        density_coefficient=0.12,
        extinction_threshold=2,
    )
    consequence = coordination_barrier_population_consequence(
        scenario,
        population,
        population,
        replicates=24,
        seed=500,
        mutation_step=0.1,
        max_rate=1.0,
        max_cycles=40,
    )

    assert consequence.barrier
    assert consequence.accessibility_gap > 0.0
    assert (
        consequence.matched_optimum.strategy_a
        == consequence.matched_optimum.strategy_b
    )
    assert (
        consequence.matched_population.summary()[
            "joint_persistence_fraction"
        ]
        >= consequence.local_population.summary()[
            "joint_persistence_fraction"
        ]
    )


def test_pair_population_ensemble_is_seed_reproducible():
    parameters = SpeciesTrackingParameters(
        interaction_strength=0.2,
        baseline_growth=0.25,
    )
    scenario = CoevolutionScenario(
        climate_velocity=0.03,
        steps=60,
        burn_in=10,
        species_a=parameters,
        species_b=parameters,
    )
    population = PopulationDynamics(
        initial_population=60,
        carrying_capacity=120.0,
        density_coefficient=0.25,
    )
    first = pair_population_ensemble(
        TrackingStrategy(0.3, 0.2),
        TrackingStrategy(0.3, 0.2),
        scenario,
        population,
        population,
        replicates=6,
        seed=77,
    )
    second = pair_population_ensemble(
        TrackingStrategy(0.3, 0.2),
        TrackingStrategy(0.3, 0.2),
        scenario,
        population,
        population,
        replicates=6,
        seed=77,
    )
    assert first == second
