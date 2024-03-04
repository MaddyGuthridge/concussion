"""
# Tests / cursed path test

Test cases for the cursed path
"""
from concussion.cursed_path import CursedPath


def test_path_equality():
    assert CursedPath('a') == 'a'
    assert CursedPath('a') != 'b'


def test_path_join_div():
    a = CursedPath('a')
    b = CursedPath('b')

    assert a / b == "a/b"
    assert a / "b" == "a/b"
    assert "a" / b == "a/b"
    assert a / ['b', 'c'] == "a/b/c"
    assert a / ('b', 'c') == "a/b/c"


def test_path_join_sub():
    a = CursedPath('a')
    assert a - "b" == "a-b"
    assert "b" - a == "b-a"


def test_path_dot_operator():
    a = CursedPath('a')
    assert a.b == "a.b"


def test_path_overall():
    bash = CursedPath() / 'bin' / 'bash'
    assert bash == "/bin/bash"

    this_file = (CursedPath('.') / 'tests' / 'cursed_path_test').py

    assert this_file == "./tests/cursed_path_test.py"


def test_order_of_operations_ignored():
    path = "~" / CursedPath("Documents") / CursedPath("example") \
        - CursedPath("file").txt

    assert path == "~/Documents/example-file.txt"
