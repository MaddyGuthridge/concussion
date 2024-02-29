from abc import abstractmethod
from copy import deepcopy
from io import StringIO
from typing import Optional, TextIO
import subprocess
import sys


class Pysh:
    """
    Pysh command component
    """
    def __init__(self) -> None:
        self._consumed = False
        """
        Whether this component has been consumed by being combined with another
        component
        """

        self._args: list[str] = []
        """
        List of arguments for the command. These are appended using the `+`
        operator.
        """

        self._pipe_from: Optional['Pysh'] = None
        """
        Command to pipe input from
        """

        self._out_file: Optional[str] = None
        """
        File to write output to (note this is only used for final outputs, and
        is unset if outputting to another command)
        """

        self._in_file: Optional[str] = None
        """
        File to read input from
        """

    def clone(self) -> 'Pysh':
        """
        Clone the command.
        """
        new = deepcopy(self)
        self._consumed = True
        new._consumed = False
        return new

    def __repr__(self) -> str:
        """
        Object representation. We use this to execute the command if needed.
        """
        # print("Repr called")
        if self._consumed or len(self._args) == 0:
            return ""

        if self._out_file:
            output: TextIO = open(self._out_file, 'w')
        else:
            output = sys.stdout

        if self._in_file:
            overall_input: TextIO = open(self._in_file, 'r')
        else:
            overall_input = sys.stdin

        if self._pipe_from:
            # Piping from another command, send it our stdin instead, and give
            # it a string buffer to write to which we can use for our input
            our_input = StringIO()
            self._pipe_from.exec(overall_input, our_input, sys.stderr)
        else:
            our_input = overall_input

        self.exec(our_input, output, sys.stderr)

        return_code = self.finish_exec()
        # TODO: Set environment variable with return code
        # print(f"Program exited with code {return_code}")

        return ""

    @abstractmethod
    def exec(self, stdin: TextIO, stdout: TextIO, stderr: TextIO) -> None:
        """
        Execute this command. Must be implemented in subclasses.
        """

    def finish_exec(self) -> int:
        """
        Finish execution of command and return result

        This part handles calling the function in programs we piped from
        """
        if self._pipe_from:
            self._pipe_from.finish_exec()
        return self.do_finish_exec()

    @abstractmethod
    def do_finish_exec(self) -> int:
        """
        Finish execution of command and return result

        This part should be overridden by child classes to actually wait for
        the execution to finish.
        """

    def __add__(self, other: object) -> 'Pysh':
        """
        Add an argument to the command.
        """
        if isinstance(other, str):
            new_cmd = self.clone()
            new_cmd._args.append(other)
            return new_cmd
        else:
            # TODO: Error handling and reporting
            # I want to make this print out when the command is actually
            # executed, perhaps by storing a collection of error messages then
            # printing them instead of executing the command.
            raise TypeError("Expected a str or something")

    def __lt__(self, other: object) -> 'Pysh':
        """
        Add a file as input
        """
        if isinstance(other, str):
            new_cmd = self.clone()
            new_cmd._in_file = other
            return new_cmd
        else:
            raise TypeError("Expected a str or something")

    def __gt__(self, other: object) -> 'Pysh':
        """
        Add a file as output
        """
        if isinstance(other, str):
            new_cmd = self.clone()
            new_cmd._out_file = other
            return new_cmd
        else:
            raise TypeError("Expected a str or something")

    def __or__(self, other: object) -> 'Pysh':
        """
        Pipe this to another command
        """
        if isinstance(other, str):
            new_cmd = PyshExecute()
            new_cmd._args.append(other)
            new_cmd._pipe_from = self
            self._consumed = True
            return new_cmd
        elif isinstance(other, Pysh):
            new_cmd = other.clone()
            new_cmd._pipe_from = self
            self._consumed = True
            return new_cmd
        else:
            raise TypeError("Give a str instead")


class PyshExecute(Pysh):
    def __init__(self) -> None:
        super().__init__()
        self._process: Optional[subprocess.Popen] = None

    def exec(self, stdin: TextIO, stdout: TextIO, stderr: TextIO) -> None:
        if isinstance(stdout, StringIO):
            # FIXME: I need a way to make these buffers work nicely if they
            # don't have a fileno
            self._process = subprocess.Popen(
                self._args,
                stdin=stdin,
                stdout=stdout,
                stderr=stderr,
                text=True,
            )

    def do_finish_exec(self) -> int:
        assert self._process is not None
        return self._process.wait()
