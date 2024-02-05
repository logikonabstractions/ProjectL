import random
from pieces import *

class Action:
    """ encapsulates everything an action does - check validity based on card or game state etc. """
    def __init__(self, piece=None, card=None, pieces = None):
        self.desc = "action"    
        self.piece = piece
        self.card = card
        self.pieces = pieces
    
    def is_action_valid(self):
        """ checks if the action is valid
            :return: Bool
        """
        
        return False

    def perform_action(self):
        """ performs the action. Will produce side-effect on objects that have been passed to the action -
            e.g. update the Card if a valid piece has been placed, changes the piece if we upgrade it, etc.
        """
        pass

    def __repr__(self):
        return self.desc

class TakePiece(Action):
    def __init__(self, piece=None, card=None, pieces = None):
        super().__init__(piece, card, pieces)
        self.desc = "Take a Piece"
        
    def perform_action(self):
        """ selects a possible piece and returns it
        """
        
        # choose a piece
        piece = PieceSquare()
        self.pieces.append(piece)

    def is_action_valid(self):
        """ checks if we can take a piece. This action is always valid we return True all the time
            :return: True
        """
        return True


class PlacePiece(Action):
    def __init__(self, piece=None, card=None, pieces = None):
        super().__init__(piece, card, pieces)
        self.desc = "Place a piece"

    def perform_action(self):
        """ places the given piece on the given card 
        """
        

        return 
    
    def is_action_valid(self):
        """ Requirements:
                * Card object 
                * Piece object
                * Configuration we want to place the piece into
            :return: Bool
        """


class UpgradePiece(Action):
    def __init__(self, piece=None, card=None, pieces = None):
        super().__init__(piece, card, pieces)
        self.desc = "Upgrade a piece"


class TakeCard(Action):
    def __init__(self, piece=None, card=None, pieces = None):
        super().__init__(piece, card, pieces)
        self.desc = "Take a card"


class Master(Action):
    def __init__(self, piece=None, card=None, pieces = None):
        super().__init__(piece, card, pieces)
        self.desc = "Master"
