#!/usr/bin/env python3
"""Add transparently POST-OUTCOME S3 science and revised paper to blinded archive.

Inputs are locked, previously source-reproduced V8+deer+day S2 review ZIP,
and separately executed S3 six-slope and spatial sensitivity artifacts.
PREPARE never declares source replay complete; FINISH is impossible without
a numerical comparison of the anonymized scientific code's actual R outputs.
No archive is deposited for journal review by this program.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import zipfile
from pathlib import Path

from scripts.build_amnat_v4_blind_repro_archive import neutral, safe, pdf_blind
from scripts.audit_amnat_v4_all_pdf_pages import audit_pdf
from scripts.verify_amnat_s3_exploratory_replay import SIX_FILES,SPATIAL_FILES

ROOT=Path(__file__).resolve().parents[1]
BASE_SHA="32593862ed317ac1bfcf9c86e46e57e9e87d34d156405fdb1a5d0125f7d544db"
ORIGINAL_SIX_R="analysis/movement_phenology/payoff_b_v8_daymetric_bird_transfer_exploratory.R"
ORIGINAL_SPATIAL_R="analysis/movement_phenology/payoff_b_v8_daymetric_spatial_sensitivity_posthoc.R"
PDF_NAME="Paper2_anonymous_real_observation_EDITORIAL_preview.pdf"


def sha(blob:bytes)->str:
    return hashlib.sha256(blob).hexdigest()


def only(root:Path,name:str)->Path:
    values=[p for p in root.rglob(name) if p.is_file()]
    if len(values)!=1:
        raise ValueError(f"Expected exact unique archived scientific file {name}; got {len(values)}")
    return values[0]


def add(root:Path,dest:str,data:bytes,check_text=True):
    if Path(dest).is_absolute() or ".." in Path(dest).parts:
        raise ValueError("Unsafe anonymous review ZIP path")
    if check_text:
        safe(data.decode("utf-8"),dest)
    path=root/dest
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(data)


def original_s3_supplement()->str:
    a=(ROOT/"submission/AMNAT_V4_SUPPLEMENTARY_TABLE_S3_DAY_TRANSFER_20261015.md").read_text()
    a=a.split("**Source and provenance:**",1)[0].rstrip()
    s=(ROOT/"docs/PAYOFF_B_V8_DAYMETRIC_SPATIAL_SENSITIVITY_RESULT_20261015.md").read_text()
    if "## Original 72-pair bootstrap" not in s:
        raise ValueError("Spatial sensitivity source with all 24 contrasts absent")
    s="## Original 72-pair bootstrap"+s.split("## Original 72-pair bootstrap",1)[1]
    s=re.sub(r"https://github\.com/zuizui0223/payoff/[^\s)]+",
             "original study provenance available to editors",s)
    combined=neutral(a)+"\n\n---\n\n# Further exploratory geographic-dependence diagnostics\n\n"+neutral(s)
    if ("10°" not in combined or "NOT_ESTIMABLE" not in combined
        or "564" not in combined or "−0.055101" not in combined):
        raise ValueError("Incomplete supplementary S3 six-model and spatial record")
    safe(combined,"Supplementary Table S3")
    return combined.rstrip()+"\n"


def reproduction_script()->str:
    return """#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p outputs/s3_transfer outputs/s3_spatial

Rscript analysis/seasonal_v8_daymetric_bird_transfer_exploratory.R \
 --pairs data/frozen_outputs/day_scale/seasonal_v8_metric_scale_pairs.csv \
 --birds data/frozen_outputs/day_scale/seasonal_v8_metric_scale_bird_rows.csv \
 --transfer data/frozen_outputs/transfer/seasonal_v8_transfer_primary_rows.csv \
 --structural data/frozen_outputs/structural/seasonal_v8_transfer_structural_null_rows.csv \
 --output outputs/s3_transfer

Rscript analysis/seasonal_v8_daymetric_spatial_sensitivity_posthoc.R \
 --original-joined outputs/s3_transfer/day_metric_to_bird_exploratory_joined_rows.csv \
 --original-slopes outputs/s3_transfer/day_metric_to_bird_exploratory_slopes.csv \
 --day-pairs data/frozen_outputs/day_scale/seasonal_v8_metric_scale_pairs.csv \
 --output outputs/s3_spatial

