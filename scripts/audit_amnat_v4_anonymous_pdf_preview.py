#!/usr/bin/env python3
"""Mechanical PDF preflight of anonymous AmNat V4 editorial preview.

Does not replace page-by-page visual inspection; does not verify underlying
individual-level data or turn a preview into a submission-ready manuscript.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_pdf(path: Path, png_dir: Path | None = None) -> dict:
    import fitz
    with fitz.open(path) as pdf:
        all_text="\n".join(p.get_text() for p in pdf)
        all_image_ids={
            img[0] for page in pdf for img in page.get_images(full=True)
        }
        if png_dir:
            png_dir.mkdir(parents=True,exist_ok=True)
            pages_to_render={0,len(pdf)-1}
            pages_to_render.update(
                idx for idx, page in enumerate(pdf)
                if page.get_images(full=True)
            )
            for ix in sorted(pages_to_render):
                pdf[ix].get_pixmap(matrix=fitz.Matrix(1.1,1.1),alpha=False).save(
                    str(png_dir/f"preview_page_{ix+1:03d}.png")
                )
        checks={
            "has_multiple_pages": len(pdf)>=10,
            "has_agreed_title": "Environmental predictability alone does not determine" in all_text,
            "retains_v8_environment_result": "0.369" in all_text,
            "retains_v8_transfer_result": "0.062" in all_text,
            "contains_literature_cited": "Literature Cited" in all_text,
            "has_four_png_images": len(all_image_ids)>=4,
            "project_name_not_revealed": "PAYOFF-B" not in all_text,
            "internal_v8_code_not_revealed": "V8" not in all_text,
            "no_git_identity": "zuizui0223" not in all_text,
            "no_admin_postfreeze_block": "Post-freeze transparency statement" not in all_text,
        }
        receipt={
            "status":"ANONYMOUS_EDITORIAL_PDF_PREFLIGHT_PASS_SUBMISSION_HOLD"
                     if all(checks.values()) else "PDF_PREFLIGHT_FAIL",
            "pdf_sha256":sha256(path),
            "pages":len(pdf),
            "embedded_image_count":len(all_image_ids),
            "checks":checks,
            "has_real_anonymized_pdf":True,
            "math_visually_verified_on_all_pages":False,
            "all_figures_visually_approved":False,
            "underlying_pair_animal_microdata_reproduced":False,
            "anonymous_data_code_archive_deposited":False,
            "submission_ready":False,
        }
    return receipt


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--pdf",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--png-dir",type=Path,default=None)
    a=p.parse_args()
    receipt=audit_pdf(a.pdf,a.png_dir)
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({k:receipt[k] for k in (
        "status","pages","embedded_image_count","checks","submission_ready"
    )}))
    if not all(receipt["checks"].values()):
        raise SystemExit(2)


if __name__=="__main__":
    main()
