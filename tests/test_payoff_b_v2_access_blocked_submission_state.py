import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS = ROOT / "docs" / "PUBLICATION_STATUS.md"
READINESS = ROOT / "submission" / "PAYOFF_B_V2_SUBMISSION_READINESS_20260927.md"
STATE = ROOT / "data" / "payoff_b_v2_submission_readiness_20260927.json"
RECEIPT = ROOT / "data" / "payoff_b_v2_access_blocked_submission_receipt_20260928.json"
ACCESS = ROOT / "data" / "aikens2022_access_blocked_submission_state_20260928.json"


def test_access_blocked_submission_state_is_explicitly_frozen():
    status = STATUS.read_text(encoding="utf-8")
    readiness = READINESS.read_text(encoding="utf-8")
    state = json.loads(STATE.read_text(encoding="utf-8"))
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))
    access = json.loads(ACCESS.read_text(encoding="utf-8"))

    assert "SCIENTIFIC_STATE = ACCESS_BLOCKED_SUBMISSION_STATE_FROZEN" in status
    assert "AIKENS_EXECUTION_STATE = ACCESS_BLOCKED_FROZEN_NONSCIENTIFIC" in status
    assert "AIKENS_SCIENTIFIC_RESULT = unavailable" in status
    assert "AIKENS_LAMBDA_OUTCOME_OPENED = false" in status
    assert "ACCESS_BLOCKED_AUTHOR_DECISION = FROZEN_SUBMIT_WITH_ACCESS_BLOCKED" in status
    assert "CURRENT_V2_FINAL_SUBMISSION_PACKAGE = ACCESS_BLOCKED_SCIENCE_CLOSED_PORTAL_BLOCKED" in status

    assert "ACCESS_BLOCKED submission state frozen" in readiness
    assert "author decision = SUBMIT_WITH_ACCESS_BLOCKED" in readiness
    assert "future authenticated execution = permitted" in readiness

    assert state["postoutcome_pipeline"]["status"] == "ACCESS_BLOCKED_STATE_FROZEN"
    assert state["postoutcome_pipeline"]["access_blocked_activation"] == (
        "ACTIVATED_AUTHOR_DECISION_FROZEN_2026-09-28"
    )
    assert state["real_aikens_execution"]["access_blocked_activated"] is True
    assert state["real_aikens_execution"]["future_authenticated_execution_permitted"] is True
    assert state["portal_readiness"]["science_state"] == "CLOSED_ACCESS_BLOCKED"

    assert receipt["status"] == "PASS_ACCESS_BLOCKED_SUBMISSION_STATE_READY"
    assert receipt["access_state"]["scientific_result_available"] is False
    assert receipt["access_state"]["lambda_outcome_opened"] is False
    assert receipt["access_state"]["future_authenticated_execution_permitted"] is True
    assert access["author_decision"]["decision"] == "SUBMIT_WITH_ACCESS_BLOCKED"


def test_access_blocked_package_is_deterministic_and_lambda_remains_unopened():
    state = json.loads(STATE.read_text(encoding="utf-8"))
    receipt = json.loads(RECEIPT.read_text(encoding="utf-8"))

    package = state["access_blocked_submission"]
    assert package["workflow_run"] == 36390286108
    assert package["primary"]["artifact_id"] == 10956335888
    assert package["reproduction"]["artifact_id"] == 10955883655

    geb_sha = "3aefc6d7ef59996f8b4edc16ac52c4be10a3761282b1c7850fa4c4f1998198cd"
    review_sha = "6bed01785d921a42f2e1659efd4da757bb86292b31fa779f5879db92c5911e75"

    assert package["primary"]["geb_inner_zip_sha256"] == geb_sha
    assert package["reproduction"]["geb_inner_zip_sha256"] == geb_sha
    assert package["primary"]["reviewer_inner_zip_sha256"] == review_sha
    assert package["reproduction"]["reviewer_inner_zip_sha256"] == review_sha
    assert package["reproduction"]["deterministic_inner_archives"] is True

    assert receipt["primary_build"]["geb_inner_zip_sha256"] == geb_sha
    assert receipt["reproduction"]["geb_inner_zip_sha256"] == geb_sha
    assert receipt["access_state"]["lambda_outcome_opened"] is False
    assert receipt["invariants"]["registered_scientific_result_frozen"] is False


def test_aikens_is_no_longer_a_current_submission_blocker():
    state = json.loads(STATE.read_text(encoding="utf-8"))
    blockers = " ".join(state["portal_readiness"]["blockers"]).lower()

    assert "aikens" not in blockers
    assert "credential" not in blockers
    assert "reviewer archive" in blockers
    assert "title-page" in blockers
    assert "human review" in blockers