python3 -m scripts.verify_s3_science \
 --six-original data/posthoc_s3_original/six \
 --spatial-original data/posthoc_s3_original/spatial \
 --six-replay outputs/s3_transfer \
 --spatial-replay outputs/s3_spatial \
 --receipt outputs/s3_source_replay_receipt.json
"""


def prepare(base_zip:Path,six:Path,spatial:Path,pdf_root:Path,dest:Path,
            preview_dir:Path)->dict:
    if dest.exists() and any(dest.iterdir()):
        raise ValueError("Do not overwrite existing verified anonymous scientific archive")
    contents=base_zip.read_bytes()
    if sha(contents)!=BASE_SHA:
        raise ValueError("Original source-reproduced 60-file archive SHA256 drift")
    with zipfile.ZipFile(base_zip) as z:
        paths=z.namelist()
        if len(paths)<55 or any(p.startswith("/") or ".." in Path(p).parts for p in paths):
            raise ValueError("Source-verified full scientific archive inventory changed")
        z.extractall(dest)
    prior=json.loads((dest/"MANIFEST.json").read_text())
    if (prior.get("mule_deer_replay_verified") is not True
        or prior.get("supplement_S2_included") is not True):
        raise ValueError("Underlying V8, deer and S2 validation status missing")

    original_count=0
    for group,root,registered in (
        ("six",six,SIX_FILES),("spatial",spatial,SPATIAL_FILES),
    ):
        for name,n in registered.items():
            path=only(root,name)
            import csv
            with path.open(newline="",encoding="utf-8-sig") as source:
                count=sum(1 for _ in csv.DictReader(source))
            if count!=n:
                raise ValueError(f"Original S3 {group}/{name} wrong scientific unit count {count}")
            add(dest,f"data/posthoc_s3_original/{group}/{name}",path.read_bytes())
            original_count+=1

    for src,target in (
        (ORIGINAL_SIX_R,"analysis/seasonal_v8_daymetric_bird_transfer_exploratory.R"),
        (ORIGINAL_SPATIAL_R,"analysis/seasonal_v8_daymetric_spatial_sensitivity_posthoc.R"),
    ):
        text=neutral((ROOT/src).read_text(encoding="utf-8"))
        add(dest,target,text.encode("utf-8"))

    a=(ROOT/"scripts/verify_amnat_s3_exploratory_replay.py").read_text(encoding="utf-8")
    add(dest,"scripts/verify_s3_science.py",neutral(a).encode("utf-8"))
    add(dest,"scripts/reproduce_s3.sh",reproduction_script().encode("utf-8"))
    add(dest,"supplementary/Table_S3_day_metric_bird_transfer.md",
        original_s3_supplement().encode("utf-8"))

    # The main text and Appendix S4 must use the same EXACT piecewise
    # optimum and the same assumptions behind lambda and phase variance.
    # No fitting of natural effects occurs in this self-contained model.
    source_model=ROOT/"src/paper2_actionability_peak.py"
    source_tests=ROOT/"tests/test_paper2_actionability_peak.py"
    proof=ROOT/"submission/AMNAT_V4_SUPPLEMENTARY_MATHEMATICAL_NOTE_S4_20261017.md"
    model_text=neutral(source_model.read_text(encoding="utf-8"))
    tests_text=neutral(source_tests.read_text(encoding="utf-8"))
    proof_text=neutral(proof.read_text(encoding="utf-8"))
    for text_required in ("A_\\infty","threshold-normalized","conditional-mean",
                          "observation","innovation"):
        if text_required not in proof_text:
            raise ValueError("Mathematical S4 derivation missing: "+text_required)
    add(dest,"src/paper2_actionability_peak.py",model_text.encode("utf-8"))
    add(dest,"tests/test_paper2_actionability_peak.py",tests_text.encode("utf-8"))
    add(dest,"supplementary/Mathematical_Note_S4.md",proof_text.encode("utf-8"))
    math_verifier=neutral((ROOT/"scripts/verify_amnat_v4_theory_source.py").read_text(encoding="utf-8"))
    add(dest,"scripts/verify_theory_math.py",math_verifier.encode("utf-8"))


    latest=only(pdf_root,PDF_NAME)
    layout_receipt=json.loads(only(pdf_root,"source_identity_receipt.json").read_text(encoding="utf-8"))
    if (layout_receipt.get("figure_source_types")!=[
            "schematic","observed_rows","observed_rows","source_summary"]
        or layout_receipt.get("figure2_real_pair_points")!=166
        or layout_receipt.get("figure3_real_species_target_points")!=150):
        raise ValueError("Anonymous manuscript source incorrectly labels true raw-point figures")
    manuscript_md=only(pdf_root,"manuscript_anonymous.md").read_text(encoding="utf-8")
    if ("Source-frozen Figure 2 summary preview" in manuscript_md
        or "These are frozen summary-level previews" in manuscript_md
        or "The 166 original, distinct geographic" not in manuscript_md
        or "The 150 original bird species-target" not in manuscript_md
        or manuscript_md.count(r"\clearpage")!=4):
        raise ValueError("Orphan figure headings or inaccurate raw-data figure provenance")
    pdf_qc=only(pdf_root,"PDF_SOURCE_PREFLIGHT_HOLD.json")
    pre=json.loads(pdf_qc.read_text(encoding="utf-8"))
    if pre.get("status")!="ANONYMOUS_EDITORIAL_PDF_PREFLIGHT_PASS_SUBMISSION_HOLD":
        raise ValueError("Latest author-blinded paper did not pass original preflight")
    cleaned=pdf_blind(latest)
    import pymupdf
    with pymupdf.open(stream=cleaned,filetype="pdf") as paper:
        page_count=len(paper)
        extracted=re.sub(r"\s+"," "," ".join(p.get_text() for p in paper))
        for needle in ("Supplementary Table S3", "0.1504", "bird-specific",
                       "2.412","4.662","threshold-normalized",
                       "Supplementary Mathematical Note S4"):
            if needle not in extracted:
                raise ValueError("S3 ecological finding missing from newer PDF: "+needle)
        if len({img[0] for p in paper for img in p.get_images(full=True)})!=4:
            raise ValueError("Four source-grounded images lost in new manuscript")
    add(dest,"manuscript/editorial_preview.pdf",cleaned,False)

    previous=dest/"qc/PDF_ALL_PAGE_SOURCE_QC.json"
    if previous.exists():
        previous.unlink()
    page_qc=audit_pdf(dest/"manuscript/editorial_preview.pdf",preview_dir)
    if (page_qc["status"]!="PDF_ALL_PAGE_MECHANICAL_PASS_HUMAN_VISUAL_HOLD"
        or page_qc["pages"]!=page_count):
        raise ValueError("New complete manuscript all-page mechanical audit failed")
    add(dest,"qc/PDF_ALL_PAGE_SOURCE_QC.json",
        (json.dumps(page_qc,indent=2,ensure_ascii=False)+"\n").encode("utf-8"))

    readme=(dest/"README.md").read_text(encoding="utf-8")
    outdated="A *separate* RMSE-change-to-bird-mismatch transfer was NOT conducted; do not claim both transfer exposures fail from this table."
    if outdated in readme:
        readme=readme.replace(outdated,
             "The registered V8 bird transfer used correlations only. A SEPARATE, explicitly post-outcome six-model exploration of day-scale LOYO forecast value against real and fixed-arrival mismatch is now included as Supplementary S3; no bird-specific increment was detected, but a zero effect is not proved.")
    readme+="""\n\n## S3: fully reported additional post-outcome bird/forecast analysis

