"""KKT audit for finite hard-partition games with negative feedback.

Returns numerical global-maximizer certificates on the declared candidate set.
Concavity implies neither a unique architecture mixture nor creation of absent
strategies. Degenerate optimal faces are represented by their extreme mixtures.
See theory/FULL_PARTITION_EQUILIBRIUM_AUDIT.md for proofs and claim boundaries.
"""
from __future__ import annotations

from itertools import combinations
from math import fsum, isfinite
from numbers import Integral
from typing import Dict, Iterable, Sequence, Tuple


def _finite(value, name):
    value = float(value)
    if not isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


def _positive_integer(value, name):
    if isinstance(value, bool) or not isinstance(value, Integral) or value < 1:
        raise ValueError(f"{name} must be a positive integer")
    return int(value)


def _prepare(intrinsic_payoffs, partitions, n, gamma, pair_weights, tol):
    n = _positive_integer(n, "n")
    gamma = _finite(gamma, "gamma")
    tol = _finite(tol, "tol")
    if gamma >= 0 or not 0 < tol < 1e-3:
        raise ValueError("requires gamma<0 and 0<tol<1e-3")
    if not partitions or len(intrinsic_payoffs) != len(partitions):
        raise ValueError("payoffs and partitions must have equal non-zero length")
    b = tuple(_finite(x, "intrinsic payoff") for x in intrinsic_payoffs)
    normalized = []
    features = []
    for partition in partitions:
        modules = []
        for module in partition:
            members = tuple(module)
            if not members or any(isinstance(i, bool) or not isinstance(i, Integral) for i in members):
                raise ValueError("modules need non-empty integer member indices")
            modules.append(tuple(sorted(int(i) for i in members)))
        if sorted(i for module in modules for i in module) != list(range(n)):
            raise ValueError("partition must contain every function exactly once")
        normalized.append(tuple(sorted(modules)))
        labels = {i: j for j, module in enumerate(modules) for i in module}
        features.append(tuple(int(labels[i] == labels[j]) for i in range(n) for j in range(i + 1, n)))
    if len(set(normalized)) != len(normalized):
        raise ValueError("candidate partitions must be distinct")
    dimension = n * (n - 1) // 2
    weights = (1.0,) * dimension if pair_weights is None else tuple(_finite(w, "pair weight") for w in pair_weights)
    if len(weights) != dimension or any(w <= 0 for w in weights):
        raise ValueError("one positive weight per unordered function pair is required")
    distances = tuple(tuple(fsum(w * (x - y) ** 2 for w, x, y in zip(weights, left, right)) for right in features) for left in features)
    # Remove a common payoff offset, then normalize before solving the KKT system.
    base = min(b)
    centered = tuple(x - base for x in b)
    scale = max(max(centered), -gamma * max(max(row) for row in distances))
    if not isfinite(scale) or not isfinite(2 * base):
        raise ValueError("payoff range overflows; rescale the input")
    if scale == 0:
        scale = 1.0  # The one-candidate game has no payoff differences.
    matrix = tuple(tuple(centered[i] / scale + centered[j] / scale + (-gamma / scale) * distances[i][j] for j in range(len(b))) for i in range(len(b)))
    return matrix, tuple(features), weights, scale, 2 * base, tol


def _matrix_vector(matrix, vector):
    return tuple(fsum(a * p for a, p in zip(row, vector)) for row in matrix)


def _rank(rows, tol=1e-12):
    work = [list(map(float, row)) for row in rows]
    if not work:
        return 0
    rank = 0
    for col in range(len(work[0])):
        pivot = max(range(rank, len(work)), key=lambda r: abs(work[r][col]), default=None)
        if pivot is None or abs(work[pivot][col]) <= tol:
            continue
        work[rank], work[pivot] = work[pivot], work[rank]
        divisor = work[rank][col]
        work[rank] = [v / divisor for v in work[rank]]
        for r in range(rank + 1, len(work)):
            factor = work[r][col]
            work[r] = [v - factor * w for v, w in zip(work[r], work[rank])]
        rank += 1
        if rank == len(work):
            break
    return rank


def _solve_linear_system(matrix, rhs):
    n = len(rhs)
    augmented = [list(row) + [target] for row, target in zip(matrix, rhs)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(augmented[r][col]))
        if abs(augmented[pivot][col]) < 1e-13:
            raise ValueError("singular KKT support")
        augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
        divisor = augmented[col][col]
        augmented[col] = [v / divisor for v in augmented[col]]
        for r in range(n):
            if r == col:
                continue
            factor = augmented[r][col]
            augmented[r] = [v - factor * w for v, w in zip(augmented[r], augmented[col])]
    return tuple(row[-1] for row in augmented)


def _solve_support_kkt(matrix, support: Tuple[int, ...], tol: float):
    size = len(support)
    system = [[matrix[i][j] for j in support] + [-1.0] for i in support]
    system.append([1.0] * size + [0.0])
    try:
        solution = _solve_linear_system(system, [0.0] * size + [1.0])
    except ValueError:
        return None
    if any(value <= tol for value in solution[:-1]):
        return None
    total = fsum(solution[:-1])
    if abs(total - 1) > 100 * tol:
        return None
    p = [0.0] * len(matrix)
    for i, value in zip(support, solution[:-1]):
        p[i] = value / total
    u = _matrix_vector(matrix, p)
    mean = fsum(pi * ui for pi, ui in zip(p, u))
    if max(u) - mean > 10 * tol or max(abs(u[i] - mean) for i in support) > 10 * tol:
        return None
    return tuple(p), mean


