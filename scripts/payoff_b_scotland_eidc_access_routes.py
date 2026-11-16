"""Public EIDC download-page link diagnosis; NEVER bypass licence/login.

Direct datastore paths returned 404, which may be a URL-layout issue rather
than restricted access. Follow only published EIDC page URLs, collect linked
official download routes, and inspect a bounded set of documented path forms.
"""
import argparse
import html.parser
import json
import re
from pathlib import Path
from urllib.parse import urljoin

from scripts.payoff_b_scotland_resource_source_probe import EIDC_ID, open_url

class Links(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs=[]
    def handle_starttag(self,tag,attrs):
        if tag in ("a","form"):
            k="href" if tag=="a" else "action"
            for a,v in attrs:
                if a==k and v and v not in self.hrefs:
                    self.hrefs.append(v)


def page(url):
    r=open_url(url,timeout=40,max_read=250_000)
    raw=r.pop("body",None)
    out={"url":url,**r}
    if not raw:
        return out
    out["byte_count"]=len(raw)
    if "html" not in str(r.get("content_type")).lower():
        out["content_is_not_html"]=True
        return out
    s=raw.decode("utf-8",errors="replace")
    p=Links()
    p.feed(s)
    out["title"]=re.search(r"<title[^>]*>(.*?)</title>",s,re.I|re.S).group(1).strip() if re.search(r"<title[^>]*>(.*?)</title>",s,re.I|re.S) else None
    out["visible_link_targets"]=[urljoin(url,x) for x in p.hrefs if x.startswith(("/","http"))][:80]
    out["login_or_licence_language"]=bool(re.search(r"login|log in|sign in|licen[cs]e|authorize|authenticat|register|access token",s,re.I))
    out["download_url_contexts"]=[s[max(0,m.start()-140):m.start()+260].replace("\n"," ") for m in list(re.finditer("download",s,re.I))[:9]]
    return out


def audit():
    core=f"https://data-package.ceh.ac.uk/data/{EIDC_ID}"
    base=f"https://catalogue.ceh.ac.uk/datastore/eidchub/{EIDC_ID}"
    urls={
        "packaged_dataset_landing":core,
        "packaged_zip_pattern":core+".zip",
        "catalogue_landing":f"https://catalogue.ceh.ac.uk/documents/{EIDC_ID}",
        "public_datastore_root":base+"/",
        "public_datastore_flat_bird_csv":base+"/bird_phenology.csv",
    }
    pages={k:page(v) if k in ("packaged_dataset_landing","catalogue_landing")
           else {"url":v,**open_url(v,method="HEAD",timeout=25)}
           for k,v in urls.items()}
    return {"status":"PAYOFF_B_EIDC_PUBLIC_DOWNLOAD_ROUTE_DIAGNOSTIC",
            "doi":"10.5285/b63d53ae-2fe7-4ce9-82a2-2325098489e3",
            "urls":pages,"no_auth_or_licence_bypass":True,
            "raw_fitness_source_acquired":False,"fitness_fitted":False}


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",type=Path,required=True)
    args=p.parse_args()
    r=audit()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(r,indent=2,ensure_ascii=False)+"\n")
    print(json.dumps(r,separators=(",",":"),ensure_ascii=False))

if __name__=="__main__":
    main()
