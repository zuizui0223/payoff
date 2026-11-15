"""JMA phenology stage- and season-matched spring comparison.

Unlike all-season pooled comparisons, retain only original event types with
spring median timing and a declared spring interval. Exact stage restrictions
avoid comparing autumn cicada first calls to spring flowering as a putative
direct interaction. This is still descriptive, not weather/biomass inference.
"""
from __future__ import annotations
from collections import defaultdict
from statistics import median
from src.japan_phenology_event_definition_audit import stage_from_label
from src.japan_phenology_coupling_robustness import station_balanced_coupling

CONTRASTS=(
    ("bird_first_sighting__plant_flowering","bird","first_sighting","plant","flowering"),
    ("bird_first_call__plant_flowering","bird","first_call","plant","flowering"),
    ("insect_first_sighting__plant_flowering","insect","first_sighting","plant","flowering"),
    ("amphibian_first_sighting__plant_flowering","amphibian","first_sighting","plant","flowering"),
    ("amphibian_first_call__plant_flowering","amphibian","first_call","plant","flowering"),
    ("bird_first_sighting__insect_first_sighting","bird","first_sighting","insect","first_sighting"),
)

def spring_stage_contrasts(events, *, spring_start=45, spring_end=160,
                           min_shared_years=10, bootstrap_reps=300):
    byfile=defaultdict(list)
    for r in events:
        byfile[r["source_file"]].append(r)
    eligible={}
    for file,rows in byfile.items():
        label=rows[0]["event_label"]
        stage=stage_from_label(label)
        med=median(int(r["day_of_year"]) for r in rows)
        if spring_start <= med <= spring_end:
            eligible[file]={"stage":stage,"group":rows[0]["source_taxon_guess"],
                            "label":label,"median_day_of_year":med}
    outputs=[]
    for name,ga,sa,gb,sb in CONTRASTS:
        files_a={f for f,v in eligible.items() if v["stage"]==sa and v["group"]==ga}
        files_b={f for f,v in eligible.items() if v["stage"]==sb and v["group"]==gb}
        subset=[]
        for r in events:
            f=r["source_file"]
            if f in files_a:
                subset.append({**r,"source_taxon_guess":"contrast_a"})
            elif f in files_b:
                subset.append({**r,"source_taxon_guess":"contrast_b"})
        stats=station_balanced_coupling(subset,"contrast_a","contrast_b",
                                      min_shared_years=min_shared_years,
                                      bootstrap_reps=bootstrap_reps)
        outputs.append({"contrast":name,"source_files_a":sorted(files_a),
                        "source_files_b":sorted(files_b),
                        "event_labels_a":[eligible[f]["label"] for f in sorted(files_a)],
                        "event_labels_b":[eligible[f]["label"] for f in sorted(files_b)],
                        **stats})
    return {"status":"EXPLORATORY_SPRING_STAGE_MATCHED_JMA_OBSERVED_EVENTS",
            "spring_median_day_of_year_bounds":[spring_start,spring_end],
            "source_event_files_spring_eligible":len(eligible),
            "rm_meanings_certified":False,
            "observation_effort_harmonized":False,
            "environmental_weather_ndvi_biomass_fitted":False,
            "contrasts":outputs}
