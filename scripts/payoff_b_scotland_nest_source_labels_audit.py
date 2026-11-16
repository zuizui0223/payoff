"""Source-label gate: require independently identified blue tit and non-manipulated nests.

This is descriptive, outcome *availability* only, no fitness model or resource
effect. Year-specific treatment descriptions from official EIDC docx:
2017–2019 clutch-swap experiment, explicit 'unmanipulated' accepted;
blank treatment in those three years is unverified and fails closed.
"""
import argparse,json
from collections import Counter,defaultdict
from pathlib import Path

from scripts.payoff_b_scotland_hatch_resource_admission import original,numeric


def audit():
    rows=original()["data/bird_phenology.csv"]
    by=defaultdict(Counter)
    reasons=Counter()
    allowed=Counter()
    for r in rows:
        yr=numeric(r.get("year"))
        if yr is None:
            reasons["no_year"]+=1;continue
        yr=int(yr)
        sp=str(r.get("species") or "").strip().lower()
        tr=str(r.get("clutch_swap_treatment") or "").strip().lower()
        hatch=numeric(r.get("hatching_first_recorded"))
        fledge=numeric(r.get("suc"))
        clutch=numeric(r.get("cs"))
        code=f"{sp or '<blank>'}|{tr or '<blank>'}"
        by[yr]["total"]+=1
        by[yr][code]+=1
        if hatch is not None:by[yr]["has_hatch"]+=1
        if fledge is not None and fledge>=0:by[yr]["has_nonnegative_fledge"]+=1
        if sp!="bluti":
            reasons["not_verified_blue_tit"]+=1;continue
        if tr not in ("","unmanipulated"):
            reasons["manipulated_or_ambiguous_treatment"]+=1;continue
        if 2017 <= yr <= 2019 and tr=="":
            reasons["unknown_treatment_during_experiment"]+=1;continue
        if hatch is None or fledge is None or fledge<0 or clutch is None or clutch<=0 or fledge>clutch:
            reasons["no_complete_valid_hatch_fledge_clutch"]+=1;continue
        allowed[yr]+=1
        by[yr]["source_identified_blue_tit_unmanipulated_and_complete"]+=1
    return {
        "status":"PAYOFF_B_EIDC_SOURCE_SPECIES_TREATMENT_CROSSTAB_GATE",
        "row_count":len(rows),
        "source_species_only_bluti":True,
        "experiment_years_blank_treatment_excluded":[2017,2018,2019],
        "no_phenotypic_effect_fitted":True,
        "year_by_category":{str(k):dict(v) for k,v in sorted(by.items())},
        "excluded":dict(reasons),
        "validated_complete_nests_by_year":{str(k):v for k,v in sorted(allowed.items())},
        "candidate_years":sorted(allowed),
        "candidate_total":sum(allowed.values()),
    }


def main():
    p=argparse.ArgumentParser();p.add_argument("--output",required=True,type=Path)
    args=p.parse_args()
    result=audit()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(result,ensure_ascii=False,separators=(",",":")))


if __name__=="__main__":
    main()
