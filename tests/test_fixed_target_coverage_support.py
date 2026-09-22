from datetime import datetime, timedelta

import pytest

from src.fixed_interval_gps_targets import FixedIntervalGPSTarget
from src.fixed_target_coverage_support import (
    exact_iid_target_coverage_support,
)


def target(
    *,
    animal_id="A",
    animal_year="A_2020",
    group="small",
    index,
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
        pixel_id=f"p{index}",
    )


def test_two_targets_one_pair_has_probability_p_squared():
    p = 0.6
    audit = exact_iid_target_coverage_support(
        [
            target(index=0),
            target(index=1),
        ],
        target_validity_probability=p,
        min_animals_per_group=1,
        min_pairs_per_group=1,
    )
    row = audit.groups[0]

    assert row.max_possible_adjacent_pairs == 1
    assert row.expected_valid_adjacent_pairs == pytest.approx(p * p)
    assert row.expected_animals_with_valid_pairs == pytest.approx(p * p)
    assert row.probability_support_gate_passes == pytest.approx(p * p)
    assert audit.joint_probability_all_groups_pass == pytest.approx(p * p)


def test_three_targets_at_least_one_pair_matches_union_formula():
    p = 0.4
    audit = exact_iid_target_coverage_support(
        [
            target(index=0),
            target(index=1),
            target(index=2),
        ],
        target_validity_probability=p,
        min_animals_per_group=1,
        min_pairs_per_group=1,
    )
    expected = 2.0 * p * p - p * p * p

    assert audit.groups[0].probability_support_gate_passes == pytest.approx(
        expected
    )


def test_three_targets_two_pairs_requires_all_three_targets_valid():
    p = 0.7
    audit = exact_iid_target_coverage_support(
        [
            target(index=0),
            target(index=1),
            target(index=2),
        ],
        target_validity_probability=p,
        min_animals_per_group=1,
        min_pairs_per_group=2,
    )

    assert audit.groups[0].probability_support_gate_passes == pytest.approx(
        p ** 3
    )


def test_two_animals_each_must_contribute_one_pair():
    p = 0.5
    rows = [
        target(animal_id="A", animal_year="A_2020", index=0),
        target(animal_id="A", animal_year="A_2020", index=1),
        target(animal_id="B", animal_year="B_2020", index=0),
        target(animal_id="B", animal_year="B_2020", index=1),
    ]
    audit = exact_iid_target_coverage_support(
        rows,
        target_validity_probability=p,
        min_animals_per_group=2,
        min_pairs_per_group=2,
    )

    assert audit.groups[0].probability_support_gate_passes == pytest.approx(
        p ** 4
    )


def test_nonadjacent_target_indices_do_not_form_pair():
    audit = exact_iid_target_coverage_support(
        [
            target(index=0),
            target(index=2),
        ],
        target_validity_probability=1.0,
        min_animals_per_group=1,
        min_pairs_per_group=1,
    )
    row = audit.groups[0]

    assert row.max_possible_adjacent_pairs == 0
    assert row.expected_valid_adjacent_pairs == 0.0
    assert row.probability_support_gate_passes == 0.0


def test_p_one_recovers_frozen_support_ceiling():
    rows = []
    for animal_index in range(3):
        animal_id = f"A{animal_index}"
        animal_year = f"{animal_id}_2020"
        for index in range(5):
            rows.append(
                target(
                    animal_id=animal_id,
                    animal_year=animal_year,
                    index=index,
                )
            )

    audit = exact_iid_target_coverage_support(
        rows,
        target_validity_probability=1.0,
        min_animals_per_group=3,
        min_pairs_per_group=12,
    )
    row = audit.groups[0]

    assert row.max_possible_adjacent_pairs == 12
    assert row.animals_with_possible_pairs == 3
    assert row.probability_support_gate_passes == pytest.approx(1.0)


def test_invalid_probability_rejected():
    with pytest.raises(ValueError):
        exact_iid_target_coverage_support(
            [target(index=0), target(index=1)],
            target_validity_probability=1.1,
            min_animals_per_group=1,
            min_pairs_per_group=1,
        )
