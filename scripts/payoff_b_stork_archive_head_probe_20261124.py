#!/usr/bin/env python3
"""Public DOI/archive HEAD-only source gate for Bontekoe white-stork tracks.

Never uses credentials, follows third-party redirects, downloads animal
events, downloads archive ZIPs, or auto-accepts license terms.
A 200 landing-page response is NOT proof of tracking event-download access.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, build_opener, HTTPRedirectHandler


DEFAULT_CONTRACT=Path(__file__).resolve().parents[1] / "data/payoff_b_stork_social_opportunity_access_contract_20261124.json"

class RefuseRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None

def check_pinned_url(url, allowed):
    if url not in allowed:
        raise ValueError("Unregistered source address blocked")
    u=urlparse(url)
    if u.scheme!="https" or u.username or u.password or u.query or u.fragment:
        raise ValueError("Unsafe or non-public source URL")
    if u.hostname not in ("doi.org","datarepository.movebank.org"):
        raise ValueError("Unexpected source domain")

def metadata_head(url, allowed, opener=None):
    check_pinned_url(url,allowed)
    opener=opener or build_opener(RefuseRedirect())
    req=Request(url, method="HEAD", headers={
        "User-Agent":"PAYOFF-B-source-landing-HEAD-only/1.0",
        "Accept":"text/html,application/xml,*/*"
    })
    try:
        r=opener.open(req,timeout=20)
        status=int(r.status)
        headers=r.headers
        r.close()
        error_class=None
    except HTTPError as exc:
        status=int(exc.code)
        headers=exc.headers
        error_class=None
        exc.close()
    except (URLError,TimeoutError,OSError) as exc:
        return {"status":"TRANSPORT_NOT_VERIFIED",
                "exception_class":type(exc).__name__,
                "http_status":None,
                "original_hostname":urlparse(url).hostname,
                "no_response_body_read":True,
                "tracking_or_event_bytes_downloaded":False}
    redirect=str(headers.get("Location",""))
    target=urlparse(redirect)
    return {
        "status":"REDIRECT_ONLY" if 300<=status<400 else
                 "LANDING_HTTP_OK" if 200<=status<300 else
                 "LANDING_ACCESS_FAILURE",
        "http_status":status,
        "original_hostname":urlparse(url).hostname,
        "original_path":urlparse(url).path,
        "redirect_hostname":target.hostname,
        "redirect_path_type":"HANDLE_OR_DOI_PATH" if (
            target.path.startswith("/handle/") or target.path.startswith("/10.5441/")) else
            "OTHER_OR_EMPTY",
        "content_type":str(headers.get("Content-Type",""))[:80],
        "no_redirect_followed":True,
        "no_response_body_read":True,
        "tracking_or_event_bytes_downloaded":False,
    }


def audit(contract):
    archives=contract["2023_archives"]
    allowed={x["landing"] for x in archives}|{
        "https://doi.org/"+x["doi"] for x in archives
    }
    entries=[]
    for x in archives:
        entries.append({
          "cohort":x["cohort"],"original_doi":x["doi"],
          "doi_status":metadata_head("https://doi.org/"+x["doi"],allowed),
          "landing_status":metadata_head(x["landing"],allowed),
        })
    return {
        "date":contract["date"],
        "status":"ARCHIVE_EVENT_DOWNLOAD_NOT_VERIFIED",
        "original_paper_doi":"10.1098/rspb.2023.1268",
        "archive_status":entries,
        "public_license_metadata_previously_verified":all(
          x["cc0_metadata_verified"] for x in archives
        ),
        "original_license_terms_accepted":False,
        "events_or_tracking_files_downloaded":False,
        "tracking_source_rows_opened":False,
        "original_analysis_outcome_reopened":False,
        "file_level_direct_download_available":None,
        "social_cue_reliability_or_remain_recourse_estimated":False,
        "no_ebird":True,
        "conclusion":"HEAD status identifies only public landing/DOI transport. It does not establish actual file access or prove social-information data can be assembled."
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--contract",type=Path,default=DEFAULT_CONTRACT)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    c=json.loads(a.contract.read_text())
    z=audit(c)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(z,indent=2,ensure_ascii=False)+"\n")
    print("PAYOFF_STORK_ARCHIVE_HEAD_RECEIPT="+json.dumps(z,separators=(",",":"),ensure_ascii=False))

if __name__=="__main__":
    main()
