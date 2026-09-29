import json
import subprocess
import sys

import pytest

pd = pytest.importorskip("pandas")
np = pytest.importorskip("numpy")
pytest.importorskip("statsmodels")


def test_synthetic_fed_only_group_clustered_j_signal(tmp_path):
    exp_rows = []
    cond_rows = []

    # Six capture groups, two groups at each 2/3/4-day duration.
    for group_index in range(6):
        days = 2 + (group_index % 3)
        group = f"cap{group_index}"
        group_noise = (group_index - 2.5) * 0.015

        for bird_index in range(6):
            collar = f"g{group_index}_{bird_index}"
            baseline = (
                120.0
                + group_index * 0.7
                + bird_index * 0.4
            )
            individual_noise = (
                ((bird_index * 3 + group_index) % 5) - 2
            ) * 0.02
            post = (
                0.92 * baseline
                - 1.8 * days
                + group_noise
                + individual_noise
            )

            exp_rows.append({
                "Collar": collar,
                "UNIKCAPT": group,
                "DaysInCap": days,
                "FoodTreatment": "FED",
            })
            cond_rows.append({
                "Collar": collar,
                "cond1": baseline,
                "cond2": post,
            })

    exp = pd.DataFrame(exp_rows)
    cond = pd.DataFrame(cond_rows)

    exp_path = tmp_path / "data_exp.txt"
    cond_path = tmp_path / "cond.txt"
    out_path = tmp_path / "result.json"
    exp.to_csv(exp_path, sep="\t", index=False)
    cond.to_csv(cond_path, sep="\t", index=False)

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/payoff_b_snow_goose_j_mechanism.py",
            "--experiment",
            str(exp_path),
            "--condition",
            str(cond_path),
            "--output",
            str(out_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0

    result = json.loads(out_path.read_text(encoding="utf-8"))
    assert result["gate"]["estimable"]
    assert result["gate"]["capture_groups"] == 6
    assert result["gate"]["females"] == 36
    assert result["status"] == (
        "FED_CAPTIVITY_PHYSIOLOGICAL_J_SIGNAL_SUPPORTED"
    )
    assert result["primary"]["estimate"] < 0.0
    assert result["primary"]["ci_high_95"] < 0.0
    assert "cond2 ~ cond1 + DaysInCap" == result["primary"]["formula"]


def test_nonfed_rows_do_not_count_toward_primary_gate(tmp_path):
    exp_rows = []
    cond_rows = []
    for group_index in range(6):
        food = "FED" if group_index < 2 else "UNFED"
        for bird_index in range(10):
            collar = f"x{group_index}_{bird_index}"
            exp_rows.append({
                "Collar": collar,
                "UNIKCAPT": f"cap{group_index}",
                "DaysInCap": 2 + group_index % 3,
                "FoodTreatment": food,
            })
            cond_rows.append({
                "Collar": collar,
                "cond1": 100 + bird_index,
                "cond2": 95 + bird_index,
            })

    exp_path = tmp_path / "data_exp.txt"
    cond_path = tmp_path / "cond.txt"
    out_path = tmp_path / "result.json"
    pd.DataFrame(exp_rows).to_csv(exp_path, sep="\t", index=False)
    pd.DataFrame(cond_rows).to_csv(cond_path, sep="\t", index=False)

    subprocess.run(
        [
            sys.executable,
            "scripts/payoff_b_snow_goose_j_mechanism.py",
            "--experiment",
            str(exp_path),
            "--condition",
            str(cond_path),
            "--output",
            str(out_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    result = json.loads(out_path.read_text(encoding="utf-8"))
    assert not result["gate"]["estimable"]
    assert result["gate"]["capture_groups"] == 2
    assert result["status"] == "NOT_ESTIMABLE"
