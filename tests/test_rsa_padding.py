"""Tests for Tier B RSA educational challenges."""

from __future__ import annotations

import pytest

from crypto_forensics.challenges.catalog import get_challenge
from crypto_forensics.challenges.rsa_padding import FakeOracle
from crypto_forensics.solvers import auto_solve


def test_rsa_challenges_exist() -> None:
    for cid in ("rsa-tiny", "rsa-stereo", "rsa-pkcs-oracle", "rsa-common-mod"):
        ch = get_challenge(cid)
        assert ch.category == "rsa"
        assert ch.tier == "B"


def test_rsa_tiny() -> None:
    ch = get_challenge("rsa-tiny")
    assert auto_solve(ch) == ch.answer


def test_rsa_stereo() -> None:
    ch = get_challenge("rsa-stereo")
    assert auto_solve(ch) == ch.answer


def test_rsa_pkcs_oracle_fake() -> None:
    ch = get_challenge("rsa-pkcs-oracle")
    oracle = FakeOracle(list(ch.payload["oracle_transcript"]))
    assert oracle.is_padding_valid(1) is True
    assert oracle.is_padding_valid("c0") is False
    with pytest.raises(KeyError):
        oracle.is_padding_valid("nope")
    assert auto_solve(ch) == ch.answer


def test_rsa_common_mod() -> None:
    ch = get_challenge("rsa-common-mod")
    assert auto_solve(ch) == ch.answer
