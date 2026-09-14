import pytest

from src.environment_mosaic import graph_laplacian
from src.spatial_environment_gradient import _validate_connected_adjacency


SCALES = (1e-16, 1e-8, 1.0, 1e8, 1e16)


def test_environment_mosaic_accepts_symmetric_graphs_at_every_scale():
    for scale in SCALES:
        lap = graph_laplacian(((0.0, scale), (scale, 0.0)))
        assert lap == [[scale, -scale], [-scale, scale]]


def test_environment_mosaic_rejects_material_asymmetry_at_every_scale():
    for scale in SCALES:
        with pytest.raises(ValueError, match="symmetric"):
            graph_laplacian(((0.0, scale), (2.0 * scale, 0.0)))


def test_spatial_gradient_accepts_connected_symmetric_graphs_at_every_scale():
    for scale in SCALES:
        _validate_connected_adjacency(
            (
                (0.0, scale, 0.0),
                (scale, 0.0, 2.0 * scale),
                (0.0, 2.0 * scale, 0.0),
            )
        )


def test_spatial_gradient_rejects_material_asymmetry_at_every_scale():
    for scale in SCALES:
        with pytest.raises(ValueError, match="symmetric"):
            _validate_connected_adjacency(
                ((0.0, scale), (2.0 * scale, 0.0))
            )


def test_derived_spatial_validators_fail_closed_on_nonfinite_weights():
    bad = ((0.0, float("nan")), (float("nan"), 0.0))
    with pytest.raises(ValueError):
        graph_laplacian(bad)
    with pytest.raises(ValueError):
        _validate_connected_adjacency(bad)
