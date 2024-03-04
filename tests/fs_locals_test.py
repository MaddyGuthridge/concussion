"""
# Tests / FS locals test

Tests for the file system locals object
"""
from concussion.cursed_path import CursedPath
from concussion.fs_locals import FsLocals


def test_get_var():
    locals = FsLocals({"hi": "hey"})
    assert locals["hi"] == "hey"


def test_set_var():
    locals = FsLocals()
    locals["hi"] = "hey"
    assert locals["hi"] == "hey"


def test_get_root():
    locals = FsLocals()
    assert locals["_"] == CursedPath("/")


def test_get_path():
    locals = FsLocals()
    assert locals["example"] == CursedPath("example")
