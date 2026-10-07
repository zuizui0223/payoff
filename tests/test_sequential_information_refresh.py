import pytest

from src.sequential_information_refresh import (
    checkpoint_predictability,
    direct_predictability,
    noisy_predictive_information,
    refresh_path,
)


def test_direct_predictability_is_product_of_local_correlations():
    assert direct_predictability([0.5, 0.8, 0.25]) == pytest.approx(0.1)


def test_checkpoint_refresh_removes_upstream_weak_link():
    rhos = [0.01, 1.0]
    assert direct_predictability(rhos) == pytest.approx(0.01)
    assert checkpoint_predictability(rhos, 1) == pytest.approx(1.0)


def test_perfect_local_links_make_predictability_weakly_increase_downstream():
    rhos = [0.5, 0.8, 0.9]
    values = [
        checkpoint_predictability(rhos, i)
        for i in range(len(rhos) + 1)
    ]
    assert values == sorted(values)


def test_noisy_checkpoint_information_has_reliability_penalty():
    out = noisy_predictive_information(
        [0.5, 0.8],
        1,
        observation_noise_variance=3.0,
    )
    assert out == pytest.approx((1 / 4) * 0.8**2)


def test_usable_information_can_peak_before_final_checkpoint():
    out = refresh_path(
        [0.5, 0.8],
        observation_noise_variances=[0.0, 0.0, 0.0],
        retained_actionability=[1.0, 0.6, 0.0],
    )
    usable = [row.usable_information for row in out]
    assert usable[1] > usable[0]
    assert usable[1] > usable[2]


def test_invalid_paths_fail_closed():
    with pytest.raises(ValueError):
        refresh_path(
            [0.5, 0.8],
            observation_noise_variances=[0.0, 0.0],
            retained_actionability=[1.0, 0.5, 0.0],
        )
