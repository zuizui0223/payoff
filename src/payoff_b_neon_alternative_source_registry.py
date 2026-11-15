"""Public NEON / USA-NPN / Dryad source alternatives for PAYOFF-B.

These are verified *catalog product identifiers*, not acquired raw observations.
NEON product availability is not evidence of same site/year coverage.
"""
from __future__ import annotations
NEON_PRODUCTS={
    "plant_phenology":{"product_id":"DP1.10055.001","quantity":"individual_phenophase_status_intensity","role":"flowering_timing_and_intensity"},
    "air_temperature":{"product_id":"DP1.00002.001","quantity":"air_temperature","role":"measured_climate"},
    "precipitation":{"product_id":"DP1.00006.001","quantity":"precipitation","role":"measured_climate"},
    "breeding_birds":{"product_id":"DP1.10003.001","quantity":"point_count","role":"bird_abundance_not_arrival_date"},
    "ground_beetles":{"product_id":"DP1.10022.001","quantity":"pitfall_count","role":"insect_activity_not_pollination"},
    "herbaceous_biomass":{"product_id":"DP1.10023.001","quantity":"clip_harvest","role":"plant_biomass_not_nectar_or_caterpillar_biomass"},
    "litterfall":{"product_id":"DP1.10033.001","quantity":"litterfall_and_woody_debris","role":"resource_flux_not_direct_food_availability"},
    "plant_cover":{"product_id":"DP1.10058.001","quantity":"cover","role":"vegetation_structure_not_biomass"},
}
def candidate_sources():
    return {"status":"PUBLIC_CATALOG_PRODUCTS_VERIFIED_NO_RAW_SOURCE_ROWS_DOWNLOADED",
        "priority":"NEON_WITHIN_SITE_CLIMATE_FLOWERING",
        "neon_api":"https://data.neonscience.org/api/v0/products/",
        "neon_phenology_release":"https://data.neonscience.org/data-products/DP1.10055.001/RELEASE-2026",
        "neon_products":NEON_PRODUCTS,
        "usanpn_api":"https://data.usanpn.org/",
        "hoge_veluwe_dryad_doi":"10.5061/dryad.f1vhhmgx6",
        "actual_shared_site_years":None,
        "source_files_acquired":False,
        "climate_resource_outcome_effect_fitted":False,
        "priority_tests":[
            {"hypothesis":"H1","products":["plant_phenology","air_temperature","precipitation"],
             "gate":"MATCH_SITE_YEAR_AND_REPEATED_OBSERVATION_COVERAGE"},
            {"hypothesis":"H2","products":["plant_phenology","herbaceous_biomass","breeding_birds"],
             "gate":"NO_DIRECT_BIRD_FOOD_BIOMASS_OR_DEMAND_CURVE"},
            {"hypothesis":"H4","products":["plant_phenology","ground_beetles"],
             "gate":"BEETLES_NOT_POLLINATOR_VISITS_OR_FOOD_WEB_EDGES"}]}
