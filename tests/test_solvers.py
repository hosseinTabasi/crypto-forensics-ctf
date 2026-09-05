"""Cross-cutting solver registry tests."""

from __future__ import annotations

from crypto_forensics.challenges.catalog import all_challenges
from crypto_forensics.solvers import auto_solve, get_solver


def test_every_challenge_has_solver() -> None:
    for ch in all_challenges():
        assert ch.solver_name
        fn = get_solver(ch.solver_name)
        assert callable(fn)


def test_all_auto_solve() -> None:
    for ch in all_challenges():
        assert ch.check_answer(auto_solve(ch))


def test_catalog_minimum_size() -> None:
    rows = all_challenges()
    assert len(rows) >= 12
    assert sum(1 for c in rows if c.tier == "A") >= 4
    assert sum(1 for c in rows if c.tier == "B") >= 4
    assert sum(1 for c in rows if c.tier == "C") >= 4
