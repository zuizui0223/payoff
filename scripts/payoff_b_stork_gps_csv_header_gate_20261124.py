#!/usr/bin/env python3
"""Read only first CSV header line(s) through strict HTTP Range ZIP file view.

No original GPS event values, individual tag IDs, locations, zip filenames or
whole files are stored or emitted. The parser may decompress an internal
bounded buffer to locate the header, but never publishes a row. No q/r fitted.
"""
from __future__ import annotations
import argparse,csv,io,json,sys,zipfile
from pathlib import Path
from urllib.error import HTTPError,URLError
from urllib.parse import urlparse
from urllib.request import Request,build_opener

HERE=Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0,str(HERE))
from payoff_b_stork_dspace_file_metadata_20261124 import (
    get_metadata,bundle_entries,bitstream_entries,UUID_RE
)
from payoff_b_stork_gps_zip_range_gate_20261124 import select_gps_zip,NoRedirect

CONTRACT=HERE.parent/"data/payoff_b_stork_gps_csv_header_contract_20261124.json"


class BoundedRemoteZipFile:
    """Minimal noncaching seekable file; never read more than declared cap."""
    def __init__(self,url,size,limits,opener=None):
        self.url=url;self.size=size;self.pos=0
        self.opener=opener or build_opener(NoRedirect())
        self.per_request=limits["max_original_request_bytes"]
        self.max_total=limits["max_total_compressed_zip_bytes_read_per_cohort"]
        self.max_calls=limits["max_http_range_calls_per_cohort"]
        self.bytes_used=0;self.calls=0;self.closed=False

    def tell(self):
        return self.pos

    def seekable(self):
        return True

    def readable(self):
        return True

    def seek(self,offset,whence=0):
        if whence==0:position=offset
        elif whence==1:position=self.pos+offset
        elif whence==2:position=self.size+offset
        else:raise ValueError("Unrecognized file seek mode")
        if not 0<=position<=self.size:
            raise ValueError("Out of bounded virtual archive offset")
        self.pos=position
        return self.pos

    def read(self,n=-1):
        if self.closed:
            raise ValueError("Remote ZIP view already closed")
        if n is None or n<0:
            n=self.size-self.pos
        n=min(n,self.size-self.pos)
        if n==0:return b""
        if n>self.per_request or self.bytes_used+n>self.max_total or self.calls>=self.max_calls:
            raise ValueError("Original remote ZIP read exceeded frozen strict Range budget")
        start=self.pos
        end=start+n-1
        req=Request(self.url,headers={
            "Range":f"bytes={start}-{end}",
            "Accept":"application/zip,application/octet-stream,*/*",
            "User-Agent":"PAYOFF-B-public-CC0-GPS-header-only/1.0"})
        try:
            with self.opener.open(req,timeout=25) as resp:
                if int(resp.status)!=206:
                    raise ValueError("Server ignored Range; refuse to read archive body")
                u=urlparse(resp.geturl())
                src=urlparse(self.url)
                if u.hostname!="datarepository.movebank.org" or u.path!=src.path:
                    raise ValueError("Source content redirected to unsupported host")
                cr=str(resp.headers.get("Content-Range",""))
                if cr!=f"bytes {start}-{end}/{self.size}":
                    raise ValueError("Archive HTTP Content-Range outside exact request")
                data=resp.read(n+1)
        except HTTPError as e:
            status=e.code
            e.close()
            raise ValueError(f"Source HTTP Range rejected: {status}") from None
        except (URLError,TimeoutError,OSError) as e:
            raise ValueError(f"Original source Range network failure {type(e).__name__}") from None
        if len(data)!=n:
            raise ValueError("Source Range returned unexpected byte count")
        self.pos+=len(data)
        self.calls+=1
        self.bytes_used+=len(data)
        return data

    def close(self):
        self.closed=True


def safe_member_header(stream,source_info,contract):
    if source_info.flag_bits&0x1:
        return {"status":"ENCRYPTED_ZIP_MEMBER_NOT_ADMITTED"}
    if source_info.compress_type!=zipfile.ZIP_DEFLATED:
        return {"status":"UNSUPPORTED_COMPRESSION"}
    # The following produces at most 4KiB of uncompressed source text and
    # throws away everything except the CSV's FIRST header line.
    with stream.open(source_info,"r") as f:
        first=f.readline(contract["metadata_scope"]["max_csv_header_bytes"])
    if not first or b"\n" not in first:
        return {"status":"FIRST_CSV_HEADER_NOT_BOUNDED_OR_INCOMPLETE"}
    header=first.decode("utf-8-sig",errors="replace").rstrip("\r\n")
    columns=next(csv.reader([header]))
    if not 1<=len(columns)<=contract["metadata_scope"]["max_column_count"]:
        return {"status":"CSV_COLUMN_COUNT_OUTSIDE_SOURCE_GATE",
                "n_fields":len(columns)}
    # Field names are public schema, never publish any data row or member name.
    clean=[str(c).strip()[:100] for c in columns]
    lower={x.lower().replace("_","-") for x in clean}
    return {
      "status":"FIRST_LINE_PUBLIC_CSV_SCHEMA_RECOVERED",
      "n_csv_columns":len(columns),
      "source_column_names":clean,
      "has_timestamp":any("timestamp" in x for x in lower),
      "has_tag_identifier":any("tag-local-identifier" in x or "tag-id"==x for x in lower),
      "has_individual_identifier":any("individual-local-identifier" in x or "individual-id"==x for x in lower),
      "has_latitude":any("location-lat" in x for x in lower),
      "has_longitude":any("location-long" in x for x in lower),
      "source_event_rows_returned":False,
      "original_member_name_returned":False,
    }


