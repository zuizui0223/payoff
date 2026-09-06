"""Environment-mosaic extension of the PAYOFF spatial game.

Each patch j has its own static architecture gap
    phi_j = s_j L_j - K_j
and frequency-feedback coefficient eta_j.

Rare differentiated architecture in an all-S landscape has local linear margin
    rD_j = phi_j - eta_j,
while rare shared architecture in an all-D landscape has
    rS_j = -phi_j - eta_j.

On an undirected patch graph with Laplacian L_G and migration rate m, the
linearized invasion operators are
    diag(rD) - m L_G
and
    diag(rS) - m L_G.
Their largest eigenvalues are the metapopulation invasion exponents.
"""

from __future__ import annotations

from math import sqrt
from typing import Dict, List, Sequence, Tuple


def patch_phi(
    conflict_loads: Sequence[float],
    separation_fractions: Sequence[float],
    architecture_costs: Sequence[float],
) -> List[float]:
    """Return patch-specific phi_j=s_j L_j-K_j."""

    if not (
        len(conflict_loads)
        == len(separation_fractions)
        == len(architecture_costs)
        and conflict_loads
    ):
        raise ValueError("patch parameter arrays must have the same non-zero length")
    out: List[float] = []
    for load, separation, cost in zip(
        conflict_loads, separation_fractions, architecture_costs
    ):
        if load < 0.0:
            raise ValueError("conflict loads must be non-negative")
        if not 0.0 <= separation <= 1.0:
            raise ValueError("separation fractions must lie in [0,1]")
        if cost < 0.0:
            raise ValueError("architecture costs must be non-negative")
        out.append(separation * load - cost)
    return out


def invasion_margins(
    phis: Sequence[float], etas: Sequence[float]
) -> Tuple[List[float], List[float]]:
    """Return local rare-D and rare-S invasion margins."""

    _validate_same_nonzero_length(phis, etas)
    return (
        [phi - eta for phi, eta in zip(phis, etas)],
        [-phi - eta for phi, eta in zip(phis, etas)],
    )


def heterogeneous_mean_selection(
    frequencies: Sequence[float], phis: Sequence[float], etas: Sequence[float]
) -> Dict[str, float]:
    """Exact spatial-average decomposition for heterogeneous patch games.

    Let g_j=p_j(1-p_j), h_j=g_j(2p_j-1). Then

        mean(selection)
        = mean(phi) mean(g) + Cov(phi,g)
        + mean(eta) mean(h) + Cov(eta,h).

    Migration on a symmetric graph contributes zero directly to the patch mean.
    """

    _validate_same_nonzero_length(frequencies, phis, etas)
    if any(not 0.0 <= p <= 1.0 for p in frequencies):
        raise ValueError("frequencies must lie in [0,1]")

    g = [p * (1.0 - p) for p in frequencies]
    h = [gi * (2.0 * p - 1.0) for gi, p in zip(g, frequencies)]
    mean_phi = _mean(phis)
    mean_eta = _mean(etas)
    mean_g = _mean(g)
    mean_h = _mean(h)
    cov_phi_g = _covariance(phis, g)
    cov_eta_h = _covariance(etas, h)
    direct = _mean(
        [phi * gi + eta * hi for phi, eta, gi, hi in zip(phis, etas, g, h)]
    )
    reconstructed = (
        mean_phi * mean_g + cov_phi_g + mean_eta * mean_h + cov_eta_h
    )
    return {
        "mean_frequency": _mean(frequencies),
        "mean_phi": mean_phi,
        "mean_eta": mean_eta,
        "mean_p1mp": mean_g,
        "mean_p1mp_2pm1": mean_h,
        "cov_phi_p1mp": cov_phi_g,
        "cov_eta_p1mp_2pm1": cov_eta_h,
        "mean_selection": direct,
        "reconstructed_mean_selection": reconstructed,
    }


def graph_laplacian(adjacency: Sequence[Sequence[float]]) -> List[List[float]]:
    """Return the Laplacian of a symmetric non-negative weighted graph."""

    _validate_adjacency(adjacency)
    n = len(adjacency)
    lap = [[0.0] * n for _ in range(n)]
    for i in range(n):
        degree = sum(adjacency[i])
        lap[i][i] = degree
        for j in range(n):
            if i != j:
                lap[i][j] = -adjacency[i][j]
    return lap


