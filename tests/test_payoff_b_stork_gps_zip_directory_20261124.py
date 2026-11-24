"""Pure synthetic ZIP EOCD tests; no original GPS member bytes."""
import io
import zipfile

from scripts import payoff_b_stork_gps_zip_directory_20261124 as s


def zipped():
    buf=io.BytesIO()
    with zipfile.ZipFile(buf,"w",compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("PRIVATE_TAG_ABC.csv","timestamp,location-lat\n2019-01-01,10\n")
        z.writestr("README_PRIVATE.txt","GPS metadata")
    return buf.getvalue()


def test_directory_member_structure_without_private_name_or_event_rows():
    raw=zipped()
    result=s.validate_zip_tail(raw,len(raw))
    assert result["status"]=="CENTRAL_DIRECTORY_METADATA_VERIFIED"
    assert result["n_original_archive_members"]==2
    assert result["extension_counts"]=={".csv":1,".txt":1}
    assert result["compression_method_counts"]=={"8":2}
    assert result["member_payloads_decompressed"] is False
    assert result["raw_member_names_exported"] is False
    assert "PRIVATE_TAG_ABC" not in str(result)
    assert "2019-01-01" not in str(result)


def test_zip_without_EOCD_is_source_not_estimated():
    assert s.validate_zip_tail(b"XXXX"*20,9999)["status"]=="END_OF_CENTRAL_DIRECTORY_NOT_VERIFIED"


def test_trailing_junk_or_inconsistent_comment_blocks_directory():
    raw=zipped()
    out=s.validate_zip_tail(raw+b"garbage",len(raw)+7)
    assert out["status"] in {"UNEXPECTED_TRAILING_BYTES_OR_COMMENT",
                             "CENTRAL_DIRECTORY_SIZE_MISMATCH"}


def test_oversize_tail_cap_and_missing_zip_data():
    assert s.validate_zip_tail(b"X"*(s.TAIL_N+1),500000)["status"]=="TAIL_SIZE_UNSUPPORTED"


def test_fixed_tail_only_no_http_200_body_read():
    class FakeResponse:
        status=200
        headers={}
        def __enter__(self):return self
        def __exit__(self,*a):return False
        def geturl(self):return "https://datarepository.movebank.org/content"
        def read(self,n):raise AssertionError("must never read 200 full archive")
    class Opener:
        def open(self,req,timeout):
            assert req.get_header("Range")=="bytes=200000-265556"
            return FakeResponse()
    url="https://datarepository.movebank.org/server/api/core/bitstreams/abcd/content"
    z=s.read_last_bytes(url,265557,s.TAIL_N,Opener())
    assert z["status"]=="TAIL_RANGE_NOT_HONORED"
    assert z["bytes_read"]==0
