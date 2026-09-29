import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs" / "PUBLICATION_STATUS.md"
READINESS = ROOT / "submission" / "PAYOFF_B_V2_SUBMISSION_READINESS_20260927.md"
STATE = ROOT / "data" / "payoff_b_v2_submission_readiness_20260927.json"
RECEIPT = ROOT / "data" / "payoff_b_v2_anonymous_review_archive_receipt_20260927.json"


def test_reviewer_archive_is_ready_but_delivery_remains_external():
    status = STATUS.read_text(encoding="utf-8")
    readiness = READINESS.read_text(encoding="utf-8")
    state = json.loads(STATE.read_text(encoding="utf-8"))
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))

    assert "CURRENT_V2_REVIEWER_ARCHIVE = READY_PREOUTCOME" in status
    assert "CURRENT_V2_REVIEWER_ARCHIVE_ARTIFACT = 11012081041" in status
    assert "CURRENT_V2_REVIEWER_ARCHIVE_IDENTITY_SCAN = PASS" in status
    assert "remaining reviewer-archive task is therefore **delivery**, not construction" in readiness

    archive = state["reviewer_archive"]
    assert archive["status"] == "READY_PREOUTCOME"
    assert archive["identity_scan_passed"] is True
    assert archive["raw_empirical_data_redistributed"] is False
    assert archive["delivery_state"] == "PENDING_ANONYMOUS_CHANNEL"
    assert archive["inner_zip_sha256"] == receipt["inner_archive"]["sha256"]
    assert receipt["aikens_outcome_state"] == "UNOPENED"
