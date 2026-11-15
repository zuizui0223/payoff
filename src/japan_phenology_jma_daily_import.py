"""Validate original daily JMA weather exports before event-date feature extraction.

This is a strict normalized-export importer, not a downloader. Original JMA
download layouts differ by station/element; require an auditable mapping of
source columns to canonical variables, and preserve original quality codes.
"""
from __future__ import annotations
import csv
import datetime as dt
import io
import math
from collections import Counter

class JmaDailySourceError(ValueError):
    pass

def admit_normalized_daily_export(raw_csv: str, *, station_metadata_id: str,
                                  source_id: str, variable_columns: dict,
                                  quality_columns: dict,
                                  allowed_quality_codes: dict,
                                  homogeneity_columns: dict | None = None) -> dict:
    if not source_id or not station_metadata_id or not variable_columns:
        raise JmaDailySourceError("Missing source, station, or variable provenance")
    if set(variable_columns) != set(quality_columns):
        raise JmaDailySourceError("Each variable requires its own original quality column")
    if set(variable_columns) - set(allowed_quality_codes):
        raise JmaDailySourceError("No independent quality-code admission for variable")
    homogeneity_columns = homogeneity_columns or {}
    if set(homogeneity_columns) - set(variable_columns):
        raise JmaDailySourceError("Homogeneity mapping for unknown variable")
    reader=csv.DictReader(io.StringIO(raw_csv))
    headers=set(reader.fieldnames or [])
    needed={"date"} | set(variable_columns.values()) | set(quality_columns.values()) | set(homogeneity_columns.values())
    if needed-headers:
        raise JmaDailySourceError("Missing original mapped source columns")
    seen=set()
    rows=[]
    rejected=Counter()
    for line,row in enumerate(reader,2):
        try:
            date=dt.date.fromisoformat(row["date"])
        except (ValueError,TypeError) as exc:
            raise JmaDailySourceError(f"line {line}: invalid source date") from exc
        if date in seen:
            raise JmaDailySourceError(f"line {line}: duplicate station-date")
        seen.add(date)
        vals={}
        flags={}
        regimes={}
        for var,col in variable_columns.items():
            flag=str(row[quality_columns[var]]).strip()
            regimes[var] = str(row[homogeneity_columns[var]]).strip() if var in homogeneity_columns else None
            flags[var]=flag
            token=str(row[col]).strip()
            if token in ("","///","--"):
                vals[var]=None
                rejected[var+":missing"]+=1
            elif flag not in {str(x) for x in allowed_quality_codes[var]}:
                vals[var]=None
                rejected[var+":unadmitted_flag"]+=1
            else:
                try:
                    value=float(token)
                except ValueError as exc:
                    raise JmaDailySourceError(f"line {line}: nonnumeric {var}") from exc
                if not math.isfinite(value):
                    raise JmaDailySourceError(f"line {line}: nonfinite {var}")
                vals[var]=value
        rows.append({"date":date.isoformat(),
                     "station_metadata_id":station_metadata_id,
                     "station_valid_for_date":False,
                     "source_id":source_id,
                     "values":vals,"quality_flags":flags,
                     "homogeneity_numbers":regimes})
    return {"status":"SOURCE_DAILY_VALUES_PARSED_NOT_STATION_HISTORY_ADMITTED",
            "daily_rows":rows,"rejected_by_variable":dict(rejected),
            "station_history_validated":False,
            "homogeneity_columns_mapped":sorted(homogeneity_columns),
            "source_id":source_id,
            "no_environmental_effect_fitted":True}


def attach_verified_station_history(import_receipt: dict, station_history: list[dict]) -> dict:
    """Attach unique date-valid source station history, never modern fallback.

    Does not certify weather station ID correspondence to a particular JMA
    download column; this must be documented separately by source provenance.
    """
    import copy
    out=copy.deepcopy(import_receipt)
    counts=Counter()
    for row in out["daily_rows"]:
        day=dt.date.fromisoformat(row["date"])
        matches=[h for h in station_history if h["station_id"]==row["station_metadata_id"]
                 and h["valid_from"]<=day
                 and (h["valid_to"] is None or day<=h["valid_to"])]
        if len(matches)==1:
            row["station_valid_for_date"]=True
            row["historical_station_lat"]=matches[0]["lat_degrees"]
            row["historical_station_lon"]=matches[0]["lon_degrees"]
            counts["unique_temporal_history"]+=1
        elif len(matches)>1:
            counts["ambiguous_history"]+=1
        else:
            counts["missing_history"]+=1
    out["historical_station_match_counts"]=dict(counts)
    out["station_history_validated"]=counts["unique_temporal_history"]==len(out["daily_rows"])
    out["status"]="STATION_HISTORY_ATTACHED_SOURCE_ID_PROOF_STILL_REQUIRED"
    return out
