from src.kernel_barrier_resolution import barrier_resolution_certificate


def test_registered_triangular_barrier_converges_to_positive_jump_distance():
    result = barrier_resolution_certificate(
        kernel="triangular",
        gamma=-2.0,
        epsilon=0.3,
    )
    assert result.positive_barrier_resolved
    assert not result.resolution_limited
    assert result.tail_lower > 0.05
    assert result.tail_spread < 0.005


def test_registered_cosine_barrier_converges_to_positive_jump_distance():
    result = barrier_resolution_certificate(
        kernel="cosine",
        gamma=-3.0,
        epsilon=0.3,
    )
    assert result.positive_barrier_resolved
    assert result.tail_lower > 0.06
    assert result.tail_spread < 0.005


def test_registered_gaussian_barrier_survives_grid_refinement():
    result = barrier_resolution_certificate(
        kernel="gaussian",
        gamma=-20.0,
        epsilon=0.05,
    )
    assert result.positive_barrier_resolved
    assert result.tail_lower > 0.04
    assert result.tail_spread < 0.005


def test_adverse_control_shrinks_with_grid_resolution_instead_of_positive_limit():
    for kernel in ("triangular", "cosine", "gaussian"):
        result = barrier_resolution_certificate(
            kernel=kernel,
            gamma=-1.0,
            epsilon=0.1,
        )
        assert result.resolution_limited
        assert not result.positive_barrier_resolved
        assert result.critical_jump_bins == (1, 1, 1)
        assert result.critical_jump_distances[-1] < result.critical_jump_distances[0]
