"""Pre-environment support ceiling for frozen fixed GPS targets.

This audit asks whether the registered Aikens phase-retention contrast could
possibly meet its sample-support gate if every preselected 24 h GPS target had
valid environmental phase.

Environmental data can only remove targets/pairs, never add them. Therefore:

- if this ceiling fails, the registered lambda contrast is necessarily
  NOT ESTIMABLE before any environmental extraction;
- if this ceiling passes, the final support gate remains unresolved until
  environmental validity is attached.

The ceiling is computed on exactly the same support units used by the final
contrast: adjacent target pairs and unique animals contributing at least one
such pair within each group.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from src.fixed_interval_gps_targets import FixedIntervalGPSTarget


@dataclass(frozen=True)
class GroupSupportCeiling:
    group: str
    selected_targets: int
    animals_with_targets: int
    animal_years_with_targets: int
    max_possible_adjacent_pairs: int
    animals_with_possible_pairs: int
    animal_years_with_possible_pairs: int
    min_animals_required: int
    min_pairs_required: int
    animals_gate_possible: bool
    pairs_gate_possible: bool
    final_support_possible: bool


@dataclass(frozen=True)
class FixedTargetSupportCeiling:
    groups: tuple[GroupSupportCeiling, ...]
    min_animals_per_group: int
    min_pairs_per_group: int

    @property
    def all_groups_support_possible(self) -> bool:
        return bool(self.groups) and all(
            row.final_support_possible for row in self.groups
        )

    @property
    def necessarily_not_estimable(self) -> bool:
        return not self.all_groups_support_possible


def audit_fixed_target_support_ceiling(
    targets: Iterable[FixedIntervalGPSTarget],
    *,
    min_animals_per_group: int = 10,
    min_pairs_per_group: int = 100,
) -> FixedTargetSupportCeiling:
    """Compute the maximum final support attainable before environment joins."""

    if min_animals_per_group <= 0:
        raise ValueError("min_animals_per_group must be positive")
    if min_pairs_per_group <= 0:
        raise ValueError("min_pairs_per_group must be positive")

    rows = tuple(targets)
    if not rows:
        raise ValueError("at least one fixed GPS target is required")

    # One target index per animal-year should already be unique by construction.
    seen: set[tuple[str, int]] = set()
    for row in rows:
        key = (row.animal_year, row.target_index)
        if key in seen:
            raise ValueError(
                "duplicate target index within animal-year: "
                f"{row.animal_year}/{row.target_index}"
            )
        seen.add(key)

    by_group: dict[str, list[FixedIntervalGPSTarget]] = {}
    for row in rows:
        by_group.setdefault(row.group, []).append(row)

    group_results: list[GroupSupportCeiling] = []

    for group, group_rows in sorted(by_group.items()):
        animals_with_targets = {
            row.animal_id for row in group_rows
        }
        years_with_targets = {
            row.animal_year for row in group_rows
        }

        by_year: dict[str, list[FixedIntervalGPSTarget]] = {}
        for row in group_rows:
            by_year.setdefault(row.animal_year, []).append(row)

        pair_count = 0
        years_with_pairs: set[str] = set()
        animals_with_pairs: set[str] = set()

        for animal_year, year_rows in by_year.items():
            animals = {row.animal_id for row in year_rows}
            groups = {row.group for row in year_rows}
            if len(animals) != 1:
                raise ValueError(
                    f"animal_year {animal_year!r} contains multiple animal IDs"
                )
            if groups != {group}:
                raise ValueError(
                    f"animal_year {animal_year!r} contains inconsistent groups"
                )

            indices = {row.target_index for row in year_rows}
            possible_pairs = sum(
                (index + 1) in indices
                for index in indices
            )
            if possible_pairs > 0:
                pair_count += possible_pairs
                years_with_pairs.add(animal_year)
                animals_with_pairs.add(next(iter(animals)))

        animals_possible = (
            len(animals_with_pairs) >= min_animals_per_group
        )
        pairs_possible = pair_count >= min_pairs_per_group

        group_results.append(
            GroupSupportCeiling(
                group=group,
                selected_targets=len(group_rows),
                animals_with_targets=len(animals_with_targets),
                animal_years_with_targets=len(years_with_targets),
                max_possible_adjacent_pairs=pair_count,
                animals_with_possible_pairs=len(animals_with_pairs),
                animal_years_with_possible_pairs=len(years_with_pairs),
                min_animals_required=min_animals_per_group,
                min_pairs_required=min_pairs_per_group,
                animals_gate_possible=animals_possible,
                pairs_gate_possible=pairs_possible,
                final_support_possible=(
                    animals_possible and pairs_possible
                ),
            )
        )

    return FixedTargetSupportCeiling(
        groups=tuple(group_results),
        min_animals_per_group=min_animals_per_group,
        min_pairs_per_group=min_pairs_per_group,
    )
