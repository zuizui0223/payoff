from datetime import datetime, timedelta

import pytest

from src.fixed_interval_gps_targets import FixedIntervalGPSTarget
from src.fixed_target_clustered_coverage import (
    simulate_pixel_year_clustered_support,
)


def target(
    *,
    animal_id="A",
    animal_year="A_2020",
    group="small",
    index,
    pixel_id,
):
    timestamp = datetime(2020, 4, 1) + timedelta(days=index)
    return FixedIntervalGPSTarget(
        animal_id=animal_id,
        animal_year=animal_year,
        group=group,
        target_index=index,
        target_timestamp=timestamp,
        observation_id=f"{animal_year}_{index}",
        observed_timestamp=timestamp,
        deviation_seconds=0.0,
        pixel_id=pixel_id,
    )


def test_same_pixel_year_edge_has_expected_valid_pair_probability_p():
    p = 0.3
    result = simulate_pixel_year_clustered_support(
        [
            target(index=0, pixel_id="P"),
            target(index=1, pixel_id="P"),
        ],
        target_validity_probability=p,
        replicates=2000,
        seed=1,
        min_animals_per_group=1,
        min_pairs_per_group=1,
    )
    row = result.groups[0]

    assert row.same_pixel_year_edges == 1
    assert row.distinct_pixel_year_edges == 0
    assert row.analytic_expected_valid_adjacent_pairs == pytest.approx(p)


def test_distinct_pixel_year_edge_has_expected_probability_p_squared():
    p = 0.3
    result = simulate_pixel_year_clustered_support(
        [
            target(index=0, pixel_id="P0"),
            target(index=1, pixel_id="P1"),
        ],
        target_validity_probability=p,
        replicates=2000,
        seed=2,
        min_animals_per_group=1,
        min_pairs_per_group=1,
    )
    row = result.groups[0]

    assert row.same_pixel_year_edges == 0
    assert row.distinct_pixel_year_edges == 1
    assert row.analytic_expected_valid_adjacent_pairs == pytest.approx(
        p * p
    )


def test_p_zero_always_fails_support():
    result = simulate_pixel_year_clustered_support(
        [
            target(index=0, pixel_id="P"),
            target(index=1, pixel_id="P"),
        ],
        target_validity_probability=0.0,
        replicates=20,
        seed=3,
        min_animals_per_group=1,
        min_pairs_per_group=1,
    )

    assert result.joint_probability_all_groups_pass == 0.0
    assert result.groups[0].probability_support_gate_passes == 0.0


def test_p_one_recovers_full_support():
    rows = []
    for animal in ("A", "B"):
        for index in range(3):
            rows.append(
                target(
                    animal_id=animal,
                    animal_year=f"{animal}_2020",
                    index=index,
                    pixel_id=f"{animal}_{index}",
                )
            )

    result = simulate_pixel_year_clustered_support(
        rows,
        target_validity_probability=1.0,
        replicates=20,
        seed=4,
        min_animals_per_group=2,
        min_pairs_per_group=4,
    )

    assert result.joint_probability_all_groups_pass == 1.0
    assert result.groups[0].probability_support_gate_passes == 1.0
    assert result.groups[0].mean_valid_adjacent_pairs == pytest.approx(4.0)
    assert result.groups[0].mean_animals_with_valid_pairs == pytest.approx(2.0)


def test_seed_reproducibility():
    rows = [
        target(index=0, pixel_id="P0"),
        target(index=1, pixel_id="P1"),
        target(index=2, pixel_id="P2"),
    ]
    first = simulate_pixel_year_clustered_support(
        rows,
        target_validity_probability=0.5,
        replicates=100,
        seed=99,
        min_animals_per_group=1,
        min_pairs_per_group=1,
    )
    second = simulate_pixel_year_clustered_support(
        rows,
        target_validity_probability=0.5,
        replicates=100,
        seed=99,
        min_animals_per_group=1,
        min_pairs_per_group=1,
    )

    assert first == second


def test_invalid_probability_rejected():
    with pytest.raises(ValueError):
        simulate_pixel_year_clustered_support(
            [
                target(index=0, pixel_id="P"),
                target(index=1, pixel_id="P"),
            ],
            target_validity_probability=-0.1,
            replicates=10,
            min_animals_per_group=1,
            min_pairs_per_group=1,
        )
