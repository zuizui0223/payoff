"""Accessibility diagnostics for hard-module partitions.

A target contiguous hard partition can be built from one fully shared module by
binary splits. Each split has exact gain G(A,B). For a fixed target partition,
the best all-uphill route maximizes the minimum split gain over all compatible
binary split trees.
"""

from __future__ import annotations

from functools import lru_cache
from math import inf
from typing import Dict, Iterable, List, Sequence, Tuple

from src.hard_module_partition import (
    hard_partition_loss,
    module_summary,
    split_gain,
    weighted_shared_loss,
)

Module = Tuple[int, ...]


def split_tree_accessibility(
    optima: Sequence[float],
    weights: Sequence[float],
    target_partition: Sequence[Iterable[int]],
) -> Dict[str, object]:
    """Return maximin split threshold and one witness tree for target partition.

    The target must consist of contiguous blocks after sorting by scalar optimum.
    If the target has one module, threshold is +infinity because no split is
    required.
    """

    modules = _ordered_contiguous_target(optima, target_partition)
    k = len(modules)

    @lru_cache(None)
    def solve(start: int, end: int):
        if end - start <= 1:
            return inf, None
        best_threshold = -inf
        best_cut = None
        for cut in range(start + 1, end):
            left_union = _union_modules(modules[start:cut])
            right_union = _union_modules(modules[cut:end])
            gain = split_gain(optima, weights, left_union, right_union)
            left_threshold, _ = solve(start, cut)
            right_threshold, _ = solve(cut, end)
            threshold = min(gain, left_threshold, right_threshold)
            if threshold > best_threshold + 1e-15:
                best_threshold = threshold
                best_cut = cut
        return best_threshold, best_cut

    threshold, _ = solve(0, k)

    def build(start: int, end: int):
        if end - start <= 1:
            return {
                "module": modules[start],
                "children": None,
            }
        _, cut = solve(start, end)
        if cut is None:
            raise RuntimeError("failed to construct split tree")
        left_union = _union_modules(modules[start:cut])
        right_union = _union_modules(modules[cut:end])
        gain = split_gain(optima, weights, left_union, right_union)
        return {
            "module": _union_modules(modules[start:end]),
            "split_gain": gain,
            "children": (build(start, cut), build(cut, end)),
        }

    tree = build(0, k) if k > 1 else {"module": modules[0], "children": None}
    return {
        "target_modules": modules,
        "accessibility_threshold": threshold,
        "tree": tree,
    }


def target_is_split_accessible(
    optima: Sequence[float],
    weights: Sequence[float],
    target_partition: Sequence[Iterable[int]],
    extra_module_cost: float,
    tol: float = 1e-12,
) -> bool:
    """Return whether some target-compatible split tree has all gains > cost."""

    if extra_module_cost < 0.0:
        raise ValueError("extra_module_cost must be non-negative")
    threshold = float(
        split_tree_accessibility(optima, weights, target_partition)[
            "accessibility_threshold"
        ]
    )
    return extra_module_cost < threshold - tol


def greedy_hard_split_path(
    optima: Sequence[float],
    weights: Sequence[float],
    extra_module_cost: float,
) -> Tuple[Dict[str, object], ...]:
    """Greedily apply the currently largest positive split margin.

    This is an accessibility heuristic, not a global optimization algorithm.
    Modules are contiguous in sorted-optimum order.
    """

    if extra_module_cost < 0.0:
        raise ValueError("extra_module_cost must be non-negative")
    order = tuple(sorted(range(len(optima)), key=lambda i: (optima[i], i)))
    modules: List[Module] = [order]
    shared_loss = weighted_shared_loss(optima, weights)
    path: List[Dict[str, object]] = []

    while True:
        current_partition = tuple(tuple(sorted(module)) for module in modules)
        within = hard_partition_loss(optima, weights, current_partition)
        recovery = shared_loss - within
        net_gain = recovery - extra_module_cost * (len(modules) - 1)

        best = None
        for module_index, module in enumerate(modules):
            if len(module) <= 1:
                continue
            # module is stored in sorted-optimum order.
            for cut in range(1, len(module)):
                left = module[:cut]
                right = module[cut:]
                gain = split_gain(optima, weights, left, right)
                margin = gain - extra_module_cost
                candidate = (margin, gain, module_index, cut, left, right)
                if best is None or candidate[0] > best[0] + 1e-15:
                    best = candidate

        path.append(
            {
                "step": len(path),
                "modules": current_partition,
                "within_loss": within,
                "recovery": recovery,
                "net_gain": net_gain,
                "next_split_margin": None if best is None else best[0],
                "next_split_gain": None if best is None else best[1],
                "next_split": None
                if best is None
                else (tuple(sorted(best[4])), tuple(sorted(best[5]))),
            }
        )

        if best is None or best[0] <= 1e-12:
            break
        _, _, module_index, _, left, right = best
        modules = modules[:module_index] + [left, right] + modules[module_index + 1 :]

    return tuple(path)


def tree_split_gains(tree: Dict[str, object]) -> Tuple[float, ...]:
    """Return all internal split gains from a witness tree."""

    children = tree.get("children")
    if children is None:
        return ()
    left, right = children
    return (
        float(tree["split_gain"]),
        *tree_split_gains(left),
        *tree_split_gains(right),
    )


def _ordered_contiguous_target(
    optima: Sequence[float], target_partition: Sequence[Iterable[int]]
) -> Tuple[Module, ...]:
    if not optima:
        raise ValueError("optima cannot be empty")
    order = tuple(sorted(range(len(optima)), key=lambda i: (optima[i], i)))
    position = {index: pos for pos, index in enumerate(order)}
    modules = [tuple(sorted(int(i) for i in module)) for module in target_partition]
    if not modules or any(not module for module in modules):
        raise ValueError("target partition must contain non-empty modules")
    flattened = [i for module in modules for i in module]
    if sorted(flattened) != list(range(len(optima))):
        raise ValueError("target partition must cover every function exactly once")

    ordered_modules = sorted(modules, key=lambda module: min(position[i] for i in module))
    expected_position = 0
    for module in ordered_modules:
        positions = sorted(position[i] for i in module)
        if positions != list(range(expected_position, expected_position + len(module))):
            raise ValueError("target modules must be contiguous in sorted-optimum order")
        expected_position += len(module)
    return tuple(tuple(sorted(module)) for module in ordered_modules)


def _union_modules(modules: Sequence[Module]) -> Module:
    return tuple(sorted(i for module in modules for i in module))
