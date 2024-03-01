"""
Main program, responsible for setting up the environment and
"""
import code

from concussion import ConcussionBase, ConcussionExecutable, ConcussionBuiltin
from . import shell_builtins


def main():
    locals: dict[str, ConcussionBase] = {
        "Ṩ": ConcussionExecutable(),
    }
    # Add all the shell builtins
    for name in dir(shell_builtins):
        object = getattr(shell_builtins, name)
        if (
            isinstance(object, type)
            and issubclass(object, ConcussionBuiltin)
            and object is not ConcussionBuiltin
        ):
            locals[name] = object()

    code.interact(local=locals)


if __name__ == '__main__':
    main()