Six exploratory slopes compare two pre-existing day-unit environmental
forecasting metrics to actual log-mismatch, fixed-arrival structural-null
mismatch and their bird-specific difference. Confidence intervals are
cluster-resampled over 72 original distinct environmental source-target
pairs with equal species weights; no individual movement route was measured.

The nominal positive association for source MSE forecast value occurred
even when bird arrival was fixed. Neither bird-specific difference had
a 95% interval excluding zero. Source-cell, target-cell and 5-degree
geographic bootstrap sensitivity supports the same discrimination
boundary; 10-degree groups have only four blocks and are NOT_ESTIMABLE.
These results were all computed after original V8 outcomes were known,
not prospective confirmatory tests or demonstrated effects on fitness.

Replay the six comparisons and geographic sensitivity from actual archived
rows with: bash scripts/reproduce_s3.sh
"""
    readme+="""\n\n## S4: exact decision-time optimum and noisy observation caveat

The information/actionability optimum is piecewise: the short formula
log(1+alpha/beta)/alpha applies only in the threshold-normalized case
S*q0=B with increasing cue accuracy, not for arbitrary cue baselines.
With no positive gross opportunity, decline action; another regime
has an immediate optimum. The phase-retention lambda is a conditional
mean slope under specified linear noise assumptions; noisy cue
estimation generally prevents variance from equalling lambda squared
times prior variance.

