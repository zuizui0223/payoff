from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
RECEIPT = ROOT / "data" / "payoff_b_aikens_credential_preflight_20260925.json"
AUTH = ROOT / "docs" / "PAYOFF_B_AIKENS_AUTH_BLOCKER_AUDIT_20260924.md"
PUB = ROOT / "docs" / "PUBLICATION_STATUS.md"


def test_credential_preflight_confirms_authentication_only_blocker() -> None:
    payload = json.loads(RECEIPT.read_text(encoding="utf-8"))
    assert payload["status"] == "NOT_CONFIGURED"
    assert payload["configured"] is False
    assert payload["credential_route"] == "none"
    assert payload["credential_values_recorded"] is False
    assert payload["network_submission_performed"] is False
    assert payload["environmental_values_opened"] is False
    assert payload["lambda_outcome_opened"] is False
    assert payload["scientific_changes_permitted"] is False


def test_docs_reference_latest_safe_preflight() -> None:
    auth = AUTH.read_text(encoding="utf-8")
    pub = PUB.read_text(encoding="utf-8")
    for text in (auth, pub):
        assert "36113621057" in text
        assert "10853764396" in text
    assert "status = NOT_CONFIGURED" in auth
    assert "LEGACY_V1_CREDENTIAL_PREFLIGHT_RUN = 36113621057" in pub
    assert "LEGACY_V1_CREDENTIAL_PREFLIGHT_ARTIFACT = 10853764396" in pub
    assert "opened no environmental" in pub
    assert "CURRENT_V2_PREOUTCOME_PACKAGE = READY" in pub
    assert "CURRENT_V2_FINAL_SUBMISSION_PACKAGE = ACCESS_BLOCKED_SCIENCE_CLOSED_PORTAL_READY_FOR_AUTHOR_METADATA" in pub
    assert "AIKENS_LAMBDA_OUTCOME_OPENED = false" in pub
    assert "FUTURE_AUTHENTICATED_EXECUTION = permitted under original preregistration" in pub
