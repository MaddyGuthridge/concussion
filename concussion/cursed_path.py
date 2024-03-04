"""
# Concussion / cursed path

A class representing a path on the file system, except the operator overloading
is very cursed.
"""
from typing import Union
import os

CursedPathJoinable = Union[str, list[str], tuple[str, ...], 'CursedPath']


class CursedPath:
    """
    A class that overloads the division operator to create an instance of
    itself with a / and then the string or CursedPath it was divided by, and
    also overloads the dot operator to create an instance of itself with a .
    and then the string of the property being accessed.

    Essentially:

    ```py
    foo = CursedPath('foo')
    bar = CursedPath('bar')

    path1 = foo/bar
    # path1 is now CursedPath('foo/bar)

    path2 = foo.baz
    # path2 is now CursedPath('foo.baz')
    ```
    """
    def __init__(self, path: CursedPathJoinable | None = None) -> None:
        """
        Create a CursedPath object.
        """
        if path is None:
            path = '/'
        if path == "~":
            path = os.environ["HOME"]
        if isinstance(path, (list, tuple)):
            for item in path:
                if not isinstance(item, str):
                    raise TypeError("All items in path list/tuple must be str")
            path = "/".join(path)
        elif not isinstance(path, (str, CursedPath)):
            raise TypeError(
                "path for CursedPath must be of type str, list[str] or "
                "tuple[str, ...]")
        self.__path = str(path)

    def __repr__(self) -> str:
        return f"CursedPath('{self.__path}')"

    def __str__(self) -> str:
        return self.__path

    def __eq__(self, other: object) -> bool:
        if isinstance(other, (CursedPath, str)):
            return str(self) == str(other)
        return NotImplemented

    def __handle_join(
        self,
        other: CursedPathJoinable,
        joiner: str,
    ) -> 'CursedPath':
        if isinstance(other, (str, CursedPath)):
            # Special case: joining / to root directory
            if self == "/" and joiner == "/":
                return CursedPath("/" + str(other))
            else:
                return CursedPath(str(self) + joiner + str(other))
        elif isinstance(other, (list, tuple)):
            for item in other:
                if not isinstance(item, str):
                    raise TypeError(
                        "All items in list/tuple must be a str when joining "
                        "to CursedPath objects")
            return CursedPath(str(self) + joiner + str(CursedPath(other)))
        else:
            return NotImplemented

    def __truediv__(self, other: CursedPathJoinable) -> 'CursedPath':
        return self.__handle_join(other, '/')

    def __rtruediv__(self, other: CursedPathJoinable) -> 'CursedPath':
        return CursedPath(other) / self

    def __sub__(self, other: CursedPathJoinable) -> 'CursedPath':
        return self.__handle_join(other, '-')

    def __rsub__(self, other: CursedPathJoinable) -> 'CursedPath':
        return CursedPath(other) - self

    def __getattr__(self, name: str) -> 'CursedPath':
        return self.__handle_join(name, '.')
