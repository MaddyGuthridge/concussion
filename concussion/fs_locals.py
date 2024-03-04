"""
# Concussion / FS locals

A dict-alike, where any lookup errors result in a the creation of a CursedPath
object. This allows for executing arbitrary system commands without needing to
bring them into scope.
"""
from typing import Any
from .based import ConcussionExecutable


class FsLocals(dict):
    """
    A dict-alike, where any lookup errors result in a the creation of a
    CursedPath object. This allows for executing arbitrary system commands
    without needing to bring them into scope.
    """
    def __init__(self, locals: dict[str, Any] | None = None) -> None:
        if locals is None:
            locals = {}
        super().__init__(locals)

    def __getitem__(self, key: str) -> Any:
        if key in self:
            return super().__getitem__(key)
        # Special case, getting `_` produces a path component pointed at root
        if key == "_":
            return ConcussionExecutable('/')
        else:
            return ConcussionExecutable(key)
