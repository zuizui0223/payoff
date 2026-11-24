"""Synthetic-only tests for CC0 tag-deployment time support; no GPS source rows."""
import pytest
from datetime import date
from scripts import payoff_b_stork_deployment_time_gate_20261124 as s


def synthetic():
    return {
      "control":[
        {"tag":"PRIVATE_C1","start":date(2019,9,1),"end":date(2019,10,1)},
        {"tag":"PRIVATE_C2","start":date(2019,9,10),"end":date(2019,9,20)}
      ],
      "delayed":[
        {"tag":"PRIVATE_D1","start":date(2019,9,15),"end":date(2019,9,30)},
        {"tag":"PRIVATE_D2","start":date(2019,11,10),"end":None}
      ],
      "naturally_timed":[
        {"tag":"PRIVATE_N1","start":date(2019,8,1),"end":date(2019,8,15)},
        {"tag":"PRIVATE_N2","start":date(2019,9,15),"end":date(2019,10,15)}
      ]
    }


def contract():
    return {"original_archives":{
        "control":{"rows":2},"delayed":{"rows":2},"naturally_timed":{"rows":2}
    }}


def test_parse_known_source_iso_without_fabricating_missing_ends():
    assert s.parse_source_date("2019-09-12")==date(2019,9,12)
    assert s.parse_source_date("2019-09-12 14:30:00.000")==date(2019,9,12)
    assert s.parse_source_date("2019-09-12T14:30:00Z")==date(2019,9,12)
    assert s.parse_source_date("NA") is None
    assert s.parse_source_date("2019/09/12") is None
    assert s.parse_source_date("") is None


def test_deployment_date_overlap_is_coverage_not_social_contact():
    rows=synthetic()
    assert s.pair_overlap(rows["control"],rows["delayed"])==2
    assert s.pair_overlap(rows["control"],rows["control"],same_cohort=True)==1
    z=s.compute(rows,contract())
    assert z["status"]=="TIME_WINDOW_ENDS_UNOBSERVED"
    assert z["source_cohorts"]["delayed"]["n_bounded_valid_on_off_intervals"]==1
    assert z["source_cohorts"]["delayed"]["n_missing_or_unparseable_off"]==1
    assert z["GPS_ZIPs_downloaded"] is False
    assert z["no_actual_bird_colocation_or_social_information_identified"] is True
    assert "PRIVATE_C1" not in str(z)
    assert "PRIVATE_D1" not in str(z)


def test_same_tag_string_across_cohorts_is_warning_not_pair():
    rows=synthetic()
    rows["delayed"][0]["tag"]="PRIVATE_C1"
    z=s.compute(rows,contract())
    rec=next(x for x in z["cross_cohort_known_bounded_tag_deployment_pair_counts"]
             if (x["cohort_a"],x["cohort_b"])==("control","delayed"))
    assert rec["n_reused_tag_strings"]==1
    assert rec["n_distinct_tag_pairs_with_known_bounded_deployment_overlap"]==1


def test_no_impute_open_end_or_negative_deployment_duration():
    rows=synthetic()
    assert s.overlap_days(rows["delayed"][1],rows["control"][0])==0
    rows["control"][0]["end"]=date(2019,8,1)
    with pytest.raises(ValueError,match="rows or temporal direction"):
        s.compute(rows,contract())


def test_csv_fields_and_original_row_count_gate():
    raw=(b"tag-id,animal-id,deploy-on-date,deploy-off-date,manipulation-type\n"
         b"PRIVATE_C1,bird-1,2019-09-01 00:00:00.000,2019-10-01 00:00:00.000,control\n")
    r=s.read_tag_intervals(raw,1)
    assert r[0]["start"]==date(2019,9,1)
    assert r[0]["end"]==date(2019,10,1)
    assert "animal-id" not in r[0]
    with pytest.raises(ValueError,match="row count"):
        s.read_tag_intervals(raw,2)


def test_do_not_equate_duplicate_deployments_with_independent_birds():
    rows=synthetic()
    rows["naturally_timed"].append({"tag":"PRIVATE_N2","start":date(2020,9,15),"end":date(2020,10,15)})
    c=contract();c["original_archives"]["naturally_timed"]["rows"]=3
    z=s.compute(rows,c)
    assert z["source_cohorts"]["naturally_timed"]["distinct_tag_ids"]==2
    assert z["source_cohorts"]["naturally_timed"]["original_csv_rows"]==3
