#!/usr/bin/env python3
"""Inspect at most 8KiB of *HTML landing pages*, never archived tracking data.

Only three fixed, already-verified Bontekoe 2023 Movebank repository landing
pages are queried. No URL found in their HTML is followed. The output is only
metadata-level counts of file links, never tags, GPS rows or animal identifiers.
"""
from __future__ import annotations
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import urlparse,unquote
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError

CONTRACT = Path(__file__).resolve().parents[1] / "data/payoff_b_stork_social_opportunity_access_contract_20261124.json"
HTML_CAP = 8192

class LinkTypes(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs=[]
    def handle_starttag(self,tag,attrs):
        if tag.lower()!="a":
            return
        href=dict(attrs).get("href","")
        if isinstance(href,str):
            self.hrefs.append(href)

def summarize_html(html:bytes,content_type:str):
    if not content_type.lower().startswith("text/html"):
        raise ValueError("No HTML landing page; refusing binary or tracking data")
    parsed=LinkTypes()
    parsed.feed(html.decode("utf-8","replace"))
    suffixes={".csv",".zip",".txt",".xml",".json",".pdf"}
    references=[]
    for link in parsed.hrefs:
        path=unquote(urlparse(link).path.lower())
        file_suffix=next((x for x in suffixes if path.endswith(x)),None)
        if file_suffix:
            references.append(file_suffix)
    s=html.decode("utf-8","replace").lower()
    return {
       "parsed_anchor_count":len(parsed.hrefs),
       "linked_file_extension_counts":{e:references.count(e) for e in sorted(set(references))},
       "contains_literal_bitstream_href":any("/bitstream/" in t.lower() for t in parsed.hrefs),
       "contains_literal_file_download_href":any("download" in t.lower() for t in parsed.hrefs),
       "html_has_word_license":("license" in s),
       "body_has_word_tracking":("tracking" in s),
       "source_html_sample_only":True,
       "source_html_text_committed":False,
       "actual_linked_files_accessed":False,
    }

def read_landing(landing,allowed):
    if landing not in allowed or urlparse(landing).hostname!="datarepository.movebank.org":
        raise ValueError("Cannot inspect an unregistered source landing")
    req=Request(landing,headers={
        "Accept":"text/html","User-Agent":"PAYOFF-B-original-metadata-manifest/1.0"})
    try:
        with urlopen(req,timeout=20) as rsp:
            resolved=rsp.geturl()
            if urlparse(resolved).hostname!="datarepository.movebank.org":
                raise ValueError("Unexpected HTML redirect host")
            content_type=str(rsp.headers.get("Content-Type",""))
            if not content_type.lower().startswith("text/html"):
                raise ValueError("Not an HTML landing; file download refused")
            declared=rsp.headers.get("Content-Length")
            data=rsp.read(HTML_CAP)
            ret=summarize_html(data,content_type)
            ret.update({
               "status":"LANDING_FIRST_8K_HTML_INSPECTED",
               "http_status":rsp.status,
               "bytes_read":len(data),
               "source_declared_content_length":int(declared) if declared and declared.isdigit() else None,
               "truncated_or_remaining_content_possible":declared is None or (int(declared)>len(data)),
               "source_metadata_only":True,
            })
            return ret
    except (HTTPError,URLError,TimeoutError,OSError,ValueError) as exc:
        return {
          "status":"HTML_LANDING_CONTENT_NOT_VERIFIED",
          "exception_class":type(exc).__name__,
          "html_loaded":False,
          "actual_linked_files_accessed":False,
        }

def audit(c):
    archives=c["2023_archives"]
    allowed={x["landing"] for x in archives}
    result={"status":"LANDING_HTML_FIRST_8K_GATE_COMPLETE",
            "date":c["date"],
            "source_doi_family":"10.5441/001/1.271;10.5441/001/1.276;10.5441/001/1.277",
            "archive_pages":[{"cohort":x["cohort"],"doi":x["doi"],
                             "page":read_landing(x["landing"],allowed)}
                             for x in archives],
            "limit_bytes_per_original_landing":HTML_CAP,
            "original_GPS_files_downloaded":False,
            "tracking_events_queried":False,
            "link_destinations_followed":False,
            "original_user_terms_accepted":False,
            "social_predictive_reliability_or_payoff_estimated":False,
            "no_ebird":True,
            "claim_boundary":"Link filenames and HTML landing navigation do not verify the existence, license, direct-download permission, grain or temporally aligned information content of GPS files."
    }
    return result

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--contract",type=Path,default=CONTRACT)
    ap.add_argument("--output",type=Path,required=True)
    args=ap.parse_args()
    c=json.loads(args.contract.read_text())
    result=audit(c)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
    print("PAYOFF_STORK_HTML_MANIFEST_AUDIT="+json.dumps(result,separators=(",",":"),ensure_ascii=False))

if __name__=="__main__":
    main()
