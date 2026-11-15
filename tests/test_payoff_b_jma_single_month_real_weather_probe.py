from scripts.payoff_b_jma_single_month_real_weather_probe import probe

def test_original_daily_table_column_mapping_and_missingness():
    row="<tr>"+ "".join(f"<td>{x}</td>" for x in [
        "1","1003.9","1006.8","31.0","5.0","1.5","11.4",
        "12.9","9.3","97","89","2.7","5.1","北西","9.8",
        "北西","0.0","--","--","雨","晴"])+"</tr>"
    html=("<html><table>"+row+"</table></html>").encode()
    out=probe(html)
    assert out["source_daily_rows"]==1
    assert out["daily_weather_unqualified_source_summary"]["precip_mm"]["sum"]==31
    assert out["daily_weather_unqualified_source_summary"]["tmean_c"]["mean"]==11.4
    assert out["daily_weather_unqualified_source_summary"]["relative_humidity_pct"]["mean"]==97
    assert out["daily_weather_unqualified_source_summary"]["sunshine_hours"]["sum"]==0
    assert out["weather_csv_quality_codes_present_and_verified"] is False
