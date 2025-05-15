import string
import random
# from actions import *
from ProjectL.actions import *
from ProjectL.strategies import *


class GameState:
    """ encapsulates the current state of a game """
    def __init__(self, current_turn_number = 1, max_turns=2):
        self.current_turn_number = current_turn_number
        self.max_turns = max_turns
        
    def next_turn(self):
        """ """
        self.current_turn_number += 1
        
    def is_game_running(self):    
        """ checks if the game is running or over"""
        is_running = self.current_turn_number <= self.max_turns
        return is_running
        

class GameManager:  
    """ the main game engine that runs the game. """
    def __init__(self, configs_dict):  
        self.configs = configs_dict
        self.configs_pieces = configs_dict["pieces"]
        self.configs_cards = configs_dict["cards"]
        self.game_state = GameState(current_turn_number=1, max_turns=configs_dict["game_parameters"]["max_turns"])
        

        self.pieces = []
        self.actions = [TakePiece, PlacePiece, TakeCard]
        self.cards = []
        
        # players        TODO: ugly, refactor & makes a more robust initialization
        self.player_1 = Player(name=configs_dict["players"][0]["name"], actions=self.actions)
        self.player_1.set_strategy(BasicStrat(player=None))
        self.player_2 = Player(name=configs_dict["players"][1]["name"], actions=self.actions)
        
        self.game_init()

    def game_init(self):
        """ setup for the beginning of the game
        """
        self.instantiate_pieces()

    def instantiate_pieces(self):
        """
        """
        for piece_confs in self.configs_pieces:
            self.pieces.append(Piece(configs=piece_confs))
            
        for card_confs in self.configs_cards:
            self.cards.append(Card(configs=card_confs))

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

            # update turn number, but for debug check the state of the game
            if self.current_turn_number%10 == 0:
                print(f"{self.player_1} has {len(self.player_1.full_cards)} full cards and {len(self.player_1.cards)} cards")
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
    def __init__(self, name=None, cards =None, pieces = None, actions = None, strategy=None, **kwargs):
        
        # attri. that defines the Player itself
        self.name = name if name is not None else self.generate_random_name()
        self.actions_left = 3
        
        # list of objects, game stuff
        self.cards = cards if cards else []
        self.full_cards = []
        self.pieces = pieces if pieces else self.get_initial_pieces()
        # self.actions = actions if actions else self.get_actions()
        self.kwargs = kwargs

        self.strategy = strategy if strategy else RandomStrat(player=self)

    def play_turn(self):
        """  delegates the playing to the strategy """
        return self.strategy.play_turn()


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

    def set_strategy(self, strategy):
        self.strategy = strategy
        self.strategy.player = self

