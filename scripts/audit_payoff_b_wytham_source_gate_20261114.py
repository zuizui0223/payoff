"""Fail-closed, metadata-only source gate for Wytham biomass × bird fitness."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "payoff_b_wytham_resource_fitness_source_admission_20261114.json"
REQUIRED = {
    "direct measured resource biomass time series",
    "same site and season as bird breeding",
    "standardized sample effort and units",
    "bird brood demand window",
    "reproductive output",
    "site and year dependence",
}


def audit(payload: dict) -> dict:
    if payload.get("schema") != "payoff_b_wytham_resource_fitness_source_admission_v1":
        raise ValueError("Unknown source metadata schema")
    if set(payload.get("predeclared_primary_model_requires", [])) != REQUIRED:
        raise ValueError("Primary source gates altered")
    sources = payload.get("sources", [])
    if len(sources) != 5 or len({x["id"] for x in sources}) != 5:
        raise ValueError("Expected five distinct screened source records")
    if len({x["doi"] for x in sources if x.get("doi")}) != 4:
        raise ValueError("Expected four distinct public source DOIs")
    for src in sources:
        if src.get("raw_file_checksum_verified") is not False:
            raise ValueError("Cannot promote source without verified checksum")
        if src.get("raw_schema_verified") is not False:
            raise ValueError("Cannot promote source without original file schema")
        if src.get("resource_biomass_magnitude_measured") is not False:
            raise ValueError("Unverified resource magnitude claim")
        if not src.get("metadata_url") or not src.get("admission"):
            raise ValueError("Incomplete provenance")
    if not payload.get("no_resource_biomass_source_admitted"):
        raise ValueError("Biomass source admission must remain closed")
    if not payload.get("no_new_biomass_fitness_effect_fitted"):
        raise ValueError("New fit cannot be asserted from metadata")
    if not payload.get("no_migrant_mechanism_inference"):
        raise ValueError("Resident bird source cannot identify migrant mechanism")
    a = {x["id"]: x for x in sources}
    if a["wytham_breeding_2020_2021"]["source_years"] != [2020, 2021]:
        raise ValueError("Breeding period changed")
    if a["wytham_vegetation_2023"]["source_years"] != [2023]:
        raise ValueError("Habitat period changed")
    return {
        "status": "NO_GO_DIRECT_RESOURCE_BIOMASS_FIT",
        "public_source_records_screened": len(sources),
        "public_dois": sum(bool(x.get("doi")) for x in sources),
        "breeding_output_metadata_available": True,
        "nestling_body_mass_candidate_available": True,
        "direct_prey_biomass_time_series_admitted": False,
        "migrant_information_recourse_identified": False,
        "year_overlap_2020_2021_breeding_vs_2023_vegetation": False,
        "next_source_requirement": "Original repeated frass dry mass, trap area, collection intervals, and same-site/year nest outcomes with source checksum and schema",
    }


if __name__ == "__main__":
    print(json.dumps(audit(json.loads(SOURCE.read_text(encoding="utf-8"))), indent=2, sort_keys=True))
