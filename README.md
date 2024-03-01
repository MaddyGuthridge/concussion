# Concussion Shell

It's kinda like Bash except it causes severe brain damage because it's actually
a Python REPL.

## Usage

```txt
$ pip install concussion
$ concussion
>>> cat + "README.md" | head + "-n" + "5"
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
>>> echo + "hello" + "world"
hello world
```

You can pipe commands using the standard `|` pipe operator.

```py
>>> ls + "-l" | less
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
>>> false or echo + "hi"
>>> false and echo + "hi"
hi
>>> true or echo + "hi"
hi
>>> true and echo + "hi"
```

You can also do file redirection like in Bash

```py
>>> echo + "hi" > "hi.txt"
>>> cat < "hi.txt"
hi
>>> echo + "hi again" >> "hi.txt"  # append
>>> cat < "hi.txt"
hi
hi again
```

Since there is no way to create a Python identifier for every possible
executable that could be run, users can also type their own shell prompt:
`Ṩ +`. Note that this isn't a dollar sign, but is rather a Latin capital
letter S with dot below and dot above (`U+1E68`), since that is the closest
valid Python identifier I could get to the traditional `$` dollar sign. Since
`Ṩ` is difficult to type, `S` is also available as a substitute.

```py
>>> Ṩ + "uname"
Linux
```

Because of Python's order of operations, you need to group arguments for
commands within a `tuple` or `list` for everything after the first command
in a pipeline if the first argument isn't a variable.

```py
>>> cat + "README.md" | ("head", "-n", "5")
# Concussion Shell

It's kinda like Bash except it causes severe brain damage because it's actually
a Python REPL.
```

## Known issues

* Currently all stderr goes directly to this process's stderr, and it cannot be
  redirected. Maybe I'll implement this at some point.

* Currently no support for executing tasks asynchronously. Perhaps I could use
  `β` to signify this since it looks kinda like an `&` but is a valid
  identifier.

* Pipes break frequently. I think there's a bug somewhere in the code for
  handling this but I don't know what.

* Many programs don't work nicely because they think they're not running in a
  terminal.
