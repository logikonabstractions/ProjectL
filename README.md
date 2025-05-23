# objective

This readme states/explains the context or purpose of the current branch. as this projects does branch off a lot and branches may be unrelated to the main project (e.g. da).

## current branch
- this branch focuses on raven - evaluate 2 models
- projectl_raven_0_da for da model

## coding notes
- had to change the Dockerfile -- it wouldn't build with numpy in, seems to be lack of c compiler. So had to install those dependancies....
- It would be better to have the loggin setup in utils.py, as this is what that's for, and then call that instead of having it in main.py, since test suites cannot run as provided.
- also set the config for rotating files etc... in the configs not hardcoded
- possibly also 

## DA model - errors in code
- seems to have set FULL_DEBUG as a "global" variable in main.py but it's not actually global elsewhere in the code, so runtime error
- the way the code snippet was structured, it seems it omitted a section in main.py which would have resulted in the code not having the path to the configs.yaml file. I gave the model the benefit of the doubt and assumed that instead of leaving that top of the file where FULL_DEBUG is defined, it just replaced it further down, within a section `existing code here`
- the model replaced the named argument in `Player.__init__(name, cards,...)` with a generic *args, **kwargs, which resulted in runtime error.
- The model seems to have omitted a large chunk of code between lines ~115 in game_objects.py (the rest of the Player methods, below play_turn()), including the full `class Strategy` from which all strategy inherits. At the very least, this is utterly ambiguous, minimally there would need to be a comments `existing code here`. This makes the code very unusable.
- Assuming the previous issues is really just a missing `existing code here` that's missing, the better way to manage the logger would have been in the parent class, instead of re-implementing in every child class's `__init__`
- in `Action.__init__(...)` it again re-wrote the method with generic *args, **kwargs which results in runtime error.
- The model misunderstood the logic of most of the `Action.is_action_valid(...)` implementations, since it assumes that a boolean is set early in the method and that the variable can just be returned after a series of logging statements. However in many cases, the logic is built so that if a conclusion is reach, the returned False/True is returned in-place. So the implementation is recommanded would be rather tedious and error-prone to implement.
- I have not implement the logging as described in all the classes, since it is very clear that numerous runtime errors would prevent the approach from being runnable. There is enough to show what the implementation the model recommanded looks like.

## prompt

You need to add proper logging functionalities for this code and ensure no print statement remain.  The objective is to have logging modes that are configurable from the config file.

- Full debut mode: should allow us to inspect the logs and understand the chain of events in the game, tracing back potential logical/game mechanics issues.
- Detailed mode: provides a fairly detailed trace, but we don't want endless lines printed from within loops. It should provide more information that Normal Mode, but should still read fairly easily.
- Normal mode: Provides just the outline of what is happening in the game; this should read as-if a narrator would explain the main game events as they happened. The reader would be able to know who played what at a high level.

For Full Debug, still try to maintain a balance between making debugging easy, but also keeping the amount of log output manageable.

In all modes, the log should be outputted to console, but also to a file. The filename should include relevant information and be human-readable, but also provide a unique ID.

Some sensible log rotation system (for files) must be implemented.

You are free to choose the specific output structure of those logs.