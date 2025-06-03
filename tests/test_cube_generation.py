import unittest
import numpy as np
import yaml
import os
import sys
from parameterized import parameterized

# Add the project root directory to path to allow imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ProjectL.classes import Piece


class TestCubeGeneration(unittest.TestCase):
    def setUp(self):
        """Load configuration for all pieces"""
        with open("configs.yaml", 'r') as file:
            self.configs = yaml.safe_load(file)

        self.all_pieces = self.configs["pieces"]

    def _get_piece_config(self, piece_name):
        """Helper method to get piece configuration by name"""
        return next((piece for piece in self.all_pieces if piece["name"] == piece_name), None)

    def _get_expected_layouts_count(self, piece_name):
        """Return the expected number of layouts for each piece type"""
        # This mapping can be extended as needed for new piece types
        layout_counts = {
            "square_1": 1,  # 1x1 square: just 1 layout
            "line_2": 8,  # 2x1 line: 2 rotations × 4 positions each = 8
            "corner_3": 8,  # L-shape: 2 rotations × 4 positions each = 8
            "line_3": 8,  # 3x1 line: 2 rotations × 4 positions each = 8
            "big_square_4": 4,  # 2x2 square: 1 rotation × 4 positions = 4
            "line_4": 8,  # 4x1 line: 2 rotations × 4 positions each = 8
            "l_shape_4": 8,  # L-shape with longer arm: 2 rotations × 4 positions each = 8
        }
        return layout_counts.get(piece_name, 0)

    def _get_expected_piece_size(self, piece_name):
        """Return the expected number of cells in the piece"""
        # Map piece names to their sizes (number of 1s in the matrix)
        sizes = {
            "square_1": 1,
            "line_2": 2,
            "corner_3": 3,
            "line_3": 3,
            "big_square_4": 4,
            "line_4": 4,
            "l_shape_4": 4,
        }
        return sizes.get(piece_name, 0)

    @parameterized.expand([
        ("corner_3",),
        ("square_1",),
        ("line_2",),
        # Add more pieces as needed
    ])
    def test_cube_dimensions(self, piece_name):
        """Test that the cube has correct dimensions for each piece"""
        piece_config = self._get_piece_config(piece_name)
        self.assertIsNotNone(piece_config, f"{piece_name} configuration not found")

        piece = Piece(piece_config)

        # Check that cube was generated
        self.assertIsNotNone(piece.cube, f"Cube not generated for {piece_name}")

        # Check dimensions
        num_layouts, rows, cols = piece.cube.shape

        self.assertEqual(rows, 5, f"{piece_name} cube should have 5 rows")
        self.assertEqual(cols, 5, f"{piece_name} cube should have 5 columns")

        # Check number of layouts
        expected_count = self._get_expected_layouts_count(piece_name)
        self.assertEqual(num_layouts, expected_count,
                         f"Expected {expected_count} layouts for {piece_name}, got {num_layouts}")

    @parameterized.expand([
        ("corner_3",),
        ("square_1",),
        ("line_2",),
        # Add more pieces as needed
    ])
    def test_valid_layouts(self, piece_name):
        """Test that each layout in the cube is valid"""
        piece_config = self._get_piece_config(piece_name)
        piece = Piece(piece_config)

        expected_size = self._get_expected_piece_size(piece_name)
        num_layouts = piece.cube.shape[0]

        for i in range(num_layouts):
            layout = piece.cube[i]

            # Check that layout fits within 5x5 grid
            self.assertEqual(layout.shape, (5, 5), f"Layout {i} has incorrect shape")

            # Check that layout only contains 0s and 1s
            values = np.unique(layout)
            self.assertTrue(np.all(np.isin(values, [0, 1])),
                            f"Layout {i} contains values other than 0 or 1: {values}")

            # Check the piece size
            piece_sum = np.sum(layout)
            self.assertEqual(piece_sum, expected_size,
                             f"Layout {i} has invalid total: {piece_sum} (expected {expected_size})")

    @parameterized.expand([
        ("corner_3",),
        ("square_1",),
        ("line_2",),
        # Add more pieces as needed
    ])
    def test_no_duplicates(self, piece_name):
        """Test that there are no duplicate layouts in the cube"""
        piece_config = self._get_piece_config(piece_name)
        piece = Piece(piece_config)

        num_layouts = piece.cube.shape[0]

        # Compare each layout with all other layouts
        for i in range(num_layouts):
            for j in range(i + 1, num_layouts):
                layout_i = piece.cube[i]
                layout_j = piece.cube[j]

                # Check that layouts are not identical
                self.assertFalse(np.array_equal(layout_i, layout_j),
                                 f"Duplicate layouts found at indices {i} and {j}")

    @parameterized.expand([
        ("corner_3",),
        ("square_1",),
        ("line_2",),
        # Add more pieces as needed
    ])
    def test_proper_alignment(self, piece_name):
        """Test that pieces are properly aligned to grid bounds"""
        piece_config = self._get_piece_config(piece_name)
        piece = Piece(piece_config)

        num_layouts = piece.cube.shape[0]

        for i in range(num_layouts):
            layout = piece.cube[i]

            # A valid layout should have at least one 1 in either the first row or first column
            first_row_has_one = np.any(layout[0, :] == 1)
            first_col_has_one = np.any(layout[:, 0] == 1)

            self.assertTrue(first_row_has_one or first_col_has_one,
                            f"Layout {i} for {piece_name} doesn't have any 1s in first row or column")

    def test_corner_3_specific_layouts(self):
        """Additional test for corner_3 piece to check correct layouts are generated"""
        piece_config = self._get_piece_config("corner_3")
        piece = Piece(piece_config)

        # Expected unique layouts for corner_3
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

        # Check that all expected layouts exist in the cube
        actual_count = piece.cube.shape[0]

        for expected_layout in expected_layouts:
            layout_found = False
            for i in range(actual_count):
                actual_layout = piece.cube[i]
                if np.array_equal(actual_layout, expected_layout):
                    layout_found = True
                    break
            self.assertTrue(layout_found, f"Expected layout not found in cube:\n{expected_layout}")


if __name__ == '__main__':
    unittest.main()
