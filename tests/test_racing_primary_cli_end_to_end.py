import csv
import json
import subprocess
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path


JST = timezone(timedelta(hours=9))


def _write_csv(path, fieldnames, rows):
    with Path(path).open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _build_tables(tmp_path):
    races = []
    results = []
    tm = []
    odds = []

    # Six dates: 4 train + 2 untouched test under the 70% date split.
    for idx in range(6):
        race_id = f"r{idx + 1}"
        post = datetime(2026, 9, idx + 1, 15, 40, tzinfo=JST)
        races.append(
            {
                "race_id": race_id,
                "race_date": post.date().isoformat(),
                "post_time": post.isoformat(),
            }
        )

        winner = "A" if idx % 2 == 0 else "B"
        tm_favored = winner
        # Keep the frozen TM forecast informative but imperfect in training.
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
            tm.append(
                {
                    "race_id": race_id,
                    "horse_id": horse,
                    "horse_number": number,
                    "tm_score": "80" if horse == tm_favored else "20",
                    "tm_data_category": "7",
                }
            )

        for minutes, winner_odds, loser_odds in (
            (30, 1.95, 2.05),
            (15, 1.75, 2.35),
            (10, 1.60, 2.80),
            (5, 1.48, 3.20),
            (2, 1.40, 3.50),
        ):
            when = post - timedelta(minutes=minutes)
            for horse, number in (("A", "01"), ("B", "02")):
                odds.append(
                    {
                        "race_id": race_id,
                        "horse_id": horse,
                        "horse_number": number,
                        "snapshot_time": when.isoformat(),
                        "decimal_odds": (
                            str(winner_odds) if horse == winner else str(loser_odds)
                        ),
                    }
                )

    paths = {
        "races": tmp_path / "races.csv",
        "results": tmp_path / "results.csv",
        "tm": tmp_path / "tm.csv",
        "odds": tmp_path / "odds.csv",
    }
    _write_csv(paths["races"], ["race_id", "race_date", "post_time"], races)
    _write_csv(
        paths["results"],
        ["race_id", "horse_id", "horse_number", "winner", "valid_starter"],
        results,
    )
    _write_csv(
        paths["tm"],
        ["race_id", "horse_id", "horse_number", "tm_score", "tm_data_category"],
        tm,
    )
    _write_csv(
        paths["odds"],
        ["race_id", "horse_id", "horse_number", "snapshot_time", "decimal_odds"],
        odds,
    )
    return paths


def test_handoff_validator_and_primary_cli_complete_end_to_end(tmp_path):
    paths = _build_tables(tmp_path)
    audit_path = tmp_path / "audit.json"
    output_path = tmp_path / "primary.json"

    subprocess.run(
        [
            sys.executable,
            "scripts/validate_racing_jvlink_handoff.py",
            "--races",
            str(paths["races"]),
            "--results",
            str(paths["results"]),
            "--tm",
            str(paths["tm"]),
            "--odds",
            str(paths["odds"]),
            "--output",
            str(audit_path),
        ],
        check=True,
    )

    audit = json.loads(audit_path.read_text())
    assert audit["status"] == "PASS"
    assert audit["candidate_races"] == 6
    assert audit["primary_tm_category"] == 7

    subprocess.run(
        [
            sys.executable,
            "scripts/run_racing_primary_analysis.py",
            "--races",
            str(paths["races"]),
            "--results",
            str(paths["results"]),
            "--tm",
            str(paths["tm"]),
            "--odds",
            str(paths["odds"]),
            "--output",
            str(output_path),
            "--bootstrap-replicates",
            "200",
            "--bootstrap-seed",
            "7",
        ],
        check=True,
    )

    payload = json.loads(output_path.read_text())
    assert payload["schema"] == "payoff_b_racing_retrospective_primary_v1"
    assert payload["source_audit"]["candidate_races"] == 6
    assert payload["split"]["eligible_train_races"] == 4
    assert payload["split"]["eligible_test_races"] == 2
    assert [row["time_slice"] for row in payload["time_slices"]] == [
        "T-30",
        "T-15",
        "T-10",
        "T-5",
        "LAST",
    ]
    assert payload["primary_contrasts"]["P1_market_improves"] is True
    assert payload["primary_contrasts"]["P2_form_weight_declines"] is True
    assert payload["primary_contrasts"]["P3_incremental_form_value_declines"] is True
    assert payload["paired_test_bootstrap"]["replicates"] == 200
