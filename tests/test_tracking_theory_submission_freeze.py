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


NOVELTY = (
    "The contribution is not a new demonstration that species can respond to "
    "climate change in both space and time. It is the separation of adaptive "
    "capacity from unilateral accessibility when interacting partners can "
    "reallocate tracking between spatial and temporal axes."
)


def test_tracking_theory_final_novelty_sentence_is_frozen():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    assert NOVELTY in text


def test_tracking_theory_visual_audit_is_frozen():
    assert AUDIT.exists()
    text = AUDIT.read_text(encoding="utf-8")
    assert "35987790697" in text
    assert "10803495155" in text
    assert "0d61c3f691d3d37cdffcb3703ec0fd6dd43efdf1d3442cda1cd8ba379a01914e" in text
    for figure in range(1, 7):
        assert f"| {figure} |" in text
    assert text.count("| PASS |") == 6


def test_tracking_theory_readiness_declares_scientific_freeze():
    text = READINESS.read_text(encoding="utf-8")
    assert "scientifically frozen" in text
    assert "No unresolved synthetic result" in text
    assert "journal-specific packaging only" in text


def test_tracking_theory_freeze_assets_exist():
    for path in [
        REFERENCES,
        CROSSWALK,
        SUPPLEMENT,
        PARAMETERS,
        CAPTIONS,
    ]:
        assert path.exists(), path
