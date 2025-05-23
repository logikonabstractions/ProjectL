import string
import random

from ProjectL.classes import TakePiece, PlacePiece, UpgradePiece, TakeCard, Master, Card, Piece, PieceSquare


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


class Strategy:
    """Base strategy class for implementing different playing strategies.

    Allows for fixed sequences of actions or dynamic decision-making.
    Used by the Player class.
    """
    def __init__(self, player, actions_sequence=None, action_list=None):
        self.player = player
        self.action_sequence = actions_sequence if actions_sequence else ()
        self.actions = action_list if action_list else (TakePiece, PlacePiece, UpgradePiece, TakeCard, Master)
        self.actions_left = 3

    def play_turn(self):
        raise NotImplemented

    @property
    def pieces(self):
        return self.player.pieces
    @property
    def cards(self):
        return self.player.cards
    @cards.setter
    def cards(self, value):
        self.player.cards = value
    @property
    def full_cards(self):
        return self.player.full_cards
    @full_cards.setter
    def full_cards(self, value):
        self.player.full_cards = value
    @property
    def name(self):
        return self.player.name


class RandomStrat(Strategy):
    """Strategy that chooses actions randomly."""

    def __init__(self, player, **kwargs):
        super().__init__(player, **kwargs)

    def choose_action(self):
        """Randomly selects an action from available action types."""
        action_selected = random.choice(self.actions)(pieces=self.pieces, cards=self.cards)
        return action_selected

    def play_turn(self):
        """Play a turn by randomly choosing valid actions until actions run out."""
        self.actions_left = 3
        while self.actions_left > 0:
            action = self.choose_action()

            # Keep trying actions until we find a valid one
            while not action.is_action_valid():
                action = self.choose_action()

            # Execute the valid action and consume an action
            action.perform_action()
            self.actions_left -= 1

        print(f"{self.name} has no action left.")
        print(f"{self.player}")


class BasicStrat(Strategy):
    """Basic strategy with a simple priority system:

    Priority order:
    1. Place a piece if you have both cards and pieces
    2. Take a piece if you have no pieces
    3. Take a card if you have no cards (and pieces available)
    """

    def __init__(self, player, **kwargs):
        super().__init__(player, **kwargs)

    def _move_full_cards(self):
        """Move completed cards from active cards to full cards collection."""
        full_cards = [card for card in self.cards if card.is_full]
        if full_cards:
            self.full_cards.extend(full_cards)
            self.cards = [card for card in self.cards if not card.is_full]

    def _execute_action(self, action):
        """Execute an action if valid and consume an action point.

        Returns:
            bool: True if action was executed successfully
        """
        if action.is_action_valid():
            action.perform_action()
            self.actions_left -= 1
            return True
        return False

    def _try_place_piece(self):
        """Attempt to place a piece on a card.

        Returns:
            bool: True if placement was successful
        """
        if not (self.cards and self.pieces):
            return False

        # Try to place a piece on the first available card
        piece = self.pieces.pop()
        action = PlacePiece(piece, self.cards[0], pieces=self.pieces)

        if self._execute_action(action):
            return True
        else:
            self.pieces.append(piece)       # put it back in the pack since the action failed
            return False

    def _determine_best_action(self):
        """Determine the best action based on current game state.

        Returns:
            Action or None: The best action to take, or None if no valid action
        """
        # Priority 1: Place a piece if we have both cards and pieces
        if self.cards and self.pieces:
            return PlacePiece(self.pieces[-1], self.cards[0], pieces=self.pieces)

        # Priority 2: Take a piece if we have no pieces
        if not self.pieces:
            return TakePiece(pieces=self.pieces)

        # Priority 3: Take a card if we have no cards
        if not self.cards:
            return TakeCard(cards=self.cards)

        # Default: Take a piece (better than nothing)
        return TakePiece(pieces=self.pieces)

    def play_turn(self):
        """Execute the turn following the basic strategy priority system."""
        self.actions_left = 3

        # First, handle any completed cards
        self._move_full_cards()

        actions_attempted = 0
        max_attempts = 10  # Prevent infinite loops

        while self.actions_left > 0 and actions_attempted < max_attempts:
            actions_attempted += 1

            # Get the best action based on current state
            action = self._determine_best_action()

            if action and self._execute_action(action):
                continue
            else:
                # No valid actions available, pass remaining actions
                print(f"{self.name} passes remaining {self.actions_left} actions")
                self.actions_left = 0

        print(f"{self.name} has no actions left.")
        print(f"{self.player}")
