#!/usr/bin/env python3
"""Update the VERIFIED V8+deer reviewer candidate with posthoc day-scale science.

Replaces only the EDITORIAL PDF and adds historically executed diagnostic R,
original recovered numerical day-scale outputs, a reproducible supplement,
and a fail-closed independent Python check. Never changes V8/deer scientific
source observations or previously locked confirmatory outcomes.

IMPORTANT: the resulting package is still NOT an external anonymous deposit.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import zipfile
from pathlib import Path

from scripts.build_amnat_v4_blind_repro_archive import neutral, safe, pdf_blind

ROOT=Path(__file__).resolve().parents[1]
BASE_ZIP_SHA="dfb568290d4a5c6a9bac21251e5c0370ca791c95faff5c599d8b2afd0ad89934"
DAY_SCRIPT_SHA="a42b4d9f1a1792d647d6091e980754c428009ce1"
DAY_FILES=(
 "payoff_b_v8_metric_scale_pairs.csv",
 "payoff_b_v8_metric_scale_summary.csv",
 "payoff_b_v8_metric_scale_forecast_skill_summary.csv",
 "payoff_b_v8_metric_scale_forecast_value_exact_complete.csv",
 "payoff_b_v8_metric_scale_bird_rows.csv",
 "payoff_b_v8_metric_scale_bird_summary.csv",
 "payoff_b_v8_metric_scale_status.csv",
)


def sha(data:bytes)->str:
    return hashlib.sha256(data).hexdigest()


def gitsha(blob:bytes)->str:
    return hashlib.sha1(b"blob "+str(len(blob)).encode()+b"\0"+blob).hexdigest()


def single(directory:Path,name:str)->Path:
    candidates=[x for x in directory.rglob(name) if x.is_file()]
    if len(candidates)!=1:
        raise ValueError("Expected exactly one verified "+name)
    return candidates[0]


def add(root:Path,relative:str,blob:bytes,check_text=True)->None:
    dest=root/relative
    if Path(relative).is_absolute() or ".." in Path(relative).parts:
        raise ValueError("Unsafe review archive destination")
    if check_text:
        safe(blob.decode("utf-8"),relative)
    dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_bytes(blob)


def reproduction_command()->str:
    return """#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p outputs
cp data/source_input.rds outputs/amaral_final_frozen.rds
Rscript analysis/seasonal_v8_metric_scale_diagnostic.R
python3 -m scripts.audit_day_scale \
  --historical data/frozen_outputs/day_scale \
  --rerun outputs \
  --supplement supplementary/Table_S2_day_scale.md \
  --receipt outputs/day_scale_reproduction_receipt.json
