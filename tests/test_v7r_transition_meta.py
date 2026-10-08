import pytest

from src.v7r_transition_meta import (
    TransitionMetaRow,
    exact_within_flyway_q_permutation,
    fit_meta,
)


def _rows(beta_qr=2.0):
    rows = []
    values = {
        "a": [(0.1, 1.0), (0.8, 0.5), (0.4, 0.2)],
        "b": [(0.2, 1.0), (0.9, 0.4), (0.5, 0.1)],
        "c": [(0.15, 1.0), (0.75, 0.6), (0.35, 0.25)],
    }
    fly_intercept = {"a": 0.1, "b": -0.1, "c": 0.0}
    for flyway, pairs in values.items():
        for q, r in pairs:
            correction = (
                fly_intercept[flyway]
                + 0.2 * q
                + 0.3 * r
                + beta_qr * q * r
            )
            rows.append(TransitionMetaRow(flyway, q, r, correction, 5.0))
    return rows


def test_meta_fit_recovers_exact_interaction_in_noise_free_fixture():
    out = fit_meta(_rows(beta_qr=1.7))
    assert out.beta_qr == pytest.approx(1.7, abs=1e-10)


def test_weighted_fit_uses_same_model_geometry():
    out = fit_meta(_rows(beta_qr=1.2), weighted=True)
    assert out.beta_qr == pytest.approx(1.2, abs=1e-10)


def test_exact_permutation_reports_positive_signal():
    out = exact_within_flyway_q_permutation(_rows(beta_qr=2.0))
    assert out.valid_permutations > 0
    assert out.observed_beta_qr > 0.0
    assert 0.0 < out.one_sided_p <= 1.0
    assert out.permutation_min <= out.permutation_median <= out.permutation_max


def test_q_outside_signed_unit_interval_fails_closed():
    rows = _rows()
    rows[0] = TransitionMetaRow("a", 1.1, 0.5, 0.0)
    with pytest.raises(ValueError, match="Q must"):
        fit_meta(rows)


def test_signed_q_is_allowed_for_frozen_sensitivity():
    rows = _rows()
    rows[0] = TransitionMetaRow("a", -0.4, 0.5, 0.0)
    out = fit_meta(rows)
    assert out.n == len(rows)


def test_r_outside_unit_interval_fails_closed():
    rows = _rows()
    rows[0] = TransitionMetaRow("a", 0.4, 1.1, 0.0)
    with pytest.raises(ValueError, match="R must"):
        fit_meta(rows)


def test_weighted_exact_permutation_uses_declared_weights():
    rows = _rows(beta_qr=1.3)
    weighted_rows = [
        TransitionMetaRow(
            row.flyway,
            row.q,
            row.r,
            row.correction,
            20.0 if i == 0 else 1.0,
        )
        for i, row in enumerate(rows)
    ]
    out = exact_within_flyway_q_permutation(weighted_rows, weighted=True)
    assert out.valid_permutations > 0
    assert 0.0 < out.one_sided_p <= 1.0


def test_runner_meta_rows_preserves_keyword_named_lambda_column():
    """Regression: pandas.itertuples() renames the 'lambda' column."""
    from scripts.run_v7r_direct_recourse_analysis import meta_rows

    class _Frame:
        def to_dict(self, orient):
            assert orient == "records"
            return [
                {
                    "flyway": "barents",
                    "n": 7,
                    "q_abs_r": 0.7,
                    "r_remaining_q10_q90": 0.2,
                    "lambda": -0.3,
                }
            ]

    rows = meta_rows(
        _Frame(),
        q="q_abs_r",
        r="r_remaining_q10_q90",
        response="lambda",
        weighted=True,
    )
    assert len(rows) == 1
    assert rows[0].correction == pytest.approx(-0.3)
    assert rows[0].weight == pytest.approx(7.0)
