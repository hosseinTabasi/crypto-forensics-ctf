"""Tier C AES-GCM misuse challenges (local lab only).

**EDUCATIONAL.** Nonce reuse, forbidden (key, nonce) pairs, missing-tag
rejection, and AAD mismatch forensics. Demonstrates why AES-GCM must be
used correctly. SAFE path: unique nonces, full tags, bound AAD, via the
``cryptography`` AESGCM API (cryptolab-kit modern.aes_gcm).
"""

from __future__ import annotations

from crypto_forensics.challenges.catalog import Challenge, load_fixture, make_challenge


def build_challenges() -> list[Challenge]:
    """Build Tier C AES-GCM misuse challenges from frozen fixtures."""
    return [
        _nonce_reuse(),
        _forbidden(),
        _tag_strip(),
        _aad_mismatch(),
    ]


def _nonce_reuse() -> Challenge:
    fix = load_fixture("gcm_nonce_reuse.json")
    return make_challenge(
        id="gcm-nonce-reuse",
        title="AES-GCM Nonce Reuse XOR Recovery",
        category="aes-gcm",
        tier="C",
        difficulty="medium",
        points=250,
        description=(
            "Two AES-GCM ciphertexts were produced with the SAME key and nonce "
            "(lab misuse). You are given P1 and both ciphertext||tag blobs. "
            "Recover P2 using C1 XOR C2 = P1 XOR P2 on the ciphertext portions "
            "(excluding the 16-byte tags).\n\n"
            f"nonce = {fix['nonce_hex']}\n"
            f"P1 (hex) = {fix['known_plaintext1_hex']}\n"
            f"C1||T1 = {fix['ciphertext1_hex']}\n"
            f"C2||T2 = {fix['ciphertext2_hex']}"
        ),
        hints=[
            "Strip the last 16 bytes (tag) before XORing ciphertexts.",
            "P2 = P1 XOR C1 XOR C2.",
            "The recovered plaintext is an ASCII FLAG{…}.",
        ],
        answer=fix["answer"],
        payload={
            "nonce_hex": fix["nonce_hex"],
            "known_plaintext1_hex": fix["known_plaintext1_hex"],
            "ciphertext1_hex": fix["ciphertext1_hex"],
            "ciphertext2_hex": fix["ciphertext2_hex"],
            # key is lab-only; included so SAFE decrypt demos can verify
            "key_hex": fix["key_hex"],
            "fixture": "gcm_nonce_reuse.json",
            "fixture_version": fix["fixture_version"],
        },
        educational_note=(
            "EDUCATIONAL nonce-reuse demo (local fixtures only). "
            "SAFE path: never reuse (key, nonce); use random 96-bit nonces."
        ),
        solver_name="solve_gcm_nonce_reuse",
        fixture_version=fix["fixture_version"],
    )


def _forbidden() -> Challenge:
    fix = load_fixture("gcm_forbidden.json")
    return make_challenge(
        id="gcm-forbidden",
        title="Forbidden Key/Nonce Pair Detection",
        category="aes-gcm",
        tier="C",
        difficulty="easy",
        points=150,
        description=(
            "NIST SP 800-38D forbids repeating a (key, nonce) pair under GCM. "
            "Inspect the record list and identify the colliding pair. "
            "Submit FLAG{FORBIDDEN_PAIR_<idA>_<idB>} with ids in ascending "
            "lexicographic order.\n\n"
            f"Records: {fix['records']}"
        ),
        hints=[
            "Group records by (key_id, nonce_hex).",
            "Exactly one pair collides in this fixture.",
            "Ids are rec1 and rec3.",
        ],
        answer=fix["answer"],
        payload={
            "records": fix["records"],
            "fixture": "gcm_forbidden.json",
            "fixture_version": fix["fixture_version"],
        },
        educational_note=(
            "EDUCATIONAL forensic detection of forbidden GCM parameter reuse."
        ),
        solver_name="solve_gcm_forbidden",
        fixture_version=fix["fixture_version"],
    )


def _tag_strip() -> Challenge:
    fix = load_fixture("gcm_tag_strip.json")
    return make_challenge(
        id="gcm-tag-strip",
        title="Missing Tag Rejection",
        category="aes-gcm",
        tier="C",
        difficulty="easy",
        points=150,
        description=(
            "An AES-GCM ciphertext had its authentication tag stripped. "
            "Demonstrate that decryption/authentication must reject the "
            "truncated blob, then submit FLAG{TAG_REQUIRED_REJECT}.\n\n"
            f"nonce = {fix['nonce_hex']}\n"
            f"ct||tag = {fix['ciphertext_with_tag_hex']}\n"
            f"ct (stripped) = {fix['ciphertext_stripped_hex']}"
        ),
        hints=[
            "AESGCM.decrypt requires ciphertext||tag.",
            "A blob shorter than plaintext+16 cannot authenticate.",
            "Compare behavior of full vs stripped ciphertext.",
        ],
        answer=fix["answer"],
        payload={
            "key_hex": fix["key_hex"],
            "nonce_hex": fix["nonce_hex"],
            "ciphertext_with_tag_hex": fix["ciphertext_with_tag_hex"],
            "ciphertext_stripped_hex": fix["ciphertext_stripped_hex"],
            "fixture": "gcm_tag_strip.json",
            "fixture_version": fix["fixture_version"],
        },
        educational_note=(
            "EDUCATIONAL missing-tag rejection demo. "
            "SAFE path: always verify the full GCM tag."
        ),
        solver_name="solve_gcm_tag_strip",
        fixture_version=fix["fixture_version"],
    )


def _aad_mismatch() -> Challenge:
    fix = load_fixture("gcm_aad_mismatch.json")
    return make_challenge(
        id="gcm-aad-mismatch",
        title="AAD Mismatch Forensic",
        category="aes-gcm",
        tier="C",
        difficulty="medium",
        points=200,
        description=(
            "Ciphertext was sealed with associated data (AAD). Wrong AAD yields "
            "InvalidTag; correct AAD recovers the plaintext FLAG.\n\n"
            f"nonce = {fix['nonce_hex']}\n"
            f"ct||tag = {fix['ciphertext_with_tag_hex']}\n"
            f"aad_correct (hex) = {fix['aad_correct_hex']}\n"
            f"aad_wrong (hex) = {fix['aad_wrong_hex']}"
        ),
        hints=[
            "Try decrypting with the wrong AAD first — expect authentication failure.",
            "Decrypt with the correct AAD to recover the flag.",
            "AAD binds headers without encrypting them.",
        ],
        answer=fix["answer"],
        payload={
            "key_hex": fix["key_hex"],
            "nonce_hex": fix["nonce_hex"],
            "ciphertext_with_tag_hex": fix["ciphertext_with_tag_hex"],
            "aad_correct_hex": fix["aad_correct_hex"],
            "aad_wrong_hex": fix["aad_wrong_hex"],
            "fixture": "gcm_aad_mismatch.json",
            "fixture_version": fix["fixture_version"],
        },
        educational_note=(
            "EDUCATIONAL AAD mismatch forensic. "
            "SAFE path: bind critical headers as AAD and verify on decrypt."
        ),
        solver_name="solve_gcm_aad_mismatch",
        fixture_version=fix["fixture_version"],
    )
