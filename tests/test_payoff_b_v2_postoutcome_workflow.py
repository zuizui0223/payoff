from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "payoff-b-aikens-appeears-full-extraction.yml"


def test_real_aikens_workflow_routes_only_to_canonical_v2_package():
    text = WORKFLOW.read_text(encoding="utf-8")

    assert "build_payoff_b_v2_geb_outcome_package.py" in text
    assert "outputs/PAYOFF_B_V2_GEB_OUTCOME_PACKAGE.zip" in text
    assert "PAYOFF_B_V2_POSTOUTCOME_INVARIANTS_OK" in text

    # V1 outcome generation is provenance-only and must never be reactivated
    # inside the real authenticated result-opening workflow.
    forbidden = (
        "PAYOFF_B_INTEGRATED_TRACKING_ECOLOGY_V1_RENDERED.md",
        "PAYOFF_B_INTEGRATED_TRACKING_OUTCOME_PACKAGE.zip",
        "GEB_INTEGRATED_OUTCOME_PACKAGE.zip",
        "build_integrated_tracking_outcome_package.py",
        "build_geb_integrated_outcome_package.py",
        "render_integrated_tracking_figures.py",
    )
    for token in forbidden:
        assert token not in text


def test_real_aikens_result_is_si_only_in_v2_workflow():
    text = WORKFLOW.read_text(encoding="utf-8")

    assert '"aikens_result_location"] == "Supporting Information only"' in text
    assert '"main_text_retuned"] is False' in text
    assert '"main_figures_retuned"] is False' in text
    assert '"v2_headline_changed"] is False' in text
