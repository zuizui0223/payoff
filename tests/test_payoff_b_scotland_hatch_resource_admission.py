"""Only synthetic event/nest fixture source-admission tests, never effect evidence."""
from scripts.payoff_b_scotland_hatch_resource_admission import candidate_nests, iso_day


def example(*, year=2020, sp="bluti", treatment="", hatch="134",
            fledged="5", clutch="8", box="1"):
    return {"year":str(year), "site":"ABC","box":box,"species":sp,
            "clutch_swap_treatment":treatment,
            "hatching_first_recorded":hatch,"suc":fledged,"cs":clutch}


def test_no_untagged_2017_2019_experiment_nests():
    rows=[
        example(year=2019,treatment="",box="1"),
        example(year=2019,treatment="unmanipulated",box="2"),
        example(year=2020,treatment="",box="3"),
        example(year=2018,treatment="odd",box="4"),
        example(year=2016,treatment="",box="5"),
    ]
    accepted,exclusions,_,_=candidate_nests(rows)
    assert {x["box"] for x in accepted}=={"2","3","5"}
    assert exclusions["unknown_treatment_during_experiment"]==1
    assert exclusions["manipulated_or_odd"]==1


def test_species_source_requires_confirmed_blue_tit():
    rows=[example(sp="",box="1"),example(sp="coati",box="2"),
          example(sp="bluti",box="3")]
    accepted,exclusions,_,_=candidate_nests(rows)
    assert len(accepted)==1 and accepted[0]["box"]=="3"
    assert exclusions["unverified_or_non_blue_tit"]==2


def test_hatch_fledgling_sentinels_and_biology_guard():
    rows=[example(box="1",hatch="-999"),
          example(box="2",fledged="-999"),
          example(box="3",clutch="0"),
          example(box="4",fledged="12",clutch="8"),
          example(box="5")]
    accepted,exclusions,_,_=candidate_nests(rows)
    assert len(accepted)==1
    assert exclusions["no_hatch"]==1
    assert exclusions["no_fledglings_or_sentinel"]==1
    assert exclusions["no_clutch"]==1
    assert exclusions["fledged_exceeds_clutch"]==1


def test_original_doy_leap_conversion_is_exact():
    assert iso_day(2020,60)=="2020-02-29"
    assert iso_day(2019,60)=="2019-03-01"
