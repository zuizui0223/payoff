from pathlib import Path

import pytest

from src.appeears_client import (
    APPEEARS_API_BASE,
    AppEEARSClient,
)


class FakeResponse:
    def __init__(
        self,
        *,
        payload=None,
        chunks=(),
        status_code=200,
    ):
        self._payload = payload
        self._chunks = tuple(chunks)
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(
                f"HTTP {self.status_code}"
            )

    def json(self):
        return self._payload

    def iter_content(self, chunk_size=1024):
        del chunk_size
        yield from self._chunks


class FakeSession:
    def __init__(self):
        self.calls = []

    def post(
        self,
        url,
        *,
        auth=None,
        json=None,
        headers=None,
        timeout=None,
    ):
        self.calls.append(
            (
                "POST",
                url,
                {
                    "auth": auth,
                    "json": json,
                    "headers": headers,
                    "timeout": timeout,
                },
            )
        )
        if url.endswith("/login"):
            return FakeResponse(
                payload={
                    "token_type": "Bearer",
                    "token": "secret-token",
                }
            )
        if url.endswith("/task"):
            return FakeResponse(
                payload={
                    "task_id": "task-123",
                    "status": "pending",
                },
                status_code=202,
            )
        raise AssertionError(f"unexpected POST {url}")

    def get(
        self,
        url,
        *,
        headers=None,
        timeout=None,
        stream=False,
        allow_redirects=True,
    ):
        self.calls.append(
            (
                "GET",
                url,
                {
                    "headers": headers,
                    "timeout": timeout,
                    "stream": stream,
                    "allow_redirects": allow_redirects,
                },
            )
        )
        if url.endswith("/task/task-123"):
            return FakeResponse(
                payload={
                    "task_id": "task-123",
                    "status": "done",
                }
            )
        if url.endswith("/bundle/task-123"):
            return FakeResponse(
                payload={
                    "files": [
                        {
                            "file_id": "f1",
                            "file_name": "nested/results.csv",
                        },
                        {
                            "file_id": "f2",
                            "file_name": "quality.csv",
                        },
                    ]
                }
            )
        if url.endswith("/bundle/task-123/f1"):
            return FakeResponse(
                chunks=(b"a,b\n", b"1,2\n")
            )
        if url.endswith("/bundle/task-123/f2"):
            return FakeResponse(
                chunks=(b"q\n", b"0\n")
            )
        raise AssertionError(f"unexpected GET {url}")


def test_login_exchanges_credentials_without_exposing_them_in_client():
    session = FakeSession()
    client = AppEEARSClient.login(
        username="earth-user",
        password="earth-password",
        session=session,
    )

    method, url, kwargs = session.calls[0]
    assert method == "POST"
    assert url == APPEEARS_API_BASE + "login"
    assert kwargs["auth"] == (
        "earth-user",
        "earth-password",
    )
    assert client._headers == {
        "Authorization": "Bearer secret-token"
    }
    assert "earth-password" not in repr(client.__dict__)


def test_submit_task_returns_task_id_and_uses_bearer_header():
    session = FakeSession()
    client = AppEEARSClient(
        token="secret-token",
        session=session,
    )
    task = {
        "task_type": "point",
        "task_name": "demo",
        "params": {},
    }
    result = client.submit_task(task)

    assert result.task_id == "task-123"
    assert result.raw_response["status"] == "pending"
    method, url, kwargs = session.calls[-1]
    assert method == "POST"
    assert url == APPEEARS_API_BASE + "task"
    assert kwargs["json"] == task
    assert kwargs["headers"]["Authorization"] == (
        "Bearer secret-token"
    )


def test_task_status_and_bundle_round_trip():
    session = FakeSession()
    client = AppEEARSClient(
        token="secret-token",
        session=session,
    )

    status = client.task_status("task-123")
    bundle = client.bundle("task-123")

    assert status["status"] == "done"
    assert len(bundle["files"]) == 2


def test_download_bundle_writes_safe_basenames(tmp_path: Path):
    session = FakeSession()
    client = AppEEARSClient(
        token="secret-token",
        session=session,
    )

    downloaded = client.download_bundle(
        "task-123",
        tmp_path,
    )

    assert len(downloaded) == 2
    assert downloaded[0].file_name == "nested/results.csv"
    assert Path(downloaded[0].local_path).name == "results.csv"
    assert (
        tmp_path / "results.csv"
    ).read_bytes() == b"a,b\n1,2\n"
    assert (
        tmp_path / "quality.csv"
    ).read_bytes() == b"q\n0\n"
    assert downloaded[0].bytes_written == len(
        b"a,b\n1,2\n"
    )


def test_empty_token_is_rejected():
    with pytest.raises(ValueError):
        AppEEARSClient(token="   ", session=FakeSession())


def test_missing_task_id_is_rejected():
    class BadSession(FakeSession):
        def post(self, url, **kwargs):
            if url.endswith("/task"):
                return FakeResponse(payload={"status": "pending"})
            return super().post(url, **kwargs)

    client = AppEEARSClient(
        token="secret-token",
        session=BadSession(),
    )
    with pytest.raises(RuntimeError, match="task_id"):
        client.submit_task(
            {
                "task_type": "point",
                "task_name": "demo",
                "params": {},
            }
        )
