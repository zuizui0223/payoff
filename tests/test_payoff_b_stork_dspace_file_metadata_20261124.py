"""DSpace source-only public item/bundle/bitstream metadata guards."""
import pytest
from scripts import payoff_b_stork_dspace_file_metadata_20261124 as s

ID="79710d0e-d1d6-45fd-90f9-1c6d9be0c46e"
BU="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"


def test_allowlist_excludes_original_event_content_and_unverified_uuid():
    for url in [
        f"/server/api/core/bitstreams/{BU}/content",
        f"/server/api/core/items/{BU}",
        f"/server/api/core/bundles/{BU}/bitstreams",
        "/server/api/core/items",
        f"/server/api/core/items/{ID}/download",
    ]:
        with pytest.raises(ValueError,match="forbidden|Unknown|not one|not recovered"):
            s.get_metadata(url,{ID},set())


def test_public_file_result_never_emits_name_or_bitstream_id():
    entry=s.public_file_entry({
        "uuid":"secret-bird-tag-123",
        "name":"GPS_Secret_Bird_123.csv",
        "sizeBytes":22000,
        "checkSum":{"checkSumAlgorithm":"MD5","value":"secretmd5"},
    })
    assert entry["extension"]==".csv"
    assert entry["name_has_GPS"] is True
    assert entry["size_bytes"]==22000
    assert entry["has_MD5_checksum"] is True
    assert "GPS_Secret_Bird" not in str(entry)
    assert "secretmd5" not in str(entry)
    assert entry["bitstream_content_requested"] is False


def test_parse_hal_bundles_and_bitstreams_without_following_content_links():
    b={"_embedded":{"bundles":[{"name":"ORIGINAL","uuid":BU}]}}
    c={"_embedded":{"bitstreams":[{"name":"tracks.csv","sizeBytes":100}]}}
    assert s.bundle_entries(b)[0]["uuid"]==BU
    assert s.bitstream_entries(c)[0]["name"]=="tracks.csv"
    assert s.bundle_entries({})==[]
    assert s.bitstream_entries({})==[]
