"""Tier B RSA padding / textbook footgun challenges (offline).

**EDUCATIONAL.** Tiny moduli, stereotyped small-e recovery, a FakeOracle
PKCS#1 v1.5 padding-oracle SIMULATION (canned transcript only — no network),
and a common-modulus demo. Not production-safe. For real RSA use OAEP/PSS
via the ``cryptography`` package (see cryptolab-kit modern.rsa).
"""

from __future__ import annotations

from typing import Any

from crypto_forensics.challenges.catalog import Challenge, load_fixture, make_challenge


class FakeOracle:
    """Offline PKCS#1 v1.5 padding-oracle SIMULATION.

    Answers only from a canned transcript. There is no network listener and
    no live decryption service. Querying unknown labels raises ``KeyError``.

    **EDUCATIONAL — not a real exploit toolkit.**
    """

    def __init__(self, transcript: list[dict[str, Any]]) -> None:
        self._by_id = {int(row["query_id"]): bool(row["padding_valid"]) for row in transcript}
        self._by_label = {
            str(row["ciphertext_label"]): bool(row["padding_valid"]) for row in transcript
        }
        self.queries: list[str | int] = []

    def is_padding_valid(self, query: str | int) -> bool:
        """Return whether the canned transcript marks ``query`` as valid padding."""
        self.queries.append(query)
        if isinstance(query, int):
            if query not in self._by_id:
                raise KeyError(f"unknown oracle query_id: {query}")
            return self._by_id[query]
        if query not in self._by_label:
            raise KeyError(f"unknown oracle ciphertext_label: {query}")
        return self._by_label[query]


def build_challenges() -> list[Challenge]:
    """Build Tier B RSA challenges from frozen fixtures."""
    return [
        _tiny(),
        _stereo(),
        _pkcs_oracle(),
        _common_mod(),
    ]


def _tiny() -> Challenge:
    fix = load_fixture("rsa_tiny.json")
    return make_challenge(
        id="rsa-tiny",
        title="Tiny Textbook RSA Decrypt",
        category="rsa",
        tier="B",
        difficulty="easy",
        points=150,
        description=(
            "Textbook RSA (no padding) with a tiny modulus. Factor n, recover d, "
            "decrypt the ciphertext integer, then submit "
            "FLAG{RSA_TINY_<plaintext_int>}.\n\n"
            f"n = {fix['n']}\ne = {fix['e']}\nc = {fix['ciphertext']}"
        ),
        hints=[
            "n is small enough for trial division.",
            "Compute φ(n)=(p-1)(q-1), then d = e^{-1} mod φ(n).",
            "Plaintext integer is 1337.",
        ],
        answer=fix["answer"],
        payload={
            "n": fix["n"],
            "e": fix["e"],
            "ciphertext": fix["ciphertext"],
            "fixture": "rsa_tiny.json",
            "fixture_version": fix["fixture_version"],
        },
        educational_note=(
            "EDUCATIONAL textbook RSA on a toy modulus. "
            "SAFE path: RSA-OAEP with >=2048-bit keys via cryptography/cryptolab-kit."
        ),
        solver_name="solve_rsa_tiny",
        fixture_version=fix["fixture_version"],
    )


def _stereo() -> Challenge:
    fix = load_fixture("rsa_stereo.json")
    return make_challenge(
        id="rsa-stereo",
        title="Small-e Stereotyped Plaintext",
        category="rsa",
        tier="B",
        difficulty="medium",
        points=200,
        description=(
            "Unpadded RSA with e=3 where m^e < n, so c = m^e over the integers. "
            "Recover m via integer cube root, then submit FLAG{STEREO_CUBE_ROOT}.\n\n"
            f"n = {fix['n']}\ne = {fix['e']}\nc = {fix['ciphertext']}\n"
            f"Hint text: {fix.get('stereotype_hint', '')}"
        ),
        hints=[
            "When m^e < n, modular reduction never happens.",
            "Take the integer e-th root of c.",
            "m is a small two-digit integer in this fixture.",
        ],
        answer=fix["answer"],
        payload={
            "n": fix["n"],
            "e": fix["e"],
            "ciphertext": fix["ciphertext"],
            "fixture": "rsa_stereo.json",
            "fixture_version": fix["fixture_version"],
        },
        educational_note=(
            "EDUCATIONAL small-e / stereotyped plaintext demo. "
            "SAFE path: always use OAEP (or equivalent) padding."
        ),
        solver_name="solve_rsa_stereo",
        fixture_version=fix["fixture_version"],
    )


