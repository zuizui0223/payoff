"""Visual-PDF source/placement checks; no natural outcomes are changed."""
from io import BytesIO
import hashlib
import json
from pathlib import Path

import pytest

pymupdf=pytest.importorskip("pymupdf")
PIL=pytest.importorskip("PIL.Image")

from scripts.audit_amnat_v4_figure_page_and_caption_qc import audit
from scripts.build_amnat_v4_anonymous_preview import (
    FIGURE_CAPTIONS, SUMMARY_FIGURE_CAPTIONS,
    figure_appendix, anonymize, build_preview
)

ROOT=Path(__file__).resolve().parents[1]
MS=ROOT/"manuscript/PAYOFF_B_INFORMATION_CONTROL_V4_V8_INTEGRATED.md"

EXPECTED=[
    "Figure 1. Serial timing and control architecture. Schematic theory",
    "Figure 2. Early versus late signed green-up correlations for 166 distinct original source-target environmental spatial pairs",
    "Figure 3. Original 150 bird species-target mismatch observations associated with 72 distinct environmental spatial pairs",
    "Figure 4. Original published-source descriptive mule-deer summaries from 152 animal-years",
]


def fake_pdf(path:Path,obsolete=False,pair_figures=False):
    from PIL import Image
    with pymupdf.open() as doc:
        for page_no in range(1,43):
            page=doc.new_page(width=612,height=792)
            if page_no==1:
                page.insert_text((55,80),"Supplementary Table S3 0.1504. Figures 2 and 3 plot the original",
                                 fontsize=12)
            if page_no>=39:
                fi=page_no-38
                if fi>4:
                    continue
                summary=EXPECTED[fi-1]
                page.insert_textbox(pymupdf.Rect(55,50,600,160),summary,fontsize=11)
                pic=Image.new("RGB",(10,10),(30*fi,20*fi,40*fi))
                bio=BytesIO()
                pic.save(bio,format="PNG")
                rect=pymupdf.Rect(65,180,230,270)
                page.insert_image(rect,stream=bio.getvalue())
                if pair_figures and page_no==40:
                    other=Image.new("RGB",(10,10),(1,1,1))
                    bio2=BytesIO()
                    other.save(bio2,format="PNG")
                    page.insert_image(pymupdf.Rect(250,180,410,270),stream=bio2.getvalue())
            if obsolete and page_no==4:
                page.insert_text((55,300),"These are frozen summary-level previews",fontsize=11)
        doc.save(path,garbage=4,deflate=True)


def test_new_figure_appendix_is_nonfloating_and_evidence_accurate():
    md=figure_appendix([f"figure{i}_preview.png" for i in range(1,5)])
    assert md.count("\\clearpage")==4
    assert md.count("\\includegraphics")==4
    assert "150 bird species-target" in md
    assert "166 distinct" in md
    assert "not 150 independent" in md
    assert "Figures 2 and 3 plot the original" in md
    assert "These are frozen summary-level previews" not in md
    assert "Source-frozen Figure 2 summary preview" not in md
    assert len(FIGURE_CAPTIONS)==4
    with pytest.raises(ValueError):
        figure_appendix(["figure1.png"])


def test_manuscript_contains_no_internal_dryad_download_failure():
    raw=MS.read_text(encoding="utf-8")
    assert "The additional source-admission screen" not in raw
    assert "HTTP 401" not in raw
    anon=anonymize(raw)
    assert "the present the bird-data test" not in anon
    assert "The\nprospectively specified environmental analysis" in anon
    assert "after\nthe registered environmental-correlation result" in anon
    assert "The the bird-data test" not in anon
    assert "after\nthe the bird-data test" not in anon
    assert "published playback or settlement result is insufficient" in anon


def test_four_separate_figures_with_real_source_captions_pass(tmp_path):
    p=tmp_path/"new.pdf"
    fake_pdf(p)
    receipt=audit(p)
    assert receipt["status"]=="FOUR_SINGLE_PAGE_SOURCE_CORRECT_FIGURES_MECHANICALLY_VERIFIED_HUMAN_HOLD"
    assert receipt["figure_image_pages"]==[39,40,41,42]
    assert len(receipt["checks"])>=10
    assert all(receipt["checks"].values())
    assert receipt["human_full_page_visual_approval"] is False
    assert receipt["journal_submission_ready"] is False


