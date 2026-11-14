"""Convert official JMA wide annual phenology tables to an event-level panel.

Preserve JMA rm code as opaque source metadata. Do not treat 0 as a date,
do not assume rm quality meanings, and do not treat first observations as
standardized abundance or physiological onset.
"""
from __future__ import annotations

import csv
import datetime as dt
import io
import re
from collections import Counter


def parse_wide_jma_csv(payload: bytes, *, source_file: str, event_label: str) -> tuple[list[dict], dict]:
    decoded = None
    for enc in ("cp932", "utf-8-sig", "shift_jis"):
        try:
            decoded = payload.decode(enc)
            break
        except UnicodeDecodeError:
            pass
    if decoded is None:
        raise ValueError("Unknown source encoding")
    rows = [r for r in csv.reader(io.StringIO(decoded)) if any(v.strip() for v in r)]
    if len(rows) < 3 or rows[1][:2] != ["番号", "地点名"]:
        raise ValueError("Not a recognized JMA wide station/year table")
    header = rows[1]
    year_cols = []
    for col in range(2, len(header) - 1, 2):
        if not re.fullmatch(r"(?:19|20)\d{2}", header[col].strip()):
            break
        if header[col + 1].strip().lower() != "rm":
            break
        year_cols.append((col, int(header[col])))
    if not year_cols:
        raise ValueError("No consecutive year/rm pairs")
    panel = []
    invalid_dates = Counter()
    rm_by_valid_date = Counter()
    duplicate_keys = set()
    for row in rows[2:]:
        if len(row) < 2 or not row[0].strip().isdigit():
            continue
        station_id, station_name = row[0].strip(), row[1].strip()
        for col, year in year_cols:
            raw_date = row[col].strip() if col < len(row) else ""
            rm = row[col + 1].strip() if col + 1 < len(row) else ""
            if not raw_date.isdigit() or not 1 <= int(raw_date) <= 1231:
                invalid_dates[raw_date] += 1
                continue
            mmdd = raw_date.zfill(4)
            try:
                observed = dt.date(year, int(mmdd[:2]), int(mmdd[2:]))
            except ValueError:
                invalid_dates["INVALID_CALENDAR_DATE"] += 1
                continue
            key = (source_file, station_id, year)
            if key in duplicate_keys:
                raise ValueError("Duplicate source-file/station/year")
            duplicate_keys.add(key)
            rm_by_valid_date[rm] += 1
            panel.append({
                "source_file": source_file,
                "event_label": event_label,
                "station_id": station_id,
                "station_name": station_name,
                "year": year,
                "event_date": observed.isoformat(),
                "day_of_year": observed.timetuple().tm_yday,
                "rm_original_code": rm,
                "rm_quality_interpretation": "UNVERIFIED",
                "observer_effort": None,
                "taxon_source_label_not_verified_species_id": True,
            })
    return panel, {
        "source_file": source_file,
        "event_label": event_label,
        "first_year_column": year_cols[0][1],
        "last_year_column": year_cols[-1][1],
        "event_rows_calendar_valid_not_rm_screened": len(panel),
        "valid_event_rm_codes": dict(rm_by_valid_date),
        "invalid_or_missing_date_cells": dict(invalid_dates),
        "distinct_stations_with_events": len({x["station_id"] for x in panel}),
    }
