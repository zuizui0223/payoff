"""Regression guards for the 25-year published BTBW annual archive."""
from pathlib import Path
import math

import pytest

from scripts.payoff_b_btbw_annual_reanalysis import read_annual, run, temporal_mse

SOURCE = Path(__file__).resolve().parents[1] / "data" / "external" / "btbw_lany_2015_annual_Dryad_mirror.csv"


def test_fixed_source_results_and_no_fitness_optimum():
    r = run(SOURCE)
    assert r["source"]["year_n"] == 25
    assert r["source"]["male_arrival_nonmissing_years"] == 22
    assert r["status"] == "DESCRIPTIVE_PRIOR_ART_ONLY"
    assert abs(
        r["temporal"]["clutch_vs_canopy"]["terms"]["Acsa.canopy"]["coef"]
        - 0.5653670750245908
    ) < 1e-9
    lag = r["annual_fitness_association"]["models"]["plus_lag"]["terms"]["lag"]
    assert lag["hc3_ci95"][0] < 0 < lag["hc3_ci95"][1]
    assert all(x == "NOT_IDENTIFIED" for x in r["unidentified"].values())


def test_legacy_cr_and_lf_parse_equal(tmp_path):
    raw = SOURCE.read_bytes()
    unix = tmp_path / "unix.csv"
    mac = tmp_path / "mac.csv"
    unix.write_bytes(raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n"))
    mac.write_bytes(unix.read_bytes().replace(b"\n", b"\r"))
    for a, b in zip(read_annual(unix), read_annual(mac)):
        for key in a:
            assert a[key] == b[key] or (
                math.isnan(a[key]) and math.isnan(b[key])
            )


def test_reject_missing_clutch_and_duplicate_year(tmp_path):
    raw = SOURCE.read_bytes().decode("utf-8").replace("\r", "\n")
    bad = tmp_path / "bad.csv"
    bad.write_text(
        raw.replace("1986,0.45,121,139,,148,", "1986,0.45,121,139,,,", 1)
    )
    with pytest.raises(ValueError, match="Unexpected NA"):
        read_annual(bad)
    lines = raw.splitlines()
    bad.write_text("\n".join([lines[0], lines[1], lines[1]] + lines[3:]) + "\n")
    with pytest.raises(ValueError, match="Source-year"):
        read_annual(bad)


def test_heldout_year_block_fixed():
    rows = read_annual(SOURCE)
    mse = temporal_mse(
        rows, ("Acsa.canopy", "ln.mean.cats", "density", "prop.F.ASY")
    )
    assert mse["train_n"] == 14
    assert mse["test_n"] == 11
    assert mse["test_mse"] > 0
