#!/usr/bin/env python3
"""Censoring-only null for observational PAYOFF-B stage-timing slopes.

Pure synthetic data, NO original animal observations or behavior. Shows that
beta(T80 ~ T20) < 1 can arise solely by conditioning Y on the end of a fixed
observational spring window even with X independent of stage duration W.

Not a calibrated null for specific tracked birds, not a test of the frozen
stork result, and not a substitute for actual stage/cue measurements.
"""
from __future__ import annotations
import argparse, json, math, random
from pathlib import Path

SEED=20261019
DRAWS=250000
X_MIN=61.0
X_MAX=106.0
W_MIN=10.0
W_MAX=45.0
RIGHT_EDGE=120.0

def stats(values):
    n,sx,sy,sxx,sxy=values
    if n<3:
        raise ValueError("Not enough synthetic selected observations")
    denominator=sxx-sx*sx/n
    if denominator<=1e-8:
        raise ValueError("Singular synthetic timing slope")
    return (sxy-sx*sy/n)/denominator

def simulate(seed=SEED,draws=DRAWS):
    if draws<1000:
        raise ValueError("Too few synthetic draws")
    rng=random.Random(seed)
    all_vals=[0.0]*5
    visible=[0.0]*5
    for _ in range(draws):
        x=X_MIN+(X_MAX-X_MIN)*rng.random()
        w=W_MIN+(W_MAX-W_MIN)*rng.random()
        y=x+w
        for sums in ([all_vals,visible] if y<=RIGHT_EDGE else [all_vals]):
            sums[0]+=1
            sums[1]+=x
            sums[2]+=y
            sums[3]+=x*x
            sums[4]+=x*y
    b_uncensored=stats(all_vals)
    b_windowed=stats(visible)
    return {
        "type":"SYNTHETIC_STRUCTURAL_NEGATIVE_CONTROL_NOT_EMPIRICAL",
        "model":"T80=T20+W; independent uniform T20 and W",
        "draws":draws,
        "seed":seed,
        "T20_uniform_days":[X_MIN,X_MAX],
        "W_uniform_days":[W_MIN,W_MAX],
        "right_censoring_condition":"T80 <= 120",
        "retained_draws":int(visible[0]),
        "retention_fraction":visible[0]/all_vals[0],
        "uncensored_stage_retention_slope":b_uncensored,
        "window_conditioned_stage_retention_slope":b_windowed,
        "unmeasured_behavioral_feedback_in_simulation":True,
        "original_tracking_fitted":False,
        "does_not_calibrate_specific_data_sources":True,
        "scientific_conclusion":"calendar censoring alone can generate a beta below one",
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,
                   default=Path("outputs/payoff_b_stage_timing_censoring_null.json"))
    args=p.parse_args()
    z=simulate()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(z,indent=2)+"\n")
    print(json.dumps(z,indent=2))
if __name__=="__main__":
    main()
