from src.spatial_metapopulation import classify_two_patch_polarization


SCALES = (1e-16, 1e-8, 1.0, 1e8, 1e16)


def test_two_patch_polarization_phase_is_invariant_to_rate_units():
    cases = (
        (0.10, "stable_polarized_patches"),
        (1.0 / 6.0, "polarized_stability_boundary"),
        (0.20, "polarized_saddle"),
        (0.25, "polarization_pitchfork_boundary"),
        (0.30, "no_polarized_equilibrium"),
    )

    for scale in SCALES:
        eta = 1.0 * scale
        for migration_ratio, expected in cases:
            migration = migration_ratio * scale
            assert classify_two_patch_polarization(eta, migration) == expected


def test_tiny_rates_do_not_collapse_strict_phases_to_boundaries():
    scale = 1e-16
    eta = scale
    assert (
        classify_two_patch_polarization(eta, 0.10 * scale)
        == "stable_polarized_patches"
    )
    assert (
        classify_two_patch_polarization(eta, 0.20 * scale)
        == "polarized_saddle"
    )
    assert (
        classify_two_patch_polarization(eta, 0.30 * scale)
        == "no_polarized_equilibrium"
    )
