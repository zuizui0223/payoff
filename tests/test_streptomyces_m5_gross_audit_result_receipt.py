import json
from pathlib import Path


def test_gross_audit_v1_receipt_is_fail_closed():
    p = Path("validation/streptomyces_m5_gross_rearrangement_audit_result_v1.json")
    data = json.loads(p.read_text())
    assert data["candidate_id"] == "M5_T0"
    assert data["v1_adjudication"]["audit_completed"] is False
    assert data["v1_adjudication"]["gross_secondary_rearrangement_unresolved"] is True
    assert data["v1_adjudication"]["blockers"] == [
        "LEFT_TERMINAL_BOUNDARY_UNRESOLVED",
        "RIGHT_TERMINAL_BOUNDARY_UNRESOLVED",
    ]
    assert data["claim_boundary"]["qualified_d_reference"] is False
    assert data["claim_boundary"]["qualified_d_reference_count_increment"] == 0
    assert data["claim_boundary"]["architecture_specific_inference_open"] is False


def test_gross_audit_v1_does_not_silently_promote_raw_bnds():
    data = json.loads(Path("validation/streptomyces_m5_gross_rearrangement_audit_result_v1.json").read_text())
    raw = data["raw_sniffles_calls"]
    assert raw["m5_total_calls_written_at_min_svlen_50000"] == 3
    assert data["v1_adjudication"]["m5_size_qualified_gross_sv_count"] == 1
    assert sum(1 for x in raw["m5_calls"] if x["type"] == "BND" and not x["size_qualified_by_v1_parser"]) == 2