def _pkcs_oracle() -> Challenge:
    fix = load_fixture("rsa_pkcs_oracle.json")
    return make_challenge(
        id="rsa-pkcs-oracle",
        title="PKCS#1 v1.5 Oracle Simulation (Offline)",
        category="rsa",
        tier="B",
        difficulty="medium",
        points=250,
        description=(
            "Offline SIMULATION of a PKCS#1 v1.5 padding oracle. "
            "A FakeOracle class answers only from a canned transcript "
            "(no network). Walk the success query path and recover the message.\n\n"
            f"Public n={fix['n']}, e={fix['e']}.\n"
            f"Transcript entries: {len(fix['oracle_transcript'])}.\n"
            f"Success query ids (lab): {fix['success_query_ids']}."
        ),
        hints=[
            "Instantiate FakeOracle with the transcript from the fixture.",
            "Only queries marked padding_valid=True on the success path matter.",
            "The recovered message bytes are in recovered_message_hex once the path validates.",
        ],
        answer=fix["answer"],
        payload={
            "n": fix["n"],
            "e": fix["e"],
            "oracle_transcript": fix["oracle_transcript"],
            "success_query_ids": fix["success_query_ids"],
            "recovered_message_hex": fix["recovered_message_hex"],
            "fixture": "rsa_pkcs_oracle.json",
            "fixture_version": fix["fixture_version"],
        },
        educational_note=(
            "EDUCATIONAL offline padding-oracle SIMULATION with canned responses. "
            "Not a network attack and not a general Bleichenbacher toolkit. "
            "SAFE path: RSA-OAEP; never expose raw PKCS#1 v1.5 decryption errors."
        ),
        solver_name="solve_rsa_pkcs_oracle",
        fixture_version=fix["fixture_version"],
    )


def _common_mod() -> Challenge:
    fix = load_fixture("rsa_common_mod.json")
    return make_challenge(
        id="rsa-common-mod",
        title="Common Modulus Related Messages",
        category="rsa",
        tier="B",
        difficulty="medium",
        points=200,
        description=(
            "The same message m was encrypted under the same n with two coprime "
            "public exponents. Recover m and submit FLAG{COMMON_MODULUS_<m>}.\n\n"
            f"n = {fix['n']}\n"
            f"e_a = {fix['e_a']}, c_a = {fix['c_a']}\n"
            f"e_b = {fix['e_b']}, c_b = {fix['c_b']}"
        ),
        hints=[
            "Use the extended Euclidean algorithm on (e_a, e_b).",
            "Combine ciphertexts: m = c_a^{x} * c_b^{y} mod n when e_a x + e_b y = 1.",
            "m is 4242 in this fixture.",
        ],
        answer=fix["answer"],
        payload={
            "n": fix["n"],
            "e_a": fix["e_a"],
            "e_b": fix["e_b"],
            "c_a": fix["c_a"],
            "c_b": fix["c_b"],
            "fixture": "rsa_common_mod.json",
            "fixture_version": fix["fixture_version"],
        },
        educational_note=(
            "EDUCATIONAL common-modulus demo with canned lab keys. "
            "SAFE path: never reuse n across distinct key pairs."
        ),
        solver_name="solve_rsa_common_mod",
        fixture_version=fix["fixture_version"],
    )