"""


def assemble(base:Path,pdf_artifact:Path,day_outputs:Path,out:Path)->dict:
    if out.exists() and any(out.iterdir()):
        raise ValueError("Do not overwrite existing scientific review archive")
    raw=base.read_bytes()
    if sha(raw)!=BASE_ZIP_SHA:
        raise ValueError("Verified 2026-10-14 V8+deer science archive SHA changed")
    with zipfile.ZipFile(base) as z:
        items=z.namelist()
        if len(items)<40 or any(x.startswith("/") or ".." in Path(x).parts for x in items):
            raise ValueError("Invalid original V8/deer review archive path inventory")
        z.extractall(out)
    original_manifest=json.loads((out/"MANIFEST.json").read_text())
    if not original_manifest.get("mule_deer_replay_verified"):
        raise ValueError("Existing deer original source not verified")

    receipt=json.loads(single(day_outputs,"amnat_v4_posthoc_daily_evidence_receipt.json").read_text())
    if (receipt.get("status")!="ORIGINAL_V8_DAY_SCALE_POSTHOC_REEXECUTED_AND_SOURCE_MATCHED"
        or receipt.get("pairs")!=166
        or receipt.get("bird_rows")!=150
        or receipt.get("bird_unique_pairs")!=72
        or receipt.get("classification")!="POSTHOC_OUTCOME_INFORMED_ONLY"
        or receipt.get("rmse_change_to_bird_mismatch_direct_transfer_tested") is not False):
        raise ValueError("Original day-scale statistical output source not admitted")

    science=(ROOT/"analysis/movement_phenology/payoff_b_v8_metric_scale_diagnostic.R").read_bytes()
    if gitsha(science)!=DAY_SCRIPT_SHA:
        raise ValueError("Original historical posthoc R program blob changed")
    text=neutral(science.decode("utf-8"))
    add(out,"analysis/seasonal_v8_metric_scale_diagnostic.R",text.encode("utf-8"))

    old_audit=(ROOT/"scripts/audit_payoff_b_v8_day_scale_posthoc.py").read_text(encoding="utf-8")
    add(out,"scripts/audit_day_scale.py",neutral(old_audit).encode("utf-8"))
    add(out,"scripts/reproduce_day_scale.sh",reproduction_command().encode("utf-8"))
    # Record a source-reproducible *theoretical* derivation and deterministic
    # counterexamples as well as the published biological input data.
    # This code identifies no individual cue/perception or demographic fitness.
    theory=ROOT/"src/paper2_actionability_peak.py"
    theory_tests=ROOT/"tests/test_paper2_actionability_peak.py"
    for origin,target in (
        (theory,"src/paper2_actionability_peak.py"),
        (theory_tests,"tests/test_paper2_actionability_peak.py")
    ):
        if not origin.is_file():
            raise ValueError("Paper 2 mathematical source missing from reviewer archive")
        payload=origin.read_bytes()
        # Avoid a lexical false positive: "payoff_blocks" is a generic
        # Python test-function suffix but contains our banned "payoff_b"
        # project-token substring. Renaming the TEST, not its assertions,
        # preserves numerical/algorithmic verification.
        if target=="tests/test_paper2_actionability_peak.py":
            payload=payload.replace(
                b"test_no_positive_gross_payoff_blocks_witness_regime",
                b"test_no_positive_return_witness_regime"
            )
        add(out,target,payload)

    for file in DAY_FILES:
        p=single(day_outputs,file)
        raw=p.read_bytes()
        expected=receipt["original_vs_new_file_checksums"][file]["rerun_sha256"]
        if sha(raw)!=expected:
            raise ValueError("Day-scale R output SHA not proven from original day-scale receipt")
        target="data/frozen_outputs/day_scale/"+neutral(file)
        add(out,target,raw)

    supplement=(ROOT/"submission/AMNAT_V4_SUPPLEMENTARY_TABLE_S2_DAY_SCALE_20261014.md").read_text(encoding="utf-8")
    supplement=supplement.split("## Immutable provenance",1)[0].rstrip()+"\n"
    if "POST HOC" not in supplement or "2.132 to +3.184" not in supplement:
        raise ValueError("Posthoc table/corrected original source interval not retained")
    add(out,"supplementary/Table_S2_day_scale.md",neutral(supplement).encode("utf-8"))

    pdf_file=single(pdf_artifact,"Paper2_anonymous_real_observation_EDITORIAL_preview.pdf")
    pdf_receipt=json.loads(single(pdf_artifact,"PDF_SOURCE_PREFLIGHT_HOLD.json").read_text())
    if pdf_receipt.get("status")!="ANONYMOUS_EDITORIAL_PDF_PREFLIGHT_PASS_SUBMISSION_HOLD":
        raise ValueError("Latest manuscript PDF mechanical source preflight failed")
    cleaned=pdf_blind(pdf_file)
    import pymupdf
    with pymupdf.open(stream=cleaned,filetype="pdf") as pdf:
        text="\n".join(page.get_text() for page in pdf)
        for required in ("2.412","4.662","1.821","2.494","4.113",
                         "4.168","2.628","Supplementary Table"):
            if required not in text:
                raise ValueError("New daily forecast result absent in revised PDF: "+required)
        if len({x[0] for page in pdf for x in page.get_images(full=True)})!=4:
            raise ValueError("Four original source-grounded figure images missing")
        math_prose=" ".join(text.lower().split())
        if "threshold" not in math_prose or "additive intercept" not in math_prose:
            raise ValueError("Corrected general actionability optimum/phase-controller caveat absent in PDF")
        pdf_n=len(pdf)
    add(out,"manuscript/editorial_preview.pdf",cleaned,check_text=False)

    # The old full-page QC certificate belongs to the previous PDF version.
    old=out/"qc/PDF_39_PAGE_MECHANICAL_QC.json"
    if old.exists():
        old.unlink()
    from scripts.audit_amnat_v4_all_pdf_pages import audit_pdf
    page_qc=audit_pdf(out/"manuscript/editorial_preview.pdf",out.parent/"page_by_page_visual_previews")
    if (page_qc["status"]!="PDF_ALL_PAGE_MECHANICAL_PASS_HUMAN_VISUAL_HOLD"
        or page_qc["pages"]!=pdf_n):
        raise ValueError("New manuscript does not pass independent all-page PDF QC")
    add(out,"qc/PDF_ALL_PAGE_SOURCE_QC.json",(
      json.dumps(page_qc,indent=2,ensure_ascii=False)+"\n"
    ).encode())

    original_readme=(out/"README.md").read_text(encoding="utf-8")
    note="""\n## After-primary day-unit forecast diagnostic: exploratory only

New supplementary/Table_S2_day_scale.md reports the independently
reproduced *post hoc* comparison of signed correlation, destination
green-up SD, fitted residual RMSE, and source-informed leave-one-year-out
RMSE. That original diagnostic was designed AFTER the V8 registered
environment-correlation result was known, and does not refit that result.

