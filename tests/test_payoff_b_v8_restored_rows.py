"""Network-free unit tests: strictly restorative V8 audit, no new outcomes."""
import json
from pathlib import Path

import pytest

from scripts.audit_payoff_b_v8_restored_rows import (
    MANIFEST, FILES, audit, weighted_slope, q_type7, quantile_ci, fail
)


def test_original_preoutcome_manifest_source_pin_and_hypothesis_lock():
    m=json.loads(MANIFEST.read_text(encoding="utf-8"))
    assert m["status"]=="PRE_RECOVERY_MANIFEST_LOCKED_NO_NEW_OUTCOMES"
    assert m["source"]["commit"]=="62c58d77c2028bd863dfe3697b0d9cf29ceaeab0"
    assert m["source"]["blob_sha1_git"]=="f1c9e63a377bb96152c573081e7c482cfe49ebc3"
    assert len(m["historical_artifacts"])==3
    assert [x["artifact_id"] for x in m["historical_artifacts"]]==[
        11334053847,11336345852,11337415962
    ]
    assert m["registered_result_contract"]["environment"]["unique_pairs"]==166
    assert m["registered_result_contract"]["transfer"]["species_target_rows"]==150


def test_independently_weighted_frozen_formula_matches_hand_calculation():
    rows=[
        {"species":"A","z_delta_rho":"0","delta_mismatch":"0"},
        {"species":"A","z_delta_rho":"1","delta_mismatch":"2"},
        {"species":"B","z_delta_rho":"2","delta_mismatch":"4"},
    ]
    assert weighted_slope(rows,"delta_mismatch")==pytest.approx(2)
    rows[1]["delta_mismatch"]="0"
    assert weighted_slope(rows,"delta_mismatch") != pytest.approx(2)


def test_r_quantile_type7_and_duplicates_are_exact():
    assert q_type7([0,2,4],0.25)==pytest.approx(1)
    assert q_type7([0,2,4],0.5)==pytest.approx(2)
    assert q_type7([0,2,4],0.75)==pytest.approx(3)
    assert q_type7([1,1,1,1],0.975)==pytest.approx(1)
    assert quantile_ci([0]*100)==[0,0]


def test_no_arbitrary_points_succeed_when_original_rows_missing(tmp_path):
    m=json.loads(MANIFEST.read_text(encoding="utf-8"))
    with pytest.raises(ValueError,match="Original frozen artifact missing"):
        audit(tmp_path,m)


def test_postoutcome_manifest_rewrite_fails_closed(tmp_path):
    m=json.loads(MANIFEST.read_text(encoding="utf-8"))
    m["status"]="OUTCOME_OPENED_NO_FROZEN_MANIFEST"
    with pytest.raises(ValueError,match="manifest status drift"):
        audit(tmp_path,m)


def test_file_registry_contains_exact_required_output_paths():
    assert len(FILES)==11
    assert FILES["environment_pairs"] == (
        "environment","payoff_b_v8_primary_unique_pairs.csv"
    )
    assert FILES["transfer_rows"] == (
        "transfer","payoff_b_v8_transfer_primary_rows.csv"
    )
    assert FILES["structural_rows"] == (
        "structural","payoff_b_v8_transfer_structural_null_rows.csv"
    )
    assert all(t[0] in ("environment","transfer","structural") for t in FILES.values())
