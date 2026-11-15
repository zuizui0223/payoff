import datetime as dt
from src.japan_phenology_plant_split_randomization import plant_reference_randomization

def test_disjoint_split_reproducibility_and_orientation():
    rows=[]
    for station in ("401","402","403","404","405","406","407","408","409","410"):
        for year in range(2001,2021):
            for f,label,g,doy in [
                ("bird.csv","つばめ初見","bird",90+(year%5)),
                ("insect.csv","もんしろちょう初見","insect",94+(year%4)),
                ("p1.csv","さくら開花","plant",101+(year%5)),
                ("p2.csv","うめ開花","plant",61+(year%4)),
                ("p3.csv","つつじ開花","plant",115+(year%3)),
                ("p4.csv","ふじ開花","plant",119+(year%6)),
            ]:
                date=dt.date(year,1,1)+dt.timedelta(days=doy-1)
                rows.append({"station_id":station,"source_file":f,"event_label":label,
                             "source_taxon_guess":g,"year":year,
                             "event_date":date.isoformat(),"day_of_year":doy})
    a=plant_reference_randomization(rows,repeats=20)
    b=plant_reference_randomization(rows,repeats=20)
    assert a==b
    p=next(x for x in a["windows"] if x["window"]==[2001,2020])
    assert p["valid_split_orientations"]==40
    assert p["stations_min"]==10
    assert a["weather_ndvi_biomass_fitted"] is False
