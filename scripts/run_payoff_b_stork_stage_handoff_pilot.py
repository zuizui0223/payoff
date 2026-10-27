#!/usr/bin/env python3
"""Execute precommitted 53-season stork stage-handoff pilot without any outcome fit.

Contract: docs/PAYOFF_B_STORK_STAGE_PROPAGATION_PILOT_LOCK_20261019.md
Uses the *original* Jan-Apr, winter-referenced 20% and 80% checkpoints.
The newer Feb-May 91-season gate is a different estimand and is not used.

No GPS/animal IDs, daily locations, reproduction values or per-individual
results leave the temporary workflow directory.
"""
from __future__ import annotations

import argparse
import calendar
import csv
import json
import math
import random
import statistics
import tempfile
from collections import Counter, defaultdict
from pathlib import Path

from scripts.qc_public_movebank_stork_breeding_2018 import (
    FILES, DOI, download_cc0,
)
from scripts.qc_public_movebank_stork_gps_join_2018 import (
    download_gps,
)
from scripts.qc_public_movebank_stork_spring_progress_2018 import (
    extract_track_progress,
)

BOOT_B = 2500
PERM_B = 1000
BOOT_SEED = 20261019
MIN_SEASONS = 40
MIN_ANIMALS = 20
MIN_YEARS = 4
MIN_REPEATED_ANIMALS = 10


def read_eligibility_keys(breeding_file, reference_file):
    """Read only source IDs and years; *never* parse fledgling outcome values."""
    with Path(reference_file).open(encoding="utf-8-sig", newline="") as f:
        refs=list(csv.DictReader(f))
    ids=[(r.get("deployment-id") or "").strip() for r in refs]
    if not ids or "" in ids or len(ids)!=len(set(ids)):
        raise ValueError("Invalid/duplicate source reference IDs")
    with Path(breeding_file).open(encoding="utf-8-sig", newline="") as f:
        reader=csv.DictReader(f)
        if not {"id","Year"}.issubset(set(reader.fieldnames or [])):
            raise ValueError("Breeding source ID/year columns missing")
        pairs=[]
        for row in reader:
            ident, year=(row["id"] or "").strip(), (row["Year"] or "").strip()
            if ident not in ids or not year.isdecimal():
                raise ValueError("Unmatched source ID/year")
            pairs.append((ident,int(year)))
    if len(pairs)!=91 or len(pairs)!=len(set(pairs)):
        raise ValueError("Historical 91 original source ID/year gate changed")
    return refs,set(pairs)


def normalize_365(raw_doy, year):
    raw=int(raw_doy)
    if raw < 1 or raw > (366 if calendar.isleap(year) else 365):
        raise ValueError("Day-of-year outside original calendar")
    return raw - int(calendar.isleap(year) and raw > 60)


def admitted_rows(classified):
    """Reproduce EXACTLY original 53; source keys are never exported."""
    rows=[]
    for (ident,year), r in sorted(classified.items()):
        if r["status"]!="NORTHWARD_PROGRESS_OBSERVED":
            continue
        rawx=int(r["first_20_percent_doy"])
        rawy=int(r["first_80_percent_doy"])
        x=normalize_365(rawx,year)
        y=normalize_365(rawy,year)
        if not 0<=y-x<=80 or (rawy-rawx)!=(y-x):
            raise ValueError("Invalid stork March-April stage sequence")
        rows.append({
            "animal":ident,"year":year,
            "x":float(x),"y":float(y),
            "x_raw":float(rawx),"y_raw":float(rawy),
        })
    return rows


def _means(rows, key, group):
    values=defaultdict(list)
    for r in rows:
        values[r[group]].append(float(r[key]))
    return {k:statistics.mean(v) for k,v in values.items()}


