"""Solvers for Tier C AES-GCM misuse challenges (local fixtures only)."""

from __future__ import annotations

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from crypto_forensics.challenges.catalog import Challenge

_TAG_LEN = 16


def solve_gcm_nonce_reuse(challenge: Challenge) -> str:
    """Recover P2 from nonce-reuse via ciphertext XOR with known P1."""
    p1 = bytes.fromhex(str(challenge.payload["known_plaintext1_hex"]))
    ct1 = bytes.fromhex(str(challenge.payload["ciphertext1_hex"]))
    ct2 = bytes.fromhex(str(challenge.payload["ciphertext2_hex"]))
    c1, c2 = ct1[:-_TAG_LEN], ct2[:-_TAG_LEN]
    if len(c1) != len(c2) or len(c1) != len(p1):
        raise ValueError("length mismatch in nonce-reuse fixture")
    p2 = bytes(a ^ b ^ c for a, b, c in zip(p1, c1, c2))
    return p2.decode("ascii")


def solve_gcm_forbidden(challenge: Challenge) -> str:
    """Find the colliding (key_id, nonce) record pair."""
    records = list(challenge.payload["records"])
    seen: dict[tuple[str, str], str] = {}
    for row in records:
        key = (str(row["key_id"]), str(row["nonce_hex"]))
        rid = str(row["id"])
        if key in seen:
            a, b = sorted([seen[key], rid])
            return f"FLAG{{FORBIDDEN_PAIR_{a}_{b}}}"
        seen[key] = rid
    raise ValueError("no forbidden pair found")


def solve_gcm_tag_strip(challenge: Challenge) -> str:
    """Confirm stripped tag fails and full blob authenticates; return lab flag."""
    key = bytes.fromhex(str(challenge.payload["key_hex"]))
    nonce = bytes.fromhex(str(challenge.payload["nonce_hex"]))
    full = bytes.fromhex(str(challenge.payload["ciphertext_with_tag_hex"]))
    stripped = bytes.fromhex(str(challenge.payload["ciphertext_stripped_hex"]))
    aes = AESGCM(key)
    # Full ciphertext must decrypt
    _ = aes.decrypt(nonce, full, None)
    # Stripped must fail (too short / bad tag)
    rejected = False
    try:
        aes.decrypt(nonce, stripped, None)
    except (InvalidTag, ValueError, Exception):
        rejected = True
    if not rejected:
        raise ValueError("stripped ciphertext unexpectedly accepted")
    return "FLAG{TAG_REQUIRED_REJECT}"


def solve_gcm_aad_mismatch(challenge: Challenge) -> str:
    """Wrong AAD fails; correct AAD recovers plaintext flag."""
    key = bytes.fromhex(str(challenge.payload["key_hex"]))
    nonce = bytes.fromhex(str(challenge.payload["nonce_hex"]))
    ct = bytes.fromhex(str(challenge.payload["ciphertext_with_tag_hex"]))
    aad_ok = bytes.fromhex(str(challenge.payload["aad_correct_hex"]))
    aad_bad = bytes.fromhex(str(challenge.payload["aad_wrong_hex"]))
    aes = AESGCM(key)
    try:
        aes.decrypt(nonce, ct, aad_bad)
        raise ValueError("wrong AAD unexpectedly accepted")
    except InvalidTag:
        pass
    plain = aes.decrypt(nonce, ct, aad_ok)
    return plain.decode("ascii")
