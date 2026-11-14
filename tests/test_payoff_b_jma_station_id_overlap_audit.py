import io
import zipfile

from scripts.payoff_b_jma_station_id_overlap_audit import compare_station_ids


def test_real_schema_id_overlap_not_promoted_to_coordinate_crosswalk():
    p = io.BytesIO()
    with zipfile.ZipFile(p, "w") as z:
        z.writestr("ruinenchi_all/001.csv", "1,うめ開花\n番号,地点名,1953,rm\n401,稚内,405,6\n402,札幌,406,6\n".encode("cp932"))
    m = io.BytesIO()
    with zipfile.ZipFile(m, "w") as z:
        z.writestr("smaster.index", ("401 18343       ﾜﾂｶﾅｲ   WAKKANAI    4524901414070        32    11961010119651231\n" +
                                    "403 18343       ﾄｳｷﾖｳ   TOKYO       3524901394070        32    11961010119651231\n").encode("cp932"))
    out = compare_station_ids(p.getvalue(), m.getvalue())
    assert out["phenology_station_ids"] == 2
    assert out["metadata_station_ids"] == 2
    assert out["overlap_station_ids"] == 1
    assert out["phenology_unmatched_ids"] == ["402"]
    assert out["coordinates_certified"] is False
    assert out["environmental_join_admitted"] is False
