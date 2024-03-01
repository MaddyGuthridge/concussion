from abc import abstractmethod
from copy import deepcopy
from typing import Optional, TextIO
import subprocess
import sys
from threading import Thread


def threaded_write_out(buf: TextIO, output_to: TextIO):
    """
    Write output from buffer to the given output in a separate thread, so that
    we can do other work elsewhere.

    I wish there was a nicer way to do this. I mean there probably is but idk
    what it is
    """
    def do_write():
        # Infinite loop until the buffer is closed, then we stop
        try:
            while True:
                # Read buffer line-by-line. I can't think of a cleaner solution
                output_to.write(buf.readline())
        except ValueError:
            pass

    Thread(target=do_write).run()


class Pysh:
    """
    Pysh command component
    """
    def __init__(self) -> None:
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
        return new

    def __repr__(self) -> str:
        """
        Object representation. We use this to execute the command.
        """
        if len(self._args) == 0:
            return ""

        if self._in_file:
            overall_input: TextIO = open(self._in_file, 'r')
        else:
            overall_input = sys.stdin

        if self._pipe_from:
            stdout, stderr = self._pipe_from.exec(overall_input)
            our_input = stdout
            threaded_write_out(stderr, sys.stderr)
        else:
            our_input = overall_input

        stdout, stderr = self.exec(our_input)

        threaded_write_out(stderr, sys.stderr)
        if self._out_file:
            threaded_write_out(stdout, open(self._out_file))
        else:
            threaded_write_out(stdout, sys.stdout)

        return_code = self.finish_exec()
        # TODO: Set environment variable with return code

        return ""

    @abstractmethod
    def exec(self, stdin: TextIO) -> tuple[TextIO, TextIO]:
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
            return new_cmd
        elif isinstance(other, Pysh):
            new_cmd = other.clone()
            new_cmd._pipe_from = self
            return new_cmd
        else:
            raise TypeError("Give a str instead")


class PyshExecute(Pysh):
    def __init__(self) -> None:
        super().__init__()
        self._process: Optional[subprocess.Popen] = None

    def exec(self, stdin: TextIO) -> tuple[TextIO, TextIO]:
        self._process = subprocess.Popen(
            self._args,
            stdin=stdin,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        assert self._process.stdout is not None
        assert self._process.stderr is not None

        # The inheritance for buffers in python is so confusing
        return self._process.stdout, self._process.stderr  # type: ignore

    def do_finish_exec(self) -> int:
        assert self._process is not None
        return self._process.wait()
