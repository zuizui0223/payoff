"""Route timing helpers for the barnacle-goose PAYOFF-B reanalysis.

The breeding endpoint follows Kölzsch et al. (2015): the last stopover before
the end of June at which the bird stayed within a 30-km radius for 7--26 days.

Stopovers themselves are supplied by the separately frozen detector.  This
module only chooses the source-defined endpoint and derives elapsed downstream
schedule durations.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Sequence

from src.goose_stopover_detection import Stopover


@dataclass(frozen=True)
class BreedingEndpoint:
    """Source-defined breeding/moulting endpoint for one spring track."""

    stopover_index: int
    arrival: datetime
    departure: datetime
    residence_days: float
    latitude: float
    longitude: float


@dataclass(frozen=True)
class RemainingSchedule:
    """Elapsed downstream timing from one stopover departure to breeding arrival."""

    stage_stopover_index: int
    stage_departure: datetime
    breeding_arrival: datetime
    remaining_hours: float
    remaining_days: float


def select_breeding_endpoint(
    stopovers: Sequence[Stopover],
    *,
    year: int,
    minimum_residence_days: float = 7.0,
    maximum_residence_days: float = 26.0,
) -> BreedingEndpoint | None:
    """Select the last qualifying stopover that begins by the end of June.

    Source rule
    -----------
    Kölzsch et al. define breeding (and moulting) sites as the last stopover
    sites before the end of June where birds stayed within a 30-km radius for
    between 7 and 26 days.

    Operationalization
    ------------------
    A stopover qualifies when:

    - its arrival/start occurs no later than 30 June 23:59:59 of the declared
      deployment year; and
    - its detected residence duration lies in [7, 26] days.

    We use the *start* cutoff rather than requiring the entire residence to end
    in June. This preserves the literal interpretation that the last stopover
    site is reached before the end of June while allowing a 7--26 day stay to
    continue into July.

    The last pre-cutoff stopover is examined. If that final stopover does not
    satisfy the 7--26 day residence range, the function returns None rather
    than falling back to an earlier site. This fail-closed behavior prevents a
    long Arctic breeding/moulting complex from causing an earlier Icelandic or
    Norwegian staging site to be mislabeled as the breeding endpoint.

    This function does not use breeding status, spring anomaly, or final timing
    mismatch to choose the endpoint.
    """

    if int(year) < 1:
        raise ValueError("year must be positive")
    lower = float(minimum_residence_days)
    upper = float(maximum_residence_days)
    if lower < 0.0 or upper < lower:
        raise ValueError("invalid residence-duration bounds")

    cutoff = datetime(
        int(year),
        6,
        30,
        23,
        59,
        59,
        tzinfo=(
            stopovers[0].start.tzinfo
            if stopovers
            else None
        ),
    )

    before_cutoff = [
        (index, stop, stop.duration_hours / 24.0)
        for index, stop in enumerate(stopovers)
        if stop.start <= cutoff
    ]
    if not before_cutoff:
        return None

    # Fail closed: the source wording describes the breeding endpoint as the
    # *last* stopover before end-June and additionally gives a 7--26 d
    # residence range. We must not skip a later non-qualifying Arctic stay and
    # silently select an earlier staging site.
    index, stop, days = max(before_cutoff, key=lambda row: row[1].start)
    if not (lower <= days <= upper):
        return None
    return BreedingEndpoint(
        stopover_index=index,
        arrival=stop.start,
        departure=stop.end,
        residence_days=days,
        latitude=stop.center_latitude,
        longitude=stop.center_longitude,
    )


def remaining_schedule_from_stopovers(
    stopovers: Sequence[Stopover],
    breeding: BreedingEndpoint,
) -> tuple[RemainingSchedule, ...]:
    """Return elapsed time from each earlier stopover departure to breeding arrival.

    Only stopovers strictly before the selected breeding stopover are returned.

    The quantity is a downstream schedule duration, not an absolute calendar
    arrival date.  It therefore avoids deriving recourse from final-arrival
    phase retention.
    """

    if breeding.stopover_index < 0 or breeding.stopover_index >= len(stopovers):
        raise ValueError("breeding stopover index is outside stopovers")

    rows = []
    for index, stop in enumerate(stopovers[: breeding.stopover_index]):
        hours = (breeding.arrival - stop.end).total_seconds() / 3600.0
        if hours < 0.0:
            raise ValueError(
                "stopover departure occurs after selected breeding arrival"
            )
        rows.append(
            RemainingSchedule(
                stage_stopover_index=index,
                stage_departure=stop.end,
                breeding_arrival=breeding.arrival,
                remaining_hours=hours,
                remaining_days=hours / 24.0,
            )
        )
    return tuple(rows)



def remaining_schedule_to_curated_arrival(
    stopovers: Sequence[Stopover],
    *,
    breeding_arrival: datetime,
) -> tuple[RemainingSchedule, ...]:
    """Return remaining elapsed time to an externally curated breeding arrival.

    This is the preferred primary route when a source publication provides an
    individual breeding-arrival date independently of our stopover detector.

    Every detected stopover whose departure is strictly before breeding_arrival
    contributes one stage.  Later detected clusters are ignored rather than
    being used to redefine the published endpoint.

    This separation is useful for identification:

    - stopover departure comes from reconstructed movement behavior;
    - destination arrival comes from an independent curated source table.
    """

    rows = []
    for index, stop in enumerate(stopovers):
        if stop.end >= breeding_arrival:
            continue
        hours = (breeding_arrival - stop.end).total_seconds() / 3600.0
        if hours < 0.0:
            continue
        rows.append(
            RemainingSchedule(
                stage_stopover_index=index,
                stage_departure=stop.end,
                breeding_arrival=breeding_arrival,
                remaining_hours=hours,
                remaining_days=hours / 24.0,
            )
        )
    return tuple(rows)
