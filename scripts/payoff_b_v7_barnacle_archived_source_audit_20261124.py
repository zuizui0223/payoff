#!/usr/bin/env python3
"""Read ONLY original public citation and file MANIFEST metadata for V7.

Kölzsch et al 2015 published three separate Movebank archived goose tracking
DOIs. This source check precedes any V7 focal tracking outcome access. It
queries DataCite DOI metadata, DSpace public discovery, pinned item records,
public 'ORIGINAL' bundle/file names/counts/digests. NEVER request GPS event
records, ZIP/bitstream '/content', body of CSV, credentials or license terms
acceptance. Counts and source names/type metadata only.
"""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
from collections import Counter
from urllib.error import HTTPError,URLError
from urllib.parse import quote,urlparse
from urllib.request import Request,build_opener,HTTPRedirectHandler

ROOT="https://datarepository.movebank.org/server/api"
DATACITE="https://api.datacite.org/dois/"
SEARCH=(ROOT+"/discover/search/objects?query=Migration%20timing%20in%20barnacle%20geese&dsoType=item&size=30")
SEARCH_ALIAS=(ROOT+"/discover/search/objects?query=Forecasting%20spring%20from%20afar&dsoType=item&size=30")
UUID_RE=re.compile(r"^[0-9a-f]{8}-(?:[0-9a-f]{4}-){3}[0-9a-f]{12}$")

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        return None

def allowed_metadata_url(url,contract,items=None,bundles=None):
    items=set(items or [])
    bundles=set(bundles or [])
    p=urlparse(url)
    if p.scheme!="https" or p.fragment or p.username or p.password:
        raise ValueError("Non-public or non-HTTPS metadata URL")
    doilist={r["doi"] for r in contract["archive_DOIs"]}
    if p.hostname=="api.datacite.org":
        if p.path.startswith("/dois/") and p.path[len("/dois/"):] in doilist and not p.query:
            return
        raise ValueError("Unregistered DataCite DOI")
    if p.hostname!="datarepository.movebank.org":
        raise ValueError("Unregistered source host")
    if url in (SEARCH,SEARCH_ALIAS,ROOT):
        return
    a=re.fullmatch(r"/server/api/core/items/([a-f0-9-]+)(/bundles)?",p.path)
    b=re.fullmatch(r"/server/api/core/bundles/([a-f0-9-]+)/bitstreams",p.path)
    if p.query:
        raise ValueError("Unregistered DSpace metadata query")
    if a and a.group(1) in items and UUID_RE.fullmatch(a.group(1)):
        return
    if b and b.group(1) in bundles and UUID_RE.fullmatch(b.group(1)):
        return
    raise ValueError("Only original registered public DSpace item/bundle metadata allowed")

def get_public_json(url,contract,items=None,bundles=None,opener=None):
    allowed_metadata_url(url,contract,items,bundles)
    opener=opener or build_opener(NoRedirect())
    req=Request(url,headers={"Accept":"application/hal+json,application/json",
                             "User-Agent":"PAYOFF-B-original-barnacle-source-metadata-only/1.0"})
    try:
        with opener.open(req,timeout=25) as rsp:
            dest=urlparse(rsp.geturl())
            base=urlparse(url)
            if dest.hostname!=base.hostname or dest.path!=base.path:
                raise ValueError("Unexpected source metadata redirect")
            if int(rsp.status)!=200:
                raise ValueError("Source returned non-200")
            if "json" not in str(rsp.headers.get("Content-Type","")).lower():
                raise ValueError("Expected metadata JSON, refusing file content")
            data=rsp.read(contract["metadata_transport"]["max_response_bytes"]+1)
            if len(data)>contract["metadata_transport"]["max_response_bytes"]:
                raise ValueError("Source metadata response exceeds fixed cap")
        return {"status":"PUBLIC_METADATA_JSON_VERIFIED","data":json.loads(data)}
    except (HTTPError,URLError,TimeoutError,OSError,ValueError,json.JSONDecodeError) as exc:
        return {"status":"PUBLIC_METADATA_JSON_NOT_VERIFIED",
                "exception_class":type(exc).__name__,
                "http_status":int(exc.code) if isinstance(exc,HTTPError) else None,
                "data":None}

def normalize(v):
    return re.sub(r"[^a-z0-9]+"," ",str(v or "").lower()).strip()

