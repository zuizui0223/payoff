"""Synthetic cohort histories; never disclose real animals."""
from scripts.qc_payoff_b_shared_tag_timeline import parse_time,tag_timeline
from scripts.qc_payoff_b_stork_cohort_overlap import NEW_REF
import pytest

def ref(animal,tag,start,end):
    return {"animal-id":animal,"animal-ring-id":animal,
            "deployment-id":animal,"tag-id":tag,
            "deploy-on-date":start,"deploy-off-date":end,
            "animal-life-stage":"adult"}

def test_timestamp_parser_and_blank():
    assert parse_time("Unknown") is None
    assert parse_time("2015-04-01 11:00:00") is not None

def test_timeline_rejects_changed_source_id_universe():
    n=[ref("a","T","2014-01-01","2014-06-01")]
    o=[ref("b","T","2015-01-01","2015-06-01")]
    with pytest.raises(ValueError,match="identity changed"):
        tag_timeline(n,o)

def test_source_checksum_pinned():
    assert NEW_REF["size"]==43098
