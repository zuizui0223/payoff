import datetime as dt
from src.japan_phenology_plant_common_support import fixed_common_support_plant_splits

def test_same_station_set_all_six_oriented_plant_splits():
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
                date=dt.date(year,1,1)+dt.timedelta(days=doy-1)
                rows.append({"station_id":str(site),"source_file":file,
                             "event_label":label,"source_taxon_guess":group,
                             "year":year,"day_of_year":doy,"event_date":date.isoformat()})
    out=fixed_common_support_plant_splits(rows)
    p=next(x for x in out["windows"] if x["window"]==[2001,2020])
    assert p["fixed_station_count"]==12
    assert p["unique_oriented_splits"]==6
    assert len({tuple(sorted(d["plant_a"]+d["plant_b"])) for d in p["draws"]})==1
    assert out["weather_ndvi_biomass_fitted"] is False
