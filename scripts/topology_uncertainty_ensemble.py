#!/usr/bin/env python3
"""Aggregate modular-topology predictions across bootstrap / posterior draws.

Input JSON schema:
{
  "schema_version": "PAYOFF_TOPOLOGY_ENSEMBLE_V1",
  "context": { ... optional context/fitness-scale identity ... },
  "population": {
    "gamma": -0.25,
    "population_size": 20,
    "beta": 0.4
  },
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

If a population block is supplied, each draw's best and runner-up intrinsic
architectures are also transported into the canonical pairwise PAYOFF game.
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
from src.topology_game import (
    classify_pairwise_topology_game,
    pairwise_payoff_parameters,
    reciprocal_fixation_probabilities,
    reciprocal_invasion_margins,
    topology_distance,
)
from src.topology_release_path import connected_components, greedy_positive_pressure_path
from src.topology_robustness import topology_robustness_summary

Edge = Tuple[int, int]
CONTEXT_FIELDS = (
    "context_id",
    "system",
    "population_id",
    "season_id",
    "fitness_scale_id",
)


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


def parse_context(payload: Dict[str, object]) -> Dict[str, str] | None:
    raw = payload.get("context")
    if raw is None:
        return None
    if not isinstance(raw, dict):
        raise ValueError("context must be an object when supplied")
    context: Dict[str, str] = {}
    for field in CONTEXT_FIELDS:
        value = str(raw.get(field, "")).strip()
        if not value:
            raise ValueError(f"context.{field} must be non-empty")
        context[field] = value
    return context


def parse_population(payload: Dict[str, object]):
    raw = payload.get("population")
    if raw is None:
        return None
    if not isinstance(raw, dict):
        raise ValueError("population must be an object when supplied")
    gamma = float(raw["gamma"])
    n = int(raw["population_size"])
    beta = float(raw["beta"])
    if n < 2:
        raise ValueError("population.population_size must be at least 2")
    if beta < 0.0:
        raise ValueError("population.beta must be non-negative")
    return {"gamma": gamma, "population_size": n, "beta": beta}


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
    context = parse_context(payload)
    population = parse_population(payload)
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
        second_released = tuple(bool(value) for value in robustness["second_released"])
        best_bits = bits(best_released)
        second_bits = bits(second_released)
        final_bits = bits(final_state["released"])
        best_current = [
            0.0 if flag else float(reference)
            for flag, reference in zip(best_released, couplings)
        ]
        best_components = connected_components(len(ids), edges, best_current)

        receipt: Dict[str, object] = {
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
            "runner_up_topology_bits": second_bits,
            "runner_up_net_gain": float(robustness["second_net_gain"]),
            "global_reserve": float(robustness["global_reserve"]),
            "local_reserve": float(robustness["local_reserve"]),
            "greedy_final_bits": final_bits,
            "greedy_final_modules": module_label(final_state["components"], ids),
            "greedy_matches_global": int(final_bits == best_bits),
            "greedy_steps": len(path) - 1,
        }

        if population is not None:
            gamma = float(population["gamma"])
            n = int(population["population_size"])
            beta = float(population["beta"])
            best_payoff = float(robustness["best_net_gain"])
            second_payoff = float(robustness["second_net_gain"])
            q = topology_distance(best_released, second_released)
            phi, eta = pairwise_payoff_parameters(
                best_payoff,
                second_payoff,
                best_released,
                second_released,
                gamma,
            )
            runner_into_best, best_into_runner = reciprocal_invasion_margins(
                best_payoff,
                second_payoff,
                best_released,
                second_released,
                gamma,
            )
            rho_runner, rho_best = reciprocal_fixation_probabilities(
                n,
                beta,
                best_payoff,
                second_payoff,
                best_released,
                second_released,
                gamma,
            )
            receipt.update(
                {
                    "top_pair_unordered": "-".join(sorted((best_bits, second_bits))),
                    "top_pair_distance": q,
                    "runner_vs_best_phi": phi,
                    "runner_vs_best_eta": eta,
                    "top_pair_class": classify_pairwise_topology_game(
                        best_payoff,
                        second_payoff,
                        best_released,
                        second_released,
                        gamma,
                    ),
                    "runner_into_best_margin": runner_into_best,
                    "best_into_runner_margin": best_into_runner,
                    "both_top_pair_invade": int(
                        runner_into_best > 0.0 and best_into_runner > 0.0
                    ),
                    "rho_runner_into_best": rho_runner,
                    "rho_best_into_runner": rho_best,
                    "best_has_larger_reciprocal_fixation": int(rho_best > rho_runner),
                    "runner_over_best_fixation_ratio": (
                        rho_runner / rho_best if rho_best > 0.0 else float("inf")
                    ),
                }
            )

        receipts.append(receipt)

    total = len(receipts)
    best_counter = Counter(row["best_topology_bits"] for row in receipts)
    pressure_counter = Counter(row["first_pressure_edge"] for row in receipts)
    favorable_counter = Counter(row["first_favorable_edge"] for row in receipts)
    greedy_counter = Counter(row["greedy_final_bits"] for row in receipts)

    consensus_bits, consensus_count = best_counter.most_common(1)[0]
    summary: Dict[str, object] = {
        "draw_count": total,
        "context": context,
        "population": population,
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
        "mean_global_reserve": sum(float(row["global_reserve"]) for row in receipts) / total,
        "minimum_global_reserve": min(float(row["global_reserve"]) for row in receipts),
        "mean_local_reserve": sum(float(row["local_reserve"]) for row in receipts) / total,
    }

    if population is not None:
        pair_counter = Counter(str(row["top_pair_unordered"]) for row in receipts)
        phase_counter = Counter(str(row["top_pair_class"]) for row in receipts)
        summary.update(
            {
                "top_pair_unordered_support": support(pair_counter, total),
                "top_pair_phase_support": support(phase_counter, total),
                "both_top_pair_invade_fraction": sum(
                    int(row["both_top_pair_invade"]) for row in receipts
                )
                / total,
                "best_has_larger_reciprocal_fixation_fraction": sum(
                    int(row["best_has_larger_reciprocal_fixation"])
                    for row in receipts
                )
                / total,
                "mean_runner_over_best_fixation_ratio": sum(
                    float(row["runner_over_best_fixation_ratio"])
                    for row in receipts
                )
                / total,
            }
        )

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
