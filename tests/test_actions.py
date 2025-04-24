import unittest
import numpy as np
from tests.test_base import BaseTest

from ProjectL.actions import Action, TakePiece, PlacePiece, TakeCard
from ProjectL.card import Card
from ProjectL.pieces import PieceSquare


class TestActions(BaseTest):
    """Test cases for the Action classes"""
    
    def setUp(self):
        """Set up test fixtures before each test"""
        super().setUp()
        self.test_piece = PieceSquare()
        self.test_card = Card()
        self.test_pieces = [self.test_piece]
        self.test_cards = [self.test_card]
    
    def test_base_action(self):
        """Test the base Action class"""
        action = Action(piece=self.test_piece, card=self.test_card, pieces=self.test_pieces, cards=self.test_cards)
        self.assertEqual(action.desc, "action")
        self.assertEqual(action.piece, self.test_piece)
        self.assertEqual(action.card, self.test_card)
        self.assertEqual(action.pieces, self.test_pieces)
        self.assertEqual(action.cards, self.test_cards)
        self.assertFalse(action.is_action_valid())
    
    def test_take_piece_action(self):
        """Test the TakePiece action"""
        action = TakePiece(pieces=self.test_pieces)
        
        # Test validity
        self.assertTrue(action.is_action_valid())
        
        # Test performing action
        initial_piece_count = len(self.test_pieces)
        action.perform_action()
        self.assertEqual(len(self.test_pieces), initial_piece_count + 1)
        self.assertIsInstance(self.test_pieces[-1], PieceSquare)
    
    def test_place_piece_action(self):
        """Test the PlacePiece action"""
        # Create a configuration for testing
        test_config = np.zeros((5, 5), dtype=int)
        test_config[1, 2] = 1  # A single block in a valid position
        
        action = PlacePiece(piece=self.test_piece, card=self.test_card, pieces=self.test_pieces)
        
        # Test validity when piece and card are provided
        self.assertTrue(action.is_action_valid())
        
        # Test performance with valid configuration
        result = action.perform_action(configuration=test_config)
        self.assertTrue(result)
        self.assertEqual(self.test_card.layout[1, 2], 1)
        
        # Test performance with invalid configuration (already placed)
        result = action.perform_action(configuration=test_config)
        self.assertFalse(result)
        
        # Test validity with no piece
        action = PlacePiece(card=self.test_card, pieces=[])
        self.assertFalse(action.is_action_valid())
        
        # Test validity with no card
        action = PlacePiece(piece=self.test_piece, cards=[])
        self.assertFalse(action.is_action_valid())
    
    def test_take_card_action(self):
        """Test the TakeCard action"""
        # Empty cards list to start
        empty_cards = []
        action = TakeCard(cards=empty_cards)
        
        # Test validity (should be true when no cards)
        self.assertTrue(action.is_action_valid())
        
        # Test performing action
        action.perform_action()
        self.assertEqual(len(empty_cards), 1)
        self.assertIsInstance(empty_cards[0], Card)
        
        # Test validity with existing card (implementation says max 1 card)
        self.assertFalse(action.is_action_valid())


if __name__ == '__main__':
    unittest.main()
