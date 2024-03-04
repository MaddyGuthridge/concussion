# Concussion Shell

It's kinda like Bash except it causes severe brain damage because it's actually
a Python REPL.

## Usage

```txt
$ pip install concussion
$ concussion
>>> cat + README.md | head + -n + 4
# Concussion Shell

It's kinda like Bash except it causes severe brain damage because it's actually
a Python REPL.
```

## How it works

Everything is implemented using horrific operator overloads.

Since the commands can't be executed while they're being constructed, commands
are instead executed when stringified using `repr()`, which works nicely with
Python's interactive console.

Python doesn't support building commands from adjacent identifiers, so
Concussion uses the `+` operator to join arguments for a command.

```py
>>> echo + hello + world
hello world
```

Notice that none of these variables were never defined. Concussion uses a custom
dictionary for the local variable scope such that any undefined variables
create a new string-like object, which helps to improve readability.

You can pipe commands using the standard `|` pipe operator.

```py
>>> ls + -l | less
# less is broken because I can't be bothered to make my shell look like a TTY
# so the output is incorrect
```

To create shell aliases, you simply use Python variable assignments

```py
>>> # This makes for an epic prank
>>> bash = concussion
>>> bash
Concussion shell...
```

Because `&&` and `||` are not supported in Python, use the `and` and `or`
keywords instead.

```py
>>> false or echo + hi
>>> false and echo + hi
hi
>>> true or echo + hi
hi
>>> true and echo + hi
```

You can also do file redirection like in Bash

```py
>>> echo + hi > hi.txt
>>> cat < hi.txt
hi
>>> echo + "hi again" >> hi.txt  # append
>>> cat < hi.txt
hi
hi again
```

Because working with regular strings or `pathlib`'s `Path` objects is tedious
in a shell-like environment, Concussion provides its own `CursedPath` object,
which simplifies many aspects of string manipulation.

```py
>>> str(path/to/some-file.txt)
"['path/to/some-file.txt']"
```

Note that the `/`, `-` and `.` operators all result in string joining.

in order to path to files from the root of the file system, a `_` can be used
before the leading `/`, since a leading `/` in Python produces a `SyntaxError`.

```py
>>> _/usr/bin/sl
# [epic train ASCII art]
```

## Known issues

* Currently all stderr goes directly to this process's stderr, and it cannot be
  redirected. Maybe I'll implement this at some point.

* Currently no support for executing tasks asynchronously. Perhaps I could use
  `β` to signify this since it looks kinda like an `&` but is a valid
  identifier.

* Many programs don't work nicely because they think they're not running in a
  terminal.