def audit_partition_mixture(intrinsic_payoffs, partitions, frequencies, n, gamma, pair_weights=None, tol=1e-10):
    """Check all declared invaders, not just strategies currently present."""
    matrix, features, weights, scale, offset, tol = _prepare(intrinsic_payoffs, partitions, n, gamma, pair_weights, tol)
    p = tuple(_finite(value, "frequency") for value in frequencies)
    if len(p) != len(matrix) or any(value < 0 for value in p) or abs(fsum(p) - 1) > tol:
        raise ValueError("frequencies must be a simplex vector matching candidates")
    u = _matrix_vector(matrix, p)
    mean = fsum(pi * ui for pi, ui in zip(p, u))
    margins = tuple(ui - mean for ui in u)
    active = tuple(i for i, value in enumerate(p) if value > tol)
    residual = max(max(margins), max((abs(margins[i]) for i in active), default=0.0))
    return {
        "invasion_margins": tuple(scale * value for value in margins),
        "normalized_kkt_residual": residual,
        "kkt_within_tolerance": residual <= 10 * tol,
        "invadable_candidate_indices": tuple(i for i, value in enumerate(margins) if value > 10 * tol),
        "comembership_marginals": tuple(fsum(pi * row[j] for pi, row in zip(p, features)) for j in range(len(weights))),
        "potential": scale * mean + offset,
    }


def stable_negative_feedback_mixture(
    intrinsic_payoffs: Sequence[float],
    partitions: Sequence[Sequence[Iterable[int]]],
    n: int,
    gamma: float,
    pair_weights: Sequence[float] | None = None,
    tol: float = 1e-10,
    max_strategies: int = 12,
) -> Dict[str, object]:
    """Return an audited numerical maximizer and bounds across optimal vertices.

    Enumerates supports up to the affine feature rank. Numerical uniqueness is
    tolerance-dependent; the certificate is not an interval-arithmetic proof.
    No claim is made about partitions omitted from the candidate set.
    """
    max_strategies = _positive_integer(max_strategies, "max_strategies")
    if len(partitions) > max_strategies:
        raise ValueError("candidate strategy count exceeds support-enumeration limit")
    matrix, features, weights, scale, offset, tol = _prepare(intrinsic_payoffs, partitions, n, gamma, pair_weights, tol)
    m = len(matrix)
    affine_rank = _rank([(1.0,) + row for row in features])
    candidates = []
    for size in range(1, min(m, affine_rank) + 1):
        for support in combinations(range(m), size):
            # Extreme optimal mixtures have affinely independent feature vectors.
            if _rank([(1.0,) + features[i] for i in support]) < size:
                continue
            solved = _solve_support_kkt(matrix, support, tol)
            if solved is not None:
                p, potential = solved
                candidates.append((support, p, potential))
    if not candidates:
        raise RuntimeError("no numerical KKT certificate found; inspect conditioning/tolerance")
    peak = max(row[2] for row in candidates)
    tied = [row for row in candidates if peak - row[2] <= 100 * tol]
    tied.sort(key=lambda row: (len(row[0]), row[0]))
    support, p, potential = tied[0]
    frequency_bounds = tuple((min(row[1][i] for row in tied), max(row[1][i] for row in tied)) for i in range(m))
    u = _matrix_vector(matrix, p)
    marginal_vectors = [tuple(fsum(pi * feature[j] for pi, feature in zip(row[1], features)) for j in range(len(weights))) for row in tied]
    marginal_spread = max((max(v[j] for v in marginal_vectors) - min(v[j] for v in marginal_vectors) for j in range(len(weights))), default=0.0)
    residual = max(max(u) - potential, max(abs(u[i] - potential) for i in support))
    return {
        "support": support,
        "frequencies": p,
        "lagrange_payoff": scale * potential + offset,
        "strategy_payoffs": tuple(scale * value + offset for value in u),
        "potential": scale * potential + offset,
        "candidate_kkt_count": len(candidates),
        "tied_global_kkt_count": len(tied),
        "equilibrium_vertex_frequencies": tuple(row[1] for row in tied),
        "equilibrium_frequency_bounds": frequency_bounds,
        "numerically_unique": all(hi - lo <= 100 * tol for lo, hi in frequency_bounds),
        "comembership_marginals": marginal_vectors[0],
        "max_equilibrium_marginal_disagreement": marginal_spread,
        "feature_affine_rank": affine_rank,
        "support_size_bound": affine_rank,
        "normalized_kkt_residual": residual,
        "maximum_invasion_advantage": scale * max(0.0, max(u) - potential),
        "invasion_margins": tuple(scale * (value - potential) for value in u),
        "payoff_normalization_scale": scale,
        "certificate_kind": "FLOATING_POINT_KKT_NOT_INTERVAL_PROOF",
        "scope": "DECLARED_CANDIDATE_SET_ONLY",
    }
