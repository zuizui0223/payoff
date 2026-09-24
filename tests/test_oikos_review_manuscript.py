import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from build_oikos_review_manuscript import build_review_rtf

BS = chr(92)


def test_oikos_review_rtf_has_required_layout_controls():
    text = build_review_rtf()
    assert text.startswith("{" + BS + "rtf1")
    assert BS + "linemod1" in text
    assert BS + "linecont" in text
    assert BS + "sl480" + BS + "slmult1" in text
    assert BS + "fldinst PAGE" in text
    assert BS + "page" in text


def test_oikos_review_rtf_puts_introduction_after_page_break():
    text = build_review_rtf()
    page = text.index(BS + "page")
    intro = text.index("1. Introduction")
    abstract = text.index("Abstract")
    assert abstract < page < intro


def test_oikos_review_rtf_is_anonymous_and_strips_internal_notes():
    text = build_review_rtf()
    forbidden = [
        "ZHANG RUIQI",
        "rachelzhang0223",
        "Programme boundary",
        "Evidence boundary",
        "synthetic theory manuscript v1",
        "Frozen result provenance",
        "PAYOFF_B_TRACKING_THEORY_PRIOR_ART",
    ]
    for item in forbidden:
        assert item not in text


def test_oikos_review_rtf_includes_figure_legends():
    text = build_review_rtf()
    assert "References" in text
    assert "Gilman RT" in text
    assert "AI use statement" in text
    assert "OpenAI ChatGPT was used" in text
    assert "Prior-art boundary" not in text
    assert "PAYOFF_B_TRACKING_THEORY_PRIOR_ART" not in text
    assert "Figure legends" in text
    for figure in range(1, 7):
        assert f"Figure {figure}." in text
