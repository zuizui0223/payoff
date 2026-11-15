"""Source-faithful JMA event label and temporal-overlap audit.

Do not equate first call, first sighting, flowering, fruiting, leaf fall or
other stages. The labels are recorded verbatim and only explicit Japanese
event words get an event-type label; otherwise unclassified.
"""
from __future__ import annotations
from collections import Counter, defaultdict
import statistics

def stage_from_label(label: str) -> str:
    patterns = [
        ("first_call", ("初鳴", "初なき", "初鳴き")),
        ("first_sighting", ("初見", "初み", "初飛", "初出")),
        ("flowering", ("開花", "咲き")),
        ("full_bloom", ("満開",)),
        ("leafout", ("発芽", "展葉", "芽吹", "新葉")),
        ("leaf_fall", ("落葉",)),
        ("color_change", ("紅葉", "黄葉")),
        ("fruiting", ("結実",)),
    ]
    matches=[name for name,terms in patterns if any(term in label for term in terms)]
    return matches[0] if len(matches)==1 else "unclassified_or_multiple"

def source_event_inventory(events: list[dict]) -> dict:
    grouped=defaultdict(list)
    for row in events:
        key=(row["source_file"],row["event_label"],row["source_taxon_guess"])
        grouped[key].append(row)
    files=[]
    by_stage=Counter()
    by_group=Counter()
    for (filename,label,group),rows in sorted(grouped.items()):
        stage=stage_from_label(label)
        by_stage[stage]+=1
        by_group[group]+=1
        years=[int(r["year"]) for r in rows]
        days=[int(r["day_of_year"]) for r in rows]
        files.append({
            "source_file":filename,"official_event_label":label,
            "provisional_taxon_group":group,
            "explicit_label_stage":stage,
            "calendar_valid_event_cells":len(rows),
            "station_count":len({r["station_id"] for r in rows}),
            "year_min":min(years),"year_max":max(years),
            "median_observed_day_of_year":round(statistics.median(days),1),
            "seasonal_stage_certified":False,
            "source_rm_semantics_certified":False,
        })
    return {"source_event_file_count":len(files),
            "source_calendar_valid_event_cells":len(events),
            "explicit_label_stage_file_counts":dict(by_stage),
            "provisional_taxon_file_counts":dict(by_group),
            "source_event_inventory":files,
            "stage_classification_is_label_only":True,
            "rm_semantics_certified":False,
            "weather_ndvi_biomass_effect_fitted":False}
