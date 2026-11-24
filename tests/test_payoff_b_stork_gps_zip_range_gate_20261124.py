"""No full GPS ZIP download; 206 with 4KiB cap is mandatory."""
import pytest
from scripts import payoff_b_stork_gps_zip_range_gate_20261124 as s

UUID="aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
URL=s.ROOT+f"/server/api/core/bitstreams/{UUID}/content"
SIZE=289189615


class Response:
    def __init__(self,status,body=None,content_range=None):
        self.status=status
        self.body=body or b""
        self.headers={
           "Content-Range":content_range or "",
           "Content-Length":str(len(self.body)),
           "Accept-Ranges":"bytes"
        }
        self.read_called=False
    def __enter__(self):return self
    def __exit__(self,*exc):return False
    def geturl(self):return URL
    def read(self,n):
        self.read_called=True
        assert n<=4097
        return self.body[:n]


class Opener:
    def __init__(self,r):self.response=r;self.req=None
    def open(self,req,timeout=25):
        self.req=req
        return self.response


def test_select_exact_smallest_public_gps_zip_without_member_download():
    def file(name,size):
        return {"name":name,"sizeBytes":size,"uuid":UUID,
                "checkSum":{"checkSumAlgorithm":"MD5","value":"a"*32},
                "_links":{"content":{"href":URL}}}
    sel=s.select_gps_zip([
       file("SomeTag_ACC.zip",65001733),
       file("2020_GPS_data.zip",350000000),
       file("2019_GPS_data.zip",SIZE),
    ],SIZE)
    assert sel["size_bytes"]==SIZE
    with pytest.raises(ValueError,match="size changed"):
        s.select_gps_zip([file("tag_GPS.zip",30000)],SIZE)


def test_ignored_range_200_does_not_read_one_archive_byte():
    rsp=Response(200,b"X"*5000)
    op=Opener(rsp)
    z=s.request_tiny_range(URL,SIZE,4096,op)
    assert z["status"]=="RANGE_NOT_HONORED"
    assert z["bytes_read"]==0
    assert rsp.read_called is False
    assert op.req.get_header("Range")=="bytes=0-4095"


def test_exact_206_ZIP_header_verifies_small_chunk_only():
    rsp=Response(206,b"PK\x03\x04"+b"Z"*4092,f"bytes 0-4095/{SIZE}")
    z=s.request_tiny_range(URL,SIZE,4096,Opener(rsp))
    assert z["status"]=="ORIGINAL_ZIP_4K_RANGE_VERIFIED"
    assert z["bytes_read"]==4096
    assert z["zip_header_verified"] is True
    assert z["original_full_zip_checksum_verified"] is False
    assert len(z["chunk_sha256"])==64


def test_content_range_wrong_never_reads():
    rsp=Response(206,b"PK\x03\x04"+b"Z"*4092,"bytes 0-8191/100")
    z=s.request_tiny_range(URL,SIZE,4096,Opener(rsp))
    assert z["status"]=="RANGE_RESPONSE_BOUNDS_MISMATCH"
    assert rsp.read_called is False


def test_invalid_zip_magic_does_not_emit_source_bytes():
    rsp=Response(206,b"BAD!"+b"X"*4092,f"bytes 0-4095/{SIZE}")
    z=s.request_tiny_range(URL,SIZE,4096,Opener(rsp))
    assert z["status"]=="ZIP_HEADER_NOT_VERIFIED"
    assert "BAD!" not in str(z)
    assert z["zip_header_verified"] is False
