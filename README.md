# Concussion Shell

It's kinda like Bash except it causes severe brain damage because it's actually
a Python REPL.

## Usage

```txt
$ pip install concussion
$ concussion
>>> Ṩ + "cat" + "README.md" | ("head", "-n", "5")
# Concussion Shell

It's kinda like Bash except it causes severe brain damage because it's actually
a Python REPL.
```

## How it works

Everything is implemented using horrific operator overloads.

Since the commands can't be executed while they're being constructed, commands
are instead executed when stringified using `repr()`, which works nicely with
Python's interactive console.

Since there is no way to create a Python identifier for every possible
executable that could be run, users must instead type their own shell prompt:
`Ṩ +`. Note that this isn't a dollar sign, but is rather a Latin capital
letter S with dot below and dot above (`U+1E68`), since that is the closest
valid Python identifier I could get to the traditional `$` dollar sign. Since
`Ṩ` is difficult to type, `S` is also available as a substitute.

```py
>>> Ṩ + "uname"
Linux
```

Python doesn't support building commands from adjacent identifiers, so
Concussion uses the `+` operator to join arguments for a command.

```py
>>> Ṩ + "echo" + "hello" + "world"
hello world
```

You can pipe commands using the standard `|` pipe operator.

```py
>>> Ṩ + "ls" + "-l" | "less"
# less is broken because I can't be bothered to make my shell look like a TTY
# so this output is invalid
```

Because of Python's order of operations, you need to group arguments for
commands within a `tuple` or `list` for everything after the first command
in a pipeline.

```py
>>> Ṩ + "cat" + "README.md" | ("head", "-n", "5")
# Concussion Shell

It's kinda like Bash except it causes severe brain damage because it's actually
a Python REPL.
```

Some commands such as `cd` and `pwd` are shell-builtins, which are provided as
commands that can be executed directly for simplicity.

```py
>>> cd + "/home/migue/concussion"
>>> pwd
/home/migue/concussion
```

To create shell aliases, you simply use Python variable assignments

```py
>>> # This makes for an epic prank
>>> bash = Ṩ + "concussion"
>>> bash
Concussion shell...
```

Because `&&` and `||` are not supported in Python, use the `and` and `or`
keywords instead.

```py
>>> S + "false" or S + "echo" + "hi"
>>> S + "false" and S + "echo" + "hi"
hi
>>> S + "true" or S + "echo" + "hi"
hi
>>> S + "true" and S + "echo" + "hi"
```

## Unimplemented features

* Currently all stderr goes directly to this process's stderr, and it cannot be
  redirected. Maybe I'll implement this at some point.

* Currently no support for executing tasks asynchronously. Perhaps I could use
  `β` to signify this since it looks kinda like an `&` but is a valid
  identifier.
