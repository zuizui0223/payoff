import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BLOCKER = ROOT / "data" / "payoff_b_snow_goose_j_row_access_blocker_20260930.json"
AUDIT = ROOT / "data" / "payoff_b_snow_goose_published_j_mechanism_audit_20260930.json"
DOC = ROOT / "docs" / "PAYOFF_B_SNOW_GOOSE_J_MECHANISM_AUDIT_20260930.md"


def test_row_access_blocker_is_not_misclassified_as_ecological_null():
    receipt = json.loads(BLOCKER.read_text(encoding="utf-8"))

    assert receipt["status"] == "SOURCE_BYTES_BLOCKED_ROW_VALUES_UNOPENED"
    assert receipt["outcome_open_status"]["table_rows_opened"] is False
    assert receipt["outcome_open_status"]["registered_model_fitted"] is False
    assert receipt["outcome_open_status"]["coefficient_seen"] is False
    assert (
        receipt["outcome_open_status"]["result_classification"]
        == "NOT_RUN_SOURCE_ACCESS_BLOCKED"
    )
    assert "not evidence" in receipt["scientific_rule"]


def test_published_mechanism_audit_keeps_J_multicomponent_and_nonidentified():
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))

    assert audit["payoff_b_interpretation"]["natural_D_eff"] == "NOT_IDENTIFIED"
    assert (
        audit["payoff_b_interpretation"]["endocrine_duration_signal"]
        == "NOT_SUPPORTED_IN_PUBLISHED_RELEASE_CORT_MODEL"
    )
    assert (
        audit["payoff_b_interpretation"]["breeding_suppression_duration_signal"]
        == "SUPPORTED_IN_PUBLISHED_2023_ANALYSIS"
    )
    assert audit["energetic_pathway"]["fed_daily_corrected_mass_change_g_per_day"] == -9.56


def test_document_preserves_frozen_future_model_and_claim_ceiling():
    text = DOC.read_text(encoding="utf-8")

    assert "cond2 \\sim cond1 + DaysInCap" in text
    assert "capture-group clustered uncertainty" in text
    assert "not an ecological null result" in text
    assert "not as a test of natural" in text
