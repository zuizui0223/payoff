#!/usr/bin/env python3
"""Attach previously reported post-outcome S3 to the anonymous Paper 2 bundle.

Keep preregistered V8/deer evidence frozen. Add two observational predictor
contrasts, fixed-arrival structural-null comparisons and dependence checks
WITHOUT falsely promoting any post-outcome analysis to confirmatory evidence.

The anonymous bundle is not a deposited reviewer link or an approved journal
submission. The sanitized scientific R scripts must reproduce all 6 + 24
original result cells and every original 10,000-draw/omission source file
before the new ZIP can be finalized.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_ZIP_SHA256 = "047527afcb6eb6f59e52d7fec4cbe6988b350138b21c969c22aea3d8a8206016"
SIX_ORIGINALS = (
    "day_metric_to_bird_exploratory_slopes.csv",
    "day_metric_to_bird_exploratory_joined_rows.csv",
    "day_metric_to_bird_exploratory_bootstrap.csv",
    "day_metric_to_bird_exploratory_status.csv",
)
SPATIAL_ORIGINALS = (
    "spatial_sensitivity_all_24_intervals.csv",
    "spatial_sensitivity_scheme_status.csv",
    "leave_one_unit_out_all_564_slopes.csv",
    "leave_one_unit_out_summary.csv",
    "bootstrap_source_cell_10000.csv",
    "bootstrap_target_cell_10000.csv",
    "bootstrap_target_grid_5deg_10000.csv",
    "bootstrap_target_grid_10deg_10000.csv",
)
ORIGINAL_SCRIPTS = {
    "analysis/movement_phenology/payoff_b_v8_daymetric_bird_transfer_exploratory.R":
        "analysis/seasonal_v8_daymetric_bird_transfer_exploratory.R",
    "analysis/movement_phenology/payoff_b_v8_daymetric_spatial_sensitivity_posthoc.R":
        "analysis/seasonal_v8_daymetric_spatial_sensitivity_posthoc.R",
}
REPRO_SCRIPT = "scripts/reproduce_s3_exploratory.sh"


def sha(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def safe_text(value: str, title: str) -> None:
    from scripts.build_amnat_v4_blind_repro_archive import safe
    safe(value, title)
    if re.search(r"(?i)https?://(?:www\.)?github\.com",value):
        # Developer identities cannot be concealed by renaming the filesystem.
        raise ValueError("GitHub provenance URL in blinded reviewer file: "+title)


def add(root: Path, name: str, content: bytes, text: bool = True) -> None:
    if Path(name).is_absolute() or ".." in Path(name).parts:
        raise ValueError("Unsafe anonymous reviewer file path")
    if text:
        safe_text(content.decode("utf-8"),name)
    dest=root/name
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_bytes(content)


def unique_file(root: Path, name: str) -> Path:
    candidates=[x for x in root.rglob(name) if x.is_file()]
    if len(candidates)!=1:
        raise ValueError("Expected exactly one authenticated S3 result "+name)
    return candidates[0]


def sanitized_r(path: Path) -> str:
    from scripts.build_amnat_v4_blind_repro_archive import neutral
    code=neutral(path.read_text(encoding="utf-8"))
    safe_text(code,str(path))
    if ("POST_OUTCOME" not in code and "POST-OUTCOME" not in code):
        raise ValueError("Missing mandatory exploratory designation")
    return code


def s3_supplement() -> str:
    source=(ROOT/"submission/AMNAT_V4_SUPPLEMENTARY_TABLE_S3_DAY_TRANSFER_20261015.md").read_text(encoding="utf-8")
    if "**Source and provenance:**" not in source:
        raise ValueError("S3 editorial statement missing source/analysis distinction")
    science=source.split("**Source and provenance:**",1)[0].strip()
    if ("−0.064456" not in science or "−0.055101" not in science
            or "POST-OUTCOME" not in science):
        raise ValueError("Complete registered S3 scientific cells absent")
    return science+"""

**Second-stage post-outcome sensitivity (also exploratory):**
The source-cell (20), target-cell (19), and target 5° grid (9)
bootstraps all yielded confidence intervals crossing zero for BOTH
bird-specific increments; the fixed-arrival squared-loss-value
association stayed positive with intervals excluding zero.
The 10° grid had only four independent blocks and is explicitly
NOT_ESTIMABLE, without unreported down-selection. All 22 species and
72 environmental pairs were omitted in turn for all six models:
564 individual omission slopes, none selectively excluded.

