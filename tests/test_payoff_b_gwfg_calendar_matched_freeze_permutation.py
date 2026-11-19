"""Source support and exact temporal-stratum invariants for weather reassignment."""
import os
from pathlib import Path

import pytest

pd = pytest.importorskip("pandas")
np = pytest.importorskip("numpy")
pytest.importorskip("scipy")
pytest.importorskip("statsmodels")
pytest.importorskip("sklearn")

from scripts.payoff_b_gwfg_lagged_weather_to_feeding import (
    make_bird_years, original_source_digest
)
from scripts.payoff_b_gwfg_calendar_matched_freeze_permutation import (
    MIN_ELIGIBLE, MIN_GROUPS, MIN_YEARS,
    ITERATIONS, SPECS, block_key,
    admission, eligible_blocks, shuffle_temporally_matched
)


def synthetic_block_source():
    rows = []
    for year in range(1, 6):
        for i in range(8):
            rows.append({
                "bird_id": i,
                "year_index": year,
                "first_day3": 90.0 + (i // 4),
                "first_day4": 104.0 + (i // 4) + (i % 2),
                "freeze3_10pp": float(i % 4) * .5 + year,
                "feed3": .4 + i / 100.,
                "feed4": .52 + (i % 3)/100.,
                "precip3": .5,
                "storm3": .1,
                "precip4": .25,
                "storm4": .05,
                "breeding_success": int(i % 2 == 0),
            })
    return pd.DataFrame(rows)


def test_calendar_match_rules_fixed_and_date_duration_not_equated():
    d = synthetic_block_source()
    a = d.iloc[0]
    b = d.iloc[1]
    assert block_key(a, "same_year_exact_start_day") == (1, 90)
    assert block_key(a, "same_year_7day_bin_and_3day_duration_band") == (
        1, (90-1)//7, (14-1)//3
    )
    assert block_key(a, "same_year_exact_start_and_exact_duration") == (1, 90, 14)
    assert block_key(b, "same_year_exact_start_day") == (1, 90)
    assert block_key(b, "same_year_exact_start_and_exact_duration") == (1, 90, 15)
    assert ITERATIONS == 99
    assert tuple(x[1] for x in SPECS) == (20261119, 20261120, None)
    assert (MIN_ELIGIBLE, MIN_GROUPS, MIN_YEARS) == (40, 8, 3)


def test_shuffle_only_weather_and_never_leaves_calendar_or_duration_block():
    d = synthetic_block_source()
    for design, seed in SPECS[:2]:
        got = shuffle_temporally_matched(d, design, np.random.default_rng(seed))
        assert not got["freeze3_10pp"].equals(d["freeze3_10pp"])
        for column in d.columns:
            if column != "freeze3_10pp":
                pd.testing.assert_series_equal(got[column], d[column])
        for _, indices in eligible_blocks(d, design).items():
            assert sorted(got.iloc[indices].freeze3_10pp.tolist()) == sorted(
                d.iloc[indices].freeze3_10pp.tolist()
            )


def test_unknown_matching_rule_is_rejected():
    with pytest.raises(ValueError, match="Unregistered"):
        block_key(synthetic_block_source().iloc[0], "shift_unfavorable_cases")


def test_noninteger_or_backward_original_dates_are_rejected():
    d = synthetic_block_source()
    d.loc[0, "first_day3"] = 90.5
    with pytest.raises(ValueError, match="increasing integer"):
        block_key(d.iloc[0], "same_year_exact_start_day")
    d = synthetic_block_source()
    d.loc[0, "first_day4"] = 89.
    with pytest.raises(ValueError, match="increasing integer"):
        block_key(d.iloc[0], "same_year_exact_start_day")


def test_original_support_and_strict_match_failure_without_outcome_fit():
    fp = os.environ.get("PAYOFF_GWFG_2024_ORIGINAL_SPRING_CSV")
    if not fp:
        pytest.skip("Official public original CSV provided in dedicated CI")
    source = Path(fp)
    info = original_source_digest(source)
    assert info["source_original_public_git_blob_SHA1"] == (
        "ca3736a281dfd2465921efc940dd985499c71a4f"
    )
    original = make_bird_years(pd.read_csv(source), strict=True)
    assert len(original) == 107
    support = {kind: admission(original, kind) for kind, _ in SPECS}
    assert (support["same_year_exact_start_day"][
        "candidate_swappable_bird_year_rows"],
        support["same_year_exact_start_day"]["n_eligible_nonconstant_groups"],
        support["same_year_exact_start_day"]["n_original_years_with_nonconstant_groups"]
    ) == (48, 14, 5)
    assert (support["same_year_7day_bin_and_3day_duration_band"][
        "candidate_swappable_bird_year_rows"],
        support["same_year_7day_bin_and_3day_duration_band"][
            "n_eligible_nonconstant_groups"]
    ) == (52, 11)
    exact = support["same_year_exact_start_and_exact_duration"]
    assert exact["candidate_swappable_bird_year_rows"] == 17
    assert exact["n_eligible_nonconstant_groups"] == 7
    assert exact["admission"] == "FAIL_NOT_ESTIMABLE_NO_SHUFFLES"
