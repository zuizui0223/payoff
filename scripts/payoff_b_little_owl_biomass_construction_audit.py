"""PAYOFF-B: original Little Owl BM mass is derived from prey-class counts.

As explicitly documented by Sailas et al. 2026 (published Methods 2.3),
mammals=25 g, birds=33 g, insects=0.9 g, earthworms=3.7 g,
unidentified=2.9 g per source prey item. Validate construction from source,
rather than mistake derived BM or post-hoc prey type shares as independent
measured biomass. This is an integrity calculation, not an ecological effect.
"""
import argparse
import json
import math
from pathlib import Path
from collections import Counter
from scripts.payoff_b_little_owl_broodday_source_admission import (
    download_original,parse_number
)

PER_PREY_GRAMS={
    "mammal":25.0,
    "bird":33.0,
    "insect":0.9,
    "earthworms":3.7,
    "other":2.9,
}
TOLERANCE=1e-7

def source_reconstruction(rows):
    bad=[]
    max_abs_bm_error=0.
    max_abs_count_error=0.
    max_abs_daily_bm_error=0.
    count_close=0
    bm_close=0
    adjusted_close=0
    rates=Counter()
    for i,r in enumerate(rows):
        terms={s:parse_number(r.get(s)) for s in PER_PREY_GRAMS}
        bm=parse_number(r.get("BM"))
        rate=parse_number(r.get("prov_rate"))
        adjusted=parse_number(r.get("BM2"))
        fraction=parse_number(r.get("prop.day.monitored"))
        if any(z is None or z<0 for z in terms.values()) or bm is None or rate is None:
            bad.append({"row":i+1,"reason":"missing_source_count_or_mass"})
            continue
        constructed=sum(terms[k]*PER_PREY_GRAMS[k] for k in PER_PREY_GRAMS)
        item_count=sum(terms.values())
        err=abs(constructed-bm)
        cerr=abs(item_count-rate)
        max_abs_bm_error=max(err,max_abs_bm_error)
        max_abs_count_error=max(cerr,max_abs_count_error)
        if math.isclose(constructed,bm,rel_tol=1e-9,abs_tol=TOLERANCE):
            bm_close+=1
        else:
            bad.append({"row":i+1,"reason":"BM_nonreconstructible",
                        "abs_error_g":round(err,7)})
        if math.isclose(item_count,rate,rel_tol=1e-9,abs_tol=TOLERANCE):
            count_close+=1
        else:
            rates["category_item_count_differs_from_rate"]+=1
        if fraction is None or fraction<=0 or adjusted is None:
            bad.append({"row":i+1,"reason":"adjusted_missing"})
        else:
            derror=abs(adjusted-constructed/fraction)
            max_abs_daily_bm_error=max(max_abs_daily_bm_error,derror)
            if math.isclose(adjusted,constructed/fraction,
                            rel_tol=1e-9,abs_tol=TOLERANCE):
                adjusted_close+=1
            else:
                bad.append({"row":i+1,"reason":"BM2_not_reconstructed",
                            "abs_error_g":round(derror,7)})
    n=len(rows)
    return {
        "status":"PAYOFF_B_ORIGINAL_LITTLE_OWL_BIOMASS_CONSTRUCTION_AUDIT",
        "original_source_rows":n,
        "published_mean_weight_grams_per_item":PER_PREY_GRAMS,
        "biomass_estimated_not_independently_weighed":True,
        "constant_g_per_prey_class_arithmetic_prior_art":True,
        "reconstructed_BM_match_n":bm_close,
        "category_count_matches_prov_rate_n":count_close,
        "reconstructed_BM2_match_n":adjusted_close,
        "maximum_absolute_BM_error_g":max_abs_bm_error,
        "maximum_absolute_category_count_error":max_abs_count_error,
        "maximum_absolute_adjusted_BM2_error_g":max_abs_daily_bm_error,
        "count_vs_rate_diagnostic":dict(rates),
        "first_10_discrepancies":bad[:10],
        "n_discrepancies":len(bad),
        "does_not_validate_independent_biomass_or_consumed_energy":True,
        "fitted_biological_effect":False,
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args()
    raw=download_original()["Littleowl.dat.JAB.csv"]
    result=source_reconstruction(raw)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps(result,separators=(",",":"),ensure_ascii=False))

if __name__=="__main__":
    main()
