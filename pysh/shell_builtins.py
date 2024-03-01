import os
from typing import TextIO
from io import StringIO
from .pysh import Pysh


class PyshCd(Pysh):
    """
    change directory
    """
    def __init__(self) -> None:
        super().__init__()
        self._args.append("cd")

    def exec(self, stdin: TextIO) -> tuple[TextIO, TextIO]:
        assert len(self._args) == 2

        try:
            os.chdir(self._args[1])
        except FileNotFoundError as e:
            return StringIO(), StringIO(str(e))

        return StringIO(), StringIO()

    def do_finish_exec(self) -> int:
        return 0


class PyshPwd(Pysh):
    """
    print working directory
    """
    def __init__(self) -> None:
        super().__init__()
        self._args.append("pwd")

    def exec(self, stdin: TextIO) -> tuple[TextIO, TextIO]:
        return StringIO(os.getcwd() + "\n"), StringIO()

    def do_finish_exec(self) -> int:
        return 0


cd = PyshCd()
pwd = PyshPwd()
