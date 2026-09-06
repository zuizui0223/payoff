"""Hard-module partition theory for scalar function optima.

Each module shares one exact coordinate. For a partition P, optimized loss is
sum of weighted within-module squared deviations. Relative to one fully shared
module, recovery equals the weighted between-module variance.

For scalar optima, an optimal partition can be chosen contiguous after sorting,
so penalized optimization with per-module cost is solved exactly by dynamic
programming.
"""

from __future__ import annotations

from math import inf
from typing import Dict, Iterable, List, Sequence, Tuple

Module = Tuple[int, ...]


def weighted_mean(values: Sequence[float], weights: Sequence[float]) -> float:
    _validate_values_weights(values, weights)
    total = sum(weights)
    return sum(w * x for x, w in zip(values, weights)) / total


def weighted_shared_loss(values: Sequence[float], weights: Sequence[float]) -> float:
    """Return weighted squared loss around the weighted mean."""

    mu = weighted_mean(values, weights)
    return sum(w * (x - mu) ** 2 for x, w in zip(values, weights))


def module_summary(
    optima: Sequence[float],
    weights: Sequence[float],
    module: Iterable[int],
) -> Dict[str, float | Tuple[int, ...]]:
    """Return weight, mean, and within loss of one non-empty module."""

    _validate_values_weights(optima, weights)
    indices = tuple(sorted(int(i) for i in module))
    if not indices:
        raise ValueError("module cannot be empty")
    if len(set(indices)) != len(indices):
        raise ValueError("module indices must be unique")
    if any(i < 0 or i >= len(optima) for i in indices):
        raise ValueError("module index out of range")
    total_weight = sum(weights[i] for i in indices)
    mean = sum(weights[i] * optima[i] for i in indices) / total_weight
    loss = sum(weights[i] * (optima[i] - mean) ** 2 for i in indices)
    return {
        "indices": indices,
        "weight": total_weight,
        "mean": mean,
        "loss": loss,
    }


def hard_partition_loss(
    optima: Sequence[float],
    weights: Sequence[float],
    partition: Sequence[Iterable[int]],
) -> float:
    """Return exact optimized hard-module loss for a valid partition."""

    modules = _normalize_partition(len(optima), partition)
    return sum(float(module_summary(optima, weights, module)["loss"]) for module in modules)


def hard_partition_recovery(
    optima: Sequence[float],
    weights: Sequence[float],
    partition: Sequence[Iterable[int]],
) -> float:
    """Return recovery relative to the fully shared one-module architecture."""

    return weighted_shared_loss(optima, weights) - hard_partition_loss(
        optima, weights, partition
    )


def between_module_recovery(
    optima: Sequence[float],
    weights: Sequence[float],
    partition: Sequence[Iterable[int]],
) -> float:
    """Return sum_M A_M(mu_M-mu)^2, equal to hard_partition_recovery."""

    modules = _normalize_partition(len(optima), partition)
    overall = weighted_mean(optima, weights)
    result = 0.0
    for module in modules:
        summary = module_summary(optima, weights, module)
        result += float(summary["weight"]) * (float(summary["mean"]) - overall) ** 2
    return result


def pairwise_module_recovery(
    optima: Sequence[float],
    weights: Sequence[float],
    partition: Sequence[Iterable[int]],
) -> float:
    """Return pairwise module-mean disagreement representation of recovery."""

    modules = _normalize_partition(len(optima), partition)
    summaries = [module_summary(optima, weights, module) for module in modules]
    total_weight = sum(weights)
    result = 0.0
    for i in range(len(summaries)):
        for j in range(i + 1, len(summaries)):
            wi = float(summaries[i]["weight"])
            wj = float(summaries[j]["weight"])
            mi = float(summaries[i]["mean"])
            mj = float(summaries[j]["mean"])
            result += wi * wj * (mi - mj) ** 2 / total_weight
    return result


