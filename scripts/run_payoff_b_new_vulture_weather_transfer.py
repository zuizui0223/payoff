#!/usr/bin/env python3
"""Unopened Egyptian-vulture source test of predeclared stork solar pattern.

The direction was locked AFTER historical stork observations but BEFORE
opening this source's NASA POWER outcomes: stork had less previous-day
surface shortwave radiation (relative to previous week) on later-moving
than continuing-stay stationary risk-days. A same-sign finding would
replicate a *physical weather association only*, not PAYOFF-B cue use.

Uses public CC0 original GPS checked by fixed MD5, 1859 observed at-risk
stationary source opportunities and 192 original 0.5-degree month-year
NASA POWER daily weather batches. Endangered-bird positions, animal IDs,
source cells and original timestamps are NEVER exported.
"""
from __future__ import annotations

import argparse,json,tempfile
from collections import Counter
from concurrent.futures import ThreadPoolExecutor,as_completed
from pathlib import Path

from scripts.qc_payoff_b_unopened_gps_source import SOURCES
from scripts.qc_public_movebank_crossguild import download_verified
from scripts.qc_payoff_b_predecision_candidates import daily_source_positions
from scripts.qc_payoff_b_complete_stationary_riskset import collect
from scripts.plan_payoff_b_batch_weather_requests import plan_batch_queries
from scripts.run_payoff_b_full_riskday_daily_weather import (
    batch_key,download_batch,event_prior_weather,grid_cell,
    calculate_contrast
)
from scripts.audit_payoff_b_weather_block_dependence import (
    complete_matched_strata,estimate_from_strata,block_sensitivity
)

SOURCE=SOURCES["egyptian_vulture"]
EXPECTED=(1859,33,1454,232,140,30,192,18,19)
MIN_OVERLAP_CASE_DAYS=10
MIN_OVERLAP_STRATA=5
MIN_COMPLETE_WEATHER_FRACTION=.95
SOLAR_FIELD="ALLSKY_SFC_SW_DWN_anomaly"
PREOPENED_HYPOTHESIS_DIRECTION="NEGATIVE_AS_IN_PRIOR_STORK_SOURCE"
VAR_ORDER=("T2M_anomaly","WS10M_anomaly","V10M_anomaly",SOLAR_FIELD)


def validate_counts(rows,counts,plan):
    vals=tuple(counts[k] for k in (
        "all_at_risk_stationary_days","NORTHWARD_CANDIDATE",
        "STAYED_TWO_DAYS","OTHER_MOVEMENT","CENSORED",
        "deduplicated_frozen_cases",
    ))+(
        plan["unique_grid_calendar_months"],
        plan["grid_months_with_both_northward_and_stay_observations"],
        plan["northward_case_days_in_overlap_gridmonths"],
    )
    if vals!=EXPECTED or len(rows)!=EXPECTED[0]:
        raise ValueError("Original 1859-riskday and 192-gridmonth source changed")
    if vals[7]<MIN_OVERLAP_STRATA or vals[8]<MIN_OVERLAP_CASE_DAYS:
        raise ValueError("Original source overlap gate no longer passes")


def describe_transfer(effect, fine_block):
    observed=effect[SOLAR_FIELD]
    ci=fine_block.get("bootstrap_interval_95pct_descriptive") or {}
    solar_ci=ci.get(SOLAR_FIELD)
    if observed is None:
        return {"status":"NOT_ESTIMABLE"}
    return {
        "prespecified_stork_solar_direction":PREOPENED_HYPOTHESIS_DIRECTION,
        "observed_vulture_solar_source_contrast_w_m2":observed,
        "descriptive_same_sign_as_stork":observed<0,
        "source_fine_gridmonth_block_ci_excludes_zero_in_negative_direction":
            bool(solar_ci and solar_ci[1]<0),
        "fine_gridmonth_95pct_descriptive_interval":solar_ci,
        "classification":"SOURCE_ASSOCIATION_REPLICATION_ONLY",
        "source_weather_replication_is_Payoff_B_information_causality":False
    }


