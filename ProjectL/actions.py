from ProjectL.card import Card
from ProjectL.pieces import *

class Action:
    """ encapsulates everything an action does - check validity based on card or game state
    
        Actions can have side effects - they may act on objects passed on to them as arguments.
        Exemples:
            - adding a piece to pieces or card to cards
            - modifying a piece or a card that was passed to it
    """
    def __init__(self, piece=None, card=None, pieces = None, cards=None):
        self.desc = "action"    
        self.piece = piece
        self.card = card
        self.pieces = pieces
        self.cards = cards 
    
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

    def __str__(self):
        return self.desc

class TakePiece(Action):
    def __init__(self, piece=None, card=None, pieces = None, **kwargs):
        super().__init__(piece, card, pieces, **kwargs)
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
    def __init__(self, piece=None, card=None, pieces = None, **kwargs):
        super().__init__(piece, card, pieces, **kwargs)
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
    def __init__(self, piece=None, card=None, pieces = None, **kwargs):
        super().__init__(piece, card, pieces, **kwargs)
        self.desc = "Upgrade a piece"


class TakeCard(Action):
    def __init__(self, piece=None, card=None, pieces = None, cards=None, **kwargs):
        super().__init__(piece, card, pieces, cards, **kwargs)
        self.desc = "Take a card"

    def perform_action(self):
        """ selects a possible piece and returns it
        """

        # choose a piece
        card = Card()
        self.cards.append(card)


    def is_action_valid(self):
        """ checks if we can take a piece. This action is always valid we return True all the time
            :return: True
        """
        return True


class Master(Action):
    def __init__(self, piece=None, card=None, pieces = None, **kwargs):
        super().__init__(piece, card, pieces, **kwargs)
        self.desc = "Master"

