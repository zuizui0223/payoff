"""Minimal authenticated AppEEARS client for frozen request manifests.

Network access is opt-in. Credentials are never serialized by this module.

Authentication:
- use an existing AppEEARS bearer token; or
- exchange NASA Earthdata Login username/password at /api/login.

Official API flow:
    POST /api/login
    POST /api/task
    GET  /api/task/{task_id}
    GET  /api/bundle/{task_id}
    GET  /api/bundle/{task_id}/{file_id}

The requests dependency is loaded lazily through the optional earthdata group.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


APPEEARS_API_BASE = "https://appeears.earthdatacloud.nasa.gov/api/"


def _requests_module():
    try:
        import requests
    except ImportError as exc:
        raise RuntimeError(
            "AppEEARS network operations require the optional earthdata "
            "dependency group"
        ) from exc
    return requests


@dataclass(frozen=True)
class AppEEARSTaskSubmission:
    task_id: str
    raw_response: dict[str, Any]


@dataclass(frozen=True)
class AppEEARSDownloadedFile:
    file_id: str
    file_name: str
    local_path: str
    bytes_written: int


class AppEEARSClient:
    def __init__(
        self,
        *,
        token: str,
        api_base: str = APPEEARS_API_BASE,
        session=None,
        timeout_seconds: float = 120.0,
    ) -> None:
        if not token.strip():
            raise ValueError("token must be non-empty")
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        self._token = token.strip()
        self.api_base = api_base.rstrip("/") + "/"
        self.timeout_seconds = timeout_seconds
        if session is None:
            self._session = _requests_module().Session()
        else:
            self._session = session

    @classmethod
    def login(
        cls,
        *,
        username: str,
        password: str,
        api_base: str = APPEEARS_API_BASE,
        session=None,
        timeout_seconds: float = 120.0,
    ) -> "AppEEARSClient":
        """Exchange Earthdata Login credentials for an AppEEARS bearer token."""

        if not username:
            raise ValueError("username must be non-empty")
        if not password:
            raise ValueError("password must be non-empty")
        requests = _requests_module()
        active_session = session or requests.Session()
        url = api_base.rstrip("/") + "/login"
        response = active_session.post(
            url,
            auth=(username, password),
            timeout=timeout_seconds,
        )
        response.raise_for_status()
        payload = response.json()
        token = payload.get("token")
        if not token:
            raise RuntimeError(
                "AppEEARS login response did not include a bearer token"
            )
        return cls(
            token=str(token),
            api_base=api_base,
            session=active_session,
            timeout_seconds=timeout_seconds,
        )

    @property
    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._token}",
        }

    def submit_task(
        self,
        task: dict[str, Any],
    ) -> AppEEARSTaskSubmission:
        response = self._session.post(
            self.api_base + "task",
            json=task,
            headers=self._headers,
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        payload = response.json()
        task_id = payload.get("task_id")
        if not task_id:
            raise RuntimeError(
                "AppEEARS task submission returned no task_id"
            )
        return AppEEARSTaskSubmission(
            task_id=str(task_id),
            raw_response=dict(payload),
        )

    def task_status(
        self,
        task_id: str,
    ) -> dict[str, Any]:
        if not task_id.strip():
            raise ValueError("task_id must be non-empty")
        response = self._session.get(
            self.api_base + f"task/{task_id}",
            headers=self._headers,
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, dict):
            raise RuntimeError(
                "AppEEARS task status response is not a JSON object"
            )
        return dict(payload)

    def bundle(
        self,
        task_id: str,
    ) -> dict[str, Any]:
        if not task_id.strip():
            raise ValueError("task_id must be non-empty")
        response = self._session.get(
            self.api_base + f"bundle/{task_id}",
            headers=self._headers,
            timeout=self.timeout_seconds,
        )
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, dict):
            raise RuntimeError(
                "AppEEARS bundle response is not a JSON object"
            )
        return dict(payload)

    def download_bundle(
        self,
        task_id: str,
        destination: Path,
    ) -> tuple[AppEEARSDownloadedFile, ...]:
        """Download every file listed by the completed task bundle."""

        bundle = self.bundle(task_id)
        files = bundle.get("files")
        if not isinstance(files, list):
            raise RuntimeError(
                "AppEEARS bundle response has no files list"
            )
        destination.mkdir(
            parents=True,
            exist_ok=True,
        )

        downloaded: list[AppEEARSDownloadedFile] = []
        for row in files:
            if not isinstance(row, dict):
                raise RuntimeError(
                    "AppEEARS bundle file record is not an object"
                )
            file_id = row.get("file_id")
            file_name = row.get("file_name")
            if not file_id or not file_name:
                raise RuntimeError(
                    "AppEEARS bundle file is missing file_id or file_name"
                )
            # Some AppEEARS names include a product subdirectory. Preserve
            # only the basename in the declared destination.
            safe_name = Path(str(file_name)).name
            target = destination / safe_name

            response = self._session.get(
                self.api_base
                + f"bundle/{task_id}/{file_id}",
                headers=self._headers,
                timeout=self.timeout_seconds,
                stream=True,
                allow_redirects=True,
            )
            response.raise_for_status()

            bytes_written = 0
            with target.open("wb") as handle:
                for chunk in response.iter_content(
                    chunk_size=1024 * 1024
                ):
                    if not chunk:
                        continue
                    handle.write(chunk)
                    bytes_written += len(chunk)

            downloaded.append(
                AppEEARSDownloadedFile(
                    file_id=str(file_id),
                    file_name=str(file_name),
                    local_path=str(target),
                    bytes_written=bytes_written,
                )
            )

        return tuple(downloaded)
