"""filetreekg.cli — Click-based CLI entry points.

Public API
----------
The root Click group is importable from either location::

    from filetreekg.cli import cli
    from filetreekg.cli.main import cli
"""

from ftree_kg.cli import (
    cmd_analyze,  # noqa: F401  — registers analyze
    cmd_build,  # noqa: F401  — registers build
    cmd_query,  # noqa: F401  — registers query, pack
    cmd_snapshot,  # noqa: F401  — registers snapshot
)
from ftree_kg.cli.group import cli

__all__ = ["cli"]