def slope_group_fe(rows, *, x="x", y="y", group="year"):
    """OLS with intercept and group fixed effects via Frisch-Waugh demeaning."""
    if not rows:
        raise ValueError("empty regression")
    avgx=_means(rows,x,group)
    avgy=_means(rows,y,group)
    num=den=0.0
    for r in rows:
        dx=float(r[x])-avgx[r[group]]
        dy=float(r[y])-avgy[r[group]]
        num+=dx*dy
        den+=dx*dx
    if den<=1e-10 or not math.isfinite(den):
        raise ValueError("Singular fixed-effect stage regression")
    beta=num/den
    if not math.isfinite(beta):
        raise ValueError("Non-finite beta")
    return beta


def percentile(values, probability):
    v=sorted(float(x) for x in values)
    if not v:
        return None
    pos=(len(v)-1)*probability
    low=int(pos)
    w=pos-low
    return v[low]*(1-w)+v[min(low+1,len(v)-1)]*w


def percentiles(values):
    if not values:
        return None
    return {f"p{int(100*p):02d}":percentile(values,p)
            for p in (0,.025,.25,.5,.75,.975,1)}


def cluster_bootstrap(rows, seed=BOOT_SEED, replicates=BOOT_B):
    group=defaultdict(list)
    for r in rows:
        group[r["animal"]].append(r)
    animals=sorted(group)
    rng=random.Random(seed)
    betas=[]
    failed=0
    for _ in range(replicates):
        sample=[r for _animal in rng.choices(animals,k=len(animals))
                for r in group[_animal]]
        try:
            betas.append(slope_group_fe(sample))
        except ValueError:
            failed+=1
    if len(betas)<int(replicates*.95):
        raise ValueError("Insufficient estimable cluster-bootstrap replicates")
    return betas, failed


def shuffle_year_x(rows, seed=BOOT_SEED, replicates=PERM_B):
    by_year=defaultdict(list)
    for r in rows:
        by_year[r["year"]].append(r)
    rng=random.Random(seed+1)
    values=[]
    for _ in range(replicates):
        shuffled=[]
        for year in sorted(by_year):
            original=by_year[year]
            x=[r["x"] for r in original]
            rng.shuffle(x)
            shuffled.extend({**r,"x":val} for r,val in zip(original,x))
        try:
            values.append(slope_group_fe(shuffled))
        except ValueError:
            raise ValueError("Unexpected singular year-preserving shuffle")
    return values


