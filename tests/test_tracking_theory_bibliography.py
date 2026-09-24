from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "submission" / "PAYOFF_B_TRACKING_REFERENCES.bib"
MANUSCRIPT = ROOT / "manuscript" / "PAYOFF_B_TRACKING_THEORY_V1.md"


EXPECTED = {
    "Muthukrishnan2025ChasingNiche": "10.1111/gcb.70167",
    "Hallfors2021WinningStrategy": "10.1111/ele.13774",
    "Macgregor2019PhenologyRange": "10.1038/s41467-019-12479-w",
    "Harsch2017MovingHabitat": "10.1111/1365-2745.12724",
    "Pontarp2015TimingAdaptation": "10.1007/s10682-015-9759-6",
    "Visser2019PhenologicalMismatch": "10.1038/s41559-019-0880-8",
    "Kharouba2020MismatchDisconnects": "10.1038/s41558-020-0752-x",
    "Gilman2012Mutualisms": "10.1111/j.1752-4571.2011.00202.x",
    "Weir2024BufferingMismatch": "10.1111/gcb.17294",
    "Fredston2025SpaceTime": "10.1016/j.tree.2025.03.015",
}


def test_tracking_bibliography_has_all_current_manuscript_sources():
    text = BIB.read_text(encoding="utf-8")
    assert text.count("@article{") == len(EXPECTED)
    for key, doi in EXPECTED.items():
        assert f"@article{{{key}," in text
        assert f"doi = {{{doi}}}" in text


def test_tracking_manuscript_points_to_submission_bibliography():
    text = MANUSCRIPT.read_text(encoding="utf-8")
    assert "submission/PAYOFF_B_TRACKING_REFERENCES.bib" in text
    for doi in EXPECTED.values():
        assert doi in text


def test_macgregor_doi_uses_correct_terminal_letter():
    text = BIB.read_text(encoding="utf-8")
    assert "10.1038/s41467-019-12479-w" in text
    assert "10.1038/s41467-019-12479-0" not in text
