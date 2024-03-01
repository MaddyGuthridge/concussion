"""
State of the shell
"""
import os
from pathlib import Path
from concussion import ConcussionBase, ConcussionExecutable, ConcussionBuiltin
from . import shell_builtins


shell_locals: dict[str, ConcussionBase] = {
    "Ṩ": ConcussionExecutable(),
    "S": ConcussionExecutable(),
}
"""
Local variables for shell
"""


def add_locals_from_path():
    """Add all the programs on the path"""
    programs = {}
    for directory in reversed(os.environ.get("PATH", "").split(":")):
        if not Path(directory).is_dir():
            continue
        for file in Path(directory).iterdir():
            # If it's an executable
            if os.access(file, os.X_OK):
                programs[file.name] = ConcussionExecutable(file.name)
    # Now add them all to locals
    shell_locals.update(programs)


def add_shell_builtins():
    """Add shell builtin commands"""
    for name in dir(shell_builtins):
        object = getattr(shell_builtins, name)
        if (
            isinstance(object, type)
            and issubclass(object, ConcussionBuiltin)
            and object is not ConcussionBuiltin
        ):
            shell_locals[name] = object()


add_locals_from_path()
add_shell_builtins()
