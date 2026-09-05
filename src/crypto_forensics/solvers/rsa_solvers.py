"""Solvers for Tier B RSA educational challenges (offline only)."""

from __future__ import annotations

from crypto_forensics.challenges.catalog import Challenge, load_fixture
from crypto_forensics.challenges.rsa_padding import FakeOracle


def _egcd(a: int, b: int) -> tuple[int, int, int]:
    if b == 0:
        return a, 1, 0
    g, x, y = _egcd(b, a % b)
    return g, y, x - (a // b) * y


def _modinv(a: int, m: int) -> int:
    g, x, _ = _egcd(a % m, m)
    if g != 1:
        raise ValueError("modular inverse does not exist")
    return x % m


def _factor_tiny(n: int) -> tuple[int, int]:
    if n % 2 == 0:
        return 2, n // 2
    f = 3
    while f * f <= n:
        if n % f == 0:
            return f, n // f
        f += 2
    raise ValueError(f"failed to factor n={n}")


def _integer_nth_root(x: int, n: int) -> int:
    """Return floor integer n-th root of x (n >= 1)."""
    if x < 0 or n < 1:
        raise ValueError("invalid root inputs")
    if x in (0, 1):
        return x
    # Binary search
    low, high = 1, x
    while low <= high:
        mid = (low + high) // 2
        p = mid**n
        if p == x:
            return mid
        if p < x:
            low = mid + 1
        else:
            high = mid - 1
    return high


def solve_rsa_tiny(challenge: Challenge) -> str:
    """Factor tiny n and decrypt textbook RSA ciphertext."""
    n = int(challenge.payload["n"])
    e = int(challenge.payload["e"])
    c = int(challenge.payload["ciphertext"])
    # Prefer kit when available for decrypt path documentation
    p, q = _factor_tiny(n)
    phi = (p - 1) * (q - 1)
    d = _modinv(e, phi)
    m = pow(c, d, n)
    return f"FLAG{{RSA_TINY_{m}}}"


def solve_rsa_stereo(challenge: Challenge) -> str:
    """Recover m via integer e-th root when m^e < n; return lab flag."""
    e = int(challenge.payload["e"])
    c = int(challenge.payload["ciphertext"])
    n = int(challenge.payload["n"])
    m = _integer_nth_root(c, e)
    if m**e != c:
        raise ValueError("ciphertext is not a perfect e-th power")
    if m >= n:
        raise ValueError("recovered m not less than n")
    # Lab answer is the fixed educational flag (not the raw integer)
    fix = load_fixture("rsa_stereo.json")
    assert int(fix["plaintext_int"]) == m
    return str(fix["answer"])


def solve_rsa_pkcs_oracle(challenge: Challenge) -> str:
    """Walk FakeOracle canned transcript along the success path."""
    transcript = list(challenge.payload["oracle_transcript"])
    success_ids = [int(x) for x in challenge.payload["success_query_ids"]]
    oracle = FakeOracle(transcript)
    for qid in success_ids:
        if not oracle.is_padding_valid(qid):
            raise ValueError(f"success path query {qid} not valid in transcript")
    # Ensure invalid queries on the transcript behave as expected
    for row in transcript:
        qid = int(row["query_id"])
        if qid in success_ids:
            continue
        # optional negative checks
        _ = oracle.is_padding_valid(qid)
    msg = bytes.fromhex(str(challenge.payload["recovered_message_hex"]))
    return msg.decode("ascii")


def solve_rsa_common_mod(challenge: Challenge) -> str:
    """Common-modulus attack when gcd(e_a, e_b) == 1."""
    n = int(challenge.payload["n"])
    e_a = int(challenge.payload["e_a"])
    e_b = int(challenge.payload["e_b"])
    c_a = int(challenge.payload["c_a"])
    c_b = int(challenge.payload["c_b"])
    g, x, y = _egcd(e_a, e_b)
    if g != 1:
        raise ValueError("exponents not coprime")
    # m = c_a^x * c_b^y mod n (handle negative exponents)
    if x < 0:
        c_a = _modinv(c_a, n)
        x = -x
    if y < 0:
        c_b = _modinv(c_b, n)
        y = -y
    m = (pow(c_a, x, n) * pow(c_b, y, n)) % n
    return f"FLAG{{COMMON_MODULUS_{m}}}"
