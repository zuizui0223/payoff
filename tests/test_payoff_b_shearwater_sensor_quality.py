"""Synthetic distinct sensor-vs-treatment coverage checks, no real IDs."""
from datetime import datetime,timedelta
from scripts.qc_payoff_b_shearwater_sensor_quality import (
    maximal_contiguous_hours,sensor_qc,compare_sensors
)

def test_contiguous_24_hour_run_requires_no_gap_over_6hours():
    t=datetime(2015,5,1)
    regular=[t+timedelta(hours=i) for i in range(30)]
    gapped=regular[:12]+[t+timedelta(hours=50+i) for i in range(12)]
    assert maximal_contiguous_hours(regular)==29
    assert maximal_contiguous_hours(gapped)<24

def test_sensors_are_not_independent_birds():
    groups={**{f"c{i}":"control" for i in range(9)},
            **{f"m{i}":"magnetic_disruption" for i in range(9)},
            **{f"a{i}":"olfactory_deprivation" for i in range(14)}}
    gps={k:[datetime(2015,5,1)] for k in groups}
    argos={"a0":[datetime(2015,5,1)]}
    r=compare_sensors(groups,gps,argos)
    assert r["olfactory_deprivation"]["any_telemetry_subject_count"]==14
    assert r["olfactory_deprivation"]["both_sensors_same_subject"]==1
    assert "a0" not in str(r)

def test_sensor_group_counts_aggregate_only():
    t=datetime(2015,5,1)
    result=sensor_qc({"secret":[t+timedelta(hours=k) for k in range(30)]},
                     {"secret":"control"})
    assert result["control"]["n_with_contiguous_24h"]==1
    assert "secret" not in str(result)
