import datetime as dt
from src.japan_phenology_independent_reference import independent_reference_controls

def test_disjoint_plant_references_and_direct_bird_insect():
    events=[]
    for station in [str(s) for s in range(401,413)]:
        for year in range(2001,2021):
            for file,label,group,doy in [
                ("019.csv","つばめ初見","bird",90+(year-2001)%4),
                ("020.csv","もんしろちょう初見","insect",95+(year-2001)%3),
                ("004.csv","さくら開花","plant",100+(year-2001)%4),
                ("006.csv","やまつつじ開花","plant",110+(year-2001)%3)]:
                d=dt.date(year,1,1)+dt.timedelta(days=doy-1)
                events.append({"station_id":station,"source_file":file,
                    "event_label":label,"source_taxon_guess":group,
                    "year":year,"day_of_year":doy,"event_date":d.isoformat()})
    out=independent_reference_controls(events)
    panel=next(x for x in out["comparisons"] if x["window"]==[2001,2020]
               and x["comparison"]=="bird_minus_plant_a__insect_minus_plant_b")
    assert panel["stations"]==12
    assert panel["shared_reference_in_difference_scores"] is False
    direct=next(x for x in out["comparisons"] if x["window"]==[2001,2020]
               and x["comparison"]=="bird__insect")
    assert direct["years"]==20
    assert out["weather_or_resource_effect_fitted"] is False
