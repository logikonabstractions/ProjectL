import string
import random
from ProjectL.classes import TakePiece, PlacePiece, UpgradePiece, TakeCard, Master, Card, Piece, PieceSquare
import logging


class GameState:
    """ encapsulates the current state of a game """

    def __init__(self, current_turn_number=1, max_turns=2, logger=None):
        self.current_turn_number = current_turn_number
        self.max_turns = max_turns
        self.logger = logger or logging.getLogger('projectL')

    def next_turn(self):
        """ """
        self.current_turn_number += 1
        self.logger.debug("Advanced to turn %d/%d",
                          self.current_turn_number, self.max_turns,
                          extra={"normal": False})

    def is_game_running(self):
        """ checks if the game is running or over"""
        is_running = self.current_turn_number <= self.max_turns
        if not is_running:
            self.logger.info("Game over: reached maximum turns (%d)",
                             self.max_turns,
                             extra={"normal": True})
        return is_running
class GameManager:
    """ the main game engine that runs the game. """

    def __init__(self, configs_dict, logger=None):
        self.configs = configs_dict
        self.configs_pieces = configs_dict["pieces"]
        self.configs_cards = configs_dict["cards"]
        self.game_state = GameState(current_turn_number=1, max_turns=configs_dict["game_parameters"]["max_turns"])

        # Set up logger
        self.logger = logger or logging.getLogger('projectL')

        self.pieces = []
        self.actions = [TakePiece, PlacePiece, TakeCard]
        self.cards = []

        # players        TODO: ugly, refactor & makes a more robust initialization
        self.player_1 = Player(name=configs_dict["players"][0]["name"], actions=self.actions, logger=self.logger)
        self.player_1.set_strategy(BasicStrat(player=None, logger=self.logger))
        self.player_2 = Player(name=configs_dict["players"][1]["name"], actions=self.actions, logger=self.logger)

        self.game_init()

    def game_init(self):
        """ setup for the beginning of the game
        """
        self.logger.debug("Initializing game", extra={"normal": False})
        self.instantiate_pieces()

    def instantiate_pieces(self):
        """
        """
        self.logger.debug("Creating game pieces", extra={"normal": False})
        for piece_confs in self.configs_pieces:
            self.pieces.append(Piece(configs=piece_confs))
            self.logger.debug("Created piece: %s", piece_confs["name"], extra={"normal": False, "verbose": True})

        for card_confs in self.configs_cards:
            self.cards.append(Card(configs=card_confs))
            self.logger.debug("Created card with reward points: %s", card_confs["reward"]["points"],
                              extra={"normal": False, "verbose": True})

    def run(self):
        """ loop that runs the game """
        self.logger.info("Game started with players: %s and %s",
                         self.player_1.name, self.player_2.name,
                         extra={"normal": True})

        while self.is_game_running:
            self.logger.info("====== Playing turn %d ======", self.current_turn_number, extra={"normal": True})

            self.logger.debug("%s's turn", self.player_1.name, extra={"normal": False})
            self.player_1.play_turn()

            self.logger.debug("%s's turn", self.player_2.name, extra={"normal": False})
            self.player_2.play_turn()

            # update turn number, but for debug check the state of the game
            if self.current_turn_number % 10 == 0:
                self.logger.info("%s has %d full cards and %d cards",
                                 self.player_1.name,
                                 len(self.player_1.full_cards),
                                 len(self.player_1.cards),
                                 extra={"normal": True})
            self.game_state.next_turn()

        self.logger.info("Game ended after %d turns", self.current_turn_number - 1, extra={"normal": True})

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

    def __init__(self, name=None, cards=None, pieces=None, actions=None, strategy=None, logger=None, **kwargs):
        # Set up logger
        self.logger = logger or logging.getLogger('projectL')

        # attri. that defines the Player itself
        self.name = name if name is not None else self.generate_random_name()
        self.actions_left = 3

        # list of objects, game stuff
        self.cards = cards if cards else []
        self.full_cards = []
        self.pieces = pieces if pieces else self.get_initial_pieces()
        # self.actions = actions if actions else self.get_actions()
        self.kwargs = kwargs

        self.strategy = strategy if strategy else RandomStrat(player=self, logger=self.logger)

        self.logger.debug("Player %s initialized", self.name, extra={"normal": False})

    def play_turn(self):
        """  delegates the playing to the strategy """
        self.logger.debug("%s is playing their turn", self.name, extra={"normal": False})
        return self.strategy.play_turn()

    def __repr__(self):
        return f"Name: {self.name} " \
               f"pieces: {self.pieces} cards: {self.cards}"

    def generate_random_name(self, length=5):
        """ just for fun - generates random names to players if none assigned """
        chars = string.ascii_lowercase
        # Generate a random name of specified length
        name = ''.join(random.choice(chars) for _ in range(length))
        self.logger.debug("Generated random name: %s", name, extra={"normal": False, "verbose": True})
        return name

    def get_initial_pieces(self):
        self.logger.debug("Getting initial pieces for %s", self.name, extra={"normal": False, "verbose": True})
        return [PieceSquare()]

    def set_strategy(self, strategy):
        self.logger.debug("Setting strategy for %s", self.name, extra={"normal": False})
        self.strategy = strategy
        self.strategy.player = self
        if hasattr(strategy, 'logger'):
            strategy.logger = self.logger

