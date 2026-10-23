"""Evidence ledger guard against primary-null relabeling and pseudo-replication."""
from pathlib import Path
import json

def test_stork_primary_cannot_be_rescued_by_exploratory_91():
    x=json.loads(Path("data/payoff_b_stage_timing_evidence_20261019.json").read_text())
    p=x["original_primary_stork"]
    assert p["status"]=="NOT_SUPPORTED"
    assert p["n_identity_years"]==53
    assert p["cluster_95pct_ci"][1] > 1
    a=x["source_geometry_exploratory"]
    assert a["exploratory_only"] is True
    assert a["not_species_pooled"] is True
    assert len(a["systems"])==5
    assert a["systems"][0]["n_identity_years"]==91
    assert a["systems"][2]["repeated_animals"]==0
    assert a["systems"][3]["beta"] is None
    assert x["scientific_verdict"]["original_primary_supported"] is False

def test_synthetic_window_null_no_biological_controller():
    x=json.loads(Path("data/payoff_b_stage_timing_evidence_20261019.json").read_text())
    z=x["illustrative_censoring_null"]
    assert z["type"]=="SYNTHETIC_NOT_FIT_TO_BIRD_DATA"
    assert z["no_behavioral_adjustment"]
    assert z["observed_if_t80_at_or_before_day120_beta"]<.8
