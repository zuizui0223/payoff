from math import exp, isclose

from src.spatiotemporal_tracking import TrackingScenario
from src.tracking_finite_evolution import (
    finite_stationary_tracking_summary,
    moran_fixation_probability_from_growth_difference,
    simulate_finite_tracking_evolution,
    weak_mutation_stationary_distribution,
)
from src.tracking_mutation_selection import StrategyLattice


def test_neutral_fixation_is_one_over_n():
    for n in (2, 10, 100):
        observed = moran_fixation_probability_from_growth_difference(
            0.0,
            n,
            5.0,
        )
        assert isclose(observed, 1.0 / n, abs_tol=1e-12)


def test_beneficial_and_deleterious_fixation_straddle_neutrality():
    n = 50
    neutral = 1.0 / n
    beneficial = moran_fixation_probability_from_growth_difference(
        0.02,
        n,
        10.0,
    )
    deleterious = moran_fixation_probability_from_growth_difference(
        -0.02,
        n,
        10.0,
    )
    assert beneficial > neutral
    assert deleterious < neutral


def test_reciprocal_fixation_ratio_matches_exact_constant_fitness_identity():
    delta = 0.03
    n = 20
    beta = 4.0
    forward = moran_fixation_probability_from_growth_difference(
        delta,
        n,
        beta,
    )
    reverse = moran_fixation_probability_from_growth_difference(
        -delta,
        n,
        beta,
    )
    expected = exp(beta * (n - 1) * delta)
    assert isclose(
        forward / reverse,
        expected,
        rel_tol=1e-11,
        abs_tol=1e-11,
    )


def test_weak_mutation_stationary_is_uniform_under_neutral_selection():
    growth = (-1.0, 0.0, 2.0, 5.0)
    probs = weak_mutation_stationary_distribution(
        growth,
        population_size=30,
        selection_strength=0.0,
    )
    assert all(
        isclose(value, 0.25, abs_tol=1e-12)
        for value in probs
    )


def test_stationary_distribution_favors_higher_growth_under_selection():
    growth = (0.0, 0.1, 0.2)
    probs = weak_mutation_stationary_distribution(
        growth,
        population_size=20,
        selection_strength=2.0,
    )
    assert probs[2] > probs[1] > probs[0]
    assert isclose(sum(probs), 1.0, abs_tol=1e-12)


def test_finite_evolution_is_seed_reproducible():
    scenario = TrackingScenario(
        climate_velocity=0.04,
        partner_spatial_share=1.0,
        interaction_strength=0.3,
        migration_cost=0.03,
        phenology_cost=0.03,
        baseline_growth=0.3,
        steps=80,
        burn_in=20,
    )
    lattice = StrategyLattice(max_rate=0.8, points=5)
    first = simulate_finite_tracking_evolution(
        scenario,
        lattice,
        population_size=40,
        selection_strength=8.0,
        mutation_events=400,
        seed=123,
    )
    second = simulate_finite_tracking_evolution(
        scenario,
        lattice,
        population_size=40,
        selection_strength=8.0,
        mutation_events=400,
        seed=123,
    )
    assert first == second


def test_selected_finite_chain_moves_away_from_stasis():
    scenario = TrackingScenario(
        climate_velocity=0.05,
        partner_spatial_share=1.0,
        interaction_strength=0.4,
        migration_cost=0.02,
        phenology_cost=0.05,
        baseline_growth=0.3,
        steps=80,
        burn_in=20,
    )
    lattice = StrategyLattice(max_rate=0.8, points=5)
    result = simulate_finite_tracking_evolution(
        scenario,
        lattice,
        population_size=80,
        selection_strength=15.0,
        mutation_events=1000,
        seed=77,
    )
    occupancy = result.empirical_occupancy()
    stasis = lattice.index(0, 0)
    assert occupancy[stasis] < 0.5
    assert result.accepted_substitutions > 0


def test_finite_stationary_summary_concentrates_more_at_larger_population_size():
    scenario = TrackingScenario(
        climate_velocity=0.04,
        partner_spatial_share=1.0,
        interaction_strength=0.3,
        migration_cost=0.03,
        phenology_cost=0.03,
        baseline_growth=0.3,
        steps=80,
        burn_in=20,
    )
    lattice = StrategyLattice(max_rate=0.8, points=5)
    small = finite_stationary_tracking_summary(
        scenario,
        lattice,
        population_size=10,
        selection_strength=5.0,
    )
    large = finite_stationary_tracking_summary(
        scenario,
        lattice,
        population_size=100,
        selection_strength=5.0,
    )
    assert large["top_probability"] > small["top_probability"]
    assert (
        large["effective_strategy_count"]
        < small["effective_strategy_count"]
    )
