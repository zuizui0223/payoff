"""Locate author/publisher-linked Kölzsch historical GDD spring-onset supplement.

Never guess a private file endpoint or substitute goose movement outcomes for
historical phenology. Only follow EXACT downloadable supporting-info hrefs
advertised in a public, official Wiley article page; fail closed on 403.
If an actual public docx is returned, identify Tables S1-S7 and source hash.
No V7 q×U coefficients; no raw copyrighted supplement redistributed.
"""
import argparse,hashlib,io,json,re,zipfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin,urlparse
from xml.etree import ElementTree as ET
from scripts.payoff_b_scotland_resource_source_probe import open_url

PAGES=[
 "https://besjournals.onlinelibrary.wiley.com/doi/10.1111/1365-2656.12281",
 "https://onlinelibrary.wiley.com/doi/10.1111/1365-2656.12281/abstract",
]
FILE_NAME="jane12281-sup-0001-SuppInfo.docx"
ALLOWED={"besjournals.onlinelibrary.wiley.com","onlinelibrary.wiley.com"}
MAX_PAGE_BYTES=2_000_000
MAX_DOC_BYTES=2_000_000


class DocumentLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[]
    def handle_starttag(self,tag,attrs):
        if tag not in ("a","link"):
            return
        for k,v in attrs:
            if k=="href" and isinstance(v,str):
                self.links.append(v)


def source_href(page,href):
    if not href or FILE_NAME.lower() not in href.lower():
        return None
    u=urljoin(page,href)
    parsed=urlparse(u)
    if parsed.scheme!="https" or parsed.hostname not in ALLOWED:
        return None
    return u


def sample_docx(raw):
    if not zipfile.is_zipfile(io.BytesIO(raw)):
        return {"verified":False,"reason":"NOT_A_ZIP_DOCX"}
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        if "word/document.xml" not in z.namelist():
            return {"verified":False,"reason":"NO_WORD_BODY"}
        xml=z.read("word/document.xml")
    root=ET.fromstring(xml)
    ns={"w":"http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    texts=[]
    for p in root.findall(".//w:p",ns):
        t="".join(x.text or "" for x in p.findall(".//w:t",ns)).strip()
        if t:
            texts.append(t)
    headers=[]
    for i,t in enumerate(texts):
        if re.search(r"\bTable\s+S[1-7]\b",t,re.I):
            headers.append({"source_paragraph_index":i,
                "source_excerpt":t[:350],
                "next_text":texts[i+1][:300] if i+1<len(texts) else ""})
    return {"verified":True,"doc_paragraph_count":len(texts),
            "historical_gdd_tables_mentions":headers[:55],
            "all_S1_to_S7_identified":all(
               any(re.search(r"\bTable\s+S"+str(n)+r"\b",t,re.I)
                   for t in texts) for n in range(1,8)),
            "original_document_text_not_shared":True}


def audit():
    report={
        "status":"PAYOFF_B_V7_HISTORICAL_30YEAR_GDD_SUPPLEMENT_SOURCE_GATE",
        "paper_doi":"10.1111/1365-2656.12281",
        "known_publisher_supplement_filename":FILE_NAME,
        "official_pages":[],
        "v7_q_x_U_fitted":False,
        "historical_spring_q_derived_from_bird_arrival":False,
        "supplement_original_verified":False,
    }
    links=[]
    for page in PAGES:
        res=open_url(page,max_read=MAX_PAGE_BYTES,timeout=28)
        raw=res.get("body")
        info={"official_page":page,"http_status":res.get("http_status"),
              "content_type":res.get("content_type")}
        if not raw or res.get("http_status")!=200:
            info["source_page_status"]="NO_PUBLIC_PAGE_CONTENT"
        elif "html" not in str(res.get("content_type")).lower():
            info["source_page_status"]="NON_HTML_PUBLISHER_SOURCE"
        else:
            parser=DocumentLinks()
            parser.feed(raw.decode("utf-8",errors="replace"))
            for anchor in parser.links:
                href=source_href(page,anchor)
                if href and href not in links:
                    links.append(href)
            info["source_page_status"]="PUBLIC_HTML_READ"
            info["advertised_supplement_links"]=len(links)
            info["html_sha256"]=hashlib.sha256(raw).hexdigest()
        report["official_pages"].append(info)
    report["supplement_links_found_on_official_publisher_pages"]=links
    if not links:
        report["gate"]="HOLD_PUBLISHER_SUPPLEMENT_HREF_UNAVAILABLE"
        return report
    if len(links)>4:
        report["gate"]="NO_GO_AMBIGUOUS_MULTIPLE_SUPPLEMENTS"
        return report
    for link in links:
        res=open_url(link,max_read=MAX_DOC_BYTES,timeout=55)
        raw=res.get("body")
        row={"source_url":link,"http_status":res.get("http_status"),
             "content_type":res.get("content_type")}
        if raw and res.get("http_status")==200:
            row["size_bytes"]=len(raw)
            row["sha256"]=hashlib.sha256(raw).hexdigest()
            row["source_docx_schema"]=sample_docx(raw)
            row["source_verified"]=row["source_docx_schema"]["verified"]
        else:
            row["source_verified"]=False
        report.setdefault("source_supplements",[]).append(row)
    passed=any(x.get("source_verified") for x in report.get("source_supplements",[]))
    report["supplement_original_verified"]=passed
    report["gate"]="PUBLIC_PUBLISHER_SUPPLEMENT_VERIFIED" if passed \
       else "HOLD_ORIGINAL_GDD_SUPPLEMENT_NOT_DOWNLOADABLE"
    return report


def main():
    p=argparse.ArgumentParser();p.add_argument("--output",required=True,type=Path)
    args=p.parse_args()
    a=audit()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(a,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(a,separators=(",",":"),ensure_ascii=False))


if __name__=="__main__":
    main()
