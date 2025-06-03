# objective

This readme states/explains the context or purpose of the current branch. as this projects does branch off a lot and branches may be unrelated to the main project (e.g. da).

## current branch
- tai-0-original

Starting point for this task.


## coding notes
- the response uses the actual project configs (/ProjectL/configs.yaml) instead of tests configs under /tests
- paths are hardcoded to local /tmp/... stuff instead of being relative and thus need to be edited to actually be used
- The logic is very poor with regards to the acceptable layouts. There are 64 valid layouts for the corners_3 piece specified within a 5x5 grid. 
- The model is right in saying the current implementation does not add rotation layouts when it generates its cube. However, hardcoding the translation-only test isn't the best answer
- Many tests are duplicated or redundant: the model checks multiple times the size of the cube
- The model re-wrote a suite to run all tests. It would be better to use unittest's built-in discovery features for this, rather than add another structure to maintain.
- unittest.makeSuite is deprec in python 3.13, thus had to re-write to use the unittest.TestLoader().loadTestsFromTestCase(...) instead.


## prompt
I want to test the configuration & layout aspects of this project. More specifically, I need to ensure that the method `Piece.generate_cube()` works as intended in generating valid configurations. I want you to add unit tests to validate this. Use the piece `corner_3` from the configs to test this. The generated cube outputted should meet the following criteria:

1 - contains ONLY valid layout, which means the entire piece must fit within the 5x5 matrice
2 - contains ALL valid layouts, which means that all translations AND rotations of a piece must be produced
3 - along axis 0 of the cube, each slice must contain a valid layout
4 - there must be no duplicates along axis 0

Write the unit tests necessary to validate this. You will likely need to produce a valid cube to test against (e.g. the "solution" numpy array for this specific piece), unless you can come up with a better way to do this.

Your answer should fit within the existing test folder & approach so that it is possible to run existing tests & any tests you write as a comprehensive test suit.

Structure your answer so that it is relatively straightforward to extend the cube unit test to any other pieces later on.


## Projet TODO
- tests for the configuration/layout of pieces
