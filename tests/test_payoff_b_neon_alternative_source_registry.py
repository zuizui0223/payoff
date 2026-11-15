from src.payoff_b_neon_alternative_source_registry import candidate_sources

def test_neon_public_catalog_does_not_fabricate_raw_overlap():
    r=candidate_sources()
    assert r["priority"]=="NEON_WITHIN_SITE_CLIMATE_FLOWERING"
    assert r["actual_shared_site_years"] is None
    assert r["source_files_acquired"] is False
    assert r["climate_resource_outcome_effect_fitted"] is False
    assert r["neon_products"]["plant_phenology"]["product_id"]=="DP1.10055.001"
    assert r["neon_products"]["breeding_birds"]["role"]=="bird_abundance_not_arrival_date"
    assert r["neon_products"]["herbaceous_biomass"]["role"]=="plant_biomass_not_nectar_or_caterpillar_biomass"
