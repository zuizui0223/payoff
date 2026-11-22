"""No-model original-data source-field diagnosis guards."""
from __future__ import annotations
import pytest

pytest.importorskip("numpy")
from scripts import payoff_b_radar_source_doy_range_diagnosis_20261122 as d


def rows():
    return [
        {"site":"PRIVATE_SITE_001","year":2003,"spring_q50":100.0,"mean_greenup":101.0,"spring_mean_temp":7.0},
        {"site":"PRIVATE_SITE_002","year":2003,"spring_q50":109.0,"mean_greenup":365.0,"spring_mean_temp":9.0},
        {"site":"PRIVATE_SITE_001","year":2004,"spring_q50":99.0,"mean_greenup":370.0,"spring_mean_temp":8.0},
        {"site":"PRIVATE_SITE_002","year":2004,"spring_q50":None,"mean_greenup":100.0,"spring_mean_temp":8.0},
    ]


def test_field_ranges_not_date_gap_or_effect():
    z=d.diagnose(rows())
    assert z["status"]=="SOURCE_FIELD_RANGE_DIAGNOSIS_NO_CHRONOLOGY"
    assert z["original_rows"]==4
    assert z["complete_rows"]==3
    assert z["source_fields"]["mean_greenup"]["n_greater_than_366"]==1
    assert z["source_fields"]["spring_q50"]["n_greater_than_366"]==0
    assert z["date_range_gate"]=="REQUIRES_SOURCE_SEMANTICS"
    assert z["source_fields"]["mean_greenup"]["invalid_count_by_year"]==[
        {"year":2004,"n_invalid":1}
    ]
    assert "PRIVATE_SITE_001" not in str(z)
    assert "PRIVATE_SITE_002" not in str(z)
    assert z["no_effect_or_gap_calculated"] is True


def test_valid_calendar_range_passes():
    r=rows()
    r[2]["mean_greenup"]=364.0
    z=d.diagnose(r)
    assert z["date_range_gate"]=="PASS"
