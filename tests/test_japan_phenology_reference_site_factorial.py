import datetime as dt
from src.japan_phenology_reference_site_factorial import factorial_reference_station_sensitivity

def test_same_plant_subset_comparison_changes_only_station_support():
    rows=[]
    for site in range(401,413):
        for year in range(2001,2021):
            for file,label,group,doy in (
                ("bird.csv","つばめ初見","bird",90+year%4),
                ("insect.csv","もんしろちょう初見","insect",95+year%5),
                ("p1.csv","さくら開花","plant",105+year%3),
                ("p2.csv","うめ開花","plant",65+year%4),
                ("p3.csv","つつじ開花","plant",112+year%5),
                ("p4.csv","ふじ開花","plant",117+year%6)):
                if site==412 and file=="p4.csv":continue
                date=dt.date(year,1,1)+dt.timedelta(days=doy-1)
                rows.append({"station_id":str(site),"source_file":file,
                             "event_label":label,"source_taxon_guess":group,
                             "year":year,"day_of_year":doy,"event_date":date.isoformat()})
    result=factorial_reference_station_sensitivity(rows,max_subsets=20)
    p=next(x for x in result["windows"] if x["window"]==[2001,2020])
    assert p["subsets_admitted"]==1
    subset=p["subsets"][0]
    assert subset["strict_stations"]==11
    assert subset["variable_stations_max"]==12
    assert subset["variable_stations_min"]==12
    assert result["weather_ndvi_biomass_fitted"] is False
