import random
from ProjectL.actions import *


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

    # Properties to access player attributes directly from strategy
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
        piece = self.pieces[-1]  # Look at the last piece without removing it yet
        action = PlacePiece(piece, self.cards[0], pieces=self.pieces)

        if self._execute_action(action):
            self.pieces.pop()  # Remove the piece only after successful placement
            return True
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

            # Special case: try to place pieces first
            if self.cards and self.pieces:
                if self._try_place_piece():
                    self._move_full_cards()  # Check for completed cards after placement
                    continue

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
