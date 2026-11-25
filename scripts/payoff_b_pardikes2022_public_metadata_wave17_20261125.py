#!/usr/bin/env python3
"""Bounded public metadata search; never download a matched data file automatically."""
import json, sys, re
from pathlib import Path
from urllib.parse import urlencode
import requests
from payoff_b_interaction_buffering_small_dryad_gate_20261125 import fetch,Hold
TARGET="10.1111/gcb.16195"
TITLE="Effects of phenological mismatch under warming are modified by community context"
def norm(t):return re.sub(r"\W+"," ",str(t).lower()).strip()
def run():
    queries={
      "datacite_related_doi":("https://api.datacite.org/dois",{"query":f'relatedIdentifiers.relatedIdentifier:"{TARGET}"',"page[size]":10}),
      "datacite_title":("https://api.datacite.org/dois",{"query":f'titles.title:"{TITLE}"',"page[size]":10}),
      "dryad_title":("https://datadryad.org/api/v2/search",{"q":TITLE,"per_page":10})
    }
    out={"status":"PUBLIC_METADATA_ONLY","target_article_doi":TARGET,"target_title":TITLE,"queries":{}}
    with requests.Session() as s:
        for key,(base,params) in queries.items():
            url=base+"?"+urlencode(params)
            z={"url":url,"status":"HOLD"};out["queries"][key]=z
            try:
                a=json.loads(fetch(s,url,cap=2_000_000))
                if key.startswith("datacite"):
                    rows=a.get("data");total=a.get("meta",{}).get("total")
                    if not isinstance(rows,list):raise Hold("SCHEMA")
                    records=[]
                    for r in rows:
                        v=r.get("attributes",{})
                        titles=[t.get("title","") for t in v.get("titles",[])]
                        related=[t.get("relatedIdentifier","") for t in v.get("relatedIdentifiers",[])]
                        records.append({"doi":v.get("doi"),"titles":titles,"related_dois":related,
                            "creators":[x.get("name") for x in v.get("creators",[])],
                            "exact_title":any(norm(x.removeprefix("Data from: "))==norm(TITLE) for x in titles),
                            "exact_related_doi":any(TARGET in str(x).lower() for x in related)})
                else:
                    rows=a.get("_embedded",{}).get("stash:datasets",[])
                    total=a.get("total",a.get("totalCount"))
                    if not isinstance(rows,list):raise Hold("SCHEMA")
                    records=[]
                    for v in rows:
                        t=v.get("title","")
                        related=[r.get("identifier",r.get("relationshipType","")) for r in v.get("relatedWorks",[]) if isinstance(r,dict)]
                        records.append({"doi":v.get("identifier"),"title":t,"authors":v.get("authors"),"related":related,
                            "exact_title":norm(str(t).removeprefix("Data from: "))==norm(TITLE),
                            "exact_related_doi":TARGET in json.dumps(v.get("relatedWorks",[])).lower()})
                z.update(status="METADATA_RETRIEVED",reported_total=total,returned_records=len(records),records=records)
            except (Hold,requests.RequestException,ValueError,KeyError,TypeError) as e:z["error"]=str(e) if isinstance(e,Hold) else type(e).__name__
    return out
if __name__=="__main__":
    d=run();print(json.dumps(d,ensure_ascii=True,separators=(",",":")),flush=True)
    p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+"\n")