The complete derivation and scope conditions are in
supplementary/Mathematical_Note_S4.md. Executable pure-Python
mathematics are in src/paper2_actionability_peak.py and tests in
tests/test_paper2_actionability_peak.py.

To verify the mathematical identities (requires pytest):
    python3 -m pytest -q tests/test_paper2_actionability_peak.py

These checks support algebraic internal consistency, not an empirical
animal information-use or fitness conclusion.
"""
    if outdated in readme:
        raise ValueError("Outdated claim that S3 was not executed remains in archive")
    add(dest,"README.md",readme.encode("utf-8"))

    manifest=json.loads((dest/"MANIFEST.json").read_text(encoding="utf-8"))
    manifest.update({
        "status":"ANONYMOUS_V8_DEER_S2_S3_SOURCE_REPLAY_PENDING_SUBMISSION_HOLD",
        "s3_six_slopes_postoutcome_and_multiplicity_exposed":True,
        "s3_spatial_sensitivity_after_six_outcomes":True,
        "s3_fixed_arrival_null_positive_not_behavioral_evidence":True,
        "s3_bird_specific_increment_detected":False,
        "s3_10degree_four_clusters_not_estimable":True,
        "registered_correlation_to_bird_transfer_changed":False,
        "day_scale_metric_to_bird_matching_direct_transfer_tested":True,
        "registered_day_scale_to_bird_transfer_tested":False,
        "s3_anonymized_R_code_replay_verified":False,
        "figure2_true_observation_points":166,
        "figure3_true_observation_points":150,
        "main_pdf_figure_heading_orphans_prevented":True,
        "s4_piecewise_actionability_derivation_archived":True,
        "s4_noisy_observation_variance_caveat_archived":True,
        "s4_math_test_verified_before_final_package":False,
        "s3_original_output_files":original_count,
        "revised_manuscript_pdf_pages":page_count,
        "revised_manuscript_sha256":sha(cleaned),
        "full_page_human_visual_approved":False,
        "anonymous_delivery_link_exists":False,
        "journal_submission_ready":False,
    })
    add(dest,"MANIFEST.json",(json.dumps(manifest,indent=2,sort_keys=True)+"\n").encode("utf-8"))
    return {"status":"S3_ANONYMOUS_INPUTS_AND_REVISED_PDF_READY_FOR_SCIENCE_REPLAY",
            "archived_original_exploratory_file_count":original_count,
            "revised_pdf_pages":page_count,
            "pdf_sha256":sha(cleaned),
            "original_registered_v8_modified":False,
            "human_visual_approved":False,
            "journal_submitted":False}


def zip_fixed(root:Path,archive:Path)->str:
    if archive.exists():
        raise ValueError("Original reviewer archive cannot be overwritten")
    archive.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(archive,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for p in sorted(x for x in root.rglob("*") if x.is_file()):
            zi=zipfile.ZipInfo(p.relative_to(root).as_posix(),date_time=(2026,10,15,0,0,0))
            zi.create_system=3
            zi.external_attr=(0o644&0xffff)<<16
            zi.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(zi,p.read_bytes())
    return sha(archive.read_bytes())


def finish(root:Path,archive:Path,receipt:Path)->dict:
    replay=root/"outputs/s3_source_replay_receipt.json"
    check=json.loads(replay.read_text())
    if check.get("status")!="S3_ORIGINAL_POSTOUTCOME_TRANSFER_AND_SPATIAL_REPLAY_MATCH":
        raise ValueError("S3 cannot become a review archive without exact numerical R replay")
    manifest=json.loads((root/"MANIFEST.json").read_text())
    if manifest.get("status")!="ANONYMOUS_V8_DEER_S2_S3_SOURCE_REPLAY_PENDING_SUBMISSION_HOLD":
        raise ValueError("Unexpected reviewer package lifecycle")
    manifest["status"]="ANONYMOUS_V8_DEER_S2_S3_SOURCE_REPRODUCED_EDITORIAL_HOLD"
    manifest["s3_anonymized_R_code_replay_verified"]=True
    required_math=("supplementary/Mathematical_Note_S4.md",
                   "src/paper2_actionability_peak.py",
                   "tests/test_paper2_actionability_peak.py",
                   "scripts/verify_theory_math.py",
                   "qc/S4_THEORY_MATH_GUARD.json")
    if any(not (root/name).is_file() for name in required_math):
        raise ValueError("S4 proof or executable mathematical replay receipt missing")
    math_audit=json.loads((root/"qc/S4_THEORY_MATH_GUARD.json").read_text(encoding="utf-8"))
    if math_audit.get("status")!="PAPER2_S4_PIECEWISE_AND_NOISY_CONTROLLER_SOURCE_PROOF_PASS":
        raise ValueError("S4 mathematics numerical/source validation not passed")
    if (math_audit.get("source_model_sha256")!=sha((root/"src/paper2_actionability_peak.py").read_bytes())
        or math_audit.get("supplement_S4_sha256")!=sha((root/"supplementary/Mathematical_Note_S4.md").read_bytes())):
        raise ValueError("S4 derivation or model differs from independently checked bytes")
    manifest["s4_math_test_verified_before_final_package"]=True
    manifest["full_page_human_visual_approved"]=False
    manifest["anonymous_delivery_link_exists"]=False
    manifest["journal_submission_ready"]=False
    add(root,"qc/S3_EXPLORATORY_SOURCE_REPLAY.json",
        (json.dumps(check,indent=2)+"\n").encode("utf-8"))
    # Derived files under outputs are not part of the archived provenance
    # (the original output draws already reside under data/posthoc_s3_original).
    manifest["file_hashes"]={
        p.relative_to(root).as_posix():sha(p.read_bytes())
        for p in sorted(root.rglob("*")) if p.is_file()
        and p.relative_to(root).parts[0]!="outputs"
        and p.relative_to(root).as_posix()!="MANIFEST.json"
    }
    add(root,"MANIFEST.json",(json.dumps(manifest,indent=2,sort_keys=True)+"\n").encode())
    for p in root.rglob("*"):
        if not p.is_file():continue
        rel=p.relative_to(root).as_posix()
        if rel.split("/")[0]=="outputs": continue
        safe(rel,"anonymous ZIP pathname")
        if p.suffix.lower() in (".r",".md",".py",".csv",".sh",".svg",".json",".txt"):
            safe(p.read_text(encoding="utf-8"),rel)
    # Remove generated R analysis outputs (can be independently reproduced)
    # but keep the cryptographic/scientific replay receipt under qc/.
    generated=root/"outputs"
    if generated.exists():
        import shutil
        shutil.rmtree(generated)
    digest=zip_fixed(root,archive)
    result={
       "status":"VERIFIED_S3_SCIENTIFIC_REPLAY_AND_ANONYMOUS_PDF_EDITORIAL_HOLD",
       "inner_zip_sha256":digest,
       "inner_zip_bytes":archive.stat().st_size,
       "archive_files":len([p for p in root.rglob("*") if p.is_file()]),
       "six_slopes_original_and_replay_matched":True,
       "spatial_sensitivity_and_564_leave_one_out_matched":True,
       "revised_manuscript_pdf_pages":manifest["revised_manuscript_pdf_pages"],
       "full_page_human_visual_approved":False,
       "anonymous_external_deposit":False,
       "journal_submitted":False,
       "original_v8_registered_results_changed":False,
    }
    receipt.parent.mkdir(parents=True,exist_ok=True)
    receipt.write_text(json.dumps(result,indent=2)+"\n",encoding="utf-8")
    return result


def main():
    p=argparse.ArgumentParser()
    sp=p.add_subparsers(dest="phase",required=True)
    p0=sp.add_parser("prepare")
    for name in ("base-zip","six","spatial","pdf","out","page-previews"):
        p0.add_argument("--"+name,type=Path,required=True)
    p1=sp.add_parser("finish")
    for name in ("root","zip","receipt"):
        p1.add_argument("--"+name,type=Path,required=True)
    a=p.parse_args()
    if a.phase=="prepare":
        result=prepare(a.base_zip,a.six,a.spatial,a.pdf,a.out,a.page_previews)
    else:
        result=finish(a.root,a.zip,a.receipt)
    print(json.dumps(result,ensure_ascii=False))


if __name__=="__main__":
    main()
