import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data" / "payoff_b_hoge_veluwe_source_gate_a_result_20260928.json"


def load_result():
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_gate_a_freezes_three_certified_coordinates_and_one_access_block():
    r = load_result()
    assert r["status"] == "MIGRANT_SOURCE_ACCESS_BLOCKED"
    assert r["gate_b_licensed"] is False
    assert r["registered_source_overlap"] == [1985, 2015]
    assert r["registered_history_span"] == [1992, 2015]
    assert r["registered_history_year_count"] == 24

    assert r["cue_extension"]["certified"] is True
    assert r["cue_extension"]["years"] == [1980, 2015]
    assert r["cue_extension"]["n_years"] == 36

    resident = r["certified_sources"]["resident_partner_timing"]
    resource = r["certified_sources"]["destination_resource_state"]
    assert resident["declared_digest_match"] is True
    assert resource["declared_digest_match"] is True
    assert resident["declared_sha256"] == resident["computed_sha256"]
    assert resource["declared_sha256"] == resource["computed_sha256"]


def test_gate_a_source_hashes_and_year_coverages_are_frozen():
    r = load_result()
    resident = r["certified_sources"]["resident_partner_timing"]
    resource = r["certified_sources"]["destination_resource_state"]

    assert resident["computed_sha256"] == (
        "a6a08800d95d5c25ffce7fcb87df5ac91fa36790a72f220e2d407c49b1dc5db2"
    )
    assert resource["computed_sha256"] == (
        "9f113eb3f95d239ac31652c4083a159d82dacb61355b03fa2f355a2733a0b984"
    )
    assert resident["schema"]["min_year"] == 1973
    assert resident["schema"]["max_year"] == 2020
    assert resource["schema"]["min_year"] == 1985
    assert resource["schema"]["max_year"] == 2020


def test_gate_a_keeps_all_outcome_firewalls_closed():
    r = load_result()
    assert all(value is False for value in r["outcome_firewall"].values())
    assert r["blocked_source"]["coordinate"] == "migrant_timing"
    assert r["blocked_source"]["landing_filename"] == "Tomotani et al.zip"
    assert r["blocked_source"]["state"] == "ANONYMOUS_DOWNLOAD_UNAVAILABLE"


def test_gate_a_receipt_is_tied_to_successful_ci_artifact():
    r = load_result()
    wf = r["workflow_provenance"]
    assert wf["run_id"] == 36367383611
    assert wf["head_sha"] == "41a87938c339f2deb62598d4c0f4e5bfb6163cb6"
    assert wf["conclusion"] == "success"
    assert wf["artifact_id"] == 10948380232
