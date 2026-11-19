"""2024 original goose weather-to-feeding temporal-source gate tests."""
from pathlib import Path
import os

import pytest

pd = pytest.importorskip("pandas")
np = pytest.importorskip("numpy")
pytest.importorskip("statsmodels")
pytest.importorskip("scipy")
pytest.importorskip("sklearn")

from scripts.payoff_b_gwfg_lagged_weather_to_feeding import (
    make_bird_years, original_source_digest, regress, run
)


def stage_fixture():
    items=[]
    for year in [1,2]:
        for stage in range(1,7):
            items.append({
                "id":7,
                "year":year,
                "sub_season":stage,
                "breeding_outcome":1 if year==1 else 2,
                "breeding_success":1 if year==1 else 0,
                "first_day":70+10*stage,
                "log_ODBA":-0.5,
                "num_feed_fixes":30+stage,
                "num_ACC_fixes":100,
                "mean_precip":1.0,
                "prop_days_below_freezing":0.30 if stage==3 else 0.,
                "prop_storm_days":0.1,
            })
    return pd.DataFrame(items)


def test_original_stage_to_wide_grain_without_false_replication():
    d=make_bird_years(stage_fixture(),strict=False)
    assert len(d)==2
    assert d.bird_id.nunique()==1
    assert d.year_index.nunique()==2
    assert d["feed3"].iloc[0]==pytest.approx(0.33)
    assert d["feed4"].iloc[0]==pytest.approx(0.34)
    assert d["freeze3_10pp"].iloc[0]==pytest.approx(3.0)
    assert list(d.breeding_success)==[1,0]
    assert "sub_season" not in d.columns
    with pytest.raises(ValueError,match="original published source grain drift|Original published source grain drift"):
        make_bird_years(stage_fixture(),strict=True)


def test_original_time_order_duplicate_and_label_mismatch_fail():
    fake=stage_fixture()
    fake.loc[(fake.year==1)&(fake.sub_season==4),"first_day"]=100
    with pytest.raises(ValueError,match="time ordering"):
        make_bird_years(fake,strict=False)
    fake=stage_fixture()
    fake.loc[(fake.year==1)&(fake.sub_season==1),"breeding_success"]=0
    with pytest.raises(ValueError,match="outcome inconsistency"):
        make_bird_years(fake,strict=False)
    fake=pd.concat([stage_fixture(),stage_fixture().iloc[[0]]],ignore_index=True)
    with pytest.raises(ValueError,match="duplicate bird-year-stage"):
        make_bird_years(fake,strict=False)


def test_no_ACC_pseudoreplication_or_zero_division():
    fake=stage_fixture()
    fake.loc[(fake.year==1)&(fake.sub_season==3),"num_ACC_fixes"]=0
    with pytest.raises(ValueError,match="ACC denominator"):
        make_bird_years(fake,strict=False)
    fake=stage_fixture()
    fake.loc[(fake.year==1)&(fake.sub_season==4),"num_feed_fixes"]=101
    with pytest.raises(ValueError,match="ACC denominator"):
        make_bird_years(fake,strict=False)


def test_only_exact_public_git_source_is_admissible(tmp_path):
    p=tmp_path/"spring_data.csv"
    p.write_text(stage_fixture().to_csv(index=False))
    with pytest.raises(ValueError,match="Git blob SHA1 mismatch"):
        original_source_digest(p)


def test_primary_never_uses_uncertified_small_synthetic_panel():
    x=make_bird_years(stage_fixture(),strict=False)
    with pytest.raises(ValueError,match="source insufficient"):
        run(x,{"fake_source":True})


def test_source_2024_public_original_full_result_when_supplied():
    source=os.environ.get("PAYOFF_GWFG_2024_ORIGINAL_SPRING_CSV")
    if not source:
        pytest.skip("Official public upstream data are read only in dedicated CI")
    file=Path(source)
    original=original_source_digest(file)
    x=make_bird_years(pd.read_csv(file),strict=True)
    assert x.shape[0]==107
    assert x.bird_id.nunique()==49
    assert x.year_index.nunique()==5
    assert int(x.breeding_success.sum())==28
    assert original["source_original_public_git_blob_SHA1"]=="ca3736a281dfd2465921efc940dd985499c71a4f"
    r=run(x,original)
    target=r["stage3_early_freezing_association"]["full_source_fixed_year_clustered_OLS"]
    assert target["n_bird_years"]==107
    assert target["n_individual_birds"]==49
    assert target["bird_t_df"]==48
    assert target["design_rank"]==target["design_columns"]
    assert target["focal_ci95"][0]<=target["focal_early_freezing_beta_per_10pp"]<=target["focal_ci95"][1]
    stress=r["stage3_early_freezing_association"]["leave_one_year_out_coefficient_stress"]
    assert len(stress)==5
    for x in stress:
        assert x["n_remaining_bird_years"]>=70
        assert len(x["CI95"])==2
    assert r["stage4_feeding_heldout_prediction"][
        "baseline_weather_earlier_feeding_no_freeze_vs_added_early_freeze"
    ]["leave_one_entire_year_out"]["n_holdout_folds"]==5
    assert r["stage4_behavior_to_later_breeding_success_prediction"][
        "leave_one_entire_bird_out"]["n_holdout_folds"]==49
    assert r["claims"]["direct_organism_observed_future_state_credibility"] is False
    assert r["claims"]["new_independent_natural_study"] is False
