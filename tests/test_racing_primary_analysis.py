from datetime import datetime, timedelta, timezone

from src.racing_primary_analysis import analyze_normalized_handoff


def _synthetic_tables():
    # Six distinct dates -> first four train, last two test at 70% floor.
    races = []
    results = []
    tm = []
    odds = []

    for idx in range(6):
        day = 1 + idx
        race_id = f"r{idx + 1}"
        post = datetime(2026, 9, day, 15, 40, tzinfo=timezone(timedelta(hours=9)))
        races.append(
            {
                "race_id": race_id,
                "race_date": post.date().isoformat(),
                "post_time": post.isoformat(),
            }
        )

        # Winner alternates.  TM is informative but not perfect: one training
        # race (idx=3) deliberately ranks the wrong horse higher.  This avoids
        # a degenerate synthetic world where the calibrated form forecast
        # dominates the market at every time slice.
        winner = "A" if idx % 2 == 0 else "B"
        tm_favored = winner
        if idx == 3:
            tm_favored = "A" if winner == "B" else "B"
        for horse, number in (("A", "01"), ("B", "02")):
            results.append(
                {
                    "race_id": race_id,
                    "horse_id": horse,
                    "horse_number": number,
                    "winner": "1" if horse == winner else "0",
                    "valid_starter": "1",
                }
            )
            tm_score = 80.0 if horse == tm_favored else 20.0
            tm.append(
                {
                    "race_id": race_id,
                    "horse_id": horse,
                    "horse_number": number,
                    "tm_score": str(tm_score),
                    "tm_data_category": "7",
                }
            )

        # Market gradually absorbs the same signal.
        for minutes, winner_odds, loser_odds in (
            (30, 1.95, 2.05),
            (15, 1.75, 2.35),
            (10, 1.60, 2.80),
            (5, 1.48, 3.20),
            (2, 1.40, 3.50),  # LAST
        ):
            when = post - timedelta(minutes=minutes)
            for horse, number in (("A", "01"), ("B", "02")):
                value = winner_odds if horse == winner else loser_odds
                odds.append(
                    {
                        "race_id": race_id,
                        "horse_id": horse,
                        "horse_number": number,
                        "snapshot_time": when.isoformat(),
                        "decimal_odds": str(value),
                    }
                )

    return races, results, tm, odds


def test_end_to_end_primary_detects_synthetic_absorption_pattern():
    out = analyze_normalized_handoff(*_synthetic_tables())
    assert out.source_audit["races"] == 6
    assert out.split["eligible_train_races"] == 4
    assert out.split["eligible_test_races"] == 2
    assert [x["time_slice"] for x in out.time_slices] == [
        "T-30",
        "T-15",
        "T-10",
        "T-5",
        "LAST",
    ]
    assert out.primary_contrasts["P1_market_improves"] is True
    assert out.primary_contrasts["P2_form_weight_declines"] is True
    assert out.primary_contrasts["P3_incremental_form_value_declines"] is True
    assert out.calibration["tm_data_category"] == 7


def test_end_to_end_excludes_selected_runner_set_change():
    races, results, tm, odds = _synthetic_tables()
    # Remove one runner only from the T-10 snapshot in the first race.
    post = datetime(2026, 9, 1, 15, 40, tzinfo=timezone(timedelta(hours=9)))
    target = (post - timedelta(minutes=10)).isoformat()
    odds = [
        row
        for row in odds
        if not (
            row["race_id"] == "r1"
            and row["horse_id"] == "B"
            and row["snapshot_time"] == target
        )
    ]
    out = analyze_normalized_handoff(races, results, tm, odds)
    assert out.exclusions["selected_snapshot_runner_set_mismatch"] == 1
    assert out.split["eligible_train_races"] == 3
