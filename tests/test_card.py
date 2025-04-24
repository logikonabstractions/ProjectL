import unittest
import numpy as np
from tests.test_base import BaseTest

from ProjectL.card import Card, Reward
from ProjectL.pieces import PieceSquare


class TestCard(BaseTest):
    """Test cases for the Card class"""
    
    def setUp(self):
        """Set up test fixtures before each test"""
        super().setUp()
        self.test_card_config = {
            "mask": [[False, False, True, True, False],
                     [True, True, True, True, True],
                     [False, False, True, True, False],
                     [False, False, False, False, False],
                     [False, False, False, False, False]],
            "reward": {"points": 1, "piece": None}
        }
        
        # Initialize test card
        self.test_card = Card(configs=self.test_card_config)
        
        # Create a test piece configuration for placing
        self.test_piece_config = np.zeros((5, 5), dtype=int)
        self.test_piece_config[1, 2] = 1  # A single block in a valid position
        
        self.invalid_piece_config = np.zeros((5, 5), dtype=int)
        self.invalid_piece_config[0, 0] = 1  # A single block in an invalid position
    
    def test_card_initialization(self):
        """Test that a card is correctly initialized from configs"""
        self.assertTrue(np.array_equal(self.test_card.mask, np.array(self.test_card_config["mask"])))
        self.assertEqual(self.test_card.reward.points, 1)
        # The default behavior creates a PieceSquare when piece is None
        self.assertIsInstance(self.test_card.reward.piece, PieceSquare)
        self.assertTrue(np.all(self.test_card.layout == 0))  # Layout should be empty initially
    
    def test_placement_valid(self):
        """Test that valid piece placement is correctly identified"""
        # Valid placement
        self.assertTrue(self.test_card.placement_valid(self.test_piece_config))
        
        # Invalid placement (outside mask)
        self.assertFalse(self.test_card.placement_valid(self.invalid_piece_config))
        
        # Invalid placement (double occupation)
        self.test_card.layout[1, 2] = 1  # Occupy the same position
        self.assertFalse(self.test_card.placement_valid(self.test_piece_config))
    
    def test_place_piece(self):
        """Test that a piece can be placed on a card"""
        # Place a valid piece
        result = self.test_card.place_piece(self.test_piece_config)
        self.assertTrue(result)
        self.assertEqual(self.test_card.layout[1, 2], 1)
        
        # Try to place an invalid piece
        result = self.test_card.place_piece(self.invalid_piece_config)
        self.assertFalse(result)
        
        # Try to place a piece on an occupied position
        result = self.test_card.place_piece(self.test_piece_config)
        self.assertFalse(result)
    
    def test_reward_class(self):
        """Test the Reward class"""
        # Test default initialization
        default_reward = Reward()
        self.assertEqual(default_reward.points, 0)
        self.assertIsInstance(default_reward.piece, PieceSquare)
        
        # Test custom initialization
        custom_piece = PieceSquare()
        custom_reward = Reward(points=5, piece=custom_piece)
        self.assertEqual(custom_reward.points, 5)
        self.assertEqual(custom_reward.piece, custom_piece)


if __name__ == '__main__':
    unittest.main()