def invasion_operator(
    margins: Sequence[float],
    adjacency: Sequence[Sequence[float]],
    migration_rate: float,
) -> List[List[float]]:
    """Return diag(margins)-m L_G."""

    if migration_rate < 0.0:
        raise ValueError("migration_rate must be non-negative")
    _validate_adjacency(adjacency)
    if len(margins) != len(adjacency):
        raise ValueError("one invasion margin is required per patch")
    lap = graph_laplacian(adjacency)
    n = len(margins)
    matrix = [[-migration_rate * lap[i][j] for j in range(n)] for i in range(n)]
    for i, margin in enumerate(margins):
        matrix[i][i] += margin
    return matrix


def invasion_exponent(
    margins: Sequence[float],
    adjacency: Sequence[Sequence[float]],
    migration_rate: float,
) -> float:
    """Largest eigenvalue of the symmetric rare-type invasion operator."""

    matrix = invasion_operator(margins, adjacency, migration_rate)
    return largest_symmetric_eigenvalue(matrix)


def d_invasion_exponent(
    phis: Sequence[float],
    etas: Sequence[float],
    adjacency: Sequence[Sequence[float]],
    migration_rate: float,
) -> float:
    """Metapopulation growth exponent of rare D in an all-S landscape."""

    d_margins, _ = invasion_margins(phis, etas)
    return invasion_exponent(d_margins, adjacency, migration_rate)


def s_invasion_exponent(
    phis: Sequence[float],
    etas: Sequence[float],
    adjacency: Sequence[Sequence[float]],
    migration_rate: float,
) -> float:
    """Metapopulation growth exponent of rare S in an all-D landscape."""

    _, s_margins = invasion_margins(phis, etas)
    return invasion_exponent(s_margins, adjacency, migration_rate)


def source_sink_summary(margins: Sequence[float]) -> Dict[str, float]:
    """Return no-migration and strong-migration endpoint diagnostics."""

    if not margins:
        raise ValueError("margins cannot be empty")
    return {
        "min_local_margin": min(margins),
        "max_local_margin": max(margins),
        "mean_local_margin": _mean(margins),
    }


def critical_migration_rate(
    margins: Sequence[float],
    adjacency: Sequence[Sequence[float]],
    tol: float = 1e-10,
    max_iterations: int = 200,
) -> float:
    """Return the unique source-sink rescue threshold m_c.

    This routine applies to a connected undirected graph with heterogeneous
    margins satisfying max(r_j)>0>mean(r_j). Under these conditions the largest
    eigenvalue of diag(r)-mL decreases strictly from max(r_j) to mean(r_j), so
    there is one finite positive crossing.
    """

    _validate_adjacency(adjacency)
    if len(margins) != len(adjacency):
        raise ValueError("one margin is required per patch")
    if not _is_connected(adjacency):
        raise ValueError("critical migration theorem requires a connected graph")
    if not (max(margins) > 0.0 and _mean(margins) < 0.0):
        raise ValueError("requires max local margin > 0 > mean local margin")
    if len(set(round(x, 15) for x in margins)) == 1:
        raise ValueError("requires heterogeneous margins")

    lower = 0.0
    upper = 1.0
    while invasion_exponent(margins, adjacency, upper) > 0.0:
        upper *= 2.0
        if upper > 1e15:
            raise RuntimeError("failed to bracket migration threshold")

    for _ in range(max_iterations):
        mid = 0.5 * (lower + upper)
        value = invasion_exponent(margins, adjacency, mid)
        if abs(value) <= tol or upper - lower <= tol:
            return mid
        if value > 0.0:
            lower = mid
        else:
            upper = mid
    return 0.5 * (lower + upper)


