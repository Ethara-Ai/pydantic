"""Git utilities, adopted from mypy's git utilities (https://github.com/python/mypy/blob/master/mypy/git.py)."""

from __future__ import annotations

import subprocess
from pathlib import Path


def is_git_repo(dir: Path) -> bool:
    """Is the given directory version-controlled with git?"""
    pass


def have_git() -> bool:  # pragma: no cover
    """Can we run the git executable?"""
    pass


def git_revision(dir: Path) -> str:
    """Get the SHA-1 of the HEAD of a git repository."""
    pass
