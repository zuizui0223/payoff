"""Original Movebank Data Repository V7 3-flyway published GPS source preflight.

No proprietary/live Movebank API or credentials. Access only DSpace public
metadata and exact repository links provided by the server. Does not fit
Kölzsch predictability q × independent route urgency U.
"""
import argparse,hashlib,json
from pathlib import Path
from urllib.parse import urlencode,urlparse,urljoin
from scripts.payoff_b_scotland_resource_source_probe import open_url

ROOT="https://datarepository.movebank.org/server"
DOIS={
  "Greenland":"10.5441/001/1.5d3f0664",
  "Svalbard":"10.5441/001/1.5k6b1364",
  "Barents Sea":"10.5441/001/1.ps244r11",
}
ALLOWED_HOSTS={"datarepository.movebank.org","www.datarepository.movebank.org"}
MAX_JSON=1_200_000

def controlled_link(url):
    if not isinstance(url,str) or not url:
        return None
    if url.startswith("/server/api/"):
        url="https://datarepository.movebank.org"+url
    elif url.startswith("/api/"):
        url=ROOT+url
    elif url.startswith("/"):
        return None
    parsed=urlparse(url)
    if parsed.scheme!="https" or parsed.hostname not in ALLOWED_HOSTS:
        return None
    if not parsed.path.startswith("/server/api/"):
        return None
    return url

def source_json(url):
    u=controlled_link(url)
    if u is None:
        return {"status":"SOURCE_LINK_BLOCKED"},None
    res=open_url(u,max_read=MAX_JSON,timeout=40)
    raw=res.get("body")
    out={"url":u,"http_status":res.get("http_status"),
         "content_type":res.get("content_type")}
    if not raw or res.get("http_status")!=200:
        out["status"]="SOURCE_JSON_UNAVAILABLE"
        return out,None
    try:
        val=json.loads(raw)
    except ValueError:
        out["status"]="INVALID_SOURCE_JSON"
        return out,None
    out["status"]="OFFICIAL_REPOSITORY_JSON_VERIFIED"
    out["source_json_sha256"]=hashlib.sha256(raw).hexdigest()
    return out,val


def extract_items(response):
    if not isinstance(response,dict):
        return []
    nested=response.get("_embedded",{}).get("searchResult",{})
    found=nested.get("_embedded",{}).get("objects",[])
    items=[]
    for row in found:
        if not isinstance(row,dict): continue
        inner=row.get("_embedded",{}).get("indexableObject")
        if isinstance(inner,dict):
            items.append(inner)
    return items


def metadata_values(item,key):
    vals=item.get("metadata",{}).get(key,[])
    if not isinstance(vals,list):return []
    return [str(v.get("value")) for v in vals
            if isinstance(v,dict) and v.get("value")]


def doi_in_metadata(item,doi):
    a=doi.lower()
    for field,values in (item.get("metadata") or {}).items():
        if not isinstance(values,list):continue
        for v in values:
            if isinstance(v,dict):
                text=str(v.get("value") or "").lower()
                if a in text:
                    return {"field":field,"value":v.get("value")}
    return None


def discover(doi):
    endpoint=ROOT+"/api/discover/search/objects?"+urlencode({
        "query":doi,"dsoType":"item","size":"10","page":"0"})
    rec,src=source_json(endpoint)
    out={"searched_doi":doi,"search_receipt":rec}
    if src is None:
        out["gate"]="NO_GO_PUBLIC_DSPACE_DISCOVERY"
        return out
    items=extract_items(src)
    out["item_count_page"]=len(items)
    out["page"]=src.get("_embedded",{}).get("searchResult",{}).get("page")
    matching=[]
    for item in items:
        doi_evidence=doi_in_metadata(item,doi)
        if doi_evidence is None:
            continue
        link=item.get("_links",{}).get("self",{}).get("href")
        matching.append({
            "uuid":item.get("uuid"),"name":item.get("name"),
            "handle":item.get("handle"),"doi_evidence":doi_evidence,
            "license":metadata_values(item,"dc.rights.uri"),
            "rights":metadata_values(item,"dc.rights"),
            "item_self":controlled_link(link),
            "bundles_link":controlled_link(item.get("_links",{}).get("bundles",{}).get("href"))
        })
    out["doi_exact_matching_items"]=matching
    out["gate"]="ARCHIVE_ITEM_DOI_MATCH" if len(matching)==1 else \
        ("NO_GO_DOI_NOT_IN_SEARCH_ITEMS" if not matching
         else "NO_GO_AMBIGUOUS_DOI_ITEMS")
    if len(matching)!=1:return out
    # HATEOAS-linked item details, license and published original file lists.
    item=matching[0]
    target=item["item_self"]
    if target:
        ir,full=source_json(target)
        out["full_item_receipt"]=ir
        if full:
            out["verified_full_item"]= {
                "uuid":full.get("uuid"),"name":full.get("name"),
                "doi_evidence":doi_in_metadata(full,doi),
                "license":metadata_values(full,"dc.rights.uri"),
                "rights":metadata_values(full,"dc.rights"),
                "metadata_keys":sorted(full.get("metadata",{})),
            }
            href=full.get("_links",{}).get("bundles",{}).get("href")
            if href:item["bundles_link"]=controlled_link(href)
    if item.get("bundles_link"):
        br,bundles=source_json(item["bundles_link"])
        out["bundles_receipt"]=br
        if bundles is not None:
            arr=bundles.get("_embedded",{}).get("bundles",[])
            out["bundle_count"]=len(arr)
            out["bundle_overview"]=[{
                "name":b.get("name"),"uuid":b.get("uuid"),
                "bitstreams":controlled_link(b.get("_links",{}).get("bitstreams",{}).get("href"))
            } for b in arr if isinstance(b,dict)]
    return out


def audit():
    results={}
    for flyway,doi in DOIS.items():
        results[flyway]=discover(doi)
    return {
        "status":"PAYOFF_B_FROZEN_V7_MOVEbank_3FLYWAY_SOURCE_PREFLIGHT",
        "frozen_contract":"docs/PAYOFF_B_V7_PREDICTABILITY_URGENCY_CONTRACT_20261005.md",
        "paper_doi":"10.1111/1365-2656.12281",
        "flyway_source_gate":results,
        "published_routes":list(DOIS),
        "all_three_archives_exactly_admitted":all(
            r.get("gate")=="ARCHIVE_ITEM_DOI_MATCH" for r in results.values()
        ),
        "gps_source_rows_downloaded":False,
        "historical_spring_predictability_identified":False,
        "focal_q_x_U_estimate_opened":False,
        "source_eBird_used":False,
    }

def main():
    p=argparse.ArgumentParser();p.add_argument("--output",required=True,type=Path)
    a=p.parse_args()
    outcome=audit()
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(outcome,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(outcome,ensure_ascii=False,separators=(",",":")))


if __name__=="__main__":
    main()
