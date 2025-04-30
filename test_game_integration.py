import unittest
import os
import yaml
from ProjectL.game_objects import GameManager, Player
from ProjectL.strategies import BasicStrat, RandomStrat

class TestGameIntegration(unittest.TestCase):
    def setUp(self):
        """Setup test game with specific config"""
        # Create a test config that's smaller but covers all mechanics
        self.test_config = {
            'game_parameters': {
                'max_turns': 10  # Smaller number for testing
            },
            'pieces': [
                {
                    'name': 'square_1',
                    'level': 1,
                    'shape': [[1, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
                },
                {
                    'name': 'line_2',
                    'level': 2,
                    'shape': [[1, 0, 0, 0, 0], [1, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
                }
            ],
            'cards': [
                {
                    'reward': {
                        'points': 1,
                        'piece': None
                    },
                    'mask': [[False,False,True,True,False], [False,False,True,True,False], 
                            [False,False,True,True,False], [False,False,False,False,False], 
                            [False,False,False,False,False]]
                }
            ],
            'players': [
                {'name': 'TestPlayer1', 'age': 30},
                {'name': 'TestPlayer2', 'age': 25}
            ]
        }

    def test_full_game_flow(self):
        """Test a complete game flow from start to finish"""
        # Initialize game
        game_manager = GameManager(self.test_config)
        
        # Validate initial game state
        self.assertEqual(game_manager.game_state.current_turn_number, 1)
        self.assertEqual(game_manager.game_state.max_turns, 10)
        
        # Validate players were created correctly
        self.assertEqual(game_manager.player_1.name, "TestPlayer1")
        self.assertEqual(game_manager.player_2.name, "TestPlayer2")
        
        # Set strategies for predictable testing
        game_manager.player_1.set_strategy(BasicStrat(player=None))
        game_manager.player_2.set_strategy(BasicStrat(player=None))
        
        # Validate initial piece setup
        self.assertTrue(len(game_manager.pieces) >= 2)  # At least our 2 configured pieces
        
        # Run the game
        game_manager.run()
        
        # Validate game completion
        self.assertGreater(game_manager.game_state.current_turn_number, 1)
        self.assertFalse(game_manager.game_state.is_game_running())
        
        # Validate player states after game
        self.assertIsNotNone(game_manager.player_1.pieces)
        self.assertIsNotNone(game_manager.player_2.pieces)
        
        # Check if players accumulated cards/pieces during the game
        total_cards = (len(game_manager.player_1.cards) + len(game_manager.player_1.full_cards) + 
                      len(game_manager.player_2.cards) + len(game_manager.player_2.full_cards))
        self.assertGreater(total_cards, 0, "No cards were collected during the game")
        
        # Validate that game ended at or before max turns
        self.assertLessEqual(game_manager.game_state.current_turn_number, 
                           game_manager.game_state.max_turns + 1)  # +1 because turn is incremented after max
        
if __name__ == '__main__':
    unittest.main()