def citation_record(doc,doi,expected):
    attrs=(doc.get("data") or {}).get("attributes") or {}
    if str(attrs.get("doi") or "").lower()!=doi.lower():
        raise ValueError("DOI identity mismatch")
    titles=attrs.get("titles") or []
    title=str((titles[0] or {}).get("title") or "") if titles else ""
    expected_flyway=next(
        (x for x in ("greenland","svalbard","barents") if x in normalize(expected)),
        None
    )
    title_label=normalize(title)
    valid_title=("migration timing in barnacle geese" in title_label
                 or "forecasting spring from afar" in title_label)
    if expected_flyway is None or not valid_title or expected_flyway not in title_label:
        raise ValueError("Original DOI title did not uniquely identify registered barnacle flyway")
    rights=[{"rights":str(x.get("rights") or "")[:150],
             "rightsIdentifier":str(x.get("rightsIdentifier") or "")[:80],
             "rightsUri":str(x.get("rightsUri") or "")[:250]} for x in (attrs.get("rightsList") or [])[:5]]
    return {"doi":doi,"title":title[:250],
            "year":attrs.get("publicationYear"),
            "publisher":str(attrs.get("publisher") or "")[:120],
            "landing":str(attrs.get("url") or "")[:250],
            "rights":rights,"CC0_metadata_confirmed":any(
               "cc0" in normalize((r["rights"]+" "+r["rightsIdentifier"]+" "+r["rightsUri"]).replace("-",""))
               or "creativecommons org/publicdomain/zero" in r["rightsUri"].lower()
               for r in rights),
            "metadata_only":True}

def dspace_discovery(doc):
    v=((doc.get("_embedded") or {}).get("searchResult") or {}).get("_embedded") or {}
    items=v.get("objects") or []
    out=[]
    for x in items:
        y=((x.get("_embedded") or {}).get("indexableObject") or {})
        title=str(y.get("name") or "")[:260]
        label=normalize(title)
        if ("migration timing in barnacle geese" not in label
            and "forecasting spring from afar" not in label):
            continue
        uuid=str(y.get("uuid") or y.get("id") or "")
        if not UUID_RE.fullmatch(uuid):
            continue
        out.append({"title":title,"uuid":uuid,
                    "handle":str(y.get("handle") or "")[:120]})
    return out

def bundle_items(doc,key):
    data=(doc.get("_embedded") or {}).get(key) or []
    return data if isinstance(data,list) else []

def find_item_for_doi(citation,discovered):
    # Derived from exact public DOI landing URL and original title, never
    # substitute a superficially similar article or unrelated population.
    lp=urlparse(citation["landing"]).path.rstrip("/")
    matches=[x for x in discovered if x["handle"] and lp.endswith("/"+x["handle"])]
    if len(matches)==1 and any(
        fly in normalize(matches[0]["title"]) and fly in normalize(citation["title"])
        for fly in ("greenland","svalbard","barents")
    ) and (
        "migration timing in barnacle geese" in normalize(matches[0]["title"])
        or "forecasting spring from afar" in normalize(matches[0]["title"])
    ):
        return matches[0]
    # Some registered DOI landing pages do not preserve the DSpace handle.
    # An unambiguous flyway in the exact registered title is a backup;
    # this is not used if multiple records match.
    title=normalize(citation["title"])
    hints=[x for x in discovered
           if ("migration timing in barnacle geese" in normalize(x["title"])
               or "forecasting spring from afar" in normalize(x["title"]))
           and any(w in normalize(x["title"]) and w in title
                   for w in ("greenland","svalbard","barents"))]
    if len(hints)==1:
        return hints[0]
    return None

def source_files(archive_files):
    records=[]
    for f in archive_files[:100]:
        name=str(f.get("name") or "")
        extension=Path(name).suffix.lower()
        orig=f.get("checkSum") or {}
        size=f.get("sizeBytes")
        records.append({
          "file_extension":extension[:12] if extension else "NO_SUFFIX",
          "name_contains_GPS":bool(re.search(r"gps|location",name,re.I)),
          "name_contains_ACC":bool(re.search(r"acc|accelerat",name,re.I)),
          "name_contains_readme":bool(re.search(r"readme|description|manifest",name,re.I)),
          "size_bytes":size if isinstance(size,int) and size>=0 else None,
          "original_MD5_metadata_present":str(orig.get("checkSumAlgorithm","")).upper()=="MD5",
          "bitstream_content_downloaded":False,
          "full_filename_or_uuid_exported":False,
        })
    return records

