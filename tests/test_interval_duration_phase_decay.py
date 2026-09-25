import math

import numpy as np

from src.interval_duration_phase_decay import (
    classify_duration_evidence,
    compare_segment_and_duration_models,
)


def test_calendar_duration_decay_recovers_synthetic_k_and_wins():
    rng = np.random.default_rng(20260925)
    n = 240
    x = rng.normal(0, 8, n)
    dt = rng.uniform(0.5, 12.0, n)
    z = np.column_stack([np.ones(n), rng.normal(size=n)])
    groups = np.asarray([f"G{i // 6:02d}" for i in range(n)])
    k_true = 0.18
    y = np.exp(-k_true * dt) * x + z @ np.array([2.0, -1.0])
    y += rng.normal(0, 0.35, n)

    result = compare_segment_and_duration_models(
        origin_phase=x,
        destination_phase=y,
        duration_days=dt,
        nuisance=z,
        groups=groups,
    )
    assert abs(result["calendar_duration_model"]["k_hat_per_day"] - k_true) < 0.02
    assert result["delta_aic_duration_minus_segment"] < -2.0


def test_segment_constant_wins_when_retention_is_event_based():
    rng = np.random.default_rng(9)
    n = 240
    x = rng.normal(0, 8, n)
    dt = rng.uniform(0.5, 12.0, n)
    z = np.column_stack([np.ones(n), rng.normal(size=n)])
    groups = np.asarray([f"G{i // 6:02d}" for i in range(n)])
    y = 0.62 * x + z @ np.array([1.0, 0.5])
    y += rng.normal(0, 0.35, n)

    result = compare_segment_and_duration_models(
        origin_phase=x,
        destination_phase=y,
        duration_days=dt,
        nuisance=z,
        groups=groups,
    )
    assert abs(result["segment_model"]["lambda_hat"] - 0.62) < 0.02
    assert result["delta_aic_duration_minus_segment"] > 2.0


def test_duration_classification_requires_replication_across_nuisance_specs():
    assert (
        classify_duration_evidence(8.0, 4.0)
        == "SEGMENT_RETENTION_PREFERRED"
    )
    assert (
        classify_duration_evidence(-8.0, -4.0)
        == "CALENDAR_DURATION_DECAY_SUPPORTED"
    )
    assert (
        classify_duration_evidence(8.0, -4.0)
        == "SPECIFICATION_SENSITIVE_OR_INCONCLUSIVE"
    )
    assert (
        classify_duration_evidence(1.0, 7.0)
        == "SPECIFICATION_SENSITIVE_OR_INCONCLUSIVE"
    )


def test_equal_parameter_count_and_cluster_uncertainty_are_reported():
    x = np.linspace(-5, 5, 40)
    dt = np.linspace(1, 8, 40)
    z = np.ones((40, 1))
    groups = np.asarray([f"G{i // 4}" for i in range(40)])
    y = 0.5 * x + 2.0 + np.sin(np.arange(40)) * 0.01
    result = compare_segment_and_duration_models(
        origin_phase=x,
        destination_phase=y,
        duration_days=dt,
        nuisance=z,
        groups=groups,
    )
    assert (
        result["segment_model"]["n_parameters"]
        == result["calendar_duration_model"]["n_parameters"]
    )
    assert math.isfinite(result["segment_model"]["lambda_cluster_se"])
    assert math.isfinite(result["calendar_duration_model"]["k_cluster_se"])
