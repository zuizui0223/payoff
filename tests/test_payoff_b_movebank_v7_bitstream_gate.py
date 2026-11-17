"""Offline GPS source digest, ID/time/coordinate contract fixtures."""
import hashlib
from scripts.payoff_b_movebank_v7_bitstream_gate import (
    checksum_compare,inspect_table
)


def test_dspace_official_hash_required():
    b=b"GMT,individual-local-identifier,location-lat,location-long\n2020,GOOSE,58,11\n"
    good={"checkSumAlgorithm":"MD5","value":hashlib.md5(b).hexdigest()}
    assert checksum_compare(b,good)["source_verified"] is True
    assert checksum_compare(b+b"tampered",good)["source_verified"] is False
    assert checksum_compare(b,None)["source_verified"] is False


def test_telemetry_id_and_location_are_not_an_outcome():
    csv=(b"individual-local-identifier,timestamp,location-lat,location-long\n"
        b"B1,2009-04-01T09:00:00Z,63.2,8.1\n")
    x=inspect_table(csv,"goose.csv")
    assert x["n_rows_scanned"]==1
    assert "timestamp" in x["date_columns"]
    assert len(x["coordinate_columns"])==2
    assert x["no_migration_stops_fitted"] is True
