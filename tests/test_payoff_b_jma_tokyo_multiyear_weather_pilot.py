from scripts.payoff_b_jma_tokyo_multiyear_weather_pilot import parse_month, summarize_sources, YEARS, MONTHS

def fake_month(year,month):
    import calendar
    n=calendar.monthrange(year,month)[1]
    rows=[]
    for day in range(1,n+1):
        values=[str(day),"1003","1006","0","0","0",str(year-2000),
                "20","8","70","40","3","5","北","8","北","7","--","--","晴","晴"]
        rows.append("<tr>"+"".join(f"<td>{v}</td>" for v in values)+"</tr>")
    return ("<html><table>"+"".join(rows)+"</table></html>").encode()

def test_six_source_months_have_correct_calendar_days_and_yearly_means():
    sources={(year,month):fake_month(year,month) for year in YEARS for month in MONTHS}
    result=summarize_sources(sources)
    assert result["years"]["2020"]["source_weather_days"]==61
    assert result["years"]["2019"]["march_april_tmean"]["mean"]==19
    assert result["years"]["2021"]["march_april_tmean"]["mean"]==21
    assert result["phenology_effect_fitted"] is False
    assert result["weather_csv_quality_codes_verified"] is False
