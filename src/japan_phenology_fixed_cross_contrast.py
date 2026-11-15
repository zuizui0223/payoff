"""Year-to-year co-fluctuation across fixed-composition phenology lag contrasts.

Uses national annual series only when identical fixed calendar blocks are
available. Correlations are exploratory and may share underlying event dates;
they are NOT independent evidence for ecological coordination.
"""
from __future__ import annotations
from itertools import combinations
from src.japan_phenology_coupling_robustness import _pearson, _detrend

def fixed_panel_cross_contrast_synchrony(receipt):
    panels=receipt["panels"]
    output=[]
    for window in receipt["windows"]:
        eligible={p["contrast"]:p for p in panels
                  if p["window"]==window and p["coverage_passed"] and len(p["annual"])==window[1]-window[0]+1}
        for a,b in combinations(sorted(eligible),2):
            aa={r["year"]:r["station_equal_mean_lag_anomaly_days"] for r in eligible[a]["annual"]}
            bb={r["year"]:r["station_equal_mean_lag_anomaly_days"] for r in eligible[b]["annual"]}
            years=sorted(set(aa)&set(bb))
            if len(years)<10:continue
            x=[aa[y] for y in years]
            y=[bb[z] for z in years]
            r=_pearson(x,y)
            detr=_pearson(_detrend(years,x),_detrend(years,y))
            loo=[_pearson(x[:i]+x[i+1:],y[:i]+y[i+1:]) for i in range(len(years))]
            loo=[v for v in loo if v is not None]
            concord=sum((u>0)==(v>0) for u,v in zip(x,y))
            output.append({"window":window,"contrast_a":a,"contrast_b":b,
                "shared_years":len(years),
                "annual_mean_lag_anomaly_pearson_r":round(r,6) if r is not None else None,
                "linearly_detrended_pearson_r":round(detr,6) if detr is not None else None,
                "leave_one_year_out_r_range":[round(min(loo),6),round(max(loo),6)] if loo else None,
                "same_sign_years":concord,
                "same_sign_fraction":round(concord/len(years),6),
                "station_sets_identical_across_contrasts":False,
                "shared_source_event_dates_not_independent":True,
                "weather_or_biomass_explanation_identified":False})
    return {"status":"DESCRIPTIVE_FIXED_BLOCK_ANNUAL_CROSS_CONTRAST_SYNCHRONY",
            "n_comparisons":len(output),
            "not_independent_due_to_shared_taxa":True,
            "no_weather_ndvi_biomass_fit":True,
            "comparisons":output}