All coordinates are retrospective statistical forecast scores,
not cues shown to have been available to a migrating bird before
departure. These sensitivities were designed after seeing the six
first-stage slopes, were not prespecified before V8, and are not
proof of zero behavioural effect, fitness or actionability.
"""


def readme_addendum() -> str:
    return """
## Supplement S3: POST-OUTCOME statistical forecast to bird matching

This reviewer candidate additionally provides Supplementary Table S3
on two retrospective day-scale predictors:

1. change in leave-one-year-out source-informed forecast RMSE (days);
2. change in source-added squared-loss forecast advantage (days squared).

Both are related to the original 150 species-target bird mismatch
responses across 72 distinct environmental source-target pairs.
Three outcomes are reported for each predictor: real bird mismatch,
fixed-arrival structural null, and real minus structural-null.
There are 6 tests in total with 10,000 bootstrap resamples of
unique environmental pairs. Four further spatial/group
sensitivity families were chosen AFTER those six results were opened:
20 source-cell groups, 19 target-cell groups, nine 5-degree blocks,
and only four 10-degree blocks (the latter NOT_ESTIMABLE).
All 22 species and 72 original environmental pairs underwent
complete leave-one-out checks; none was selected away post hoc.

RESULTS: Neither bird-specific incremental slope has a 95% interval
excluding zero; the source forecast-value association with fixed-bird-
arrival mismatch does have an interval above zero in estimable
spatial sensitivity schemes. This is structural/model compatibility,
NOT demonstrated bird cognition, recourse or a demographic fitness
change. The initial preregistered V8 rho-to-mismatch test remains
NOT_SUPPORTED and untouched. No selective result promotion.

To re-execute these post-outcome checks from the extracted ZIP:

    bash scripts/reproduce_s3_exploratory.sh

Python 3 and standard R are used. The verifier checks original and
replayed six slopes, 24 sensitivity cells, 40,000 total spatial
bootstrap rows (including the explicitly nonestimable 10-degree
scheme), and all 564 original deletion-slope rows.

Formal software license approval, author human review, all-page PDF
proofreading and anonymous reviewer delivery remain outstanding.
"""


def reproduction_command() -> str:
    return """#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p outputs/s3/six outputs/s3/spatial
Rscript analysis/seasonal_v8_daymetric_bird_transfer_exploratory.R \\
  --pairs data/frozen_outputs/day_scale/seasonal_v8_metric_scale_pairs.csv \\
  --birds data/frozen_outputs/day_scale/seasonal_v8_metric_scale_bird_rows.csv \\
  --transfer data/frozen_outputs/transfer/seasonal_v8_transfer_primary_rows.csv \\
  --structural data/frozen_outputs/structural/seasonal_v8_transfer_structural_null_rows.csv \\
  --output outputs/s3/six
Rscript analysis/seasonal_v8_daymetric_spatial_sensitivity_posthoc.R \\
  --original-joined outputs/s3/six/day_metric_to_bird_exploratory_joined_rows.csv \\
  --original-slopes outputs/s3/six/day_metric_to_bird_exploratory_slopes.csv \\
  --day-pairs data/frozen_outputs/day_scale/seasonal_v8_metric_scale_pairs.csv \\
  --output outputs/s3/spatial
python3 -m scripts.verify_s3_exploratory \\
  --six-original data/frozen_outputs/s3/six \\
  --spatial-original data/frozen_outputs/s3/spatial \\
  --six-replay outputs/s3/six \\
  --spatial-replay outputs/s3/spatial \\
  --receipt outputs/s3/S3_reproduction_verified.json
