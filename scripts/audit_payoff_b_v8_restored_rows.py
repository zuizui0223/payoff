#!/usr/bin/env python3
"""Independent arithmetic + provenance audit of ORIGINAL FROZEN V8 ROW OUTPUTS.

Input files MUST be restored unmodified from the named 2026-10-05 GitHub
Actions artifacts; the script never selects alternative data/windows, fits
new ecological hypotheses, or promotes a frozen null result.

This recomputes estimates FROM the archived row/bootstrap files, not a
complete new raw-R-data resimulation. Only a separate controlled R replay can
independently reconstruct the original bootstrap draws from final.rds.
"""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import json
import math
import statistics
import subprocess
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MANIFEST=ROOT/"data/payoff_b_v8_row_archive_provenance_20261013.json"

FILES={
 "environment_pairs":("environment","payoff_b_v8_primary_unique_pairs.csv"),
 "environment_species":("environment","payoff_b_v8_primary_species_means.csv"),
 "environment_incidence":("environment","payoff_b_v8_primary_pair_species_incidence.csv"),
 "environment_bootstrap":("environment","payoff_b_v8_primary_bootstrap.csv"),
 "transfer_rows":("transfer","payoff_b_v8_transfer_primary_rows.csv"),
 "transfer_bootstrap":("transfer","payoff_b_v8_transfer_primary_bootstrap.csv"),
 "structural_rows":("structural","payoff_b_v8_transfer_structural_null_rows.csv"),
 "structural_bootstrap":("structural","payoff_b_v8_transfer_structural_null_bootstrap.csv"),
 "structural_permutations":("structural","payoff_b_v8_transfer_arrival_permutation.csv"),
 "structural_status":("structural","payoff_b_v8_transfer_structural_null_status.csv"),
 "structural_summary":("structural","payoff_b_v8_transfer_structural_null_summary.csv"),
}


def fail(message):
    raise ValueError(message)


def close(actual, expected, tolerance, what):
    if not math.isfinite(actual) or abs(actual-expected)>tolerance:
        fail(f"{what}: {actual} vs frozen {expected}, tolerance {tolerance}")


def require_fields(rows, cols, kind):
    if not rows:
        fail(kind+": empty original analysis output")
    missing=set(cols)-set(rows[0])
    if missing:
        fail(kind+": missing source fields "+",".join(sorted(missing)))


def numeric(row,name):
    try:
        v=float(row[name])
    except (KeyError,ValueError,TypeError):
        fail(f"Bad numeric {name}")
    if not math.isfinite(v):
        fail("Nonfinite source numeric "+name)
    return v


def load_rows(path):
    with path.open("r",encoding="utf-8-sig",newline="") as f:
        z=list(csv.DictReader(f))
    if not z or not z[0]:
        fail("Empty CSV "+str(path))
    return z


def q_type7(values,proportion):
    """Default R quantile() interpolation type 7 for finite sorted replicates."""
    if not values:
        fail("Empty bootstrap series")
    ordered=sorted(values)
    where=(len(ordered)-1)*proportion
    low=math.floor(where)
    high=math.ceil(where)
    return ordered[low]*(high-where)+ordered[high]*(where-low) if high!=low else ordered[low]


def quantile_ci(values):
    return [q_type7(values,0.025),q_type7(values,0.975)]


def weighted_slope(rows,ycol,xcol="z_delta_rho"):
    """Independently recompute standard species-equal weighted OLS slope."""
    counts=collections.Counter(row["species"] for row in rows)
    weights=[1.0/counts[row["species"]] for row in rows]
    xx=[numeric(row,xcol) for row in rows]
    yy=[numeric(row,ycol) for row in rows]
    total=sum(weights)
    mx=sum(w*x for w,x in zip(weights,xx))/total
    my=sum(w*y for w,y in zip(weights,yy))/total
    numerator=sum(w*(x-mx)*(y-my) for w,x,y in zip(weights,xx,yy))
    denominator=sum(w*(x-mx)**2 for w,x in zip(weights,xx))
    if denominator<=0:
        fail("Degenerate weighted x variance")
    return numerator/denominator


def input_receipt(src: Path, expected_git_sha: str, expected_size: int):
    if src.stat().st_size!=expected_size:
        fail("Frozen source RDS file byte-size drift")
    git_sha=subprocess.check_output(["git","hash-object",str(src)],text=True).strip()
    if git_sha!=expected_git_sha:
        fail(f"Original final.rds git blob differs from pinned source: {git_sha}")
    return {
        "source_git_blob_sha":git_sha,
        "sha256":hashlib.sha256(src.read_bytes()).hexdigest(),
        "size_bytes":src.stat().st_size,
        "source_content_checked":True,
        "scientific_R_full_replay":False,
    }


