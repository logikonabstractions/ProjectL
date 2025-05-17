import random

from ProjectL.card import Card
from ProjectL.pieces import *


class Action:
    """ encapsulates everything an action does - check validity based on card or game state

        Actions can have side effects - they may act on objects passed on to them as arguments.
        Exemples:
            - adding a piece to pieces or card to cards
            - modifying a piece or a card that was passed to it
    """

    def __init__(self, piece=None, card=None, pieces=None, cards=None):
        self.desc = "action"
        self.piece = piece
        self.card = card
        self.pieces = pieces
        self.cards = cards

    def is_action_valid(self, *args, **kwargs):
        """ checks if the action is valid
            :return: Bool
        """

        return False

    def perform_action(self, *args, **kwargs):
        """ performs the action. Will produce side-effect on objects that have been passed to the action -
            e.g. update the Card if a valid piece has been placed, changes the piece if we upgrade it, etc.

            After is_action_valid() returns True, perform_action() should always succeed.
        """
        pass

    def __str__(self):
        return self.desc


class TakePiece(Action):
    def __init__(self, piece=None, card=None, pieces=None, **kwargs):
        super().__init__(piece, card, pieces, **kwargs)
        self.desc = "Take a Piece"

    def perform_action(self):
        """ selects an available piece and returns it
        """

        # choose a piece, for now only Square pieces
        piece = PieceSquare()
        self.pieces.append(piece)
        return True

    def is_action_valid(self):
        """ This action is always valid we return True all the time
            :return: True
        """
        return True


class PlacePiece(Action):
    def __init__(self, piece=None, card=None, pieces=None, **kwargs):
        super().__init__(piece, card, pieces, **kwargs)
        self.desc = "Place a piece"
        self._valid_configurations = None  # Cache of valid configurations

    def _find_valid_configurations(self):
        """Find all valid configurations for placing the piece on the card.

        Returns:
            list: List of valid configuration matrices
        """
        if self.piece is None or self.card is None:
            return []

        valid_configs = []
        for config_no in range(self.piece.cube.shape[0]):
            configuration = self.piece.cube[config_no, :, :]
            if self.card.placement_valid(configuration):
                valid_configs.append(configuration)

        return valid_configs

    def perform_action(self, configuration=None):
        """
        Place the piece on the card. After is_action_valid() returns True,
        this method is guaranteed to succeed.

        Args:
            configuration: Optional specific configuration to use. If None,
                         will use a random valid configuration.

        Returns:
            bool: True (always succeeds after valid check)
        """
        if configuration is None:
            # Use cached valid configurations if available
            if self._valid_configurations:
                configuration = random.choice(self._valid_configurations)
            else:
                # Find valid configurations
                valid_configs = self._find_valid_configurations()
                if not valid_configs:
                    # This should never happen if is_action_valid() was called first
                    raise RuntimeError("No valid configurations found in perform_action")
                configuration = random.choice(valid_configs)

        # Place the piece - this should always succeed after validation
        result = self.card.place_piece(configuration)
        if not result:
            raise RuntimeError("Unexpected placement failure after validation")
        return True

    def is_action_valid(self):
        """ Must have a piece and a card that is not full, and the piece must be placeable on the card
        """
        # Select piece and card if not provided
        if self.piece is None:
            if self.pieces:
                self.piece = random.choice(self.pieces)
            else:
                return False  # cannot place a piece if we have none

        if self.card is None:
            if self.cards:
                self.card = random.choice(self.cards)
            else:
                return False

        if self.card is None or self.piece is None:
            return False

        # Check if the piece can actually be placed on the card
        self._valid_configurations = self._find_valid_configurations()
        return len(self._valid_configurations) > 0


class UpgradePiece(Action):
    def __init__(self, piece=None, card=None, pieces=None, **kwargs):
        super().__init__(piece, card, pieces, **kwargs)
        self.desc = "Upgrade a piece"
        if self.piece is None and self.pieces:
            self.piece = random.choice(self.pieces)

    def perform_action(self):
        """Placeholder - always succeeds after valid check"""
        # TODO: Implement upgrade logic
        return True

    def is_action_valid(self):
        """Check if we have a piece to upgrade"""
        if self.piece is None and self.pieces:
            self.piece = random.choice(self.pieces)
        return self.piece is not None


class TakeCard(Action):
    def __init__(self, piece=None, card=None, pieces=None, cards=None, **kwargs):
        super().__init__(piece, card, pieces, cards, **kwargs)
        self.desc = "Take a card"

    def perform_action(self):
        """ selects a possible piece and returns it
        """
        # choose a piece
        card = Card()
        self.cards.append(card)
        return True

    def is_action_valid(self):
        """ checks if we can take a card - limited to 1 card for now
            :return: True if we can take a card
        """
        # TODO: check this
        if len(self.cards) >= 1:
            return False

        return True


class Master(Action):
    def __init__(self, piece=None, card=None, pieces=None, **kwargs):
        super().__init__(piece, card, pieces, **kwargs)
        self.desc = "Master"

    def perform_action(self):
        """Placeholder - always succeeds after valid check"""
        # TODO: Implement master action
        return True

    def is_action_valid(self):
        """Placeholder for master action validity"""
        # TODO: Implement validation logic
        return True
