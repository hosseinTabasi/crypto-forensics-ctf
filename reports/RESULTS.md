# Empirical Results

Author: Hossein Tabasi

This file is generated from measured experiment artifacts. Do not invent numbers — regenerate via `python -m crypto_forensics experiment report`.

## Run metadata

- Artifact id: `run_20260905T165930Z_d3fce9be`
- Package version: `0.1.0`
- N runs: **5**
- Challenges: **12**
- Started (UTC): 2026-09-05T16:59:30.571167+00:00
- Finished (UTC): 2026-09-05T16:59:30.596576+00:00
- Platform: `Linux-6.12.94+-x86_64-with-glibc2.41` / Python `3.13.5`
- cryptolab-kit: `True` (v0.1.0)
- cryptolab-suite: `True` (v0.1.0)

## Overall

- Overall auto-solve success rate: **100.0%**
- Points available: **2100**; expected recovered (rate-weighted): **2100.0**
- Mean per-challenge solve time (mean of means): **0.421 ms**
- Median per-challenge solve time (median of means): **0.028 ms**

## Per-challenge metrics

| id | category | points | success rate | mean ms | median ms | stdev ms | min ms | max ms |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `classic-caesar` | classic | 100 | 100.0% | 1.913 | 0.118 | 4.014 | 0.102 | 9.093 |
| `classic-vigenere` | classic | 150 | 100.0% | 2.699 | 2.614 | 0.146 | 2.578 | 2.907 |
| `classic-mono` | classic | 200 | 100.0% | 0.076 | 0.075 | 0.019 | 0.049 | 0.097 |
| `classic-xor` | classic | 100 | 100.0% | 0.085 | 0.079 | 0.017 | 0.072 | 0.113 |
| `rsa-tiny` | rsa | 150 | 100.0% | 0.009 | 0.009 | 0.002 | 0.007 | 0.012 |
| `rsa-stereo` | rsa | 200 | 100.0% | 0.047 | 0.044 | 0.010 | 0.040 | 0.063 |
| `rsa-pkcs-oracle` | rsa | 250 | 100.0% | 0.009 | 0.008 | 0.004 | 0.006 | 0.016 |
| `rsa-common-mod` | rsa | 200 | 100.0% | 0.007 | 0.007 | 0.001 | 0.005 | 0.008 |
| `gcm-nonce-reuse` | aes-gcm | 250 | 100.0% | 0.006 | 0.006 | 0.001 | 0.004 | 0.007 |
| `gcm-forbidden` | aes-gcm | 150 | 100.0% | 0.005 | 0.005 | 0.001 | 0.003 | 0.007 |
| `gcm-tag-strip` | aes-gcm | 150 | 100.0% | 0.195 | 0.016 | 0.395 | 0.010 | 0.902 |
| `gcm-aad-mismatch` | aes-gcm | 200 | 100.0% | 0.006 | 0.006 | 0.002 | 0.005 | 0.009 |

## Category totals

| category | challenges | points available | mean success rate | mean ms |
|---|---:|---:|---:|---:|
| classic | 4 | 550 | 100.0% | 1.193 |
| rsa | 4 | 800 | 100.0% | 0.018 |
| aes-gcm | 4 | 750 | 100.0% | 0.053 |

## Manual difficulty (static design table)

Point values and qualitative difficulty are design-time constants (not measured). Timing and success rates above are measured.

| id | tier | difficulty | points |
|---|---|---|---:|
| `classic-caesar` | A | easy | 100 |
| `classic-vigenere` | A | easy | 150 |
| `classic-mono` | A | medium | 200 |
| `classic-xor` | A | easy | 100 |
| `rsa-tiny` | B | easy | 150 |
| `rsa-stereo` | B | medium | 200 |
| `rsa-pkcs-oracle` | B | medium | 250 |
| `rsa-common-mod` | B | medium | 200 |
| `gcm-nonce-reuse` | C | medium | 250 |
| `gcm-forbidden` | C | easy | 150 |
| `gcm-tag-strip` | C | easy | 150 |
| `gcm-aad-mismatch` | C | medium | 200 |

