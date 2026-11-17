"""Source-derived aggregates, not synthetic bird outcomes."""
from copy import deepcopy
import pytest
from scripts.payoff_b_v7_suppinfo_aggregate_gate import (
    QP,REGIONS,SOURCE_SHA,readrows,audit_pairs
)

def reference():
    return readrows(QP),readrows(REGIONS)

def test_original_source_q_admission_but_not_V7_outcome():
    q,r=reference()
    x=audit_pairs(q,r)
    assert x["uploaded_original_docx_sha256"]==SOURCE_SHA
    assert x["original_30year_pairwise_q"]==23
    assert x["original_table_S1_regions"]==16
    assert x["consecutive_route_pairs"]==13
    assert x["consecutive_unambiguous_S1_candidate_names"]==11
    assert x["pairwise_q_by_flyway"]=={
       "Greenland":7,"Svalbard":5,"Barents Sea":11
    }
    assert x["frozen_V7_q_transition_count_admission"]=="PASS_Q_COUNTS_ONLY"
    assert x["frozen_V7_bird_arrival_response_y_opened"] is False
    assert x["original_annual_1982_2011_regional_onsets_as_tabular_rows"] is False

def test_missing_source_q_fails_closed():
    q,r=reference()
    with pytest.raises(ValueError,match="Expected"):
        audit_pairs(q[:-1],r)

def test_corrupted_q_cannot_replace_source():
    q,r=reference()
    q=deepcopy(q)
    q[0]["q_30year_correlation"]="1.6"
    with pytest.raises(ValueError,match="correlation"):
        audit_pairs(q,r)

def test_duplicate_original_pair_rejected():
    q,r=reference()
    q=deepcopy(q)
    q[1]=deepcopy(q[0])
    with pytest.raises(ValueError,match="Repeated"):
        audit_pairs(q,r)

def test_S1_unverified_aliases_not_promoted():
    q,r=reference()
    q=deepcopy(q)
    row=next(v for v in q if v["source_code"]=="NLDK")
    row["source_alias_status"]="exact"
    with pytest.raises(ValueError,match="alias"):
        audit_pairs(q,r)

def test_wrong_original_digest_rejected():
    q,r=reference()
    r=deepcopy(r)
    r[0]["source_docx_sha256"]="0"*64
    with pytest.raises(ValueError,match="hash"):
        audit_pairs(q,r)
