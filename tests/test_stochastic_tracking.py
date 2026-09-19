from math import isclose

from src.spatiotemporal_tracking import (
    TrackingScenario,
    TrackingStrategy,
    simulate_tracking,
)
from src.stochastic_tracking import (
    StochasticForcing,
    simulate_stochastic_tracking,
    stochastic_tracking_ensemble,
)


def test_zero_noise_matches_deterministic_tracking():
    scenario = TrackingScenario(
        climate_velocity=0.04,
        partner_spatial_share=0.7,
        interaction_strength=0.4,
        migration_cost=0.03,
        phenology_cost=0.05,
        baseline_growth=0.3,
        steps=100,
        burn_in=20,
    )
    strategy = TrackingStrategy(0.4, 0.2)

    deterministic = simulate_tracking(strategy, scenario)
    stochastic = simulate_stochastic_tracking(
        strategy,
        scenario,
        StochasticForcing(),
        seed=123,
    )

    assert isclose(
        stochastic.mean_log_growth,
        deterministic.mean_log_growth,
        rel_tol=1e-12,
        abs_tol=1e-12,
    )
    assert isclose(
        stochastic.abiotic_only_mean_log_growth,
        deterministic.abiotic_only_mean_log_growth,
        rel_tol=1e-12,
        abs_tol=1e-12,
    )
    assert isclose(
        stochastic.rms_abiotic_mismatch,
        deterministic.rms_abiotic_mismatch,
        rel_tol=1e-12,
        abs_tol=1e-12,
    )
    assert isclose(
        stochastic.rms_interaction_mismatch,
        deterministic.rms_interaction_mismatch,
        rel_tol=1e-12,
        abs_tol=1e-12,
    )


def test_stochastic_tracking_is_seed_reproducible():
    scenario = TrackingScenario(steps=80, burn_in=20)
    strategy = TrackingStrategy(0.3, 0.2)
    forcing = StochasticForcing(
        climate_increment_sd=0.02,
        partner_spatial_share_sd=0.1,
        partner_demand_noise_sd=0.05,
    )

    first = simulate_stochastic_tracking(
        strategy, scenario, forcing, seed=999
    )
    second = simulate_stochastic_tracking(
        strategy, scenario, forcing, seed=999
    )

    assert first == second


def test_different_seeds_change_noisy_realization():
    scenario = TrackingScenario(steps=80, burn_in=20)
    strategy = TrackingStrategy(0.3, 0.2)
    forcing = StochasticForcing(
        climate_increment_sd=0.03,
        partner_spatial_share_sd=0.1,
    )

    first = simulate_stochastic_tracking(
        strategy, scenario, forcing, seed=1
    )
    second = simulate_stochastic_tracking(
        strategy, scenario, forcing, seed=2
    )

    assert (
        first.final_environmental_demand
        != second.final_environmental_demand
    )


def test_ensemble_summary_is_bounded_and_complete():
    scenario = TrackingScenario(
        climate_velocity=0.05,
        steps=80,
        burn_in=20,
    )
    strategy = TrackingStrategy(0.4, 0.2)
    forcing = StochasticForcing(
        climate_increment_sd=0.02,
        partner_spatial_share_sd=0.05,
    )
    ensemble = stochastic_tracking_ensemble(
        strategy,
        scenario,
        forcing,
        replicates=8,
        seed=100,
    )
    summary = ensemble.summary()

    assert summary["replicates"] == 8
    assert 0.0 <= summary["viability_fraction"] <= 1.0
    assert (
        0.0
        <= summary["interaction_failure_fraction"]
        <= 1.0
    )
    assert summary["sd_log_growth"] >= 0.0
