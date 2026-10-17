"""Reproducible algebra and source-integrity proof audit for Paper 2 S4.

Pure Python standard library; no natural data or new fitted parameters.
Run from reviewer ZIP with: python -m scripts.verify_theory_math --out qc/S4_THEORY_MATH_GUARD.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

from src.paper2_actionability_peak import (
    ActionabilityPeak,
    linear_phase_expectation,
    noisy_cue_phase_variance,
    symmetric_threshold_peak,
    two_actor_mismatch,
)

MODEL=Path("src/paper2_actionability_peak.py")
PROOF=Path("supplementary/Mathematical_Note_S4.md")


def _close(a:float,b:float,what:str,tol=1e-10)->None:
    if abs(a-b)>tol or not all(math.isfinite(z) for z in (a,b)):
        raise ValueError("Theory source identity failure "+what+": "+str(a)+" vs "+str(b))


def audit(model_path:Path=MODEL,proof_path:Path=PROOF)->dict:
    source=model_path.read_bytes()
    proof=proof_path.read_bytes()
    readable=proof.decode("utf-8")
    for needed in ("threshold-normalized", "A_\\infty", "posterior",
                   "noisy cue", "variance", "no finite waiting time"):
        if needed.casefold() not in readable.casefold():
            raise ValueError("Incomplete S4 mathematical proof: "+needed)
    witness=ActionabilityPeak(.5,.5,1,1,2,1)
    w=witness.optimum()
    if w["regime"]!="INTERIOR_CHECKPOINT":
        raise ValueError("Threshold-normalized witness lost")
    _close(w["optimal_wait_time"],math.log(2),"threshold witness")
    _close(symmetric_threshold_peak(1,1),math.log(2),"short formula")
    _close(witness.cue_accuracy(w["optimal_wait_time"]),.75,"cue at optimum")

    nonstandard=ActionabilityPeak(.55,.45,1,1,10,5).optimum()
    _close(nonstandard["optimal_wait_time"],math.log(1.8),"general interior")
    instant=ActionabilityPeak(.6,.3,1,1,10,3).optimum()
    _close(instant["optimal_wait_time"],0,"immediate decision")
    zero=ActionabilityPeak(.5,.1,1,1,4,3).optimum()
    if zero["regime"]!="NO_POSITIVE_INFORMATION_RETURN":
        raise ValueError("Zero-payoff outside action misidentified")
    for m in (w, nonstandard, instant, zero):
        if m["optimal_net_value"] < 0:
            raise ValueError("Optional net benefit violated")

    phase=linear_phase_expectation(3,1.5,.8,.7,.4,.1)
    _close(phase["direct"],phase["decomposed"],"phase intercept")
    if abs(phase["intercept"])<1e-5:
        raise ValueError("Phase intercept incorrectly suppressed")

    variance=noisy_cue_phase_variance(2,2,.9,.7,.03)
    _close(variance["actual_p_next"],.9129,"variance formula")
    _close(variance["retention_squared_times_p"],.68445,"wrong reduced variance comparator")
    _close(variance["difference"],.22845,"noisy cue variance gap")
    _close(variance["noise_and_estimation_gap"],.22845,"gap decomposition")

    checked=0
    for n in range(7):
        for e1,e2 in ((1,1),(-2,3),(.2,-.7)):
            for lam1,lam2 in ((.2,.8),(-.6,.3),(1,1)):
                got=two_actor_mismatch(e1,e2,lam1,lam2,n)
                _close(got["direct"],got["decomposed"],"two-actor identity")
                checked+=1
    return {
        "status":"PAPER2_S4_PIECEWISE_AND_NOISY_CONTROLLER_SOURCE_PROOF_PASS",
        "source_model_sha256":hashlib.sha256(source).hexdigest(),
        "supplement_S4_sha256":hashlib.sha256(proof).hexdigest(),
        "threshold_optimum":w["optimal_wait_time"],
        "general_interior_optimum":nonstandard["optimal_wait_time"],
        "immediate_optimum":instant["optimal_wait_time"],
        "zero_information_action_chosen":zero["regime"],
        "noisy_phase_variance_gap":variance["difference"],
        "two_actor_exact_cases":checked,
        "natural_animal_forecast_estimated":False,
        "ecological_fitness_identified":False,
        "journal_submission_ready":False,
    }


def main()->None:
    parser=argparse.ArgumentParser()
    parser.add_argument("--out",type=Path,required=True)
    args=parser.parse_args()
    value=audit()
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(value,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({k:value[k] for k in ("status","threshold_optimum",
              "general_interior_optimum","noisy_phase_variance_gap",
              "journal_submission_ready")}))


if __name__=="__main__":
    main()
