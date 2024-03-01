# Pysh

It's kinda like Bash but it's actually Python, and it is horrific and will cause permanent brain damage.

## How it works

* Horrific operator overloads

* Since Python doesn't support building commands from adjacent identifiers,
  Pysh uses the `+` operator to join arguments for a command.

* Since the commands can't be executed while they're being constructed,
  commands are instead executed when stringified, but only if the object hasn't
  been operated upon (ie piped to another command).

* Some commands are shell-builtins, which are provided as commands that can be
  executed.

* Since there is no way to create a Pysh command for every possible executable
  that could be run, users must instead type their own shell prompt: `Ṩ +`.
  Note that this isn't a dollar sign, but is rather a Latin capital letter S
  with dot below and dot above (`U+1E68`), since that is the closest I could
  get to the traditional `$` dollar sign.

* Similarly, to execute a task asynchronously, users must use a `+ β`, since
  `&` is not a valid Python identifier, and this was the most similar looking
  character that is still a valid Python identifier.

* Because `&&` and `||` are not supported in Python, use the `and` and `or`
  keywords instead.

## Unimplemented features

* Currently all stderr goes directly to this process's stderr, and it cannot be
  redirected. Maybe I'll implement this at some point.
