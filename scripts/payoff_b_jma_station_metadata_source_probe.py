"""Audit the official JMA ground-observation station metadata ZIP, without guessing ID joins."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
import urllib.request
import zipfile
from pathlib import Path

URL = "https://www.data.jma.go.jp/stats/data/mdrr/chiten/meta/smaster.index.zip"
LIMIT = 30_000_000


def audit_station_zip(raw: bytes) -> dict:
    if len(raw) > LIMIT:
        raise ValueError("Station metadata exceeds size bound")
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        members = [m for m in z.infolist() if not m.is_dir()]
        if len(members) > 30:
            raise ValueError("Unexpected number of metadata files")
        files = []
        for m in members:
            if m.file_size > 20_000_000:
                raise ValueError("Unexpected metadata member size")
            payload = z.read(m)
            samples = {}
            for enc in ("utf-8-sig", "cp932", "shift_jis"):
                try:
                    samples[enc] = payload[:600].decode(enc)
                except UnicodeDecodeError:
                    pass
            files.append({
                "filename": m.filename, "size": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
                "first_600_byte_decoding_candidates": samples,
                "format_admitted": False,
                "phenology_station_id_crosswalk_admitted": False,
            })
    return {
        "source": URL,
        "archive_sha256": hashlib.sha256(raw).hexdigest(),
        "member_count": len(files),
        "files": files,
        "status": "METADATA_BYTES_VERIFIED_SCHEMA_AND_ID_CROSSWALK_PENDING",
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    req = urllib.request.Request(URL, headers={"User-Agent": "PAYOFF-B-JMA-station-source-audit/1.0"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw = resp.read(LIMIT + 1)
    receipt = audit_station_zip(raw)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"member_count": receipt["member_count"], "archive_sha256": receipt["archive_sha256"], "file_summaries": [{"filename": x["filename"], "size": x["size"], "encoding_candidates": list(x["first_600_byte_decoding_candidates"])} for x in receipt["files"]]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
