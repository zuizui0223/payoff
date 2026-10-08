#!/usr/bin/env python3
"""PAYOFF-B: source-only goose stage calendar versus compensation audit.

No breeding-success values, resources, energy variables, or
fitness regressions are read in this analysis.

The source is pinned original author CSV, matching published Dryad v5
SHA256 after normalizing LF->CRLF line endings.
"""

import csv
import hashlib
import io
import json
import math
import random
import statistics
from collections import defaultdict
from pathlib import Path
from urllib.request import Request, urlopen

COMMIT = "2171bcd36bf37022c8716e15c0f75412103b0f3f"
URL = (
    "https://raw.githubusercontent.com/aschindler23/"
    "Schindler_etal_2024_ProcB/" + COMMIT + "/spring_data.csv"
)
DRYAD_SHA = "9ef98e6b5e979e93476ed076a018db13bdf03aab6dcc5ca728b5fd866e79c1bd"
BOOT = 4000
SEED = 20261008


def read_verified_records(raw: bytes):
    normalized = raw.replace(b"\r\n", b"\n").replace(b"\n", b"\r\n")
    if hashlib.sha256(normalized).hexdigest() != DRYAD_SHA:
        raise ValueError("author CSV does not match Dryad v5 SHA256")
    reader = csv.DictReader(io.StringIO(raw.decode("utf-8-sig")))
    required = {"id", "year", "sub_season", "first_day"}
    if not required.issubset(set(reader.fieldnames or [])):
        raise ValueError("source lacks required movement-time columns")
    seen = {}
    for r in reader:
        try:
            bird = int(r["id"])
            year = int(r["year"])
            stage = int(r["sub_season"])
            day = float(r["first_day"])
        except (ValueError, TypeError) as ex:
            raise ValueError("invalid movement-timing source code") from ex
        if not 1 <= year <= 5 or not 1 <= stage <= 6 or not 1 <= day <= 366:
            raise ValueError("out-of-bounds source timing")
        key = (bird, year, stage)
        if key in seen:
            raise ValueError("duplicate individual/year/stage")
        seen[key] = day
    if len(seen) != 642:
        raise ValueError("published author-data stage count changed")
    groups = defaultdict(dict)
    for (bird, year, stage), day in seen.items():
        groups[(bird, year)][stage] = day
    if len(groups) != 107 or len({b for b, _ in groups}) != 49:
        raise ValueError("source bird-year and individual count drift")
    output = []
    for (bird, year), timing in sorted(groups.items()):
        if set(timing) != set(range(1, 7)):
            raise ValueError("not all six annotated stages are present")
        if any(timing[k+1] <= timing[k] for k in range(1, 6)):
            # Strictly positive stage intervals are required for the
            # predeclared decision-stage duration definition.
            raise ValueError("nonpositive or out-of-order stage interval")
        a, d, b = timing[3], timing[5], timing[6]
        output.append({
            "bird": bird,
            "year": year,
            "arrive_staging": a,
            "exit_staging": d,
            "begin_breeding": b,
            "staging_duration": d-a,
            "post_staging_duration": b-d,
        })
    return output


def within_slope(rows, xkey, ykey):
    byyear = defaultdict(list)
    for row in rows:
        byyear[row["year"]].append(row)
    xy = 0.0
    xx = 0.0
    for yr in byyear.values():
        xm = statistics.mean(z[xkey] for z in yr)
        ym = statistics.mean(z[ykey] for z in yr)
        xy += sum((z[xkey]-xm)*(z[ykey]-ym) for z in yr)
        xx += sum((z[xkey]-xm)**2 for z in yr)
    return xy / xx if xx > 1e-12 else None


def within_ratio(rows, source="arrive_staging", target="exit_staging"):
    byyear = defaultdict(list)
    for row in rows:
        byyear[row["year"]].append(row)
    ss0, ss1 = 0.0, 0.0
    for yr in byyear.values():
        a = statistics.mean(z[source] for z in yr)
        d = statistics.mean(z[target] for z in yr)
        ss0 += sum((z[source]-a)**2 for z in yr)
        ss1 += sum((z[target]-d)**2 for z in yr)
    return math.sqrt(ss1 / ss0) if ss0 > 0 else None


def percentile(x, p):
    z = sorted(x)
    j = (len(z) - 1) * p
    left = int(j)
    right = min(left+1, len(z)-1)
    return z[left]*(1-(j-left))+z[right]*(j-left)


