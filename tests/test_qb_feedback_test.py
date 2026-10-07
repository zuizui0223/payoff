import pytest

from src.qb_feedback_test import (
    FeedbackBehaviorRow,
    exact_origin_region_qb_permutation,
    fit_feedback_model,
)


def _fixture(beta=-0.8):
    rows = []
    q = {
        ("a", "R1"): -1.0,
        ("a", "R2"): 1.0,
        ("b", "R1"): -0.5,
        ("b", "R2"): 0.5,
        ("c", "R1"): -1.2,
        ("c", "R2"): -0.2,
        ("c", "R3"): 0.4,
        ("c", "R4"): 0.9,
        ("c", "R5"): 1.3,
    }
    transition_index = 0
    for flyway, origins in {
        "a": ["R1", "R2"],
        "b": ["R1", "R2"],
        "c": ["R1", "R2", "R3", "R4", "R5"],
    }.items():
        for origin in origins:
            transition = f"{flyway}:{origin}->X{transition_index}"
            r = 1.0 - 0.08 * transition_index
            for j, e in enumerate((-2.0, -1.0, 1.0, 2.0)):
                stop = (
                    5.0
                    + 0.3 * transition_index
                    - 0.2 * e
                    + 0.1 * e * r
                    + 0.05 * e * q[(flyway, origin)]
                    + beta * e * q[(flyway, origin)] * r
                    + 0.001 * j
                )
                rows.append(
                    FeedbackBehaviorRow(
                        flyway=flyway,
                        transition_id=transition,
                        origin_region=origin,
                        incoming_phase_error=e,
                        stopover_days=stop,
                        retained_recourse=r,
                    )
                )
            transition_index += 1
    return rows, q


def test_feedback_fit_recovers_negative_triple_interaction():
    rows, q = _fixture(beta=-0.7)
    out = fit_feedback_model(rows, q)
    assert out.beta_e_qb_r == pytest.approx(-0.7, abs=0.01)


def test_permutation_space_is_region_level_2x2x5_factorial():
    rows, q = _fixture(beta=-1.0)
    out = exact_origin_region_qb_permutation(rows, q)
    assert out.total_permutations == 480
    assert out.valid_permutations > 0
    assert out.observed_beta_e_qb_r < 0.0
    assert 0.0 < out.one_sided_p <= 1.0


def test_missing_origin_qb_fails_closed():
    rows, q = _fixture()
    del q[("a", "R1")]
    with pytest.raises(ValueError, match="missing q_B"):
        fit_feedback_model(rows, q)
