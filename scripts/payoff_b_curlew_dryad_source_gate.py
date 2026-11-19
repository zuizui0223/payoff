#!/usr/bin/env python3
"""Dryad 2026 Curlew source-only gate (no new nest-success outcome fit).

Read-only public Dryad REST API. Attempts small README and HTTP byte-range ZIP
central-directory access, not a 591MB full archive download. Fails closed if
anonymous API or HTTP ranges are unavailable. Emits aggregate counts only,
never bird identifiers, exact sites, GPS rows or raw phenotypes.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import re
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import quote

import requests

DOI = "doi:10.5061/dryad.31zcrjf22"
BASE = "https://datadryad.org/api/v2"
DATASET_API = f"{BASE}/datasets/{quote(DOI, safe='')}"
ARCHIVE_NAME = "Curlew_COE_habitat.zip"
README_NAME = "README.md"
TARGET_CSV = "dt_hab_Curlew.csv"
TIMEOUT = (12, 50)
MAX_REQUESTS = 90
MAX_RANGED_BYTES = 6_000_000
MAX_CSV_BYTES = 10_000_000
EXPECTED_SOURCE_FIELDS = {
    "ID_seas", "Bird_ID", "Sex", "Non_gr", "Br_gr", "Nest_succ",
    "Dist", "Prebr", "st_grass", "st_wetland"
}
ADMISSION = {
    "min_repeated_birds": 30,
    "min_birds_with_success_switch": 20,
    "min_repeated_birds_with_nonzero_Prebr_change": 20,
    "min_documented_years": 3,
}

class AccessHold(RuntimeError):
    pass


class LimitedSession:
    def __init__(self):
        self.session = requests.Session()
        self.n_requests = 0

    def get(self, url, **kwargs):
        self.n_requests += 1
        if self.n_requests > MAX_REQUESTS:
            raise AccessHold("REQUEST_LIMIT_FAIL_CLOSED")
        kwargs.setdefault("timeout", TIMEOUT)
        kwargs.setdefault("allow_redirects", True)
        return self.session.get(url, **kwargs)


class RangeFile(io.RawIOBase):
    """Small, bounded read-only seeks for a published public ZIP."""

    def __init__(self, client: LimitedSession, url: str):
        super().__init__()
        self.client, self.url = client, url
        self.position = 0
        with client.get(url, headers={"Range":"bytes=0-0"},
                        stream=True) as response:
            if response.status_code != 206:
                raise AccessHold(f"ZIP_HTTP_RANGE_NOT_AVAILABLE_STATUS_{response.status_code}")
            rng=response.headers.get("Content-Range","")
            match=re.match(r"^bytes 0-0/(\d+)$",rng)
            if match is None:
                raise AccessHold("ZIP_CONTENT_RANGE_HEADER_NOT_VERIFIABLE")
            self.total_bytes=int(match.group(1))
            if self.total_bytes < 1000 or self.total_bytes > 700_000_000:
                raise AccessHold("ZIP_LENGTH_NOT_WITHIN_SOURCE_EXPECTATION")

    def seekable(self):
        return True

    def readable(self):
        return True

    def tell(self):
        return self.position

    def seek(self, offset, whence=io.SEEK_SET):
        if whence==io.SEEK_SET: new=offset
        elif whence==io.SEEK_CUR: new=self.position+offset
        elif whence==io.SEEK_END: new=self.total_bytes+offset
        else: raise ValueError("Invalid ZIP seek")
        if new < 0: raise ValueError("Negative ZIP seek")
        self.position=new
        return new

    def read(self, size=-1):
        if size is None or size < 0:
            size=self.total_bytes-self.position
        if size==0 or self.position>=self.total_bytes:
            return b""
        if size > MAX_RANGED_BYTES:
            raise AccessHold("ZIP_RANGE_REQUEST_TOO_LARGE_NO_FULL_DOWNLOAD")
        start=self.position
        end=min(self.total_bytes-1,start+size-1)
        with self.client.get(self.url,headers={"Range":f"bytes={start}-{end}"},
                             stream=True) as response:
            if response.status_code!=206:
                raise AccessHold(f"ZIP_RANGE_READ_STATUS_{response.status_code}")
            needed=end-start+1
            data=response.content
            if len(data)!=needed:
                raise AccessHold("ZIP_RANGE_READ_LENGTH_MISMATCH")
        self.position=end+1
        return data


def _fetch_json(client, url):
    with client.get(url, stream=True) as r:
        if r.status_code!=200:
            raise AccessHold(f"PUBLIC_DRYAD_API_HTTP_{r.status_code}")
        if int(r.headers.get("Content-Length",0) or 0)>2_000_000:
            raise AccessHold("DRYAD_METADATA_TOO_LARGE")
        data=r.content
    if len(data)>2_000_000:
        raise AccessHold("DRYAD_METADATA_BODY_TOO_LARGE")
    return json.loads(data)


def _records(obj):
    """Public Dryad HAL envelopes can use varying embedded collection labels."""
    if isinstance(obj,dict):
        if ("id" in obj or "_links" in obj) and any(
            k in obj for k in ("path","filename","name")
        ):
            yield obj
        for v in obj.values():
            yield from _records(v)
    elif isinstance(obj,list):
        for v in obj:
            yield from _records(v)


def _name(item):
    return str(item.get("path") or item.get("filename") or item.get("name") or "").split("/")[-1]


def _file_id(item):
    v=item.get("id")
    if isinstance(v,(int,str)) and str(v).isdigit():
        return int(v)
    # Official Dryad v2 files HAL records in this published dataset omit
    # scalar "id" and expose the file identifier only in _links.self.href.
    # Parse that provider path; never synthesize an ID from filename/order.
    links=item.get("_links",{})
    if isinstance(links,dict):
        for row in links.values():
            if isinstance(row,dict):
                href=str(row.get("href",""))
                match=re.search(r"/(?:files|versions)/(\d+)(?:[/?#]|$)",href)
                if match:
                    return int(match.group(1))
    return None


def discover(client):
    dataset=_fetch_json(client,DATASET_API)
    versions=_fetch_json(client,DATASET_API+"/versions")
    ids=[]
    found_shapes=[]
    # Current Dryad HAL version entries can identify the version by an ID,
    # versionId or self-link href; do not guess the newest version if no
    # original version identifier can be verified.
    def scan_versions(v):
        if isinstance(v,dict):
            has_version = any(k in v for k in (
                "versionNumber","versionStatus","version","versionId",
                "version_id","version_number"
            ))
            if has_version:
                vid=_file_id(v)
                if vid is None:
                    raw=v.get("versionId") or v.get("version_id")
                    if raw is not None and str(raw).isdigit():
                        vid=int(raw)
                if vid is None:
                    # HAL self links are canonical provider identifiers.
                    links=v.get("_links",{})
                    if isinstance(links,dict):
                        paths=[
                            z.get("href","") for z in links.values()
                            if isinstance(z,dict) and "href" in z
                        ]
                        for href in paths:
                            m=re.search(r"/versions/(\d+)(?:\?|$)",str(href))
                            if m:
                                vid=int(m.group(1))
                                break
                found_shapes.append(",".join(sorted(k for k in v.keys()
                     if k.lower() in {"id","versionnumber","versionstatus","version","versionid","version_id"})))
                if vid is not None:
                    ids.append((v.get("versionNumber",v.get("version_number",0)),vid))
            for val in v.values(): scan_versions(val)
        elif isinstance(v,list):
            for val in v: scan_versions(val)
    scan_versions(versions)
    if not ids:
        toplist=",".join(sorted(versions.keys())) if isinstance(versions,dict) else type(versions).__name__
        raise AccessHold(
            "DRYAD_PUBLIC_VERSION_NOT_RESOLVED:"
            f"top={toplist};version_shapes={';'.join(found_shapes[:3])}"
        )
    # Use the latest original published version's validated integer ID.
    id_version=max(ids,key=lambda t:(int(t[0]) if str(t[0]).isdigit() else 0,t[1]))[1]
    details=_fetch_json(client,f"{BASE}/versions/{id_version}/files")
    items=list(_records(details))
    unique={}
    for item in items:
        fid=_file_id(item)
        if fid is not None and _name(item):
            unique[fid]=item
    files=[{
        "file_id":k,
        "filename":_name(v),
        "provider_size_bytes":v.get("size") or v.get("sizeBytes"),
        "provider_md5_reported_not_verified":v.get("digest") or v.get("md5"),
    } for k,v in unique.items()]
    if not any(x["filename"]==ARCHIVE_NAME for x in files):
        # Explicit original metadata-shape diagnosis before changing a
        # version selector or guessing an alternate data archive.
        embedded=details.get("_embedded",{}) if isinstance(details,dict) else {}
        collections={
            str(k): {
                "type":type(v).__name__,
                "first_entry_keys":sorted(list(v[0].keys()))[:20]
                    if isinstance(v,list) and v and isinstance(v[0],dict) else [],
                "first_entry_file_name":str(
                    v[0].get("path") or v[0].get("filename") or v[0].get("name") or ""
                )[:120] if isinstance(v,list) and v and isinstance(v[0],dict) else ""
            } for k,v in embedded.items()
        } if isinstance(embedded,dict) else {}
        reason=json.dumps({
            "reason":"DRYAD_ARCHIVE_NOT_FOUND_IN_ORIGINAL_VERSION",
            "version_id":id_version,
            "top_level_response_keys":sorted(details.keys()) if isinstance(details,dict) else [],
            "embedded_collection_shape":collections,
            "parsed_file_count":len(files),
            "parsed_public_filenames":[f["filename"] for f in files[:6]],
        },ensure_ascii=False,separators=(",",":"))
        raise AccessHold(reason)
    return {
        "dataset_title":dataset.get("title"),
        "dataset_identifier":dataset.get("identifier"),
        "source_doi":DOI,
        "dataset_publication_date":dataset.get("publicationDate"),
        "dataset_license":dataset.get("license"),
        "version_id":id_version,
        "file_manifest":files,
    }


def _parse_number(value):
    if value is None:
        return None
    s=str(value).strip()
    if not s or s.lower() in {"na","nan","null","n/a"}:
        return None
    if "," in s and "." not in s:
        s=s.replace(",",".")
    try:
        v=float(s)
    except ValueError:
        raise ValueError("Non-numeric source field")
    if not math.isfinite(v):
        raise ValueError("Nonfinite source field")
    return v


def _parse_year(id_seas: str):
    # README says composite bird + year but does not document exact syntax.
    # Only a clearly delimited trailing four-digit YYYY is accepted.
    m=re.search(r"(?:_|-|\s)(20(?:1[6-9]|2[0-5]))$",id_seas)
    return int(m.group(1)) if m else None


def summarize_original_csv(raw_bytes: bytes) -> dict:
    if len(raw_bytes)>MAX_CSV_BYTES:
        raise ValueError("Published derived CSV exceeds 10MB source guard")
    try:
        content=raw_bytes.decode("utf-8-sig")
    except UnicodeDecodeError:
        content=raw_bytes.decode("cp1252")
    reader=csv.DictReader(io.StringIO(content),delimiter=";")
    if reader.fieldnames is None or not EXPECTED_SOURCE_FIELDS.issubset(set(reader.fieldnames)):
        raise ValueError("Source semicolon schema / original columns mismatch")
    if any(field.startswith("Unnamed:") for field in reader.fieldnames):
        # Keep provider text exact; extra unnamed columns are a warning only.
        pass
    records=list(reader)
    if not records:
        raise ValueError("No original bird/season source records")
    unique_ids=set()
    bird_years=defaultdict(set)
    bird_success=defaultdict(set)
    bird_prebr=defaultdict(set)
    sex_count,breeding_count,outcome_count=Counter(),Counter(),Counter()
    bad_success=0
    parsed_years=[]
    missing={"Bird_ID":0,"ID_seas":0,"Prebr":0,"Nest_succ":0,"Dist":0}
    habitat_fields=[f for f in reader.fieldnames if f.startswith(("st_","br_","non_"))]
    for r in records:
        bird=str(r["Bird_ID"] or "").strip()
        season=str(r["ID_seas"] or "").strip()
        if not bird or not season:
            missing["Bird_ID"]+=not bool(bird)
            missing["ID_seas"]+=not bool(season)
            continue
        unique_ids.add(bird)
        bird_years[bird].add(season)
        yy=_parse_year(season)
        if yy is not None: parsed_years.append(yy)
        success=_parse_number(r["Nest_succ"])
        if success is None:
            missing["Nest_succ"]+=1
        elif success not in (0,1):
            bad_success+=1
        else:
            bird_success[bird].add(int(success))
            outcome_count[int(success)]+=1
        prebr=_parse_number(r["Prebr"])
        if prebr is None: missing["Prebr"]+=1
        elif prebr<0:
            raise ValueError("Negative source Prebr is not arrival-to-incubation time")
        else: bird_prebr[bird].add(prebr)
        dist=_parse_number(r["Dist"])
        if dist is None: missing["Dist"]+=1
        elif dist<0: raise ValueError("Negative source migration distance")
        sex_count[str(r["Sex"] or "").strip()]+=1
        breeding_count[str(r["Br_gr"] or "").strip()]+=1
        for key in habitat_fields:
            v=_parse_number(r.get(key))
            if v is not None and not (0<=v<=1):
                raise ValueError("Source habitat use proportion out of bounds")
    repeated={k for k,v in bird_years.items() if len(v)>=2}
    switched=sum(len(bird_success.get(k,set()))==2 for k in repeated)
    varied_prebr=sum(len(bird_prebr.get(k,set()))>=2 for k in repeated)
    n_unique_seasons=len({r["ID_seas"] for r in records if r.get("ID_seas")})
    n_distinct_years=len(set(parsed_years))
    years_unambiguous=len(parsed_years)==len(records)
    enough=(
        len(repeated)>=ADMISSION["min_repeated_birds"]
        and switched>=ADMISSION["min_birds_with_success_switch"]
        and varied_prebr>=ADMISSION["min_repeated_birds_with_nonzero_Prebr_change"]
        and years_unambiguous
        and n_distinct_years>=ADMISSION["min_documented_years"]
        and bad_success==0
    )
    return {
        "csv_sha256_exact_extracted_raw_bytes":hashlib.sha256(raw_bytes).hexdigest(),
        "n_original_derived_rows":len(records),
        "n_unique_source_ID_seas":n_unique_seasons,
        "n_unique_Bird_ID":len(unique_ids),
        "n_birds_with_two_or_more_distinct_season_IDs":len(repeated),
        "n_repeated_birds_with_both_success_values":switched,
        "n_repeated_birds_with_Prebr_change":varied_prebr,
        "n_distinct_suffix_years_under_conservative_rule":n_distinct_years,
        "n_rows_with_unambiguous_source_year_suffix":len(parsed_years),
        "year_suffix_fully_parseable":years_unambiguous,
        "n_duplicate_original_ID_seas_rows":len(records)-n_unique_seasons,
        "sex_row_counts":dict(sex_count),
        "breeding_group_row_counts":dict(breeding_count),
        "source_nest_success_binary_counts":{str(k):v for k,v in outcome_count.items()},
        "n_invalid_source_nest_success_values":bad_success,
        "source_missing_counts":missing,
        "habitat_fraction_columns_screened":len(habitat_fields),
        "within_individual_observational_gate":"DESIGN_SUPPORT_ONLY_ELIGIBLE_NOT_YET_FITTED" if enough
            else "NOT_IDENTIFIABLE_UNDER_FROZEN_MINIMUM_SUPPORT",
        "within_individual_effect_fitted":False,
        "actual_predecision_cue_observed":False,
        "actual_independently_measured_actionability":False,
        "direct_PAYOFF_B_information_deadline":"NOT_ESTIMABLE",
    }


def audit():
    out={
        "as_of":"2026-11-19",
        "analysis":"CURLEW_SOURCE_ONLY_NO_BIOLOGICAL_MODEL",
        "source":"Dryad doi:10.5061/dryad.31zcrjf22",
        "readme_source_author_reported_n_birds":124,
        "readme_source_author_reported_n_periods":233,
        "source_author_2016_2025":True,
        "source_code_readme_has_Prebr_as_existing_model_covariate":True,
        "source_reported_nest_success_inferred_from_individual_GPS":True,
        "source_sensitive_breeding_coordinates_redacted":True,
        "source_summary_is_fitness_to_age_one":False,
        "no_raw_identifier_or_sensitive_GPS_export":True,
        "no_full_archive_download_if_HTTP_range_unsupported":True,
        "source_original_zip_sha256_verified":False,
        "source_original_readme_sha256_verified":False,
        "original_source_record_grain_verified":False,
        "source_access_status":"NOT_RUN",
        "direct_PAYOFF_B_information_deadline":"NOT_ESTIMABLE",
        "frozen_support_thresholds":ADMISSION,
    }
    client=LimitedSession()
    try:
        meta=discover(client)
        out["public_dryad_metadata"]=meta
        files={f["filename"]:f for f in meta["file_manifest"]}
        # Public file downloads without a user account; never try other routes
        # when the provider denies this official /files/{id}/download endpoint.
        if README_NAME in files:
            fid=files[README_NAME]["file_id"]
            with client.get(f"{BASE}/files/{fid}/download",stream=True) as r:
                out["README_public_download_HTTP_status"]=r.status_code
                if r.status_code==200 and int(r.headers.get("Content-Length",0) or 0)<120_000:
                    data=r.content
                    if len(data)<120_000:
                        out["README_downloaded_sha256"]=hashlib.sha256(data).hexdigest()
                        out["source_original_readme_sha256_verified"]=False
                        out["README_exact_original_bytes_retrieved"]=True
                        out["README_declares_semicolon_CSV"]=(
                            "semicolon-delimited" in data.decode("utf-8","replace")
                        )
        zipid=files[ARCHIVE_NAME]["file_id"]
        with RangeFile(client,f"{BASE}/files/{zipid}/download") as remote:
            out["remote_zip_provider_content_range_size_bytes"]=remote.total_bytes
            with zipfile.ZipFile(remote) as z:
                hits=[x for x in z.infolist()
                      if x.filename.replace("\\","/").split("/")[-1]==TARGET_CSV]
                if len(hits)!=1:
                    raise AccessHold("ZIP_TARGET_DERIVED_CSV_NOT_UNIQUELY_PRESENT")
                info=hits[0]
                if info.file_size>MAX_CSV_BYTES:
                    raise AccessHold("ORIGINAL_DERIVED_CSV_EXCEEDS_SIZE_GUARD")
                with z.open(info,"r") as h:
                    original_csv=h.read(MAX_CSV_BYTES+1)
                    if len(original_csv)>MAX_CSV_BYTES:
                        raise AccessHold("CSV_DECOMPRESSION_EXCEEDS_GUARD")
                out["original_derived_csv_record_grain"]=summarize_original_csv(original_csv)
                out["original_source_record_grain_verified"]=True
                out["source_access_status"]="PUBLIC_RANGE_DERIVED_CSV_ACQUIRED"
    except (AccessHold,ValueError,KeyError,zipfile.BadZipFile,
            requests.RequestException,TimeoutError) as e:
        out["source_access_status"]="SOURCE_ACCESS_OR_STRUCTURE_HOLD"
        out["source_hold_reason"]=str(e)[:1700]
    out["number_of_public_HTTP_requests"]=client.n_requests
    return out


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--output",required=True,type=Path)
    args=p.parse_args()
    result=audit()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    print(json.dumps({
      "access":result["source_access_status"],
      "reason":result.get("source_hold_reason"),
      "source_grain":result.get("original_derived_csv_record_grain"),
      "n_requests":result["number_of_public_HTTP_requests"],
      "direct_information_deadline":"NOT_ESTIMABLE",
    },ensure_ascii=False))


if __name__=="__main__":
    main()
