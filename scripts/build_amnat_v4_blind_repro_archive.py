#!/usr/bin/env python3
"""Assemble an internal source-checked, content-blinded V8 Paper 2 review ZIP.

The ZIP's text is anonymized. Public release and the external double-blind
delivery channel remain separate author/journal responsibilities.
"""
from __future__ import annotations
import argparse,hashlib,json,re,zipfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SOURCE_SHA="f1c9e63a377bb96152c573081e7c482cfe49ebc3"
SOURCE_SIZE=7250107
FORBIDDEN=("zuizui0223","PAYOFF-B","payoff_b","ZHANG RUIQI","rachelzhang0223")
EMAIL=re.compile(r"(?i)[\w.+-]+@[\w.-]+\.[a-z]{2,}")
R_ORIG=(
 "analysis/movement_phenology/payoff_b_v8_primary.R",
 "analysis/movement_phenology/payoff_b_v8_downstream_transfer_primary.R",
 "analysis/movement_phenology/payoff_b_v8_transfer_structural_null_audit.R"
)
CONTRACT_ORIG=(
 "docs/PAYOFF_B_V8_DOWNSTREAM_TRANSFER_CONTRACT_20261005.md",
 "docs/PAYOFF_B_V8_TRANSFER_STRUCTURAL_NULL_CONTRACT_20261005.md"
)
ORIGINAL_DATA={
 "environment":["primary_unique_pairs","primary_species_means",
                "primary_pair_species_incidence","primary_bootstrap","primary_summary"],
 "transfer":["transfer_primary_rows","transfer_primary_bootstrap","transfer_primary_summary"],
 "structural":["transfer_structural_null_rows","transfer_structural_null_bootstrap",
               "transfer_structural_null_status","transfer_structural_null_summary",
               "transfer_arrival_permutation"]
}
FIGURES=("figure1_summary.svg","figure2_summary.svg",
         "figure3_summary.svg","figure4_summary.svg")

def digest(blob):
    return hashlib.sha256(blob).hexdigest()
def git_blob(blob):
    return hashlib.sha1(b"blob "+str(len(blob)).encode()+b"\0"+blob).hexdigest()
def neutral(txt):
    return (txt.replace("analysis/movement_phenology/","analysis/")
            .replace("payoff_b_v8_","seasonal_v8_")
            .replace("PAYOFF_B_V8_","SEASONAL_V8_")
            .replace("PAYOFF-B","Seasonal tracking")
            .replace("PAYOFF_B","SEASONAL_TRACKING"))
def safe(txt,name):
    if any(token.casefold() in txt.casefold() for token in FORBIDDEN):
        raise ValueError("Identifying project/owner string in "+name)
    if EMAIL.search(txt):
        raise ValueError("Email address in "+name)
def add(root,relative,blob,text=True):
    if text:safe(blob.decode("utf-8"),relative)
    if Path(relative).is_absolute() or ".." in Path(relative).parts:
        raise ValueError("Unsafe archive path")
    path=root/relative
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_bytes(blob)
    return {"sha256":digest(blob),"bytes":len(blob)}
def one(root,name):
    files=list(root.rglob(name))
    if len(files)!=1:raise ValueError(f"Expected unique {name}, found {len(files)}")
    return files[0]
def pdf_blind(path):
    import pymupdf
    with pymupdf.open(path) as d:
        text="\n".join(p.get_text() for p in d)
        safe(text,"PDF rendered text")
        if len(d)<10 or "0.369" not in text or "0.062" not in text:
            raise ValueError("Incomplete scientific manuscript PDF")
        if len([p for p in d if p.get_images()])<4:
            raise ValueError("Four images not embedded")
        for p in d:
            for link in p.get_links():
                if any(tok.casefold() in (link.get("uri") or "").casefold() for tok in FORBIDDEN):
                    raise ValueError("Identifying hyperlink within manuscript")
        d.set_metadata({"title":"Environmental predictability alone does not determine seasonal tracking",
                        "author":"","subject":"","keywords":"","creator":"","producer":""})
        return d.tobytes(garbage=4,deflate=True)
