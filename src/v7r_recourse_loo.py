"""Post-outcome source-only stability audit for PAYOFF-B V7R recourse proxy.

Recalculate a flyway's empirical remaining-route window after removing every
observation from one focal individual. No phase errors, environmental
predictability values or lambda outcomes are consumed.

The diagnostic asks whether a recourse proxy built from the same tracked
population can be estimated without the focal individual's own behavior.
It is NOT a new test of the already non-supported V7R Q x R interaction.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from math import isfinite
from typing import Iterable, Mapping

from src.route_recourse_capacity import (
    TransitionDuration,
    build_edge_envelopes,
    remaining_recourse,
)


@dataclass(frozen=True)
class EdgeLeaveAnimalOut:
    flyway: str
    origin_region: str
    destination_region: str
    full_recourse: float
    n_individuals: int
    n_estimable: int
    n_not_estimable: int
    mean_absolute_difference: float | None
    max_absolute_difference: float | None
    minimum_estimable_recourse: float | None
    maximum_estimable_recourse: float | None
    failed_individual_ids: tuple[str, ...]


def recourse_map(
    transitions: Iterable[TransitionDuration],
    *,
    terminal_by_flyway: Mapping[str, str],
    minimum_edge_rows: int = 3,
) -> dict[tuple[str, str], float]:
    """Compute node recourse using the frozen 10–90% route envelope definition."""

    env = build_edge_envelopes(
        transitions, min_edge_rows=minimum_edge_rows,
        lower_quantile=0.1, upper_quantile=0.9
    )
    vals = remaining_recourse(env, terminal_by_flyway=terminal_by_flyway)
    return {(row.flyway, row.region): row.retained_recourse for row in vals}


def audit_individual_exclusion(
    transitions: Iterable[TransitionDuration],
    *,
    focal_edges: Iterable[tuple[str, str, str]],
    terminal_by_flyway: Mapping[str, str],
    minimum_edge_rows: int = 3,
) -> tuple[EdgeLeaveAnimalOut, ...]:
    """Refit R for each focal individual without using that animal's rows.

    Failures are retained as explicit non-estimability; graph admission rules
    are never relaxed. All original rows can be used in the full-source
    reference; individual exclusion removes all the individual's edges from
    the relevant flyway, not only the current focal edge.
    """

    rows = list(transitions)
    original = recourse_map(
        rows, terminal_by_flyway=terminal_by_flyway,
        minimum_edge_rows=minimum_edge_rows
    )
    result: list[EdgeLeaveAnimalOut] = []

    for flyway, origin, destination in sorted(set(focal_edges)):
        if flyway not in terminal_by_flyway:
            raise ValueError("focal flyway lacks a declared terminal")
        key = (flyway, origin)
        if key not in original:
            raise ValueError("focal origin has no full-sample recourse")
        full = original[key]
        ids = sorted({
            str(row.individual_id) for row in rows
            if row.flyway == flyway
            and row.origin_region == origin
            and row.destination_region == destination
        })
        if not ids:
            raise ValueError("focal transition has no individuals")

        estimates: list[float] = []
        failures: list[str] = []
        for identifier in ids:
            others = [
                row for row in rows
                if not (row.flyway == flyway
                        and str(row.individual_id) == identifier)
            ]
            try:
                submap = recourse_map(
                    others, terminal_by_flyway=terminal_by_flyway,
                    minimum_edge_rows=minimum_edge_rows
                )
                estimate = submap.get(key)
                if estimate is None or not isfinite(estimate):
                    failures.append(identifier)
                else:
                    estimates.append(estimate)
            except ValueError:
                failures.append(identifier)

        diffs = [abs(value - full) for value in estimates]
        result.append(EdgeLeaveAnimalOut(
            flyway=flyway,
            origin_region=origin,
            destination_region=destination,
            full_recourse=full,
            n_individuals=len(ids),
            n_estimable=len(estimates),
            n_not_estimable=len(failures),
            mean_absolute_difference=(
                sum(diffs) / len(diffs) if diffs else None
            ),
            max_absolute_difference=max(diffs) if diffs else None,
            minimum_estimable_recourse=min(estimates) if estimates else None,
            maximum_estimable_recourse=max(estimates) if estimates else None,
            failed_individual_ids=tuple(failures),
        ))
    return tuple(result)
