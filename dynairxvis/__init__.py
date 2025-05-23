"""
dynairxvis top-level package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Tiny API re-exports + metadata.
"""

from importlib.metadata import version as _pkg_version  # stdlib ≥3.8

__author__ = "DynAIRx"
try:
    __version__ = _pkg_version(__name__)
except Exception:  # e.g. not installed
    __version__ = "unknown"

__all__ = [
    # public re-exports (populated lazily below)
    "dot", "box", "bar", "pie", "table_list", "line", "gantt",
    "radar", "violin", "histogram", "scatter", "heatmap", "calendar",
    "profile", "findIndex",
]

# --- lazy re-exports ---------------------------------------------------------

from importlib import import_module as _imp
import typing as _t


def __getattr__(name: str) -> _t.Any:
    """
    Lazily import sub-modules the first time they’re requested.

    >>> from dynairxvis import bar   # triggers real import only here
    """
    module_map = {
        "dot": ".dot",
        "box": ".box",
        "bar": ".bar",
        "pie": ".pie",
        "table_list": ".pie",
        "line": ".time",
        "gantt": ".gantt",
        "radar": ".radar",
        "violin": ".violin",
        "histogram": ".hist",
        "scatter": ".scatter",
        "heatmap": ".heatmap",
        "calendar": ".calendar",
        "profile": ".utils",
        "findIndex": ".utils",
    }
    if name in module_map:
        mod = _imp(module_map[name], package=__name__)
        attr = getattr(mod, name)
        globals()[name] = attr          # cache for future access
        return attr
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
