"""Source weather independent-taxon transfer verdict invariants."""
import json
from pathlib import Path
def test_vulture_source_transfer_receipt():
    x=json.loads(Path("data/payoff_b_new_vulture_solar_transfer_result_20261022.json").read_text("utf-8"))
    assert x["n_complete_vulture_riskdays"]==1859
    assert x["n_original_northward_source_case_days"]==33
    assert x["original_nasa_daily_batches_failed"]==0
    assert x["n_same_gridyearmonth_case_days"]==19
    assert x["n_same_gridyearmonth_strata"]==18
    assert x["vulture_solar_association"]["descriptive_same_sign_as_stork"] is False
    assert x["vulture_solar_association"]["observed_vulture_solar_source_contrast_w_m2"]>0
    assert x["solar_hypothesis_directional_replication_support"] is False
    assert x["prior_V7V8_stork53_nonsupport_unchanged"] is True
