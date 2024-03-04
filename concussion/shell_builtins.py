"""
# Concussion / shell builtins

Shell builtin functions
"""
import os
import sys
from typing import TextIO
from concussion import ConcussionBuiltin


__all__ = ['cd', 'pwd', 'exit']


class cd(ConcussionBuiltin):
    """
    change directory
    """
    def run_builtin(self, stdin: TextIO) -> tuple[str, str]:
        if len(self._args) == 1:
            # cd with no args
            home = os.getenv("HOME")
            assert home is not None
            os.chdir(home)
        else:
            os.chdir(self._args[1])

        return "", ""


class pwd(ConcussionBuiltin):
    """
    print working directory
    """
    def run_builtin(self, stdin: TextIO) -> tuple[str, str]:
        return os.getcwd() + "\n", ""


class exit(ConcussionBuiltin):
    """
    exit the shell

    Whenever this is `repr`d it causes the process to exit, incidentally making
    this program really painful to debug.
    """
    def run_builtin(self, stdin: TextIO) -> tuple[str, str]:
        if len(self._args) == 1:
            sys.exit()
        else:
            sys.exit(int(self._args[1]))
