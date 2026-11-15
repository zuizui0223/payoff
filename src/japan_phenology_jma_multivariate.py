"""Strict JMA daily weather feature engineering for pre-event prediction.

No data download or effect estimation. This module accepts only source-verified
station daily records and retains variable-specific missingness and provenance.
"""
from __future__ import annotations
import datetime as dt
import math
from collections import Counter

class MeteorologyNotAdmitted(ValueError):
    pass

def build_pre_event_features(rows, event_date, *, days=30, base_temperature_c=5.0,
                             admitted_quality_codes=None):
    """Calculate only source-certified daily values.

    admitted_quality_codes must be an explicit mapping from variable name to
    independently verified acceptable JMA quality flags. Unknown flags never
    silently enter a predictive model.
    """
    event = dt.date.fromisoformat(event_date)
    if days not in (7, 30, 60, 90):
        raise MeteorologyNotAdmitted("Unregistered temporal window")
    start = event - dt.timedelta(days=days)
    allowed = {"tmean", "tmax", "tmin", "precip", "sunshine", "global_radiation",
               "snow_depth", "snowfall", "wind_mean", "wind_gust", "relative_humidity",
               "vapour_pressure", "pressure", "cloud"}
    bydate = {}
    admitted_quality_codes = admitted_quality_codes or {}
    for row in rows:
        date = dt.date.fromisoformat(row["date"])
        if not (start <= date < event):
            raise MeteorologyNotAdmitted("Post-event or out-of-window weather record")
        if date in bydate:
            raise MeteorologyNotAdmitted("Duplicate daily weather record")
        if not str(row.get("station_metadata_id", "")).strip() or row.get("station_valid_for_date") is not True:
            raise MeteorologyNotAdmitted("Unverified station provenance")
        if not str(row.get("source_id", "")).strip():
            raise MeteorologyNotAdmitted("Unverified daily weather source")
        vals = row.get("values", {})
        flags = row.get("quality_flags", {})
        if set(vals) - allowed or set(vals) - set(flags):
            raise MeteorologyNotAdmitted("Unknown field or missing per-variable quality flags")
        if any((not isinstance(v, (int, float)) or not math.isfinite(v)) for v in vals.values() if v is not None):
            raise MeteorologyNotAdmitted("Nonfinite weather measurement")
        if "precip" in vals and vals["precip"] is not None and vals["precip"] < 0:
            raise MeteorologyNotAdmitted("Negative precipitation")
        if "relative_humidity" in vals and vals["relative_humidity"] is not None and not 0 <= vals["relative_humidity"] <= 100:
            raise MeteorologyNotAdmitted("Invalid humidity")
        if "sunshine" in vals and vals["sunshine"] is not None and not 0 <= vals["sunshine"] <= 24:
            raise MeteorologyNotAdmitted("Invalid sunshine duration")
        bydate[date] = row
    result = {"event_date": event_date, "window_days": days, "source_days": len(bydate),
              "features": {}, "valid_day_counts": {}, "quality_codes": {},
              "status": "SOURCE_FEATURES_ONLY_NO_EFFECT_FIT"}
    for field in sorted(allowed):
        valid = []
        codes = Counter()
        for row in bydate.values():
            if field not in row["values"]:
                continue
            code = str(row["quality_flags"][field])
            codes[code] += 1
            if row["values"][field] is not None and code in admitted_quality_codes.get(field, set()):
                valid.append(row["values"][field])
        result["valid_day_counts"][field] = len(valid)
        result["quality_codes"][field] = dict(codes)
        # Do not automatically treat quality codes as verified: caller must
        # certify admissible codes before using a feature in a model.
        if len(valid) >= 0.9 * days:
            result["features"][field + "_mean"] = sum(valid) / len(valid)
            if field == "tmean":
                result["features"]["gdd_" + str(base_temperature_c)] = sum(max(v - base_temperature_c, 0) for v in valid)
            if field == "tmin":
                result["features"]["frost_days"] = sum(v < 0 for v in valid)
            if field == "precip":
                result["features"]["precip_total"] = sum(valid)
                result["features"]["rain_days_ge1mm"] = sum(v >= 1 for v in valid)
    result["quality_codes_certified"] = bool(admitted_quality_codes)
    result["ready_for_model"] = bool(admitted_quality_codes and result["features"])
    result["admitted_quality_codes_by_variable"] = {
        field: sorted(map(str, codes)) for field, codes in admitted_quality_codes.items()
    }
    return result
