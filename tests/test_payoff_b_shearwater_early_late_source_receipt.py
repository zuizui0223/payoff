"""Archive frozen source-only early/late GPS quality with correct denominators."""
import json
from pathlib import Path
def test_shearwater_two_window_source_receipt():
    x=json.loads(Path("data/payoff_b_shearwater_early_late_GPS_source_result_20261028.json").read_text("utf-8"))
    assert x["total_eligible"]==22
    assert x["eligible_GPS_0to12_and_12to24h"]=={"control":8,"magnetic_disruption":8,"olfactory_deprivation":6}
    assert x["original_ARGOS_allocated_to_olfactory_by_design"]==5
    assert abs(x["olfactory_minus_control_maximum_missing_outcome_bound_width"]-(8/14+1/9))<1e-12
    assert x["novel_PayoffB_theory_supported"] is False
