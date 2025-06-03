import unittest
import numpy as np
import yaml
import os
import sys

# Add the project root directory to path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ProjectL.classes import Piece


class TestPiece(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures, loading the corner_3 piece config"""
        with open("configs.yaml", 'r') as file:
            self.configs = yaml.safe_load(file)

        # Get the corner_3 piece configuration
        self.corner_3_config = next((piece for piece in self.configs["pieces"] if piece["name"] == "corner_3"), None)
        self.assertIsNotNone(self.corner_3_config, "corner_3 piece config not found")

        # Create a Piece instance with the corner_3 configuration
        self.piece = Piece(self.corner_3_config)

    def test_generate_cube_produces_valid_layouts(self):
        """Test that each layout in the cube is valid (fits within 5x5 matrix)"""
        # Ensure cube was generated
        self.assertIsNotNone(self.piece.cube, "Cube was not generated")

        # Get the dimensions of the cube
        num_layouts, rows, cols = self.piece.cube.shape

        # Check the dimensions are correct
        # TODO: # of expected layout should be here and loaded in testconfigs.yaml as valid answers to check against
        self.assertEqual(rows, 5, "Cube should have 5 rows")
        self.assertEqual(cols, 5, "Cube should have 5 columns")

        # Check that each layout fits within the 5x5 grid
        for i in range(num_layouts):
            layout = self.piece.cube[i]

            # Check that the piece doesn't extend beyond the boundary
            # TODO: remove
            self.assertEqual(layout.shape, (5, 5), f"Layout {i} has incorrect shape")

            # Check that the layout only contains 0s and 1s
            values = np.unique(layout)
            self.assertTrue(np.all(np.isin(values, [0, 1])),
                            f"Layout {i} contains values other than 0 or 1: {values}")

            # Calculate the sum to ensure it matches the expected piece size (3 for corner_3)
            piece_sum = np.sum(layout)
            self.assertEqual(piece_sum, 3, f"Layout {i} has invalid total: {piece_sum} (expected 3)")

    def test_generate_cube_produces_all_valid_layouts(self):
        """Test that all valid translations and rotations are generated"""
        # For corner_3 piece, we know there should be 8 unique valid layouts:
        # 2 rotations × 4 positions each = 8 total

        expected_count = 8
        actual_count = self.piece.cube.shape[0]

        self.assertEqual(actual_count, expected_count,
                         f"Expected {expected_count} unique layouts, but got {actual_count}")

        # TODO: this is false, very poor logic
        # The "correct" layouts for corner_3 can be algorithmically determined
        # For simplicity, let's manually define the expected layouts
        expected_layouts = [
            # Original L-shape
            np.array([[1, 0, 0, 0, 0],
                      [1, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]),
            # Shifted right once
            np.array([[0, 1, 0, 0, 0],
                      [0, 1, 1, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]),
            # Shifted right twice
            np.array([[0, 0, 1, 0, 0],
                      [0, 0, 1, 1, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]),
            # Shifted right three times
            np.array([[0, 0, 0, 1, 0],
                      [0, 0, 0, 1, 1],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]),
            # Rotated 90° (upside-down L)
            np.array([[1, 1, 0, 0, 0],
                      [1, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]),
            # Shifted right once
            np.array([[0, 1, 1, 0, 0],
                      [0, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]),
            # Shifted right twice
            np.array([[0, 0, 1, 1, 0],
                      [0, 0, 1, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]),
            # Shifted right three times
            np.array([[0, 0, 0, 1, 1],
                      [0, 0, 0, 1, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]),
        ]

        # todo: acceptable logic, just correct the references above
        # Check that all expected layouts exist in the cube
        for expected_layout in expected_layouts:
            layout_found = False
            for i in range(actual_count):
                actual_layout = self.piece.cube[i]
                if np.array_equal(actual_layout, expected_layout):
                    layout_found = True
                    break
            self.assertTrue(layout_found, f"Expected layout not found in cube:\n{expected_layout}")

    def test_each_slice_contains_valid_layout(self):
        """Test that along axis 0, each slice contains a valid layout"""
        # Ensure cube was generated
        self.assertIsNotNone(self.piece.cube, "Cube was not generated")

        num_layouts = self.piece.cube.shape[0]

        for i in range(num_layouts):
            layout = self.piece.cube[i]

            # Check that the layout is valid for the game
            # A valid layout must have:
            # - All 1s connected
            # - No 1s hanging outside the 5x5 area
            # - The piece structure preserved

            # For corner_3, sum should be 3
            self.assertEqual(np.sum(layout), 3, f"Layout {i} doesn't contain the right number of cells")

            # TODO: remove
            # Check that there are no 1s in the last column when the piece is at the left edge
            if layout[0, 0] == 1 or layout[1, 0] == 1:
                self.assertEqual(np.sum(layout[:, 4]), 0,
                                 f"Layout {i} has pieces in both first and last column")

            # TODO: remove, useless
            # Check that at least one element in the layout is 1
            self.assertGreater(np.sum(layout), 0, f"Layout {i} is empty")

            # TODO: remove, useless
            # Check that the shape is preserved (L-shape for corner_3)
            # This can be complex to validate for all shape types, but for corner_3:
            if layout[0, 0] == 1 and layout[1, 0] == 1:
                self.assertEqual(layout[1, 1], 1, "L-shape is malformed")
            # Similar checks for other orientations

    # TODO: byte-array approach is much more efficient
    def test_no_duplicates_along_axis_0(self):
        """Test that there are no duplicate layouts along axis 0"""
        # Ensure cube was generated
        self.assertIsNotNone(self.piece.cube, "Cube was not generated")

        num_layouts = self.piece.cube.shape[0]

        # Compare each layout with all other layouts
        for i in range(num_layouts):
            for j in range(i + 1, num_layouts):
                layout_i = self.piece.cube[i]
                layout_j = self.piece.cube[j]

                # Check that layouts are not identical
                self.assertFalse(np.array_equal(layout_i, layout_j),
                                 f"Duplicate layouts found at indices {i} and {j}")

    # TODO: remove, actually not a condition we need to meet
    def test_cube_boundary_conditions(self):
        """Test boundary conditions for the generated cube"""
        # Ensure cube was generated
        self.assertIsNotNone(self.piece.cube, "Cube was not generated")

        num_layouts = self.piece.cube.shape[0]

        # Check that each layout has at least one 1 in the first row or column
        # This ensures that pieces are properly aligned to the grid bounds
        for i in range(num_layouts):
            layout = self.piece.cube[i]

            # A valid layout should have at least one 1 in either the first row or first column
            first_row_has_one = np.any(layout[0, :] == 1)
            first_col_has_one = np.any(layout[:, 0] == 1)

            self.assertTrue(first_row_has_one or first_col_has_one,
                            f"Layout {i} doesn't have any 1s in first row or column")


if __name__ == '__main__':
    unittest.main()
