from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "PAYOFF_B_TRACKING_THEORY_V1.md"
READINESS = ROOT / "submission" / "PAYOFF_B_TRACKING_SUBMISSION_READINESS.md"
AUDIT = ROOT / "submission" / "PAYOFF_B_TRACKING_FIGURE_VISUAL_AUDIT.md"
REFERENCES = ROOT / "submission" / "PAYOFF_B_TRACKING_REFERENCES.bib"
CROSSWALK = ROOT / "submission" / "PAYOFF_B_TRACKING_RESULTS_FIGURE_CROSSWALK.md"
SUPPLEMENT = ROOT / "submission" / "PAYOFF_B_TRACKING_SUPPLEMENT_MAP.md"
PARAMETERS = ROOT / "submission" / "PAYOFF_B_TRACKING_PARAMETER_TABLE.md"
CAPTIONS = ROOT / "submission" / "PAYOFF_B_TRACKING_FIGURE_CAPTIONS.md"


FRAMING_AMENDMENT = (
    ROOT / "data" / "payoff_b_tracking_theory_framing_amendment_20260925.json"
)


def test_tracking_theory_final_novelty_sentence_is_amendment_frozen():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    assert (
        "formal separation of endpoint environmental mismatch from the tracking "
        "architecture that produces it"
    ) in text
    assert FRAMING_AMENDMENT.exists()


def test_tracking_theory_visual_audit_is_frozen():
    assert AUDIT.exists()
    text = AUDIT.read_text(encoding="utf-8")
    assert "36089011639" in text
    assert "10845126875" in text
    assert "5249d69a52b0e95f958432d121910bc1b45a90f6074ac7f5961492b3f2453513" in text
    assert "From buffered mismatch to tracking breakdown" in text
    for figure in range(1, 7):
        assert f"| {figure} |" in text
    assert text.count("| PASS |") == 6


def test_tracking_theory_readiness_declares_scientific_freeze():
    text = READINESS.read_text(encoding="utf-8")
    assert "scientifically frozen" in text
    assert "No unresolved synthetic result" in text
    assert "human/administrative rather than scientific or mechanical" in text
    assert "No unresolved synthetic result" in text
    assert "10" in text
    assert "235" in text
    assert "endpoint mismatch" in text
    assert "OIKOS_MACHINE_PREPARATION_AUDIT_20260925.md" in text


def test_tracking_theory_freeze_assets_exist():
    for path in [
        REFERENCES,
        CROSSWALK,
        SUPPLEMENT,
        PARAMETERS,
        CAPTIONS,
    ]:
        assert path.exists(), path
