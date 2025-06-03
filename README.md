# objective

This readme states/explains the context or purpose of the current branch. as this projects does branch off a lot and branches may be unrelated to the main project (e.g. da).

## current branch
- tai-0-original

Starting point for this task.


## coding notes
- sourcing the test configs from a dedicated tests/test_configs_cubes.yaml instead of the production configs.yaml
- added the solutions to the tests for difference pieces configuration, so we can validate code outputs against known expected value that we can update from the test configs (instead of having to edit the test suite itself)
  - this is under the "solution" key for each piece configuration in test_configs_cubes.yaml
- remove irrelevant tests ("test_cube_boundary_conditions" for example)
- improved inefficient tests, which I replaced with "test_validate_cube_configurations_sum". The sum of position at each (x,y) position along the z axis (axis 0) leaves a specific trace for each cube, given a specific piece
- remove redundant tests given above improvements (test_generate_cube_produces_all_valid_layouts, test_each_slice_contains_valid_layout)

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
