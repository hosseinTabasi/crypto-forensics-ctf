"""Tests for Tier A classic challenges."""

from __future__ import annotations

from crypto_forensics.challenges.catalog import get_challenge
from crypto_forensics.solvers import auto_solve


def test_classic_challenges_exist() -> None:
    for cid in ("classic-caesar", "classic-vigenere", "classic-mono", "classic-xor"):
        ch = get_challenge(cid)
        assert ch.category == "classic"
        assert ch.tier == "A"
        assert ch.answer_hash


def test_caesar_solver() -> None:
    ch = get_challenge("classic-caesar")
    assert auto_solve(ch) == ch.answer


def test_vigenere_solver() -> None:
    ch = get_challenge("classic-vigenere")
    assert auto_solve(ch) == ch.answer


def test_mono_solver() -> None:
    ch = get_challenge("classic-mono")
    assert auto_solve(ch) == ch.answer


def test_xor_solver() -> None:
    ch = get_challenge("classic-xor")
    assert auto_solve(ch) == ch.answer
