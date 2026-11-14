"""Official JMA smaster.index fixed-width temporal station-location parser.

Specification: https://www.data.jma.go.jp/stats/data/mdrr/man/smasterindex_format.pdf
Bytes 1-3 station ID, 37-42 latitude DDMMm0, 43-49 longitude DDDMMm0,
65-72 valid-from YYYYMMDD, 73-80 valid-through YYYYMMDD.
The official coordinate fields are degree + minute to 0.1 minute, NOT
decimal degrees or WGS84-datum-certified coordinates.
"""
from __future__ import annotations
import datetime as dt
import io
import zipfile
from collections import Counter, defaultdict


def _dms_tenth_minute(raw: bytes, degree_digits: int) -> float:
    token = raw.decode("ascii").strip()
    if len(token) != degree_digits + 4 or not token.isdigit():
        raise ValueError(f"Unexpected JMA degree-minute field: {token!r}")
    degree = int(token[:degree_digits])
    minutes_tenths = int(token[degree_digits:])
    if minutes_tenths >= 6000 or minutes_tenths % 10 != 0:
        raise ValueError("Invalid minutes")
    return round(degree + minutes_tenths / 6000, 7)


def _period(raw: bytes, *, end: bool = False):
    token = raw.decode("ascii")
    if end and token == "99999999":
        return None
    return dt.datetime.strptime(token, "%Y%m%d").date()


def parse_smaster(raw: bytes) -> list[dict]:
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        names = [n for n in z.namelist() if n.endswith("smaster.index")]
        if len(names) != 1:
            raise ValueError("One original smaster.index required")
        lines = z.read(names[0]).splitlines()
    result = []
    for n, line in enumerate(lines, 1):
        if len(line) != 146:
            raise ValueError(f"line {n}: expected 146 source bytes, got {len(line)}")
        sid = line[:3].decode("ascii")
        if not sid.isdigit():
            raise ValueError(f"line {n}: nonnumeric station ID")
        start = _period(line[64:72])
        end = _period(line[72:80], end=True)
        if end is not None and start > end:
            raise ValueError(f"line {n}: inverted station-history period")
        lat = _dms_tenth_minute(line[36:42], 2)
        lon = _dms_tenth_minute(line[42:49], 3)
        if not (20 <= lat <= 46.5 and 120 <= lon <= 155):
            raise ValueError(f"line {n}: unexpected Japan station coordinates")
        result.append({
            "station_id": sid, "valid_from": start, "valid_to": end,
            "lat_degrees": lat, "lon_degrees": lon,
            "coordinate_precision_minutes": 0.1,
            "coordinate_datum_certified_wgs84": False,
            "metadata_source_line": n,
        })
    return result


def audit_event_coverage(events: list[dict], metadata: list[dict]) -> dict:
    byid = defaultdict(list)
    for m in metadata:
        byid[m["station_id"]].append(m)
    status = Counter()
    relocation = Counter()
    examples = []
    for sid, records in byid.items():
        coords = {(r["lat_degrees"], r["lon_degrees"]) for r in records}
        if len(coords) > 1:
            relocation[sid] = len(coords)
    for event in events:
        sid = event["station_id"]
        date = dt.date.fromisoformat(event["event_date"])
        matches = [m for m in byid.get(sid, [])
                   if m["valid_from"] <= date and
                   (m["valid_to"] is None or date <= m["valid_to"])]
        if not matches:
            status["no_metadata_valid_on_event_date"] += 1
        elif len(matches) > 1:
            coords = {(m["lat_degrees"], m["lon_degrees"]) for m in matches}
            if len(coords) == 1:
                status["overlapping_metadata_same_coordinates"] += 1
            else:
                status["ambiguous_overlapping_coordinates"] += 1
                if len(examples) < 10:
                    examples.append({"station_id": sid, "event_date": str(date),
                                     "candidate_coordinates": sorted([list(x) for x in coords])})
        else:
            status["unique_temporal_metadata_record"] += 1
    return {
        "event_rows": len(events),
        "source_metadata_records": len(metadata),
        "metadata_station_ids": len(byid),
        "stations_with_multiple_coordinates": len(relocation),
        "event_match_status": dict(status),
        "ambiguous_examples": examples,
        "coordinate_degree_minute_decoding_verified_against_format": True,
        "coordinate_datum_certified_wgs84": False,
        "environmental_join_admitted": False,
        "reason": "Numeric and temporal coordinate crosswalk verified; weather/NDVI raw joins, observation process and coordinate datum still require independent validation.",
    }
