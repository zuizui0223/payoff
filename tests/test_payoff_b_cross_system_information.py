from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "data" / "payoff_b_cross_system_information_result_20260928.json"
DOC = ROOT / "docs" / "PAYOFF_B_CROSS_SYSTEM_INFORMATION_RESULT_20260928.md"


def load_result() -> dict:
    return json.loads(RESULT.read_text(encoding="utf-8"))


def test_cross_system_result_is_frozen_and_passed():
    x = load_result()
    assert x["status"] == "PROMOTION_GATE_PASSED"
    assert x["provenance"]["workflow_run"] == 36383464308
    assert x["provenance"]["head_sha"] == "986257f19abba0cd8b1387984e6f45607f68ecbc"
    assert x["provenance"]["usui_sha256"] == "68816f6cbfccbb9b47b45be0df49f077db914c8e43e567d0ed2cac9bbafde56c"
    assert x["provenance"]["freimuth_temp_sha256"] == "946f56b8aa5f43bb15f5bbbd8c5174be23c12691332651e09bce2cb20edf7efd"


def test_bird_information_distance_signal_is_robust():
    x = load_result()["bird_temperature_meta_regression"]
    assert x["eligible_rows"] == 944
    assert x["studies"] == 28
    assert x["species"] == 279

    primary = x["adjusted_primary"]
    assert primary["long_minus_short_days_per_C"] > 0
    assert primary["ci95"][0] > 0
    assert primary["p"] < 0.01

    assert x["sensitivity"]["weight_cap_99"]["ci95"][0] > 0
    assert x["sensitivity"]["unweighted_adjusted"]["ci95"][0] > 0


def test_freimuth_published_group_reconstruction_passed():
    x = load_result()["freimuth_local_benchmark"]
    assert x["rows"] == 1763
    assert x["taxonomy_unresolved"] == 0
    assert x["published_group_count_and_mean_reproduction"] == "PASS"

    assert x["groups"]["Plants"]["n"] == 1438
    assert x["groups"]["Bees"]["n"] == 20
    assert x["groups"]["Flies"]["n"] == 22
    assert x["groups"]["Butterflies/Moths"]["n"] == 206
    assert x["groups"]["Beetles"]["n"] == 77


def test_claim_boundary_blocks_taxon_ranking_and_fake_novelty():
    x = load_result()
    prohibited = " ".join(x["prohibited_claims"])
    assert "pollinators universally" in prohibited
    assert "causal" in prohibited
    assert "newly discovered" in prohibited
    assert "new cross-taxon meta-analysis" in prohibited

    doc = DOC.read_text(encoding="utf-8")
    assert "E6 — cross-system information-distance" in doc
    assert "full natural degradation--recovery hysteresis remains unobserved" in doc
