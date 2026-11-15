from src.japan_phenology_event_definition_audit import stage_from_label, source_event_inventory

def test_event_types_not_conflated():
    assert stage_from_label("うぐいすの初鳴")=="first_call"
    assert stage_from_label("つばめの初見")=="first_sighting"
    assert stage_from_label("さくらの開花")=="flowering"
    assert stage_from_label("さくらの満開")=="full_bloom"
    assert stage_from_label("いちょうの黄葉")=="color_change"
    assert stage_from_label("不明な季節観測")=="unclassified_or_multiple"

def test_inventory_retains_original_labels():
    rows=[{"source_file":"x.csv","event_label":"さくらの開花",
           "source_taxon_guess":"plant_or_unclassified","year":2020,
           "day_of_year":100,"station_id":"401"}]
    out=source_event_inventory(rows)
    assert out["source_event_file_count"]==1
    assert out["explicit_label_stage_file_counts"]=={"flowering":1}
    assert out["source_event_inventory"][0]["official_event_label"]=="さくらの開花"
    assert out["rm_semantics_certified"] is False
