"""Exact small-sample meta-model for PAYOFF-B V7R.

Transition is the analysis unit.  The primary model is

    C = flyway fixed effects + beta_Q Q + beta_R R + beta_QR Q*R + error.

Primary inference permutes Q labels only within flyway while holding C and R
fixed.  This preserves flyway-specific Q distributions and route structure.

The implementation is dependency-free so the exact permutation test runs in
the base repository CI environment.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations, product
from math import isfinite
from typing import Iterable, Sequence


_TOL = 1e-12


@dataclass(frozen=True)
class TransitionMetaRow:
    flyway: str
    q: float
    r: float
    correction: float
    weight: float = 1.0


@dataclass(frozen=True)
class MetaFit:
    coefficient_names: tuple[str, ...]
    coefficients: tuple[float, ...]
    beta_qr: float
    rss: float
    n: int


@dataclass(frozen=True)
class ExactPermutationResult:
    observed_beta_qr: float
    total_permutations: int
    valid_permutations: int
    count_at_least_observed: int
    one_sided_p: float
    permutation_min: float
    permutation_median: float
    permutation_max: float


def _solve(a: list[list[float]], b: list[float]) -> list[float]:
    n = len(b)
    aug = [list(map(float, a[i])) + [float(b[i])] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda row: abs(aug[row][col]))
        if abs(aug[pivot][col]) <= _TOL:
            raise ValueError("singular design matrix")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        scale = aug[col][col]
        aug[col] = [v / scale for v in aug[col]]
        for row in range(n):
            if row == col:
                continue
            factor = aug[row][col]
            if abs(factor) <= _TOL:
                continue
            aug[row] = [
                aug[row][j] - factor * aug[col][j]
                for j in range(n + 1)
            ]
    return [aug[i][-1] for i in range(n)]


def _median(values: Sequence[float]) -> float:
    xs = sorted(values)
    n = len(xs)
    if n % 2:
        return float(xs[n // 2])
    return 0.5 * (xs[n // 2 - 1] + xs[n // 2])


def fit_meta(rows: Iterable[TransitionMetaRow], *, weighted: bool = False) -> MetaFit:
    data = list(rows)
    if len(data) < 7:
        raise ValueError("at least seven transition rows are required")
    flyways = sorted({str(row.flyway) for row in data})
    if len(flyways) < 2:
        raise ValueError("at least two flyways are required")

    baseline = flyways[0]
    dummy_flyways = flyways[1:]
    names = ["intercept"] + [f"flyway[{f}]" for f in dummy_flyways] + [
        "Q",
        "R",
        "QxR",
    ]

    x: list[list[float]] = []
    y: list[float] = []
    weights: list[float] = []

    for row in data:
        q = float(row.q)
        r = float(row.r)
        c = float(row.correction)
        w = float(row.weight)
        if not all(isfinite(v) for v in (q, r, c, w)):
            raise ValueError("all meta-model values must be finite")
        if not -1.0 <= q <= 1.0:
            raise ValueError("Q must lie in [-1, 1]")
        if not 0.0 <= r <= 1.0:
            raise ValueError("R must lie in [0, 1]")
        if w <= 0.0:
            raise ValueError("weights must be positive")
        vector = [1.0]
        vector.extend(1.0 if row.flyway == f else 0.0 for f in dummy_flyways)
        vector.extend([q, r, q * r])
        x.append(vector)
        y.append(c)
        weights.append(w if weighted else 1.0)

    p = len(names)
    if len(data) <= p:
        raise ValueError("model requires more rows than coefficients")

    xtwx = [[0.0 for _ in range(p)] for _ in range(p)]
    xtwy = [0.0 for _ in range(p)]
    for xi, yi, wi in zip(x, y, weights):
        for j in range(p):
            xtwy[j] += wi * xi[j] * yi
            for k in range(p):
                xtwx[j][k] += wi * xi[j] * xi[k]

    beta = _solve(xtwx, xtwy)
    rss = 0.0
    for xi, yi, wi in zip(x, y, weights):
        pred = sum(b * v for b, v in zip(beta, xi))
        rss += wi * (yi - pred) ** 2

    return MetaFit(
        coefficient_names=tuple(names),
        coefficients=tuple(beta),
        beta_qr=beta[-1],
        rss=rss,
        n=len(data),
    )


def exact_within_flyway_q_permutation(
    rows: Iterable[TransitionMetaRow],
) -> ExactPermutationResult:
    data = list(rows)
    observed = fit_meta(data, weighted=False)

    groups: dict[str, list[int]] = {}
    for index, row in enumerate(data):
        groups.setdefault(str(row.flyway), []).append(index)

    flyways = sorted(groups)
    q_permutations = []
    for flyway in flyways:
        indexes = groups[flyway]
        q_values = tuple(data[i].q for i in indexes)
        unique = sorted(set(permutations(q_values)))
        q_permutations.append((indexes, unique))

    betas: list[float] = []
    total = 0
    for combo in product(*(perms for _, perms in q_permutations)):
        total += 1
        q_by_index: dict[int, float] = {}
        for (indexes, _), perm in zip(q_permutations, combo):
            for index, q in zip(indexes, perm):
                q_by_index[index] = q

        permuted = [
            TransitionMetaRow(
                flyway=row.flyway,
                q=q_by_index[i],
                r=row.r,
                correction=row.correction,
                weight=row.weight,
            )
            for i, row in enumerate(data)
        ]
        try:
            betas.append(fit_meta(permuted, weighted=False).beta_qr)
        except ValueError:
            continue

    if not betas:
        raise ValueError("no valid permutation fits")
    count = sum(beta >= observed.beta_qr - _TOL for beta in betas)
    p = (1.0 + count) / (1.0 + len(betas))

    ordered = sorted(betas)
    return ExactPermutationResult(
        observed_beta_qr=observed.beta_qr,
        total_permutations=total,
        valid_permutations=len(betas),
        count_at_least_observed=count,
        one_sided_p=p,
        permutation_min=ordered[0],
        permutation_median=_median(ordered),
        permutation_max=ordered[-1],
    )
