#!/usr/bin/env python3
"""Predict modular topology from function optima, coupling graph, and edge costs.

Input files
-----------
functions.csv
    function_id,optimum,weight

edges.csv
    source,target,coupling,release_cost

The script writes a reference edge-pressure table, a local accessibility path,
and (for sufficiently small edge sets) all binary retain/release vertex
topologies. It is intended as the concrete SCH/BITA/BALANCE -> PAYOFF handoff.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.edgewise_modularity import (
    edge_pressures,
    enumerate_vertex_topologies,
    optimized_loss,
    optimized_phenotype,
)
from src.topology_release_path import connected_components, greedy_positive_pressure_path

Edge = Tuple[int, int]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--functions", type=Path, required=True)
    parser.add_argument("--edges", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument(
        "--max-enumeration-edges",
        type=int,
        default=12,
        help="enumerate all 2^m vertex topologies only when m is at most this value",
    )
    return parser.parse_args()


def load_functions(path: Path):
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"function_id", "optimum", "weight"}
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            raise ValueError(f"{path} must contain columns {sorted(required)}")
        ids: List[str] = []
        optima: List[float] = []
        weights: List[float] = []
        for line, row in enumerate(reader, start=2):
            function_id = row["function_id"].strip()
            if not function_id:
                raise ValueError(f"empty function_id at {path}:{line}")
            if function_id in ids:
                raise ValueError(f"duplicate function_id {function_id!r}")
            optimum = float(row["optimum"])
            weight = float(row["weight"])
            if weight <= 0.0:
                raise ValueError(f"weight must be positive for {function_id}")
            ids.append(function_id)
            optima.append(optimum)
            weights.append(weight)
    if not ids:
        raise ValueError("functions file cannot be empty")
    return ids, optima, weights


def load_edges(path: Path, function_ids: Sequence[str]):
    index = {name: i for i, name in enumerate(function_ids)}
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"source", "target", "coupling", "release_cost"}
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            raise ValueError(f"{path} must contain columns {sorted(required)}")
        edges: List[Edge] = []
        labels: List[Tuple[str, str]] = []
        couplings: List[float] = []
        costs: List[float] = []
        seen = set()
        for line, row in enumerate(reader, start=2):
            source = row["source"].strip()
            target = row["target"].strip()
            if source not in index or target not in index:
                raise ValueError(f"unknown function id at {path}:{line}: {source},{target}")
            if source == target:
                raise ValueError(f"self edge is not allowed at {path}:{line}")
            key = tuple(sorted((source, target)))
            if key in seen:
                raise ValueError(f"duplicate undirected edge {key}")
            seen.add(key)
            coupling = float(row["coupling"])
            release_cost = float(row["release_cost"])
            if coupling < 0.0:
                raise ValueError(f"coupling must be non-negative at {path}:{line}")
            if release_cost < 0.0:
                raise ValueError(f"release_cost must be non-negative at {path}:{line}")
            edges.append((index[source], index[target]))
            labels.append((source, target))
            couplings.append(coupling)
            costs.append(release_cost)
    if not edges:
        raise ValueError("edges file cannot be empty")
    return edges, labels, couplings, costs


def fmt_tuple(values: Sequence[float]) -> str:
    return ";".join(f"{float(value):.12g}" for value in values)


def topology_bits(released: Sequence[bool]) -> str:
    return "".join("1" if value else "0" for value in released)


def released_labels(released: Sequence[bool], labels: Sequence[Tuple[str, str]]) -> str:
    chosen = [f"{source}-{target}" for flag, (source, target) in zip(released, labels) if flag]
    return ";".join(chosen) if chosen else "none"


def module_label(components, function_ids: Sequence[str]) -> str:
    return "|".join(
        "{" + ",".join(function_ids[index] for index in component) + "}"
        for component in components
    )


def write_edge_pressures(
    output: Path,
    ids: Sequence[str],
    optima: Sequence[float],
    weights: Sequence[float],
    edges: Sequence[Edge],
    labels: Sequence[Tuple[str, str]],
    couplings: Sequence[float],
    costs: Sequence[float],
):
    pressures = edge_pressures(optima, weights, edges, couplings)
    rows = []
    for index, ((source, target), coupling, cost, pressure) in enumerate(
        zip(labels, couplings, costs, pressures)
    ):
        margin = pressure - cost
        rows.append(
            {
                "edge_index": index,
                "source": source,
                "target": target,
                "reference_coupling": coupling,
                "release_cost_per_unit": cost,
                "pressure": pressure,
                "margin": margin,
                "direction": (
                    "favor_more_decoupling"
                    if margin > 1e-12
                    else "favor_more_coupling"
                    if margin < -1e-12
                    else "marginal_balance"
                ),
            }
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return rows


def write_path(
    output: Path,
    ids: Sequence[str],
    optima: Sequence[float],
    weights: Sequence[float],
    edges: Sequence[Edge],
    labels: Sequence[Tuple[str, str]],
    couplings: Sequence[float],
    costs: Sequence[float],
):
    path = greedy_positive_pressure_path(optima, weights, edges, couplings, costs)
    rows = []
    for state in path:
        next_edge = state["next_edge_index"]
        rows.append(
            {
                "step": state["step"],
                "released_bits": topology_bits(state["released"]),
                "released_edges": released_labels(state["released"], labels),
                "modules": module_label(state["components"], ids),
                "phenotype": fmt_tuple(state["phenotype"]),
                "optimized_loss": state["optimized_loss"],
                "recovery": state["recovery"],
                "net_gain": state["net_gain"],
                "pressures": fmt_tuple(state["pressures"]),
                "next_edge": (
                    "stop"
                    if next_edge is None
                    else f"{labels[next_edge][0]}-{labels[next_edge][1]}"
                ),
            }
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return path, rows


def write_topologies(
    output: Path,
    ids: Sequence[str],
    optima: Sequence[float],
    weights: Sequence[float],
    edges: Sequence[Edge],
    labels: Sequence[Tuple[str, str]],
    couplings: Sequence[float],
    costs: Sequence[float],
):
    topologies = enumerate_vertex_topologies(optima, weights, edges, couplings, costs)
    rows = []
    reference_loss = optimized_loss(optima, weights, edges, couplings)
    for topology in topologies:
        current = tuple(float(value) for value in topology["couplings"])
        phenotype = optimized_phenotype(optima, weights, edges, current)
        components = connected_components(len(ids), edges, current)
        rows.append(
            {
                "released_bits": topology_bits(topology["released"]),
                "released_edges": released_labels(topology["released"], labels),
                "modules": module_label(components, ids),
                "phenotype": fmt_tuple(phenotype),
                "optimized_loss": reference_loss - float(topology["recovery"]),
                "recovery": topology["recovery"],
                "architecture_cost": topology["architecture_cost"],
                "net_gain": topology["net_gain"],
            }
        )
    rows.sort(key=lambda row: float(row["net_gain"]), reverse=True)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return rows


def main() -> None:
    args = parse_args()
    if args.max_enumeration_edges < 0:
        raise ValueError("max-enumeration-edges must be non-negative")

    ids, optima, weights = load_functions(args.functions)
    edges, labels, couplings, costs = load_edges(args.edges, ids)
    args.output_dir.mkdir(parents=True, exist_ok=True)

    reference_phenotype = optimized_phenotype(optima, weights, edges, couplings)
    reference_loss = optimized_loss(optima, weights, edges, couplings)
    pressure_rows = write_edge_pressures(
        args.output_dir / "edge_pressures.csv",
        ids,
        optima,
        weights,
        edges,
        labels,
        couplings,
        costs,
    )
    path, path_rows = write_path(
        args.output_dir / "greedy_release_path.csv",
        ids,
        optima,
        weights,
        edges,
        labels,
        couplings,
        costs,
    )

    topology_rows = None
    if len(edges) <= args.max_enumeration_edges:
        topology_rows = write_topologies(
            args.output_dir / "vertex_topologies.csv",
            ids,
            optima,
            weights,
            edges,
            labels,
            couplings,
            costs,
        )

    summary: Dict[str, object] = {
        "function_count": len(ids),
        "edge_count": len(edges),
        "function_ids": ids,
        "reference_phenotype": reference_phenotype,
        "reference_loss": reference_loss,
        "highest_reference_pressure_edge": max(
            pressure_rows, key=lambda row: float(row["pressure"])
        )["source"]
        + "-"
        + max(pressure_rows, key=lambda row: float(row["pressure"]))["target"],
        "greedy_final_modules": path_rows[-1]["modules"],
        "greedy_final_net_gain": path_rows[-1]["net_gain"],
        "greedy_steps": len(path) - 1,
        "vertex_enumerated": topology_rows is not None,
    }
    if topology_rows is not None:
        summary.update(
            {
                "vertex_count": len(topology_rows),
                "best_vertex_bits": topology_rows[0]["released_bits"],
                "best_vertex_modules": topology_rows[0]["modules"],
                "best_vertex_net_gain": topology_rows[0]["net_gain"],
                "greedy_matches_global_vertex": (
                    topology_rows[0]["released_bits"] == path_rows[-1]["released_bits"]
                ),
            }
        )

    with (args.output_dir / "summary.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, ensure_ascii=False)

    print(args.output_dir)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
