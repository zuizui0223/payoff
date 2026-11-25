"""Synthetic safety checks only; no ecological outcomes."""
import hashlib, io, json
import openpyxl
import pytest
from scripts import payoff_b_interaction_buffering_small_dryad_gate_20261125 as g

class Response:
    def __init__(self, body, code=200):
        self.body=body
        self.status_code=code
        self.headers={"Content-Length":str(len(body))}
    def __enter__(self): return self
    def __exit__(self,*args): pass
    def iter_content(self,n): yield self.body

class Session:
    def __init__(self, mapping):
        self.mapping=mapping
        self.calls=[]
    def get(self,url,**kwargs):
        self.calls.append(url)
        return self.mapping[url]

def J(o): return Response(json.dumps(o).encode())

def test_exact_manifest_and_digest():
    doi="10.5061/dryad.rm317"
    u=g.BASE+"/datasets/"+g.quote("doi:"+doi,safe="")
    b=b"header\nvalue\n"
    s=Session({u:J({"identifier":"doi:"+doi,"title":"fixture"}),
        u+"/versions":J({"_embedded":{"versions":[{"versionNumber":1,"_links":{"self":{"href":"/api/v2/versions/123"}}}]}}),
        g.BASE+"/versions/123/files":J({"_embedded":{"files":[{"path":"test.csv","size":len(b),"digest":hashlib.sha256(b).hexdigest(),"digestType":"SHA-256","_links":{"self":{"href":"/api/v2/files/456"}}}]}}),
        g.BASE+"/files/456/download":Response(b)})
    m=g.manifest(s,doi)
    assert m["version"]==123
    assert g.verified_bytes(s,m["files"]["test.csv"])==b
    assert g.inspect_schema(b,"test.csv")=={"header":["header"],"nonempty_data_rows":1}

def test_no_bypass_on_401():
    u=g.BASE+"/files/1/download"
    s=Session({u:Response(b"unauthorized",401)})
    with pytest.raises(g.Hold,match="HTTP_401"):
        g.verified_bytes(s,{"file_id":1,"bytes":100,"digest":"0"*64,"digest_type":"sha256"})
    assert s.calls==[u]

def test_digest_mismatch():
    u=g.BASE+"/files/1/download"
    s=Session({u:Response(b"wrong")})
    with pytest.raises(g.Hold,match="DIGEST_MISMATCH"):
        g.verified_bytes(s,{"file_id":1,"bytes":5,"digest":"0"*64,"digest_type":"sha256"})

def test_oversize():
    s=Session({})
    with pytest.raises(g.Hold,match="LIMIT"):
        g.verified_bytes(s,{"file_id":1,"bytes":g.CAP+1,"digest":"0"*64,"digest_type":"sha256"})
    assert not s.calls

def test_xlsx_schema_no_outcomes():
    wb=openpyxl.Workbook()
    wb.active.title="example"
    wb.active.append(["cage","response"])
    wb.active.append(["synthetic-id",42])
    b=io.BytesIO(); wb.save(b)
    got=g.inspect_schema(b.getvalue(),"test.xlsx")
    assert got["sheets"][0]["first_row_text_headers"]==["cage","response"]
    assert "synthetic-id" not in json.dumps(got)
    assert "42" not in json.dumps(got)
