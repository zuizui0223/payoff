from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "PAYOFF_B_TRACKING_THEORY_V1.md"
CROSSWALK = ROOT / "submission" / "PAYOFF_B_TRACKING_RESULTS_FIGURE_CROSSWALK.md"
SUPPLEMENT = ROOT / "submission" / "PAYOFF_B_TRACKING_SUPPLEMENT_MAP.md"


def test_every_results_subsection_is_in_crosswalk():
    manuscript = MANUSCRIPT.read_text(encoding="utf-8")
    crosswalk = CROSSWALK.read_text(encoding="utf-8")
    for index in range(1, 11):
        marker = f"### 3.{index} "
        heading = next(
            line for line in manuscript.splitlines()
            if line.startswith(marker)
        )
        assert f"3.{index} " in crosswalk, heading


def test_crosswalk_maps_all_main_result_figures():
    crosswalk = CROSSWALK.read_text(encoding="utf-8")
    for figure in range(2, 7):
        assert f"Figure {figure}" in crosswalk
    assert "No-orphan-number rule" in crosswalk
    assert "GEB phase-retention numbers never enter this crosswalk" in crosswalk


def test_supplement_map_has_six_declared_sections():
    supplement = SUPPLEMENT.read_text(encoding="utf-8")
    for index in range(1, 7):
        assert f"## Supplement S{index} " in supplement
    assert "The failed large-effect replication is retained, not hidden." in supplement
    assert "Synthetic controller gain is not an empirical Aikens estimate." in supplement


def test_supplement_keeps_main_paper_mechanism_first():
    supplement = SUPPLEMENT.read_text(encoding="utf-8")
    assert "mechanism-first rather than" in supplement
    assert "parameter-sweep-first" in supplement
    assert "resolution checks" in supplement
    assert "complete controller grids" in supplement
