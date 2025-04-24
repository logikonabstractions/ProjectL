import unittest
import numpy as np

from ProjectL.actions import PlacePiece
from tests.test_base import BaseTest

from ProjectL.card import Card, Reward
from ProjectL.pieces import PieceSquare, Piece


class TestCard(BaseTest):
    """Test cases for the Card class"""
    
    def setUp(self):
        """Set up test fixtures before each test"""
        super().setUp()
        self.cards = []
        for card_confs in self.test_configs['cards']:
            self.cards.append(Card(card_confs))
    
    def test_card_initialization(self):
        """Test that a card is correctly initialized from configs"""
        for i, card in enumerate(self.cards):
            self.assertTrue(np.array_equal(card.mask, np.array(self.test_configs["cards"][i]["mask"])))
            self.assertEqual(card.reward.points, self.test_configs["cards"][i]["reward"]['points'])
            # The default behavior creates a PieceSquare when piece is None
            self.assertIsInstance(card.reward.piece, PieceSquare)
            self.assertTrue(np.all(card.layout == 0))  # Layout should be empty initially

    def test_valid_placement_1(self):
        """ test placing a simple piece on a card. valid placement """
        card = self.cards[0]
        piece = Piece(self.get_piececonfs_from_name(name="corner_3"))
        action = PlacePiece(piece=piece, card=card)
        result = action.perform_action(piece.cube[2])
        assert result

    def test_invalid_placement(self):
        """ test placing a simple piece on a card. Stuff is already on the card and we place someting valid on it """
        card = self.cards[1]
        piece = Piece(self.get_piececonfs_from_name(name="line_2"))
        action = PlacePiece(piece=piece, card=card)
        result_1 = action.perform_action(piece.cube[5])
        assert not(result_1)



    def test_default_reward_class(self):
        """Test the Reward class"""
        # Test default initialization
        default_reward = Reward()
        self.assertEqual(default_reward.points, 0)
        self.assertIsInstance(default_reward.piece, PieceSquare)

    def test_custom_reward_class(self):
        # Test custom initialization
        custom_piece = Piece(self.get_piececonfs_from_name("corner_3"))
        custom_reward = Reward(points=5, piece=custom_piece)
        self.assertEqual(custom_reward.points, 5)
        self.assertEqual(custom_reward.piece, custom_piece)

    def get_piececonfs_from_name(self,name):
        """ returns a piece's configs from the configs based on the piece name """
        p = next((d for d in self.test_configs["pieces"] if d.get('name') == name), None)
        if p:
            return p
        else:
            raise Exception("invalid piece name from configs - check the name of the pieces defined in config file")

if __name__ == '__main__':
    unittest.main()
