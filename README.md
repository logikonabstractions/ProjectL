# objective

This readme states/explains the context or purpose of the current branch. as this projects does branch off a lot and branches may be unrelated to the main project (e.g. da).

## current branch
- this branch focuses on raven - evaluate 2 models
- projectl_raven_0 as we are allowed to reuse for different prompt a given codebase

## prompt

You need to add proper logging functionalities for this code and ensure no print statement remain.  The objective is to have logging modes that are configurable from the config file.

- Full debut mode: should allow us to inspect the logs and understand the chain of events in the game, tracing back potential logical/game mechanics issues.
- Detailed mode: provides a fairly detailed trace, but we don't want endless lines printed from within loops. It should provide more information that Normal Mode, but should still read fairly easily.
- Normal mode: Provides just the outline of what is happening in the game; this should read as-if a narrator would explain the main game events as they happened. The reader would be able to know who played what at a high level.

For Full Debug, still try to maintain a balance between making debugging easy, but also keeping the amount of log output manageable.

In all modes, the log should be outputted to console, but also to a file. The filename should include relevant information and be human-readable, but also provide a unique ID.

Some sensible log rotation system (for files) must be implemented.

You are free to choose the specific output structure of those logs.