import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data" / "payoff_b_hoge_veluwe_gate_b_result_20260928.json"


def load_result():
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_gate_b_is_frozen_negative_and_gate_c_stays_closed():
    r = load_result()
    assert r["status"] == "NO_CUE_RESOURCE_REVERSAL"
    assert r["gate_b_passed"] is False
    assert r["gate_c_licensed"] is False
    assert r["gate_c_status"] == "NOT_RUN"
    assert r["connectivity_rows"] == 24


def test_gate_b_fails_the_registered_slope_geometry_not_just_support():
    r = load_result()
    fit = r["full_fit"]
    seg = fit["segmented"]

    assert fit["estimable"] is True
    assert fit["geometry_pass"] is False
    assert seg["break_year"] == 1999
    assert seg["delta_aicc_vs_linear"] > 4
    assert seg["left_slope"] > 0
    assert seg["right_slope"] > 0
    assert seg["recovery_fraction"] is None


def test_gate_b_keeps_history_timing_firewall_closed():
    r = load_result()
    firewall = r["outcome_firewall"]
    assert firewall["cue_data_read"] is True
    assert firewall["resource_data_read"] is True
    assert firewall["resident_timing_read"] is False
    assert firewall["migrant_timing_read"] is False
    assert firewall["focal_partner_mismatch_computed"] is False
    assert firewall["history_test_opened"] is False


def test_gate_b_is_tied_to_exact_sources_outputs_and_ci_artifact():
    r = load_result()
    source = r["source_provenance"]
    assert source["cue_csv_sha256"] == (
        "14cf9d5d249e582cf07079f3724b227a835acae95c297e3e8a1bac1bede5cc31"
    )
    assert source["resource_file_sha256"] == (
        "9f113eb3f95d239ac31652c4083a159d82dacb61355b03fa2f355a2733a0b984"
    )
    assert r["output_hashes"]["connectivity_sha256"] == (
        "36cef859c759599d9a2bc6254e86e2e19b9081be18e29e125ce095cadeafae62"
    )
    wf = r["workflow_provenance"]
    assert wf["run_id"] == 36368451182
    assert wf["head_sha"] == "f8f968d627a01f8545c9a376d224be81f154db41"
    assert wf["artifact_id"] == 10947973142
    assert wf["conclusion"] == "success"
