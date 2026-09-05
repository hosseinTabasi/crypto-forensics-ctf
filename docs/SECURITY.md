# Security notes

Author: Hossein Tabasi

## EDUCATIONAL vs SAFE

| Area | Label | Guidance |
|---|---|---|
| Classic ciphers (Caesar, Vigenère, monoalphabetic, XOR) | **EDUCATIONAL** | Classroom cryptanalysis only. Never protect real data. |
| Textbook RSA / small moduli / small e | **EDUCATIONAL** | Toy parameters for factoring and stereotyping demos. |
| PKCS#1 v1.5 FakeOracle | **EDUCATIONAL (simulation)** | Offline canned transcript only. No network listener. Not a Bleichenbacher toolkit. |
| AES-GCM nonce reuse / missing tag / AAD mismatch | **EDUCATIONAL misuse demos** | Local fixtures illustrating failure modes. |
| AES-GCM / RSA-OAEP via `cryptography` (cryptolab-kit modern) | **SAFE path** | Use unique 96-bit nonces, full tags, bound AAD, OAEP/PSS, ≥2048-bit RSA. |

## What this pack is not

- Not malware, ransomware, or credential-stealing software
- Not a keylogger or surveillance tool
- Not a live network attack platform
- Not authorization to test third-party systems

## Lab keys

Hex keys and toy RSA primes in `data/challenges/` are published lab material.
Do not reuse them outside this repository.

## Responsible use

Use this pack in coursework, self-study, and controlled labs. If you discover
a packaging bug that could be misunderstood as production guidance, open an
issue on the project tracker.
