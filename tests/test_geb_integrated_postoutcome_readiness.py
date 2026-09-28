from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
READY = ROOT / "submission" / "GEB_INTEGRATED_POSTOUTCOME_PIPELINE_READINESS_20260925.md"
PUB = ROOT / "docs" / "PUBLICATION_STATUS.md"
WORKFLOW = ROOT / ".github" / "workflows" / "payoff-b-aikens-appeears-full-extraction.yml"


def test_geb_postoutcome_readiness_keeps_real_outcome_unopened() -> None:
    text = READY.read_text(encoding="utf-8")
    assert "run = 36110717190" in text
    assert "status = PASS" in text
    assert "REAL_AIKENS_LAMBDA_OUTCOME = UNOPENED" in text
    assert "FINAL_SCIENCE_BLOCKER = none" in text
    assert "No simulated test payload is a scientific result." in text


def test_publication_status_routes_v2_to_geb_without_inheriting_v1_pipeline_readiness() -> None:
    text = PUB.read_text(encoding="utf-8")
    assert "FIRST_SHOT = Global Ecology and Biogeography / Research Article" in text
    assert "LEGACY_V1_POSTOUTCOME_GEB_PIPELINE = READY_FOR_V1_ONLY" in text
    assert "LEGACY_V1_POSTOUTCOME_READINESS = GEB_INTEGRATED_POSTOUTCOME_PIPELINE_READINESS_20260925.md" in text
    assert (
        "CURRENT_V2_POSTOUTCOME_GEB_PIPELINE = ACCESS_BLOCKED_STATE_FROZEN" in text
    )
    assert "Aikens fixed-24 h" in text and "adjudication" in text
    assert "CURRENT_V2_POSTOUTCOME_RESULT_LOCATION = Supporting Information only" in text
    assert "LAST_VERIFIED_AIKENS_CREDENTIAL_PREFLIGHT = NOT_CONFIGURED_2026-09-28" in text
    assert "LAST_VERIFIED_AIKENS_CREDENTIAL_PREFLIGHT_RUN = 36372973062" in text
    assert "LAST_VERIFIED_AIKENS_CREDENTIAL_PREFLIGHT_ARTIFACT = 10950280495" in text
    assert "CURRENT_CREDENTIAL_STATE = NOT_CONFIGURED_CONFIRMED_2026-09-28" in text
    assert "ACCESS_BLOCKED" in text
    assert "not a scientific result" in text
    assert "ACCESS_BLOCKED_AUTHOR_DECISION = FROZEN_SUBMIT_WITH_ACCESS_BLOCKED" in text
    assert "CURRENT_V2_ACCESS_BLOCKED_PACKAGE = READY" in text
    assert "CURRENT_V2_ACCESS_BLOCKED_BUILD_RUN = 36390286108" in text
    assert "AIKENS_LAMBDA_OUTCOME_OPENED = false" in text
    assert "FUTURE_AUTHENTICATED_EXECUTION = permitted under original preregistration" in text


def test_authenticated_aikens_workflow_builds_canonical_v2_outcome_package() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "Build canonical V2 GEB outcome package" in text
    assert "scripts/build_payoff_b_v2_geb_outcome_package.py" in text
    assert "outputs/PAYOFF_B_V2_GEB_OUTCOME_PACKAGE.zip" in text
    assert "scripts/build_geb_integrated_outcome_package.py" not in text
    assert "outputs/GEB_INTEGRATED_OUTCOME_PACKAGE.zip" not in text
