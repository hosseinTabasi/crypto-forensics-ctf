# crypto-forensics-ctf

[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Educational Lab](https://img.shields.io/badge/lab-educational-orange.svg)](docs/SECURITY.md)
[![Offline](https://img.shields.io/badge/network-offline%20fixtures-lightgrey.svg)](PROTOCOL.md)

Offline **cryptography forensics CTF pack** by **Hossein Tabasi**
([GitHub: hosseinTabasi](https://github.com/hosseinTabasi)).

Extends [cryptolab-kit](https://github.com/hosseinTabasi/cryptolab-kit) and
optionally bridges [cryptolab-suite](https://github.com/hosseinTabasi/cryptolab-suite)
concepts into a graded challenge chain:

**classic ciphers → RSA padding footguns (offline sims) → AES-GCM misuse**.

> Educational laboratory only — no live network attacks, no malware, no
> ransomware, no keyloggers, no real exploit tooling against third parties.

## Features

| Area | What you get |
|---|---|
| Tier A Classic | Caesar, Vigenère (known period), monoalphabetic frequency, single-byte XOR |
| Tier B RSA | Tiny textbook RSA, small-e stereotyped plaintext, PKCS#1 v1.5 **FakeOracle** simulation (canned transcript), common-modulus demo |
| Tier C AES-GCM | Nonce-reuse XOR recovery, forbidden (key,nonce) detection, missing-tag rejection, AAD mismatch forensic |
| CLI | `list` / `show` / `hint` / `solve` / `auto-solve` / `experiment` |
| Empirical study | N-run auto-solve timings → `artifacts/run_*.json` → `reports/RESULTS.md` |
| Kit bridge | Optional use of cryptolab-kit classic helpers when installed |

## Install

```bash
python -m venv .venv
source .venv/bin/activate

# recommended: editable sibling kit
pip install -e ../cryptolab-kit -e ".[dev]"

# optional suite bridge metadata
pip install -e ../cryptolab-suite
```

Or from GitHub (after publish):

```bash
pip install "crypto-forensics-ctf @ git+https://github.com/hosseinTabasi/crypto-forensics-ctf.git"
```

Requires **Python 3.11+**.

## Quickstart

```bash
crypto-forensics list
crypto-forensics show classic-caesar
crypto-forensics hint classic-caesar --level 1
crypto-forensics solve classic-caesar --answer 'FLAG{...}'
crypto-forensics auto-solve classic-caesar --check

# empirical study (see PROTOCOL.md)
crypto-forensics experiment run -n 5
crypto-forensics experiment report
```

Equivalent module form: `python -m crypto_forensics …`.

## Challenge tiers (12)

| Tier | Count | Themes |
|---|---:|---|
| A Classic | 4 | Shift / polyalphabetic / substitution / XOR |
| B RSA | 4 | Factorable n, small e, FakeOracle PKCS sim, common modulus |
| C AES-GCM | 4 | Nonce reuse, forbidden pairs, tag strip, AAD |

Points and qualitative difficulty are listed in `PROTOCOL.md` and the
static table inside `reports/RESULTS.md` after a study run.

## Security disclaimer

This repository teaches **why** certain constructions fail. Misuse demos are
local and fixture-driven. For production cryptography follow the **SAFE**
paths in [docs/SECURITY.md](docs/SECURITY.md) (AES-GCM with unique nonces and
full tags; RSA-OAEP/PSS via well-reviewed libraries).

The PKCS#1 v1.5 challenge uses an offline `FakeOracle` with canned responses
only — it is **not** a network padding-oracle service.

## Related projects

- [cryptolab-kit](https://github.com/hosseinTabasi/cryptolab-kit) — classic + modern crypto toolkit
- [cryptolab-suite](https://github.com/hosseinTabasi/cryptolab-suite) — advanced lab suite (Shamir, Merkle, vault, …)

## Topics

`cryptography` · `ctf` · `forensics` · `educational` · `aes-gcm` · `rsa` ·
`classic-ciphers` · `padding-oracle-simulation` · `nonce-reuse`

## License

MIT © Hossein Tabasi — see [LICENSE](LICENSE).

## Documentation

- [PROTOCOL.md](PROTOCOL.md) — reproducible empirical study
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — package design
- [docs/SECURITY.md](docs/SECURITY.md) — EDUCATIONAL vs SAFE
- [examples/demo_session.md](examples/demo_session.md) — sample CLI session
- [reports/RESULTS.md](reports/RESULTS.md) — measured results (after `experiment run`)