def run_pilot(rows):
    n=len(rows)
    animals=len({r["animal"] for r in rows})
    years=sorted({r["year"] for r in rows})
    repeated=sum(v>=2 for v in Counter(r["animal"] for r in rows).values())
    result={
        "sample_seasons":n,"individuals":animals,"calendar_years":years,
        "repeated_individuals":repeated,
        "primary_design":"Y_80%_normalized_day ~ X_20%_normalized_day + year_FE",
        "bootstrap_replicates":BOOT_B,
        "bootstrap_seed":BOOT_SEED,
        "shuffled_within_year_replicates":PERM_B,
    }
    if n!=53 or animals!=27 or repeated!=15:
        result["status"]="NOT_ESTIMABLE_ORIGINAL_SAMPLE_IDENTITY_CHANGED"
        return result
    if n<MIN_SEASONS or animals<MIN_ANIMALS or len(years)<MIN_YEARS:
        result["status"]="NOT_ESTIMABLE_PREDECLARED_GATE"
        return result
    try:
        beta=slope_group_fe(rows)
        raw_beta=slope_group_fe(rows,x="x_raw",y="y_raw")
    except ValueError:
        result["status"]="NOT_ESTIMABLE_SINGULAR_YEAR_FE"
        return result
    boots,invalid=cluster_bootstrap(rows)
    ci=(percentile(boots,.025),percentile(boots,.975))
    perms=shuffle_year_x(rows)
    loo=[]
    for individual in sorted({r["animal"] for r in rows}):
        loo.append(slope_group_fe([r for r in rows if r["animal"]!=individual]))
    subset=[r for r in rows
            if Counter(x["animal"] for x in rows)[r["animal"]]>=2]
    within=(slope_group_fe(subset,group="animal")
            if repeated>=MIN_REPEATED_ANIMALS else None)
    yearcounts=Counter(r["year"] for r in rows)
    yearvalues={}
    for yr in years:
        yy=[r for r in rows if r["year"]==yr]
        yearvalues[str(yr)]={
            "seasons":len(yy),
            "first20_normalized_doy_quartiles":{
                "q25":percentile([r["x"] for r in yy],.25),
                "median":percentile([r["x"] for r in yy],.5),
                "q75":percentile([r["x"] for r in yy],.75),
            },
            "first80_normalized_doy_quartiles":{
                "q25":percentile([r["y"] for r in yy],.25),
                "median":percentile([r["y"] for r in yy],.5),
                "q75":percentile([r["y"] for r in yy],.75),
            },
        }
    result.update(
        status="SUPPORTED_DESCRIPTIVE_COMPRESSION"
               if beta<1 and ci[1]<1 else "NOT_SUPPORTED",
        beta_year_FE=beta,
        interval_on_entry_slope=beta-1.0,
        stage_timing_retention=beta,
        bootstrap_95pct_CI=list(ci),
        valid_bootstrap_replicates=len(boots),
        invalid_bootstrap_replicates=invalid,
        repeated_animals_within_slope=within,
        leave_one_animal_out_slope_range=[min(loo),max(loo)],
        year_preserving_shuffle_beta_quantiles=percentiles(perms),
        raw_DOY_year_FE_beta=raw_beta,
        leap_calendar_correction_difference=beta-raw_beta,
        admitted_seasons_by_year=dict(sorted(yearcounts.items())),
        admitted_year_summary=yearvalues,
        no_animal_ID_or_coordinate_in_output=True,
        not_active_control_identification=True,
        cue_information_unobserved=True,
        true_breeding_arrival_unobserved=True,
        no_fecundity_or_fitness_fit=True,
        prior_V7_V8_registered_outcomes_unchanged=True,
    )
    return result


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--out",type=Path,
        default=Path("outputs/payoff_b_stork_stage_handoff_pilot.json"))
    args=p.parse_args()
    receipt={
        "schema":"payoff_b_stork_53_season_year_FE_handoff_v1",
        "registration":"docs/PAYOFF_B_STORK_STAGE_PROPAGATION_PILOT_LOCK_20261019.md",
        "source_doi":DOI,
        "source_class":"ORIGINAL_JAN_APR_STORK_PROGRESS",
        "model_role":"DESCRIPTIVE_PILOT_NOT_FITNESS_OR_INFORMATION_EFFECT",
    }
    try:
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)
            originals={
                name:path/(name+(".txt" if name=="readme" else ".csv"))
                for name in FILES
            }
            for name,file in originals.items():
                download_cc0(name,file)
            refs,pairs=read_eligibility_keys(originals["breeding"],
                                             originals["reference"])
            gps=path/"gps.csv"
            receipt["original_gps_checksum"]=download_gps(gps)
            classified,_,_=extract_track_progress(gps,refs,pairs)
            rows=admitted_rows(classified)
            receipt["result"]=run_pilot(rows)
            receipt["processing_status"]="COMPLETE"
    except (OSError,ValueError,TypeError) as exc:
        receipt["processing_status"]="SOURCE_OR_MODEL_FAILURE"
        receipt["error"]=type(exc).__name__+": "+str(exc)[:400]
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(receipt,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps(receipt,indent=2,ensure_ascii=False))
    if receipt["processing_status"]!="COMPLETE":
        raise SystemExit("Original source or fixed stork pilot failed")
    if receipt["result"]["status"].startswith("NOT_ESTIMABLE"):
        raise SystemExit("Original pre-committed 53 season pilot not estimable")


if __name__=="__main__":
    main()