def split_gain(
    optima: Sequence[float],
    weights: Sequence[float],
    left: Iterable[int],
    right: Iterable[int],
) -> float:
    """Return exact loss recovered by splitting union(left,right) into two modules."""

    left_indices = tuple(sorted(int(i) for i in left))
    right_indices = tuple(sorted(int(i) for i in right))
    if not left_indices or not right_indices:
        raise ValueError("split groups must both be non-empty")
    if set(left_indices) & set(right_indices):
        raise ValueError("split groups must be disjoint")
    left_summary = module_summary(optima, weights, left_indices)
    right_summary = module_summary(optima, weights, right_indices)
    wl = float(left_summary["weight"])
    wr = float(right_summary["weight"])
    ml = float(left_summary["mean"])
    mr = float(right_summary["mean"])
    return wl * wr / (wl + wr) * (ml - mr) ** 2


def optimal_contiguous_partition_fixed_k(
    optima: Sequence[float],
    weights: Sequence[float],
    module_count: int,
) -> Dict[str, object]:
    """Return one exact optimal scalar hard partition with exactly k modules."""

    order, sorted_optima, sorted_weights = _sorted_problem(optima, weights)
    n = len(order)
    if not 1 <= module_count <= n:
        raise ValueError("module_count must lie in [1,n]")
    prefix_w, prefix_wx, prefix_wx2 = _prefixes(sorted_optima, sorted_weights)

    dp = [[inf] * (n + 1) for _ in range(module_count + 1)]
    prev = [[-1] * (n + 1) for _ in range(module_count + 1)]
    dp[0][0] = 0.0

    for k in range(1, module_count + 1):
        for end in range(k, n + 1):
            best = inf
            best_start = -1
            for start in range(k - 1, end):
                candidate = dp[k - 1][start] + _segment_loss(
                    prefix_w, prefix_wx, prefix_wx2, start, end
                )
                if candidate < best - 1e-15:
                    best = candidate
                    best_start = start
            dp[k][end] = best
            prev[k][end] = best_start

    boundaries: List[Tuple[int, int]] = []
    end = n
    for k in range(module_count, 0, -1):
        start = prev[k][end]
        if start < 0:
            raise RuntimeError("failed to backtrack partition")
        boundaries.append((start, end))
        end = start
    boundaries.reverse()

    modules = tuple(tuple(sorted(order[start:end])) for start, end in boundaries)
    means = tuple(
        float(module_summary(optima, weights, module)["mean"]) for module in modules
    )
    return {
        "module_count": module_count,
        "modules": modules,
        "module_means": means,
        "within_loss": dp[module_count][n],
        "recovery": weighted_shared_loss(optima, weights) - dp[module_count][n],
        "sorted_order": tuple(order),
    }


def optimal_penalized_partition(
    optima: Sequence[float],
    weights: Sequence[float],
    extra_module_cost: float,
) -> Dict[str, object]:
    """Return exact partition maximizing recovery - kappa*(modules-1).

    Uses an O(n^2) dynamic programme over contiguous blocks after sorting.
    """

    if extra_module_cost < 0.0:
        raise ValueError("extra_module_cost must be non-negative")
    order, sorted_optima, sorted_weights = _sorted_problem(optima, weights)
    n = len(order)
    prefix_w, prefix_wx, prefix_wx2 = _prefixes(sorted_optima, sorted_weights)

    dp = [inf] * (n + 1)
    prev = [-1] * (n + 1)
    count = [0] * (n + 1)
    dp[0] = 0.0
    for end in range(1, n + 1):
        best = inf
        best_start = -1
        best_count = 0
        for start in range(end):
            candidate = (
                dp[start]
                + _segment_loss(prefix_w, prefix_wx, prefix_wx2, start, end)
                + extra_module_cost
            )
            candidate_count = count[start] + 1
            if candidate < best - 1e-15 or (
                abs(candidate - best) <= 1e-15 and candidate_count < best_count
            ):
                best = candidate
                best_start = start
                best_count = candidate_count
        dp[end] = best
        prev[end] = best_start
        count[end] = best_count

    boundaries: List[Tuple[int, int]] = []
    end = n
    while end > 0:
        start = prev[end]
        if start < 0:
            raise RuntimeError("failed to backtrack penalized partition")
        boundaries.append((start, end))
        end = start
    boundaries.reverse()
    modules = tuple(tuple(sorted(order[start:end])) for start, end in boundaries)
    within_loss = hard_partition_loss(optima, weights, modules)
    recovery = weighted_shared_loss(optima, weights) - within_loss
    architecture_cost = extra_module_cost * (len(modules) - 1)
    return {
        "module_count": len(modules),
        "modules": modules,
        "module_means": tuple(
            float(module_summary(optima, weights, module)["mean"]) for module in modules
        ),
        "within_loss": within_loss,
        "recovery": recovery,
        "architecture_cost": architecture_cost,
        "net_gain": recovery - architecture_cost,
        "sorted_order": tuple(order),
    }


