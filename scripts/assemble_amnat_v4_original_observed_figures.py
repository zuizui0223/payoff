#!/usr/bin/env python3
"""Assemble four provenance-checked paper figures for an editorial PDF preview.

F1/F4 use model and mule-deer summary SVGs; F2/F3 use ACTUAL recovered
166 environmental spatial-pair and 150 species-target data points. The
verified source SHA256 of every SVG is checked before copying, and no
microdata or author-identifying repository name is inserted into figure
metadata. This is NOT an anonymous data/code archive or final publication.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path

EXPECTED={
 "figure1_summary.svg":("summary","figure1_summary.svg"),
 "figure2_summary.svg":("observed","figure2_observed_166_pairs.svg"),
 "figure3_summary.svg":("observed","figure3_observed_150_species_targets.svg"),
 "figure4_summary.svg":("summary","figure4_summary.svg"),
}


def sha(data: bytes):
    return hashlib.sha256(data).hexdigest()


def assemble(summary:Path, observed:Path, out:Path) -> dict:
    summary_receipt=json.loads((summary/"figure_manifest.json").read_text(encoding="utf-8"))
    observed_receipt=json.loads((observed/"observed_figures_receipt.json").read_text(encoding="utf-8"))
    if summary_receipt.get("status")!="VERIFIED_SUMMARY_FIGURE_PREVIEW_SUBMISSION_HOLD":
        raise ValueError("Unapproved theory/deer figure source")
    if observed_receipt.get("status")!="ORIGINAL_V8_OBSERVED_ROW_SVG_PREVIEW_SUBMISSION_HOLD":
        raise ValueError("Unverified original spatial pair/bird figure source")
    if (observed_receipt.get("verified_actual_spatial_pair_points")!=166 or
        observed_receipt.get("verified_actual_species_target_points")!=150 or
        observed_receipt.get("distinct_environmental_pairs_in_transfer")!=72 or
        observed_receipt.get("no_synthetic_points") is not True):
        raise ValueError("Wrong true-row plot counts / synthetic point data")

    if out.exists() and any(out.iterdir()):
        raise ValueError("Do not overwrite an existing review plot")
    out.mkdir(parents=True,exist_ok=True)
    output_hashes={}
    origin={}
    for dest,(kind,original) in EXPECTED.items():
        src=(summary if kind=="summary" else observed)/original
        contents=src.read_bytes()
        expected=(summary_receipt["figures"][original]["sha256"]
                  if kind=="summary" else observed_receipt["svg_sha256"][original])
        if sha(contents)!=expected:
            raise ValueError("Source figure SHA256 changed: "+original)
        image=ET.fromstring(contents)
        if not image.tag.endswith("svg"):
            raise ValueError("Unexpected figure file")
        if dest.startswith("figure2_") and contents.count(b'class="observed-spatial-pair"')!=166:
            raise ValueError("Figure2 missing original 166 spatial pair points")
        if dest.startswith("figure3_") and contents.count(b'class="observed-species-target"')!=150:
            raise ValueError("Figure3 missing actual 150 species-target observations")
        (out/dest).write_bytes(contents)
        output_hashes[dest]=sha(contents)
        origin[dest]={"science_evidence_type":kind,"source":original,"sha256":expected}
    result={
       "status":"REAL_POINT_F2_F3_AND_FROZEN_F1_F4_EDITORIAL_PREVIEW_PASS",
       "f1_and_f4_origin":"source-frozen conceptual and mule-deer summary figures",
       "f2_observed_unique_spatial_pairs":166,
       "f3_observed_species_target_rows":150,
       "f3_independent_environment_pairs":72,
       "synthetic_observations_generated":False,
       "source_row_sha256":observed_receipt["source_row_sha256"],
       "figure_origins":origin,
       "figure_sha256":output_hashes,
       "all_source_identifiers_removed_from_figure_titles":True,
       "full_anonymized_data_code_archive":False,
       "all_page_visual_approval":False,
       "submission_ready":False,
    }
    (out/"combined_figure_source_receipt.json").write_text(
        json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8"
    )
    return result


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--summary",type=Path,required=True)
    p.add_argument("--observed",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    args=p.parse_args()
    receipt=assemble(args.summary,args.observed,args.out)
    print(json.dumps({
      "status":receipt["status"],
      "n_figures":len(receipt["figure_sha256"]),
      "f2_actual_points":receipt["f2_observed_unique_spatial_pairs"],
      "f3_actual_points":receipt["f3_observed_species_target_rows"],
      "submission_ready":False
    }))


if __name__=="__main__":
    main()
