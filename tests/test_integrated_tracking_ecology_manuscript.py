from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTEGRATED = ROOT / "manuscript" / "PAYOFF_B_INTEGRATED_TRACKING_ECOLOGY_V1_PREOUTCOME.md"
ARCH = ROOT / "docs" / "PAYOFF_B_TWO_PAPER_PUBLICATION_ARCHITECTURE_20260925.md"
THEOREM = ROOT / "manuscript" / "PAYOFF_B_THEORETICAL_ECOLOGY_BRIEF_V1.md"
TRACKING_SOURCE = ROOT / "manuscript" / "PAYOFF_B_TRACKING_THEORY_V1.md"
GEB_SOURCE = ROOT / "manuscript" / "PAYOFF_B_MOVEMENT_PHENOLOGY_GEB_V3_PREOUTCOME.md"


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_two_paper_architecture_keeps_exact_theorem_independent() -> None:
    m = text(INTEGRATED)
    a = text(ARCH)
    assert THEOREM.exists()
    assert "exact anti-phase optimum theorem remains a separate PAYOFF-B1 paper" in m
    assert "Paper 1 — exact benchmark" in a


def test_integrated_manuscript_retains_primary_broad_falsification() -> None:
    m = text(INTEGRATED)
    assert "5,816 observations from 55 migratory bird species" in m
    assert "does not support one portable natural movement-speed/environmental-wave-speed optimum" in m
    assert "The primary macroecological result is therefore a falsification" in m


def test_integrated_manuscript_keeps_aikens_outcome_unopened() -> None:
    m = text(INTEGRATED)
    assert "Aikens industrial-development lambda outcome remains unopened" in m
    assert "[AIKENS LAMBDA RESULT PENDING" in m
    assert "[AIKENS LAMBDA DISCUSSION PENDING" in m
    assert "[AIKENS LAMBDA CONCLUSION PENDING" in m


def test_integration_does_not_promote_universal_lambda() -> None:
    m = text(INTEGRATED)
    assert "common inference framework rather than a common coefficient" in m
    assert "It does not support:" in m
    assert "a universal lambda or universal actuator" in m


def test_original_source_manuscripts_remain_available() -> None:
    assert TRACKING_SOURCE.exists()
    assert GEB_SOURCE.exists()
