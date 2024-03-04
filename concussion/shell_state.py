"""
# Concussion / shell state

State of the Concussion shell. Contains the dictionary of local variables used
by the REPL. Modifications to these locals are passed through to the REPL,
allowing for programmatic modification of the REPL environment.
"""
from concussion import ConcussionBuiltin
from . import shell_builtins
from .fs_locals import FsLocals


shell_locals = FsLocals()
"""
Local variables for shell
"""


def add_shell_builtins():
    """Build dict of shell builtin commands"""
    builtins = {}
    for name in dir(shell_builtins):
        object = getattr(shell_builtins, name)
        if (
            isinstance(object, type)
            and issubclass(object, ConcussionBuiltin)
            and object is not ConcussionBuiltin
        ):
            builtins[name] = object()

    return builtins


shell_locals |= add_shell_builtins()
