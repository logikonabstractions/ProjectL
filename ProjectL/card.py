import numpy as np
from ProjectL.pieces import PieceSquare



class Reward:
    """
        Describes what we get for finishing a card. Points and/or a piece
    """
    def __init__(self, points = 0, piece = None):
        self.points = points
        self.piece = piece if piece else PieceSquare()

class Card:
    """ Describes the different cards we can play with. 
    
        layout: the numpy array that describes the state of the card (1 = occupied, 0 = empty for each square)
        reward: the object that describes what piece / points we get for completing the card 
        mask: a bool numpy array that describes the playable structure of that card within the maximal matrix
    """

    # def __init__(self, layout = np.zeros(shape=(5, 5), dtype=int), mask= None, reward = Reward()):
    def __init__(self, configs = None):
        if configs:
            self.layout = np.zeros(shape=(5, 5), dtype=int)
            self.mask = configs["mask"]
            self.reward = Reward(points=configs["reward"]["points"], piece=configs["reward"]["piece"])
        else:
            self.layout = np.zeros(shape=(5, 5), dtype=int)
            self.mask = None
            self.reward = Reward()
        
    def place_piece(self, piece, configuration):
        #TODO: determine how the placement at the position will be described. Ideas: 
        
        """ 
            places the provided piece on the card at a given position. returns T/F for success
            piece: a Piece object to be placed on the current card
            configuration: a description of where on the card to place the piece
        """
        
        return False
    
    
    def placement_valid(self, piece, configuration):
        """ checks if the placement of the piece on this card is valid. conditions: 
            - no position on self.layout > 1 after self.layout += configuration
            - no bit of configuration falls on a region where the mask is false
        
        """
    


