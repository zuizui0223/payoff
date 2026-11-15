"""JMA homogeneity-number and source quality admission for time-series models.

JMA warns that comparisons across distinct homogeneity numbers require
caution. This gate treats a numeric homogeneity number as a regime label,
not a quality score, and refuses a cross-regime trend fit by default.
"""
from __future__ import annotations
from collections import Counter, defaultdict

class HomogeneityNotAdmitted(ValueError):
    pass

def audit_homogeneity_regimes(rows, *, variable, min_days=27,
                              allow_multi_regime=False):
    if not rows:
        raise HomogeneityNotAdmitted("No daily source rows")
    station_ids={r.get("station_metadata_id") for r in rows}
    if len(station_ids)!=1 or None in station_ids:
        raise HomogeneityNotAdmitted("Exactly one source station required")
    seen=set()
    by_regime=defaultdict(list)
    rejected=Counter()
    for r in rows:
        day=r.get("date")
        if day in seen:
            raise HomogeneityNotAdmitted("Duplicate station-day")
        seen.add(day)
        if not r.get("station_valid_for_date",False):
            rejected["station_history_unverified"]+=1
            continue
        if variable not in r.get("values",{}):
            rejected["variable_unavailable"]+=1
            continue
        if r["values"][variable] is None:
            rejected["variable_missing_or_quality_rejected"]+=1
            continue
        hom=r.get("homogeneity_numbers",{}).get(variable)
        if hom is None or str(hom).strip()=="":
            rejected["homogeneity_number_missing"]+=1
            continue
        by_regime[str(hom)].append(r)
    counts={k:len(v) for k,v in sorted(by_regime.items())}
    enough={k:v for k,v in counts.items() if v>=min_days}
    status=("ADMITTED_ONE_REGIME" if len(enough)==1 and len(counts)==1
            else "MULTIPLE_REGIMES_REQUIRE_STRATIFICATION" if len(counts)>1
            else "INSUFFICIENT_SINGLE_REGIME")
    return {"station_metadata_id":next(iter(station_ids)),"variable":variable,
            "homogeneity_regime_day_counts":counts,
            "rejected_day_counts":dict(rejected),
            "status":status,
            "ready_for_unstratified_time_series":status=="ADMITTED_ONE_REGIME",
            "allow_multi_regime_requested":allow_multi_regime,
            "regime_values_are_not_quality_scores":True,
            "no_weather_effect_fitted":True}