def fixed_zip(root,target):
    if target.exists():raise ValueError("Refuse overwrite of ZIP")
    target.parent.mkdir(parents=True,exist_ok=True)
    with zipfile.ZipFile(target,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for f in sorted(p for p in root.rglob("*") if p.is_file()):
            info=zipfile.ZipInfo(f.relative_to(root).as_posix(),date_time=(2026,10,13,0,0,0))
            info.create_system=3
            info.external_attr=(0o644&0xffff)<<16
            info.compress_type=zipfile.ZIP_DEFLATED
            z.writestr(info,f.read_bytes())
def readme():
    return """# Anonymous Paper 2 reviewer data and code candidate

This is an internally generated content-blinded package, not a submitted
manuscript or a deposited anonymous reviewer link. The data and scientific
claims are frozen: no results are refitted post hoc.

The dataset is from Amaral et al., Shifting gears in a shifting climate:
birds adjust migration speed in response to spring vegetation green-up,
Dryad DOI 10.5061/dryad.ttdz08m6w. Source repository commit:
62c58d77c2028bd863dfe3697b0d9cf29ceaeab0.
The original final.rds has Git blob digest
f1c9e63a377bb96152c573081e7c482cfe49ebc3 and size 7,250,107 bytes.
Dryad research data are CC0; credit the original researchers. This
package does not assign an open-source license to unpublished analysis
software; final author approval of code reuse is required.

Offline reproduction requires R, Python 3 and Git installed. From the ZIP
root, run: bash scripts/reproduce.sh
This copies the bundled source to the frozen input cache, runs the original
science with presentation-only neutralized filenames and log messages, and
checks sample units, weighted slope, original bootstrap and permutation
confidence intervals against the frozen values.

Archive contents:
- data/source_input.rds original publicly distributed data
- data/frozen_outputs/environment, transfer, structural: original
  processed rows, bootstrap outputs and signed structural-null results
- analysis/*.R: original science with only project-identifying names,
  comments and output filenames renamed
- docs/*.md: frozen contracts
- scripts/verify_science.py and scripts/reproduce.sh
- figures/*.svg and manuscript/editorial_preview.pdf: evidence-labelled
  scientific figures and editorial manuscript, NOT final journal versions.

Interpretation: 166 distinct environmental pairs from 28 bird species,
mean signed correlation change +0.3690 (95% CI +0.2984 to +0.4365);
150 species-target rows using 72 unique environmental pairs from 22
species; registered mismatch transfer +0.06244 (CI -0.01411 to +0.13635).
Both prespecified negative predictions were not supported. A fixed-arrival
structural-null slope +0.04742 reproduced the apparent positive pattern.
Neither animal-perceived forecast quality nor demographic fitness is shown.

Original numerical estimates are independently reproducible using the
pinned raw source and the actual original R code. This ZIP's neutrally
renamed R scripts are separately regression-tested before reviewer release.
All-page figure/typesetting inspection, journal citation style, final
software permissions, human author approval and a separate anonymous
data/code sharing endpoint remain outside this package.
"""
def replay_script():
    return """#!/bin/sh
set -eu
cd "$(dirname "$0")/.."
mkdir -p outputs/verified/environment outputs/verified/transfer outputs/verified/structural
cp data/source_input.rds outputs/amaral_final_frozen.rds
Rscript analysis/seasonal_v8_transfer_structural_null_audit.R
cp outputs/seasonal_v8_primary_{unique_pairs,species_means,pair_species_incidence,bootstrap}.csv outputs/verified/environment/
cp outputs/seasonal_v8_transfer_primary_{rows,bootstrap}.csv outputs/verified/transfer/
cp outputs/seasonal_v8_transfer_structural_null_{rows,bootstrap,status,summary}.csv outputs/verified/structural/
cp outputs/seasonal_v8_transfer_arrival_permutation.csv outputs/verified/structural/
python3 -m scripts.verify_science --artifacts outputs/verified --source-rds data/source_input.rds --manifest data/lock.json --receipt outputs/verified/result.json
"""
def build(original,source,paper,out,zippath):
    if out.exists() and any(out.iterdir()):raise ValueError("Nonempty archive directory")
    raw=source.read_bytes()
    if len(raw)!=SOURCE_SIZE or git_blob(raw)!=SOURCE_SHA:
        raise ValueError("Published input SHA or size drift")
    hashes={}; originals={}
    for name in R_ORIG+CONTRACT_ORIG:
        data=(ROOT/name).read_bytes()
        originals[name]=digest(data)
        new=neutral(name)
        if new.startswith("analysis/movement_phenology/"):
            raise ValueError("Original author-identifying script path remains")
        hashes[new]=add(out,new,neutral(data.decode("utf-8")).encode())
    hashes["data/source_input.rds"]=add(out,"data/source_input.rds",raw,False)
    for role,terms in ORIGINAL_DATA.items():
        for term in terms:
            old="payoff_b_v8_"+term+".csv"
            new="seasonal_v8_"+term+".csv"
            hashes["data/frozen_outputs/"+role+"/"+new]=add(
                out,"data/frozen_outputs/"+role+"/"+new,(original/role/old).read_bytes())
    frozen=json.loads((ROOT/"data/payoff_b_v8_row_archive_provenance_20261013.json").read_text())
    lock={"status":frozen["status"],"source":{
          "blob_sha1_git":SOURCE_SHA,"source_size_bytes":SOURCE_SIZE,
          "data_doi":"10.5061/dryad.ttdz08m6w"},
          "registered_result_contract":frozen["registered_result_contract"],
          "historical_artifacts":[]}
    hashes["data/lock.json"]=add(out,"data/lock.json",(json.dumps(lock,sort_keys=True,indent=2)+"\n").encode())
    validator=neutral((ROOT/"scripts/audit_payoff_b_v8_restored_rows.py").read_text())
    validator=validator.replace("data/seasonal_v8_row_archive_provenance_20261013.json","data/lock.json")
    if "data/lock.json" not in validator:
        raise ValueError("Scientific validator was not pointed at anonymous lock")
    hashes["scripts/verify_science.py"]=add(out,"scripts/verify_science.py",validator.encode())
    hashes["scripts/reproduce.sh"]=add(out,"scripts/reproduce.sh",replay_script().encode())
    hashes["README.md"]=add(out,"README.md",readme().encode())
    hashes["manuscript/editorial_preview.pdf"]=add(
        out,"manuscript/editorial_preview.pdf",
        pdf_blind(one(paper,"Paper2_anonymous_real_observation_EDITORIAL_preview.pdf")),False)
    figure_receipt=json.loads(one(paper,"combined_figure_source_receipt.json").read_text())
    if (figure_receipt.get("status")!="REAL_POINT_F2_F3_AND_FROZEN_F1_F4_EDITORIAL_PREVIEW_PASS"
        or figure_receipt.get("f2_observed_unique_spatial_pairs")!=166
        or figure_receipt.get("f3_observed_species_target_rows")!=150):
        raise ValueError("Original-point source figure authorization missing")
    for i,name in enumerate(FIGURES,1):
        data=one(paper,name).read_bytes()
        if digest(data)!=figure_receipt["figure_sha256"][name]:
            raise ValueError("Figure content SHA256 drift")
        hashes["figures/figure"+str(i)+".svg"]=add(out,"figures/figure"+str(i)+".svg",data)
    status={"status":"ANON_SCIENCE_ARCHIVE_CANDIDATE_REPLAY_PENDING",
            "file_hashes":hashes,"raw_source_repackaged":True,
            "data_cc0_source_doi":"10.5061/dryad.ttdz08m6w",
            "science_code_labels_neutralized":True,
            "anonymized_delivery_link":False,"journal_submission_ready":False}
    add(out,"MANIFEST.json",(json.dumps(status,indent=2,sort_keys=True)+"\n").encode())
    fixed_zip(out,zippath)
    return {"status":status["status"],"zip_sha256":digest(zippath.read_bytes()),
            "file_count":len(hashes)+1,"original_scientific_script_sha256_INTERNAL":originals,
            "source_rds_sha256":digest(raw),"human_visual_approved":False,
            "anonymous_reviewer_delivery":False,"submission_ready":False}
def main():
    p=argparse.ArgumentParser()
    for option in ("original","source-rds","paper-root","out","zip","receipt"):
        p.add_argument("--"+option,type=Path,required=True)
    a=p.parse_args()
    receipt=build(a.original,a.source_rds,a.paper_root,a.out,a.zip)
    a.receipt.parent.mkdir(parents=True,exist_ok=True)
    a.receipt.write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps({"status":receipt["status"],
                      "file_count":receipt["file_count"],
                      "submission_ready":False}))
if __name__=="__main__":
    main()