def test_duplicate_figure_on_one_page_is_rejected(tmp_path):
    p=tmp_path/"crowded.pdf"
    fake_pdf(p,pair_figures=True)
    receipt=audit(p)
    assert receipt["status"]=="FIGURE_LAYOUT_OR_SOURCE_CAPTION_REVIEW_REQUIRED"
    assert not receipt["checks"]["exactly_four_separate_figure_pages"]


def test_legacy_false_summary_only_statement_is_rejected(tmp_path):
    p=tmp_path/"misleading.pdf"
    fake_pdf(p,obsolete=True)
    receipt=audit(p)
    assert receipt["status"]=="FIGURE_LAYOUT_OR_SOURCE_CAPTION_REVIEW_REQUIRED"
    assert receipt["checks"]["no_false_all_summary_only_statement"] is False



def figure_source_fixture(tmp_path:Path,kind:str):
    directory=tmp_path/kind
    directory.mkdir()
    raw=b'<svg xmlns="http://www.w3.org/2000/svg" width="20" height="10"><rect width="20" height="10" fill="blue"/></svg>'
    sha=hashlib.sha256(raw).hexdigest()
    for i in range(1,5):
        (directory/f"figure{i}_summary.svg").write_bytes(raw)
    if kind=="observed":
        receipt={
          "status":"REAL_POINT_F2_F3_AND_FROZEN_F1_F4_EDITORIAL_PREVIEW_PASS",
          "f2_observed_unique_spatial_pairs":166,
          "f3_observed_species_target_rows":150,
          "f3_independent_environment_pairs":72,
          "figure_sha256":{f"figure{i}_summary.svg":sha for i in range(1,5)},
        }
        (directory/"combined_figure_source_receipt.json").write_text(json.dumps(receipt))
    else:
        receipt={
          "status":"VERIFIED_SUMMARY_FIGURE_PREVIEW_SUBMISSION_HOLD",
          "figures":{f"figure{i}_summary.svg":{"sha256":sha} for i in range(1,5)},
        }
        (directory/"figure_manifest.json").write_text(json.dumps(receipt))
    return directory


def test_same_builder_respects_empirical_observations_vs_summary_mode(tmp_path):
    original=MS.read_text(encoding="utf-8")
    obs=figure_source_fixture(tmp_path,"observed")
    sm=figure_source_fixture(tmp_path,"summary")
    obs_path=tmp_path/"obs.md"
    sm_path=tmp_path/"summary.md"
    obs_receipt=build_preview(original,obs_path,obs)
    summary_receipt=build_preview(original,sm_path,sm)
    assert obs_receipt["figure_evidence_kind"]=="observed"
    assert summary_receipt["figure_evidence_kind"]=="summary"
    observed=obs_path.read_text(encoding="utf-8")
    summary=sm_path.read_text(encoding="utf-8")
    assert "166 distinct original source-target environmental spatial pairs" in observed
    assert "Original 150 bird species-target" in observed
    assert "150 bird species-target" not in summary
    assert "DOES NOT plot original pair rows" in summary
    assert "not scatterplots of original environmental pairs" in summary
    assert observed.count("\\clearpage")==4
    assert summary.count("\\clearpage")==4
    assert len(SUMMARY_FIGURE_CAPTIONS)==4


def test_altered_original_observation_svg_cannot_pass_source_hash_gate(tmp_path):
    original=MS.read_text(encoding="utf-8")
    observation=figure_source_fixture(tmp_path,"observed")
    src=observation/"figure2_summary.svg"
    src.write_bytes(src.read_bytes().replace(b'blue',b'red'))
    with pytest.raises(ValueError,match="SHA256 mismatch"):
        build_preview(original,tmp_path/"tamper.md",observation)
