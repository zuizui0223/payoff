import datetime as dt
import io
import zipfile
import pytest
from src.japan_phenology_smaster_temporal import _dms_tenth_minute, parse_smaster, audit_event_coverage

def record(sid="401", lat="452490", lon="1414070", start="19610101", end="99999999"):
    raw = bytearray(b" " * 146)
    for pos, value in [(0,sid),(36,lat),(42,lon),(64,start),(72,end)]:
        raw[pos:pos+len(value)] = value.encode("ascii")
    return bytes(raw)

def zipped(*records):
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w") as z:
        z.writestr("smaster.index", b"\n".join(records) + b"\n")
    return b.getvalue()

def test_official_degree_minute_conversion_and_period():
    parsed = parse_smaster(zipped(record()))
    assert parsed[0]["lat_degrees"] == pytest.approx(45 + 24.9/60)
    assert parsed[0]["lon_degrees"] == pytest.approx(141 + 40.7/60)
    assert parsed[0]["valid_from"] == dt.date(1961,1,1)
    assert parsed[0]["valid_to"] is None
    assert parsed[0]["coordinate_datum_certified_wgs84"] is False

def test_pre1961_event_is_not_silently_matched():
    m = parse_smaster(zipped(record()))
    e = [{"station_id":"401","event_date":"1953-04-05"},
         {"station_id":"401","event_date":"1970-04-05"}]
    result = audit_event_coverage(e,m)
    assert result["event_match_status"] == {
        "no_metadata_valid_on_event_date":1,
        "unique_temporal_metadata_record":1,
    }
    assert result["environmental_join_admitted"] is False

def test_overlapping_distinct_locations_are_ambiguous():
    m = parse_smaster(zipped(record(end="19801231"),record(lat="452590",start="19750101")))
    out = audit_event_coverage([{"station_id":"401","event_date":"1978-05-01"}],m)
    assert out["event_match_status"]["ambiguous_overlapping_coordinates"] == 1
    assert out["stations_with_multiple_coordinates"] == 1

@pytest.mark.parametrize("bad", [
    record(lat="459990"),record(lon="1416070"),
    record(start="20000101",end="19990101"),record()[:-1],
])
def test_malformed_source_rejected(bad):
    with pytest.raises(ValueError):
        parse_smaster(zipped(bad))
