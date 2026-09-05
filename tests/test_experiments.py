"""Tests for experiment runner / metrics (short N)."""

from __future__ import annotations

import json
from pathlib import Path

from crypto_forensics.experiments.metrics import aggregate_runs, render_results_md
from crypto_forensics.experiments.runner import run_experiment


def test_run_experiment_short(tmp_path: Path) -> None:
    path = run_experiment(n_runs=2, artifacts_dir=tmp_path)
    assert path.exists()
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["n_runs"] == 2
    assert len(data["runs"]) == 2
    assert data["runs"][0]["success_count"] == data["runs"][0]["total"]
    summary = aggregate_runs(data)
    assert summary["overall_success_rate"] == 1.0
    md = render_results_md(summary)
    assert "Empirical Results" in md
    assert "classic-caesar" in md
