#!/usr/bin/env python3
"""Content-aware figure-placement QC for the anonymous AmNat Paper 2 PDF.

The original 41-page mechanically checked review copy had two serious
editorial failures: headings 2/3 orphaned on the page before their two
small plots, and a falsely generic "all figures are summary-only" line.
This checker requires four different image-bearing pages, one real data
figure per page, authentic caption descriptions and removal of inherited
internal operational prose. Mechanical QC is not author visual approval.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

def audit(pdf:Path)->dict:
    import pymupdf
    with pymupdf.open(pdf) as doc:
        n=len(doc)
        texts=[" ".join(p.get_text("text",sort=True).split()) for p in doc]
        whole=" ".join(texts)
        images={
            i+1:sorted({z[0] for z in p.get_images(full=True)})
            for i,p in enumerate(doc) if p.get_images(full=True)
        }
        result={
            "pdf_sha256":hashlib.sha256(pdf.read_bytes()).hexdigest(),
            "page_count":n,
            "figure_image_pages":list(images),
            "figures_per_page":{str(page):len(ids) for page,ids in images.items()},
            "checks":{},
            "human_full_page_visual_approval":False,
            "anonymous_reviewer_deposit_exists":False,
            "journal_submission_ready":False,
        }
        checks=result["checks"]
        checks["credible_review_page_count"]=39<=n<=48
        checks["exactly_four_separate_figure_pages"]=len(images)==4 and all(len(v)==1 for v in images.values())
        checks["four_nonduplicated_image_sources"]=len({ids[0] for ids in images.values() if ids})==4
        checks["figures_appear_in_original_number_order"]=False
        expected=[
            (1,("Figure 1.", "Conceptual timer-controller", "schematic")),
            (2,("Figure 2.", "166 original, distinct geographic", "environmental pairs")),
            (3,("Figure 3.", "150 original bird species-target", "72 environmental pairs")),
            (4,("Figure 4.", "Mule-deer phase contraction", "152 animal-years")),
        ]
        matches=[]
        for i,phrases in expected:
            containing=[
                p for p in images
                if all(phrase.casefold() in texts[p-1].casefold() for phrase in phrases)
            ]
            checks[f"figure_{i}_caption_on_image_page"]=len(containing)==1
            matches.extend(containing[:1])
        if len(matches)==4:
            checks["figures_appear_in_original_number_order"]=matches==sorted(matches) and len(set(matches))==4
        checks["no_false_all_summary_only_statement"]="These are frozen summary-level previews" not in whole
        checks["no_old_generic_figure_preview_caption"]="Source-frozen Figure 2 summary preview" not in whole and "Source-frozen Figure 3 summary preview" not in whole
        checks["no_internal_dryad_http_access_note"]="HTTP 401" not in whole and "the present the bird-data test" not in whole
        checks["s3_registered_conclusions_present"]="Supplementary Table S3" in whole and "0.1504" in whole
        checks["genuine_data_and_conceptual_figure_distinction"]=("166 original, distinct geographic" in whole and "150 original bird species-target" in whole and "This schematic" not in whole)
        checks["no_identifying_owner"]="zuizui0223" not in whole.lower() and "PAYOFF-B" not in whole
        result["status"]=(
           "FOUR_SINGLE_PAGE_SOURCE_CORRECT_FIGURES_MECHANICALLY_VERIFIED_HUMAN_HOLD"
           if all(checks.values()) else
           "FIGURE_LAYOUT_OR_SOURCE_CAPTION_REVIEW_REQUIRED"
        )
        return result

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--pdf",type=Path,required=True)
    parser.add_argument("--receipt",type=Path,required=True)
    opts=parser.parse_args()
    r=audit(opts.pdf)
    opts.receipt.parent.mkdir(parents=True,exist_ok=True)
    opts.receipt.write_text(json.dumps(r,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({key:r[key] for key in (
        "status","page_count","figure_image_pages","checks","journal_submission_ready"
    )},ensure_ascii=False))
    if r["status"]!="FOUR_SINGLE_PAGE_SOURCE_CORRECT_FIGURES_MECHANICALLY_VERIFIED_HUMAN_HOLD":
        raise SystemExit(2)

if __name__=="__main__":
    main()
