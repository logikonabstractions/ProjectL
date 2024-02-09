import os
import unittest
import yaml
import ProjectL
from ProjectL.actions import *

class TestPieces(unittest.TestCase):
    # def __init__(self):
    #     super().__init__()

    def setUp(self):
        """Initialize before every test."""
        file_path = os.path.dirname(os.path.realpath(__file__))
        # parent_dir = os.path.dirname(dir_path)  # since configs are in project root
        file_path = os.path.join(file_path, 'configs_tests.yaml')
        with open(file_path, 'r') as file:
            # Parse YAML content
            confs = yaml.safe_load(file)
            self.configs = confs["pieces"]
            
        self.solutions = {"square_1": np.ones(shape=(5,5), dtype=int),
            "line_2":[[1, 1, 1, 1, 1], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2], [1, 1, 1, 1, 1], ],
            "corner_3":[[1, 1, 1, 1, 0], [2, 3, 3, 3, 1], [2, 3, 3, 3, 1], [2, 3, 3, 3, 1], [1, 2, 2, 2,1]],
            "line_3":[[1, 1, 1, 1, 1], [2, 2, 2, 2, 2], [3, 3, 3, 3, 3], [2, 2, 2, 2, 2], [1, 1, 1, 1, 1],] }

    def test_PieceSquare(self):
        """ The square should produce a cube where each position is occupied once and only once.
            
            We assess this by summing along the z-axis the cube.
        """
        piece = PieceSquare()
        summed_matrix = np.sum(piece.cube, axis=0)
        self.assertTrue(np.array_equal(self.solutions["square_1"], summed_matrix))

    def test_line_2(self):
        """ """
        p = next((d for d in self.configs if d.get('name') == 'line_2'), None)
        piece = Piece(configs=p)
        summed_matrix = np.sum(piece.cube, axis=0)
        self.assertTrue(np.array_equal(self.solutions["line_2"], summed_matrix))

    def test_corner_3(self):
        """ """
        p = next((d for d in self.configs if d.get('name') == 'corner_3'), None)
        piece = Piece(configs=p)
        summed_matrix = np.sum(piece.cube, axis=0)
        self.assertTrue(np.array_equal(self.solutions["corner_3"], summed_matrix))

    def test_line_3(self):
        """ """
        p = next((d for d in self.configs if d.get('name') == 'line_3'), None)
        piece = Piece(configs=p)
        summed_matrix = np.sum(piece.cube, axis=0)
        self.assertTrue(np.array_equal(self.solutions["line_3"], summed_matrix))


if __name__ == '__main__':
    unittest.main()