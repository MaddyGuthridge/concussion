"""
# Concussion shell

It's kinda like Bash except it causes severe brain damage because it's actually
a Python REPL.
"""
__version__ = "0.2.0"
__all__ = [
    "ConcussionBase",
    "ConcussionExecutable",
    "ConcussionBuiltin",
    "main",
]

from .based import ConcussionBase, ConcussionExecutable, ConcussionBuiltin
from .repl import main
