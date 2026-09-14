from src.spatial_environment_gradient import (
    classify_two_patch_midpoint,
    two_patch_coordination_switch_rate,
    two_patch_midpoint_exponent,
)


SCALES = (1e-16, 1e-8, 1.0, 1e8, 1e16)
PHI_1 = 0.6
PHI_2 = -0.6
ETA = 0.1
SWITCH = two_patch_coordination_switch_rate(PHI_1, PHI_2, ETA)


def _classify(scale: float, migration: float) -> str:
    return classify_two_patch_midpoint(
        scale * PHI_1,
        scale * PHI_2,
        scale * ETA,
        scale * migration,
    )


def test_all_midpoint_phase_labels_are_invariant_to_rate_scale():
    for scale in SCALES:
        assert _classify(scale, 1.0) == "reciprocal_spatial_invasion"
        assert _classify(scale, SWITCH) == "spatial_coordination_switch_boundary"
        assert _classify(scale, 2.5) == "mutual_spatial_noninvasion"


def test_tiny_strict_positive_exponent_is_not_collapsed_to_boundary():
    scale = 1e-16
    exponent = two_patch_midpoint_exponent(
        scale * PHI_1,
        scale * PHI_2,
        scale * ETA,
        scale * 1.0,
    )
    assert 0.0 < exponent < 1e-12
    assert _classify(scale, 1.0) == "reciprocal_spatial_invasion"


def test_common_phi_baseline_does_not_change_midpoint_phase_label():
    for scale in SCALES:
        offset = 1e6 * scale
        observed = classify_two_patch_midpoint(
            offset + scale * PHI_1,
            offset + scale * PHI_2,
            scale * ETA,
            scale * 1.0,
        )
        assert observed == "reciprocal_spatial_invasion"
