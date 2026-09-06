#!/usr/bin/env python3
"""Aggregate modular-topology predictions across bootstrap / posterior draws.

Input JSON schema:
{
  "schema_version": "PAYOFF_TOPOLOGY_ENSEMBLE_V1",
  "draws": [
    {
      "draw_id": "...",
      "functions": [
        {"function_id": "F1", "optimum": ..., "weight": ...}, ...
      ],
      "edges": [
        {"source": "F1", "target": "F2", "coupling": ..., "release_cost": ...}, ...
      ]
    }
  ]
}

All draws must preserve the same function ordering and edge ordering so topology
bits have one stable meaning across the ensemble.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.edgewise_modularity import edge_pressures
from src.topology_release_path import connected_components, greedy_positive_pressure_path
from src.topology_robustness import topology_robustness_summary

Edge = Tuple[int, int]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--max-enumeration-edges", type=int, default=12)
    return parser.parse_args()


def bits(released: Sequence[bool]) -> str:
    return "".join("1" if bool(value) else "0" for value in released)


def module_label(components, function_ids: Sequence[str]) -> str:
    return "|".join(
        "{" + ",".join(function_ids[index] for index in component) + "}"
        for component in components
    )


def edge_label(label: Tuple[str, str]) -> str:
    return f"{label[0]}-{label[1]}"


def parse_draw(draw: Dict[str, object]):
    draw_id = str(draw.get("draw_id", "")).strip()
    if not draw_id:
        raise ValueError("every draw requires non-empty draw_id")

    functions = draw.get("functions")
    edges_raw = draw.get("edges")
    if not isinstance(functions, list) or not functions:
        raise ValueError(f"draw {draw_id}: functions must be a non-empty list")
    if not isinstance(edges_raw, list) or not edges_raw:
        raise ValueError(f"draw {draw_id}: edges must be a non-empty list")

    ids: List[str] = []
    optima: List[float] = []
    weights: List[float] = []
    for row in functions:
        if not isinstance(row, dict):
            raise ValueError(f"draw {draw_id}: function entries must be objects")
        fid = str(row.get("function_id", "")).strip()
        if not fid or fid in ids:
            raise ValueError(f"draw {draw_id}: function ids must be non-empty and unique")
        optimum = float(row["optimum"])
        weight = float(row["weight"])
        if weight <= 0.0:
            raise ValueError(f"draw {draw_id}: function weight must be positive")
        ids.append(fid)
        optima.append(optimum)
        weights.append(weight)

    index = {fid: i for i, fid in enumerate(ids)}
    edges: List[Edge] = []
    labels: List[Tuple[str, str]] = []
    couplings: List[float] = []
    costs: List[float] = []
    seen = set()
    for row in edges_raw:
        if not isinstance(row, dict):
            raise ValueError(f"draw {draw_id}: edge entries must be objects")
        source = str(row.get("source", "")).strip()
        target = str(row.get("target", "")).strip()
        if source not in index or target not in index or source == target:
            raise ValueError(f"draw {draw_id}: invalid edge {source}-{target}")
        canonical = tuple(sorted((source, target)))
        if canonical in seen:
            raise ValueError(f"draw {draw_id}: duplicate edge {canonical}")
        seen.add(canonical)
        coupling = float(row["coupling"])
        cost = float(row["release_cost"])
        if coupling < 0.0 or cost < 0.0:
            raise ValueError(f"draw {draw_id}: coupling and release cost must be non-negative")
        edges.append((index[source], index[target]))
        labels.append((source, target))
        couplings.append(coupling)
        costs.append(cost)

    return draw_id, ids, optima, weights, edges, labels, couplings, costs


def support(counter: Counter, total: int) -> Dict[str, float]:
    return {
        key: count / total
        for key, count in sorted(counter.items(), key=lambda item: (-item[1], item[0]))
    }


def main() -> None:
    args = parse_args()
    if args.max_enumeration_edges < 0:
        raise ValueError("max-enumeration-edges must be non-negative")

    payload = json.loads(args.input.read_text(encoding="utf-8"))
    if payload.get("schema_version") != "PAYOFF_TOPOLOGY_ENSEMBLE_V1":
        raise ValueError("unsupported or missing schema_version")
    draws = payload.get("draws")
    if not isinstance(draws, list) or not draws:
        raise ValueError("draws must be a non-empty list")

    receipts = []
    expected_ids = None
    expected_labels = None

    for raw_draw in draws:
        if not isinstance(raw_draw, dict):
            raise ValueError("draw entries must be objects")
        (
            draw_id,
            ids,
            optima,
            weights,
            edges,
            labels,
            couplings,
            costs,
        ) = parse_draw(raw_draw)

        if expected_ids is None:
            expected_ids = tuple(ids)
            expected_labels = tuple(labels)
        elif tuple(ids) != expected_ids or tuple(labels) != expected_labels:
            raise ValueError(
                "all draws must preserve identical function and edge ordering"
            )
        if len(edges) > args.max_enumeration_edges:
            raise ValueError(
                f"draw {draw_id}: {len(edges)} edges exceed enumeration limit "
                f"{args.max_enumeration_edges}"
            )

        pressures = edge_pressures(optima, weights, edges, couplings)
        pressure_index = max(range(len(edges)), key=lambda index: pressures[index])
        path = greedy_positive_pressure_path(
            optima, weights, edges, couplings, costs
        )
        first_favorable_index = path[0]["next_edge_index"]
        final_state = path[-1]

        robustness = topology_robustness_summary(
            optima, weights, edges, couplings, costs
        )
        best_released = tuple(bool(value) for value in robustness["best_released"])
        best_bits = bits(best_released)
        final_bits = bits(final_state["released"])
        best_current = [
            0.0 if flag else float(reference)
            for flag, reference in zip(best_released, couplings)
        ]
        best_components = connected_components(len(ids), edges, best_current)

        receipts.append(
            {
                "draw_id": draw_id,
                "first_pressure_edge": edge_label(labels[pressure_index]),
                "first_favorable_edge": (
                    "stop"
                    if first_favorable_index is None
                    else edge_label(labels[first_favorable_index])
                ),
                "best_topology_bits": best_bits,
                "best_modules": module_label(best_components, ids),
                "best_net_gain": float(robustness["best_net_gain"]),
                "global_reserve": float(robustness["global_reserve"]),
                "local_reserve": float(robustness["local_reserve"]),
                "greedy_final_bits": final_bits,
                "greedy_final_modules": module_label(final_state["components"], ids),
                "greedy_matches_global": int(final_bits == best_bits),
                "greedy_steps": len(path) - 1,
            }
        )

    total = len(receipts)
    best_counter = Counter(row["best_topology_bits"] for row in receipts)
    pressure_counter = Counter(row["first_pressure_edge"] for row in receipts)
    favorable_counter = Counter(row["first_favorable_edge"] for row in receipts)
    greedy_counter = Counter(row["greedy_final_bits"] for row in receipts)

    consensus_bits, consensus_count = best_counter.most_common(1)[0]
    summary = {
        "draw_count": total,
        "best_topology_support": support(best_counter, total),
        "first_pressure_edge_support": support(pressure_counter, total),
        "first_favorable_edge_support": support(favorable_counter, total),
        "greedy_final_topology_support": support(greedy_counter, total),
        "greedy_matches_global_fraction": sum(
            row["greedy_matches_global"] for row in receipts
        )
        / total,
        "consensus_best_topology": consensus_bits,
        "consensus_best_topology_fraction": consensus_count / total,
        "mean_global_reserve": sum(row["global_reserve"] for row in receipts) / total,
        "minimum_global_reserve": min(row["global_reserve"] for row in receipts),
        "mean_local_reserve": sum(row["local_reserve"] for row in receipts) / total,
    }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    with (args.output_dir / "draw_receipts.csv").open(
        "w", newline="", encoding="utf-8"
    ) as handle:
        writer = csv.DictWriter(handle, fieldnames=list(receipts[0]))
        writer.writeheader()
        writer.writerows(receipts)
    with (args.output_dir / "ensemble_summary.json").open(
        "w", encoding="utf-8"
    ) as handle:
        json.dump(summary, handle, indent=2, ensure_ascii=False)

    print(args.output_dir)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
