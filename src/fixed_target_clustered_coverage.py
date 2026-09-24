"""Pixel-year clustered environmental-validity sensitivity for frozen targets.

Each unique (pixel_id, target_year) cluster is valid with common probability p.
All frozen targets in the same pixel-year share that validity state.

This is a stochastic sensitivity model, not an empirical missingness model.
It is more correlated than the IID target-level envelope but still assumes
independence between pixel-years.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite, sqrt
from random import Random
from typing import Iterable

from src.fixed_interval_gps_targets import FixedIntervalGPSTarget


_Z_975 = 1.959963984540054


@dataclass(frozen=True)
class ClusteredGroupSupport:
    group: str
    replicates: int
    target_validity_probability: float
    probability_support_gate_passes: float
    wilson_low_95: float
    wilson_high_95: float
    mean_valid_adjacent_pairs: float
    analytic_expected_valid_adjacent_pairs: float
    mean_animals_with_valid_pairs: float
    max_possible_adjacent_pairs: int
    animals_with_possible_pairs: int
    same_pixel_year_edges: int
    distinct_pixel_year_edges: int


@dataclass(frozen=True)
class ClusteredCoverageSupport:
    replicates: int
    seed: int
    target_validity_probability: float
    groups: tuple[ClusteredGroupSupport, ...]
    joint_probability_all_groups_pass: float
    joint_wilson_low_95: float
    joint_wilson_high_95: float
    unique_pixel_years: int


@dataclass(frozen=True)
class _PreparedClusteredGroup:
    group: str
    edges: tuple[tuple[int, int, int], ...]
    animals: tuple[str, ...]
    same_cluster_edges: int
    distinct_cluster_edges: int


@dataclass(frozen=True)
class _PreparedClusteredCoverage:
    unique_clusters: int
    groups: tuple[_PreparedClusteredGroup, ...]


def _wilson_interval(
    successes: int,
    trials: int,
) -> tuple[float, float]:
    if trials <= 0:
        raise ValueError("trials must be positive")
    p = successes / trials
    z2 = _Z_975 * _Z_975
    denominator = 1.0 + z2 / trials
    center = (
        p + z2 / (2.0 * trials)
    ) / denominator
    half = (
        _Z_975
        * sqrt(
            p * (1.0 - p) / trials
            + z2 / (4.0 * trials * trials)
        )
        / denominator
    )
    return max(0.0, center - half), min(1.0, center + half)


def _prepare(
    targets: Iterable[FixedIntervalGPSTarget],
) -> _PreparedClusteredCoverage:
    rows = tuple(targets)
    if not rows:
        raise ValueError("at least one fixed GPS target is required")

    cluster_ids: dict[tuple[str, int], int] = {}

    def cluster_id(row: FixedIntervalGPSTarget) -> int:
        key = (row.pixel_id, row.target_timestamp.year)
        if key not in cluster_ids:
            cluster_ids[key] = len(cluster_ids)
        return cluster_ids[key]

    by_group_year: dict[
        str,
        dict[str, list[FixedIntervalGPSTarget]],
    ] = {}
    seen: set[tuple[str, int]] = set()

    for row in rows:
        key = (row.animal_year, row.target_index)
        if key in seen:
            raise ValueError(
                "duplicate target index within animal-year: "
                f"{row.animal_year}/{row.target_index}"
            )
        seen.add(key)
        by_group_year.setdefault(
            row.group, {}
        ).setdefault(
            row.animal_year, []
        ).append(row)
        cluster_id(row)

    prepared_groups: list[_PreparedClusteredGroup] = []

    for group, years in sorted(by_group_year.items()):
        animal_names: list[str] = []
        animal_index: dict[str, int] = {}
        edges: list[tuple[int, int, int]] = []
        same = 0
        distinct = 0

        for animal_year, year_rows in years.items():
            animals = {row.animal_id for row in year_rows}
            if len(animals) != 1:
                raise ValueError(
                    f"animal_year {animal_year!r} contains multiple animals"
                )
            animal = next(iter(animals))
            if animal not in animal_index:
                animal_index[animal] = len(animal_names)
                animal_names.append(animal)
            aidx = animal_index[animal]

            ordered = sorted(
                year_rows,
                key=lambda row: row.target_index,
            )
            for first, second in zip(
                ordered,
                ordered[1:],
            ):
                if second.target_index != first.target_index + 1:
                    continue
                c1 = cluster_id(first)
                c2 = cluster_id(second)
                edges.append((c1, c2, aidx))
                if c1 == c2:
                    same += 1
                else:
                    distinct += 1

        prepared_groups.append(
            _PreparedClusteredGroup(
                group=group,
                edges=tuple(edges),
                animals=tuple(animal_names),
                same_cluster_edges=same,
                distinct_cluster_edges=distinct,
            )
        )

    return _PreparedClusteredCoverage(
        unique_clusters=len(cluster_ids),
        groups=tuple(prepared_groups),
    )


def simulate_pixel_year_clustered_support(
    targets: Iterable[FixedIntervalGPSTarget],
    *,
    target_validity_probability: float,
    replicates: int = 10000,
    seed: int = 20260922,
    min_animals_per_group: int = 10,
    min_pairs_per_group: int = 100,
) -> ClusteredCoverageSupport:
    """Monte Carlo support probability under pixel-year clustered validity."""

    p = target_validity_probability
    if not isfinite(p) or not 0.0 <= p <= 1.0:
        raise ValueError(
            "target_validity_probability must lie in [0,1]"
        )
    if replicates <= 0:
        raise ValueError("replicates must be positive")
    if min_animals_per_group <= 0:
        raise ValueError("min_animals_per_group must be positive")
    if min_pairs_per_group <= 0:
        raise ValueError("min_pairs_per_group must be positive")

    prepared = _prepare(targets)
    rng = Random(seed)

    group_success = {
        group.group: 0
        for group in prepared.groups
    }
    group_pair_sum = {
        group.group: 0
        for group in prepared.groups
    }
    group_animal_sum = {
        group.group: 0
        for group in prepared.groups
    }
    joint_success = 0

    for _ in range(replicates):
        valid = [
            rng.random() < p
            for _ in range(prepared.unique_clusters)
        ]

        all_groups_pass = True

        for group in prepared.groups:
            pair_count = 0
            animal_has_pair = [
                False
                for _ in group.animals
            ]
            animal_count = 0

            for c1, c2, aidx in group.edges:
                if valid[c1] and valid[c2]:
                    pair_count += 1
                    if not animal_has_pair[aidx]:
                        animal_has_pair[aidx] = True
                        animal_count += 1

            passed = (
                pair_count >= min_pairs_per_group
                and animal_count >= min_animals_per_group
            )
            if passed:
                group_success[group.group] += 1
            else:
                all_groups_pass = False

            group_pair_sum[group.group] += pair_count
            group_animal_sum[group.group] += animal_count

        if all_groups_pass:
            joint_success += 1

    group_results: list[ClusteredGroupSupport] = []
    for group in prepared.groups:
        successes = group_success[group.group]
        low, high = _wilson_interval(
            successes,
            replicates,
        )
        analytic_expected = (
            group.same_cluster_edges * p
            + group.distinct_cluster_edges * p * p
        )
        group_results.append(
            ClusteredGroupSupport(
                group=group.group,
                replicates=replicates,
                target_validity_probability=p,
                probability_support_gate_passes=(
                    successes / replicates
                ),
                wilson_low_95=low,
                wilson_high_95=high,
                mean_valid_adjacent_pairs=(
                    group_pair_sum[group.group]
                    / replicates
                ),
                analytic_expected_valid_adjacent_pairs=(
                    analytic_expected
                ),
                mean_animals_with_valid_pairs=(
                    group_animal_sum[group.group]
                    / replicates
                ),
                max_possible_adjacent_pairs=len(group.edges),
                animals_with_possible_pairs=len(group.animals),
                same_pixel_year_edges=(
                    group.same_cluster_edges
                ),
                distinct_pixel_year_edges=(
                    group.distinct_cluster_edges
                ),
            )
        )

    joint_low, joint_high = _wilson_interval(
        joint_success,
        replicates,
    )

    return ClusteredCoverageSupport(
        replicates=replicates,
        seed=seed,
        target_validity_probability=p,
        groups=tuple(group_results),
        joint_probability_all_groups_pass=(
            joint_success / replicates
        ),
        joint_wilson_low_95=joint_low,
        joint_wilson_high_95=joint_high,
        unique_pixel_years=prepared.unique_clusters,
    )