def audit(artifact_root: Path, manifest: dict, source_rds: Path|None=None)->dict:
    if manifest.get("status")!="PRE_RECOVERY_MANIFEST_LOCKED_NO_NEW_OUTCOMES":
        fail("Frozen pre-recovery manifest status drift")
    stored={}
    hashes={}
    for role,(subdir,name) in FILES.items():
        path=artifact_root/subdir/name
        if not path.is_file():
            fail(f"Original frozen artifact missing file: {role}: {path}")
        raw=path.read_bytes()
        hashes[role]={
            "relative_path":str(Path(subdir)/name),
            "sha256":hashlib.sha256(raw).hexdigest(),
            "bytes":len(raw),
        }
        stored[role]=load_rows(path)

    frozen=manifest["registered_result_contract"]
    env=stored["environment_pairs"]
    envsp=stored["environment_species"]
    inci=stored["environment_incidence"]
    assert frozen["environment"]["unique_pairs"]==166
    require_fields(env,("pair_key","rho_early","rho_late","delta_rho"),"environment pairs")
    require_fields(envsp,("species","delta_rho"),"environment species")
    require_fields(inci,("species","pair_key"),"incidence")
    if len(env)!=166 or len({r["pair_key"] for r in env})!=166:
        fail("Environment unit differs from 166 unique source-target pairs")
    if len(envsp)!=28 or len({r["species"] for r in envsp})!=28:
        fail("Species count changed from registered 28")
    if any(r["pair_key"] not in {v["pair_key"] for v in env} for r in inci):
        fail("Species incidence has unregistered environmental pair")
    for row in env:
        close(numeric(row,"rho_late")-numeric(row,"rho_early"),numeric(row,"delta_rho"),
              1e-9,"environment delta identity")
        if max(abs(numeric(row,"rho_early")),abs(numeric(row,"rho_late")))>1.00000001:
            fail("Impossible Pearson rho")
    env_mean=statistics.mean(numeric(r,"delta_rho") for r in env)
    species_mean=statistics.mean(numeric(r,"delta_rho") for r in envsp)
    close(env_mean,frozen["environment"]["pair_mean_delta_rho"],0.00011,"environment pair mean")
    close(species_mean,frozen["environment"]["equal_species_mean_delta_rho"],0.00011,
          "environment species mean")
    eb=stored["environment_bootstrap"]
    require_fields(eb,("pair_mean","equal_species_mean"),"environment bootstrap")
    if len(eb)!=10000:
        fail("Environmental 10,000 bootstraps not restored")
    environment_ci=quantile_ci([numeric(r,"pair_mean") for r in eb])
    env_species_ci=quantile_ci([numeric(r,"equal_species_mean") for r in eb])
    for i in range(2):
        close(environment_ci[i],frozen["environment"]["pair_ci95"][i],0.00015,
              "environment pair bootstrap CI")
        close(env_species_ci[i],frozen["environment"]["equal_species_ci95"][i],0.00015,
              "environment species bootstrap CI")

    tr=stored["transfer_rows"]
    require_fields(tr,("species","pair_key","target_cell","delta_mismatch",
                       "z_delta_rho","delta_rho"),"transfer rows")
    if len(tr)!=150 or len(set(x["pair_key"] for x in tr))!=72 or len(set(x["species"] for x in tr))!=22:
        fail("Transfer unit differs from frozen 150 rows / 72 pairs / 22 species")
    beta=weighted_slope(tr,"delta_mismatch")
    close(beta,frozen["transfer"]["beta"],0.0000002,"weighted transfer beta")
    tb=stored["transfer_bootstrap"]
    require_fields(tb,("beta_transfer",),"transfer bootstrap")
    vals=[numeric(r,"beta_transfer") for r in tb if r.get("beta_transfer") not in ("","NA","NaN")]
    if len(tb)!=10000 or len(vals)<9500:
        fail("Missing 10,000 registered transfer bootstrap draws")
    tci=quantile_ci(vals)
    for i in range(2):
        close(tci[i],frozen["transfer"]["ci95"][i],0.00015,"transfer bootstrap CI")

    st=stored["structural_rows"]
    require_fields(st,("species","pair_key","target_cell","z_delta_rho",
                       "delta_mismatch","delta_pseudo_mismatch"),"structural rows")
    if len(st)!=150 or len({r["pair_key"] for r in st})!=72 or len({r["species"] for r in st})!=22:
        fail("Structural null sample drift")
    ob=weighted_slope(st,"delta_mismatch")
    null=weighted_slope(st,"delta_pseudo_mismatch")
    inc=ob-null
    close(ob,beta,0.0000002,"structural observed beta vs primary")
    close(null,frozen["structural"]["fixed_arrival_beta"],0.00011,"fixed-arrival null beta")
    close(inc,frozen["structural"]["bird_increment_beta"],0.00011,"bird-specific increment")
    sb=stored["structural_bootstrap"]
    require_fields(sb,("a2_bird_increment",),"structural 10,000 draws")
    if len(sb)!=10000:
        fail("Not 10,000 original structural-null draws")
    ci_increment=quantile_ci([numeric(r,"a2_bird_increment")
                             for r in sb if r.get("a2_bird_increment") not in ("","NA","NaN")])
    for i in range(2):
        close(ci_increment[i],frozen["structural"]["bird_increment_ci95"][i],0.00015,
              "bird increment bootstrap CI")
    perm=stored["structural_permutations"]
    require_fields(perm,("beta",),"structural 2,000 arrival permutations")
    if len(perm)!=2000:
        fail("Not 2,000 frozen arrival permutations")
    permvals=[numeric(r,"beta") for r in perm]
    perm_ci=quantile_ci(permvals)
    median=q_type7(permvals,0.5)
    close(median,frozen["structural"]["permutation_median"],0.00015,"permutation median")
    for i in range(2):
        close(perm_ci[i],frozen["structural"]["permutation_95_interval"][i],0.00015,
              "permutation central interval")
    status=stored["structural_status"]
    require_fields(status,("structural_explained","bird_increment_detected"),"structural status")
    if len(status)!=1 or status[0]["structural_explained"]!="YES" or status[0]["bird_increment_detected"]!="NO":
        fail("Frozen structural gate unexpectedly altered")

    raw_verified=None
    if source_rds is not None:
        raw_verified=input_receipt(source_rds,manifest["source"]["blob_sha1_git"],
                                   manifest["source"]["source_size_bytes"])
    return {
        "status":"FROZEN_V8_ROW_LEVEL_ARTIFACTS_RESTORED_AND_ARITHMETIC_VERIFIED",
        "original_results_unchanged":True,
        "recomputed_new_hypothesis":False,
        "full_raw_R_bootstrap_replay":False,
        "individual_perception_or_demographic_fitness_identified":False,
        "source_rds":raw_verified,
        "original_artifact_metadata":manifest["historical_artifacts"],
        "archived_csv_file_sha256":hashes,
        "environment":{
            "unique_spatial_pairs":len(env),
            "species":len(envsp),
            "mean_delta_rho":env_mean,
            "ci95_pair_bootstrap":environment_ci,
            "species_exposure_mean":species_mean,
            "ci95_species_exposure":env_species_ci,
            "registered_degradation_supported":False,
        },
        "transfer":{
            "species_target_rows":len(tr),
            "unique_pairs":len({r["pair_key"] for r in tr}),
            "species":len({r["species"] for r in tr}),
            "beta":beta,
            "bootstrap_ci95":tci,
            "registered_negative_transfer_supported":False,
        },
        "structural_null":{
            "fixed_arrival_beta":null,
            "observed_minus_fixed_arrival":inc,
            "bird_increment_ci95":ci_increment,
            "permutation_median":median,
            "permutation_interval_95":perm_ci,
            "bird_specific_increment_detected":False,
        },
        "remaining_gates":[
            "Independently rerun the original frozen R estimators from the pinned final.rds, if needed",
            "Source/processed row-data redistribution rights and final reviewer anonymity require independent assessment",
            "Citation and figure/source crosswalk to anonymous manuscript PDF requires final author inspection",
        ],
        "submission_ready":False,
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--artifacts",type=Path,required=True)
    p.add_argument("--source-rds",type=Path)
    p.add_argument("--manifest",type=Path,default=MANIFEST)
    p.add_argument("--receipt",type=Path,required=True)
    args=p.parse_args()
    result=audit(args.artifacts,json.loads(args.manifest.read_text(encoding="utf-8")),
                 args.source_rds)
    args.receipt.parent.mkdir(parents=True,exist_ok=True)
    args.receipt.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",
                            encoding="utf-8")
    print(json.dumps({"status":result["status"],
          "environment":result["environment"],
          "transfer":result["transfer"],
          "structural_null":result["structural_null"],
          "submission_ready":False}))
if __name__=="__main__":
    main()
