"""Source-gated Monitoring Sites 1000 / resource / weather outcome bridge.

An observation-count series is not automatically abundance, a greenness
index is not biomass, and a first-sighting date is not a demand curve.
No ecological effect is fitted by this module.
"""
from __future__ import annotations
import datetime as dt
import math

class EvidenceNotAdmitted(ValueError):
    pass

def validate_site_year_bundle(bundle: dict) -> dict:
    required=("site_id","year","monitoring","climate","resource","consumer")
    if any(k not in bundle for k in required):
        raise EvidenceNotAdmitted("Missing site/year or one evidence channel")
    site=str(bundle["site_id"]).strip()
    year=int(bundle["year"])
    if not site or not 1900<=year<=2100:
        raise EvidenceNotAdmitted("Invalid site or year")
    checks={}
    for channel in ("monitoring","climate","resource","consumer"):
        row=bundle[channel]
        if row.get("site_id")!=site or row.get("year")!=year:
            raise EvidenceNotAdmitted("Unmatched site/year in "+channel)
        if not str(row.get("source_id","")).strip():
            raise EvidenceNotAdmitted("Missing original source in "+channel)
    monitoring=bundle["monitoring"]
    if monitoring.get("effort_standardized") is not True:
        raise EvidenceNotAdmitted("Monitoring observation effort not standardized")
    if monitoring.get("quantity_kind") not in ("abundance_index","occupancy","breeding_success"):
        raise EvidenceNotAdmitted("Monitoring count not an admitted population outcome")
    if monitoring.get("observation_process_verified") is not True:
        raise EvidenceNotAdmitted("Monitoring detection process not verified")
    checks["monitoring_outcome"]=True
    climate=bundle["climate"]
    if climate.get("station_crosswalk_verified") is not True or climate.get("quality_homogeneity_verified") is not True:
        raise EvidenceNotAdmitted("Weather station/quality/homogeneity not verified")
    if climate.get("window_fixed_before_outcome") is not True:
        raise EvidenceNotAdmitted("Outcome-dependent climate window leakage")
    if not climate.get("climate_variables"):
        raise EvidenceNotAdmitted("No measured climate variables")
    checks["measured_climate"]=True
    resource=bundle["resource"]
    if resource.get("quantity_kind")!="biomass_g_m2":
        raise EvidenceNotAdmitted("NDVI/greenness/cover is not measured resource biomass")
    if resource.get("independent_from_outcome") is not True or resource.get("sampling_effort_verified") is not True:
        raise EvidenceNotAdmitted("Unverified biomass effort or outcome-dependent resource")
    if resource.get("mass_basis") not in ("dry","fresh") or not resource.get("resource_guild"):
        raise EvidenceNotAdmitted("Biomass guild or mass basis unverified")
    if not isinstance(resource.get("daily_series"),list) or len(resource["daily_series"])<2:
        raise EvidenceNotAdmitted("No resource time series")
    checks["independent_biomass"]=True
    consumer=bundle["consumer"]
    if consumer.get("demand_curve_source_verified") is not True:
        raise EvidenceNotAdmitted("Unverified consumer demand window")
    if not isinstance(consumer.get("daily_demand"),list) or not consumer["daily_demand"]:
        raise EvidenceNotAdmitted("Missing demand curve")
    checks["consumer_demand"]=True
    resource_by_day={}
    for point in resource["daily_series"]:
        day=dt.date.fromisoformat(point["date"])
        val=float(point["biomass_g_m2"])
        if day.year!=year or not math.isfinite(val) or val<0 or day in resource_by_day:
            raise EvidenceNotAdmitted("Invalid resource date, value or duplicate")
        resource_by_day[day]=val
    demand_by_day={}
    for point in consumer["daily_demand"]:
        day=dt.date.fromisoformat(point["date"])
        weight=float(point["weight"])
        if day.year!=year or not math.isfinite(weight) or weight<0 or day in demand_by_day:
            raise EvidenceNotAdmitted("Invalid consumer demand date, weight or duplicate")
        demand_by_day[day]=weight
    if set(demand_by_day)-set(resource_by_day):
        raise EvidenceNotAdmitted("Biomass missing on consumer demand days; no extrapolation")
    total=sum(demand_by_day.values())
    if total<=0:
        raise EvidenceNotAdmitted("Zero consumer demand")
    exposure=sum(resource_by_day[d]*weight for d,weight in demand_by_day.items())/total
    return {"site_id":site,"year":year,"status":"SOURCE_VERIFIED_BUNDLE_FEATURES_ONLY",
        "checks":checks,
        "demand_weighted_resource_biomass_g_m2":round(exposure,6),
        "resource_mass_basis":resource["mass_basis"],
        "monitoring_quantity_kind":monitoring["quantity_kind"],
        "outcome_effect_estimated":False,
        "climate_causality_identified":False,
        "taxon_interaction_proven":False}
