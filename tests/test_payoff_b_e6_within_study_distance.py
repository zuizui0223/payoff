"""Source-verified previous E6 effect rows; no independent ecological replication."""
from pathlib import Path
import os
import pytest

pd = pytest.importorskip("pandas")
np = pytest.importorskip("numpy")

from scripts.payoff_b_e6_known_ebird_exclusion import read_verified_artifact
from scripts.payoff_b_e6_within_study_distance import (
    fixed_study_design, run, source_only_crossed_studies,
)


def test_fixed_study_dummy_design_is_rank_identifiable():
    rows=[]
    for study in ("A","B","C"):
        for distance in ("short","long"):
            rows.append({"Study":study,"Migration_distance":distance})
    x,cols=fixed_study_design(pd.DataFrame(rows))
    assert x.shape==(6,4)
    assert len(cols)==4
    assert cols[0]=="intercept"
    assert cols[1]=="long_minus_short"
    assert int(np.linalg.matrix_rank(x))==4


def test_non_crossed_study_fixed_effect_identification_rejected():
    df=pd.DataFrame({
        "Study":["A","A","B","B"],
        "Migration_distance":["short","short","short","short"],
    })
    with pytest.raises(ValueError,match="Study FE model not full rank"):
        fixed_study_design(df)


def test_original_13_source_study_temperature_response_with_frozen_archive():
    path=os.environ.get("PAYOFF_E6_ARCHIVED_ARTIFACT_ZIP")
    if not path:
        pytest.skip("Original SHA-verified E6 artifact supplied by dedicated GitHub CI")
    original=read_verified_artifact(Path(path))
    paired=source_only_crossed_studies(original)
    assert len(paired)==444
    assert paired.Study.nunique()==13
    assert paired.Species.nunique()==269
    result=run(original)
    q=result["primary_study_fixed_effect_ivw"]
    assert q["n_effect_rows"]==444
    assert q["n_independent_source_studies"]==13
    assert q["study_cluster_df"]==12
    assert q["design_columns"]==14
    assert q["design_rank"]==14
    assert q["beta_long_minus_short_days_per_C"]==pytest.approx(
        0.5252532818331183,abs=1e-7)
    assert q["cluster_se"]==pytest.approx(0.13813488906607674,abs=1e-7)
    assert q["ci95"]==pytest.approx([0.22428321331129092,0.8262233503549457],abs=1e-7)
    assert result["weight_capped_99_sensitivity"]["beta_long_minus_short_days_per_C"]==pytest.approx(
        0.5254375013693964,abs=1e-7)
    assert result["unweighted_sensitivity"]["beta_long_minus_short_days_per_C"]==pytest.approx(
        0.6086066573240716,abs=1e-7)
    loo=result["leave_one_original_study_out"]
    assert loo["n_repeats"]==13
    assert loo["all_positive_estimates"] is True
    assert loo["min_beta"]==pytest.approx(0.47279272297930114,abs=1e-7)
    assert loo["max_beta"]==pytest.approx(0.6230059463836852,abs=1e-7)
    assert result["study_descriptive_unadjusted_signs"]["positive"]==11
    assert result["study_descriptive_unadjusted_signs"]["negative"]==2
    assert result["no_new_source_independent_replication"] is True
    assert result["no_information_distance_causal_mechanism_identified"] is True
    assert result["frozen_V7_individual_q_times_geography_urgency"]=="NOT_ESTIMABLE"
