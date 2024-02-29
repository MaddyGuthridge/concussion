import os
from typing import TextIO
from .pysh import Pysh


class PyshCd(Pysh):
    """
    change directory
    """
    def __init__(self) -> None:
        super().__init__()
        self._args.append("cd")

    def exec(self, stdin: TextIO, stdout: TextIO, stderr: TextIO) -> None:
        assert len(self._args) == 2

        os.chdir(self._args[1])

    def do_finish_exec(self) -> int:
        return 0


class PyshPwd(Pysh):
    """
    print working directory
    """
    def __init__(self) -> None:
        super().__init__()
        self._args.append("pwd")

    def exec(self, stdin: TextIO, stdout: TextIO, stderr: TextIO) -> None:
        stdout.write(os.getcwd() + "\n")

    def do_finish_exec(self) -> int:
        return 0


cd = PyshCd()
pwd = PyshPwd()