def run(raw: bytes):
    rows = read_verified_records(raw)
    beta_exit = within_slope(rows,"arrive_staging","exit_staging")
    beta_stay = within_slope(rows,"arrive_staging","staging_duration")
    if beta_exit is None or beta_stay is None or abs(beta_stay-(beta_exit-1.0))>1e-10:
        raise ArithmeticError("same-sample exact accounting identity failed")
    ratio = within_ratio(rows)
    bybird = defaultdict(list)
    byyear = defaultdict(list)
    for r in rows:
        bybird[r["bird"]].append(r)
        byyear[r["year"]].append(r)
    birds = sorted(bybird)
    rng = random.Random(SEED)
    boot = []
    for _ in range(BOOT):
        resampled = []
        for id_ in (rng.choice(birds) for __ in range(len(birds))):
            resampled.extend(bybird[id_])
        b = within_slope(resampled,"arrive_staging","exit_staging")
        if b is not None and math.isfinite(b):
            boot.append(b)
    if len(boot) < BOOT*0.95:
        raise ValueError("cluster bootstrap insufficient support")
    perm = []
    for _ in range(BOOT):
        shuffled = []
        for year, yr in byyear.items():
            dat = [dict(z) for z in yr]
            dvals = [z["exit_staging"] for z in yr]
            rng.shuffle(dvals)
            for z, d in zip(dat, dvals):
                z["exit_staging"] = d
            shuffled.extend(dat)
        p = within_slope(shuffled,"arrive_staging","exit_staging")
        if p is not None:
            perm.append(p)
    if len(perm) < BOOT*0.95:
        raise ValueError("permutation insufficient support")
    year_detail = []
    for yr, zs in sorted(byyear.items()):
        year_detail.append({
            "year_code": yr,
            "bird_years": len(zs),
            "staging_arrival_mean_doy": statistics.mean(z["arrive_staging"] for z in zs),
            "staging_exit_mean_doy": statistics.mean(z["exit_staging"] for z in zs),
            "staging_arrival_sd": statistics.stdev(z["arrive_staging"] for z in zs) if len(zs)>1 else None,
            "staging_exit_sd": statistics.stdev(z["exit_staging"] for z in zs) if len(zs)>1 else None,
            "median_staging_duration": statistics.median(z["staging_duration"] for z in zs),
        })
    leaving = []
    for y in sorted(byyear):
        subset=[r for r in rows if r["year"] != y]
        leaving.append({"omitted_year":y,"within_year_exit_on_arrival":within_slope(subset,"arrive_staging","exit_staging")})
    report = {
        "status":"POST_PR318_SOURCE_ONLY_CALENDAR_ASSOCIATION; NO FITNESS_MODEL",
        "source_commit":COMMIT,
        "source_sha256_normalized_crlf":DRYAD_SHA,
        "bird_years":len(rows),
        "birds":len(birds),
        "years":len(byyear),
        "inference":"descriptive not causal",
        "timing_definition":"Stage3 start of Iceland staging; Stage5 start second flight; Stage6 start early breeding",
        "beta_stage5_exit_on_stage3_arrival_within_year":beta_exit,
        "beta_staging_duration_on_stage3_arrival_within_year":beta_stay,
        "exact_slope_identity_pass":True,
        "pooled_within_year_exit_vs_arrival_sd_ratio":ratio,
        "bird_cluster_bootstrap_95_exit_on_arrival":[percentile(boot,.025),percentile(boot,.975)],
        "bird_cluster_bootstrap_draws":len(boot),
        "within_year_departure_permutation_two_sided_p_description_only":(1+sum(abs(x)>=abs(beta_exit) for x in perm))/(len(perm)+1),
        "within_year_permutation_95":[percentile(perm,.025),percentile(perm,.975)],
        "calendar_year_detail":year_detail,
        "leave_one_year_out":leaving,
        "breeding_outcome_read":False,
        "energy_feeding_outcomes_read":False,
        "cue_perception_identified":False,
        "active_feedback_identified":False,
        "fitness_cost_identified":False
    }
    return report


def synthetic_test():
    # D=y-constant regardless of arrival: staging duration compensation
    # appears with beta=-1 even though the exit schedule has NO cue use.
    rows=[]
    for y in range(1,4):
        for x in (83,91,102,119,136):
            d=160+y
            rows.append({"year":y,"arrive_staging":x,"exit_staging":d,"staging_duration":d-x})
    assert abs(within_slope(rows,"arrive_staging","exit_staging"))<1e-12
    assert abs(within_slope(rows,"arrive_staging","staging_duration")+1)<1e-12
    assert within_ratio(rows)==0
    print("PAYOFF_B_GOOSE_STAGE_CALENDAR_SYNTHETIC_PASS")


if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument("--self-test",action="store_true")
    parser.add_argument("--output",default="outputs/payoff_b_goose_staging_calendar_null_result.json")
    args=parser.parse_args()
    if args.self_test:
        synthetic_test()
    else:
        request=Request(URL,headers={"User-Agent":"PAYOFF-B/source-only-audit","Accept":"text/csv"})
        with urlopen(request,timeout=30) as response:
            data=response.read(200000)
        result=run(data)
        path=Path(args.output)
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8")
        print("PAYOFF_B_GOOSE_STAGING_CALENDAR_SOURCE_RESULT")
        print(json.dumps(result,sort_keys=True))
        print("NO BREEDING, FEEDING, OR ENERGY OUTCOME OPENED")
