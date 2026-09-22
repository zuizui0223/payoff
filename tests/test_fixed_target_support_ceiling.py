from datetime import datetime, timedelta

import pytest

from src.fixed_interval_gps_targets import FixedIntervalGPSTarget
from src.fixed_target_support_ceiling import (
    audit_fixed_target_support_ceiling,
)


def targets_for_group(
    group: str,
    *,
    animals: int,
    targets_per_animal: int,
    missing_index: int | None = None,
):
    rows = []
    start = datetime(2020, 4, 1)
    for animal in range(animals):
        animal_id = f"{group}_{animal:02d}"
        animal_year = f"{animal_id}_2020"
        for index in range(targets_per_animal):
            if missing_index is not None and index == missing_index:
                continue
            timestamp = start + timedelta(days=index)
            rows.append(
                FixedIntervalGPSTarget(
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
            )
    return rows


def test_support_ceiling_passes_exact_10_animals_100_pairs_per_group():
    rows = (
        targets_for_group(
            "small",
            animals=10,
            targets_per_animal=11,
        )
        + targets_for_group(
            "large",
            animals=10,
            targets_per_animal=11,
        )
    )
    audit = audit_fixed_target_support_ceiling(
        rows,
        min_animals_per_group=10,
        min_pairs_per_group=100,
    )

    assert audit.all_groups_support_possible
    assert not audit.necessarily_not_estimable
    for group in audit.groups:
        assert group.animals_with_possible_pairs == 10
        assert group.max_possible_adjacent_pairs == 100
        assert group.final_support_possible


def test_support_ceiling_fails_when_one_group_has_only_nine_pair_contributors():
    rows = (
        targets_for_group(
            "small",
            animals=10,
            targets_per_animal=11,
        )
        + targets_for_group(
            "large",
            animals=9,
            targets_per_animal=20,
        )
    )
    audit = audit_fixed_target_support_ceiling(
        rows,
        min_animals_per_group=10,
        min_pairs_per_group=100,
    )
    by_group = {row.group: row for row in audit.groups}

    assert by_group["large"].max_possible_adjacent_pairs > 100
    assert by_group["large"].animals_with_possible_pairs == 9
    assert not by_group["large"].animals_gate_possible
    assert audit.necessarily_not_estimable


def test_support_ceiling_fails_at_99_pairs_even_with_ten_animals():
    # Nine animals contribute 10 pairs and one contributes 9: total 99.
    rows = targets_for_group(
        "small",
        animals=9,
        targets_per_animal=11,
    )
    rows += targets_for_group(
        "small",
        animals=1,
        targets_per_animal=10,
    )
    # Give the last animal/year a unique identity after helper reuse.
    patched = []
    for index, row in enumerate(rows):
        if index >= 9 * 11:
            patched.append(
                FixedIntervalGPSTarget(
                    animal_id="small_extra",
                    animal_year="small_extra_2020",
                    group=row.group,
                    target_index=row.target_index,
                    target_timestamp=row.target_timestamp,
                    observation_id="extra_" + row.observation_id,
                    observed_timestamp=row.observed_timestamp,
                    deviation_seconds=row.deviation_seconds,
                    pixel_id=row.pixel_id,
                )
            )
        else:
            patched.append(row)

    audit = audit_fixed_target_support_ceiling(
        patched,
        min_animals_per_group=10,
        min_pairs_per_group=100,
    )
    group = audit.groups[0]
    assert group.animals_with_possible_pairs == 10
    assert group.max_possible_adjacent_pairs == 99
    assert group.animals_gate_possible
    assert not group.pairs_gate_possible
    assert audit.necessarily_not_estimable


def test_missing_target_breaks_two_adjacent_pair_opportunities():
    rows = targets_for_group(
        "small",
        animals=1,
        targets_per_animal=6,
        missing_index=3,
    )
    audit = audit_fixed_target_support_ceiling(
        rows,
        min_animals_per_group=1,
        min_pairs_per_group=1,
    )
    group = audit.groups[0]

    # Present indices: 0,1,2,4,5 -> pairs 0-1, 1-2, 4-5.
    assert group.max_possible_adjacent_pairs == 3


def test_duplicate_target_index_within_animal_year_is_rejected():
    row = targets_for_group(
        "small",
        animals=1,
        targets_per_animal=2,
    )[0]
    with pytest.raises(ValueError, match="duplicate target index"):
        audit_fixed_target_support_ceiling(
            [row, row],
            min_animals_per_group=1,
            min_pairs_per_group=1,
        )
