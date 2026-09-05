"""Aggregate experiment artifacts and render RESULTS.md."""

from __future__ import annotations

import json
import statistics
from pathlib import Path
from typing import Any

_ROOT = Path(__file__).resolve().parents[3]
_ARTIFACTS = _ROOT / "artifacts"
_RESULTS = _ROOT / "reports" / "RESULTS.md"

# Static manual-difficulty table (points design — not measured timing).
MANUAL_DIFFICULTY = [
    ("classic-caesar", "A", "easy", 100),
    ("classic-vigenere", "A", "easy", 150),
    ("classic-mono", "A", "medium", 200),
    ("classic-xor", "A", "easy", 100),
    ("rsa-tiny", "B", "easy", 150),
    ("rsa-stereo", "B", "medium", 200),
    ("rsa-pkcs-oracle", "B", "medium", 250),
    ("rsa-common-mod", "B", "medium", 200),
    ("gcm-nonce-reuse", "C", "medium", 250),
    ("gcm-forbidden", "C", "easy", 150),
    ("gcm-tag-strip", "C", "easy", 150),
    ("gcm-aad-mismatch", "C", "medium", 200),
]


def load_artifact(path: Path) -> dict[str, Any]:
    """Load a run artifact JSON file."""
    return json.loads(path.read_text(encoding="utf-8"))


def find_artifacts(artifacts_dir: Path | None = None) -> list[Path]:
    """Return sorted ``run_*.json`` artifact paths."""
    d = artifacts_dir or _ARTIFACTS
    return sorted(d.glob("run_*.json"))


def aggregate_runs(artifact: dict[str, Any]) -> dict[str, Any]:
    """Compute per-challenge and overall metrics from one multi-run artifact."""
    runs = artifact["runs"]
    n_runs = len(runs)
    ids = artifact["challenge_ids"]
    per: dict[str, dict[str, Any]] = {}
    for cid in ids:
        times: list[float] = []
        successes = 0
        attempts_list: list[int] = []
        points = 0
        category = ""
        for run in runs:
            row = next(r for r in run["challenges"] if r["id"] == cid)
            times.append(float(row["elapsed_ms"]))
            attempts_list.append(int(row["attempts"]))
            if row["success"]:
                successes += 1
            points = int(row["points"])
            category = str(row["category"])
        per[cid] = {
            "id": cid,
            "category": category,
            "points": points,
            "successes": successes,
            "n_runs": n_runs,
            "success_rate": successes / n_runs if n_runs else 0.0,
            "mean_ms": statistics.mean(times) if times else 0.0,
            "median_ms": statistics.median(times) if times else 0.0,
            "stdev_ms": statistics.stdev(times) if len(times) > 1 else 0.0,
            "min_ms": min(times) if times else 0.0,
            "max_ms": max(times) if times else 0.0,
            "mean_attempts": statistics.mean(attempts_list) if attempts_list else 0.0,
        }

    # Category totals
    categories: dict[str, dict[str, Any]] = {}
    for cid, row in per.items():
        cat = row["category"]
        bucket = categories.setdefault(
            cat,
            {"challenges": 0, "points_available": 0, "mean_success_rate": 0.0, "mean_ms": 0.0},
        )
        bucket["challenges"] += 1
        bucket["points_available"] += row["points"]
        bucket["mean_success_rate"] += row["success_rate"]
        bucket["mean_ms"] += row["mean_ms"]
    for cat, bucket in categories.items():
        n = bucket["challenges"]
        bucket["mean_success_rate"] = bucket["mean_success_rate"] / n if n else 0.0
        bucket["mean_ms"] = bucket["mean_ms"] / n if n else 0.0

    all_times = [row["mean_ms"] for row in per.values()]
    overall_success = (
        sum(row["successes"] for row in per.values()) / (n_runs * len(ids)) if ids and n_runs else 0.0
    )
    points_recovered = sum(
        row["points"] * row["success_rate"] for row in per.values()
    )
    points_available = sum(row["points"] for row in per.values())

    return {
        "n_runs": n_runs,
        "n_challenges": len(ids),
        "overall_success_rate": overall_success,
        "points_available": points_available,
        "points_recovered_expected": points_recovered,
        "mean_solve_ms": statistics.mean(all_times) if all_times else 0.0,
        "median_solve_ms": statistics.median(all_times) if all_times else 0.0,
        "per_challenge": per,
        "categories": categories,
        "platform": artifact.get("platform", {}),
        "kit_status": artifact.get("kit_status", {}),
        "artifact_id": artifact.get("artifact_id", ""),
        "started_utc": artifact.get("started_utc", ""),
        "finished_utc": artifact.get("finished_utc", ""),
        "package_version": artifact.get("package_version", ""),
    }


