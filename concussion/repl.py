"""
# Concussion / REPL

Code for running the Python REPL that concussion is based on
"""
import sys
import code

from .shell_state import shell_locals
from concussion import __version__ as version


def main():
    code.interact(
        banner="\n".join([
            f"Concussion Shell - v{version}",
            f"Python {sys.version} on {sys.platform}"
        ]),
        local=shell_locals,
        exitmsg="exit",
    )
