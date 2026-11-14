import io
import zipfile

import pytest

from scripts.payoff_b_jma_station_metadata_source_probe import audit_station_zip


def test_station_zip_provenance_only():
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w") as z:
        z.writestr("metadata.txt", "station,latitude,longitude\n401,45.4,141.7\n")
    receipt = audit_station_zip(b.getvalue())
    assert receipt["member_count"] == 1
    assert len(receipt["archive_sha256"]) == 64
    assert receipt["files"][0]["format_admitted"] is False
    assert receipt["files"][0]["phenology_station_id_crosswalk_admitted"] is False


def test_invalid_metadata_archive_rejected():
    with pytest.raises(zipfile.BadZipFile):
        audit_station_zip(b"invalid")
