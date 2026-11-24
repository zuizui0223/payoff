"""Synthetic code-notebook audits; negative code evidence is NOT a bird-cognition claim."""
import json
import pytest
from scripts import payoff_b_stork_author_code_cue_audit_20261124 as s


def nb(code):
    return json.dumps({"nbformat":4,"nbformat_minor":5,
        "cells":[{"cell_type":"code","source":[code],"metadata":{},"outputs":[],"execution_count":None},
                 {"cell_type":"markdown","source":["social information flock neighbors"],"metadata":{}}],
        "metadata":{}},separators=(",",":")).encode()


def test_cohort_and_flight_are_not_direct_social_information():
    raw=nb('Aviary = "control"; WindSupport = 3; Stopover=4; Survival=1')
    out=s.audit_notebook(raw,s.git_blob_sha1(raw))
    assert out["notebook_code_cell_count"]==1
    assert sum(out["explicit_social_cue_terms_in_code_cells"].values())==0
    assert out["already_published_behavioral_variables"]["cohort"]==1
    assert out["already_published_behavioral_variables"]["wind"]==1
    assert out["original_data_files_opened"] is False


def test_explicit_flock_and_nearest_neighbor_are_detected():
    raw=nb('flock_size=5; nearest_bird_dist=100; social_information=1')
    out=s.audit_notebook(raw,s.git_blob_sha1(raw))
    assert out["explicit_social_cue_terms_in_code_cells"]["social_group_size"]==1
    assert out["explicit_social_cue_terms_in_code_cells"]["neighbor_proximity"]==1
    assert out["explicit_social_cue_terms_in_code_cells"]["social_information"]==1


def test_unpinned_source_code_rejected():
    raw=nb("WindSupport=1")
    with pytest.raises(ValueError,match="changed"):
        s.audit_notebook(raw,"0"*40)


def test_only_original_six_notebooks_allowed():
    assert len(s.PINNED_NOTEBOOKS)==6
    with pytest.raises(ValueError,match="fixed"):
        s.get_raw_notebook("GPS_tracks.csv","deadbeef")
