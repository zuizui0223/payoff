import json
import subprocess
import sys

import pytest

pd = pytest.importorskip("pandas")
np = pytest.importorskip("numpy")
pytest.importorskip("statsmodels")


def test_synthetic_dual_use_screen_recovers_registered_negative_signal(tmp_path):
    rows = []
    contexts = [
        ("St_Lawrence", "Nunavik"),
        ("Nunavik", "Baffin"),
        ("Baffin", "Bylot"),
    ]

    for i in range(30):
        for year_index, year in enumerate(range(2020, 2024)):
            for context_index, (origin, destination) in enumerate(contexts):
                # Context-year predictive connectivity with non-additive
                # variation so it is not absorbed by context + year effects.
                rho = (
                    0.18
                    + 0.08 * context_index
                    + 0.035 * year_index
                    + 0.018 * context_index * year_index
                )
                wait_days = 1 + ((i + 2 * context_index + year_index) % 8)
                temp = (
                    ((i * 5 + context_index * 3 + year_index) % 17) - 8
                ) * 0.11
                wind = ((i + context_index + year_index) % 9 - 4) * 0.08
                precip = ((i + 2 * year_index) % 5) * 0.12
                same_day = temp * 0.55 + ((i + context_index) % 7 - 3) * 0.03
                doy = 122 + context_index * 13 + year_index + (i % 4)

                rows.append(
                    {
                        "individual": f"g{i:02d}",
                        "year": year,
                        "origin_context": origin,
                        "destination_context": destination,
                        "departure_date": f"{year}-05-{1 + (i % 20):02d}",
                        "wait_days_in_origin": wait_days,
                        "local_temp_anom3": temp,
                        "same_day_temp_anom": same_day,
                        "day_of_year_within_context": doy,
                        "wind_support": wind,
                        "precipitation": precip,
                        "predictive_connectivity_rho": rho,
                        "connectivity_training_n": 20,
                        "connectivity_window_end_year": year - 1,
                    }
                )

    df = pd.DataFrame(rows)
    zrho = (
        df["predictive_connectivity_rho"]
        - df["predictive_connectivity_rho"].mean()
    ) / df["predictive_connectivity_rho"].std(ddof=0)
    zwait = (
        df["wait_days_in_origin"] - df["wait_days_in_origin"].mean()
    ) / df["wait_days_in_origin"].std(ddof=0)

    # Strong registered negative dual-use signal plus deterministic small
    # nuisance variation. Duration remains positive after exponentiation.
    noise = np.array(
        [((idx * 7) % 19 - 9) * 0.005 for idx in range(len(df))]
    )
    log_duration = (
        2.0
        - 0.55 * df["local_temp_anom3"].to_numpy() * zrho.to_numpy()
        + 0.04 * zwait.to_numpy()
        + 0.015 * df["wind_support"].to_numpy()
        + noise
    )
    df["transit_duration_days"] = np.exp(log_duration)

    input_path = tmp_path / "transitions.csv"
    output_path = tmp_path / "result.json"
    df.to_csv(input_path, index=False)

    completed = subprocess.run(
        [
            sys.executable,
            "scripts/payoff_b_greater_snow_goose_dual_use_compensation_screen.py",
            "--transitions",
            str(input_path),
            "--output",
            str(output_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    assert completed.returncode == 0

    result = json.loads(output_path.read_text(encoding="utf-8"))
    assert result["estimability_gate"]["estimable"]
    assert result["status"] == "DUAL_USE_BEHAVIORAL_SIGNAL_SUPPORTED"
    assert result["primary"]["estimate"] < 0.0
    assert result["primary"]["ci_high_95"] < 0.0



def test_forward_route_skip_is_accepted_by_frozen_transition_semantics():
    # Static contract guard: the script must define all forward route pairs,
    # not only consecutive segments.
    from scripts.payoff_b_greater_snow_goose_dual_use_compensation_screen import (
        ALLOWED_SEGMENTS,
    )

    assert ("St_Lawrence", "Baffin") in ALLOWED_SEGMENTS
    assert ("St_Lawrence", "Bylot") in ALLOWED_SEGMENTS
    assert ("Nunavik", "Bylot") in ALLOWED_SEGMENTS
    assert ("Baffin", "St_Lawrence") not in ALLOWED_SEGMENTS
