#!/usr/bin/env python3
"""Reproduce the three-function edge-release topology example."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.edgewise_modularity import (
    enumerate_vertex_topologies,
    optimized_loss,
    optimized_phenotype,
)
from src.topology_release_path import connected_components, greedy_positive_pressure_path


OPTIMA = (0.0, 1.0, 3.0)
WEIGHTS = (1.0, 1.0, 1.0)
EDGES = ((0, 1), (0, 2), (1, 2))
COUPLINGS = (1.0, 1.0, 1.0)


def _fmt_tuple(values) -> str:
    return ";".join(f"{float(value):.12g}" for value in values)


def _released_label(bits) -> str:
    names = ["01", "02", "12"]
    chosen = [name for name, released in zip(names, bits) if released]
    return "+".join(chosen) if chosen else "none"


def _module_label(components) -> str:
    return "|".join("{" + ",".join(str(node) for node in component) + "}" for component in components)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--edge-cost", type=float, default=0.4)
    parser.add_argument(
        "--topologies-output",
        type=Path,
        default=Path("outputs/three_function_topologies.csv"),
    )
    parser.add_argument(
        "--path-output",
        type=Path,
        default=Path("outputs/three_function_release_path.csv"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.edge_cost < 0.0:
        raise ValueError("edge cost must be non-negative")
    costs = (args.edge_cost,) * len(EDGES)

    topologies = enumerate_vertex_topologies(
        OPTIMA, WEIGHTS, EDGES, COUPLINGS, costs
    )
    reference_loss = optimized_loss(OPTIMA, WEIGHTS, EDGES, COUPLINGS)

    topology_rows = []
    for row in topologies:
        couplings = tuple(float(value) for value in row["couplings"])
        phenotype = optimized_phenotype(OPTIMA, WEIGHTS, EDGES, couplings)
        topology_rows.append(
            {
                "released_edges": _released_label(row["released"]),
                "released_bits": "".join("1" if value else "0" for value in row["released"]),
                "modules": _module_label(connected_components(3, EDGES, couplings)),
                "couplings": _fmt_tuple(couplings),
                "phenotype": _fmt_tuple(phenotype),
                "optimized_loss": f"{reference_loss-float(row['recovery']):.12g}",
                "recovery": f"{float(row['recovery']):.12g}",
                "architecture_cost": f"{float(row['architecture_cost']):.12g}",
                "net_gain": f"{float(row['net_gain']):.12g}",
            }
        )

    topology_rows.sort(key=lambda row: float(row["net_gain"]), reverse=True)
    args.topologies_output.parent.mkdir(parents=True, exist_ok=True)
    with args.topologies_output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(topology_rows[0]))
        writer.writeheader()
        writer.writerows(topology_rows)

    path = greedy_positive_pressure_path(
        OPTIMA, WEIGHTS, EDGES, COUPLINGS, costs
    )
    path_rows = []
    for state in path:
        next_edge = state["next_edge_index"]
        path_rows.append(
            {
                "step": state["step"],
                "released_edges": _released_label(state["released"]),
                "modules": _module_label(state["components"]),
                "phenotype": _fmt_tuple(state["phenotype"]),
                "pressures": _fmt_tuple(state["pressures"]),
                "margins": _fmt_tuple(
                    value if value != float("-inf") else -999999.0
                    for value in state["margins"]
                ),
                "recovery": f"{float(state['recovery']):.12g}",
                "net_gain": f"{float(state['net_gain']):.12g}",
                "next_edge": "stop" if next_edge is None else ("01", "02", "12")[next_edge],
            }
        )

    args.path_output.parent.mkdir(parents=True, exist_ok=True)
    with args.path_output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(path_rows[0]))
        writer.writeheader()
        writer.writerows(path_rows)

    best = topology_rows[0]
    print(args.topologies_output)
    print(args.path_output)
    print(
        "best topology: "
        f"released={best['released_edges']} modules={best['modules']} net_gain={best['net_gain']}"
    )
    print("accessible path: " + " -> ".join(row["next_edge"] for row in path_rows))


if __name__ == "__main__":
    main()
