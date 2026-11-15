import io
import zipfile
from scripts.payoff_b_jma_tokyo_2020_real_weather_phenology_alignment import align_original_sources

def test_original_source_alignment_no_post_event_leakage():
    row=lambda d:"<tr>"+"".join(f"<td>{v}</td>" for v in [str(d),"1003","1006","0","0","0","12","18","7","65","35","3","5","北","8","北","7","--","--","晴","晴"])+"</tr>"
    html=("<html><table>"+"".join(row(i) for i in range(1,31))+"</table></html>").encode()
    z=io.BytesIO()
    with zipfile.ZipFile(z,"w") as out:
        out.writestr("004.csv","4,さくら開花\n番号,地点名,2020,rm\n441,東京,415,8\n".encode("cp932"))
    receipt=align_original_sources(html,z.getvalue(),{"004.csv":"さくら開花"})
    event=receipt["events"][0]
    assert event["april_weather_days_strictly_before_event"]==14
    assert event["april_weather_days_on_or_after_event"]==16
    assert event["full_30day_pre_event_window_covered_by_april_source"] is False
    assert receipt["weather_phenology_effect_fitted"] is False
    assert event["full_30day_pre_event_window_covered_by_april_source"] is False


def test_june_event_does_not_misclassify_april_as_immediate_30day_window():
    row=lambda d:"<tr>"+"".join(f"<td>{v}</td>" for v in [str(d),"1003","1006","0","0","0","12","18","7","65","35","3","5","北","8","北","7","--","--","晴","晴"])+"</tr>"
    html=("<html><table>"+"".join(row(i) for i in range(1,31))+"</table></html>").encode()
    z=io.BytesIO()
    with zipfile.ZipFile(z,"w") as out:
        out.writestr("009.csv","9,あじさい開花\n番号,地点名,2020,rm\n662,東京,608,9\n".encode("cp932"))
    result=align_original_sources(html,z.getvalue(),{"009.csv":"あじさい開花"})
    assert result["events"][0]["april_weather_days_strictly_before_event"]==30
    assert result["events"][0]["full_30day_pre_event_window_covered_by_april_source"] is False
