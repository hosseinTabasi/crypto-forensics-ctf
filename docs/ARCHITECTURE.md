# Architecture

Author: Hossein Tabasi

## Package layout

```
src/crypto_forensics/
  cli.py                 # argparse CLI entry
  kit_bridge.py          # optional cryptolab-kit / suite imports
  challenges/            # definitions + FakeOracle
  solvers/               # deterministic auto-solvers
  experiments/           # study runner + metrics → artifacts JSON / RESULTS.md
data/challenges/         # frozen fixtures (JSON/hex)
artifacts/               # measured run_*.json
reports/RESULTS.md       # generated from artifacts only
```

## Data flow

1. Fixtures under `data/challenges/` define public payloads and checker answers.
2. `challenges/*.py` wrap fixtures into `Challenge` dataclasses (catalog).
3. `solvers/*` implement `auto_solve` for grading / empirical study.
4. `experiments.runner` times N full passes and writes JSON artifacts.
5. `experiments.metrics` aggregates artifacts into `reports/RESULTS.md`.

## Bridge to cryptolab-kit

`kit_bridge.try_cryptolab()` loads the sibling package when installed.
Classic solvers prefer kit Caesar / Vigenère / frequency helpers and fall
back to local implementations so the pack remains usable standalone.

Optional `cryptolab-suite` presence is recorded in experiment metadata only.

## CLI surface

Entry points: `crypto-forensics` and `python -m crypto_forensics`.

Commands: `list`, `show`, `hint`, `solve`, `auto-solve`,
`experiment run`, `experiment report`.

## Testing

Pytest is offline (no network). Tests assert catalog size, FakeOracle
behavior, and that every challenge auto-solves to its checker answer.