The registered correlation transfer to bird mismatch remains NOT
SUPPORTED. A *separate* RMSE-change-to-bird-mismatch transfer was NOT
conducted; do not claim both transfer exposures fail from this table.

Additional offline reproduction:
    bash scripts/reproduce_day_scale.sh

The source values 0.2838 to 0.6528, target SD 2.412 to 4.662 days,
in-sample RMSE 1.821 to 2.494 days, and LOYO source RMSE 4.113 to
4.168 days distinguish standardized coupling, absolute uncertainty,
relative forecast skill, and realized biological timing. The cue
used here is statistical; bird access before departure was not observed.

The editorial manuscript PDF was rebuilt after this scientific
clarification. The general zero-cost actionability optimum (valid for
arbitrary initial cue values) and its threshold-only special case are
checked in src/paper2_actionability_peak.py and
tests/test_paper2_actionability_peak.py. The general formula must NOT
be replaced with the threshold-only logarithm. Run the mathematical
guards with Python pytest when preparing the reviewer submission.
This is NOT an author-approved journal submission.
"""
    add(out,"README.md",(original_readme+"\n"+note).encode())

    manifest=json.loads((out/"MANIFEST.json").read_text(encoding="utf-8"))
    manifest.update({
       "status":"V8_DEER_AND_DAY_SCALE_POSTHOC_SOURCE_VERIFIED_EDITORIAL_HOLD",
       "v8_registered_analysis_unchanged":True,
       "deer_published_source_result_unchanged":True,
       "day_scale_status":"HISTORICAL_POSTHOC_AND_HISTORICAL_OUTPUT_RERUN_MATCH",
       "day_scale_original_R_git_blob":DAY_SCRIPT_SHA,
       "day_scale_metric_to_bird_matching_direct_transfer_tested":False,
       "supplement_S2_included":True,
       "revised_pdf_sha256":sha(cleaned),
       "new_pdf_pages_mechanically_verified":pdf_n,
       "full_page_human_visual_approved":False,
       "anonymous_delivery_link_exists":False,
       "journal_submission_ready":False,
    })
    manifest["file_hashes"]={
        file.relative_to(out).as_posix():sha(file.read_bytes())
        for file in sorted(out.rglob("*")) if file.is_file()
        and file.relative_to(out).as_posix()!="MANIFEST.json"
    }
    add(out,"MANIFEST.json",(json.dumps(manifest,indent=2,sort_keys=True)+"\n").encode())

    # Text content/path anonymity is independently rechecked before packaging.
    for file in out.rglob("*"):
        if file.is_file():
            rel=file.relative_to(out).as_posix()
            safe(rel,"filename")
            if file.suffix.lower() in (".py",".r",".sh",".md",".json",".csv",".svg",".txt"):
                safe(file.read_text(encoding="utf-8"),rel)
    return {
       "status":"ANON_POSTHOC_DAY_SCALE_PAPER2_ARCHIVE_CONTENT_VERIFIED",
       "paper_pages":pdf_n,
       "pdf_sha256":sha(cleaned),
       "n_archive_files":len([file for file in out.rglob("*") if file.is_file()]),
       "source_original_day_diagnostic_sha":DAY_SCRIPT_SHA,
       "new_day_results_count":len(DAY_FILES),
       "original_reproducibility_preserved":True,
       "human_visual_review":False,
       "anonymous_external_deposit":False,
       "journal_submission_ready":False,
    }


def zip_deterministic(root:Path,dest:Path)->str:
    if dest.exists():
        raise ValueError("Refuse overwrite of original reviewer bundle")
    dest.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(dest,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for file in sorted(p for p in root.rglob("*") if p.is_file()):
            info=zipfile.ZipInfo(file.relative_to(root).as_posix(),date_time=(2026,10,14,0,0,0))
            info.create_system=3
            info.external_attr=(0o644&0xffff)<<16
            info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,file.read_bytes())
    return sha(dest.read_bytes())


def main()->None:
    p=argparse.ArgumentParser()
    p.add_argument("--base-zip",type=Path,required=True)
    p.add_argument("--paper",type=Path,required=True)
    p.add_argument("--day-scale",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--zip",type=Path,required=True)
    p.add_argument("--receipt",type=Path,required=True)
    a=p.parse_args()
    res=assemble(a.base_zip,a.paper,a.day_scale,a.out)
    res["inner_archive_sha256"]=zip_deterministic(a.out,a.zip)
    res["inner_archive_bytes"]=a.zip.stat().st_size
    a.receipt.parent.mkdir(parents=True,exist_ok=True)
    a.receipt.write_text(json.dumps(res,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps({k:res[k] for k in (
        "status","paper_pages","n_archive_files",
        "new_day_results_count","journal_submission_ready"
    )}))


if __name__=="__main__":
    main()
