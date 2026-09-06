from math import isclose

from src.hard_partition_feedback_identification import (
    architecture_phi_residual,
    endpoint_gap_inversion,
    gamma_from_endpoint_gaps,
    gamma_from_reciprocal_invasions,
    reciprocal_invasion_inversion,
    weighted_common_gamma_fit,
)


def test_endpoint_gap_inversion_registered_MF_pair():
    result = endpoint_gap_inversion(0.5, -1.5)
    assert isclose(result["phi"], -0.5, rel_tol=1e-12)
    assert isclose(result["eta"], -1.0, rel_tol=1e-12)

    gamma = gamma_from_endpoint_gaps(0.5, -1.5, 1.0)
    assert isclose(gamma["gamma"], -1.0, rel_tol=1e-12)
    assert isclose(
        architecture_phi_residual(gamma["phi"], 19.0 / 6.0, 8.0 / 3.0),
        0.0,
        abs_tol=1e-12,
    )


def test_reciprocal_invasion_form_matches_endpoint_form():
    # For phi=-1/2, eta=-1:
    # second (F) into first (M): phi-eta=+1/2
    # first (M) into second (F): -phi-eta=+3/2
    result = reciprocal_invasion_inversion(0.5, 1.5)
    assert isclose(result["phi"], -0.5, rel_tol=1e-12)
    assert isclose(result["eta"], -1.0, rel_tol=1e-12)
    gamma = gamma_from_reciprocal_invasions(0.5, 1.5, 1.0)
    assert isclose(gamma["gamma"], -1.0, rel_tol=1e-12)


def test_two_partition_pairs_overidentify_common_gamma():
    # M-F: q=1, eta=-1
    # S-M: q=2, eta=-2
    fit = weighted_common_gamma_fit(
        etas=[-1.0, -2.0],
        partition_distances=[1.0, 2.0],
    )
    assert isclose(fit["gamma_hat"], -1.0, rel_tol=1e-12)
    assert all(isclose(value, -1.0, rel_tol=1e-12) for value in fit["implied_gammas"])
    assert all(abs(value) < 1e-12 for value in fit["residuals"])
    assert isclose(fit["weighted_sse"], 0.0, abs_tol=1e-12)


def test_distance_kernel_failure_leaves_feedback_residual():
    fit = weighted_common_gamma_fit(
        etas=[-1.0, -1.2],
        partition_distances=[1.0, 2.0],
    )
    assert fit["weighted_sse"] > 0.0
    assert max(abs(value) for value in fit["residuals"]) > 0.0
    assert not isclose(fit["implied_gammas"][0], fit["implied_gammas"][1])


def test_analysis_weights_move_gamma_toward_high_weight_pair():
    unweighted = weighted_common_gamma_fit(
        etas=[-1.0, -1.2],
        partition_distances=[1.0, 2.0],
    )
    weighted = weighted_common_gamma_fit(
        etas=[-1.0, -1.2],
        partition_distances=[1.0, 2.0],
        analysis_weights=[100.0, 1.0],
    )
    assert abs(weighted["gamma_hat"] + 1.0) < abs(unweighted["gamma_hat"] + 1.0)
