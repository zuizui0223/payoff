import datetime as dt
from src.japan_phenology_rm_sensitivity import leap_normalize, rm_sensitivity

def test_leap_year_seasonal_normalization():
    rows=[]
    for year,month,day in [(2020,2,29),(2020,3,1),(2019,3,1),(2020,12,31)]:
        date=dt.date(year,month,day)
        rows.append({"event_date":date.isoformat(),"year":year,"day_of_year":date.timetuple().tm_yday})
    normalized,excluded=leap_normalize(rows)
    assert excluded==1
    assert [r["day_of_year"] for r in normalized]==[60,60,365]

def test_rm_code_strata_preserve_unknown_semantics():
    rows=[]
    for year in range(2000,2012):
        for group,src,day,rm in [
            ("bird","bird.csv",100+year-2000,"8"),
            ("plant","plant.csv",110+year-2000,"9"),
        ]:
            d=dt.date(year,1,1)+dt.timedelta(days=day-1)
            rows.append({"station_id":"401","source_file":src,
                         "source_taxon_guess":group,"year":year,
                         "event_date":d.isoformat(),"day_of_year":day,
                         "rm_original_code":rm})
    out=rm_sensitivity(rows,bootstrap_reps=100)
    assert out["source_quality_code_meanings_certified"] is False
    assert out["strata"][0]["comparisons"][1]["stations_with_pairs"]==1
    assert out["strata"][1]["comparisons"][1]["stations_with_pairs"]==0
    assert out["strata"][2]["comparisons"][1]["stations_with_pairs"]==0
    assert out["strata"][3]["comparisons"][1]["stations_with_pairs"]==1
