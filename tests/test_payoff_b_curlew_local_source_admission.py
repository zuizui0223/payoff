"""Original Curlew source local read: exact SHA ZIP or CSV provenance hold."""
import hashlib
import zipfile
import pytest

pytest.importorskip("requests")
from scripts.payoff_b_curlew_local_source_admission import (
    TARGET_CSV,
    PUBLISHED_ZIP_NAME,
    offline_original_source,
)


def valid_csv():
    return (
        "ID_seas;Bird_ID;Sex;Non_gr;Br_gr;Nest_succ;Dist;Prebr;st_grass;st_wetland\n"
        "A_2019;A;F;ATL-S;NE;0;1100;10;0.2;0.3\n"
        "A_2020;A;F;ATL-S;NE;1;1100;14;0.5;0.3\n"
    ).encode()


def test_extracted_csv_reports_only_unknown_source_origin(tmp_path):
    p=tmp_path/TARGET_CSV
    p.write_bytes(valid_csv())
    out=offline_original_source(p)
    assert out["source_original_zip_sha256_verified"] is False
    assert "NOT_INDEPENDENTLY_HASH_VERIFIED" in out["source_provenance_status"]
    assert out["verified_source_semantics"]["n_unique_Bird_ID"]==1
    assert out["verified_source_semantics"]["n_birds_with_two_or_more_distinct_season_IDs"]==1
    assert "A_2019" not in str(out)
    assert out["actual_original_cue_and_observability_available"] is False
    assert out["new_biological_fit_performed"] is False


def test_exact_original_zip_digest_and_size_guard_using_synthetic_source(tmp_path):
    p=tmp_path/PUBLISHED_ZIP_NAME
    with zipfile.ZipFile(p,"w") as z:
        z.writestr("data/"+TARGET_CSV,valid_csv())
    raw=p.read_bytes()
    out=offline_original_source(
        p,expected_zip_size=len(raw),
        expected_zip_sha256=hashlib.sha256(raw).hexdigest()
    )
    assert out["source_original_zip_sha256_verified"] is True
    assert out["source_original_zip_sha256"]==hashlib.sha256(raw).hexdigest()
    assert out["verified_source_semantics"]["n_original_derived_rows"]==2
    with pytest.raises(ValueError,match="size mismatched"):
        offline_original_source(p,expected_zip_size=len(raw)+1,
                                expected_zip_sha256=hashlib.sha256(raw).hexdigest())
    with pytest.raises(ValueError,match="SHA256 mismatched"):
        offline_original_source(p,expected_zip_size=len(raw),
                                expected_zip_sha256="0"*64)


def test_no_forged_source_filename(tmp_path):
    p=tmp_path/"random_migration_data.csv"
    p.write_bytes(valid_csv())
    with pytest.raises(ValueError,match="Only exact"):
        offline_original_source(p)
