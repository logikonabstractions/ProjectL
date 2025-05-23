# objective

This readme states/explains the context or purpose of the current branch. as this projects does branch off a lot and branches may be unrelated to the main project (e.g. da).

## current branch
- this branch focuses on raven - evaluate 2 models
- projectl_raven_0_model_sonnet for the sonnet answer

## coding notes
- had to change the Dockerfile -- it wouldn't build with numpy in, seems to be lack of c compiler. So had to install those dependancies....
- minor: the name of the logger should be defined in configs.yaml, so that different logger may be configured as the application grows
- minor: The way the partial update for `GameManager` is presented for `game_objects.py` is somewhat ambiguous and should be clearer. The imports which are top of file in python are presented directly abovbe the `GameManager` class, but in reality the `GameState` class is between...

## prompt

You need to add proper logging functionalities for this code and ensure no print statement remain.  The objective is to have logging modes that are configurable from the config file.

- Full debut mode: should allow us to inspect the logs and understand the chain of events in the game, tracing back potential logical/game mechanics issues.
- Detailed mode: provides a fairly detailed trace, but we don't want endless lines printed from within loops. It should provide more information that Normal Mode, but should still read fairly easily.
- Normal mode: Provides just the outline of what is happening in the game; this should read as-if a narrator would explain the main game events as they happened. The reader would be able to know who played what at a high level.

For Full Debug, still try to maintain a balance between making debugging easy, but also keeping the amount of log output manageable.

In all modes, the log should be outputted to console, but also to a file. The filename should include relevant information and be human-readable, but also provide a unique ID.

Some sensible log rotation system (for files) must be implemented.

You are free to choose the specific output structure of those logs.