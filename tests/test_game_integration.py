import unittest
import os
import yaml
from ProjectL.game_objects import GameManager, Player, RandomStrat, BasicStrat


class TestGameIntegration(unittest.TestCase):
    def setUp(self):
        """Setup test game with specific config"""
        # Create a test config that's smaller but covers all mechanics

        with open("tests/test_configs.yaml", 'r') as file:
            self.test_config = yaml.safe_load(file)

    def test_full_game_flow(self):
        """Test a complete game flow from start to finish"""
        # Initialize game
        game_manager = GameManager(self.test_config)

        # Validate initial game state
        self.assertEqual(game_manager.game_state.current_turn_number, 1)
        self.assertEqual(game_manager.game_state.max_turns, 10)
        
        # Validate players were created correctly
        self.assertEqual(game_manager.player_1.name, self.test_config["players"][0]["name"])
        self.assertEqual(game_manager.player_2.name, self.test_config["players"][1]["name"])
        
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
