"""Direct remaining-recourse coordinate for PAYOFF-B V7R.

The coordinate is deliberately constructed without environmental phase,
spring-onset values, or phase-retention outcomes.

For edge j->k:
    D_jk = origin stopover duration + transit duration.

Empirical Q10/Q90 edge-duration envelopes define earliest and latest remaining
arrival times on a directed route graph.  Route branching contributes to the
remaining feasible temporal window.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable, Mapping, Sequence


@dataclass(frozen=True)
class TransitionDuration:
    flyway: str
    origin_region: str
    destination_region: str
    duration_days: float
    individual_id: str


@dataclass(frozen=True)
class EdgeEnvelope:
    flyway: str
    origin_region: str
    destination_region: str
    n: int
    n_individuals: int
    lower_days: float
    median_days: float
    upper_days: float


@dataclass(frozen=True)
class RegionRecourse:
    flyway: str
    region: str
    earliest_remaining_days: float
    latest_remaining_days: float
    window_days: float
    retained_recourse: float


def _rank(region: str) -> int:
    text = str(region)
    if not text.startswith("R"):
        raise ValueError("region ids must have form R<number>")
    try:
        return int(text[1:])
    except ValueError as exc:
        raise ValueError("region ids must have form R<number>") from exc


def _quantile(values: Sequence[float], p: float) -> float:
    xs = sorted(float(v) for v in values)
    if not xs:
        raise ValueError("quantile requires values")
    if len(xs) == 1:
        return xs[0]
    pos = p * (len(xs) - 1)
    lo = int(pos)
    hi = min(lo + 1, len(xs) - 1)
    frac = pos - lo
    return xs[lo] * (1.0 - frac) + xs[hi] * frac


def build_edge_envelopes(
    transitions: Iterable[TransitionDuration],
    *,
    min_edge_rows: int = 3,
    lower_quantile: float = 0.10,
    upper_quantile: float = 0.90,
) -> tuple[EdgeEnvelope, ...]:
    if min_edge_rows < 1:
        raise ValueError("min_edge_rows must be positive")
    if not 0.0 <= lower_quantile < upper_quantile <= 1.0:
        raise ValueError("quantiles must satisfy 0 <= lower < upper <= 1")

    grouped: dict[tuple[str, str, str], list[TransitionDuration]] = {}
    for row in transitions:
        duration = float(row.duration_days)
        if not isfinite(duration) or duration < 0.0:
            raise ValueError("duration_days must be finite and non-negative")
        if _rank(row.destination_region) <= _rank(row.origin_region):
            continue
        key = (str(row.flyway), str(row.origin_region), str(row.destination_region))
        grouped.setdefault(key, []).append(row)

    out: list[EdgeEnvelope] = []
    for (flyway, origin, destination), rows in sorted(grouped.items()):
        if len(rows) < min_edge_rows:
            continue
        values = [float(row.duration_days) for row in rows]
        out.append(
            EdgeEnvelope(
                flyway=flyway,
                origin_region=origin,
                destination_region=destination,
                n=len(rows),
                n_individuals=len({str(row.individual_id) for row in rows}),
                lower_days=_quantile(values, lower_quantile),
                median_days=_quantile(values, 0.50),
                upper_days=_quantile(values, upper_quantile),
            )
        )
    return tuple(out)


def remaining_recourse(
    envelopes: Iterable[EdgeEnvelope],
    *,
    terminal_by_flyway: Mapping[str, str],
) -> tuple[RegionRecourse, ...]:
    by_flyway: dict[str, list[EdgeEnvelope]] = {}
    for edge in envelopes:
        by_flyway.setdefault(edge.flyway, []).append(edge)

    output: list[RegionRecourse] = []
    for flyway, terminal in terminal_by_flyway.items():
        edges = by_flyway.get(flyway, [])
        if not edges:
            raise ValueError(f"no admitted edges for flyway {flyway}")

        terminal_rank = _rank(terminal)
        nodes = {terminal}
        for edge in edges:
            if _rank(edge.destination_region) <= terminal_rank:
                nodes.add(edge.origin_region)
                nodes.add(edge.destination_region)

        earliest: dict[str, float] = {terminal: 0.0}
        latest: dict[str, float] = {terminal: 0.0}

        for node in sorted(nodes, key=_rank, reverse=True):
            if node == terminal:
                continue
            candidates_early = []
            candidates_late = []
            for edge in edges:
                if edge.origin_region != node:
                    continue
                destination = edge.destination_region
                if destination not in earliest:
                    continue
                candidates_early.append(
                    edge.lower_days + earliest[destination]
                )
                candidates_late.append(
                    edge.upper_days + latest[destination]
                )
            if candidates_early:
                earliest[node] = min(candidates_early)
                latest[node] = max(candidates_late)

        upstream = [node for node in earliest if node != terminal]
        if not upstream:
            raise ValueError(f"no upstream path reaches terminal for {flyway}")
        start = min(upstream, key=_rank)
        start_window = latest[start] - earliest[start]
        if start_window <= 0.0:
            raise ValueError(f"initial recourse window is non-positive for {flyway}")

        for node in sorted(earliest, key=_rank):
            window = latest[node] - earliest[node]
            retained = 0.0 if node == terminal else window / start_window
            output.append(
                RegionRecourse(
                    flyway=flyway,
                    region=node,
                    earliest_remaining_days=earliest[node],
                    latest_remaining_days=latest[node],
                    window_days=window,
                    retained_recourse=retained,
                )
            )

    return tuple(output)
