from fractions import Fraction as F
from itertools import product

from src.frequency_holdout_detection import comparison_nondetection_threshold
from src.frequency_response_holdout import validate_frequency_response_holdouts


def gate(u_band, v_band, p, y_band):
    return validate_frequency_response_holdouts(
        u_band, v_band, [(p, y_band)],
        support_reference="synthetic_bounded_error_integration",
        resident_contexts_matched_declared=True,
        common_oriented_gap_scale_declared=True,
    )


def band(center, halfwidth):
    return center-halfwidth, center+halfwidth


def test_residual_strictly_above_threshold_rejects_for_every_error_corner():
    p = F(1,3)
    u, v = F(2,5), F(-1,5)
    eu, ev, eh = F(1,10), F(1,20), F(1,25)
    line = (1-p)*u-p*v
    threshold = comparison_nondetection_threshold(
        p, endpoint_u_error_halfwidth=eu, endpoint_v_error_halfwidth=ev,
        interior_error_halfwidth=eh)
    true_y = line + threshold + F(1,1000)

    for su, sv, sy in product((-1,1), repeat=3):
        u_hat, v_hat, y_hat = u+su*eu, v+sv*ev, true_y+sy*eh
        receipt = gate(band(u_hat,eu), band(v_hat,ev), p, band(y_hat,eh))
        assert not receipt.all_holdouts_compatible
        assert receipt.status == "canonical_linear_frequency_response_rejected_by_holdout"


def test_exact_threshold_can_escape_by_closed_band_contact():
    p = F(1,3)
    u, v = F(2,5), F(-1,5)
    eu, ev, eh = F(1,10), F(1,20), F(1,25)
    line = (1-p)*u-p*v
    threshold = comparison_nondetection_threshold(
        p, endpoint_u_error_halfwidth=eu, endpoint_v_error_halfwidth=ev,
        interior_error_halfwidth=eh)
    true_y = line + threshold

    # For a positive residual, shift the predicted endpoint line upward as far as
    # allowed and the observed interior centre downward as far as allowed.
    u_hat, v_hat, y_hat = u+eu, v-ev, true_y-eh
    receipt = gate(band(u_hat,eu), band(v_hat,ev), p, band(y_hat,eh))
    assert receipt.all_holdouts_compatible
    assert receipt.holdouts[0].overlap_band_exact is not None
    lo, hi = map(F, receipt.holdouts[0].overlap_band_exact)
    assert lo == hi  # exact closed-band contact witnesses the excluded boundary
