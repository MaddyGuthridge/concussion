"""
# Concussion / based

Base class for Concussion commands
"""
from abc import abstractmethod
from copy import deepcopy
from io import StringIO
from typing import Optional, TextIO, cast
import subprocess
import sys
import os
from threading import current_thread

from concussion.stoppable_thread import StoppableThread


def threaded_write_out(buf: TextIO, output_to: TextIO) -> StoppableThread:
    """
    Write output from buffer to the given output in a separate thread, so that
    we can do other work elsewhere.

    I wish there was a nicer way to do this. I mean there probably is but idk
    what it is
    """
    def do_write():
        t = cast(StoppableThread, current_thread())
        # print(f"Thread buffer start: {buf} -> {output_to}")
        # Infinite loop until the buffer is closed, then we stop
        try:
            while not t.stopped():
                # Read buffer line-by-line. I can't think of a cleaner solution
                output_to.write(buf.readline())
            # Read the last of the buffer
            output_to.write(buf.read())
        except ValueError:
            # Close the output buffer
            output_to.close()
            # print(f"Thread buffer end: {buf} -> {output_to}")

    # The threads don't seem to be dying properly, so let's at least make sure
    # they don't prevent us from exiting
    t = StoppableThread(target=do_write, daemon=True)
    t.start()

    return t


class ConcussionBase:
    """
    Concussion command - abstract base class
    """
    def __init__(self) -> None:
        self._args: list[str] = []
        """
        List of arguments for the command. These are appended using the `+`
        operator.
        """

        self._pipe_from: Optional['ConcussionBase'] = None
        """
        Command to pipe input from
        """

        self._out_file: Optional[str] = None
        """
        File to write output to (note this is only used for final outputs, and
        is unset if outputting to another command)
        """

        self._out_append = False
        """
        Whether to append instead of write to the output file if applicable
        """

        self._in_file: Optional[str] = None
        """
        File to read input from
        """

        self._stderr_thread: Optional[StoppableThread] = None

    def clone(self) -> 'ConcussionBase':
        """
        Clone the command.
        """
        new = deepcopy(self)
        return new

    def __repr__(self) -> str:
        """
        Object representation. We use this to execute the command.
        """
        self.run()
        return ""

    def run(self) -> int:
        """
        Run the command and return its exit code
        """
        if len(self._args) == 0:
            return 0

        if self._in_file:
            overall_input: TextIO = open(self._in_file, 'r')
        else:
            overall_input = sys.stdin

        stdout, stderr = self.exec(overall_input)

        t_stderr = threaded_write_out(stderr, sys.stderr)

        if self._out_file:
            t_stdout = threaded_write_out(
                stdout,
                # Handle logic for appending
                open(self._out_file, 'a' if self._out_append else 'w')
            )
        else:
            t_stdout = threaded_write_out(stdout, sys.stdout)

        return_code = self.finish_exec()

        # Set environment variable with return code
        os.environ["?"] = str(return_code)

        # Kill all our threads
        t_stderr.stop()
        t_stdout.stop()

        return return_code

    def exec(self, stdin: TextIO) -> tuple[TextIO, TextIO]:
        if self._pipe_from:
            stdout, stderr = self._pipe_from.exec(stdin)
            our_input = stdout
            self._stderr_thread = threaded_write_out(stderr, sys.stderr)
        else:
            our_input = stdin

        return self.do_exec(our_input)

    @abstractmethod
    def do_exec(self, stdin: TextIO) -> tuple[TextIO, TextIO]:
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
        if self._stderr_thread:
            self._stderr_thread.stop()
        return self.do_finish_exec()

    @abstractmethod
    def do_finish_exec(self) -> int:
        """
        Finish execution of command and return result

        This part should be overridden by child classes to actually wait for
        the execution to finish.
        """

    def __add__(self, other: object) -> 'ConcussionBase':
        """
        Add an argument to the command.
        """
        if isinstance(other, str):
            new_cmd = self.clone()
            new_cmd._args.append(other)
            return new_cmd
        elif isinstance(other, (list, tuple)):
            for i in other:
                if not isinstance(i, str):
                    raise TypeError("Each element of iterable must be str")
            new_cmd = self.clone()
            new_cmd._args.extend(other)
            return new_cmd
        else:
            # TODO: Error handling and reporting
            # I want to make this print out when the command is actually
            # executed, perhaps by storing a collection of error messages then
            # printing them instead of executing the command.
            raise TypeError("Expected a str or something")

    def __lt__(self, other: object) -> 'ConcussionBase':
        """
        Add a file as input
        """
        if isinstance(other, str):
            new_cmd = self.clone()
            new_cmd._in_file = other
            return new_cmd
        else:
            raise TypeError("Expected a str or something")

    def __gt__(self, other: object) -> 'ConcussionBase':
        """
        Add a file as output
        """
        if isinstance(other, str):
            new_cmd = self.clone()
            new_cmd._out_file = other
            return new_cmd
        else:
            raise TypeError("Expected a str or something")

    def __rshift__(self, other: object) -> 'ConcussionBase':
        """
        Append to a file as output
        """
        if isinstance(other, str):
            new_cmd = self.clone()
            new_cmd._out_file = other
            new_cmd._out_append = True
            return new_cmd
        else:
            raise TypeError("Expected a str or something")

    def __or__(self, other: object) -> 'ConcussionBase':
        """
        Pipe this to another command
        """
        if isinstance(other, str):
            new_cmd: 'ConcussionBase' = ConcussionExecutable()
            new_cmd._args.append(other)
            new_cmd._pipe_from = self
            return new_cmd
        if isinstance(other, (list, tuple)):
            for i in other:
                if not isinstance(i, str):
                    raise TypeError("Each element of iterable must be str")
            new_cmd = ConcussionExecutable()
            new_cmd._args.extend(other)
            new_cmd._pipe_from = self
            return new_cmd
        elif isinstance(other, ConcussionBase):
            new_cmd = other.clone()
            new_cmd._pipe_from = self
            return new_cmd
        else:
            raise TypeError("Give a str instead")

    def __bool__(self) -> bool:
        """Get the status of the command"""
        return bool(self.run())


class ConcussionBuiltin(ConcussionBase):
    """
    Builtin shell function
    """
    def __init__(self) -> None:
        super().__init__()
        self._args.append(self.__class__.__name__)
        self._exit_code = 0

    @abstractmethod
    def run_builtin(self, stdin: TextIO) -> tuple[str, str]:
        """Run the command"""

    def do_exec(self, stdin: TextIO) -> tuple[TextIO, TextIO]:
        try:
            out, err = self.run_builtin(stdin)
            return StringIO(out), StringIO(err)
        except Exception as e:
            self._exit_code = 1
            return StringIO(), StringIO(str(e) + "\n")

    def do_finish_exec(self) -> int:
        return self._exit_code


class ConcussionExecutable(ConcussionBase):
    def __init__(self, executable: Optional[str] = None) -> None:
        super().__init__()
        if executable:
            self._args.append(executable)
        self._process: Optional[subprocess.Popen] = None

    def do_exec(self, stdin: TextIO) -> tuple[TextIO, TextIO]:
        try:
            self._process = subprocess.Popen(
                self._args,
                stdin=stdin,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
        except FileNotFoundError:
            return (
                StringIO(),
                StringIO(f"{self._args[0]}: command not found\n")
            )

        assert self._process.stdout is not None
        assert self._process.stderr is not None

        # The inheritance for buffers in python is so confusing
        return self._process.stdout, self._process.stderr  # type: ignore

    def do_finish_exec(self) -> int:
        if self._process is None:
            return 1
        return self._process.wait()
