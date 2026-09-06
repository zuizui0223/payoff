from math import isclose

from src.hard_module_cost_identification import (
    constant_kappa_max_abs_residual,
    partition_cost_receipt,
    weighted_constant_kappa_fit,
)


def test_single_partition_identifies_kappa():
    receipt = partition_cost_receipt(
        recovery=25.0 / 6.0,
        direct_margin=19.0 / 6.0,
        module_count=2,
    )
    assert isclose(receipt["implied_total_cost"], 1.0, rel_tol=1e-12)
    assert isclose(receipt["implied_kappa"], 1.0, rel_tol=1e-12)


def test_registered_three_function_two_worldlines_overidentify_kappa_one():
    recoveries = [25.0 / 6.0, 14.0 / 3.0]
    direct_margins = [19.0 / 6.0, 8.0 / 3.0]
    module_counts = [2, 3]
    fit = weighted_constant_kappa_fit(recoveries, direct_margins, module_counts)
    assert isclose(fit["kappa_hat"], 1.0, rel_tol=1e-12)
    assert all(isclose(value, 1.0, rel_tol=1e-12) for value in fit["implied_kappas"])
    assert all(abs(value) < 1e-12 for value in fit["residuals"])
    assert isclose(fit["weighted_sse"], 0.0, abs_tol=1e-12)
    assert isclose(
        constant_kappa_max_abs_residual(
            recoveries, direct_margins, module_counts
        ),
        0.0,
        abs_tol=1e-12,
    )


def test_inconsistent_partition_costs_leave_bridge_residual():
    recoveries = [25.0 / 6.0, 14.0 / 3.0]
    direct_margins = [19.0 / 6.0, 3.0]
    module_counts = [2, 3]
    fit = weighted_constant_kappa_fit(recoveries, direct_margins, module_counts)
    assert fit["weighted_sse"] > 0.0
    assert max(abs(value) for value in fit["residuals"]) > 0.0
    assert not isclose(fit["implied_kappas"][0], fit["implied_kappas"][1])


def test_analysis_weights_change_fit_when_receipts_conflict():
    recoveries = [4.0, 6.0]
    direct_margins = [3.0, 3.0]
    module_counts = [2, 3]
    unweighted = weighted_constant_kappa_fit(
        recoveries, direct_margins, module_counts
    )
    weighted = weighted_constant_kappa_fit(
        recoveries, direct_margins, module_counts, analysis_weights=[100.0, 1.0]
    )
    assert weighted["kappa_hat"] < unweighted["kappa_hat"]
    assert abs(weighted["kappa_hat"] - 1.0) < abs(unweighted["kappa_hat"] - 1.0)
