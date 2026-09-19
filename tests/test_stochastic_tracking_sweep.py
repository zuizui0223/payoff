from math import isclose

from src.spatiotemporal_tracking import TrackingScenario
from src.stochastic_tracking_sweep import (
    StochasticSweepRanges,
    draw_stochastic_sweep_point,
    optimize_stochastic_strategy,
    planned_tracking_steps,
    shard_sample_indices,
)


def test_sweep_point_is_reproducible_by_index_and_seed():
    base = TrackingScenario(steps=60, burn_in=10)
    first = draw_stochastic_sweep_point(
        17,
        seed=1234,
        base_scenario=base,
    )
    second = draw_stochastic_sweep_point(
        17,
        seed=1234,
        base_scenario=base,
    )
    other = draw_stochastic_sweep_point(
        18,
        seed=1234,
        base_scenario=base,
    )

    assert first == second
    assert first != other


def test_shards_partition_global_sample_indices_exactly():
    samples = 23
    shards = [
        set(shard_sample_indices(samples, index, 4))
        for index in range(4)
    ]
    union = set().union(*shards)

    assert union == set(range(samples))
    for i in range(4):
        for j in range(i + 1, 4):
            assert shards[i].isdisjoint(shards[j])


def test_workload_formula_counts_strategy_replicate_step_updates():
    assert planned_tracking_steps(
        samples=10,
        strategy_points=7,
        replicates=8,
        ecological_steps=120,
    ) == 10 * 49 * 8 * 120


def test_zero_noise_stochastic_optimizer_recovers_partner_axis_direction():
    base = TrackingScenario(
        climate_velocity=0.04,
        partner_spatial_share=1.0,
        interaction_strength=0.35,
        migration_cost=0.03,
        phenology_cost=0.03,
        baseline_growth=0.3,
        steps=80,
        burn_in=20,
    )
    point = draw_stochastic_sweep_point(
        0,
        seed=1,
        base_scenario=base,
        ranges=StochasticSweepRanges(
            climate_velocity=StochasticSweepRanges().climate_velocity,
        ),
    )
    # Override the sampled point with the declared deterministic scenario
    # while retaining a valid zero-noise forcing object.
    optimum = optimize_stochastic_strategy(
        base,
        type(point.forcing)(),
        replicates=2,
        seed=42,
        max_rate=0.8,
        points=5,
    )
    assert optimum.strategy.migration_rate > optimum.strategy.phenology_rate


def test_sampled_ranges_respect_declared_bounds():
    base = TrackingScenario(steps=60, burn_in=10)
    ranges = StochasticSweepRanges()
    for index in range(20):
        point = draw_stochastic_sweep_point(
            index,
            seed=777,
            base_scenario=base,
            ranges=ranges,
        )
        assert (
            ranges.climate_velocity.low
            <= point.scenario.climate_velocity
            <= ranges.climate_velocity.high
        )
        assert 0.0 <= point.scenario.partner_spatial_share <= 1.0
        assert point.forcing.climate_increment_sd >= 0.0
