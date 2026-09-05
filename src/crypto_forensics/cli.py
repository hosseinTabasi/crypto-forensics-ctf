"""Command-line interface for crypto-forensics-ctf.

Commands: list, show, hint, solve, auto-solve, experiment run/report.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Sequence

from crypto_forensics import __author__, __version__
from crypto_forensics.challenges.catalog import all_challenges, get_challenge
from crypto_forensics.experiments.metrics import write_results_md
from crypto_forensics.experiments.runner import run_experiment
from crypto_forensics.kit_bridge import kit_status
from crypto_forensics.solvers import auto_solve


def _cmd_list(_args: argparse.Namespace) -> int:
    rows = all_challenges()
    print(f"{'ID':<22} {'TIER':<4} {'CAT':<10} {'PTS':>4}  TITLE")
    print("-" * 72)
    for ch in rows:
        print(f"{ch.id:<22} {ch.tier:<4} {ch.category:<10} {ch.points:>4}  {ch.title}")
    print(f"\n{len(rows)} challenges — author {__author__}")
    return 0


def _cmd_show(args: argparse.Namespace) -> int:
    ch = get_challenge(args.id)
    print(f"[{ch.id}] {ch.title}")
    print(f"tier={ch.tier} category={ch.category} difficulty={ch.difficulty} points={ch.points}")
    print(f"fixture_version={ch.fixture_version}")
    print()
    print(ch.description)
    print()
    print(ch.educational_note)
    print()
    print("Public payload:")
    # Omit nothing critical for solving from public view except we already
    # put public material in description; still show payload sans answer.
    public = {k: v for k, v in ch.payload.items()}
    print(json.dumps(public, indent=2))
    return 0


def _cmd_hint(args: argparse.Namespace) -> int:
    ch = get_challenge(args.id)
    level = args.level
    if level is None:
        for i, hint in enumerate(ch.hints, start=1):
            print(f"Hint {i}/{len(ch.hints)}: {hint}")
        return 0
    if level < 1 or level > len(ch.hints):
        print(f"hint level must be 1..{len(ch.hints)}", file=sys.stderr)
        return 2
    print(f"Hint {level}/{len(ch.hints)}: {ch.hints[level - 1]}")
    return 0


def _cmd_solve(args: argparse.Namespace) -> int:
    ch = get_challenge(args.id)
    ok = ch.check_answer(args.answer)
    if ok:
        print(f"CORRECT — {ch.points} points")
        return 0
    print("INCORRECT")
    return 1


def _cmd_auto_solve(args: argparse.Namespace) -> int:
    ch = get_challenge(args.id)
    answer = auto_solve(ch)
    ok = ch.check_answer(answer)
    print(answer)
    if args.check:
        print("CORRECT" if ok else "INCORRECT")
    return 0 if ok else 1


def _cmd_experiment_run(args: argparse.Namespace) -> int:
    path = run_experiment(n_runs=args.n)
    print(f"wrote {path}")
    status = kit_status()
    print(f"kit_status={status}")
    return 0


def _cmd_experiment_report(args: argparse.Namespace) -> int:
    artifact = Path(args.artifact) if args.artifact else None
    dest = write_results_md(artifact)
    print(f"wrote {dest}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Build the top-level argument parser."""
    parser = argparse.ArgumentParser(
        prog="crypto-forensics",
        description=(
            "Offline cryptography forensics CTF pack "
            f"(v{__version__}, {__author__}). Educational lab only."
        ),
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list", help="list challenges")
    p_list.set_defaults(func=_cmd_list)

    p_show = sub.add_parser("show", help="show challenge briefing + public payload")
    p_show.add_argument("id", help="challenge id")
    p_show.set_defaults(func=_cmd_show)

    p_hint = sub.add_parser("hint", help="show progressive hints")
    p_hint.add_argument("id", help="challenge id")
    p_hint.add_argument(
        "--level",
        type=int,
        default=None,
        help="1-based hint index (default: all)",
    )
    p_hint.set_defaults(func=_cmd_hint)

    p_solve = sub.add_parser("solve", help="check an answer locally")
    p_solve.add_argument("id", help="challenge id")
    p_solve.add_argument("--answer", required=True, help="candidate answer string")
    p_solve.set_defaults(func=_cmd_solve)

    p_auto = sub.add_parser("auto-solve", help="run built-in solver (lab/grading)")
    p_auto.add_argument("id", help="challenge id")
    p_auto.add_argument(
        "--check",
        action="store_true",
        help="also print CORRECT/INCORRECT",
    )
    p_auto.set_defaults(func=_cmd_auto_solve)

    p_exp = sub.add_parser("experiment", help="empirical study commands")
    exp_sub = p_exp.add_subparsers(dest="experiment_command", required=True)

    p_run = exp_sub.add_parser("run", help="run full auto-solve study (N passes)")
    p_run.add_argument("-n", type=int, default=5, help="number of full passes (default 5)")
    p_run.set_defaults(func=_cmd_experiment_run)

    p_rep = exp_sub.add_parser("report", help="regenerate RESULTS.md from artifacts")
    p_rep.add_argument(
        "--artifact",
        default=None,
        help="path to run_*.json (default: latest under artifacts/)",
    )
    p_rep.set_defaults(func=_cmd_experiment_report)

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """CLI entry point."""
    parser = build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)
    try:
        return int(args.func(args))
    except KeyError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except FileNotFoundError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
