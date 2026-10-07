"""Validation of normalized JV-Link handoff tables for PAYOFF-B racing.

The statistical layer consumes normalized CSV exports rather than parsing raw
JV-Data records.  This module validates the cross-table source contract before
any forecast calibration or market-absorption analysis is attempted.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from math import isfinite
from typing import Iterable, Mapping


@dataclass(frozen=True)
class RacingHandoffAudit:
    races: int
    result_rows: int
    tm_rows: int
    odds_rows: int
    candidate_races: int
    excluded_no_valid_starters: int
    excluded_non_single_winner: int


def _parse_bool01(value: object, *, field: str) -> int:
    try:
        out = int(str(value))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field} must be 0 or 1") from exc
    if out not in {0, 1}:
        raise ValueError(f"{field} must be 0 or 1")
    return out


def _parse_iso_datetime(value: object, *, field: str) -> datetime:
    try:
        out = datetime.fromisoformat(str(value))
    except ValueError as exc:
        raise ValueError(f"{field} must be ISO-8601 datetime") from exc
    return out


def _parse_iso_date(value: object, *, field: str) -> date:
    try:
        return date.fromisoformat(str(value))
    except ValueError as exc:
        raise ValueError(f"{field} must be ISO date YYYY-MM-DD") from exc


def validate_normalized_handoff(
    races: Iterable[Mapping[str, object]],
    results: Iterable[Mapping[str, object]],
    tm: Iterable[Mapping[str, object]],
    odds: Iterable[Mapping[str, object]],
) -> RacingHandoffAudit:
    """Validate the retrospective category-7 / time-series handoff contract."""

    race_rows = list(races)
    result_rows = list(results)
    tm_rows = list(tm)
    odds_rows = list(odds)
    if not race_rows:
        raise ValueError("races table must not be empty")
    if not result_rows:
        raise ValueError("results table must not be empty")
    if not tm_rows:
        raise ValueError("TM table must not be empty")
    if not odds_rows:
        raise ValueError("odds table must not be empty")

    race_meta: dict[str, tuple[date, datetime]] = {}
    for row in race_rows:
        race_id = str(row["race_id"])
        if race_id in race_meta:
            raise ValueError(f"duplicate race_id in races table: {race_id}")
        race_day = _parse_iso_date(row["race_date"], field="race_date")
        post = _parse_iso_datetime(row["post_time"], field="post_time")
        if post.date() != race_day:
            raise ValueError(f"post_time date does not match race_date: {race_id}")
        race_meta[race_id] = (race_day, post)

    result_keys: set[tuple[str, str]] = set()
    result_numbers: dict[tuple[str, str], str] = {}
    valid_by_race: dict[str, set[str]] = {}
    winners_by_race: dict[str, list[str]] = {}
    for row in result_rows:
        race_id = str(row["race_id"])
        horse_id = str(row["horse_id"])
        horse_number = str(row["horse_number"])
        if race_id not in race_meta:
            raise ValueError(f"result references unknown race_id: {race_id}")
        key = (race_id, horse_id)
        if key in result_keys:
            raise ValueError(f"duplicate result horse key: {race_id}/{horse_id}")
        result_keys.add(key)
        result_numbers[key] = horse_number
        valid = _parse_bool01(row["valid_starter"], field="valid_starter")
        winner = _parse_bool01(row["winner"], field="winner")
        if winner and not valid:
            raise ValueError(f"winner is not a valid starter: {race_id}/{horse_id}")
        if valid:
            valid_by_race.setdefault(race_id, set()).add(horse_id)
        if winner:
            winners_by_race.setdefault(race_id, []).append(horse_id)

    tm_keys: set[tuple[str, str]] = set()
    tm_by_race: dict[str, set[str]] = {}
    for row in tm_rows:
        race_id = str(row["race_id"])
        horse_id = str(row["horse_id"])
        horse_number = str(row["horse_number"])
        key = (race_id, horse_id)
        if key in tm_keys:
            raise ValueError(f"duplicate TM horse key: {race_id}/{horse_id}")
        tm_keys.add(key)
        if key not in result_keys:
            raise ValueError(f"TM references unknown result horse: {race_id}/{horse_id}")
        if horse_number != result_numbers[key]:
            raise ValueError(f"TM horse_number mismatch: {race_id}/{horse_id}")
        try:
            category = int(str(row["tm_data_category"]))
        except ValueError as exc:
            raise ValueError("tm_data_category must be integer 7") from exc
        if category != 7:
            raise ValueError(
                f"retrospective primary requires TM data category 7: "
                f"{race_id}/{horse_id}"
            )
        score = float(row["tm_score"])
        if not isfinite(score) or not 0.0 <= score <= 100.0:
            raise ValueError(f"tm_score outside 0--100: {race_id}/{horse_id}")
        tm_by_race.setdefault(race_id, set()).add(horse_id)

    odds_keys: set[tuple[str, str, str]] = set()
    odds_by_race: dict[str, set[str]] = {}
    snapshots_by_race: dict[str, set[str]] = {}
    for row in odds_rows:
        race_id = str(row["race_id"])
        horse_id = str(row["horse_id"])
        horse_number = str(row["horse_number"])
        if race_id not in race_meta:
            raise ValueError(f"odds reference unknown race_id: {race_id}")
        result_key = (race_id, horse_id)
        if result_key not in result_keys:
            raise ValueError(f"odds reference unknown result horse: {race_id}/{horse_id}")
        if horse_number != result_numbers[result_key]:
            raise ValueError(f"odds horse_number mismatch: {race_id}/{horse_id}")
        snap = _parse_iso_datetime(row["snapshot_time"], field="snapshot_time")
        post = race_meta[race_id][1]
        if snap.tzinfo != post.tzinfo:
            raise ValueError(
                f"snapshot/post timezone awareness mismatch: {race_id}"
            )
        if snap >= post:
            raise ValueError(f"odds snapshot is not strictly pre-post: {race_id}")
        value = float(row["decimal_odds"])
        if not isfinite(value) or value < 1.0:
            raise ValueError(
                f"decimal_odds must be finite and >= 1: {race_id}/{horse_id}"
            )
        snap_key = snap.isoformat()
        key = (race_id, snap_key, horse_id)
        if key in odds_keys:
            raise ValueError(
                f"duplicate odds key: {race_id}/{snap_key}/{horse_id}"
            )
        odds_keys.add(key)
        odds_by_race.setdefault(race_id, set()).add(horse_id)
        snapshots_by_race.setdefault(race_id, set()).add(snap_key)

    candidate = 0
    excluded_no_valid_starters = 0
    excluded_non_single_winner = 0
    for race_id in race_meta:
        valid = valid_by_race.get(race_id, set())
        if not valid:
            excluded_no_valid_starters += 1
            continue
        if len(winners_by_race.get(race_id, [])) != 1:
            excluded_non_single_winner += 1
            continue
        if tm_by_race.get(race_id, set()) != valid:
            continue
        if not valid.issubset(odds_by_race.get(race_id, set())):
            continue
        if not snapshots_by_race.get(race_id):
            continue
        candidate += 1

    return RacingHandoffAudit(
        races=len(race_rows),
        result_rows=len(result_rows),
        tm_rows=len(tm_rows),
        odds_rows=len(odds_rows),
        candidate_races=candidate,
        excluded_no_valid_starters=excluded_no_valid_starters,
        excluded_non_single_winner=excluded_non_single_winner,
    )
