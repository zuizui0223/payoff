#!/usr/bin/env python3
"""Analyze long-term resident--migrant timing divergence in Kallander et al.

Source columns are frozen by Dryad metadata:
Year, Sp, Reg., Temp, Date, Anno
Sp: 1 marsh tit, 2 blue tit, 3 great tit, 4 pied flycatcher.

This script does not test predictive-information hysteresis.  It quantifies the
long-term phenological gap between locally responding resident tits and the
migratory pied flycatcher, using within-region/year pairing where possible.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


SPECIES = {
    1: "marsh_tit",
    2: "blue_tit",
    3: "great_tit",
    4: "pied_flycatcher",
}


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    p.add_argument(
        "--output-json",
        type=Path,
        default=Path("outputs/sweden_long_term_timing_result.json"),
    )
    p.add_argument(
        "--paired-output",
        type=Path,
        default=Path("outputs/sweden_resident_migrant_pairs.csv"),
    )
    return p.parse_args()


def _normalise_columns(df):
    rename = {}
    for column in df.columns:
        key = str(column).strip().lower().replace(" ", "")
        if key in {"year"}:
            rename[column] = "year"
        elif key in {"sp", "species"}:
            rename[column] = "species_code"
        elif key in {"reg.", "reg", "region"}:
            rename[column] = "region"
        elif key in {"temp", "temperature"}:
            rename[column] = "temperature"
        elif key in {"date", "laydate", "layingdate"}:
            rename[column] = "lay_date"
        elif key in {"anno"}:
            rename[column] = "anno"
    return df.rename(columns=rename)


def main():
    args = parse_args()
    try:
        import numpy as np
        import pandas as pd
        import statsmodels.formula.api as smf
    except ImportError as exc:
        raise RuntimeError(
            "Swedish timing analysis requires pandas, numpy, statsmodels, openpyxl"
        ) from exc

    raw = pd.read_excel(args.input)
    data = _normalise_columns(raw.copy())
    required = {
        "year",
        "species_code",
        "region",
        "temperature",
        "lay_date",
    }
    missing = required.difference(data.columns)
    if missing:
        raise ValueError("missing columns: " + ", ".join(sorted(missing)))

    for column in (
        "year",
        "species_code",
        "region",
        "temperature",
        "lay_date",
    ):
        data[column] = pd.to_numeric(data[column], errors="coerce")
    data = data.dropna(subset=list(required)).copy()
    data["species_code"] = data["species_code"].astype(int)
    data = data[data["species_code"].isin(SPECIES)].copy()
    data["species"] = data["species_code"].map(SPECIES)
    data["year"] = data["year"].astype(int)
    data["region"] = data["region"].astype(int)

    # Collapse duplicate study rows to one regional species-year mean.
    yearly = (
        data.groupby(["year", "region", "species_code", "species"], as_index=False)
        .agg(
            lay_date=("lay_date", "mean"),
            temperature=("temperature", "mean"),
            source_rows=("lay_date", "size"),
        )
    )

    migrant = yearly[yearly["species_code"] == 4].rename(
        columns={
            "lay_date": "migrant_lay_date",
            "temperature": "migrant_temperature",
        }
    )
    resident = yearly[yearly["species_code"].isin([1, 2, 3])].rename(
        columns={
            "lay_date": "resident_lay_date",
            "temperature": "resident_temperature",
            "species": "resident_species",
            "species_code": "resident_species_code",
        }
    )

    paired = resident.merge(
        migrant[
            [
                "year",
                "region",
                "migrant_lay_date",
                "migrant_temperature",
            ]
        ],
        on=["year", "region"],
        how="inner",
        validate="many_to_one",
    )
    if len(paired) < 20:
        raise ValueError("too few within-region resident-migrant pairs")

    paired["timing_gap_days"] = (
        paired["migrant_lay_date"] - paired["resident_lay_date"]
    )
    paired["temperature_gap_c"] = (
        paired["migrant_temperature"] - paired["resident_temperature"]
    )
    paired["year_centered"] = paired["year"] - paired["year"].mean()

    # Primary model: within-region/year resident-specific gap trend.
    gap_fit = smf.ols(
        "timing_gap_days ~ year_centered * C(resident_species) + C(region)",
        data=paired,
    ).fit(cov_type="HC3")

    # Shared slope summary after controlling resident species and region.
    pooled_gap = smf.ols(
        "timing_gap_days ~ year_centered + C(resident_species) + C(region)",
        data=paired,
    ).fit(cov_type="HC3")

    # Species-specific laying-date trend, controlling region.
    species_rows = []
    for code, name in SPECIES.items():
        subset = yearly[yearly["species_code"] == code].copy()
        if len(subset) < 10:
            continue
        subset["year_centered"] = subset["year"] - subset["year"].mean()
        model = smf.ols(
            "lay_date ~ year_centered + C(region)",
            data=subset,
        ).fit(cov_type="HC3")
        beta = float(model.params["year_centered"])
        se = float(model.bse["year_centered"])
        species_rows.append(
            {
                "species_code": code,
                "species": name,
                "rows": int(len(subset)),
                "years": int(subset["year"].nunique()),
                "regions": int(subset["region"].nunique()),
                "lay_date_trend_days_per_year": beta,
                "se_hc3": se,
                "ci_low_95": beta - 1.96 * se,
                "ci_high_95": beta + 1.96 * se,
                "p_value": float(model.pvalues["year_centered"]),
            }
        )

    # Temperature sensitivity, within species and region.
    temperature_rows = []
    for code, name in SPECIES.items():
        subset = yearly[yearly["species_code"] == code].copy()
        if len(subset) < 10:
            continue
        subset["year_centered"] = subset["year"] - subset["year"].mean()
        model = smf.ols(
            "lay_date ~ temperature + year_centered + C(region)",
            data=subset,
        ).fit(cov_type="HC3")
        beta = float(model.params["temperature"])
        se = float(model.bse["temperature"])
        temperature_rows.append(
            {
                "species_code": code,
                "species": name,
                "temperature_sensitivity_days_per_c": beta,
                "se_hc3": se,
                "ci_low_95": beta - 1.96 * se,
                "ci_high_95": beta + 1.96 * se,
                "p_value": float(model.pvalues["temperature"]),
            }
        )

    # Year-level network gap using resident centroid when >=2 resident species
    # are represented in the same region/year.
    resident_centroid = (
        resident.groupby(["year", "region"], as_index=False)
        .agg(
            resident_centroid=("resident_lay_date", "mean"),
            resident_species_n=("resident_species_code", "nunique"),
        )
    )
    network = resident_centroid.merge(
        migrant[["year", "region", "migrant_lay_date"]],
        on=["year", "region"],
        how="inner",
    )
    network = network[network["resident_species_n"] >= 2].copy()
    network["network_gap_days"] = (
        network["migrant_lay_date"] - network["resident_centroid"]
    )
    network["year_centered"] = network["year"] - network["year"].mean()

    if len(network) >= 10:
        network_fit = smf.ols(
            "network_gap_days ~ year_centered + C(region)",
            data=network,
        ).fit(cov_type="HC3")
        network_beta = float(network_fit.params["year_centered"])
        network_se = float(network_fit.bse["year_centered"])
        network_summary = {
            "rows": int(len(network)),
            "years": int(network["year"].nunique()),
            "regions": int(network["region"].nunique()),
            "trend_days_per_year": network_beta,
            "se_hc3": network_se,
            "ci_low_95": network_beta - 1.96 * network_se,
            "ci_high_95": network_beta + 1.96 * network_se,
            "p_value": float(network_fit.pvalues["year_centered"]),
        }
    else:
        network_summary = {"status": "NOT_ESTIMABLE"}

    beta = float(pooled_gap.params["year_centered"])
    se = float(pooled_gap.bse["year_centered"])
    primary = {
        "paired_rows": int(len(paired)),
        "years": int(paired["year"].nunique()),
        "regions": int(paired["region"].nunique()),
        "resident_species": int(paired["resident_species"].nunique()),
        "pooled_gap_trend_days_per_year": beta,
        "se_hc3": se,
        "ci_low_95": beta - 1.96 * se,
        "ci_high_95": beta + 1.96 * se,
        "p_value": float(pooled_gap.pvalues["year_centered"]),
    }

    args.paired_output.parent.mkdir(parents=True, exist_ok=True)
    paired.to_csv(args.paired_output, index=False)

    result = {
        "result_id": "payoff_b_sweden_resident_migrant_timing_v1",
        "status": "LONG_TERM_INTERACTION_TIMING_ANALYSIS",
        "source": {
            "doi": "10.5061/dryad.sq651",
            "paper_doi": "10.1111/jav.01287",
            "file": "All laydate.xlsx",
            "dryad_file_id": 34004,
            "md5": "50bb3503258e5f8ce4db043d0bfe895d",
        },
        "source_rows": int(len(data)),
        "source_year_min": int(data["year"].min()),
        "source_year_max": int(data["year"].max()),
        "primary_relative_timing": primary,
        "network_centroid_gap": network_summary,
        "species_lay_date_trends": species_rows,
        "species_temperature_sensitivities": temperature_rows,
        "claim_boundary": [
            "this is a long-term resident-migrant timing contrast, not a pre-commitment information test",
            "the 30-day temperature variable is species-specific and centered on each species' laying phenology",
            "no remote wintering-ground cue exists in this dataset",
            "therefore no natural information-triggered hysteresis claim is licensed",
        ],
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(result, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
