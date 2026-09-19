from src.spatiotemporal_tracking import TrackingStrategy
from src.tracking_coevolution import (
    CoevolutionScenario,
    SpeciesTrackingParameters,
    coevolve_tracking_pair,
    simulate_coevolving_pair,
)


def test_identical_strategies_have_zero_interaction_mismatch():
    scenario = CoevolutionScenario(
        climate_velocity=0.04,
        steps=100,
        burn_in=20,
    )
    strategy = TrackingStrategy(0.4, 0.3)
    result = simulate_coevolving_pair(
        strategy,
        strategy,
        scenario,
    )
    assert result.rms_interaction_mismatch == 0.0


def test_axis_mismatch_can_reduce_both_species_growth():
    strong = SpeciesTrackingParameters(
        interaction_strength=1.0,
        migration_cost=0.02,
        phenology_cost=0.02,
        baseline_growth=0.3,
    )
    scenario = CoevolutionScenario(
        climate_velocity=0.05,
        steps=120,
        burn_in=20,
        species_a=strong,
        species_b=strong,
    )
    matched = simulate_coevolving_pair(
        TrackingStrategy(0.6, 0.0),
        TrackingStrategy(0.6, 0.0),
        scenario,
    )
    mismatched = simulate_coevolving_pair(
        TrackingStrategy(0.6, 0.0),
        TrackingStrategy(0.0, 0.6),
        scenario,
    )
    assert mismatched.rms_interaction_mismatch > 0.0
    assert mismatched.mean_log_growth_a < matched.mean_log_growth_a
    assert mismatched.mean_log_growth_b < matched.mean_log_growth_b


def test_shared_migration_cost_advantage_drives_both_species_toward_migration():
    cheap_migration = SpeciesTrackingParameters(
        interaction_strength=0.3,
        migration_cost=0.01,
        phenology_cost=0.12,
        baseline_growth=0.35,
    )
    scenario = CoevolutionScenario(
        climate_velocity=0.04,
        steps=100,
        burn_in=20,
        species_a=cheap_migration,
        species_b=cheap_migration,
    )
    result = coevolve_tracking_pair(
        scenario,
        mutation_step=0.1,
        max_rate=1.0,
        max_cycles=40,
    )
    assert result.converged
    assert (
        result.final.strategy_a.migration_rate
        > result.final.strategy_a.phenology_rate
    )
    assert (
        result.final.strategy_b.migration_rate
        > result.final.strategy_b.phenology_rate
    )


def test_shared_phenology_cost_advantage_drives_both_species_toward_phenology():
    cheap_phenology = SpeciesTrackingParameters(
        interaction_strength=0.3,
        migration_cost=0.12,
        phenology_cost=0.01,
        baseline_growth=0.35,
    )
    scenario = CoevolutionScenario(
        climate_velocity=0.04,
        steps=100,
        burn_in=20,
        species_a=cheap_phenology,
        species_b=cheap_phenology,
    )
    result = coevolve_tracking_pair(
        scenario,
        mutation_step=0.1,
        max_rate=1.0,
        max_cycles=40,
    )
    assert result.converged
    assert (
        result.final.strategy_a.phenology_rate
        > result.final.strategy_a.migration_rate
    )
    assert (
        result.final.strategy_b.phenology_rate
        > result.final.strategy_b.migration_rate
    )


def test_each_substitution_improves_the_mutating_species():
    a = SpeciesTrackingParameters(
        interaction_strength=0.4,
        migration_cost=0.02,
        phenology_cost=0.08,
        baseline_growth=0.35,
    )
    b = SpeciesTrackingParameters(
        interaction_strength=0.4,
        migration_cost=0.08,
        phenology_cost=0.02,
        baseline_growth=0.35,
    )
    scenario = CoevolutionScenario(
        climate_velocity=0.04,
        steps=100,
        burn_in=20,
        species_a=a,
        species_b=b,
    )
    result = coevolve_tracking_pair(
        scenario,
        mutation_step=0.1,
        max_rate=1.0,
        max_cycles=20,
    )
    assert len(result.path) > 1
    # Alternating updates mean consecutive rows differ in exactly one species.
    for previous, current in zip(result.path, result.path[1:]):
        changed_a = current.strategy_a != previous.strategy_a
        changed_b = current.strategy_b != previous.strategy_b
        assert changed_a != changed_b
        if changed_a:
            assert current.mean_log_growth_a > previous.mean_log_growth_a
        else:
            assert current.mean_log_growth_b > previous.mean_log_growth_b
