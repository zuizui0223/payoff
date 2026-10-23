"""Synthetic controls for common-weather vs individual history uncertainty."""
from datetime import date
from scripts.audit_payoff_b_weather_block_dependence import (
    VARS, CASE, STAY, complete_matched_strata, estimate_from_strata,
    block_sensitivity, analyse_original,
)


def sample():
    rows=[]
    # Across 12 years, animals share one calendar weather cell each year.
    for year in range(2006,2018):
        for k in range(3):
            animal=f"secret_{k}"
            cell=(34.0+(year%2),12.0+(k//2)*2)
            # Two source labels observed per animal, same exact cell/month.
            for day,label,delta in ((8,CASE,2.0),(10,STAY,1.0)):
                weather={x:delta for x in VARS}
                rows.append((animal,date(year,3,day),cell,label,weather))
    return rows


def test_original_weather_stratum_computation_unchanged():
    rows=sample()
    strata,counts=complete_matched_strata(rows)
    result=estimate_from_strata(strata)
    assert counts["matched_strata_count"]==24
    assert counts["case_risk_days_in_matched_strata"]==36
    assert all(abs(x-1)<1e-12 for x in result["case_weighted_difference"].values())


def test_own_identity_and_calendar_gridmonth_can_be_checked():
    source=sample()
    paired,counts=complete_matched_strata(source,within_identity=True)
    assert counts["matched_strata_count"]==36
    assert counts["distinct_case_animals_with_instrumental_overlap"]==3
    assert estimate_from_strata(paired)["case_weighted_difference"]["T2M_anomaly"]==1.
    out=analyse_original(source)
    assert out["within_same_bird_gridmonth_effect"] is None
    assert "secret" not in str(out)


def test_block_resampling_clumps_correlated_weather_cells():
    strata, _=complete_matched_strata(sample())
    fine=block_sensitivity(strata,"grid_half_degree",draws=50,seed=12)
    broad=block_sensitivity(strata,"weather_episode_year_month",draws=50,seed=12)
    assert fine["n_distinct_weather_blocks"]==24
    assert broad["n_distinct_weather_blocks"]==12
    for result in (fine,broad):
        assert result["status"]=="DESCRIPTIVE_BLOCK_SENSITIVITY_ESTIMABLE"
        assert result["bootstrap_completed"]==50
        assert result["bootstrap_interval_95pct_descriptive"]["T2M_anomaly"]==[1.,1.]
        assert result["leave_one_weather_block_sign_consistent"]["T2M_anomaly"] is True
        assert not result["source_weather_blocks_independent_in_nature"]


def test_coarse_blocks_use_weather_not_individual_ids():
    strata,_=complete_matched_strata(sample())
    out=block_sensitivity(strata,"weather_block_2_degree",draws=10,seed=11)
    assert out["n_distinct_weather_blocks"]==24
    assert "secret" not in str(out)
    assert "34.0" not in str(out)
