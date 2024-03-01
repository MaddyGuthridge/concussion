from abc import abstractmethod
import os
from typing import TextIO
from io import StringIO
from .pysh import Pysh


class PyshBuiltin(Pysh):
    def __init__(self) -> None:
        super().__init__()
        self._args.append(self.__class__.__name__)
        self._exit_code = 0

    @abstractmethod
    def run(self, stdin: TextIO) -> tuple[str, str]:
        """Run the command"""

    def do_exec(self, stdin: TextIO) -> tuple[TextIO, TextIO]:
        try:
            out, err = self.run(stdin)
            return StringIO(out), StringIO(err)
        except Exception as e:
            self._exit_code = 1
            return StringIO(), StringIO(str(e))

    def do_finish_exec(self) -> int:
        return self._exit_code


class cd(PyshBuiltin):
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


class pwd(PyshBuiltin):
    """
    print working directory
    """
    def run(self, stdin: TextIO) -> tuple[str, str]:
        return os.getcwd() + "\n", ""