def audit(contract):
    recs=[]
    for entry in contract["archive_DOIs"]:
        doi=entry["doi"]
        r=get_public_json(DATACITE+doi,contract)
        if r["status"]!="PUBLIC_METADATA_JSON_VERIFIED":
            recs.append({"flyway":entry["flyway"],"doi":doi,
                         "status":"DATACITE_SOURCE_NOT_VERIFIED",
                         "error_class":r.get("exception_class"),
                         "http_status":r.get("http_status")})
        else:
            try:
                citation=citation_record(r["data"],doi,entry["expected_label"])
                recs.append({"flyway":entry["flyway"],"doi":doi,
                             "status":"ORIGINAL_DATACITE_CITATION_VERIFIED",
                             "citation":citation})
            except ValueError as e:
                recs.append({"flyway":entry["flyway"],"doi":doi,
                             "status":"DOI_TITLE_OR_IDENTITY_MISMATCH",
                             "error_class":type(e).__name__})
    searches=[get_public_json(u,contract) for u in (SEARCH,SEARCH_ALIAS)]
    original_discovered=[
        item for search in searches if search["data"]
        for item in dspace_discovery(search["data"])
    ]
    discovered=list({item["uuid"]:item for item in original_discovered}.values())
    for record in recs:
        if record["status"]!="ORIGINAL_DATACITE_CITATION_VERIFIED":
            continue
        match=find_item_for_doi(record["citation"],discovered)
        if match is None:
            record["status"]="DOI_VERIFIED_DSPACE_ITEM_NOT_UNIQUELY_MATCHED"
            continue
        item_id=match["uuid"]
        item=get_public_json(ROOT+f"/core/items/{item_id}",contract,items={item_id})
        if item["status"]!="PUBLIC_METADATA_JSON_VERIFIED":
            record["status"]="PUBLIC_DSPACE_ITEM_UNREADABLE"
            continue
        doc=item["data"] or {}
        if str(doc.get("uuid") or doc.get("id") or "")!=item_id or str(doc.get("handle") or "")!=match["handle"]:
            record["status"]="DSPACE_ORIGINAL_ITEM_IDENTITY_CHANGED"
            continue
        record["dspace_original_title"]=match["title"]
        record["dspace_original_handle"]=match["handle"]
        record["dspace_item_uuid_verified"]=True
        bundles=get_public_json(ROOT+f"/core/items/{item_id}/bundles",contract,items={item_id})
        if bundles["status"]!="PUBLIC_METADATA_JSON_VERIFIED":
            record["status"]="ORIGINAL_BUNDLE_METADATA_UNAVAILABLE"
            continue
        eligible=[b for b in bundle_items(bundles["data"],"bundles")
                  if b.get("name")=="ORIGINAL" and UUID_RE.fullmatch(str(b.get("uuid") or ""))]
        if len(eligible)!=1:
            record["status"]="ORIGINAL_BUNDLE_NOT_UNIQUE"
            continue
        uuid=str(eligible[0]["uuid"])
        files=get_public_json(ROOT+f"/core/bundles/{uuid}/bitstreams",contract,bundles={uuid})
        if files["status"]!="PUBLIC_METADATA_JSON_VERIFIED":
            record["status"]="ORIGINAL_PUBLIC_FILE_METADATA_UNAVAILABLE"
            continue
        bitstreams=bundle_items(files["data"],"bitstreams")
        record.update({
           "status":"ORIGINAL_PUBLIC_ARCHIVE_BUNDLE_FILE_METADATA_VERIFIED",
           "source_public_file_count":len(bitstreams),
           "file_extensions_and_sizes":source_files(bitstreams),
           "original_source_file_bytes_downloaded":False
        })
    full=sum(r["status"]=="ORIGINAL_PUBLIC_ARCHIVE_BUNDLE_FILE_METADATA_VERIFIED" for r in recs)
    return {
      "date":contract["frozen_at"],
      "status":"V7_BARNACLE_ORIGINAL_PUBLIC_ARCHIVE_METADATA_SCREEN_COMPLETED",
      "original_reference":"Kölzsch et al 2015 J Anim Ecol DOI 10.1111/1365-2656.12281",
      "doi_recognized":sum(r["status"]!="DATACITE_SOURCE_NOT_VERIFIED" for r in recs),
      "dspace_discovery_status":"PUBLIC_METADATA_JSON_VERIFIED" if all(
        s["status"]=="PUBLIC_METADATA_JSON_VERIFIED" for s in searches)
        else "ONE_OR_MORE_PUBLIC_SOURCE_SEARCHES_FAILED",
      "n_discovered_barnacle_related_public_items":len(discovered),
      "source_archives":recs,
      "n_original_archives_with_file_manifest":full,
      "all_three_manifest_verified":full==3,
      "individual_tracking_rows_read":False,
      "original_GPS_archive_downloaded":False,
      "focal_v7_environmental_q_U_effect_estimated":False,
      "Aikens_frozen_outcomes_opened":False,
      "no_ebird":True,
      "prior_art_boundary":"Source availability is not the V7 q×U biological interaction. The original publication already studies phenology predictability and migration timing and V7 itself is preoutcome."
    }

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--contract",type=Path,default=Path(__file__).resolve().parents[1]/"data/payoff_b_v7_barnacle_archive_metadata_contract_20261124.json")
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    c=json.loads(args.contract.read_text())
    obj=audit(c)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+"\n")
    print("PAYOFF_B_V7_BARNACLE_ORIGINAL_SOURCE="+json.dumps(obj,separators=(",",":"),ensure_ascii=False))

if __name__=="__main__":
    main()