def inspect_one_zip(selection,cohort,contract):
    s=contract["observed_original_directory"][cohort]
    if selection["size_bytes"]!=s["gps_zip_bytes"]:
        raise ValueError("Source archive differs from previously verified ZIP directory")
    view=BoundedRemoteZipFile(selection["url"],selection["size_bytes"],contract["transport"])
    try:
        with zipfile.ZipFile(view,"r") as zipped:
            entries=zipped.infolist()
            if len(entries)!=s["members"] or any(
                Path(info.filename).suffix.lower()!=s["extension"] for info in entries
            ):
                raise ValueError("Original source central directory changed after prior audit")
            members=[{
                **safe_member_header(zipped,inf,contract),
                "original_uncompressed_member_size_bytes":inf.file_size,
                "original_compressed_member_size_bytes":inf.compress_size,
            } for inf in entries]
        return {
            "status":"SOURCE_FIRST_LINE_SCHEMA_ATTEMPT_COMPLETED",
            "cohort":cohort,
            "n_original_member_files":len(entries),
            "member_schemas_no_filename":members,
            "bounded_range_calls":view.calls,
            "bounded_compressed_bytes_read":view.bytes_used,
            "full_original_zip_downloaded":False,
            "source_GPS_event_rows_published":False,
        }
    except (zipfile.BadZipFile,ValueError,OSError,UnicodeError) as exc:
        return {
          "status":"SOURCE_HEADER_GATE_FAIL_CLOSED",
          "cohort":cohort,
          "error_class":type(exc).__name__,
          "bounded_range_calls":view.calls,
          "bounded_compressed_bytes_read":view.bytes_used,
          "source_GPS_event_rows_published":False,
        }
    finally:
        view.close()


def audit(contract):
    original=contract["observed_original_directory"]
    # Three item UUIDs/handles are not outcome-dependent and were verified
    # in the preceding exact-source DSpace public file audit.
    ids={
      "control":("79710d0e-d1d6-45fd-90f9-1c6d9be0c46e","10255/move.1627"),
      "delayed":("e0181e26-4f70-45cf-a3f7-6c61ce368af0","10255/move.1632"),
      "naturally_timed":("3949d945-4730-4c24-96e8-4e6bb0234e1c","10255/move.1633"),
    }
    allowed={x[0] for x in ids.values()}
    receipts=[]
    for cohort,(uuid,handle) in ids.items():
        item=get_metadata(f"/server/api/core/items/{uuid}",allowed,set())
        if item["status"]!="PUBLIC_METADATA_OK" or (item["data"] or {}).get("handle")!=handle:
            receipts.append({"cohort":cohort,"status":"SOURCE_ITEM_NOT_VERIFIED"});continue
        bundles=get_metadata(f"/server/api/core/items/{uuid}/bundles",allowed,set())
        if bundles["status"]!="PUBLIC_METADATA_OK":
            receipts.append({"cohort":cohort,"status":"SOURCE_BUNDLE_NOT_VERIFIED"});continue
        orig=[x for x in bundle_entries(bundles["data"] or {})
              if x.get("name")=="ORIGINAL" and UUID_RE.fullmatch(str(x.get("uuid") or ""))]
        if len(orig)!=1:
            receipts.append({"cohort":cohort,"status":"SOURCE_ORIGINAL_BUNDLE_NOT_UNIQUE"});continue
        bid=orig[0]["uuid"]
        files=get_metadata(f"/server/api/core/bundles/{bid}/bitstreams",allowed,{bid})
        if files["status"]!="PUBLIC_METADATA_OK":
            receipts.append({"cohort":cohort,"status":"SOURCE_FILE_METADATA_NOT_VERIFIED"});continue
        info=select_gps_zip(bitstream_entries(files["data"] or {}),original[cohort]["gps_zip_bytes"])
        receipts.append(inspect_one_zip(info,cohort,contract))
    verified=sum(
      x.get("status")=="SOURCE_FIRST_LINE_SCHEMA_ATTEMPT_COMPLETED" and all(
        y.get("status")=="FIRST_LINE_PUBLIC_CSV_SCHEMA_RECOVERED"
        for y in x.get("member_schemas_no_filename",[])
      ) for x in receipts)
    return {
      "date":contract["date"],
      "status":"GPS_FIRST_LINE_SCHEMAS_SOURCE_ONLY",
      "n_original_cohorts":len(receipts),
      "n_cohorts_with_all_member_headers_verified":verified,
      "cohort_schemas":receipts,
      "original_ZIP_files_fully_downloaded":False,
      "GPS_event_values_exported":False,
      "original_file_or_member_identifiers_exported":False,
      "social_information_q_or_recourse_r_estimated":False,
      "same_bird_cross_cohort_identity_inferred":False,
      "no_ebird":True,
      "claim_limit":"Only technical source CSV column names. No event timestamps, locations, sample size, migration decisions, cue reception, validity of full ZIP or biological response estimated."
    }


def main():
    p=argparse.ArgumentParser()
    p.add_argument("--contract",type=Path,default=CONTRACT)
    p.add_argument("--output",type=Path,required=True)
    a=p.parse_args()
    c=json.loads(a.contract.read_text())
    z=audit(c)
    a.output.parent.mkdir(parents=True,exist_ok=True)
    a.output.write_text(json.dumps(z,indent=2)+"\n")
    print("STORK_GPS_CSV_HEADER_SOURCE="+json.dumps(z,separators=(",",":")))

if __name__=="__main__":
    main()
