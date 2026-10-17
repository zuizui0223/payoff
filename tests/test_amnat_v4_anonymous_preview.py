"""Tests of anonymization and non-submission-ready anonymous editorial preview."""
from __future__ import annotations

from pathlib import Path

import pytest

from scripts.build_amnat_v4_anonymous_preview import (
    TITLE, anonymize, build_preview,
)

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"manuscript/PAYOFF_B_INFORMATION_CONTROL_V4_V8_INTEGRATED.md"


def source():
    return SOURCE.read_text(encoding="utf-8")


def test_anonymization_preserves_frozen_claims_math_and_20_reference_core():
    old=source()
    new=anonymize(old)
    assert new.startswith("# "+TITLE)
    assert "PAYOFF-B" not in new
    assert "V8" not in new
    assert "V3" not in new
    assert "V4" not in new
    assert "Post-freeze transparency statement" not in new
    assert "## Literature Cited" in new
    assert new.count("https://doi.org/") >= 20
    assert "0.369" in new and "0.062" in new
    assert "152 animal-years" in new
    assert "same individuals' migration speed" in new
    assert old.count(r"\[") == new.count(r"\[")
    assert len(new) < len(old)


def test_preview_receipt_is_explicitly_non_submission_ready(tmp_path):
    path=tmp_path/"anonymous_preview.md"
    result=build_preview(source(),path)
    assert path.exists()
    assert result["status"]=="ANONYMOUS_MARKDOWN_EDITORIAL_PREVIEW_SUBMISSION_HOLD"
    assert result["admin_provenance_stripped"]
    assert result["figure_count"]==0
    assert result["approved_for_journal_submission"] is False
    assert result["full_underlying_data_included"] is False
    assert "Original" not in result.get("figure_images",[])
    assert "PAYOFF-B" not in path.read_text(encoding="utf-8")


def test_missing_cited_bibliography_fails_closed():
    text=source()
    with pytest.raises(ValueError,match="Literature Cited"):
        anonymize(text.replace("## Literature Cited","## Bibliography Missing"))


def test_internal_project_title_drift_fails_closed():
    text=source()
    with pytest.raises(ValueError,match="title"):
        anonymize(text.replace(TITLE,"A dramatically different title",1))


def test_missing_data_claim_fails_closed():
    text=source().replace("+0.369","0.999")
    with pytest.raises(ValueError,match="Major numeric"):
        anonymize(text)



def _figure_fixtures(folder, bad_pair_n=None):
    folder.mkdir()
    def svg(points=""):
        return ('<svg xmlns="http://www.w3.org/2000/svg" '
                'width="240" height="150" viewBox="0 0 240 150">'
                '<rect width="240" height="150" fill="white"/>'
                +points+"</svg>")
    for i in (1,4):
        (folder/f"figure{i}_summary.svg").write_text(svg(),encoding="utf-8")
    n=166 if bad_pair_n is None else bad_pair_n
    pair="".join(f'<circle class="observed-spatial-pair" cx="{j%230}" cy="45" r="1"/>'
                 for j in range(n))
    bird="".join(f'<circle class="observed-species-target" cx="{j%230}" cy="70" r="1"/>'
                 for j in range(150))
    (folder/"figure2_summary.svg").write_text(svg(pair),encoding="utf-8")
    (folder/"figure3_summary.svg").write_text(svg(bird),encoding="utf-8")


def test_true_166_and_150_observations_are_not_mislabeled_as_summary_figures(tmp_path):
    pytest.importorskip("cairosvg")
    folder=tmp_path/"sourcefigs"
    _figure_fixtures(folder)
    result=build_preview(source(),tmp_path/"manuscript.md",folder)
    text=(tmp_path/"manuscript.md").read_text(encoding="utf-8")
    assert result["figure_count"]==4
    assert result["figure_source_types"]==[
        "schematic","observed_rows","observed_rows","source_summary"
    ]
    assert result["figure2_real_pair_points"]==166
    assert result["figure3_real_species_target_points"]==150
    assert "The 166 original, distinct geographic" in text
    assert "The 150 original bird species-target" in text
    assert "Source-frozen Figure 2 summary preview" not in text
    assert "These are frozen summary-level previews" not in text
    assert "### Figure 2" not in text
    assert text.count(r"\clearpage")==4
    assert result["approved_for_journal_submission"] is False


def test_counterfeit_partial_observation_panel_fails_closed(tmp_path):
    pytest.importorskip("cairosvg")
    folder=tmp_path/"sourcefigs"
    _figure_fixtures(folder,bad_pair_n=165)
    with pytest.raises(ValueError,match="original-row plot count"):
        build_preview(source(),tmp_path/"manuscript.md",folder)
