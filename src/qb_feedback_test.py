"""Exact row-level q_B x recourse feedback test for PAYOFF-B.

Primary model:
    stopover_days
      = transition fixed effects
      + E
      + E*R
      + E*Q_B
      + E*Q_B*R
      + error

Q_B is permuted at unique origin-region level within flyway. All transitions
sharing an origin receive the same permuted Q_B value.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations, product
from math import isfinite
from typing import Iterable


_TOL = 1e-12


@dataclass(frozen=True)
class FeedbackBehaviorRow:
    flyway: str
    transition_id: str
    origin_region: str
    incoming_phase_error: float
    stopover_days: float
    retained_recourse: float


@dataclass(frozen=True)
class FeedbackFit:
    coefficient_names: tuple[str, ...]
    coefficients: tuple[float, ...]
    beta_e_qb_r: float
    rss: float
    n: int


@dataclass(frozen=True)
class FeedbackPermutationResult:
    observed_beta_e_qb_r: float
    total_permutations: int
    valid_permutations: int
    count_at_most_observed: int
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


def _median(values: list[float]) -> float:
    xs = sorted(values)
    n = len(xs)
    return xs[n // 2] if n % 2 else 0.5 * (xs[n // 2 - 1] + xs[n // 2])


def fit_feedback_model(
    behavior_rows: Iterable[FeedbackBehaviorRow],
    q_b_by_origin: dict[tuple[str, str], float],
) -> FeedbackFit:
    rows = list(behavior_rows)
    if len(rows) < 10:
        raise ValueError("at least ten behavior rows are required")

    transitions = sorted({row.transition_id for row in rows})
    if len(transitions) < 2:
        raise ValueError("at least two transitions are required")
    baseline = transitions[0]
    dummies = transitions[1:]

    names = (
        ["intercept"]
        + [f"transition[{name}]" for name in dummies]
        + ["E", "ExR", "ExQB", "ExQBxR"]
    )
    x = []
    y = []
    for row in rows:
        e = float(row.incoming_phase_error)
        r = float(row.retained_recourse)
        stop = float(row.stopover_days)
        key = (str(row.flyway), str(row.origin_region))
        if key not in q_b_by_origin:
            raise ValueError(f"missing q_B for origin {key}")
        qb = float(q_b_by_origin[key])
        if not all(isfinite(v) for v in (e, r, stop, qb)):
            raise ValueError("all feedback-model values must be finite")
        if not 0.0 <= r <= 1.0:
            raise ValueError("retained recourse must lie in [0,1]")

        vector = [1.0]
        vector.extend(
            1.0 if row.transition_id == name else 0.0
            for name in dummies
        )
        vector.extend([e, e * r, e * qb, e * qb * r])
        x.append(vector)
        y.append(stop)

    p = len(names)
    if len(rows) <= p:
        raise ValueError("model requires more rows than coefficients")

    xtx = [[0.0 for _ in range(p)] for _ in range(p)]
    xty = [0.0 for _ in range(p)]
    for xi, yi in zip(x, y):
        for j in range(p):
            xty[j] += xi[j] * yi
            for k in range(p):
                xtx[j][k] += xi[j] * xi[k]

    beta = _solve(xtx, xty)
    rss = 0.0
    for xi, yi in zip(x, y):
        pred = sum(b * v for b, v in zip(beta, xi))
        rss += (yi - pred) ** 2

    return FeedbackFit(
        coefficient_names=tuple(names),
        coefficients=tuple(beta),
        beta_e_qb_r=beta[-1],
        rss=rss,
        n=len(rows),
    )


def exact_origin_region_qb_permutation(
    behavior_rows: Iterable[FeedbackBehaviorRow],
    q_b_by_origin: dict[tuple[str, str], float],
) -> FeedbackPermutationResult:
    rows = list(behavior_rows)
    observed = fit_feedback_model(rows, q_b_by_origin)

    origins_by_flyway: dict[str, list[str]] = {}
    for row in rows:
        origins_by_flyway.setdefault(str(row.flyway), [])
        origin = str(row.origin_region)
        if origin not in origins_by_flyway[str(row.flyway)]:
            origins_by_flyway[str(row.flyway)].append(origin)

    flyways = sorted(origins_by_flyway)
    permutation_sets = []
    for flyway in flyways:
        origins = sorted(origins_by_flyway[flyway])
        values = tuple(q_b_by_origin[(flyway, origin)] for origin in origins)
        unique = sorted(set(permutations(values)))
        permutation_sets.append((flyway, origins, unique))

    beta_perm: list[float] = []
    total = 0
    for combo in product(*(entry[2] for entry in permutation_sets)):
        total += 1
        mapping = dict(q_b_by_origin)
        for (flyway, origins, _), perm in zip(permutation_sets, combo):
            for origin, qb in zip(origins, perm):
                mapping[(flyway, origin)] = qb
        try:
            beta_perm.append(
                fit_feedback_model(rows, mapping).beta_e_qb_r
            )
        except ValueError:
            continue

    if not beta_perm:
        raise ValueError("no valid q_B permutations")
    count = sum(
        beta <= observed.beta_e_qb_r + _TOL
        for beta in beta_perm
    )
    ordered = sorted(beta_perm)
    return FeedbackPermutationResult(
        observed_beta_e_qb_r=observed.beta_e_qb_r,
        total_permutations=total,
        valid_permutations=len(beta_perm),
        count_at_most_observed=count,
        one_sided_p=(1.0 + count) / (1.0 + len(beta_perm)),
        permutation_min=ordered[0],
        permutation_median=_median(ordered),
        permutation_max=ordered[-1],
    )
