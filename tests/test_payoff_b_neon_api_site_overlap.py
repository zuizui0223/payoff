from scripts.payoff_b_neon_api_site_overlap import summarize,availability_rows,PRODUCTS

def test_exact_site_month_overlap_from_public_api_schema():
    def data(sites):
        return {"productName":"test","siteCodes":[{"siteCode":site,
                 "availableMonths":months} for site,months in sites.items()]}
    inputs={
        "plant_phenology":data({"ABBY":["2020-05","2020-06"],"BART":["2021-07"]}),
        "air_temperature":data({"ABBY":["2020-05","2020-07"],"BART":["2021-07"]}),
        "precipitation":data({"ABBY":["2020-05"]}),
        "breeding_birds":data({}),
        "herbaceous_biomass":data({"BART":["2021-07"]})}
    result=summarize({k:(v,"abc") for k,v in inputs.items()})
    assert result["availability"]["air_temperature"]["phenology_shared_site_months"]==2
    assert result["availability"]["precipitation"]["phenology_shared_site_months"]==1
    assert result["availability"]["breeding_birds"]["phenology_shared_site_months"]==0
    assert result["availability"]["herbaceous_biomass"]["phenology_shared_site_codes"]==["BART"]
    assert result["raw_neon_observations_downloaded"] is False
    assert result["phenology_climate_effect_fitted"] is False
