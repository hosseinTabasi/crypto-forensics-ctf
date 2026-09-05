"""Run the full empirical study per PROTOCOL.md."""

from __future__ import annotations

import json
import platform
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from crypto_forensics import __version__
from crypto_forensics.challenges.catalog import all_challenges
from crypto_forensics.kit_bridge import kit_status
from crypto_forensics.solvers import auto_solve

_ROOT = Path(__file__).resolve().parents[3]
_ARTIFACTS = _ROOT / "artifacts"
_DEFAULT_N = 5


def run_experiment(*, n_runs: int = _DEFAULT_N, artifacts_dir: Path | None = None) -> Path:
    """Execute ``n_runs`` full auto-solve passes and write a JSON artifact.

    Returns the path to the written ``artifacts/run_*.json`` file.
    """
    if n_runs < 1:
        raise ValueError("n_runs must be >= 1")
    out_dir = artifacts_dir or _ARTIFACTS
    out_dir.mkdir(parents=True, exist_ok=True)

    challenges = all_challenges()
    uname = platform.uname()
    # Avoid leaking ephemeral/CI hostnames into published artifacts.
    node_label = "lab-host"
    started = datetime.now(timezone.utc).isoformat()
    runs: list[dict[str, Any]] = []

    for run_idx in range(n_runs):
        per_challenge: list[dict[str, Any]] = []
        run_t0 = time.perf_counter()
        for ch in challenges:
            attempts = 0
            success = False
            answer = ""
            err: str | None = None
            t0 = time.perf_counter()
            try:
                attempts = 1
                answer = auto_solve(ch)
                success = ch.check_answer(answer)
                if not success:
                    err = "answer mismatch"
            except Exception as exc:  # noqa: BLE001 — record failures for metrics
                err = f"{type(exc).__name__}: {exc}"
                success = False
            elapsed_ms = (time.perf_counter() - t0) * 1000.0
            per_challenge.append(
                {
                    "id": ch.id,
                    "category": ch.category,
                    "tier": ch.tier,
                    "points": ch.points,
                    "success": success,
                    "elapsed_ms": round(elapsed_ms, 3),
                    "attempts": attempts,
                    "points_recovered": ch.points if success else 0,
                    "fixture_version": ch.fixture_version,
                    "error": err,
                }
            )
        run_elapsed_ms = (time.perf_counter() - run_t0) * 1000.0
        runs.append(
            {
                "run_index": run_idx,
                "elapsed_ms": round(run_elapsed_ms, 3),
                "challenges": per_challenge,
                "success_count": sum(1 for row in per_challenge if row["success"]),
                "total": len(per_challenge),
            }
        )

    finished = datetime.now(timezone.utc).isoformat()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    artifact_id = f"run_{stamp}_{uuid.uuid4().hex[:8]}"
    payload: dict[str, Any] = {
        "artifact_id": artifact_id,
        "protocol": "PROTOCOL.md",
        "package_version": __version__,
        "n_runs": n_runs,
        "started_utc": started,
        "finished_utc": finished,
        "platform": {
            "system": uname.system,
            "node": node_label,
            "release": uname.release,
            "version": uname.version,
            "machine": uname.machine,
            "processor": uname.processor,
            "python": platform.python_version(),
            "platform": platform.platform(),
        },
        "kit_status": kit_status(),
        "challenge_ids": [c.id for c in challenges],
        "runs": runs,
    }
    path = out_dir / f"{artifact_id}.json"
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    # Also write a stable pointer for report generation
    (out_dir / "latest.json").write_text(json.dumps({"path": str(path)}, indent=2) + "\n")
    return path
