from scripts.qc_public_movebank_crossguild_v2 import SOURCE
def test_distinct_doi_not_equivalent_to_distinct_sensor_streams():
    assert len(SOURCE)==3
    assert SOURCE["woodcock_gps"]["doi"]==SOURCE["woodcock_argos"]["doi"]
    assert SOURCE["woodcock_gps"]["original_sensor"]=="GPS"
    assert SOURCE["woodcock_argos"]["original_sensor"]=="Argos Doppler Shift"
    assert SOURCE["dabbling_ducks"]["taxon"]=="Anas acuta; Anas platyrhynchos"
    for v in SOURCE.values():
        assert len(v["md5"])==32 and len(v["uuid"])==36 and v["size"]>0
