"""
shell builtin functions
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
    def run(self, stdin: TextIO) -> tuple[str, str]:
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
    def run(self, stdin: TextIO) -> tuple[str, str]:
        return os.getcwd() + "\n", ""


class exit(ConcussionBuiltin):
    """
    exit the shell
    """
    def run(self, stdin: TextIO) -> tuple[str, str]:
        if len(self._args) == 1:
            sys.exit()
        else:
            sys.exit(int(self._args[1]))
