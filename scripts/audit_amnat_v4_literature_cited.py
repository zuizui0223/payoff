#!/usr/bin/env python3
"""Audit the 20 core author/year DOI bibliography entries against manuscript.

This verifies an editorial crosswalk from manually source-reviewed metadata;
it does NOT independently validate original data fits, every supporting
noncore natural example, publisher-specific bibliography typography or the
final blind-review packet.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

MANUSCRIPT=Path("manuscript/PAYOFF_B_INFORMATION_CONTROL_V4_V8_INTEGRATED.md")
CATALOGUE=Path("submission/AMNAT_V4_REFERENCE_CATALOGUE_20261013.json")

ANCHORS={
    "Amaral2025":"Amaral et al. (2025)",
    "Bauer2008":"Bauer et al. 2008",
    "Bety2003":"Bêty et al. 2003",
    "Burgess2018":"Burgess et al. 2018",
    "Chu2026":"Chu et al. (2026)",
    "Conklin2021":"Conklin et al. 2021",
    "Dossman2023":"Dossman et al. 2023",
    "Jonzen2007":"Jonzén et al. 2007",
    "Kharouba2020":"Kharouba and Wolkovich 2020",
    "Kolzsch2015":"Kölzsch et al. 2015",
    "Morinay2020":"Morinay et al. 2020",
    "Ortega2023":"Ortega et al. (2023)",
    "Samplonius2017":"Samplonius and Both 2017",
    "Samplonius2018":"Samplonius et al. 2018",
    "Samplonius2019":"Samplonius and Both 2019",
    "Senner2014":"Senner et al. 2014",
    "Taylor2016":"Taylor et al. (2016)",
    "Torstenson2025":"Torstenson and Shaw (2025)",
    "Usui2017":"Usui et al. (2017)",
    "Visser2019":"Visser and Gienapp 2019",
}

DOI_PATTERN=re.compile(r"^10\.\d{4,9}/[-._;()/:a-zA-Z0-9]+$")

def audit(manuscript:str, catalogue:dict)->dict:
    records=catalogue.get("records",[])
    errors=[]
    if len(records)!=20 or catalogue.get("n")!=20:
        errors.append("reference catalogue must retain exactly 20 core entries")
    if "## Literature Cited" not in manuscript:
        errors.append("full core bibliography section absent")
        science=manuscript
        bib=""
    else:
        science,bib=manuscript.split("## Literature Cited",1)
        bib=bib.split("## Post-freeze transparency statement",1)[0]
    seen_keys=set()
    seen_dois=set()
    results=[]
    for item in records:
        key=item["key"]
        doi=item["doi"]
        if key in seen_keys:
            errors.append("duplicate reference key: "+key)
        seen_keys.add(key)
        if doi.lower() in seen_dois:
            errors.append("duplicate DOI: "+doi)
        seen_dois.add(doi.lower())
        valid=bool(DOI_PATTERN.fullmatch(doi))
        if not valid:
            errors.append("invalid DOI: "+doi)
        direct="https://doi.org/"+doi
        in_bibliography=(direct in bib and item["title"] in bib)
        if not in_bibliography:
            errors.append("DOI/title missing from core bibliography: "+key)
        pattern=ANCHORS.get(key)
        in_text=bool(pattern and pattern in science)
        if not in_text:
            errors.append("verified core source absent from body: "+key)
        results.append({"key":key,"doi":doi,
                        "citation_anchor":pattern,
                        "in_body":in_text,
                        "in_bibliography":in_bibliography})
    if set(ANCHORS)!=seen_keys:
        errors.append("reference-key map does not match registered catalogue")
    # Known source-availability caveats are non-optional but are NOT all
    # independent tests of outcomes.
    if "same individuals' migration speed" not in science:
        errors.append("redstart independent-sample caveat missing")
    if "registered negative" not in science:
        errors.append("negative transfer registration caveat missing")
    return {
        "status":"VERIFIED_CORE_CITATION_CROSSWALK_SUBMISSION_HOLD"
                 if not errors else "CITATION_CROSSWALK_FAIL",
        "n_core_references":len(records),
        "n_in_text":sum(x["in_body"] for x in results),
        "n_in_bibliography":sum(x["in_bibliography"] for x in results),
        "audit_errors":errors,
        "references":results,
        "full_in_text_claim_citation_validation":False,
        "publisher_bibliography_style_final":False,
        "full_raw_data_reproduction":False,
        "anonymous_submission_ready":False,
        "remaining_tasks":[
            "Check all study-specific natural examples and observational magnitudes against originals",
            "Complete journal-specific bibliography styling and access/date annotations",
            "Generate and visually inspect anonymous manuscript PDF with equations and figures",
            "Independent data/code availability archive, declarations and final author approval",
        ],
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",type=Path,default=MANUSCRIPT)
    p.add_argument("--catalogue",type=Path,default=CATALOGUE)
    p.add_argument("--out",type=Path,required=True)
    a=p.parse_args()
    result=audit(a.source.read_text(encoding="utf-8"),
                 json.loads(a.catalogue.read_text(encoding="utf-8")))
    a.out.parent.mkdir(parents=True,exist_ok=True)
    a.out.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({k:result[k] for k in ("status","n_core_references","n_in_text","n_in_bibliography","audit_errors")},ensure_ascii=False))
    if result["audit_errors"]:
        raise SystemExit(2)

if __name__=="__main__":
    main()
