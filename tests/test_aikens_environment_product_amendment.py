import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AMENDMENT = (
    ROOT
    / "data"
    / "aikens2022_environment_product_amendment_20260922.json"
)
MANIFEST_STATUS = (
    ROOT
    / "data"
    / "payoff_b_aikens_exact_manifest_status_20260921.json"
)
REGISTRATION = (
    ROOT
    / "data"
    / "aikens2022_lambda_perturbation_registration_20260921.json"
)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_v061_primary_successor_amendment_is_frozen_before_lambda_outcome():
    amendment = load(AMENDMENT)

    assert amendment["frozen_date"] == "2026-09-22"
    assert amendment["outcome_state_at_freeze"] == "lambda_outcome_unopened"
    assert (
        amendment["effective_primary_environment_lane"]
        == "v061_primary_successor_after_v006_decommission"
    )
    availability = amendment["external_availability_change"]
    assert availability["original_study_product"] == "MOD09Q1.006"
    assert availability["official_distribution_end_date"] == "2023-07-31"
    assert availability["distribution_status"] == "decommissioned"
    assert availability["replacement_current_product"] == "MOD09Q1.061"
    assert availability["replacement_snow_product"] == "MOD10A2.061"


def test_product_amendment_reuses_exact_frozen_v061_request_geometry():
    amendment = load(AMENDMENT)
    status = load(MANIFEST_STATUS)

    exact = status["exact_modis250_manifest"]
    assert (
        amendment["frozen_v061_manifest_sha256"]
        == exact["manifest_sha256"]
    )
    source = amendment["frozen_source_contract"]
    assert source["gps_observations"] == 64539
    assert source["unique_modis250_cells"] == exact["unique_cells"]
    assert (
        source["unique_modis250_cell_years"]
        == exact["unique_cell_years"]
    )
    assert (
        source["year_scoped_tasks_at_1000_cells"]
        == exact["year_scoped_tasks_at_1000_cells"]
    )


def test_product_amendment_does_not_retune_lambda_registration():
    amendment = load(AMENDMENT)
    registration = load(REGISTRATION)
    contract = amendment["unchanged_confirmatory_contract"]

    for key in (
        "independent_test_id",
        "phase_coordinate_id",
        "segment_scale_id",
        "expected_direction",
        "max_p_value",
        "min_abs_difference",
    ):
        assert contract[key] == registration[key]

    invariants = amendment["invariants"]
    assert all(invariants.values())
    assert contract["min_animals_per_group"] == 10
    assert contract["min_transitions_per_group"] == 100
    assert (
        contract["primary_model"]
        == "E_next ~ E_current + E_current:large_development + C(animal_year)"
    )
    assert contract["cluster_uncertainty_by"] == "animal_id"
