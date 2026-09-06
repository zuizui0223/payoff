from collections import Counter

from src.architecture_phase_atlas import regular_grid
from src.kernel_accessibility_envelope import kernel_accessibility_envelope


KERNELS = ("hard", "triangular", "cosine", "gaussian")
GAMMAS = (-30.0, -20.0, -10.0, -5.0, -3.0, -2.0, -1.0, 0.0)
EPSILONS = (0.05, 0.1, 0.2, 0.3, 0.4)


def test_registered_kernel_robustness_sweep_counts():
    grid = regular_grid(1.0, 161)
    counts = Counter()
    robust_trapped = []
    for epsilon in EPSILONS:
        for gamma in GAMMAS:
            env = kernel_accessibility_envelope(
                grid,
                KERNELS,
                alpha=0.5,
                kappa=1.0,
                gamma=gamma,
                epsilon=epsilon,
                declared_jump_radius_bins=1,
            )
            counts[env.robustness_class] += 1
            if env.robustness_class == "all_trapped":
                robust_trapped.append((gamma, epsilon))

    assert counts == Counter({
        "kernel_sensitive": 21,
        "all_accessible": 18,
        "all_trapped": 1,
    })
    assert robust_trapped == [(-30.0, 0.05)]
