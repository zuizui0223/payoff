import json
from pathlib import Path


def test_pacbio_corroboration_merge_guard_stays_below_primary_bgi_gate():
    data = json.loads(Path("validation/streptomyces_m5_pacbio_marker_corroboration_merge_guard_v1.json").read_text())
    assert data["pacbio_corroboration_available"] is True
    assert data["primary_bgi_target_opened"] is False
    assert data["response_blind_bgi_calibration_still_required"] is True
    assert data["qualified_d_reference"] is False
    assert data["qualified_d_reference_count_increment"] == 0
    assert data["architecture_specific_inference_open"] is False
