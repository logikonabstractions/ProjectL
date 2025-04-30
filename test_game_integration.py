import unittest
import os
import sys
import yaml
from unittest.mock import patch, MagicMock

# Add the parent directory to the path so we can import the ProjectL module
sys.path.append('/tmp/inputs')

from ProjectL.game_objects import GameManager, Player, GameState
from ProjectL.strategies import BasicStrat
from ProjectL.card import Card


class TestGameIntegration(unittest.TestCase):
    """
    Integration test for the ProjectL game.
    This test validates that the game mechanics run properly from start to finish.
    """
    
    def setUp(self):
        """Set up the test environment before each test method."""
        # Load the configuration file
        config_path = '/tmp/inputs/configs.yaml'
        with open(config_path, 'r') as file:
            self.configs_dict = yaml.safe_load(file)
        
        # Create a game manager with the test configuration
        self.game_manager = GameManager(self.configs_dict)
        
    def test_game_initialization(self):
        """Test that the game initializes correctly."""
        # Check that the game state is properly initialized
        self.assertEqual(self.game_manager.game_state.current_turn_number, 1)
        self.assertEqual(self.game_manager.game_state.max_turns, self.configs_dict["game_parameters"]["max_turns"])
        
        # Check that pieces are initialized
        self.assertGreater(len(self.game_manager.pieces), 0, "Game should have at least one piece")
        
        # Check that cards are initialized
        self.assertGreater(len(self.game_manager.cards), 0, "Game should have at least one card")
        
        # Check that players are initialized
        self.assertIsNotNone(self.game_manager.player_1)
        self.assertIsNotNone(self.game_manager.player_2)
        
    def test_player_initialization(self):
        """Test that players are initialized correctly."""
        # Check player names from config
        self.assertEqual(self.game_manager.player_1.name, self.configs_dict["players"][0]["name"])
        self.assertEqual(self.game_manager.player_2.name, self.configs_dict["players"][1]["name"])
        
        # Check that each player has initial pieces
        self.assertGreater(len(self.game_manager.player_1.pieces), 0, "Player should have at least one initial piece")
        
        # Check that player_1 has BasicStrat
        self.assertIsInstance(self.game_manager.player_1.strategy, BasicStrat)
        
    def test_single_turn_execution(self):
        """Test that a single turn executes correctly."""
        initial_turn = self.game_manager.current_turn_number
        initial_player1_pieces_count = len(self.game_manager.player_1.pieces)
        initial_player1_cards_count = len(self.game_manager.player_1.cards)
        
        # Execute one complete turn (both players play)
        with patch.object(Player, 'play_turn') as mock_play_turn:
            self.game_manager.run()  # This will run all turns, but we'll interrupt after one turn
            self.assertEqual(mock_play_turn.call_count, 2)  # Once for each player
        
        # Verify that the turn number has been incremented
        self.assertEqual(self.game_manager.current_turn_number, initial_turn + 1)
    
    @patch('builtins.print')  # Mock print to avoid cluttering test output
    def test_game_completion(self, mock_print):
        """Test that the game completes after the maximum number of turns."""
        # Create a game with a small number of turns for testing
        configs_with_short_game = self.configs_dict.copy()
        configs_with_short_game["game_parameters"]["max_turns"] = 3  # Small number for testing
        
        short_game = GameManager(configs_with_short_game)
        
        # Mock the game loop to avoid player actions and just advance turns
        with patch.object(short_game, 'player_1'),\
             patch.object(short_game, 'player_2'):
            # Run the game
            short_game.run()
        
        # Check that the game completed after the expected number of turns
        self.assertEqual(short_game.current_turn_number, 4)  # max_turns + 1
        self.assertFalse(short_game.is_game_running)
    
    def test_piece_placement(self):
        """Test that placing pieces on cards works correctly."""
        # Get a piece and card from the game
        piece = self.game_manager.player_1.pieces[0]
        card = self.game_manager.cards[0]
        
        # Create a PlacePiece action and execute it
        from ProjectL.actions import PlacePiece
        place_action = PlacePiece(piece=piece, card=card)
        
        # Check if action is valid and get a configuration
        if place_action.is_action_valid():
            # Get a valid configuration (first one in the piece's cube)
            configuration = piece.cube[0]
            # Perform the action
            result = place_action.perform_action(configuration)
            # Check if placement was successful
            self.assertTrue(result, "Piece placement should be successful")
            # Verify that the card's layout was updated
            self.assertTrue(1 in card.layout, "Card layout should be updated after placement")
    
    def test_take_card_action(self):
        """Test that taking a card action works correctly."""
        # The player starts with no cards
        initial_card_count = len(self.game_manager.player_1.cards)
        
        # Create a TakeCard action
        from ProjectL.actions import TakeCard
        take_card = TakeCard(cards=self.game_manager.player_1.cards)
        
        # Check if action is valid
        if take_card.is_action_valid():
            # Perform the action
            take_card.perform_action()
            # Check if a card was added to the player's cards
            self.assertGreater(len(self.game_manager.player_1.cards), initial_card_count,
                               "Player should have more cards after taking a card")
    
    def test_take_piece_action(self):
        """Test that taking a piece action works correctly."""
        # Get the player's initial pieces
        initial_piece_count = len(self.game_manager.player_1.pieces)
        
        # Create a TakePiece action
        from ProjectL.actions import TakePiece
        take_piece = TakePiece(pieces=self.game_manager.player_1.pieces)
        
        # Perform the action
        take_piece.perform_action()
        
        # Check if a piece was added
        self.assertGreater(len(self.game_manager.player_1.pieces), initial_piece_count,
                           "Player should have more pieces after taking a piece")


if __name__ == '__main__':
    unittest.main()
