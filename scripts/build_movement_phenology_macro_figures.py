#!/usr/bin/env python3
"""Build publication-oriented movement–phenology synthesis figures.

Figure 4 has two panels:
A. one descriptive phase-retention record per taxon; repeated barnacle-goose
   routes appear as an observed within-taxon range, not independent studies;
B. independently reconstructed environmental innovation versus phase retention
   for stable barnacle-goose transitions.

The figure is descriptive. Whiskers in panel A are within-taxon route ranges,
not confidence intervals. Panel B transition points are not independent studies.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DIRECT = ROOT / "data/MOVEMENT_PHENOLOGY_DIRECT_CONTROLLER_REGISTRY.csv"
UNCERTAINTY = ROOT / "data/MOVEMENT_PHENOLOGY_PHASE_UNCERTAINTY_REGISTRY.csv"
OUT = ROOT / "outputs/movement_phenology/figures"
OUT.mkdir(parents=True, exist_ok=True)


TAXON_LABELS = {
    "Odocoileus hemionus": "Mule deer",
    "Branta leucopsis": "Barnacle goose",
    "Mareca penelope": "Eurasian wigeon",
}


def taxon_summary() -> pd.DataFrame:
    d = pd.read_csv(DIRECT)
    d = d[d["status"].astype(str).str.startswith("DIRECT_")].copy()
    d["phase_retention_abs"] = pd.to_numeric(
        d["phase_retention_abs"], errors="coerce"
    )
    d = d[np.isfinite(d["phase_retention_abs"])].copy()

    rows = []
    for taxon, x in d.groupby("taxon"):
        vals = x["phase_retention_abs"].to_numpy(float)
        rows.append(
            {
                "taxon": taxon,
                "label": TAXON_LABELS.get(taxon, taxon),
                "median_abs_lambda": float(np.median(vals)),
                "min_abs_lambda": float(np.min(vals)),
                "max_abs_lambda": float(np.max(vals)),
                "n_direct_rows": int(len(x)),
            }
        )
    order = ["Odocoileus hemionus", "Branta leucopsis", "Mareca penelope"]
    out = pd.DataFrame(rows)
    out["order"] = out["taxon"].map({x: i for i, x in enumerate(order)})
    return out.sort_values("order").reset_index(drop=True)


def build_figure4() -> Path:
    taxa = taxon_summary()
    env = pd.read_csv(UNCERTAINTY)
    env = env[
        env["stable_phase_map"].astype(str).str.lower().eq("true")
    ].copy()
    env["environmental_innovation_sd_days"] = pd.to_numeric(
        env["environmental_innovation_sd_days"], errors="coerce"
    )
    env["abs_lambda"] = pd.to_numeric(env["abs_lambda"], errors="coerce")
    env = env.dropna(
        subset=["environmental_innovation_sd_days", "abs_lambda"]
    )

    fig, axes = plt.subplots(
        1,
        2,
        figsize=(11.4, 4.9),
        gridspec_kw={"width_ratios": [0.9, 1.1]},
        constrained_layout=True,
    )

    # Panel A — taxon-level retention.
    ax = axes[0]
    y = np.arange(len(taxa))
    for i, row in taxa.iterrows():
        lo = row["median_abs_lambda"] - row["min_abs_lambda"]
        hi = row["max_abs_lambda"] - row["median_abs_lambda"]
        ax.errorbar(
            row["median_abs_lambda"],
            i,
            xerr=np.array([[lo], [hi]]),
            fmt="o",
            capsize=5,
            linewidth=1.6,
            markersize=7,
        )
        ax.text(
            row["median_abs_lambda"] + 0.025,
            i + 0.14,
            f'{row["median_abs_lambda"]:.2f}',
            fontsize=9,
        )

    ax.axvline(1.0, linestyle="--", linewidth=1.2)
    ax.set_xlim(-0.02, 1.06)
    ax.set_yticks(y, taxa["label"])
    ax.invert_yaxis()
    ax.set_xlabel(r"Phase retention $R_\phi=|\lambda|$")
    ax.set_title("A  Phase retention spans a broad range")
    ax.text(
        1.0,
        len(taxa) - 0.2,
        "no correction",
        rotation=90,
        va="bottom",
        ha="right",
        fontsize=8,
    )
    ax.text(
        0.01,
        -0.52,
        "Barnacle-goose whisker = observed route range, not a CI",
        transform=ax.transAxes,
        fontsize=8,
        va="top",
    )

    # Panel B — two-channel plane.
    ax = axes[1]
    markers = {"Greenland": "s", "Barents": "o"}
    for flyway, d in env.groupby("flyway"):
        ax.scatter(
            d["environmental_innovation_sd_days"],
            d["abs_lambda"],
            marker=markers.get(flyway, "o"),
            s=55,
            label=flyway,
        )
        for _, row in d.iterrows():
            ax.annotate(
                row["transition"],
                (
                    row["environmental_innovation_sd_days"],
                    row["abs_lambda"],
                ),
                xytext=(5, 5),
                textcoords="offset points",
                fontsize=8,
            )

    ax.axhline(1.0, linestyle="--", linewidth=1.2)
    ax.set_xlim(
        max(0, env["environmental_innovation_sd_days"].min() - 0.5),
        env["environmental_innovation_sd_days"].max() + 0.7,
    )
    ax.set_ylim(-0.03, 1.05)
    ax.set_xlabel("Environmental innovation SD (days)")
    ax.set_ylabel(r"Phase retention $|\lambda|$")
    ax.set_title("B  Information and correction are separate channels")
    ax.legend(frameon=False, title="Flyway", loc="upper left")
    ax.text(
        0.99,
        -0.20,
        "Transition points share species/routes; not independent studies",
        transform=ax.transAxes,
        fontsize=8,
        ha="right",
        va="top",
    )

    fig.suptitle(
        "Movement–phenology phase control: common coordinate, heterogeneous regimes",
        fontsize=13,
    )

    png = OUT / "FIG4_PHASE_RETENTION_INFORMATION.png"
    pdf = OUT / "FIG4_PHASE_RETENTION_INFORMATION.pdf"
    svg = OUT / "FIG4_PHASE_RETENTION_INFORMATION.svg"
    fig.savefig(png, dpi=300, bbox_inches="tight")
    fig.savefig(pdf, bbox_inches="tight")
    fig.savefig(svg, bbox_inches="tight")
    plt.close(fig)

    taxa.to_csv(OUT / "FIG4_PANEL_A_DATA.csv", index=False)
    env.to_csv(OUT / "FIG4_PANEL_B_DATA.csv", index=False)
    return png


def main():
    path = build_figure4()
    print(path)


if __name__ == "__main__":
    main()
