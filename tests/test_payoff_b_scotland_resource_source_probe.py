"""Offline synthetic fixtures only: provenance/header/ZIP parsing."""
import hashlib
import io
import zipfile

from scripts.payoff_b_scotland_resource_source_probe import (
    inspect_csv_bytes, inspect_zip_bytes, validate_checksum,
)


def test_checksum_verification_real_and_tampered():
    raw = b"caterpillar,site,date\n3,A,2020-05-01\n"
    digest = hashlib.sha256(raw).hexdigest()
    assert validate_checksum(raw, "sha256:" + digest)["verified"] is True
    assert validate_checksum(raw + b"x", "sha256:" + digest)["verified"] is False
    assert validate_checksum(raw, None)["verified"] is False


def test_source_headers_not_effects():
    raw = b"site,year,date,hatch_date,caterpillar_count,mass_g,fledged\nAB,2020,2020-05-01,2020-05-15,3,0.1,5\n"
    result = inspect_csv_bytes(raw)
    assert result["date_like"] == ["year", "date", "hatch_date"]
    assert result["site_like"] == ["site"]
    assert "mass_g" in result["reproduction_or_mass_like"]
    assert result["full_scan"] is True


def test_zip_headers_from_synthetic_source():
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as writer:
        writer.writestr("resource.csv", "site,year,date,biomass\nA,2020,2020-05-02,2\n")
        writer.writestr("README.txt", "synthetic fixture")
    r = inspect_zip_bytes(stream.getvalue())
    assert r["zip_member_count"] == 2
    assert r["zip_members"][0]["csv"]["n_columns"] == 4
