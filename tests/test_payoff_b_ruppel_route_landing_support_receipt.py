"""Rüppel original source 2x2 support is checked without modeling its effect."""
import csv
import pytest

from scripts.payoff_b_ruppel_route_landing_support_receipt import (
    audit_cross_tab, ROUTES, YEARS,
)


def synthetic_source_aggregate(locs=(10,14),nonland=(144,10)):
    # Only synthetic group counts to test gates; not original bird data.
    birds=("SyntheticTaxonA","SyntheticTaxonB","SyntheticTaxonC")
    out=[]
    for ri,route in enumerate(ROUTES):
        for land,total in (("0",nonland[ri]),("1",locs[ri])):
            q,rem=divmod(total,9)
            for i,sp in enumerate(birds):
                for j,year in enumerate(YEARS):
                    index=i*3+j
                    out.append({
                        "species":sp,"year":year,"route":route,
                        "landing":land,
                        "count":q+int(index<rem)
                    })
    assert len(out)==36
    return out


def write(rows,path):
    with path.open("w",encoding="utf-8",newline="") as h:
        writer=csv.DictWriter(h,fieldnames=[
            "species","year","route","landing","count"
        ])
        writer.writeheader()
        writer.writerows(rows)


def test_original_study_support_threshold_only_when_both_route_cells_cross(tmp_path):
    p=tmp_path/"synthetic_aggregate.csv"
    write(synthetic_source_aggregate(),p)
    x=audit_cross_tab(p)
    assert x["source_2by2_route_landing"]["coasting"]["observed_landings"]==10
    assert x["source_2by2_route_landing"]["sea-crossing"]["observed_landings"]==14
    assert x["route_landing_modifier_source_support"]==(
        "DESIGN_SUPPORT_PRESENT_NO_EFFECT_FITTED"
    )
    assert x["postflight_weather_measured_at_end_is_a_predeparture_forecast"] is False
    assert x["novel_biological_effect_fitted"] is False


def test_perfect_route_landing_confounding_fails_without_pseudocount(tmp_path):
    p=tmp_path/"synthetic_aggregate.csv"
    write(synthetic_source_aggregate(locs=(0,24),nonland=(154,0)),p)
    out=audit_cross_tab(p)
    assert out["source_2by2_route_landing"]["coasting"]["observed_landings"]==0
    assert out["source_2by2_route_landing"]["sea-crossing"]["observed_nonlandings"]==0
    assert out["route_landing_modifier_source_support"]==(
        "ROUTE_LANDING_MODIFIER_NOT_ESTIMABLE_UNDER_FROZEN_SUPPORT"
    )


def test_missing_original_zero_cell_is_not_interpreted_as_unobserved(tmp_path):
    p=tmp_path/"synthetic_aggregate.csv"
    d=synthetic_source_aggregate()
    write(d[:-1],p)
    with pytest.raises(ValueError,match="exactly 3 original"):
        audit_cross_tab(p)


def test_raw_animal_identifier_column_not_promoted(tmp_path):
    p=tmp_path/"synthetic_aggregate.csv"
    d=synthetic_source_aggregate()
    d.append({
      "species":"SyntheticTaxonA","year":"2019","route":"coasting",
      "landing":"1","count":"SECRET_ID"
    })
    write(d,p)
    with pytest.raises(ValueError,match="exactly 3 original"):
        audit_cross_tab(p)


def test_route_and_landing_totals_must_match_original_paper(tmp_path):
    p=tmp_path/"synthetic_aggregate.csv"
    d=synthetic_source_aggregate()
    d[0]["count"]+=1
    write(d,p)
    with pytest.raises(ValueError,match="coasting/sea-crossing totals"):
        audit_cross_tab(p)
