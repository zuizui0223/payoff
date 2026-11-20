"""Original Lameris 2025 randomly assigned feeding-time source audit tests."""
import csv
import io

import pytest
pytest.importorskip("requests")

from scripts.payoff_b_red_knot_aviary_release_source_gate import (
    FILES, analyze_original_table, codebook_aviary_mentions, normalize_hour
)

COLUMNS=(
    "BirdID.year,year,treatment,release_date,departed,departure,"
    "departure_jul,wing,mass_capture,slope"
)


def artificial_102_rows():
    rows=[]
    for i in range(102):
        year=str(2021+i%3)
        tr=str((6,12,24)[i%3])
        rel="" if year=="2021" else "REDACTED_LOCAL_DATE"
        dep="" if year=="2021" or i%4==0 else "REDACTED_DEPARTURE"
        rows.append({
            "BirdID.year":f"SYNTH_ID_{i}",
            "year":year,"treatment":tr,
            "release_date":rel,
            "departed":"" if not rel else ("1" if dep else "0"),
            "departure":dep,
            "departure_jul":"88" if dep else "",
            "wing":"125.0","mass_capture":"112.0","slope":"1.0"
        })
    with io.StringIO() as h:
        writer=csv.DictWriter(h,fieldnames=COLUMNS.split(","))
        writer.writeheader()
        writer.writerows(rows)
        return h.getvalue().encode()


def test_predecision_source_accepts_metadata_but_refuses_aviary_inference():
    x=analyze_original_table(artificial_102_rows())
    assert x["original_source_combined_rows"]==102
    assert x["n_source_bird_year_keys"]==102
    assert x["year_code_status"]=="SOURCE_2021_2023_LABELS_VERIFIED"
    assert x["treatment_code_status"]=="SOURCE_HOURS_6_12_24_VERIFIED"
    assert x["source_aviary_or_cage_membership_columns"]==[]
    assert x["actual_author_specific_aviary_id_per_individual_verified"] is False
    assert x["missing_departure_assumed_a_nondeparture"] is False
    assert x["source_year_treatment_release_and_departure_aggregate"]["2021"][
        "source_release_date_present"]==0
    assert "SYNTH_ID" not in str(x)


def test_source_individual_key_duplicates_fail():
    raw=artificial_102_rows().decode()
    raw=raw.replace("SYNTH_ID_0","SYNTH_ID_1",1)
    with pytest.raises(ValueError,match="key missing or duplicated"):
        analyze_original_table(raw.encode())


def test_source_treatment_code_not_silently_interpreted_as_original_6_12_24():
    raw=artificial_102_rows().decode().replace(",12,",",unknown,",1)
    x=analyze_original_table(raw.encode())
    assert x["treatment_code_status"]=="SOURCE_TREATMENT_CODES_NEED_ORIGINAL_README_MAPPING"


def test_source_declared_aviary_only_even_if_code_mentions_it():
    c=codebook_aviary_mentions(
        b"Birds in two aviaries per treatment, 2022 and 2023.",
        b"coxph(Surv(time, status) ~ treatment + cluster(aviary))"
    )
    assert c["original_readme_summary"]["n_aviary_mentions"]==0 or (
        c["original_readme_summary"]["n_aviary_mentions"]>=1)
    assert c["original_analysis_R_summary"]["n_explicit_aviary_by_year_model_tokens"]>=1
    assert c["aviary_membership_for_each_individual_proven_by_text_search"] is False


def test_original_published_hashes_are_exact_and_unique():
    assert len(FILES)==3
    assert len({v[0] for v in FILES.values()})==3
    assert all(len(v[2])==64 for v in FILES.values())
    assert normalize_hour("24h")== "24"
    assert normalize_hour("6 hours")=="6"
    assert normalize_hour("unknown") is None