"""


def prepare(base_zip: Path, six: Path, spatial: Path, paper: Path, out: Path) -> dict:
    if out.exists() and any(out.iterdir()):
        raise ValueError("Refusing to overwrite existing blind-review candidate")
    if sha(base_zip.read_bytes())!=BASE_ZIP_SHA256:
        raise ValueError("Original verified S2/V8/deer review ZIP SHA256 drift")
    with zipfile.ZipFile(base_zip) as zipped:
        files=zipped.namelist()
        if len(files)<55 or any(x.startswith("/") or ".." in Path(x).parts for x in files):
            raise ValueError("Unsafe or incomplete original data/code archive")
        zipped.extractall(out)

    manifest=json.loads((out/"MANIFEST.json").read_text(encoding="utf-8"))
    if manifest.get("status")!="V8_DEER_AND_DAY_SCALE_POSTHOC_SOURCE_VERIFIED_EDITORIAL_HOLD":
        raise ValueError("Unverified original V8+deer+S2 source status")
    if manifest.get("day_scale_metric_to_bird_matching_direct_transfer_tested") is not False:
        raise ValueError("Original S2 must not claim S3 as already tested")

    for original,neutral_path in ORIGINAL_SCRIPTS.items():
        add(out,neutral_path,sanitized_r(ROOT/original).encode("utf-8"))
    verifier=(ROOT/"scripts/verify_amnat_s3_exploratory_replay.py").read_text(encoding="utf-8")
    add(out,"scripts/verify_s3_exploratory.py",verifier.encode("utf-8"))
    add(out,REPRO_SCRIPT,reproduction_command().encode("utf-8"))
    for group,source,files in (("six",six,SIX_ORIGINALS),
                                ("spatial",spatial,SPATIAL_ORIGINALS)):
        for name in files:
            value=unique_file(source,name).read_bytes()
            add(out,"data/frozen_outputs/s3/"+group+"/"+name,value)

    add(out,"supplementary/Table_S3_day_metric_bird_transfer.md",
        s3_supplement().encode("utf-8"))

    src=(out/"README.md").read_text(encoding="utf-8")
    add(out,"README.md",(src+readme_addendum()).encode("utf-8"))

    new_pdf=unique_file(paper,"Paper2_anonymous_real_observation_EDITORIAL_preview.pdf")
    from scripts.build_amnat_v4_blind_repro_archive import pdf_blind
    pdf_bytes=pdf_blind(new_pdf)
    import pymupdf
    with pymupdf.open(stream=pdf_bytes,filetype="pdf") as document:
        extracted="\n".join(page.get_text() for page in document)
        if "Supplementary Table S3" not in extracted or "+0.1504" not in extracted:
            raise ValueError("Current PDF does not incorporate S3 source-backed result")
        if "0.369" not in extracted or "0.062" not in extracted:
            raise ValueError("Preregistered V8 results lost from revised paper")
        page_count=len(document)
        image_xrefs={x[0] for page in document for x in page.get_images(full=True)}
        if len(image_xrefs)!=4:
            raise ValueError("Four source-grounded figures absent from new PDF")
    add(out,"manuscript/editorial_preview.pdf",pdf_bytes,False)

    from scripts.audit_amnat_v4_all_pdf_pages import audit_pdf
    prev=out/"qc/PDF_ALL_PAGE_SOURCE_QC.json"
    if prev.exists():prev.unlink()
    all_pages=audit_pdf(out/"manuscript/editorial_preview.pdf",
                        out.parent/"S3_full_page_visual_contact_sheets")
    if all_pages["status"]!="PDF_ALL_PAGE_MECHANICAL_PASS_HUMAN_VISUAL_HOLD":
        raise ValueError("New S3 manuscript PDF has failed whole-page QC")
    if all_pages["pages"]!=page_count:
        raise ValueError("Revised PDF page count drift")
    add(out,"qc/PDF_ALL_PAGE_SOURCE_QC.json",
        (json.dumps(all_pages,indent=2,ensure_ascii=False)+"\n").encode())

    manifest.update({
        "status":"V8_DEER_S2_S3_POSTOUTCOME_SOURCE_REPLAY_PENDING",
        "s3_analysis_status":"POST_OUTCOME_EXPLORATORY_SIX_SLOPES_PLUS_SECOND_STAGE_SPATIAL",
        "s3_six_slopes_and_four_spatial_schemes_included":True,
        "s3_bird_specific_information_use_identified":False,
        "original_v8_preregistered_analysis_modified":False,
        "original_deer_source_result_modified":False,
        "s3_anonymized_R_replay_confirmed":False,
        "s3_results_multiple_exploratory_comparisons":6,
        "s3_10_degree_spatial_scheme":"NOT_ESTIMABLE",
        "pdf_pages":page_count,
        "human_full_resolution_visual_approval":False,
        "anonymous_delivery_link_exists":False,
        "journal_submission_ready":False,
    })
    add(out,"MANIFEST.json",(json.dumps(manifest,indent=2,sort_keys=True)+"\n").encode())
    return {"status":manifest["status"],"pdf_pages":page_count,
            "six_source_rows":[6,150,10000,1],
            "spatial_source_files":len(SPATIAL_ORIGINALS),
            "anonymous_reviewer_archive_deposited":False,
            "journal_submission_ready":False}


def finalize(root:Path,output_zip:Path)->dict:
    receipt=root/"outputs/s3/S3_reproduction_verified.json"
    state=json.loads(receipt.read_text(encoding="utf-8"))
    if state.get("status")!="S3_ORIGINAL_POSTOUTCOME_TRANSFER_AND_SPATIAL_REPLAY_MATCH":
        raise ValueError("Replayed anonymous exploratory S3 not verified")
    if (state["six_original_comparisons"]!=6 or
        state["spatial_scheme_CI_rows"]!=24 or
        state["omission_slope_rows"]!=564):
        raise ValueError("S3 exploratory original row counts changed")
    add(root,"qc/S3_source_science_reproduction.json",
        (json.dumps(state,indent=2)+"\n").encode())
    manifest=json.loads((root/"MANIFEST.json").read_text(encoding="utf-8"))
    manifest["status"]="V8_DEER_S2_S3_POSTOUTCOME_SCIENTIFIC_REPLAY_VERIFIED_EDITORIAL_HOLD"
    manifest["s3_anonymized_R_replay_confirmed"]=True
    manifest["journal_submission_ready"]=False
    manifest["file_hashes"]={
        entry.relative_to(root).as_posix():sha(entry.read_bytes())
        for entry in sorted(root.rglob("*")) if entry.is_file()
        and entry.relative_to(root).as_posix()!="MANIFEST.json"
        and "outputs/" not in entry.relative_to(root).as_posix()
    }
    add(root,"MANIFEST.json",(json.dumps(manifest,sort_keys=True,indent=2)+"\n").encode())

    for file in root.rglob("*"):
        if file.is_file():
            path=file.relative_to(root).as_posix()
            # Replayed code results remain on disk for CI, not in reviewer
            # package; the original sources plus verification code suffice.
            if path.startswith("outputs/"):continue
            safe_text(path,"reviewer file name")
            if file.suffix.lower() in (".r",".py",".md",".csv",".json",".txt",".sh",".svg"):
                safe_text(file.read_text(encoding="utf-8"),path)

    if output_zip.exists():
        raise ValueError("Refusing to overwrite reviewer ZIP")
    output_zip.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(output_zip,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for file in sorted(p for p in root.rglob("*") if p.is_file()):
            key=file.relative_to(root).as_posix()
            if key.startswith("outputs/"):continue
            info=zipfile.ZipInfo(key,date_time=(2026,10,15,0,0,0))
            info.create_system=3
            info.external_attr=(0o644&0xffff)<<16
            info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,file.read_bytes())
    return {
        "status":"V8_DEER_S2_S3_ANONYMOUS_REPRODUCIBILITY_CANDIDATE_EDITORIAL_HOLD",
        "archive_sha256":sha(output_zip.read_bytes()),
        "archive_size_bytes":output_zip.stat().st_size,
        "archived_members":len(zipfile.ZipFile(output_zip).namelist()),
        "postoutcome_six_models_reproduced":True,
        "spatial_four_schemes_reproduced":True,
        "full_raw_source_available":True,
        "new_manuscript_S3_referenced":True,
        "underlying_causal_bird_mechanism_identified":False,
        "journal_submitted":False,
        "anonymous_external_review_link":False,
    }


def main()->None:
    p=argparse.ArgumentParser()
    sub=p.add_subparsers(dest="stage",required=True)
    first=sub.add_parser("prepare")
    for name in ("base-zip","six-original","spatial-original","paper","output"):
        first.add_argument("--"+name,type=Path,required=True)
    last=sub.add_parser("finalize")
    for name in ("input","zip","receipt"):
        last.add_argument("--"+name,type=Path,required=True)
    args=p.parse_args()
    if args.stage=="prepare":
        ans=prepare(args.base_zip,args.six_original,args.spatial_original,args.paper,args.output)
    else:
        ans=finalize(args.input,args.zip)
        args.receipt.parent.mkdir(parents=True,exist_ok=True)
        args.receipt.write_text(json.dumps(ans,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(ans,ensure_ascii=False))


if __name__=="__main__":
    main()
