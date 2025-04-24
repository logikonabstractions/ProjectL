import unittest
import numpy as np
from tests.test_base import BaseTest

from ProjectL.pieces import Piece, PieceSquare


class TestPiece(BaseTest):
    """Test cases for the Piece class"""
    
    def setUp(self):
        """Set up test fixtures before each test"""
        super().setUp()
        self.square_piece_config = {
            "name": "square_1", 
            "level": 1, 
            "shape": [[1, 0, 0, 0, 0], 
                      [0, 0, 0, 0, 0], 
                      [0, 0, 0, 0, 0], 
                      [0, 0, 0, 0, 0], 
                      [0, 0, 0, 0, 0]]
        }
        self.l_shape_piece_config = {
            "name": "L_shape_2", 
            "level": 2, 
            "shape": [[1, 0, 0, 0, 0],
                      [1, 0, 0, 0, 0],
                      [1, 1, 0, 0, 0],
                      [0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0]]
        }
        
        # Initialize pieces
        self.square_piece = Piece(configs=self.square_piece_config)
        self.l_shape_piece = Piece(configs=self.l_shape_piece_config)
    
    def test_piece_initialization(self):
        """Test that a piece is correctly initialized from configs"""
        self.assertEqual(self.square_piece.name, "square_1")
        self.assertEqual(self.square_piece.level, 1)
        self.assertTrue(np.array_equal(self.square_piece.shape, np.array(self.square_piece_config["shape"])))
        
        self.assertEqual(self.l_shape_piece.name, "L_shape_2")
        self.assertEqual(self.l_shape_piece.level, 2)
        self.assertTrue(np.array_equal(self.l_shape_piece.shape, np.array(self.l_shape_piece_config["shape"])))
    
    def test_generate_cube(self):
        """Test that cube generation produces a valid 3D array"""
        # Verify cube dimensions
        self.assertIsInstance(self.square_piece.cube, np.ndarray)
        self.assertEqual(len(self.square_piece.cube.shape), 3)
        
        # Verify first configuration matches original shape
        self.assertTrue(np.array_equal(self.square_piece.cube[0], self.square_piece.shape))
        
        # Verify configurations are valid (sum of 1s remains constant)
        expected_sum = np.sum(self.square_piece.shape)
        for i in range(self.square_piece.cube.shape[0]):
            self.assertEqual(np.sum(self.square_piece.cube[i]), expected_sum)
    
    def test_piece_square_subclass(self):
        """Test the PieceSquare subclass"""
        square = PieceSquare()
        
        # Verify initialization
        self.assertEqual(square.name, "square_1")
        self.assertEqual(square.level, 1)
        self.assertTrue(np.array_equal(square.shape, np.array([[1, 0, 0, 0, 0],
                                                             [0, 0, 0, 0, 0],
                                                             [0, 0, 0, 0, 0], 
                                                             [0, 0, 0, 0, 0],
                                                             [0, 0, 0, 0, 0]])))
        
        # Verify cube generation
        self.assertIsNotNone(square.cube)
        self.assertGreater(len(square.configurations_array), 0)


if __name__ == '__main__':
    unittest.main()
