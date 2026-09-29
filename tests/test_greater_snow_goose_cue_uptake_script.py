import json
import math
import subprocess
import sys
from pathlib import Path

import pandas as pd


def test_registered_script_runs_on_synthetic_estimable_panel(tmp_path):
    contexts = [
        "southern_staging",
        "mid_arctic_staging",
        "northern_arctic_staging",
    ]
    years = [2019, 2020, 2021, 2022]
    rho = {
        "southern_staging": [0.05, 0.10, 0.15, 0.20],
        "mid_arctic_staging": [0.20, 0.25, 0.30, 0.35],
        "northern_arctic_staging": [0.35, 0.40, 0.45, 0.50],
    }

    connectivity = []
    for context in contexts:
        for year_index, year in enumerate(years):
            connectivity.append(
                {
                    "context": context,
                    "year": year,
                    "connectivity_rho": rho[context][year_index],
                    "training_end_year": year - 1,
                    "training_years": 20,
                }
            )

    rows = []
    for individual_index in range(30):
        for year_index, year in enumerate(years):
            for context_index, context in enumerate(contexts):
                event_day = (
                    individual_index + year_index + context_index
                ) % 5
                for day in range(5):
                    rows.append(
                        {
                            "individual_id": f"id{individual_index:02d}",
                            "year": year,
                            "context": context,
                            "depart_next_24h": int(day == event_day),
                            "local_temp_anom3": math.sin(
                                (individual_index + 1) * 0.17
                                + year_index * 0.31
                                + context_index * 0.47
                                + day * 0.59
                            ),
                            "day_of_year_within_context": day - 2,
                            "wind_support": math.cos(
                                (individual_index + 1) * 0.13
                                + day * 0.20
                            ),
                            "precipitation": (
                                (individual_index + day + context_index) % 4
                            ) * 0.20,
                        }
                    )

    risk_path = tmp_path / "risk.csv"
    connectivity_path = tmp_path / "connectivity.csv"
    output_path = tmp_path / "result.json"
    pd.DataFrame(rows).to_csv(risk_path, index=False)
    pd.DataFrame(connectivity).to_csv(connectivity_path, index=False)

    subprocess.run(
        [
            sys.executable,
            "scripts/payoff_b_greater_snow_goose_cue_uptake.py",
            "--day-risk",
            str(risk_path),
            "--connectivity",
            str(connectivity_path),
            "--output",
            str(output_path),
        ],
        check=True,
        timeout=120,
    )

    result = json.loads(output_path.read_text())
    assert result["status"] == "ESTIMABLE"
    assert result["gate"]["individuals"] == 30
    assert result["gate"]["context_years"] == 12
    assert result["primary"]["individual_cluster"]["clusters"] == 30
    assert result["primary"]["context_year_cluster"]["clusters"] == 12
    assert result["primary"]["support_status"] in {
        "SUPPORTED",
        "NOT_SUPPORTED",
    }
    assert result["threshold_secondary"]["status"] in {
        "SUPPORTED_BEHAVIORAL_THRESHOLD_LIKE",
        "THRESHOLD_NOT_IDENTIFIED",
    }
