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


def test_publication_status_routes_integrated_paper_to_geb() -> None:
    text = PUB.read_text(encoding="utf-8")
    assert "FIRST_SHOT = Global Ecology and Biogeography / Research Article" in text
    assert "POSTOUTCOME_GEB_PIPELINE = READY" in text
    assert "GEB_INTEGRATED_POSTOUTCOME_PIPELINE_READINESS_20260925.md" in text
    assert "Aikens fixed-24 h" in text and "adjudication" in text


def test_authenticated_aikens_workflow_builds_geb_outcome_package() -> None:
    text = WORKFLOW.read_text(encoding="utf-8")
    assert "Build science-ready GEB outcome package" in text
    assert "scripts/build_geb_integrated_outcome_package.py" in text
    assert "outputs/GEB_INTEGRATED_OUTCOME_PACKAGE.zip" in text
