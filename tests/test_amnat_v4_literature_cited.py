"""Bibliography audit tests; no source outcome is recalculated."""
import copy
import json
from pathlib import Path

from scripts.audit_amnat_v4_literature_cited import audit, ANCHORS

ROOT=Path(__file__).resolve().parents[1]
MS=ROOT/"manuscript/PAYOFF_B_INFORMATION_CONTROL_V4_V8_INTEGRATED.md"
CAT=ROOT/"submission/AMNAT_V4_REFERENCE_CATALOGUE_20261013.json"


def source():
    return MS.read_text(encoding="utf-8"),json.loads(CAT.read_text(encoding="utf-8"))


def test_20_publisher_verified_sources_are_all_in_main_text_and_bib():
    s,c=source()
    r=audit(s,c)
    assert r["status"]=="VERIFIED_CORE_CITATION_CROSSWALK_SUBMISSION_HOLD"
    assert r["n_core_references"]==20
    assert r["n_in_text"]==20
    assert r["n_in_bibliography"]==20
    assert not r["audit_errors"]
    assert r["anonymous_submission_ready"] is False
    assert r["full_raw_data_reproduction"] is False
    assert set(ANCHORS)=={x["key"] for x in c["records"]}


def test_missing_intext_citation_cannot_be_masked_by_bibliography():
    s,c=source()
    s=s.replace("Bauer et al. 2008","Bauer et al. YEAR_MISSING",1)
    r=audit(s,c)
    assert "verified core source absent from body: Bauer2008" in r["audit_errors"]


def test_unverified_or_duplicate_doi_fails():
    s,c=source()
    cc=copy.deepcopy(c)
    cc["records"][0]["doi"]=cc["records"][1]["doi"]
    r=audit(s,cc)
    assert r["status"]=="CITATION_CROSSWALK_FAIL"
    assert any("duplicate DOI" in x for x in r["audit_errors"])


def test_missing_reference_section_fails():
    s,c=source()
    s=s.replace("## Literature Cited","## Not Literature Cited",1)
    r=audit(s,c)
    assert "full core bibliography section absent" in r["audit_errors"]


def test_core_reference_cannot_be_silently_relabeled():
    s,c=source()
    cc=copy.deepcopy(c)
    cc["records"][0]["key"]="Fictitious2026"
    r=audit(s,cc)
    assert "reference-key map does not match registered catalogue" in r["audit_errors"]
