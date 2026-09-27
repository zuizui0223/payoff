from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEGACY_READY = ROOT / "submission" / "GEB_INTEGRATED_POSTOUTCOME_PIPELINE_READINESS_20260925.md"
V2_READY = ROOT / "submission" / "PAYOFF_B_V2_POSTOUTCOME_PIPELINE_READINESS_20260927.md"
PUB = ROOT / "docs" / "PUBLICATION_STATUS.md"
WORKFLOW = ROOT / ".github" / "workflows" / "payoff-b-aikens-appeears-full-extraction.yml"


def test_legacy_v1_postoutcome_readiness_remains_provenance() -> None:
    text = LEGACY_READY.read_text(encoding="utf-8")
    assert "run = 36110717190" in text
    assert "status = PASS" in text
    assert "REAL_AIKENS_LAMBDA_OUTCOME = UNOPENED" in text
    assert "No simulated test payload is a scientific result." in text


def test_v2_postoutcome_pipeline_is_ready_but_real_outcome_unopened() -> None:
    text = V2_READY.read_text(encoding="utf-8")
    assert "Status: **PASS — V2 postoutcome pipeline ready" in text
    assert "run = 36311298413" in text
    assert "run = 36311298440" in text
    assert "REAL_AIKENS_LAMBDA_OUTCOME =" in text
    assert "UNOPENED" in text
    assert "identical blinded V2 main-manuscript hash" in text


def test_publication_status_routes_v2_to_geb_without_inheriting_v1_pipeline_readiness() -> None:
    text = PUB.read_text(encoding="utf-8")
    assert "FIRST_SHOT = Global Ecology and Biogeography / Research Article" in text
    assert "LEGACY_V1_POSTOUTCOME_GEB_PIPELINE = READY_FOR_V1_ONLY" in text
    assert "LEGACY_V1_POSTOUTCOME_READINESS = GEB_INTEGRATED_POSTOUTCOME_PIPELINE_READINESS_20260925.md" in text
    assert "CURRENT_V2_POSTOUTCOME_GEB_PIPELINE = READY" in text
    assert "CURRENT_V2_POSTOUTCOME_FASTCHECK_RUN = 36311298413" in text
    assert "REAL_AIKENS_LAMBDA_OUTCOME = UNOPENED" in text
    assert "Aikens fixed-24 h" in text and "adjudication" in text


def test_authenticated_aikens_workflow_builds_only_canonical_v2_outcome_package() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "Render registered Aikens outcome into V2 Supporting Information" in text
    assert "Build canonical V2 GEB postoutcome package" in text
    assert "scripts/build_payoff_b_v2_geb_postoutcome_package.py" in text
    assert "outputs/PAYOFF_B_V2_GEB_POSTOUTCOME_PACKAGE.zip" in text
    assert "scripts/build_geb_integrated_outcome_package.py" not in text
    assert "PAYOFF_B_INTEGRATED_TRACKING_ECOLOGY_V1_RENDERED.md" not in text
