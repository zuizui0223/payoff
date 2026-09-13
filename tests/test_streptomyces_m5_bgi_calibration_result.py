import csv
import hashlib
import json
from pathlib import Path


def test_response_blind_calibration_result_recomputes_from_frozen_evidence():
    evidence_path = Path("data/STREPTOMYCES_M5_BGI_CALIBRATION_CONTROL_EVIDENCE_V1.tsv")
    receipt = json.loads(Path("validation/streptomyces_m5_bgi_response_blind_calibration_result_v1.json").read_text())
    raw = evidence_path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == receipt["frozen_control_evidence_sha256"]

    with evidence_path.open(newline="") as h:
        rows = list(csv.DictReader(h, delimiter="\t"))
    assert len(rows) == 24
    assert {r["candidate_id"] for r in rows} == {
        "WT_ancestor", "M1_T0", "M2_T0", "M3_T0", "M4_T0", "M6_T0"
    }
    assert all(r["candidate_id"] != "M5_T0" for r in rows)

    absent = []
    present = []
    for r in rows:
        core = float(r["pacbio_core_coverage_pct"])
        marker = float(r["pacbio_marker_coverage_pct"])
        ratio = float(r["bgi_normalized_ratio"])
        assert core == 100.0
        if marker == 0.0:
            absent.append((r["candidate_id"], ratio))
        elif marker == 100.0:
            present.append((r["candidate_id"], ratio))
        else:
            raise AssertionError("unexpected unresolved PacBio control state")

    result = receipt["result"]
    assert max(x[1] for x in absent) == result["absence_max_ratio"]
    assert min(x[1] for x in present) == result["presence_min_ratio"]
    assert len(absent) == result["absent_pair_count"] == 10
    assert len(present) == result["present_pair_count"] == 14
    assert len({x[0] for x in absent}) == result["absent_candidate_count"] == 5
    assert len({x[0] for x in present}) == result["present_candidate_count"] == 6
    assert result["unresolved_pair_count"] == 0
    assert result["absence_max_ratio"] < result["presence_min_ratio"]
    assert result["blockers"] == []
    assert result["calibration_qualified"] is True


def test_calibration_pass_does_not_promote_m5_or_architecture_inference():
    receipt = json.loads(Path("validation/streptomyces_m5_bgi_response_blind_calibration_result_v1.json").read_text())
    assert receipt["target_used_in_calibration"] is False
    assert receipt["target_bgi_run_opened"] is False
    ceiling = receipt["claim_boundary"]
    assert ceiling["m5_primary_bgi_class_known"] is False
    assert ceiling["m5_target_bgi_run_may_now_be_opened_only_through_registered_target_gate"] is True
    assert ceiling["r2_gross_structure_resolved"] is False
    assert ceiling["physical_stock_access_confirmed"] is False
    assert ceiling["realization_d_band_available"] is False
    assert ceiling["qualified_d_reference"] is False
    assert ceiling["qualified_d_reference_count_increment"] == 0
    assert ceiling["architecture_specific_inference_open"] is False
