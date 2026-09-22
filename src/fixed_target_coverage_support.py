"""Exact support probability under IID target-level environmental validity.

This module is outcome-blind. It starts from the frozen fixed GPS targets and
asks:

    if each selected target independently has valid environmental phase with
    probability p, what is the exact probability that the registered final
    support gate is met?

The final support gate is defined on:
- adjacent valid target pairs; and
- unique animals contributing at least one valid adjacent pair.

The calculation is exact for the declared IID target-validity model. It is not
an empirical model of MODIS missingness. Pixel-year failures can be correlated,
so this result is a synthetic robustness envelope rather than a guarantee.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable

from src.fixed_interval_gps_targets import FixedIntervalGPSTarget


@dataclass(frozen=True)
class GroupCoverageSupport:
    group: str
    target_validity_probability: float
    selected_targets: int
    animals_with_possible_pairs: int
    max_possible_adjacent_pairs: int
    expected_valid_adjacent_pairs: float
    expected_animals_with_valid_pairs: float
    probability_support_gate_passes: float
    min_animals_required: int
    min_pairs_required: int


@dataclass(frozen=True)
class FixedTargetCoverageSupport:
    target_validity_probability: float
    groups: tuple[GroupCoverageSupport, ...]
    min_animals_per_group: int
    min_pairs_per_group: int
    joint_probability_all_groups_pass: float

    @property
    def all_groups_probabilistically_supported(self) -> bool:
        return all(
            row.probability_support_gate_passes > 0.0
            for row in self.groups
        )


def _capped_convolution(
    left: list[float],
    right: list[float],
    cap: int,
) -> list[float]:
    out = [0.0] * (cap + 1)
    for i, p_i in enumerate(left):
        if p_i == 0.0:
            continue
        for j, p_j in enumerate(right):
            if p_j == 0.0:
                continue
            out[min(cap, i + j)] += p_i * p_j
    return out


def _run_pair_distribution(
    targets_in_run: int,
    p: float,
    pair_cap: int,
) -> list[float]:
    """Distribution of adjacent valid-pair count in one contiguous target run."""

    if targets_in_run <= 0:
        raise ValueError("targets_in_run must be positive")
    if pair_cap <= 0:
        raise ValueError("pair_cap must be positive")

    # DP indexed by capped pair count and validity state of the current target.
    invalid = [0.0] * (pair_cap + 1)
    valid = [0.0] * (pair_cap + 1)
    invalid[0] = 1.0 - p
    valid[0] = p

    for _ in range(1, targets_in_run):
        next_invalid = [0.0] * (pair_cap + 1)
        next_valid = [0.0] * (pair_cap + 1)

        for pairs in range(pair_cap + 1):
            mass_invalid = invalid[pairs]
            mass_valid = valid[pairs]
            total = mass_invalid + mass_valid

            # New target invalid: no new adjacent pair.
            next_invalid[pairs] += total * (1.0 - p)

            # New target valid after invalid predecessor: no new pair.
            next_valid[pairs] += mass_invalid * p

            # New target valid after valid predecessor: one adjacent pair.
            if mass_valid:
                next_valid[min(pair_cap, pairs + 1)] += (
                    mass_valid * p
                )

        invalid = next_invalid
        valid = next_valid

    return [
        invalid[index] + valid[index]
        for index in range(pair_cap + 1)
    ]


def _contiguous_run_lengths(indices: Iterable[int]) -> tuple[int, ...]:
    ordered = sorted(set(indices))
    if not ordered:
        return ()

    runs: list[int] = []
    run_length = 1
    previous = ordered[0]
    for index in ordered[1:]:
        if index == previous + 1:
            run_length += 1
        else:
            runs.append(run_length)
            run_length = 1
        previous = index
    runs.append(run_length)
    return tuple(runs)


def _animal_pair_distribution(
    rows: tuple[FixedIntervalGPSTarget, ...],
    *,
    p: float,
    pair_cap: int,
) -> list[float]:
    """Pair-count distribution for one animal across all animal-years/runs."""

    by_year: dict[str, list[int]] = {}
    for row in rows:
        by_year.setdefault(row.animal_year, []).append(
            row.target_index
        )

    distribution = [0.0] * (pair_cap + 1)
    distribution[0] = 1.0

    for indices in by_year.values():
        for run_length in _contiguous_run_lengths(indices):
            run_distribution = _run_pair_distribution(
                run_length,
                p,
                pair_cap,
            )
            distribution = _capped_convolution(
                distribution,
                run_distribution,
                pair_cap,
            )

    return distribution


def _group_support_probability(
    group: str,
    rows: tuple[FixedIntervalGPSTarget, ...],
    *,
    p: float,
    min_animals: int,
    min_pairs: int,
) -> GroupCoverageSupport:
    by_animal: dict[str, list[FixedIntervalGPSTarget]] = {}
    for row in rows:
        by_animal.setdefault(row.animal_id, []).append(row)

    animal_distributions: list[list[float]] = []
    animals_with_possible_pairs = 0
    expected_animals = 0.0

    possible_pairs = 0
    for animal_rows_list in by_animal.values():
        animal_rows = tuple(animal_rows_list)
        distribution = _animal_pair_distribution(
            animal_rows,
            p=p,
            pair_cap=min_pairs,
        )
        animal_distributions.append(distribution)

        # A positive pair count at p=1 identifies an animal that can
        # contribute to the final animal-support gate.
        possible_distribution = _animal_pair_distribution(
            animal_rows,
            p=1.0,
            pair_cap=min_pairs,
        )
        if sum(possible_distribution[1:]) > 0.0:
            animals_with_possible_pairs += 1

        expected_animals += 1.0 - distribution[0]

        # Count frozen adjacent target edges exactly.
        by_year_indices: dict[str, list[int]] = {}
        for row in animal_rows:
            by_year_indices.setdefault(
                row.animal_year, []
            ).append(row.target_index)
        for indices in by_year_indices.values():
            ordered = set(indices)
            possible_pairs += sum(
                (index + 1) in ordered
                for index in ordered
            )

    # Exact group DP: state = capped animals with >=1 pair x capped pair count.
    state = [
        [0.0] * (min_pairs + 1)
        for _ in range(min_animals + 1)
    ]
    state[0][0] = 1.0

    for distribution in animal_distributions:
        next_state = [
            [0.0] * (min_pairs + 1)
            for _ in range(min_animals + 1)
        ]
        for animal_count in range(min_animals + 1):
            for pair_count in range(min_pairs + 1):
                base = state[animal_count][pair_count]
                if base == 0.0:
                    continue
                for animal_pairs, probability in enumerate(distribution):
                    if probability == 0.0:
                        continue
                    next_animals = min(
                        min_animals,
                        animal_count + int(animal_pairs > 0),
                    )
                    next_pairs = min(
                        min_pairs,
                        pair_count + animal_pairs,
                    )
                    next_state[next_animals][next_pairs] += (
                        base * probability
                    )
        state = next_state

    support_probability = state[min_animals][min_pairs]
    expected_pairs = possible_pairs * p * p

    return GroupCoverageSupport(
        group=group,
        target_validity_probability=p,
        selected_targets=len(rows),
        animals_with_possible_pairs=animals_with_possible_pairs,
        max_possible_adjacent_pairs=possible_pairs,
        expected_valid_adjacent_pairs=expected_pairs,
        expected_animals_with_valid_pairs=expected_animals,
        probability_support_gate_passes=support_probability,
        min_animals_required=min_animals,
        min_pairs_required=min_pairs,
    )


def exact_iid_target_coverage_support(
    targets: Iterable[FixedIntervalGPSTarget],
    *,
    target_validity_probability: float,
    min_animals_per_group: int = 10,
    min_pairs_per_group: int = 100,
) -> FixedTargetCoverageSupport:
    """Compute exact support probability under IID target validity."""

    p = target_validity_probability
    if not isfinite(p) or not 0.0 <= p <= 1.0:
        raise ValueError(
            "target_validity_probability must lie in [0,1]"
        )
    if min_animals_per_group <= 0:
        raise ValueError("min_animals_per_group must be positive")
    if min_pairs_per_group <= 0:
        raise ValueError("min_pairs_per_group must be positive")

    rows = tuple(targets)
    if not rows:
        raise ValueError("at least one fixed GPS target is required")

    seen: set[tuple[str, int]] = set()
    by_group: dict[str, list[FixedIntervalGPSTarget]] = {}
    for row in rows:
        key = (row.animal_year, row.target_index)
        if key in seen:
            raise ValueError(
                "duplicate target index within animal-year: "
                f"{row.animal_year}/{row.target_index}"
            )
        seen.add(key)
        by_group.setdefault(row.group, []).append(row)

    group_results = tuple(
        _group_support_probability(
            group,
            tuple(group_rows),
            p=p,
            min_animals=min_animals_per_group,
            min_pairs=min_pairs_per_group,
        )
        for group, group_rows in sorted(by_group.items())
    )

    joint = 1.0
    for row in group_results:
        joint *= row.probability_support_gate_passes

    return FixedTargetCoverageSupport(
        target_validity_probability=p,
        groups=group_results,
        min_animals_per_group=min_animals_per_group,
        min_pairs_per_group=min_pairs_per_group,
        joint_probability_all_groups_pass=joint,
    )



@dataclass(frozen=True)
class CoverageProbabilityThreshold:
    target_joint_support_probability: float
    minimum_target_validity_probability: float | None
    achieved_joint_support_probability: float
    groups: tuple[GroupCoverageSupport, ...]
    iterations: int
    tolerance: float


def find_minimum_iid_target_validity(
    targets: Iterable[FixedIntervalGPSTarget],
    *,
    target_joint_support_probability: float = 0.95,
    min_animals_per_group: int = 10,
    min_pairs_per_group: int = 100,
    tolerance: float = 1e-4,
    max_iterations: int = 60,
) -> CoverageProbabilityThreshold:
    """Find the smallest IID target-validity probability meeting a joint gate.

    The search is exact up to the declared bisection tolerance because each
    support probability evaluation uses the exact dynamic programme above.

    If even p=1 cannot reach the requested joint support probability, the
    returned minimum_target_validity_probability is None.
    """

    if (
        not isfinite(target_joint_support_probability)
        or not 0.0 < target_joint_support_probability <= 1.0
    ):
        raise ValueError(
            "target_joint_support_probability must lie in (0,1]"
        )
    if not isfinite(tolerance) or tolerance <= 0.0:
        raise ValueError("tolerance must be positive and finite")
    if max_iterations <= 0:
        raise ValueError("max_iterations must be positive")

    rows = tuple(targets)
    if not rows:
        raise ValueError("at least one fixed GPS target is required")

    at_one = exact_iid_target_coverage_support(
        rows,
        target_validity_probability=1.0,
        min_animals_per_group=min_animals_per_group,
        min_pairs_per_group=min_pairs_per_group,
    )
    if (
        at_one.joint_probability_all_groups_pass
        < target_joint_support_probability
    ):
        return CoverageProbabilityThreshold(
            target_joint_support_probability=(
                target_joint_support_probability
            ),
            minimum_target_validity_probability=None,
            achieved_joint_support_probability=(
                at_one.joint_probability_all_groups_pass
            ),
            groups=at_one.groups,
            iterations=0,
            tolerance=tolerance,
        )

    low = 0.0
    high = 1.0
    best = at_one
    iterations = 0

    while iterations < max_iterations and high - low > tolerance:
        iterations += 1
        mid = 0.5 * (low + high)
        audit = exact_iid_target_coverage_support(
            rows,
            target_validity_probability=mid,
            min_animals_per_group=min_animals_per_group,
            min_pairs_per_group=min_pairs_per_group,
        )
        if (
            audit.joint_probability_all_groups_pass
            >= target_joint_support_probability
        ):
            high = mid
            best = audit
        else:
            low = mid

    final = exact_iid_target_coverage_support(
        rows,
        target_validity_probability=high,
        min_animals_per_group=min_animals_per_group,
        min_pairs_per_group=min_pairs_per_group,
    )
    return CoverageProbabilityThreshold(
        target_joint_support_probability=(
            target_joint_support_probability
        ),
        minimum_target_validity_probability=high,
        achieved_joint_support_probability=(
            final.joint_probability_all_groups_pass
        ),
        groups=final.groups,
        iterations=iterations,
        tolerance=tolerance,
    )
