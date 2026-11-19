"""Post-open within-year weather-assignment negative-control tests."""
import os
from pathlib import Path

import pytest

pd=pytest.importorskip("pandas")
np=pytest.importorskip("numpy")
pytest.importorskip("scipy")
pytest.importorskip("statsmodels")
pytest.importorskip("sklearn")

from scripts.payoff_b_gwfg_lagged_weather_to_feeding import (
    make_bird_years, original_source_digest
)
from scripts.payoff_b_gwfg_within_year_freeze_permutation import (
    SEED, PERMUTATIONS, within_year_shuffle, updated_ridge_mse
)


def fabricated_groups():
    return pd.DataFrame([
        {"bird_id":f"B{i}","year_index":y,
         "freeze3_10pp":0.5*i+0.3*y,"feed3":0.4+0.01*i,
         "feed4":0.5+0.01*i,"precip3":1.0,"storm3":0.,
         "first_day3":90+i,"precip4":0.2,"storm4":0.,
         "breeding_success":int(i%2==0)}
        for y in range(1,6) for i in range(4)
    ])


def test_within_year_shuffle_preserves_yearly_weather_marginals_and_all_other_records():
    original=fabricated_groups()
    rng=np.random.default_rng(SEED)
    shuffled=within_year_shuffle(original,rng)
    for y in range(1,6):
        a=original.loc[original.year_index==y,"freeze3_10pp"]
        b=shuffled.loc[shuffled.year_index==y,"freeze3_10pp"]
        assert sorted(a.tolist())==sorted(b.tolist())
        assert sum(original.loc[original.year_index==y,"breeding_success"])==sum(
            shuffled.loc[shuffled.year_index==y,"breeding_success"])
    for col in original.columns:
        if col!="freeze3_10pp":
            pd.testing.assert_series_equal(original[col],shuffled[col])
    assert PERMUTATIONS==99
    assert SEED==20261119


def test_no_silent_year_substitution():
    df=fabricated_groups()
    df=df.loc[df.year_index!=5].copy()
    with pytest.raises(ValueError,match="five published calendar years"):
        within_year_shuffle(df,np.random.default_rng(SEED))


def test_prediction_rejects_any_non_frozen_group_dimension():
    df=fabricated_groups()
    with pytest.raises(ValueError,match="independent group folds"):
        updated_ridge_mse(df,"breeding_success")


def test_original_source_unchanged_and_frozen_ridge_reproduced_in_dedicated_CI():
    fp=os.environ.get("PAYOFF_GWFG_2024_ORIGINAL_SPRING_CSV")
    if not fp:
        pytest.skip("Original public source loaded in dedicated source-hashed CI")
    file=Path(fp)
    source=original_source_digest(file)
    assert source["source_original_public_git_blob_SHA1"]=="ca3736a281dfd2465921efc940dd985499c71a4f"
    original=make_bird_years(pd.read_csv(file),strict=True)
    assert len(original)==107
    assert original.bird_id.nunique()==49
    for group,expected in (
        ("bird_id",0.004399626468961512),
        ("year_index",0.010500353704119267),
    ):
        # Independent reimplementation of original fixed ridge prediction
        # must reproduce the original 2026-11-19 result before permutations.
        assert updated_ridge_mse(original,group)==pytest.approx(expected,abs=1e-11)
