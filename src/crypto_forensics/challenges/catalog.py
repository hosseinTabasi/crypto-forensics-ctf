"""Challenge catalog: ids, titles, categories, points, hints, checkers.

All solutions are deterministic from frozen fixtures under ``data/challenges/``.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

# Fixture root: package-relative data/challenges (repo layout).
_DATA_DIR = Path(__file__).resolve().parents[3] / "data" / "challenges"


@dataclass(frozen=True)
class Challenge:
    """A single offline forensics challenge.

    Parameters
    ----------
    id:
        Stable challenge identifier (e.g. ``classic-caesar``).
    title:
        Short human title.
    category:
        One of ``classic``, ``rsa``, ``aes-gcm``.
    tier:
        ``A``, ``B``, or ``C``.
    difficulty:
        Qualitative label (easy / medium / hard).
    points:
        Static point value for manual-difficulty scoring.
    description:
        Public briefing (no solution).
    hints:
        Progressive hints (index 0 = gentlest).
    answer:
        Exact expected answer string (lab checker).
    answer_hash:
        SHA-256 hex of the answer (UTF-8) for optional opaque checks.
    payload:
        Public challenge material (ciphertext, keys, transcripts).
    educational_note:
        EDUCATIONAL / SAFE labeling for docs and CLI.
    """

    id: str
    title: str
    category: str
    tier: str
    difficulty: str
    points: int
    description: str
    hints: tuple[str, ...]
    answer: str
    answer_hash: str
    payload: dict[str, Any]
    educational_note: str = (
        "EDUCATIONAL lab challenge. Offline only. Not for production misuse."
    )
    fixture_version: str = "1.0.0"
    solver_name: str = ""

    def check_answer(self, candidate: str) -> bool:
        """Return True if ``candidate`` matches the lab answer exactly."""
        return candidate.strip() == self.answer


def _sha256_hex(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_fixture(name: str) -> dict[str, Any]:
    """Load a frozen JSON fixture from ``data/challenges/``."""
    path = _DATA_DIR / name
    if not path.exists():
        raise FileNotFoundError(f"missing fixture: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def _build_challenges() -> list[Challenge]:
    """Assemble the full catalog from modules + fixtures."""
    from crypto_forensics.challenges import aes_gcm_misuse, classic, rsa_padding

    items: list[Challenge] = []
    items.extend(classic.build_challenges())
    items.extend(rsa_padding.build_challenges())
    items.extend(aes_gcm_misuse.build_challenges())
    return items


_CACHE: list[Challenge] | None = None


def all_challenges() -> list[Challenge]:
    """Return all challenges (cached)."""
    global _CACHE
    if _CACHE is None:
        _CACHE = _build_challenges()
    return list(_CACHE)


def get_challenge(challenge_id: str) -> Challenge:
    """Look up a challenge by id or raise ``KeyError``."""
    for ch in all_challenges():
        if ch.id == challenge_id:
            return ch
    raise KeyError(f"unknown challenge id: {challenge_id}")


def list_challenge_ids() -> list[str]:
    """Return challenge ids in catalog order."""
    return [c.id for c in all_challenges()]


def make_challenge(
    *,
    id: str,
    title: str,
    category: str,
    tier: str,
    difficulty: str,
    points: int,
    description: str,
    hints: list[str] | tuple[str, ...],
    answer: str,
    payload: dict[str, Any],
    educational_note: str,
    solver_name: str,
    fixture_version: str = "1.0.0",
) -> Challenge:
    """Factory that fills ``answer_hash`` consistently."""
    return Challenge(
        id=id,
        title=title,
        category=category,
        tier=tier,
        difficulty=difficulty,
        points=points,
        description=description,
        hints=tuple(hints),
        answer=answer,
        answer_hash=_sha256_hex(answer),
        payload=payload,
        educational_note=educational_note,
        fixture_version=fixture_version,
        solver_name=solver_name,
    )


# Re-export helper for challenge modules.
__all__ = [
    "Challenge",
    "all_challenges",
    "get_challenge",
    "list_challenge_ids",
    "load_fixture",
    "make_challenge",
]
