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
    def __init__(self, piece=None, card=None, pieces = None, cards=None):
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
        """
        pass

    def __str__(self):
        return self.desc

class TakePiece(Action):
    def __init__(self, piece=None, card=None, pieces = None, **kwargs):
        super().__init__(piece, card, pieces, **kwargs)
        self.desc = "Take a Piece"
        
    def perform_action(self):
        """ selects an available piece and returns it
        """
        
        # choose a piece, for now only Square pieces
        piece = PieceSquare()
        self.pieces.append(piece)

    def is_action_valid(self):
        """ This action is always valid we return True all the time
            :return: True
        """
        return True


class PlacePiece(Action):
    def __init__(self, piece=None, card=None, pieces = None, **kwargs):
        super().__init__(piece, card, pieces, **kwargs)
        self.desc = "Place a piece"


    def perform_action(self, configuration=None):
        """
            
        """
        if configuration is None:
            config_no = random.randint(0,self.piece.cube.shape[0]-1)
            configuration = self.piece.cube[config_no,:,:]
        if self.is_action_valid():
            result = self.card.place_piece(configuration)
            return result
        else:
            return False
    
    def is_action_valid(self):
        """ must have a piece and a card that is not full
        """
        if self.piece is None:
            # randomly select a piece to be placed as none provided
            if self.pieces:
                self.piece = random.choice(self.pieces)
            else:
                return False        # cannot place a piece if we have none
        if self.card is None:
            # same
            if self.cards:
                self.card = random.choice(self.cards)
            else:
                return False
        return self.card is not None and self.piece is not None
        
class UpgradePiece(Action):
    def __init__(self, piece=None, card=None, pieces = None, **kwargs):
        super().__init__(piece, card, pieces, **kwargs)
        self.desc = "Upgrade a piece"
        if self.piece is None:
            self.piece = random.choice(self.pieces)


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
        """ checks if we can take a card. This action is always valid we return True all the time
            :return: True
        """
    
        #TODO: check this
        if len(self.cards) >= 1:
            return False
    
        return True


class Master(Action):
    def __init__(self, piece=None, card=None, pieces = None, **kwargs):
        super().__init__(piece, card, pieces, **kwargs)
        self.desc = "Master"

