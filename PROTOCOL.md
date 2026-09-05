# Study Protocol — crypto-forensics-ctf

Author: Hossein Tabasi

This protocol defines the reproducible empirical study for the offline
cryptography forensics CTF pack. Timing and success metrics MUST be measured
by running the experiment; do not invent numbers.

## Scope

Educational laboratory only. Challenges are offline fixtures. There are no
live network attacks, no malware, no ransomware, no keyloggers, and no
third-party exploitation tooling.

## Challenges included

| id | tier | category | fixture |
|---|---|---|---|
| `classic-caesar` | A | classic | `data/challenges/classic_caesar.json` |
| `classic-vigenere` | A | classic | `data/challenges/classic_vigenere.json` |
| `classic-mono` | A | classic | `data/challenges/classic_mono.json` |
| `classic-xor` | A | classic | `data/challenges/classic_xor.json` |
| `rsa-tiny` | B | rsa | `data/challenges/rsa_tiny.json` |
| `rsa-stereo` | B | rsa | `data/challenges/rsa_stereo.json` |
| `rsa-pkcs-oracle` | B | rsa | `data/challenges/rsa_pkcs_oracle.json` |
| `rsa-common-mod` | B | rsa | `data/challenges/rsa_common_mod.json` |
| `gcm-nonce-reuse` | C | aes-gcm | `data/challenges/gcm_nonce_reuse.json` |
| `gcm-forbidden` | C | aes-gcm | `data/challenges/gcm_forbidden.json` |
| `gcm-tag-strip` | C | aes-gcm | `data/challenges/gcm_tag_strip.json` |
| `gcm-aad-mismatch` | C | aes-gcm | `data/challenges/gcm_aad_mismatch.json` |

Fixture version field: `fixture_version` (currently `1.0.0` for all).

## Seeds / determinism

- All ciphertexts and keys are frozen JSON under `data/challenges/`.
- Solvers are deterministic given those fixtures (no RNG in the happy path).
- AES-GCM lab keys are fixed hex constants for reproducibility (not production secrets).

## Metrics

For each challenge, on each run:

- `success` — whether `auto_solve` matches the checker answer
- `elapsed_ms` — wall-clock milliseconds (`time.perf_counter`)
- `attempts` — solver invocation count until success (1 for designed solvers)
- `points_recovered` — challenge points if success else 0

Aggregates:

- per-challenge success rate across N runs
- mean / median / stdev / min / max solve time (ms)
- category totals (challenge count, points available, mean success, mean ms)
- overall success rate and rate-weighted points recovered

## Hardware note

Record `platform.uname()` (and Python version / `platform.platform()`) at run
time inside the artifact JSON.

## Procedure

1. Create a virtualenv and install:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e /path/to/cryptolab-kit -e ".[dev]"
   # optional: pip install -e /path/to/cryptolab-suite
   ```
2. Run unit tests offline:
   ```bash
   pytest -q
   ```
3. Execute the study with **N ≥ 5** full auto-solve passes:
   ```bash
   python -m crypto_forensics experiment run -n 5
   ```
   This writes `artifacts/run_*.json`.
4. Regenerate the human-readable report from artifacts only:
   ```bash
   python -m crypto_forensics experiment report
   ```
   Output: `reports/RESULTS.md`.

## Success criteria

- Designed-solvable challenges should achieve **100%** auto-solve success.
- `reports/RESULTS.md` must contain only numbers present in the JSON artifacts.
- Manual difficulty / points table may be static; timing and success must be measured.

## Ethical boundary

PKCS#1 v1.5 “oracle” material is a `FakeOracle` class driven by a canned
transcript. It is not a network service and not a general exploit framework.
