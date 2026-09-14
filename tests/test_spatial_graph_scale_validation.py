import math

import pytest

from src.spatial_metapopulation import network_rhs, synchronous_mode_rates


SCALES = (1e-16, 1e-8, 1.0, 1e8, 1e16)


def test_symmetric_adjacency_is_accepted_at_every_graph_weight_scale():
    frequencies = (0.2, 0.8)
    for scale in SCALES:
        adjacency = ((0.0, scale), (scale, 0.0))
        rhs = network_rhs(
            frequencies,
            adjacency,
            migration_rate=0.3 / scale,
            phi=0.1,
            eta=-0.2,
        )
        assert len(rhs) == 2
        assert all(math.isfinite(value) for value in rhs)


def test_materially_asymmetric_adjacency_is_rejected_at_every_scale():
    frequencies = (0.2, 0.8)
    for scale in SCALES:
        adjacency = ((0.0, scale), (2.0 * scale, 0.0))
        with pytest.raises(ValueError, match="symmetric"):
            network_rhs(
                frequencies,
                adjacency,
                migration_rate=1.0,
                phi=0.0,
                eta=0.0,
            )


def test_nonfinite_adjacency_fails_closed():
    with pytest.raises(ValueError):
        network_rhs(
            (0.2, 0.8),
            ((0.0, float("nan")), (float("nan"), 0.0)),
            migration_rate=1.0,
            phi=0.0,
            eta=0.0,
        )


def test_laplacian_validation_tracks_spectrum_scale():
    reference = None
    for scale in SCALES:
        # The negative value is 1e-16 of the spectral scale and represents
        # ordinary roundoff leakage around the exact zero eigenvalue.
        eigenvalues = (-1e-16 * scale, 2.0 * scale)
        rates = synchronous_mode_rates(
            p_star=0.5,
            phi=0.0,
            eta=-1.0,
            migration_rate=0.3 / scale,
            laplacian_eigenvalues=eigenvalues,
        )
        if reference is None:
            reference = rates
        else:
            assert rates == pytest.approx(reference, rel=1e-12, abs=1e-15)


def test_materially_negative_laplacian_eigenvalue_is_rejected_at_every_scale():
    for scale in SCALES:
        with pytest.raises(ValueError, match="non-negative"):
            synchronous_mode_rates(
                p_star=0.5,
                phi=0.0,
                eta=-1.0,
                migration_rate=1.0,
                laplacian_eigenvalues=(-0.1 * scale, 1.0 * scale),
            )
