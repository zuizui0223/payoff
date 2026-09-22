from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = (
    ROOT
    / ".github"
    / "workflows"
    / "payoff-b-aikens-appeears-full-extraction.yml"
)


def test_aikens_full_workflow_freezes_target_geometry_before_environment():
    text = WORKFLOW.read_text(encoding="utf-8")

    required_order = [
        "Build exact canonical manifest",
        "Build frozen GPS-to-pixel phase keys",
        "Select fixed 24-hour GPS targets before environmental joining",
        "Require pre-environment support ceiling",
        "Require configured AppEEARS credentials",
        "Submit all exact-manifest tasks and download bundles",
        "Reconstruct primary V061 peak IRG",
        "Attach primary V061 phase to frozen GPS targets",
        "Build adjacent valid fixed-target phase pairs",
        "Fit preregistered within-mule-deer lambda contrast",
        "Evaluate registered lambda gate or record NOT ESTIMABLE",
        "Render preregistered Aikens outcome into GEB manuscript",
        "Audit rendered GEB manuscript",
    ]

    positions = []
    for label in required_order:
        assert label in text, f"workflow missing required step: {label}"
        positions.append(text.index(label))

    assert positions == sorted(positions)


def test_aikens_full_workflow_does_not_reselect_pairs_after_environment():
    text = WORKFLOW.read_text(encoding="utf-8")

    # The superseded environment-first pair selector must not return to the
    # canonical Aikens workflow.
    assert "scripts/build_fixed_interval_phase_pairs.py" not in text
    assert "scripts/select_fixed_interval_gps_targets.py" in text
    assert "scripts/attach_peak_irg_to_fixed_targets.py" in text
    assert "scripts/build_phase_pairs_from_fixed_targets.py" in text


def test_aikens_full_workflow_freezes_support_before_network_submission():
    text = WORKFLOW.read_text(encoding="utf-8")

    ceiling = text.index(
        "scripts/audit_fixed_target_support_ceiling.py"
    )
    credentials = text.index(
        "Require configured AppEEARS credentials"
    )
    submit = text.index(
        "scripts/run_appeears_manifest.py"
    )

    assert ceiling < credentials < submit


def test_aikens_full_workflow_keeps_registered_support_thresholds():
    text = WORKFLOW.read_text(encoding="utf-8")

    # Both pre-environment ceiling and final fitted contrast must preserve the
    # registered support thresholds.
    assert text.count("--min-animals-per-group 10") >= 2
    assert text.count("--min-pairs-per-group 100") >= 2
