# ProjectL Integration Test

This directory contains integration tests for the ProjectL game. The integration test validates that the game mechanics run properly from start to finish.

## Files

- `test_game_integration.py`: Contains the unittest-based integration test for ProjectL
- `run_integration_test.py`: A helper script to run the integration tests

## Running the Integration Test

To run the integration test, follow these steps:

1. Ensure that you have Python installed (Python 3.6 or higher is recommended)
2. Make sure you have the required dependencies installed:
   ```
   pip install -r requirements.txt
   ```
3. Run the integration test using the provided runner script:
   ```
   python run_integration_test.py
   ```

Alternatively, you can run the tests directly using the unittest framework:
```
python -m unittest test_game_integration.py
```

## Test Structure

The `TestGameIntegration` class contains the following test methods:

1. `test_game_initialization`: Verifies that the game initializes correctly with proper configuration.
2. `test_player_initialization`: Ensures players are initialized with correct names and initial state.
3. `test_single_turn_execution`: Tests that a single turn (both players playing) executes correctly.
4. `test_game_completion`: Validates that the game completes after the maximum number of turns.
5. `test_piece_placement`: Checks that placing pieces on cards works correctly.
6. `test_take_card_action`: Ensures that taking a card action works as expected.
7. `test_take_piece_action`: Verifies that taking a piece action works properly.

## Notes

- The tests use mocking to avoid certain behaviors that could interfere with test execution.
- Some tests are limited by the design of the code being tested (e.g., the `run()` method in `GameManager` which doesn't provide a clean way to test individual turns).
- The integration test validates the core game mechanics without testing the visualization or UI components.
