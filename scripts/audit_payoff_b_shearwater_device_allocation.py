#!/usr/bin/env python3
"""Shearwater source allocation vs GPS capture, not a navigation effect.

Uses only already verified public source aggregates, original paper's
9/9/9 GPS assignments and 5 additional Argos assignments in olfactory arm.
No GPS fixes or original subject identifiers are touched or exported.
"""
from __future__ import annotations
import argparse, json
from math import comb
from pathlib import Path

GROUPS = ("control","magnetic_disruption","olfactory_deprivation")
REFERENCE = (9,9,14)
GPS_EQUIPPED = (9,9,9)
ORIGINAL_GPS = (8,9,6)
ORIGINAL_ARGOS = (0,0,5)
DOI = "10.5441/001/1.tc76g560"

def exact_three_arm(sizes, captured):
    """Conditional three-arm probability-ordering test, no treatment causality."""
    total=sum(captured)
    den=comb(sum(sizes),total)
    observed=1
    for n,k in zip(sizes,captured):observed*=comb(n,k)
    mass=extreme=states=0
    for i in range(sizes[0]+1):
        for j in range(sizes[1]+1):
            k=total-i-j
            if not 0<=k<=sizes[2]:continue
            v=comb(sizes[0],i)*comb(sizes[1],j)*comb(sizes[2],k)
            mass+=v
            extreme+=v if v<=observed else 0
            states+=1
    if mass!=den:raise ValueError("Exact conditional distribution not normalized")
    return {"two_sided_conditional_probability":extreme/den,"feasible_tables":states}

def fisher_two_sided(t_n,t_k,c_n,c_k):
    total=t_k+c_k
    den=comb(t_n+c_n,t_n)
    target=comb(total,t_k)*comb(t_n+c_n-total,t_n-t_k)
    mass=0
    for x in range(max(0,t_n-(t_n+c_n-total)),min(t_n,total)+1):
        v=comb(total,x)*comb(t_n+c_n-total,t_n-x)
        if v<=target:mass+=v
    return mass/den

def run(receipt):
    if receipt["original_source_doi"]!=DOI or not receipt["GPS_source_gate_passed"]:
        raise ValueError("Unverified or wrong source")
    src=receipt["subject_capture_by_sensor_and_group"]
    if tuple(receipt["public_reference_groups"][g] for g in GROUPS)!=REFERENCE:
        raise ValueError("Treatment denominator changed")
    gps=tuple(src[g]["GPS_subjects"] for g in GROUPS)
    argos=tuple(src[g]["Argos_subjects"] for g in GROUPS)
    if gps!=ORIGINAL_GPS or argos!=ORIGINAL_ARGOS:
        raise ValueError("Original treatment-specific source capture changed")
    for g in GROUPS:
        if src[g]["both_sensors_same_subject"]!=0:
            raise ValueError("Sensor subject overlap changed")
    equip=GPS_EQUIPPED
    pct=[gps[i]/equip[i] for i in range(3)]
    gpstotal=[gps[i]/REFERENCE[i] for i in range(3)]
    if sum(gps)!=23 or sum(argos)!=5:raise ValueError("Original observed subjects changed")
    return {
      "schema":"payoff_b_shearwater_assignment_adjusted_GPS_capture_v1",
      "original_source_doi":DOI,
      "original_reference_subjects":sum(REFERENCE),
      "GPS_equipped_by_original_publication":dict(zip(GROUPS,equip)),
      "GPS_valid_by_archived_source":dict(zip(GROUPS,gps)),
      "Argos_assigned_by_original_publication":dict(zip(GROUPS,ORIGINAL_ARGOS)),
      "GPS_capture_fraction_among_GPS_equipped":dict(zip(GROUPS,pct)),
      "GPS_capture_fraction_among_all_treated":dict(zip(GROUPS,gpstotal)),
      "GPS_equipped_only_three_arm_exact":exact_three_arm(equip,gps),
      "olfactory_vs_other_GPS_equipped_Fisher_two_sided":fisher_two_sided(
          equip[2],gps[2],equip[0]+equip[1],gps[0]+gps[1]),
      "all_treated_GPS_yes_no_three_arm_exact_but_design_confounding":
          exact_three_arm(REFERENCE,gps),
      "missing_binary_GPS_outcome_arm_mean_bound_width":{
          g:(REFERENCE[i]-gps[i])/REFERENCE[i] for i,g in enumerate(GROUPS)},
      "olfactory_minus_control_GPS_outcome_difference_bound_width":
          (REFERENCE[2]-gps[2])/REFERENCE[2]+(REFERENCE[0]-gps[0])/REFERENCE[0],
      "experimental_effect_on_navigation_identified":False,
      "assignment_randomization_verified_here":False,
      "Argos_and_GPS_are_comparable_hourly_traces":False,
      "original_animal_identifiers_or_locations_exported":False,
      "classification":"POST_SOURCE_SENSOR_ALLOCATION_DIAGNOSTIC_NOT_CAUSAL",
    }

def main():
    a=argparse.ArgumentParser()
    a.add_argument("--input",type=Path,default=Path(
       "data/payoff_b_shearwater_experiment_sensor_coverage_20261023.json"))
    a.add_argument("--output",type=Path,default=Path(
       "outputs/payoff_b_shearwater_device_allocation.json"))
    x=a.parse_args()
    result=run(json.loads(x.input.read_text(encoding="utf-8")))
    x.output.parent.mkdir(parents=True,exist_ok=True)
    x.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(result,indent=2,ensure_ascii=False))

if __name__=="__main__":main()