def run(fget=download_batch):
    with tempfile.TemporaryDirectory() as td:
        path=Path(td)/"public_CC0_GPS.csv"
        integrity=download_verified(SOURCE,path)
        groups,counters,idcol=daily_source_positions(path,SOURCE["taxon"])
        risk,counts,by_month,by_year=collect(groups)
        plan=plan_batch_queries(risk)
        validate_counts(risk,counts,plan)
        batches=sorted({batch_key(day,site) for _,day,site,_ in risk})
        weather={}
        fails=Counter()
        with ThreadPoolExecutor(max_workers=3) as pool:
            futures={pool.submit(fget,k):k for k in batches}
            for fut in as_completed(futures):
                key=futures[fut]
                try:weather[key]=fut.result()
                except Exception as e:fails[type(e).__name__]+=1
        valid=Counter()
        rows=[]
        for (tax,animal,year),day,site,label in risk:
            src=weather.get(batch_key(day,site))
            v=event_prior_weather(src,day) if src is not None else None
            if v is None:
                valid[label+"_MISSING_WEATHER"]+=1
                continue
            valid[label]+=1
            if label in ("NORTHWARD_CANDIDATE","STAYED_TWO_DAYS"):
                rows.append((animal,day,grid_cell(site),label,v))
        if any(valid[label] < .95*counts[label]
               for label in ("NORTHWARD_CANDIDATE","STAYED_TWO_DAYS")):
            return {"status":"NOT_ESTIMABLE_SOURCE_WEATHER_COVERAGE",
                    "source_counts":dict(counts),"valid":dict(valid),
                    "weather_failures":dict(fails)}
        raw=[(SOURCE["taxon"],animal,day.year) for animal,day,_,_,_ in rows]
        original=calculate_contrast([(identity,day,cell,label,weather)
                        for identity,day,cell,label,weather in rows])
        strata,cases=complete_matched_strata(rows)
        fine=estimate_from_strata(strata)
        if (cases["matched_strata_count"]!=18 or
            cases["case_risk_days_in_matched_strata"]!=19):
            raise ValueError("Original accepted weather overlap changed")
        for var in VAR_ORDER:
            a=fine["case_weighted_difference"][var]
            b=original["grid_year_month_adjusted_case_weighted_descriptive_difference"][var]
            if abs(a-b)>1e-8:raise ValueError("Independent weather calculations disagree")
        block_results={
            scale:block_sensitivity(strata,scale,draws=3000,seed=20261022)
            for scale in ("grid_half_degree","weather_block_2_degree",
                          "weather_episode_year_month")
        }
        within,within_summary=complete_matched_strata(rows,within_identity=True)
        return {
            "status":"NEW_TAXON_SOURCE_WEATHER_TRANSFER_DESCRIPTIVE_COMPLETE",
            "original_doi":SOURCE["doi"],
            "original_paper":SOURCE["paper"],
            "original_study_id":SOURCE["published_study_id"],
            "source_taxon":SOURCE["taxon"],
            "original_file_integrity":integrity,
            "source_risk_days":len(risk),
            "source_later_gps_labels":dict(sorted(counts.items())),
            "source_weather_complete_labels":dict(sorted(valid.items())),
            "API_batches_requested":len(batches),
            "API_failures":dict(sorted(fails.items())),
            "original_overlap_geometry":plan,
            "estimated_source_contrasts_original":{
                "unadjusted":original["source_group_mean_case_minus_stay"],
                "fine_gridmonth_case_weighted":
                    fine["case_weighted_difference"],
                "fine_gridmonth_overlap_strata":cases["matched_strata_count"],
                "case_days_in_gridmonth_overlap":cases["case_risk_days_in_matched_strata"],
            },
            "prespecified_solar_source_replication":describe_transfer(
                fine["case_weighted_difference"],block_results["grid_half_degree"]),
            "descriptive_shared_weather_block_uncertainty":block_results,
            "within_same_bird_gridmonth_geometry":within_summary,
            "within_same_bird_descriptive":{
                "case_weighted_weather_contrasts":
                    estimate_from_strata(within)["case_weighted_difference"]
                    if within_summary["matched_strata_count"]>=10 and
                       within_summary["distinct_case_animals_with_instrumental_overlap"]>=10
                    else None,
                "if_not_available":"NOT_ESTIMABLE_FEWER_THAN_10_INDEPENDENT_ANIMAL_IDENTITIES"
            },
            "prior_stork_data_reused_in_effect_fitting":False,
            "source_environmental_forecast_use_measured":False,
            "independent_true_departure_stages_verified":False,
            "fitness_or_recourse_measured":False,
            "sensitive_original_IDs_GPS_positions_event_dates_exported":False,
        }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--out",type=Path,
                   default=Path("outputs/payoff_b_new_vulture_transfer"))
    args=p.parse_args()
    record={
      "schema":"payoff_b_unopened_soaring_vulture_solar_association_transfer_20261022",
      "preopening_lock":"docs/PAYOFF_B_NEW_VULTURE_SOLAR_TRANSFER_LOCK_20261022.md",
      "experimental_status":"NONRANDOMIZED_INDEPENDENT_TAXON_EXPLORATORY_TRANSFER",
    }
    try:record["result"]=run()
    except (OSError,ValueError,TypeError) as e:
        record["result"]={"status":"SOURCE_OR_WEATHER_TRANSFER_GATE_FAILED",
                          "error":type(e).__name__+": "+str(e)[:280]}
    args.out.mkdir(parents=True,exist_ok=True)
    (args.out/"egyptian_vulture.json").write_text(
        json.dumps(record,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(record,ensure_ascii=False,indent=2))
    if record["result"]["status"]!="NEW_TAXON_SOURCE_WEATHER_TRANSFER_DESCRIPTIVE_COMPLETE":
        raise SystemExit("Vulture source transfer not estimable")

if __name__=="__main__":main()
