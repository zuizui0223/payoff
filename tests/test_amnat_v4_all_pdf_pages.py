"""All-page PDF inspection is comprehensive mechanically but NOT human approval."""
from __future__ import annotations

from io import BytesIO
from pathlib import Path

import pytest

pymupdf=pytest.importorskip("pymupdf")
Image=pytest.importorskip("PIL.Image")

from scripts.audit_amnat_v4_all_pdf_pages import audit_pdf


def make_pdf(dest, pages=31, blank_page=None, identity=False, images=4, doi_tail_page=None):
    with pymupdf.open() as pdf:
        for i in range(pages):
            page=pdf.new_page(width=595,height=842)
            if i!=blank_page:
                text=(
                    "Environmental predictability alone does not determine seasonal tracking\n"
                    "Literature Cited 0.369 0.062; manuscript content and scientific text "
                    "for independent quality checking.\n"
                ) if i==0 else ("Unrelated section "+str(i)+": scientific discussion text "*3)
                if doi_tail_page is not None and i==doi_tail_page:
                    text="019-0880-8."
                if identity and i==4:
                    text="PAYOFF-B "+text
                page.insert_text((80,100),text[:150],fontsize=11)
            if 1<=i<=images:
                im=Image.new("RGB",(12,12),(30*i,10*i,50*i))
                stream=BytesIO()
                im.save(stream,format="PNG")
                page.insert_image(pymupdf.Rect(80,160,110,190),stream=stream.getvalue())
        pdf.save(dest,garbage=4,deflate=True)


def test_every_page_rasterized_with_non_submission_and_four_embedded_images(tmp_path):
    src=tmp_path/"proof.pdf"
    make_pdf(src)
    target=tmp_path/"audit"
    result=audit_pdf(src,target)
    assert result["status"]=="PDF_ALL_PAGE_MECHANICAL_PASS_HUMAN_VISUAL_HOLD"
    assert result["pages"]==31
    assert result["embedded_image_xrefs"]==4
    assert len(list(target.glob("page_*.png")))==31
    assert len(list(target.glob("contact_sheet_*.png")))==3
    assert result["human_visual_approval"] is False
    assert result["journal_submission_ready"] is False


def test_identity_leak_not_ignored(tmp_path):
    src=tmp_path/"leak.pdf"
    make_pdf(src,identity=True)
    with pytest.raises(ValueError,match="identity"):
        audit_pdf(src,tmp_path/"audit")


def test_blank_page_fails_audit_instead_of_claiming_visual_approval(tmp_path):
    src=tmp_path/"blank.pdf"
    make_pdf(src,blank_page=10)
    result=audit_pdf(src,tmp_path/"audit")
    assert result["status"]=="PDF_ALL_PAGE_MECHANICAL_REVIEW_REQUIRED"
    assert 11 in result["blank_pages"]
    assert not result["checks"]["no_blank_text_and_image_pages"]


def test_expected_four_figure_gate_fails_without_images(tmp_path):
    src=tmp_path/"no_images.pdf"
    make_pdf(src,images=0)
    result=audit_pdf(src,tmp_path/"audit")
    assert result["status"]=="PDF_ALL_PAGE_MECHANICAL_REVIEW_REQUIRED"
    assert not result["checks"]["four_embedded_figures"]



def test_doi_tail_only_reference_page_counts_real_chars_not_generated_spaces(tmp_path):
    src=tmp_path/"orphaned_doi.pdf"
    make_pdf(src,doi_tail_page=10)
    result=audit_pdf(src,tmp_path/"audit")
    assert result["status"]=="PDF_ALL_PAGE_MECHANICAL_REVIEW_REQUIRED"
    assert 11 in result["blank_pages"]
    assert result["per_page"][10]["chars"]<35
    assert result["checks"]["no_blank_text_and_image_pages"] is False
