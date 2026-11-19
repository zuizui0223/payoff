#!/usr/bin/env python3
"""Prospective external GFS issue-time gate for 2019–2021 bird decisions.

Only historical provider metadata has been inspected. No GRIB, source bird
timestamps or biological outcomes are downloaded or modelled by this script.
Hypothetical record validator used to prevent future-issued/hindcast leakage.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime,timedelta,timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
CONTRACT=ROOT/"data/payoff_b_ruppel_GFS_2019_2021_forecast_source_gate_20261119.json"
REQUIRED={
    "decision_utc",
    "forecast_issue_utc",
    "forecast_valid_utc",
    "original_forecast_product",
    "original_operational_archive",
    "original_GRIB2_file_sha256",
}
DATE_HOURS=[0,6,12,18]


def utc_instant(value:str)->datetime:
    if not isinstance(value,str) or not value:
        raise ValueError("Original timestamp is missing")
    try:
        result=datetime.fromisoformat(value.replace("Z","+00:00"))
    except ValueError as e:
        raise ValueError("ISO UTC original source timestamp not parseable") from e
    if result.tzinfo is None or result.utcoffset()!=timedelta(0):
        raise ValueError("Only offset-aware UTC source timestamps admitted")
    return result.astimezone(timezone.utc)


def admission(manifest:dict)->dict:
    if manifest.get("status")!=(
      "PROVIDER_METADATA_2019_2021_AVAILABLE_SUBSET_LOGIN_REQUIRED_FORECAST_BYTES_NOT_ADMITTED"
    ):
        raise ValueError("Original historical forecast source metadata status changed")
    source=manifest["external_forecast_archive"]
    gate=manifest["chronology_gate"]
    if (source["dataset_id"]!="d084001"
        or source["DOI"]!="10.5065/D65D8PWK"
        or source["published_historical_years_covered"]!=[2019,2020,2021]
        or source["nominal_initializations_UTC_hours"]!=DATE_HOURS
        or gate["target_hours_after_decision_primary"]!=6
        or gate["target_alignment_tolerance_hours"]!=1.5
        or gate["sensitivities_target_hours_after_decision"]!=[3,12]):
        raise ValueError("Locked original forecast-source/timing contract drift")
    if any(bool(source[key]) for key in (
        "user_login_or_terms_accepted","subset_request_performed",
        "original_operational_GRIB2_bytes_fetched",
        "original_file_sha256_checked",
        "exact_requested_u10_v10_cloud_cover_fields_confirmed_in_original_GRIB2",
        "actual_source_issue_timestamp_verified",
    )):
        raise ValueError("Forecast source access cannot be asserted without original bytes")
    return {
        "status":"2019_2021_OPERATIONAL_FORECAST_ARCHIVE_EXISTS_METADATA_ONLY",
        "registered_archive_DOI":source["DOI"],
        "dataset_id":source["dataset_id"],
        "original_forecast_issued_values_obtained":False,
        "original_bird_times_opened_in_this_gate":False,
        "bird_cue_vs_landing_biological_effect_fitted":False,
        "original_source_subset_login_required":True,
        "future_user_authorized_GRIB2_admission_needed":True,
        "theory_q_wait_D_eff_r_t_measured":False,
    }


def test_future_issue_time_record(record:dict, primary_horizon_hours:int=6)->dict:
    """Evaluate a *future authenticated original source* record, no animal fit.

    Return flags without echoing individual original dates or coordinates.
    """
    if set(record)!=REQUIRED:
        raise ValueError("Unexpected source record fields, or missing forecast provenance")
    decision=utc_instant(record["decision_utc"])
    issued=utc_instant(record["forecast_issue_utc"])
    valid=utc_instant(record["forecast_valid_utc"])
    if decision.year not in (2019,2020,2021):
        raise ValueError("Bird decision outside source-verified study years")
    if record["original_operational_archive"]!="d084001":
        raise ValueError("External source is not original historical GFS archive")
    if record["original_forecast_product"]!="operational_issue_time_forecast":
        raise ValueError("Hindcast/reanalysis/analysis not eligible")
    digest=record["original_GRIB2_file_sha256"]
    if not isinstance(digest,str) or len(digest)!=64 or any(
        c not in "0123456789abcdef" for c in digest
    ):
        raise ValueError("Invalid source GRIB digest")
    if issued.hour not in DATE_HOURS or issued.minute!=0 or issued.second!=0:
        raise ValueError("Unexpected operational source initialization time")
    before=issued<=decision-timedelta(hours=1)
    future=valid>decision
    forward=valid>issued
    aligned=abs(
        (valid-decision).total_seconds()/3600-primary_horizon_hours
    )<=1.5
    return {
        "issued_at_least_1h_predecision":before,
        "valid_after_decision":future,
        "positive_model_forecast_lead":forward,
        "issue_time_UTC_registered":True,
        "eligible_future_cue_by_issue_time_UTC_only":before and future and forward and aligned,
        "original_forecast_GRIB_digest_source_claimed_not_external_verified":True,
        "decision_to_target_near_primary_plus6h":aligned,
        "raw_animal_ID_date_weather_rows_emitted":False,
        "animal_subjective_access_verified":False,
        "biological_effect_fitted":False,
    }


def main()->None:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--manifest",type=Path,default=CONTRACT)
    p.add_argument("--output",required=True,type=Path)
    opts=p.parse_args()
    original=json.loads(opts.manifest.read_text(encoding="utf-8"))
    out=admission(original)
    opts.output.parent.mkdir(parents=True,exist_ok=True)
    opts.output.write_text(json.dumps(out,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps(out,ensure_ascii=False,sort_keys=True))


if __name__=="__main__":
    main()
