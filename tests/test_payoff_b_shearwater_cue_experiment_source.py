"""Synthetic manipulation metadata controls, no real subject identifiers."""
import csv
from pathlib import Path
from scripts.qc_payoff_b_shearwater_cue_experiment_source import (
    arm,refs,tracking_stream,EXPECTED_REFERENCE_GROUPS
)

def test_source_spelling_asnomic_preserved():
    assert arm("asnomic treatment group; relocated and released")=="olfactory_deprivation"
    assert arm("anosmic treatment group")=="olfactory_deprivation"
    assert arm("magnetically disrupted treatment group")=="magnetic_disruption"
    assert arm("control group; relocated and released")=="control"
    assert arm("n/a")=="UNRESOLVED_TREATMENT"

def test_actual_32_reference_arms_encoded_only_as_counts(tmp_path:Path):
    file=tmp_path/"ref.csv"
    rows=[]
    for group,n in [("control group",9),("magnetically disrupted",9),
                    ("asnomic treatment",14)]:
        for i in range(n):
            rows.append({"animal-id":f"bird-{group}-{i}",
                         "tag-id":f"tag-{group}-{i}",
                         "manipulation-type":"other",
                         "manipulation-comments":group})
    with file.open("w",newline="") as h:
        w=csv.DictWriter(h,fieldnames=list(rows[0]))
        w.writeheader();w.writerows(rows)
    ident,tags,report=refs(file)
    assert len(ident)==32
    assert report["published_treatment_groups"]==EXPECTED_REFERENCE_GROUPS
    assert "bird-control" not in str(report)
    assert report["original_group_assignment_is_blinded_randomized"] is False

def test_source_sensor_match_preserves_animal_group_and_no_coords(tmp_path:Path):
    file=tmp_path/"gps.csv"
    file.write_text("timestamp,individual-local-identifier,location-lat,location-long\n"+
        "".join(f"2015-04-01 {h:02d}:00:00,anon,40,12\n" for h in range(12)))
    r=tracking_stream(file,{"anon":"control"},{})
    assert r["original_valid_events_by_manipulation_group"]["control"]==12
    assert r["individual_tracks_with_at_least_10_events"]["control"]==1
    assert "anon" not in str(r)
    assert "40" not in str(r)
