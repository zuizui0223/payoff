import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "data" / "payoff_b_two_clock_classification_20261003.json"


def load():
    return json.loads(PATH.read_text(encoding="utf-8"))


def test_two_clock_classification_is_postfreeze_and_noncanonical():
    payload = load()
    assert payload["status"] == "POSTFREEZE_TWO_CLOCK_CLASSIFICATION_FROZEN_FROM_EXISTING_EVIDENCE"
    assert payload["frozen_submission_affected"] is False


def test_mule_deer_is_not_relabelled_as_timer_or_full_hybrid():
    rows = {row["system"]: row for row in load()["systems"]}
    deer = rows["Ortega mule deer"]
    assert deer["timer"] == "T0"
    assert deer["decision"] == "D2"
    assert deer["hybrid"] == "H0"


def test_osmia_event_timing_is_not_called_a_molecular_clock():
    rows = {row["system"]: row for row in load()["systems"]}
    osm = rows["Osmia lignaria greenhouse"]
    assert osm["timer"] == "T1"
    assert osm["decision"] == "D0"
    assert "molecular" in osm["boundary"]


def test_no_current_system_is_claimed_as_h2():
    payload = load()
    assert all(row["hybrid"] != "H2" for row in payload["systems"])
    assert "No current PAYOFF-B natural system" in payload["global_boundary"]


def test_wigeon_registered_null_is_preserved():
    rows = {row["system"]: row for row in load()["systems"]}
    wig = rows["Eurasian wigeon"]
    assert "not supported" in wig["boundary"]
