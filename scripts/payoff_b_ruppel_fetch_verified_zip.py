#!/usr/bin/env python3
"""Fetch the exact Figshare ZIP for a source-only RData object audit."""
import argparse
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

FILE_ID = 38968813
URL = f"https://ndownloader.figshare.com/files/{FILE_ID}"
MD5 = "e8fc27e9eb44aa1e89da09310183b39a"
SHA256 = "0ef08e19104aaceff5ef2700c324a094c49cbe2cd24ca198e3853b656d7744c6"
SIZE = 100303


def verify(data):
    if len(data) != SIZE or hashlib.md5(data).hexdigest() != MD5:
        raise ValueError("Figshare original ZIP size or MD5 changed")
    if hashlib.sha256(data).hexdigest() != SHA256:
        raise ValueError("Figshare original ZIP SHA256 changed")
    return True


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--out", default="outputs/.source-only-ruppel-2023.zip")
    args = p.parse_args()
    if args.self_test:
        assert len(MD5) == 32 and len(SHA256) == 64
        try:
            verify(b"synthetic")
        except ValueError:
            pass
        else:
            raise AssertionError("bad checksum accepted")
        print("RUPPEL_PINNED_ZIP_CHECKSUM_SYNTHETIC_PASS")
        return
    req = Request(URL, headers={"User-Agent":"PAYOFF-B-original-source-audit/1.0","Accept":"application/zip"})
    with urlopen(req, timeout=35) as r:
        if int(r.headers.get("Content-Length","0") or 0) > 150000:
            raise ValueError("unexpected Figshare archive size")
        raw = r.read(150001)
    verify(raw)
    outfile = Path(args.out)
    outfile.parent.mkdir(parents=True,exist_ok=True)
    outfile.write_bytes(raw)
    print("RUPPEL_ORIGINAL_BINARY_VERIFIED " + json.dumps({
        "doi":"10.6084/m9.figshare.c.6403996",
        "figshare_file_id":FILE_ID,
        "bytes":len(raw),
        "md5":MD5,
        "sha256":SHA256,
        "stored_for_schema_inspection_only":True,
    }))
    print("NO INDIVIDUAL OUTCOMES OR WEATHER EFFECTS INSPECTED")


if __name__=="__main__":
    main()