def fixed_k_loss_curve(
    optima: Sequence[float],
    weights: Sequence[float],
) -> Tuple[Dict[str, object], ...]:
    """Return exact best partition result for every k=1,...,n."""

    _validate_values_weights(optima, weights)
    return tuple(
        optimal_contiguous_partition_fixed_k(optima, weights, k)
        for k in range(1, len(optima) + 1)
    )


def module_count_intervals(
    optima: Sequence[float],
    weights: Sequence[float],
) -> Tuple[Dict[str, object], ...]:
    """Return non-empty kappa intervals where each module count is optimal."""

    curve = fixed_k_loss_curve(optima, weights)
    losses = {int(row["module_count"]): float(row["within_loss"]) for row in curve}
    n = len(curve)
    rows: List[Dict[str, object]] = []
    for k in range(1, n + 1):
        lower = 0.0
        for other in range(k + 1, n + 1):
            lower = max(lower, (losses[k] - losses[other]) / (other - k))
        upper = inf
        for other in range(1, k):
            upper = min(upper, (losses[other] - losses[k]) / (k - other))
        if lower <= upper + 1e-12:
            result = curve[k - 1]
            rows.append(
                {
                    "module_count": k,
                    "lower_cost": max(0.0, lower),
                    "upper_cost": upper,
                    "modules": result["modules"],
                    "within_loss": result["within_loss"],
                    "recovery": result["recovery"],
                }
            )
    return tuple(rows)


def _sorted_problem(
    optima: Sequence[float], weights: Sequence[float]
) -> Tuple[List[int], List[float], List[float]]:
    _validate_values_weights(optima, weights)
    order = sorted(range(len(optima)), key=lambda i: (optima[i], i))
    return order, [float(optima[i]) for i in order], [float(weights[i]) for i in order]


def _prefixes(values: Sequence[float], weights: Sequence[float]):
    prefix_w = [0.0]
    prefix_wx = [0.0]
    prefix_wx2 = [0.0]
    for x, w in zip(values, weights):
        prefix_w.append(prefix_w[-1] + w)
        prefix_wx.append(prefix_wx[-1] + w * x)
        prefix_wx2.append(prefix_wx2[-1] + w * x * x)
    return prefix_w, prefix_wx, prefix_wx2


def _segment_loss(prefix_w, prefix_wx, prefix_wx2, start: int, end: int) -> float:
    weight = prefix_w[end] - prefix_w[start]
    weighted_sum = prefix_wx[end] - prefix_wx[start]
    weighted_sq_sum = prefix_wx2[end] - prefix_wx2[start]
    return weighted_sq_sum - weighted_sum * weighted_sum / weight


def _normalize_partition(n: int, partition: Sequence[Iterable[int]]) -> Tuple[Module, ...]:
    if not partition:
        raise ValueError("partition cannot be empty")
    modules = tuple(tuple(sorted(int(i) for i in module)) for module in partition)
    if any(not module for module in modules):
        raise ValueError("partition modules cannot be empty")
    flattened = [i for module in modules for i in module]
    if sorted(flattened) != list(range(n)):
        raise ValueError("partition must contain every index exactly once")
    return modules


def _validate_values_weights(values: Sequence[float], weights: Sequence[float]) -> None:
    if not values or len(values) != len(weights):
        raise ValueError("values and weights must have same non-zero length")
    if any(float(w) <= 0.0 for w in weights):
        raise ValueError("weights must be positive")
