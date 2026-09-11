import json
from pathlib import Path


REALIZATION = Path("validation/streptomyces_direct_mu_realization_design_v1.json")
ASSAY = Path("validation/streptomyces_congener_assay_scale_status_v1.json")
ARCH = Path("validation/architecture_mapping_status_v1.json")


def test_absolute_mass_design_advances_measurement_only_not_architecture():
    realization = json.loads(REALIZATION.read_text())
    assay = json.loads(ASSAY.read_text())
    arch = json.loads(ARCH.read_text())
    strepto = next(
        row for row in arch["systems"] if row["system_id"] == "STREPTOMYCES_COELICOLOR"
    )

    assert realization["status"]["design_frozen_preoutcome"]
    assert assay["current_summary"]["direct_mu_realization_design_frozen_preoutcome"]

    assert not realization["status"]["reference_panel_materialized"]
    assert not realization["status"]["reference_panel_qualified"]
    assert not realization["status"]["d_band_available"]
    assert not realization["status"]["absolute_mass_route_ready"]
    assert not assay["current_summary"]["direct_mu_fully_ready"]

    assert not strepto["matched_generalist_shared_architecture_recovered"]
    assert not strepto["matched_s_promotion_licensed"]
    assert not strepto["mapping_certified"]
    assert not arch["frequency_game_evidence_used_to_certify_mapping"]
    assert not arch["any_mapping_certified"]
