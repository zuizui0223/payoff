from copy import deepcopy

import pytest

from src.racing_jvlink_contract import validate_normalized_handoff


def _tables():
    races = [
        {
            "race_id": "r1",
            "race_date": "2026-10-04",
            "post_time": "2026-10-04T15:40:00+09:00",
        }
    ]
    results = [
        {
            "race_id": "r1",
            "horse_id": "h1",
            "horse_number": "01",
            "winner": "1",
            "valid_starter": "1",
        },
        {
            "race_id": "r1",
            "horse_id": "h2",
            "horse_number": "02",
            "winner": "0",
            "valid_starter": "1",
        },
    ]
    tm = [
        {
            "race_id": "r1",
            "horse_id": "h1",
            "horse_number": "01",
            "tm_score": "80.0",
            "tm_data_category": "7",
        },
        {
            "race_id": "r1",
            "horse_id": "h2",
            "horse_number": "02",
            "tm_score": "40.0",
            "tm_data_category": "7",
        },
    ]
    odds = [
        {
            "race_id": "r1",
            "horse_id": "h1",
            "horse_number": "01",
            "snapshot_time": "2026-10-04T15:10:00+09:00",
            "decimal_odds": "2.0",
        },
        {
            "race_id": "r1",
            "horse_id": "h2",
            "horse_number": "02",
            "snapshot_time": "2026-10-04T15:10:00+09:00",
            "decimal_odds": "3.0",
        },
    ]
    return races, results, tm, odds


def test_clean_handoff_passes_and_counts_candidate_race():
    out = validate_normalized_handoff(*_tables())
    assert out.races == 1
    assert out.candidate_races == 1


def test_non_category7_tm_fails_retrospective_primary():
    races, results, tm, odds = _tables()
    tm = deepcopy(tm)
    tm[0]["tm_data_category"] = "3"
    with pytest.raises(ValueError, match="requires TM data category 7"):
        validate_normalized_handoff(races, results, tm, odds)


def test_post_race_odds_snapshot_fails_closed():
    races, results, tm, odds = _tables()
    odds = deepcopy(odds)
    odds[0]["snapshot_time"] = "2026-10-04T15:41:00+09:00"
    with pytest.raises(ValueError, match="strictly pre-post"):
        validate_normalized_handoff(races, results, tm, odds)


def test_horse_number_mismatch_fails_closed():
    races, results, tm, odds = _tables()
    tm = deepcopy(tm)
    tm[0]["horse_number"] = "99"
    with pytest.raises(ValueError, match="horse_number mismatch"):
        validate_normalized_handoff(races, results, tm, odds)


def test_missing_tm_runner_removes_race_from_candidate_set_without_fabrication():
    races, results, tm, odds = _tables()
    out = validate_normalized_handoff(races, results, tm[:1], odds)
    assert out.candidate_races == 0


def test_dead_heat_is_explicit_exclusion_not_whole_file_failure():
    races, results, tm, odds = _tables()
    results = deepcopy(results)
    results[1]["winner"] = "1"
    out = validate_normalized_handoff(races, results, tm, odds)
    assert out.candidate_races == 0
    assert out.excluded_non_single_winner == 1


def test_no_valid_starter_is_explicit_exclusion():
    races, results, tm, odds = _tables()
    results = deepcopy(results)
    for row in results:
        row["winner"] = "0"
        row["valid_starter"] = "0"
    out = validate_normalized_handoff(races, results, tm, odds)
    assert out.candidate_races == 0
    assert out.excluded_no_valid_starters == 1


def test_one_point_zero_odds_are_valid_in_handoff():
    races, results, tm, odds = _tables()
    odds = deepcopy(odds)
    odds[0]["decimal_odds"] = "1.0"
    out = validate_normalized_handoff(races, results, tm, odds)
    assert out.candidate_races == 1
