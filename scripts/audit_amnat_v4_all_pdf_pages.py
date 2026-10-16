#!/usr/bin/env python3
"""All-page structural/raster PDF audit for the AmNat Paper 2 review candidate.

Review EVERY page for extreme text overflow, missing glyphs, empty pages,
rendering exceptions, and unexpected project-identifying content. Export all
page thumbnails and contact sheets for HUMAN visual review. Automated checks
do not constitute human visual approval.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

FORBIDDEN=("zuizui0223","payoff_b","PAYOFF-B","ZHANG RUIQI","rachelzhang0223")
TITLE="Environmental predictability alone does not determine seasonal tracking"


def audit_pdf(pdf:Path,output:Path,render_all:bool=True) -> dict:
    import pymupdf
    from PIL import Image,ImageDraw

    output.mkdir(parents=True,exist_ok=True)
    raw=pdf.read_bytes()
    if any(x.casefold() in raw.decode("latin-1",errors="ignore").casefold() for x in FORBIDDEN):
        raise ValueError("Known internal identity token in PDF bytes")
    diagnostics=[]
    contact_images=[]
    overflow_all=[]
    blank_pages=[]
    replacement_pages=[]
    figure_xrefs=set()
    with pymupdf.open(pdf) as doc:
        metadata=doc.metadata or {}
        for k in ("author","creator","producer","subject","keywords"):
            if any(token.casefold() in str(metadata.get(k,"")).casefold() for token in FORBIDDEN):
                raise ValueError("PDF metadata contains author/project identifiers")
        for i,page in enumerate(doc):
            page_number=i+1
            content=page.get_text("text",sort=True)
            if any(t.casefold() in content.casefold() for t in FORBIDDEN):
                raise ValueError("Anonymous extracted text contains identity")
            if "\ufffd" in content or "\u25a0" in content:
                replacement_pages.append(page_number)
            rect=page.rect
            spans=[]
            overflow=[]
            for block in page.get_text("dict").get("blocks",[]):
                if block.get("type")!=0:
                    continue
                for ln in block.get("lines",[]):
                    for sp in ln.get("spans",[]):
                        spans.append(sp)
                        x0,y0,x1,y1=sp["bbox"]
                        if any(not math.isfinite(float(x)) for x in (x0,y0,x1,y1)):
                            overflow.append({"text":sp.get("text","")[:50],"error":"nonfinite bbox"})
                            continue
                        if x0 < rect.x0-4 or y0 < rect.y0-4 or x1>rect.x1+4 or y1>rect.y1+4:
                            overflow.append({"text":sp.get("text","")[:55],"bbox":[x0,y0,x1,y1]})
            if overflow:
                overflow_all.append({"page":page_number,"spans":overflow[:12],"n":len(overflow)})
            images=page.get_images(full=True)
            figure_xrefs.update(x[0] for x in images)
            # PyMuPDF sort=True can insert many synthetic spaces/newlines
            # for geometric text reconstruction. A DOI-tail-only page may
            # otherwise look like a 70-character page and evade QC.
            chars=len("".join(content.split()))
            if chars<35 and not images:
                blank_pages.append(page_number)
            entries={
                "page":page_number,
                "chars":chars,
                "spans":len(spans),
                "unique_image_xrefs":sorted({x[0] for x in images}),
                "boundary_overflow_n":len(overflow),
                "page_size_pt":[round(rect.width,2),round(rect.height,2)],
                "suspicious_missing_glyph":("\ufffd" in content or "\u25a0" in content),
            }
            if render_all:
                pix=page.get_pixmap(matrix=pymupdf.Matrix(.70,.70),alpha=False,colorspace=pymupdf.csRGB)
                thumb=Image.frombytes("RGB",[pix.width,pix.height],pix.samples)
                thumb.thumbnail((255,356))
                # Save EVERY page for human review, not selected-page sampling.
                thumb.save(output/f"page_{page_number:03d}.png",optimize=True)
                bg=Image.new("RGB",(280,386),"white")
                bg.paste(thumb,((280-thumb.width)//2,8))
                ImageDraw.Draw(bg).text((12,361),f"Page {page_number}/{len(doc)}",fill="black")
                contact_images.append(bg)
            diagnostics.append(entries)
        n_pages=len(doc)
        paper_text="\n".join(p.get_text("text") for p in doc)
    check={
        "length_in_expected_editorial_range":30<=n_pages<=60,
        "all_page_images_rendered":render_all and len(contact_images)==n_pages,
        "four_embedded_figures":len(figure_xrefs)==4,
        "no_text_span_extends_beyond_page":not overflow_all,
        "no_blank_text_and_image_pages":not blank_pages,
        "no_replacement_or_black_square_glyphs":not replacement_pages,
        "agreed_manuscript_title_retained":TITLE[:45] in paper_text,
        "literature_cited_retained":"Literature Cited" in paper_text,
        "frozen_v8_coefficients_present":("0.369" in paper_text and "0.062" in paper_text),
    }
    if render_all:
        for start in range(0,len(contact_images),12):
            group=contact_images[start:start+12]
            sheet=Image.new("RGB",(3*280,4*386),"#eeeeee")
            for j,item in enumerate(group):
                sheet.paste(item,((j%3)*280,(j//3)*386))
            sheet.save(output/f"contact_sheet_{start//12+1:02d}.png",optimize=True)
    status=("PDF_ALL_PAGE_MECHANICAL_PASS_HUMAN_VISUAL_HOLD"
            if all(check.values()) else "PDF_ALL_PAGE_MECHANICAL_REVIEW_REQUIRED")
    receipt={
        "status":status,
        "pdf_sha256":hashlib.sha256(raw).hexdigest(),
        "pages":n_pages,
        "embedded_image_xrefs":len(figure_xrefs),
        "checks":check,
        "blank_pages":blank_pages,
        "off_page_text_spans":overflow_all,
        "suspicious_character_pages":replacement_pages,
        "per_page":diagnostics,
        "every_page_rendered":render_all and len(contact_images)==n_pages,
        "human_visual_approval":False,
        "all_equations_human_approved":False,
        "all_figures_human_approved":False,
        "all_references_human_approved":False,
        "journal_submission_ready":False,
    }
    (output/"PDF_ALL_PAGE_AUDIT.json").write_text(
        json.dumps(receipt,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    return receipt


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--pdf",type=Path,required=True)
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    r=audit_pdf(args.pdf,args.output)
    print(json.dumps({"status":r["status"],"pages":r["pages"],
                      "checks":r["checks"],"human_approved":False}))
    if r["status"]!="PDF_ALL_PAGE_MECHANICAL_PASS_HUMAN_VISUAL_HOLD":
        raise SystemExit(2)


if __name__=="__main__":
    main()
