import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "data" / "payoff_b_aikens_auth_blocker_audit_20260924.json"
DOC = ROOT / "docs" / "PAYOFF_B_AIKENS_AUTH_BLOCKER_AUDIT_20260924.md"


def load():
    return json.loads(RECEIPT.read_text(encoding="utf-8"))


def test_aikens_blocker_is_authentication_only():
    receipt = load()
    assert receipt["source_identity_gate"]["status"] == "PASS"
    assert receipt["exact_manifest"]["coverage_gate"] == "PASS"
    assert receipt["exact_manifest"]["credentials_configured"] is False
    assert receipt["live_smoke"]["status"] == "SKIPPED_NO_APPEEARS_CREDENTIALS"
    assert receipt["anonymous_s3_probe"]["status"] == "ANONYMOUS_S3_ACCESS_INCOMPLETE"
    assert receipt["blocker_classification"] == "authentication_only"


def test_aikens_lambda_outcome_remains_unopened():
    receipt = load()
    assert receipt["lambda_outcome_opened"] is False
    assert receipt["scientific_contract_changed"] is False
    assert receipt["retuning_permitted"] is False


def test_aikens_auth_routes_and_artifacts_are_frozen():
    receipt = load()
    assert receipt["accepted_authentication_routes"] == [
        "APPEEARS_TOKEN",
        "EARTHDATA_USERNAME_plus_EARTHDATA_PASSWORD",
    ]
    assert receipt["exact_manifest"]["artifact_id"] == 10813652391
    assert receipt["live_smoke"]["artifact_id"] == 10813373749
    assert receipt["anonymous_s3_probe"]["artifact_id"] == 10813433240


def test_aikens_blocker_doc_keeps_scientific_stop_rule():
    text = DOC.read_text(encoding="utf-8")
    assert "authentication only" in text
    assert "lambda outcome = UNOPENED" in text
    assert "Do not change any of the following" in text
    assert "not a negative scientific result" in text
