#!/usr/bin/env python3
"""Submit frozen AppEEARS task manifests with explicit opt-in network access.

Default behavior is dry-run validation only.

Authentication is read from environment variables only:
- APPEEARS_TOKEN, or
- EARTHDATA_USERNAME + EARTHDATA_PASSWORD.

No credential value is written to the output receipt.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.appeears_client import AppEEARSClient


TERMINAL_STATUSES = {
    "done",
    "error",
    "failed",
    "cancelled",
    "canceled",
}


def load_client_from_environment() -> AppEEARSClient:
    token = os.environ.get("APPEEARS_TOKEN")
    if token:
        return AppEEARSClient(token=token)

    username = os.environ.get("EARTHDATA_USERNAME")
    password = os.environ.get("EARTHDATA_PASSWORD")
    if username and password:
        return AppEEARSClient.login(
            username=username,
            password=password,
        )

    raise SystemExit(
        "AppEEARS submission requires APPEEARS_TOKEN or both "
        "EARTHDATA_USERNAME and EARTHDATA_PASSWORD in the environment"
    )


def select_tasks(
    manifest: dict,
    *,
    task_indices: tuple[int, ...],
    submit_all: bool,
) -> list[dict]:
    rows = manifest.get("tasks")
    if not isinstance(rows, list) or not rows:
        raise SystemExit("manifest contains no tasks")

    if submit_all and task_indices:
        raise SystemExit(
            "--submit-all cannot be combined with --task-index"
        )
    if submit_all:
        return rows
    if not task_indices:
        raise SystemExit(
            "choose at least one --task-index or use --submit-all"
        )

    selected = []
    for index in task_indices:
        if not 0 <= index < len(rows):
            raise SystemExit(
                f"task index {index} outside 0..{len(rows)-1}"
            )
        selected.append(rows[index])
    return selected


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest_json", type=Path)
    parser.add_argument(
        "--submit",
        action="store_true",
        help="explicitly enable authenticated task submission",
    )
    parser.add_argument(
        "--task-index",
        type=int,
        action="append",
        default=[],
        help="zero-based manifest task index; repeatable",
    )
    parser.add_argument(
        "--submit-all",
        action="store_true",
    )
    parser.add_argument(
        "--wait",
        action="store_true",
        help="poll submitted tasks until a terminal status",
    )
    parser.add_argument(
        "--poll-seconds",
        type=float,
        default=20.0,
    )
    parser.add_argument(
        "--max-polls",
        type=int,
        default=180,
    )
    parser.add_argument(
        "--download-dir",
        type=Path,
        help=(
            "download completed task bundles after --wait; "
            "requires --submit and --wait"
        ),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(
            "outputs/appeears_submission_receipt.json"
        ),
    )
    args = parser.parse_args()

    if args.poll_seconds <= 0:
        raise SystemExit("--poll-seconds must be positive")
    if args.max_polls <= 0:
        raise SystemExit("--max-polls must be positive")
    if args.download_dir is not None and (
        not args.submit or not args.wait
    ):
        raise SystemExit(
            "--download-dir requires both --submit and --wait"
        )

    manifest = json.loads(
        args.manifest_json.read_text(encoding="utf-8")
    )
    tasks = select_tasks(
        manifest,
        task_indices=tuple(args.task_index),
        submit_all=args.submit_all,
    )

    receipt = {
        "manifest_source": str(args.manifest_json),
        "manifest_status": manifest.get("status"),
        "reconstruction_lane": manifest.get(
            "reconstruction_lane"
        ),
        "selected_task_count": len(tasks),
        "selected_task_names": [
            row["task"]["task_name"]
            for row in tasks
        ],
        "network_submission_enabled": bool(args.submit),
        "authentication_source": None,
        "submissions": [],
        "credentials_recorded": False,
        "lambda_outcome_opened": False,
    }

    if not args.submit:
        receipt["status"] = "dry_run_no_network_submission"
        receipt["claim_boundary"] = (
            "manifest selection only; no AppEEARS task was submitted"
        )
    else:
        client = load_client_from_environment()
        receipt["authentication_source"] = (
            "APPEEARS_TOKEN"
            if os.environ.get("APPEEARS_TOKEN")
            else "EARTHDATA_USERNAME_PASSWORD"
        )

        for manifest_row in tasks:
            submission = client.submit_task(
                manifest_row["task"]
            )
            row = {
                "task_name": manifest_row["task"][
                    "task_name"
                ],
                "year": manifest_row.get("year"),
                "part": manifest_row.get("part"),
                "cell_count": manifest_row.get(
                    "cell_count"
                ),
                "task_id": submission.task_id,
                "status": "submitted",
                "downloads": [],
            }

            if args.wait:
                status = None
                for _ in range(args.max_polls):
                    status_payload = client.task_status(
                        submission.task_id
                    )
                    status = str(
                        status_payload.get(
                            "status",
                            "unknown",
                        )
                    ).lower()
                    row["status"] = status
                    if status in TERMINAL_STATUSES:
                        break
                    time.sleep(args.poll_seconds)
                else:
                    row["status"] = "poll_limit_reached"

                if (
                    row["status"] == "done"
                    and args.download_dir is not None
                ):
                    task_dir = (
                        args.download_dir
                        / submission.task_id
                    )
                    downloaded = client.download_bundle(
                        submission.task_id,
                        task_dir,
                    )
                    row["downloads"] = [
                        asdict(item)
                        for item in downloaded
                    ]

            receipt["submissions"].append(row)

        terminal = {
            row["status"]
            for row in receipt["submissions"]
        }
        if args.wait:
            receipt["status"] = (
                "submitted_tasks_complete"
                if terminal == {"done"}
                else "submitted_tasks_finished_with_non_done_status"
            )
        else:
            receipt["status"] = "submitted_tasks_not_waited"
        receipt["claim_boundary"] = (
            "authenticated AppEEARS operational receipt; submission/download "
            "status only and not an environmental or lambda result"
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(receipt, indent=2) + "\n",
        encoding="utf-8",
    )

    print(args.output)
    print(
        "appeears_submission "
        f"status={receipt['status']} "
        f"selected={receipt['selected_task_count']} "
        f"network={int(receipt['network_submission_enabled'])} "
        f"credentials_recorded=0"
    )


if __name__ == "__main__":
    main()
