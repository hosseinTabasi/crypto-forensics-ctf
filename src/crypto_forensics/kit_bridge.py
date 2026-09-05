"""Optional bridge to cryptolab-kit (and cryptolab-suite when present).

**SAFE path:** this module only loads sibling educational packages. Challenge
solvers prefer kit primitives when available and fall back to local
implementations otherwise.
"""

from __future__ import annotations

from types import ModuleType
from typing import Any


class KitNotInstalledError(ImportError):
    """Raised when cryptolab-kit is required but not importable."""


def require_cryptolab() -> ModuleType:
    """Import and return the ``cryptolab`` package.

    Raises
    ------
    KitNotInstalledError
        With install instructions if the package is missing.
    """
    try:
        import cryptolab
    except ImportError as exc:
        raise KitNotInstalledError(
            "cryptolab-kit is not installed. Install the sibling package first:\n"
            "  pip install -e ../cryptolab-kit -e \".[dev]\"\n"
            "Or from GitHub:\n"
            "  pip install \"cryptolab-kit @ git+https://github.com/hosseinTabasi/cryptolab-kit.git\"\n"
            "See README.md."
        ) from exc
    return cryptolab


def try_cryptolab() -> ModuleType | None:
    """Return ``cryptolab`` if installed, else ``None``."""
    try:
        return require_cryptolab()
    except KitNotInstalledError:
        return None


def try_suite() -> ModuleType | None:
    """Return ``cryptolab_suite`` if installed, else ``None``."""
    try:
        import cryptolab_suite
    except ImportError:
        return None
    return cryptolab_suite


def get_attr(dotted: str) -> Any:
    """Resolve ``cryptolab.<dotted>`` or raise :class:`KitNotInstalledError`."""
    mod = require_cryptolab()
    obj: Any = mod
    for part in dotted.split("."):
        try:
            obj = getattr(obj, part)
        except AttributeError:
            import importlib

            obj = importlib.import_module(f"cryptolab.{dotted}")
            break
    return obj


def kit_status() -> dict[str, bool | str | None]:
    """Return a small status dict for CLI / experiment metadata."""
    kit = try_cryptolab()
    suite = try_suite()
    return {
        "cryptolab_kit": kit is not None,
        "cryptolab_kit_version": getattr(kit, "__version__", None) if kit else None,
        "cryptolab_suite": suite is not None,
        "cryptolab_suite_version": getattr(suite, "__version__", None) if suite else None,
    }
