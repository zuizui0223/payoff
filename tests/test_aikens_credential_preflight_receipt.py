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
    assert "opened no environmental" in pub