def two_patch_invasion_exponent(r1: float, r2: float, migration_rate: float) -> float:
    """Exact principal exponent for two unit-coupled patches."""

    if migration_rate < 0.0:
        raise ValueError("migration_rate must be non-negative")
    return 0.5 * (
        r1 + r2 - 2.0 * migration_rate
        + sqrt((r1 - r2) ** 2 + 4.0 * migration_rate**2)
    )


def two_patch_rescue_threshold(r1: float, r2: float) -> float:
    """Exact migration threshold for one-source/one-sink with negative mean.

    Requires one margin positive, the other negative, and r1+r2<0. Then
        m_c = r1*r2/(r1+r2) > 0.
    """

    if not (r1 * r2 < 0.0 and r1 + r2 < 0.0):
        raise ValueError("requires opposite-sign margins with negative mean")
    return r1 * r2 / (r1 + r2)


def largest_symmetric_eigenvalue(
    matrix: Sequence[Sequence[float]], tol: float = 1e-13, max_rotations: int = 100000
) -> float:
    """Largest eigenvalue of a real symmetric matrix via Jacobi rotations."""

    n = len(matrix)
    if n == 0 or any(len(row) != n for row in matrix):
        raise ValueError("matrix must be non-empty and square")
    a = [[float(matrix[i][j]) for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if abs(a[i][j] - a[j][i]) > 1e-10:
                raise ValueError("matrix must be symmetric")
    if n == 1:
        return a[0][0]

    for _ in range(max_rotations):
        p, q = 0, 1
        maximum = abs(a[p][q])
        for i in range(n):
            for j in range(i + 1, n):
                value = abs(a[i][j])
                if value > maximum:
                    maximum = value
                    p, q = i, j
        if maximum <= tol:
            return max(a[i][i] for i in range(n))

        app = a[p][p]
        aqq = a[q][q]
        apq = a[p][q]
        tau = (aqq - app) / (2.0 * apq)
        if tau >= 0.0:
            t = 1.0 / (tau + sqrt(1.0 + tau * tau))
        else:
            t = -1.0 / (-tau + sqrt(1.0 + tau * tau))
        c = 1.0 / sqrt(1.0 + t * t)
        s = t * c

        for k in range(n):
            if k == p or k == q:
                continue
            akp = a[k][p]
            akq = a[k][q]
            new_kp = c * akp - s * akq
            new_kq = s * akp + c * akq
            a[k][p] = a[p][k] = new_kp
            a[k][q] = a[q][k] = new_kq

        a[p][p] = c * c * app - 2.0 * s * c * apq + s * s * aqq
        a[q][q] = s * s * app + 2.0 * s * c * apq + c * c * aqq
        a[p][q] = a[q][p] = 0.0

    raise RuntimeError("Jacobi eigenvalue solver did not converge")


def _mean(values: Sequence[float]) -> float:
    return sum(values) / len(values)


def _covariance(x: Sequence[float], y: Sequence[float]) -> float:
    _validate_same_nonzero_length(x, y)
    mx = _mean(x)
    my = _mean(y)
    return _mean([(a - mx) * (b - my) for a, b in zip(x, y)])


def _validate_same_nonzero_length(*arrays: Sequence[float]) -> None:
    if not arrays or not arrays[0]:
        raise ValueError("arrays cannot be empty")
    n = len(arrays[0])
    if any(len(array) != n for array in arrays):
        raise ValueError("arrays must have the same length")


def _validate_adjacency(adjacency: Sequence[Sequence[float]]) -> None:
    n = len(adjacency)
    if n == 0 or any(len(row) != n for row in adjacency):
        raise ValueError("adjacency must be non-empty and square")
    for i in range(n):
        for j in range(n):
            if adjacency[i][j] < 0.0:
                raise ValueError("adjacency weights must be non-negative")
            if abs(adjacency[i][j] - adjacency[j][i]) > 1e-12:
                raise ValueError("adjacency must be symmetric")


def _is_connected(adjacency: Sequence[Sequence[float]]) -> bool:
    n = len(adjacency)
    seen = {0}
    stack = [0]
    while stack:
        i = stack.pop()
        for j, weight in enumerate(adjacency[i]):
            if weight > 0.0 and j not in seen:
                seen.add(j)
                stack.append(j)
    return len(seen) == n
