"""Tests for Tier C AES-GCM misuse challenges."""

from __future__ import annotations

from crypto_forensics.challenges.catalog import get_challenge
from crypto_forensics.solvers import auto_solve


def test_gcm_challenges_exist() -> None:
    for cid in (
        "gcm-nonce-reuse",
        "gcm-forbidden",
        "gcm-tag-strip",
        "gcm-aad-mismatch",
    ):
        ch = get_challenge(cid)
        assert ch.category == "aes-gcm"
        assert ch.tier == "C"


def test_gcm_nonce_reuse() -> None:
    ch = get_challenge("gcm-nonce-reuse")
    assert auto_solve(ch) == ch.answer


def test_gcm_forbidden() -> None:
    ch = get_challenge("gcm-forbidden")
    assert auto_solve(ch) == ch.answer


def test_gcm_tag_strip() -> None:
    ch = get_challenge("gcm-tag-strip")
    assert auto_solve(ch) == ch.answer


def test_gcm_aad_mismatch() -> None:
    ch = get_challenge("gcm-aad-mismatch")
    assert auto_solve(ch) == ch.answer
