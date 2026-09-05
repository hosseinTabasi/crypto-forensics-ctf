"""Tier A classic-cipher challenges.

**EDUCATIONAL.** Caesar, Vigenère, monoalphabetic substitution, and
single-byte XOR. Never use these constructions for real secrets.
"""

from __future__ import annotations

from typing import Any

from crypto_forensics.challenges.catalog import Challenge, load_fixture, make_challenge


def build_challenges() -> list[Challenge]:
    """Build Tier A classic challenges from frozen fixtures."""
    return [
        _caesar(),
        _vigenere(),
        _mono(),
        _xor(),
    ]


def _caesar() -> Challenge:
    fix: dict[str, Any] = load_fixture("classic_caesar.json")
    return make_challenge(
        id="classic-caesar",
        title="Caesar Shift Recovery",
        category="classic",
        tier="A",
        difficulty="easy",
        points=100,
        description=(
            "A short flag was encrypted with a Caesar (shift) cipher. "
            "Recover the plaintext flag. Non-letters are unchanged.\n\n"
            f"Ciphertext:\n{fix['ciphertext']}"
        ),
        hints=[
            "There are only 26 possible shifts.",
            "English flags often start with FLAG{…}.",
            "Try shift=7.",
        ],
        answer=fix["answer"],
        payload={
            "ciphertext": fix["ciphertext"],
            "fixture": "classic_caesar.json",
            "fixture_version": fix["fixture_version"],
        },
        educational_note=(
            "EDUCATIONAL classic cipher. Brute-force / frequency analysis only. "
            "Not production-safe."
        ),
        solver_name="solve_caesar",
        fixture_version=fix["fixture_version"],
    )


def _vigenere() -> Challenge:
    fix = load_fixture("classic_vigenere.json")
    return make_challenge(
        id="classic-vigenere",
        title="Vigenère with Known Period",
        category="classic",
        tier="A",
        difficulty="easy",
        points=150,
        description=(
            "Vigenère ciphertext with a repeating alphabetic key. "
            f"The period is known to be {fix['known_period']}. "
            "Recover the FLAG{…} substring.\n\n"
            f"Ciphertext:\n{fix['ciphertext']}"
        ),
        hints=[
            "Split letters into period columns and attack each as Caesar.",
            "Score candidates against English letter frequencies.",
            "The key is three letters related to a classroom acronym.",
        ],
        answer=fix["answer"],
        payload={
            "ciphertext": fix["ciphertext"],
            "known_period": fix["known_period"],
            "fixture": "classic_vigenere.json",
            "fixture_version": fix["fixture_version"],
        },
        educational_note=(
            "EDUCATIONAL Vigenère lab. Kasiski / IC methods apply once period leaks. "
            "Not production-safe."
        ),
        solver_name="solve_vigenere",
        fixture_version=fix["fixture_version"],
    )


def _mono() -> Challenge:
    fix = load_fixture("classic_mono.json")
    return make_challenge(
        id="classic-mono",
        title="Monoalphabetic Frequency Puzzle",
        category="classic",
        tier="A",
        difficulty="medium",
        points=200,
        description=(
            "English plaintext was encrypted with a fixed monoalphabetic "
            "substitution (A–Z only; spaces unchanged). Recover the FLAG{…}.\n\n"
            f"Ciphertext:\n{fix['ciphertext']}"
        ),
        hints=[
            "Letter frequencies and common words (THE, FLAG) survive substitution.",
            "A full key alphabet is recoverable from enough English text.",
            "In this lab fixture the key alphabet is a well-known keyboard row permutation.",
        ],
        answer=fix["answer"],
        payload={
            "ciphertext": fix["ciphertext"],
            "fixture": "classic_mono.json",
            "fixture_version": fix["fixture_version"],
        },
        educational_note=(
            "EDUCATIONAL monoalphabetic substitution. Frequency analysis classroom demo."
        ),
        solver_name="solve_mono",
        fixture_version=fix["fixture_version"],
    )


def _xor() -> Challenge:
    fix = load_fixture("classic_xor.json")
    return make_challenge(
        id="classic-xor",
        title="Single-Byte XOR",
        category="classic",
        tier="A",
        difficulty="easy",
        points=100,
        description=(
            "A printable ASCII flag was XOR-encrypted with a single repeating byte. "
            "Ciphertext (hex):\n"
            f"{fix['ciphertext_hex']}"
        ),
        hints=[
            "Brute-force all 256 key bytes.",
            "Prefer candidates that decode to printable ASCII containing FLAG{",
            "The key byte is 0x42.",
        ],
        answer=fix["answer"],
        payload={
            "ciphertext_hex": fix["ciphertext_hex"],
            "fixture": "classic_xor.json",
            "fixture_version": fix["fixture_version"],
        },
        educational_note="EDUCATIONAL single-byte XOR. Trivial brute force.",
        solver_name="solve_xor",
        fixture_version=fix["fixture_version"],
    )