def render_results_md(summary: dict[str, Any]) -> str:
    """Render RESULTS.md markdown from an aggregate summary (real numbers only)."""
    lines: list[str] = []
    lines.append("# Empirical Results")
    lines.append("")
    lines.append("Author: Hossein Tabasi")
    lines.append("")
    lines.append(
        "This file is generated from measured experiment artifacts. "
        "Do not invent numbers — regenerate via "
        "`python -m crypto_forensics experiment report`."
    )
    lines.append("")
    lines.append("## Run metadata")
    lines.append("")
    lines.append(f"- Artifact id: `{summary['artifact_id']}`")
    lines.append(f"- Package version: `{summary['package_version']}`")
    lines.append(f"- N runs: **{summary['n_runs']}**")
    lines.append(f"- Challenges: **{summary['n_challenges']}**")
    lines.append(f"- Started (UTC): {summary['started_utc']}")
    lines.append(f"- Finished (UTC): {summary['finished_utc']}")
    plat = summary.get("platform") or {}
    lines.append(
        f"- Platform: `{plat.get('platform', 'n/a')}` / Python `{plat.get('python', 'n/a')}`"
    )
    kit = summary.get("kit_status") or {}
    lines.append(
        f"- cryptolab-kit: `{kit.get('cryptolab_kit')}` "
        f"(v{kit.get('cryptolab_kit_version')})"
    )
    lines.append(
        f"- cryptolab-suite: `{kit.get('cryptolab_suite')}` "
        f"(v{kit.get('cryptolab_suite_version')})"
    )
    lines.append("")
    lines.append("## Overall")
    lines.append("")
    lines.append(
        f"- Overall auto-solve success rate: "
        f"**{summary['overall_success_rate'] * 100:.1f}%**"
    )
    lines.append(
        f"- Points available: **{summary['points_available']}**; "
        f"expected recovered (rate-weighted): "
        f"**{summary['points_recovered_expected']:.1f}**"
    )
    lines.append(
        f"- Mean per-challenge solve time (mean of means): "
        f"**{summary['mean_solve_ms']:.3f} ms**"
    )
    lines.append(
        f"- Median per-challenge solve time (median of means): "
        f"**{summary['median_solve_ms']:.3f} ms**"
    )
    lines.append("")
    lines.append("## Per-challenge metrics")
    lines.append("")
    lines.append(
        "| id | category | points | success rate | mean ms | median ms | stdev ms | min ms | max ms |"
    )
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---:|")
    for cid, row in summary["per_challenge"].items():
        lines.append(
            f"| `{cid}` | {row['category']} | {row['points']} | "
            f"{row['success_rate'] * 100:.1f}% | "
            f"{row['mean_ms']:.3f} | {row['median_ms']:.3f} | "
            f"{row['stdev_ms']:.3f} | {row['min_ms']:.3f} | {row['max_ms']:.3f} |"
        )
    lines.append("")
    lines.append("## Category totals")
    lines.append("")
    lines.append("| category | challenges | points available | mean success rate | mean ms |")
    lines.append("|---|---:|---:|---:|---:|")
    for cat, bucket in summary["categories"].items():
        lines.append(
            f"| {cat} | {bucket['challenges']} | {bucket['points_available']} | "
            f"{bucket['mean_success_rate'] * 100:.1f}% | {bucket['mean_ms']:.3f} |"
        )
    lines.append("")
    lines.append("## Manual difficulty (static design table)")
    lines.append("")
    lines.append(
        "Point values and qualitative difficulty are design-time constants "
        "(not measured). Timing and success rates above are measured."
    )
    lines.append("")
    lines.append("| id | tier | difficulty | points |")
    lines.append("|---|---|---|---:|")
    for cid, tier, diff, pts in MANUAL_DIFFICULTY:
        lines.append(f"| `{cid}` | {tier} | {diff} | {pts} |")
    lines.append("")
    return "\n".join(lines) + "\n"


def write_results_md(
    artifact_path: Path | None = None,
    *,
    results_path: Path | None = None,
) -> Path:
    """Load latest (or given) artifact, aggregate, write RESULTS.md."""
    if artifact_path is None:
        arts = find_artifacts()
        if not arts:
            raise FileNotFoundError("no artifacts/run_*.json found; run experiment first")
        artifact_path = arts[-1]
    summary = aggregate_runs(load_artifact(artifact_path))
    text = render_results_md(summary)
    dest = results_path or _RESULTS
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8")
    return dest
