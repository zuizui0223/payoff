import json
from pathlib import Path

from src.prodiginine_congener_sof import (
    ProdiginineCongenerProbeReceipt,
    adjudicate_prodiginine_congener_probe,
)


PATH = Path("validation/streptomyces_prodiginine_congener_sof_candidates_v1.json")


def load():
    return json.loads(PATH.read_text())


def receipt(row):
    return ProdiginineCongenerProbeReceipt(
        probe_id=row["probe_id"],
        support_reference=";".join(row["support_references"]),
        same_background_declared=row["same_background_declared"],
        congener_profile_changed_declared=row["congener_profile_changed_declared"],
        prodiginine_output_not_fully_abolished_declared=row[
            "prodiginine_output_not_fully_abolished_declared"
        ],
        candidate_selected_before_mu_outcome_declared=row[
            "candidate_selected_before_mu_outcome_declared"
        ],
        gross_development_matched_declared=row["gross_development_matched_declared"],
        focal_antibacterial_task_preserved_declared=row[
            "focal_antibacterial_task_preserved_declared"
        ],
        dna_damage_or_genotoxicity_difference_measured_declared=row[
            "dna_damage_or_genotoxicity_difference_measured_declared"
        ],
        direct_mu_difference_measured_declared=row["direct_mu_difference_measured_declared"],
        focal_task_assay_same_context_declared=row["focal_task_assay_same_context_declared"],
        mu_assay_same_context_declared=row["mu_assay_same_context_declared"],
    )


def test_registry_recomputes_expected_candidate_statuses():
    data = load()
    ready = 0
    certified = 0
    for row in data["candidates"]:
        got = adjudicate_prodiginine_congener_probe(receipt(row))
        assert got.biochemical_congener_probe_ready == row[
            "expected_biochemical_congener_probe_ready"
        ]
        assert got.separation_of_function_certified == row[
            "expected_separation_of_function_certified"
        ]
        ready += int(got.biochemical_congener_probe_ready)
        certified += int(got.separation_of_function_certified)
    assert ready == data["current_summary"]["biochemical_congener_probe_ready_count"]
    assert certified == data["current_summary"]["separation_of_function_certified_count"]


def test_two_candidates_are_ready_but_none_is_sof_certified():
    data = load()
    assert data["current_summary"]["biochemical_congener_probe_ready_count"] == 2
    assert data["current_summary"]["separation_of_function_certified_count"] == 0


def test_redg_candidates_are_frozen_preoutcome():
    data = load()
    assert data["selection_frozen_before_direct_mu_outcome"]
    rows = {row["probe_id"]: row for row in data["candidates"]}
    for probe_id in (
        "DELTA_redG_CONGENER_PARTITION",
        "DELTA_redG_PLUS_mcpG_CYCLIC_CONGENER_SWAP",
    ):
        assert rows[probe_id]["candidate_selected_before_mu_outcome_declared"]
        assert not rows[probe_id]["direct_mu_difference_measured_declared"]


def test_registry_never_promotes_architecture_or_game_claims():
    summary = load()["current_summary"]
    assert not summary["matched_s_certified"]
    assert not summary["architecture_mapping_certified"]
    assert not summary["generic_game_promoted"]
    assert not summary["eta_promoted"]
    assert not summary["e1_promoted"]
