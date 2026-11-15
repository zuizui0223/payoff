from src.japan_phenology_spring_stage_matched import spring_stage_contrasts

def test_spring_stage_contrast_excludes_autumn_first_call():
    rows=[]
    for y in range(2000,2012):
        for file,label,group,day in [
            ("bird.csv","つばめ初見","bird",90+y-2000),
            ("plant.csv","さくら開花","plant",95+y-2000),
            ("autumn.csv","もず初鳴","bird",260+y-2000),
        ]:
            rows.append({"source_file":file,"event_label":label,
                         "source_taxon_guess":group,"station_id":"401",
                         "year":y,"day_of_year":day})
    out=spring_stage_contrasts(rows,bootstrap_reps=100)
    assert out["source_event_files_spring_eligible"]==2
    contrast=out["contrasts"][0]
    assert contrast["source_files_a"]==["bird.csv"]
    assert contrast["source_files_b"]==["plant.csv"]
    assert contrast["mean_station_equal_weight_r"]==1
    assert out["environmental_weather_ndvi_biomass_fitted"] is False
