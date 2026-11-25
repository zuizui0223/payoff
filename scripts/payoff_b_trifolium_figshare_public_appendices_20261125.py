#!/usr/bin/env python3
"""Verify public CC0 Geib & Galen appendices via documented Figshare API.
No change to duplicate-species quarantine or new biological fit.
"""
import hashlib,json,re,sys
from pathlib import Path
import requests
from bs4 import BeautifulSoup
from payoff_b_interaction_buffering_small_dryad_gate_20261125 import fetch,Hold

FILES={
"A":(3553704,5622411,"appendix-A.htm",73789,"e3fc793b003b6572402308bbe71dde80"),
"B":(3553701,5622408,"appendix-B.htm",60950,"9ec547207aa02ac99b27a710d90a2d66"),
"C":(3553698,5622405,"appendix-C.htm",30534,"66433a1664e6e072b5abeef7ab0c9838")}
def inspect(b,k):
    h=BeautifulSoup(b,"html.parser")
    tables=[]
    for i,t in enumerate(h.find_all("table")):
        rows=[[v.get_text(" ",strip=True) for v in tr.find_all(["td","th"],recursive=False)] for tr in t.find_all("tr")]
        rows=[r for r in rows if r]
        caption=t.find("caption")
        # Numeric source tables / short labels only. CC0 original source.
        ctx=[]
        for prev in t.find_all_previous(["p","h1","h2","h3","h4"],limit=6):
            s=prev.get_text(" ",strip=True)
            if re.search(r"\bTable\s+[ABC]\d|seed|germin|pollin|flower",s,re.I):ctx.append(s[:240])
            if re.search(r"\bTable\s+[ABC]\d",s,re.I):break
        tables.append({"ordinal":i+1,"caption":caption.get_text(" ",strip=True)[:200] if caption else None,"preceding_context":ctx[:2],"row_count":len(rows),
            "headers":rows[:2],"selected_rows":[r[:14] for r in rows[2:] if any(re.search(r"\d",v) for v in r)][:80] if k in ("B","C") else []})
    terms=["0.311","0.686","0.989","0.653","0.259489884","0.349874263","0.521003839"]
    txt=h.get_text(" ",strip=True)
    return {"html_table_count":len(tables),"image_elements":len(h.find_all("img")),
            "exact_compiled_tokens":{t:len(re.findall(r"(?<![\d.])"+re.escape(t)+r"(?![\d.])",txt)) for t in terms},
            "tables":tables}
def run():
    out={"status":"SOURCE_APPENDICES_ONLY_NO_MODEL","doi":"10.1890/11-1271.1","files":{},"trifolium_quarantine_unchanged":True}
    with requests.Session() as s:
        for k,(aid,fid,name,size,md5) in FILES.items():
            z=out["files"][k]={"article_id":aid,"file_id":fid,"name":name,"expected_md5":md5,"expected_bytes":size}
            try:
                m=json.loads(fetch(s,f"https://api.figshare.com/v2/articles/{aid}",cap=800000))
                if m.get("id")!=aid or m.get("license",{}).get("name")!="CC0":raise Hold("SOURCE_LICENSE_OR_ID")
                f=[v for v in m.get("files",[]) if v.get("id")==fid and v.get("name")==name and v.get("size")==size and v.get("computed_md5")==md5]
                if len(f)!=1:raise Hold("PINNED_METADATA_CHANGED")
                # Official Figshare public download endpoint:
                # https://info.figshare.com/user-guide/how-to-use-the-figshare-api/
                url=f"https://api.figshare.com/v2/file/download/{fid}"
                b=fetch(s,url,cap=200000)
                if len(b)!=size or hashlib.md5(b).hexdigest()!=md5:raise Hold("SOURCE_BYTES_MISMATCH")
                z.update(status="CC0_ORIGINAL_BYTES_VERIFIED",source_url=url,sha256=hashlib.sha256(b).hexdigest(),**inspect(b,k))
            except (Hold,ValueError,requests.RequestException,KeyError) as e:z.update(status="HOLD",error=str(e) if isinstance(e,Hold) else type(e).__name__)
    return out
if __name__=="__main__":
    d=run()
    print(json.dumps(d,ensure_ascii=True,separators=(",",":")),flush=True)
    p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2,ensure_ascii=True)+"\n")
