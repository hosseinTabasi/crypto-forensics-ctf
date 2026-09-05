"""Automated solvers for the forensics CTF pack (lab / grading)."""

from __future__ import annotations

from typing import Callable

from crypto_forensics.challenges.catalog import Challenge
from crypto_forensics.solvers import classic_solvers, gcm_solvers, rsa_solvers

SolverFn = Callable[[Challenge], str]

_REGISTRY: dict[str, SolverFn] = {
    "solve_caesar": classic_solvers.solve_caesar,
    "solve_vigenere": classic_solvers.solve_vigenere,
    "solve_mono": classic_solvers.solve_mono,
    "solve_xor": classic_solvers.solve_xor,
    "solve_rsa_tiny": rsa_solvers.solve_rsa_tiny,
    "solve_rsa_stereo": rsa_solvers.solve_rsa_stereo,
    "solve_rsa_pkcs_oracle": rsa_solvers.solve_rsa_pkcs_oracle,
    "solve_rsa_common_mod": rsa_solvers.solve_rsa_common_mod,
    "solve_gcm_nonce_reuse": gcm_solvers.solve_gcm_nonce_reuse,
    "solve_gcm_forbidden": gcm_solvers.solve_gcm_forbidden,
    "solve_gcm_tag_strip": gcm_solvers.solve_gcm_tag_strip,
    "solve_gcm_aad_mismatch": gcm_solvers.solve_gcm_aad_mismatch,
}


def get_solver(name: str) -> SolverFn:
    """Return a solver function by registry name."""
    if name not in _REGISTRY:
        raise KeyError(f"unknown solver: {name}")
    return _REGISTRY[name]


def auto_solve(challenge: Challenge) -> str:
    """Run the registered solver for ``challenge`` and return the answer string."""
    if not challenge.solver_name:
        raise ValueError(f"challenge {challenge.id} has no solver_name")
    return get_solver(challenge.solver_name)(challenge)


__all__ = ["auto_solve", "get_solver"]
