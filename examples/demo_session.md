# Demo session

Author: Hossein Tabasi

```bash
# install (from repo root)
python -m venv .venv && source .venv/bin/activate
pip install -e ../cryptolab-kit -e ".[dev]"

# list challenges
crypto-forensics list

# inspect one challenge (no solution)
crypto-forensics show classic-caesar

# progressive hints
crypto-forensics hint classic-caesar --level 1

# submit an answer locally
crypto-forensics solve classic-caesar --answer 'FLAG{SHIFT_THE_ALPHABET_BY_SEVEN}'

# run built-in solver (lab / grading)
crypto-forensics auto-solve classic-caesar --check

# empirical study (see PROTOCOL.md)
crypto-forensics experiment run -n 5
crypto-forensics experiment report
```

All operations are offline. The PKCS#1 challenge uses `FakeOracle` with a
canned transcript only.
