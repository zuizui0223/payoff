#!/usr/bin/env python3
"""Encoding-only amendment for authenticated GloPL source-frame text screen."""
import csv, hashlib, io, json, re, sys
from collections import Counter
from pathlib import Path
import requests
import payoff_b_gezon_glopl_source_screen_20261125 as core
from payoff_b_interaction_buffering_small_dryad_gate_20261125 import fetch, Hold

def ascii_identity(value):
    # Reversible encoding of source bytes; never assert the author name's charset.
    return "".join(c if ord(c)<128 else f"\\x{ord(c):02x}" for c in value)

def amended(b):
    core.verify_git_blob(b)
    try:
        b.decode("utf-8-sig")
        raise Hold("EXPECTED_UTF8_FAILURE_NOT_REPRODUCED")
    except UnicodeDecodeError as e:
        diagnostic={"first_bad_byte_offset":e.start,"first_bad_byte_hex":b[e.start:e.end].hex(),
                    "nonascii_bytes":sum(x>=128 for x in b),"c1_bytes":sum(128<=x<=159 for x in b)}
    t=b.decode("latin-1")
    if t.encode("latin-1")!=b:raise Hold("BYTE_ROUNDTRIP_FAILURE")
    dialect=csv.Sniffer().sniff(t[:16000],delimiters=",;\t")
    r=csv.DictReader(io.StringIO(t),dialect=dialect)
    h=r.fieldnames
    if not h or len(set(h))!=len(h):raise Hold("CSV_HEADER")
    rows=list(r)
    if not rows or any(None in v or any(z is None for z in v.values()) for v in rows):
        raise Hold("CSV_ROW_SHAPE")
    context=[c for c in h if core.context_column(c)]
    identity=core.identity_columns(h)
    taxa=[c for c in h if re.search(r"species|taxon|genus|binomial",c,re.I)]
    # Exact same lexical pattern, ASCII word boundaries in a byte-preserving view.
    pat=re.compile(core.PATTERN.pattern,re.I|re.ASCII)
    hits=Counter();cand={};ge=cl=0
    coverage={c:sum(v[c].strip().lower() not in core.MISSING for v in rows) for c in context}
    for v in rows:
        ge+=any(re.search(r"\bgezon\b",v[c],re.I|re.ASCII) for c in identity)
        cl+=any(re.search(r"\bclaytonia\b",v[c],re.I|re.ASCII) for c in taxa)
        cc=[c for c in context if pat.search(v[c])]
        for c in cc:hits[c]+=1
        if not cc:continue
        key=tuple(v[c].strip() for c in identity)
        x=cand.setdefault(key,{"rows":0,"fields":set(),"terms":set()})
        x["rows"]+=1;x["fields"].update(cc)
        for c in cc:x["terms"].update(m.group(0).lower() for m in pat.finditer(v[c]))
    return {"status":"AUTHENTICATED_AUTHOR_SOURCE_FRAME_ONLY","rows":len(rows),"columns":h,
        "sha256":hashlib.sha256(b).hexdigest(),"git_blob_sha":core.GLOPL_BLOB,"bytes":len(b),
        "encoding_diagnostic":diagnostic,"encoding":"reversible Latin-1 byte view; author charset not inferred",
        "delimiter":dialect.delimiter,"context_columns":context,"identity_columns":identity,
        "taxon_columns":taxa,"context_nonmissing":coverage,"field_hit_counts":dict(hits),
        "matching_rows":sum(x["rows"] for x in cand.values()),"candidate_identity_groups":len(cand),
        "gezon_identity_matching_rows":ge,"claytonia_taxon_matching_rows":cl,
        "candidate_identities":[{"identity":dict(zip(identity,map(ascii_identity,k))),"rows":v["rows"],
              "matched_fields":sorted(v["fields"]),"matched_terms":sorted(v["terms"])} for k,v in sorted(cand.items())],
        "note":"ASCII lexical leads only; source preceding final curation; no numeric biological effect fitted."}

def run():
    out={"status":"SOURCE_FRAME_ONLY_NO_NEW_EFFECT","glopl":{"url":core.GLOPL_URL}}
    with requests.Session() as s:
        try:out["glopl"].update(amended(fetch(s,core.GLOPL_URL,cap=6_000_000)))
        except (Hold,ValueError,requests.RequestException,csv.Error,UnicodeError) as e:
            out["glopl"].update(status="HOLD",error=str(e) if isinstance(e,Hold) else type(e).__name__)
    print(json.dumps(out,indent=2,ensure_ascii=True),flush=True)
    return out
if __name__=="__main__":
    p=Path(sys.argv[1]);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(run(),indent=2,ensure_ascii=True)+"\n")
