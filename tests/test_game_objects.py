import unittest
import numpy as np
from tests.test_base import BaseTest

from ProjectL.game_objects import GameState, Player
from ProjectL.actions import TakePiece, PlacePiece, TakeCard
from ProjectL.pieces import PieceSquare


class TestGameState(BaseTest):
    """Test cases for the GameState class"""
    
    def test_game_state_initialization(self):
        """Test that game state is correctly initialized"""
        game_state = GameState()
        self.assertEqual(game_state.current_turn_number, 1)
        self.assertEqual(game_state.max_turns, 2)
        
        custom_game_state = GameState(current_turn_number=3, max_turns=10)
        self.assertEqual(custom_game_state.current_turn_number, 3)
        self.assertEqual(custom_game_state.max_turns, 10)
    
    def test_next_turn(self):
        """Test that next_turn increments the turn number"""
        game_state = GameState(current_turn_number=1, max_turns=5)
        game_state.next_turn()
        self.assertEqual(game_state.current_turn_number, 2)
        game_state.next_turn()
        self.assertEqual(game_state.current_turn_number, 3)
    
    def test_is_game_running(self):
        """Test that is_game_running returns correct value based on turns"""
        game_state = GameState(current_turn_number=1, max_turns=2)
        self.assertTrue(game_state.is_game_running())
        
        game_state.next_turn()
        self.assertTrue(game_state.is_game_running())
        
        game_state.next_turn()
        self.assertFalse(game_state.is_game_running())


class TestPlayer(BaseTest):
    """Test cases for the Player class"""
    
    def setUp(self):
        """Set up test fixtures before each test"""
        super().setUp()
        self.actions = [TakePiece, PlacePiece, TakeCard]
    
    def test_player_initialization(self):
        """Test that player is correctly initialized"""
        # Default initialization
        player = Player()
        self.assertIsInstance(player.name, str)
        self.assertEqual(player.actions_left, 3)
        self.assertEqual(len(player.pieces), 1)
        self.assertIsInstance(player.pieces[0], PieceSquare)
        self.assertEqual(len(player.cards), 0)
        self.assertGreater(len(player.actions), 0)
        
        # Custom initialization
        # Note: Player class auto-initializes pieces with PieceSquare even if we pass empty list
        test_pieces = [PieceSquare()]
        custom_player = Player(name="TestPlayer", cards=[], pieces=test_pieces, actions=self.actions)
        self.assertEqual(custom_player.name, "TestPlayer")
        self.assertEqual(custom_player.actions_left, 3)
        self.assertEqual(len(custom_player.pieces), 1)  # Always has at least one piece due to implementation
        self.assertEqual(len(custom_player.cards), 0)
        self.assertEqual(custom_player.actions, self.actions)
    
    def test_choose_action(self):
        """Test that choose_action returns a valid action"""
        player = Player(name="TestPlayer", actions=self.actions)
        action = player.choose_action()
        
        # Action should be an instance of one of the allowed actions
        self.assertIsInstance(action, tuple(self.actions))
        
        # Actions_left should be decremented
        self.assertEqual(player.actions_left, 2)
    
    def test_get_actions(self):
        """Test that get_actions returns expected action classes"""
        player = Player()
        actions = player.get_actions()
        
        # Should include basic actions
        self.assertTrue(TakePiece in actions)
        self.assertTrue(PlacePiece in actions)
        self.assertTrue(TakeCard in actions)
    
    def test_get_initial_pieces(self):
        """Test that get_initial_pieces returns a square piece"""
        player = Player()
        pieces = player.get_initial_pieces()
        
        self.assertEqual(len(pieces), 1)
        self.assertIsInstance(pieces[0], PieceSquare)


if __name__ == '__main__':
    unittest.main()
