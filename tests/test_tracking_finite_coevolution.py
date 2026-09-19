from src.tracking_coevolution import (
    CoevolutionScenario,
    SpeciesTrackingParameters,
)
from src.tracking_finite_coevolution import (
    build_pair_growth_landscape,
    finite_coevolution_escape_ensemble,
    simulate_finite_coevolution_escape,
)
from src.tracking_mutation_selection import StrategyLattice


def barrier_scenario():
    parameters = SpeciesTrackingParameters(
        interaction_strength=0.3,
        migration_cost=0.01,
        phenology_cost=0.12,
        baseline_growth=0.35,
    )
    return CoevolutionScenario(
        climate_velocity=0.04,
        steps=80,
        burn_in=20,
        species_a=parameters,
        species_b=parameters,
    )


def test_pair_growth_landscape_recovers_positive_coordination_gap():
    lattice = StrategyLattice(max_rate=0.8, points=9)
    landscape = build_pair_growth_landscape(
        barrier_scenario(),
        lattice,
    )
    assert landscape.accessibility_gap > 0.0
    assert landscape.local_state != landscape.matched_state


def test_finite_coevolution_escape_is_seed_reproducible():
    lattice = StrategyLattice(max_rate=0.8, points=5)
    landscape = build_pair_growth_landscape(
        barrier_scenario(),
        lattice,
    )
    first = simulate_finite_coevolution_escape(
        landscape,
        population_size_a=20,
        selection_strength=10.0,
        mutation_events=500,
        evolutionary_burn_in=100,
        seed=123,
    )
    second = simulate_finite_coevolution_escape(
        landscape,
        population_size_a=20,
        selection_strength=10.0,
        mutation_events=500,
        evolutionary_burn_in=100,
        seed=123,
    )
    assert first == second


def test_neutral_finite_coevolution_accepts_drift_substitutions():
    lattice = StrategyLattice(max_rate=0.8, points=5)
    landscape = build_pair_growth_landscape(
        barrier_scenario(),
        lattice,
    )
    result = simulate_finite_coevolution_escape(
        landscape,
        population_size_a=10,
        selection_strength=0.0,
        mutation_events=2000,
        evolutionary_burn_in=200,
        seed=5,
    )
    assert result.accepted_a + result.accepted_b > 10
    summary = result.summary()
    assert 0.0 <= summary["high_payoff_fraction"] <= 1.0
    assert 0.0 <= summary["matched_optimum_fraction"] <= 1.0


def test_finite_coevolution_ensemble_summary_is_bounded():
    lattice = StrategyLattice(max_rate=0.8, points=5)
    landscape = build_pair_growth_landscape(
        barrier_scenario(),
        lattice,
    )
    ensemble = finite_coevolution_escape_ensemble(
        landscape,
        population_size=20,
        selection_strength=5.0,
        mutation_events=500,
        evolutionary_burn_in=100,
        replicates=4,
        seed=99,
    )
    summary = ensemble.summary()
    assert summary["replicates"] == 4
    assert 0.0 <= summary["escape_replicate_fraction"] <= 1.0
    assert 0.0 <= summary["mean_high_payoff_fraction"] <= 1.0