class Strategy:
    """Base strategy class for implementing different playing strategies.

    Allows for fixed sequences of actions or dynamic decision-making.
    Used by the Player class.
    """
    def __init__(self, player, actions_sequence=None, action_list=None, logger=None):
        self.player = player
        self.action_sequence = actions_sequence if actions_sequence else ()
        self.actions = action_list if action_list else (TakePiece, PlacePiece, UpgradePiece, TakeCard, Master)
        self.actions_left = 3
        self.logger = logger or logging.getLogger('projectL')

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

    def __init__(self, player, logger=None, **kwargs):
        super().__init__(player, logger=logger, **kwargs)

    def choose_action(self):
        """Randomly selects an action from available action types."""
        action_class = random.choice(self.actions)
        action_selected = action_class(pieces=self.pieces, cards=self.cards)
        self.logger.debug("%s randomly selected action: %s",
                          self.name, action_selected.desc,
                          extra={"normal": False, "verbose": True})
        return action_selected

    def play_turn(self):
        """Play a turn by randomly choosing valid actions until actions run out."""
        self.actions_left = 3
        self.logger.debug("%s starting turn with %d actions (RandomStrat)",
                          self.name, self.actions_left,
                          extra={"normal": False})

        while self.actions_left > 0:
            action = self.choose_action()

            # Keep trying actions until we find a valid one
            attempts = 0
            while not action.is_action_valid() and attempts < 10:
                self.logger.debug("%s action invalid, trying another",
                                  self.name,
                                  extra={"normal": False, "verbose": True})
                action = self.choose_action()
                attempts += 1

            if attempts >= 10:
                self.logger.debug("%s couldn't find valid action after 10 attempts",
                                  self.name,
                                  extra={"normal": False})
                break

            # Execute the valid action and consume an action
            self.logger.info("%s performs: %s", self.name, action.desc, extra={"normal": True})
            action.perform_action()
            self.actions_left -= 1

        self.logger.debug("%s has no actions left", self.name, extra={"normal": False})
        self.logger.debug("Player state: %s", self.player, extra={"normal": False, "verbose": True})

class BasicStrat(Strategy):
    """Basic strategy with a simple priority system:

    Priority order:
    1. Place a piece if you have both cards and pieces
    2. Take a piece if you have no pieces
    3. Take a card if you have no cards (and pieces available)
    """

    def __init__(self, player, logger=None, **kwargs):
        super().__init__(player, logger=logger, **kwargs)

    def _move_full_cards(self):
        """Move completed cards from active cards to full cards collection."""
        full_cards = [card for card in self.cards if card.is_full]
        if full_cards:
            self.logger.info("%s completed %d cards", self.name, len(full_cards), extra={"normal": True})
            self.full_cards.extend(full_cards)
            self.cards = [card for card in self.cards if not card.is_full]

    def _execute_action(self, action):
        """Execute an action if valid and consume an action point.

        Returns:
            bool: True if action was executed successfully
        """
        if action.is_action_valid():
            self.logger.info("%s performs: %s", self.name, action.desc, extra={"normal": True})
            action.perform_action()
            self.actions_left -= 1
            return True
        else:
            self.logger.debug("%s action invalid: %s", self.name, action.desc, extra={"normal": False, "verbose": True})
            return False

    def _try_place_piece(self):
        """Attempt to place a piece on a card.

        Returns:
            bool: True if placement was successful
        """
        if not (self.cards and self.pieces):
            self.logger.debug("%s can't place piece - missing cards or pieces",
                             self.name,
                             extra={"normal": False, "verbose": True})
            return False

        # Try to place a piece on the first available card
        piece = self.pieces.pop()
        action = PlacePiece(piece, self.cards[0], pieces=self.pieces)
        self.logger.debug("%s attempting to place piece on card", self.name, extra={"normal": False})

        if self._execute_action(action):
            return True
        else:
            self.pieces.append(piece)  # put it back in the pack since the action failed
            self.logger.debug("%s failed to place piece, returning to inventory",
                             self.name,
                             extra={"normal": False, "verbose": True})
            return False

    def _determine_best_action(self):
        """Determine the best action based on current game state.

        Returns:
            Action or None: The best action to take, or None if no valid action
        """
        # Priority 1: Place a piece if we have both cards and pieces
        if self.cards and self.pieces:
            self.logger.debug("%s strategy: place piece (has cards and pieces)",
                             self.name,
                             extra={"normal": False})
            return PlacePiece(self.pieces[-1], self.cards[0], pieces=self.pieces)

        # Priority 2: Take a piece if we have no pieces
        if not self.pieces:
            self.logger.debug("%s strategy: take piece (no pieces)",
                             self.name,
                             extra={"normal": False})
            return TakePiece(pieces=self.pieces)

        # Priority 3: Take a card if we have no cards
        if not self.cards:
            self.logger.debug("%s strategy: take card (no cards)",
                             self.name,
                             extra={"normal": False})
            return TakeCard(cards=self.cards)

        # Default: Take a piece (better than nothing)
        self.logger.debug("%s strategy: default to take piece",
                         self.name,
                         extra={"normal": False})
        return TakePiece(pieces=self.pieces)

    def play_turn(self):
        """Execute the turn following the basic strategy priority system."""
        self.actions_left = 3
        self.logger.debug("%s starting turn with %d actions (BasicStrat)",
                         self.name, self.actions_left,
                         extra={"normal": False})

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
                self.logger.info("%s passes remaining %d actions",
                               self.name, self.actions_left,
                               extra={"normal": True})
                self.actions_left = 0

        self.logger.debug("%s has no actions left", self.name, extra={"normal": False})
        self.logger.debug("Player state: %s", self.player, extra={"normal": False, "verbose": True})