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
        with open("tests/test_configs_cube.yaml", 'r') as file:
            self.configs = yaml.safe_load(file)

        # Get the corner_3 piece configuration
        self.corner_3_config = next((piece for piece in self.configs["pieces"] if piece["name"] == "corner_3"), None)
        self.solutions = self.corner_3_config["solutions"]
        self.assertIsNotNone(self.corner_3_config, "corner_3 piece config not found")

        # Create a Piece instance with the corner_3 configuration
        self.piece = Piece(self.corner_3_config)

    def test_generate_cube_produces_valid_layouts(self):
        """Test that each layout in the cube is valid (fits within 5x5 matrix)"""
        # Ensure cube was generated
        self.assertIsNotNone(self.piece.cube, "Cube was not generated")

        # Get the dimensions of the cube
        num_configurations, rows, cols = self.piece.cube.shape

        # Check that each layout fits within the 5x5 grid
        for i in range(num_configurations):
            layout = self.piece.cube[i]

            # Check that the layout only contains 0s and 1s
            values = np.unique(layout)
            self.assertTrue(np.all(np.isin(values, [0, 1])),
                            f"Layout {i} contains values other than 0 or 1: {values}")

            # Calculate the sum to ensure it matches the expected piece size (3 for corner_3)
            piece_sum = np.sum(layout)
            self.assertEqual(piece_sum, self.solutions["piece_size"], f"Layout {i} has invalid total: {piece_sum} (expected {self.solutions["piece_size"]})")

    def test_validate_cube_configurations_sum(self):
        """Summing the cube for a piece along axis 0 should yield specific integers at each position
            The expected sum is provided as check in the config file
        """

        expected_sum_matrix = np.array(self.solutions["configuration_sum"])
        actual_sum_matrix = np.sum(self.piece.cube, axis=0)

        self.assertEqual(expected_sum_matrix.tobytes(), actual_sum_matrix.tobytes() ,
                         f"Expected {expected_sum_matrix} unique layouts, but got {actual_sum_matrix}")


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

if __name__ == '__main__':
    unittest.main()
