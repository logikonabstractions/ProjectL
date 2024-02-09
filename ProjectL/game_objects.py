import string
import random
from actions import *

class GameState:
    """ encapsulates the current state of a game """
    def __init__(self, current_turn_number = 1, max_turns=2):
        self.current_turn_number = current_turn_number
        self.max_turns = max_turns
        
    def next_turn(self):
        """ updates whatever needs updating in the state so that we can move on to next turn """
        self.current_turn_number += 1
        
    def is_game_running(self):    
        """ checks if the game is running or over"""
        is_running = self.current_turn_number <= self.max_turns
        return is_running
        

class GameManager:  
    """ the main game engine that runs the game. """
    def __init__(self, configs_dict):  
        self.configs = configs_dict
        # self.configs_actions = configs_dict["game_parameters"]["actions"]
        self.configs_pieces = configs_dict["pieces"]
        self.game_state = GameState(current_turn_number=1, max_turns=configs_dict["game_parameters"]["max_turns"])
        
        # game parameters - extraction for easier access
        # self.current_turn_number = 1
        # self.max_turns = configs_dict["game_parameters"]["max_turns"]
        self.pieces = []
        self.actions = [TakePiece, PlacePiece, UpgradePiece, TakeCard, Master]
        
        # players        
        self.player_1 = Player(name=configs_dict["players"][0]["name"])
        self.player_2 = Player(name=configs_dict["players"][1]["name"])
        
        # game init
        self.game_init()

    def game_init(self):
        """ instantiates the pieces, cards, etc... any setup steps required for the game .
            mostly based on configs 
        """
        self.instantiate_pieces()

    def instantiate_pieces(self):
        """ instantiates all the pieces: loads from configs, converts to numpy arrays
            creates the objects, and plots them (For debug at least)
        """
        for piece_confs in self.configs_pieces:
            self.pieces.append(Piece(configs=piece_confs))

    def run(self):
        """ loop that runs the game """
        print("Please welcome our players!")
        print(f"Player One: {self.player_1} ")
        print(f"Player Two: {self.player_2} ")

        print("Now let's run the game")
        while self.is_game_running:
            print(f"")
            print(f"====== Playing turn {self.current_turn_number} ======")
            self.player_1.play_turn()
            self.player_2.play_turn()

            # update turn number
            self.game_state.next_turn()
        
        
    @property
    def is_game_running(self):    
        """ checks if the game is running or over"""
        is_running = self.current_turn_number <= self.max_turns
        return is_running
    
    @property
    def current_turn_number(self):
        return self.game_state.current_turn_number
    
    @property
    def max_turns(self):
        return self.configs["game_parameters"]["max_turns"]


class Player:
    """ a class that describes a player """
    def __init__(self, name=None, cards =None, pieces = None, actions = None, **kwargs):
        
        # attri. that defines the Player itself
        self.name = name if name is not None else self.generate_random_name()
        self.actions_left = 3
        
        # list of objects, game stuff
        self.cards = cards if cards else []
        self.pieces = pieces if pieces else self.get_initial_pieces()
        self.actions = actions if actions else self.get_actions()
        self.kwargs = kwargs        

    def play_turn(self):
        """  """
        self.actions_left = 3
        while self.actions_left > 0:
            print(f"{self.name} chooses and action...")
            action = self.choose_action()
            print(f"Action: {action}")
            if action.is_action_valid():
                result = action.perform_action()
            print(f"{self}")
            
            
        print(f"{self.name} has no action left.")
        print(f"{self}")

    def choose_action(self):
        """ decides what the player does this turn"""
        action_selected = random.choice(self.actions)(pieces=self.pieces, cards=self.cards)
        self.actions_left -= 1        
        return action_selected
    
    def get_actions(self):
        
        actions = [TakePiece, PlacePiece, UpgradePiece,  TakeCard, Master]
        # actions = [PlacePiece, UpgradePiece,  TakeCard]
        
        
        return actions

    def __repr__(self):
        return f"Name: {self.name} " \
               f"pieces: {self.pieces} cards: {self.cards}"

    def generate_random_name(self, length=5):
        """ just for fun - generates random names to players if none assigned """
        chars = string.ascii_lowercase
        # Generate a random name of specified length
        return ''.join(random.choice(chars) for _ in range(length))

    def get_initial_pieces(self):
        return [PieceSquare()]

