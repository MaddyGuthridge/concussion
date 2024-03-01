"""
Main program, responsible for setting up the environment and
"""
import code

from .shell_state import shell_locals


def main():
    code.interact(local=shell_locals)


if __name__ == '__main__':
    main()
